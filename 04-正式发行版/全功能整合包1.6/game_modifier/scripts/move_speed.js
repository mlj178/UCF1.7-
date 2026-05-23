// move_speed.js - 滑板鞋 (Move Speed)
// Hook PropertyModifier.Get，拦截 MoveSpeedRatio Modifier 的查询，为本地玩家返回倍数后的值

modules.movespeed = (function() {
  var enabled = false;
  var currentSpeed = 3.0;
  var hookAddr = null;
  var isMyPlayerFn = null;
  var originalFn = null;
  var logCount = 0;

  return {
    setSpeed: function(speed) {
      currentSpeed = speed;
      if (enabled) {
        sendLog('info', '滑板鞋', '速度已切换: ' + speed + 'x（实时生效）');
      } else {
        sendLog('info', '滑板鞋', '速度已预选: ' + speed + 'x（开启后生效）');
      }
    },
    enable: function() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) { sendLog('error', '滑板鞋', '无 GameAssembly.dll'); return; }

      var base = mod.base;
      hookAddr = base.add(0xB17590);
      isMyPlayerFn = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
      originalFn = new NativeFunction(hookAddr, 'float', ['pointer', 'pointer']);
      logCount = 0;

      Interceptor.replace(hookAddr, new NativeCallback(function(self, player) {
        var result = originalFn(self, player);
        if (player && !player.isNull() && isMyPlayerFn(player)) {
          var moveMod = player.add(0x8C).readPointer();
          if (moveMod && !moveMod.isNull() && self.equals(moveMod)) {
            logCount++;
            if (logCount <= 10)
              sendLog('info', '滑板鞋', '原值=' + result.toFixed(3) + ' 修改后=' + currentSpeed.toFixed(1) + 'x');
            return currentSpeed;
          }
        }
        return result;
      }, 'float', ['pointer', 'pointer']));

      enabled = true;
      sendLog('success', '滑板鞋', '已启用 (' + currentSpeed + 'x) — 仅对玩家生效');
      sendStatus('movespeed', true);
    },
    disable: function() {
      if (!enabled || !hookAddr) return;
      Interceptor.revert(hookAddr);
      enabled = false;
      sendLog('info', '滑板鞋', '已禁用');
      sendStatus('movespeed', false);
    }
  };
})();
