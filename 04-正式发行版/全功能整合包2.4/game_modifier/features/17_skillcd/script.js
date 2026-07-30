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

// skill_cd.js - 生化模式英雄技能无冷却
// 精确捕获本地玩家，并在该玩家的 Update 游戏线程中节流调用 EndCold。

modules.skillcd = (function() {
  var enabled = false;
  var myPlayerPtr = null;
  var endColdFn = null;
  var lastEndColdTime = 0;
  var processing = false;
  var hooks = [];

  var RVA = {
    EndCold: 0xAE1BC0,
    PlayerGetIsMyPlayer: 0xB55FD0,
    PlayerUpdate: 0xB551D0,
    PlayerOnDestroy: 0xB511C0,
    GameManagerOnDestroy: 0xAFB6F0
  };

  function readPtr(addr) {
    try {
      if (!addr || addr.isNull()) return null;
      var value = addr.readPointer();
      return value && !value.isNull() ? value : null;
    } catch (e) {
      return null;
    }
  }

  function readI32(addr) {
    try { return addr ? addr.readS32() : null; } catch (e) { return null; }
  }

  function readF32(addr) {
    try { return addr ? addr.readFloat() : null; } catch (e) { return null; }
  }

  function clearPlayerState(reason) {
    if (myPlayerPtr && reason) {
      sendLog('info', '技能CD', reason);
    }
    myPlayerPtr = null;
    lastEndColdTime = 0;
    processing = false;
  }

  function scanSkillSteps(playerPtr) {
    var playerSkills = readPtr(playerPtr.add(0xB0));
    if (!playerSkills) return;

    var skillArray = readPtr(playerSkills.add(0x08));
    if (!skillArray) return;

    var length = readI32(skillArray.add(0x0C));
    if (!length || length <= 0 || length > 20) return;

    var found = 0;
    for (var i = 0; i < length; i++) {
      var skill = readPtr(skillArray.add(0x10 + 4 * i));
      if (!skill) continue;
      var coldFinish = readF32(skill.add(0x1C));
      var coldTime = readF32(skill.add(0x24));
      if (coldFinish !== null && coldTime !== null) found++;
    }

    if (found > 0) {
      sendLog('info', '技能CD', '找到 ' + found + ' 个技能');
    }
  }

  function scanAndEndCold(playerPtr) {
    if (!enabled || processing || !endColdFn || !playerPtr || playerPtr.isNull()) return;
    if (!myPlayerPtr || !myPlayerPtr.equals(playerPtr)) return;

    processing = true;
    try {
      var playerSkills = readPtr(playerPtr.add(0xB0));
      if (!playerSkills) return;

      var skillArray = readPtr(playerSkills.add(0x08));
      if (!skillArray) return;

      var length = readI32(skillArray.add(0x0C));
      if (!length || length <= 0 || length > 20) return;

      for (var i = 0; i < length; i++) {
        var skill = readPtr(skillArray.add(0x10 + 4 * i));
        if (!skill) continue;

        // IL2CPP object must have a readable class pointer and class metadata pointer.
        var klass = readPtr(skill);
        if (!klass || !readPtr(klass)) continue;

        var coldFinish = readF32(skill.add(0x1C));
        var coldTime = readF32(skill.add(0x24));
        if (coldFinish === null || coldTime === null) continue;
        if (!isFinite(coldFinish) || !isFinite(coldTime)) continue;

        endColdFn(skill);
      }
    } catch (e) {
      // Frida can catch read errors, but native access violations are prevented
      // primarily by correct identity, thread context and lifecycle cleanup.
    } finally {
      processing = false;
    }
  }

  function detachHooks() {
    for (var i = 0; i < hooks.length; i++) {
      try { hooks[i].detach(); } catch (e) {}
    }
    hooks = [];
  }

  function rollbackEnable(message) {
    enabled = false;
    clearPlayerState(null);
    detachHooks();
    endColdFn = null;
    sendBothLog('error', '技能CD', '技能无冷却启用失败，请稍后重试', 'SkillCD enable failed and rolled back: ' + message);
    sendStatus('skillcd', false);
  }

  return {
    enable: function() {
      if (enabled) return;

      var mod = getGameAssembly();
      if (!mod) {
        sendBothLog('error', '技能CD', '技能无冷却暂未就绪，请重新连接游戏后重试', 'SkillCD GameAssembly.dll not found');
        return;
      }

      var base = mod.base;
      try {
        endColdFn = new NativeFunction(base.add(RVA.EndCold), 'void', ['pointer']);
        sendLog('info', '技能CD', 'EndCold 函数就绪 (RVA 0xAE1BC0)');

        // Observe the game's real result; do not replace get_isMyPlayer.
        hooks.push(Interceptor.attach(base.add(RVA.PlayerGetIsMyPlayer), {
          onEnter: function(args) {
            this.candidatePlayer = args[0];
          },
          onLeave: function(retval) {
            try {
              var playerPtr = this.candidatePlayer;
              // IL2CPP bool is returned in AL on x86. The upper 24 bits of EAX
              // are not guaranteed to be zero, so reading the full Int32 can
              // turn a false result into true.
              var isMyPlayer = (retval.toUInt32() & 0xFF) !== 0;
              if (!isMyPlayer || !playerPtr || playerPtr.isNull()) return;
              if (myPlayerPtr && myPlayerPtr.equals(playerPtr)) return;

              myPlayerPtr = playerPtr;
              lastEndColdTime = 0;
              scanSkillSteps(playerPtr);
              sendLog('info', '技能CD', '本地玩家指针已更新: ' + playerPtr);
            } catch (e) {
              clearPlayerState('本地玩家识别异常，已清空缓存');
            }
          }
        }));
        sendLog('success', '技能CD', 'isMyPlayer Hook OK');

        // Player.Update is a game-thread callback. Only the confirmed local
        // player is processed, at most once every 200 ms.
        hooks.push(Interceptor.attach(base.add(RVA.PlayerUpdate), {
          onEnter: function(args) {
            var playerPtr = args[0];
            if (!enabled || !myPlayerPtr || !playerPtr || playerPtr.isNull()) return;
            if (!myPlayerPtr.equals(playerPtr)) return;

            var now = Date.now();
            if (now - lastEndColdTime < 200) return;
            lastEndColdTime = now;
            scanAndEndCold(playerPtr);
          }
        }));
        sendLog('success', '技能CD', 'Player.Update Hook OK');

        hooks.push(Interceptor.attach(base.add(RVA.PlayerOnDestroy), {
          onEnter: function(args) {
            var playerPtr = args[0];
            if (myPlayerPtr && playerPtr && !playerPtr.isNull() && myPlayerPtr.equals(playerPtr)) {
              clearPlayerState('本地玩家已销毁，已清空技能缓存');
            }
          }
        }));
        sendLog('success', '技能CD', 'Player.OnDestroy Hook OK');

        hooks.push(Interceptor.attach(base.add(RVA.GameManagerOnDestroy), {
          onEnter: function() {
            clearPlayerState('GameManager 已销毁，已清空技能缓存');
          }
        }));
        sendLog('success', '技能CD', 'GameManager.OnDestroy Hook OK');

        enabled = true;
        sendLog('success', '技能CD', '已开启 — 本地玩家 Update 中每 200ms 调用 EndCold()');
        sendStatus('skillcd', true);
      } catch (e) {
        rollbackEnable(e.message || String(e));
      }
    },

    disable: function() {
      if (!enabled && hooks.length === 0) return;

      enabled = false;
      clearPlayerState(null);
      detachHooks();
      endColdFn = null;
      sendLog('info', '技能CD', '已关闭');
      sendStatus('skillcd', false);
    },

    isEnabled: function() {
      return enabled;
    }
  };
})();


// Plugin RPC wrapper. Hook internals above are copied unchanged from the legacy script.
var __pluginFeatureId = "skillcd";
var __pluginModuleName = "skillcd";
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

