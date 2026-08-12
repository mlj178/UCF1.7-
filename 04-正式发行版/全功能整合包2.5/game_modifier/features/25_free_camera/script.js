// ============================================================
// free_camera_v1_3.js
//
// 自由视角 / Free Camera v1.3 - Soul Camera
//
// v1.3 目标：
//   真正脱离人物模型的位置绑定。
//   开启瞬间只从当前最终相机取一次初始位置。
//   之后相机位置完全由 freeCam.x/y/z 独立维护。
//
// 控制：
//   鼠标：继续复用游戏 Player.cameraRotation 的 yaw/pitch 输入。
//   W/S：沿镜头 forward 飞行。抬头按 W 上天，低头按 W 入地。
//   A/D：水平左右平移。
//   暂不使用空格上升、Ctrl/Shift 下降或加速。
//
// 修复：
//   1. 不再使用人物 CharacterContainer / CameraManager 作为相机位置来源。
//   2. 不再把自由相机跟随人物。
//   3. 不再用 Player.GetWalkVelocity 作为主要输入源。
//   4. 使用 WinAPI GetAsyncKeyState 读取 WASD；带多种安全解析方式。
//   5. 如果 WinAPI 不可用，才降级为 Player.GetWalkVelocity 的 displayClass 输入。
//   6. 点击开启才安装 Hook，不再脚本加载时预安装。
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

    function sendStatus(feature, enabled) {
        try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (_) {}
    }

    var state = {
        moduleOk: false,
        archOk: false,
        installed: false,
        enabled: false,
        pendingApply: false,
        applied: false,
        generation: 0,
        roomGeneration: 0,
        lastResetReason: '',
        lastApplyReason: '',
        lastRoomReadyReason: '',
        lastRoomReadyAt: 0,
        cameraTransform: null,
        localPlayer: null,
        listeners: [],
        inputMode: 'none',
        keyApiReady: false,
        getAsyncKeyState: null,
        freeCam: {
            initialized: false,
            valid: false,
            x: 0.0,
            y: 0.0,
            z: 0.0,
            yaw: 0.0,
            pitch: 0.0,
            lastFrameMs: 0,
            forwardX: 0.0,
            forwardY: 0.0,
            forwardZ: 1.0
        },
        mouseInput: {
            valid: false,
            yaw: 0.0,
            pitch: 0.0,
            lastSampleMs: 0
        },
        fallbackMoveInput: {
            valid: false,
            x: 0.0,
            z: 0.0,
            lastSampleMs: 0
        },
        stats: {
            hooksInstalled: 0,
            hookFailures: 0,
            roomReadyHits: 0,
            cameraFrames: 0,
            movedFrames: 0,
            keyFrames: 0,
            fallbackInputSamples: 0,
            mouseSamples: 0,
            lockPlayerWrites: 0,
            cameraFailures: 0,
            errors: 0,
            cleanupCount: 0
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

        CameraManager_Awake:                   0x00B35550,
        GameManager_Awake:                     0x00AFA250,
        GameManager_OnDestroy:                 0x00AFB6F0,
        ModeBase_Update:                       0x00AF6A00,
        ModeBase_ExitGame:                     0x00AEE850,

        Brain_PushStateToUnityCamera:          0x0082B750,
        Brain_get_OutputCamera:                0x0082CDB0,

        Component_get_transform:               0x0032CF40,
        Transform_get_position_Injected:       0x003F4280,
        Transform_get_forward_Injected:        0x003F3F20,
        Transform_set_position_Injected:       0x003F4810,
        Transform_set_rotation_Injected:       0x003F4870
    };

    var OFF = {
        Player_cameraRotation:      0x4C
    };

    var VK = {
        A: 0x41,
        D: 0x44,
        S: 0x53,
        W: 0x57
    };

    var config = {
        moveSpeed: 30.0,
        pitchMin: -88.0,
        pitchMax: 88.0,
        lockPlayerMove: true,
        fallbackInputStaleMs: 140,
        logEveryFrames: 300
    };

    var posBuffer = Memory.alloc(12);
    var fwdBuffer = Memory.alloc(12);
    var writePosBuffer = Memory.alloc(12);
    var writeRotBuffer = Memory.alloc(16);

    var native = {
        ready: false,
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
        if (state.stats.errors <= 8) sendLog('error', state.lastError);
    }

    function clamp(v, lo, hi) {
        return Math.max(lo, Math.min(hi, v));
    }

    function normalizeAngle(angle) {
        var value = angle % 360.0;
        if (value > 180.0) value -= 360.0;
        if (value < -180.0) value += 360.0;
        return value;
    }

    function safeReadF32(p, fallback) {
        try {
            var v = p.readFloat();
            return isFinite(v) ? v : fallback;
        } catch (_) {
            return fallback;
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
                var m = Process.getModuleByName(moduleName);
                if (m && typeof m.getExportByName === 'function') {
                    addr = m.getExportByName(exportName);
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
            var mod = Process.findModuleByName(moduleName);
            if (mod && typeof mod.enumerateExports === 'function') {
                var exports = mod.enumerateExports();
                for (var i = 0; i < exports.length; i++) {
                    if (exports[i].name === exportName) return exports[i].address;
                }
            }
        } catch (_) {
        }

        return null;
    }

    function initKeyApi() {
        if (state.keyApiReady) return true;

        var addr = resolveExportAddress('user32.dll', 'GetAsyncKeyState');
        if (isNull(addr)) {
            state.inputMode = 'fallback_displayClass';
            sendLog('warning', 'GetAsyncKeyState 未解析到，降级使用 Player.GetWalkVelocity 输入');
            return false;
        }

        try {
            state.getAsyncKeyState = new NativeFunction(addr, 'int16', ['int']);
            state.keyApiReady = true;
            state.inputMode = 'winapi_get_async_key_state';
            sendLog('info', 'GetAsyncKeyState 已启用', { address: addr.toString() });
            return true;
        } catch (error) {
            state.inputMode = 'fallback_displayClass';
            setError('创建 GetAsyncKeyState NativeFunction 失败', error);
            return false;
        }
    }

    function keyDown(vk) {
        if (!state.keyApiReady || state.getAsyncKeyState === null) return false;
        try {
            return (state.getAsyncKeyState(vk) & 0x8000) !== 0;
        } catch (_) {
            return false;
        }
    }

    function initNativeFunctions() {
        if (native.ready) return true;
        if (!state.moduleOk || !state.archOk) return false;

        try {
            native.isMyPlayer = new NativeFunction(base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer'], CALL_CONV);
            native.brainGetOutputCamera = new NativeFunction(base.add(RVA.Brain_get_OutputCamera), 'pointer', ['pointer', 'pointer'], CALL_CONV);
            native.componentGetTransform = new NativeFunction(base.add(RVA.Component_get_transform), 'pointer', ['pointer', 'pointer'], CALL_CONV);
            native.transformGetPosition = new NativeFunction(base.add(RVA.Transform_get_position_Injected), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
            native.transformGetForward = new NativeFunction(base.add(RVA.Transform_get_forward_Injected), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
            native.transformSetPosition = new NativeFunction(base.add(RVA.Transform_set_position_Injected), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
            native.transformSetRotation = new NativeFunction(base.add(RVA.Transform_set_rotation_Injected), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
            native.ready = true;
            return true;
        } catch (error) {
            setError('初始化 NativeFunction 失败', error);
            native.ready = false;
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

    function readTransformPosition(transform) {
        if (isNull(transform) || !native.ready) return null;
        try {
            native.transformGetPosition(transform, posBuffer, ptr(0));
            return readVector3FromBuffer(posBuffer);
        } catch (_) {
            return null;
        }
    }

    function readTransformForward(transform) {
        if (isNull(transform) || !native.ready) return null;
        try {
            native.transformGetForward(fwdBuffer, transform, ptr(0));
            var v = readVector3FromBuffer(fwdBuffer);
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
        var horizontal = Math.sqrt(fwd.x * fwd.x + fwd.z * fwd.z);
        if (!isFinite(horizontal) || horizontal < 0.00001) return null;
        return {
            yaw: normalizeAngle(Math.atan2(fwd.x / horizontal, fwd.z / horizontal) * 180.0 / Math.PI),
            pitch: clamp(Math.asin(clamp(-fwd.y, -1.0, 1.0)) * 180.0 / Math.PI, config.pitchMin, config.pitchMax)
        };
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

    function isLocalPlayer(player) {
        if (isNull(player) || !native.ready) return false;
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

    function resetRuntime(reason) {
        state.generation++;
        state.lastResetReason = reason || 'unknown';
        state.cameraTransform = null;
        state.localPlayer = null;
        state.freeCam.initialized = false;
        state.freeCam.valid = false;
        state.freeCam.lastFrameMs = 0;
        state.mouseInput.valid = false;
        state.mouseInput.lastSampleMs = 0;
        state.fallbackMoveInput.valid = false;
        state.fallbackMoveInput.lastSampleMs = 0;
    }

    function markApplyPending(reason) {
        state.pendingApply = true;
        state.applied = false;
        state.lastApplyReason = reason || 'pending';
    }

    function markApplied(reason) {
        state.pendingApply = false;
        state.applied = true;
        state.lastApplyReason = reason || 'applied';
    }

    function resetFreeCam(reason) {
        resetRuntime(reason || 'free_camera_reset');
        if (state.enabled) markApplyPending(reason || 'free_camera_reset');
    }

    function onRoomReady(reason, forceReset) {
        state.stats.roomReadyHits++;
        state.lastRoomReadyReason = reason || 'room_ready';
        state.lastRoomReadyAt = Date.now();
        if (!state.enabled) return;
        if (forceReset || state.applied || !state.pendingApply) {
            resetFreeCam(reason || 'room_ready');
        } else {
            markApplyPending(reason || 'room_ready');
        }
    }

    function onRoomExit(reason) {
        state.roomGeneration++;
        state.lastRoomReadyReason = reason || 'room_exit';
        state.lastRoomReadyAt = Date.now();
        resetFreeCam(reason || 'room_exit');
    }

    function acquireOutputCameraTransform(brain) {
        if (isNull(brain) || !native.ready) return null;
        try {
            var camera = native.brainGetOutputCamera(brain, ptr(0));
            if (isNull(camera)) return null;
            var transform = native.componentGetTransform(camera, ptr(0));
            if (isNull(transform)) return null;
            state.cameraTransform = transform;
            return transform;
        } catch (error) {
            state.stats.cameraFailures++;
            if (state.stats.cameraFailures <= 3) setError('获取最终相机 Transform 失败', error);
            return null;
        }
    }

    function initFreeCamFromCurrentCamera(transform) {
        var pos = readTransformPosition(transform);
        if (pos === null) return false;

        var fwd = readTransformForward(transform);
        var angles = yawPitchFromForward(fwd);

        state.freeCam.x = pos.x;
        state.freeCam.y = pos.y;
        state.freeCam.z = pos.z;

        if (state.mouseInput.valid) {
            state.freeCam.yaw = state.mouseInput.yaw;
            state.freeCam.pitch = state.mouseInput.pitch;
        } else if (angles !== null) {
            state.freeCam.yaw = angles.yaw;
            state.freeCam.pitch = angles.pitch;
        }

        state.freeCam.initialized = true;
        state.freeCam.valid = true;
        state.freeCam.lastFrameMs = Date.now();
        markApplied('camera_ready');

        sendLog('info', '灵魂相机初始化完成', {
            x: state.freeCam.x,
            y: state.freeCam.y,
            z: state.freeCam.z,
            yaw: state.freeCam.yaw,
            pitch: state.freeCam.pitch
        });

        return true;
    }

    function updateMouseFromPlayer(player) {
        if (!state.enabled || !isLocalPlayer(player)) return;

        try {
            var yaw = safeReadF32(player.add(OFF.Player_cameraRotation), state.freeCam.yaw);
            var pitchRaw = safeReadF32(player.add(OFF.Player_cameraRotation + 4), -state.freeCam.pitch);
            var pitch = -pitchRaw;

            state.mouseInput.valid = true;
            state.mouseInput.yaw = normalizeAngle(yaw);
            state.mouseInput.pitch = clamp(pitch, config.pitchMin, config.pitchMax);
            state.mouseInput.lastSampleMs = Date.now();

            state.freeCam.yaw = state.mouseInput.yaw;
            state.freeCam.pitch = state.mouseInput.pitch;
            state.stats.mouseSamples++;
        } catch (error) {
            setError('读取鼠标视角输入失败', error);
        }
    }

    function updateFallbackMoveInput(returnBuffer, player, displayClass) {
        if (!state.enabled || isNull(displayClass) || !isLocalPlayer(player)) return;

        try {
            state.fallbackMoveInput.x = displayClass.readS32();
            state.fallbackMoveInput.z = displayClass.add(4).readS32();
            state.fallbackMoveInput.valid = true;
            state.fallbackMoveInput.lastSampleMs = Date.now();
            state.stats.fallbackInputSamples++;

            if (config.lockPlayerMove && !isNull(returnBuffer)) {
                var y = safeReadF32(returnBuffer.add(4), 0.0);
                returnBuffer.writeFloat(0.0);
                returnBuffer.add(4).writeFloat(y);
                returnBuffer.add(8).writeFloat(0.0);
                state.stats.lockPlayerWrites++;
            }
        } catch (_) {
        }
    }

    function getMoveInput(now) {
        if (state.keyApiReady) {
            var x = 0.0;
            var z = 0.0;
            if (keyDown(VK.W)) z += 1.0;
            if (keyDown(VK.S)) z -= 1.0;
            if (keyDown(VK.D)) x += 1.0;
            if (keyDown(VK.A)) x -= 1.0;
            state.stats.keyFrames++;
            return { x: x, z: z, source: 'winapi' };
        }

        if (state.fallbackMoveInput.valid &&
            now - state.fallbackMoveInput.lastSampleMs <= config.fallbackInputStaleMs) {
            return {
                x: state.fallbackMoveInput.x,
                z: state.fallbackMoveInput.z,
                source: 'fallback'
            };
        }

        return { x: 0.0, z: 0.0, source: 'none' };
    }

    function updateSoulCamera(brain) {
        if (!state.enabled || !native.ready) return false;

        var transform = acquireOutputCameraTransform(brain);
        if (isNull(transform)) return false;

        if (!state.freeCam.initialized) {
            if (!initFreeCamFromCurrentCamera(transform)) {
                state.stats.cameraFailures++;
                markApplyPending('camera_not_ready');
                return false;
            }
        } else if (state.pendingApply) {
            markApplied('camera_ready');
        }

        var now = Date.now();
        var dt = state.freeCam.lastFrameMs === 0
            ? 1.0 / 60.0
            : Math.max(0.001, Math.min(0.05, (now - state.freeCam.lastFrameMs) / 1000.0));
        state.freeCam.lastFrameMs = now;

        var yawRad = state.freeCam.yaw * Math.PI / 180.0;
        var pitchRad = state.freeCam.pitch * Math.PI / 180.0;
        var cosPitch = Math.cos(pitchRad);

        var forwardX = Math.sin(yawRad) * cosPitch;
        var forwardY = -Math.sin(pitchRad);
        var forwardZ = Math.cos(yawRad) * cosPitch;

        var rightX = Math.cos(yawRad);
        var rightY = 0.0;
        var rightZ = -Math.sin(yawRad);

        var move = getMoveInput(now);
        var mx = move.x;
        var mz = move.z;
        var len = Math.sqrt(mx * mx + mz * mz);

        if (len > 0.00001) {
            mx /= len;
            mz /= len;
            state.freeCam.x += (forwardX * mz + rightX * mx) * config.moveSpeed * dt;
            state.freeCam.y += (forwardY * mz + rightY * mx) * config.moveSpeed * dt;
            state.freeCam.z += (forwardZ * mz + rightZ * mx) * config.moveSpeed * dt;
            state.stats.movedFrames++;
        }

        writeVector3(writePosBuffer, state.freeCam.x, state.freeCam.y, state.freeCam.z);
        writeQuaternionFromPitchYaw(writeRotBuffer, state.freeCam.pitch, state.freeCam.yaw);

        try {
            native.transformSetPosition(transform, writePosBuffer, ptr(0));
            native.transformSetRotation(transform, writeRotBuffer, ptr(0));

            state.freeCam.valid = true;
            state.freeCam.forwardX = forwardX;
            state.freeCam.forwardY = forwardY;
            state.freeCam.forwardZ = forwardZ;
            state.stats.cameraFrames++;

            if (state.stats.cameraFrames === 1 ||
                state.stats.cameraFrames % config.logEveryFrames === 0) {
                sendLog('info', '灵魂相机运行中', {
                    frame: state.stats.cameraFrames,
                    inputMode: state.inputMode,
                    x: state.freeCam.x,
                    y: state.freeCam.y,
                    z: state.freeCam.z,
                    yaw: state.freeCam.yaw,
                    pitch: state.freeCam.pitch
                });
            }
            return true;
        } catch (error) {
            state.stats.cameraFailures++;
            if (state.stats.cameraFailures <= 3) setError('写入最终相机失败', error);
            resetFreeCam('camera_write_failed');
            return false;
        }
    }

    function attachHook(name, rva, callbacks) {
        var address = base.add(rva);
        if (!isExecutable(address)) throw new Error(name + ' 地址不可执行: ' + address);
        var listener = Interceptor.attach(address, callbacks);
        state.listeners.push(listener);
        state.stats.hooksInstalled++;
        sendLog('info', 'Hook 已安装: ' + name, { rva: '0x' + rva.toString(16), address: address.toString() });
        return true;
    }

    function tryAttachHook(name, rva, callbacks, required) {
        try {
            return attachHook(name, rva, callbacks);
        } catch (error) {
            state.stats.hookFailures++;
            setError('安装 Hook 失败: ' + name, error);
            if (required) throw error;
            return false;
        }
    }

    function installHooks() {
        if (state.installed) return { ok: true, installed: true };
        if (!state.moduleOk || !state.archOk) return { ok: false, error: state.lastError || 'module/arch not ready' };
        if (!initNativeFunctions()) return { ok: false, error: state.lastError || 'NativeFunction init failed' };

        initKeyApi();

        try {
            tryAttachHook('CinemachineBrain.PushStateToUnityCamera', RVA.Brain_PushStateToUnityCamera, {
                onEnter: function (args) { this.brain = args[0]; },
                onLeave: function () { updateSoulCamera(this.brain); }
            }, true);

            tryAttachHook('Player.UpdateCameraRotaion', RVA.Player_UpdateCameraRotaion, {
                onEnter: function (args) { this.player = args[0]; },
                onLeave: function () { updateMouseFromPlayer(this.player); }
            }, false);

            tryAttachHook('Player.GetWalkVelocity', RVA.Player_GetWalkVelocity, {
                onEnter: function (args) {
                    this.returnBuffer = args[0];
                    this.player = args[1];
                    this.displayClass = args[2];
                },
                onLeave: function () {
                    updateFallbackMoveInput(this.returnBuffer, this.player, this.displayClass);
                }
            }, false);

            tryAttachHook('CameraManager.Awake', RVA.CameraManager_Awake, {
                onLeave: function () { onRoomReady('CameraManager.Awake', true); }
            }, false);

            tryAttachHook('GameManager.Awake', RVA.GameManager_Awake, {
                onLeave: function () { onRoomReady('GameManager.Awake', true); }
            }, false);

            tryAttachHook('ModeBase.Update', RVA.ModeBase_Update, {
                onEnter: function () {
                    if (!state.enabled || state.applied) return;
                    var now = Date.now();
                    if (now - state.lastRoomReadyAt < 750) return;
                    onRoomReady('ModeBase.Update', false);
                }
            }, false);

            tryAttachHook('ModeBase.ExitGame', RVA.ModeBase_ExitGame, {
                onEnter: function () { onRoomExit('ModeBase.ExitGame'); }
            }, false);

            tryAttachHook('GameManager.OnDestroy', RVA.GameManager_OnDestroy, {
                onEnter: function () { onRoomExit('GameManager.OnDestroy'); }
            }, false);

            state.installed = true;
            state.lastError = null;
            return { ok: true, installed: true };
        } catch (error) {
            state.stats.hookFailures++;
            setError('安装 Hook 失败', error);
            removeHooks();
            return { ok: false, error: state.lastError };
        }
    }

    function removeHooks() {
        for (var i = 0; i < state.listeners.length; i++) {
            try { state.listeners[i].detach(); } catch (_) { }
        }
        state.listeners = [];
        state.installed = false;
    }

    function enableFeature() {
        var installResult = installHooks();
        if (!installResult.ok) return installResult;
        if (state.enabled) return { ok: true, enabled: true, message: '已经开启' };
        resetFreeCam('enable');
        state.enabled = true;
        sendStatus('free_camera', true);
        markApplyPending('enable');
        sendLog('info', '自由视角 v1.3 已开启：灵魂相机模式', {
            mode: 'independent_position',
            move: 'W/S follow camera forward including vertical pitch; A/D strafe',
            inputMode: state.inputMode,
            speed: config.moveSpeed,
            lockPlayerMove: config.lockPlayerMove
        });
        return { ok: true, enabled: true, message: '自由视角已开启：灵魂相机模式' };
    }

    function disableFeature() {
        if (!state.enabled) return { ok: true, enabled: false, message: '已经关闭' };
        state.enabled = false;
        sendStatus('free_camera', false);
        state.pendingApply = false;
        state.applied = false;
        state.lastApplyReason = 'disable';
        resetFreeCam('disable');
        sendLog('info', '自由视角 v1.3 已关闭');
        return { ok: true, enabled: false, message: '自由视角已关闭' };
    }

    function updateConfig(input) {
        if (!input) return { ok: true, config: config };
        if (input.moveSpeed !== undefined) {
            var speed = Number(input.moveSpeed);
            if (!isFinite(speed) || speed < 1.0 || speed > 80.0) return { ok: false, error: 'moveSpeed 必须在 1.0～80.0' };
            config.moveSpeed = speed;
        }
        if (input.lockPlayerMove !== undefined) config.lockPlayerMove = !!input.lockPlayerMove;
        return { ok: true, config: config };
    }

    function getStatus() {
        return {
            ok: true,
            version: 'v1.3',
            moduleOk: state.moduleOk,
            archOk: state.archOk,
            nativeReady: native.ready,
            installed: state.installed,
            enabled: state.enabled,
            pendingApply: state.pendingApply,
            applied: state.applied,
            generation: state.generation,
            roomGeneration: state.roomGeneration,
            lastResetReason: state.lastResetReason,
            lastApplyReason: state.lastApplyReason,
            lastRoomReadyReason: state.lastRoomReadyReason,
            lastRoomReadyAt: state.lastRoomReadyAt,
            inputMode: state.inputMode,
            keyApiReady: state.keyApiReady,
            cameraValid: state.freeCam.valid,
            cameraInitialized: state.freeCam.initialized,
            inputValid: state.mouseInput.valid,
            movementInputValid: state.keyApiReady || state.fallbackMoveInput.valid,
            x: state.freeCam.x,
            y: state.freeCam.y,
            z: state.freeCam.z,
            yaw: state.freeCam.yaw,
            pitch: state.freeCam.pitch,
            config: config,
            stats: state.stats,
            lastError: state.lastError
        };
    }

    rpc.exports = {
        enable: function (input) {
            if (input) {
                var configResult = updateConfig(input || {});
                if (!configResult.ok) return configResult;
            }
            return enableFeature();
        },
        disable: function () { return disableFeature(); },
        configure: function (input) { return updateConfig(input || {}); },
        setConfig: function (input) { return updateConfig(input || {}); },
        setconfig: function (input) { return updateConfig(input || {}); },
        status: function () { return getStatus(); },
        cleanup: function (payload) {
            state.enabled = false;
            state.pendingApply = false;
            state.applied = false;
            state.lastApplyReason = 'cleanup';
            state.stats.cleanupCount++;
            resetFreeCam('cleanup');
            removeHooks();
            sendLog('info', 'cleanup 完成');
            return { ok: true, enabled: false, installed: state.installed, generation: state.generation };
        }
    };

    sendLog('info', 'free_camera_v1_3.js loaded');
})();
