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

// move_speed.js - 滑板鞋 (Move Speed)
// Hook PropertyModifier.Get，拦截 MoveSpeedRatio Modifier 的查询，为本地玩家返回倍数后的值

modules.movespeed = (function() {
  var enabled = false;
  var currentSpeed = 3.0;
  var hookAddr = null;
  var isMyPlayerFn = null;
  var originalFn = null;
  var logCount = 0;

  return {
    setSpeed: function(speed) {
      currentSpeed = speed;
      if (enabled) {
        sendLog('info', '滑板鞋', '速度已切换: ' + speed + 'x（实时生效）');
      } else {
        sendLog('info', '滑板鞋', '速度已预选: ' + speed + 'x（开启后生效）');
      }
    },
    enable: function() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) {
        sendBothLog('error', '滑板鞋', '滑板鞋暂未就绪，请重新连接游戏后重试', 'MoveSpeed GameAssembly.dll not found');
        return;
      }

      var base = mod.base;
      hookAddr = base.add(0xB17590);
      isMyPlayerFn = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
      originalFn = new NativeFunction(hookAddr, 'float', ['pointer', 'pointer']);
      logCount = 0;

      Interceptor.replace(hookAddr, new NativeCallback(function(self, player) {
        var result = originalFn(self, player);
        if (player && !player.isNull() && isMyPlayerFn(player)) {
          var moveMod = player.add(0x8C).readPointer();
          if (moveMod && !moveMod.isNull() && self.equals(moveMod)) {
            logCount++;
            if (logCount <= 10)
              sendLog('info', '滑板鞋', '原值=' + result.toFixed(3) + ' 修改后=' + currentSpeed.toFixed(1) + 'x');
            return currentSpeed;
          }
        }
        return result;
      }, 'float', ['pointer', 'pointer']));

      enabled = true;
      sendLog('success', '滑板鞋', '已启用 (' + currentSpeed + 'x) — 仅对玩家生效');
      sendStatus('movespeed', true);
    },
    disable: function() {
      if (!enabled || !hookAddr) return;
      Interceptor.revert(hookAddr);
      enabled = false;
      sendLog('info', '滑板鞋', '已禁用');
      sendStatus('movespeed', false);
    }
  };
})();


// Plugin RPC wrapper. Hook internals above are copied unchanged from the legacy script.
var __pluginFeatureId = "movespeed";
var __pluginModuleName = "movespeed";
var __pluginEnabled = false;
var __pluginConfig = {"speed": 3.0};

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
  var speed = __pluginConfig.speed;
  if (typeof speed !== 'number') speed = __pluginConfig.value;
  if (typeof speed === 'number' && typeof module.setSpeed === 'function') module.setSpeed(speed);
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

