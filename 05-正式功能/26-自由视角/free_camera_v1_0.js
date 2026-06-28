// ============================================================
// free_camera_v1_0.js
//
// 自由视角 / Free Camera v1.0
//
// 控制：
//   鼠标：控制相机朝向，复用游戏 Player.cameraRotation 数据。
//   W/A/S/D：控制相机在水平面自由移动。
//   暂不实现：空格上升、Ctrl/Shift 下降或加速。
//
// 规则：
//   不调用 IL2CPP API / 反射 API。
//   不调用 il2cpp_runtime_class_init / il2cpp_class_* / il2cpp_field_*。
//   只使用固定 RVA、固定字段偏移、Hook、WinAPI GetAsyncKeyState。
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

    if (module === null) {
        sendLog('error', MODULE_NAME + ' 未加载');
        return;
    }

    if (Process.arch !== 'ia32' || Process.pointerSize !== 4) {
        sendLog('error', '只支持 32 位 x86 游戏进程', {
            arch: Process.arch,
            pointerSize: Process.pointerSize
        });
        return;
    }

    var base = module.base;
    var CALL_CONV = 'mscdecl';
    var PTR_SIZE = 4;

    var RVA = {
        CameraManager_Awake:                   0x00B35550,
        CameraManager_Update:                  0x00B36FA0,
        CameraManager_OnDestroy:               0x00B360E0,

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
        CM_focusPlayer:             0x0C,
        Player_cameraRotation:      0x4C
    };

    var VK = {
        W: 0x57,
        A: 0x41,
        S: 0x53,
        D: 0x44
    };

    var config = {
        moveSpeed: 8.0,
        pitchMin: -80.0,
        pitchMax: 80.0,
        lockPlayerMove: true
    };

    var state = {
        installed: false,
        enabled: false,
        pendingEnable: false,
        pendingDisable: false,
        commandBusy: false,
        cameraManager: null,
        localPlayer: null,
        listeners: [],
        camera: {
            valid: false,
            camera: null,
            transform: null,
            initialized: false,
            x: 0.0,
            y: 0.0,
            z: 0.0,
            yaw: 0.0,
            pitch: 0.0,
            lastFrameMs: 0
        },
        input: {
            valid: false,
            yaw: 0.0,
            pitch: 0.0,
            lastSampleMs: 0
        },
        stats: {
            cameraFrames: 0,
            moveFrames: 0,
            zeroWalkVelocity: 0,
            cameraFailures: 0,
            inputSamples: 0,
            errors: 0
        },
        lastError: null
    };

    var posBuffer = Memory.alloc(12);
    var fwdBuffer = Memory.alloc(12);
    var writePosBuffer = Memory.alloc(12);
    var writeRotBuffer = Memory.alloc(16);

    function isNull(p) {
        if (p === null || p === undefined) return true;
        try {
            return p.isNull();
        } catch (_) {
            return true;
        }
    }

    function isReadable(p) {
        if (isNull(p)) return false;
        try {
            var range = Process.findRangeByAddress(p);
            return range !== null && range.protection.indexOf('r') !== -1;
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

    function fail(label, error) {
        state.stats.errors++;
        state.lastError = label + ': ' + error;
        if (state.stats.errors <= 8) {
            sendLog('error', state.lastError);
        }
    }

    function clamp(value, minValue, maxValue) {
        return Math.max(minValue, Math.min(maxValue, value));
    }

    function normalizeAngle(angle) {
        var value = angle % 360.0;
        if (value > 180.0) value -= 360.0;
        if (value < -180.0) value += 360.0;
        return value;
    }

    function keyDown(vk) {
        try {
            return (getAsyncKeyState(vk) & 0x8000) !== 0;
        } catch (_) {
            return false;
        }
    }

    function readVector3FromBuffer(buffer) {
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
        var pitchRadians = pitchDeg * Math.PI / 180.0;
        var yawRadians = yawDeg * Math.PI / 180.0;

        var halfPitch = pitchRadians * 0.5;
        var halfYaw = yawRadians * 0.5;

        var sx = Math.sin(halfPitch);
        var cx = Math.cos(halfPitch);
        var sy = Math.sin(halfYaw);
        var cy = Math.cos(halfYaw);

        buffer.writeFloat(cy * sx);
        buffer.add(4).writeFloat(sy * cx);
        buffer.add(8).writeFloat(-sy * sx);
        buffer.add(12).writeFloat(cy * cx);
    }

    function readTransformPosition(transform) {
        if (isNull(transform)) return null;
        try {
            transformGetPosition(transform, posBuffer, ptr(0));
            return readVector3FromBuffer(posBuffer);
        } catch (_) {
            return null;
        }
    }

    function readTransformForward(transform) {
        if (isNull(transform)) return null;
        try {
            transformGetForward(fwdBuffer, transform, ptr(0));
            var v = readVector3FromBuffer(fwdBuffer);
            if (v === null) return null;

            var length = Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
            if (!isFinite(length) || length < 0.00001) return null;

            return {
                x: v.x / length,
                y: v.y / length,
                z: v.z / length
            };
        } catch (_) {
            return null;
        }
    }

    function yawPitchFromForward(fwd) {
        if (fwd === null) return null;

        var horizontal = Math.sqrt(fwd.x * fwd.x + fwd.z * fwd.z);
        if (!isFinite(horizontal) || horizontal < 0.00001) return null;

        var yaw = Math.atan2(fwd.x / horizontal, fwd.z / horizontal) * 180.0 / Math.PI;
        var pitch = Math.asin(clamp(-fwd.y, -1.0, 1.0)) * 180.0 / Math.PI;

        return {
            yaw: normalizeAngle(yaw),
            pitch: clamp(pitch, config.pitchMin, config.pitchMax)
        };
    }

    var isMyPlayer = new NativeFunction(
        base.add(RVA.Player_get_isMyPlayer),
        'bool',
        ['pointer', 'pointer'],
        CALL_CONV
    );

    var brainGetOutputCamera = new NativeFunction(
        base.add(RVA.Brain_get_OutputCamera),
        'pointer',
        ['pointer', 'pointer'],
        CALL_CONV
    );

    var componentGetTransform = new NativeFunction(
        base.add(RVA.Component_get_transform),
        'pointer',
        ['pointer', 'pointer'],
        CALL_CONV
    );

    var transformGetPosition = new NativeFunction(
        base.add(RVA.Transform_get_position_Injected),
        'void',
        ['pointer', 'pointer', 'pointer'],
        CALL_CONV
    );

    var transformGetForward = new NativeFunction(
        base.add(RVA.Transform_get_forward_Injected),
        'void',
        ['pointer', 'pointer', 'pointer'],
        CALL_CONV
    );

    var transformSetPosition = new NativeFunction(
        base.add(RVA.Transform_set_position_Injected),
        'void',
        ['pointer', 'pointer', 'pointer'],
        CALL_CONV
    );

    var transformSetRotation = new NativeFunction(
        base.add(RVA.Transform_set_rotation_Injected),
        'void',
        ['pointer', 'pointer', 'pointer'],
        CALL_CONV
    );

    var getAsyncKeyStateAddr = Module.findExportByName('user32.dll', 'GetAsyncKeyState');
    if (getAsyncKeyStateAddr === null) {
        sendLog('error', 'user32!GetAsyncKeyState 未找到');
        return;
    }

    var getAsyncKeyState = new NativeFunction(
        getAsyncKeyStateAddr,
        'int16',
        ['int']
    );

    function cacheCameraManager(manager, source) {
        if (isNull(manager) || !isReadable(manager)) return false;

        var changed = isNull(state.cameraManager) || !state.cameraManager.equals(manager);
        state.cameraManager = manager;

        if (changed) {
            state.localPlayer = null;
            sendLog('info', 'CameraManager 已捕获', {
                pointer: manager.toString(),
                source: source || 'unknown'
            });
        }

        tryCacheLocalPlayerFromCameraManager();
        return true;
    }

    function tryCacheLocalPlayerFromCameraManager() {
        var manager = state.cameraManager;
        if (isNull(manager) || !isReadable(manager)) return false;

        try {
            var focusPlayer = manager.add(OFF.CM_focusPlayer).readPointer();
            if (isNull(focusPlayer) || !isReadable(focusPlayer)) return false;

            if (isMyPlayer(focusPlayer, ptr(0))) {
                state.localPlayer = focusPlayer;
                return true;
            }
        } catch (_) {
        }

        return false;
    }

    function isLocalPlayer(player) {
        if (isNull(player)) return false;

        if (!isNull(state.localPlayer) && player.equals(state.localPlayer)) {
            return true;
        }

        try {
            if (isReadable(player) && isMyPlayer(player, ptr(0))) {
                state.localPlayer = player;
                return true;
            }
        } catch (_) {
        }

        return false;
    }

    function resetCameraRuntime() {
        state.camera.valid = false;
        state.camera.camera = null;
        state.camera.transform = null;
        state.camera.initialized = false;
        state.camera.lastFrameMs = 0;
    }

    function acquireOutputCameraTransform(brain) {
        if (isNull(brain)) return false;

        try {
            if (isNull(state.camera.transform) || !isReadable(state.camera.transform)) {
                var camera = brainGetOutputCamera(brain, ptr(0));
                if (isNull(camera) || !isReadable(camera)) return false;

                var transform = componentGetTransform(camera, ptr(0));
                if (isNull(transform) || !isReadable(transform)) return false;

                state.camera.camera = camera;
                state.camera.transform = transform;
            }

            return true;
        } catch (error) {
            fail('获取输出相机 Transform 失败', error);
            return false;
        }
    }

    function initializeFreeCameraFromCurrentTransform() {
        var transform = state.camera.transform;
        if (isNull(transform)) return false;

        var position = readTransformPosition(transform);
        if (position === null) return false;

        var forward = readTransformForward(transform);
        var angles = yawPitchFromForward(forward);

        state.camera.x = position.x;
        state.camera.y = position.y;
        state.camera.z = position.z;

        if (state.input.valid) {
            state.camera.yaw = state.input.yaw;
            state.camera.pitch = state.input.pitch;
        } else if (angles !== null) {
            state.camera.yaw = angles.yaw;
            state.camera.pitch = angles.pitch;
        }

        state.camera.initialized = true;
        state.camera.valid = true;
        state.camera.lastFrameMs = Date.now();

        sendLog('info', '自由相机已初始化', {
            x: state.camera.x,
            y: state.camera.y,
            z: state.camera.z,
            yaw: state.camera.yaw,
            pitch: state.camera.pitch
        });

        return true;
    }

    function updateInputFromPlayer(player) {
        if (!state.enabled || !isLocalPlayer(player)) return;

        try {
            var yaw = player.add(OFF.Player_cameraRotation).readFloat();
            var pitchRaw = player.add(OFF.Player_cameraRotation + 4).readFloat();

            if (!isFinite(yaw) || !isFinite(pitchRaw)) return;

            /*
             * 复用第三人称已验证的方向关系：
             * 游戏 cameraRotation.y 与 Unity pitch 写入方向相反。
             */
            var pitch = -pitchRaw;

            state.input.valid = true;
            state.input.yaw = normalizeAngle(yaw);
            state.input.pitch = clamp(pitch, config.pitchMin, config.pitchMax);
            state.input.lastSampleMs = Date.now();

            state.camera.yaw = state.input.yaw;
            state.camera.pitch = state.input.pitch;
            state.stats.inputSamples++;
        } catch (error) {
            fail('读取玩家相机输入失败', error);
        }
    }

    function updateFreeCamera(brain) {
        if (!state.enabled) return false;

        if (!acquireOutputCameraTransform(brain)) {
            state.stats.cameraFailures++;
            return false;
        }

        if (!state.camera.initialized) {
            if (!initializeFreeCameraFromCurrentTransform()) {
                state.stats.cameraFailures++;
                return false;
            }
        }

        var now = Date.now();
        var dt = state.camera.lastFrameMs === 0
            ? 1.0 / 60.0
            : Math.max(0.001, Math.min(0.05, (now - state.camera.lastFrameMs) / 1000.0));
        state.camera.lastFrameMs = now;

        var yawRad = state.camera.yaw * Math.PI / 180.0;
        var pitchRad = state.camera.pitch * Math.PI / 180.0;

        var moveX = 0.0;
        var moveZ = 0.0;

        if (keyDown(VK.W)) moveZ += 1.0;
        if (keyDown(VK.S)) moveZ -= 1.0;
        if (keyDown(VK.D)) moveX += 1.0;
        if (keyDown(VK.A)) moveX -= 1.0;

        var moveLen = Math.sqrt(moveX * moveX + moveZ * moveZ);
        if (moveLen > 0.00001) {
            moveX /= moveLen;
            moveZ /= moveLen;

            var forwardX = Math.sin(yawRad);
            var forwardZ = Math.cos(yawRad);
            var rightX = Math.cos(yawRad);
            var rightZ = -Math.sin(yawRad);

            state.camera.x += (forwardX * moveZ + rightX * moveX) * config.moveSpeed * dt;
            state.camera.z += (forwardZ * moveZ + rightZ * moveX) * config.moveSpeed * dt;
            state.stats.moveFrames++;
        }

        var cosPitch = Math.cos(pitchRad);
        var fwdX = Math.sin(yawRad) * cosPitch;
        var fwdY = -Math.sin(pitchRad);
        var fwdZ = Math.cos(yawRad) * cosPitch;

        writeVector3(writePosBuffer, state.camera.x, state.camera.y, state.camera.z);
        writeQuaternionFromPitchYaw(writeRotBuffer, state.camera.pitch, state.camera.yaw);

        try {
            transformSetPosition(state.camera.transform, writePosBuffer, ptr(0));
            transformSetRotation(state.camera.transform, writeRotBuffer, ptr(0));

            state.camera.valid = true;
            state.camera.forwardX = fwdX;
            state.camera.forwardY = fwdY;
            state.camera.forwardZ = fwdZ;
            state.stats.cameraFrames++;
            return true;
        } catch (error) {
            state.stats.cameraFailures++;
            fail('写入自由相机 Transform 失败', error);
            resetCameraRuntime();
            return false;
        }
    }

    function zeroLocalWalkVelocity(returnBuffer, player) {
        if (!state.enabled || !config.lockPlayerMove) return;
        if (isNull(returnBuffer) || !isLocalPlayer(player)) return;

        try {
            var originalY = returnBuffer.add(4).readFloat();
            if (!isFinite(originalY)) originalY = 0.0;

            returnBuffer.writeFloat(0.0);
            returnBuffer.add(4).writeFloat(originalY);
            returnBuffer.add(8).writeFloat(0.0);

            state.stats.zeroWalkVelocity++;
        } catch (_) {
        }
    }

    function performEnable() {
        state.pendingEnable = false;
        state.pendingDisable = false;

        if (state.enabled) {
            return { ok: true, enabled: true, message: '已经开启' };
        }

        state.commandBusy = true;
        resetCameraRuntime();
        tryCacheLocalPlayerFromCameraManager();

        state.enabled = true;
        state.commandBusy = false;

        sendLog('info', '自由视角已开启', {
            move: 'W/A/S/D',
            vertical: false,
            speed: config.moveSpeed,
            lockPlayerMove: config.lockPlayerMove
        });

        return { ok: true, enabled: true, message: '自由视角已开启' };
    }

    function performDisable() {
        state.pendingEnable = false;
        state.pendingDisable = false;

        if (!state.enabled) {
            return { ok: true, enabled: false, message: '已经关闭' };
        }

        state.commandBusy = true;
        state.enabled = false;
        resetCameraRuntime();
        state.commandBusy = false;

        sendLog('info', '自由视角已关闭');
        return { ok: true, enabled: false, message: '自由视角已关闭' };
    }

    function processCommands() {
        if (state.commandBusy) return;

        if (state.pendingDisable) {
            performDisable();
            return;
        }

        if (state.pendingEnable) {
            performEnable();
        }
    }

    function attachHook(name, rva, callbacks) {
        var address = base.add(rva);
        if (!isExecutable(address)) {
            throw new Error(name + ' 地址不可执行: ' + address);
        }

        var listener = Interceptor.attach(address, callbacks);
        state.listeners.push(listener);

        sendLog('info', 'Hook 已安装: ' + name, {
            rva: '0x' + rva.toString(16),
            address: address.toString()
        });
    }

    function installHooks() {
        if (state.installed) {
            return { ok: true, installed: true };
        }

        try {
            attachHook('CameraManager.Awake', RVA.CameraManager_Awake, {
                onEnter: function (args) {
                    cacheCameraManager(args[0], 'CameraManager.Awake');
                }
            });

            attachHook('CameraManager.Update', RVA.CameraManager_Update, {
                onEnter: function (args) {
                    cacheCameraManager(args[0], 'CameraManager.Update');
                },
                onLeave: function () {
                    processCommands();
                }
            });

            attachHook('CameraManager.OnDestroy', RVA.CameraManager_OnDestroy, {
                onEnter: function (args) {
                    if (!isNull(state.cameraManager) && args[0].equals(state.cameraManager)) {
                        state.cameraManager = null;
                        state.localPlayer = null;
                        resetCameraRuntime();
                    }
                }
            });

            attachHook('Player.UpdateCameraRotaion', RVA.Player_UpdateCameraRotaion, {
                onEnter: function (args) {
                    this.player = args[0];
                },
                onLeave: function () {
                    updateInputFromPlayer(this.player);
                }
            });

            attachHook('Player.GetWalkVelocity', RVA.Player_GetWalkVelocity, {
                onEnter: function (args) {
                    this.returnBuffer = args[0];
                    this.player = args[1];
                },
                onLeave: function () {
                    zeroLocalWalkVelocity(this.returnBuffer, this.player);
                }
            });

            attachHook('CinemachineBrain.PushStateToUnityCamera', RVA.Brain_PushStateToUnityCamera, {
                onEnter: function (args) {
                    this.brain = args[0];
                },
                onLeave: function () {
                    if (state.enabled) {
                        updateFreeCamera(this.brain);
                    }
                }
            });

            state.installed = true;
            return { ok: true, installed: true };
        } catch (error) {
            fail('安装 Hook 失败', error);
            return { ok: false, error: String(error) };
        }
    }

    function removeHooks() {
        for (var i = 0; i < state.listeners.length; i++) {
            try {
                state.listeners[i].detach();
            } catch (_) {
            }
        }
        state.listeners = [];
        state.installed = false;
    }

    function updateConfig(input) {
        if (!input) {
            return { ok: true, config: config };
        }

        if (input.moveSpeed !== undefined) {
            var speed = Number(input.moveSpeed);
            if (!isFinite(speed) || speed < 1.0 || speed > 50.0) {
                return { ok: false, error: 'moveSpeed 必须在 1.0～50.0' };
            }
            config.moveSpeed = speed;
        }

        if (input.lockPlayerMove !== undefined) {
            config.lockPlayerMove = !!input.lockPlayerMove;
        }

        return { ok: true, config: config };
    }

    installHooks();

    rpc.exports = {
        enable: function () {
            var result = installHooks();
            if (!result.ok) return result;

            state.pendingEnable = true;
            state.pendingDisable = false;

            return {
                ok: true,
                enabled: state.enabled,
                queued: true,
                message: state.enabled ? '已经开启' : '开启命令已排队'
            };
        },

        disable: function () {
            state.pendingDisable = true;
            state.pendingEnable = false;

            return {
                ok: true,
                enabled: state.enabled,
                queued: true,
                message: '关闭命令已排队'
            };
        },

        configure: function (input) {
            return updateConfig(input || {});
        },

        status: function () {
            return {
                ok: true,
                installed: state.installed,
                enabled: state.enabled,
                pendingEnable: state.pendingEnable,
                pendingDisable: state.pendingDisable,
                cameraValid: state.camera.valid,
                cameraInitialized: state.camera.initialized,
                inputValid: state.input.valid,
                x: state.camera.x,
                y: state.camera.y,
                z: state.camera.z,
                yaw: state.camera.yaw,
                pitch: state.camera.pitch,
                config: config,
                stats: state.stats,
                lastError: state.lastError
            };
        },

        cleanup: function () {
            state.pendingEnable = false;
            state.pendingDisable = false;
            state.enabled = false;
            resetCameraRuntime();
            removeHooks();
            sendLog('info', 'cleanup 完成');
            return { ok: true, enabled: false, installed: state.installed };
        }
    };

    sendLog('info', 'free_camera_v1_0.js loaded');
})();
