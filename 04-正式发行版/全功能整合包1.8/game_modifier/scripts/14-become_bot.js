// is_bot.js - 天机傀儡 — 修改 ClientData.isBot (v2)
// replace isMyPlayer 捕获localPlayer → 读取clientData → 直接写 isBot 字节

modules.isbot = (function() {
  var enabled = false;
  var localPlayer = null;
  var clientData = null;
  var dumped = false;
  var logCount = 0;
  var MAX_LOG = 15;
  var hookInstalled = false;
  var retryInterval = null;
  var addrIsMy = null;

  var RVA_IS_MY_PLAYER = 0xB55FD0;
  var OFF_CLIENT = 0x94;
  var OFF_ISBOT = 0x1C;
  var OFF_NICK = 0x10;

  function log(level, msg) {
    if (logCount >= MAX_LOG && level !== 'error') return;
    logCount++;
    send({ type: 'log', level: level, module: 'isBot', message: msg });
  }

  function readStr(p) {
    try {
      var obj = p.readPointer();
      if (!obj || obj.isNull()) return '?';
      var len = obj.add(-4).readS32();
      if (len < 0 || len > 64) return '?';
      return obj.readUtf8String(len);
    } catch(e) { return '?'; }
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
      log('info', 'isBot=' + after + ' (写入' + val + ')');
      return true;
    } catch(e) { return false; }
  }

  function tryWriteBotOnCapture() {
    if (clientData) {
      writeBot(1);
      sendLog('info', '天机傀儡', 'Bot 模式已应用');
      if (retryInterval) {
        clearInterval(retryInterval);
        retryInterval = null;
      }
      return true;
    }
    return false;
  }

  function installHook() {
    if (hookInstalled) return;
    try {
      var mod = getGameAssembly();
      if (!mod) { sendLog('error', '天机傀儡', '未找到 GameAssembly.dll'); return; }

      var base = mod.base;
      addrIsMy = base.add(RVA_IS_MY_PLAYER);
      var origIsMy = new NativeFunction(addrIsMy, 'bool', ['pointer', 'pointer']);

      Interceptor.replace(addrIsMy, new NativeCallback(function (playerPtr, methodInfo) {
        var result = origIsMy(playerPtr, methodInfo);
        if (result && !localPlayer) {
          localPlayer = playerPtr;
          var cd = playerPtr.add(OFF_CLIENT).readPointer();
          if (cd) {
            clientData = cd;
            dumped = true;
            setTimeout(dump, 2000);
            tryWriteBotOnCapture();
          }
        }
        return result;
      }, 'bool', ['pointer', 'pointer']));

      hookInstalled = true;
    } catch(e) {
      sendLog('error', '天机傀儡', 'Hook安装失败: ' + (e.message || e));
    }
  }

  function uninstallHook() {
    if (hookInstalled && addrIsMy) {
      try { Interceptor.revert(addrIsMy); } catch(e) {}
      hookInstalled = false;
      addrIsMy = null;
    }
  }

  return {
    enable: function() {
      if (enabled) return;

      installHook();

      if (tryWriteBotOnCapture()) {
        enabled = true;
        sendLog('success', '天机傀儡', '已启用');
        sendStatus('isbot', true);
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
          sendLog('error', '天机傀儡', '等待本地玩家超时');
        }
      }, 500);

      enabled = true;
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
      log('info', '已禁用');
      sendStatus('isbot', false);
    },
    isEnabled: function() { return enabled; },
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
        bot: clientData ? clientData.add(OFF_ISBOT).readU8() : null
      });
    }
  };
})();
