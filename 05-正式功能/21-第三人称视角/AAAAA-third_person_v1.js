(function() {
    'use strict';

    // =============================================
    // UCF1.7 第三人称视角修改器 v9
    // 修复：32位 x86 ABI、射击Hook地址、MethodInfo*参数
    //       CameraManager安全获取、Transform/Camera调用修正
    //       武器Transform树枚举、诊断启动条件
    // =============================================

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { send('no module'); return; }
    var base = mod.base;
    send({type:'log', level:'info', module:'TP', message:'base=' + base + ' size=' + mod.size});

    // ---- 32位验证 ----
    var PTR_SIZE = Process.pointerSize;
    var IS_32BIT = (PTR_SIZE === 4);
    var CALL_CONV = 'mscdecl';  // 32位 IL2CPP 使用 __cdecl，Frida 对应 'mscdecl'
    send({type:'log', level:'info', module:'TP', message:'arch=' + Process.arch + ' pointerSize=' + PTR_SIZE + ' is32bit=' + IS_32BIT});
    if (!IS_32BIT) {
        send({type:'log', level:'error', module:'TP', message:'WARNING: 非32位进程，当前代码仅支持32位! pointerSize=' + PTR_SIZE});
    }

    // ---- RVA 常量 (全部经过 dump.cs + script.json 验证) ----
    var RVA = {
        // CameraManager (dump.cs line 242236)
        CameraManager_Awake:                  0xB35550,
        CameraManager_Update:                 0xB36FA0,
        CameraManager_OnDestroy:              0xB360E0,
        CameraManager_ChangePVandCV:          0xB35920,
        CameraManager_SetFreeLookCameraActive:0xB36790,
        CameraManager_SpawnEvent:             0xB36A30,

        // GameManager (dump.cs line 242579)
        GameManager_Awake:                    0xAFA250,
        GameManager_OnDestroy:                0xAFB6F0,
        GameManager_AddPlayer:                0xAF9A90,
        GameManager_NewGameRoundStart:        0xAEBCB0,

        // PlayerController (dump.cs line 244432)
        PlayerController_CameraRotation:      0xB12420,

        // Player (dump.cs line 234190)
        Player_get_isMyPlayer:                0xB55FD0,
        Player_get_currentCharacter:          0x1CF1D0,
        Player_get_playerData:                0x2A42D0,
        Player_get_wpns:                      0x1CF190,

        // PlayerData (dump.cs line 233146)
        PlayerData_SetObserveMode:            0xB13AD0,  // script.json: 11614928 = 0xB13AD0 ✓
        PlayerData_get_observeMode:           0x1D7B80,  // script.json: 1932160 = 0x1D7B80 ✓
        PlayerData_set_observeMode:           0x1D7C30,  // script.json: 1932336 = 0x1D7C30 (private setter)

        // PlayerCameraManager (dump.cs line 234955)
        PCM_set_modelVisible:                 0xB12370,  // script.json: 11608944 = 0xB12370 ✓

        // Model (dump.cs line 244160)
        Model_SetModelLayer:                  0xB4B4C0,
        Model_OnOwnerObserveModeChange:       0xB4B300,  // script.json: 11842304 = 0xB4B300 ✓
        Model_BindSocket:                     0xB4AF40,  // dump.cs: public void BindSocket(Transform tsf, string socketName)

        // Weapon (dump.cs line 249654)
        Weapon_PlayerViewSetting:             0xB6CFB0,  // script.json: 11980720 = 0xB6CFB0 ✓
        Weapon_SynchronizeHand:               0xB6DA20,  // script.json: 11983392 = 0xB6DA20 ✓

        // CinemachineFreeLook (dump.cs line 206617)
        CFL_set_Follow:                       0x439270,
        CFL_set_LookAt:                       0x2E7E10,
        CFL_GetRig:                           0x6BEDF0,

        // CinemachineVirtualCamera (dump.cs line 207657)
        CVC_GetComponentPipeline:             0x501E80,

        // Unity 核心方法
        GameObject_SetActive:                 0x331CF0,
        GameObject_get_activeSelf:            0x331F50,
        GameObject_get_layer:                 0x331FB0,
        GameObject_set_layer:                 0x332040,
        GameObject_get_name:                  0x4EA1B0,
        Renderer_get_enabled:                 0x3E4D70,
        Renderer_set_enabled:                 0x3E5030,

        // Singleton<T>
        Singleton_GetInstance:                0x4A8170,

        // MethodInfo 指针
        GameManager_SingletonMethodInfo:      0xE1CE64,
        CameraManager_SingletonMethodInfo:    0xE1CD68,

        // v9: 射击相关 (IDA验证，修正 +0x1000)
        Recoil_GetShootRay:                   0xB195C0,  // IDA: il2cpp:10B195C0, 原0xB185C0错误
        WPN_Gun_Damage:                       0xB613D0,  // IDA: il2cpp:10B613D0, 原0xB603D0错误
        WPN_Gun_GunShoot:                     0xB624C0,  // IDA: il2cpp:10B624C0, 原0xB614C0错误
        WPN_Gun_GunShoot_Logic:               0xB62170,  // IDA: il2cpp:10B62170, 原0xB61170错误

        // Phase6: 事件处理 (dump.cs)
        Player_OnEntityDeath:                 0xB51210,  // Player.OnEntityDeath
        Player_SetWeapon:                     0xB53650,  // Player.SetWeapon
        Player_Respawn:                       0xB527A0,  // Player.Respawn
        Player_Spawn:                         0xB53760,  // Player.Spawn

        // Phase5: 相机碰撞
        Physics_SphereCast:                   0xABB560,  // Physics.SphereCast

        // v9: Unity API (32位 _Injected 版本)
        // Transform
        Transform_get_position_Injected:      0x3F4280,
        Transform_get_rotation_Injected:      0x3F4380,
        Transform_get_forward:                0x3F3F20,
        Transform_get_right:                  0x3F42F0,
        Transform_get_up:                     0x3F43F0,
        Transform_get_parent:                 0x3F31D0,
        Transform_GetChild:                   0x3F3150,
        Transform_get_childCount:             0x3F3E80,
        // Component.get_transform: 返回 Transform*
        Component_get_transform:              0x032CF40,  // 修复: 正确 RVA
        // Object.get_name: 返回 String*
        Object_get_name:                      0x4EA1B0,
        // Camera
        Camera_get_main:                      0x328310,
        Camera_get_current:                   0x3281C0,
        Camera_get_fieldOfView:               0x328270,
        Camera_get_pixelWidth:                0x328490,
        Camera_get_pixelHeight:               0x3283F0,
        Camera_get_aspect:                    0x328090,
        Camera_ScreenPointToRay_Injected:     0x327AD0,
        Camera_WorldToScreenPoint_Injected:   0x327EE0,
        // CinemachineBrain
        Brain_get_OutputCamera:               0x82CDB0,
        // Physics
        Physics_Raycast:                      0xABAF40,
    };

    // ---- 字段偏移 (dump.cs 验证) ----
    var OFF = {
        // CameraManager
        CM_focusPlayer:         0x0C,
        CM_freeLookCamera:      0x10,
        CM_brain:               0x14,

        // Player
        Player_cameraManager:   0x48,
        Player_cameraRotation:  0x4C,
        Player_recoil:          0x54,  // Phase4: Player.recoil -> Recoil
        Player_characterContainer: 0x58,
        Player_currentCharacter:   0x5C,
        Player_playerData:      0x98,
        Player_wpns:            0xA0,

        // PlayerData
        PD_observeMode:         0x08,
        PD_ObserveMode_Listener:0x0C,
        PD_playerViewModelVisible: 0x24,

        // PlayerWeapons
        PW_inUse:               0x18,
        PW_current:             0x1C,

        // CharacterModel (继承自 Model)
        Model_objectInPV:       0x34,
        Model_objectInCV:       0x38,
        Model_sockets:          0x3C,
        CM_spine:               0x5C,
        CM_spine1:              0x60,
        CM_neck:                0x64,
        CM_handAnimator:        0x4C,
        CM_characterAnimator:   0x48,
        CM_cvRenderers:         0x54,
        CM_socketItemsName:     0x68,
        // Phase2: QVModel 相关偏移 (Kimi 验证)
        CM_bindQvMdl:           0xB4,  // CharacterModel.bindQvMdl -> QVModel

        // Phase2: QVModel (Kimi 验证)
        QV_left:                0x44,  // QVModel.left -> QVModel.Data
        QV_right:               0x7C,  // QVModel.right -> QVModel.Data
        QV_bindWpn:             0xB8,  // QVModel.bindWpn -> Weapon

        // Phase2: QVModel.Data (Kimi 验证, 大小 0x38)
        QVD_Model:              0x00,  // QVModel.Data.Model -> Transform
        QVD_GunFire:            0x34,  // QVModel.Data.GunFire -> ParticleSystem

        // Phase4: AimIK (Kimi 验证)
        Recoil_aimIK:           0x18,  // Recoil.aimIK -> AimIK
        AimIK_solver:           0x1C,  // AimIK.solver -> IKSolverAim
        IKSolver_IKPosition:    0x08,  // IKSolver.IKPosition -> Vector3
        IKSolver_IKPositionWeight: 0x14, // IKSolver.IKPositionWeight -> float

        // CinemachineFreeLook
        CFL_m_LookAt:           0x40,
        CFL_m_Follow:           0x44,
        CFL_m_YAxis:            0x88,
        CFL_m_XAxis:            0x104,
        CFL_m_Orbits:           0x194,
        CFL_m_Rigs:             0x258,

        // CinemachineVirtualCamera
        CVC_m_ComponentPipeline: 0x140,

        // CinemachineTransposer
        CT_m_FollowOffset:      0x2C,

        // CinemachineOrbitalTransposer (继承自 CinemachineTransposer)
        COT_m_XAxis:            0xC0,

        // CinemachineComposer
        CC_m_TrackedObjectOffset: 0x28,
        CC_m_ScreenX:           0x48,
        CC_m_ScreenY:           0x4C,
        CC_m_DeadZoneWidth:     0x50,
        CC_m_DeadZoneHeight:    0x54,

        // GameManager
        GM_allPlayers:          0x1C,

        // Model.Socket
        MS_name:                0x00,
        MS_node:                0x04,
        MS_offset:              0x08,
        MS_euler:               0x14,

        // PlayerCameraManager
        PCM_modelCamera:        0x10,
        PCM_modelContainer:     0x18,
    };

    // ---- NativeFunction 声明 (v9: 全部使用 mscdecl + MethodInfo*) ----
    // 规则：
    // 1. 所有 IL2CPP 实例方法最后一个参数是 MethodInfo*，传入 ptr(0)
    // 2. 所有函数使用 'mscdecl' 调用约定 (32位 __cdecl)
    // 3. 值类型返回 >8B 的函数，调用者分配 retBuf 作为隐藏参数

    // --- 游戏逻辑方法 ---
    var isMyPlayer = new NativeFunction(base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer'], CALL_CONV);
    var singletonGetter = new NativeFunction(base.add(RVA.Singleton_GetInstance), 'pointer', ['pointer'], CALL_CONV);
    var cflSetFollow = new NativeFunction(base.add(RVA.CFL_set_Follow), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
    var cflSetLookAt = new NativeFunction(base.add(RVA.CFL_set_LookAt), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
    var setFreeLookActive = new NativeFunction(base.add(RVA.CameraManager_SetFreeLookCameraActive), 'void', ['pointer', 'bool', 'pointer'], CALL_CONV);
    var setModelLayer = new NativeFunction(base.add(RVA.Model_SetModelLayer), 'void', ['pointer', 'int', 'int', 'pointer'], CALL_CONV);
    var setObserveMode = new NativeFunction(base.add(RVA.PlayerData_SetObserveMode), 'void', ['pointer', 'int', 'pointer'], CALL_CONV);
    var getObserveMode = new NativeFunction(base.add(RVA.PlayerData_get_observeMode), 'int', ['pointer', 'pointer'], CALL_CONV);
    // v9 修复: set_modelVisible 加 MethodInfo* 参数
    var setModelVisible = new NativeFunction(base.add(RVA.PCM_set_modelVisible), 'void', ['pointer', 'bool', 'pointer'], CALL_CONV);
    var playerViewSetting = new NativeFunction(base.add(RVA.Weapon_PlayerViewSetting), 'void', ['pointer', 'pointer'], CALL_CONV);
    var synchronizeHand = new NativeFunction(base.add(RVA.Weapon_SynchronizeHand), 'void', ['pointer', 'pointer'], CALL_CONV);
    var gameObjectSetActive = new NativeFunction(base.add(RVA.GameObject_SetActive), 'void', ['pointer', 'bool', 'pointer'], CALL_CONV);
    var gameObjectGetActiveSelf = new NativeFunction(base.add(RVA.GameObject_get_activeSelf), 'bool', ['pointer', 'pointer'], CALL_CONV);
    var gameObjectGetLayer = new NativeFunction(base.add(RVA.GameObject_get_layer), 'int', ['pointer', 'pointer'], CALL_CONV);
    var gameObjectSetLayer = new NativeFunction(base.add(RVA.GameObject_set_layer), 'void', ['pointer', 'int', 'pointer'], CALL_CONV);
    var gameObjectGetName = new NativeFunction(base.add(RVA.GameObject_get_name), 'pointer', ['pointer', 'pointer'], CALL_CONV);
    var rendererGetEnabled = new NativeFunction(base.add(RVA.Renderer_get_enabled), 'bool', ['pointer', 'pointer'], CALL_CONV);
    var rendererSetEnabled = new NativeFunction(base.add(RVA.Renderer_set_enabled), 'void', ['pointer', 'bool', 'pointer'], CALL_CONV);
    var getRig = new NativeFunction(base.add(RVA.CFL_GetRig), 'pointer', ['pointer', 'int', 'pointer'], CALL_CONV);
    var getComponentPipeline = new NativeFunction(base.add(RVA.CVC_GetComponentPipeline), 'pointer', ['pointer', 'pointer'], CALL_CONV);
    var onOwnerObserveModeChange = new NativeFunction(base.add(RVA.Model_OnOwnerObserveModeChange), 'void', ['pointer', 'int', 'pointer'], CALL_CONV);

    // --- Unity API (32位 _Injected 版本) ---
    // Transform 方法: _Injected 版本签名 void(Transform*, Vector3*/Quaternion* ret, MethodInfo*)
    var transformGetPosition = new NativeFunction(base.add(RVA.Transform_get_position_Injected), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
    var transformGetRotation = new NativeFunction(base.add(RVA.Transform_get_rotation_Injected), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
    // get_forward/right/up: 32位返回Vector3(12B>8B), 隐藏retBuf参数
    // 签名: void(Vector3* retBuf, Transform*, MethodInfo*)
    var transformGetForward  = new NativeFunction(base.add(RVA.Transform_get_forward), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
    var transformGetRight    = new NativeFunction(base.add(RVA.Transform_get_right), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
    var transformGetUp       = new NativeFunction(base.add(RVA.Transform_get_up), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
    // get_parent: 返回 Transform* (指针, <=8B), 正常调用
    var transformGetParent   = new NativeFunction(base.add(RVA.Transform_get_parent), 'pointer', ['pointer', 'pointer'], CALL_CONV);
    // GetChild: 返回 Transform* (指针)
    var transformGetChild    = new NativeFunction(base.add(RVA.Transform_GetChild), 'pointer', ['pointer', 'int', 'pointer'], CALL_CONV);
    // get_childCount: 返回 int32
    var transformGetChildCount = new NativeFunction(base.add(RVA.Transform_get_childCount), 'int', ['pointer', 'pointer'], CALL_CONV);
    // Component.get_transform: 返回 Transform*
    var componentGetTransform = new NativeFunction(base.add(RVA.Component_get_transform), 'pointer', ['pointer', 'pointer'], CALL_CONV);
    // Object.get_name: 返回 String*
    var objectGetName = new NativeFunction(base.add(RVA.Object_get_name), 'pointer', ['pointer', 'pointer'], CALL_CONV);

    // Camera 方法
    var cameraGetMain        = new NativeFunction(base.add(RVA.Camera_get_main), 'pointer', ['pointer'], CALL_CONV);
    var cameraGetCurrent     = new NativeFunction(base.add(RVA.Camera_get_current), 'pointer', ['pointer'], CALL_CONV);
    var cameraGetFieldOfView = new NativeFunction(base.add(RVA.Camera_get_fieldOfView), 'float', ['pointer', 'pointer'], CALL_CONV);
    var cameraGetPixelWidth  = new NativeFunction(base.add(RVA.Camera_get_pixelWidth), 'int', ['pointer', 'pointer'], CALL_CONV);
    var cameraGetPixelHeight = new NativeFunction(base.add(RVA.Camera_get_pixelHeight), 'int', ['pointer', 'pointer'], CALL_CONV);
    var cameraGetAspect      = new NativeFunction(base.add(RVA.Camera_get_aspect), 'float', ['pointer', 'pointer'], CALL_CONV);
    // ScreenPointToRay_Injected: void(Camera*, Vector2* pos, int eye, Ray* ret, MethodInfo*)
    var cameraScreenPointToRay = new NativeFunction(base.add(RVA.Camera_ScreenPointToRay_Injected), 'void', ['pointer', 'pointer', 'int', 'pointer', 'pointer'], CALL_CONV);
    // WorldToScreenPoint_Injected: void(Camera*, Vector3* position, int eye, Vector3* ret, MethodInfo*)
    var cameraWorldToScreenPoint = new NativeFunction(base.add(RVA.Camera_WorldToScreenPoint_Injected), 'void', ['pointer', 'pointer', 'int', 'pointer', 'pointer'], CALL_CONV);

    // CinemachineBrain.get_OutputCamera: 返回 Camera*
    var brainGetOutputCamera = new NativeFunction(base.add(RVA.Brain_get_OutputCamera), 'pointer', ['pointer', 'pointer'], CALL_CONV);

    // Physics.Raycast: bool(Ray*, RaycastHit*, float, MethodInfo*)
    var physicsRaycast = new NativeFunction(base.add(RVA.Physics_Raycast), 'bool', ['pointer', 'pointer', 'float', 'pointer'], CALL_CONV);

    // Physics.SphereCast: bool(Vector3* origin, float radius, Vector3* direction, RaycastHit* hitInfo, float maxDistance, int layerMask, MethodInfo*)
    var physicsSphereCast = new NativeFunction(base.add(RVA.Physics_SphereCast), 'bool', ['pointer', 'float', 'pointer', 'pointer', 'float', 'int', 'pointer'], CALL_CONV);

    send({type:'log', level:'info', module:'TP', message:'NativeFunction 声明完成 (v9, mscdecl + MethodInfo*)'});

    // ============================================================
    // 状态机
    // ============================================================
    var STATE = {
        NO_GAME:       'NO_GAME',
        WAITING_ROOM:  'WAITING_ROOM',
        ROOM_READY:    'ROOM_READY',
        TP_ENABLED:    'TP_ENABLED',
        DISCONNECTED:  'DISCONNECTED',
    };

    var fsm = {
        current: STATE.NO_GAME,
        lastError: '',
        cameraDistance: 3.0,
        cameraSensitivity: 1.0,
        stats: { hookCalls: 0, stateChanges: 0, objectRegets: 0, errors: 0 },
    };

    function setState(newState) {
        if (fsm.current === newState) return;
        fsm.stats.stateChanges++;
        var old = fsm.current;
        fsm.current = newState;
        logOnce('state_change', '状态: ' + old + ' -> ' + newState);

        // Phase2: 离开房间或游戏时清空枪口缓存
        if (newState === STATE.NO_GAME || newState === STATE.WAITING_ROOM) {
            clearMuzzleCache();
        }
        send({type:'state_changed', oldState: old, newState: newState});
    }

    // ============================================================
    // 日志限流
    // ============================================================
    var logCache = {};
    var LOG_COOLDOWN = 3000;

    function log(level, msg) {
        send({type:'log', level:level, module:'TP', message:msg});
    }

    function logOnce(key, msg) {
        var now = Date.now();
        if (logCache[key] && (now - logCache[key]) < LOG_COOLDOWN) return;
        logCache[key] = now;
        log('info', msg);
    }

    function logError(key, msg) {
        fsm.lastError = msg;
        fsm.stats.errors++;
        var now = Date.now();
        if (logCache['err_' + key] && (now - logCache['err_' + key]) < LOG_COOLDOWN) return;
        logCache['err_' + key] = now;
        log('error', msg);
    }

    // ============================================================
    // 核心变量
    // ============================================================
    var gm = null;
    var cameraManager = null;
    var timer = null;
    var enabled = false;

    // 保存原始值用于恢复
    var savedState = {
        observeMode: -1,
        pvActiveStates: [],
        cvActiveStates: [],
        pvLayerStates: [],
        cvLayerStates: [],
        pvRendererStates: [],       // v8: PV 对象的 Renderer.enabled 状态
        cvRendererStates: [],       // v8: CV 对象的 Renderer.enabled 状态
        playerViewModelVisible: false, // v8: PlayerData.playerViewModelVisible 原始值
        freeLookActive: false,
        followSet: false,
        lookAtSet: false,
        orbitHeights: [],
        orbitRadii: [],
        composerScreenX: [],
        composerScreenY: [],
        composerTrackedOffset: [],
        composerDeadZoneW: [],      // v8
        composerDeadZoneH: [],      // v8
    };

    // ============================================================
    // 工具函数
    // ============================================================
    function ptrEquals(a, b) {
        if (!a || !b) return false;
        try { return a.equals(b); } catch(e) { return false; }
    }

    function isNull(p) {
        if (!p) return true;
        try { return p.isNull(); } catch(e) { return true; }
    }

    function isReadable(p) {
        try { p.readU8(); return true; } catch(e) { return false; }
    }

    function hasGm() {
        if (isNull(gm) || !isReadable(gm)) return false;
        try {
            var ap = gm.add(OFF.GM_allPlayers).readPointer();
            return !isNull(ap);
        } catch(e) { return false; }
    }

    function tryGetGM() {
        if (hasGm()) return true;
        try {
            var methodInfo = base.add(RVA.GameManager_SingletonMethodInfo).readPointer();
            if (isNull(methodInfo)) { logError('gm_mi', 'GameManager MethodInfo null'); return false; }
            var temp = singletonGetter(methodInfo);
            if (!isNull(temp) && isReadable(temp)) {
                gm = temp;
                log('info', 'GameManager 获取成功: ' + gm);
                return true;
            }
        } catch(e) { logError('gm_get', 'GameManager 获取失败: ' + e); }
        return false;
    }

    function tryGetCameraManager() {
        // v9: 如果 Awake 尚未触发，直接返回 null，不调用 Singleton getter
        if (!isNull(cameraManager) && isReadable(cameraManager)) return cameraManager;
        // 不再尝试 Singleton 获取，避免 Awake 前越界
        return null;
    }

    function findMyPlayer() {
        if (!hasGm()) return null;
        try {
            var ap = gm.add(OFF.GM_allPlayers).readPointer();
            if (isNull(ap)) return null;
            var total = ap.add(0xC).readU32();
            if (total < 1 || total > 64) return null;
            for (var i = 0; i < total; i++) {
                // 32位: 指针大小 4 字节
                var pp = ap.add(0x10 + i * PTR_SIZE).readPointer();
                if (!isNull(pp) && isMyPlayer(pp, ptr(0))) return pp;
            }
        } catch(e) { logError('find_player', 'findMyPlayer 失败: ' + e); }
        return null;
    }

    function readIl2cppString(strPtr) {
        if (isNull(strPtr)) return '<null>';
        try {
            // 修复: 32位 IL2CPP 字符串偏移
            // +0x08 length (int32)
            // +0x0C characters (UTF-16)
            var len = strPtr.add(0x08).readS32();
            if (len < 0 || len > 1024) return '<invalid_len>';
            return strPtr.add(0x0C).readUtf16String(len);
        } catch(e) { return '<read_err>'; }
    }

    // Phase1: 32位 List<T> 布局
    // +0x08 _items (T[])
    // +0x0C _size (int)
    // +0x10 _version (int)
    function readListItems(listPtr, label) {
        var result = { items: [], count: 0 };
        if (isNull(listPtr)) return result;
        try {
            // Phase1: 修正 32 位 List 偏移
            var itemsPtr = listPtr.add(0x08).readPointer();  // _items (Il2CppArray*)
            var count = listPtr.add(0x0C).readS32();          // _size
            if (count < 0 || count > 100) return result;
            result.count = count;
            // 修复: Il2CppArray 元素从 +0x10 开始
            for (var i = 0; i < count; i++) {
                var itemPtr = itemsPtr.add(0x10 + i * PTR_SIZE).readPointer();
                result.items.push(itemPtr);
            }
        } catch(e) {}
        return result;
    }

    // Phase1: 32位 Il2CppArray 布局
    // +0x10 第一个元素
    function readArrayItems(arrayPtr, elementSize) {
        var result = { items: [], count: 0 };
        if (isNull(arrayPtr)) return result;
        try {
            var bounds = arrayPtr.add(0x04).readPointer();  // bounds
            if (!isNull(bounds)) {
                var count = bounds.readU32();  // length
                if (count < 0 || count > 100) return result;
                result.count = count;
                var dataPtr = arrayPtr.add(0x10);  // 第一个元素
                for (var i = 0; i < count; i++) {
                    var itemPtr = dataPtr.add(i * elementSize);
                    result.items.push(itemPtr);
                }
            }
        } catch(e) {}
        return result;
    }

    function getGameObjectName(goPtr) {
        if (isNull(goPtr)) return '<null_go>';
        try {
            var namePtr = gameObjectGetName(goPtr, ptr(0));
            return readIl2cppString(namePtr);
        } catch(e) { return '<name_err>'; }
    }

    // 读取 List<GameObject> 的信息（含 Renderer.enabled）
    // Phase1: 使用 32 位 List 偏移
    function readGameObjectList(listPtr, label) {
        var result = { count: 0, items: [] };
        if (isNull(listPtr)) {
            log('info', '[诊断] ' + label + ': null');
            return result;
        }
        try {
            // Phase1: 修正 32 位 List 偏移
            var itemsPtr = listPtr.add(0x08).readPointer();  // _items
            var count = listPtr.add(0x0C).readS32();          // _size
            result.count = count;
            log('info', '[诊断] ' + label + ' 数量: ' + count);
            for (var i = 0; i < count && i < 30; i++) {
                // 32位: 指针大小 4 字节
                var goPtr = itemsPtr.add(i * PTR_SIZE).readPointer();
                if (isNull(goPtr)) {
                    result.items.push({ name: '<null>', active: false, layer: -1, rendererEnabled: null });
                    continue;
                }
                var name = getGameObjectName(goPtr);
                var active = false;
                var layer = -1;
                var renEnabled = null;
                try { active = gameObjectGetActiveSelf(goPtr, ptr(0)); } catch(e) {}
                try { layer = gameObjectGetLayer(goPtr, ptr(0)); } catch(e) {}
                // 尝试获取 Renderer.enabled（GameObject 可能有多个 Renderer 组件，这里只尝试第一个）
                try {
                    // Unity GameObject.GetComponent 快捷方式不可用，但我们可以通过
                    // 遍历子对象的 Renderer 来获取。此处先标记为 null，在诊断 RPC 中详细获取
                } catch(e) {}
                result.items.push({ name: name, active: active, layer: layer, rendererEnabled: renEnabled });
                if (i < 15) {
                    log('info', '[诊断]   [' + i + '] ' + name + ' active=' + active + ' layer=' + layer);
                }
            }
            if (count > 15) {
                log('info', '[诊断]   ... 还有 ' + (count - 15) + ' 个对象');
            }
        } catch(e) {
            logError('list_read', label + ' 读取失败: ' + e);
        }
        return result;
    }

    // ============================================================
    // 核心：PV/CV 模型切换 (v8 重写)
    // ============================================================
    function switchToCVMode(player, character) {
        // 1. 保存原始观察模式
        try {
            var playerData = player.add(OFF.Player_playerData).readPointer();
            if (!isNull(playerData)) {
                savedState.observeMode = getObserveMode(playerData, ptr(0));
                // v8: 保存 playerViewModelVisible
                savedState.playerViewModelVisible = playerData.add(OFF.PD_playerViewModelVisible).readU8() !== 0;
                log('info', '[Model] 原始 observeMode=' + savedState.observeMode +
                    ' playerViewModelVisible=' + savedState.playerViewModelVisible);
            }
        } catch(e) {
            logError('save_mode', '保存 observeMode 失败: ' + e);
        }

        // 2. 保存 PV/CV 对象的原始状态（含 Layer）
        if (!isNull(character)) {
            try {
                var pvListPtr = character.add(OFF.Model_objectInPV).readPointer();
                var cvListPtr = character.add(OFF.Model_objectInCV).readPointer();

                savedState.pvActiveStates = [];
                savedState.pvLayerStates = [];
                savedState.cvActiveStates = [];
                savedState.cvLayerStates = [];

                // 保存 PV 对象状态
                // Phase1: 使用 32 位 List 偏移
                if (!isNull(pvListPtr)) {
                    var pvItems = pvListPtr.add(0x08).readPointer();  // _items (Il2CppArray*)
                    var pvCount = pvListPtr.add(0x0C).readS32();      // _size
                    for (var i = 0; i < pvCount && i < 30; i++) {
                        // 修复: Il2CppArray 元素从 +0x10 开始
                        var goPtr = pvItems.add(0x10 + i * PTR_SIZE).readPointer();
                        if (!isNull(goPtr)) {
                            try {
                                savedState.pvActiveStates.push(gameObjectGetActiveSelf(goPtr, ptr(0)));
                                savedState.pvLayerStates.push(gameObjectGetLayer(goPtr, ptr(0)));
                            } catch(e) {
                                savedState.pvActiveStates.push(true);
                                savedState.pvLayerStates.push(-1);
                            }
                        }
                    }
                    log('info', '[Model] 保存 PV 对象状态: ' + savedState.pvActiveStates.length + ' 个');
                }

                // 保存 CV 对象状态
                // Phase1: 使用 32 位 List 偏移
                if (!isNull(cvListPtr)) {
                    var cvItems = cvListPtr.add(0x08).readPointer();  // _items (Il2CppArray*)
                    var cvCount = cvListPtr.add(0x0C).readS32();      // _size
                    for (var i = 0; i < cvCount && i < 30; i++) {
                        // 修复: Il2CppArray 元素从 +0x10 开始
                        var goPtr = cvItems.add(0x10 + i * PTR_SIZE).readPointer();
                        if (!isNull(goPtr)) {
                            try {
                                savedState.cvActiveStates.push(gameObjectGetActiveSelf(goPtr, ptr(0)));
                                savedState.cvLayerStates.push(gameObjectGetLayer(goPtr, ptr(0)));
                            } catch(e) {
                                savedState.cvActiveStates.push(false);
                                savedState.cvLayerStates.push(-1);
                            }
                        }
                    }
                    log('info', '[Model] 保存 CV 对象状态: ' + savedState.cvActiveStates.length + ' 个');
                }
            } catch(e) {
                logError('save_state', '保存 PV/CV 对象状态失败: ' + e);
            }
        }

        // 3. 调用 PlayerData.SetObserveMode(Character=0) — 触发 ObserveMode_Listener
        try {
            var playerData = player.add(OFF.Player_playerData).readPointer();
            if (!isNull(playerData)) {
                setObserveMode(playerData, 0, ptr(0)); // Model.Type.Character = 0
                log('info', '[Model] SetObserveMode(Character=0) 已调用');
            }
        } catch(e) {
            logError('set_observe', 'SetObserveMode 失败: ' + e);
        }

        // 4. v8 核心：直接调用 Model.OnOwnerObserveModeChange(Character=0)
        //    这是游戏原生的 PV→CV 切换函数，会自动：
        //    - 隐藏 objectInPV 中的对象
        //    - 显示 objectInCV 中的对象
        //    - 切换动画器
        //    - 同步武器
        if (!isNull(character)) {
            try {
                onOwnerObserveModeChange(character, 0, ptr(0)); // Model.Type.Character = 0
                log('info', '[Model] OnOwnerObserveModeChange(Character=0) 已调用');
            } catch(e) {
                logError('on_observe', 'OnOwnerObserveModeChange 失败: ' + e);
            }
        }

        // 5. 显式隐藏 PV 对象（双重保险，确保第一人称枪模消失）
        // Phase1: 使用 32 位 List 偏移
        if (!isNull(character)) {
            try {
                var pvListPtr = character.add(OFF.Model_objectInPV).readPointer();
                if (!isNull(pvListPtr)) {
                    var pvItems = pvListPtr.add(0x08).readPointer();  // _items (Il2CppArray*)
                    var pvCount = pvListPtr.add(0x0C).readS32();      // _size
                    var hiddenCount = 0;
                    for (var i = 0; i < pvCount && i < 30; i++) {
                        // 修复: Il2CppArray 元素从 +0x10 开始
                        var goPtr = pvItems.add(0x10 + i * PTR_SIZE).readPointer();
                        if (!isNull(goPtr)) {
                            try {
                                // 先检查当前状态
                                var wasActive = gameObjectGetActiveSelf(goPtr, ptr(0));
                                if (wasActive) {
                                    gameObjectSetActive(goPtr, 0, ptr(0));  // Phase1: bool -> 0
                                    hiddenCount++;
                                }
                            } catch(e) {}
                        }
                    }
                    log('info', '[Model] PV 对象显式隐藏: ' + hiddenCount + '/' + pvCount + ' 个 (从 active 变为 inactive)');
                }
            } catch(e) {
                logError('pv_hide', 'PV 对象隐藏失败: ' + e);
            }

            // 6. 显式显示 CV 对象（双重保险）
            // Phase1: 使用 32 位 List 偏移
            try {
                var cvListPtr = character.add(OFF.Model_objectInCV).readPointer();
                if (!isNull(cvListPtr)) {
                    var cvItems = cvListPtr.add(0x08).readPointer();  // _items (Il2CppArray*)
                    var cvCount = cvListPtr.add(0x0C).readS32();      // _size
                    var shownCount = 0;
                    for (var i = 0; i < cvCount && i < 30; i++) {
                        // 修复: Il2CppArray 元素从 +0x10 开始
                        var goPtr = cvItems.add(0x10 + i * PTR_SIZE).readPointer();
                        if (!isNull(goPtr)) {
                            try {
                                var wasActive = gameObjectGetActiveSelf(goPtr, ptr(0));
                                if (!wasActive) {
                                    gameObjectSetActive(goPtr, 1, ptr(0));  // Phase1: bool -> 1
                                    shownCount++;
                                }
                            } catch(e) {}
                        }
                    }
                    log('info', '[Model] CV 对象显式显示: ' + shownCount + '/' + cvCount + ' 个 (从 inactive 变为 active)');
                }
            } catch(e) {
                logError('cv_show', 'CV 对象显示失败: ' + e);
            }

            // 7. 设置模型 Layer 为 Default (0)，确保全身模型被主相机渲染
            try {
                setModelLayer(character, 0, 0, ptr(0)); // Model.Type.Character=0, Layer=0(Default)
                log('info', '[Model] SetModelLayer(Character, Default) 已调用');
            } catch(e) {
                logError('set_layer', 'SetModelLayer 失败: ' + e);
            }
        }

        // 8. 隐藏 PlayerCameraManager 的 modelVisible (第一人称手臂相机)
        try {
            var pcm = player.add(OFF.Player_cameraManager).readPointer();
            if (!isNull(pcm)) {
                setModelVisible(pcm, 0, ptr(0));  // Phase1: bool -> 0
                log('info', '[Model] PlayerCameraManager.modelVisible = false');
            }
        } catch(e) {
            logError('model_visible', 'set_modelVisible 失败: ' + e);
        }

        // 9. 设置 PlayerData.playerViewModelVisible = false
        try {
            var playerData = player.add(OFF.Player_playerData).readPointer();
            if (!isNull(playerData)) {
                playerData.add(OFF.PD_playerViewModelVisible).writeU8(0);
                log('info', '[Model] playerViewModelVisible = false');
            }
        } catch(e) {
            logError('pvm_visible', '设置 playerViewModelVisible 失败: ' + e);
        }

        // 10. 调用 Weapon.SynchronizeHand() 同步第三人称武器
        try {
            var wpns = player.add(OFF.Player_wpns).readPointer();
            if (!isNull(wpns)) {
                var inUse = wpns.add(OFF.PW_inUse).readPointer();
                if (!isNull(inUse)) {
                    try {
                        synchronizeHand(inUse, ptr(0));
                        log('info', '[Weapon] SynchronizeHand 已调用');
                    } catch(e) {
                        logError('sync_hand', 'SynchronizeHand 失败: ' + e);
                    }
                } else {
                    log('info', '[Weapon] inUse 为 null，跳过 SynchronizeHand');
                }
            }
        } catch(e) {
            logError('wpn_sync', '获取武器失败: ' + e);
        }
    }

    // ============================================================
    // 核心：相机配置 (v8 重写 — 肩后 TPS 视角)
    // 修正：不修改 FollowOffset，只用轨道+Composer 实现肩后视角
    // ============================================================
    function configureCamera(freeLook, charContainer, spine1) {
        // 1. 保存原始轨道参数
        try {
            savedState.orbitHeights = [];
            savedState.orbitRadii = [];
            var orbitsPtr = freeLook.add(OFF.CFL_m_Orbits).readPointer();
            if (!isNull(orbitsPtr)) {
                var arrLen = orbitsPtr.add(0xC).readU32();
                for (var i = 0; i < arrLen && i < 3; i++) {
                    savedState.orbitHeights.push(orbitsPtr.add(0x10 + i * 8).readFloat());
                    savedState.orbitRadii.push(orbitsPtr.add(0x14 + i * 8).readFloat());
                }
                log('info', '[Camera] 原始轨道: Top(' + savedState.orbitHeights[0] + ',' + savedState.orbitRadii[0] +
                    ') Mid(' + savedState.orbitHeights[1] + ',' + savedState.orbitRadii[1] +
                    ') Bot(' + savedState.orbitHeights[2] + ',' + savedState.orbitRadii[2] + ')');
            }
        } catch(e) {
            logError('save_orbits', '保存轨道参数失败: ' + e);
        }

        // 2. 设置肩后 TPS 轨道（降低高度，减少俯视）
        try {
            var orbitsPtr = freeLook.add(OFF.CFL_m_Orbits).readPointer();
            if (!isNull(orbitsPtr)) {
                var arrLen = orbitsPtr.add(0xC).readU32();
                if (arrLen >= 3) {
                    var dist = fsm.cameraDistance;
                    // Top Rig: 略高于头部
                    orbitsPtr.add(0x10).writeFloat(1.8);
                    orbitsPtr.add(0x14).writeFloat(dist);
                    // Middle Rig: 肩膀高度
                    orbitsPtr.add(0x18).writeFloat(1.4);
                    orbitsPtr.add(0x1C).writeFloat(dist);
                    // Bottom Rig: 腰部高度
                    orbitsPtr.add(0x20).writeFloat(0.6);
                    orbitsPtr.add(0x24).writeFloat(dist * 0.85);
                    log('info', '[Camera] 轨道已设置: Top(1.8,' + dist + ') Mid(1.4,' + dist + ') Bot(0.6,' + (dist * 0.85) + ')');
                }
            }
        } catch(e) {
            logError('set_orbits', '设置轨道失败: ' + e);
        }

        // 3. 设置每个 Rig 的 Composer (ScreenX 偏移实现肩后视角)
        //    v8 修正：不修改 FollowOffset，只修改 Composer 参数
        try {
            savedState.composerScreenX = [];
            savedState.composerScreenY = [];
            savedState.composerTrackedOffset = [];
            savedState.composerDeadZoneW = [];
            savedState.composerDeadZoneH = [];

            for (var rigIdx = 0; rigIdx < 3; rigIdx++) {
                var rig = getRig(freeLook, rigIdx, ptr(0));
                if (isNull(rig)) continue;
                var pipeline = getComponentPipeline(rig, ptr(0));
                if (isNull(pipeline)) continue;

                var pipeLen = pipeline.add(0xC).readU32();
                for (var ci = 0; ci < pipeLen && ci < 10; ci++) {
                    // 32位: 指针大小 4 字节
                    var comp = pipeline.add(0x10 + ci * PTR_SIZE).readPointer();
                    if (isNull(comp)) continue;

                    // 尝试设置 Composer 参数
                    // 判断方法：读取 m_ScreenX (0x48) 处的值，如果合理（0~1 范围），认为是 Composer
                    try {
                        var screenX = comp.add(OFF.CC_m_ScreenX).readFloat();
                        var screenY = comp.add(OFF.CC_m_ScreenY).readFloat();
                        // 验证是否是合理的 Composer 值（ScreenX/Y 通常在 0~1）
                        if (screenX < -1 || screenX > 2 || screenY < -1 || screenY > 2) continue;

                        var trackedX = comp.add(OFF.CC_m_TrackedObjectOffset).readFloat();
                        var trackedY = comp.add(OFF.CC_m_TrackedObjectOffset + 4).readFloat();
                        var trackedZ = comp.add(OFF.CC_m_TrackedObjectOffset + 8).readFloat();
                        var deadW = comp.add(OFF.CC_m_DeadZoneWidth).readFloat();
                        var deadH = comp.add(OFF.CC_m_DeadZoneHeight).readFloat();

                        // 保存原始值
                        savedState.composerScreenX.push(screenX);
                        savedState.composerScreenY.push(screenY);
                        savedState.composerTrackedOffset.push([trackedX, trackedY, trackedZ]);
                        savedState.composerDeadZoneW.push(deadW);
                        savedState.composerDeadZoneH.push(deadH);

                        // 设置肩后视角：
                        // ScreenX=0.4 让角色偏左（右肩视角）
                        // ScreenY=0.5 垂直居中
                        // TrackedObjectOffset: 横向偏移看向右肩方向
                        comp.add(OFF.CC_m_ScreenX).writeFloat(0.4);
                        comp.add(OFF.CC_m_ScreenY).writeFloat(0.5);
                        comp.add(OFF.CC_m_TrackedObjectOffset).writeFloat(0.5);    // X: 右偏
                        comp.add(OFF.CC_m_TrackedObjectOffset + 4).writeFloat(0.3); // Y: 上偏
                        comp.add(OFF.CC_m_TrackedObjectOffset + 8).writeFloat(0.0); // Z: 不偏
                        // 减小死区让相机更跟手
                        comp.add(OFF.CC_m_DeadZoneWidth).writeFloat(0.03);
                        comp.add(OFF.CC_m_DeadZoneHeight).writeFloat(0.03);

                        log('info', '[Camera] Rig' + rigIdx + ' Composer: 原始 ScreenX=' + screenX.toFixed(2) +
                            ' ScreenY=' + screenY.toFixed(2) + ' -> ScreenX=0.4 ScreenY=0.5 TrackedOffset=(0.5,0.3,0)');
                    } catch(e) {
                        // 不是 Composer，跳过
                    }

                    // v8: 不再修改 FollowOffset
                    // OrbitalTransposer 的 FollowOffset 不应该被修改，
                    // 因为 CinemachineFreeLook 的轨道系统已经控制了相机位置。
                    // 修改 FollowOffset 会导致相机位置与轨道参数冲突，产生俯视效果。
                }
            }
        } catch(e) {
            logError('set_composer', '设置 Composer 失败: ' + e);
        }

        // 4. 设置 Follow 和 LookAt
        try {
            cflSetFollow(freeLook, charContainer, ptr(0));
            // LookAt 使用 spine1 (胸部位置)，而不是头部，减少俯视
            if (!isNull(spine1)) {
                cflSetLookAt(freeLook, spine1, ptr(0));
            } else {
                cflSetLookAt(freeLook, charContainer, ptr(0));
            }
            savedState.followSet = true;
            savedState.lookAtSet = true;
            log('info', '[Camera] Follow=charContainer LookAt=spine1');
        } catch(e) {
            logError('set_follow', '设置 Follow/LookAt 失败: ' + e);
        }
    }

    // ============================================================
    // 核心：启用/禁用第三人称
    // ============================================================
    function enableThirdPerson() {
        if (!tryGetGM()) {
            return { ok: false, enabled: false, error: 'GameManager 未就绪，请先进入房间' };
        }

        var player = findMyPlayer();
        if (!player) {
            return { ok: false, enabled: false, error: '找不到自己的玩家' };
        }

        var camMgr = tryGetCameraManager();
        if (!camMgr) {
            return { ok: false, enabled: false, error: 'CameraManager 未获取到' };
        }

        try {
            var freeLook = camMgr.add(OFF.CM_freeLookCamera).readPointer();
            if (isNull(freeLook)) {
                return { ok: false, enabled: false, error: 'FreeLook 相机为 null' };
            }

            var charContainer = player.add(OFF.Player_characterContainer).readPointer();
            if (isNull(charContainer)) {
                return { ok: false, enabled: false, error: 'CharacterContainer 为 null' };
            }

            var character = player.add(OFF.Player_currentCharacter).readPointer();
            var spine1 = null;
            if (!isNull(character)) {
                spine1 = character.add(OFF.CM_spine1).readPointer();
            }

            // 阶段1: 切换 PV/CV 模型
            switchToCVMode(player, character);

            // 阶段2: 配置相机
            configureCamera(freeLook, charContainer, spine1);

            // 激活 FreeLook
            setFreeLookActive(camMgr, 1, ptr(0));
            savedState.freeLookActive = true;

            // 全部成功，更新状态
            setState(STATE.TP_ENABLED);
            log('info', '第三人称已启用 (v8) - 距离=' + fsm.cameraDistance);
            return { ok: true, enabled: true, error: '' };
        } catch(e) {
            logError('enable', '启用第三人称异常: ' + e);
            return { ok: false, enabled: false, error: String(e) };
        }
    }

    function disableThirdPerson() {
        var errors = [];

        // Phase2: 清空枪口缓存
        clearMuzzleCache();

        // Phase4: 重置 AimIK 权重
        // 修复: AimIK 对象取错，暂时关闭
        // try {
        //     var player = findMyPlayer();
        //     if (player) {
        //         resetAimIKWeight(player);
        //         log('info', '[AimIK] 权重已重置');
        //     }
        // } catch(e) {}

        // Phase5: 重置相机碰撞状态
        cameraCollisionState.currentDistance = fsm.cameraDistance;
        cameraCollisionState.targetDistance = fsm.cameraDistance;

        try {
            // 1. 恢复观察模式
            var player = findMyPlayer();
            if (player) {
                // 1a. 调用 OnOwnerObserveModeChange(PlayerView=1) 恢复 PV 模式
                var character = player.add(OFF.Player_currentCharacter).readPointer();
                if (!isNull(character)) {
                    try {
                        onOwnerObserveModeChange(character, 1, ptr(0)); // Model.Type.PlayerView = 1
                        log('info', '[Restore] OnOwnerObserveModeChange(PlayerView=1) 已调用');
                    } catch(e) {
                        errors.push('OnOwnerObserveModeChange 恢复失败: ' + e);
                    }
                }

                // 1b. 恢复 PlayerData.SetObserveMode
                try {
                    var playerData = player.add(OFF.Player_playerData).readPointer();
                    if (!isNull(playerData) && savedState.observeMode >= 0) {
                        setObserveMode(playerData, savedState.observeMode, ptr(0));
                        log('info', '[Restore] SetObserveMode 恢复为 ' + savedState.observeMode);
                    }
                } catch(e) {
                    errors.push('恢复 SetObserveMode 失败: ' + e);
                }

                // 1c. 恢复 playerViewModelVisible
                try {
                    var playerData = player.add(OFF.Player_playerData).readPointer();
                    if (!isNull(playerData)) {
                        playerData.add(OFF.PD_playerViewModelVisible).writeU8(savedState.playerViewModelVisible ? 1 : 0);
                        log('info', '[Restore] playerViewModelVisible 恢复为 ' + savedState.playerViewModelVisible);
                    }
                } catch(e) {
                    errors.push('恢复 playerViewModelVisible 失败: ' + e);
                }

                // 2. 恢复 PV/CV 对象状态
                if (!isNull(character)) {
                    try {
                        // 恢复 PV 对象
                        // Phase1: 使用 32 位 List 偏移
                        var pvListPtr = character.add(OFF.Model_objectInPV).readPointer();
                        if (!isNull(pvListPtr)) {
                            var pvItems = pvListPtr.add(0x08).readPointer();  // _items (Il2CppArray*)
                            var pvCount = pvListPtr.add(0x0C).readS32();      // _size
                            for (var i = 0; i < pvCount && i < savedState.pvActiveStates.length; i++) {
                                // 修复: Il2CppArray 元素从 +0x10 开始
                                var goPtr = pvItems.add(0x10 + i * PTR_SIZE).readPointer();
                                if (!isNull(goPtr)) {
                                    try {
                                        gameObjectSetActive(goPtr, savedState.pvActiveStates[i], ptr(0));
                                        if (savedState.pvLayerStates[i] >= 0) {
                                            gameObjectSetLayer(goPtr, savedState.pvLayerStates[i], ptr(0));
                                        }
                                    } catch(e) {}
                                }
                            }
                            log('info', '[Restore] PV 对象已恢复: ' + pvCount + ' 个');
                        }

                        // 恢复 CV 对象
                        // Phase1: 使用 32 位 List 偏移
                        var cvListPtr = character.add(OFF.Model_objectInCV).readPointer();
                        if (!isNull(cvListPtr)) {
                            var cvItems = cvListPtr.add(0x08).readPointer();  // _items (Il2CppArray*)
                            var cvCount = cvListPtr.add(0x0C).readS32();      // _size
                            for (var i = 0; i < cvCount && i < savedState.cvActiveStates.length; i++) {
                                // 修复: Il2CppArray 元素从 +0x10 开始
                                var goPtr = cvItems.add(0x10 + i * PTR_SIZE).readPointer();
                                if (!isNull(goPtr)) {
                                    try {
                                        gameObjectSetActive(goPtr, savedState.cvActiveStates[i], ptr(0));
                                        if (savedState.cvLayerStates[i] >= 0) {
                                            gameObjectSetLayer(goPtr, savedState.cvLayerStates[i], ptr(0));
                                        }
                                    } catch(e) {}
                                }
                            }
                            log('info', '[Restore] CV 对象已恢复: ' + cvCount + ' 个');
                        }
                    } catch(e) {
                        errors.push('恢复 PV/CV 对象失败: ' + e);
                    }

                    // 3. 恢复模型 Layer
                    try {
                        setModelLayer(character, 1, 8, ptr(0)); // PlayerView, PV layer
                        log('info', '[Restore] SetModelLayer(PlayerView, Layer8) 已调用');
                    } catch(e) {
                        errors.push('恢复模型 Layer 失败: ' + e);
                    }
                }

                // 4. 恢复 PlayerCameraManager.modelVisible
                try {
                    var pcm = player.add(OFF.Player_cameraManager).readPointer();
                    if (!isNull(pcm)) {
                        setModelVisible(pcm, 1, ptr(0));  // Phase1: bool -> 1
                        log('info', '[Restore] modelVisible = true');
                    }
                } catch(e) {
                    errors.push('恢复 modelVisible 失败: ' + e);
                }

                // 5. 调用 Weapon.PlayerViewSetting 恢复第一人称武器
                try {
                    var wpns = player.add(OFF.Player_wpns).readPointer();
                    if (!isNull(wpns)) {
                        var inUse = wpns.add(OFF.PW_inUse).readPointer();
                        if (!isNull(inUse)) {
                            playerViewSetting(inUse, ptr(0));
                            log('info', '[Restore] PlayerViewSetting 已调用');
                        }
                    }
                } catch(e) {
                    errors.push('恢复武器设置失败: ' + e);
                }
            }

            // 6. 停用 FreeLook
            var camMgr = tryGetCameraManager();
            if (camMgr) {
                try {
                    setFreeLookActive(camMgr, 0, ptr(0));
                    savedState.freeLookActive = false;
                    log('info', '[Restore] FreeLook 已停用');
                } catch(e) {
                    errors.push('停用 FreeLook 失败: ' + e);
                }

                // 7. 恢复相机轨道参数
                try {
                    var freeLook = camMgr.add(OFF.CM_freeLookCamera).readPointer();
                    if (!isNull(freeLook)) {
                        // 恢复轨道
                        var orbitsPtr = freeLook.add(OFF.CFL_m_Orbits).readPointer();
                        if (!isNull(orbitsPtr) && savedState.orbitHeights.length >= 3) {
                            for (var i = 0; i < 3; i++) {
                                orbitsPtr.add(0x10 + i * 8).writeFloat(savedState.orbitHeights[i]);
                                orbitsPtr.add(0x14 + i * 8).writeFloat(savedState.orbitRadii[i]);
                            }
                            log('info', '[Restore] 轨道参数已恢复');
                        }

                        // 恢复 Composer 参数
                        var composerIdx = 0;
                        for (var rigIdx = 0; rigIdx < 3; rigIdx++) {
                            var rig = getRig(freeLook, rigIdx, ptr(0));
                            if (isNull(rig)) continue;
                            var pipeline = getComponentPipeline(rig, ptr(0));
                            if (isNull(pipeline)) continue;
                            var pipeLen = pipeline.add(0xC).readU32();
                            for (var ci = 0; ci < pipeLen && ci < 10; ci++) {
                                var comp = pipeline.add(0x10 + ci * PTR_SIZE).readPointer();
                                if (isNull(comp)) continue;

                                // 恢复 Composer
                                try {
                                    if (composerIdx < savedState.composerScreenX.length) {
                                        comp.add(OFF.CC_m_ScreenX).writeFloat(savedState.composerScreenX[composerIdx]);
                                        comp.add(OFF.CC_m_ScreenY).writeFloat(savedState.composerScreenY[composerIdx]);
                                        var tOff = savedState.composerTrackedOffset[composerIdx];
                                        if (tOff) {
                                            comp.add(OFF.CC_m_TrackedObjectOffset).writeFloat(tOff[0]);
                                            comp.add(OFF.CC_m_TrackedObjectOffset + 4).writeFloat(tOff[1]);
                                            comp.add(OFF.CC_m_TrackedObjectOffset + 8).writeFloat(tOff[2]);
                                        }
                                        if (composerIdx < savedState.composerDeadZoneW.length) {
                                            comp.add(OFF.CC_m_DeadZoneWidth).writeFloat(savedState.composerDeadZoneW[composerIdx]);
                                            comp.add(OFF.CC_m_DeadZoneHeight).writeFloat(savedState.composerDeadZoneH[composerIdx]);
                                        }
                                    }
                                } catch(e) {}

                                composerIdx++;
                            }
                        }
                        log('info', '[Restore] Composer 参数已恢复');
                    }
                } catch(e) {
                    errors.push('恢复相机参数失败: ' + e);
                }
            }

            // 重置保存的状态
            savedState.observeMode = -1;
            savedState.pvActiveStates = [];
            savedState.cvActiveStates = [];
            savedState.pvLayerStates = [];
            savedState.cvLayerStates = [];
            savedState.pvRendererStates = [];
            savedState.cvRendererStates = [];
            savedState.playerViewModelVisible = false;
            savedState.followSet = false;
            savedState.lookAtSet = false;
            savedState.orbitHeights = [];
            savedState.orbitRadii = [];
            savedState.composerScreenX = [];
            savedState.composerScreenY = [];
            savedState.composerTrackedOffset = [];
            savedState.composerDeadZoneW = [];
            savedState.composerDeadZoneH = [];

            if (fsm.current === STATE.TP_ENABLED) {
                setState(STATE.ROOM_READY);
            }

            if (errors.length > 0) {
                log('warn', '关闭第三人称有错误: ' + errors.join('; '));
            } else {
                log('info', '第三人称已关闭，所有状态已恢复');
            }
        } catch(e) {
            logError('disable', '关闭第三人称异常: ' + e);
        }
    }

    // ============================================================
    // 主循环
    // ============================================================
    var loopCounter = 0;

    function loop() {
        if (fsm.current !== STATE.TP_ENABLED) return;
        loopCounter++;

        try {
            if (!hasGm()) {
                gm = null;
                cameraManager = null;
                setState(STATE.NO_GAME);
                return;
            }

            var player = findMyPlayer();
            if (!player) return;

            var camMgr = tryGetCameraManager();
            if (!camMgr) return;

            var freeLook = camMgr.add(OFF.CM_freeLookCamera).readPointer();
            if (isNull(freeLook)) return;

            // Phase4: 每帧更新 AimIK 目标点
            // 修复: AimIK 对象取错，暂时关闭
            // try {
            //     var shootRay = calculateShootRay(player);
            //     if (shootRay.valid && shootRay.aimPoint) {
            //         var aimIKResult = setAimIKTarget(player, shootRay.aimPoint);
            //         // 只在首次成功时记录日志
            //         if (aimIKResult.ok && loopCounter === 1) {
            //             log('info', '[AimIK] 目标点设置成功');
            //         }
            //     }
            // } catch(e) {}

            // Phase5: 相机碰撞检测
            // 修复: 暂时关闭相机 SphereCast，避免未验证的 ABI 问题
            // try {
            //     checkCameraCollision(freeLook, player);
            // } catch(e) {}

            // v10: 100ms 间隔，计数器调整
            // 每 500ms 重新激活 FreeLook (5 次)
            if (loopCounter % 5 === 0) {
                try { setFreeLookActive(camMgr, 1, ptr(0)); } catch(e) {}
            }

            // 每 2 秒重新同步武器 (20 次)
            if (loopCounter % 20 === 0) {
                try {
                    var wpns = player.add(OFF.Player_wpns).readPointer();
                    if (!isNull(wpns)) {
                        var inUse = wpns.add(OFF.PW_inUse).readPointer();
                        if (!isNull(inUse)) {
                            synchronizeHand(inUse, ptr(0));
                        }
                    }
                } catch(e) {}
            }

            // 每 5 秒确保 PV 对象仍然隐藏 + PV Renderer 禁用 (50 次)
            if (loopCounter % 50 === 0) {
                try {
                    var character = player.add(OFF.Player_currentCharacter).readPointer();
                    if (!isNull(character)) {
                        // Phase1: 使用 32 位 List 偏移
                        var pvListPtr = character.add(OFF.Model_objectInPV).readPointer();
                        if (!isNull(pvListPtr)) {
                            var pvItems = pvListPtr.add(0x08).readPointer();  // _items (Il2CppArray*)
                            var pvCount = pvListPtr.add(0x0C).readS32();      // _size
                            for (var i = 0; i < pvCount && i < 30; i++) {
                                // 修复: Il2CppArray 元素从 +0x10 开始
                                var goPtr = pvItems.add(0x10 + i * PTR_SIZE).readPointer();
                                if (!isNull(goPtr)) {
                                    try {
                                        if (gameObjectGetActiveSelf(goPtr, ptr(0))) {
                                            gameObjectSetActive(goPtr, 0, ptr(0));  // Phase1: bool -> 0
                                        }
                                    } catch(e) {}
                                }
                            }
                        }

                        // v8: 同时确保 CV 对象仍然显示
                        // Phase1: 使用 32 位 List 偏移
                        var cvListPtr = character.add(OFF.Model_objectInCV).readPointer();
                        if (!isNull(cvListPtr)) {
                            var cvItems = cvListPtr.add(0x08).readPointer();  // _items (Il2CppArray*)
                            var cvCount = cvListPtr.add(0x0C).readS32();      // _size
                            for (var i = 0; i < cvCount && i < 30; i++) {
                                // 修复: Il2CppArray 元素从 +0x10 开始
                                var goPtr = cvItems.add(0x10 + i * PTR_SIZE).readPointer();
                                if (!isNull(goPtr)) {
                                    try {
                                        if (!gameObjectGetActiveSelf(goPtr, ptr(0))) {
                                            gameObjectSetActive(goPtr, 1, ptr(0));  // Phase1: bool -> 1
                                        }
                                    } catch(e) {}
                                }
                            }
                        }
                    }
                } catch(e) {}

                // 确保 playerViewModelVisible 仍然为 false
                try {
                    var playerData = player.add(OFF.Player_playerData).readPointer();
                    if (!isNull(playerData)) {
                        if (playerData.add(OFF.PD_playerViewModelVisible).readU8() !== 0) {
                            playerData.add(OFF.PD_playerViewModelVisible).writeU8(0);
                        }
                    }
                } catch(e) {}
            }
        } catch(e) {
            logError('loop', '主循环异常: ' + e);
        }
    }

    // ============================================================
    // Hook 安装
    // ============================================================
    function installHooks() {
        log('info', '开始安装 Hooks (v8, RVA 已验证)...');

        // Hook 1: CameraManager.Awake
        try {
            Interceptor.attach(base.add(RVA.CameraManager_Awake), {
                onEnter: function(args) {
                    if (!isNull(args[0]) && isReadable(args[0])) {
                        cameraManager = args[0];
                        log('info', 'CameraManager.Awake 捕获: ' + args[0]);
                    }
                }
            });
            log('info', 'Hook 1: CameraManager.Awake (0x' + RVA.CameraManager_Awake.toString(16) + ')');
        } catch(e) { logError('hook1', 'CameraManager.Awake 失败: ' + e); }

        // Hook 2: GameManager.Awake
        try {
            Interceptor.attach(base.add(RVA.GameManager_Awake), {
                onEnter: function(args) {
                    if (!isNull(args[0]) && isReadable(args[0])) {
                        gm = args[0];
                        log('info', 'GameManager.Awake 捕获: ' + args[0]);
                        setState(STATE.WAITING_ROOM);
                    }
                }
            });
            log('info', 'Hook 2: GameManager.Awake (0x' + RVA.GameManager_Awake.toString(16) + ')');
        } catch(e) { logError('hook2', 'GameManager.Awake 失败: ' + e); }

        // Hook 3: GameManager.OnDestroy
        try {
            Interceptor.attach(base.add(RVA.GameManager_OnDestroy), {
                onEnter: function(args) {
                    if (fsm.current === STATE.TP_ENABLED) disableThirdPerson();
                    gm = null;
                    cameraManager = null;
                    setState(STATE.NO_GAME);
                    log('info', 'GameManager.OnDestroy');
                }
            });
            log('info', 'Hook 3: GameManager.OnDestroy');
        } catch(e) { logError('hook3', 'GameManager.OnDestroy 失败: ' + e); }

        // Hook 4: CameraManager.OnDestroy
        try {
            Interceptor.attach(base.add(RVA.CameraManager_OnDestroy), {
                onEnter: function(args) { cameraManager = null; }
            });
            log('info', 'Hook 4: CameraManager.OnDestroy');
        } catch(e) { logError('hook4', 'CameraManager.OnDestroy 失败: ' + e); }

        // Hook 5: NewGameRoundStart
        var roomStartLogged = false;
        try {
            Interceptor.attach(base.add(RVA.GameManager_NewGameRoundStart), {
                onEnter: function(args) {
                    fsm.stats.hookCalls++;
                    if (!roomStartLogged) {
                        roomStartLogged = true;
                        log('info', '房间开始 (NewGameRoundStart)');
                    }
                    setState(STATE.ROOM_READY);
                }
            });
            log('info', 'Hook 5: NewGameRoundStart');
        } catch(e) { logError('hook5', 'NewGameRoundStart 失败: ' + e); }

        // Hook 6: AddPlayer
        try {
            Interceptor.attach(base.add(RVA.GameManager_AddPlayer), {
                onEnter: function(args) {
                    fsm.stats.hookCalls++;
                    if (fsm.current === STATE.WAITING_ROOM || fsm.current === STATE.NO_GAME) {
                        setState(STATE.ROOM_READY);
                    }
                }
            });
            log('info', 'Hook 6: AddPlayer');
        } catch(e) { logError('hook6', 'AddPlayer 失败: ' + e); }

        // Hook 7: SpawnEvent
        try {
            Interceptor.attach(base.add(RVA.CameraManager_SpawnEvent), {
                onEnter: function(args) {
                    fsm.stats.hookCalls++;
                    if (fsm.current === STATE.WAITING_ROOM) setState(STATE.ROOM_READY);
                }
            });
            log('info', 'Hook 7: SpawnEvent');
        } catch(e) { logError('hook7', 'SpawnEvent 失败: ' + e); }

        // Hook 8: ChangePVandCV — 第三人称下阻止视角切换回 PV
        try {
            Interceptor.attach(base.add(RVA.CameraManager_ChangePVandCV), {
                onEnter: function(args) {
                    fsm.stats.hookCalls++;
                    if (fsm.current === STATE.TP_ENABLED) {
                        this._skip = true;
                        this._camMgr = args[0]; // 保存 this 指针
                    }
                },
                onLeave: function(retval) {
                    if (this._skip && !isNull(this._camMgr)) {
                        // ChangePVandCV 执行后，重新激活 FreeLook
                        try {
                            setFreeLookActive(this._camMgr, 1, ptr(0));
                        } catch(e) {}
                    }
                }
            });
            log('info', 'Hook 8: ChangePVandCV (v8: onLeave 重新激活 FreeLook)');
        } catch(e) { logError('hook8', 'ChangePVandCV 失败: ' + e); }

        // Hook 9: CameraRotation
        try {
            Interceptor.attach(base.add(RVA.PlayerController_CameraRotation), {
                onLeave: function(retval) {
                    if (fsm.current !== STATE.TP_ENABLED) return;
                    try {
                        var player = findMyPlayer();
                        if (!player) return;
                        var camMgr = tryGetCameraManager();
                        if (!camMgr) return;
                        var freeLook = camMgr.add(OFF.CM_freeLookCamera).readPointer();
                        if (isNull(freeLook)) return;

                        var camRot = player.add(OFF.Player_cameraRotation);
                        var rotY = camRot.add(4).readFloat();
                        if (!isFinite(rotY)) return;

                        var yAxisValue = 0.5 + (rotY / 178.0);
                        if (yAxisValue < 0.05) yAxisValue = 0.05;
                        if (yAxisValue > 0.95) yAxisValue = 0.95;
                        freeLook.add(OFF.CFL_m_YAxis).writeFloat(yAxisValue);
                    } catch(e) {}
                }
            });
            log('info', 'Hook 9: CameraRotation');
        } catch(e) { logError('hook9', 'CameraRotation 失败: ' + e); }

        log('info', '所有 Hook 安装完成');
    }

    // ============================================================
    // 瞄准诊断系统
    // ============================================================
    var aimDiag = {
        active: false,
        sessionId: '',
        shotId: 0,
        startTime: 0,
        duration: 15,
        intervalId: null,
        logLines: [],      // 缓冲区，最终写入文件
        shootHooksInstalled: false,
        eventHooksInstalled: false,  // Phase6: 事件 Hook 标志
        lastShotData: null, // 最近一次射击数据
    };

    // 读取 Vector3 (3 个 float)
    function readVec3(p) {
        if (isNull(p)) return { x: 0, y: 0, z: 0, valid: false };
        try {
            return {
                x: p.readFloat(),
                y: p.add(4).readFloat(),
                z: p.add(8).readFloat(),
                valid: true
            };
        } catch(e) {
            return { x: 0, y: 0, z: 0, valid: false, error: String(e) };
        }
    }

    // 格式化 Vector3
    function fmtVec3(v) {
        if (!v.valid) return '(invalid)';
        return '(' + v.x.toFixed(4) + ', ' + v.y.toFixed(4) + ', ' + v.z.toFixed(4) + ')';
    }

    // 读取 Quaternion (4 个 float)
    function readQuat(p) {
        if (isNull(p)) return { x: 0, y: 0, z: 0, w: 0, valid: false };
        try {
            return {
                x: p.readFloat(),
                y: p.add(4).readFloat(),
                z: p.add(8).readFloat(),
                w: p.add(12).readFloat(),
                valid: true
            };
        } catch(e) {
            return { x: 0, y: 0, z: 0, w: 0, valid: false, error: String(e) };
        }
    }

    function fmtQuat(q) {
        if (!q.valid) return '(invalid)';
        return '(' + q.x.toFixed(4) + ', ' + q.y.toFixed(4) + ', ' + q.z.toFixed(4) + ', ' + q.w.toFixed(4) + ')';
    }

    // 读取 Ray (origin: Vector3, direction: Vector3, 共 24 字节)
    function readRay(p) {
        if (isNull(p)) return { origin: { x:0,y:0,z:0,valid:false }, direction: { x:0,y:0,z:0,valid:false }, valid: false };
        try {
            return {
                origin: readVec3(p),
                direction: readVec3(p.add(12)),
                valid: true
            };
        } catch(e) {
            return { origin: { x:0,y:0,z:0,valid:false }, direction: { x:0,y:0,z:0,valid:false }, valid: false, error: String(e) };
        }
    }

    function fmtRay(r) {
        if (!r.valid) return 'origin=(invalid) direction=(invalid)';
        return 'origin=' + fmtVec3(r.origin) + ' direction=' + fmtVec3(r.direction);
    }

    // 向量运算
    function vec3Sub(a, b) { return { x: a.x - b.x, y: a.y - b.y, z: a.z - b.z, valid: true }; }
    function vec3Add(a, b) { return { x: a.x + b.x, y: a.y + b.y, z: a.z + b.z, valid: true }; }
    function vec3Scale(a, s) { return { x: a.x * s, y: a.y * s, z: a.z * s, valid: true }; }
    function vec3Length(a) { return Math.sqrt(a.x * a.x + a.y * a.y + a.z * a.z); }
    function vec3Normalize(a) { var l = vec3Length(a); if (l < 0.0001) return { x:0,y:0,z:0,valid:true }; return { x:a.x/l, y:a.y/l, z:a.z/l, valid:true }; }
    function vec3Dot(a, b) { return a.x * b.x + a.y * b.y + a.z * b.z; }
    function angleBetween(a, b) {
        var na = vec3Normalize(a), nb = vec3Normalize(b);
        var d = vec3Dot(na, nb);
        if (d > 1.0) d = 1.0; if (d < -1.0) d = -1.0;
        return Math.acos(d) * 180.0 / Math.PI;
    }

    // 检查 Transform 是否激活（通过 GameObject.activeSelf）
    function isTransformActive(tPtr) {
        if (isNull(tPtr)) return false;
        try {
            // Transform -> Component -> GameObject
            // 需要调用 Component.get_gameObject，但 RVA 未验证
            // 暂时使用简化方法：检查 Transform 的 hierarchyCount 或 childCount
            // 如果 hierarchyCount > 0，说明该节点在场景中是激活的
            var childCount = transformGetChildCount(tPtr, ptr(0));
            // 注意: 这个方法不准确，只是临时方案
            // 真正的激活检查需要 Component.get_gameObject -> GameObject.activeSelf
            return true;  // 暂时假设所有 Transform 都是激活的
        } catch(e) {
            return false;
        }
    }

    // 安全获取 Transform 的 position/forward 等
    // Phase1 修复: _Injected 函数调用顺序为 (this, retBuf, MethodInfo*)
    function safeGetTransformPos(tPtr) {
        if (isNull(tPtr)) return { x:0,y:0,z:0,valid:false,reason:'null_transform' };
        try {
            var retBuf = Memory.alloc(12); // Vector3 = 12 bytes
            transformGetPosition(tPtr, retBuf, ptr(0));  // Phase1: 修正调用顺序 (this, retBuf, MethodInfo*)
            return readVec3(retBuf);
        } catch(e) { return { x:0,y:0,z:0,valid:false,reason:String(e) }; }
    }

    function safeGetTransformForward(tPtr) {
        if (isNull(tPtr)) return { x:0,y:0,z:0,valid:false,reason:'null_transform' };
        try {
            var retBuf = Memory.alloc(12);
            transformGetForward(retBuf, tPtr, ptr(0));
            return readVec3(retBuf);
        } catch(e) { return { x:0,y:0,z:0,valid:false,reason:String(e) }; }
    }

    function safeGetTransformRight(tPtr) {
        if (isNull(tPtr)) return { x:0,y:0,z:0,valid:false,reason:'null_transform' };
        try {
            var retBuf = Memory.alloc(12);
            transformGetRight(retBuf, tPtr, ptr(0));
            return readVec3(retBuf);
        } catch(e) { return { x:0,y:0,z:0,valid:false,reason:String(e) }; }
    }

    function safeGetTransformUp(tPtr) {
        if (isNull(tPtr)) return { x:0,y:0,z:0,valid:false,reason:'null_transform' };
        try {
            var retBuf = Memory.alloc(12);
            transformGetUp(retBuf, tPtr, ptr(0));
            return readVec3(retBuf);
        } catch(e) { return { x:0,y:0,z:0,valid:false,reason:String(e) }; }
    }

    function safeGetTransformRotation(tPtr) {
        if (isNull(tPtr)) return { x:0,y:0,z:0,w:0,valid:false,reason:'null_transform' };
        try {
            var retBuf = Memory.alloc(16); // Quaternion = 16 bytes
            transformGetRotation(tPtr, retBuf, ptr(0));  // Phase1: 修正调用顺序 (this, retBuf, MethodInfo*)
            return readQuat(retBuf);
        } catch(e) { return { x:0,y:0,z:0,w:0,valid:false,reason:String(e) }; }
    }

    // ========================================
    // Phase2: 第三人称枪口定位
    // ========================================

    // 枪口缓存
    var muzzleCache = {
        transform: null,        // 枪口 Transform
        position: null,         // 缓存的位置
        forward: null,          // 缓存的方向
        lastUpdateTime: 0,      // 上次更新时间
        cacheValid: false,      // 缓存是否有效
        weaponPtr: null,        // 当前武器指针（用于检测换枪）
        qvModelPtr: null,       // 当前 QVModel 指针
        selectedSide: null,     // 选择的 left/right
        muzzleName: null,       // 枪口节点名称
    };

    // 清空枪口缓存（换枪、死亡、复活、离开房间时调用）
    function clearMuzzleCache() {
        muzzleCache.transform = null;
        muzzleCache.position = null;
        muzzleCache.forward = null;
        muzzleCache.lastUpdateTime = 0;
        muzzleCache.cacheValid = false;
        muzzleCache.weaponPtr = null;
        muzzleCache.qvModelPtr = null;
        muzzleCache.selectedSide = null;
        muzzleCache.muzzleName = null;
    }

    // 枚举 Transform 子节点，查找枪口候选
    function findMuzzleCandidates(parentTransform, depth, maxDepth, candidates) {
        if (depth > maxDepth || isNull(parentTransform)) return;
        try {
            var childCount = transformGetChildCount(parentTransform, ptr(0));
            for (var i = 0; i < childCount && i < 20; i++) {
                var child = transformGetChild(parentTransform, i, ptr(0));
                if (isNull(child)) continue;

                // 获取名称
                var goPtr = componentGetTransform(child, ptr(0)); // Transform -> GameObject (需要反向)
                // 注意: Transform 是 Component，可以通过 Component.gameObject 获取 GameObject
                // 但这里我们直接使用 Object.get_name
                var namePtr = objectGetName(child, ptr(0));
                var name = readIl2cppString(namePtr);
                var lowerName = name.toLowerCase();

                // 检查是否是枪口候选
                var isCandidate = false;
                var priority = 0;
                if (lowerName.indexOf('muzzle') >= 0) { isCandidate = true; priority = 10; }
                else if (lowerName.indexOf('firepoint') >= 0) { isCandidate = true; priority = 9; }
                else if (lowerName.indexOf('shotpoint') >= 0) { isCandidate = true; priority = 8; }
                else if (lowerName.indexOf('bulletpoint') >= 0) { isCandidate = true; priority = 7; }
                else if (lowerName.indexOf('barrel') >= 0) { isCandidate = true; priority = 6; }
                else if (lowerName.indexOf('fire') >= 0 && lowerName.indexOf('gunfire') < 0) { isCandidate = true; priority = 5; }

                if (isCandidate) {
                    var pos = safeGetTransformPos(child);
                    var fwd = safeGetTransformForward(child);
                    candidates.push({
                        name: name,
                        transform: child,
                        position: pos,
                        forward: fwd,
                        priority: priority,
                        depth: depth
                    });
                }

                // 递归查找
                findMuzzleCandidates(child, depth + 1, maxDepth, candidates);
            }
        } catch(e) {}
    }

    // 从 QVModel.Data 获取枪口
    function getMuzzleFromQVData(qvDataPtr, side) {
        if (isNull(qvDataPtr)) return null;

        var result = {
            modelTransform: null,
            gunFire: null,
            muzzleTransform: null,
            muzzleName: null,
            candidates: []
        };

        try {
            // 读取 Model Transform
            var modelTf = qvDataPtr.add(OFF.QVD_Model).readPointer();
            result.modelTransform = modelTf;

            // 读取 GunFire ParticleSystem
            var gunFire = qvDataPtr.add(OFF.QVD_GunFire).readPointer();
            result.gunFire = gunFire;

            // 修复: 优先使用 GunFire Transform 作为枪口
            if (!isNull(gunFire)) {
                var gunFireTf = componentGetTransform(gunFire, ptr(0));
                if (!isNull(gunFireTf)) {
                    result.muzzleTransform = gunFireTf;
                    result.muzzleName = 'GunFire';
                    result.candidates.push({
                        transform: gunFireTf,
                        name: 'GunFire',
                        priority: 100,  // 最高优先级
                        depth: 0
                    });
                    return result;  // 直接返回，不再枚举子节点
                }
            }

            // 从 Model Transform 枚举子节点查找枪口（备用方案）
            if (!isNull(modelTf)) {
                findMuzzleCandidates(modelTf, 0, 8, result.candidates);

                // 按优先级排序
                result.candidates.sort(function(a, b) {
                    if (a.priority !== b.priority) return b.priority - a.priority;
                    return a.depth - b.depth;
                });

                // 选择最高优先级的候选
                if (result.candidates.length > 0) {
                    result.muzzleTransform = result.candidates[0].transform;
                    result.muzzleName = result.candidates[0].name;
                }
            }
        } catch(e) {}

        return result;
    }

    // 解析第三人称枪口（主函数）
    function resolveThirdPersonMuzzle(player) {
        // 检查缓存是否仍然有效
        var now = Date.now();
        if (muzzleCache.cacheValid && (now - muzzleCache.lastUpdateTime < 1000)) {
            // 检查武器是否变化
            try {
                var wpns = player.add(OFF.Player_wpns).readPointer();
                var inUse = !isNull(wpns) ? wpns.add(OFF.PW_inUse).readPointer() : null;
                // 修复: NativePointer 应使用 equals() 比较，而不是 ===
                if (!isNull(inUse) && !isNull(muzzleCache.weaponPtr) && inUse.equals(muzzleCache.weaponPtr)) {
                    // 武器未变化，返回缓存
                    return muzzleCache;
                }
            } catch(e) {}
        }

        // 清空缓存
        clearMuzzleCache();

        try {
            // 1. 获取 CharacterModel
            var character = player.add(OFF.Player_currentCharacter).readPointer();
            if (isNull(character)) {
                log('info', '[Muzzle] character is null');
                return muzzleCache;
            }

            // 2. 获取 QVModel
            var qvModel = character.add(OFF.CM_bindQvMdl).readPointer();
            if (isNull(qvModel)) {
                log('info', '[Muzzle] bindQvMdl is null');
                return muzzleCache;
            }
            muzzleCache.qvModelPtr = qvModel;

            // 3. 获取当前武器
            var wpns = player.add(OFF.Player_wpns).readPointer();
            var inUse = !isNull(wpns) ? wpns.add(OFF.PW_inUse).readPointer() : null;
            muzzleCache.weaponPtr = inUse;

            // 4. 检查 bindWpn 是否匹配当前武器
            var bindWpn = qvModel.add(OFF.QV_bindWpn).readPointer();
            var weaponMatches = (!isNull(inUse) && inUse.equals(bindWpn));

            // 修复: 如果 bindWpn 不匹配当前武器，返回未找到
            if (!weaponMatches) {
                log('info', '[Muzzle] bindWpn 不匹配当前武器，跳过此 QVModel');
                return muzzleCache;  // 返回空缓存
            }

            // 5. 尝试从 left 和 right 获取枪口
            // 修复: QVModel.left/right 是内联结构体，不是指针
            var leftData = qvModel.add(OFF.QV_left);  // 直接使用地址，不调用 readPointer()
            var rightData = qvModel.add(OFF.QV_right);

            var leftResult = getMuzzleFromQVData(leftData, 'left');
            var rightResult = getMuzzleFromQVData(rightData, 'right');

            // 6. 选择合适的枪口
            // 修复: 检查哪一侧模型实际激活，而不是永远优先选择右侧
            var selectedResult = null;
            var selectedSide = null;

            // 检查 left 和 right 的 modelTransform 是否激活
            var leftActive = leftResult && leftResult.modelTransform && isTransformActive(leftResult.modelTransform);
            var rightActive = rightResult && rightResult.modelTransform && isTransformActive(rightResult.modelTransform);

            // 优先选择激活且有枪口的一侧
            if (rightActive && rightResult.muzzleTransform) {
                selectedResult = rightResult;
                selectedSide = 'right';
            } else if (leftActive && leftResult.muzzleTransform) {
                selectedResult = leftResult;
                selectedSide = 'left';
            } else if (rightResult && rightResult.muzzleTransform) {
                // 如果两侧都不激活，但右侧有枪口，使用右侧（备用）
                selectedResult = rightResult;
                selectedSide = 'right (inactive)';
            } else if (leftResult && leftResult.muzzleTransform) {
                // 如果两侧都不激活，但左侧有枪口，使用左侧（备用）
                selectedResult = leftResult;
                selectedSide = 'left (inactive)';
            }

            if (selectedResult) {
                muzzleCache.transform = selectedResult.muzzleTransform;
                muzzleCache.muzzleName = selectedResult.muzzleName;
                muzzleCache.selectedSide = selectedSide;
                muzzleCache.cacheValid = true;
                muzzleCache.lastUpdateTime = now;

                log('info', '[Muzzle] 找到枪口: side=' + selectedSide + ' name=' + selectedResult.muzzleName +
                    ' candidates=' + selectedResult.candidates.length);
            } else {
                // 修复: 添加 WPN_Gun.gunFire +0x114 回退
                log('info', '[Muzzle] QVModel 未找到枪口，尝试 WPN_Gun.gunFire 回退');
                try {
                    if (!isNull(inUse)) {
                        // WPN_Gun.gunFire 偏移 0x114
                        var wpnGunFire = inUse.add(0x114).readPointer();
                        if (!isNull(wpnGunFire)) {
                            var gunFireTf = componentGetTransform(wpnGunFire, ptr(0));
                            if (!isNull(gunFireTf)) {
                                muzzleCache.transform = gunFireTf;
                                muzzleCache.muzzleName = 'WPN_Gun.gunFire';
                                muzzleCache.selectedSide = 'weapon_fallback';
                                muzzleCache.cacheValid = true;
                                muzzleCache.lastUpdateTime = now;
                                log('info', '[Muzzle] 使用 WPN_Gun.gunFire 作为枪口');
                            }
                        }
                    }
                } catch(e) {
                    log('info', '[Muzzle] WPN_Gun.gunFire 回退失败: ' + e);
                }
            }

        } catch(e) {
            logError('muzzle_resolve', 'resolveThirdPersonMuzzle 失败: ' + e);
        }

        return muzzleCache;
    }

    // 获取枪口位置
    function getMuzzlePosition(player) {
        var cache = resolveThirdPersonMuzzle(player);
        if (!cache.cacheValid || isNull(cache.transform)) {
            return { x:0, y:0, z:0, valid: false, reason: 'no_muzzle' };
        }

        // 每帧更新位置
        var pos = safeGetTransformPos(cache.transform);
        cache.position = pos;
        return pos;
    }

    // 获取枪口方向
    function getMuzzleForward(player) {
        var cache = resolveThirdPersonMuzzle(player);
        if (!cache.cacheValid || isNull(cache.transform)) {
            return { x:0, y:0, z:0, valid: false, reason: 'no_muzzle' };
        }

        // 每帧更新方向
        var fwd = safeGetTransformForward(cache.transform);
        cache.forward = fwd;
        return fwd;
    }

    // ========================================
    // Phase3: 两段式射击 Ray
    // ========================================

    // 计算最终的射击 Ray
    // 返回: { origin: Vector3, direction: Vector3, valid: boolean, reason: string }
    function calculateShootRay(player) {
        var result = { origin: null, direction: null, valid: false, reason: 'unknown' };

        try {
            // 1. 获取实际渲染的 Camera
            var actualCam = getActualCamera();
            if (isNull(actualCam)) {
                result.reason = 'no_camera';
                return result;
            }

            // 2. 获取 Camera Transform
            var camTransform = getCameraTransform(actualCam);
            if (isNull(camTransform)) {
                result.reason = 'no_camera_transform';
                return result;
            }

            // 3. 获取 Camera 位置和方向
            var camPos = safeGetTransformPos(camTransform);
            var camFwd = safeGetTransformForward(camTransform);
            if (!camPos.valid || !camFwd.valid) {
                result.reason = 'camera_pos_or_fwd_invalid';
                return result;
            }

            // 4. 获取屏幕尺寸
            var screenWidth = cameraGetPixelWidth(actualCam, ptr(0));
            var screenHeight = cameraGetPixelHeight(actualCam, ptr(0));
            if (screenWidth <= 0 || screenHeight <= 0) {
                result.reason = 'invalid_screen_size';
                return result;
            }

            // 5. 使用屏幕中心调用 ScreenPointToRay
            var centerX = screenWidth / 2;
            var centerY = screenHeight / 2;
            var cameraRay = callScreenPointToRay(actualCam, centerX, centerY);
            if (!cameraRay.valid) {
                result.reason = 'screenpointtoray_failed';
                return result;
            }

            // 6. 从相机射线 Raycast 获取目标点
            var maxDist = 1000.0;  // 最大距离
            var raycastResult = callPhysicsRaycast(cameraRay, maxDist);  // 修复: 传递完整 Ray 对象

            var aimPoint = null;
            if (raycastResult.hit) {
                aimPoint = raycastResult.point;
            } else {
                // 未命中，使用相机射线远点
                aimPoint = vec3Add(cameraRay.origin, vec3Scale(cameraRay.direction, maxDist));
            }

            // 7. 获取枪口位置
            var muzzlePos = getMuzzlePosition(player);
            if (!muzzlePos.valid) {
                result.reason = 'no_muzzle_position';
                return result;
            }

            // 8. 计算最终方向
            var toTarget = vec3Sub(aimPoint, muzzlePos);
            var finalDirection = vec3Normalize(toTarget);
            if (vec3Length(finalDirection) < 0.1) {
                result.reason = 'direction_too_short';
                return result;
            }

            // 9. 从枪口向目标点再做一次 Raycast，检测近墙遮挡
            var nearWallDist = vec3Length(toTarget);
            // 修复: 构造完整的 Ray 对象
            var muzzleRay = {
                origin: muzzlePos,
                direction: finalDirection,
                valid: true
            };
            var nearWallResult = callPhysicsRaycast(muzzleRay, nearWallDist);

            // 10. 设置最终 Ray
            result.origin = muzzlePos;
            result.direction = finalDirection;
            result.valid = true;
            result.reason = 'ok';
            result.aimPoint = aimPoint;
            result.cameraRay = cameraRay;
            result.nearWallHit = nearWallResult.hit;

            return result;

        } catch(e) {
            result.reason = 'exception: ' + e;
            return result;
        }
    }

    // 写入 Ray 到缓冲区
    function writeRayToBuffer(rayBuf, origin, direction) {
        if (isNull(rayBuf)) return false;
        try {
            // Ray 结构: origin (12 bytes) + direction (12 bytes)
            rayBuf.writeFloat(origin.x);
            rayBuf.add(4).writeFloat(origin.y);
            rayBuf.add(8).writeFloat(origin.z);
            rayBuf.add(12).writeFloat(direction.x);
            rayBuf.add(16).writeFloat(direction.y);
            rayBuf.add(20).writeFloat(direction.z);
            return true;
        } catch(e) {
            return false;
        }
    }

    // ========================================
    // Phase4: 角色和武器视觉瞄准 (AimIK)
    // ========================================

    // 修复: AimIK 对象取错，暂时关闭所有 AimIK 相关代码
    // Player.recoil 是游戏的射击 Recoil (MonoBehaviour)，不是 FinalIK.Recoil
    // FinalIK.Recoil 的 +0x18 才是 AimIK，但 Player.recoil 指向的是另一个类
    // 因此 player.add(0x54).readPointer().add(0x18).readPointer() 是错误的路径

    // 设置 AimIK 目标点 (暂时禁用)
    // function setAimIKTarget(player, aimPoint) {
    //     try {
    //         // 1. 获取 Recoil 组件
    //         var recoil = player.add(OFF.Player_recoil).readPointer();
    //         if (isNull(recoil)) {
    //             return { ok: false, reason: 'no_recoil' };
    //         }
    //
    //         // 2. 获取 AimIK 组件
    //         var aimIK = recoil.add(OFF.Recoil_aimIK).readPointer();
    //         if (isNull(aimIK)) {
    //             return { ok: false, reason: 'no_aimIK' };
    //         }
    //
    //         // 3. 获取 IKSolverAim
    //         var solver = aimIK.add(OFF.AimIK_solver).readPointer();
    //         if (isNull(solver)) {
    //             return { ok: false, reason: 'no_solver' };
    //         }
    //
    //         // 4. 设置 IKPosition (目标点)
    //         solver.add(OFF.IKSolver_IKPosition).writeFloat(aimPoint.x);
    //         solver.add(OFF.IKSolver_IKPosition + 4).writeFloat(aimPoint.y);
    //         solver.add(OFF.IKSolver_IKPosition + 8).writeFloat(aimPoint.z);
    //
    //         // 5. 设置 IKPositionWeight = 1.0
    //         solver.add(OFF.IKSolver_IKPositionWeight).writeFloat(1.0);
    //
    //         return { ok: true, reason: 'ok' };
    //
    //     } catch(e) {
    //         return { ok: false, reason: 'exception: ' + e };
    //     }
    // }

    // 重置 AimIK 权重 (暂时禁用)
    // function resetAimIKWeight(player) {
    //     try {
    //         var recoil = player.add(OFF.Player_recoil).readPointer();
    //         if (isNull(recoil)) return;
    //
    //         var aimIK = recoil.add(OFF.Recoil_aimIK).readPointer();
    //         if (isNull(aimIK)) return;
    //         var solver = aimIK.add(OFF.AimIK_solver).readPointer();
    //         if (isNull(solver)) return;
    //
    //         // 设置 IKPositionWeight = 0.0
    //         solver.add(OFF.IKSolver_IKPositionWeight).writeFloat(0.0);
    //
    //     } catch(e) {}
    // }

    // ========================================
    // Phase5: 相机碰撞检测
    // ========================================

    // 相机碰撞状态
    var cameraCollisionState = {
        lastDistance: 3.0,        // 上次有效距离
        targetDistance: 3.0,      // 目标距离
        currentDistance: 3.0,     // 当前插值距离
        smoothing: 0.15,          // 平滑系数 (0~1, 越小越平滑)
        minDistance: 0.5,         // 最小距离
        collisionLayerMask: 0xFFFFFFFF, // 碰撞层掩码（默认所有层）
    };

    // 检测相机碰撞并调整距离
    function checkCameraCollision(freeLook, player) {
        try {
            // 1. 获取 Follow 目标位置（角色位置）
            var followPtr = freeLook.add(OFF.CFL_m_LookAt).readPointer();
            if (isNull(followPtr)) {
                followPtr = freeLook.add(OFF.CFL_m_Follow).readPointer();
            }
            if (isNull(followPtr)) return;

            var characterPos = safeGetTransformPos(followPtr);
            if (!characterPos.valid) return;

            // 2. 获取实际相机位置
            var actualCam = getActualCamera();
            if (isNull(actualCam)) return;

            var camTransform = getCameraTransform(actualCam);
            if (isNull(camTransform)) return;

            var camPos = safeGetTransformPos(camTransform);
            if (!camPos.valid) return;

            // 3. 计算方向和距离
            var toCam = vec3Sub(camPos, characterPos);
            var currentDist = vec3Length(toCam);
            var direction = vec3Normalize(toCam);

            // 4. 使用 SphereCast 检测碰撞（半径 0.3 米）
            var sphereRadius = 0.3;
            var maxDist = fsm.cameraDistance;
            var raycastResult = callPhysicsSphereCast(
                characterPos,
                sphereRadius,
                direction,
                maxDist
            );

            // 5. 计算目标距离
            var targetDist = maxDist;
            if (raycastResult.hit) {
                // 碰撞，使用碰撞点距离（留一点余量）
                targetDist = Math.max(raycastResult.distance - sphereRadius - 0.1, cameraCollisionState.minDistance);
            }

            // 6. 平滑插值
            cameraCollisionState.targetDistance = targetDist;
            cameraCollisionState.currentDistance = cameraCollisionState.currentDistance +
                (targetDist - cameraCollisionState.currentDistance) * cameraCollisionState.smoothing;

            // 7. 更新 Orbit Radius
            var orbitsPtr = freeLook.add(OFF.CFL_m_Orbits).readPointer();
            if (!isNull(orbitsPtr)) {
                var arrLen = orbitsPtr.add(0xC).readU32();
                if (arrLen >= 3) {
                    var newRadius = cameraCollisionState.currentDistance;
                    // 更新所有轨道的 Radius
                    for (var i = 0; i < 3; i++) {
                        orbitsPtr.add(0x14 + i * 8).writeFloat(newRadius);
                    }
                }
            }

            // 8. 记录日志（仅在有碰撞时）
            if (raycastResult.hit && loopCounter % 30 === 0) {
                log('info', '[CameraCollision] 检测到碰撞，距离: ' + targetDist.toFixed(2) + 'm');
            }

        } catch(e) {
            // 静默失败
        }
    }

    // 获取实际渲染的 Unity Camera
    function getActualCamera() {
        // 方法1: 通过 CinemachineBrain.OutputCamera
        var camMgr = tryGetCameraManager();
        if (!isNull(camMgr)) {
            try {
                var brainPtr = camMgr.add(OFF.CM_brain).readPointer();
                if (!isNull(brainPtr)) {
                    var outCam = brainGetOutputCamera(brainPtr, ptr(0));
                    if (!isNull(outCam)) return outCam;
                }
            } catch(e) {}
        }
        // 方法2: Camera.current
        try {
            var cur = cameraGetCurrent(ptr(0));
            if (!isNull(cur)) return cur;
        } catch(e) {}
        // 方法3: Camera.main
        try {
            var main = cameraGetMain(ptr(0));
            if (!isNull(main)) return main;
        } catch(e) {}
        return null;
    }

    // v9: 安全获取 Camera 的 Transform，使用 Component.get_transform API
    function getCameraTransform(camPtr) {
        if (isNull(camPtr)) return null;
        try {
            return componentGetTransform(camPtr, ptr(0));
        } catch(e) { return null; }
    }

    // 查找枪口 Transform：枚举武器子节点
    var MUZZLE_KEYWORDS = ['muzzle', 'firepoint', 'fire_point', 'fire', 'shotpoint', 'shot_point', 'bulletpoint', 'bullet_point', 'barrel', 'weaponroot', 'weapon_root', 'socket'];
    var MUZZLE_EXACT = ['muzzle', 'firePoint', 'fire_point', 'shotPoint', 'bulletPoint', 'barrelEnd'];

    // v9: 使用经过验证的 Component.get_transform API 获取 Transform
    // 不再使用硬编码偏移 weapon+0x10 -> cachedGo+0x30
    function findMuzzleTransform(weaponPtr) {
        if (isNull(weaponPtr)) return { found: false, reason: 'weapon_null' };
        try {
            // 使用 Component.get_transform (RVA 0x3F2D80) 获取 Transform
            var transformPtr = componentGetTransform(weaponPtr, ptr(0));
            if (isNull(transformPtr)) return { found: false, reason: 'transform_null' };

            // 递归搜索子节点 (深度最多8)
            var candidates = [];
            searchChildrenForMuzzle(transformPtr, '', 0, 8, candidates);

            if (candidates.length === 0) {
                return { found: false, reason: 'no_muzzle_keyword_found', candidates: [] };
            }

            // 优先精确匹配
            for (var i = 0; i < candidates.length; i++) {
                var nameLower = candidates[i].name.toLowerCase();
                for (var j = 0; j < MUZZLE_EXACT.length; j++) {
                    if (nameLower === MUZZLE_EXACT[j]) {
                        return { found: true, transform: candidates[i].transform, name: candidates[i].name, matchType: 'exact' };
                    }
                }
            }

            // 模糊匹配 — 不自动选择第一个，返回所有候选
            return { found: true, transform: candidates[0].transform, name: candidates[0].name, matchType: 'fuzzy', candidates: candidates };
        } catch(e) {
            return { found: false, reason: String(e) };
        }
    }

    function searchChildrenForMuzzle(tPtr, parentName, depth, maxDepth, results) {
        if (depth > maxDepth || isNull(tPtr)) return;
        try {
            var childCount = transformGetChildCount(tPtr, ptr(0));
            for (var i = 0; i < childCount && i < 20; i++) {
                var child = transformGetChild(tPtr, i, ptr(0));
                if (isNull(child)) continue;
                var name = getTransformName(child);
                var nameLower = name.toLowerCase();
                for (var k = 0; k < MUZZLE_KEYWORDS.length; k++) {
                    if (nameLower.indexOf(MUZZLE_KEYWORDS[k]) >= 0) {
                        results.push({ name: name, transform: child });
                        break;
                    }
                }
                searchChildrenForMuzzle(child, name, depth + 1, maxDepth, results);
            }
        } catch(e) {}
    }

    // v9: 使用 Object.get_name (RVA 0x4EA1B0) 获取 Transform 名称
    // Transform 继承自 Component 继承自 Object，所以可以使用 Object.get_name
    function getTransformName(tPtr) {
        if (isNull(tPtr)) return '<null>';
        try {
            var namePtr = objectGetName(tPtr, ptr(0));
            return readIl2cppString(namePtr);
        } catch(e) { return '<name_err>'; }
    }

    // 写入诊断日志行 (v10: 添加限流机制)
    var diagLogCounter = 0;
    var diagLogLastTime = 0;
    var DIAG_LOG_LIMIT = 100;  // 每秒最多 100 行

    function diagLog(line) {
        // v10: 限流，防止日志洪泛
        var now = Date.now();
        if (now - diagLogLastTime > 1000) {
            // 新的一秒，重置计数器
            diagLogCounter = 0;
            diagLogLastTime = now;
        }
        diagLogCounter++;
        if (diagLogCounter > DIAG_LOG_LIMIT) {
            // 超过限制，跳过
            return;
        }

        aimDiag.logLines.push(line);
        // 同时通过 send 发送到 Python
        send({type:'aim_diag', line: line});
    }

    // ---- Unity API 辅助函数 (封装 _Injected 和 x64 ABI 调用) ----
    // Camera.ScreenPointToRay: 使用 _Injected 版本
    // 签名: void(Camera*, Vector2* pos, int eye, Ray* ret, MethodInfo*)
    function callScreenPointToRay(camPtr, pixelX, pixelY) {
        try {
            var posBuf = Memory.alloc(8);  // Vector2 = 8 bytes
            posBuf.writeFloat(pixelX);
            posBuf.add(4).writeFloat(pixelY);
            var rayBuf = Memory.alloc(24); // Ray = 24 bytes (origin + direction)
            cameraScreenPointToRay(camPtr, posBuf, 0, rayBuf, ptr(0));
            return readRay(rayBuf);
        } catch(e) {
            return { origin: {x:0,y:0,z:0,valid:false}, direction: {x:0,y:0,z:0,valid:false}, valid: false, error: String(e) };
        }
    }

    // Camera.WorldToScreenPoint: 使用 _Injected 版本
    // 签名: void(Camera*, Vector3* position, int eye, Vector3* ret, MethodInfo*)
    function callWorldToScreenPoint(camPtr, wx, wy, wz) {
        try {
            var posBuf = Memory.alloc(12); // Vector3 = 12 bytes
            posBuf.writeFloat(wx);
            posBuf.add(4).writeFloat(wy);
            posBuf.add(8).writeFloat(wz);
            var retBuf = Memory.alloc(12);
            cameraWorldToScreenPoint(camPtr, posBuf, 0, retBuf, ptr(0));
            return readVec3(retBuf);
        } catch(e) {
            return { x:0, y:0, z:0, valid: false, error: String(e) };
        }
    }

    // Physics.Raycast: 签名 bool(Ray*, RaycastHit*, float, MethodInfo*)
    // 注意: Ray 在 C# 中是值类型，但 IL2CPP ABI 可能将其作为指针传递
    // TODO: 需要运行时验证 Ray 是内联传递还是指针传递
    function callPhysicsRaycast(rayData, maxDist) {
        try {
            var rayBuf = Memory.alloc(24); // Ray = 24 bytes
            if (rayData.origin && rayData.origin.valid) {
                rayBuf.writeFloat(rayData.origin.x);
                rayBuf.add(4).writeFloat(rayData.origin.y);
                rayBuf.add(8).writeFloat(rayData.origin.z);
            }
            if (rayData.direction && rayData.direction.valid) {
                rayBuf.add(12).writeFloat(rayData.direction.x);
                rayBuf.add(16).writeFloat(rayData.direction.y);
                rayBuf.add(20).writeFloat(rayData.direction.z);
            }
            var hitBuf = Memory.alloc(256); // RaycastHit 结构体
            var hit = physicsRaycast(rayBuf, hitBuf, maxDist, ptr(0));
            if (hit) {
                // 修复: RaycastHit 布局
                // point    +0x00 (12 bytes)
                // normal   +0x0C (12 bytes)
                // faceID   +0x18 (4 bytes)
                // distance +0x1C (4 bytes) <- 修复: 从 0x30 改为 0x1C
                // UV       +0x20 (8 bytes)
                // collider +0x28 (4 bytes)
                return {
                    hit: true,
                    point: readVec3(hitBuf),
                    normal: readVec3(hitBuf.add(12)),
                    distance: (function() { try { return hitBuf.add(0x1C).readFloat(); } catch(e) { return -1; } })(),
                };
            }
            return { hit: false };
        } catch(e) {
            return { hit: false, error: String(e) };
        }
    }

    // Physics.SphereCast: 封装调用
    function callPhysicsSphereCast(origin, radius, direction, maxDist) {
        try {
            // 分配缓冲区
            var originBuf = Memory.alloc(12);  // Vector3
            var dirBuf = Memory.alloc(12);      // Vector3
            var hitBuf = Memory.alloc(256);     // RaycastHit

            // 写入数据
            originBuf.writeFloat(origin.x);
            originBuf.add(4).writeFloat(origin.y);
            originBuf.add(8).writeFloat(origin.z);

            dirBuf.writeFloat(direction.x);
            dirBuf.add(4).writeFloat(direction.y);
            dirBuf.add(8).writeFloat(direction.z);

            // 调用 SphereCast
            var hit = physicsSphereCast(originBuf, radius, dirBuf, hitBuf, maxDist, 0xFFFFFFFF, ptr(0));

            if (hit) {
                return {
                    hit: true,
                    point: readVec3(hitBuf),
                    normal: readVec3(hitBuf.add(12)),
                    distance: (function() { try { return hitBuf.add(0x30).readFloat(); } catch(e) { return -1; } })(),
                };
            }
            return { hit: false, point: null, normal: null, distance: -1 };
        } catch(e) {
            return { hit: false, point: null, normal: null, distance: -1, error: String(e) };
        }
    }

    // Camera 属性读取辅助
    function callCameraGetPixelWidth(camPtr) { return cameraGetPixelWidth(camPtr, ptr(0)); }
    function callCameraGetPixelHeight(camPtr) { return cameraGetPixelHeight(camPtr, ptr(0)); }

    // ---- 静态快照 ----
    function captureStaticSnapshot(tag) {
        var ts = new Date().toISOString();
        diagLog('');
        diagLog('========== STATIC SNAPSHOT [' + tag + '] BEGIN ==========');
        diagLog('sessionId=' + aimDiag.sessionId);
        diagLog('timestamp=' + ts);
        diagLog('tag=' + tag);

        // [Session]
        diagLog('');
        diagLog('[Session]');
        diagLog('sessionId=' + aimDiag.sessionId);
        diagLog('gamePID=' + Process.id);
        diagLog('gameAssemblyBase=' + base);
        diagLog('stateMachineState=' + fsm.current);
        diagLog('thirdPersonEnabled=' + (fsm.current === STATE.TP_ENABLED));
        diagLog('cameraDistance=' + fsm.cameraDistance);
        diagLog('cameraSensitivity=' + fsm.cameraSensitivity);

        // [Pointers]
        diagLog('');
        diagLog('[Pointers]');
        var player = findMyPlayer();
        diagLog('GameManager=' + gm + ' readable=' + isReadable(gm));
        diagLog('CameraManager=' + cameraManager + ' readable=' + isReadable(cameraManager));

        // CinemachineBrain
        var brainPtr = null;
        try {
            var camMgr = tryGetCameraManager();
            if (!isNull(camMgr)) brainPtr = camMgr.add(OFF.CM_brain).readPointer();
        } catch(e) {}
        diagLog('CinemachineBrain=' + brainPtr + ' readable=' + isReadable(brainPtr));

        // FreeLook
        var freeLook = null;
        try {
            var camMgr = tryGetCameraManager();
            if (!isNull(camMgr)) freeLook = camMgr.add(OFF.CM_freeLookCamera).readPointer();
        } catch(e) {}
        diagLog('FreeLook=' + freeLook + ' readable=' + isReadable(freeLook));

        diagLog('localPlayer=' + player + ' readable=' + isReadable(player));

        // PlayerController
        var playerCtrl = null;
        try { if (player) playerCtrl = player.add(0x50).readPointer(); } catch(e) {}
        diagLog('PlayerController=' + playerCtrl + ' readable=' + isReadable(playerCtrl));

        // PlayerCameraManager
        var pcm = null;
        try { if (player) pcm = player.add(OFF.Player_cameraManager).readPointer(); } catch(e) {}
        diagLog('PlayerCameraManager=' + pcm + ' readable=' + isReadable(pcm));

        // CharacterModel
        var character = null;
        try { if (player) character = player.add(OFF.Player_currentCharacter).readPointer(); } catch(e) {}
        diagLog('CharacterModel=' + character + ' readable=' + isReadable(character));

        // CharacterContainer
        var charContainer = null;
        try { if (player) charContainer = player.add(OFF.Player_characterContainer).readPointer(); } catch(e) {}
        diagLog('characterContainer=' + charContainer + ' readable=' + isReadable(charContainer));

        // 骨骼
        var spine = null, spine1 = null, neck = null;
        try {
            if (!isNull(character)) {
                spine = character.add(OFF.CM_spine).readPointer();
                spine1 = character.add(OFF.CM_spine1).readPointer();
                neck = character.add(OFF.CM_neck).readPointer();
            }
        } catch(e) {}
        diagLog('spine=' + spine + ' readable=' + isReadable(spine));
        diagLog('spine1=' + spine1 + ' readable=' + isReadable(spine1));
        diagLog('neck=' + neck + ' readable=' + isReadable(neck));

        // Animators
        var charAnim = null, handAnim = null;
        try {
            if (!isNull(character)) {
                charAnim = character.add(OFF.CM_characterAnimator).readPointer();
                handAnim = character.add(OFF.CM_handAnimator).readPointer();
            }
        } catch(e) {}
        diagLog('characterAnimator=' + charAnim + ' readable=' + isReadable(charAnim));
        diagLog('handAnimator=' + handAnim + ' readable=' + isReadable(handAnim));

        // Weapon
        var weapon = null;
        try {
            if (player) {
                var wpns = player.add(OFF.Player_wpns).readPointer();
                if (!isNull(wpns)) weapon = wpns.add(OFF.PW_inUse).readPointer();
            }
        } catch(e) {}
        diagLog('currentWeapon=' + weapon + ' readable=' + isReadable(weapon));

        // Phase2: 使用新的枪口定位函数
        var muzzleInfo = null;
        if (player) {
            muzzleInfo = resolveThirdPersonMuzzle(player);
            diagLog('[Muzzle]');
            diagLog('muzzleCacheValid=' + muzzleInfo.cacheValid);
            diagLog('muzzleTransform=' + muzzleInfo.transform + ' readable=' + isReadable(muzzleInfo.transform));
            diagLog('muzzleName=' + (muzzleInfo.muzzleName || 'null'));
            diagLog('muzzleSelectedSide=' + (muzzleInfo.selectedSide || 'null'));
            diagLog('muzzleWeaponPtr=' + muzzleInfo.weaponPtr);
            diagLog('muzzleQVModelPtr=' + muzzleInfo.qvModelPtr);

            if (muzzleInfo.cacheValid && !isNull(muzzleInfo.transform)) {
                var muzzlePos = safeGetTransformPos(muzzleInfo.transform);
                var muzzleFwd = safeGetTransformForward(muzzleInfo.transform);
                diagLog('muzzle.position=' + fmtVec3(muzzlePos));
                diagLog('muzzle.forward=' + fmtVec3(muzzleFwd));
            }
        }

        // [Camera Data]
        diagLog('');
        diagLog('[CameraData]');
        var actualCam = getActualCamera();
        diagLog('actualCamera=' + actualCam + ' readable=' + isReadable(actualCam));

        if (!isNull(actualCam)) {
            try {
                // v9: 使用 Component.get_transform API 获取 Camera Transform
                var camTransform = getCameraTransform(actualCam);
                if (!isNull(camTransform)) {
                    var camPos = safeGetTransformPos(camTransform);
                    var camFwd = safeGetTransformForward(camTransform);
                    var camRight = safeGetTransformRight(camTransform);
                    var camUp = safeGetTransformUp(camTransform);
                    var camRot = safeGetTransformRotation(camTransform);

                    diagLog('actualCamera.position=' + fmtVec3(camPos));
                    diagLog('actualCamera.rotation=' + fmtQuat(camRot));
                    diagLog('actualCamera.forward=' + fmtVec3(camFwd));
                    diagLog('actualCamera.right=' + fmtVec3(camRight));
                    diagLog('actualCamera.up=' + fmtVec3(camUp));
                }

                // Camera 属性 (所有方法需要 MethodInfo* 参数)
                try {
                    var fov = cameraGetFieldOfView(actualCam, ptr(0));
                    var pw = cameraGetPixelWidth(actualCam, ptr(0));
                    var ph = cameraGetPixelHeight(actualCam, ptr(0));
                    var asp = cameraGetAspect(actualCam, ptr(0));
                    diagLog('actualCamera.fieldOfView=' + fov.toFixed(4));
                    diagLog('actualCamera.pixelWidth=' + pw);
                    diagLog('actualCamera.pixelHeight=' + ph);
                    diagLog('actualCamera.aspect=' + asp.toFixed(4));
                    diagLog('screen.width=' + pw + ' screen.height=' + ph);
                } catch(e) {
                    diagLog('camera_properties_error=' + e);
                }
            } catch(e) {
                diagLog('actualCamera_read_error=' + e);
            }
        }

        // FreeLook 参数
        if (!isNull(freeLook)) {
            try {
                var followPtr = freeLook.add(OFF.CFL_m_Follow).readPointer();
                var lookAtPtr = freeLook.add(OFF.CFL_m_LookAt).readPointer();
                diagLog('freeLook.follow=' + followPtr);
                diagLog('freeLook.lookAt=' + lookAtPtr);

                if (!isNull(followPtr)) {
                    var followPos = safeGetTransformPos(followPtr);
                    diagLog('freeLook.follow.position=' + fmtVec3(followPos));
                }
                if (!isNull(lookAtPtr)) {
                    var lookAtPos = safeGetTransformPos(lookAtPtr);
                    diagLog('freeLook.lookAt.position=' + fmtVec3(lookAtPos));
                }

                var yAxis = freeLook.add(OFF.CFL_m_YAxis).readFloat();
                var xAxis = freeLook.add(OFF.CFL_m_XAxis).readFloat();
                diagLog('freeLook.yAxis=' + yAxis.toFixed(4));
                diagLog('freeLook.xAxis=' + xAxis.toFixed(4));

                // Orbits
                var orbitsPtr = freeLook.add(OFF.CFL_m_Orbits).readPointer();
                if (!isNull(orbitsPtr)) {
                    for (var i = 0; i < 3; i++) {
                        var h = orbitsPtr.add(0x10 + i * 8).readFloat();
                        var r = orbitsPtr.add(0x14 + i * 8).readFloat();
                        diagLog('orbit[' + i + '].height=' + h.toFixed(4) + ' radius=' + r.toFixed(4));
                    }
                }

                // Rig Composer 参数
                for (var rigIdx = 0; rigIdx < 3; rigIdx++) {
                    var rig = getRig(freeLook, rigIdx, ptr(0));
                    if (isNull(rig)) continue;
                    var pipeline = getComponentPipeline(rig, ptr(0));
                    if (isNull(pipeline)) continue;
                    var pipeLen = pipeline.add(0xC).readU32();
                    for (var ci = 0; ci < pipeLen && ci < 10; ci++) {
                        var comp = pipeline.add(0x10 + ci * PTR_SIZE).readPointer();
                        if (isNull(comp)) continue;
                        try {
                            var sx = comp.add(OFF.CC_m_ScreenX).readFloat();
                            var sy = comp.add(OFF.CC_m_ScreenY).readFloat();
                            if (sx < -1 || sx > 2 || sy < -1 || sy > 2) continue;
                            diagLog('rig[' + rigIdx + '].composer.screenX=' + sx.toFixed(4));
                            diagLog('rig[' + rigIdx + '].composer.screenY=' + sy.toFixed(4));
                            var tx = comp.add(OFF.CC_m_TrackedObjectOffset).readFloat();
                            var ty = comp.add(OFF.CC_m_TrackedObjectOffset + 4).readFloat();
                            var tz = comp.add(OFF.CC_m_TrackedObjectOffset + 8).readFloat();
                            diagLog('rig[' + rigIdx + '].composer.trackedObjectOffset=(' + tx.toFixed(4) + ',' + ty.toFixed(4) + ',' + tz.toFixed(4) + ')');
                            var dzw = comp.add(OFF.CC_m_DeadZoneWidth).readFloat();
                            var dzh = comp.add(OFF.CC_m_DeadZoneHeight).readFloat();
                            diagLog('rig[' + rigIdx + '].composer.deadZone=(' + dzw.toFixed(4) + ',' + dzh.toFixed(4) + ')');
                        } catch(e) {}
                    }
                }

                // 相机与角色距离
                if (!isNull(actualCam) && !isNull(charContainer)) {
                    try {
                        var camT = getCameraTransform(actualCam);
                        var camP = safeGetTransformPos(camT);
                        var charP = safeGetTransformPos(charContainer);
                        if (camP.valid && charP.valid) {
                            var diff = vec3Sub(camP, charP);
                            var dist = vec3Length(diff);
                            diagLog('cameraToCharacter.distance=' + dist.toFixed(4));
                            diagLog('cameraToCharacter.localOffset=' + fmtVec3(diff));
                        }
                    } catch(e) {}
                }
            } catch(e) {
                diagLog('freeLook_read_error=' + e);
            }
        }

        // [Crosshair Ray]
        diagLog('');
        diagLog('[CrosshairRay]');
        if (!isNull(actualCam)) {
            try {
                var pw2 = callCameraGetPixelWidth(actualCam);
                var ph2 = callCameraGetPixelHeight(actualCam);
                var cx = pw2 / 2.0;
                var cy = ph2 / 2.0;
                diagLog('crosshair.pixelX=' + cx.toFixed(4));
                diagLog('crosshair.pixelY=' + cy.toFixed(4));

                // ScreenPointToRay (使用 _Injected 版本)
                var crosshairRay = callScreenPointToRay(actualCam, cx, cy);
                if (crosshairRay.valid) {
                    diagLog('cameraRay.origin=' + fmtVec3(crosshairRay.origin));
                    diagLog('cameraRay.direction=' + fmtVec3(crosshairRay.direction));

                    // Physics.Raycast
                    try {
                        var rayHit = callPhysicsRaycast(crosshairRay, 1000.0);
                        diagLog('cameraRay.hit=' + rayHit.hit);
                        if (rayHit.hit) {
                            diagLog('cameraRay.hitPoint=' + fmtVec3(rayHit.point));
                            diagLog('cameraRay.hitNormal=' + fmtVec3(rayHit.normal));
                            try { diagLog('cameraRay.hitDistance=' + rayHit.distance.toFixed(4)); } catch(e) {}
                        }
                    } catch(e) {
                        diagLog('cameraRay.raycast_error=' + e);
                    }
                } else {
                    diagLog('cameraRay=FAILED_TO_COMPUTE' + (crosshairRay.error ? ' error=' + crosshairRay.error : ''));
                }
            } catch(e) {
                diagLog('crosshair_error=' + e);
            }
        }

        // [Weapon & Muzzle]
        diagLog('');
        diagLog('[WeaponMuzzle]');
        if (!isNull(weapon)) {
            try {
                var wpnName = getGameObjectName(weapon.add(0x10).readPointer());
                diagLog('weapon.name=' + wpnName);

                // weaponRoot — v9: 使用 Component.get_transform API
                var wpnTransform = componentGetTransform(weapon, ptr(0));
                if (!isNull(wpnTransform)) {
                    var wpnPos = safeGetTransformPos(wpnTransform);
                    var wpnFwd = safeGetTransformForward(wpnTransform);
                    var wpnRot = safeGetTransformRotation(wpnTransform);
                    diagLog('weaponRoot.position=' + fmtVec3(wpnPos));
                    diagLog('weaponRoot.rotation=' + fmtQuat(wpnRot));
                    diagLog('weaponRoot.forward=' + fmtVec3(wpnFwd));

                    // Parent
                    try {
                        var parent = transformGetParent(wpnTransform, ptr(0));
                        if (!isNull(parent)) {
                            var parentName = getTransformName(parent);
                            diagLog('weaponRoot.parent=' + parentName);
                        }
                    } catch(e) {}
                }
            } catch(e) {
                diagLog('weapon_read_error=' + e);
            }
        }

        // Muzzle 数据
        if (muzzleResult.found) {
            var mPos = safeGetTransformPos(muzzleResult.transform);
            var mFwd = safeGetTransformForward(muzzleResult.transform);
            var mRot = safeGetTransformRotation(muzzleResult.transform);
            diagLog('muzzle.name=' + muzzleResult.name);
            diagLog('muzzle.position=' + fmtVec3(mPos));
            diagLog('muzzle.rotation=' + fmtQuat(mRot));
            diagLog('muzzle.forward=' + fmtVec3(mFwd));

            try {
                var mParent = transformGetParent(muzzleResult.transform, ptr(0));
                if (!isNull(mParent)) {
                    diagLog('muzzle.parent=' + getTransformName(mParent));
                }
            } catch(e) {}
        } else {
            diagLog('muzzle=NOT_FOUND');
            // v9: 使用 logWeaponTree 输出完整武器树
            if (!isNull(weapon)) {
                try {
                    logWeaponTree(weapon);
                } catch(e) {
                    diagLog('weapon_children_error=' + e);
                }
            }
        }

        // [Skeleton]
        diagLog('');
        diagLog('[Skeleton]');
        try {
            if (!isNull(spine)) {
                diagLog('spine.position=' + fmtVec3(safeGetTransformPos(spine)));
                diagLog('spine.forward=' + fmtVec3(safeGetTransformForward(spine)));
            }
            if (!isNull(spine1)) {
                diagLog('spine1.position=' + fmtVec3(safeGetTransformPos(spine1)));
                diagLog('spine1.forward=' + fmtVec3(safeGetTransformForward(spine1)));
            }
            if (!isNull(neck)) {
                diagLog('neck.position=' + fmtVec3(safeGetTransformPos(neck)));
                diagLog('neck.forward=' + fmtVec3(safeGetTransformForward(neck)));
            }
            if (!isNull(charContainer)) {
                diagLog('characterRoot.position=' + fmtVec3(safeGetTransformPos(charContainer)));
                diagLog('characterRoot.forward=' + fmtVec3(safeGetTransformForward(charContainer)));
            }
        } catch(e) {
            diagLog('skeleton_error=' + e);
        }

        // [Animator State]
        diagLog('');
        diagLog('[AnimatorState]');
        try {
            // 读取 Player.cameraRotation
            if (player) {
                try {
                    var camRotX = player.add(OFF.Player_cameraRotation).readFloat();
                    var camRotY = player.add(OFF.Player_cameraRotation + 4).readFloat();
                    diagLog('player.cameraRotation.x=' + camRotX.toFixed(4));
                    diagLog('player.cameraRotation.y=' + camRotY.toFixed(4));
                } catch(e) {
                    diagLog('player.cameraRotation_error=' + e);
                }
            }
            // 读取角色根节点 rotation
            if (!isNull(charContainer)) {
                var rootRot = safeGetTransformRotation(charContainer);
                diagLog('characterRoot.rotation=' + fmtQuat(rootRot));
                diagLog('characterRoot.forward=' + fmtVec3(safeGetTransformForward(charContainer)));
            }
            // 读取 handAnimator 和 characterAnimator 的基本信息
            if (!isNull(character)) {
                try {
                    var handAnim = character.add(OFF.CM_handAnimator).readPointer();
                    var charAnim = character.add(OFF.CM_characterAnimator).readPointer();
                    diagLog('handAnimator=' + handAnim + ' readable=' + isReadable(handAnim));
                    diagLog('characterAnimator=' + charAnim + ' readable=' + isReadable(charAnim));
                    // 尝试读取 Animator 的参数 (如果可读)
                    if (!isNull(charAnim)) {
                        try {
                            // Il2CppObject.klass 在 offset 0x0
                            var klass = charAnim.readPointer();
                            if (!isNull(klass)) {
                                // klass.name 在 offset 0x10 (const char*)
                                var namePtr = klass.add(0x10).readPointer();
                                if (!isNull(namePtr)) {
                                    diagLog('characterAnimator.klassName=' + namePtr.readUtf8String());
                                }
                            }
                        } catch(e2) {
                            diagLog('characterAnimator.klass_error=' + e2);
                        }
                    }
                } catch(e) {
                    diagLog('animator_read_error=' + e);
                }
            }
        } catch(e) {
            diagLog('animator_state_error=' + e);
        }

        // [Screen Projection Error]
        diagLog('');
        diagLog('[ScreenProjection]');
        if (!isNull(actualCam) && muzzleResult.found) {
            try {
                var mPos2 = safeGetTransformPos(muzzleResult.transform);
                var mFwd2 = safeGetTransformForward(muzzleResult.transform);
                var pw3 = callCameraGetPixelWidth(actualCam);
                var ph3 = callCameraGetPixelHeight(actualCam);
                var cx2 = pw3 / 2.0;
                var cy2 = ph3 / 2.0;

                // 投影各点
                var points = [
                    { label: 'muzzle.position', v: mPos2 },
                    { label: 'muzzle.position+muzzle.forward*10', v: vec3Add(mPos2, vec3Scale(mFwd2, 10)) },
                    { label: 'muzzle.position+muzzle.forward*100', v: vec3Add(mPos2, vec3Scale(mFwd2, 100)) },
                ];

                // 如果有准星射线命中点，添加 desiredDirection 投影
                var crosshairRay2 = callScreenPointToRay(actualCam, cx2, cy2);
                var rayHit2 = null;
                if (crosshairRay2 && crosshairRay2.valid) {
                    rayHit2 = callPhysicsRaycast(crosshairRay2, 1000.0);
                    if (rayHit2 && rayHit2.hit) {
                        points.push({ label: 'cameraRay.hitPoint', v: rayHit2.point });
                        // desiredDirection: 从枪口到命中点
                        if (mPos2.valid) {
                            var desiredDir = vec3Normalize(vec3Sub(rayHit2.point, mPos2));
                            points.push({ label: 'muzzle.position+desiredDirection*10', v: vec3Add(mPos2, vec3Scale(desiredDir, 10)) });
                            points.push({ label: 'muzzle.position+desiredDirection*100', v: vec3Add(mPos2, vec3Scale(desiredDir, 100)) });
                        }
                    }
                }

                for (var pi = 0; pi < points.length; pi++) {
                    var pt = points[pi];
                    if (!pt.v.valid) continue;
                    try {
                        var screenPt = callWorldToScreenPoint(actualCam, pt.v.x, pt.v.y, pt.v.z);
                        if (screenPt.valid) {
                            var sx = screenPt.x;
                            var sy = screenPt.y;
                            var sz = screenPt.z;
                            var dx = sx - cx2;
                            var dy = sy - cy2;
                            var errPx = Math.sqrt(dx * dx + dy * dy);
                            diagLog(pt.label + '.screen=(' + sx.toFixed(1) + ',' + sy.toFixed(1) + ',' + sz.toFixed(4) + ') dx=' + dx.toFixed(1) + ' dy=' + dy.toFixed(1) + ' errorPixels=' + errPx.toFixed(1));
                        }
                    } catch(e) {
                        diagLog(pt.label + '.screen_error=' + e);
                    }
                }
            } catch(e) {
                diagLog('screen_projection_error=' + e);
            }
        }

        // [PV/CV 异常检查]
        diagLog('');
        diagLog('[PV_CV_Anomaly]');
        if (!isNull(character)) {
            try {
                var pvListPtr = character.add(OFF.Model_objectInPV).readPointer();
                var cvListPtr = character.add(OFF.Model_objectInCV).readPointer();
                var pvCount = 0, cvCount = 0;
                if (!isNull(pvListPtr)) {
                    pvCount = pvListPtr.add(0x18).readU32();
                }
                if (!isNull(cvListPtr)) {
                    cvCount = cvListPtr.add(0x18).readU32();
                }
                diagLog('objectInPV.count=' + pvCount);
                diagLog('objectInCV.count=' + cvCount);

                if (pvCount === 0) {
                    diagLog('ANOMALY: objectInPV is empty! Checking if character is really Model base...');
                    // 检查 0x34/0x38 是否真的是 List
                    try {
                        var pvFieldPtr = character.add(OFF.Model_objectInPV).readPointer();
                        diagLog('character+0x34=' + pvFieldPtr + ' readable=' + isReadable(pvFieldPtr));
                        if (!isNull(pvFieldPtr)) {
                            // List 布局: 0x0 = klass, 0x8 = monitor, 0x10 = _items, 0x18 = _size, 0x1C = _version
                            var klassPtr = pvFieldPtr.readPointer();
                            diagLog('PV_list.klass=' + klassPtr);
                        }
                    } catch(e) {
                        diagLog('PV_list_inspect_error=' + e);
                    }
                }
                if (cvCount === 0) {
                    diagLog('ANOMALY: objectInCV is empty!');
                }
            } catch(e) {
                diagLog('pv_cv_anomaly_error=' + e);
            }
        }

        // PlayerCameraManager.set_modelVisible 检查
        diagLog('');
        diagLog('[PCM_Anomaly]');
        try {
            if (!isNull(pcm)) {
                diagLog('PlayerCameraManager=' + pcm);
                // 尝试调用 set_modelVisible 并捕获异常
                try {
                    setModelVisible(pcm, 1, ptr(0));  // Phase1: bool -> 1
                    diagLog('set_modelVisible(true)=OK');
                    setModelVisible(pcm, 0, ptr(0));  // Phase1: bool -> 0
                    diagLog('set_modelVisible(false)=OK');
                    // 恢复
                    if (fsm.current === STATE.TP_ENABLED) {
                        setModelVisible(pcm, 0, ptr(0));  // Phase1: bool -> 0
                    } else {
                        setModelVisible(pcm, 1, ptr(0));  // Phase1: bool -> 1
                    }
                } catch(e) {
                    diagLog('set_modelVisible_ERROR=' + e);
                }
            }
        } catch(e) {
            diagLog('pcm_anomaly_error=' + e);
        }

        diagLog('========== STATIC SNAPSHOT [' + tag + '] END ==========');
        diagLog('');
    }

    // v9: 完整的武器 Transform 树枚举，输出所有节点信息
    function enumerateWeaponTree(weaponPtr) {
        var nodes = [];
        if (isNull(weaponPtr)) return nodes;
        try {
            var transformPtr = componentGetTransform(weaponPtr, ptr(0));
            if (isNull(transformPtr)) return nodes;
            _enumTransformNode(transformPtr, null, 0, 8, nodes);
        } catch(e) {
            diagLog('enumerateWeaponTree_error=' + e);
        }
        return nodes;
    }

    function _enumTransformNode(tPtr, parentPtr, depth, maxDepth, results) {
        if (depth > maxDepth || isNull(tPtr)) return;
        try {
            var name = getTransformName(tPtr);
            var pos = safeGetTransformPos(tPtr);
            var fwd = safeGetTransformForward(tPtr);
            var nameLower = name.toLowerCase();

            // 标记关键词候选
            var isCandidate = false;
            var candidateKeyword = '';
            var candidateKeywords = ['muzzle', 'firepoint', 'fire_point', 'shotpoint', 'shot_point',
                'bulletpoint', 'bullet_point', 'barrel', 'barrelend', 'fire'];
            for (var ck = 0; ck < candidateKeywords.length; ck++) {
                if (nameLower.indexOf(candidateKeywords[ck]) >= 0) {
                    isCandidate = true;
                    candidateKeyword = candidateKeywords[ck];
                    break;
                }
            }

            results.push({
                name: name,
                transform: tPtr,
                parent: parentPtr,
                depth: depth,
                position: pos,
                forward: fwd,
                isMuzzleCandidate: isCandidate,
                candidateKeyword: candidateKeyword
            });

            // 递归子节点
            var childCount = transformGetChildCount(tPtr, ptr(0));
            for (var i = 0; i < childCount && i < 20; i++) {
                var child = transformGetChild(tPtr, i, ptr(0));
                if (!isNull(child)) {
                    _enumTransformNode(child, tPtr, depth + 1, maxDepth, results);
                }
            }
        } catch(e) {}
    }

    // v9: 诊断日志输出武器树
    function logWeaponTree(weaponPtr) {
        var nodes = enumerateWeaponTree(weaponPtr);
        diagLog('[WeaponTree] total_nodes=' + nodes.length);
        for (var i = 0; i < nodes.length; i++) {
            var n = nodes[i];
            var indent = '';
            for (var d = 0; d < n.depth; d++) indent += '  ';
            var candidateTag = n.isMuzzleCandidate ? ' *** MUZZLE_CANDIDATE(' + n.candidateKeyword + ') ***' : '';
            diagLog(indent + n.name + ' pos=' + fmtVec3(n.position) + ' fwd=' + fmtVec3(n.forward) + candidateTag);
        }
        return nodes;
    }

    function enumerateChildren(tPtr, prefix, depth, maxDepth) {
        if (depth > maxDepth || isNull(tPtr)) return;
        try {
            var count = transformGetChildCount(tPtr, ptr(0));
            for (var i = 0; i < count && i < 15; i++) {
                var child = transformGetChild(tPtr, i, ptr(0));
                if (isNull(child)) continue;
                var name = getTransformName(child);
                diagLog(prefix + '[' + i + '] ' + name);
                enumerateChildren(child, prefix + '  ', depth + 1, maxDepth);
            }
        } catch(e) {}
    }

    // ---- 射击快照 ----
    function captureShotSnapshot(hookName, thisPtr, inputRay, tag) {
        aimDiag.shotId++;
        var sid = aimDiag.shotId;
        var ts = new Date().toISOString();

        diagLog('');
        diagLog('========== SHOT ' + String(sid).padStart(4, '0') + ' BEGIN ==========');
        diagLog('sessionId=' + aimDiag.sessionId);
        diagLog('shotId=' + sid);
        diagLog('timestamp=' + ts);
        diagLog('hookName=' + hookName);
        diagLog('thisPtr=' + thisPtr);
        diagLog('tag=' + tag);

        // 实际相机
        var actualCam = getActualCamera();
        if (!isNull(actualCam)) {
            try {
                var camT = getCameraTransform(actualCam);
                diagLog('actualCamera.position=' + fmtVec3(safeGetTransformPos(camT)));
                diagLog('actualCamera.forward=' + fmtVec3(safeGetTransformForward(camT)));
            } catch(e) {}
        }

        // 准星射线 (使用 _Injected 版本)
        var cRay = null;
        var rayHitResult = null;
        if (!isNull(actualCam)) {
            try {
                var pw = callCameraGetPixelWidth(actualCam);
                var ph = callCameraGetPixelHeight(actualCam);
                diagLog('crosshair=(' + (pw / 2.0).toFixed(1) + ',' + (ph / 2.0).toFixed(1) + ')');
                cRay = callScreenPointToRay(actualCam, pw / 2.0, ph / 2.0);
                if (cRay && cRay.valid) {
                    diagLog('cameraRay.origin=' + fmtVec3(cRay.origin));
                    diagLog('cameraRay.direction=' + fmtVec3(cRay.direction));

                    // Raycast
                    try {
                        rayHitResult = callPhysicsRaycast(cRay, 1000.0);
                        if (rayHitResult.hit) {
                            diagLog('cameraRay.hitPoint=' + fmtVec3(rayHitResult.point));
                        }
                    } catch(e) {}
                }
            } catch(e) {}
        }

        // 武器和枪口
        var player = findMyPlayer();
        var weapon = null;
        try {
            if (player) {
                var wpns = player.add(OFF.Player_wpns).readPointer();
                if (!isNull(wpns)) weapon = wpns.add(OFF.PW_inUse).readPointer();
            }
        } catch(e) {}
        diagLog('weapon=' + weapon);

        var muzzleResult = findMuzzleTransform(weapon);
        if (muzzleResult.found) {
            var mPos = safeGetTransformPos(muzzleResult.transform);
            var mFwd = safeGetTransformForward(muzzleResult.transform);
            diagLog('muzzle.position=' + fmtVec3(mPos));
            diagLog('muzzle.forward=' + fmtVec3(mFwd));

            // desiredDirection
            if (!isNull(actualCam) && cRay && cRay.valid) {
                try {
                    if (rayHitResult && rayHitResult.hit && mPos.valid) {
                        var hitPt = rayHitResult.point;
                        var desired = vec3Sub(hitPt, mPos);
                        var desiredNorm = vec3Normalize(desired);
                        diagLog('desiredDirection=' + fmtVec3(desiredNorm));

                        var angleMuzzleTarget = angleBetween(mFwd, desiredNorm);
                        diagLog('angle.muzzle_to_target=' + angleMuzzleTarget.toFixed(4) + ' degrees');

                        var distMuzzleToTarget = vec3Length(desired);
                        diagLog('distance.muzzle_to_target=' + distMuzzleToTarget.toFixed(4));
                    }

                    // 输入 Ray 与 cameraRay 的夹角
                    if (inputRay && inputRay.valid && cRay.valid) {
                        var angleInputCam = angleBetween(inputRay.direction, cRay.direction);
                        diagLog('angle.shootRay_to_cameraRay=' + angleInputCam.toFixed(4) + ' degrees');

                        var angleInputMuzzle = angleBetween(inputRay.direction, mFwd);
                        diagLog('angle.shootRay_to_muzzleForward=' + angleInputMuzzle.toFixed(4) + ' degrees');

                        // 输入 Ray 起点到 muzzle 的距离
                        if (inputRay.origin.valid && mPos.valid) {
                            var distInputToMuzzle = vec3Length(vec3Sub(inputRay.origin, mPos));
                            diagLog('distance.shootRayOrigin_to_muzzle=' + distInputToMuzzle.toFixed(4));
                        }
                    }
                } catch(e) {
                    diagLog('desired_direction_error=' + e);
                }
            }

            // 屏幕投影误差
            if (!isNull(actualCam) && mPos.valid) {
                try {
                    var pw3 = callCameraGetPixelWidth(actualCam);
                    var ph3 = callCameraGetPixelHeight(actualCam);
                    var cx = pw3 / 2.0;
                    var cy = ph3 / 2.0;

                    // muzzle forward 投影
                    var mFwdEnd = vec3Add(mPos, vec3Scale(mFwd, 100));
                    var screenMuzzleFwd = callWorldToScreenPoint(actualCam, mFwdEnd.x, mFwdEnd.y, mFwdEnd.z);
                    if (screenMuzzleFwd.valid) {
                        var sx = screenMuzzleFwd.x;
                        var sy = screenMuzzleFwd.y;
                        var dx = sx - cx;
                        var dy = sy - cy;
                        diagLog('errorPixels.muzzleForward100=(' + sx.toFixed(1) + ',' + sy.toFixed(1) + ') dx=' + dx.toFixed(1) + ' dy=' + dy.toFixed(1) + ' error=' + Math.sqrt(dx*dx+dy*dy).toFixed(1));
                    }
                } catch(e) {}
            }
        } else {
            diagLog('muzzle=NOT_FOUND');
        }

        // 输入 Ray
        if (inputRay && inputRay.valid) {
            diagLog('inputRay.origin=' + fmtVec3(inputRay.origin));
            diagLog('inputRay.direction=' + fmtVec3(inputRay.direction));
        }

        diagLog('========== SHOT ' + String(sid).padStart(4, '0') + ' END ==========');
        diagLog('');
    }

    // ---- 射击观察 Hook (v10: 简化回调逻辑，减少阻塞) ----
    function installShootHooks() {
        if (aimDiag.shootHooksInstalled) return;
        aimDiag.shootHooksInstalled = true;

        // Hook: Recoil.GetShootRay — RVA 0xB195C0
        // Phase3: 修改射击 Ray，实现两段式射击
        try {
            var hookAddr = base.add(RVA.Recoil_GetShootRay);
            log('info', '[AimDiag] Hook: Recoil.GetShootRay RVA=0x' + RVA.Recoil_GetShootRay.toString(16));

            Interceptor.attach(hookAddr, {
                onEnter: function(args) {
                    this._retBuf = args[0];
                    this._thisPtr = args[1];  // Recoil* this
                    this._shouldModify = (fsm.current === STATE.TP_ENABLED);
                    this._player = findMyPlayer();

                    // 修复: 只允许本地玩家的 Recoil
                    if (this._shouldModify && this._player) {
                        try {
                            var localRecoil = this._player.add(OFF.Player_recoil).readPointer();
                            if (isNull(localRecoil) || !this._thisPtr.equals(localRecoil)) {
                                // 不是本地玩家的 Recoil，不修改
                                this._shouldModify = false;
                            }
                        } catch(e) {
                            this._shouldModify = false;
                        }
                    }
                },
                onLeave: function(retval) {
                    // Phase1: 先读取原始 Ray（在修改前）
                    var originalRay = null;
                    if (!isNull(this._retBuf)) {
                        try {
                            originalRay = readRay(this._retBuf);
                        } catch(e) {}
                    }

                    // Phase3: 在第三人称模式下修改射击 Ray
                    var finalRay = originalRay;
                    if (this._shouldModify && !isNull(this._retBuf) && this._player) {
                        try {
                            var shootRay = calculateShootRay(this._player);
                            if (shootRay.valid) {
                                // 写入新的 Ray 到返回缓冲区
                                if (writeRayToBuffer(this._retBuf, shootRay.origin, shootRay.direction)) {
                                    finalRay = { origin: shootRay.origin, direction: shootRay.direction, valid: true };
                                    log('info', '[ShootRay] 已修改射击 Ray: origin=' + fmtVec3(shootRay.origin) + ' dir=' + fmtVec3(shootRay.direction));
                                }
                            } else {
                                log('info', '[ShootRay] 计算失败: ' + shootRay.reason + '，保留原始 Ray');
                            }
                        } catch(e) {
                            logError('shoot_ray', '修改射击 Ray 失败: ' + e);
                        }
                    }

                    // 诊断日志（仅在诊断模式下）
                    if (!aimDiag.active) return;
                    try {
                        // 输出原始 Ray 和最终 Ray
                        if (originalRay && originalRay.valid) {
                            diagLog('[GetShootRay] originalRay.origin=' + fmtVec3(originalRay.origin));
                            diagLog('[GetShootRay] originalRay.direction=' + fmtVec3(originalRay.direction));
                        }
                        if (finalRay && finalRay.valid) {
                            diagLog('[GetShootRay] finalRay.origin=' + fmtVec3(finalRay.origin));
                            diagLog('[GetShootRay] finalRay.direction=' + fmtVec3(finalRay.direction));
                        }

                        // 保存到 lastShotData
                        if (finalRay && finalRay.valid) {
                            aimDiag.lastShotData = { originalRay: originalRay, finalRay: finalRay, hook: 'GetShootRay', thisPtr: String(this._thisPtr) };
                            // Phase1: 保存必要变量，避免异步回调中 this 丢失
                            var thisPtr = this._thisPtr;
                            var rayData = finalRay;
                            // v10: 使用 setTimeout 异步处理快照，避免阻塞游戏线程
                            setTimeout(function() {
                                captureShotSnapshot('GetShootRay', thisPtr, rayData, 'auto');
                            }, 0);
                        }
                    } catch(e) {
                        // 静默失败，不阻塞游戏
                    }
                }
            });
            log('info', '[AimDiag] Hook: Recoil.GetShootRay installed (Phase3: 两段式射击)');
        } catch(e) {
            logError('aim_hook_gsr', 'GetShootRay Hook 失败: ' + e);
        }

        // Hook: WPN_Gun.GunShoot — RVA 0xB624C0
        try {
            var hookAddr2 = base.add(RVA.WPN_Gun_GunShoot);
            log('info', '[AimDiag] Hook: WPN_Gun.GunShoot RVA=0x' + RVA.WPN_Gun_GunShoot.toString(16));

            Interceptor.attach(hookAddr2, {
                onEnter: function(args) {
                    if (!aimDiag.active) return;
                    this._thisPtr = args[0];
                },
                onLeave: function(retval) {
                    if (!aimDiag.active) return;
                    // v10: 简化，只记录射击事件
                    diagLog('[GunShoot] this=' + this._thisPtr);
                }
            });
            log('info', '[AimDiag] Hook: WPN_Gun.GunShoot installed');
        } catch(e) {
            logError('aim_hook_gs', 'GunShoot Hook 失败: ' + e);
        }

        // Hook: WPN_Gun.GunShoot_Logic — RVA 0xB62170
        try {
            var hookAddr3 = base.add(RVA.WPN_Gun_GunShoot_Logic);
            log('info', '[AimDiag] Hook: WPN_Gun.GunShoot_Logic RVA=0x' + RVA.WPN_Gun_GunShoot_Logic.toString(16));

            Interceptor.attach(hookAddr3, {
                onEnter: function(args) {
                    if (!aimDiag.active) return;
                    this._thisPtr = args[0];
                },
                onLeave: function(retval) {
                    if (!aimDiag.active) return;
                    diagLog('[GunShoot_Logic] this=' + this._thisPtr);
                }
            });
            log('info', '[AimDiag] Hook: WPN_Gun.GunShoot_Logic installed');
        } catch(e) {
            logError('aim_hook_gsl', 'GunShoot_Logic Hook 失败: ' + e);
        }

        // Hook: WPN_Gun.Damage — RVA 0xB613D0
        // v10: 简化 Ray 读取逻辑
        try {
            var hookAddr4 = base.add(RVA.WPN_Gun_Damage);
            log('info', '[AimDiag] Hook: WPN_Gun.Damage RVA=0x' + RVA.WPN_Gun_Damage.toString(16));

            Interceptor.attach(hookAddr4, {
                onEnter: function(args) {
                    if (!aimDiag.active) return;
                    this._thisPtr = args[0];

                    // v10: 简化 Ray 读取，只尝试一种方法
                    try {
                        var esp = this.context.esp;
                        if (esp) {
                            var rayAddr = esp.add(8);
                            var ray = readRay(rayAddr);
                            if (ray.valid) {
                                // Phase1: 输出 Damage 接收到的 Ray
                                diagLog('[Damage] receivedRay.origin=' + fmtVec3(ray.origin));
                                diagLog('[Damage] receivedRay.direction=' + fmtVec3(ray.direction));

                                // 检查与 GetShootRay 的最终 Ray 是否一致
                                if (aimDiag.lastShotData && aimDiag.lastShotData.finalRay) {
                                    var finalRay = aimDiag.lastShotData.finalRay;
                                    var originDiff = vec3Length(vec3Sub(ray.origin, finalRay.origin));
                                    var directionDiff = angleBetween(ray.direction, finalRay.direction);
                                    diagLog('[Damage] compare.originDiff=' + originDiff.toFixed(4));
                                    diagLog('[Damage] compare.directionDiff=' + directionDiff.toFixed(4) + ' degrees');

                                    if (originDiff < 0.01 && directionDiff < 0.1) {
                                        diagLog('[Damage] ✓ Ray 一致');
                                    } else {
                                        diagLog('[Damage] ✗ Ray 不一致');
                                    }
                                }

                                // Phase1: 保存局部变量，避免 setTimeout 回调中访问 this
                                var thisPtr = this._thisPtr;
                                var rayData = ray;
                                aimDiag.lastShotData = { ray: rayData, hook: 'Damage', thisPtr: String(thisPtr) };
                                setTimeout(function() {
                                    captureShotSnapshot('Damage', thisPtr, rayData, 'auto');
                                }, 0);
                            }
                        }
                    } catch(e) {
                        // 静默失败
                    }
                }
            });
            log('info', '[AimDiag] Hook: WPN_Gun.Damage installed');
        } catch(e) {
            logError('aim_hook_dmg', 'Damage Hook 失败: ' + e);
        }
    }

    // ---- Phase6: 事件处理 Hook ----
    function installEventHooks() {
        if (aimDiag.eventHooksInstalled) return;
        aimDiag.eventHooksInstalled = true;

        // Hook: Player.OnEntityDeath — RVA 0xB51210
        try {
            var hookAddr = base.add(RVA.Player_OnEntityDeath);
            log('info', '[EventHook] Hook: Player.OnEntityDeath RVA=0x' + RVA.Player_OnEntityDeath.toString(16));

            Interceptor.attach(hookAddr, {
                onEnter: function(args) {
                    this._player = args[0];
                },
                onLeave: function(retval) {
                    // 清空枪口缓存
                    clearMuzzleCache();
                    // 重置 AimIK 权重
                    // 修复: AimIK 对象取错，暂时关闭
                    // try {
                    //     resetAimIKWeight(this._player);
                    // } catch(e) {}
                    log('info', '[EventHook] Player.OnEntityDeath: 已清空缓存');
                }
            });
            log('info', '[EventHook] Player.OnEntityDeath installed');
        } catch(e) {
            logError('event_hook_death', 'OnEntityDeath Hook 失败: ' + e);
        }

        // Hook: Player.SetWeapon — RVA 0xB53650
        try {
            var hookAddr = base.add(RVA.Player_SetWeapon);
            log('info', '[EventHook] Hook: Player.SetWeapon RVA=0x' + RVA.Player_SetWeapon.toString(16));

            Interceptor.attach(hookAddr, {
                onEnter: function(args) {
                    this._player = args[0];
                },
                onLeave: function(retval) {
                    // 清空枪口缓存
                    clearMuzzleCache();
                    log('info', '[EventHook] Player.SetWeapon: 已清空缓存');
                }
            });
            log('info', '[EventHook] Player.SetWeapon installed');
        } catch(e) {
            logError('event_hook_weapon', 'SetWeapon Hook 失败: ' + e);
        }

        // Hook: Player.Respawn — RVA 0xB527A0
        try {
            var hookAddr = base.add(RVA.Player_Respawn);
            log('info', '[EventHook] Hook: Player.Respawn RVA=0x' + RVA.Player_Respawn.toString(16));

            Interceptor.attach(hookAddr, {
                onEnter: function(args) {
                    this._player = args[0];
                },
                onLeave: function(retval) {
                    // 清空枪口缓存
                    clearMuzzleCache();
                    log('info', '[EventHook] Player.Respawn: 已清空缓存');
                }
            });
            log('info', '[EventHook] Player.Respawn installed');
        } catch(e) {
            logError('event_hook_respawn', 'Respawn Hook 失败: ' + e);
        }

        // Hook: Player.Spawn — RVA 0xB53760
        try {
            var hookAddr = base.add(RVA.Player_Spawn);
            log('info', '[EventHook] Hook: Player.Spawn RVA=0x' + RVA.Player_Spawn.toString(16));

            Interceptor.attach(hookAddr, {
                onEnter: function(args) {
                    this._player = args[0];
                },
                onLeave: function(retval) {
                    // 清空枪口缓存
                    clearMuzzleCache();
                    log('info', '[EventHook] Player.Spawn: 已清空缓存');
                }
            });
            log('info', '[EventHook] Player.Spawn installed');
        } catch(e) {
            logError('event_hook_spawn', 'Spawn Hook 失败: ' + e);
        }
    }

    // ---- 动态采集定时器 ----
    function startDynamicCapture(intervalMs) {
        if (aimDiag.intervalId) clearInterval(aimDiag.intervalId);
        var captureCount = 0;
        aimDiag.intervalId = setInterval(function() {
            if (!aimDiag.active) {
                clearInterval(aimDiag.intervalId);
                aimDiag.intervalId = null;
                return;
            }
            captureCount++;
            var elapsed = Date.now() - aimDiag.startTime;
            if (elapsed >= aimDiag.duration * 1000) {
                stopAimDiagnostic();
                return;
            }
            // 动态快照（精简版，只记录关键变化）
            diagLog('[Dynamic #' + captureCount + ' t=' + (elapsed / 1000).toFixed(1) + 's]');

            var actualCam = getActualCamera();
            if (!isNull(actualCam)) {
                try {
                    var camT = getCameraTransform(actualCam);
                    diagLog('  camera.pos=' + fmtVec3(safeGetTransformPos(camT)));
                    diagLog('  camera.fwd=' + fmtVec3(safeGetTransformForward(camT)));
                } catch(e) {}
            }

            // Player cameraRotation
            var player = findMyPlayer();
            if (player) {
                try {
                    var camRot = player.add(OFF.Player_cameraRotation);
                    var rotX = camRot.readFloat();
                    var rotY = camRot.add(4).readFloat();
                    diagLog('  player.cameraRotation=(' + rotX.toFixed(4) + ',' + rotY.toFixed(4) + ')');
                } catch(e) {}
            }

            // FreeLook YAxis/XAxis
            var camMgr = tryGetCameraManager();
            if (!isNull(camMgr)) {
                try {
                    var fl = camMgr.add(OFF.CM_freeLookCamera).readPointer();
                    if (!isNull(fl)) {
                        diagLog('  freeLook.yAxis=' + fl.add(OFF.CFL_m_YAxis).readFloat().toFixed(4) +
                            ' xAxis=' + fl.add(OFF.CFL_m_XAxis).readFloat().toFixed(4));
                    }
                } catch(e) {}
            }

            // Muzzle position/forward
            if (player) {
                try {
                    var wpns = player.add(OFF.Player_wpns).readPointer();
                    if (!isNull(wpns)) {
                        var weapon = wpns.add(OFF.PW_inUse).readPointer();
                        var muzzleResult = findMuzzleTransform(weapon);
                        if (muzzleResult.found) {
                            diagLog('  muzzle.pos=' + fmtVec3(safeGetTransformPos(muzzleResult.transform)));
                            diagLog('  muzzle.fwd=' + fmtVec3(safeGetTransformForward(muzzleResult.transform)));
                        }
                    }
                } catch(e) {}
            }
        }, intervalMs);
    }

    // ---- 诊断控制函数 ----
    // ---- 启动瞄准诊断 ----
    // 测试步骤 (请依次完成):
    //   A. 站在空旷处，不开枪，水平和垂直转动视角
    //   B. 距离平整墙壁约 2 米，准星对准固定点，单发 3 次
    //   C. 距离墙壁约 10 米，单发 3 次
    //   D. 距离墙壁约 30 米，单发 3 次
    //   E. 角色贴墙，枪口靠近墙体，单发 3 次
    //   F. 待机、开火、换弹时分别调用 captureaimsnapshot('idle'/'fire'/'reload')
    //   G. 切换一次武器后再射击
    function startAimDiagnostic(durationSeconds) {
        if (aimDiag.active) {
            return { ok: false, error: '诊断已在进行中, sessionId=' + aimDiag.sessionId };
        }

        // v9: 诊断启动条件检查
        if (fsm.current !== STATE.TP_ENABLED) {
            return { ok: false, error: '诊断条件未就绪: 状态机不是TP_ENABLED (当前=' + fsm.current + ')' };
        }
        var camMgr = tryGetCameraManager();
        if (isNull(camMgr)) {
            return { ok: false, error: '诊断条件未就绪: CameraManager无效' };
        }
        var player = findMyPlayer();
        if (!player) {
            return { ok: false, error: '诊断条件未就绪: 本地Player无效' };
        }
        var actualCam = getActualCamera();
        if (isNull(actualCam)) {
            return { ok: false, error: '诊断条件未就绪: 实际Camera无效' };
        }
        var wpns = null, weapon = null;
        try {
            wpns = player.add(OFF.Player_wpns).readPointer();
            if (!isNull(wpns)) weapon = wpns.add(OFF.PW_inUse).readPointer();
        } catch(e) {}
        if (isNull(weapon)) {
            return { ok: false, error: '诊断条件未就绪: 当前Weapon无效' };
        }

        aimDiag.active = true;
        aimDiag.sessionId = 'aim_' + Date.now().toString(36);
        aimDiag.shotId = 0;
        aimDiag.startTime = Date.now();
        aimDiag.duration = durationSeconds || 15;
        aimDiag.logLines = [];
        aimDiag.lastShotData = null;

        // 安装射击 Hook
        installShootHooks();

        // 初始静态快照
        captureStaticSnapshot('start');

        // 启动动态采集 (200ms)
        startDynamicCapture(200);

        log('info', '[AimDiag] 瞄准诊断已启动: sessionId=' + aimDiag.sessionId + ' duration=' + aimDiag.duration + 's');
        return { ok: true, sessionId: aimDiag.sessionId, duration: aimDiag.duration };
    }

    function stopAimDiagnostic() {
        if (!aimDiag.active) {
            return { ok: false, error: '诊断未在运行' };
        }

        aimDiag.active = false;

        // 停止定时器
        if (aimDiag.intervalId) {
            clearInterval(aimDiag.intervalId);
            aimDiag.intervalId = null;
        }

        // 结束标记
        var elapsed = Date.now() - aimDiag.startTime;
        diagLog('');
        diagLog('========== DIAGNOSTIC SESSION END ==========');
        diagLog('sessionId=' + aimDiag.sessionId);
        diagLog('duration=' + (elapsed / 1000).toFixed(1) + 's');
        diagLog('totalShots=' + aimDiag.shotId);
        diagLog('totalLines=' + aimDiag.logLines.length);
        diagLog('========== END ==========');

        // 将日志发送到 Python 写入文件
        send({type:'aim_diag_complete', sessionId: aimDiag.sessionId, lines: aimDiag.logLines, shotCount: aimDiag.shotId});

        log('info', '[AimDiag] 瞄准诊断已停止: shots=' + aimDiag.shotId + ' lines=' + aimDiag.logLines.length);
        return { ok: true, sessionId: aimDiag.sessionId, shotCount: aimDiag.shotId, lineCount: aimDiag.logLines.length };
    }

    function captureAimSnapshot(tag) {
        if (!aimDiag.active) {
            return { ok: false, error: '诊断未在运行' };
        }
        captureStaticSnapshot(tag || 'manual');
        return { ok: true, tag: tag };
    }

    // ============================================================
    // RPC 接口
    // ============================================================
    rpc.exports = {
        installhook: function() {
            if (enabled) return { ok: true };
            try {
                installHooks();
                installEventHooks();  // Phase6: 在 installhook 时安装事件 Hook
                installShootHooks();  // 修复: 在 installhook 时安装射击 Hook，而不是只在诊断时安装
                timer = setInterval(loop, 100);  // v10: 50ms -> 100ms，减少主循环频率
                enabled = true;
                log('info', '修改器 v10 已启动');
                return { ok: true };
            } catch(e) {
                logError('install', 'installhook 异常: ' + e);
                return { ok: false, error: String(e) };
            }
        },

        enable: function() {
            return enableThirdPerson();
        },

        disable: function() {
            disableThirdPerson();
            return { ok: true, enabled: false, error: '' };
        },

        cleanup: function() {
            // 清理资源（用于脚本卸载前）
            log('info', '[Cleanup] 开始清理资源...');

            // 1. 清理主循环定时器
            if (timer) {
                clearInterval(timer);
                timer = null;
                log('info', '[Cleanup] 主循环定时器已清理');
            }

            // 2. 清理诊断定时器
            if (aimDiag.intervalId) {
                clearInterval(aimDiag.intervalId);
                aimDiag.intervalId = null;
                log('info', '[Cleanup] 诊断定时器已清理');
            }

            // 3. 禁用第三人称（如果启用）
            if (fsm.current === STATE.TP_ENABLED) {
                try {
                    disableThirdPerson();
                    log('info', '[Cleanup] 第三人称已禁用');
                } catch(e) {
                    logError('cleanup', '禁用第三人称失败: ' + e);
                }
            }

            // 4. Detach 所有 Hook
            try {
                Interceptor.detachAll();
                log('info', '[Cleanup] 所有 Hook 已 detach');
            } catch(e) {
                logError('cleanup', 'Detach Hook 失败: ' + e);
            }

            // 5. 清空枪口缓存
            clearMuzzleCache();

            log('info', '[Cleanup] 资源清理完成');
            return { ok: true };
        },

        toggle: function() {
            if (fsm.current === STATE.TP_ENABLED) {
                return rpc.exports.disable();
            } else {
                return rpc.exports.enable();
            }
        },

        setdistance: function(dist) {
            if (!isFinite(dist) || dist < 1.0 || dist > 8.0) {
                return { ok: false, error: '距离范围 1.0-8.0' };
            }
            fsm.cameraDistance = dist;
            if (fsm.current === STATE.TP_ENABLED) {
                try {
                    var camMgr = tryGetCameraManager();
                    if (camMgr) {
                        var freeLook = camMgr.add(OFF.CM_freeLookCamera).readPointer();
                        if (!isNull(freeLook)) {
                            // 更新轨道半径
                            var orbitsPtr = freeLook.add(OFF.CFL_m_Orbits).readPointer();
                            if (!isNull(orbitsPtr)) {
                                orbitsPtr.add(0x14).writeFloat(dist);
                                orbitsPtr.add(0x1C).writeFloat(dist);
                                orbitsPtr.add(0x24).writeFloat(dist * 0.85);
                            }
                        }
                    }
                } catch(e) {
                    logError('set_dist', '更新距离失败: ' + e);
                }
            }
            return { ok: true, distance: dist };
        },

        setsensitivity: function(s) {
            if (!isFinite(s) || s < 0.2 || s > 3.0) {
                return { ok: false, error: '灵敏度范围 0.2-3.0' };
            }
            fsm.cameraSensitivity = s;
            return { ok: true, sensitivity: s, note: '灵敏度暂未生效' };
        },

        getstatus: function() {
            return {
                state: fsm.current,
                enabled: fsm.current === STATE.TP_ENABLED,
                distance: fsm.cameraDistance,
                sensitivity: fsm.cameraSensitivity,
                haveGM: hasGm(),
                haveCameraManager: !isNull(tryGetCameraManager()),
                lastError: fsm.lastError,
                stats: fsm.stats,
            };
        },

        resetall: function() {
            disableThirdPerson();
            fsm.cameraDistance = 3.0;
            fsm.cameraSensitivity = 1.0;
            return { ok: true };
        },

        // v8 增强：诊断 RPC，输出模型详细信息
        debugmodel: function() {            var result = {
                player: null, character: null, playerData: null,
                pvCount: 0, cvCount: 0, pvItems: [], cvItems: [],
                weapon: null, sockets: [], freeLookRigs: [],
                observeMode: -1, playerViewModelVisible: null,
                playerCameraManager: null
            };

            try {
                var player = findMyPlayer();
                if (!player) {
                    log('info', '[诊断] 未找到本地玩家');
                    return { ok: false, error: '未找到本地玩家' };
                }
                result.player = String(player);

                var character = player.add(OFF.Player_currentCharacter).readPointer();
                result.character = isNull(character) ? null : String(character);

                // PlayerData 信息
                try {
                    var playerData = player.add(OFF.Player_playerData).readPointer();
                    if (!isNull(playerData)) {
                        result.playerData = String(playerData);
                        result.observeMode = getObserveMode(playerData, ptr(0));
                        result.playerViewModelVisible = playerData.add(OFF.PD_playerViewModelVisible).readU8() !== 0;
                        log('info', '[诊断] PlayerData: observeMode=' + result.observeMode +
                            ' playerViewModelVisible=' + result.playerViewModelVisible);
                    }
                } catch(e) {
                    logError('diag_pd', '读取 PlayerData 失败: ' + e);
                }

                // PlayerCameraManager 信息
                try {
                    var pcm = player.add(OFF.Player_cameraManager).readPointer();
                    if (!isNull(pcm)) {
                        result.playerCameraManager = String(pcm);
                        var modelCam = pcm.add(OFF.PCM_modelCamera).readPointer();
                        var modelCont = pcm.add(OFF.PCM_modelContainer).readPointer();
                        log('info', '[诊断] PlayerCameraManager: ' + pcm +
                            ' modelCamera=' + modelCam + ' modelContainer=' + modelCont);
                    }
                } catch(e) {}

                if (!isNull(character)) {
                    // PV 对象列表
                    var pvListPtr = character.add(OFF.Model_objectInPV).readPointer();
                    var pvResult = readGameObjectList(pvListPtr, 'objectInPV');
                    result.pvCount = pvResult.count;
                    result.pvItems = pvResult.items;

                    // CV 对象列表
                    var cvListPtr = character.add(OFF.Model_objectInCV).readPointer();
                    var cvResult = readGameObjectList(cvListPtr, 'objectInCV');
                    result.cvCount = cvResult.count;
                    result.cvItems = cvResult.items;

                    // Sockets (List<Model.Socket> — Socket 是值类型 struct，0x20 字节)
                    try {
                        var socketsPtr = character.add(OFF.Model_sockets).readPointer();
                        if (!isNull(socketsPtr)) {
                            var sockItems = socketsPtr.add(0x10).readPointer();
                            var sockCount = socketsPtr.add(0x18).readU32();
                            log('info', '[诊断] Sockets 数量: ' + sockCount);
                            for (var i = 0; i < sockCount && i < 20; i++) {
                                // Socket 是 struct，直接在数组中按值存储，每个 0x20 字节
                                var sockBase = sockItems.add(i * 0x20);
                                var sockNamePtr = sockBase.add(OFF.MS_name).readPointer();
                                var sockName = readIl2cppString(sockNamePtr);
                                var sockNode = sockBase.add(OFF.MS_node).readPointer();
                                log('info', '[诊断]   Socket[' + i + '] name=' + sockName + ' node=' + sockNode);
                                result.sockets.push({ name: sockName, node: String(sockNode) });
                            }
                        }
                    } catch(e) {
                        logError('diag_sockets', '读取 Sockets 失败: ' + e);
                    }

                    // 当前武器
                    try {
                        var wpns = player.add(OFF.Player_wpns).readPointer();
                        if (!isNull(wpns)) {
                            var inUse = wpns.add(OFF.PW_inUse).readPointer();
                            result.weapon = isNull(inUse) ? null : String(inUse);
                            log('info', '[诊断] 当前武器 inUse: ' + result.weapon);

                            // 武器详情
                            if (!isNull(inUse)) {
                                try {
                                    var wpnData = inUse.add(0x68).readPointer();
                                    log('info', '[诊断]   Weapon.data: ' + wpnData);
                                } catch(e) {}
                            }
                        }
                    } catch(e) {
                        logError('diag_weapon', '获取武器失败: ' + e);
                    }

                    // CharacterModel 字段
                    try {
                        var charAnim = character.add(OFF.CM_characterAnimator).readPointer();
                        var handAnim = character.add(OFF.CM_handAnimator).readPointer();
                        var cvRend = character.add(OFF.CM_cvRenderers).readPointer();
                        log('info', '[诊断] CharacterModel: characterAnimator=' + charAnim +
                            ' handAnimator=' + handAnim + ' cvRenderers=' + cvRend);
                    } catch(e) {}

                    // socketItemsName (string[] — Il2Cpp 数组，不是 List)
                    try {
                        var sockItemsNamePtr = character.add(OFF.CM_socketItemsName).readPointer();
                        if (!isNull(sockItemsNamePtr)) {
                            // Il2CppArray 布局 (32位): 0x0C = max_length, 0x10 = data[0]
                            var sinCount = sockItemsNamePtr.add(0xC).readU32();
                            log('info', '[诊断] socketItemsName 数量: ' + sinCount);
                            for (var i = 0; i < sinCount && i < 10; i++) {
                                // 32位: 指针大小 4 字节
                                var namePtr = sockItemsNamePtr.add(0x10 + i * PTR_SIZE).readPointer();
                                var name = readIl2cppString(namePtr);
                                log('info', '[诊断]   socketItemsName[' + i + '] = ' + name);
                            }
                        }
                    } catch(e) {}
                }

                // FreeLook Rig 信息
                var camMgr = tryGetCameraManager();
                if (camMgr) {
                    var freeLook = camMgr.add(OFF.CM_freeLookCamera).readPointer();
                    if (!isNull(freeLook)) {
                        // 轨道信息
                        try {
                            var orbitsPtr = freeLook.add(OFF.CFL_m_Orbits).readPointer();
                            if (!isNull(orbitsPtr)) {
                                var arrLen = orbitsPtr.add(0xC).readU32();
                                for (var i = 0; i < arrLen && i < 3; i++) {
                                    var h = orbitsPtr.add(0x10 + i * 8).readFloat();
                                    var r = orbitsPtr.add(0x14 + i * 8).readFloat();
                                    log('info', '[诊断] Orbit[' + i + '] Height=' + h.toFixed(2) + ' Radius=' + r.toFixed(2));
                                }
                            }
                        } catch(e) {}

                        // YAxis/XAxis
                        try {
                            var yAxis = freeLook.add(OFF.CFL_m_YAxis).readFloat();
                            var xAxis = freeLook.add(OFF.CFL_m_XAxis).readFloat();
                            log('info', '[诊断] YAxis=' + yAxis.toFixed(3) + ' XAxis=' + xAxis.toFixed(3));
                        } catch(e) {}

                        for (var rigIdx = 0; rigIdx < 3; rigIdx++) {
                            var rig = getRig(freeLook, rigIdx, ptr(0));
                            if (isNull(rig)) continue;
                            var rigInfo = { index: rigIdx, components: [] };
                            var pipeline = getComponentPipeline(rig, ptr(0));
                            if (isNull(pipeline)) continue;
                            var pipeLen = pipeline.add(0xC).readU32();
                            for (var ci = 0; ci < pipeLen && ci < 10; ci++) {
                                var comp = pipeline.add(0x10 + ci * PTR_SIZE).readPointer();
                                if (isNull(comp)) continue;
                                var compInfo = { address: String(comp) };

                                // 尝试读取 Composer 参数
                                try {
                                    var sx = comp.add(OFF.CC_m_ScreenX).readFloat();
                                    var sy = comp.add(OFF.CC_m_ScreenY).readFloat();
                                    if (sx >= -1 && sx <= 2 && sy >= -1 && sy <= 2) {
                                        compInfo.type = 'Composer';
                                        compInfo.screenX = sx;
                                        compInfo.screenY = sy;
                                        compInfo.trackedOffset = [
                                            comp.add(OFF.CC_m_TrackedObjectOffset).readFloat(),
                                            comp.add(OFF.CC_m_TrackedObjectOffset + 4).readFloat(),
                                            comp.add(OFF.CC_m_TrackedObjectOffset + 8).readFloat()
                                        ];
                                        compInfo.deadZone = [
                                            comp.add(OFF.CC_m_DeadZoneWidth).readFloat(),
                                            comp.add(OFF.CC_m_DeadZoneHeight).readFloat()
                                        ];
                                    }
                                } catch(e) {}

                                // 尝试读取 Transposer 参数
                                if (!compInfo.type) {
                                    try {
                                        compInfo.type = 'Transposer';
                                        compInfo.followOffset = [
                                            comp.add(OFF.CT_m_FollowOffset).readFloat(),
                                            comp.add(OFF.CT_m_FollowOffset + 4).readFloat(),
                                            comp.add(OFF.CT_m_FollowOffset + 8).readFloat()
                                        ];
                                    } catch(e) {}
                                }

                                rigInfo.components.push(compInfo);
                            }
                            result.freeLookRigs.push(rigInfo);
                            log('info', '[诊断] Rig' + rigIdx + ': ' + JSON.stringify(rigInfo.components));
                        }
                    }
                }
            } catch(e) {
                logError('debug', '诊断异常: ' + e);
                return { ok: false, error: String(e) };
            }

            return { ok: true, result: result };
        },

        // ---- 瞄准诊断 RPC ----
        startaimdiagnostic: function(durationSeconds) {
            return startAimDiagnostic(durationSeconds);
        },

        stopaimdiagnostic: function() {
            return stopAimDiagnostic();
        },

        captureaimsnapshot: function(tag) {
            return captureAimSnapshot(tag);
        },

        getaimdiagstatus: function() {
            return {
                active: aimDiag.active,
                sessionId: aimDiag.sessionId,
                shotId: aimDiag.shotId,
                elapsed: aimDiag.active ? ((Date.now() - aimDiag.startTime) / 1000).toFixed(1) + 's' : '0s',
                duration: aimDiag.duration + 's',
                lineCount: aimDiag.logLines.length,
            };
        },
    };

    // Phase6: 不要在脚本加载时安装事件 Hook，应该在 installhook() 时安装
    // installEventHooks(); // 移除这行

    send({type:'log', level:'info', module:'TP', message:'脚本 v8 加载完成'});
})();
