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

// recoil.js - 无后座力 v14
// 替换 Recoil.OnGunShot，将后座力相关字段归零

modules.recoil = (function() {
  var replacedAddr = null;
  var callbackFunc = null;
  var enabled = false;
  var suppressCount = 0;

  return {
    enable: function() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) { sendBothLog('error', '无后座力', '无后座力暂未就绪，请重新连接游戏后重试', 'NoRecoil GameAssembly.dll not found'); return; }

      var base = mod.base;
      replacedAddr = base.add(0xB19980);
      sendLog('info', '无后座力', 'Recoil$$OnGunShot @ ' + replacedAddr);

      suppressCount = 0;

      callbackFunc = new NativeCallback(function(recoilThis, methodInfo) {
        suppressCount++;
        try {
          recoilThis.add(0x68).writeFloat(0.0);
          recoilThis.add(0x6C).writeFloat(0.0);
          recoilThis.add(0x70).writeFloat(0.0);
          recoilThis.add(0x74).writeFloat(0.0);
        } catch (e) {}

        if (suppressCount <= 3) {
          sendLog('info', '无后座力', '[Suppress #' + suppressCount + '] ' + recoilThis);
        } else if (suppressCount === 4) {
          sendLog('info', '无后座力', '...suppressing silently');
        }
      }, 'void', ['pointer', 'pointer']);

      try {
        Interceptor.replace(replacedAddr, callbackFunc);
        sendLog('success', '无后座力', '已替换 Recoil.OnGunShot');
      } catch(e) {
        sendBothLog('error', '无后座力', '无后座力启用失败，请稍后重试', 'NoRecoil replace failed: ' + e.message);
        return;
      }

      enabled = true;
      sendLog('success', '无后座力', 'v14 已启用 (replace OnGunShot + zero 4 fields)');
      sendStatus('recoil', true);
    },
    disable: function() {
      if (!enabled) return;
      if (replacedAddr) { try { Interceptor.revert(replacedAddr); } catch(e) {} }
      callbackFunc = null; replacedAddr = null;
      enabled = false;
      sendLog('info', '无后座力', '已禁用');
      sendStatus('recoil', false);
    }
  };
})();


// Plugin RPC wrapper. Hook internals above are copied unchanged from the legacy script.
var __pluginFeatureId = "recoil";
var __pluginModuleName = "recoil";
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

