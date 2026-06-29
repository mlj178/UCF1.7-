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
