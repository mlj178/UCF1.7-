// ============================================================
// AAAAA-healthbar_prefab_probe_min.js
//
// feature_id: "healthbar_prefab_probe"
// 目标：默认只读验证墓碑出现前 HUD_HealthBar Prefab、Image、Sprite、Material；
//       仅在用户显式请求时，在主线程主动创建/回收一个测试血条。
//
// 静态调用链：
//   HUD_Tombstone.this+0x0C (otherBarPrefab)
//     -> HUD_ProjectionID.GetSign(prefab)
//     -> NameKeyPool.Get(prefab)
//
// 约束：
//   - RPC 线程只排队动作，不直接调用 Unity/IL2CPP 游戏方法。
//   - Unity API 和主动测试只在 HUD_Tombstone.Update 的游戏主线程 Hook 中调用。
//   - 所有对象仅用于当前 generation 的诊断，不跨房间长期信任。
// ============================================================

(function () {
    "use strict";

    var MODULE_NAME = "GameAssembly.dll";
    var CALL_CONV = "mscdecl";

    var RVA = {
        HUD_ProjectionID_Awake: 0x00AD9910,
        HUD_ProjectionID_GetSign: 0x00AD9980,
        HUD_Tombstone_AddHealthBar: 0x00AE1210,
        HUD_Tombstone_Update: 0x00AE18C0,
        SentryGun_AddHealthBar: 0x00B1C8C0,
        GameObject_GetComponent_Type: 0x00331C10,
        Object_GetInstanceID: 0x004E96C0,
        Object_get_name: 0x004EA1B0,
        GameObject_get_activeInHierarchy: 0x00331F20,
        GameObject_get_activeSelf: 0x00331F50,
        HUD_HealthBar_Bind: 0x00B07290,
        RecyclableObject_Active: 0x00B1A500,
        HUD_ProjectionSign_Recycle: 0x00AD9AD0,
        Player_get_isMyPlayer: 0x00B55FD0,
        Entity_get_isDead: 0x00B400E0,
        Singleton_GameManager_get_instance: 0x004A8170,
        SingletonGameManager_get_instance_Method: 0x00E1CE64,
        GameManager_TypeInfo: 0x00E2933C
    };

    var OFF = {
        UnityObject_m_CachedPtr: 0x08,
        HUD_Tombstone_otherBarPrefab: 0x0C,
        HUD_HealthBar_entityName: 0x50,
        HUD_HealthBar_bar: 0x54,
        HUD_HealthBar_health: 0x58,
        Graphic_m_Material: 0x0C,
        Image_m_Sprite: 0x80,
        Image_m_OverrideSprite: 0x84,
        GameManager_allPlayers: 0x1C,
        Entity_healthData: 0x1C,
        Il2CppArray_length: 0x0C,
        Il2CppArray_items: 0x10
    };

    var Runtime = {
        feature_id: "healthbar_prefab_probe",
        enabled: false,
        initialized: false,
        generation: 0,
        pendingAction: "",
        activeTestBar: ptr(0),
        activeTestTarget: ptr(0),
        activeTestGeneration: 0,
        hooks: [],
        timers: [],
        config: {
            sample_interval_ms: 2000,
            log_unchanged_every_ms: 15000
        },
        cache: {
            hudTombstone: ptr(0),
            hudProjectionID: ptr(0),
            prefab: ptr(0),
            healthBar: ptr(0),
            image: ptr(0)
        },
        stats: {
            updateHits: 0,
            samples: 0,
            changes: 0,
            timelineEvents: 0,
            errorCount: 0,
            cleanupCount: 0,
            resetCount: 0,
            lastError: "",
            lastResetReason: "",
            lastSampleAt: 0,
            lastChangeAt: 0,
            activeTestRequests: 0,
            activeTestCreated: 0,
            activeTestRecycled: 0,
            activeTestRejected: 0
        },
        lastSnapshot: null,
        lastSignature: "",
        lastUnchangedLogAt: 0,
        forceDump: false
    };

    var native = {
        ready: false,
        module: null,
        objectGetName: null,
        objectGetInstanceID: null,
        gameObjectGetActiveSelf: null,
        gameObjectGetActiveInHierarchy: null,
        gameObjectGetComponentType: null,
        hudProjectionGetSign: null,
        hudHealthBarBind: null,
        recyclableObjectActive: null,
        hudProjectionSignRecycle: null,
        playerGetIsMyPlayer: null,
        entityGetIsDead: null,
        singletonGameManagerGetInstance: null,
        il2cppDomainGet: null,
        il2cppDomainGetAssemblies: null,
        il2cppAssemblyGetImage: null,
        il2cppClassFromName: null,
        il2cppClassGetType: null,
        il2cppTypeGetObject: null,
        hudHealthBarClass: ptr(0),
        hudHealthBarSystemType: ptr(0)
    };

    var LogLimiter = {};

    function log(level, category, message, data) {
        var prefix = "[" + Runtime.feature_id + "][" + category + "] ";
        var text = prefix + message;
        if (level === "error") console.error(text);
        else if (level === "warn") console.warn(text);
        else console.log(text);
        try {
            send({
                type: "log",
                level: level,
                category: category,
                message: message,
                data: data || null
            });
        } catch (e) {}
    }

    function logOnce(key, level, category, message, intervalMs) {
        var now = Date.now();
        var wait = intervalMs || 1500;
        if (!LogLimiter[key] || now - LogLimiter[key] >= wait) {
            LogLimiter[key] = now;
            log(level, category, message);
        }
    }

    function setError(context, error) {
        var detail = context + (error ? ": " + error.message : "");
        Runtime.stats.errorCount += 1;
        Runtime.stats.lastError = detail;
        logOnce("error:" + context, "error", "ERROR", detail, 2000);
    }

    function isNull(value) {
        return !value || value.isNull();
    }

    function ptrText(value) {
        return isNull(value) ? "0x0" : value.toString();
    }

    function safeReadPointer(base, offset) {
        try {
            if (isNull(base)) return ptr(0);
            return base.add(offset || 0).readPointer();
        } catch (e) {
            return ptr(0);
        }
    }

    function isReadable(value) {
        try {
            if (isNull(value)) return false;
            value.readPointer();
            return true;
        } catch (e) {
            return false;
        }
    }

    function readManagedString(value) {
        try {
            if (!isReadable(value)) return "";
            var length = value.add(0x08).readS32();
            if (length < 0 || length > 4096) return "";
            return value.add(0x0C).readUtf16String(length) || "";
        } catch (e) {
            return "";
        }
    }

    function readClassName(obj) {
        try {
            var klass = safeReadPointer(obj, 0);
            var namePtr = safeReadPointer(klass, 0x08);
            if (isNull(namePtr)) return "";
            return namePtr.readCString() || "";
        } catch (e) {
            return "";
        }
    }

    function objectInfo(obj, kind) {
        var result = {
            kind: kind || "Object",
            ptr: ptrText(obj),
            className: readClassName(obj),
            cachedPtr: "0x0",
            validManaged: isReadable(obj),
            validNative: false,
            instanceID: null,
            name: ""
        };

        if (!result.validManaged) return result;

        try {
            var cached = safeReadPointer(obj, OFF.UnityObject_m_CachedPtr);
            result.cachedPtr = ptrText(cached);
            result.validNative = !isNull(cached);
            if (!result.validNative || !native.ready) return result;
            result.instanceID = native.objectGetInstanceID(obj, ptr(0));
            result.name = readManagedString(native.objectGetName(obj, ptr(0)));
        } catch (error) {
            result.apiError = error.message;
        }
        return result;
    }

    function rawObjectInfo(obj, kind) {
        return {
            kind: kind || "Object",
            ptr: ptrText(obj),
            className: readClassName(obj),
            cachedPtr: ptrText(safeReadPointer(obj, OFF.UnityObject_m_CachedPtr)),
            readable: isReadable(obj)
        };
    }

    function gameObjectInfo(obj, kind) {
        var result = objectInfo(obj, kind || "GameObject");
        result.activeSelf = null;
        result.activeInHierarchy = null;
        if (!result.validNative || !native.ready) return result;
        try {
            result.activeSelf = !!native.gameObjectGetActiveSelf(obj, ptr(0));
            result.activeInHierarchy = !!native.gameObjectGetActiveInHierarchy(obj, ptr(0));
        } catch (error) {
            result.activeError = error.message;
        }
        return result;
    }

    function getExport(name) {
        var mod = native.module || Process.findModuleByName(MODULE_NAME);
        var address = mod ? mod.findExportByName(name) : null;
        if (!address) throw new Error("missing export " + name);
        return address;
    }

    function findClass(namespaceName, className) {
        var domain = native.il2cppDomainGet();
        if (isNull(domain)) return ptr(0);
        var sizePtr = Memory.alloc(Process.pointerSize);
        sizePtr.writeU32(0);
        var assemblies = native.il2cppDomainGetAssemblies(domain, sizePtr);
        var count = sizePtr.readU32();
        for (var index = 0; index < count; index++) {
            var assembly = assemblies.add(index * Process.pointerSize).readPointer();
            if (isNull(assembly)) continue;
            var image = native.il2cppAssemblyGetImage(assembly);
            if (isNull(image)) continue;
            var klass = native.il2cppClassFromName(image, namespaceName, className);
            if (!isNull(klass)) return klass;
        }
        return ptr(0);
    }

    function initNativeFunctions() {
        if (native.ready) return true;
        var mod = Process.findModuleByName(MODULE_NAME);
        if (!mod) {
            Runtime.stats.lastError = MODULE_NAME + " not found";
            return false;
        }
        if (Process.arch !== "ia32" || Process.pointerSize !== 4) {
            Runtime.stats.lastError = "unsupported target: arch=" + Process.arch + ", pointerSize=" + Process.pointerSize;
            log("error", "INIT", Runtime.stats.lastError);
            return false;
        }

        try {
            native.module = mod;
            native.objectGetName = new NativeFunction(mod.base.add(RVA.Object_get_name), "pointer", ["pointer", "pointer"], CALL_CONV);
            native.objectGetInstanceID = new NativeFunction(mod.base.add(RVA.Object_GetInstanceID), "int", ["pointer", "pointer"], CALL_CONV);
            native.gameObjectGetActiveSelf = new NativeFunction(mod.base.add(RVA.GameObject_get_activeSelf), "bool", ["pointer", "pointer"], CALL_CONV);
            native.gameObjectGetActiveInHierarchy = new NativeFunction(mod.base.add(RVA.GameObject_get_activeInHierarchy), "bool", ["pointer", "pointer"], CALL_CONV);
            native.gameObjectGetComponentType = new NativeFunction(mod.base.add(RVA.GameObject_GetComponent_Type), "pointer", ["pointer", "pointer", "pointer"], CALL_CONV);
            native.hudProjectionGetSign = new NativeFunction(mod.base.add(RVA.HUD_ProjectionID_GetSign), "pointer", ["pointer", "pointer"], CALL_CONV);
            native.hudHealthBarBind = new NativeFunction(mod.base.add(RVA.HUD_HealthBar_Bind), "void", ["pointer", "pointer", "pointer"], CALL_CONV);
            native.recyclableObjectActive = new NativeFunction(mod.base.add(RVA.RecyclableObject_Active), "void", ["pointer", "pointer"], CALL_CONV);
            native.hudProjectionSignRecycle = new NativeFunction(mod.base.add(RVA.HUD_ProjectionSign_Recycle), "void", ["pointer", "bool", "pointer"], CALL_CONV);
            native.playerGetIsMyPlayer = new NativeFunction(mod.base.add(RVA.Player_get_isMyPlayer), "bool", ["pointer", "pointer"], CALL_CONV);
            native.entityGetIsDead = new NativeFunction(mod.base.add(RVA.Entity_get_isDead), "bool", ["pointer", "pointer"], CALL_CONV);
            native.singletonGameManagerGetInstance = new NativeFunction(mod.base.add(RVA.Singleton_GameManager_get_instance), "pointer", ["pointer"], CALL_CONV);

            native.il2cppDomainGet = new NativeFunction(getExport("il2cpp_domain_get"), "pointer", [], CALL_CONV);
            native.il2cppDomainGetAssemblies = new NativeFunction(getExport("il2cpp_domain_get_assemblies"), "pointer", ["pointer", "pointer"], CALL_CONV);
            native.il2cppAssemblyGetImage = new NativeFunction(getExport("il2cpp_assembly_get_image"), "pointer", ["pointer"], CALL_CONV);
            native.il2cppClassFromName = new NativeFunction(getExport("il2cpp_class_from_name"), "pointer", ["pointer", "pointer", "pointer"], CALL_CONV);
            native.il2cppClassGetType = new NativeFunction(getExport("il2cpp_class_get_type"), "pointer", ["pointer"], CALL_CONV);
            native.il2cppTypeGetObject = new NativeFunction(getExport("il2cpp_type_get_object"), "pointer", ["pointer"], CALL_CONV);

            var ns = Memory.allocUtf8String("");
            var name = Memory.allocUtf8String("HUD_HealthBar");
            native.hudHealthBarClass = findClass(ns, name);
            if (isNull(native.hudHealthBarClass)) throw new Error("HUD_HealthBar class not found");
            var il2cppType = native.il2cppClassGetType(native.hudHealthBarClass);
            native.hudHealthBarSystemType = native.il2cppTypeGetObject(il2cppType);
            if (isNull(native.hudHealthBarSystemType)) throw new Error("HUD_HealthBar System.Type not found");

            native.ready = true;
            log("info", "INIT", "native/type resolution ready; HUD_HealthBar klass=" + ptrText(native.hudHealthBarClass));
            return true;
        } catch (error) {
            setError("initNativeFunctions failed", error);
            native.ready = false;
            return false;
        }
    }

    function describeImage(image) {
        var info = objectInfo(image, "Image");
        var material = safeReadPointer(image, OFF.Graphic_m_Material);
        var sprite = safeReadPointer(image, OFF.Image_m_Sprite);
        var overrideSprite = safeReadPointer(image, OFF.Image_m_OverrideSprite);
        info.material = objectInfo(material, "Material");
        info.sprite = objectInfo(sprite, "Sprite");
        info.overrideSprite = objectInfo(overrideSprite, "OverrideSprite");
        info.hasUsableGraphicResource = !!(
            info.sprite.validNative || info.overrideSprite.validNative || info.material.validNative
        );
        return info;
    }

    function describeHealthBar(component) {
        var info = objectInfo(component, "HUD_HealthBar");
        var entityName = safeReadPointer(component, OFF.HUD_HealthBar_entityName);
        var image = safeReadPointer(component, OFF.HUD_HealthBar_bar);
        var health = safeReadPointer(component, OFF.HUD_HealthBar_health);
        info.entityName = objectInfo(entityName, "Text");
        info.bar = describeImage(image);
        info.health = {
            ptr: ptrText(health),
            className: readClassName(health),
            readable: isReadable(health)
        };
        return info;
    }

    function snapshotSignature(snapshot) {
        var healthBar = snapshot.healthBar || {};
        var bar = healthBar.bar || {};
        return JSON.stringify({
            hud: snapshot.hudTombstone.ptr,
            prefab: snapshot.prefab.ptr,
            prefabNative: snapshot.prefab.cachedPtr,
            healthBar: healthBar.ptr || "0x0",
            image: bar.ptr || "0x0",
            imageNative: bar.cachedPtr || "0x0",
            sprite: bar.sprite ? bar.sprite.ptr : "0x0",
            spriteNative: bar.sprite ? bar.sprite.cachedPtr : "0x0",
            overrideSprite: bar.overrideSprite ? bar.overrideSprite.ptr : "0x0",
            material: bar.material ? bar.material.ptr : "0x0"
        });
    }

    function inspectHudTombstone(hudTombstone, reason) {
        var now = Date.now();
        var previousHud = Runtime.cache.hudTombstone;
        if (isNull(previousHud) || !previousHud.equals(hudTombstone)) {
            if (!isNull(Runtime.activeTestBar)) {
                log("warn", "ACTIVE_TEST_STALE", "HUD generation changed; dropping old test-bar handle without cross-scene call");
                Runtime.activeTestBar = ptr(0);
                Runtime.activeTestTarget = ptr(0);
                Runtime.activeTestGeneration = 0;
            }
            Runtime.generation += 1;
            Runtime.cache.hudTombstone = hudTombstone;
            Runtime.lastSignature = "";
            log("info", "LIFECYCLE", "HUD_Tombstone changed; generation=" + Runtime.generation + ", this=" + ptrText(hudTombstone));
        }

        var prefab = safeReadPointer(hudTombstone, OFF.HUD_Tombstone_otherBarPrefab);
        var prefabInfo = gameObjectInfo(prefab, "otherBarPrefab");
        var healthBar = ptr(0);
        var componentError = "";
        if (prefabInfo.validNative && native.ready) {
            try {
                healthBar = native.gameObjectGetComponentType(prefab, native.hudHealthBarSystemType, ptr(0));
            } catch (error) {
                componentError = error.message;
                setError("GameObject.GetComponent(HUD_HealthBar) failed", error);
            }
        }

        var snapshot = {
            timestamp: new Date(now).toISOString(),
            reason: reason || "periodic",
            generation: Runtime.generation,
            threadId: Process.getCurrentThreadId(),
            hudTombstone: {
                ptr: ptrText(hudTombstone),
                className: readClassName(hudTombstone),
                readable: isReadable(hudTombstone)
            },
            prefab: prefabInfo,
            healthBar: describeHealthBar(healthBar),
            componentError: componentError
        };

        snapshot.conclusion = {
            prefabReady: snapshot.prefab.validNative,
            componentReady: snapshot.healthBar.validNative,
            imageReady: snapshot.healthBar.bar.validNative,
            spriteReady: snapshot.healthBar.bar.sprite.validNative || snapshot.healthBar.bar.overrideSprite.validNative,
            materialReady: snapshot.healthBar.bar.material.validNative,
            completeOriginalBar: snapshot.prefab.validNative && snapshot.healthBar.validNative &&
                snapshot.healthBar.bar.validNative &&
                (snapshot.healthBar.bar.sprite.validNative || snapshot.healthBar.bar.overrideSprite.validNative)
        };

        Runtime.cache.prefab = prefab;
        Runtime.cache.healthBar = healthBar;
        Runtime.cache.image = safeReadPointer(healthBar, OFF.HUD_HealthBar_bar);
        Runtime.stats.samples += 1;
        Runtime.stats.lastSampleAt = now;
        Runtime.lastSnapshot = snapshot;

        var signature = snapshotSignature(snapshot);
        var changed = signature !== Runtime.lastSignature;
        if (changed || Runtime.forceDump) {
            Runtime.stats.changes += changed ? 1 : 0;
            Runtime.stats.lastChangeAt = changed ? now : Runtime.stats.lastChangeAt;
            Runtime.lastSignature = signature;
            Runtime.forceDump = false;
            log("info", "PREFAB_SNAPSHOT", JSON.stringify(snapshot), snapshot);
        } else if (now - Runtime.lastUnchangedLogAt >= Runtime.config.log_unchanged_every_ms) {
            Runtime.lastUnchangedLogAt = now;
            log("info", "PREFAB_UNCHANGED", "generation=" + Runtime.generation + ", conclusion=" + JSON.stringify(snapshot.conclusion));
        }
        return snapshot;
    }

    function shouldSample() {
        if (!Runtime.enabled) return false;
        if (Runtime.forceDump) return true;
        return Date.now() - Runtime.stats.lastSampleAt >= Runtime.config.sample_interval_ms;
    }

    function addTimeline(eventName, detail) {
        Runtime.stats.timelineEvents += 1;
        log("info", "TIMELINE", eventName + " " + JSON.stringify(detail || {}), detail || null);
    }

    function rejectActiveTest(reason, detail) {
        Runtime.stats.activeTestRejected += 1;
        Runtime.stats.lastError = reason;
        log("warn", "ACTIVE_TEST_REJECTED", reason, detail || null);
    }

    function getGameManager() {
        try {
            var methodInfo = native.module.base.add(RVA.SingletonGameManager_get_instance_Method).readPointer();
            if (!isReadable(methodInfo)) return ptr(0);
            return native.singletonGameManagerGetInstance(methodInfo);
        } catch (error) {
            setError("Singleton<GameManager>.get_instance failed", error);
            return ptr(0);
        }
    }

    function findVisibleTargetPlayer() {
        var manager = getGameManager();
        if (!isReadable(manager)) return null;
        var players = safeReadPointer(manager, OFF.GameManager_allPlayers);
        if (!isReadable(players)) return null;
        try {
            var count = players.add(OFF.Il2CppArray_length).readU32();
            if (count > 64) count = 64;
            for (var index = 0; index < count; index += 1) {
                var player = players.add(OFF.Il2CppArray_items + index * Process.pointerSize).readPointer();
                if (!isReadable(player) || isNull(safeReadPointer(player, OFF.UnityObject_m_CachedPtr))) continue;
                if (native.playerGetIsMyPlayer(player, ptr(0))) continue;
                if (native.entityGetIsDead(player, ptr(0))) continue;
                var health = safeReadPointer(player, OFF.Entity_healthData);
                if (!isReadable(health)) continue;
                return { player: player, health: health, index: index };
            }
        } catch (error) {
            setError("GameManager.allPlayers scan failed", error);
        }
        return null;
    }

    function createActiveTestBar(hudTombstone) {
        if (!isNull(Runtime.activeTestBar)) {
            rejectActiveTest("a test health bar is already active; recycle it first");
            return;
        }
        var prefab = safeReadPointer(hudTombstone, OFF.HUD_Tombstone_otherBarPrefab);
        var prefabInfo = gameObjectInfo(prefab, "activeTest.prefab");
        if (!prefabInfo.validNative) {
            rejectActiveTest("otherBarPrefab is not a valid Unity object", prefabInfo);
            return;
        }
        var targetInfo = findVisibleTargetPlayer();
        if (!targetInfo) {
            rejectActiveTest("no live non-local player is available");
            return;
        }
        var healthBar = ptr(0);
        try {
            healthBar = native.hudProjectionGetSign(prefab, ptr(0));
            if (!isReadable(healthBar) || readClassName(healthBar) !== "HUD_HealthBar") {
                rejectActiveTest("GetSign did not return HUD_HealthBar", rawObjectInfo(healthBar, "GetSign.result"));
                return;
            }
            native.hudHealthBarBind(healthBar, targetInfo.player, ptr(0));
            var boundHealth = safeReadPointer(healthBar, OFF.HUD_HealthBar_health);
            if (isNull(boundHealth) || !boundHealth.equals(targetInfo.health)) {
                native.hudProjectionSignRecycle(healthBar, false, ptr(0));
                rejectActiveTest("HUD_HealthBar.Bind did not retain the target HealthData", {
                    expected: ptrText(targetInfo.health),
                    actual: ptrText(boundHealth)
                });
                return;
            }
            native.recyclableObjectActive(healthBar, ptr(0));
            Runtime.activeTestBar = healthBar;
            Runtime.activeTestTarget = targetInfo.player;
            Runtime.activeTestGeneration = Runtime.generation;
            Runtime.stats.activeTestCreated += 1;
            var detail = {
                generation: Runtime.generation,
                threadId: Process.getCurrentThreadId(),
                playerIndex: targetInfo.index,
                target: objectInfo(targetInfo.player, "Player"),
                expectedHealth: ptrText(targetInfo.health),
                healthBar: describeHealthBar(healthBar)
            };
            log("info", "ACTIVE_TEST_CREATED", JSON.stringify(detail), detail);
        } catch (error) {
            if (!isNull(healthBar)) {
                try { native.hudProjectionSignRecycle(healthBar, false, ptr(0)); } catch (_) {}
            }
            setError("active test create failed", error);
            rejectActiveTest("native create/bind/active call failed", { error: error.message });
        }
    }

    function recycleActiveTestBar() {
        if (isNull(Runtime.activeTestBar)) {
            rejectActiveTest("no active test health bar to recycle");
            return;
        }
        if (Runtime.activeTestGeneration !== Runtime.generation) {
            Runtime.activeTestBar = ptr(0);
            Runtime.activeTestTarget = ptr(0);
            Runtime.activeTestGeneration = 0;
            rejectActiveTest("test health bar belongs to an old HUD generation; handle discarded");
            return;
        }
        var recycled = Runtime.activeTestBar;
        try {
            native.hudProjectionSignRecycle(recycled, false, ptr(0));
            Runtime.stats.activeTestRecycled += 1;
            log("info", "ACTIVE_TEST_RECYCLED", "recycled=" + ptrText(recycled));
            Runtime.activeTestBar = ptr(0);
            Runtime.activeTestTarget = ptr(0);
            Runtime.activeTestGeneration = 0;
        } catch (error) {
            setError("active test recycle failed", error);
        }
    }

    function consumePendingAction(hudTombstone) {
        var action = Runtime.pendingAction;
        if (!action) return;
        Runtime.pendingAction = "";
        inspectHudTombstone(hudTombstone, "active_test_preflight");
        if (action === "create") createActiveTestBar(hudTombstone);
        else if (action === "recycle") recycleActiveTestBar();
    }

    function requestActiveTest(action) {
        if (!Runtime.enabled || !Runtime.initialized) {
            rejectActiveTest("probe is not enabled");
            return buildStatus();
        }
        if (Runtime.pendingAction) {
            rejectActiveTest("another active-test action is already pending");
            return buildStatus();
        }
        Runtime.pendingAction = action;
        Runtime.stats.activeTestRequests += 1;
        log("info", "ACTIVE_TEST_REQUESTED", "queued=" + action + "; waiting for HUD_Tombstone.Update main thread");
        return buildStatus();
    }

    function attachHook(address, callbacks, name) {
        var handle = Interceptor.attach(address, callbacks);
        Runtime.hooks.push(handle);
        log("info", "HOOK", name + " installed @ " + address);
    }

    function installHudTombstoneUpdateHook() {
        var address = native.module.base.add(RVA.HUD_Tombstone_Update);
        attachHook(address, {
            onEnter: function (args) {
                Runtime.stats.updateHits += 1;
                if (Runtime.pendingAction) {
                    try { consumePendingAction(args[0]); }
                    catch (error) { setError("consumePendingAction failed", error); }
                }
                if (!shouldSample()) return;
                try {
                    inspectHudTombstone(args[0], Runtime.forceDump ? "manual_request" : "HUD_Tombstone.Update");
                } catch (error) {
                    setError("inspectHudTombstone failed", error);
                }
            }
        }, "HUD_Tombstone.Update");
    }

    function installTimelineHooks() {
        attachHook(native.module.base.add(RVA.HUD_ProjectionID_Awake), {
            onEnter: function (args) {
                this.probeEnabled = Runtime.enabled;
                this.instance = args[0];
            },
            onLeave: function () {
                if (!this.probeEnabled || !Runtime.enabled) return;
                Runtime.cache.hudProjectionID = this.instance;
                addTimeline("HUD_ProjectionID.Awake", { instance: ptrText(this.instance) });
            }
        }, "HUD_ProjectionID.Awake");

        attachHook(native.module.base.add(RVA.HUD_ProjectionID_GetSign), {
            onEnter: function (args) {
                this.probeEnabled = Runtime.enabled;
                this.prefab = args[0];
            },
            onLeave: function (retval) {
                if (!this.probeEnabled || !Runtime.enabled) return;
                addTimeline("HUD_ProjectionID.GetSign", {
                    prefab: rawObjectInfo(this.prefab, "GetSign.prefab"),
                    result: rawObjectInfo(retval, "RecyclableObject")
                });
            }
        }, "HUD_ProjectionID.GetSign");

        attachHook(native.module.base.add(RVA.HUD_Tombstone_AddHealthBar), {
            onEnter: function (args) {
                this.probeEnabled = Runtime.enabled;
                this.tomb = args[0];
            },
            onLeave: function (retval) {
                if (!this.probeEnabled || !Runtime.enabled) return;
                addTimeline("HUD_Tombstone.AddHealthBar", {
                    tomb: ptrText(this.tomb),
                    result: rawObjectInfo(retval, "HUD_HealthBar")
                });
                Runtime.forceDump = true;
            }
        }, "HUD_Tombstone.AddHealthBar");

        attachHook(native.module.base.add(RVA.SentryGun_AddHealthBar), {
            onEnter: function (args) {
                if (!Runtime.enabled) return;
                addTimeline("SentryGun.AddHealthBar", { sentryGun: ptrText(args[0]) });
                Runtime.forceDump = true;
            }
        }, "SentryGun.AddHealthBar");
    }

    function startWatchdog() {
        var timerId = setInterval(function () {
            if (!Runtime.enabled) return;
            if (Runtime.stats.updateHits === 0) {
                log("warn", "WATCHDOG", "HUD_Tombstone.Update 尚未命中；当前场景可能未激活该 HUD 组件");
            } else {
                log("info", "WATCHDOG", "Update命中=" + Runtime.stats.updateHits + ", 采样=" + Runtime.stats.samples + ", generation=" + Runtime.generation);
            }
        }, 10000);
        Runtime.timers.push(timerId);
    }

    function installHooks() {
        if (Runtime.initialized) return true;
        if (!initNativeFunctions()) return false;
        try {
            installHudTombstoneUpdateHook();
            installTimelineHooks();
            startWatchdog();
            Runtime.initialized = true;
            log("info", "INIT", "all read-only hooks installed");
            return true;
        } catch (error) {
            setError("installHooks failed", error);
            cleanupHooks();
            return false;
        }
    }

    function cleanupHooks() {
        for (var index = 0; index < Runtime.hooks.length; index++) {
            try { Runtime.hooks[index].detach(); } catch (e) {}
        }
        Runtime.hooks = [];
        Runtime.initialized = false;
    }

    function cleanupTimers() {
        for (var index = 0; index < Runtime.timers.length; index++) {
            try { clearInterval(Runtime.timers[index]); } catch (e) {}
        }
        Runtime.timers = [];
    }

    function resetRuntime(reason) {
        Runtime.generation += 1;
        Runtime.cache.hudTombstone = ptr(0);
        Runtime.cache.hudProjectionID = ptr(0);
        Runtime.cache.prefab = ptr(0);
        Runtime.cache.healthBar = ptr(0);
        Runtime.cache.image = ptr(0);
        Runtime.lastSnapshot = null;
        Runtime.lastSignature = "";
        Runtime.forceDump = false;
        Runtime.pendingAction = "";
        Runtime.activeTestBar = ptr(0);
        Runtime.activeTestTarget = ptr(0);
        Runtime.activeTestGeneration = 0;
        Runtime.stats.resetCount += 1;
        Runtime.stats.lastResetReason = reason || "unknown";
        log("info", "LIFECYCLE", "resetRuntime: " + Runtime.stats.lastResetReason + ", generation=" + Runtime.generation);
    }

    function enableFeature() {
        if (!installHooks()) return false;
        Runtime.enabled = true;
        Runtime.forceDump = true;
        Runtime.stats.lastError = "";
        log("info", "LIFECYCLE", "enabled; waiting for HUD_Tombstone.Update main-thread sample");
        return true;
    }

    function disableFeature() {
        Runtime.enabled = false;
        Runtime.forceDump = false;
        log("info", "LIFECYCLE", "disabled; hooks remain inert");
        return true;
    }

    function cleanupFeature() {
        Runtime.enabled = false;
        Runtime.stats.cleanupCount += 1;
        cleanupTimers();
        cleanupHooks();
        resetRuntime("cleanup");
        log("info", "LIFECYCLE", "cleanup done");
        return true;
    }

    function setConfig(config) {
        var next = config || {};
        if (next.sample_interval_ms !== undefined) {
            Runtime.config.sample_interval_ms = Math.max(250, Number(next.sample_interval_ms) || 2000);
        }
        if (next.log_unchanged_every_ms !== undefined) {
            Runtime.config.log_unchanged_every_ms = Math.max(2000, Number(next.log_unchanged_every_ms) || 15000);
        }
        return Runtime.config;
    }

    function buildStatus() {
        return {
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            generation: Runtime.generation,
            native_ready: native.ready,
            force_dump_pending: Runtime.forceDump,
            pending_action: Runtime.pendingAction,
            active_test: {
                healthBar: ptrText(Runtime.activeTestBar),
                target: ptrText(Runtime.activeTestTarget),
                generation: Runtime.activeTestGeneration
            },
            config: Runtime.config,
            cache: {
                hudTombstone: ptrText(Runtime.cache.hudTombstone),
                hudProjectionID: ptrText(Runtime.cache.hudProjectionID),
                prefab: ptrText(Runtime.cache.prefab),
                healthBar: ptrText(Runtime.cache.healthBar),
                image: ptrText(Runtime.cache.image)
            },
            stats: Runtime.stats,
            snapshot: Runtime.lastSnapshot
        };
    }

    rpc.exports = {
        enable() { return enableFeature(); },
        disable() { return disableFeature(); },
        status() { return buildStatus(); },
        cleanup() { return cleanupFeature(); },
        setConfig(config) { return setConfig(config); },
        setconfig(config) { return setConfig(config); },
        reset(reason) { resetRuntime(reason || "manual"); return true; },
        createTestBar() { return requestActiveTest("create"); },
        createtestbar() { return requestActiveTest("create"); },
        recycleTestBar() { return requestActiveTest("recycle"); },
        recycletestbar() { return requestActiveTest("recycle"); },
        debugDump() { Runtime.forceDump = true; return buildStatus(); },
        debugdump() { Runtime.forceDump = true; return buildStatus(); }
    };
})();
