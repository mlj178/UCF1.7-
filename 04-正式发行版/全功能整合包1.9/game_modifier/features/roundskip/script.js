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

// round_skip.js - Round Skip
// Writes ModeBase.restGameTime to 0:00. Room generation prevents stale writes.

modules.roundskip = (function() {
  var modeBaseInstance = null;
  var modeBaseGeneration = -1;
  var roomGeneration = 0;
  var skipCount = 0;
  var skipErrorCount = 0;
  var roundActive = false;
  var currentRound = 0;
  var inHook = false;
  var skipGuard = false;
  var hooks = [];

  var RVA = {
    ModeBase_UpdateTimeUI: 0xAF6930,
    GameManager_GameRoundEnd: 0xAFAA40,
    ModeBase_Nano_OnTimeOut: 0xAF1920,
    ModeBase_ExitGame: 0xAEE850,
    GameManager_OnDestroy: 0xAFB6F0
  };

  function pad2(n) { return n < 10 ? "0" + n : "" + n; }
  function addDevLog(level, message, detail) { sendDevLog(level, 'RoundSkip', message, detail || 'RoundSkip internal'); }
  function addUserLog(level, message) { sendUserLog(level, 'RoundSkip', message); }

  function isValidInstance(instance) {
    try {
      if (!instance || instance.equals(ptr(0))) return false;
      if (instance.compare(ptr(0x10000)) < 0) return false;
      instance.readU8();
      return true;
    } catch (e) {
      return false;
    }
  }

  function clearRoomState(reason, bumpGeneration) {
    if (bumpGeneration) roomGeneration++;
    modeBaseInstance = null;
    modeBaseGeneration = -1;
    roundActive = false;
    skipGuard = false;
    addDevLog('info', reason, 'RoundSkip cleared room state');
  }

  function captureModeBase(instance) {
    if (!isValidInstance(instance)) return;
    if (!modeBaseInstance || !instance.equals(modeBaseInstance)) {
      modeBaseInstance = instance;
      modeBaseGeneration = roomGeneration;
      try { currentRound = instance.add(0x14).readS32(); } catch (e) {}
      roundActive = true;
      addDevLog('info', 'new round #' + currentRound, 'RoundSkip captured ModeBase instance');
    }
  }

  function skipRound() {
    if (skipGuard) return { ok: false, reason: 'guard_active' };

    var instance = modeBaseInstance;
    if (modeBaseGeneration !== roomGeneration) {
      modeBaseInstance = null;
      modeBaseGeneration = -1;
      skipErrorCount++;
      return { ok: false, reason: 'stale_room_generation' };
    }
    if (!isValidInstance(instance)) {
      skipErrorCount++;
      return { ok: false, reason: 'no_instance' };
    }

    var minute = 0;
    var second = 0;
    try {
      minute = instance.add(0x34).readS32();
      second = instance.add(0x38).readS32();
    } catch (e) {
      skipErrorCount++;
      return { ok: false, reason: 'read_failed' };
    }
    if (minute === 0 && second === 0) return { ok: false, reason: 'already_zero' };

    try {
      skipGuard = true;
      try { if (modules.time) modules.time.pauseFor(1000); } catch (e1) {}
      instance.add(0x34).writeS32(0);
      instance.add(0x38).writeS32(0);
      skipCount++;
      roundActive = false;
      send({ type: 'round_skipped', from: minute + ':' + pad2(second), count: skipCount });
      addDevLog('info', 'SKIP! ' + minute + ':' + pad2(second) + ' -> 0:00 (total:' + skipCount + ')', 'RoundSkip wrote restGameTime to 0:00');
      return { ok: true };
    } catch (e2) {
      skipErrorCount++;
      return { ok: false, reason: 'write_failed' };
    } finally {
      skipGuard = false;
    }
  }

  function installHooks() {
    var mod = getGameAssembly();
    if (!mod) {
      addUserLog('error', 'RoundSkip is not ready, reconnect to the game and try again');
      addDevLog('error', 'missing GameAssembly.dll', 'RoundSkip installHooks failed: GameAssembly.dll missing');
      return false;
    }

    var base = mod.base;
    try {
      hooks.push(Interceptor.attach(base.add(RVA.ModeBase_UpdateTimeUI), {
        onEnter: function(args) {
          if (inHook) return;
          inHook = true;
          captureModeBase(args[0]);
          inHook = false;
        },
        onLeave: function() { inHook = false; }
      }));
    } catch (e) {}
    try { hooks.push(Interceptor.attach(base.add(RVA.GameManager_GameRoundEnd), { onEnter: function() { clearRoomState('GameRoundEnd', false); } })); } catch (e1) {}
    try { hooks.push(Interceptor.attach(base.add(RVA.ModeBase_Nano_OnTimeOut), { onEnter: function() { roundActive = false; addDevLog('info', 'OnTimeOut', 'RoundSkip detected timeout'); } })); } catch (e2) {}
    try { hooks.push(Interceptor.attach(base.add(RVA.ModeBase_ExitGame), { onEnter: function() { clearRoomState('ModeBase.ExitGame', true); } })); } catch (e3) {}
    try { hooks.push(Interceptor.attach(base.add(RVA.GameManager_OnDestroy), { onEnter: function() { clearRoomState('GameManager.OnDestroy', true); } })); } catch (e4) {}
    return true;
  }

  return {
    enable: function() {
      if (hooks.length > 0) return;
      installHooks();
    },
    disable: function() {
      for (var i = 0; i < hooks.length; i++) {
        try { hooks[i].detach(); } catch (e) {}
      }
      hooks = [];
      modeBaseInstance = null;
      modeBaseGeneration = -1;
      roundActive = false;
      addDevLog('info', 'unloaded', 'RoundSkip hooks detached');
    },
    skipround: function() {
      var result = skipRound();
      return { ok: result.ok, reason: result.reason };
    },
    getstatus: function() {
      var timeStr = null;
      if (isValidInstance(modeBaseInstance) && modeBaseGeneration === roomGeneration) {
        try {
          var m = modeBaseInstance.add(0x34).readS32();
          var s = modeBaseInstance.add(0x38).readS32();
          if (m >= 0 && m <= 200 && s >= 0 && s <= 59) timeStr = m + ":" + pad2(s);
        } catch (e) {}
      }
      return {
        ok: true,
        roundActive: roundActive,
        currentRound: currentRound,
        skipCount: skipCount,
        skipErrorCount: skipErrorCount,
        hasInstance: !!modeBaseInstance,
        restGameTime: timeStr
      };
    },
    reset: function() {
      modeBaseInstance = null;
      modeBaseGeneration = -1;
      roundActive = false;
      currentRound = 0;
      skipCount = 0;
      skipErrorCount = 0;
      skipGuard = false;
      inHook = false;
      return { ok: true };
    }
  };
})();


// Plugin RPC wrapper. Hook internals above are copied unchanged from the legacy script.
var __pluginFeatureId = "roundskip";
var __pluginModuleName = "roundskip";
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
  if (typeof module.skipround === 'function') {
    result = module.skipround();
  }
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
