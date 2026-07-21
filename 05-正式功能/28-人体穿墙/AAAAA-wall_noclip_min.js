// ============================================================
// AAAAA-wall_noclip_min.js
//
// feature_id: "wall_noclip"
// 功能目标：只让本地玩家横向穿过墙体/障碍物，不提供上升/下降控制。
//
// 实现原理：
//   1. Hook Player.MoveByLocalDirection，捕获本地 Player 和 CharacterController。
//   2. Hook UnityEngine.CharacterController.Move。
//   3. 只有功能开启且 Alt 按住时，Move 进入前才记录原始位置和 x/z 水平位移。
//   4. Move 返回后把 x/z 改成“原始位置 + 原始水平位移”，y 保留原游戏 Move 后的值。
//
// RVA / 字段来源：
//   Player_get_isMyPlayer:              0x00B55FD0  dump.cs + 常用判断点
//   Player_MoveByLocalDirection:        0x00B50A00  dump.cs + IDA 汇编
//   CharacterController_Move:           0x00AB8210  dump.cs + IDA 汇编
//   Component_get_transform:            0x0032CF40  已有自由视角功能验证
//   Transform_get_position_Injected:    0x003F4280  已有自由视角功能验证
//   Transform_set_position_Injected:    0x003F4810  已有自由视角功能验证
//   Player_characterController:         0x2C        dump.cs 字段偏移
// ============================================================

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';
    var WINAPI_CALL_CONV = 'stdcall';

    var KEY = {
        VK_MENU: 0x12
    };

    var RVA = {
        Player_get_isMyPlayer: 0x00B55FD0,
        Player_MoveByLocalDirection: 0x00B50A00,
        CharacterController_Move: 0x00AB8210,
        Component_get_transform: 0x0032CF40,
        Transform_get_position_Injected: 0x003F4280,
        Transform_set_position_Injected: 0x003F4810
    };

    var OFF = {
        Player_characterController: 0x2C
    };

    var Runtime = {
        feature_id: "wall_noclip",
        enabled: false,
        initialized: false,
        applied: false,
        pendingApply: false,
        generation: 0,
        module: null,
        base: ptr(0),
        hooks: [],
        config: {
            horizontalScale: 1.0,
            minHorizontalMotion: 0.00001,
            logEveryMoveHits: 180,
            requireAltKey: true
        },
        cache: {
            localPlayer: ptr(0),
            localController: ptr(0)
        },
        stats: {
            hookHits: 0,
            playerMoveHits: 0,
            controllerMoveHits: 0,
            noclipWrites: 0,
            altGateSkipped: 0,
            skippedNull: 0,
            skippedInvalid: 0,
            errorCount: 0,
            cleanupCount: 0,
            lastResetReason: "",
            lastApplyReason: "",
            lastError: ""
        }
    };

    var native = {
        ready: false,
        isMyPlayer: null,
        componentGetTransform: null,
        transformGetPosition: null,
        transformSetPosition: null,
        getAsyncKeyState: null
    };

    var posBuffer = Memory.alloc(12);
    var writePosBuffer = Memory.alloc(12);
    var floatScratch = Memory.alloc(4);
    var LogLimiter = {};

    function log(level, message) {
        try {
            var text = '[' + Runtime.feature_id + '][' + level + '] ' + message;
            console.log(text);
            send({ type: 'log', level: level, module: Runtime.feature_id, message: message });
        } catch (_) {
        }
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

    function resetRuntime(reason) {
        Runtime.generation += 1;
        Runtime.cache.localPlayer = ptr(0);
        Runtime.cache.localController = ptr(0);
        Runtime.applied = false;
        Runtime.pendingApply = Runtime.enabled;
        Runtime.stats.lastResetReason = reason || 'unknown';
        Runtime.stats.lastApplyReason = '';
        log('info', 'resetRuntime: ' + Runtime.stats.lastResetReason + ', gen=' + Runtime.generation);
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
            native.isMyPlayer = new NativeFunction(
                Runtime.base.add(RVA.Player_get_isMyPlayer),
                'bool',
                ['pointer', 'pointer'],
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
            native.transformSetPosition = new NativeFunction(
                Runtime.base.add(RVA.Transform_set_position_Injected),
                'void',
                ['pointer', 'pointer', 'pointer'],
                CALL_CONV
            );
            initKeyboardFunctions();
            native.ready = true;
            return true;
        } catch (error) {
            setError('initNativeFunctions failed', error);
            native.ready = false;
            return false;
        }
    }

    function resolveExportAddress(moduleName, exportName) {
        var addr = null;

        try {
            if (typeof Module !== 'undefined' && typeof Module.findExportByName === 'function') {
                addr = Module.findExportByName(moduleName, exportName);
                if (!isNull(addr)) return addr;
            }
        } catch (_) {
        }

        try {
            if (typeof Module !== 'undefined' && typeof Module.getExportByName === 'function') {
                addr = Module.getExportByName(moduleName, exportName);
                if (!isNull(addr)) return addr;
            }
        } catch (_) {
        }

        try {
            if (typeof Process.getModuleByName === 'function') {
                var mod = Process.getModuleByName(moduleName);
                if (mod && typeof mod.getExportByName === 'function') {
                    addr = mod.getExportByName(exportName);
                    if (!isNull(addr)) return addr;
                }
            }
        } catch (_) {
        }

        try {
            if (typeof ApiResolver !== 'undefined') {
                var resolver = new ApiResolver('module');
                var matches = resolver.enumerateMatches('exports:' + moduleName + '!' + exportName);
                if (matches && matches.length > 0 && !isNull(matches[0].address)) {
                    return matches[0].address;
                }
            }
        } catch (_) {
        }

        try {
            var processModule = Process.findModuleByName(moduleName);
            if (processModule && typeof processModule.enumerateExports === 'function') {
                var exports = processModule.enumerateExports();
                for (var i = 0; i < exports.length; i++) {
                    if (exports[i].name === exportName) return exports[i].address;
                }
            }
        } catch (_) {
        }

        return null;
    }

    function initKeyboardFunctions() {
        if (native.getAsyncKeyState !== null) return true;

        try {
            var address = resolveExportAddress('user32.dll', 'GetAsyncKeyState');
            if (address === null) {
                logLimited('keyboard:init', 'warn', 'GetAsyncKeyState not found; Alt gate will stay closed', 3000);
                return false;
            }

            native.getAsyncKeyState = new NativeFunction(
                address,
                'int16',
                ['int'],
                WINAPI_CALL_CONV
            );
            return true;
        } catch (error) {
            setError('init GetAsyncKeyState failed', error);
            native.getAsyncKeyState = null;
            return false;
        }
    }

    function isAltNoclipKeyDown() {
        if (native.getAsyncKeyState === null && !initKeyboardFunctions()) return false;

        try {
            return (native.getAsyncKeyState(KEY.VK_MENU) & 0x8000) !== 0;
        } catch (error) {
            setError('GetAsyncKeyState failed', error);
            native.getAsyncKeyState = null;
            return false;
        }
    }

    function isLocalPlayer(player) {
        if (isNull(player) || !native.ready) return false;
        if (!isNull(Runtime.cache.localPlayer) && player.equals(Runtime.cache.localPlayer)) return true;
        try {
            if (native.isMyPlayer(player, ptr(0))) {
                Runtime.cache.localPlayer = player;
                return true;
            }
        } catch (error) {
            setError('Player.get_isMyPlayer failed', error);
        }
        return false;
    }

    function readPlayerController(player) {
        try {
            if (!isReadablePtr(player)) {
                Runtime.stats.skippedInvalid += 1;
                return ptr(0);
            }
            var controller = player.add(OFF.Player_characterController).readPointer();
            if (isNull(controller)) {
                Runtime.stats.skippedNull += 1;
                return ptr(0);
            }
            return controller;
        } catch (error) {
            Runtime.stats.skippedInvalid += 1;
            setError('read Player.characterController failed', error);
            return ptr(0);
        }
    }

    function captureLocalController(player, reason) {
        if (!Runtime.enabled || !native.ready) return;
        if (!isLocalPlayer(player)) return;

        var controller = readPlayerController(player);
        if (isNull(controller)) {
            Runtime.pendingApply = true;
            Runtime.applied = false;
            Runtime.stats.lastApplyReason = 'controller_not_ready';
            return;
        }

        if (isNull(Runtime.cache.localController) || !controller.equals(Runtime.cache.localController)) {
            Runtime.cache.localController = controller;
            Runtime.applied = true;
            Runtime.pendingApply = false;
            Runtime.stats.lastApplyReason = reason || 'controller_captured';
            log('info', 'local CharacterController captured: ' + controller);
        }
    }

    function readVector3(buffer) {
        var x = buffer.readFloat();
        var y = buffer.add(4).readFloat();
        var z = buffer.add(8).readFloat();
        if (!isFinite(x) || !isFinite(y) || !isFinite(z)) return null;
        return { x: x, y: y, z: z };
    }

    function writeVector3(buffer, x, y, z) {
        buffer.writeFloat(x);
        buffer.add(4).writeFloat(y);
        buffer.add(8).writeFloat(z);
    }

    function stackArgToFloat(arg) {
        floatScratch.writeU32(arg.toUInt32());
        return floatScratch.readFloat();
    }

    function getTransform(component) {
        if (isNull(component) || !native.ready) return ptr(0);
        try {
            return native.componentGetTransform(component, ptr(0));
        } catch (error) {
            setError('Component.get_transform failed', error);
            return ptr(0);
        }
    }

    function readTransformPosition(transform) {
        if (isNull(transform) || !native.ready) return null;
        try {
            native.transformGetPosition(transform, posBuffer, ptr(0));
            return readVector3(posBuffer);
        } catch (error) {
            setError('Transform.get_position failed', error);
            return null;
        }
    }

    function writeTransformPosition(transform, pos) {
        if (isNull(transform) || pos === null || !native.ready) return false;
        try {
            writeVector3(writePosBuffer, pos.x, pos.y, pos.z);
            native.transformSetPosition(transform, writePosBuffer, ptr(0));
            return true;
        } catch (error) {
            setError('Transform.set_position failed', error);
            return false;
        }
    }

    function applyHorizontalNoclip(controller, beforePosition, motionX, motionZ) {
        var scale = Number(Runtime.config.horizontalScale) || 1.0;
        var dx = motionX * scale;
        var dz = motionZ * scale;
        var abs = Math.abs(dx) + Math.abs(dz);

        if (abs < Runtime.config.minHorizontalMotion) return false;
        if (beforePosition === null) return false;

        var transform = getTransform(controller);
        if (isNull(transform)) {
            Runtime.stats.skippedNull += 1;
            return false;
        }

        var afterPosition = readTransformPosition(transform);
        if (afterPosition === null) {
            Runtime.stats.skippedInvalid += 1;
            return false;
        }

        var target = {
            x: beforePosition.x + dx,
            y: afterPosition.y,
            z: beforePosition.z + dz
        };

        if (!writeTransformPosition(transform, target)) {
            Runtime.stats.skippedInvalid += 1;
            return false;
        }

        Runtime.stats.noclipWrites += 1;
        if (Runtime.stats.noclipWrites === 1 ||
            Runtime.stats.noclipWrites % Runtime.config.logEveryMoveHits === 0) {
            log('info', 'horizontal noclip write #' + Runtime.stats.noclipWrites +
                ', dx=' + dx.toFixed(4) + ', dz=' + dz.toFixed(4));
        }
        return true;
    }

    function isCurrentLocalController(controller) {
        if (isNull(controller) || isNull(Runtime.cache.localController)) return false;
        try {
            return controller.equals(Runtime.cache.localController);
        } catch (_) {
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
            attachHook('Player.MoveByLocalDirection', RVA.Player_MoveByLocalDirection, {
                onEnter: function (args) {
                    Runtime.stats.hookHits += 1;
                    Runtime.stats.playerMoveHits += 1;
                    if (!Runtime.enabled) return;
                    captureLocalController(args[0], 'Player.MoveByLocalDirection');
                }
            });

            attachHook('UnityEngine.CharacterController.Move', RVA.CharacterController_Move, {
                onEnter: function (args) {
                    Runtime.stats.hookHits += 1;
                    Runtime.stats.controllerMoveHits += 1;
                    this.shouldApplyHorizontal = false;
                    this.controller = ptr(0);
                    this.beforePosition = null;
                    this.motionX = 0.0;
                    this.motionZ = 0.0;
                    if (!Runtime.enabled) return;

                    try {
                        var controller = args[0];
                        if (!isCurrentLocalController(controller)) return;
                        if (Runtime.config.requireAltKey && !isAltNoclipKeyDown()) {
                            Runtime.stats.altGateSkipped += 1;
                            return;
                        }

                        var transform = getTransform(controller);
                        if (isNull(transform)) return;

                        this.controller = controller;
                        this.beforePosition = readTransformPosition(transform);
                        this.motionX = stackArgToFloat(args[1]);
                        this.motionZ = stackArgToFloat(args[3]);
                        this.shouldApplyHorizontal = this.beforePosition !== null;
                    } catch (error) {
                        setError('CharacterController.Move onEnter failed', error);
                    }
                },

                onLeave: function () {
                    if (!Runtime.enabled || !this.shouldApplyHorizontal) return;

                    try {
                        applyHorizontalNoclip(this.controller, this.beforePosition, this.motionX, this.motionZ);
                    } catch (error) {
                        setError('CharacterController.Move onLeave failed', error);
                        if (Runtime.stats.errorCount >= 8) {
                            Runtime.enabled = false;
                            resetRuntime('too_many_errors');
                        }
                    }
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
        Runtime.pendingApply = isNull(Runtime.cache.localController);
        Runtime.stats.errorCount = 0;
        Runtime.stats.lastError = '';
        Runtime.stats.lastApplyReason = Runtime.pendingApply ? 'waiting_for_local_player' : 'already_captured';
        log('info', 'enabled; waiting for local player movement');
        return getStatus();
    }

    function disableFeature() {
        Runtime.enabled = false;
        resetRuntime('disable');
        log('info', 'disabled');
        return getStatus();
    }

    function cleanupFeature() {
        Runtime.enabled = false;
        Runtime.stats.cleanupCount += 1;
        cleanupHooks();
        resetRuntime('cleanup');
        log('info', 'cleanup done');
        return getStatus();
    }

    function updateConfig(input) {
        input = input || {};
        if (input.horizontalScale !== undefined) {
            var scale = Number(input.horizontalScale);
            if (isFinite(scale) && scale >= 0.5 && scale <= 2.0) {
                Runtime.config.horizontalScale = scale;
            }
        }
        if (input.requireAltKey !== undefined) {
            Runtime.config.requireAltKey = input.requireAltKey !== false;
        }
        log('info', 'config changed: horizontalScale=' + Runtime.config.horizontalScale +
            ', requireAltKey=' + Runtime.config.requireAltKey);
        return getStatus();
    }

    function getStatus() {
        return {
            ok: Runtime.stats.lastError === '',
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            applied: Runtime.applied,
            pendingApply: Runtime.pendingApply,
            generation: Runtime.generation,
            localPlayer: isNull(Runtime.cache.localPlayer) ? '' : Runtime.cache.localPlayer.toString(),
            localController: isNull(Runtime.cache.localController) ? '' : Runtime.cache.localController.toString(),
            config: Runtime.config,
            alt_key_required: Runtime.config.requireAltKey,
            alt_key_down: isAltNoclipKeyDown(),
            hook_hits: Runtime.stats.hookHits,
            player_move_hits: Runtime.stats.playerMoveHits,
            controller_move_hits: Runtime.stats.controllerMoveHits,
            noclip_writes: Runtime.stats.noclipWrites,
            alt_gate_skipped: Runtime.stats.altGateSkipped,
            error_count: Runtime.stats.errorCount,
            last_error: Runtime.stats.lastError,
            last_reset_reason: Runtime.stats.lastResetReason,
            lastApplyReason: Runtime.stats.lastApplyReason,
            stats: Runtime.stats
        };
    }

    rpc.exports = {
        enable: function () {
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

        reset: function (reason) {
            resetRuntime(reason || 'manual');
            return getStatus();
        }
    };

    log('info', 'script loaded; pointerSize=' + Process.pointerSize + ', arch=' + Process.arch);
})();
