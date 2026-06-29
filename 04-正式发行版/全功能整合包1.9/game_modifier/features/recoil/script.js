// Plugin script compatibility prelude. The real hook code copied from scripts/ follows below.
if (typeof modules === 'undefined') { var modules = {}; }
if (typeof send === 'undefined') { var send = function(_) {}; }
if (typeof sendStatus === 'undefined') { var sendStatus = function(_, __) {}; }
if (typeof sendLog === 'undefined') { var sendLog = function(_, __, ___) {}; }
if (typeof sendDevLog === 'undefined') { var sendDevLog = function(_, __, ___, ____) {}; }
if (typeof sendUserLog === 'undefined') { var sendUserLog = function(_, __, ___) {}; }
if (typeof sendBothLog === 'undefined') { var sendBothLog = function(_, __, ___, ____) {}; }
if (typeof sendLogFile === 'undefined') { var sendLogFile = function(_, __, ___) {}; }
if (typeof registerCleanup === 'undefined') { var registerCleanup = function(_) { return false; }; }
if (typeof getGameAssembly === 'undefined') {
  var getGameAssembly = function() {
    try { return Process.findModuleByName('GameAssembly.dll'); } catch (_) { return null; }
  };
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
