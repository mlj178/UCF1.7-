(function () {
    'use strict';

    /*
     * UCF1.7 第三人称战斗性能优化版 v3.1
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

    var logRateState = Object.create(null);

    function sendLogRateLimited(key, intervalMs, level, message, extra) {
        var now = Date.now();
        var last = logRateState[key] || 0;
        if (now - last < intervalMs) {
            stats.logMessagesSuppressed++;
            return false;
        }
        logRateState[key] = now;
        sendLog(level, message, extra);
        return true;
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
        Camera_get_pixelWidth:                  0x00328490,
        Camera_get_pixelHeight:                 0x003283F0,
        Camera_get_aspect:                      0x00328090,

        Component_get_transform:               0x0032CF40,
        Component_GetComponentInChildren:      0x0032CC90,
        Transform_get_position_Injected:       0x003F4280,
        Transform_get_forward_Injected:        0x003F3F20,

        Input_GetMouseButton:                  0x00ACFB20,
        Input_GetKeyDown:                      0x00ACFA00,

        Physics_get_defaultPhysicsScene_Injected: 0x00ABB6F0,
        PhysicsScene_Internal_Raycast_Injected:    0x00AB8C20,

        Recoil_GetShootRay:                    0x00B195C0,
        WPN_Gun_Damage:                        0x00B613D0,
        Player_OnEntityDeath:                  0x00B51210,
        Player_SetWeapon:                      0x00B53650,
        Player_Respawn:                        0x00B527A0,
        Player_Spawn:                          0x00B53760,
        CharacterModel_LateUpdate:             0x00B385C0,

        CinemachineCollider_PostPipelineStageCallback: 0x00830700,
        CinemachineCollider_CameraWasDisplaced:        0x0082EDD0,
        CinemachineCollider_GetDisplacementDistance:   0x0082F790,

        Renderer_get_enabled:                 0x003E4D70,
        Renderer_set_enabled:                 0x003E5030,
        Renderer_get_material:                0x003E4BE0,
        Shader_PropertyToID:                  0x003E8AE0,
        Material_HasProperty:                 0x004E1800,
        Material_GetFloat:                    0x004E13D0,
        Material_SetFloat:                    0x004E19A0,
        Material_GetColor_Injected:           0x004E1280,
        Material_SetColor_Injected:           0x004E1870,
        Material_get_renderQueue:             0x004E2560,
        Material_set_renderQueue:             0x004E2830,
        Material_EnableKeyword:               0x004E1250,
        Material_DisableKeyword:              0x004E1220
    };

    var OFF = {
        CM_focusPlayer:          0x0C,
        CM_freeLookCamera:       0x10,
        CM_brain:                0x14,

        GM_allPlayers:           0x1C,

        Player_cameraManager:    0x48,
        Player_cameraRotation:   0x4C,  // Vector2: x=yaw, y=pitch
        Player_recoil:           0x54,
        Player_characterContainer: 0x58,
        Player_currentCharacter: 0x5C,
        Player_playerData:       0x98,
        Player_wpns:             0xA0,

        PD_observeMode:          0x08,
        PD_playerViewModelVisible: 0x24,

        PW_inUse:                0x18,

        Character_cvRenderers:   0x54,
        Character_targetLowerAngle: 0x78,
        Character_lowerAngle:    0x7C,
        WPN_Gun_gunFire:         0x114,
        AimController_ik:        0x0C,
        AimIK_solver:            0x1C,
        IKSolver_IKPosition:     0x08,
        IKSolver_IKPositionWeight: 0x14,

        Collider_MinimumDistanceFromTarget: 0x20,
        Collider_AvoidObstacles: 0x24,
        Collider_CameraRadius:   0x30,
        Collider_Damping:        0x40,
        Collider_DampingWhenOccluded: 0x44,

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
    var sessionDestroyed = false;
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
        invertY: false,

        dynamicShoulder: true,
        shootingRay: true,
        physicsAimRaycast: true,
        maxAimDistance: 1000.0,
        adsFirstPerson: true,
        upperBodyAim: true,
        upperBodyPitchScale: 1.0,
        aimIK: false,
        aimIKWeight: 0.85,
        collisionEnhance: true,
        collisionRadius: 0.25,
        collisionDamping: 0.15,
        collisionOccludedDamping: 0.25,
        occlusionFade: false,
        occlusionFadeStart: 1.15,
        occlusionFadeEnd: 0.55,
        occlusionMinAlpha: 0.12
    };

    var PERF = {
        runtimeIntervalMs: 16,
        finalCameraIntervalMs: 33,
        aimRaycastIntervalMs: 66,
        muzzleIntervalMs: 50,
        shootSolutionIntervalMs: 66,
        inputIntervalMs: 16,
        fadeIntervalMs: 50,
        colliderQueryIntervalMs: 100,
        fovCheckIntervalMs: 250,
        combatLogIntervalMs: 2000,
        visualLogIntervalMs: 2000,
        colliderLogIntervalMs: 2000
    };

    var configRevision = 1;

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
        lifecycleDestroyCount: 0,
        telemetrySuppressed: 0,
        featureAssessmentLines: 0,

        finalCameraSamples: 0,
        finalCameraSampleFailures: 0,
        lastFinalCameraPitch: 0.0,
        aimTargetUpdates: 0,
        aimRaycastHits: 0,
        aimRaycastMisses: 0,
        aimRaycastFailures: 0,
        muzzleObstructionHits: 0,
        lastAimDistance: 0.0,
        muzzleResolves: 0,
        muzzleFailures: 0,
        shootRayCalls: 0,
        shootRayModified: 0,
        shootRaySkipped: 0,
        shootRayFailures: 0,
        damageRayChecks: 0,
        damageRayMatches: 0,
        adsEnterCount: 0,
        adsExitCount: 0,
        shoulderSwapCount: 0,
        colliderCallbacks: 0,
        colliderDisplacedFrames: 0,
        colliderMaxDisplacement: 0.0,
        weaponChangeEvents: 0,
        deathEvents: 0,
        respawnEvents: 0,
        spawnEvents: 0,
        lifecycleReapplyCount: 0,
        upperBodyWrites: 0,
        aimIKSearches: 0,
        aimIKFound: 0,
        aimIKWrites: 0,
        aimIKFailures: 0,
        fadeUpdates: 0,
        fadeMaterialSuccess: 0,
        fadeFallbackHides: 0,
        currentFadeAlpha: 1.0,

        runtimeTicks: 0,
        runtimeTicksSkipped: 0,
        finalCameraSamplesSkipped: 0,
        aimUpdatesSkipped: 0,
        muzzleUpdatesSkipped: 0,
        shootSolutionUpdatesSkipped: 0,
        colliderQueries: 0,
        colliderQueriesSkipped: 0,
        physicsRaycastCalls: 0,
        physicsRaycastDisabledSkips: 0,
        logMessagesSuppressed: 0,

        errors: 0
    };

    var telemetry = {
        activeIntervalMs: 2000,
        idleIntervalMs: 6000,
        lastLogTime: 0,
        lastPitchWrites: 0,
        enabledAt: 0,

        previousPlayerPitch: null,
        previousYAxisWritten: null,
        previousCameraPitch: null,

        previousLoggedPlayerPitch: null,
        previousLoggedYAxis: null,
        lastInputActivityTime: 0,

        playerPitchMin: null,
        playerPitchMax: null,
        yAxisMin: null,
        yAxisMax: null,
        cameraPitchMin: null,
        cameraPitchMax: null
    };

    var cameraForwardBuffer = Memory.alloc(12);
    var transformPositionBuffer = Memory.alloc(12);
    var transformForwardBuffer = Memory.alloc(12);

    var combat = {
        adsActive: false,
        playerDead: false,
        pendingLifecycleRefresh: false,
        finalCamera: { valid:false, camera:null, transform:null, position:null, forward:null, pitchDeg:0, timestamp:0, consecutiveFailures:0, disabledByError:false },
        physics: {
            consecutiveFailures:0,
            disabledByError:false,
            totalFailures:0,
            lastError:null
        },
        timing: {
            lastRuntime:0,
            lastFinalCamera:0,
            lastAimRaycast:0,
            lastMuzzle:0,
            lastShootSolution:0,
            lastInput:0,
            lastFade:0,
            lastFovCheck:0
        },
        aimTarget: { valid:false, point:null, distance:0, hit:false, colliderId:0, reason:'none', timestamp:0 },
        muzzle: { valid:false, weapon:null, transform:null, position:null, source:'none', timestamp:0 },
        shootSolution: { valid:false, origin:null, direction:null, targetPoint:null, cameraTargetHit:false, muzzleObstructionHit:false, distance:0, reason:'none', timestamp:0 },
        lastModifiedRay: null,
        lastCombatLog: 0,
        lastVisualLog: 0,
        lastCollisionLog: 0,
        lastFadeLog: 0,
        collider: {
            pointer:null,
            vcam:null,
            original:null,
            displaced:false,
            distance:0,
            queryFailures:0,
            telemetryDisabled:false,
            appliedRevision:-1,
            lastQueryTime:0
        },
        aimIK: { character:null, component:null, solver:null, originalWeight:0, found:false, reason:'not_searched' },
        renderers: { character:null, entries:[], captured:false, usingMaterialFade:false, hiddenFallback:false },
        materialIds: null,
        keywordStrings: null
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
        originalFov: -1.0,
        upperBodyTargetOriginal: null
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

    var transformGetPosition = new NativeFunction(
        base.add(RVA.Transform_get_position_Injected),
        'void',
        ['pointer', 'pointer', 'pointer'],
        CALL_CONV
    );

    var cameraGetPixelWidth = new NativeFunction(
        base.add(RVA.Camera_get_pixelWidth), 'int', ['pointer','pointer'], CALL_CONV
    );
    var cameraGetPixelHeight = new NativeFunction(
        base.add(RVA.Camera_get_pixelHeight), 'int', ['pointer','pointer'], CALL_CONV
    );
    var cameraGetAspect = new NativeFunction(
        base.add(RVA.Camera_get_aspect), 'float', ['pointer','pointer'], CALL_CONV
    );
    var inputGetMouseButton = new NativeFunction(
        base.add(RVA.Input_GetMouseButton), 'bool', ['int','pointer'], CALL_CONV
    );
    var inputGetKeyDown = new NativeFunction(
        base.add(RVA.Input_GetKeyDown), 'bool', ['int','pointer'], CALL_CONV
    );
    var physicsGetDefaultSceneInjected = new NativeFunction(
        base.add(RVA.Physics_get_defaultPhysicsScene_Injected),
        'void',
        ['pointer', 'pointer'],
        CALL_CONV
    );
    var physicsInternalRaycastInjected = new NativeFunction(
        base.add(RVA.PhysicsScene_Internal_Raycast_Injected),
        'bool',
        ['pointer', 'pointer', 'float', 'pointer', 'int', 'int', 'pointer'],
        CALL_CONV
    );
    var componentGetComponentInChildren = new NativeFunction(
        base.add(RVA.Component_GetComponentInChildren), 'pointer', ['pointer','pointer','bool','pointer'], CALL_CONV
    );
    var colliderCameraWasDisplaced = new NativeFunction(
        base.add(RVA.CinemachineCollider_CameraWasDisplaced), 'bool', ['pointer','pointer','pointer'], CALL_CONV
    );
    var colliderGetDisplacementDistance = new NativeFunction(
        base.add(RVA.CinemachineCollider_GetDisplacementDistance), 'float', ['pointer','pointer','pointer'], CALL_CONV
    );
    var rendererGetEnabled = new NativeFunction(
        base.add(RVA.Renderer_get_enabled), 'bool', ['pointer','pointer'], CALL_CONV
    );
    var rendererSetEnabled = new NativeFunction(
        base.add(RVA.Renderer_set_enabled), 'void', ['pointer','bool','pointer'], CALL_CONV
    );
    var rendererGetMaterial = new NativeFunction(
        base.add(RVA.Renderer_get_material), 'pointer', ['pointer','pointer'], CALL_CONV
    );
    var shaderPropertyToID = new NativeFunction(
        base.add(RVA.Shader_PropertyToID), 'int', ['pointer','pointer'], CALL_CONV
    );
    var materialHasProperty = new NativeFunction(
        base.add(RVA.Material_HasProperty), 'bool', ['pointer','int','pointer'], CALL_CONV
    );
    var materialGetFloat = new NativeFunction(
        base.add(RVA.Material_GetFloat), 'float', ['pointer','int','pointer'], CALL_CONV
    );
    var materialSetFloat = new NativeFunction(
        base.add(RVA.Material_SetFloat), 'void', ['pointer','int','float','pointer'], CALL_CONV
    );
    var materialGetColorInjected = new NativeFunction(
        base.add(RVA.Material_GetColor_Injected), 'void', ['pointer','int','pointer','pointer'], CALL_CONV
    );
    var materialSetColorInjected = new NativeFunction(
        base.add(RVA.Material_SetColor_Injected), 'void', ['pointer','int','pointer','pointer'], CALL_CONV
    );
    var materialGetRenderQueue = new NativeFunction(
        base.add(RVA.Material_get_renderQueue), 'int', ['pointer','pointer'], CALL_CONV
    );
    var materialSetRenderQueue = new NativeFunction(
        base.add(RVA.Material_set_renderQueue), 'void', ['pointer','int','pointer'], CALL_CONV
    );
    var materialEnableKeyword = new NativeFunction(
        base.add(RVA.Material_EnableKeyword), 'void', ['pointer','pointer','pointer'], CALL_CONV
    );
    var materialDisableKeyword = new NativeFunction(
        base.add(RVA.Material_DisableKeyword), 'void', ['pointer','pointer','pointer'], CALL_CONV
    );

    var il2cppStringNew = null;
    var il2cppGcHandleNew = null;
    var il2cppGcHandleFree = null;
    var il2cppDomainGet = null;
    var il2cppDomainGetAssemblies = null;
    var il2cppAssemblyGetImage = null;
    var il2cppClassFromName = null;
    var il2cppClassGetType = null;
    var il2cppTypeGetObject = null;

    guarded('初始化 IL2CPP 字符串 API', function () {
        var stringNewAddress = findExport('il2cpp_string_new');
        var handleNewAddress = findExport('il2cpp_gchandle_new');
        var handleFreeAddress = findExport('il2cpp_gchandle_free');
        var domainGetAddress = findExport('il2cpp_domain_get');
        var domainGetAssembliesAddress = findExport('il2cpp_domain_get_assemblies');
        var assemblyGetImageAddress = findExport('il2cpp_assembly_get_image');
        var classFromNameAddress = findExport('il2cpp_class_from_name');
        var classGetTypeAddress = findExport('il2cpp_class_get_type');
        var typeGetObjectAddress = findExport('il2cpp_type_get_object');

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
            il2cppGcHandleFree = new NativeFunction(handleFreeAddress, 'void', ['uint32']);
        }
        if (!isNull(domainGetAddress)) il2cppDomainGet = new NativeFunction(domainGetAddress, 'pointer', []);
        if (!isNull(domainGetAssembliesAddress)) il2cppDomainGetAssemblies = new NativeFunction(domainGetAssembliesAddress, 'pointer', ['pointer','pointer']);
        if (!isNull(assemblyGetImageAddress)) il2cppAssemblyGetImage = new NativeFunction(assemblyGetImageAddress, 'pointer', ['pointer']);
        if (!isNull(classFromNameAddress)) il2cppClassFromName = new NativeFunction(classFromNameAddress, 'pointer', ['pointer','pointer','pointer']);
        if (!isNull(classGetTypeAddress)) il2cppClassGetType = new NativeFunction(classGetTypeAddress, 'pointer', ['pointer']);
        if (!isNull(typeGetObjectAddress)) il2cppTypeGetObject = new NativeFunction(typeGetObjectAddress, 'pointer', ['pointer']);
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
        if (isNull(instance)) return false;

        var changed =
            isNull(cameraManager) ||
            !cameraManager.equals(instance);

        if (changed && !isReadable(instance)) return false;

        cameraManager = instance;
        sessionDestroyed = false;
        cameraManagerCaptureSource = source || 'unknown';

        if (changed) {
            combat.finalCamera.disabledByError = false;
            combat.finalCamera.consecutiveFailures = 0;
            combat.physics.disabledByError = false;
            combat.physics.consecutiveFailures = 0;
            combat.physics.totalFailures = 0;

            combat.timing.lastRuntime = 0;
            combat.timing.lastFinalCamera = 0;
            combat.timing.lastAimRaycast = 0;
            combat.timing.lastMuzzle = 0;
            combat.timing.lastShootSolution = 0;
            combat.timing.lastInput = 0;
            combat.timing.lastFade = 0;
            combat.timing.lastFovCheck = 0;

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

    // ============================================================
    // v3.1 战斗集成与性能调度模块
    // ============================================================

    function v3(x, y, z) {
        return { x:x, y:y, z:z, valid:true };
    }

    function v3Add(a, b) {
        return v3(a.x + b.x, a.y + b.y, a.z + b.z);
    }

    function v3Sub(a, b) {
        return v3(a.x - b.x, a.y - b.y, a.z - b.z);
    }

    function v3Scale(a, scale) {
        return v3(a.x * scale, a.y * scale, a.z * scale);
    }

    function v3Length(a) {
        return Math.sqrt(a.x * a.x + a.y * a.y + a.z * a.z);
    }

    function v3Normalize(a) {
        var length = v3Length(a);
        if (!isFinite(length) || length < 0.00001) {
            return { x:0, y:0, z:1, valid:false };
        }
        return v3(a.x / length, a.y / length, a.z / length);
    }

    function v3Distance(a, b) {
        return v3Length(v3Sub(a, b));
    }

    function v3Angle(a, b) {
        var na = v3Normalize(a);
        var nb = v3Normalize(b);
        if (!na.valid || !nb.valid) return 180.0;
        var dot = na.x * nb.x + na.y * nb.y + na.z * nb.z;
        dot = Math.max(-1.0, Math.min(1.0, dot));
        return Math.acos(dot) * 180.0 / Math.PI;
    }

    function readRayAt(pointer) {
        if (isNull(pointer)) return { valid:false };
        try {
            var origin = readVector3(pointer);
            var direction = readVector3(pointer.add(12));
            return {
                origin: origin,
                direction: direction,
                valid: origin.valid && direction.valid
            };
        } catch (_) {
            return { valid:false };
        }
    }

    function writeRayAt(pointer, origin, direction) {
        if (isNull(pointer)) return false;
        try {
            pointer.writeFloat(origin.x);
            pointer.add(4).writeFloat(origin.y);
            pointer.add(8).writeFloat(origin.z);
            pointer.add(12).writeFloat(direction.x);
            pointer.add(16).writeFloat(direction.y);
            pointer.add(20).writeFloat(direction.z);
            return true;
        } catch (_) {
            return false;
        }
    }

    var physicsSceneBuffer = Memory.alloc(4);
    var physicsRayBuffer = Memory.alloc(24);
    var physicsHitBuffer = Memory.alloc(0x2C);

    function clearBuffer(pointer, size) {
        var offset = 0;
        while (offset + 4 <= size) {
            pointer.add(offset).writeU32(0);
            offset += 4;
        }
        while (offset < size) {
            pointer.add(offset).writeU8(0);
            offset++;
        }
    }

    function physicsRaycastMainThread(origin, direction, maxDistance) {
        if (!config.physicsAimRaycast) {
            return { hit:false, reason:'disabled' };
        }
        if (combat.physics.disabledByError) {
            stats.physicsRaycastDisabledSkips++;
            return { hit:false, reason:'disabled_after_errors' };
        }

        stats.physicsRaycastCalls++;

        try {
            var normalized = v3Normalize(direction);
            if (!normalized.valid) {
                return { hit:false, reason:'invalid_direction' };
            }

            clearBuffer(physicsHitBuffer, 0x2C);
            physicsGetDefaultSceneInjected(physicsSceneBuffer, ptr(0));
            writeRayAt(physicsRayBuffer, origin, normalized);

            var hit = physicsInternalRaycastInjected(
                physicsSceneBuffer,
                physicsRayBuffer,
                maxDistance,
                physicsHitBuffer,
                -1,
                0,
                ptr(0)
            );

            combat.physics.consecutiveFailures = 0;

            if (!hit) return { hit:false, reason:'no_hit' };

            var point = readVector3(physicsHitBuffer);
            var normal = readVector3(physicsHitBuffer.add(0x0C));
            var distance = physicsHitBuffer.add(0x1C).readFloat();
            var colliderId = physicsHitBuffer.add(0x28).readS32();

            if (!point.valid || !normal.valid ||
                !isFinite(distance) || distance < 0 ||
                distance > maxDistance + 1.0) {
                stats.aimRaycastFailures++;
                return { hit:false, reason:'invalid_hit' };
            }

            return {
                hit:true,
                reason:'physics_hit',
                point:point,
                normal:normal,
                distance:distance,
                colliderId:colliderId
            };
        } catch (error) {
            stats.errors++;
            stats.aimRaycastFailures++;
            combat.physics.consecutiveFailures++;
            combat.physics.totalFailures++;
            combat.physics.lastError = String(error);

            sendLogRateLimited(
                'physics_aim_error',
                3000,
                'error',
                '[PhysicsAim] 射线调用失败',
                {
                    error:String(error),
                    consecutiveFailures:
                        combat.physics.consecutiveFailures,
                    totalFailures:
                        combat.physics.totalFailures
                }
            );

            if (combat.physics.consecutiveFailures >= 3) {
                combat.physics.disabledByError = true;
                sendLog('warning', '[PhysicsAim] 已熔断，改用远点目标', {
                    reason:'three_consecutive_failures',
                    totalFailures:combat.physics.totalFailures
                });
            }
            return { hit:false, reason:'exception_fallback' };
        }
    }

    function safeTransformPosition(transform) {
        if (isNull(transform)) {
            return { x:0, y:0, z:0, valid:false };
        }
        return guarded('读取 Transform.position', function () {
            transformGetPosition(
                transform,
                transformPositionBuffer,
                ptr(0)
            );
            return readVector3(transformPositionBuffer);
        }, { x:0, y:0, z:0, valid:false });
    }

    function safeTransformForward(transform) {
        if (isNull(transform)) {
            return { x:0, y:0, z:1, valid:false };
        }
        return guarded('读取 Transform.forward', function () {
            transformGetForward(
                transformForwardBuffer,
                transform,
                ptr(0)
            );
            var value = readVector3(transformForwardBuffer);
            return value.valid ? v3Normalize(value) : value;
        }, { x:0, y:0, z:1, valid:false });
    }

    function sampleFinalCameraOnMainThread(brain, force) {
        if (!enabled || combat.adsActive ||
            isNull(brain) ||
            combat.finalCamera.disabledByError) {
            return false;
        }

        var now = Date.now();
        if (!force &&
            now - combat.timing.lastFinalCamera <
                PERF.finalCameraIntervalMs) {
            stats.finalCameraSamplesSkipped++;
            return combat.finalCamera.valid;
        }
        combat.timing.lastFinalCamera = now;

        try {
            var camera = combat.finalCamera.camera;
            var transform = combat.finalCamera.transform;

            if (isNull(camera) || isNull(transform)) {
                camera = brainGetOutputCamera(brain, ptr(0));
                if (isNull(camera) || !isReadable(camera)) {
                    stats.finalCameraSampleFailures++;
                    return false;
                }

                transform = componentGetTransform(camera, ptr(0));
                if (isNull(transform) || !isReadable(transform)) {
                    stats.finalCameraSampleFailures++;
                    return false;
                }

                combat.finalCamera.camera = camera;
                combat.finalCamera.transform = transform;
            }

            var position = safeTransformPosition(transform);
            var forward = safeTransformForward(transform);
            if (!position.valid || !forward.valid) {
                stats.finalCameraSampleFailures++;
                return false;
            }

            var pitch = Math.asin(
                Math.max(-1.0, Math.min(1.0, forward.y))
            ) * 180.0 / Math.PI;

            combat.finalCamera.valid = true;
            combat.finalCamera.position = position;
            combat.finalCamera.forward = forward;
            combat.finalCamera.pitchDeg = pitch;
            combat.finalCamera.timestamp = now;
            combat.finalCamera.consecutiveFailures = 0;

            stats.finalCameraSamples++;
            stats.lastFinalCameraPitch = pitch;
            return true;
        } catch (error) {
            stats.errors++;
            stats.finalCameraSampleFailures++;
            combat.finalCamera.consecutiveFailures++;
            combat.finalCamera.valid = false;
            combat.finalCamera.camera = null;
            combat.finalCamera.transform = null;

            sendLogRateLimited(
                'final_camera_error',
                3000,
                'error',
                '[FinalCamera] 采样失败',
                {
                    error:String(error),
                    consecutiveFailures:
                        combat.finalCamera.consecutiveFailures
                }
            );

            if (combat.finalCamera.consecutiveFailures >= 3) {
                combat.finalCamera.disabledByError = true;
                sendLog('warning', '[FinalCamera] 已自动禁用独立采样', {
                    reason:'three_consecutive_failures'
                });
            }
            return false;
        }
    }

    function updateAimTargetOnMainThread(force) {
        if (!enabled || combat.adsActive || combat.playerDead ||
            !combat.finalCamera.valid ||
            combat.finalCamera.position === null ||
            combat.finalCamera.forward === null) {
            return false;
        }

        var now = Date.now();
        if (!force &&
            now - combat.timing.lastAimRaycast <
                PERF.aimRaycastIntervalMs) {
            stats.aimUpdatesSkipped++;
            return combat.aimTarget.valid;
        }
        combat.timing.lastAimRaycast = now;

        var targetHit = physicsRaycastMainThread(
            combat.finalCamera.position,
            combat.finalCamera.forward,
            config.maxAimDistance
        );

        combat.aimTarget.valid = true;
        combat.aimTarget.hit = !!targetHit.hit;
        combat.aimTarget.colliderId = targetHit.colliderId || 0;
        combat.aimTarget.reason = targetHit.reason;

        if (targetHit.hit) {
            combat.aimTarget.point = targetHit.point;
            combat.aimTarget.distance = targetHit.distance;
            stats.aimRaycastHits++;
        } else {
            combat.aimTarget.distance = config.maxAimDistance;
            combat.aimTarget.point = v3Add(
                combat.finalCamera.position,
                v3Scale(
                    combat.finalCamera.forward,
                    config.maxAimDistance
                )
            );
            stats.aimRaycastMisses++;
        }

        combat.aimTarget.timestamp = now;
        stats.lastAimDistance = combat.aimTarget.distance;
        stats.aimTargetUpdates++;
        return true;
    }

    function clearMuzzleCache(reason) {
        combat.muzzle.valid = false;
        combat.muzzle.weapon = null;
        combat.muzzle.transform = null;
        combat.muzzle.position = null;
        combat.muzzle.source = 'none';
        combat.muzzle.timestamp = 0;
        if (reason) {
            sendLog('info', '[WeaponLifecycle] 枪口缓存已清空', {
                reason: reason
            });
        }
    }

    function updateMuzzleOnMainThread(force) {
        if (!enabled || combat.adsActive || combat.playerDead) return false;

        var now = Date.now();
        if (!force &&
            now - combat.timing.lastMuzzle < PERF.muzzleIntervalMs) {
            stats.muzzleUpdatesSkipped++;
            return combat.muzzle.valid;
        }
        combat.timing.lastMuzzle = now;

        var player = localPlayer;
        if (isNull(player)) player = resolveLocalPlayer();
        if (isNull(player)) return false;

        return guarded('更新枪口缓存', function () {
            var weapons = player.add(OFF.Player_wpns).readPointer();
            if (isNull(weapons) || !isReadable(weapons)) {
                stats.muzzleFailures++;
                return false;
            }

            var weapon = weapons.add(OFF.PW_inUse).readPointer();
            if (isNull(weapon) || !isReadable(weapon)) {
                stats.muzzleFailures++;
                return false;
            }

            var needResolve = !combat.muzzle.valid ||
                isNull(combat.muzzle.weapon) ||
                !combat.muzzle.weapon.equals(weapon) ||
                isNull(combat.muzzle.transform) ||
                !isReadable(combat.muzzle.transform);

            if (needResolve) {
                clearMuzzleCache(null);
                combat.muzzle.weapon = weapon;

                var transform = null;
                var source = 'none';
                try {
                    var gunFire = weapon.add(OFF.WPN_Gun_gunFire).readPointer();
                    if (!isNull(gunFire) && isReadable(gunFire)) {
                        transform = componentGetTransform(gunFire, ptr(0));
                        if (!isNull(transform) && isReadable(transform)) {
                            source = 'WPN_Gun.gunFire';
                        }
                    }
                } catch (_) {
                }

                if (isNull(transform) || !isReadable(transform)) {
                    transform = componentGetTransform(weapon, ptr(0));
                    if (!isNull(transform) && isReadable(transform)) {
                        source = 'weapon.transform_fallback';
                    }
                }

                if (isNull(transform) || !isReadable(transform)) {
                    stats.muzzleFailures++;
                    return false;
                }

                combat.muzzle.transform = transform;
                combat.muzzle.source = source;
                combat.muzzle.valid = true;
                stats.muzzleResolves++;

                sendLog('info', '[Muzzle] 枪口已解析', {
                    weapon: weapon.toString(),
                    transform: transform.toString(),
                    source: source,
                    resolveCount: stats.muzzleResolves
                });
            }

            var position = safeTransformPosition(combat.muzzle.transform);
            if (!position.valid) {
                stats.muzzleFailures++;
                combat.muzzle.valid = false;
                return false;
            }

            combat.muzzle.position = position;
            combat.muzzle.timestamp = Date.now();
            return true;
        }, false);
    }

    function updateShootSolutionOnMainThread(force) {
        if (!enabled || combat.adsActive || combat.playerDead ||
            !config.shootingRay ||
            !combat.aimTarget.valid ||
            !combat.muzzle.valid ||
            combat.aimTarget.point === null ||
            combat.muzzle.position === null) {
            combat.shootSolution.valid = false;
            return false;
        }

        var now = Date.now();
        if (!force &&
            now - combat.timing.lastShootSolution <
                PERF.shootSolutionIntervalMs) {
            stats.shootSolutionUpdatesSkipped++;
            return combat.shootSolution.valid;
        }
        combat.timing.lastShootSolution = now;

        var origin = combat.muzzle.position;
        var target = combat.aimTarget.point;
        var direction = v3Normalize(v3Sub(target, origin));
        if (!direction.valid) {
            combat.shootSolution.valid = false;
            combat.shootSolution.reason = 'invalid_direction';
            return false;
        }

        var targetDistance = v3Distance(origin, target);
        var obstruction = physicsRaycastMainThread(
            origin,
            direction,
            targetDistance
        );
        var finalTarget = target;

        if (obstruction.hit &&
            obstruction.distance + 0.02 < targetDistance) {
            finalTarget = obstruction.point;
            direction = v3Normalize(
                v3Sub(finalTarget, origin)
            );
            targetDistance = obstruction.distance;
            stats.muzzleObstructionHits++;
        }

        combat.shootSolution.valid = direction.valid;
        combat.shootSolution.origin = origin;
        combat.shootSolution.direction = direction;
        combat.shootSolution.targetPoint = finalTarget;
        combat.shootSolution.cameraTargetHit =
            combat.aimTarget.hit;
        combat.shootSolution.muzzleObstructionHit =
            !!obstruction.hit;
        combat.shootSolution.distance = targetDistance;
        combat.shootSolution.reason = obstruction.hit
            ? 'muzzle_obstruction_or_target'
            : combat.aimTarget.reason;
        combat.shootSolution.timestamp = Date.now();
        return combat.shootSolution.valid;
    }

    function buildCombatShootRay() {
        if (!combat.shootSolution.valid ||
            combat.shootSolution.origin === null ||
            combat.shootSolution.direction === null ||
            Date.now() - combat.shootSolution.timestamp > 300) {
            return { valid:false, reason:'solution_not_ready_or_stale' };
        }

        return {
            valid:true,
            reason:combat.shootSolution.reason,
            origin:combat.shootSolution.origin,
            direction:combat.shootSolution.direction,
            targetPoint:combat.shootSolution.targetPoint,
            cameraTargetHit:combat.shootSolution.cameraTargetHit,
            muzzleObstructionHit:
                combat.shootSolution.muzzleObstructionHit,
            distance:combat.shootSolution.distance
        };
    }

    function isLocalPlayerObject(candidate) {
        var player = resolveLocalPlayer();
        return !isNull(candidate) && !isNull(player) &&
            isReadable(candidate) && candidate.equals(player);
    }

    function isLocalCharacter(candidate) {
        if (isNull(candidate)) return false;

        var character = saved.character;
        if (isNull(character) && !isNull(localPlayer)) {
            try {
                character = localPlayer.add(
                    OFF.Player_currentCharacter
                ).readPointer();
                if (!isNull(character)) saved.character = character;
            } catch (_) {
                return false;
            }
        }

        return !isNull(character) && candidate.equals(character);
    }

    function enterAdsOnMainThread() {
        if (!enabled || combat.adsActive || !config.adsFirstPerson) return;
        combat.adsActive = true;
        restoreAimIK(false);
        restoreCharacterVisibility();
        restoreCameraState();
        restoreModelMode();
        if (!isNull(cameraManager) && isReadable(cameraManager)) {
            setFreeLookActive(cameraManager, 0, ptr(0));
        }
        stats.adsEnterCount++;
        sendLog('info', '[ADS] 进入第一人称精确瞄准', {
            enterCount: stats.adsEnterCount
        });
    }

    function exitAdsOnMainThread() {
        if (!enabled || !combat.adsActive) return;
        combat.adsActive = false;
        var player = resolveLocalPlayer();
        if (!isNull(player)) {
            applyModelMode(player);
            applyCameraConfiguration();
        }
        stats.adsExitCount++;
        sendLog('info', '[ADS] 退出瞄准并恢复第三人称', {
            exitCount: stats.adsExitCount
        });
    }

    function updateInputFeaturesOnMainThread() {
        if (!enabled || combat.playerDead) return;

        var now = Date.now();
        if (now - combat.timing.lastInput < PERF.inputIntervalMs) {
            return;
        }
        combat.timing.lastInput = now;

        if (config.adsFirstPerson) {
            var adsPressed = guarded('读取鼠标右键', function () {
                return inputGetMouseButton(1, ptr(0));
            }, false);
            if (adsPressed && !combat.adsActive) enterAdsOnMainThread();
            if (!adsPressed && combat.adsActive) exitAdsOnMainThread();
        }

        if (config.dynamicShoulder && !combat.adsActive) {
            var swap = guarded('读取换肩热键', function () {
                return inputGetKeyDown(118, ptr(0));
            }, false);
            if (swap) {
                config.shoulder = config.shoulder === 'left' ? 'right' : 'left';
                pendingReapply = true;
                stats.shoulderSwapCount++;
                sendLog('info', '[Shoulder] V 键动态换肩', {
                    shoulder: config.shoulder,
                    count: stats.shoulderSwapCount
                });
                send({ type:'shoulder_changed', shoulder:config.shoulder });
            }
        }
    }

    function findManagedType(namespaceName, className) {
        if (il2cppDomainGet === null || il2cppDomainGetAssemblies === null ||
            il2cppAssemblyGetImage === null || il2cppClassFromName === null ||
            il2cppClassGetType === null || il2cppTypeGetObject === null) {
            return null;
        }

        return guarded('查找托管类型 ' + namespaceName + '.' + className, function () {
            var domain = il2cppDomainGet();
            if (isNull(domain)) return null;
            var countBuf = Memory.alloc(PTR_SIZE);
            countBuf.writeU32(0);
            var assemblies = il2cppDomainGetAssemblies(domain, countBuf);
            var count = countBuf.readU32();
            if (isNull(assemblies) || count < 1 || count > 512) return null;

            var namespaceUtf8 = Memory.allocUtf8String(namespaceName);
            var classUtf8 = Memory.allocUtf8String(className);
            for (var index = 0; index < count; index++) {
                var assembly = assemblies.add(index * PTR_SIZE).readPointer();
                if (isNull(assembly)) continue;
                var image = il2cppAssemblyGetImage(assembly);
                if (isNull(image)) continue;
                var klass = il2cppClassFromName(image, namespaceUtf8, classUtf8);
                if (isNull(klass)) continue;
                var type = il2cppClassGetType(klass);
                if (isNull(type)) continue;
                var typeObject = il2cppTypeGetObject(type);
                if (!isNull(typeObject) && isReadable(typeObject)) return typeObject;
            }
            return null;
        }, null);
    }

    var aimIKTypeObject = null;
    var aimControllerTypeObject = null;

    function resolveAimIKOnMainThread(character) {
        if (!config.aimIK || isNull(character) || !isReadable(character)) return false;
        if (combat.aimIK.found && !isNull(combat.aimIK.solver) &&
            isReadable(combat.aimIK.solver) && !isNull(combat.aimIK.character) &&
            combat.aimIK.character.equals(character)) return true;

        if (!isNull(combat.aimIK.character) &&
            combat.aimIK.character.equals(character) &&
            combat.aimIK.reason === 'not_found') return false;

        stats.aimIKSearches++;
        combat.aimIK.character = character;
        combat.aimIK.component = null;
        combat.aimIK.solver = null;
        combat.aimIK.found = false;

        if (aimIKTypeObject === null) {
            aimIKTypeObject = findManagedType('RootMotion.FinalIK', 'AimIK');
        }
        if (aimControllerTypeObject === null) {
            aimControllerTypeObject = findManagedType('RootMotion.FinalIK', 'AimController');
        }

        var aimIK = null;
        if (!isNull(aimIKTypeObject)) {
            aimIK = componentGetComponentInChildren(character, aimIKTypeObject, true, ptr(0));
        }

        if ((isNull(aimIK) || !isReadable(aimIK)) && !isNull(aimControllerTypeObject)) {
            var controller = componentGetComponentInChildren(
                character, aimControllerTypeObject, true, ptr(0)
            );
            if (!isNull(controller) && isReadable(controller)) {
                aimIK = controller.add(OFF.AimController_ik).readPointer();
            }
        }

        if (isNull(aimIK) || !isReadable(aimIK)) {
            combat.aimIK.reason = 'not_found';
            sendLog('warning', '[AimIK] 当前人物模型未找到 AimIK，使用上半身角度回退');
            return false;
        }

        var solver = aimIK.add(OFF.AimIK_solver).readPointer();
        if (isNull(solver) || !isReadable(solver)) {
            combat.aimIK.reason = 'solver_invalid';
            stats.aimIKFailures++;
            return false;
        }

        combat.aimIK.component = aimIK;
        combat.aimIK.solver = solver;
        combat.aimIK.originalWeight = solver.add(
            OFF.IKSolver_IKPositionWeight
        ).readFloat();
        combat.aimIK.found = true;
        combat.aimIK.reason = 'ok';
        stats.aimIKFound++;
        sendLog('info', '[AimIK] 组件已解析', {
            component: aimIK.toString(),
            solver: solver.toString(),
            originalWeight: combat.aimIK.originalWeight
        });
        return true;
    }

    function writeAimIKOnMainThread(character) {
        if (!enabled || combat.adsActive || combat.playerDead ||
            !config.aimIK || !combat.aimTarget.valid) return false;
        if (!resolveAimIKOnMainThread(character)) return false;

        return guarded('写入 AimIK 目标', function () {
            var solver = combat.aimIK.solver;
            var point = combat.aimTarget.point;
            solver.add(OFF.IKSolver_IKPosition).writeFloat(point.x);
            solver.add(OFF.IKSolver_IKPosition + 4).writeFloat(point.y);
            solver.add(OFF.IKSolver_IKPosition + 8).writeFloat(point.z);
            solver.add(OFF.IKSolver_IKPositionWeight).writeFloat(config.aimIKWeight);
            stats.aimIKWrites++;
            return true;
        }, false);
    }

    function restoreAimIK(clearCache) {
        if (!isNull(combat.aimIK.solver) && isReadable(combat.aimIK.solver)) {
            guarded('恢复 AimIK 权重', function () {
                combat.aimIK.solver.add(
                    OFF.IKSolver_IKPositionWeight
                ).writeFloat(combat.aimIK.originalWeight);
            }, null);
        }
        if (clearCache) {
            combat.aimIK.character = null;
            combat.aimIK.component = null;
            combat.aimIK.solver = null;
            combat.aimIK.originalWeight = 0;
            combat.aimIK.found = false;
            combat.aimIK.reason = 'cleared';
        }
    }

    function initializeFadeResources() {
        if (combat.materialIds !== null) return true;
        if (il2cppStringNew === null) return false;
        return guarded('初始化人物淡出资源', function () {
            function managed(text) {
                return il2cppStringNew(Memory.allocUtf8String(text));
            }
            var color = managed('_Color');
            var baseColor = managed('_BaseColor');
            var mode = managed('_Mode');
            var surface = managed('_Surface');
            var srcBlend = managed('_SrcBlend');
            var dstBlend = managed('_DstBlend');
            var zWrite = managed('_ZWrite');
            combat.materialIds = {
                color: shaderPropertyToID(color, ptr(0)),
                baseColor: shaderPropertyToID(baseColor, ptr(0)),
                mode: shaderPropertyToID(mode, ptr(0)),
                surface: shaderPropertyToID(surface, ptr(0)),
                srcBlend: shaderPropertyToID(srcBlend, ptr(0)),
                dstBlend: shaderPropertyToID(dstBlend, ptr(0)),
                zWrite: shaderPropertyToID(zWrite, ptr(0))
            };
            combat.keywordStrings = {
                alphaBlend: managed('_ALPHABLEND_ON'),
                alphaTest: managed('_ALPHATEST_ON'),
                alphaPremul: managed('_ALPHAPREMULTIPLY_ON')
            };
            return true;
        }, false);
    }

    function getMaterialColor(material, propertyId) {
        var buffer = Memory.alloc(16);
        return guarded('读取材质颜色', function () {
            materialGetColorInjected(material, propertyId, buffer, ptr(0));
            return {
                r:buffer.readFloat(), g:buffer.add(4).readFloat(),
                b:buffer.add(8).readFloat(), a:buffer.add(12).readFloat(), valid:true
            };
        }, { r:1,g:1,b:1,a:1,valid:false });
    }

    function setMaterialColor(material, propertyId, color) {
        var buffer = Memory.alloc(16);
        buffer.writeFloat(color.r);
        buffer.add(4).writeFloat(color.g);
        buffer.add(8).writeFloat(color.b);
        buffer.add(12).writeFloat(color.a);
        materialSetColorInjected(material, propertyId, buffer, ptr(0));
    }

    function captureCharacterRenderers(character) {
        if (!config.occlusionFade || isNull(character) || !isReadable(character)) return false;
        if (combat.renderers.captured && !isNull(combat.renderers.character) &&
            combat.renderers.character.equals(character)) return true;

        restoreCharacterVisibility();
        combat.renderers.character = character;
        combat.renderers.entries = [];
        initializeFadeResources();

        return guarded('捕获人物 Renderer', function () {
            var array = character.add(OFF.Character_cvRenderers).readPointer();
            if (isNull(array) || !isReadable(array)) return false;
            var count = array.add(0x0C).readU32();
            if (count < 1 || count > 256) return false;

            for (var i = 0; i < count; i++) {
                var renderer = array.add(0x10 + i * PTR_SIZE).readPointer();
                if (isNull(renderer) || !isReadable(renderer)) continue;
                var entry = {
                    renderer:renderer,
                    originalEnabled:rendererGetEnabled(renderer, ptr(0)),
                    material:null,
                    colorId:0,
                    originalColor:null,
                    originalQueue:-1,
                    originalProps:{},
                    fadeCapable:false
                };

                if (combat.materialIds !== null) {
                    var material = rendererGetMaterial(renderer, ptr(0));
                    if (!isNull(material) && isReadable(material)) {
                        entry.material = material;
                        if (materialHasProperty(material, combat.materialIds.baseColor, ptr(0))) {
                            entry.colorId = combat.materialIds.baseColor;
                        } else if (materialHasProperty(material, combat.materialIds.color, ptr(0))) {
                            entry.colorId = combat.materialIds.color;
                        }
                        if (entry.colorId !== 0) {
                            entry.originalColor = getMaterialColor(material, entry.colorId);
                            entry.originalQueue = materialGetRenderQueue(material, ptr(0));
                            var keys = ['mode','surface','srcBlend','dstBlend','zWrite'];
                            for (var k = 0; k < keys.length; k++) {
                                var key = keys[k];
                                var id = combat.materialIds[key];
                                if (materialHasProperty(material, id, ptr(0))) {
                                    entry.originalProps[key] = materialGetFloat(material, id, ptr(0));
                                }
                            }
                            entry.fadeCapable = entry.originalColor.valid;
                        }
                    }
                }
                combat.renderers.entries.push(entry);
            }

            combat.renderers.captured = combat.renderers.entries.length > 0;
            sendLog('info', '[OcclusionFade] Renderer 捕获完成', {
                rendererCount: combat.renderers.entries.length,
                fadeCapableCount: combat.renderers.entries.filter(function (e) {
                    return e.fadeCapable;
                }).length
            });
            return combat.renderers.captured;
        }, false);
    }

    function configureFadeMaterial(entry) {
        if (!entry.fadeCapable || isNull(entry.material) || !isReadable(entry.material)) return false;
        return guarded('配置透明材质', function () {
            var m = entry.material;
            var ids = combat.materialIds;
            if (entry.originalProps.surface !== undefined) materialSetFloat(m, ids.surface, 1.0, ptr(0));
            if (entry.originalProps.mode !== undefined) materialSetFloat(m, ids.mode, 2.0, ptr(0));
            if (entry.originalProps.srcBlend !== undefined) materialSetFloat(m, ids.srcBlend, 5.0, ptr(0));
            if (entry.originalProps.dstBlend !== undefined) materialSetFloat(m, ids.dstBlend, 10.0, ptr(0));
            if (entry.originalProps.zWrite !== undefined) materialSetFloat(m, ids.zWrite, 0.0, ptr(0));
            materialDisableKeyword(m, combat.keywordStrings.alphaTest, ptr(0));
            materialEnableKeyword(m, combat.keywordStrings.alphaBlend, ptr(0));
            materialDisableKeyword(m, combat.keywordStrings.alphaPremul, ptr(0));
            materialSetRenderQueue(m, 3000, ptr(0));
            return true;
        }, false);
    }

    function applyCharacterFade(alpha) {
        if (!combat.renderers.captured) return false;
        alpha = Math.max(config.occlusionMinAlpha, Math.min(1.0, alpha));
        stats.currentFadeAlpha = alpha;
        var materialCount = 0;

        for (var i = 0; i < combat.renderers.entries.length; i++) {
            var entry = combat.renderers.entries[i];
            if (isNull(entry.renderer) || !isReadable(entry.renderer)) continue;
            var materialConfigured = false;
            if (entry.fadeCapable) {
                materialConfigured = configureFadeMaterial(entry);
                if (!materialConfigured) {
                    entry.fadeCapable = false;
                }
            }
            if (entry.fadeCapable && materialConfigured) {
                setMaterialColor(entry.material, entry.colorId, {
                    r:entry.originalColor.r, g:entry.originalColor.g,
                    b:entry.originalColor.b, a:entry.originalColor.a * alpha
                });
                rendererSetEnabled(entry.renderer, true, ptr(0));
                materialCount++;
                stats.fadeMaterialSuccess++;
            } else {
                var show = alpha > 0.28;
                rendererSetEnabled(entry.renderer, show, ptr(0));
                if (!show) stats.fadeFallbackHides++;
            }
        }

        combat.renderers.usingMaterialFade = materialCount > 0;
        combat.renderers.hiddenFallback = materialCount === 0 && alpha <= 0.28;
        stats.fadeUpdates++;
        return true;
    }

    function restoreCharacterVisibility() {
        if (!combat.renderers.captured) {
            combat.renderers.entries = [];
            combat.renderers.character = null;
            return;
        }

        for (var i = 0; i < combat.renderers.entries.length; i++) {
            var entry = combat.renderers.entries[i];
            if (isNull(entry.renderer) || !isReadable(entry.renderer)) continue;
            guarded('恢复人物 Renderer', function () {
                rendererSetEnabled(entry.renderer, entry.originalEnabled, ptr(0));
                if (entry.fadeCapable && !isNull(entry.material) && isReadable(entry.material)) {
                    setMaterialColor(entry.material, entry.colorId, entry.originalColor);
                    var keys = Object.keys(entry.originalProps);
                    for (var k = 0; k < keys.length; k++) {
                        var key = keys[k];
                        materialSetFloat(entry.material, combat.materialIds[key], entry.originalProps[key], ptr(0));
                    }
                    if (entry.originalQueue >= 0) {
                        materialSetRenderQueue(entry.material, entry.originalQueue, ptr(0));
                    }

                    // 按原始 Standard/URP 模式恢复常见透明关键字。
                    var originalMode = entry.originalProps.mode;
                    var originalSurface = entry.originalProps.surface;
                    if (originalMode === 1.0) {
                        materialEnableKeyword(
                            entry.material,
                            combat.keywordStrings.alphaTest,
                            ptr(0)
                        );
                    } else {
                        materialDisableKeyword(
                            entry.material,
                            combat.keywordStrings.alphaTest,
                            ptr(0)
                        );
                    }

                    if (originalMode === 3.0) {
                        materialEnableKeyword(
                            entry.material,
                            combat.keywordStrings.alphaPremul,
                            ptr(0)
                        );
                        materialDisableKeyword(
                            entry.material,
                            combat.keywordStrings.alphaBlend,
                            ptr(0)
                        );
                    } else if (originalMode === 2.0 ||
                               originalSurface === 1.0) {
                        materialEnableKeyword(
                            entry.material,
                            combat.keywordStrings.alphaBlend,
                            ptr(0)
                        );
                        materialDisableKeyword(
                            entry.material,
                            combat.keywordStrings.alphaPremul,
                            ptr(0)
                        );
                    } else {
                        materialDisableKeyword(
                            entry.material,
                            combat.keywordStrings.alphaBlend,
                            ptr(0)
                        );
                        materialDisableKeyword(
                            entry.material,
                            combat.keywordStrings.alphaPremul,
                            ptr(0)
                        );
                    }
                }
            }, null);
        }

        combat.renderers.character = null;
        combat.renderers.entries = [];
        combat.renderers.captured = false;
        combat.renderers.usingMaterialFade = false;
        combat.renderers.hiddenFallback = false;
        stats.currentFadeAlpha = 1.0;
    }

    function updateOcclusionFadeOnMainThread() {
        if (!enabled || combat.adsActive || combat.playerDead ||
            !config.occlusionFade || !combat.finalCamera.valid) return;

        var player = resolveLocalPlayer();
        if (isNull(player)) return;
        var character = player.add(OFF.Player_currentCharacter).readPointer();
        var container = player.add(OFF.Player_characterContainer).readPointer();
        if (isNull(character) || isNull(container) ||
            !isReadable(character) || !isReadable(container)) return;
        if (!captureCharacterRenderers(character)) return;

        var target = safeTransformPosition(container);
        if (!target.valid) return;
        var distance = v3Distance(combat.finalCamera.position, target);
        var alpha = 1.0;
        if (distance <= config.occlusionFadeEnd) {
            alpha = config.occlusionMinAlpha;
        } else if (distance < config.occlusionFadeStart) {
            var t = (distance - config.occlusionFadeEnd) /
                (config.occlusionFadeStart - config.occlusionFadeEnd);
            alpha = config.occlusionMinAlpha + (1.0 - config.occlusionMinAlpha) * t;
        }
        applyCharacterFade(alpha);

        var now = Date.now();
        if (alpha < 0.99 && now - combat.lastFadeLog >= 1000) {
            combat.lastFadeLog = now;
            sendLog('info', '[OcclusionFade]', {
                distance:distance,
                alpha:alpha,
                materialFade:combat.renderers.usingMaterialFade,
                hiddenFallback:combat.renderers.hiddenFallback
            });
        }
    }

    function applyColliderSettings(collider) {
        if (!config.collisionEnhance || isNull(collider)) return;

        var newCollider =
            isNull(combat.collider.pointer) ||
            !combat.collider.pointer.equals(collider);

        if (newCollider) {
            if (!isReadable(collider)) return;

            combat.collider.pointer = collider;
            combat.collider.appliedRevision = -1;
            combat.collider.original = {
                minimumDistance:collider.add(
                    OFF.Collider_MinimumDistanceFromTarget
                ).readFloat(),
                avoidObstacles:collider.add(
                    OFF.Collider_AvoidObstacles
                ).readU8() !== 0,
                cameraRadius:collider.add(
                    OFF.Collider_CameraRadius
                ).readFloat(),
                damping:collider.add(
                    OFF.Collider_Damping
                ).readFloat(),
                dampingOccluded:collider.add(
                    OFF.Collider_DampingWhenOccluded
                ).readFloat()
            };
            sendLog('info', '[Collider] 原始配置已保存',
                combat.collider.original
            );
        }

        if (combat.collider.appliedRevision === configRevision) return;

        collider.add(OFF.Collider_AvoidObstacles).writeU8(1);
        collider.add(OFF.Collider_CameraRadius).writeFloat(
            config.collisionRadius
        );
        collider.add(OFF.Collider_Damping).writeFloat(
            config.collisionDamping
        );
        collider.add(
            OFF.Collider_DampingWhenOccluded
        ).writeFloat(config.collisionOccludedDamping);

        combat.collider.appliedRevision = configRevision;
    }

    function restoreColliderSettings() {
        var collider = combat.collider.pointer;
        var original = combat.collider.original;
        if (isNull(collider) || !isReadable(collider) || original === null) {
            combat.collider.pointer = null;
            combat.collider.original = null;
            return;
        }
        guarded('恢复 Collider 配置', function () {
            collider.add(OFF.Collider_MinimumDistanceFromTarget).writeFloat(original.minimumDistance);
            collider.add(OFF.Collider_AvoidObstacles).writeU8(original.avoidObstacles ? 1 : 0);
            collider.add(OFF.Collider_CameraRadius).writeFloat(original.cameraRadius);
            collider.add(OFF.Collider_Damping).writeFloat(original.damping);
            collider.add(OFF.Collider_DampingWhenOccluded).writeFloat(original.dampingOccluded);
        }, null);
        combat.collider.pointer = null;
        combat.collider.original = null;
        combat.collider.displaced = false;
        combat.collider.distance = 0;
    }

    function updateCombatRuntimeOnMainThread() {
        if (!enabled) return;

        var now = Date.now();
        if (now - combat.timing.lastRuntime <
            PERF.runtimeIntervalMs) {
            stats.runtimeTicksSkipped++;
            return;
        }
        combat.timing.lastRuntime = now;
        stats.runtimeTicks++;

        if (!config.aimIK && combat.aimIK.found) {
            restoreAimIK(true);
            sendLog('info', '[AimIK] 已按配置关闭并恢复权重');
        }
        if (!config.occlusionFade && combat.renderers.captured) {
            restoreCharacterVisibility();
            sendLog('info',
                '[OcclusionFade] 已按配置关闭并恢复人物材质'
            );
        }
        if (!config.collisionEnhance &&
            !isNull(combat.collider.pointer)) {
            restoreColliderSettings();
            sendLog('info', '[Collider] 已按配置关闭并恢复原参数');
        }
        if (!config.upperBodyAim &&
            saved.upperBodyTargetOriginal !== null &&
            !isNull(saved.character)) {
            guarded('运行时恢复上半身瞄准角', function () {
                saved.character.add(
                    OFF.Character_targetLowerAngle
                ).writeFloat(saved.upperBodyTargetOriginal);
            }, null);
            saved.upperBodyTargetOriginal = null;
        }

        updateInputFeaturesOnMainThread();
        if (combat.adsActive || combat.playerDead) return;

        updateAimTargetOnMainThread(false);
        updateMuzzleOnMainThread(false);
        updateShootSolutionOnMainThread(false);

        if (config.occlusionFade &&
            now - combat.timing.lastFade >= PERF.fadeIntervalMs) {
            combat.timing.lastFade = now;
            updateOcclusionFadeOnMainThread();
        }

        if (combat.pendingLifecycleRefresh) {
            combat.pendingLifecycleRefresh = false;
            var player = resolveLocalPlayer();
            if (!isNull(player)) {
                applyModelMode(player);
                applyCameraConfiguration();
                updateAimTargetOnMainThread(true);
                updateMuzzleOnMainThread(true);
                updateShootSolutionOnMainThread(true);
                stats.lifecycleReapplyCount++;
                sendLog('info',
                    '[WeaponLifecycle] 生命周期重新绑定完成',
                    { count:stats.lifecycleReapplyCount }
                );
            }
        }

        if (now - combat.lastCombatLog >= PERF.combatLogIntervalMs) {
            combat.lastCombatLog = now;
            sendLog('info', '[CombatTelemetry]', {
                finalCameraValid:combat.finalCamera.valid,
                finalCameraPitchDeg:stats.lastFinalCameraPitch,
                aimTargetValid:combat.aimTarget.valid,
                targetMode:combat.aimTarget.reason,
                aimTargetHit:combat.aimTarget.hit,
                aimColliderId:combat.aimTarget.colliderId,
                aimDistance:combat.aimTarget.distance,
                muzzleValid:combat.muzzle.valid,
                muzzleSource:combat.muzzle.source,
                adsActive:combat.adsActive,
                shoulder:config.shoulder,
                shootRayModified:stats.shootRayModified,
                damageRayMatches:stats.damageRayMatches,
                damageRayChecks:stats.damageRayChecks,
                aimIKFound:combat.aimIK.found,
                aimIKWrites:stats.aimIKWrites,
                colliderDisplaced:combat.collider.displaced,
                colliderDistance:combat.collider.distance,
                fadeAlpha:stats.currentFadeAlpha,
                performance:{
                    runtimeTicks:stats.runtimeTicks,
                    physicsCalls:stats.physicsRaycastCalls,
                    physicsFailures:stats.aimRaycastFailures,
                    physicsDisabled:combat.physics.disabledByError,
                    colliderQueries:stats.colliderQueries,
                    suppressedLogs:stats.logMessagesSuppressed
                }
            });
        }
    }

    function clearCombatCachesWithoutUnity(reason) {
        combat.adsActive = false;
        combat.playerDead = false;
        combat.pendingLifecycleRefresh = false;
        combat.finalCamera.valid = false;
        combat.finalCamera.camera = null;
        combat.finalCamera.transform = null;
        combat.finalCamera.position = null;
        combat.finalCamera.forward = null;
        combat.aimTarget.valid = false;
        combat.aimTarget.point = null;
        combat.aimTarget.hit = false;
        combat.aimTarget.colliderId = 0;
        combat.aimTarget.reason = 'cleared';
        combat.lastModifiedRay = null;
        combat.shootSolution.valid = false;
        combat.shootSolution.origin = null;
        combat.shootSolution.direction = null;
        combat.shootSolution.targetPoint = null;
        combat.shootSolution.reason = 'cleared';
        combat.muzzle.valid = false;
        combat.muzzle.weapon = null;
        combat.muzzle.transform = null;
        combat.muzzle.position = null;
        combat.muzzle.source = 'none';
        combat.aimIK.character = null;
        combat.aimIK.component = null;
        combat.aimIK.solver = null;
        combat.aimIK.found = false;
        combat.aimIK.reason = 'cleared_without_unity';
        combat.renderers.character = null;
        combat.renderers.entries = [];
        combat.renderers.captured = false;
        combat.renderers.usingMaterialFade = false;
        combat.renderers.hiddenFallback = false;
        combat.collider.pointer = null;
        combat.collider.vcam = null;
        combat.collider.original = null;
        combat.collider.displaced = false;
        combat.collider.distance = 0.0;
        stats.currentFadeAlpha = 1.0;

        if (reason) {
            sendLog('info', '[CombatLifecycle] 已清空纯 JS 缓存', {
                reason: reason
            });
        }
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
        telemetry.previousLoggedPlayerPitch = null;
        telemetry.previousLoggedYAxis = null;
        telemetry.lastInputActivityTime = Date.now();

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

        var loggedPlayerDelta =
            telemetry.previousLoggedPlayerPitch === null
                ? 0.0
                : stats.lastPlayerPitch -
                  telemetry.previousLoggedPlayerPitch;

        var loggedYAxisDelta =
            telemetry.previousLoggedYAxis === null
                ? 0.0
                : stats.lastYAxisWritten -
                  telemetry.previousLoggedYAxis;

        var playerPitchActive = Math.abs(loggedPlayerDelta) >= 0.05;
        var yAxisActive = Math.abs(loggedYAxisDelta) >= 0.0005;

        if (playerPitchActive || yAxisActive) {
            telemetry.lastInputActivityTime = now;
        }

        var recentlyActive =
            now - telemetry.lastInputActivityTime <= 2000;
        var targetInterval = recentlyActive
            ? telemetry.activeIntervalMs
            : telemetry.idleIntervalMs;

        if (!forceReason && now - telemetry.lastLogTime < targetInterval) {
            stats.telemetrySuppressed++;
            return;
        }

        var writesDelta = stats.pitchWrites - telemetry.lastPitchWrites;
        var elapsedSeconds = telemetry.enabledAt > 0
            ? (now - telemetry.enabledAt) / 1000.0
            : 0.0;

        var cameraPitchActive = false;

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
            playerPitchFrameDeltaDeg: Number(
                stats.lastPlayerPitchDelta.toFixed(4)
            ),
            playerPitchLogIntervalDeltaDeg: Number(
                loggedPlayerDelta.toFixed(4)
            ),
            playerPitchChangedDuringInterval: playerPitchActive,
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
            yAxisLogIntervalDelta: Number(
                loggedYAxisDelta.toFixed(6)
            ),
            yAxisChangedDuringInterval: yAxisActive,
            yAxisMin: telemetry.yAxisMin,
            yAxisMax: telemetry.yAxisMax,

            actualCameraPitchSampling: 'output_camera_transform_main_thread',
            cameraForwardY: combat.finalCamera.valid
                ? combat.finalCamera.forward.y : null,
            actualCameraPitchDeg: combat.finalCamera.valid
                ? combat.finalCamera.pitchDeg : null,
            actualCameraPitchDeltaDeg: null,
            actualCameraPitchChanged: combat.finalCamera.valid,
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
                inputChangedDuringInterval: playerPitchActive,
                yAxisChangedDuringInterval: yAxisActive,
                cameraChanging: combat.finalCamera.valid,
                cameraSamplingDisabled: false,
                yAxisWasOverwritten:
                    Math.abs(stats.lastYAxisOverwriteDelta) >= 0.0005
            }
        });

        stats.telemetryLines++;
        telemetry.lastLogTime = now;
        telemetry.lastPitchWrites = stats.pitchWrites;
        telemetry.previousYAxisWritten = stats.lastYAxisWritten;
        telemetry.previousLoggedPlayerPitch = stats.lastPlayerPitch;
        telemetry.previousLoggedYAxis = stats.lastYAxisWritten;
    }

    function emitFeatureAssessment(reason) {
        var pitchPipelineHealthy =
            stats.pitchWrites > 0 &&
            stats.pitchWriteFailures === 0 &&
            stats.invalidPitchSamples === 0 &&
            Math.abs(stats.lastYAxisOverwriteDelta) < 0.0005;

        var cameraFoundationHealthy =
            enabled &&
            !isNull(cameraManager) &&
            isReadable(cameraManager) &&
            !isNull(saved.freeLook) &&
            isReadable(saved.freeLook) &&
            stats.freeLookUpdateCalls > 0 &&
            stats.finalCameraWrites > 0;

        var assessment = {
            reason: reason || 'periodic',
            version: '3.0',
            state: state,
            enabled: enabled,

            completed: {
                mainThreadCommandQueue:
                    stats.enableMainThreadRuns > 0,
                cameraManagerLifecycle:
                    stats.cameraManagerCaptures > 0,
                localPlayerLifecycle:
                    stats.localPlayerCaptures > 0,
                thirdPersonModelSwitch:
                    saved.player !== null,
                freeLookConfigured:
                    saved.valid &&
                    !isNull(saved.freeLook),
                verticalPitchDataPipeline:
                    pitchPipelineHealthy,
                fovPipeline:
                    stats.finalCameraWrites > 0,
                wasdPreserved:
                    true
            },

            verifiedByLog: {
                pitchWrites: stats.pitchWrites,
                pitchWriteFailures: stats.pitchWriteFailures,
                invalidPitchSamples: stats.invalidPitchSamples,
                yAxisRange: [
                    telemetry.yAxisMin,
                    telemetry.yAxisMax
                ],
                playerPitchRange: [
                    telemetry.playerPitchMin,
                    telemetry.playerPitchMax
                ],
                yAxisOverwriteDelta:
                    stats.lastYAxisOverwriteDelta,
                freeLookUpdateCalls:
                    stats.freeLookUpdateCalls,
                finalCameraWrites:
                    stats.finalCameraWrites
            },

            combatModules: {
                actualRenderedCameraPitchVerification: stats.finalCameraSamples > 0,
                cameraCollisionRuntimeVerification: stats.colliderCallbacks > 0,
                thirdPersonShootingRay: stats.shootRayModified > 0,
                crosshairTargetPoint: stats.aimTargetUpdates > 0,
                muzzleConvergence: stats.muzzleResolves > 0 && stats.shootRayModified > 0,
                adsTransition: stats.adsEnterCount > 0 || stats.adsExitCount > 0,
                aimIK: stats.aimIKFound > 0 && stats.aimIKWrites > 0,
                upperBodyAimPose: stats.upperBodyWrites > 0,
                weaponLifecycle: stats.weaponChangeEvents > 0 || stats.muzzleResolves > 0,
                deathRespawnLifecycle: stats.deathEvents > 0 || stats.respawnEvents > 0 || stats.spawnEvents > 0,
                dynamicShoulderSwap: stats.shoulderSwapCount > 0,
                occlusionFade: stats.fadeUpdates > 0
            },

            combatData: {
                finalCameraSamples: stats.finalCameraSamples,
                finalCameraSampleFailures: stats.finalCameraSampleFailures,
                colliderCallbacks: stats.colliderCallbacks,
                colliderDisplacedFrames: stats.colliderDisplacedFrames,
                shootRayModified: stats.shootRayModified,
                shootRayFailures: stats.shootRayFailures,
                damageRayChecks: stats.damageRayChecks,
                damageRayMatches: stats.damageRayMatches,
                aimTargetUpdates: stats.aimTargetUpdates,
                aimRaycastHits: stats.aimRaycastHits,
                aimRaycastMisses: stats.aimRaycastMisses,
                aimRaycastFailures: stats.aimRaycastFailures,
                muzzleObstructionHits: stats.muzzleObstructionHits,
                aimIKWrites: stats.aimIKWrites,
                upperBodyWrites: stats.upperBodyWrites,
                fadeUpdates: stats.fadeUpdates
            },

            classification: cameraFoundationHealthy && pitchPipelineHealthy &&
                stats.finalCameraSamples > 0
                ? 'third_person_combat_integration'
                : 'partial_camera_demo',

            matureThirdPersonShooterReady:
                stats.finalCameraSamples > 0 &&
                stats.shootRayModified > 0 &&
                stats.damageRayMatches > 0 &&
                stats.colliderCallbacks > 0
        };

        sendLog('info', '[FeatureAssessment]', assessment);
        stats.featureAssessmentLines++;
        return assessment;
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
        if (!enabled && !enableInProgress) return false;
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
        if (!enabled || combat.adsActive) return false;
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

            captureCharacterRenderers(character);

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
        if (!enabled || combat.adsActive) return;

        var now = Date.now();
        if (now - combat.timing.lastFovCheck <
            PERF.fovCheckIntervalMs) {
            return;
        }
        combat.timing.lastFovCheck = now;

        guarded('应用 FOV', function () {
            var camera = brainGetOutputCamera(brain, ptr(0));
            if (isNull(camera) || !isReadable(camera)) return;

            saveOriginalFov(brain);
            var current = cameraGetFieldOfView(camera, ptr(0));
            if (!isFinite(current)) return;

            if (Math.abs(current - config.fieldOfView) > 0.05) {
                cameraSetFieldOfView(
                    camera,
                    config.fieldOfView,
                    ptr(0)
                );
                stats.finalCameraWrites++;
            }
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
        restoreAimIK(false);
        restoreCharacterVisibility();

        if (saved.upperBodyTargetOriginal !== null &&
            !isNull(saved.character) &&
            isReadable(saved.character)) {
            guarded('恢复上半身瞄准角', function () {
                saved.character.add(
                    OFF.Character_targetLowerAngle
                ).writeFloat(saved.upperBodyTargetOriginal);
            }, null);
        }

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
            originalFov: -1.0,
            upperBodyTargetOriginal: null
        };
    }

    function resetCombatRunState() {
        var fields = [
            'finalCameraSamples',
            'finalCameraSampleFailures',
            'aimTargetUpdates',
            'aimRaycastHits',
            'aimRaycastMisses',
            'aimRaycastFailures',
            'muzzleObstructionHits',
            'muzzleResolves',
            'muzzleFailures',
            'shootRayCalls',
            'shootRayModified',
            'shootRaySkipped',
            'shootRayFailures',
            'damageRayChecks',
            'damageRayMatches',
            'adsEnterCount',
            'adsExitCount',
            'shoulderSwapCount',
            'colliderCallbacks',
            'colliderDisplacedFrames',
            'weaponChangeEvents',
            'deathEvents',
            'respawnEvents',
            'spawnEvents',
            'lifecycleReapplyCount',
            'upperBodyWrites',
            'aimIKSearches',
            'aimIKFound',
            'aimIKWrites',
            'aimIKFailures',
            'fadeUpdates',
            'fadeMaterialSuccess',
            'fadeFallbackHides'
        ];
        for (var index = 0; index < fields.length; index++) {
            stats[fields[index]] = 0;
        }
        stats.colliderMaxDisplacement = 0.0;
        stats.lastAimDistance = 0.0;
        stats.lastFinalCameraPitch = 0.0;
        stats.currentFadeAlpha = 1.0;

        combat.finalCamera.valid = false;
        combat.finalCamera.disabledByError = false;
        combat.finalCamera.consecutiveFailures = 0;
        combat.physics.disabledByError = false;
        combat.physics.consecutiveFailures = 0;
        combat.physics.totalFailures = 0;

        combat.timing.lastRuntime = 0;
        combat.timing.lastFinalCamera = 0;
        combat.timing.lastAimRaycast = 0;
        combat.timing.lastMuzzle = 0;
        combat.timing.lastShootSolution = 0;
        combat.timing.lastInput = 0;
        combat.timing.lastFade = 0;
        combat.timing.lastFovCheck = 0;

        combat.collider.queryFailures = 0;
        combat.collider.lastQueryTime = 0;
        combat.collider.appliedRevision = -1;
        combat.collider.telemetryDisabled = false;
        combat.lastModifiedRay = null;
        combat.shootSolution.valid = false;
        combat.aimTarget.valid = false;
        combat.aimTarget.reason = 'new_run';
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
        resetCombatRunState();

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
        sendLog('info', '第三人称战斗集成版已启用', {
            modelSwitched: modelOk,
            movementModified: false,
            shootingModified: config.shootingRay,
            characterYawModified: false
        });
        emitPitchTelemetry('enabled');
        emitFeatureAssessment('enabled');

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
        emitFeatureAssessment('before_disable');
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
        restoreColliderSettings();
        clearMuzzleCache('disable');
        combat.adsActive = false;
        combat.playerDead = false;
        combat.aimTarget.valid = false;
        combat.finalCamera.valid = false;
        restoreAimIK(true);
        resetSavedState();

        setState(
            !isNull(gameManager) && isReadable(gameManager)
                ? STATE.READY
                : STATE.NO_GAME
        );

        disableInProgress = false;
        sendLog('info', '第三人称战斗集成版已关闭');
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

        if (
            sessionDestroyed ||
            isNull(cameraManager) ||
            !isReadable(cameraManager) ||
            state === STATE.NO_GAME
        ) {
            pendingDisable = false;
            enabled = false;
            sendLog(
                'info',
                '[CommandQueue] 当前场景已销毁，无需排队关闭'
            );
            return {
                ok: true,
                enabled: false,
                queued: false,
                noLiveSession: true,
                message: '游戏场景已销毁，无需恢复'
            };
        }

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
            invertY: config.invertY,
            dynamicShoulder: config.dynamicShoulder,
            shootingRay: config.shootingRay,
            physicsAimRaycast: config.physicsAimRaycast,
            maxAimDistance: config.maxAimDistance,
            adsFirstPerson: config.adsFirstPerson,
            upperBodyAim: config.upperBodyAim,
            upperBodyPitchScale: config.upperBodyPitchScale,
            aimIK: config.aimIK,
            aimIKWeight: config.aimIKWeight,
            collisionEnhance: config.collisionEnhance,
            collisionRadius: config.collisionRadius,
            collisionDamping: config.collisionDamping,
            collisionOccludedDamping: config.collisionOccludedDamping,
            occlusionFade: config.occlusionFade,
            occlusionFadeStart: config.occlusionFadeStart,
            occlusionFadeEnd: config.occlusionFadeEnd,
            occlusionMinAlpha: config.occlusionMinAlpha
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

        var booleanFields = [
            'dynamicShoulder', 'shootingRay', 'physicsAimRaycast', 'adsFirstPerson',
            'upperBodyAim', 'aimIK', 'collisionEnhance', 'occlusionFade'
        ];
        for (var bi = 0; bi < booleanFields.length; bi++) {
            var booleanName = booleanFields[bi];
            if (input[booleanName] !== undefined) {
                next[booleanName] = !!input[booleanName];
            }
        }

        error = numberField('maxAimDistance', 50.0, 3000.0);
        if (error) return { ok:false, error:error };
        error = numberField('upperBodyPitchScale', 0.2, 2.0);
        if (error) return { ok:false, error:error };
        error = numberField('aimIKWeight', 0.0, 1.0);
        if (error) return { ok:false, error:error };
        error = numberField('collisionRadius', 0.05, 1.0);
        if (error) return { ok:false, error:error };
        error = numberField('collisionDamping', 0.0, 2.0);
        if (error) return { ok:false, error:error };
        error = numberField('collisionOccludedDamping', 0.0, 2.0);
        if (error) return { ok:false, error:error };
        error = numberField('occlusionFadeStart', 0.6, 3.0);
        if (error) return { ok:false, error:error };
        error = numberField('occlusionFadeEnd', 0.2, 2.0);
        if (error) return { ok:false, error:error };
        error = numberField('occlusionMinAlpha', 0.0, 0.8);
        if (error) return { ok:false, error:error };
        if (next.occlusionFadeEnd >= next.occlusionFadeStart) {
            return { ok:false, error:'occlusionFadeEnd 必须小于 occlusionFadeStart' };
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
                        updateCombatRuntimeOnMainThread();
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
                                emitFeatureAssessment(
                                    'camera_manager_destroy'
                                );
                            }

                            stats.lifecycleDestroyCount++;
                            sessionDestroyed = true;
                            enabled = false;
                            pendingEnable = false;
                            pendingDisable = false;
                            pendingReapply = false;
                            enableInProgress = false;
                            disableInProgress = false;
                            cameraManager = null;
                            localPlayer = null;
                            clearCombatCachesWithoutUnity(
                                'CameraManager.OnDestroy'
                            );
                            resetSavedState();
                            setState(STATE.NO_GAME);
                            send({
                                type: 'session_destroyed',
                                reason: 'CameraManager.OnDestroy'
                            });
                            sendLog(
                                'info',
                                'CameraManager 正在销毁，已清空 Demo 状态'
                            );
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
                            clearCombatCachesWithoutUnity(
                                'GameManager.OnDestroy'
                            );
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
                        sampleFinalCameraOnMainThread(
                            this.brain,
                            false
                        );
                        emitPitchTelemetry(null);
                    }
                }
            );

            attach(
                'CinemachineCollider.PostPipelineStageCallback',
                RVA.CinemachineCollider_PostPipelineStageCallback,
                {
                    onEnter: function (args) {
                        this.collider = args[0];
                        this.vcam = args[1];
                        this.active = false;

                        if (!enabled || combat.adsActive ||
                            !config.collisionEnhance ||
                            isNull(this.collider) ||
                            isNull(this.vcam)) {
                            return;
                        }

                        this.active = true;
                        stats.colliderCallbacks++;
                        combat.collider.vcam = this.vcam;
                        applyColliderSettings(this.collider);
                    },
                    onLeave: function () {
                        if (!this.active ||
                            combat.collider.telemetryDisabled) {
                            return;
                        }

                        var now = Date.now();
                        if (now - combat.collider.lastQueryTime <
                            PERF.colliderQueryIntervalMs) {
                            stats.colliderQueriesSkipped++;
                            return;
                        }
                        combat.collider.lastQueryTime = now;
                        stats.colliderQueries++;

                        var ok = guarded(
                            '读取 CinemachineCollider 位移',
                            function () {
                                var displaced =
                                    colliderCameraWasDisplaced(
                                        this.collider,
                                        this.vcam,
                                        ptr(0)
                                    );
                                var distance =
                                    colliderGetDisplacementDistance(
                                        this.collider,
                                        this.vcam,
                                        ptr(0)
                                    );

                                if (!isFinite(distance) ||
                                    distance < 0) {
                                    distance = 0.0;
                                }

                                combat.collider.displaced = displaced;
                                combat.collider.distance = distance;

                                if (displaced) {
                                    stats.colliderDisplacedFrames++;
                                    if (distance >
                                        stats.colliderMaxDisplacement) {
                                        stats.colliderMaxDisplacement =
                                            distance;
                                    }
                                }

                                if (displaced &&
                                    now - combat.lastCollisionLog >=
                                        PERF.colliderLogIntervalMs) {
                                    combat.lastCollisionLog = now;
                                    sendLog('info',
                                        '[ColliderTelemetry]',
                                        {
                                            displaced:displaced,
                                            displacementDistance:distance,
                                            maxDisplacement:
                                                stats.colliderMaxDisplacement,
                                            cameraRadius:
                                                config.collisionRadius,
                                            callbacks:
                                                stats.colliderCallbacks,
                                            queries:
                                                stats.colliderQueries
                                        }
                                    );
                                }

                                combat.collider.queryFailures = 0;
                                return true;
                            }.bind(this),
                            false
                        );

                        if (!ok) {
                            combat.collider.queryFailures++;
                            if (combat.collider.queryFailures >= 3) {
                                combat.collider.telemetryDisabled = true;
                                sendLog('warning',
                                    '[Collider] 位移查询已自动禁用',
                                    {
                                        reason:
                                            'three_consecutive_failures'
                                    }
                                );
                            }
                        }
                    }
                }
            );

            attach(
                'Recoil.GetShootRay',
                RVA.Recoil_GetShootRay,
                {
                    onEnter: function (args) {
                        this.retBuffer = args[0];
                        this.recoil = args[1];
                        this.shouldModify = false;

                        if (!enabled || combat.adsActive ||
                            combat.playerDead ||
                            !config.shootingRay) {
                            return;
                        }

                        var player = resolveLocalPlayer();
                        if (isNull(player) || !isReadable(player)) {
                            return;
                        }

                        guarded('校验本地 Recoil', function () {
                            var localRecoil = player.add(
                                OFF.Player_recoil
                            ).readPointer();
                            this.shouldModify =
                                !isNull(localRecoil) &&
                                localRecoil.equals(this.recoil);
                        }.bind(this), null);
                    },
                    onLeave: function () {
                        if (!enabled) return;
                        stats.shootRayCalls++;

                        if (!this.shouldModify ||
                            isNull(this.retBuffer)) {
                            stats.shootRaySkipped++;
                            return;
                        }

                        var original = readRayAt(this.retBuffer);
                        var ray = buildCombatShootRay();

                        if (!ray.valid ||
                            !writeRayAt(
                                this.retBuffer,
                                ray.origin,
                                ray.direction
                            )) {
                            stats.shootRayFailures++;
                            sendLog('warning', '[ShootRay] 保留原始射线', {
                                reason: ray.reason,
                                originalValid: original.valid,
                                failures: stats.shootRayFailures
                            });
                            return;
                        }

                        stats.shootRayModified++;
                        combat.lastModifiedRay = {
                            origin: ray.origin,
                            direction: ray.direction,
                            targetPoint: ray.targetPoint,
                            timestamp: Date.now()
                        };

                        if (stats.shootRayModified <= 5 ||
                            stats.shootRayModified % 10 === 0) {
                            sendLog('info', '[ShootRayTelemetry]', {
                                shot: stats.shootRayModified,
                                origin: ray.origin,
                                direction: ray.direction,
                                targetPoint: ray.targetPoint,
                                targetDistance: ray.distance,
                                targetMode: ray.reason,
                                muzzleSource: combat.muzzle.source,
                                originalDirection:
                                    original.valid
                                        ? original.direction
                                        : null,
                                correctionAngleDeg:
                                    original.valid
                                        ? v3Angle(
                                            original.direction,
                                            ray.direction
                                        )
                                        : null
                            });
                        }
                    }
                }
            );

            attach(
                'WPN_Gun.Damage',
                RVA.WPN_Gun_Damage,
                {
                    onEnter: function (args) {
                        if (!enabled || combat.adsActive ||
                            !config.shootingRay ||
                            combat.lastModifiedRay === null ||
                            !combat.muzzle.valid ||
                            isNull(combat.muzzle.weapon) ||
                            isNull(args[0]) ||
                            !args[0].equals(combat.muzzle.weapon)) {
                            return;
                        }

                        try {
                            var rayAddress = this.context.esp.add(8);
                            var received = readRayAt(rayAddress);
                            if (!received.valid) return;

                            stats.damageRayChecks++;
                            var originDiff = v3Distance(
                                received.origin,
                                combat.lastModifiedRay.origin
                            );
                            var directionDiff = v3Angle(
                                received.direction,
                                combat.lastModifiedRay.direction
                            );
                            var match =
                                originDiff < 0.05 &&
                                directionDiff < 0.25;

                            if (match) {
                                stats.damageRayMatches++;
                            }

                            if (stats.damageRayChecks <= 5 ||
                                !match ||
                                stats.damageRayChecks % 10 === 0) {
                                sendLog(
                                    match ? 'info' : 'warning',
                                    '[DamageRayVerification]',
                                    {
                                        check: stats.damageRayChecks,
                                        match: match,
                                        originDiff: originDiff,
                                        directionDiffDeg: directionDiff,
                                        matchRate:
                                            stats.damageRayChecks > 0
                                                ? stats.damageRayMatches /
                                                  stats.damageRayChecks
                                                : 0
                                    }
                                );
                            }
                        } catch (_) {
                        }
                    }
                }
            );

            attach(
                'Player.OnEntityDeath',
                RVA.Player_OnEntityDeath,
                {
                    onEnter: function (args) {
                        this.player = args[0];
                    },
                    onLeave: function () {
                        if (!isLocalPlayerObject(this.player)) return;

                        combat.playerDead = true;
                        combat.adsActive = false;
                        stats.deathEvents++;
                        clearMuzzleCache('death');
                        restoreAimIK(true);
                        restoreCharacterVisibility();

                        sendLog('info', '[PlayerLifecycle] 本地玩家死亡', {
                            count: stats.deathEvents
                        });
                    }
                }
            );

            attach(
                'Player.SetWeapon',
                RVA.Player_SetWeapon,
                {
                    onEnter: function (args) {
                        this.player = args[0];
                    },
                    onLeave: function () {
                        if (!isLocalPlayerObject(this.player)) return;

                        stats.weaponChangeEvents++;
                        clearMuzzleCache('set_weapon');
                        restoreAimIK(true);
                        combat.pendingLifecycleRefresh = true;

                        sendLog('info', '[PlayerLifecycle] 本地玩家切枪', {
                            count: stats.weaponChangeEvents
                        });
                    }
                }
            );

            attach(
                'Player.Respawn',
                RVA.Player_Respawn,
                {
                    onEnter: function (args) {
                        this.player = args[0];
                    },
                    onLeave: function () {
                        if (!isLocalPlayerObject(this.player)) return;

                        combat.playerDead = false;
                        stats.respawnEvents++;
                        clearMuzzleCache('respawn');
                        restoreAimIK(true);
                        combat.pendingLifecycleRefresh = true;

                        sendLog('info', '[PlayerLifecycle] 本地玩家复活', {
                            count: stats.respawnEvents
                        });
                    }
                }
            );

            attach(
                'Player.Spawn',
                RVA.Player_Spawn,
                {
                    onEnter: function (args) {
                        this.player = args[0];
                    },
                    onLeave: function () {
                        if (!isLocalPlayerObject(this.player)) return;

                        combat.playerDead = false;
                        stats.spawnEvents++;
                        clearMuzzleCache('spawn');
                        restoreAimIK(true);
                        combat.pendingLifecycleRefresh = true;

                        sendLog('info', '[PlayerLifecycle] 本地玩家出生', {
                            count: stats.spawnEvents
                        });
                    }
                }
            );

            attach(
                'CharacterModel.LateUpdate',
                RVA.CharacterModel_LateUpdate,
                {
                    onEnter: function (args) {
                        this.character = args[0];
                        this.local =
                            enabled &&
                            !combat.adsActive &&
                            !combat.playerDead &&
                            isLocalCharacter(this.character);

                        if (!this.local) return;

                        if (config.upperBodyAim &&
                            combat.finalCamera.valid) {
                            var targetPitch =
                                combat.finalCamera.pitchDeg *
                                config.upperBodyPitchScale;
                            targetPitch = Math.max(
                                -70.0,
                                Math.min(70.0, targetPitch)
                            );

                            if (saved.upperBodyTargetOriginal === null) {
                                saved.upperBodyTargetOriginal =
                                    this.character.add(
                                        OFF.Character_targetLowerAngle
                                    ).readFloat();
                            }

                            this.character.add(
                                OFF.Character_targetLowerAngle
                            ).writeFloat(targetPitch);
                            stats.upperBodyWrites++;
                        }

                        if (config.aimIK &&
                            combat.aimTarget.valid) {
                            var ikOk = writeAimIKOnMainThread(
                                this.character
                            );
                            if (!ikOk &&
                                combat.aimIK.reason !== 'not_found') {
                                stats.aimIKFailures++;
                            }
                        }
                    },
                    onLeave: function () {
                        if (!this.local ||
                            isNull(this.character) ||
                            !isReadable(this.character)) {
                            return;
                        }

                        var now = Date.now();
                        if (now - combat.lastIKLog < PERF.visualLogIntervalMs) return;
                        combat.lastIKLog = now;

                        guarded('读取视觉瞄准结果', function () {
                            sendLog('info', '[VisualAimTelemetry]', {
                                finalCameraPitch:
                                    combat.finalCamera.pitchDeg,
                                targetLowerAngle:
                                    this.character.add(
                                        OFF.Character_targetLowerAngle
                                    ).readFloat(),
                                lowerAngle:
                                    this.character.add(
                                        OFF.Character_lowerAngle
                                    ).readFloat(),
                                upperBodyWrites:
                                    stats.upperBodyWrites,
                                aimIKEnabled:
                                    config.aimIK,
                                aimIKFound:
                                    combat.aimIK.found,
                                aimIKWrites:
                                    stats.aimIKWrites,
                                aimIKReason:
                                    combat.aimIK.reason
                            });
                        }.bind(this), null);
                    }
                }
            );

            installed = true;
            sendLog('info', '第三人称战斗 Hook 安装完成');
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

        if (
            enabled &&
            !sessionDestroyed &&
            !isNull(cameraManager) &&
            isReadable(cameraManager)
        ) {
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

        // 场景已销毁或功能已经关闭：RPC 线程只清理纯 JS 缓存，
        // 不调用任何 Unity NativeFunction。
        enabled = false;
        pendingDisable = false;
        clearCombatCachesWithoutUnity('cleanup_rpc');

        for (var index = 0; index < listeners.length; index++) {
            try {
                listeners[index].detach();
            } catch (_) {
            }
        }
        listeners = [];
        installed = false;

        // GCHandle 随 Frida 脚本卸载回收；RPC 线程不调用 IL2CPP API。
        mouseYHandle = 0;
        mouseYString = null;
        sendLog('info', '第三人称战斗资源已清理');
        return { ok: true };
    }

    rpc.exports = {
        installhooks: installHooks,

        enable: requestEnable,

        disable: requestDisable,

        setconfig: function (input) {
            var validation = validateConfig(input);
            if (!validation.ok) return validation;

            var previous = config;
            var next = validation.config;

            var cameraChanged =
                previous.shoulder !== next.shoulder ||
                previous.distance !== next.distance ||
                previous.pivotHeight !== next.pivotHeight ||
                previous.screenY !== next.screenY ||
                previous.fieldOfView !== next.fieldOfView ||
                previous.pitchScale !== next.pitchScale ||
                previous.invertY !== next.invertY;

            var colliderChanged =
                previous.collisionEnhance !== next.collisionEnhance ||
                previous.collisionRadius !== next.collisionRadius ||
                previous.collisionDamping !== next.collisionDamping ||
                previous.collisionOccludedDamping !==
                    next.collisionOccludedDamping;

            var physicsWasEnabled = previous.physicsAimRaycast;
            var physicsWillEnable = next.physicsAimRaycast;

            config = next;
            configRevision++;

            if (!physicsWasEnabled &&
                physicsWillEnable &&
                combat.physics.disabledByError) {
                combat.physics.disabledByError = false;
                combat.physics.consecutiveFailures = 0;
                combat.physics.totalFailures = 0;
                sendLog('info',
                    '[PhysicsAim] 用户关闭后重新开启，熔断器已复位'
                );
            }

            if (colliderChanged) {
                combat.collider.appliedRevision = -1;
            }

            if (enabled && cameraChanged) {
                pendingReapply = true;
            }

            return {
                ok: true,
                queued: enabled && cameraChanged,
                config: config,
                cameraReapply: cameraChanged,
                message: enabled && cameraChanged
                    ? '相机参数已保存，将在主线程重新应用'
                    : '参数已保存，无需重建相机'
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
                sessionDestroyed: sessionDestroyed,
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
                combatRuntime: {
                    adsActive: combat.adsActive,
                    playerDead: combat.playerDead,
                    finalCamera: {
                        valid: combat.finalCamera.valid,
                        pitchDeg: combat.finalCamera.pitchDeg,
                        position: combat.finalCamera.position,
                        forward: combat.finalCamera.forward
                    },
                    aimTarget: {
                        valid: combat.aimTarget.valid,
                        mode: combat.aimTarget.reason,
                        hit: combat.aimTarget.hit,
                        colliderId: combat.aimTarget.colliderId,
                        point: combat.aimTarget.point,
                        distance: combat.aimTarget.distance
                    },
                    shootSolution: {
                        valid: combat.shootSolution.valid,
                        reason: combat.shootSolution.reason,
                        distance: combat.shootSolution.distance,
                        muzzleObstructionHit:
                            combat.shootSolution.muzzleObstructionHit
                    },
                    muzzle: {
                        valid: combat.muzzle.valid,
                        source: combat.muzzle.source,
                        position: combat.muzzle.position
                    },
                    aimIK: {
                        enabled: config.aimIK,
                        found: combat.aimIK.found,
                        reason: combat.aimIK.reason
                    },
                    collider: {
                        captured: !isNull(combat.collider.pointer),
                        displaced: combat.collider.displaced,
                        distance: combat.collider.distance
                    },
                    fade: {
                        enabled: config.occlusionFade,
                        alpha: stats.currentFadeAlpha,
                        materialFade:
                            combat.renderers.usingMaterialFade,
                        hiddenFallback:
                            combat.renderers.hiddenFallback
                    }
                },
                featureAssessment: {
                    classification:
                        enabled &&
                        stats.finalCameraSamples > 0
                            ? 'third_person_combat_integration'
                            : 'partial_camera_demo',
                    matureThirdPersonShooterReady:
                        stats.shootRayModified > 0 &&
                        stats.damageRayMatches > 0 &&
                        stats.finalCameraSamples > 0 &&
                        stats.colliderCallbacks > 0,
                    shootingImplemented:
                        config.shootingRay,
                    physicsAimRaycastImplemented:
                        config.physicsAimRaycast,
                    shootingRuntimeVerified:
                        stats.shootRayModified > 0 &&
                        stats.damageRayMatches > 0,
                    adsImplemented:
                        config.adsFirstPerson,
                    adsRuntimeVerified:
                        stats.adsEnterCount > 0 &&
                        stats.adsExitCount > 0,
                    aimIKImplemented:
                        config.aimIK,
                    aimIKRuntimeVerified:
                        stats.aimIKFound > 0 &&
                        stats.aimIKWrites > 0,
                    upperBodyRuntimeVerified:
                        stats.upperBodyWrites > 0,
                    collisionRuntimeVerified:
                        stats.colliderCallbacks > 0,
                    dynamicShoulderRuntimeVerified:
                        stats.shoulderSwapCount > 0,
                    lifecycleRuntimeVerified:
                        stats.weaponChangeEvents > 0 ||
                        stats.deathEvents > 0 ||
                        stats.respawnEvents > 0 ||
                        stats.spawnEvents > 0,
                    fadeRuntimeVerified:
                        stats.fadeUpdates > 0
                },
                design: {
                    movementModified: false,
                    characterYawModified: false,
                    shootingRayModified:
                        config.shootingRay,
                    damageModified: false,
                    crosshairPolicy:
                        'fixed screen center -> final camera forward -> PhysicsScene hit/far fallback',
                    cameraTarget:
                        'stable characterContainer',
                    verticalPitch:
                        'Player.cameraRotation.y -> FreeLook.YAxis.Value',
                    finalCameraVerification:
                        'output Camera transform sampled on Brain callback',
                    shootingPipeline:
                        'camera target -> muzzle convergence -> Recoil.GetShootRay',
                    ads:
                        'right mouse -> temporary first-person ADS',
                    aimIK:
                        'runtime AimIK/AimController lookup; upper-body fallback',
                    upperBodyAim:
                        'CharacterModel.targetLowerAngle',
                    collision:
                        'native CinemachineCollider + displacement telemetry',
                    occlusion:
                        'material alpha fade with renderer-hide fallback',
                    telemetry:
                        'Pitch + Combat + Collider + ShootRay + DamageRay + VisualAim'
                }
            };
        },

        cleanup: cleanup
    };

    sendLog('info', '第三人称战斗性能优化版 v3.1 脚本已加载', {
        base: base.toString(),
        arch: Process.arch,
        pointerSize: Process.pointerSize
    });
})();
