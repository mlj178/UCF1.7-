(function() {
  'use strict';

  // ================================================================
  // 无敌模式 v1.0 — Hook Entity.OnEntityHurt 实现仅玩家不掉血
  //
  // 原理:
  //   1. Interceptor.attach(Entity_OnEntityHurt)
  //   2. 在 onEnter 中检查 this(Entity) 是否为 myPlayer
  //   3. 如果是玩家 → 修改栈上 DamageEventData.type = 4 (跳过掉血)
  //   4. 如果不是玩家 → 正常执行
  //
  // RVA 来源: IDA Pro + dump.cs (Il2CppDumper)
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
        console.log('[系统] 未找到 GameAssembly.dll');
        return null;
      }
      _gameAssembly = mod;
      console.log('[系统] GameAssembly.dll: base=' + mod.base + ' size=' + mod.size);
      return mod;
    } catch(e) {
      console.log('[系统] 获取模块失败: ' + e.message);
      return null;
    }
  }

  // ================================================================
  // RVA 常量
  // ================================================================
  var RVA = {
    SingletonGet:                    0x4A8170,   // Singleton<GameManager>.get_instance
    GM_Singleton_MethodInfo:         0xE1CE64,   // MethodInfo* 元数据指针
    Player_get_isMyPlayer:           0xB55FD0,   // bool (Player*, MethodInfo*)
    Entity_get_isDead:               0xB400E0,   // bool (Entity*, MethodInfo*)
    Entity_get_team:                 0x1E0070,   // Team/int32 (Entity*, MethodInfo*)
    Entity_OnEntityHurt:             0xB3F470,   // void (Entity*, DamageEventData, MethodInfo*)
    Component_get_transform:         0x32CF40,   // Transform* (Component*, MethodInfo*)
    Transform_get_position:          0x3F42B0,   // Vector3* (Vector3* ret, Transform*, MethodInfo*)
  };

  // ================================================================
  // 字段偏移
  // ================================================================
  var OFF = {
    GM_allPlayers:      0x1C,   // Player[]
    GM_playersBL:       0x20,   // List<Player>
    GM_playersGR:       0x28,   // List<Player>
    E_team:             0x20,   // Team (int32)

    Arr_len:            0x0C,   // il2cpp_array_size_t
    Arr_data:           0x10,   // data start
    List_items:         0x08,   // T[] _items
    List_size:          0x0C,   // int _size
    ptrSize:            4,

    // DamageEventData 结构体偏移 (IL2CPP x86)
    // DamageEventData { Entity* attacker(4B), Entity* victim(4B), int type(4B), ... }
    Dmg_type:           0x08,   // type 字段偏移 (attacker=0x00, victim=0x04, type=0x08)
  };

  // ================================================================
  // NativeFunction 缓存
  // ================================================================
  var singletonGetter = null;
  var isMyPlayerFn = null;
  var isDeadFn = null;

  // ================================================================
  // 模块状态
  // ================================================================
  var cachedMyPlayer = null;
  var hurtHook = null;
  var refreshTimer = null;
  var enabled = false;

  // ================================================================
  // 初始化 NativeFunction
  // ================================================================
  function initNativeFunctions() {
    var mod = getGameAssembly();
    if (!mod) return false;
    var base = mod.base;

    try {
      singletonGetter = new NativeFunction(base.add(RVA.SingletonGet), 'pointer', ['pointer']);
    } catch(e) {
      sendLog('error', '初始化', 'singletonGetter 失败: ' + e.message);
      return false;
    }

    try {
      isMyPlayerFn = new NativeFunction(base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer']);
    } catch(e) {
      sendLog('error', '初始化', 'isMyPlayerFn 失败: ' + e.message);
      return false;
    }

    try {
      isDeadFn = new NativeFunction(base.add(RVA.Entity_get_isDead), 'bool', ['pointer', 'pointer']);
    } catch(e) {
      sendLog('error', '初始化', 'isDeadFn 失败: ' + e.message);
      return false;
    }

    sendLog('success', '初始化', 'NativeFunction 全部就绪');
    return true;
  }

  // ================================================================
  // 获取 GameManager 单例
  // ================================================================
  function getGM() {
    try {
      var base = getGameAssembly().base;
      var mi = base.add(RVA.GM_Singleton_MethodInfo).readPointer();
      if (mi.isNull()) {
        return singletonGetter(ptr(0));
      }
      var gm = singletonGetter(mi);
      if (gm.isNull()) return null;
      return gm;
    } catch(e) {
      return null;
    }
  }

  // ================================================================
  // 工具函数 — 读取列表/数组/玩家
  // ================================================================
  function readList(listPtr) {
    var result = [];
    if (!listPtr || listPtr.isNull()) return result;
    try {
      var items = listPtr.add(OFF.List_items).readPointer();
      if (!items || items.isNull()) return result;
      var count = listPtr.add(OFF.List_size).readS32();
      for (var i = 0; i < count; i++) {
        var elem = items.add(OFF.Arr_data + i * OFF.ptrSize).readPointer();
        if (elem && !elem.isNull()) result.push(elem);
      }
    } catch(e) {}
    return result;
  }

  function readArray(arrPtr) {
    var result = [];
    if (!arrPtr || arrPtr.isNull()) return result;
    try {
      var len = arrPtr.add(OFF.Arr_len).readU32();
      for (var i = 0; i < len; i++) {
        var elem = arrPtr.add(OFF.Arr_data + i * OFF.ptrSize).readPointer();
        if (elem && !elem.isNull()) result.push(elem);
      }
    } catch(e) {}
    return result;
  }

  function isValidPlayer(pp) {
    if (!pp || pp.isNull()) return false;
    try {
      var team = pp.add(OFF.E_team).readS32();
      return (team === 0 || team === 1 || team === 2);
    } catch(e) { return false; }
  }

  function getAllPlayers(gm) {
    var map = {};
    var arr = readArray(gm.add(OFF.GM_allPlayers).readPointer());
    for (var i = 0; i < arr.length; i++) {
      if (isValidPlayer(arr[i])) map[arr[i].toString()] = arr[i];
    }
    var bl = readList(gm.add(OFF.GM_playersBL).readPointer());
    for (var i = 0; i < bl.length; i++) {
      if (isValidPlayer(bl[i])) map[bl[i].toString()] = bl[i];
    }
    var gr = readList(gm.add(OFF.GM_playersGR).readPointer());
    for (var i = 0; i < gr.length; i++) {
      if (isValidPlayer(gr[i])) map[gr[i].toString()] = gr[i];
    }
    return Object.values(map);
  }

  function findMyPlayer() {
    try {
      var gm = getGM();
      if (!gm || gm.isNull()) return null;
      var all = getAllPlayers(gm);
      for (var i = 0; i < all.length; i++) {
        try {
          if (isMyPlayerFn(all[i], ptr(0))) return all[i];
        } catch(e) {}
      }
    } catch(e) {}
    return null;
  }

  // ================================================================
  // 核心 Hook — Entity_OnEntityHurt
  //
  // 函数签名 (__cdecl):
  //   void Entity__OnEntityHurt(Entity_o* this, DamageEventData_o eventData, const MethodInfo* method)
  //
  // 关键汇编逻辑 (IDA):
  //   0xB3F473  cmp [ebp+eventData.fields.type], 4
  //   0xB3F477  jz skip  (type==4 则跳过掉血)
  //   0xB3F47C  mov ecx, [eax+1Ch]  ← _healthData_k__BackingField
  //
  // 方案: 栈上修改 eventData.type = 4 → 函数自动跳过掉血
  //
  // __cdecl 函数入口栈布局 (onEnter 时):
  //   [ESP+0x00] = return address     (由 CALL 压入, 4B)
  //   [ESP+0x04] = this               (第一个参数, 4B)
  //   [ESP+0x08] = eventData.attacker (结构体开始, 4B)
  //   [ESP+0x0C] = eventData.victim   (4B)
  //   [ESP+0x10] = eventData.type     (4B)  ← 要写的位置!
  //   [ESP+0x14] = ... 后续字段 ...
  //   [ESP+0x??] = MethodInfo*        (第三个参数)
  // ================================================================
  function installHooks(base) {
    var entityHurtAddr = base.add(RVA.Entity_OnEntityHurt);

    var diagCount = 0;

    var hookHandler = {
      onEnter: function(args) {
        var entity = args[0];
        if (!entity || entity.isNull()) return;

        if (diagCount < 20) {
          sendLog('debug', 'HP', '[诊断] Hook触发! entity=' + entity + ' cachedMyPlayer=' + (cachedMyPlayer || 'null'));
          diagCount++;
        }

        if (!cachedMyPlayer || cachedMyPlayer.isNull()) {
          return;
        }

        var isMyPlayer = entity.equals(cachedMyPlayer);

        if (diagCount < 20) {
          sendLog('debug', 'HP', '[诊断] isMyPlayer=' + isMyPlayer + ' entity=' + entity + ' myPlayer=' + cachedMyPlayer);
        }

        if (isMyPlayer) {
          var espPtr = ptr(this.context.esp.toString());
          var structStart = espPtr.add(8);
          var typeFieldAddr = structStart.add(OFF.Dmg_type);

          var oldType = typeFieldAddr.readS32();
          typeFieldAddr.writeS32(4);

          if (diagCount < 20) {
            sendLog('debug', 'HP', '[诊断] 修改type: ' + oldType + ' -> 4, ESP=' + espPtr + ' typeAddr=' + typeFieldAddr);
          }

          if (moduleLogCounts['HP'] < 30) {
            sendLog('info', 'HP', '玩家掉血已拦截! (oldType=' + oldType + ')');
          }
        }
      }
    };

    hurtHook = Interceptor.attach(entityHurtAddr, hookHandler);
    sendLog('success', 'HP', 'Entity_OnEntityHurt Hook 已安装 (RVA: 0xB3F470)');

    // 同时 Hook Player_OnEntityHurt 防止虚函数覆盖
    var playerHurtAddr = base.add(0xB516B0);
    try {
      Interceptor.attach(playerHurtAddr, hookHandler);
      sendLog('success', 'HP', 'Player_OnEntityHurt 兜底Hook已安装 (RVA: 0xB516B0)');
    } catch(e) {
      sendLog('warn', 'HP', 'Player_OnEntityHurt Hook失败: ' + e.message + ' (不影响)');
    }
  }

  // ================================================================
  // myPlayer 刷新机制
  // ================================================================
  function startRefresh() {
    if (refreshTimer) return;
    refreshTimer = setInterval(function() {
      if (!cachedMyPlayer || cachedMyPlayer.isNull()) {
        var found = findMyPlayer();
        if (found && !found.isNull()) {
          cachedMyPlayer = found;
          sendLog('info', 'HP', '已找到玩家: ' + found);
        }
      }

      if (cachedMyPlayer && !cachedMyPlayer.isNull()) {
        try {
          var gm = getGM();
          if (gm && !gm.isNull()) {
            var all = getAllPlayers(gm);
            var found = false;
            for (var i = 0; i < all.length; i++) {
              if (all[i].equals(cachedMyPlayer)) { found = true; break; }
            }
            if (!found) {
              sendLog('info', 'HP', '玩家已离开（房间切换），重置');
              cachedMyPlayer = null;
            }
          }
        } catch(e) {
          cachedMyPlayer = null;
        }
      }
    }, 2000);
  }

  function stopRefresh() {
    if (refreshTimer) {
      clearInterval(refreshTimer);
      refreshTimer = null;
    }
  }

  // ================================================================
  // 公开接口
  // ================================================================
  var godModeModule = {
    enable: function() {
      if (enabled) {
        sendLog('info', 'HP', '无敌模式已启用，跳过');
        return;
      }

      var mod = getGameAssembly();
      if (!mod) {
        sendLog('error', 'HP', '未找到 GameAssembly.dll');
        return;
      }

      if (!initNativeFunctions()) {
        sendLog('error', 'HP', 'NativeFunction 初始化失败');
        return;
      }

      cachedMyPlayer = findMyPlayer();
      if (cachedMyPlayer) {
        sendLog('info', 'HP', '已找到玩家: ' + cachedMyPlayer);
      } else {
        sendLog('info', 'HP', '等待玩家出现（自动刷新中）...');
      }

      installHooks(mod.base);
      startRefresh();

      enabled = true;
      sendLog('success', 'HP', '无敌模式已启用!');
      sendStatus('无敌HP', true);
    },

    disable: function() {
      if (!enabled) return;

      if (hurtHook) {
        try { hurtHook.detach(); } catch(e) {}
        hurtHook = null;
      }
      stopRefresh();
      cachedMyPlayer = null;
      enabled = false;
      sendLog('info', 'HP', '无敌模式已禁用');
      sendStatus('无敌HP', false);
    },

    toggle: function() {
      if (enabled) this.disable();
      else this.enable();
    },

    isEnabled: function() { return enabled; },

    getStatus: function() {
      return {
        enabled: enabled,
        hookInstalled: hurtHook !== null,
        myPlayer: cachedMyPlayer ? cachedMyPlayer.toString() : null,
      };
    },
  };

  // ================================================================
  // rpc.exports — Python UI 调用接口
  // ================================================================
  rpc.exports = {
    godmodeEnable: function() { godModeModule.enable(); return 'ok'; },
    godmode_enable: function() { godModeModule.enable(); return 'ok'; },
    godmodeDisable: function() { godModeModule.disable(); return 'ok'; },
    godmode_disable: function() { godModeModule.disable(); return 'ok'; },
    godmodeToggle: function() { godModeModule.toggle(); return godModeModule.isEnabled() ? 'enabled' : 'disabled'; },
    godmode_toggle: function() { godModeModule.toggle(); return godModeModule.isEnabled() ? 'enabled' : 'disabled'; },
    godmodeStatus: function() { return godModeModule.isEnabled() ? 'enabled' : 'disabled'; },
    godmode_status: function() { return godModeModule.isEnabled() ? 'enabled' : 'disabled'; },
    godmodeGetStatus: function() { return JSON.stringify(godModeModule.getStatus()); },
    godmode_get_status: function() { return JSON.stringify(godModeModule.getStatus()); },
  };

  console.log('[HP] 无敌模式脚本加载完成');
  sendLog('info', 'HP', '脚本已加载，等待 UI 激活...');
})();
