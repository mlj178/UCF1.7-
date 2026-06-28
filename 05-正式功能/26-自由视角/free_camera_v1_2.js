// ============================================================
// free_camera_v1_2.js
//
// 自由视角 / Free Camera v1.2
//
// 修复 v1.1：
//   1. 删除 CameraManager 系列 Hook，避免开启后热路径掉帧。
//   2. 不再加载时预安装 Hook，点击开启后才安装。
//   3. 热路径不再调用 Process.findRangeByAddress。
//   4. 每帧从 CinemachineBrain 输出相机重新取 Transform，避免旧 Transform 指针导致崩溃。
//   5. 默认不锁玩家移动，先保证自由相机有效果；UI 可手动开启锁移动。
//
// 控制：
//   鼠标：控制相机朝向，复用游戏 Player.cameraRotation。
//   W/A/S/D：控制相机水平自由移动，输入来源为 Player.GetWalkVelocity 的 displayClass。
//   暂不实现：空格上升、Ctrl/Shift 下降或加速。
//
// 规则：
//   不调用 IL2CPP API / 反射 API。
//   不调用 il2cpp_runtime_class_init / il2cpp_class_* / il2cpp_field_*。
// ============================================================

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var module = Process.findModuleByName(MODULE_NAME);

    function sendLog(level, message, extra) {
        try {
            var payload = {
                type: 'log',
                level: level,
                module: 'FREE-CAMERA',
                message: message
            };
            if (extra !== undefined) payload.extra = extra;
            send(payload);
            console.log('[free_camera][' + level + '] ' + message);
        } catch (_) {
        }
    }

    var state = {
        moduleOk: false,
        archOk: false,
        nativeReady: false,
        installed: false,
        enabled: false,
        listeners: [],
        localPlayer: null,
        camera: {
            valid: false,
            initialized: false,
            x: 0.0,
            y: 0.0,
            z: 0.0,
            yaw: 0.0,
            pitch: 0.0,
            lastFrameMs: 0,
            lastTransform: null
        },
        input: {
            valid: false,
            yaw: 0.0,
            pitch: 0.0,
            lastSampleMs: 0
        },
        moveInput: {
            valid: false,
            x: 0.0,
            z: 0.0,
            lastSampleMs: 0
        },
        stats: {
            hooksInstalled: 0,
            hookFailures: 0,
            cameraFrames: 0,
            cameraWrites: 0,
            moveFrames: 0,
            movementSamples: 0,
            zeroWalkVelocity: 0,
            cameraFailures: 0,
            inputSamples: 0,
            errors: 0
        },
        lastError: null
    };

    if (module === null) {
        state.lastError = MODULE_NAME + ' 未加载';
        sendLog('error', state.lastError);
    } else {
        state.moduleOk = true;
    }

    if (Process.arch !== 'ia32' || Process.pointerSize !== 4) {
        state.lastError = '只支持 32 位 x86 游戏进程，当前 arch=' + Process.arch + ', pointerSize=' + Process.pointerSize;
        sendLog('error', state.lastError);
    } else {
        state.archOk = true;
    }

    var base = state.moduleOk ? module.base : ptr(0);
    var CALL_CONV = 'mscdecl';

    var RVA = {
        Player_get_isMyPlayer:                 0x00B55FD0,
        Player_UpdateCameraRotaion:            0x00B54870,
        Player_GetWalkVelocity:                0x00B54220,

        Brain_PushStateToUnityCamera:          0x0082B750,
        Brain_get_OutputCamera:                0x0082CDB0,

        Component_get_transform:               0x0032CF40,
        Transform_get_position_Injected:       0x003F4280,
        Transform_get_forward_Injected:        0x003F3F20,
        Transform_set_position_Injected:       0x003F4810,
        Transform_set_rotation_Injected:       0x003F4870
    };

    var OFF = {
        Player_cameraRotation: 0x4C
    };

    var config = {
        moveSpeed: 8.0,
        pitchMin: -80.0,
        pitchMax: 80.0,
        lockPlayerMove: false,
        inputStaleMs: 180
    };

    var posBuffer = Memory.alloc(12);
    var fwdBuffer = Memory.alloc(12);
    var writePosBuffer = Memory.alloc(12);
    var writeRotBuffer = Memory.alloc(16);

    var native = {
        isMyPlayer: null,
        brainGetOutputCamera: null,
        componentGetTransform: null,
        transformGetPosition: null,
        transformGetForward: null,
        transformSetPosition: null,
        transformSetRotation: null
    };

    function isNull(p) {
        if (p === null || p === undefined) return true;
        try { return p.isNull(); } catch (_) { return true; }
    }

    function isExecutable(p) {
        try {
            var range = Process.findRangeByAddress(p);
            return range !== null && range.protection.indexOf('x') !== -1;
        } catch (_) {
            return false;
        }
    }

    function setError(label, error) {
        state.stats.errors++;
        state.lastError = label + (error ? ': ' + error : '');
        if (state.stats.errors <= 10) sendLog('error', state.lastError);
    }

    function clamp(v, minV, maxV) {
        return Math.max(minV, Math.min(maxV, v));
    }

    function normalizeAngle(angle) {
        var v = angle % 360.0;
        if (v > 180.0) v -= 360.0;
        if (v < -180.0) v += 360.0;
        return v;
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

    function writeQuaternionFromPitchYaw(buffer, pitchDeg, yawDeg) {
        var pitch = pitchDeg * Math.PI / 180.0;
        var yaw = yawDeg * Math.PI / 180.0;
        var hp = pitch * 0.5;
        var hy = yaw * 0.5;
        var sx = Math.sin(hp);
        var cx = Math.cos(hp);
        var sy = Math.sin(hy);
        var cy = Math.cos(hy);
        buffer.writeFloat(cy * sx);
        buffer.add(4).writeFloat(sy * cx);
        buffer.add(8).writeFloat(-sy * sx);
        buffer.add(12).writeFloat(cy * cx);
    }

    function initNativeFunctions() {
        if (state.nativeReady) return true;
        if (!state.moduleOk || !state.archOk) return false;

        try {
            native.isMyPlayer = new NativeFunction(base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer'], CALL_CONV);
            native.brainGetOutputCamera = new NativeFunction(base.add(RVA.Brain_get_OutputCamera), 'pointer', ['pointer', 'pointer'], CALL_CONV);
            native.componentGetTransform = new NativeFunction(base.add(RVA.Component_get_transform), 'pointer', ['pointer', 'pointer'], CALL_CONV);
            native.transformGetPosition = new NativeFunction(base.add(RVA.Transform_get_position_Injected), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
            native.transformGetForward = new NativeFunction(base.add(RVA.Transform_get_forward_Injected), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
            native.transformSetPosition = new NativeFunction(base.add(RVA.Transform_set_position_Injected), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
            native.transformSetRotation = new NativeFunction(base.add(RVA.Transform_set_rotation_Injected), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
            state.nativeReady = true;
            return true;
        } catch (e) {
            setError('初始化 NativeFunction 失败', e);
            state.nativeReady = false;
            return false;
        }
    }

    function isLocalPlayer(player) {
        if (isNull(player) || !state.nativeReady) return false;

        if (!isNull(state.localPlayer) && player.equals(state.localPlayer)) return true;

        try {
            if (native.isMyPlayer(player, ptr(0))) {
                state.localPlayer = player;
                return true;
            }
        } catch (_) {
        }

        return false;
    }

    function readTransformPosition(transform) {
        if (isNull(transform) || !state.nativeReady) return null;
        try {
            native.transformGetPosition(transform, posBuffer, ptr(0));
            return readVector3(posBuffer);
        } catch (_) {
            return null;
        }
    }

    function readTransformForward(transform) {
        if (isNull(transform) || !state.nativeReady) return null;
        try {
            native.transformGetForward(fwdBuffer, transform, ptr(0));
            var v = readVector3(fwdBuffer);
            if (v === null) return null;
            var len = Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
            if (!isFinite(len) || len < 0.00001) return null;
            return { x: v.x / len, y: v.y / len, z: v.z / len };
        } catch (_) {
            return null;
        }
    }

    function yawPitchFromForward(fwd) {
        if (fwd === null) return null;
        var h = Math.sqrt(fwd.x * fwd.x + fwd.z * fwd.z);
        if (!isFinite(h) || h < 0.00001) return null;
        return {
            yaw: normalizeAngle(Math.atan2(fwd.x / h, fwd.z / h) * 180.0 / Math.PI),
            pitch: clamp(Math.asin(clamp(-fwd.y, -1.0, 1.0)) * 180.0 / Math.PI, config.pitchMin, config.pitchMax)
        };
    }

    function resetCameraRuntime() {
        state.camera.valid = false;
        state.camera.initialized = false;
        state.camera.lastFrameMs = 0;
        state.camera.lastTransform = null;
    }

    function updateInputFromPlayer(player) {
        if (!state.enabled || !isLocalPlayer(player)) return;
        try {
            var yaw = player.add(OFF.Player_cameraRotation).readFloat();
            var pitchRaw = player.add(OFF.Player_cameraRotation + 4).readFloat();
            if (!isFinite(yaw) || !isFinite(pitchRaw)) return;

            state.input.valid = true;
            state.input.yaw = normalizeAngle(yaw);
            state.input.pitch = clamp(-pitchRaw, config.pitchMin, config.pitchMax);
            state.input.lastSampleMs = Date.now();
            state.camera.yaw = state.input.yaw;
            state.camera.pitch = state.input.pitch;
            state.stats.inputSamples++;
        } catch (e) {
            setError('读取玩家相机输入失败', e);
        }
    }

    function updateMovementInput(returnBuffer, player, displayClass) {
        if (!state.enabled || isNull(displayClass) || !isLocalPlayer(player)) return;
        try {
            var ix = displayClass.readS32();
            var iz = displayClass.add(4).readS32();
            state.moveInput.x = ix;
            state.moveInput.z = iz;
            state.moveInput.valid = true;
            state.moveInput.lastSampleMs = Date.now();
            state.stats.movementSamples++;

            if (config.lockPlayerMove && !isNull(returnBuffer)) {
                var y = returnBuffer.add(4).readFloat();
                if (!isFinite(y)) y = 0.0;
                returnBuffer.writeFloat(0.0);
                returnBuffer.add(4).writeFloat(y);
                returnBuffer.add(8).writeFloat(0.0);
                state.stats.zeroWalkVelocity++;
            }
        } catch (_) {
        }
    }

    function getMove(now) {
        if (!state.moveInput.valid || now - state.moveInput.lastSampleMs > config.inputStaleMs) {
            return { x: 0.0, z: 0.0 };
        }
        return { x: state.moveInput.x, z: state.moveInput.z };
    }

    function initializeCameraFromTransform(transform) {
        var pos = readTransformPosition(transform);
        if (pos === null) return false;
        var fwd = readTransformForward(transform);
        var ang = yawPitchFromForward(fwd);

        state.camera.x = pos.x;
        state.camera.y = pos.y;
        state.camera.z = pos.z;
        if (state.input.valid) {
            state.camera.yaw = state.input.yaw;
            state.camera.pitch = state.input.pitch;
        } else if (ang !== null) {
            state.camera.yaw = ang.yaw;
            state.camera.pitch = ang.pitch;
        }

        state.camera.initialized = true;
        state.camera.valid = true;
        state.camera.lastFrameMs = Date.now();
        state.camera.lastTransform = transform;
        sendLog('info', '自由相机已初始化', { x: state.camera.x, y: state.camera.y, z: state.camera.z });
        return true;
    }

    function updateFreeCamera(brain) {
        if (!state.enabled || !state.nativeReady || isNull(brain)) return false;

        var camera = null;
        var transform = null;

        try {
            camera = native.brainGetOutputCamera(brain, ptr(0));
            if (isNull(camera)) return false;
            transform = native.componentGetTransform(camera, ptr(0));
            if (isNull(transform)) return false;
        } catch (e) {
            state.stats.cameraFailures++;
            setError('获取输出相机失败', e);
            return false;
        }

        if (!state.camera.initialized) {
            if (!initializeCameraFromTransform(transform)) {
                state.stats.cameraFailures++;
                return false;
            }
        }

        var now = Date.now();
        var dt = state.camera.lastFrameMs === 0 ? 1.0 / 60.0 : Math.max(0.001, Math.min(0.04, (now - state.camera.lastFrameMs) / 1000.0));
        state.camera.lastFrameMs = now;
        state.camera.lastTransform = transform;

        var yawRad = state.camera.yaw * Math.PI / 180.0;
        var pitchRad = state.camera.pitch * Math.PI / 180.0;
        var move = getMove(now);
        var mx = move.x;
        var mz = move.z;
        var len = Math.sqrt(mx * mx + mz * mz);

        if (len > 0.00001) {
            mx /= len;
            mz /= len;
            var fx = Math.sin(yawRad);
            var fz = Math.cos(yawRad);
            var rx = Math.cos(yawRad);
            var rz = -Math.sin(yawRad);
            state.camera.x += (fx * mz + rx * mx) * config.moveSpeed * dt;
            state.camera.z += (fz * mz + rz * mx) * config.moveSpeed * dt;
            state.stats.moveFrames++;
        }

        writeVector3(writePosBuffer, state.camera.x, state.camera.y, state.camera.z);
        writeQuaternionFromPitchYaw(writeRotBuffer, state.camera.pitch, state.camera.yaw);

        try {
            native.transformSetPosition(transform, writePosBuffer, ptr(0));
            native.transformSetRotation(transform, writeRotBuffer, ptr(0));
            state.camera.valid = true;
            state.stats.cameraFrames++;
            state.stats.cameraWrites++;
            return true;
        } catch (e) {
            state.stats.cameraFailures++;
            setError('写入自由相机失败', e);
            resetCameraRuntime();
            return false;
        }
    }

    function attachHook(name, rva, callbacks) {
        var address = base.add(rva);
        if (!isExecutable(address)) throw new Error(name + ' 地址不可执行: ' + address);
        var listener = Interceptor.attach(address, callbacks);
        state.listeners.push(listener);
        state.stats.hooksInstalled++;
        sendLog('info', 'Hook 已安装: ' + name);
    }

    function installHooks() {
        if (state.installed) return { ok: true, installed: true };
        if (!state.moduleOk || !state.archOk) return { ok: false, error: state.lastError || 'module/arch not ready' };
        if (!initNativeFunctions()) return { ok: false, error: state.lastError || 'NativeFunction init failed' };

        try {
            attachHook('Player.UpdateCameraRotaion', RVA.Player_UpdateCameraRotaion, {
                onEnter: function (args) { this.player = args[0]; },
                onLeave: function () { updateInputFromPlayer(this.player); }
            });

            attachHook('Player.GetWalkVelocity', RVA.Player_GetWalkVelocity, {
                onEnter: function (args) {
                    this.returnBuffer = args[0];
                    this.player = args[1];
                    this.displayClass = args[2];
                },
                onLeave: function () { updateMovementInput(this.returnBuffer, this.player, this.displayClass); }
            });

            attachHook('CinemachineBrain.PushStateToUnityCamera', RVA.Brain_PushStateToUnityCamera, {
                onEnter: function (args) { this.brain = args[0]; },
                onLeave: function () { updateFreeCamera(this.brain); }
            });

            state.installed = true;
            state.lastError = null;
            return { ok: true, installed: true };
        } catch (e) {
            state.stats.hookFailures++;
            setError('安装 Hook 失败', e);
            removeHooks();
            return { ok: false, error: state.lastError };
        }
    }

    function removeHooks() {
        for (var i = 0; i < state.listeners.length; i++) {
            try { state.listeners[i].detach(); } catch (_) {}
        }
        state.listeners = [];
        state.installed = false;
    }

    function updateConfig(input) {
        if (!input) return { ok: true, config: config };
        if (input.moveSpeed !== undefined) {
            var speed = Number(input.moveSpeed);
            if (!isFinite(speed) || speed < 1.0 || speed > 50.0) return { ok: false, error: 'moveSpeed 必须在 1.0～50.0' };
            config.moveSpeed = speed;
        }
        if (input.lockPlayerMove !== undefined) config.lockPlayerMove = !!input.lockPlayerMove;
        return { ok: true, config: config };
    }

    rpc.exports = {
        enable: function () {
            var r = installHooks();
            if (!r.ok) return r;
            state.enabled = true;
            resetCameraRuntime();
            sendLog('info', '自由视角已开启', { lockPlayerMove: config.lockPlayerMove, speed: config.moveSpeed });
            return { ok: true, enabled: true, message: '自由视角已开启' };
        },
        disable: function () {
            state.enabled = false;
            resetCameraRuntime();
            sendLog('info', '自由视角已关闭');
            return { ok: true, enabled: false, message: '自由视角已关闭' };
        },
        configure: function (input) {
            return updateConfig(input || {});
        },
        status: function () {
            return {
                ok: true,
                moduleOk: state.moduleOk,
                archOk: state.archOk,
                nativeReady: state.nativeReady,
                installed: state.installed,
                enabled: state.enabled,
                cameraValid: state.camera.valid,
                cameraInitialized: state.camera.initialized,
                inputValid: state.input.valid,
                movementInputValid: state.moveInput.valid,
                x: state.camera.x,
                y: state.camera.y,
                z: state.camera.z,
                yaw: state.camera.yaw,
                pitch: state.camera.pitch,
                moveInputX: state.moveInput.x,
                moveInputZ: state.moveInput.z,
                config: config,
                stats: state.stats,
                lastError: state.lastError
            };
        },
        cleanup: function () {
            state.enabled = false;
            resetCameraRuntime();
            removeHooks();
            sendLog('info', 'cleanup 完成');
            return { ok: true, enabled: false, installed: state.installed };
        }
    };

    sendLog('info', 'free_camera_v1_2.js loaded');
})();
