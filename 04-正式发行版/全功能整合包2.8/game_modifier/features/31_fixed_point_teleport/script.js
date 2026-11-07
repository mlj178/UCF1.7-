// ============================================================
// AAAAA-fixed_point_teleport_min.js
//
// feature_id: "fixed_point_teleport"
// 功能目标：本地玩家保存一个定点，然后通过按钮瞬移回保存点。
//
// 实现原理：
//   1. 本地玩家主来源：直读 GameManager.myPlayer 静态字段（GameManager_TypeInfo + 0x5C + 0x0），
//      由 ModeBase.UpdateTimeUI 每帧刷新一次，不再逐个扫描 Player。
//   2. Player.Update 只做“快速通道”：args[0] 就是已缓存的本地玩家时才消费 pending，
//      其他人机/玩家在两次指针比较内直接返回（不进 isReadablePtr / isMyPlayer）。
//      仅在静态字段暂不可用时，才回退到 isMyPlayer 捕获。
//   3. savePoint 读取本地 Player 的 Transform.position 并保存为单个点。
//   4. teleportToPoint 调用原游戏 Player.SetPos(Vector3)，由原游戏处理碰撞器禁用/恢复。
//
// RVA / 字段来源：
//   Player_Update:                    0x00B551D0  dump.cs + IDA 汇编索引（快速通道 + 兜底捕获）
//   Player_get_isMyPlayer:            0x00B55FD0  dump.cs + 常用本地玩家判断点（仅兜底）
//   Player_SetPos:                    0x00B534C0  dump.cs + IDA 汇编确认会处理 Collider.enabled
//   Component_get_transform:          0x0032CF40  已有自由视角/穿墙功能验证
//   Transform_get_position_Injected:  0x003F4280  已有自由视角/穿墙功能验证
//   ModeBase_UpdateTimeUI:            0x00AF6930  全模式通用模式实例触发点（每帧刷新本地玩家 + 消费 pending）
//   GameManager_TypeInfo:             0x00E2933C  GameManager 静态字段区：static_fields@0x5C, myPlayer@0x0
//   GameManager_GameRoundEnd:         0x00AFAA40  任意模式回合结束
//   GameManager_NewGameRoundStart:    0x00AEBCB0  新回合开始
//   GameManager_OnDestroy:            0x00AEBD40  房间对象销毁/离开房间
//   Player_characterController:       0x2C        dump.cs 字段偏移，Player.SetPos 内部会读取
// ============================================================

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';

    var RVA = {
        Player_Update: 0x00B551D0,
        Player_get_isMyPlayer: 0x00B55FD0,
        Player_SetPos: 0x00B534C0,
        Component_get_transform: 0x0032CF40,
        Transform_get_position_Injected: 0x003F4280,
        ModeBase_UpdateTimeUI: 0x00AF6930,
        GameManager_TypeInfo: 0x00E2933C,
        GameManager_GameRoundEnd: 0x00AFAA40,
        GameManager_NewGameRoundStart: 0x00AEBCB0,
        GameManager_OnDestroy: 0x00AEBD40
    };

    var OFF = {
        Player_characterController: 0x2C,
        Il2CppClass_static_fields: 0x5C,
        GameManager_myPlayer: 0x00
    };

    var MAX_POINT_SLOTS = 2;

    var Runtime = {
        feature_id: "fixed_point_teleport",
        enabled: false,
        initialized: false,
        applied: false,
        pendingApply: false,
        lastApplyReason: "script_loaded",
        generation: 0,
        roomGeneration: 0,
        module: null,
        base: ptr(0),
        hooks: [],
        config: {
            require_enabled_for_actions: true,
            max_cached_player_age_ms: 3000
        },
        cache: {
            localPlayer: ptr(0),
            localPlayerSeenAt: 0,
            staticSource: false,
            modeBase: ptr(0)
        },
        savedPoints: {
            1: null,
            2: null
        },
        pending: {
            saveSlot: 0,
            teleportSlot: 0
        },
        stats: {
            hookHits: 0,
            localPlayerHits: 0,
            staticPlayerHits: 0,
            staticPlayerMiss: 0,
            modeBaseHits: 0,
            roundBoundaryCount: 0,
            saveCount: 0,
            teleportCount: 0,
            skippedNull: 0,
            skippedInvalid: 0,
            errorCount: 0,
            cleanupCount: 0,
            lastError: "",
            lastResetReason: "",
            lastRoomReason: "",
            lastSaveResult: "",
            lastTeleportResult: "",
            lastPointSource: ""
        }
    };

    var native = {
        ready: false,
        isMyPlayer: null,
        playerSetPos: null,
        componentGetTransform: null,
        transformGetPosition: null
    };

    var posBuffer = Memory.alloc(12);
    var LogLimiter = {};

    function log(level, message) {
        var text = "[" + Runtime.feature_id + "] " + message;
        if (level === 'error') console.error(text);
        else if (level === 'warn') console.warn(text);
        else console.log(text);
        try {
            send({ type: 'log', level: level, message: message });
        } catch (e) {}
    }

    function sendStatus(feature, enabled) {
        try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (_) {}
    }

    function logOnce(key, level, message, intervalMs) {
        var now = Date.now();
        var wait = intervalMs || 1000;
        if (!LogLimiter[key] || now - LogLimiter[key] >= wait) {
            LogLimiter[key] = now;
            log(level, message);
        }
    }

    function setError(message, error) {
        Runtime.stats.errorCount += 1;
        Runtime.stats.lastError = message + (error ? ": " + error.message : "");
        logOnce("error:" + message, "error", Runtime.stats.lastError, 1500);
    }

    function isNull(p) {
        return !p || p.isNull();
    }

    function isReadablePtr(p) {
        try {
            if (isNull(p)) return false;
            p.readPointer();
            return true;
        } catch (e) {
            return false;
        }
    }

    function readVector3(buffer) {
        var x = buffer.readFloat();
        var y = buffer.add(4).readFloat();
        var z = buffer.add(8).readFloat();
        if (!isFinite(x) || !isFinite(y) || !isFinite(z)) return null;
        return { x: x, y: y, z: z };
    }

    function normalizeSlot(slot) {
        var value = Number(slot) || 1;
        if (value < 1) return 1;
        if (value > MAX_POINT_SLOTS) return MAX_POINT_SLOTS;
        return Math.floor(value);
    }

    function resetSavedPointSlots() {
        for (var slot = 1; slot <= MAX_POINT_SLOTS; slot += 1) {
            Runtime.savedPoints[slot] = null;
        }
    }

    function clonePoint(point, slot) {
        if (!point) return null;
        return {
            x: Number(point.x),
            y: Number(point.y),
            z: Number(point.z),
            slot: normalizeSlot(slot),
            generation: Runtime.generation,
            room_generation: Runtime.roomGeneration,
            saved_at: Date.now()
        };
    }

    function formatPoint(point) {
        if (!point) return "(none)";
        return "(" + point.x.toFixed(3) + ", " + point.y.toFixed(3) + ", " + point.z.toFixed(3) + ")";
    }

    function initNativeFunctions() {
        if (native.ready) return true;

        Runtime.module = Process.findModuleByName(MODULE_NAME);
        if (!Runtime.module) {
            Runtime.stats.lastError = "GameAssembly.dll not found";
            return false;
        }

        Runtime.base = Runtime.module.base;
        if (Process.arch !== 'ia32' || Process.pointerSize !== 4) {
            Runtime.stats.lastError = "unsupported process: arch=" + Process.arch + ", pointerSize=" + Process.pointerSize;
            log("error", Runtime.stats.lastError);
            return false;
        }

        try {
            native.isMyPlayer = new NativeFunction(
                Runtime.base.add(RVA.Player_get_isMyPlayer),
                'bool',
                ['pointer', 'pointer'],
                CALL_CONV
            );
            native.playerSetPos = new NativeFunction(
                Runtime.base.add(RVA.Player_SetPos),
                'void',
                ['pointer', 'float', 'float', 'float', 'pointer'],
                CALL_CONV
            );
            native.componentGetTransform = new NativeFunction(
                Runtime.base.add(RVA.Component_get_transform),
                'pointer',
                ['pointer', 'pointer'],
                CALL_CONV
            );
            native.transformGetPosition = new NativeFunction(
                Runtime.base.add(RVA.Transform_get_position_Injected),
                'void',
                ['pointer', 'pointer', 'pointer'],
                CALL_CONV
            );
            native.ready = true;
            return true;
        } catch (error) {
            setError("initNativeFunctions failed", error);
            native.ready = false;
            return false;
        }
    }

    function cleanupHooks() {
        for (var i = 0; i < Runtime.hooks.length; i += 1) {
            try {
                if (Runtime.hooks[i] && Runtime.hooks[i].detach) Runtime.hooks[i].detach();
            } catch (e) {}
        }
        Runtime.hooks = [];
        Runtime.initialized = false;
    }

    function resetRuntime(reason) {
        Runtime.generation += 1;
        Runtime.cache.localPlayer = ptr(0);
        Runtime.cache.localPlayerSeenAt = 0;
        Runtime.cache.staticSource = false;
        Runtime.cache.modeBase = ptr(0);
        resetSavedPointSlots();
        Runtime.pending.saveSlot = 0;
        Runtime.pending.teleportSlot = 0;
        Runtime.applied = false;
        Runtime.pendingApply = Runtime.enabled;
        Runtime.lastApplyReason = reason || "runtime_reset";
        Runtime.stats.lastResetReason = reason || "unknown";
        log("info", "resetRuntime: " + Runtime.stats.lastResetReason + ", gen=" + Runtime.generation);
    }

    function clearPendingRoundActions(reason) {
        Runtime.pending.saveSlot = 0;
        Runtime.pending.teleportSlot = 0;
        log("info", "round pending actions cleared: " + (reason || "round_boundary"));
    }

    function handleRoundBoundary(reason, nextModeBase) {
        Runtime.roomGeneration += 1;
        Runtime.stats.roundBoundaryCount += 1;
        Runtime.stats.lastRoomReason = reason || "room_boundary";
        resetRuntime(Runtime.stats.lastRoomReason);
        if (!isNull(nextModeBase)) {
            Runtime.cache.modeBase = nextModeBase;
        }
        log("info", "room boundary: " + Runtime.stats.lastRoomReason + ", room_gen=" + Runtime.roomGeneration);
    }

    function handleModeBaseSeen(modeBase) {
        if (isNull(modeBase)) return;

        Runtime.stats.modeBaseHits += 1;
        if (isNull(Runtime.cache.modeBase)) {
            Runtime.cache.modeBase = modeBase;
            return;
        }

        if (!modeBase.equals(Runtime.cache.modeBase)) {
            handleRoundBoundary("mode_base_changed", modeBase);
        }
    }

    // 直读 GameManager.myPlayer（public static Player，静态字段区偏移 0x0）。
    // 链路：base + GameManager_TypeInfo -> klass -> +0x5C static_fields -> +0x0 myPlayer。
    // 同一地址已在 16/22/23/27/39 等功能验证。
    function readStaticLocalPlayer() {
        try {
            if (isNull(Runtime.base)) return ptr(0);

            var klass = Runtime.base.add(RVA.GameManager_TypeInfo).readPointer();
            if (isNull(klass)) return ptr(0);

            var staticFields = klass.add(OFF.Il2CppClass_static_fields).readPointer();
            if (isNull(staticFields)) return ptr(0);

            var player = staticFields.add(OFF.GameManager_myPlayer).readPointer();
            if (isNull(player)) return ptr(0);

            return player;
        } catch (error) {
            return ptr(0);
        }
    }

    // 每帧一次（由 ModeBase.UpdateTimeUI 驱动）：刷新本地玩家缓存并标记来源为静态字段。
    function refreshLocalPlayerFromStatic(reason) {
        var player = readStaticLocalPlayer();
        if (isNull(player)) {
            Runtime.stats.staticPlayerMiss += 1;
            Runtime.cache.staticSource = false;
            return ptr(0);
        }

        if (isNull(Runtime.cache.localPlayer) || !player.equals(Runtime.cache.localPlayer)) {
            Runtime.stats.localPlayerHits += 1;
        }

        Runtime.cache.localPlayer = player;
        Runtime.cache.localPlayerSeenAt = Date.now();
        Runtime.cache.staticSource = true;
        Runtime.applied = true;
        Runtime.pendingApply = false;
        Runtime.lastApplyReason = reason || "gamemanager_static";
        Runtime.stats.staticPlayerHits += 1;
        return player;
    }

    function captureLocalPlayer(player, reason) {
        if (isNull(player) || !native.ready) return false;

        if (!isReadablePtr(player)) {
            Runtime.stats.skippedInvalid += 1;
            return false;
        }

        try {
            if (!native.isMyPlayer(player, ptr(0))) return false;
        } catch (error) {
            Runtime.stats.skippedInvalid += 1;
            return false;
        }

        Runtime.cache.localPlayer = player;
        Runtime.cache.localPlayerSeenAt = Date.now();
        Runtime.applied = true;
        Runtime.pendingApply = false;
        Runtime.lastApplyReason = reason || "player_update";
        Runtime.stats.localPlayerHits += 1;
        Runtime.stats.lastPointSource = reason || "player_update";
        return true;
    }

    function attachHook(name, rva, callbacks) {
        var hook = Interceptor.attach(Runtime.base.add(rva), callbacks);
        Runtime.hooks.push(hook);
        log("info", "hook installed: " + name + " @ " + Runtime.base.add(rva));
    }

    function installHooks() {
        if (Runtime.initialized) return true;
        if (!initNativeFunctions()) return false;

        try {
            attachHook("Player.Update", RVA.Player_Update, {
                onEnter: function (args) {
                    if (!Runtime.enabled) return;

                    var local = Runtime.cache.localPlayer;
                    if (!isNull(local) && Runtime.cache.staticSource) {
                        // 快速通道：静态字段已在刷新缓存，这里只做一次指针相等比较；
                        // 人机/其他玩家到这里直接返回，不做任何内存读取或原生调用。
                        if (args[0].equals(local)) {
                            Runtime.stats.hookHits += 1;
                            performPendingActions(args[0]);
                        }
                        return;
                    }

                    // 兜底通道：静态字段暂不可用（进房瞬间）或缓存过期时，才用 isMyPlayer 重新捕获。
                    try {
                        if (isNull(local) || Date.now() - Runtime.cache.localPlayerSeenAt > Runtime.config.max_cached_player_age_ms) {
                            if (captureLocalPlayer(args[0], "Player.Update")) {
                                Runtime.stats.hookHits += 1;
                                performPendingActions(args[0]);
                            }
                            return;
                        }
                        if (args[0].equals(local)) {
                            Runtime.stats.hookHits += 1;
                            performPendingActions(args[0]);
                        }
                    } catch (error) {
                        setError("Player.Update hook failed", error);
                    }
                }
            });
            attachHook("ModeBase.UpdateTimeUI", RVA.ModeBase_UpdateTimeUI, {
                onEnter: function (args) {
                    try {
                        handleModeBaseSeen(args[0]);
                        if (!Runtime.enabled) return;

                        // 每帧只跑一次：刷新本地玩家 + 消费 pending。
                        var player = refreshLocalPlayerFromStatic("ModeBase.UpdateTimeUI");
                        if (isNull(player)) return;

                        performPendingActions(player);
                    } catch (error) {
                        setError("ModeBase.UpdateTimeUI hook failed", error);
                    }
                }
            });
            attachHook("GameManager.GameRoundEnd", RVA.GameManager_GameRoundEnd, {
                onEnter: function () {
                    try {
                        clearPendingRoundActions("game_round_end");
                    } catch (error) {
                        setError("GameManager.GameRoundEnd hook failed", error);
                    }
                }
            });
            attachHook("GameManager.NewGameRoundStart", RVA.GameManager_NewGameRoundStart, {
                onEnter: function () {
                    try {
                        clearPendingRoundActions("new_game_round_start");
                    } catch (error) {
                        setError("GameManager.NewGameRoundStart hook failed", error);
                    }
                }
            });
            attachHook("GameManager.OnDestroy", RVA.GameManager_OnDestroy, {
                onEnter: function () {
                    try {
                        handleRoundBoundary("game_manager_destroy");
                    } catch (error) {
                        setError("GameManager.OnDestroy hook failed", error);
                    }
                }
            });
            Runtime.initialized = true;
            return true;
        } catch (error) {
            setError("installHooks failed", error);
            cleanupHooks();
            return false;
        }
    }

    function readPlayerPosition(player) {
        if (isNull(player) || !native.ready) return null;
        if (!isReadablePtr(player)) {
            Runtime.stats.skippedInvalid += 1;
            return null;
        }

        try {
            var transform = native.componentGetTransform(player, ptr(0));
            if (isNull(transform)) {
                Runtime.stats.skippedNull += 1;
                return null;
            }
            if (!isReadablePtr(transform)) {
                Runtime.stats.skippedInvalid += 1;
                return null;
            }
            native.transformGetPosition(transform, posBuffer, ptr(0));
            return readVector3(posBuffer);
        } catch (error) {
            setError("readPlayerPosition failed", error);
            return null;
        }
    }

    function canQueueAction(kind) {
        if (!native.ready && !initNativeFunctions()) {
            if (kind === "save") Runtime.stats.lastSaveResult = "native_not_ready";
            else Runtime.stats.lastTeleportResult = "native_not_ready";
            return false;
        }
        if (Runtime.config.require_enabled_for_actions && !Runtime.enabled) {
            if (kind === "save") Runtime.stats.lastSaveResult = "feature_disabled";
            else Runtime.stats.lastTeleportResult = "feature_disabled";
            return false;
        }
        return true;
    }

    function queueSavePoint(slot) {
        slot = normalizeSlot(slot);
        if (!canQueueAction("save")) {
            return false;
        }

        Runtime.pending.saveSlot = slot;
        Runtime.stats.lastSaveResult = "save_pending slot " + slot;
        log("info", "save point " + slot + " pending until next Update pump");
        return true;
    }

    function saveCurrentPoint() {
        return queueSavePoint(1);
    }

    function saveCurrentPointFromPlayer(player, slot) {
        slot = normalizeSlot(slot);
        if (!captureLocalPlayer(player, "saveCurrentPoint")) {
            Runtime.stats.lastSaveResult = "not_local_player";
            return false;
        }

        var point = readPlayerPosition(player);
        if (point === null) {
            Runtime.stats.lastSaveResult = "read_position_failed";
            return false;
        }

        Runtime.savedPoints[slot] = clonePoint(point, slot);
        Runtime.stats.saveCount += 1;
        Runtime.stats.lastSaveResult = "saved_point " + slot + " " + formatPoint(Runtime.savedPoints[slot]);
        log("info", Runtime.stats.lastSaveResult);
        return true;
    }

    function hasValidSavedPoint(slot) {
        slot = normalizeSlot(slot);
        if (Runtime.savedPoints[slot] === null) return false;
        if (Runtime.savedPoints[slot].room_generation !== Runtime.roomGeneration) {
            Runtime.stats.lastTeleportResult = "saved_point_expired";
            Runtime.savedPoints[slot] = null;
            Runtime.pending.teleportSlot = 0;
            return false;
        }
        return true;
    }

    function queueTeleportToPoint(slot) {
        slot = normalizeSlot(slot);
        if (!canQueueAction("teleport")) {
            return false;
        }
        if (!hasValidSavedPoint(slot)) {
            if (Runtime.stats.lastTeleportResult !== "saved_point_expired") {
                Runtime.stats.lastTeleportResult = "no_saved_point";
            }
            return false;
        }

        Runtime.pending.teleportSlot = slot;
        Runtime.stats.lastTeleportResult = "teleport_pending slot " + slot;
        log("info", "teleport point " + slot + " pending until next Update pump");
        return true;
    }

    function requestTeleportToSavedPoint() {
        return queueTeleportToPoint(1);
    }

    function teleportToSavedPointFromPlayer(player, slot) {
        slot = normalizeSlot(slot);
        if (!hasValidSavedPoint(slot)) {
            if (Runtime.stats.lastTeleportResult !== "saved_point_expired") {
                Runtime.stats.lastTeleportResult = "no_saved_point";
            }
            return false;
        }
        if (!captureLocalPlayer(player, "teleportToSavedPoint")) {
            Runtime.stats.lastTeleportResult = "not_local_player";
            return false;
        }

        var point = Runtime.savedPoints[slot];
        try {
            native.playerSetPos(player, point.x, point.y, point.z, ptr(0));
            Runtime.stats.teleportCount += 1;
            Runtime.stats.lastTeleportResult = "teleported " + slot + " " + formatPoint(point);
            log("info", Runtime.stats.lastTeleportResult);
            return true;
        } catch (error) {
            setError("Player.SetPos failed", error);
            Runtime.stats.lastTeleportResult = "setpos_failed";
            return false;
        }
    }

    function performPendingActions(player) {
        if (!Runtime.enabled || isNull(player)) return;

        if (Runtime.pending.saveSlot) {
            var saveSlot = Runtime.pending.saveSlot;
            Runtime.pending.saveSlot = 0;
            saveCurrentPointFromPlayer(player, saveSlot);
        }

        if (Runtime.pending.teleportSlot) {
            var teleportSlot = Runtime.pending.teleportSlot;
            Runtime.pending.teleportSlot = 0;
            teleportToSavedPointFromPlayer(player, teleportSlot);
        }
    }

    function enableFeature() {
        if (!installHooks()) return false;
        Runtime.enabled = true;
        sendStatus('fixed_point_teleport', true);
        refreshLocalPlayerFromStatic("enable");
        Runtime.pendingApply = isNull(Runtime.cache.localPlayer);
        Runtime.lastApplyReason = Runtime.pendingApply ? "enable_waiting_for_local_player" : "enable_cached_local_player";
        Runtime.stats.errorCount = 0;
        Runtime.stats.lastError = "";
        log("info", "enabled");
        return true;
    }

    function disableFeature() {
        Runtime.enabled = false;
        sendStatus('fixed_point_teleport', false);
        resetRuntime("disable");
        Runtime.pendingApply = false;
        Runtime.lastApplyReason = "disable";
        log("info", "disabled");
        return true;
    }

    function cleanupFeature() {
        Runtime.enabled = false;
        Runtime.stats.cleanupCount += 1;
        try { cleanupHooks(); } catch (e) {}
        resetRuntime("cleanup");
        Runtime.pendingApply = false;
        Runtime.lastApplyReason = "cleanup";
        native.ready = false;
        log("info", "cleanup done");
        return true;
    }

    function updateConfig(config) {
        config = config || {};
        for (var key in config) {
            if (!Object.prototype.hasOwnProperty.call(config, key)) continue;
            if (key === "max_cached_player_age_ms") {
                Runtime.config.max_cached_player_age_ms = Math.max(500, Number(config[key]) || 3000);
            } else if (key === "require_enabled_for_actions") {
                Runtime.config.require_enabled_for_actions = !!config[key];
            }
        }
        log("info", "config changed");
        return true;
    }

    function buildStatus() {
        return {
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            applied: Runtime.applied,
            pendingApply: Runtime.pendingApply,
            lastApplyReason: Runtime.lastApplyReason,
            last_apply_reason: Runtime.lastApplyReason,
            generation: Runtime.generation,
            room_generation: Runtime.roomGeneration,
            hook_hits: Runtime.stats.hookHits,
            local_player_hits: Runtime.stats.localPlayerHits,
            mode_base_hits: Runtime.stats.modeBaseHits,
            round_boundary_count: Runtime.stats.roundBoundaryCount,
            error_count: Runtime.stats.errorCount,
            last_error: Runtime.stats.lastError,
            last_reset_reason: Runtime.stats.lastResetReason,
            last_room_reason: Runtime.stats.lastRoomReason,
            has_saved_point: Runtime.savedPoints[1] !== null,
            saved_point: Runtime.savedPoints[1],
            has_saved_point2: Runtime.savedPoints[2] !== null,
            saved_point2: Runtime.savedPoints[2],
            saved_points: Runtime.savedPoints,
            save_count: Runtime.stats.saveCount,
            teleport_count: Runtime.stats.teleportCount,
            last_save_result: Runtime.stats.lastSaveResult,
            last_teleport_result: Runtime.stats.lastTeleportResult,
            player_cached: !isNull(Runtime.cache.localPlayer),
            player_static_source: Runtime.cache.staticSource,
            static_player_hits: Runtime.stats.staticPlayerHits,
            static_player_miss: Runtime.stats.staticPlayerMiss,
            pending_save: Runtime.pending.saveSlot !== 0,
            pending_teleport: Runtime.pending.teleportSlot !== 0,
            pending_save_slot: Runtime.pending.saveSlot,
            pending_teleport_slot: Runtime.pending.teleportSlot,
            require_enabled_for_actions: Runtime.config.require_enabled_for_actions
        };
    }

    rpc.exports = {
        enable: function (config) {
            updateConfig(config);
            enableFeature();
            return buildStatus();
        },

        disable: function () {
            disableFeature();
            return buildStatus();
        },

        status: function () {
            return buildStatus();
        },

        cleanup: function (payload) {
            cleanupFeature();
            return buildStatus();
        },

        setConfig: function (config) {
            updateConfig(config);
            return buildStatus();
        },

        set_config: function (config) {
            updateConfig(config);
            return buildStatus();
        },

        setconfig: function (config) {
            updateConfig(config);
            return buildStatus();
        },

        savepoint: function () {
            queueSavePoint(1);
            return buildStatus();
        },

        teleporttopoint: function () {
            queueTeleportToPoint(1);
            return buildStatus();
        },

        savepoint2: function () {
            queueSavePoint(2);
            return buildStatus();
        },

        teleporttopoint2: function () {
            queueTeleportToPoint(2);
            return buildStatus();
        }
    };

    log("info", "script loaded");
})();
