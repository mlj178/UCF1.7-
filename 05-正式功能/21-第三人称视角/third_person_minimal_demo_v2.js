(function () {
    'use strict';

    /*
     * UCF1.7 第三人称最小化 Demo v2
     *
     * 设计原则：
     * 1. 只复用游戏已有的 Cinemachine FreeLook 和 CinemachineCollider。
     * 2. Follow / LookAt 都使用稳定的 characterContainer，不跟随 spine/head 动画骨骼。
     * 3. 只修改 FreeLook 轨道、Composer 构图、YAxis 数值和 FOV。
     * 4. 只调用游戏原生 PV/CV 模型切换。
     * 5. 不修改 WASD、不旋转 CharacterModel、不 Hook 射击 Ray、不修改 Damage。
     * 6. 不安装诊断定时器，不从 Frida RPC 线程调用 Unity Camera/Transform API。
     *
     * 这是一个用于验证“移动 + 相机 + 模型显示 + 纵向俯仰”的最小基础版，
     * 不是完整第三人称战斗实现。
     */

    var MODULE_NAME = 'GameAssembly.dll';
    var module = Process.findModuleByName(MODULE_NAME);

    function sendLog(level, message, extra) {
        var payload = {
            type: 'log',
            level: level,
            module: 'TP-MIN',
            message: message
        };
        if (extra !== undefined) payload.extra = extra;
        send(payload);
    }

    if (module === null) {
        sendLog('error', MODULE_NAME + ' 未加载');
        return;
    }

    if (Process.arch !== 'ia32' || Process.pointerSize !== 4) {
        sendLog('error', '本 Demo 只支持 32 位 x86 进程', {
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
        CameraManager_ChangePVandCV:           0x00B35920,
        CameraManager_SetFreeLookCameraActive: 0x00B36790,

        GameManager_Awake:                     0x00AFA250,
        GameManager_OnDestroy:                 0x00AFB6F0,
        MapManager_NewGameRoundStart:          0x00AEBCB0,

        Player_get_isMyPlayer:                 0x00B55FD0,
        PlayerData_SetObserveMode:             0x00B13AD0,
        Model_OnOwnerObserveModeChange:        0x00B4B300,
        Weapon_SynchronizeHand:                0x00B6DA20,

        CinemachineFreeLook_set_Follow:        0x00439270,
        CinemachineFreeLook_set_LookAt:        0x002E7E10,
        CinemachineFreeLook_GetRig:            0x006BEDF0,
        CinemachineFreeLook_InternalUpdateCameraState: 0x006BF2F0,
        CinemachineVirtualCamera_GetPipeline:  0x00501E80,

        Singleton_GetInstance:                 0x004A8170,
        GameManager_SingletonMethodInfo:       0x00E1CE64,
        CameraManager_SingletonMethodInfo:     0x00E1CD68,

        Brain_PushStateToUnityCamera:          0x0082B750,
        Brain_get_OutputCamera:                0x0082CDB0,
        Camera_get_fieldOfView:                0x00328270,
        Camera_set_fieldOfView:                0x003289B0
    };

    var OFF = {
        CM_focusPlayer:          0x0C,
        CM_freeLookCamera:       0x10,
        CM_brain:                0x14,

        GM_allPlayers:           0x1C,

        Player_cameraManager:    0x48,
        Player_cameraRotation:   0x4C,  // Vector2: x=yaw, y=pitch
        Player_characterContainer: 0x58,
        Player_currentCharacter: 0x5C,
        Player_playerData:       0x98,
        Player_wpns:             0xA0,

        PD_observeMode:          0x08,
        PD_playerViewModelVisible: 0x24,

        PW_inUse:                0x18,

        CFL_m_LookAt:            0x40,
        CFL_m_Follow:            0x44,
        CFL_m_YAxis:             0x88,
        CFL_m_XAxis:             0x104,
        CFL_m_Orbits:            0x194,

        AX_Value:                0x00,
        AX_MaxSpeed:             0x08,
        AX_InputAxisName:        0x14,
        AX_InputAxisValue:       0x18,
        AX_InvertInput:          0x1C,
        AX_MinValue:             0x20,
        AX_MaxValue:             0x24,
        AX_Wrap:                 0x28,
        AX_InputProvider:        0x54,

        CC_m_TrackedObjectOffset: 0x28,
        CC_m_ScreenX:            0x48,
        CC_m_ScreenY:            0x4C
    };

    var STATE = {
        NO_GAME: 'NO_GAME',
        READY: 'READY',
        ENABLED: 'ENABLED'
    };

    var state = STATE.NO_GAME;
    var installed = false;
    var enabled = false;

    var gameManager = null;
    var cameraManager = null;
    var localPlayer = null;
    var listeners = [];

    var config = {
        shoulder: 'right',
        distance: 3.0,
        pivotHeight: 1.40,
        screenY: 0.52,
        fieldOfView: 70.0,
        pitchScale: 1.0,
        invertY: false
    };

    var stats = {
        cameraUpdates: 0,
        finalCameraWrites: 0,
        reapplyCount: 0,
        pitchWrites: 0,
        lastPlayerPitch: 0.0,
        lastYAxisValue: 0.5,
        errors: 0
    };

    var saved = {
        valid: false,

        player: null,
        character: null,
        playerData: null,
        weapon: null,

        observeMode: -1,
        playerViewModelVisible: true,

        freeLook: null,
        originalFollow: null,
        originalLookAt: null,

        orbitArray: null,
        orbitHeights: [],
        orbitRadii: [],

        composers: [],

        yAxisCaptured: false,
        yAxisInputName: null,
        yAxisInputProvider: null,
        yAxisInputNameHandle: 0,
        yAxisInputProviderHandle: 0,
        yAxisInputValue: 0.0,
        yAxisInvert: false,
        yAxisMaxSpeed: 0.0,
        yAxisMinValue: 0.0,
        yAxisMaxValue: 1.0,
        yAxisWrap: false,

        outputCamera: null,
        originalFov: -1.0
    };

    function isNull(pointer) {
        if (pointer === null || pointer === undefined) return true;
        try {
            return pointer.isNull();
        } catch (_) {
            return true;
        }
    }

    function isReadable(pointer) {
        if (isNull(pointer)) return false;
        try {
            var range = Process.findRangeByAddress(pointer);
            return range !== null && range.protection.indexOf('r') !== -1;
        } catch (_) {
            return false;
        }
    }

    function isExecutable(address) {
        try {
            var range = Process.findRangeByAddress(address);
            return range !== null && range.protection.indexOf('x') !== -1;
        } catch (_) {
            return false;
        }
    }

    function guarded(label, callback, fallback) {
        try {
            return callback();
        } catch (error) {
            stats.errors++;
            sendLog('error', label + ': ' + error);
            return fallback;
        }
    }

    function setState(nextState) {
        if (state === nextState) return;
        var previous = state;
        state = nextState;
        sendLog('info', '状态: ' + previous + ' -> ' + nextState);
        send({
            type: 'state_changed',
            oldState: previous,
            newState: nextState
        });
    }

    function findExport(name) {
        var result = null;
        try {
            if (typeof Module.findExportByName === 'function') {
                result = Module.findExportByName(MODULE_NAME, name);
            }
        } catch (_) {
        }
        if (isNull(result)) {
            try {
                if (typeof Module.findGlobalExportByName === 'function') {
                    result = Module.findGlobalExportByName(name);
                }
            } catch (_) {
            }
        }
        return result;
    }

    var isMyPlayer = new NativeFunction(
        base.add(RVA.Player_get_isMyPlayer),
        'bool',
        ['pointer', 'pointer'],
        CALL_CONV
    );

    var singletonGetInstance = new NativeFunction(
        base.add(RVA.Singleton_GetInstance),
        'pointer',
        ['pointer'],
        CALL_CONV
    );

    var setFreeLookActive = new NativeFunction(
        base.add(RVA.CameraManager_SetFreeLookCameraActive),
        'void',
        ['pointer', 'bool', 'pointer'],
        CALL_CONV
    );

    var setObserveMode = new NativeFunction(
        base.add(RVA.PlayerData_SetObserveMode),
        'void',
        ['pointer', 'int', 'pointer'],
        CALL_CONV
    );

    var onOwnerObserveModeChange = new NativeFunction(
        base.add(RVA.Model_OnOwnerObserveModeChange),
        'void',
        ['pointer', 'int', 'pointer'],
        CALL_CONV
    );

    var synchronizeHand = new NativeFunction(
        base.add(RVA.Weapon_SynchronizeHand),
        'void',
        ['pointer', 'pointer'],
        CALL_CONV
    );

    var setFollow = new NativeFunction(
        base.add(RVA.CinemachineFreeLook_set_Follow),
        'void',
        ['pointer', 'pointer', 'pointer'],
        CALL_CONV
    );

    var setLookAt = new NativeFunction(
        base.add(RVA.CinemachineFreeLook_set_LookAt),
        'void',
        ['pointer', 'pointer', 'pointer'],
        CALL_CONV
    );

    var getRig = new NativeFunction(
        base.add(RVA.CinemachineFreeLook_GetRig),
        'pointer',
        ['pointer', 'int', 'pointer'],
        CALL_CONV
    );

    var getPipeline = new NativeFunction(
        base.add(RVA.CinemachineVirtualCamera_GetPipeline),
        'pointer',
        ['pointer', 'pointer'],
        CALL_CONV
    );

    var brainGetOutputCamera = new NativeFunction(
        base.add(RVA.Brain_get_OutputCamera),
        'pointer',
        ['pointer', 'pointer'],
        CALL_CONV
    );

    var cameraGetFieldOfView = new NativeFunction(
        base.add(RVA.Camera_get_fieldOfView),
        'float',
        ['pointer', 'pointer'],
        CALL_CONV
    );

    var cameraSetFieldOfView = new NativeFunction(
        base.add(RVA.Camera_set_fieldOfView),
        'void',
        ['pointer', 'float', 'pointer'],
        CALL_CONV
    );

    var il2cppStringNew = null;
    var il2cppGcHandleNew = null;
    var il2cppGcHandleFree = null;

    guarded('初始化 IL2CPP 字符串 API', function () {
        var stringNewAddress = findExport('il2cpp_string_new');
        var handleNewAddress = findExport('il2cpp_gchandle_new');
        var handleFreeAddress = findExport('il2cpp_gchandle_free');

        if (!isNull(stringNewAddress)) {
            il2cppStringNew = new NativeFunction(
                stringNewAddress,
                'pointer',
                ['pointer']
            );
        }
        if (!isNull(handleNewAddress)) {
            il2cppGcHandleNew = new NativeFunction(
                handleNewAddress,
                'uint32',
                ['pointer', 'int']
            );
        }
        if (!isNull(handleFreeAddress)) {
            il2cppGcHandleFree = new NativeFunction(
                handleFreeAddress,
                'void',
                ['uint32']
            );
        }
    }, null);

    var mouseYUtf8 = Memory.allocUtf8String('Mouse Y');
    var mouseYString = null;
    var mouseYHandle = 0;

    function ensureMouseYString() {
        if (!isNull(mouseYString) && isReadable(mouseYString)) return true;
        if (il2cppStringNew === null) {
            sendLog('error', '找不到 il2cpp_string_new，无法配置 Mouse Y');
            return false;
        }

        return guarded('创建 Mouse Y 字符串', function () {
            mouseYString = il2cppStringNew(mouseYUtf8);
            if (isNull(mouseYString) || !isReadable(mouseYString)) return false;

            if (il2cppGcHandleNew !== null && mouseYHandle === 0) {
                mouseYHandle = il2cppGcHandleNew(mouseYString, 0);
            }
            return true;
        }, false);
    }

    function resolveGameManager() {
        if (!isNull(gameManager) && isReadable(gameManager)) return gameManager;

        if (state === STATE.NO_GAME && isNull(cameraManager)) return null;

        return guarded('解析 GameManager', function () {
            var slot = base.add(RVA.GameManager_SingletonMethodInfo);
            if (!isReadable(slot)) return null;

            var methodInfo = slot.readPointer();
            if (isNull(methodInfo) || !isReadable(methodInfo)) return null;

            var instance = singletonGetInstance(methodInfo);
            if (isNull(instance) || !isReadable(instance)) return null;

            gameManager = instance;
            return instance;
        }, null);
    }

    function resolveCameraManager() {
        if (!isNull(cameraManager) && isReadable(cameraManager)) return cameraManager;
        if (resolveGameManager() === null) return null;

        return guarded('解析 CameraManager', function () {
            var slot = base.add(RVA.CameraManager_SingletonMethodInfo);
            if (!isReadable(slot)) return null;

            var methodInfo = slot.readPointer();
            if (isNull(methodInfo) || !isReadable(methodInfo)) return null;

            var instance = singletonGetInstance(methodInfo);
            if (isNull(instance) || !isReadable(instance)) return null;

            cameraManager = instance;
            return instance;
        }, null);
    }

    function resolveLocalPlayer() {
        if (!isNull(localPlayer) && isReadable(localPlayer)) return localPlayer;

        var manager = resolveCameraManager();
        if (!isNull(manager)) {
            var focusPlayer = guarded('读取 focusPlayer', function () {
                return manager.add(OFF.CM_focusPlayer).readPointer();
            }, null);

            if (!isNull(focusPlayer) && isReadable(focusPlayer)) {
                var isLocal = guarded('验证 focusPlayer', function () {
                    return isMyPlayer(focusPlayer, ptr(0));
                }, false);

                if (isLocal) {
                    localPlayer = focusPlayer;
                    return localPlayer;
                }
            }
        }

        var gm = resolveGameManager();
        if (isNull(gm)) return null;

        return guarded('遍历本地玩家', function () {
            var array = gm.add(OFF.GM_allPlayers).readPointer();
            if (isNull(array) || !isReadable(array)) return null;

            var count = array.add(0x0C).readU32();
            if (count < 1 || count > 64) return null;

            for (var index = 0; index < count; index++) {
                var candidate = array.add(0x10 + index * PTR_SIZE).readPointer();
                if (isNull(candidate) || !isReadable(candidate)) continue;

                if (isMyPlayer(candidate, ptr(0))) {
                    localPlayer = candidate;
                    return candidate;
                }
            }
            return null;
        }, null);
    }

    function releaseHandle(handle) {
        if (handle === 0 || il2cppGcHandleFree === null) return;
        guarded('释放 GCHandle', function () {
            il2cppGcHandleFree(handle);
        }, null);
    }

    function captureYAxis(freeLook) {
        if (saved.yAxisCaptured) return true;

        return guarded('保存 YAxis 配置', function () {
            var axis = freeLook.add(OFF.CFL_m_YAxis);

            saved.yAxisInputName = axis.add(OFF.AX_InputAxisName).readPointer();
            saved.yAxisInputProvider = axis.add(OFF.AX_InputProvider).readPointer();
            saved.yAxisInputValue = axis.add(OFF.AX_InputAxisValue).readFloat();
            saved.yAxisInvert = axis.add(OFF.AX_InvertInput).readU8() !== 0;
            saved.yAxisMaxSpeed = axis.add(OFF.AX_MaxSpeed).readFloat();
            saved.yAxisMinValue = axis.add(OFF.AX_MinValue).readFloat();
            saved.yAxisMaxValue = axis.add(OFF.AX_MaxValue).readFloat();
            saved.yAxisWrap = axis.add(OFF.AX_Wrap).readU8() !== 0;

            if (il2cppGcHandleNew !== null) {
                if (!isNull(saved.yAxisInputName) && isReadable(saved.yAxisInputName)) {
                    saved.yAxisInputNameHandle = il2cppGcHandleNew(
                        saved.yAxisInputName,
                        0
                    );
                }
                if (!isNull(saved.yAxisInputProvider) && isReadable(saved.yAxisInputProvider)) {
                    saved.yAxisInputProviderHandle = il2cppGcHandleNew(
                        saved.yAxisInputProvider,
                        0
                    );
                }
            }

            saved.yAxisCaptured = true;
            sendLog('info', '已保存 FreeLook YAxis 原始状态', {
                value: axis.add(OFF.AX_Value).readFloat(),
                maxSpeed: saved.yAxisMaxSpeed,
                invert: saved.yAxisInvert
            });
            return true;
        }, false);
    }

    function clamp01(value) {
        if (value < 0.0) return 0.0;
        if (value > 1.0) return 1.0;
        return value;
    }

    function lockYAxisForDirectDrive(freeLook) {
        if (!enabled) return false;
        if (!captureYAxis(freeLook)) return false;

        return guarded('锁定 YAxis 为直接驱动模式', function () {
            var axis = freeLook.add(OFF.CFL_m_YAxis);

            // 游戏当前的 FreeLook YAxis 原始 MaxSpeed=0，
            // 说明它没有可用的原生纵向输入链。
            // v2 不再自行调用 Input.GetAxis，而是复用 Player.cameraRotation.y。
            axis.add(OFF.AX_InputAxisName).writePointer(ptr(0));
            axis.add(OFF.AX_InputProvider).writePointer(ptr(0));
            axis.add(OFF.AX_InputAxisValue).writeFloat(0.0);
            axis.add(OFF.AX_MaxSpeed).writeFloat(0.0);
            axis.add(OFF.AX_InvertInput).writeU8(0);
            axis.add(OFF.AX_MinValue).writeFloat(0.0);
            axis.add(OFF.AX_MaxValue).writeFloat(1.0);
            axis.add(OFF.AX_Wrap).writeU8(0);
            return true;
        }, false);
    }

    function driveVerticalPitch(freeLook) {
        if (!enabled) return false;
        if (isNull(freeLook) || !isReadable(freeLook)) return false;
        if (!lockYAxisForDirectDrive(freeLook)) return false;

        var player = localPlayer;
        if (isNull(player) || !isReadable(player)) {
            player = resolveLocalPlayer();
        }
        if (isNull(player) || !isReadable(player)) return false;

        return guarded('同步 Player pitch 到 FreeLook YAxis', function () {
            var pitch = player.add(
                OFF.Player_cameraRotation + 4
            ).readFloat();

            if (!isFinite(pitch) || pitch < -180.0 || pitch > 180.0) {
                return false;
            }

            // 已有运行日志显示：
            // cameraRotation.y ≈ 44.4° 时，FreeLook.yAxis ≈ 0.749；
            // 对应关系约为 0.5 + pitch / 180。
            var signedPitch = config.invertY ? -pitch : pitch;
            var yAxisValue = 0.5 + (
                signedPitch * config.pitchScale / 180.0
            );

            // 留少量边界，避免相机完全卡在顶/底 Rig。
            yAxisValue = Math.max(0.02, Math.min(0.98, clamp01(yAxisValue)));

            var axis = freeLook.add(OFF.CFL_m_YAxis);
            axis.add(OFF.AX_Value).writeFloat(yAxisValue);
            axis.add(OFF.AX_InputAxisValue).writeFloat(0.0);
            axis.add(OFF.AX_MaxSpeed).writeFloat(0.0);

            stats.pitchWrites++;
            stats.lastPlayerPitch = pitch;
            stats.lastYAxisValue = yAxisValue;
            return true;
        }, false);
    }

    function restoreYAxis() {
        if (!saved.yAxisCaptured || isNull(saved.freeLook) || !isReadable(saved.freeLook)) {
            releaseHandle(saved.yAxisInputNameHandle);
            releaseHandle(saved.yAxisInputProviderHandle);
            saved.yAxisInputNameHandle = 0;
            saved.yAxisInputProviderHandle = 0;
            saved.yAxisCaptured = false;
            return;
        }

        guarded('恢复 YAxis', function () {
            var axis = saved.freeLook.add(OFF.CFL_m_YAxis);

            axis.add(OFF.AX_InputAxisName).writePointer(
                isNull(saved.yAxisInputName) ? ptr(0) : saved.yAxisInputName
            );
            axis.add(OFF.AX_InputProvider).writePointer(
                isNull(saved.yAxisInputProvider) ? ptr(0) : saved.yAxisInputProvider
            );
            axis.add(OFF.AX_InputAxisValue).writeFloat(saved.yAxisInputValue);
            axis.add(OFF.AX_MaxSpeed).writeFloat(saved.yAxisMaxSpeed);
            axis.add(OFF.AX_InvertInput).writeU8(saved.yAxisInvert ? 1 : 0);
            axis.add(OFF.AX_MinValue).writeFloat(saved.yAxisMinValue);
            axis.add(OFF.AX_MaxValue).writeFloat(saved.yAxisMaxValue);
            axis.add(OFF.AX_Wrap).writeU8(saved.yAxisWrap ? 1 : 0);
        }, null);

        releaseHandle(saved.yAxisInputNameHandle);
        releaseHandle(saved.yAxisInputProviderHandle);
        saved.yAxisInputNameHandle = 0;
        saved.yAxisInputProviderHandle = 0;
        saved.yAxisCaptured = false;
    }

    function shoulderScreenX() {
        if (config.shoulder === 'left') return 0.58;
        if (config.shoulder === 'center') return 0.50;
        return 0.42;
    }

    function captureCameraState(freeLook) {
        if (saved.valid) return true;

        return guarded('保存相机状态', function () {
            saved.freeLook = freeLook;
            saved.originalFollow = freeLook.add(OFF.CFL_m_Follow).readPointer();
            saved.originalLookAt = freeLook.add(OFF.CFL_m_LookAt).readPointer();

            saved.orbitArray = freeLook.add(OFF.CFL_m_Orbits).readPointer();
            if (!isNull(saved.orbitArray) && isReadable(saved.orbitArray)) {
                var orbitCount = saved.orbitArray.add(0x0C).readU32();
                for (var index = 0; index < orbitCount && index < 3; index++) {
                    saved.orbitHeights.push(
                        saved.orbitArray.add(0x10 + index * 8).readFloat()
                    );
                    saved.orbitRadii.push(
                        saved.orbitArray.add(0x14 + index * 8).readFloat()
                    );
                }
            }

            saved.composers = [];
            for (var rigIndex = 0; rigIndex < 3; rigIndex++) {
                var rig = getRig(freeLook, rigIndex, ptr(0));
                if (isNull(rig) || !isReadable(rig)) continue;

                var pipeline = getPipeline(rig, ptr(0));
                if (isNull(pipeline) || !isReadable(pipeline)) continue;

                var componentCount = pipeline.add(0x0C).readU32();
                for (var componentIndex = 0;
                     componentIndex < componentCount && componentIndex < 10;
                     componentIndex++) {

                    var component = pipeline.add(
                        0x10 + componentIndex * PTR_SIZE
                    ).readPointer();

                    if (isNull(component) || !isReadable(component)) continue;

                    var screenX = component.add(OFF.CC_m_ScreenX).readFloat();
                    var screenY = component.add(OFF.CC_m_ScreenY).readFloat();

                    // 排除 OrbitalTransposer 等字段碰巧为 0 的组件。
                    if (screenX <= 0.10 || screenX >= 0.90 ||
                        screenY <= 0.10 || screenY >= 0.90) {
                        continue;
                    }

                    saved.composers.push({
                        pointer: component,
                        screenX: screenX,
                        screenY: screenY,
                        trackedX: component.add(
                            OFF.CC_m_TrackedObjectOffset
                        ).readFloat(),
                        trackedY: component.add(
                            OFF.CC_m_TrackedObjectOffset + 4
                        ).readFloat(),
                        trackedZ: component.add(
                            OFF.CC_m_TrackedObjectOffset + 8
                        ).readFloat()
                    });
                    break;
                }
            }

            saved.valid = true;
            return true;
        }, false);
    }

    function applyCameraConfiguration() {
        if (!enabled) return false;

        var manager = resolveCameraManager();
        var player = resolveLocalPlayer();

        if (isNull(manager) || isNull(player)) return false;

        return guarded('应用最小相机配置', function () {
            var freeLook = manager.add(OFF.CM_freeLookCamera).readPointer();
            if (isNull(freeLook) || !isReadable(freeLook)) return false;

            var characterContainer = player.add(
                OFF.Player_characterContainer
            ).readPointer();

            if (isNull(characterContainer) || !isReadable(characterContainer)) {
                return false;
            }

            if (!captureCameraState(freeLook)) return false;

            // 稳定枢轴：Follow / LookAt 都使用同一个非骨骼对象。
            setFollow(freeLook, characterContainer, ptr(0));
            setLookAt(freeLook, characterContainer, ptr(0));

            var orbitArray = freeLook.add(OFF.CFL_m_Orbits).readPointer();
            if (!isNull(orbitArray) && isReadable(orbitArray)) {
                var count = orbitArray.add(0x0C).readU32();
                if (count >= 3) {
                    orbitArray.add(0x10).writeFloat(config.pivotHeight + 0.55);
                    orbitArray.add(0x14).writeFloat(config.distance);

                    orbitArray.add(0x18).writeFloat(config.pivotHeight);
                    orbitArray.add(0x1C).writeFloat(config.distance);

                    orbitArray.add(0x20).writeFloat(
                        Math.max(0.35, config.pivotHeight - 0.70)
                    );
                    orbitArray.add(0x24).writeFloat(config.distance * 0.90);
                }
            }

            var targetScreenX = shoulderScreenX();
            for (var index = 0; index < saved.composers.length; index++) {
                var composer = saved.composers[index].pointer;
                if (isNull(composer) || !isReadable(composer)) continue;

                composer.add(OFF.CC_m_ScreenX).writeFloat(targetScreenX);
                composer.add(OFF.CC_m_ScreenY).writeFloat(config.screenY);

                composer.add(
                    OFF.CC_m_TrackedObjectOffset
                ).writeFloat(0.0);
                composer.add(
                    OFF.CC_m_TrackedObjectOffset + 4
                ).writeFloat(config.pivotHeight);
                composer.add(
                    OFF.CC_m_TrackedObjectOffset + 8
                ).writeFloat(0.0);
            }

            driveVerticalPitch(freeLook);
            setFreeLookActive(manager, 1, ptr(0));

            stats.reapplyCount++;
            return true;
        }, false);
    }

    function applyModelMode(player) {
        return guarded('切换第三人称模型', function () {
            var playerData = player.add(OFF.Player_playerData).readPointer();
            var character = player.add(OFF.Player_currentCharacter).readPointer();

            if (isNull(playerData) || !isReadable(playerData) ||
                isNull(character) || !isReadable(character)) {
                return false;
            }

            if (!saved.valid) {
                saved.player = player;
                saved.character = character;
                saved.playerData = playerData;
                saved.observeMode = playerData.add(
                    OFF.PD_observeMode
                ).readS32();
                saved.playerViewModelVisible = playerData.add(
                    OFF.PD_playerViewModelVisible
                ).readU8() !== 0;
            }

            setObserveMode(playerData, 0, ptr(0));
            onOwnerObserveModeChange(character, 0, ptr(0));
            playerData.add(
                OFF.PD_playerViewModelVisible
            ).writeU8(0);

            var weapons = player.add(OFF.Player_wpns).readPointer();
            if (!isNull(weapons) && isReadable(weapons)) {
                var weapon = weapons.add(OFF.PW_inUse).readPointer();
                if (!isNull(weapon) && isReadable(weapon)) {
                    saved.weapon = weapon;
                    synchronizeHand(weapon, ptr(0));
                }
            }

            return true;
        }, false);
    }

    function saveOriginalFov(brain) {
        if (saved.originalFov > 0) return;

        guarded('保存 FOV', function () {
            var camera = brainGetOutputCamera(brain, ptr(0));
            if (isNull(camera) || !isReadable(camera)) return;

            var fov = cameraGetFieldOfView(camera, ptr(0));
            if (!isFinite(fov) || fov <= 1 || fov >= 179) return;

            saved.outputCamera = camera;
            saved.originalFov = fov;
        }, null);
    }

    function enforceFov(brain) {
        if (!enabled) return;

        guarded('应用 FOV', function () {
            var camera = brainGetOutputCamera(brain, ptr(0));
            if (isNull(camera) || !isReadable(camera)) return;

            saveOriginalFov(brain);
            cameraSetFieldOfView(camera, config.fieldOfView, ptr(0));
            stats.finalCameraWrites++;
        }, null);
    }

    function restoreCameraState() {
        if (!saved.valid) return;

        restoreYAxis();

        guarded('恢复 FreeLook', function () {
            if (!isNull(saved.freeLook) && isReadable(saved.freeLook)) {
                setFollow(
                    saved.freeLook,
                    isNull(saved.originalFollow) ? ptr(0) : saved.originalFollow,
                    ptr(0)
                );
                setLookAt(
                    saved.freeLook,
                    isNull(saved.originalLookAt) ? ptr(0) : saved.originalLookAt,
                    ptr(0)
                );

                if (!isNull(saved.orbitArray) &&
                    isReadable(saved.orbitArray) &&
                    saved.orbitHeights.length >= 3) {

                    for (var index = 0; index < 3; index++) {
                        saved.orbitArray.add(
                            0x10 + index * 8
                        ).writeFloat(saved.orbitHeights[index]);
                        saved.orbitArray.add(
                            0x14 + index * 8
                        ).writeFloat(saved.orbitRadii[index]);
                    }
                }
            }

            for (var composerIndex = 0;
                 composerIndex < saved.composers.length;
                 composerIndex++) {

                var item = saved.composers[composerIndex];
                if (isNull(item.pointer) || !isReadable(item.pointer)) continue;

                item.pointer.add(
                    OFF.CC_m_ScreenX
                ).writeFloat(item.screenX);
                item.pointer.add(
                    OFF.CC_m_ScreenY
                ).writeFloat(item.screenY);
                item.pointer.add(
                    OFF.CC_m_TrackedObjectOffset
                ).writeFloat(item.trackedX);
                item.pointer.add(
                    OFF.CC_m_TrackedObjectOffset + 4
                ).writeFloat(item.trackedY);
                item.pointer.add(
                    OFF.CC_m_TrackedObjectOffset + 8
                ).writeFloat(item.trackedZ);
            }

            if (!isNull(saved.outputCamera) &&
                isReadable(saved.outputCamera) &&
                saved.originalFov > 1) {
                cameraSetFieldOfView(
                    saved.outputCamera,
                    saved.originalFov,
                    ptr(0)
                );
            }
        }, null);
    }

    function restoreModelMode() {
        if (isNull(saved.playerData) || !isReadable(saved.playerData) ||
            isNull(saved.character) || !isReadable(saved.character)) {
            return;
        }

        guarded('恢复模型模式', function () {
            onOwnerObserveModeChange(
                saved.character,
                saved.observeMode,
                ptr(0)
            );
            setObserveMode(
                saved.playerData,
                saved.observeMode,
                ptr(0)
            );
            saved.playerData.add(
                OFF.PD_playerViewModelVisible
            ).writeU8(saved.playerViewModelVisible ? 1 : 0);

            if (!isNull(saved.weapon) && isReadable(saved.weapon)) {
                synchronizeHand(saved.weapon, ptr(0));
            }
        }, null);
    }

    function resetSavedState() {
        releaseHandle(saved.yAxisInputNameHandle);
        releaseHandle(saved.yAxisInputProviderHandle);

        saved = {
            valid: false,

            player: null,
            character: null,
            playerData: null,
            weapon: null,

            observeMode: -1,
            playerViewModelVisible: true,

            freeLook: null,
            originalFollow: null,
            originalLookAt: null,

            orbitArray: null,
            orbitHeights: [],
            orbitRadii: [],

            composers: [],

            yAxisCaptured: false,
            yAxisInputName: null,
            yAxisInputProvider: null,
            yAxisInputNameHandle: 0,
            yAxisInputProviderHandle: 0,
            yAxisInputValue: 0.0,
            yAxisInvert: false,
            yAxisMaxSpeed: 0.0,
            yAxisMinValue: 0.0,
            yAxisMaxValue: 1.0,
            yAxisWrap: false,

            outputCamera: null,
            originalFov: -1.0
        };
    }

    function enableDemo() {
        if (enabled) {
            return { ok: true, enabled: true, message: '已经启用' };
        }

        var manager = resolveCameraManager();
        var player = resolveLocalPlayer();

        if (isNull(manager)) {
            return { ok: false, enabled: false, error: 'CameraManager 未就绪' };
        }
        if (isNull(player)) {
            return { ok: false, enabled: false, error: '本地玩家未就绪' };
        }

        enabled = true;

        var modelOk = applyModelMode(player);
        var cameraOk = applyCameraConfiguration();

        if (!cameraOk) {
            enabled = false;
            restoreModelMode();
            resetSavedState();
            return {
                ok: false,
                enabled: false,
                error: '相机配置失败'
            };
        }

        setState(STATE.ENABLED);
        sendLog('info', '最小第三人称 Demo 已启用', {
            modelSwitched: modelOk,
            movementModified: false,
            shootingModified: false,
            characterYawModified: false
        });

        return {
            ok: true,
            enabled: true,
            modelSwitched: modelOk
        };
    }

    function disableDemo() {
        if (!enabled) {
            return { ok: true, enabled: false, message: '已经关闭' };
        }

        enabled = false;

        // 对象仍有效时才执行恢复；场景销毁阶段只清空状态。
        if (!isNull(cameraManager) && isReadable(cameraManager)) {
            restoreCameraState();
            guarded('关闭 FreeLook', function () {
                setFreeLookActive(cameraManager, 0, ptr(0));
            }, null);
        }

        restoreModelMode();
        resetSavedState();

        setState(
            !isNull(gameManager) && isReadable(gameManager)
                ? STATE.READY
                : STATE.NO_GAME
        );

        sendLog('info', '最小第三人称 Demo 已关闭');
        return { ok: true, enabled: false };
    }

    function validateConfig(input) {
        var next = {
            shoulder: config.shoulder,
            distance: config.distance,
            pivotHeight: config.pivotHeight,
            screenY: config.screenY,
            fieldOfView: config.fieldOfView,
            pitchScale: config.pitchScale,
            invertY: config.invertY
        };

        if (input === null || typeof input !== 'object') {
            return { ok: false, error: '需要配置对象' };
        }

        if (input.shoulder !== undefined) {
            var shoulder = String(input.shoulder).toLowerCase();
            if (shoulder !== 'left' &&
                shoulder !== 'center' &&
                shoulder !== 'right') {
                return {
                    ok: false,
                    error: 'shoulder 只能是 left / center / right'
                };
            }
            next.shoulder = shoulder;
        }

        function numberField(name, minValue, maxValue) {
            if (input[name] === undefined) return null;
            var value = Number(input[name]);
            if (!isFinite(value) || value < minValue || value > maxValue) {
                return name + ' 范围应为 ' + minValue + ' - ' + maxValue;
            }
            next[name] = value;
            return null;
        }

        var error = numberField('distance', 1.5, 6.0);
        if (error) return { ok: false, error: error };

        error = numberField('pivotHeight', 0.8, 2.2);
        if (error) return { ok: false, error: error };

        error = numberField('screenY', 0.40, 0.65);
        if (error) return { ok: false, error: error };

        error = numberField('fieldOfView', 50.0, 100.0);
        if (error) return { ok: false, error: error };

        error = numberField('pitchScale', 0.5, 2.0);
        if (error) return { ok: false, error: error };

        if (input.invertY !== undefined) {
            next.invertY = !!input.invertY;
        }

        return { ok: true, config: next };
    }

    function installHooks() {
        if (installed) {
            return { ok: true, installed: true };
        }

        function attach(name, rva, callbacks) {
            var address = base.add(rva);

            if (!isExecutable(address)) {
                throw new Error(name + ' 地址不可执行: ' + address);
            }

            var listener = Interceptor.attach(address, callbacks);
            listeners.push(listener);
            sendLog('info', 'Hook 已安装: ' + name, {
                rva: '0x' + rva.toString(16),
                runtime: address.toString()
            });
        }

        try {
            attach(
                'CameraManager.Awake',
                RVA.CameraManager_Awake,
                {
                    onEnter: function (args) {
                        cameraManager = args[0];
                        localPlayer = null;
                        setState(STATE.READY);
                    }
                }
            );

            attach(
                'CameraManager.Update',
                RVA.CameraManager_Update,
                {
                    onEnter: function () {
                        stats.cameraUpdates++;
                    },
                    onLeave: function () {
                        if (!enabled) return;
                        var manager = cameraManager;
                        if (isNull(manager) || !isReadable(manager)) return;

                        var freeLook = guarded(
                            '维护 YAxis 读取 FreeLook',
                            function () {
                                return manager.add(
                                    OFF.CM_freeLookCamera
                                ).readPointer();
                            },
                            null
                        );

                        if (!isNull(freeLook) && isReadable(freeLook)) {
                            // 维护直接驱动模式；只读写字段，不调用 Unity API。
                            driveVerticalPitch(freeLook);
                        }
                    }
                }
            );

            attach(
                'CinemachineFreeLook.InternalUpdateCameraState',
                RVA.CinemachineFreeLook_InternalUpdateCameraState,
                {
                    onEnter: function (args) {
                        if (!enabled) return;

                        var freeLook = args[0];
                        if (isNull(freeLook) || !isReadable(freeLook)) return;

                        // 精确时机：在 FreeLook 计算本帧 CameraState 之前写入 YAxis.Value。
                        driveVerticalPitch(freeLook);
                    }
                }
            );

            attach(
                'CameraManager.ChangePVandCV',
                RVA.CameraManager_ChangePVandCV,
                {
                    onLeave: function () {
                        if (!enabled) return;

                        var player = resolveLocalPlayer();
                        if (!isNull(player)) {
                            applyModelMode(player);
                        }
                        applyCameraConfiguration();
                    }
                }
            );

            attach(
                'CameraManager.OnDestroy',
                RVA.CameraManager_OnDestroy,
                {
                    onEnter: function (args) {
                        if (!isNull(cameraManager) &&
                            args[0].equals(cameraManager)) {
                            // 对象已经进入销毁流程，不再调用恢复函数。
                            enabled = false;
                            cameraManager = null;
                            localPlayer = null;
                            resetSavedState();
                            setState(STATE.NO_GAME);
                            sendLog('info', 'CameraManager 正在销毁，已清空 Demo 状态');
                        }
                    }
                }
            );

            attach(
                'GameManager.Awake',
                RVA.GameManager_Awake,
                {
                    onEnter: function (args) {
                        gameManager = args[0];
                        localPlayer = null;
                        setState(STATE.READY);
                    }
                }
            );

            attach(
                'GameManager.OnDestroy',
                RVA.GameManager_OnDestroy,
                {
                    onEnter: function (args) {
                        if (!isNull(gameManager) &&
                            args[0].equals(gameManager)) {
                            enabled = false;
                            gameManager = null;
                            localPlayer = null;
                            resetSavedState();
                            setState(STATE.NO_GAME);
                            sendLog('info', 'GameManager 正在销毁，已清空 Demo 状态');
                        }
                    }
                }
            );

            attach(
                'MapManager.NewGameRoundStart',
                RVA.MapManager_NewGameRoundStart,
                {
                    onEnter: function () {
                        localPlayer = null;
                        if (!enabled) setState(STATE.READY);
                    }
                }
            );

            attach(
                'CinemachineBrain.PushStateToUnityCamera',
                RVA.Brain_PushStateToUnityCamera,
                {
                    onEnter: function (args) {
                        this.brain = args[0];
                    },
                    onLeave: function () {
                        if (!enabled) return;
                        enforceFov(this.brain);
                    }
                }
            );

            installed = true;
            sendLog('info', '最小化 Hook 安装完成');
            return { ok: true, installed: true };
        } catch (error) {
            stats.errors++;
            sendLog('error', '安装 Hook 失败: ' + error);
            return {
                ok: false,
                installed: false,
                error: String(error)
            };
        }
    }

    function cleanup() {
        if (enabled) {
            disableDemo();
        }

        for (var index = 0; index < listeners.length; index++) {
            try {
                listeners[index].detach();
            } catch (_) {
            }
        }
        listeners = [];
        installed = false;

        if (mouseYHandle !== 0 && il2cppGcHandleFree !== null) {
            guarded('释放 Mouse Y GCHandle', function () {
                il2cppGcHandleFree(mouseYHandle);
            }, null);
            mouseYHandle = 0;
        }

        mouseYString = null;
        sendLog('info', 'Demo 资源已清理');
        return { ok: true };
    }

    rpc.exports = {
        installhooks: installHooks,

        enable: enableDemo,

        disable: disableDemo,

        setconfig: function (input) {
            var validation = validateConfig(input);
            if (!validation.ok) return validation;

            config = validation.config;

            if (enabled) {
                applyCameraConfiguration();
            }

            return {
                ok: true,
                config: config
            };
        },

        getstatus: function () {
            return {
                ok: true,
                installed: installed,
                enabled: enabled,
                state: state,
                haveGameManager:
                    !isNull(gameManager) && isReadable(gameManager),
                haveCameraManager:
                    !isNull(cameraManager) && isReadable(cameraManager),
                haveLocalPlayer:
                    !isNull(localPlayer) && isReadable(localPlayer),
                config: config,
                stats: stats,
                design: {
                    movementModified: false,
                    characterYawModified: false,
                    shootingRayModified: false,
                    damageModified: false,
                    crosshairPolicy: 'screen-center / native HUD',
                    cameraTarget: 'stable characterContainer',
                    verticalPitch: 'Player.cameraRotation.y -> FreeLook.YAxis.Value',
                    collision: 'native CinemachineCollider'
                }
            };
        },

        cleanup: cleanup
    };

    sendLog('info', '第三人称最小化 Demo v2 脚本已加载', {
        base: base.toString(),
        arch: Process.arch,
        pointerSize: Process.pointerSize
    });
})();
