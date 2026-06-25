// is_bot.js - 天机傀儡，修改 ClientData.isBot
// 通过替换 isMyPlayer 捕获 localPlayer，再直接写入 isBot 字节。

modules.isbot = (function() {
  var enabled = false;
  var localPlayer = null;
  var clientData = null;
  var logCount = 0;
  var MAX_LOG = 15;
  var hookInstalled = false;
  var retryInterval = null;
  var addrIsMy = null;
  var roomCaptureCount = 0;

  var RVA_IS_MY_PLAYER = 0xB55FD0;
  var OFF_CLIENT = 0x94;
  var OFF_ISBOT = 0x1C;
  var OFF_NICK = 0x10;

  function log(level, msg) {
    if (logCount >= MAX_LOG && level !== 'error') return;
    logCount++;
    send({ type: 'log', level: level, module: 'isBot', message: msg });
  }

  function sendUiState(state) {
    send({ type: 'isbot_state', state: state });
  }

  function readStr(p) {
    try {
      var obj = p.readPointer();
      if (!obj || obj.isNull()) return '?';
      var len = obj.add(-4).readS32();
      if (len < 0 || len > 64) return '?';
      return obj.readUtf8String(len);
    } catch (e) {
      return '?';
    }
  }

  function dump() {
    if (!clientData) return;
    var bot = clientData.add(OFF_ISBOT).readU8();
    var nick = readStr(clientData.add(OFF_NICK));
    log('info', localPlayer + '|' + clientData + '|0x1C:' + bot + '|nick:' + nick);
  }

  function writeBot(val) {
    if (!clientData) return false;
    try {
      clientData.add(OFF_ISBOT).writeU8(val);
      var after = clientData.add(OFF_ISBOT).readU8();
      log('info', 'isBot=' + after + ' (写入 ' + val + ')');
      return true;
    } catch (e) {
      return false;
    }
  }

  function tryWriteBotOnCapture() {
    if (!clientData) {
      return false;
    }

    var ok = writeBot(1);
    if (ok) {
      sendLog('info', '天机傀儡', 'Bot 模式已写入');
      if (retryInterval) {
        clearInterval(retryInterval);
        retryInterval = null;
      }
    }
    return ok;
  }

  function handlePlayerCapture(playerPtr) {
    if (localPlayer && playerPtr.equals(localPlayer)) {
      return;
    }

    localPlayer = playerPtr;

    var cd = playerPtr.add(OFF_CLIENT).readPointer();
    if (!cd || cd.isNull()) {
      return;
    }

    clientData = cd;
    roomCaptureCount += 1;
    setTimeout(dump, 2000);

    if (!enabled) {
      return;
    }

    if (tryWriteBotOnCapture()) {
      if (roomCaptureCount >= 2) {
        sendUiState('active');
      } else {
        sendUiState('awaiting_reenter');
      }
    }
  }

  function installHook() {
    if (hookInstalled) return;
    try {
      var mod = getGameAssembly();
      if (!mod) {
        sendBothLog('error', '天机傀儡', '天机傀儡暂未就绪，请重新连接游戏后重试', 'IsBot GameAssembly.dll not found');
        return;
      }

      var base = mod.base;
      addrIsMy = base.add(RVA_IS_MY_PLAYER);
      var origIsMy = new NativeFunction(addrIsMy, 'bool', ['pointer', 'pointer']);

      Interceptor.replace(addrIsMy, new NativeCallback(function(playerPtr, methodInfo) {
        var result = origIsMy(playerPtr, methodInfo);
        if (result) {
          handlePlayerCapture(playerPtr);
        }
        return result;
      }, 'bool', ['pointer', 'pointer']));

      hookInstalled = true;
    } catch (e) {
      sendBothLog('error', '天机傀儡', '天机傀儡初始化失败，请稍后重试', 'IsBot hook install failed: ' + (e.message || e));
    }
  }

  function uninstallHook() {
    if (hookInstalled && addrIsMy) {
      try {
        Interceptor.revert(addrIsMy);
      } catch (e) {}
      hookInstalled = false;
      addrIsMy = null;
    }
  }

  return {
    enable: function() {
      if (enabled) return;

      installHook();
      enabled = true;
      sendUiState('awaiting_room');

      if (tryWriteBotOnCapture()) {
        sendLog('success', '天机傀儡', '已启用');
        sendStatus('isbot', true);
        sendUiState(roomCaptureCount >= 2 ? 'active' : 'awaiting_reenter');
        return;
      }

      var retries = 0;
      retryInterval = setInterval(function() {
        if (clientData) {
          tryWriteBotOnCapture();
        }
        retries++;
        if (retries > 20) {
          clearInterval(retryInterval);
          retryInterval = null;
          sendBothLog('warn', '天机傀儡', '暂未捕获本地玩家，请进入房间后重新尝试', 'IsBot waiting for local player timed out');
        }
      }, 500);

      sendLog('success', '天机傀儡', '已启用（等待本地玩家）');
      sendStatus('isbot', true);
    },
    disable: function() {
      if (!enabled) return;
      if (retryInterval) {
        clearInterval(retryInterval);
        retryInterval = null;
      }
      writeBot(0);
      uninstallHook();
      enabled = false;
      localPlayer = null;
      clientData = null;
      roomCaptureCount = 0;
      log('info', '已禁用');
      sendStatus('isbot', false);
      sendUiState('off');
    },
    isEnabled: function() {
      return enabled;
    },
    modify: function() {
      if (writeBot(1)) return JSON.stringify({ success: true, bot: 1 });
      return JSON.stringify({ success: false });
    },
    restore: function() {
      if (writeBot(0)) return JSON.stringify({ success: true, bot: 0 });
      return JSON.stringify({ success: false });
    },
    stop: function() {
      if (writeBot(0)) return JSON.stringify({ success: true, bot: 0 });
      return JSON.stringify({ success: false });
    },
    status: function() {
      return JSON.stringify({
        player: localPlayer ? localPlayer.toString() : null,
        cd: clientData ? clientData.toString() : null,
        bot: clientData ? clientData.add(OFF_ISBOT).readU8() : null,
        roomCaptureCount: roomCaptureCount
      });
    }
  };
})();
