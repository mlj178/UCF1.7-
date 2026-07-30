// ============================================================
// AAAAA-bot_pause_min.js - Bot pause minimum implementation
// v1.2-no-il2cpp-api
//
// Goal:
//   Toggle Bot.stopAllBot by fixed RVA + static field pointer chain.
//
// User rule:
//   Do NOT call IL2CPP API / reflection API.
//   No class init API.
//   No runtime metadata API.
//
// Verified data:
//   Bot_TypeInfo:    GameAssembly.dll + 0xE25F44
//   static_fields:   Bot_TypeInfo + 0x5C
//   Bot.stopAllBot:  static_fields + 0xC
//
// Safety fixes:
//   1. Resolve pointers on every operation; never keep stale pointers.
//   2. Validate pointer size and every pointer read.
//   3. Read before write; skip duplicate writes.
//   4. Write then read back to verify.
//   5. If the room is not ready yet, keep user intent and retry until Bot.stopAllBot is writable.
// ============================================================

(function () {
  'use strict';

  var RVA = {
    Bot_TypeInfo: 0xE25F44,
    Bot_Update: 0xB33370,
    GameManager_Awake: 0xAFA250,
    GameManager_OnDestroy: 0xAFB6F0,
    ModeBase_Update: 0xAF6A00,
    ModeBase_ExitGame: 0xAEE850
  };

  var OFF = {
    Il2CppClass_static_fields: 0x5C,
    Bot_stopAllBot: 0xC
  };

  var state = {
    enabled: false,
    pendingApply: false,
    applied: false,
    retryTimer: null,
    retryCount: 0,
    hooksInstalled: false,
    hooks: [],
    roomGeneration: 0,
    lastRoomReadyApplyAt: 0,
    lastApplyReason: '',
    lastError: null,
    writeCount: 0,
    pointerSize: Process.pointerSize,
    lastResolved: null
  };

  function safeString(x) {
    try {
      if (x === null || x === undefined) return String(x);
      return x.toString();
    } catch (_) {
      return '<unprintable>';
    }
  }

  function setError(msg, e) {
    state.lastError = msg + (e && e.message ? ': ' + e.message : '');
    return state.lastError;
  }

  function sendLog(level, message) {
    try {
      var text = '[bot_pause][' + level + '] ' + message;
      console.log(text);
      send({ type: 'log', level: level, module: 'bot_pause', message: message });
    } catch (_) {
    }
  }

  function clearRoomReadyRetry() {
    if (state.retryTimer !== null) {
      try { clearInterval(state.retryTimer); } catch (_) {}
      state.retryTimer = null;
    }
  }

  function detachRoomReadyHooks() {
    for (var i = 0; i < state.hooks.length; i++) {
      try { state.hooks[i].detach(); } catch (_) {}
    }
    state.hooks = [];
    state.hooksInstalled = false;
  }

  function isExecutable(addr) {
    try {
      var range = Process.findRangeByAddress(addr);
      return range !== null && range.protection.indexOf('x') !== -1;
    } catch (_) {
      return false;
    }
  }

  function attachRoomHook(mod, name, rva, callbacks) {
    var addr = mod.base.add(rva);
    if (!isExecutable(addr)) {
      sendLog('warn', name + ' hook skipped; address is not executable: ' + safeString(addr));
      return false;
    }
    try {
      state.hooks.push(Interceptor.attach(addr, callbacks));
      sendLog('info', 'room-ready hook installed: ' + name);
      return true;
    } catch (e) {
      sendLog('warn', name + ' hook install failed: ' + (e && e.message ? e.message : safeString(e)));
      return false;
    }
  }

  function triggerRoomReadyApply(reason, force) {
    if (!state.enabled) return;
    var now = Date.now();
    if (!force && state.applied && !state.pendingApply && now - state.lastRoomReadyApplyAt < 1000) return;
    state.lastRoomReadyApplyAt = now;
    var result = applyEnabledState(reason || 'room_ready_hook');
    if (result.ok) {
      if (reason !== 'ModeBase.Update' || state.retryCount === 0 || state.retryCount % 30 === 0) {
        sendLog('info', 'room-ready apply ok: ' + (reason || 'hook'));
      }
    } else {
      startRoomReadyRetry(reason || 'room_ready_hook');
    }
  }

  function clearRoomState(reason) {
    state.roomGeneration += 1;
    state.applied = false;
    state.pendingApply = !!state.enabled;
    state.lastApplyReason = reason || 'room_destroyed';
    state.lastRoomReadyApplyAt = 0;
    if (state.enabled) startRoomReadyRetry(reason || 'room_destroyed');
  }

  function installRoomReadyHooks() {
    if (state.hooksInstalled) return true;

    var mod = getGameAssembly();
    if (!mod) return false;

    var installed = 0;
    if (attachRoomHook(mod, 'GameManager.Awake', RVA.GameManager_Awake, {
      onLeave: function () { triggerRoomReadyApply('GameManager.Awake', true); }
    })) installed += 1;

    if (attachRoomHook(mod, 'ModeBase.Update', RVA.ModeBase_Update, {
      onEnter: function () { triggerRoomReadyApply('ModeBase.Update', false); }
    })) installed += 1;

    if (attachRoomHook(mod, 'Bot.Update', RVA.Bot_Update, {
      onEnter: function () { triggerRoomReadyApply('Bot.Update', false); }
    })) installed += 1;

    if (attachRoomHook(mod, 'ModeBase.ExitGame', RVA.ModeBase_ExitGame, {
      onEnter: function () { clearRoomState('ModeBase.ExitGame'); }
    })) installed += 1;

    if (attachRoomHook(mod, 'GameManager.OnDestroy', RVA.GameManager_OnDestroy, {
      onEnter: function () { clearRoomState('GameManager.OnDestroy'); }
    })) installed += 1;

    state.hooksInstalled = installed > 0;
    if (!state.hooksInstalled) {
      state.lastError = 'no room-ready hooks installed';
      return false;
    }
    return true;
  }

  function applyEnabledState(reason) {
    if (!state.enabled) {
      state.pendingApply = false;
      state.applied = false;
      state.lastApplyReason = reason || 'disabled';
      clearRoomReadyRetry();
      return { ok: true, enabled: false, pendingApply: false, applied: false };
    }

    var result = writeStopAllBot(true);
    state.lastApplyReason = reason || 'apply_enabled_state';
    if (result.ok) {
      state.pendingApply = false;
      state.applied = true;
      clearRoomReadyRetry();
      return result;
    }

    state.pendingApply = true;
    state.applied = false;
    return result;
  }

  function startRoomReadyRetry(reason) {
    state.pendingApply = true;
    state.lastApplyReason = reason || 'room_ready_retry';
    if (state.retryTimer !== null) return;

    state.retryTimer = setInterval(function () {
      if (!state.enabled) {
        clearRoomReadyRetry();
        return;
      }
      state.retryCount += 1;
      var result = applyEnabledState('room_ready_retry');
      if (result.ok) {
        sendLog('info', 'room-ready retry applied Bot.stopAllBot = true');
      } else if (state.retryCount === 1 || state.retryCount % 10 === 0) {
        sendLog('warn', 'waiting for Bot.stopAllBot to become writable: ' + (result.msg || 'unknown'));
      }
    }, 500);
  }

  function getGameAssembly() {
    try {
      var mod = Process.findModuleByName('GameAssembly.dll');
      if (!mod) {
        state.lastError = 'GameAssembly.dll not found';
        return null;
      }
      return mod;
    } catch (e) {
      setError('find GameAssembly failed', e);
      return null;
    }
  }

  function readPointerAt(addr, label) {
    try {
      if (!addr || addr.isNull()) {
        state.lastError = label + ' address is null';
        return null;
      }
      var value = addr.readPointer();
      if (!value || value.isNull()) {
        state.lastError = label + ' pointer is null';
        return null;
      }
      return value;
    } catch (e) {
      setError('readPointer failed at ' + label + ' ' + safeString(addr), e);
      return null;
    }
  }

  function readU8(addr, label) {
    try {
      if (!addr || addr.isNull()) {
        state.lastError = label + ' address is null';
        return null;
      }
      return addr.readU8();
    } catch (e) {
      setError('readU8 failed at ' + label + ' ' + safeString(addr), e);
      return null;
    }
  }

  function writeU8(addr, value, label) {
    try {
      if (!addr || addr.isNull()) {
        state.lastError = label + ' address is null';
        return false;
      }
      addr.writeU8(value);
      var readBack = addr.readU8();
      if (readBack !== value) {
        state.lastError = label + ' verify failed: wrote=' + value + ', readBack=' + readBack;
        return false;
      }
      state.writeCount += 1;
      return true;
    } catch (e) {
      setError('writeU8 failed at ' + label + ' ' + safeString(addr), e);
      return false;
    }
  }

  function resolveStopAllBot() {
    var mod = getGameAssembly();
    if (!mod) return { ok: false, msg: state.lastError || 'GameAssembly.dll not found' };

    var warnings = [];
    if (Process.pointerSize !== 4) {
      warnings.push('unexpected pointerSize=' + Process.pointerSize + ', offsets were verified for 32-bit GameAssembly');
    }

    var typeInfoPtrAddr = mod.base.add(RVA.Bot_TypeInfo);
    var typeInfo = readPointerAt(typeInfoPtrAddr, 'Bot_TypeInfo');
    if (!typeInfo) return { ok: false, msg: state.lastError || 'Bot_TypeInfo pointer is null' };

    var staticFieldsAddr = typeInfo.add(OFF.Il2CppClass_static_fields);
    var staticFields = readPointerAt(staticFieldsAddr, 'Bot.static_fields');
    if (!staticFields) {
      return {
        ok: false,
        msg: state.lastError || 'Bot static_fields pointer is null',
        base: mod.base.toString(),
        pointerSize: Process.pointerSize,
        typeInfoPtrAddr: typeInfoPtrAddr.toString(),
        typeInfo: typeInfo.toString(),
        staticFieldsAddr: staticFieldsAddr.toString(),
        warning: 'static_fields is null. This version does not call any runtime metadata API by user rule.'
      };
    }

    var fieldAddr = staticFields.add(OFF.Bot_stopAllBot);
    var resolved = {
      ok: true,
      base: mod.base.toString(),
      pointerSize: Process.pointerSize,
      typeInfoPtrAddr: typeInfoPtrAddr.toString(),
      typeInfo: typeInfo.toString(),
      staticFieldsAddr: staticFieldsAddr.toString(),
      staticFields: staticFields.toString(),
      staticFieldsPtr: staticFields,
      fieldAddrPtr: fieldAddr,
      fieldAddr: fieldAddr.toString(),
      warnings: warnings
    };

    state.lastResolved = {
      base: resolved.base,
      typeInfoPtrAddr: resolved.typeInfoPtrAddr,
      typeInfo: resolved.typeInfo,
      staticFieldsAddr: resolved.staticFieldsAddr,
      staticFields: resolved.staticFields,
      fieldAddr: resolved.fieldAddr
    };
    return resolved;
  }

  function readStopAllBot() {
    var resolved = resolveStopAllBot();
    if (!resolved.ok) {
      return {
        ok: false,
        msg: resolved.msg,
        enabled: state.enabled,
        writeCount: state.writeCount,
        lastError: state.lastError,
        pointerSize: Process.pointerSize,
        lastResolved: state.lastResolved,
        warning: resolved.warning
      };
    }

    var currentValue = readU8(resolved.fieldAddrPtr, 'Bot.stopAllBot');
    if (currentValue === null) {
      return {
        ok: false,
        msg: state.lastError || 'failed to read Bot.stopAllBot',
        enabled: state.enabled,
        writeCount: state.writeCount,
        lastError: state.lastError,
        lastResolved: state.lastResolved
      };
    }

    return {
      ok: true,
      currentValue: currentValue,
      paused: currentValue !== 0,
      enabled: state.enabled,
      writeCount: state.writeCount,
      lastError: state.lastError,
      base: resolved.base,
      pointerSize: resolved.pointerSize,
      typeInfoPtrAddr: resolved.typeInfoPtrAddr,
      typeInfo: resolved.typeInfo,
      staticFieldsAddr: resolved.staticFieldsAddr,
      staticFields: resolved.staticFields,
      fieldAddr: resolved.fieldAddr,
      warnings: resolved.warnings
    };
  }

  function writeStopAllBot(paused) {
    var resolved = resolveStopAllBot();
    if (!resolved.ok) return resolved;

    var target = paused ? 1 : 0;
    var current = readU8(resolved.fieldAddrPtr, 'Bot.stopAllBot(before write)');
    if (current === null) {
      return { ok: false, msg: state.lastError || 'failed to read Bot.stopAllBot before write' };
    }

    if (current === target) {
      state.enabled = paused;
      state.applied = paused;
      state.pendingApply = false;
      state.lastError = null;
      return {
        ok: true,
        changed: false,
        msg: paused ? 'bots already paused' : 'bots already resumed',
        currentValue: current,
        paused: paused,
        enabled: state.enabled,
        writeCount: state.writeCount,
        fieldAddr: resolved.fieldAddr,
        warnings: resolved.warnings
      };
    }

    if (!writeU8(resolved.fieldAddrPtr, target, 'Bot.stopAllBot')) {
      return { ok: false, msg: state.lastError || 'failed to write Bot.stopAllBot' };
    }

    state.enabled = paused;
    state.applied = paused;
    state.pendingApply = false;
    state.lastError = null;
    return {
      ok: true,
      changed: true,
      msg: paused ? 'bots paused' : 'bots resumed',
      currentValue: target,
      paused: paused,
      enabled: state.enabled,
      writeCount: state.writeCount,
      fieldAddr: resolved.fieldAddr,
      warnings: resolved.warnings
    };
  }

  function applyConfig(config) {
    return { ok: true, config: config || {} };
  }

  rpc.exports = {
    enable: function () {
      state.enabled = true;
      installRoomReadyHooks();
      var result = applyEnabledState('enable');
      if (!result.ok) startRoomReadyRetry('enable');
      sendLog(result.ok ? 'success' : 'warn', result.msg || safeString(result));
      return result;
    },

    disable: function () {
      clearRoomReadyRetry();
      detachRoomReadyHooks();
      state.enabled = false;
      state.pendingApply = false;
      state.applied = false;
      var result = writeStopAllBot(false);
      sendLog(result.ok ? 'info' : 'error', result.msg || safeString(result));
      return result;
    },

    status: function () {
      var result = readStopAllBot();
      result.pendingApply = state.pendingApply;
      result.applied = state.applied;
      result.retryCount = state.retryCount;
      result.hooksInstalled = state.hooksInstalled;
      result.roomGeneration = state.roomGeneration;
      result.lastApplyReason = state.lastApplyReason;
      return result;
    },

    setConfig: function (config) {
      return applyConfig(config);
    },

    setconfig: function (config) {
      return applyConfig(config);
    },

    cleanup: function (payload) {
      clearRoomReadyRetry();
      detachRoomReadyHooks();
      state.pendingApply = false;
      state.applied = false;
      var result = writeStopAllBot(false);
      state.enabled = false;
      if (result.ok) sendLog('info', 'cleanup restored Bot.stopAllBot = false');
      else sendLog('warn', 'cleanup failed: ' + (result.msg || 'unknown'));
      return result;
    },

    dispose: function () {
      return this.cleanup();
    }
  };

  sendLog('info', 'script loaded; no runtime metadata API; pointerSize=' + Process.pointerSize);
})();
