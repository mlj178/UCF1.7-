(function () {
    'use strict';

    /*
     * UCF1.7 第三人称最小化 Demo v2.3（主线程命令队列修正版）
     *
     * 设计原则：
     * 1. 只复用游戏已有的 Cinemachine FreeLook 和 CinemachineCollider。
     * 2. Follow / LookAt 都使用稳定的 characterContainer，不跟随 spine/head 动画骨骼。
     * 3. 只修改 FreeLook 轨道、Composer 构图、YAxis 数值和 FOV。
     * 4. 只调用游戏原生 PV/CV 模型切换。
     * 5. 不修改 WASD、不旋转 CharacterModel、不 Hook 射击 Ray、不修改 Damage。
     * 6. 不安装诊断定时器，不从 Frida RPC 线程调用 Unity Camera/Transform API。
     *
     * 这是一个用于验证“移动 + 相机 + 模型显示 + 纵向俯仰”的可分析基础版，
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
        Camera_set_fieldOfView:                0x003289B0,
        Component_get_transform:               0x0032CF40,
        Transform_get_forward_Injected:        0x003F3F20
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

    // v2.2：支持脚本晚于游戏 Awake 阶段附加。
    var pendingEnable = false;
    var pendingDisable = false;
    var pendingReapply = false;
    var enableInProgress = false;
    var disableInProgress = false;
    var lastEnableError = '';
    var lastMainThreadCommand = 'none';
    var mainThreadId = 0;
    var cameraManagerCaptureSource = 'none';
    var cameraManagerCaptureCount = 0;
    var localPlayerCaptureCount = 0;

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
        freeLookUpdateCalls: 0,
        finalCameraWrites: 0,
        reapplyCount: 0,

        pitchWriteAttempts: 0,
        pitchWrites: 0,
        pitchWriteFailures: 0,
        invalidPitchSamples: 0,

        playerPitchChangeCount: 0,
        yAxisChangeCount: 0,
        cameraPitchChangeCount: 0,

        lastPlayerPitch: 0.0,
        lastPlayerPitchDelta: 0.0,

        lastYAxisBeforeWrite: 0.5,
        lastYAxisWritten: 0.5,
        lastYAxisAfterUpdate: 0.5,
        lastYAxisOverwriteDelta: 0.0,

        lastCameraForwardY: 0.0,
        lastCameraPitch: 0.0,
        lastCameraPitchDelta: 0.0,

        telemetryLines: 0,
        cameraManagerCaptures: 0,
        localPlayerCaptures: 0,
        queuedEnableRequests: 0,
        automaticEnableAttempts: 0,
        automaticEnableSuccesses: 0,
        mainThreadCommands: 0,
        enableMainThreadRuns: 0,
        disableMainThreadRuns: 0,
        reapplyMainThreadRuns: 0,
        unsafeRpcUnityCalls: 0,
        errors: 0
    };

    var telemetry = {
        intervalMs: 1000,
        lastLogTime: 0,
        lastPitchWrites: 0,
        enabledAt: 0,

        previousPlayerPitch: null,
        previousYAxisWritten: null,
        previousCameraPitch: null,

        playerPitchMin: null,
        playerPitchMax: null,
        yAxisMin: null,
        yAxisMax: null,
        cameraPitchMin: null,
        cameraPitchMax: null
    };

    var cameraForwardBuffer = Memory.alloc(12);

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

    var componentGetTransform = new NativeFunction(
        base.add(RVA.Component_get_transform),
        'pointer',
        ['pointer', 'pointer'],
        CALL_CONV
    );

    var transformGetForward = new NativeFunction(
        base.add(RVA.Transform_get_forward_Injected),
        'void',
        ['pointer', 'pointer', 'pointer'],
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

    function cacheCameraManager(instance, source) {
        if (isNull(instance) || !isReadable(instance)) return false;

        var changed =
            isNull(cameraManager) ||
            !isReadable(cameraManager) ||
            !cameraManager.equals(instance);

        cameraManager = instance;
        cameraManagerCaptureSource = source || 'unknown';

        if (changed) {
            cameraManagerCaptureCount++;
            stats.cameraManagerCaptures++;
            localPlayer = null;

            sendLog('info', '[Lifecycle] CameraManager 已捕获', {
                pointer: instance.toString(),
                source: cameraManagerCaptureSource,
                captureCount: cameraManagerCaptureCount,
                previousState: state
            });
        }

        if (state === STATE.NO_GAME) {
            setState(STATE.READY);
        }
        return true;
    }

    function cacheLocalPlayer(instance, source) {
        if (isNull(instance) || !isReadable(instance)) return false;

        var changed =
            isNull(localPlayer) ||
            !isReadable(localPlayer) ||
            !localPlayer.equals(instance);

        localPlayer = instance;

        if (changed) {
            localPlayerCaptureCount++;
            stats.localPlayerCaptures++;
            sendLog('info', '[Lifecycle] 本地玩家已捕获', {
                pointer: instance.toString(),
                source: source || 'unknown',
                captureCount: localPlayerCaptureCount
            });
        }
        return true;
    }

    function resolveGameManager() {
        if (!isNull(gameManager) && isReadable(gameManager)) return gameManager;

        // v2.2：NO_GAME 只代表尚未捕获生命周期对象，
        // 不能再作为禁止解析的条件。
        return guarded('解析 GameManager Singleton', function () {
            var slot = base.add(RVA.GameManager_SingletonMethodInfo);
            if (!isReadable(slot)) return null;

            var methodInfo = slot.readPointer();
            if (isNull(methodInfo) || !isReadable(methodInfo)) return null;

            var instance = singletonGetInstance(methodInfo);
            if (isNull(instance) || !isReadable(instance)) return null;

            gameManager = instance;
            sendLog('info', '[Lifecycle] GameManager 通过 Singleton 恢复', {
                pointer: instance.toString()
            });
            if (state === STATE.NO_GAME) setState(STATE.READY);
            return instance;
        }, null);
    }

    function resolveCameraManager() {
        if (!isNull(cameraManager) && isReadable(cameraManager)) {
            return cameraManager;
        }

        // 正常路径由 CameraManager.Update 在 Unity 主线程捕获。
        // Singleton 仅作为晚连接兜底，不再依赖 GameManager。
        return guarded('解析 CameraManager Singleton', function () {
            var slot = base.add(RVA.CameraManager_SingletonMethodInfo);
            if (!isReadable(slot)) return null;

            var methodInfo = slot.readPointer();
            if (isNull(methodInfo) || !isReadable(methodInfo)) return null;

            var instance = singletonGetInstance(methodInfo);
            if (isNull(instance) || !isReadable(instance)) return null;

            cacheCameraManager(instance, 'singleton_fallback');
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
                    cacheLocalPlayer(focusPlayer, 'CameraManager.focusPlayer');
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
                    cacheLocalPlayer(candidate, 'GameManager.allPlayers');
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

    function updateRange(keyMin, keyMax, value) {
        if (!isFinite(value)) return;
        if (telemetry[keyMin] === null || value < telemetry[keyMin]) {
            telemetry[keyMin] = value;
        }
        if (telemetry[keyMax] === null || value > telemetry[keyMax]) {
            telemetry[keyMax] = value;
        }
    }

    function readVector3(pointer) {
        try {
            var value = {
                x: pointer.readFloat(),
                y: pointer.add(4).readFloat(),
                z: pointer.add(8).readFloat()
            };
            value.valid =
                isFinite(value.x) &&
                isFinite(value.y) &&
                isFinite(value.z);
            return value;
        } catch (_) {
            return { x: 0.0, y: 0.0, z: 0.0, valid: false };
        }
    }

    function sampleActualCameraPitch(brain) {
        if (!enabled || isNull(brain) || !isReadable(brain)) return false;

        return guarded('采样真实相机俯仰', function () {
            var outputCamera = brainGetOutputCamera(brain, ptr(0));
            if (isNull(outputCamera) || !isReadable(outputCamera)) return false;

            var cameraTransform = componentGetTransform(outputCamera, ptr(0));
            if (isNull(cameraTransform) || !isReadable(cameraTransform)) {
                return false;
            }

            transformGetForward(
                cameraTransform,
                cameraForwardBuffer,
                ptr(0)
            );

            var forward = readVector3(cameraForwardBuffer);
            if (!forward.valid) return false;

            var clampedY = Math.max(-1.0, Math.min(1.0, forward.y));
            var cameraPitch = Math.asin(clampedY) * 180.0 / Math.PI;

            var previous = telemetry.previousCameraPitch;
            var delta = previous === null ? 0.0 : cameraPitch - previous;

            stats.lastCameraForwardY = forward.y;
            stats.lastCameraPitch = cameraPitch;
            stats.lastCameraPitchDelta = delta;

            if (previous !== null && Math.abs(delta) >= 0.05) {
                stats.cameraPitchChangeCount++;
            }

            telemetry.previousCameraPitch = cameraPitch;
            updateRange('cameraPitchMin', 'cameraPitchMax', cameraPitch);
            return true;
        }, false);
    }

    function resetTelemetryForEnable() {
        telemetry.lastLogTime = 0;
        telemetry.lastPitchWrites = stats.pitchWrites;
        telemetry.enabledAt = Date.now();

        telemetry.previousPlayerPitch = null;
        telemetry.previousYAxisWritten = null;
        telemetry.previousCameraPitch = null;

        telemetry.playerPitchMin = null;
        telemetry.playerPitchMax = null;
        telemetry.yAxisMin = null;
        telemetry.yAxisMax = null;
        telemetry.cameraPitchMin = null;
        telemetry.cameraPitchMax = null;
    }

    function emitPitchTelemetry(forceReason) {
        if (!enabled && !forceReason) return;

        var now = Date.now();
        if (!forceReason && now - telemetry.lastLogTime < telemetry.intervalMs) {
            return;
        }

        var writesDelta = stats.pitchWrites - telemetry.lastPitchWrites;
        var elapsedSeconds = telemetry.enabledAt > 0
            ? (now - telemetry.enabledAt) / 1000.0
            : 0.0;

        var playerPitchActive = Math.abs(stats.lastPlayerPitchDelta) >= 0.05;
        var yAxisActive =
            Math.abs(
                stats.lastYAxisWritten -
                (telemetry.previousYAxisWritten === null
                    ? stats.lastYAxisWritten
                    : telemetry.previousYAxisWritten)
            ) >= 0.0005;
        var cameraPitchActive = Math.abs(stats.lastCameraPitchDelta) >= 0.05;

        var mappingExpected = 0.5 + (
            (config.invertY ? -stats.lastPlayerPitch : stats.lastPlayerPitch) *
            config.pitchScale / 180.0
        );
        mappingExpected = Math.max(0.02, Math.min(0.98, mappingExpected));

        sendLog('info', '[PitchTelemetry]', {
            reason: forceReason || 'periodic',
            elapsedSeconds: Number(elapsedSeconds.toFixed(1)),

            state: state,
            enabled: enabled,

            cameraManager: isNull(cameraManager)
                ? null
                : cameraManager.toString(),
            localPlayer: isNull(localPlayer)
                ? null
                : localPlayer.toString(),
            freeLook: isNull(saved.freeLook)
                ? null
                : saved.freeLook.toString(),

            pitchWriteAttempts: stats.pitchWriteAttempts,
            pitchWritesTotal: stats.pitchWrites,
            pitchWritesPerSecond: writesDelta,
            pitchWriteFailures: stats.pitchWriteFailures,
            invalidPitchSamples: stats.invalidPitchSamples,

            playerPitchDeg: Number(stats.lastPlayerPitch.toFixed(4)),
            playerPitchDeltaDeg: Number(
                stats.lastPlayerPitchDelta.toFixed(4)
            ),
            playerPitchChanged: playerPitchActive,
            playerPitchMin: telemetry.playerPitchMin,
            playerPitchMax: telemetry.playerPitchMax,

            yAxisBeforeWrite: Number(
                stats.lastYAxisBeforeWrite.toFixed(6)
            ),
            yAxisWritten: Number(
                stats.lastYAxisWritten.toFixed(6)
            ),
            yAxisAfterFreeLookUpdate: Number(
                stats.lastYAxisAfterUpdate.toFixed(6)
            ),
            yAxisOverwriteDelta: Number(
                stats.lastYAxisOverwriteDelta.toFixed(6)
            ),
            yAxisExpectedFromMapping: Number(
                mappingExpected.toFixed(6)
            ),
            yAxisMin: telemetry.yAxisMin,
            yAxisMax: telemetry.yAxisMax,

            actualCameraPitchSampling: 'disabled_unverified_native_call',
            cameraForwardY: null,
            actualCameraPitchDeg: null,
            actualCameraPitchDeltaDeg: null,
            actualCameraPitchChanged: null,
            cameraPitchMin: null,
            cameraPitchMax: null,

            config: {
                pitchScale: config.pitchScale,
                invertY: config.invertY,
                distance: config.distance,
                pivotHeight: config.pivotHeight,
                screenY: config.screenY,
                fieldOfView: config.fieldOfView
            },

            verdict: {
                inputChanging: playerPitchActive,
                yAxisChanging: yAxisActive,
                cameraChanging: null,
                cameraSamplingDisabled: true,
                yAxisWasOverwritten:
                    Math.abs(stats.lastYAxisOverwriteDelta) >= 0.0005
            }
        });

        stats.telemetryLines++;
        telemetry.lastLogTime = now;
        telemetry.lastPitchWrites = stats.pitchWrites;
        telemetry.previousYAxisWritten = stats.lastYAxisWritten;
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

        stats.pitchWriteAttempts++;

        var result = guarded('同步 Player pitch 到 FreeLook YAxis', function () {
            var pitch = player.add(
                OFF.Player_cameraRotation + 4
            ).readFloat();

            if (!isFinite(pitch) || pitch < -180.0 || pitch > 180.0) {
                stats.invalidPitchSamples++;
                return false;
            }

            var previousPitch = telemetry.previousPlayerPitch;
            var pitchDelta = previousPitch === null
                ? 0.0
                : pitch - previousPitch;

            stats.lastPlayerPitch = pitch;
            stats.lastPlayerPitchDelta = pitchDelta;

            if (previousPitch !== null && Math.abs(pitchDelta) >= 0.05) {
                stats.playerPitchChangeCount++;
            }

            telemetry.previousPlayerPitch = pitch;
            updateRange('playerPitchMin', 'playerPitchMax', pitch);

            var signedPitch = config.invertY ? -pitch : pitch;
            var yAxisValue = 0.5 + (
                signedPitch * config.pitchScale / 180.0
            );

            yAxisValue = Math.max(
                0.02,
                Math.min(0.98, clamp01(yAxisValue))
            );

            var axis = freeLook.add(OFF.CFL_m_YAxis);
            var beforeWrite = axis.add(OFF.AX_Value).readFloat();

            axis.add(OFF.AX_Value).writeFloat(yAxisValue);
            axis.add(OFF.AX_InputAxisValue).writeFloat(0.0);
            axis.add(OFF.AX_MaxSpeed).writeFloat(0.0);

            var afterWrite = axis.add(OFF.AX_Value).readFloat();

            stats.lastYAxisBeforeWrite = beforeWrite;
            stats.lastYAxisWritten = afterWrite;

            if (
                telemetry.previousYAxisWritten !== null &&
                Math.abs(
                    afterWrite - telemetry.previousYAxisWritten
                ) >= 0.0005
            ) {
                stats.yAxisChangeCount++;
            }

            updateRange('yAxisMin', 'yAxisMax', afterWrite);

            stats.pitchWrites++;
            return true;
        }, false);

        if (!result) {
            stats.pitchWriteFailures++;
        }
        return result;
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
        if (!enabled && !enableInProgress) return false;

        var manager = resolveCameraManager();
        var player = resolveLocalPlayer();

        if (isNull(manager) || isNull(player)) return false;

        return guarded('应用最小相机配置', function () {
            sendLog('info', '[MainThread] 相机配置阶段', {
                stage: 'read_freeLook',
                threadId: Process.getCurrentThreadId()
            });

            var freeLook = manager.add(OFF.CM_freeLookCamera).readPointer();
            if (isNull(freeLook) || !isReadable(freeLook)) {
                lastEnableError = 'FreeLook 无效';
                return false;
            }

            var characterContainer = player.add(
                OFF.Player_characterContainer
            ).readPointer();

            if (isNull(characterContainer) || !isReadable(characterContainer)) {
                lastEnableError = 'characterContainer 无效';
                return false;
            }

            sendLog('info', '[MainThread] 相机配置阶段', {
                stage: 'capture_state',
                freeLook: freeLook.toString(),
                characterContainer: characterContainer.toString()
            });
            if (!captureCameraState(freeLook)) {
                lastEnableError = '保存 FreeLook 状态失败';
                return false;
            }

            sendLog('info', '[MainThread] 相机配置阶段', {
                stage: 'set_follow_lookat'
            });
            setFollow(freeLook, characterContainer, ptr(0));
            setLookAt(freeLook, characterContainer, ptr(0));

            sendLog('info', '[MainThread] 相机配置阶段', {
                stage: 'write_orbits'
            });
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

            sendLog('info', '[MainThread] 相机配置阶段', {
                stage: 'configure_yaxis'
            });
            // 启用完成后由 FreeLook Hook 持续驱动。
            lockYAxisForDirectDrive(freeLook);

            sendLog('info', '[MainThread] 相机配置阶段', {
                stage: 'activate_freelook'
            });
            setFreeLookActive(manager, 1, ptr(0));

            sendLog('info', '[MainThread] 相机配置完成', {
                freeLook: freeLook.toString()
            });
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

    function performEnableOnMainThread(options) {
        options = options || {};

        if (enabled) {
            pendingEnable = false;
            return { ok: true, enabled: true, message: '已经启用' };
        }

        if (enableInProgress) {
            return {
                ok: true,
                enabled: false,
                queued: true,
                message: '启用流程正在执行'
            };
        }

        enableInProgress = true;
        stats.enableMainThreadRuns++;
        mainThreadId = Process.getCurrentThreadId();
        lastMainThreadCommand = 'enable';

        sendLog('info', '[MainThread] 开始执行启用', {
            threadId: mainThreadId,
            source: options.source || 'main_thread_queue'
        });

        var manager = resolveCameraManager();
        var player = resolveLocalPlayer();

        if (isNull(manager) || isNull(player)) {
            enableInProgress = false;
            pendingEnable = true;
            stats.queuedEnableRequests++;

            lastEnableError = isNull(manager)
                ? 'CameraManager 未就绪'
                : '本地玩家未就绪';

            sendLog('warning', '[Enable] 已进入等待队列', {
                reason: lastEnableError,
                state: state,
                haveGameManager:
                    !isNull(gameManager) && isReadable(gameManager),
                haveCameraManager:
                    !isNull(cameraManager) && isReadable(cameraManager),
                haveLocalPlayer:
                    !isNull(localPlayer) && isReadable(localPlayer),
                cameraManagerCaptureSource: cameraManagerCaptureSource,
                requestedFrom: options.source || 'rpc'
            });

            return {
                ok: true,
                enabled: false,
                queued: true,
                error: lastEnableError,
                message: '已等待进入对局，CameraManager/本地玩家就绪后自动开启'
            };
        }

        pendingEnable = false;
        lastEnableError = '';
        resetTelemetryForEnable();

        sendLog('info', '[PitchTelemetry] 启用前快照', {
            cameraManager: manager.toString(),
            localPlayer: player.toString(),
            config: config,
            playerCameraRotationAddress:
                player.add(OFF.Player_cameraRotation).toString()
        });

        var modelOk = applyModelMode(player);
        var cameraOk = applyCameraConfiguration();

        if (!cameraOk) {
            enabled = false;
            enableInProgress = false;
            restoreModelMode();
            resetSavedState();
            lastEnableError = '相机配置失败';
            return {
                ok: false,
                enabled: false,
                error: '相机配置失败'
            };
        }

        enabled = true;
        setState(STATE.ENABLED);
        sendLog('info', '最小第三人称 Demo 已启用', {
            modelSwitched: modelOk,
            movementModified: false,
            shootingModified: false,
            characterYawModified: false
        });
        emitPitchTelemetry('enabled');

        enableInProgress = false;

        return {
            ok: true,
            enabled: true,
            queued: false,
            modelSwitched: modelOk
        };
    }

    function performDisableOnMainThread() {
        pendingEnable = false;
        pendingDisable = false;
        pendingReapply = false;
        enableInProgress = false;
        disableInProgress = true;
        stats.disableMainThreadRuns++;
        mainThreadId = Process.getCurrentThreadId();
        lastMainThreadCommand = 'disable';
        lastEnableError = '';

        sendLog('info', '[MainThread] 开始执行关闭', {
            threadId: mainThreadId
        });

        if (!enabled) {
            disableInProgress = false;
            sendLog('info', '[Enable] 已取消等待开启');
            return { ok: true, enabled: false, message: '已经关闭/已取消等待' };
        }

        emitPitchTelemetry('before_disable');
        enabled = false;

        sendLog('info', '[PitchTelemetry] 本次运行汇总', {
            durationSeconds: telemetry.enabledAt > 0
                ? Number(((Date.now() - telemetry.enabledAt) / 1000.0).toFixed(1))
                : 0.0,
            pitchWriteAttempts: stats.pitchWriteAttempts,
            pitchWrites: stats.pitchWrites,
            pitchWriteFailures: stats.pitchWriteFailures,
            invalidPitchSamples: stats.invalidPitchSamples,
            playerPitchChangeCount: stats.playerPitchChangeCount,
            yAxisChangeCount: stats.yAxisChangeCount,
            cameraPitchChangeCount: stats.cameraPitchChangeCount,
            playerPitchRange: [
                telemetry.playerPitchMin,
                telemetry.playerPitchMax
            ],
            yAxisRange: [
                telemetry.yAxisMin,
                telemetry.yAxisMax
            ],
            cameraPitchRange: [
                telemetry.cameraPitchMin,
                telemetry.cameraPitchMax
            ],
            lastYAxisOverwriteDelta:
                stats.lastYAxisOverwriteDelta
        });

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

        disableInProgress = false;
        sendLog('info', '最小第三人称 Demo 已关闭');
        send({ type: 'auto_disabled', result: { ok: true, enabled: false } });
        return { ok: true, enabled: false };
    }

    function requestEnable() {
        pendingDisable = false;
        pendingEnable = true;
        lastEnableError = '';
        stats.queuedEnableRequests++;

        sendLog('info', '[CommandQueue] 已排队开启', {
            state: state,
            haveCameraManager:
                !isNull(cameraManager) && isReadable(cameraManager),
            haveLocalPlayer:
                !isNull(localPlayer) && isReadable(localPlayer)
        });

        return {
            ok: true,
            enabled: enabled,
            queued: !enabled,
            message: enabled
                ? '已经启用'
                : '开启命令已排队，将在游戏主线程执行'
        };
    }

    function requestDisable() {
        pendingEnable = false;
        pendingReapply = false;
        pendingDisable = true;

        sendLog('info', '[CommandQueue] 已排队关闭');

        return {
            ok: true,
            enabled: enabled,
            queued: true,
            message: '关闭命令已排队，将在游戏主线程执行'
        };
    }

    function processMainThreadCommands() {
        if (disableInProgress || enableInProgress) return;

        if (pendingDisable) {
            stats.mainThreadCommands++;
            performDisableOnMainThread();
            return;
        }

        if (pendingEnable && !enabled) {
            var managerReady =
                !isNull(cameraManager) && isReadable(cameraManager);
            var player = resolveLocalPlayer();
            var playerReady = !isNull(player) && isReadable(player);

            if (!managerReady || !playerReady) {
                lastEnableError = !managerReady
                    ? 'CameraManager 未就绪'
                    : '本地玩家未就绪';
                return;
            }

            stats.mainThreadCommands++;
            stats.automaticEnableAttempts++;

            var result = performEnableOnMainThread({
                source: 'CameraManager.Update.command_queue'
            });

            if (result && result.enabled) {
                stats.automaticEnableSuccesses++;
                send({
                    type: 'auto_enabled',
                    result: result
                });
            }
            return;
        }

        if (pendingReapply && enabled) {
            pendingReapply = false;
            stats.mainThreadCommands++;
            stats.reapplyMainThreadRuns++;
            lastMainThreadCommand = 'reapply';

            sendLog('info', '[MainThread] 开始重新应用参数', {
                threadId: Process.getCurrentThreadId()
            });

            var reapplyOk = applyCameraConfiguration();
            sendLog(
                reapplyOk ? 'info' : 'error',
                '[MainThread] 参数重新应用结果',
                { ok: reapplyOk }
            );
        }
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
                        cacheCameraManager(args[0], 'CameraManager.Awake');
                    }
                }
            );

            attach(
                'CameraManager.Update',
                RVA.CameraManager_Update,
                {
                    onEnter: function (args) {
                        stats.cameraUpdates++;

                        // v2.2 关键修复：
                        // 即使脚本错过 Awake，也能从每帧 Update(this) 捕获实例。
                        cacheCameraManager(args[0], 'CameraManager.Update');
                    },
                    onLeave: function () {
                        // 所有 Unity NativeFunction 调用只从这里进入。
                        processMainThreadCommands();
                    }
                }
            );

            attach(
                'CinemachineFreeLook.InternalUpdateCameraState',
                RVA.CinemachineFreeLook_InternalUpdateCameraState,
                {
                    onEnter: function (args) {
                        this.freeLook = null;
                        if (!enabled) return;

                        var freeLook = args[0];
                        if (isNull(freeLook) || !isReadable(freeLook)) return;

                        stats.freeLookUpdateCalls++;
                        this.freeLook = freeLook;

                        // 在 FreeLook 计算本帧 CameraState 之前写入。
                        driveVerticalPitch(freeLook);
                    },
                    onLeave: function () {
                        if (!enabled ||
                            isNull(this.freeLook) ||
                            !isReadable(this.freeLook)) {
                            return;
                        }

                        guarded('验证 FreeLook YAxis 写入结果', function () {
                            var axis = this.freeLook.add(OFF.CFL_m_YAxis);
                            var afterUpdate = axis.add(
                                OFF.AX_Value
                            ).readFloat();

                            stats.lastYAxisAfterUpdate = afterUpdate;
                            stats.lastYAxisOverwriteDelta =
                                afterUpdate - stats.lastYAxisWritten;
                        }.bind(this), null);
                    }
                }
            );

            attach(
                'CameraManager.ChangePVandCV',
                RVA.CameraManager_ChangePVandCV,
                {
                    onEnter: function (args) {
                        cacheCameraManager(
                            args[0],
                            'CameraManager.ChangePVandCV'
                        );
                    },
                    onLeave: function () {
                        if (!enabled) return;

                        // 当前回调虽在游戏线程，但为了避免嵌套调用，
                        // 统一交给下一次 CameraManager.Update。
                        pendingReapply = true;
                        sendLog('info', '[CommandQueue] ChangePVandCV 请求重新应用');
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
                            if (enabled) {
                                emitPitchTelemetry('camera_manager_destroy');
                            }
                            enabled = false;
                            pendingEnable = false;
                            pendingDisable = false;
                            pendingReapply = false;
                            enableInProgress = false;
                            disableInProgress = false;
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
                            pendingEnable = false;
                            pendingDisable = false;
                            pendingReapply = false;
                            enableInProgress = false;
                            disableInProgress = false;
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

                        // v2.3：不再调用未经验证的
                        // Component.get_transform / Transform.get_forward。
                        // 遥测只读取已验证的 Player 与 FreeLook 字段。
                        emitPitchTelemetry(null);
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
        // cleanup 由 Python/Frida RPC 线程调用。
        // 禁止在这里执行任何 Unity NativeFunction。
        pendingEnable = false;
        pendingReapply = false;

        if (enabled) {
            pendingDisable = true;
            sendLog(
                'warning',
                '[CommandQueue] cleanup 收到时功能仍开启；已排队关闭，等待主线程'
            );
            return {
                ok: true,
                queuedDisable: true,
                enabled: true
            };
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

        enable: requestEnable,

        disable: requestDisable,

        setconfig: function (input) {
            var validation = validateConfig(input);
            if (!validation.ok) return validation;

            config = validation.config;

            if (enabled) {
                pendingReapply = true;
            }

            return {
                ok: true,
                queued: enabled,
                config: config,
                message: enabled
                    ? '参数已保存，将在游戏主线程重新应用'
                    : '参数已保存'
            };
        },

        getstatus: function () {
            return {
                ok: true,
                installed: installed,
                enabled: enabled,
                pendingEnable: pendingEnable,
                pendingDisable: pendingDisable,
                pendingReapply: pendingReapply,
                enableInProgress: enableInProgress,
                disableInProgress: disableInProgress,
                lastMainThreadCommand: lastMainThreadCommand,
                mainThreadId: mainThreadId,
                lastEnableError: lastEnableError,
                state: state,
                cameraManagerCaptureSource: cameraManagerCaptureSource,
                cameraManagerCaptureCount: cameraManagerCaptureCount,
                localPlayerCaptureCount: localPlayerCaptureCount,
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
                    telemetry: '1Hz safe memory telemetry; native camera sampling disabled',
                    collision: 'native CinemachineCollider'
                }
            };
        },

        cleanup: cleanup
    };

    sendLog('info', '第三人称最小化 Demo v2.3 脚本已加载', {
        base: base.toString(),
        arch: Process.arch,
        pointerSize: Process.pointerSize
    });
})();
