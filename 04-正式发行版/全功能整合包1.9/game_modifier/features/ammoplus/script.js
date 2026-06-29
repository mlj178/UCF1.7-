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

// reload_speed.js - 快速换弹
// 替换 get_ReloadSpeed，为本地玩家返回2倍加速

modules.ammoplus = (function() {
  var enabled = false;
  var getReloadSpeedAddr = null;
  var isMyPlayer = null;
  var reloadLogCount = 0;

  return {
    enable: function() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) { sendBothLog('error', '快速换弹', '快速换弹暂未就绪，请重新连接游戏后重试', 'FastReload GameAssembly.dll not found'); return; }

      var base = mod.base;
      getReloadSpeedAddr = base.add(0xB170E0);
      isMyPlayer = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
      reloadLogCount = 0;

      sendLog('info', '快速换弹', 'get_ReloadSpeed @ ' + getReloadSpeedAddr);

      Interceptor.replace(getReloadSpeedAddr, new NativeCallback(function(self) {
        try {
          var owner = self.add(0x8).readPointer();
          if (!owner || owner.isNull()) return 4.0;
          if (isMyPlayer(owner)) {
            reloadLogCount++;
            if (reloadLogCount <= 5) {
              sendLog('info', '快速换弹', '本地玩家换弹加速 4.0x (#' + reloadLogCount + ')');
            }
            return 4.0;
          }
          return 1.0;
        } catch(e) {
          return 4.0;
        }
      }, 'float', ['pointer']));

      enabled = true;
      sendLog('success', '快速换弹', '已启用 — 2x快速换弹');
      sendStatus('ammoplus', true);
    },
    disable: function() {
      if (!enabled) return;
      if (getReloadSpeedAddr) { try { Interceptor.revert(getReloadSpeedAddr); } catch(e) {} }
      getReloadSpeedAddr = null;
      isMyPlayer = null;
      enabled = false;
      sendLog('info', '快速换弹', '已禁用');
      sendStatus('ammoplus', false);
    }
  };
})();


// Plugin RPC wrapper. Hook internals above are copied unchanged from the legacy script.
var __pluginFeatureId = "ammoplus";
var __pluginModuleName = "ammoplus";
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
