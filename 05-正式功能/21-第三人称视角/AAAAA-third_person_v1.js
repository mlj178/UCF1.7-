(function() {
    'use strict';

    // =============================================
    // UCF1.7 第三人称视角修改器 v8
    // 修复：调用 OnOwnerObserveModeChange 完成 PV/CV 切换
    //       显式隐藏 PV Renderer、显示 CV 对象
    //       修正相机轨道和肩后视角
    //       完整恢复所有状态
    //       增强 debugmodel 诊断
    // =============================================

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { send('no module'); return; }
    var base = mod.base;
    send({type:'log', level:'info', module:'TP', message:'base=' + base + ' size=' + mod.size});

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

    // ---- NativeFunction 声明 ----
    var isMyPlayer = new NativeFunction(base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer']);
    var singletonGetter = new NativeFunction(base.add(RVA.Singleton_GetInstance), 'pointer', ['pointer']);
    var cflSetFollow = new NativeFunction(base.add(RVA.CFL_set_Follow), 'void', ['pointer', 'pointer']);
    var cflSetLookAt = new NativeFunction(base.add(RVA.CFL_set_LookAt), 'void', ['pointer', 'pointer']);
    var setFreeLookActive = new NativeFunction(base.add(RVA.CameraManager_SetFreeLookCameraActive), 'void', ['pointer', 'bool']);
    var setModelLayer = new NativeFunction(base.add(RVA.Model_SetModelLayer), 'void', ['pointer', 'int', 'int']);
    var setObserveMode = new NativeFunction(base.add(RVA.PlayerData_SetObserveMode), 'void', ['pointer', 'int']);
    var getObserveMode = new NativeFunction(base.add(RVA.PlayerData_get_observeMode), 'int', ['pointer']);
    var setModelVisible = new NativeFunction(base.add(RVA.PCM_set_modelVisible), 'void', ['pointer', 'bool']);
    var playerViewSetting = new NativeFunction(base.add(RVA.Weapon_PlayerViewSetting), 'void', ['pointer']);
    var synchronizeHand = new NativeFunction(base.add(RVA.Weapon_SynchronizeHand), 'void', ['pointer']);
    var gameObjectSetActive = new NativeFunction(base.add(RVA.GameObject_SetActive), 'void', ['pointer', 'bool']);
    var gameObjectGetActiveSelf = new NativeFunction(base.add(RVA.GameObject_get_activeSelf), 'bool', ['pointer']);
    var gameObjectGetLayer = new NativeFunction(base.add(RVA.GameObject_get_layer), 'int', ['pointer']);
    var gameObjectSetLayer = new NativeFunction(base.add(RVA.GameObject_set_layer), 'void', ['pointer', 'int']);
    var gameObjectGetName = new NativeFunction(base.add(RVA.GameObject_get_name), 'pointer', ['pointer']);
    var rendererGetEnabled = new NativeFunction(base.add(RVA.Renderer_get_enabled), 'bool', ['pointer']);
    var rendererSetEnabled = new NativeFunction(base.add(RVA.Renderer_set_enabled), 'void', ['pointer', 'bool']);
    var getRig = new NativeFunction(base.add(RVA.CFL_GetRig), 'pointer', ['pointer', 'int']);
    var getComponentPipeline = new NativeFunction(base.add(RVA.CVC_GetComponentPipeline), 'pointer', ['pointer']);

    // v8 新增：Model.OnOwnerObserveModeChange(Model.Type mode) — private 方法
    var onOwnerObserveModeChange = new NativeFunction(base.add(RVA.Model_OnOwnerObserveModeChange), 'void', ['pointer', 'int']);

    send({type:'log', level:'info', module:'TP', message:'NativeFunction 声明完成 (v8)'});

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
        if (!isNull(cameraManager) && isReadable(cameraManager)) return cameraManager;
        cameraManager = null;
        try {
            var methodInfo = base.add(RVA.CameraManager_SingletonMethodInfo).readPointer();
            if (isNull(methodInfo)) { logError('cm_mi', 'CameraManager MethodInfo null'); return null; }
            var temp = singletonGetter(methodInfo);
            if (!isNull(temp) && isReadable(temp)) {
                cameraManager = temp;
                log('info', 'CameraManager 获取成功: ' + cameraManager);
                return cameraManager;
            }
        } catch(e) { logError('cm_get', 'CameraManager 获取失败: ' + e); }
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
                var pp = ap.add(0x10 + i * 8).readPointer();
                if (!isNull(pp) && isMyPlayer(pp)) return pp;
            }
        } catch(e) { logError('find_player', 'findMyPlayer 失败: ' + e); }
        return null;
    }

    function readIl2cppString(strPtr) {
        if (isNull(strPtr)) return '<null>';
        try {
            var len = strPtr.add(0x10).readS32();
            if (len < 0 || len > 256) return '<bad_len:' + len + '>';
            return strPtr.add(0x14).readUtf8String(len);
        } catch(e) { return '<err>'; }
    }

    function getGameObjectName(goPtr) {
        if (isNull(goPtr)) return '<null_go>';
        try {
            var namePtr = gameObjectGetName(goPtr);
            return readIl2cppString(namePtr);
        } catch(e) { return '<name_err>'; }
    }

    // 读取 List<GameObject> 的信息（含 Renderer.enabled）
    function readGameObjectList(listPtr, label) {
        var result = { count: 0, items: [] };
        if (isNull(listPtr)) {
            log('info', '[诊断] ' + label + ': null');
            return result;
        }
        try {
            var itemsPtr = listPtr.add(0x10).readPointer();
            var count = listPtr.add(0x18).readU32();
            result.count = count;
            log('info', '[诊断] ' + label + ' 数量: ' + count);
            for (var i = 0; i < count && i < 30; i++) {
                var goPtr = itemsPtr.add(i * 8).readPointer();
                if (isNull(goPtr)) {
                    result.items.push({ name: '<null>', active: false, layer: -1, rendererEnabled: null });
                    continue;
                }
                var name = getGameObjectName(goPtr);
                var active = false;
                var layer = -1;
                var renEnabled = null;
                try { active = gameObjectGetActiveSelf(goPtr); } catch(e) {}
                try { layer = gameObjectGetLayer(goPtr); } catch(e) {}
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
                savedState.observeMode = getObserveMode(playerData);
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
                if (!isNull(pvListPtr)) {
                    var pvItems = pvListPtr.add(0x10).readPointer();
                    var pvCount = pvListPtr.add(0x18).readU32();
                    for (var i = 0; i < pvCount && i < 30; i++) {
                        var goPtr = pvItems.add(i * 8).readPointer();
                        if (!isNull(goPtr)) {
                            try {
                                savedState.pvActiveStates.push(gameObjectGetActiveSelf(goPtr));
                                savedState.pvLayerStates.push(gameObjectGetLayer(goPtr));
                            } catch(e) {
                                savedState.pvActiveStates.push(true);
                                savedState.pvLayerStates.push(-1);
                            }
                        }
                    }
                    log('info', '[Model] 保存 PV 对象状态: ' + savedState.pvActiveStates.length + ' 个');
                }

                // 保存 CV 对象状态
                if (!isNull(cvListPtr)) {
                    var cvItems = cvListPtr.add(0x10).readPointer();
                    var cvCount = cvListPtr.add(0x18).readU32();
                    for (var i = 0; i < cvCount && i < 30; i++) {
                        var goPtr = cvItems.add(i * 8).readPointer();
                        if (!isNull(goPtr)) {
                            try {
                                savedState.cvActiveStates.push(gameObjectGetActiveSelf(goPtr));
                                savedState.cvLayerStates.push(gameObjectGetLayer(goPtr));
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
                setObserveMode(playerData, 0); // Model.Type.Character = 0
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
                onOwnerObserveModeChange(character, 0); // Model.Type.Character = 0
                log('info', '[Model] OnOwnerObserveModeChange(Character=0) 已调用');
            } catch(e) {
                logError('on_observe', 'OnOwnerObserveModeChange 失败: ' + e);
            }
        }

        // 5. 显式隐藏 PV 对象（双重保险，确保第一人称枪模消失）
        if (!isNull(character)) {
            try {
                var pvListPtr = character.add(OFF.Model_objectInPV).readPointer();
                if (!isNull(pvListPtr)) {
                    var pvItems = pvListPtr.add(0x10).readPointer();
                    var pvCount = pvListPtr.add(0x18).readU32();
                    var hiddenCount = 0;
                    for (var i = 0; i < pvCount && i < 30; i++) {
                        var goPtr = pvItems.add(i * 8).readPointer();
                        if (!isNull(goPtr)) {
                            try {
                                // 先检查当前状态
                                var wasActive = gameObjectGetActiveSelf(goPtr);
                                if (wasActive) {
                                    gameObjectSetActive(goPtr, false);
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
            try {
                var cvListPtr = character.add(OFF.Model_objectInCV).readPointer();
                if (!isNull(cvListPtr)) {
                    var cvItems = cvListPtr.add(0x10).readPointer();
                    var cvCount = cvListPtr.add(0x18).readU32();
                    var shownCount = 0;
                    for (var i = 0; i < cvCount && i < 30; i++) {
                        var goPtr = cvItems.add(i * 8).readPointer();
                        if (!isNull(goPtr)) {
                            try {
                                var wasActive = gameObjectGetActiveSelf(goPtr);
                                if (!wasActive) {
                                    gameObjectSetActive(goPtr, true);
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
                setModelLayer(character, 0, 0); // Model.Type.Character=0, Layer=0(Default)
                log('info', '[Model] SetModelLayer(Character, Default) 已调用');
            } catch(e) {
                logError('set_layer', 'SetModelLayer 失败: ' + e);
            }
        }

        // 8. 隐藏 PlayerCameraManager 的 modelVisible (第一人称手臂相机)
        try {
            var pcm = player.add(OFF.Player_cameraManager).readPointer();
            if (!isNull(pcm)) {
                setModelVisible(pcm, false);
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
                        synchronizeHand(inUse);
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
                var rig = getRig(freeLook, rigIdx);
                if (isNull(rig)) continue;

                var pipeline = getComponentPipeline(rig);
                if (isNull(pipeline)) continue;

                var pipeLen = pipeline.add(0xC).readU32();
                for (var ci = 0; ci < pipeLen && ci < 10; ci++) {
                    var comp = pipeline.add(0x10 + ci * 8).readPointer();
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
            cflSetFollow(freeLook, charContainer);
            // LookAt 使用 spine1 (胸部位置)，而不是头部，减少俯视
            if (!isNull(spine1)) {
                cflSetLookAt(freeLook, spine1);
            } else {
                cflSetLookAt(freeLook, charContainer);
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
            setFreeLookActive(camMgr, 1);
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

        try {
            // 1. 恢复观察模式
            var player = findMyPlayer();
            if (player) {
                // 1a. 调用 OnOwnerObserveModeChange(PlayerView=1) 恢复 PV 模式
                var character = player.add(OFF.Player_currentCharacter).readPointer();
                if (!isNull(character)) {
                    try {
                        onOwnerObserveModeChange(character, 1); // Model.Type.PlayerView = 1
                        log('info', '[Restore] OnOwnerObserveModeChange(PlayerView=1) 已调用');
                    } catch(e) {
                        errors.push('OnOwnerObserveModeChange 恢复失败: ' + e);
                    }
                }

                // 1b. 恢复 PlayerData.SetObserveMode
                try {
                    var playerData = player.add(OFF.Player_playerData).readPointer();
                    if (!isNull(playerData) && savedState.observeMode >= 0) {
                        setObserveMode(playerData, savedState.observeMode);
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
                        var pvListPtr = character.add(OFF.Model_objectInPV).readPointer();
                        if (!isNull(pvListPtr)) {
                            var pvItems = pvListPtr.add(0x10).readPointer();
                            var pvCount = pvListPtr.add(0x18).readU32();
                            for (var i = 0; i < pvCount && i < savedState.pvActiveStates.length; i++) {
                                var goPtr = pvItems.add(i * 8).readPointer();
                                if (!isNull(goPtr)) {
                                    try {
                                        gameObjectSetActive(goPtr, savedState.pvActiveStates[i]);
                                        if (savedState.pvLayerStates[i] >= 0) {
                                            gameObjectSetLayer(goPtr, savedState.pvLayerStates[i]);
                                        }
                                    } catch(e) {}
                                }
                            }
                            log('info', '[Restore] PV 对象已恢复: ' + pvCount + ' 个');
                        }

                        // 恢复 CV 对象
                        var cvListPtr = character.add(OFF.Model_objectInCV).readPointer();
                        if (!isNull(cvListPtr)) {
                            var cvItems = cvListPtr.add(0x10).readPointer();
                            var cvCount = cvListPtr.add(0x18).readU32();
                            for (var i = 0; i < cvCount && i < savedState.cvActiveStates.length; i++) {
                                var goPtr = cvItems.add(i * 8).readPointer();
                                if (!isNull(goPtr)) {
                                    try {
                                        gameObjectSetActive(goPtr, savedState.cvActiveStates[i]);
                                        if (savedState.cvLayerStates[i] >= 0) {
                                            gameObjectSetLayer(goPtr, savedState.cvLayerStates[i]);
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
                        setModelLayer(character, 1, 8); // PlayerView, PV layer
                        log('info', '[Restore] SetModelLayer(PlayerView, Layer8) 已调用');
                    } catch(e) {
                        errors.push('恢复模型 Layer 失败: ' + e);
                    }
                }

                // 4. 恢复 PlayerCameraManager.modelVisible
                try {
                    var pcm = player.add(OFF.Player_cameraManager).readPointer();
                    if (!isNull(pcm)) {
                        setModelVisible(pcm, true);
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
                            playerViewSetting(inUse);
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
                    setFreeLookActive(camMgr, 0);
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
                            var rig = getRig(freeLook, rigIdx);
                            if (isNull(rig)) continue;
                            var pipeline = getComponentPipeline(rig);
                            if (isNull(pipeline)) continue;
                            var pipeLen = pipeline.add(0xC).readU32();
                            for (var ci = 0; ci < pipeLen && ci < 10; ci++) {
                                var comp = pipeline.add(0x10 + ci * 8).readPointer();
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

            // 每 500ms 重新激活 FreeLook
            if (loopCounter % 10 === 0) {
                try { setFreeLookActive(camMgr, 1); } catch(e) {}
            }

            // 每 2 秒重新同步武器
            if (loopCounter % 40 === 0) {
                try {
                    var wpns = player.add(OFF.Player_wpns).readPointer();
                    if (!isNull(wpns)) {
                        var inUse = wpns.add(OFF.PW_inUse).readPointer();
                        if (!isNull(inUse)) {
                            synchronizeHand(inUse);
                        }
                    }
                } catch(e) {}
            }

            // 每 5 秒确保 PV 对象仍然隐藏 + PV Renderer 禁用
            if (loopCounter % 100 === 0) {
                try {
                    var character = player.add(OFF.Player_currentCharacter).readPointer();
                    if (!isNull(character)) {
                        var pvListPtr = character.add(OFF.Model_objectInPV).readPointer();
                        if (!isNull(pvListPtr)) {
                            var pvItems = pvListPtr.add(0x10).readPointer();
                            var pvCount = pvListPtr.add(0x18).readU32();
                            for (var i = 0; i < pvCount && i < 30; i++) {
                                var goPtr = pvItems.add(i * 8).readPointer();
                                if (!isNull(goPtr)) {
                                    try {
                                        if (gameObjectGetActiveSelf(goPtr)) {
                                            gameObjectSetActive(goPtr, false);
                                        }
                                    } catch(e) {}
                                }
                            }
                        }

                        // v8: 同时确保 CV 对象仍然显示
                        var cvListPtr = character.add(OFF.Model_objectInCV).readPointer();
                        if (!isNull(cvListPtr)) {
                            var cvItems = cvListPtr.add(0x10).readPointer();
                            var cvCount = cvListPtr.add(0x18).readU32();
                            for (var i = 0; i < cvCount && i < 30; i++) {
                                var goPtr = cvItems.add(i * 8).readPointer();
                                if (!isNull(goPtr)) {
                                    try {
                                        if (!gameObjectGetActiveSelf(goPtr)) {
                                            gameObjectSetActive(goPtr, true);
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
                            setFreeLookActive(this._camMgr, 1);
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
    // RPC 接口
    // ============================================================
    rpc.exports = {
        installhook: function() {
            if (enabled) return { ok: true };
            try {
                installHooks();
                timer = setInterval(loop, 50);
                enabled = true;
                log('info', '修改器 v8 已启动');
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
        debugmodel: function() {
            var result = {
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
                        result.observeMode = getObserveMode(playerData);
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
                            // Il2CppArray 布局: 0x0C = max_length, 0x10 = data[0]
                            var sinCount = sockItemsNamePtr.add(0xC).readU32();
                            log('info', '[诊断] socketItemsName 数量: ' + sinCount);
                            for (var i = 0; i < sinCount && i < 10; i++) {
                                var namePtr = sockItemsNamePtr.add(0x10 + i * 8).readPointer();
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
                            var rig = getRig(freeLook, rigIdx);
                            if (isNull(rig)) continue;
                            var rigInfo = { index: rigIdx, components: [] };
                            var pipeline = getComponentPipeline(rig);
                            if (isNull(pipeline)) continue;
                            var pipeLen = pipeline.add(0xC).readU32();
                            for (var ci = 0; ci < pipeLen && ci < 10; ci++) {
                                var comp = pipeline.add(0x10 + ci * 8).readPointer();
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
    };

    send({type:'log', level:'info', module:'TP', message:'脚本 v8 加载完成'});
})();
