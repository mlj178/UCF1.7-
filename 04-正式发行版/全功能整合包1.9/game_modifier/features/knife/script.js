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

// knife.js - 快刀模块 v16 (NativeCallback Replace)
// 替换 PlayerWeapons.get_KnifeSpeed，为本地玩家返回指定的速度倍数

modules.knife = (function() {
  var enabled = false;
  var currentSpeed = 5.0;
  var isMyPlayer = null;
  var originalGetKnifeSpeed = null;
  var getKnifeSpeedAddr = null;
  var logCount = 0;

  return {
    setSpeed: function(speed) {
      currentSpeed = speed;
      if (enabled) {
        sendLog('info', '快刀', '速度已切换: ' + speed + 'x（实时生效）');
      } else {
        sendLog('info', '快刀', '速度已预选: ' + speed + 'x（开启后生效）');
      }
    },
    enable: function() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) { sendBothLog('error', '快刀', '快刀暂未就绪，请重新连接游戏后重试', 'Knife GameAssembly.dll not found'); return; }

      var base = mod.base;
      var isMyPlayerAddr = base.add(0xB55FD0);
      getKnifeSpeedAddr = base.add(0xB170A0);

      sendLog('info', '快刀', 'isMyPlayer @ ' + isMyPlayerAddr);
      sendLog('info', '快刀', 'get_KnifeSpeed @ ' + getKnifeSpeedAddr);

      isMyPlayer = new NativeFunction(isMyPlayerAddr, 'bool', ['pointer']);
      originalGetKnifeSpeed = new NativeFunction(getKnifeSpeedAddr, 'float', ['pointer']);

      logCount = 0;

      Interceptor.replace(getKnifeSpeedAddr, new NativeCallback(function(self) {
        try {
          var owner = self.add(0x8).readPointer();
          if (!owner || owner.isNull()) {
            return originalGetKnifeSpeed(self);
          }

          if (isMyPlayer(owner)) {
            logCount++;
            if (logCount <= 10) {
              sendLog('info', '快刀', '[KnifeSpeed] Player detected, returning ' + currentSpeed);
            }
            return currentSpeed;
          }

          return originalGetKnifeSpeed(self);
        } catch(e) {
          sendDevLog('error', '快刀', '快刀 Hook 回调异常: ' + e.message, 'KnifeSpeed callback error');
          return originalGetKnifeSpeed(self);
        }
      }, 'float', ['pointer']));

      enabled = true;
      sendLog('success', '快刀', '已启用 (v16, Speed=' + currentSpeed + 'x) — 仅对玩家生效');
      sendStatus('knife', true);
    },
    disable: function() {
      if (!enabled) return;
      if (getKnifeSpeedAddr) {
        try { Interceptor.revert(getKnifeSpeedAddr); } catch(e) {}
      }
      isMyPlayer = null;
      originalGetKnifeSpeed = null;
      getKnifeSpeedAddr = null;
      enabled = false;
      sendLog('info', '快刀', '已禁用');
      sendStatus('knife', false);
    }
  };
})();


// Plugin RPC wrapper. Hook internals above are copied unchanged from the legacy script.
var __pluginFeatureId = "knife";
var __pluginModuleName = "knife";
var __pluginEnabled = false;
var __pluginConfig = {"speed": 5.0};

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
