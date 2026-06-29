// recoil.js - 无后座力 v14
// 替换 Recoil.OnGunShot，将后座力相关字段归零

modules.recoil = (function() {
  var replacedAddr = null;
  var callbackFunc = null;
  var enabled = false;
  var suppressCount = 0;

  return {
    enable: function() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) { sendBothLog('error', '无后座力', '无后座力暂未就绪，请重新连接游戏后重试', 'NoRecoil GameAssembly.dll not found'); return; }

      var base = mod.base;
      replacedAddr = base.add(0xB19980);
      sendLog('info', '无后座力', 'Recoil$$OnGunShot @ ' + replacedAddr);

      suppressCount = 0;

      callbackFunc = new NativeCallback(function(recoilThis, methodInfo) {
        suppressCount++;
        try {
          recoilThis.add(0x68).writeFloat(0.0);
          recoilThis.add(0x6C).writeFloat(0.0);
          recoilThis.add(0x70).writeFloat(0.0);
          recoilThis.add(0x74).writeFloat(0.0);
        } catch (e) {}

        if (suppressCount <= 3) {
          sendLog('info', '无后座力', '[Suppress #' + suppressCount + '] ' + recoilThis);
        } else if (suppressCount === 4) {
          sendLog('info', '无后座力', '...suppressing silently');
        }
      }, 'void', ['pointer', 'pointer']);

      try {
        Interceptor.replace(replacedAddr, callbackFunc);
        sendLog('success', '无后座力', '已替换 Recoil.OnGunShot');
      } catch(e) {
        sendBothLog('error', '无后座力', '无后座力启用失败，请稍后重试', 'NoRecoil replace failed: ' + e.message);
        return;
      }

      enabled = true;
      sendLog('success', '无后座力', 'v14 已启用 (replace OnGunShot + zero 4 fields)');
      sendStatus('recoil', true);
    },
    disable: function() {
      if (!enabled) return;
      if (replacedAddr) { try { Interceptor.revert(replacedAddr); } catch(e) {} }
      callbackFunc = null; replacedAddr = null;
      enabled = false;
      sendLog('info', '无后座力', '已禁用');
      sendStatus('recoil', false);
    }
  };
})();
