(function() {
  'use strict';

  // ================================================================
  // 热成像透视功能 v2.0 - 方式A: 调用CameraManager.SetThermalVision
  //
  // 核心思路:
  //   1. 直接调用CameraManager.SetThermalVision(float duration, bool showHuman)
  //   2. 这是静态方法，无需获取实例，全模式通用
  //
  // 优势:
  //   - 实现简单，只需一个函数调用
  //   - 全模式支持（不限于Nano6）
  //   - 全角色支持
  //   - 无访问违规风险
  // ================================================================

  // ================================================================
  // 日志系统
  // ================================================================
  var MAX_LOGS_PER_MODULE = 100;
  var moduleLogCounts = {};

  function sendLog(level, module, message) {
    if (!moduleLogCounts[module]) moduleLogCounts[module] = 0;
    if (moduleLogCounts[module] >= MAX_LOGS_PER_MODULE) return;
    moduleLogCounts[module]++;
    var fullMsg = '[' + module + '] ' + message;
    console.log(fullMsg);
    send({ type: 'log', level: level, module: module, message: message });
  }

  function sendStatus(feature, enabled) {
    console.log('[状态] ' + feature + ' -> ' + (enabled ? '开' : '关'));
    send({ type: 'status', feature: feature, enabled: enabled });
  }

  // ================================================================
  // 获取 GameAssembly.dll
  // ================================================================
  var _gameAssembly = null;

  function getGameAssembly() {
    if (_gameAssembly) return _gameAssembly;
    try {
      var mod = Process.findModuleByName('GameAssembly.dll');
      if (!mod) {
        sendLog('error', '系统', '未找到 GameAssembly.dll');
        return null;
      }
      _gameAssembly = mod;
      sendLog('info', '系统', 'GameAssembly.dll: base=' + mod.base + ' size=' + mod.size);
      return mod;
    } catch(e) {
      sendLog('error', '系统', '获取模块失败: ' + e.message);
      return null;
    }
  }

  // ================================================================
  // RVA 常量
  // ================================================================
  var RVA = {
    GameManager_TypeInfo: 0x0E2933C,
    CameraManager_TypeInfo: 0x0E263C0,
    SetThermalVision: 0xB36960,
    il2cpp_runtime_class_init: 0x108970,
    VolumeProfile_TryGet_ThermalVision: 0x7D34F0,
    VolumeProfile_TryGet_ThermalVision_MethodInfo: 0x0E24E38,
    Singleton_CameraManager_get_instance: 0x4A8090,
    Singleton_CameraManager_get_instance_MethodInfo: 0x0E1CD68,
    GraphicsSettings_get_currentRenderPipeline: 0x3331B0,
    Awake_ConditionalJump_RVA: 0x0B357B2,
  };

  // ================================================================
  // CameraManager静态字段偏移
  // ================================================================
  var CM_STATIC = {
    playerView: 0x00,         // static ObscuredBool playerView
    FocusPlayerChangeEvent: 0x0C,  // static Action FocusPlayerChangeEvent_Observers
    volumeProfile: 0x10,      // static VolumeProfile volumeProfile
    oneShine: 0x14,           // static GhostBladeOneShine oneShine
    thermalVision: 0x18,      // static ThermalVision thermalVision  <-- 关键字段！
  };

  // ================================================================
  // ThermalVision组件字段偏移
  // ================================================================
  var TV_FIELD = {
    active: 0x0C,
    Duration: 0x1C,
    MainColor: 0x20,
    NoiseScale: 0x24,
    NoisePower: 0x28,
  };

  var VOLUMEPARAM = {
    overrideState: 0x08,
    value: 0x0C,
  };

  // ================================================================
  // 静态字段偏移 (GameManager)
  // ================================================================
  var GM_STATIC = {
    myPlayer: 0x00,           // static Player myPlayer
    gameMode: 0x04,           // static GameMode gameMode
    weaponLimited: 0x08,      // static WeaponLimited weaponLimited
    revengeEnable: 0x0C,      // static bool revengeEnable
    gameModePrefab: 0x10,     // static GameObject gameModePrefab
    ace: 0x14,                // static Player ace
    WpnDictionary: 0x18,      // static Dictionary WpnDictionary
  };

  // ================================================================
  // 模块状态
  // ================================================================
  var state = {
    enabled: false,
    lastTriggerTime: 0,
    cooldown: 3000,
    duration: 3.0,
    showHuman: false,
    timer: null,
  };

  // ================================================================
  // NativeFunction 缓存
  // ================================================================
  var setThermalVision = null;
  var GetAsyncKeyState = null;
  var T_KEY = 0x54;
  
  // GameManager静态字段地址
  var gmStaticFields = null;
  // CameraManager静态字段地址
  var cmStaticFields = null;
  // ThermalVision组件地址
  var thermalVisionComponent = null;
  var setThermalVisionMethodInfo = null;

  // ================================================================
  // 查找CameraManager TypeInfo地址 (参考get_all_instances.js)
  // ================================================================
  function getCameraManagerKlass() {
    var mod = getGameAssembly();
    if (!mod) return null;
    
    try {
      var typeInfoSlot = mod.base.add(RVA.CameraManager_TypeInfo);
      var klass = typeInfoSlot.readPointer();
      
      if (!klass || klass.isNull()) {
        sendLog('error', 'CameraManager', 'klass为空');
        return null;
      }
      
      var name_ptr = klass.add(0x08).readPointer();
      if (name_ptr && !name_ptr.isNull()) {
        var className = name_ptr.readCString();
        if (className !== 'CameraManager') {
          sendLog('error', 'CameraManager', '类名不匹配: ' + className);
          return null;
        }
      }
      
      sendLog('info', 'CameraManager', 'klass: ' + klass);
      return klass;
    } catch(e) {
      sendLog('error', 'CameraManager', '获取klass失败: ' + e.message);
      return null;
    }
  }

  function findSetThermalVisionMethodInfo() {
    if (setThermalVisionMethodInfo) return setThermalVisionMethodInfo;
    
    var mod = getGameAssembly();
    if (!mod) return null;
    
    var klass = getCameraManagerKlass();
    if (!klass || klass.isNull()) {
      sendLog('error', 'MethodInfo', '无法获取CameraManager klass');
      return null;
    }
    
    var targetAddr = mod.base.add(RVA.SetThermalVision);
    
    try {
      var exportAddr = mod.getExportByName('il2cpp_class_get_method_from_name');
      if (exportAddr) {
        sendLog('info', 'MethodInfo', 'Strategy 1: il2cpp_class_get_method_from_name...');
        var getClassMethod = new NativeFunction(exportAddr, 'pointer', ['pointer', 'pointer', 'uint32']);
        var methodName = Memory.allocUtf8String('SetThermalVision');
        var methodInfo = getClassMethod(klass, methodName, 2);
        
        if (methodInfo && !methodInfo.isNull()) {
          setThermalVisionMethodInfo = methodInfo;
          sendLog('success', 'MethodInfo', '✅ Strategy 1 成功! MethodInfo*: ' + methodInfo);
          var mp = methodInfo.readPointer();
          sendLog('success', 'MethodInfo', '  methodPointer: ' + mp);
          return methodInfo;
        }
        sendLog('warn', 'MethodInfo', 'Strategy 1: 导出函数存在但未找到方法');
      }
    } catch(e) {
      sendLog('warn', 'MethodInfo', 'Strategy 1 失败: ' + e.message);
    }
    
    try {
      var exportAddr2 = mod.getExportByName('il2cpp_class_get_methods');
      if (exportAddr2) {
        sendLog('info', 'MethodInfo', 'Strategy 2: il2cpp_class_get_methods 遍历...');
        var getClassMethods = new NativeFunction(exportAddr2, 'pointer', ['pointer', 'pointer']);
        var iter = Memory.alloc(Process.pointerSize);
        iter.writePointer(ptr(0));
        
        var count = 0;
        while (count < 200) {
          var methodInfo = getClassMethods(klass, iter);
          if (!methodInfo || methodInfo.isNull()) break;
          
          count++;
          var methodPointer = methodInfo.readPointer();
          if (methodPointer && !methodPointer.isNull() && methodPointer.equals(targetAddr)) {
            setThermalVisionMethodInfo = methodInfo;
            sendLog('success', 'MethodInfo', '✅ Strategy 2 成功! MethodInfo*: ' + methodInfo);
            sendLog('success', 'MethodInfo', '  遍历了 ' + count + ' 个方法');
            return methodInfo;
          }
        }
        sendLog('warn', 'MethodInfo', 'Strategy 2: 遍历了 ' + count + ' 个方法，未找到匹配');
      }
    } catch(e) {
      sendLog('warn', 'MethodInfo', 'Strategy 2 失败: ' + e.message);
    }
    
    try {
      sendLog('info', 'MethodInfo', 'Strategy 3: 扫描klass结构...');
      var possibleOffsets = [0x44, 0x48, 0x50, 0x54, 0x40, 0x3C];
      for (var oi = 0; oi < possibleOffsets.length; oi++) {
        var off = possibleOffsets[oi];
        try {
          var methodsPtr = klass.add(off).readPointer();
          if (!methodsPtr || methodsPtr.isNull()) continue;
          
          for (var mi = 0; mi < 50; mi++) {
            try {
              var methodInfo = methodsPtr.add(Process.pointerSize * mi).readPointer();
              if (!methodInfo || methodInfo.isNull()) break;
              
              var methodPointer = methodInfo.readPointer();
              if (methodPointer && !methodPointer.isNull() && methodPointer.equals(targetAddr)) {
                setThermalVisionMethodInfo = methodInfo;
                sendLog('success', 'MethodInfo', '✅ Strategy 3 成功! offset=0x' + off.toString(16) + ' MethodInfo*: ' + methodInfo);
                return methodInfo;
              }
            } catch(e) {
              break;
            }
          }
        } catch(e) {
          continue;
        }
      }
      sendLog('warn', 'MethodInfo', 'Strategy 3: 结构扫描未找到');
    } catch(e) {
      sendLog('warn', 'MethodInfo', 'Strategy 3 失败: ' + e.message);
    }
    
    sendLog('error', 'MethodInfo', '❌ 所有策略均失败，无法获取MethodInfo*');
    return null;
  }

  // ================================================================
  // 获取CameraManager静态字段 (参考get_all_instances.js)
  // ================================================================
  function getCameraManagerStaticFields() {
    if (cmStaticFields) return cmStaticFields;
    
    var mod = getGameAssembly();
    if (!mod) return null;
    
    try {
      var klass = getCameraManagerKlass();
      if (!klass || klass.isNull()) {
        sendLog('error', 'CameraManager', 'klass为空');
        return null;
      }
      
      var sf = klass.add(0x5C).readPointer();
      sendLog('info', 'CameraManager', 'static_fields: ' + sf);
      
      if (!sf || sf.isNull()) {
        sendLog('info', 'CameraManager', 'static_fields为空，尝试初始化...');
        
        var Il2CppClass_2_base = klass.add(0x64);
        var cctor_finished = Il2CppClass_2_base.add(0x10).readU32();
        var bitflags2 = Il2CppClass_2_base.add(0x57).readU8();
        var needInit = ((bitflags2 & 4) !== 0) && (cctor_finished === 0);
        
        sendLog('info', 'CameraManager', 'cctor_finished=' + cctor_finished + ' bitflags2=' + bitflags2 + ' needInit=' + needInit);
        
        if (needInit) {
          try {
            var initFn = new NativeFunction(mod.base.add(RVA.il2cpp_runtime_class_init), 'void', ['pointer']);
            initFn(klass);
            sendLog('success', 'CameraManager', '✅ il2cpp_runtime_class_init完成');
            
            sf = klass.add(0x5C).readPointer();
            sendLog('success', 'CameraManager', 'static_fields(初始化后): ' + sf);
          } catch(e) {
            sendLog('error', 'CameraManager', '初始化失败: ' + e.message);
            return null;
          }
        }
      }
      
      if (!sf || sf.isNull()) {
        sendLog('error', 'CameraManager', 'static_fields仍为空');
        return null;
      }
      
      cmStaticFields = sf;
      sendLog('success', 'CameraManager', '✅ CameraManager静态字段获取成功: ' + sf);
      return sf;
    } catch(e) {
      sendLog('error', 'CameraManager', '获取静态字段失败: ' + e.message);
      return null;
    }
  }

  // ================================================================
  // 获取ThermalVision组件
  // ================================================================
  function getThermalVisionComponent() {
    if (thermalVisionComponent) return thermalVisionComponent;
    
    try {
      var sf = getCameraManagerStaticFields();
      if (!sf || sf.isNull()) {
        sendLog('error', 'ThermalVision', '无法获取CameraManager静态字段');
        return null;
      }
      
      // 读取thermalVision指针 (偏移0x18)
      var tv = sf.add(CM_STATIC.thermalVision).readPointer();
      sendLog('info', 'ThermalVision', '组件地址: ' + tv);
      
      if (!tv || tv.isNull()) {
        sendLog('error', 'ThermalVision', 'thermalVision组件为空');
        return null;
      }
      
      thermalVisionComponent = tv;
      sendLog('info', 'ThermalVision', '✅ ThermalVision组件获取成功: ' + tv);
      return tv;
    } catch(e) {
      sendLog('error', 'ThermalVision', '获取组件失败: ' + e.message);
      return null;
    }
  }

  // ================================================================
  // 获取GameManager静态字段 (参考get_all_instances.js)
  // ================================================================
  function getGameManagerStaticFields() {
    if (gmStaticFields) return gmStaticFields;
    
    var mod = getGameAssembly();
    if (!mod) return null;
    
    try {
      // 1. 读取TypeInfo槽
      var typeInfoSlot = mod.base.add(RVA.GameManager_TypeInfo);
      var klass = typeInfoSlot.readPointer();
      
      sendLog('info', 'GameManager', 'TypeInfo槽: ' + typeInfoSlot);
      sendLog('info', 'GameManager', 'klass: ' + klass);
      
      if (!klass || klass.isNull()) {
        sendLog('error', 'GameManager', 'klass为空');
        return null;
      }
      
      // 2. 读取static_fields指针 (klass + 0x5C)
      var sf = klass.add(0x5C).readPointer();
      sendLog('info', 'GameManager', 'static_fields: ' + sf);
      
      if (!sf || sf.isNull()) {
        // 3. 如果static_fields为空，需要初始化
        sendLog('info', 'GameManager', 'static_fields为空，尝试初始化...');
        
        // 检查是否需要初始化
        var cctor_finished = klass.add(0x64 + 0x10).readU32();
        var bitflags2 = klass.add(0x64 + 0x57).readU8();
        var needInit = ((bitflags2 & 4) !== 0) && (cctor_finished === 0);
        
        sendLog('info', 'GameManager', 'cctor_finished=' + cctor_finished + ' bitflags2=' + bitflags2 + ' needInit=' + needInit);
        
        if (needInit) {
          try {
            var initFn = new NativeFunction(mod.base.add(RVA.il2cpp_runtime_class_init), 'void', ['pointer']);
            initFn(klass);
            sendLog('info', 'GameManager', '✅ il2cpp_runtime_class_init完成');
            
            // 重新读取static_fields
            sf = klass.add(0x5C).readPointer();
            sendLog('info', 'GameManager', 'static_fields(初始化后): ' + sf);
          } catch(e) {
            sendLog('error', 'GameManager', '初始化失败: ' + e.message);
            return null;
          }
        }
      }
      
      if (!sf || sf.isNull()) {
        sendLog('error', 'GameManager', 'static_fields仍为空');
        return null;
      }
      
      gmStaticFields = sf;
      sendLog('info', 'GameManager', '✅ GameManager静态字段获取成功: ' + sf);
      return sf;
    } catch(e) {
      sendLog('error', 'GameManager', '获取静态字段失败: ' + e.message);
      return null;
    }
  }

  // ================================================================
  // 游戏状态检测
  // ================================================================
  function getGameState() {
    var mod = getGameAssembly();
    if (!mod) return null;
    
    try {
      // 获取GameManager静态字段
      var sf = getGameManagerStaticFields();
      if (!sf || sf.isNull()) {
        sendLog('error', '状态', '无法获取GameManager静态字段');
        return null;
      }
      
      // 读取静态字段
      var myPlayer = sf.add(GM_STATIC.myPlayer).readPointer();
      var gameMode = sf.add(GM_STATIC.gameMode).readS32();
      
      return {
        myPlayer: myPlayer,
        gameMode: gameMode,
        inGame: !myPlayer.isNull(),
        gameModeName: getGameModeName(gameMode)
      };
    } catch(e) {
      sendLog('error', '状态', '读取游戏状态失败: ' + e.message);
      return null;
    }
  }

  function getGameModeName(mode) {
    var names = {
      0: 'TeamDeath',
      1: 'DeathMatch',
      2: 'Special',
      3: 'Nano3',
      4: 'Nano4',
      5: 'Nano6',
      6: 'Nano4_Terminator'
    };
    return names[mode] || 'Unknown';
  }

  // ================================================================
  // 初始化函数
  // ================================================================
  function init() {
    var mod = getGameAssembly();
    if (!mod) return false;
    var base = mod.base;

    try {
      sendLog('info', '初始化', '初始化SetThermalVision...');
      try {
        var setThermalVisionAddr = base.add(RVA.SetThermalVision);
        sendLog('info', '初始化', 'SetThermalVision地址: ' + setThermalVisionAddr);
        
        setThermalVision = new NativeFunction(setThermalVisionAddr, 'void', ['float', 'int', 'pointer']);
        sendLog('info', '初始化', '✅ SetThermalVision已绑定 (3参数: float, int, pointer)');
      } catch(e) {
        sendLog('error', '初始化', 'SetThermalVision绑定失败: ' + e.message);
        setThermalVision = null;
        return false;
      }

      sendLog('info', '初始化', '查找SetThermalVision的MethodInfo*...');
      var mi = findSetThermalVisionMethodInfo();
      if (mi && !mi.isNull()) {
        sendLog('success', '初始化', '✅ MethodInfo*: ' + mi);
      } else {
        sendLog('warn', '初始化', '⚠️ 未找到MethodInfo*，将使用方案B（直接修改组件）作为后备');
      }

      // 初始化 GetAsyncKeyState
      sendLog('info', '初始化', '初始化GetAsyncKeyState...');
      try {
        var user32 = Process.getModuleByName('user32.dll');
        var getAsyncKeyStateExport = user32.getExportByName('GetAsyncKeyState');
        GetAsyncKeyState = new NativeFunction(getAsyncKeyStateExport, 'int16', ['int32']);
        sendLog('info', '初始化', '✅ GetAsyncKeyState已绑定');
      } catch(e) {
        sendLog('error', '初始化', 'GetAsyncKeyState初始化失败: ' + e.message);
        return false;
      }

      sendLog('info', '初始化', '✅ 初始化完成');
      return true;
    } catch(e) {
      sendLog('error', '初始化', '初始化失败: ' + e.message);
      return false;
    }
  }

  // ================================================================
  // 按键检测
  // ================================================================
  function isKeyPressed() {
    try {
      return (GetAsyncKeyState(T_KEY) & 0x8000) !== 0;
    } catch(e) {
      return false;
    }
  }

  // ================================================================
  // 热成像控制 (方式A: 调用CameraManager.SetThermalVision静态方法)
  // ================================================================
  function readFloatParam(tv, fieldOffset) {
    try {
      var paramObj = tv.add(fieldOffset).readPointer();
      if (!paramObj || paramObj.isNull()) return null;
      var value = paramObj.add(VOLUMEPARAM.value).readFloat();
      var overrideState = paramObj.add(VOLUMEPARAM.overrideState).readU8();
      return { value: value, overrideState: overrideState };
    } catch(e) {
      return null;
    }
  }

  function writeFloatParam(tv, fieldOffset, value) {
    try {
      var paramObj = tv.add(fieldOffset).readPointer();
      if (!paramObj || paramObj.isNull()) return false;
      paramObj.add(VOLUMEPARAM.value).writeFloat(value);
      paramObj.add(VOLUMEPARAM.overrideState).writeU8(1);
      return true;
    } catch(e) {
      return false;
    }
  }

  function getCameraManagerInstance() {
    var mod = getGameAssembly();
    if (!mod) return null;
    
    try {
      var getInstanceAddr = mod.base.add(RVA.Singleton_CameraManager_get_instance);
      var methodInfoAddr = mod.base.add(RVA.Singleton_CameraManager_get_instance_MethodInfo);
      var methodInfo = methodInfoAddr.readPointer();
      
      if (!methodInfo || methodInfo.isNull()) {
        sendLog('error', '单例', 'get_instance MethodInfo为空');
        return null;
      }
      
      var getInstance = new NativeFunction(getInstanceAddr, 'pointer', ['pointer']);
      var instance = getInstance(methodInfo);
      
      if (!instance || instance.isNull()) {
        sendLog('warn', '单例', 'CameraManager单例为空');
        return null;
      }
      
      sendLog('info', '单例', 'CameraManager实例: ' + instance);
      return instance;
    } catch(e) {
      sendLog('error', '单例', '获取CameraManager实例失败: ' + e.message);
      return null;
    }
  }

  function readListItems(listPtr) {
    if (!listPtr || listPtr.isNull()) return { items: null, size: 0 };
    try {
      var items = listPtr.add(0x08).readPointer();
      var size = listPtr.add(0x0C).readU32();
      return { items: items, size: size };
    } catch(e) {
      return { items: null, size: 0 };
    }
  }

  function diagnoseThermalVisionPipeline() {
    try {
      var sf = getCameraManagerStaticFields();
      if (!sf || sf.isNull()) {
        sendLog('error', '诊断', 'CameraManager static_fields 为空');
        return;
      }
      
      var tvPtr = sf.add(CM_STATIC.thermalVision).readPointer();
      sendLog('info', '诊断', '1. thermalVision静态字段: ' + (tvPtr && !tvPtr.isNull() ? tvPtr : 'NULL'));
      
      var vpPtr = sf.add(CM_STATIC.volumeProfile).readPointer();
      sendLog('info', '诊断', '2. volumeProfile静态字段: ' + (vpPtr && !vpPtr.isNull() ? vpPtr : 'NULL'));
      
      if (vpPtr && !vpPtr.isNull()) {
        try {
          var componentsList = vpPtr.add(0x0C).readPointer();
          if (componentsList && !componentsList.isNull()) {
            var listInfo = readListItems(componentsList);
            sendLog('info', '诊断', '3. VolumeProfile.components数量: ' + listInfo.size);
            
            for (var i = 0; i < listInfo.size && i < 20; i++) {
              try {
                var comp = listInfo.items.add(Process.pointerSize * i).readPointer();
                if (!comp || comp.isNull()) continue;
                var compKlass = comp.readPointer();
                if (!compKlass || compKlass.isNull()) continue;
                var namePtr = compKlass.add(0x08).readPointer();
                var compName = namePtr && !namePtr.isNull() ? namePtr.readCString() : '?';
                var compActive = comp.add(0x0C).readU8();
                sendLog('info', '诊断', '   [' + i + '] ' + compName + ' active=' + compActive + ' addr=' + comp);
              } catch(e) { continue; }
            }
          }
        } catch(e) {
          sendLog('warn', '诊断', '读取VolumeProfile.components失败: ' + e.message);
        }
      }
      
      var instance = getCameraManagerInstance();
      if (instance && !instance.isNull()) {
        var fwdRenderData = instance.add(0x20).readPointer();
        sendLog('info', '诊断', '4. fwdRenderData: ' + (fwdRenderData && !fwdRenderData.isNull() ? fwdRenderData : 'NULL'));
        
        var humanCatchFeature = instance.add(0x24).readPointer();
        sendLog('info', '诊断', '5. humanCatchFeature: ' + (humanCatchFeature && !humanCatchFeature.isNull() ? humanCatchFeature : 'NULL'));
        
        if (fwdRenderData && !fwdRenderData.isNull()) {
          try {
            var rendererFeatures = fwdRenderData.add(0x10).readPointer();
            if (rendererFeatures && !rendererFeatures.isNull()) {
              var rfInfo = readListItems(rendererFeatures);
              sendLog('info', '诊断', '6. RendererFeatures数量: ' + rfInfo.size);
              
              for (var j = 0; j < rfInfo.size && j < 20; j++) {
                try {
                  var feature = rfInfo.items.add(Process.pointerSize * j).readPointer();
                  if (!feature || feature.isNull()) continue;
                  var fKlass = feature.readPointer();
                  if (!fKlass || fKlass.isNull()) continue;
                  var fNamePtr = fKlass.add(0x08).readPointer();
                  var fName = fNamePtr && !fNamePtr.isNull() ? fNamePtr.readCString() : '?';
                  var fActive = feature.add(0x0C).readU8();
                  sendLog('info', '诊断', '   [' + j + '] ' + fName + ' active=' + fActive + ' addr=' + feature);
                } catch(e) { continue; }
              }
            }
          } catch(e) {
            sendLog('warn', '诊断', '读取RendererFeatures失败: ' + e.message);
          }
        }
      }
    } catch(e) {
      sendLog('error', '诊断', '诊断失败: ' + e.message);
    }
  }

  function planD_InitThermalVisionRef() {
    sendLog('info', '方案D', '--- 方案D: 调用VolumeProfile.TryGet<ThermalVision>() ---');
    
    var mod = getGameAssembly();
    if (!mod) return false;
    
    try {
      var sf = getCameraManagerStaticFields();
      if (!sf || sf.isNull()) {
        sendLog('error', '方案D', 'CameraManager static_fields 为空');
        return false;
      }
      
      var vpPtr = sf.add(CM_STATIC.volumeProfile).readPointer();
      if (!vpPtr || vpPtr.isNull()) {
        sendLog('error', '方案D', 'volumeProfile为空');
        return false;
      }
      
      var methodInfoAddr = mod.base.add(RVA.VolumeProfile_TryGet_ThermalVision_MethodInfo);
      var methodInfo = methodInfoAddr.readPointer();
      
      if (!methodInfo || methodInfo.isNull()) {
        sendLog('error', '方案D', 'TryGet<ThermalVision> MethodInfo为空');
        return false;
      }
      
      sendLog('info', '方案D', 'MethodInfo: ' + methodInfo);
      
      var outPtr = Memory.alloc(Process.pointerSize);
      outPtr.writePointer(ptr(0));
      
      var tryGetFn = new NativeFunction(
        mod.base.add(RVA.VolumeProfile_TryGet_ThermalVision),
        'int',
        ['pointer', 'pointer', 'pointer']
      );
      
      var result = tryGetFn(vpPtr, outPtr, methodInfo);
      sendLog('info', '方案D', 'TryGet<ThermalVision>返回: ' + result);
      
      var tvFromTryGet = outPtr.readPointer();
      sendLog('info', '方案D', 'TryGet输出ThermalVision: ' + tvFromTryGet);
      
      if (tvFromTryGet && !tvFromTryGet.isNull()) {
        sf.add(CM_STATIC.thermalVision).writePointer(tvFromTryGet);
        thermalVisionComponent = tvFromTryGet;
        sendLog('success', '方案D', '✅ thermalVision引用已初始化: ' + tvFromTryGet);
        
        var active = tvFromTryGet.add(TV_FIELD.active).readU8();
        var dur = readFloatParam(tvFromTryGet, TV_FIELD.Duration);
        sendLog('info', '方案D', '组件状态: active=' + active + ' Duration=' + (dur ? dur.value : '?'));
        return true;
      } else {
        sendLog('warn', '方案D', 'TryGet未找到ThermalVision组件，VolumeProfile中可能没有该组件');
        return false;
      }
    } catch(e) {
      sendLog('error', '方案D', '失败: ' + e.message);
      return false;
    }
  }

  function getForwardRendererDataFromURP() {
    var mod = getGameAssembly();
    if (!mod) return null;
    
    try {
      var fnAddr = mod.base.add(RVA.GraphicsSettings_get_currentRenderPipeline);
      var getCurrentRP = new NativeFunction(fnAddr, 'pointer', ['pointer']);
      
      var pipelineAsset = getCurrentRP(ptr(0));
      if (!pipelineAsset || pipelineAsset.isNull()) {
        sendLog('error', 'URP', 'currentRenderPipeline为空');
        return null;
      }
      
      var assetKlass = pipelineAsset.readPointer();
      var namePtr = assetKlass.add(0x08).readPointer();
      var assetName = namePtr && !namePtr.isNull() ? namePtr.readCString() : '?';
      sendLog('info', 'URP', 'PipelineAsset: ' + pipelineAsset + ' klass=' + assetName);
      
      var rendererData = pipelineAsset.add(0x20).readPointer();
      if (rendererData && !rendererData.isNull()) {
        var rdKlass = rendererData.readPointer();
        var rdNamePtr = rdKlass.add(0x08).readPointer();
        var rdName = rdNamePtr && !rdNamePtr.isNull() ? rdNamePtr.readCString() : '?';
        sendLog('info', 'URP', 'm_RendererData: ' + rendererData + ' klass=' + rdName);
        return rendererData;
      }
      
      var rendererDataList = pipelineAsset.add(0x24).readPointer();
      if (rendererDataList && !rendererDataList.isNull()) {
        var listInfo = readListItems(rendererDataList);
        sendLog('info', 'URP', 'm_RendererDataList数量: ' + listInfo.size);
        
        for (var i = 0; i < listInfo.size && i < 10; i++) {
          var rd = listInfo.items.add(Process.pointerSize * i).readPointer();
          if (!rd || rd.isNull()) continue;
          var rdKlass2 = rd.readPointer();
          var rdNamePtr2 = rdKlass2.add(0x08).readPointer();
          var rdName2 = rdNamePtr2 && !rdNamePtr2.isNull() ? rdNamePtr2.readCString() : '?';
          sendLog('info', 'URP', '  [' + i + '] ' + rdName2 + ' addr=' + rd);
          
          if (rdName2.indexOf('ForwardRenderer') !== -1 || rdName2.indexOf('RendererData') !== -1) {
            sendLog('success', 'URP', '✅ 找到RendererData: ' + rdName2);
            return rd;
          }
        }
        
        if (listInfo.size > 0) {
          var firstRd = listInfo.items.readPointer();
          if (firstRd && !firstRd.isNull()) {
            sendLog('info', 'URP', '使用第一个RendererData: ' + firstRd);
            return firstRd;
          }
        }
      }
      
      sendLog('error', 'URP', '未找到ForwardRendererData');
      return null;
    } catch(e) {
      sendLog('error', 'URP', '获取ForwardRendererData失败: ' + e.message);
      return null;
    }
  }

  function patchAwakeCondition() {
    var mod = getGameAssembly();
    if (!mod) return false;
    
    try {
      var baseAddr = mod.base.add(RVA.Awake_ConditionalJump_RVA);
      
      var bytes = [];
      for (var i = 0; i < 32; i++) {
        bytes.push(baseAddr.add(i).readU8());
      }
      sendLog('info', '补丁', 'Awake条件区域: ' + bytes.map(function(b) { return ('0' + b.toString(16)).slice(-2); }).join(' '));
      
      var cmpOffset = -1;
      for (var i = 0; i < 28; i++) {
        if (bytes[i] === 0x83 && (bytes[i+1] & 0xF8) === 0x78 && bytes[i+2] === 0x04 && bytes[i+3] === 0x05) {
          cmpOffset = i;
          break;
        }
      }
      
      if (cmpOffset === -1) {
        sendLog('error', '补丁', '未找到cmp [reg+4], 5指令');
        return false;
      }
      
      sendLog('info', '补丁', '找到cmp指令 at offset +' + cmpOffset);
      
      var jneOffset = cmpOffset + 4;
      if (bytes[jneOffset] === 0x75) {
        sendLog('info', '补丁', '找到short jne at offset +' + jneOffset + ', 跳转距离=' + bytes[jneOffset+1]);
        var patchAddr = baseAddr.add(jneOffset);
        Memory.protect(patchAddr, 2, 'rwx');
        patchAddr.writeByteArray([0x90, 0x90]);
        sendLog('success', '补丁', '✅ 已补丁short jne → NOP NOP (条件跳转已移除)');
        return true;
      } else if (bytes[jneOffset] === 0x0F && jneOffset + 1 < bytes.length && bytes[jneOffset+1] === 0x85) {
        sendLog('info', '补丁', '找到near jne at offset +' + jneOffset);
        var patchAddr2 = baseAddr.add(jneOffset);
        Memory.protect(patchAddr2, 6, 'rwx');
        patchAddr2.writeByteArray([0x90, 0x90, 0x90, 0x90, 0x90, 0x90]);
        sendLog('success', '补丁', '✅ 已补丁near jne → 6x NOP (条件跳转已移除)');
        return true;
      } else {
        sendLog('warn', '补丁', 'cmp后未找到jne, 字节: ' + ('0' + bytes[jneOffset].toString(16)).slice(-2) + ' ' + ('0' + (jneOffset+1 < bytes.length ? bytes[jneOffset+1].toString(16) : 0)).slice(-2));
        
        for (var j = cmpOffset + 4; j < Math.min(cmpOffset + 12, bytes.length); j++) {
          if (bytes[j] === 0x75 || (bytes[j] === 0x0F && j+1 < bytes.length && bytes[j+1] === 0x85)) {
            jneOffset = j;
            sendLog('info', '补丁', '在offset +' + j + '找到jne');
            if (bytes[j] === 0x75) {
              var pa = baseAddr.add(j);
              Memory.protect(pa, 2, 'rwx');
              pa.writeByteArray([0x90, 0x90]);
              sendLog('success', '补丁', '✅ 已补丁short jne → NOP NOP');
            } else {
              var pa2 = baseAddr.add(j);
              Memory.protect(pa2, 6, 'rwx');
              pa2.writeByteArray([0x90, 0x90, 0x90, 0x90, 0x90, 0x90]);
              sendLog('success', '补丁', '✅ 已补丁near jne → 6x NOP');
            }
            return true;
          }
        }
        return false;
      }
    } catch(e) {
      sendLog('error', '补丁', '补丁失败: ' + e.message);
      return false;
    }
  }

  function planE_FullInit() {
    sendLog('info', '方案E', '--- 方案E: 手动补执行Awake()的Nano6初始化路径 ---');
    
    var mod = getGameAssembly();
    if (!mod) return false;
    
    try {
      patchAwakeCondition();
      
      var sf = getCameraManagerStaticFields();
      if (!sf || sf.isNull()) {
        sendLog('error', '方案E', 'CameraManager static_fields 为空');
        return false;
      }
      
      var vpPtr = sf.add(CM_STATIC.volumeProfile).readPointer();
      if (!vpPtr || vpPtr.isNull()) {
        sendLog('error', '方案E', 'volumeProfile为空，无法初始化');
        return false;
      }
      
      var componentsList = vpPtr.add(0x0C).readPointer();
      var listInfo = readListItems(componentsList);
      sendLog('info', '方案E', 'VolumeProfile.components数量: ' + listInfo.size);
      
      var tvInProfile = null;
      for (var i = 0; i < listInfo.size && i < 30; i++) {
        try {
          var comp = listInfo.items.add(Process.pointerSize * i).readPointer();
          if (!comp || comp.isNull()) continue;
          var compKlass = comp.readPointer();
          if (!compKlass || compKlass.isNull()) continue;
          var namePtr = compKlass.add(0x08).readPointer();
          var compName = namePtr && !namePtr.isNull() ? namePtr.readCString() : '?';
          sendLog('info', '方案E', '  Component[' + i + ']: ' + compName + ' addr=' + comp);
          if (compName === 'ThermalVision') {
            tvInProfile = comp;
            sendLog('success', '方案E', '在VolumeProfile中找到ThermalVision: ' + comp);
          }
        } catch(e) { continue; }
      }
      
      if (tvInProfile) {
        sf.add(CM_STATIC.thermalVision).writePointer(tvInProfile);
        thermalVisionComponent = tvInProfile;
        sendLog('success', '方案E', '✅ thermalVision引用已从VolumeProfile设置: ' + tvInProfile);
      } else {
        sendLog('warn', '方案E', 'VolumeProfile中没有ThermalVision组件');
      }
      
      var instance = getCameraManagerInstance();
      if (!instance || instance.isNull()) {
        sendLog('error', '方案E', 'CameraManager单例为空');
        return !!tvInProfile;
      }
      
      var fwdRenderData = instance.add(0x20).readPointer();
      if (fwdRenderData && !fwdRenderData.isNull()) {
        sendLog('info', '方案E', 'fwdRenderData已存在: ' + fwdRenderData);
      } else {
        sendLog('info', '方案E', 'fwdRenderData为空，从URP管线获取...');
        fwdRenderData = getForwardRendererDataFromURP();
        if (fwdRenderData) {
          instance.add(0x20).writePointer(fwdRenderData);
          sendLog('success', '方案E', '✅ fwdRenderData已从URP管线设置: ' + fwdRenderData);
        } else {
          sendLog('error', '方案E', '无法获取ForwardRendererData');
        }
      }
      
      var humanCatchFeature = instance.add(0x24).readPointer();
      if (humanCatchFeature && !humanCatchFeature.isNull()) {
        sendLog('info', '方案E', 'humanCatchFeature已存在: ' + humanCatchFeature);
      } else {
        sendLog('info', '方案E', 'humanCatchFeature为空，尝试从RendererFeatures查找...');
        
        if (fwdRenderData && !fwdRenderData.isNull()) {
          var rendererFeatures = fwdRenderData.add(0x10).readPointer();
          if (rendererFeatures && !rendererFeatures.isNull()) {
            var rfInfo = readListItems(rendererFeatures);
            sendLog('info', '方案E', 'RendererFeatures数量: ' + rfInfo.size);
            
            for (var j = 0; j < rfInfo.size && j < 30; j++) {
              try {
                var feature = rfInfo.items.add(Process.pointerSize * j).readPointer();
                if (!feature || feature.isNull()) continue;
                var fKlass = feature.readPointer();
                if (!fKlass || fKlass.isNull()) continue;
                var fNamePtr = fKlass.add(0x08).readPointer();
                var fName = fNamePtr && !fNamePtr.isNull() ? fNamePtr.readCString() : '?';
                
                sendLog('info', '方案E', '  Feature[' + j + ']: ' + fName + ' addr=' + feature);
                if (fName.indexOf('ThermalVision') !== -1 || fName.indexOf('HumanCatch') !== -1 || fName.indexOf('humanCatch') !== -1) {
                  instance.add(0x24).writePointer(feature);
                  humanCatchFeature = feature;
                  sendLog('success', '方案E', '✅ 找到并设置humanCatchFeature: ' + fName);
                  break;
                }
              } catch(e) { continue; }
            }
          }
        }
        
        if (!humanCatchFeature || humanCatchFeature.isNull()) {
          sendLog('warn', '方案E', '未找到humanCatchFeature，热成像渲染可能不完整');
        }
      }
      
      return true;
    } catch(e) {
      sendLog('error', '方案E', '失败: ' + e.message);
      return false;
    }
  }

  function enableThermalVisionByComponent() {
    try {
      diagnoseThermalVisionPipeline();
      
      var tv = getThermalVisionComponent();
      if (!tv || tv.isNull()) {
        sendLog('warn', '热成像B', 'ThermalVision组件未找到，尝试方案E(补丁+URP+全初始化)...');
        
        var eOk = planE_FullInit();
        if (eOk) {
          tv = getThermalVisionComponent();
        }
        
        if (!tv || tv.isNull()) {
          sendLog('warn', '热成像B', '方案E失败，尝试方案D...');
          var dOk = planD_InitThermalVisionRef();
          if (dOk) {
            tv = getThermalVisionComponent();
          }
        }
        
        if (!tv || tv.isNull()) {
          sendLog('error', '热成像B', '所有方案均失败，ThermalVision组件无法初始化');
          return false;
        }
      }
      
      tv.add(TV_FIELD.active).writeU8(1);
      
      if (!writeFloatParam(tv, TV_FIELD.Duration, state.duration)) {
        sendLog('error', '热成像B', '写入Duration失败');
        return false;
      }
      
      var dur = readFloatParam(tv, TV_FIELD.Duration);
      var active = tv.add(TV_FIELD.active).readU8();
      sendLog('info', '热成像B', '验证: Duration=' + (dur ? dur.value : '?') + ' override=' + (dur ? dur.overrideState : '?') + ' active=' + active);
      
      sendLog('success', '热成像B', '✅ 方案B: 直接修改组件参数完成');
      sendStatus('thermal_vision', true);
      return true;
    } catch(e) {
      sendLog('error', '热成像B', '方案B失败: ' + e.message);
      return false;
    }
  }

  function disableThermalVisionByComponent() {
    try {
      var tv = getThermalVisionComponent();
      if (!tv || tv.isNull()) return true;
      
      writeFloatParam(tv, TV_FIELD.Duration, 0.0);
      tv.add(TV_FIELD.active).writeU8(0);
      
      sendLog('info', '热成像B', '❌ 方案B: 热成像已关闭');
      sendStatus('thermal_vision', false);
      return true;
    } catch(e) {
      sendLog('error', '热成像B', '方案B关闭失败: ' + e.message);
      return false;
    }
  }

  function enableThermalVision() {
    try {
      var gameState = getGameState();
      if (!gameState) {
        sendLog('error', '热成像', '无法获取游戏状态');
        return false;
      }
      
      sendLog('info', '热成像', '游戏状态:');
      sendLog('info', '热成像', '  - 在游戏中: ' + gameState.inGame);
      sendLog('info', '热成像', '  - 游戏模式: ' + gameState.gameModeName + ' (' + gameState.gameMode + ')');
      sendLog('info', '热成像', '  - 当前玩家: ' + gameState.myPlayer);
      
      if (!gameState.inGame) {
        sendLog('error', '热成像', '❌ 不在游戏中，无法启用热成像');
        return false;
      }
      
      var mi = findSetThermalVisionMethodInfo();
      
      if (mi && setThermalVision) {
        sendLog('info', '热成像', '方案A: 调用SetThermalVision(' + state.duration + ', ' + (state.showHuman ? 1 : 0) + ', ' + mi + ')...');
        try {
          setThermalVision(state.duration, state.showHuman ? 1 : 0, mi);
          sendLog('success', '热成像', '✅ 方案A: SetThermalVision调用完成');
        } catch(e) {
          sendLog('error', '热成像', '方案A调用失败: ' + e.message + '，切换到方案B');
          return enableThermalVisionByComponent();
        }
      } else {
        sendLog('warn', '热成像', 'MethodInfo*未找到，使用方案B（直接修改组件）');
        return enableThermalVisionByComponent();
      }
      
      var tv = getThermalVisionComponent();
      if (tv && !tv.isNull()) {
        var dur = readFloatParam(tv, TV_FIELD.Duration);
        var active = tv.add(TV_FIELD.active).readU8();
        sendLog('info', '热成像', '验证: Duration=' + (dur ? dur.value : '?') + ' override=' + (dur ? dur.overrideState : '?') + ' active=' + active);
        
        if (dur && Math.abs(dur.value - state.duration) < 0.1 && active) {
          sendLog('success', '热成像', '✅ 热成像效果已确认生效！持续 ' + dur.value + ' 秒');
        } else {
          sendLog('warn', '热成像', '⚠️ 调用完成但Duration不匹配(期望=' + state.duration + ')，可能需要其他条件');
        }
      }
      
      sendStatus('thermal_vision', true);
      return true;
    } catch(e) {
      sendLog('error', '热成像', '启用失败: ' + e.message);
      sendLog('error', '热成像', '错误堆栈: ' + e.stack);
      return false;
    }
  }

  function disableThermalVision() {
    try {
      var mi = findSetThermalVisionMethodInfo();
      
      if (mi && setThermalVision) {
        try {
          setThermalVision(0.0, 0, mi);
          sendLog('info', '热成像', '❌ 方案A: 热成像已关闭');
        } catch(e) {
          sendLog('warn', '热成像', '方案A关闭失败，使用方案B');
          return disableThermalVisionByComponent();
        }
      } else {
        return disableThermalVisionByComponent();
      }
      
      sendStatus('thermal_vision', false);
      return true;
    } catch(e) {
      sendLog('error', '热成像', '关闭失败: ' + e.message);
      return false;
    }
  }

  // ================================================================
  // 主循环
  // ================================================================
  function mainLoop() {
    if (!state.enabled) return;

    var now = Date.now();

    // 检测T键按下
    if (isKeyPressed()) {
      // 检查冷却
      var timeSinceLastTrigger = now - state.lastTriggerTime;
      if (timeSinceLastTrigger >= state.cooldown) {
        // 启用热成像
        if (enableThermalVision()) {
          state.lastTriggerTime = now;
        }
      } else {
        // 冷却中
        var remainingTime = (state.cooldown - timeSinceLastTrigger) / 1000;
        sendLog('warn', '热成像', '⏳ 冷却中，剩余 ' + remainingTime.toFixed(1) + ' 秒');
      }
    }
  }

  // ================================================================
  // 启用/禁用功能
  // ================================================================
  function enable() {
    if (state.enabled) return;
    if (!init()) {
      sendLog('error', '热成像', '初始化失败，无法启用');
      return;
    }

    state.enabled = true;
    state.lastTriggerTime = 0;

    // 启动定时器 (50ms检测一次)
    state.timer = setInterval(mainLoop, 50);

    sendLog('info', '热成像', '✅ 功能已启用');
    sendLog('info', '热成像', '按键: T | 持续: ' + state.duration + '秒 | 显示: 仅敌人');
    sendStatus('thermal_vision_enabled', true);
  }

  function disable() {
    if (!state.enabled) return;

    state.enabled = false;

    // 停止定时器
    if (state.timer) {
      clearInterval(state.timer);
      state.timer = null;
    }

    // 关闭热成像
    disableThermalVision();

    sendLog('info', '热成像', '❌ 功能已禁用');
    sendStatus('thermal_vision_enabled', false);
  }

  // ================================================================
  // RPC 导出
  // ================================================================
  rpc.exports = {
    enable: function() {
      enable();
      return { ok: true };
    },

    disable: function() {
      disable();
      return { ok: true };
    },

    setconfig: function(duration, showHuman) {
      state.duration = duration || 3.0;
      state.showHuman = showHuman || false;
      state.cooldown = (duration || 3.0) * 1000;
      sendLog('info', '配置', '持续: ' + state.duration + '秒, 显示人类: ' + state.showHuman);
      return { ok: true };
    },

    getstatus: function() {
      var now = Date.now();
      var timeSinceLastTrigger = now - state.lastTriggerTime;
      var cooldownRemaining = Math.max(0, (state.cooldown - timeSinceLastTrigger) / 1000);

      return {
        enabled: state.enabled,
        duration: state.duration,
        showHuman: state.showHuman,
        cooldownRemaining: cooldownRemaining,
        canTrigger: timeSinceLastTrigger >= state.cooldown,
      };
    },

    checkgamestate: function() {
      var gameState = getGameState();
      if (!gameState) {
        return { ok: false, message: '无法获取游戏状态' };
      }
      return {
        ok: true,
        inGame: gameState.inGame,
        gameMode: gameState.gameMode,
        gameModeName: gameState.gameModeName,
        myPlayer: gameState.myPlayer.toString(),
        thermalVision: gameState.thermalVision.toString()
      };
    }
  };

  // ================================================================
  // 启动提示
  // ================================================================
  console.log('');
  console.log('========================================');
  console.log('  热成像透视功能 v2.3 (补丁+URP管线+全模式初始化)');
  console.log('  实现: 方案A(SetThermalVision) → 方案B(组件修改) → 方案D(TryGet) → 方案E(手动初始化)');
  console.log('按键: T键');
  console.log('持续时间: ' + state.duration + '秒');
  console.log('显示范围: 仅敌人');
  console.log('适用模式: 所有模式 ✅');
  console.log('适用角色: 所有角色 ✅');
  console.log('移动限制: 无（可在移动中使用）');
  console.log('========================================');
  console.log('');

})();
