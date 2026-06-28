// ============================================================
// AAAAA-bot_pause_min.js - Bot pause minimum implementation
//
// Goal:
//   Toggle Bot.stopAllBot by writing the Bot static field.
//
// Verified data:
//   Bot_TypeInfo:    0xE25F44
//   static_fields:   Bot_c + 0x5C
//   Bot_stopAllBot:  0xC
// ============================================================

(function () {
  'use strict';

  var RVA = {
    Bot_TypeInfo: 0xE25F44
  };

  var OFF = {
    Bot_stopAllBot: 0xC
  };

  var state = {
    enabled: false,
    lastError: null,
    writeCount: 0
  };

  function sendLog(level, message) {
    try {
      console.log('[bot_pause][' + level + '] ' + message);
      send({ type: 'log', level: level, module: 'bot_pause', message: message });
    } catch (e) {
    }
  }

  function getGameAssembly() {
    try {
      return Process.findModuleByName('GameAssembly.dll');
    } catch (e) {
      state.lastError = 'find GameAssembly failed: ' + e.message;
      return null;
    }
  }

  function readPointer(addr) {
    try {
      if (!addr || addr.isNull()) return null;
      var value = addr.readPointer();
      if (!value || value.isNull()) return null;
      return value;
    } catch (e) {
      state.lastError = 'readPointer failed: ' + e.message;
      return null;
    }
  }

  function readU8(addr) {
    try {
      if (!addr || addr.isNull()) return null;
      return addr.readU8();
    } catch (e) {
      state.lastError = 'readU8 failed: ' + e.message;
      return null;
    }
  }

  function writeU8(addr, value) {
    try {
      if (!addr || addr.isNull()) return false;
      addr.writeU8(value);
      state.writeCount += 1;
      return true;
    } catch (e) {
      state.lastError = 'writeU8 failed: ' + e.message;
      return false;
    }
  }

  function resolveStopAllBot() {
    var mod = getGameAssembly();
    if (!mod) {
      return { ok: false, msg: 'GameAssembly.dll not found' };
    }

    var typeInfo = readPointer(mod.base.add(RVA.Bot_TypeInfo));
    if (!typeInfo) {
      return { ok: false, msg: 'Bot_TypeInfo pointer is null' };
    }

    var staticFields = readPointer(typeInfo.add(0x5C));
    if (!staticFields) {
      return { ok: false, msg: 'Bot static_fields pointer is null' };
    }

    return {
      ok: true,
      base: mod.base.toString(),
      typeInfo: typeInfo.toString(),
      staticFields: staticFields.toString(),
      staticFieldsPtr: staticFields,
      fieldAddr: staticFields.add(OFF.Bot_stopAllBot)
    };
  }

  function readStopAllBot() {
    var resolved = resolveStopAllBot();
    if (!resolved.ok) return resolved;

    var staticFields = resolved.staticFieldsPtr;
    var currentValue = readU8(staticFields.add(OFF.Bot_stopAllBot));
    if (currentValue === null) {
      return { ok: false, msg: 'failed to read Bot.stopAllBot' };
    }

    return {
      ok: true,
      currentValue: currentValue,
      paused: currentValue !== 0,
      base: resolved.base,
      typeInfo: resolved.typeInfo,
      staticFields: resolved.staticFields,
      fieldAddr: resolved.fieldAddr.toString()
    };
  }

  function writeStopAllBot(paused) {
    var resolved = resolveStopAllBot();
    if (!resolved.ok) return resolved;

    var staticFields = resolved.staticFieldsPtr;
    if (paused) {
      if (!writeU8(staticFields.add(OFF.Bot_stopAllBot), 1)) {
        return { ok: false, msg: 'failed to write Bot.stopAllBot' };
      }
    } else {
      if (!writeU8(staticFields.add(OFF.Bot_stopAllBot), 0)) {
        return { ok: false, msg: 'failed to write Bot.stopAllBot' };
      }
    }

    state.enabled = paused;
    state.lastError = null;

    return {
      ok: true,
      msg: paused ? 'bots paused' : 'bots resumed',
      currentValue: paused ? 1 : 0,
      paused: paused,
      fieldAddr: resolved.fieldAddr.toString()
    };
  }

  rpc.exports = {
    enable: function () {
      var result = writeStopAllBot(true);
      if (result.ok) {
        sendLog('success', 'Bot.stopAllBot = true');
      } else {
        sendLog('error', result.msg);
      }
      return result;
    },

    disable: function () {
      var result = writeStopAllBot(false);
      if (result.ok) {
        sendLog('info', 'Bot.stopAllBot = false');
      } else {
        sendLog('error', result.msg);
      }
      return result;
    },

    status: function () {
      var result = readStopAllBot();
      result.enabled = state.enabled;
      result.writeCount = state.writeCount;
      result.lastError = state.lastError;
      return result;
    },

    cleanup: function () {
      var result = writeStopAllBot(false);
      state.enabled = false;
      if (result.ok) {
        sendLog('info', 'cleanup restored Bot.stopAllBot = false');
      }
      return result;
    }
  };

  sendLog('info', 'script loaded');
})();
