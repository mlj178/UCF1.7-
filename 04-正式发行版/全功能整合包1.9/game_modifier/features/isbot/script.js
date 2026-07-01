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

// is_bot.js - 天机傀儡，修改 ClientData.isBot
// 通过替换 isMyPlayer 捕获 localPlayer，再直接写入 isBot 字节。

modules.isbot = (function() {
  var enabled = false;
  var localPlayer = null;
  var clientData = null;
  var logCount = 0;
  var MAX_LOG = 15;
  var hookInstalled = false;
  var retryInterval = null;
  var addrIsMy = null;
  var roomCaptureCount = 0;
  var lifecycleHooks = [];
  var roomGeneration = 0;
  var capturedGeneration = -1;
  var lastCaptureAtMs = 0;
  var pendingRestoreOnCapture = false;

  var RVA = {
    Player_get_isMyPlayer: 0xB55FD0,
    ModeBase_ExitGame: 0xAEE850,
    Player_OnDestroy: 0xB511C0,
    GameManager_OnDestroy: 0xAFB6F0
  };
  var OFF_CLIENT = 0x94;
  var OFF_ISBOT = 0x1C;
  var OFF_NICK = 0x10;

  function log(level, msg) {
    if (logCount >= MAX_LOG && level !== 'error') return;
    logCount++;
    send({ type: 'log', level: level, module: 'isBot', message: msg });
  }

  function sendUiState(state) {
    send({
      type: 'plugin_event',
      feature: 'isbot',
      event: 'state',
      payload: { state: state },
      audience: 'both'
    });
  }

  function currentAppliedState() {
    return roomCaptureCount >= 2 ? 'active' : 'awaiting_reenter';
  }

  function readStr(p) {
    try {
      var obj = p.readPointer();
      if (!obj || obj.isNull()) return '?';
      var len = obj.add(-4).readS32();
      if (len < 0 || len > 64) return '?';
      return obj.readUtf8String(len);
    } catch (e) {
      return '?';
    }
  }

  function dump() {
    if (!clientData || capturedGeneration !== roomGeneration) return;
    var bot = clientData.add(OFF_ISBOT).readU8();
    var nick = readStr(clientData.add(OFF_NICK));
    log('info', localPlayer + '|' + clientData + '|0x1C:' + bot + '|nick:' + nick);
  }

  function writeBot(val) {
    if (!clientData) return false;
    if (capturedGeneration !== roomGeneration) return false;
    try {
      clientData.add(OFF_ISBOT).writeU8(val);
      var after = clientData.add(OFF_ISBOT).readU8();
      log('info', 'isBot=' + after + ' (写入 ' + val + ')');
      return true;
    } catch (e) {
      return false;
    }
  }

  function forceWriteBot(val) {
    if (!clientData) return false;
    try {
      var target = clientData.add(OFF_ISBOT);
      if (!target || target.isNull()) return false;
      if (target.compare(ptr(0x10000)) < 0) return false;
      var range = Process.findRangeByAddress(target);
      if (!range || range.protection.indexOf('w') === -1) return false;
      target.writeU8(val);
      var after = target.readU8();
      log('info', 'force isBot=' + after + ' (写入 ' + val + ')');
      return true;
    } catch (e) {
      return false;
    }
  }

  function clearRoomState(reason) {
    roomGeneration++;
    if (retryInterval) {
      clearInterval(retryInterval);
      retryInterval = null;
    }
    localPlayer = null;
    clientData = null;
    capturedGeneration = -1;
    lastCaptureAtMs = 0;
    if (enabled) sendUiState('awaiting_room');
    log('info', 'room state cleared: ' + reason);
  }

  function shouldIgnoreLateGameManagerDestroy() {
    if (!enabled || !clientData || capturedGeneration !== roomGeneration) return false;
    if (!lastCaptureAtMs) return false;
    return (Date.now() - lastCaptureAtMs) < 500;
  }

  function tryWriteBotOnCapture() {
    if (!clientData) {
      return false;
    }
    if (capturedGeneration !== roomGeneration) return false;

    var ok = writeBot(1);
    if (ok) {
      sendLog('info', '天机傀儡', 'Bot 模式已写入');
      if (retryInterval) {
        clearInterval(retryInterval);
        retryInterval = null;
      }
    }
    return ok;
  }

  function restoreBotOnNextCapture() {
    if (!pendingRestoreOnCapture) return false;
    var restored = writeBot(0);
    pendingRestoreOnCapture = !restored;
    if (restored) {
      uninstallHook();
      localPlayer = null;
      clientData = null;
      capturedGeneration = -1;
      sendUiState('off');
    }
    return restored;
  }

  function handlePlayerCapture(playerPtr) {
    if (localPlayer && playerPtr.equals(localPlayer)) {
      return;
    }

    localPlayer = playerPtr;

    var cd = playerPtr.add(OFF_CLIENT).readPointer();
    if (!cd || cd.isNull()) {
      return;
    }

    clientData = cd;
    capturedGeneration = roomGeneration;
    roomCaptureCount += 1;
    lastCaptureAtMs = Date.now();
    setTimeout(dump, 2000);

    if (!enabled) {
      restoreBotOnNextCapture();
      return;
    }

    if (tryWriteBotOnCapture()) {
      sendUiState(currentAppliedState());
    }
  }

  function installHook() {
    if (hookInstalled) return;
    try {
      var mod = getGameAssembly();
      if (!mod) {
        sendBothLog('error', '天机傀儡', '天机傀儡暂未就绪，请重新连接游戏后重试', 'IsBot GameAssembly.dll not found');
        return;
      }

      var base = mod.base;
      addrIsMy = base.add(RVA.Player_get_isMyPlayer);
      var origIsMy = new NativeFunction(addrIsMy, 'bool', ['pointer', 'pointer']);

      Interceptor.replace(addrIsMy, new NativeCallback(function(playerPtr, methodInfo) {
        var result = origIsMy(playerPtr, methodInfo);
        if (result) {
          handlePlayerCapture(playerPtr);
        }
        return result;
      }, 'bool', ['pointer', 'pointer']));

      try { lifecycleHooks.push(Interceptor.attach(base.add(RVA.ModeBase_ExitGame), { onEnter: function() { clearRoomState('ModeBase.ExitGame'); } })); } catch (e1) {}
      try { lifecycleHooks.push(Interceptor.attach(base.add(RVA.Player_OnDestroy), { onEnter: function(args) { try { if (localPlayer && args[0] && args[0].equals(localPlayer)) clearRoomState('Player.OnDestroy'); } catch (_) {} } })); } catch (e2) {}
      try { lifecycleHooks.push(Interceptor.attach(base.add(RVA.GameManager_OnDestroy), { onEnter: function() { if (!shouldIgnoreLateGameManagerDestroy()) clearRoomState('GameManager.OnDestroy'); } })); } catch (e3) {}

      hookInstalled = true;
    } catch (e) {
      sendBothLog('error', '天机傀儡', '天机傀儡初始化失败，请稍后重试', 'IsBot hook install failed: ' + (e.message || e));
    }
  }

  function uninstallHook() {
    if (hookInstalled && addrIsMy) {
      try {
        Interceptor.revert(addrIsMy);
      } catch (e) {}
      hookInstalled = false;
      addrIsMy = null;
    }
    for (var i = 0; i < lifecycleHooks.length; i++) {
      try { lifecycleHooks[i].detach(); } catch (e) {}
    }
    lifecycleHooks = [];
  }

  return {
    enable: function() {
      if (enabled) return;

      installHook();
      enabled = true;
      pendingRestoreOnCapture = false;
      sendUiState('awaiting_room');

      if (tryWriteBotOnCapture()) {
        sendLog('success', '天机傀儡', '已启用');
        sendStatus('isbot', true);
        sendUiState(currentAppliedState());
        return;
      }

      var retries = 0;
      var retryGeneration = roomGeneration;
      retryInterval = setInterval(function() {
        if (retryGeneration !== roomGeneration) {
          clearInterval(retryInterval);
          retryInterval = null;
          return;
        }
        if (clientData) {
          if (tryWriteBotOnCapture()) {
            sendUiState(currentAppliedState());
          }
        }
        retries++;
        if (retries > 20) {
          clearInterval(retryInterval);
          retryInterval = null;
          sendBothLog('warn', '天机傀儡', '暂未捕获本地玩家，请进入房间后重新尝试', 'IsBot waiting for local player timed out');
        }
      }, 500);

      sendLog('success', '天机傀儡', '已启用（等待本地玩家）');
      sendStatus('isbot', true);
    },
    disable: function(options) {
      if (!enabled && !hookInstalled) return;
      if (retryInterval) {
        clearInterval(retryInterval);
        retryInterval = null;
      }
      enabled = false;
      var restored = writeBot(0) || forceWriteBot(0);
      pendingRestoreOnCapture = true;
      if (options && options.cleanup) {
        pendingRestoreOnCapture = !restored;
        uninstallHook();
      }
      localPlayer = null;
      clientData = null;
      capturedGeneration = -1;
      roomCaptureCount = 0;
      lastCaptureAtMs = 0;
      log('info', '已禁用');
      sendStatus('isbot', false);
      sendUiState('off');
    },
    isEnabled: function() {
      return enabled;
    },
    modify: function() {
      if (writeBot(1)) return JSON.stringify({ success: true, bot: 1 });
      return JSON.stringify({ success: false });
    },
    restore: function() {
      if (writeBot(0)) return JSON.stringify({ success: true, bot: 0 });
      return JSON.stringify({ success: false });
    },
    stop: function() {
      if (writeBot(0)) return JSON.stringify({ success: true, bot: 0 });
      return JSON.stringify({ success: false });
    },
    status: function() {
      return JSON.stringify({
        player: localPlayer ? localPlayer.toString() : null,
        cd: clientData ? clientData.toString() : null,
        bot: clientData ? clientData.add(OFF_ISBOT).readU8() : null,
        roomCaptureCount: roomCaptureCount
      });
    }
  };
})();


// Plugin RPC wrapper. Hook internals above are copied unchanged from the legacy script.
var __pluginFeatureId = "isbot";
var __pluginModuleName = "isbot";
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

function __pluginDisable(options) {
  var module = __pluginModule();
  if (module && typeof module.disable === 'function') module.disable(options || {});
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
  var module = __pluginModule();
  if (module && typeof module.disable === 'function') module.disable({ cleanup: true });
  __pluginEnabled = false;
  return { ok: true, reason: payload && payload.reason ? payload.reason : 'cleanup' };
}

rpc.exports = {
  enable: __pluginEnable,
  disable: __pluginDisable,
  setConfig: __pluginApplyConfig,
  status: __pluginStatus,
  cleanup: __pluginCleanup
};

