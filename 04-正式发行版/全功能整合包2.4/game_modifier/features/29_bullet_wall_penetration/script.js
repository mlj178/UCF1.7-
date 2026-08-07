// ============================================================
// AAAAA-bullet_wall_penetration_min.js
//
// feature_id: "bullet_wall_penetration"
// 功能目标：仿原版穿透版。子弹可以穿墙命中墙后的 HitBox，
// 但仍让 WPN_Gun.Damage 的原逻辑调用 WeaponLogic.CheckWall，
// 使用 WeaponData_Gun.wallShotDamageRatio 做伤害衰减，并保留
// wallThrough 命中/击杀标记。
//
// 实现原理：
//   1. Hook WPN_Gun.Damage，不替换原伤害流程。
//   2. 仅当本地玩家武器进入 Damage 时，临时把 LayerConstant.LM_GunShoot
//      改成 HitBox-only mask，让原 RaycastAll 可拿到墙后的 hitbox。
//   3. Damage 返回后立刻恢复 LM_GunShoot。
//   4. WeaponLogic.CheckWall 保持原样，只记录状态；墙体判定、伤害衰减、
//      wallThrough 标记继续由游戏原版代码执行。
//
// RVA / 字段来源：dump.cs + IDA 汇编交叉验证
//   Weapon_get_isMyWeapon:                 0x00B6E1D0
//   WPN_Gun_Damage:                        0x00B613D0
//   WeaponLogic_CheckWall:                 0x00B78F80
//   LayerConstant_cctor:                   0x00AE7CD0
//   LayerConstant_TypeInfo:                0x0E2BE3C
//   Weapon.data:                           0x68
//   WPN_Gun.realData:                      0xEC
//   WeaponData_Gun.wallShotDamageRatio:    0x158
//   LayerConstant.HitBox:                  0x8
//   LayerConstant.LM_GunShoot:             0x38
// ============================================================

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';

    var RVA = {
        Weapon_get_isMyWeapon: 0x00B6E1D0,
        WPN_Gun_Damage: 0x00B613D0,
        WeaponLogic_CheckWall: 0x00B78F80,
        LayerConstant_cctor: 0x00AE7CD0,
        LayerConstant_TypeInfo: 0x0E2BE3C
    };

    var OFF = {
        Weapon_data: 0x68,
        WPN_Gun_realData: 0xEC,
        WeaponData_Gun_wallShotDamageRatio: 0x158,
        Klass_staticFields: 0x5C,
        LayerConstant_HitBox: 0x8,
        LayerConstant_LM_GunShoot: 0x38
    };

    var Runtime = {
        feature_id: "bullet_wall_penetration",
        enabled: false,
        initialized: false,
        module: null,
        base: ptr(0),
        hooks: [],
        damageDepth: 0,
        activeDamageWeapon: ptr(0),
        layerInitialized: false,
        currentPatch: null,
        config: {
            forceHitboxOnlyDuringLocalDamage: true,
            logEveryDamageHits: 25
        },
        stats: {
            damageHits: 0,
            localDamageHits: 0,
            checkWallHits: 0,
            layerPatchCount: 0,
            layerRestoreCount: 0,
            skippedRemoteWeapon: 0,
            skippedInvalid: 0,
            errorCount: 0,
            cleanupCount: 0,
            lastWallRatio: -1.0,
            lastCheckWallResult: null,
            lastHitBoxLayer: -1,
            lastOriginalGunShootMask: 0,
            lastPatchedGunShootMask: 0,
            lastError: "",
            lastPatchReason: "",
            lastRestoreReason: ""
        }
    };

    var native = {
        ready: false,
        isMyWeapon: null,
        layerConstantCctor: null
    };

    var LogLimiter = {};

    function log(level, message) {
        try {
            var text = '[' + Runtime.feature_id + '][' + level + '] ' + message;
            console.log(text);
            send({ type: 'log', level: level, module: Runtime.feature_id, message: message });
        } catch (_) {
        }
    }

    function sendStatus(feature, enabled) {
        try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (_) {}
    }

    function logLimited(key, level, message, intervalMs) {
        var now = Date.now();
        var wait = intervalMs || 1000;
        if (!LogLimiter[key] || now - LogLimiter[key] >= wait) {
            LogLimiter[key] = now;
            log(level, message);
        }
    }

    function setError(label, error) {
        Runtime.stats.errorCount += 1;
        Runtime.stats.lastError = label + (error && error.message ? ': ' + error.message : '');
        logLimited('error:' + label, 'error', Runtime.stats.lastError, 1500);
    }

    function isNull(p) {
        if (p === null || p === undefined) return true;
        try { return p.isNull(); } catch (_) { return true; }
    }

    function isReadablePtr(p) {
        try {
            if (isNull(p)) return false;
            p.readPointer();
            return true;
        } catch (_) {
            return false;
        }
    }

    function isExecutable(p) {
        try {
            var range = Process.findRangeByAddress(p);
            return range !== null && range.protection.indexOf('x') !== -1;
        } catch (_) {
            return false;
        }
    }

    function findGameAssembly() {
        if (Runtime.module) return Runtime.module;
        var mod = Process.findModuleByName(MODULE_NAME);
        if (!mod) {
            Runtime.stats.lastError = MODULE_NAME + ' not found';
            return null;
        }
        Runtime.module = mod;
        Runtime.base = mod.base;
        return mod;
    }

    function initNativeFunctions() {
        if (native.ready) return true;
        var mod = findGameAssembly();
        if (!mod) return false;

        if (Process.arch !== 'ia32' || Process.pointerSize !== 4) {
            Runtime.stats.lastError = 'unsupported process: arch=' + Process.arch + ', pointerSize=' + Process.pointerSize;
            log('error', Runtime.stats.lastError);
            return false;
        }

        try {
            native.isMyWeapon = new NativeFunction(
                Runtime.base.add(RVA.Weapon_get_isMyWeapon),
                'bool',
                ['pointer', 'pointer'],
                CALL_CONV
            );
            native.layerConstantCctor = new NativeFunction(
                Runtime.base.add(RVA.LayerConstant_cctor),
                'void',
                ['pointer'],
                CALL_CONV
            );
            native.ready = true;
            return true;
        } catch (error) {
            setError('initNativeFunctions failed', error);
            native.ready = false;
            return false;
        }
    }

    function initializeLayerConstant() {
        if (Runtime.layerInitialized) return true;
        try {
            native.layerConstantCctor(ptr(0));
            Runtime.layerInitialized = true;
            return true;
        } catch (error) {
            setError('LayerConstant..cctor failed', error);
            return false;
        }
    }

    function getLayerStaticFields() {
        if (!native.ready && !initNativeFunctions()) return ptr(0);
        if (!Runtime.layerInitialized && !initializeLayerConstant()) return ptr(0);

        try {
            var klassPtr = Runtime.base.add(RVA.LayerConstant_TypeInfo).readPointer();
            if (isNull(klassPtr) || !isReadablePtr(klassPtr)) return ptr(0);
            return klassPtr.add(OFF.Klass_staticFields).readPointer();
        } catch (error) {
            setError('get LayerConstant static fields failed', error);
            return ptr(0);
        }
    }

    function readLayerValue(offset) {
        try {
            var fields = getLayerStaticFields();
            if (isNull(fields)) return null;
            return fields.add(offset).readS32();
        } catch (error) {
            setError('read LayerConstant field failed', error);
            return null;
        }
    }

    function writeLayerValue(offset, value) {
        try {
            var fields = getLayerStaticFields();
            if (isNull(fields)) return false;
            fields.add(offset).writeS32(value | 0);
            return true;
        } catch (error) {
            setError('write LayerConstant field failed', error);
            return false;
        }
    }

    function buildHitBoxOnlyMask() {
        var hitBoxLayer = readLayerValue(OFF.LayerConstant_HitBox);
        if (hitBoxLayer === null || hitBoxLayer < 0 || hitBoxLayer > 30) {
            Runtime.stats.skippedInvalid += 1;
            logLimited('hitbox-layer-invalid', 'warn', 'invalid LayerConstant.HitBox=' + hitBoxLayer, 2000);
            return null;
        }
        Runtime.stats.lastHitBoxLayer = hitBoxLayer;
        return 1 << hitBoxLayer;
    }

    function patchGunShootLayerMask(reason) {
        if (!Runtime.enabled || !Runtime.config.forceHitboxOnlyDuringLocalDamage) return false;
        if (Runtime.currentPatch !== null) {
            Runtime.currentPatch.depth += 1;
            return true;
        }

        var originalMask = readLayerValue(OFF.LayerConstant_LM_GunShoot);
        var patchedMask = buildHitBoxOnlyMask();
        if (originalMask === null || patchedMask === null) return false;
        if (originalMask === patchedMask) {
            Runtime.currentPatch = {
                depth: 1,
                originalMask: originalMask,
                patchedMask: patchedMask,
                alreadyMatched: true
            };
            return true;
        }

        if (!writeLayerValue(OFF.LayerConstant_LM_GunShoot, patchedMask)) return false;

        Runtime.currentPatch = {
            depth: 1,
            originalMask: originalMask,
            patchedMask: patchedMask,
            alreadyMatched: false
        };
        Runtime.stats.layerPatchCount += 1;
        Runtime.stats.lastOriginalGunShootMask = originalMask;
        Runtime.stats.lastPatchedGunShootMask = patchedMask;
        Runtime.stats.lastPatchReason = reason || '';
        logLimited('layer-patch', 'info', 'LM_GunShoot patched 0x' +
            (originalMask >>> 0).toString(16) + ' -> 0x' + (patchedMask >>> 0).toString(16), 1000);
        return true;
    }

    function writeOriginalMaskAndClearPatch(reason) {
        if (Runtime.currentPatch === null) return false;

        var patch = Runtime.currentPatch;
        Runtime.stats.lastRestoreReason = reason || '';

        if (patch.alreadyMatched) {
            Runtime.currentPatch = null;
            return true;
        }

        if (!writeLayerValue(OFF.LayerConstant_LM_GunShoot, patch.originalMask)) {
            patch.depth = Math.max(patch.depth, 1);
            setError('restore LM_GunShoot failed', { message: 'write original mask failed' });
            return false;
        }

        var readbackMask = readLayerValue(OFF.LayerConstant_LM_GunShoot);
        if (readbackMask !== patch.originalMask) {
            patch.depth = Math.max(patch.depth, 1);
            setError('restore LM_GunShoot readback mismatch', {
                message: 'expected 0x' + (patch.originalMask >>> 0).toString(16) +
                    ', got 0x' + ((readbackMask || 0) >>> 0).toString(16)
            });
            return false;
        }

        Runtime.currentPatch = null;

        Runtime.stats.layerRestoreCount += 1;
        logLimited('layer-restore', 'info', 'LM_GunShoot restored to 0x' +
            (patch.originalMask >>> 0).toString(16), 1000);
        return true;
    }

    function restoreGunShootLayerMask(reason) {
        if (Runtime.currentPatch === null) return false;

        if (Runtime.currentPatch.depth > 1) {
            Runtime.currentPatch.depth -= 1;
            return true;
        }

        Runtime.currentPatch.depth = 1;
        return writeOriginalMaskAndClearPatch(reason);
    }

    function forceRestoreGunShootLayerMask(reason) {
        if (Runtime.currentPatch === null) return false;

        Runtime.currentPatch.depth = 1;
        return writeOriginalMaskAndClearPatch(reason);
    }

    function readWallShotDamageRatio(wpnGun) {
        try {
            if (isNull(wpnGun)) return null;

            var data = wpnGun.add(OFF.WPN_Gun_realData).readPointer();
            if (isNull(data)) {
                data = wpnGun.add(OFF.Weapon_data).readPointer();
            }
            if (isNull(data)) return null;

            var wallShotDamageRatio = data.add(OFF.WeaponData_Gun_wallShotDamageRatio).readFloat();
            if (!isFinite(wallShotDamageRatio)) return null;

            Runtime.stats.lastWallRatio = wallShotDamageRatio;
            return wallShotDamageRatio;
        } catch (error) {
            setError('readWallShotDamageRatio failed', error);
            return null;
        }
    }

    function isLocalWeapon(weapon) {
        if (isNull(weapon) || !native.ready) return false;
        try {
            return native.isMyWeapon(weapon, ptr(0)) === true;
        } catch (error) {
            setError('Weapon.get_isMyWeapon failed', error);
            return false;
        }
    }

    function attachHook(name, rva, callbacks) {
        var address = Runtime.base.add(rva);
        if (!isExecutable(address)) throw new Error(name + ' address is not executable: ' + address);
        var handle = Interceptor.attach(address, callbacks);
        Runtime.hooks.push(handle);
        log('info', 'hook installed: ' + name + ' @ 0x' + rva.toString(16));
    }

    function installHooks() {
        if (Runtime.initialized) return true;
        if (!initNativeFunctions()) return false;

        try {
            attachHook('WPN_Gun.Damage', RVA.WPN_Gun_Damage, {
                onEnter: function (args) {
                    Runtime.stats.damageHits += 1;
                    this.localDamage = false;
                    this.weapon = args[0];

                    if (!Runtime.enabled) return;

                    try {
                        if (!native.isMyWeapon(args[0], ptr(0))) {
                            Runtime.stats.skippedRemoteWeapon += 1;
                            return;
                        }

                        this.localDamage = true;
                        Runtime.stats.localDamageHits += 1;
                        Runtime.damageDepth += 1;
                        Runtime.activeDamageWeapon = args[0];
                        readWallShotDamageRatio(args[0]);
                        patchGunShootLayerMask('WPN_Gun.Damage onEnter');

                        if (Runtime.stats.localDamageHits === 1 ||
                            Runtime.stats.localDamageHits % Runtime.config.logEveryDamageHits === 0) {
                            log('info', 'local WPN_Gun.Damage #' + Runtime.stats.localDamageHits +
                                ', wallShotDamageRatio=' + Runtime.stats.lastWallRatio);
                        }
                    } catch (error) {
                        setError('WPN_Gun.Damage onEnter failed', error);
                    }
                },

                onLeave: function () {
                    if (!this.localDamage) return;

                    try {
                        restoreGunShootLayerMask('WPN_Gun.Damage onLeave');
                    } catch (error) {
                        setError('WPN_Gun.Damage onLeave restore failed', error);
                    } finally {
                        Runtime.damageDepth -= 1;
                        if (Runtime.damageDepth <= 0) {
                            Runtime.damageDepth = 0;
                            Runtime.activeDamageWeapon = ptr(0);
                        }
                    }
                }
            });

            attachHook('WeaponLogic.CheckWall', RVA.WeaponLogic_CheckWall, {
                onEnter: function () {
                    this.track = Runtime.enabled && Runtime.damageDepth > 0;
                },

                onLeave: function (retval) {
                    if (!this.track) return;
                    Runtime.stats.checkWallHits += 1;
                    Runtime.stats.lastCheckWallResult = retval.toInt32() !== 0;
                }
            });

            Runtime.initialized = true;
            log('info', 'hooks installed');
            return true;
        } catch (error) {
            setError('installHooks failed', error);
            cleanupHooks();
            return false;
        }
    }

    function cleanupHooks() {
        for (var i = 0; i < Runtime.hooks.length; i++) {
            try {
                if (Runtime.hooks[i] && Runtime.hooks[i].detach) Runtime.hooks[i].detach();
            } catch (_) {
            }
        }
        Runtime.hooks = [];
        Runtime.initialized = false;
    }

    function enableFeature() {
        if (!installHooks()) {
            return {
                ok: false,
                feature_id: Runtime.feature_id,
                enabled: Runtime.enabled,
                initialized: Runtime.initialized,
                error: Runtime.stats.lastError || 'installHooks failed'
            };
        }

        Runtime.enabled = true;
        sendStatus('29_bullet_wall_penetration', true);
        Runtime.stats.errorCount = 0;
        Runtime.stats.lastError = '';
        log('info', 'enabled: original damage flow + wallShotDamageRatio preserved');
        return getStatus();
    }

    function disableFeature() {
        Runtime.enabled = false;
        sendStatus('29_bullet_wall_penetration', false);
        forceRestoreGunShootLayerMask('disable');
        Runtime.damageDepth = 0;
        Runtime.activeDamageWeapon = ptr(0);
        log('info', 'disabled');
        return getStatus();
    }

    function cleanupFeature() {
        Runtime.enabled = false;
        Runtime.stats.cleanupCount += 1;
        forceRestoreGunShootLayerMask('cleanup');
        cleanupHooks();
        Runtime.damageDepth = 0;
        Runtime.activeDamageWeapon = ptr(0);
        log('info', 'cleanup done');
        return getStatus();
    }

    function updateConfig(input) {
        input = input || {};
        if (input.forceHitboxOnlyDuringLocalDamage !== undefined) {
            Runtime.config.forceHitboxOnlyDuringLocalDamage =
                input.forceHitboxOnlyDuringLocalDamage !== false;
        }
        if (input.logEveryDamageHits !== undefined) {
            var every = Number(input.logEveryDamageHits);
            if (isFinite(every) && every >= 1 && every <= 1000) {
                Runtime.config.logEveryDamageHits = Math.floor(every);
            }
        }
        log('info', 'config changed: forceHitboxOnlyDuringLocalDamage=' +
            Runtime.config.forceHitboxOnlyDuringLocalDamage);
        return getStatus();
    }

    function getStatus() {
        return {
            ok: Runtime.stats.lastError === '',
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            damage_depth: Runtime.damageDepth,
            active_weapon: isNull(Runtime.activeDamageWeapon) ? '' : Runtime.activeDamageWeapon.toString(),
            current_patch_active: Runtime.currentPatch !== null,
            config: Runtime.config,
            damage_hits: Runtime.stats.damageHits,
            local_damage_hits: Runtime.stats.localDamageHits,
            layer_patch_count: Runtime.stats.layerPatchCount,
            layer_restore_count: Runtime.stats.layerRestoreCount,
            check_wall_hits: Runtime.stats.checkWallHits,
            last_wall_ratio: Runtime.stats.lastWallRatio,
            last_check_wall_result: Runtime.stats.lastCheckWallResult,
            last_hitbox_layer: Runtime.stats.lastHitBoxLayer,
            last_original_gunshoot_mask: Runtime.stats.lastOriginalGunShootMask,
            last_patched_gunshoot_mask: Runtime.stats.lastPatchedGunShootMask,
            skipped_remote_weapon: Runtime.stats.skippedRemoteWeapon,
            error_count: Runtime.stats.errorCount,
            last_error: Runtime.stats.lastError,
            stats: Runtime.stats
        };
    }

    rpc.exports = {
        enable: function (config) {
            if (config) updateConfig(config || {});
            return enableFeature();
        },

        disable: function () {
            return disableFeature();
        },

        status: function () {
            return getStatus();
        },

        cleanup: function () {
            return cleanupFeature();
        },

        setconfig: function (config) {
            return updateConfig(config || {});
        },

        setConfig: function (config) {
            return updateConfig(config || {});
        },

        set_config: function (config) {
            return updateConfig(config || {});
        }
    };

    log('info', 'script loaded; pointerSize=' + Process.pointerSize + ', arch=' + Process.arch);
})();
