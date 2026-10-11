// Local helpers for this feature only.
var modules = {};
var __localMaxLogsPerModule = 10;
var __localModuleLogCounts = {};

function sendRoutedLog(level, module, message, audience, devDetail) {
  try {
    if (!__localModuleLogCounts[module]) __localModuleLogCounts[module] = 0;
    if (__localModuleLogCounts[module] >= __localMaxLogsPerModule) return;
    if (module !== '??' && __localModuleLogCounts[module] === __localMaxLogsPerModule - 1) {
      __localModuleLogCounts[module]++;
      send({ type: 'log', level: 'info', module: module, message: message + ' (???????)', audience: audience || 'dev', dev_detail: devDetail || '' });
      return;
    }
    __localModuleLogCounts[module]++;
    send({ type: 'log', level: level, module: module, message: message, audience: audience || 'dev', dev_detail: devDetail || '' });
  } catch (_) {}
}

function sendUserLog(level, module, message) {
  sendRoutedLog(level, module, message, 'user', '');
}

function sendDevLog(level, module, message, devDetail) {
  sendRoutedLog(level, module, message, 'dev', devDetail || '');
}

function sendBothLog(level, module, message, devDetail) {
  sendRoutedLog(level, module, message, 'both', devDetail || '');
}

function sendLog(level, module, message) {
  sendDevLog(level, module, message);
}

function sendLogFile(level, module, message) {
  try { send({ type: 'log_file', level: level, module: module, message: message, audience: 'dev' }); } catch (_) {}
}

function sendStatus(feature, enabled) {
  try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (_) {}
}

var __localGameAssemblyCache = null;
var __localGameAssemblyLogged = false;

function getGameAssembly() {
  try {
    if (__localGameAssemblyCache) return __localGameAssemblyCache;
    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) {
      sendDevLog('error', '??', '??? GameAssembly.dll', 'GameAssembly.dll not found');
      return null;
    }
    __localGameAssemblyCache = mod;
    if (!__localGameAssemblyLogged) {
      __localGameAssemblyLogged = true;
      sendDevLog('info', '??', 'GameAssembly.dll: base=' + mod.base + ' size=' + mod.size, 'GameAssembly module located');
    }
    return mod;
  } catch (e) {
    sendDevLog('error', '??', '??????: ' + e.message, 'getGameAssembly failed: ' + e.message);
    return null;
  }
}

function readPtr(addr) {
  try { if (!addr || addr.isNull()) return null; var v = addr.readPointer(); return (v && !v.isNull()) ? v : null; } catch (_) { return null; }
}

function readI32(addr) { try { return addr ? addr.readS32() : null; } catch (_) { return null; } }
function readF32(addr) { try { return addr ? addr.readFloat() : null; } catch (_) { return null; } }
function readU8(addr) { try { return addr ? addr.readU8() : null; } catch (_) { return null; } }

var __localCleanupCallbacks = [];
function registerCleanup(callback) {
  if (typeof callback !== 'function') return false;
  __localCleanupCallbacks.push(callback);
  return true;
}

// godmode.js - 金刚不坏 — Hook Entity.OnEntityHurt + Player.OnEntityHurt
// 通过ESP读取伤害结构体，将type字段改为4（无敌类型）

modules.godmode = (function() {
  var enabled = false;
  var hurtHook = null;
  var playerHurtHook = null;
  var refreshTimer = null;
  var cachedMyPlayer = null;
  var isMyPlayerFn = null;
  var isDeadFn = null;
  var singletonGetter = null;
  var roomShuttingDown = true;
  var lifecycleHooks = [];

  var RVA = {
    SingletonGet:                    0x4A8170,
    GM_Singleton_MethodInfo:         0xE1CE64,
    Player_get_isMyPlayer:           0xB55FD0,
    Entity_get_isDead:               0xB400E0,
    Entity_get_team:                 0x1E0070,
    Entity_OnEntityHurt:             0xB3F470,
    Component_get_transform:         0x32CF40,
    Transform_get_position:          0x3F42B0,
  };

  var OFF = {
    GM_allPlayers:      0x1C,
    GM_playersBL:       0x20,
    GM_playersGR:       0x28,
    E_team:             0x20,
    Arr_len:            0x0C,
    Arr_data:           0x10,
    List_items:         0x08,
    List_size:          0x0C,
    ptrSize:            4,
    Dmg_type:           0x08,
  };

  function initNativeFunctions() {
    var mod = getGameAssembly();
    if (!mod) return false;
    var base = mod.base;
    try {
      singletonGetter = new NativeFunction(base.add(RVA.SingletonGet), 'pointer', ['pointer']);
    } catch(e) { sendLog('error', 'HP', 'singletonGetter 失败: ' + e.message); return false; }
    try {
      isMyPlayerFn = new NativeFunction(base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer']);
    } catch(e) { sendLog('error', 'HP', 'isMyPlayerFn 失败: ' + e.message); return false; }
    try {
      isDeadFn = new NativeFunction(base.add(RVA.Entity_get_isDead), 'bool', ['pointer', 'pointer']);
    } catch(e) { sendLog('error', 'HP', 'isDeadFn 失败: ' + e.message); return false; }
    sendLog('success', 'HP', 'NativeFunction 全部就绪');
    return true;
  }

  function getGM() {
    if (roomShuttingDown) return null;
    try {
      var base = getGameAssembly().base;
      var mi = base.add(RVA.GM_Singleton_MethodInfo).readPointer();
      if (mi.isNull()) return singletonGetter(ptr(0));
      var gm = singletonGetter(mi);
      if (gm.isNull()) return null;
      return gm;
    } catch(e) { return null; }
  }

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
    if (roomShuttingDown) return null;
    try {
      var gm = getGM();
      if (!gm || gm.isNull()) return null;
      var all = getAllPlayers(gm);
      for (var i = 0; i < all.length; i++) {
        try { if (isMyPlayerFn(all[i], ptr(0))) return all[i]; } catch(e) {}
      }
    } catch(e) {}
    return null;
  }

  function installHooks(base) {
    function beginRoomShutdown() {
      roomShuttingDown = true;
      cachedMyPlayer = null;
    }

    var entityHurtAddr = base.add(RVA.Entity_OnEntityHurt);
    var hookHandler = {
      onEnter: function(args) {
        if (roomShuttingDown) return;
        var entity = args[0];
        if (!entity || entity.isNull()) return;
        if (!cachedMyPlayer || cachedMyPlayer.isNull()) return;
        var isMyPlayer = entity.equals(cachedMyPlayer);
        if (isMyPlayer) {
          var espPtr = ptr(this.context.esp.toString());
          var structStart = espPtr.add(8);
          var typeFieldAddr = structStart.add(OFF.Dmg_type);
          var oldType = typeFieldAddr.readS32();
          typeFieldAddr.writeS32(4);
          sendLog('info', 'HP', '玩家掉血已拦截! (oldType=' + oldType + ')');
        }
      }
    };
    hurtHook = Interceptor.attach(entityHurtAddr, hookHandler);
    sendLog('success', 'HP', 'Entity_OnEntityHurt Hook 已安装 (RVA: 0xB3F470)');
    var playerHurtAddr = base.add(0xB516B0);
    try {
      playerHurtHook = Interceptor.attach(playerHurtAddr, hookHandler);
      sendLog('success', 'HP', 'Player_OnEntityHurt 兜底Hook已安装 (RVA: 0xB516B0)');
    } catch(e) { sendLog('warn', 'HP', 'Player_OnEntityHurt Hook失败: ' + e.message + ' (不影响)'); }
    try {
      lifecycleHooks.push(Interceptor.attach(base.add(0xAF6A00), {
        onEnter: function() {
          roomShuttingDown = false;
        }
      }));
    } catch(e) {}
    try {
      lifecycleHooks.push(Interceptor.attach(base.add(0xAF9A90), {
        onEnter: function() {
          roomShuttingDown = false;
          cachedMyPlayer = null;
        }
      }));
    } catch(e) {}
    try { lifecycleHooks.push(Interceptor.attach(base.add(0xAEE850), { onEnter: beginRoomShutdown })); } catch(e) {}
    try { lifecycleHooks.push(Interceptor.attach(base.add(0xAFB6F0), { onEnter: beginRoomShutdown })); } catch(e) {}
  }

  function startRefresh() {
    if (refreshTimer) return;
    refreshTimer = setInterval(function() {
      if (roomShuttingDown) return;
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
        } catch(e) { cachedMyPlayer = null; }
      }
    }, 2000);
  }

  function stopRefresh() {
    if (refreshTimer) {
      clearInterval(refreshTimer);
      refreshTimer = null;
    }
  }

  return {
    enable: function() {
      if (enabled) {
        sendLog('info', 'HP', '无敌模式已启用，跳过');
        return;
      }
      var mod = getGameAssembly();
      if (!mod) {
        sendBothLog('error', 'HP', '无敌暂未就绪，请重新连接游戏后重试', 'Invincibility GameAssembly.dll not found');
        return;
      }
      if (!initNativeFunctions()) {
        sendBothLog('error', 'HP', '无敌初始化失败，请稍后重试', 'Invincibility NativeFunction init failed');
        return;
      }
      installHooks(mod.base);
      cachedMyPlayer = findMyPlayer();
      if (cachedMyPlayer) {
        sendLog('info', 'HP', '已找到玩家: ' + cachedMyPlayer);
      } else {
        sendLog('info', 'HP', '等待玩家出现（自动刷新中）...');
      }
      startRefresh();
      enabled = true;
      sendLog('success', 'HP', '无敌模式已启用!');
      sendStatus('godmode', true);
    },
    disable: function() {
      if (!enabled) return;
      if (hurtHook) { try { hurtHook.detach(); } catch(e) {} hurtHook = null; }
      if (playerHurtHook) { try { playerHurtHook.detach(); } catch(e) {} playerHurtHook = null; }
      for (var i = 0; i < lifecycleHooks.length; i++) { try { lifecycleHooks[i].detach(); } catch(e) {} }
      lifecycleHooks = [];
      stopRefresh();
      roomShuttingDown = true;
      cachedMyPlayer = null;
      enabled = false;
      sendLog('info', 'HP', '无敌模式已禁用');
      sendStatus('godmode', false);
    },
    isEnabled: function() { return enabled; },
    getStatus: function() {
      return {
        enabled: enabled,
        hookInstalled: hurtHook !== null,
        myPlayer: cachedMyPlayer ? cachedMyPlayer.toString() : null,
      };
    }
  };
})();


// Plugin RPC wrapper. Hook internals above are copied unchanged from the legacy script.
var __pluginFeatureId = "godmode";
var __pluginModuleName = "godmode";
var __pluginEnabled = false;
var __pluginConfig = {};

function __pluginModule() {
  return modules[__pluginModuleName];
}

function __pluginApplyConfig(config) {
  if (config) {
    for (var key in config) {
      if (Object.prototype.hasOwnProperty.call(config, key)) __pluginConfig[key] = config[key];
    }
  }
  var module = __pluginModule();
  if (!module) return { ok: false, reason: 'module_not_loaded', config: __pluginConfig };

  return { ok: true, config: __pluginConfig };
}

function __pluginEnable(config) {
  if (config) __pluginApplyConfig(config);
  var module = __pluginModule();
  if (!module || typeof module.enable !== 'function') return { ok: false, reason: 'enable_missing' };
  var result = module.enable();
  __pluginEnabled = true;
  return result || { ok: true, enabled: true };
}

function __pluginDisable() {
  var module = __pluginModule();
  if (module && typeof module.disable === 'function') module.disable();
  __pluginEnabled = false;
  return { ok: true, enabled: false };
}

function __pluginStatus() {
  var module = __pluginModule();
  var stats = {};
  try {
    if (module && typeof module.getstatus === 'function') stats = module.getstatus();
    else if (module && typeof module.getStatus === 'function') stats = module.getStatus();
  } catch (_) {}
  return { enabled: __pluginEnabled, config: __pluginConfig, stats: stats };
}

function __pluginCleanup(payload) {
  __pluginDisable();
  return { ok: true, reason: payload && payload.reason ? payload.reason : 'cleanup' };
}

rpc.exports = {
  enable: __pluginEnable,
  disable: __pluginDisable,
  setConfig: __pluginApplyConfig,
  status: __pluginStatus,
  cleanup: __pluginCleanup
};

