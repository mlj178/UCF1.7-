// time_freeze.js - 无限时间模块
// 锁定游戏时间为 99:59，永不结束

modules.time = (function() {
  var hooks = [];
  var intervalId = null;
  var enabled = false;
  var modeBaseInstance = null;
  var pauseUntil = 0;

  function safeModifyTime(instance, minute, second) {
    try {
      if (!instance || instance.equals(ptr(0))) return false;
      if (instance.compare(ptr(0x10000)) < 0) return false;
      instance.add(0x34).writeS32(minute);
      instance.add(0x38).writeS32(second);
      return true;
    } catch(e) { return false; }
  }

  function readCurrentTime(instance) {
    try {
      if (!instance || instance.equals(ptr(0))) return null;
      var minute = instance.add(0x34).readS32();
      var second = instance.add(0x38).readS32();
      if (minute < 0 || minute > 200 || second < 0 || second > 59) return null;
      return { minute: minute, second: second };
    } catch(e) { return null; }
  }

  return {
    enable: function() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) { sendLog('error', '无限时间', '无 GameAssembly.dll'); return; }

      var base = mod.base;

      var h1 = Interceptor.attach(base.add(0xAF6930), {
        onEnter: function(args) {
          if (Date.now() < pauseUntil) return;
          var instance = args[0];
          if (!modeBaseInstance || !instance.equals(modeBaseInstance)) {
            modeBaseInstance = instance;
            sendLog('info', '无限时间', '新 ModeBase 实例: ' + instance);
          }
          if (modeBaseInstance) {
            var ct = readCurrentTime(modeBaseInstance);
            if (ct && ct.minute < 90) safeModifyTime(modeBaseInstance, 99, 59);
          }
        }
      });
      hooks.push(h1);

      var h2 = Interceptor.attach(base.add(0xAFAA40), {
        onEnter: function() { modeBaseInstance = null; }
      });
      hooks.push(h2);

      var h3 = Interceptor.attach(base.add(0xAEF8A0), {
        onEnter: function(args) {
          if (Date.now() < pauseUntil) return;
          var newInstance = args[0];
          if (!modeBaseInstance || !newInstance.equals(modeBaseInstance)) {
            modeBaseInstance = newInstance;
            sendLog('info', '无限时间', 'Nano 新实例: ' + modeBaseInstance);
          }
          var ct = readCurrentTime(modeBaseInstance);
          if (ct && ct.minute < 90) safeModifyTime(modeBaseInstance, 99, 59);
        }
      });
      hooks.push(h3);

      var h4 = Interceptor.attach(base.add(0xAF1920), {
        onEnter: function() { modeBaseInstance = null; }
      });
      hooks.push(h4);

      intervalId = setInterval(function() {
        if (Date.now() < pauseUntil) return;
        if (modeBaseInstance) {
          var ct = readCurrentTime(modeBaseInstance);
          if (ct && ct.minute < 90) safeModifyTime(modeBaseInstance, 99, 59);
        }
      }, 1000);

      enabled = true;
      sendLog('success', '无限时间', '已启用 (' + hooks.length + ' Hook + 1s 定时器)');
      sendStatus('time', true);
    },
    disable: function() {
      if (!enabled) return;
      for (var i = 0; i < hooks.length; i++) hooks[i].detach();
      hooks = [];
      if (intervalId) { clearInterval(intervalId); intervalId = null; }
      modeBaseInstance = null; enabled = false;
      sendLog('info', '无限时间', '已禁用');
      sendStatus('time', false);
    },
    pauseFor: function(ms) {
      pauseUntil = Date.now() + ms;
    }
  };
})();
