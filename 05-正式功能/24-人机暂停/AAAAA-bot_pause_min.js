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
//   5. No timers / no background JS threads.
// ============================================================

(function () {
  'use strict';

  var RVA = {
    Bot_TypeInfo: 0xE25F44
  };

  var OFF = {
    Il2CppClass_static_fields: 0x5C,
    Bot_stopAllBot: 0xC
  };

  var state = {
    enabled: false,
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

  rpc.exports = {
    enable: function () {
      var result = writeStopAllBot(true);
      sendLog(result.ok ? 'success' : 'error', result.msg || safeString(result));
      return result;
    },

    disable: function () {
      var result = writeStopAllBot(false);
      sendLog(result.ok ? 'info' : 'error', result.msg || safeString(result));
      return result;
    },

    status: function () {
      return readStopAllBot();
    },

    cleanup: function () {
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
