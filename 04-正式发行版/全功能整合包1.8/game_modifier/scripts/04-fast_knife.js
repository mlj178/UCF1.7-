// knife.js - 快刀模块 v16 (NativeCallback Replace)
// 替换 PlayerWeapons.get_KnifeSpeed，为本地玩家返回指定的速度倍数

modules.knife = (function() {
  var enabled = false;
  var currentSpeed = 5.0;
  var isMyPlayer = null;
  var originalGetKnifeSpeed = null;
  var getKnifeSpeedAddr = null;
  var logCount = 0;

  return {
    setSpeed: function(speed) {
      currentSpeed = speed;
      if (enabled) {
        sendLog('info', '快刀', '速度已切换: ' + speed + 'x（实时生效）');
      } else {
        sendLog('info', '快刀', '速度已预选: ' + speed + 'x（开启后生效）');
      }
    },
    enable: function() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) { sendBothLog('error', '快刀', '快刀暂未就绪，请重新连接游戏后重试', 'Knife GameAssembly.dll not found'); return; }

      var base = mod.base;
      var isMyPlayerAddr = base.add(0xB55FD0);
      getKnifeSpeedAddr = base.add(0xB170A0);

      sendLog('info', '快刀', 'isMyPlayer @ ' + isMyPlayerAddr);
      sendLog('info', '快刀', 'get_KnifeSpeed @ ' + getKnifeSpeedAddr);

      isMyPlayer = new NativeFunction(isMyPlayerAddr, 'bool', ['pointer']);
      originalGetKnifeSpeed = new NativeFunction(getKnifeSpeedAddr, 'float', ['pointer']);

      logCount = 0;

      Interceptor.replace(getKnifeSpeedAddr, new NativeCallback(function(self) {
        try {
          var owner = self.add(0x8).readPointer();
          if (!owner || owner.isNull()) {
            return originalGetKnifeSpeed(self);
          }

          if (isMyPlayer(owner)) {
            logCount++;
            if (logCount <= 10) {
              sendLog('info', '快刀', '[KnifeSpeed] Player detected, returning ' + currentSpeed);
            }
            return currentSpeed;
          }

          return originalGetKnifeSpeed(self);
        } catch(e) {
          sendDevLog('error', '快刀', '快刀 Hook 回调异常: ' + e.message, 'KnifeSpeed callback error');
          return originalGetKnifeSpeed(self);
        }
      }, 'float', ['pointer']));

      enabled = true;
      sendLog('success', '快刀', '已启用 (v16, Speed=' + currentSpeed + 'x) — 仅对玩家生效');
      sendStatus('knife', true);
    },
    disable: function() {
      if (!enabled) return;
      if (getKnifeSpeedAddr) {
        try { Interceptor.revert(getKnifeSpeedAddr); } catch(e) {}
      }
      isMyPlayer = null;
      originalGetKnifeSpeed = null;
      getKnifeSpeedAddr = null;
      enabled = false;
      sendLog('info', '快刀', '已禁用');
      sendStatus('knife', false);
    }
  };
})();
