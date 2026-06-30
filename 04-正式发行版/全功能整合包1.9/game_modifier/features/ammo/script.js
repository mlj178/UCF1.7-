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

// ammo.js - 无限子弹 plan4
// 替换 ConsumeAmmo 函数，消耗子弹时返回 true 但不扣弹

modules.ammo = (function() {
  var enabled = false;
  var hooks = [];

  return {
    enable: function() {
      if (enabled) return;
      var mod = Process.findModuleByName('GameAssembly.dll');
      if (!mod) { sendBothLog('error', '无限子弹', '无限子弹暂未就绪，请重新连接游戏后重试', 'Ammo GameAssembly.dll not found'); return; }
      var base = mod.base;

      try {
        var addrConsumeAmmo = base.add(0xB61140);
        Interceptor.replace(addrConsumeAmmo, new NativeCallback(function(thisPtr, methodInfo) {
          return 1;
        }, 'bool', ['pointer', 'pointer']));
        hooks.push({ type: 'replace', addr: addrConsumeAmmo });
        sendLog('info', '无限子弹', 'WPN_Gun.ConsumeAmmo 已替换');
      } catch (e) {
        sendBothLog('error', '无限子弹', '无限子弹初始化失败，请稍后重试', 'Ammo replace WPN_Gun.ConsumeAmmo failed: ' + e);
      }

      try {
        var addrConsumeBase = base.add(0xB6C310);
        Interceptor.replace(addrConsumeBase, new NativeCallback(function(thisPtr, methodInfo) {
          return 1;
        }, 'bool', ['pointer', 'pointer']));
        hooks.push({ type: 'replace', addr: addrConsumeBase });
        sendLog('info', '无限子弹', 'Weapon.ConsumeAmmo 已替换');
      } catch (e) {
        sendDevLog('warn', '无限子弹', '替换 Weapon.ConsumeAmmo 失败: ' + e, 'Ammo fallback replace failed');
      }

      try {
        var addrRpgFire = base.add(0xB670A0);
        var addrRpgFillAmmo = base.add(0xB67070);
        var rpgFillAmmoFn = new NativeFunction(addrRpgFillAmmo, 'void', ['pointer', 'pointer']);
        
        var rpgFireHook = Interceptor.attach(addrRpgFire, {
          onEnter: function(args) {
            try {
              var self = args[0];
              if (self && !self.isNull()) {
                rpgFillAmmoFn(self, ptr(0));
              }
            } catch (e) {}
          }
        });
        hooks.push({ type: 'attach', handle: rpgFireHook });
        sendLog('info', '无限子弹', 'RPG/AT4 无限子弹已启用');
      } catch (e) {
        sendDevLog('warn', '无限子弹', 'RPG/AT4 初始化失败: ' + e, 'Ammo RPG/AT4 hook init failed');
      }

      enabled = true;
      sendLog('success', '无限子弹', '已启用 (Zero ammo consumption)');
      sendStatus('ammo', true);
    },
    disable: function() {
      if (!enabled) return;
      for (var i = 0; i < hooks.length; i++) {
        try {
          if (hooks[i].type === 'replace') {
            Interceptor.revert(hooks[i].addr);
          } else {
            hooks[i].handle.detach();
          }
        } catch(e) {}
      }
      hooks = [];
      enabled = false;
      sendLog('info', '无限子弹', '已禁用');
      sendStatus('ammo', false);
    }
  };
})();


// Plugin RPC wrapper. Hook internals above are copied unchanged from the legacy script.
var __pluginFeatureId = "ammo";
var __pluginModuleName = "ammo";
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

