// knife_range.js - 剑气化丝 (Knife Range)
// attach get_KnifeSpeed 捕获本地玩家指针，Hook GetKnifeAttackData 修改攻击距离

modules.range = (function() {
  var enabled = false;
  var KNIFE_RANGE_MULTIPLIER = 50.0;
  var myPlayer = null;
  var myPlayerFound = false;
  var callCount = 0;
  var rangeLogCount = 0;
  var isMyPlayerFn = null;
  var getKnifeSpeedAddr = null;
  var getKnifeSpeedHook = null;
  var getKnifeAttackDataAddr = null;
  var hookHandles = [];

  return {
    enable: function() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) { sendBothLog('error', '剑气化丝', '剑气化丝暂未就绪，请重新连接游戏后重试', 'KnifeRange GameAssembly.dll not found'); return; }

      var base = mod.base;
      isMyPlayerFn = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
      myPlayer = null;
      myPlayerFound = false;
      callCount = 0;
      rangeLogCount = 0;
      hookHandles = [];

      try {
        getKnifeSpeedAddr = base.add(0xB170A0);
        getKnifeSpeedHook = Interceptor.attach(getKnifeSpeedAddr, {
          onEnter: function(args) { this._self = args[0]; },
          onLeave: function(retval) {
            if (myPlayerFound) return;
            try {
              var owner = this._self.add(0x8).readPointer();
              if (owner && !owner.isNull() && isMyPlayerFn(owner)) {
                myPlayer = owner;
                myPlayerFound = true;
                sendLog('info', '剑气化丝', '捕获本地玩家 @ ' + myPlayer);
              }
            } catch(e) {}
          }
        });
        sendLog('info', '剑气化丝', 'get_KnifeSpeed attach @ ' + getKnifeSpeedAddr + ' (兼容模式)');
      } catch(e) {
        sendDevLog('warn', '剑气化丝', 'get_KnifeSpeed hook失败: ' + e.message, 'KnifeRange compatible player capture hook failed');
      }

      try {
        getKnifeAttackDataAddr = base.add(0xB63EC0);
        var h = Interceptor.attach(getKnifeAttackDataAddr, {
          onEnter: function(args) {
            this.wpnSelf = args[1];
            this.attackIdx = args[2].toInt32();
            try { this.owner = args[1].add(0x30).readPointer(); } catch(e) { this.owner = null; }
          },
          onLeave: function(retval) {
            callCount++;
            try {
              var orig = retval.add(0x4).readFloat();
              var isOwnerMine = myPlayerFound && this.owner && !this.owner.isNull() && this.owner.equals(myPlayer);
              if (!isOwnerMine) return;
              if (!(orig > 0.3 && orig < 500)) return;

              retval.add(0x4).writeFloat(orig * KNIFE_RANGE_MULTIPLIER);
              var after = retval.add(0x4).readFloat();

              rangeLogCount++;
              if (rangeLogCount <= 10) {
                sendLog('info', '剑气化丝', '攻击距离 ' + orig.toFixed(2) + ' → ' + after.toFixed(2) + ' (' + KNIFE_RANGE_MULTIPLIER + 'x)');
              }
            } catch(e) {
              if (callCount <= 5) sendDevLog('error', '剑气化丝', '攻击距离 Hook 回调异常: ' + e.message, 'KnifeRange callback exception');
            }
          }
        });
        hookHandles.push(h);
        sendLog('info', '剑气化丝', 'Hook GetKnifeAttackData @ ' + getKnifeAttackDataAddr);
      } catch(e) { sendBothLog('error', '剑气化丝', '剑气化丝启用失败，请稍后重试', 'KnifeRange GetKnifeAttackData hook failed: ' + e.message); }

      var cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
      for (var i = 0; i < cleanupAddrs.length; i++) {
        try {
          var h = Interceptor.attach(base.add(cleanupAddrs[i]), {
            onEnter: function() {
              myPlayer = null;
              myPlayerFound = false;
              callCount = 0;
              rangeLogCount = 0;
              sendLog('info', '剑气化丝', '房间切换，状态重置');
            }
          });
          hookHandles.push(h);
        } catch(e) {}
      }

      enabled = true;
      sendLog('success', '剑气化丝', '已启用 (' + KNIFE_RANGE_MULTIPLIER + 'x) — 仅对玩家生效');
      sendStatus('range', true);
    },
    disable: function() {
      if (!enabled) return;
      if (getKnifeSpeedHook) { try { getKnifeSpeedHook.detach(); } catch(e) {} }
      for (var i = 0; i < hookHandles.length; i++) { try { hookHandles[i].detach(); } catch(e) {} }
      getKnifeSpeedAddr = null;
      getKnifeSpeedHook = null;
      getKnifeAttackDataAddr = null;
      hookHandles = [];
      myPlayer = null;
      myPlayerFound = false;
      enabled = false;
      sendLog('info', '剑气化丝', '已禁用');
      sendStatus('range', false);
    },
    setRange: function(multiplier) {
      KNIFE_RANGE_MULTIPLIER = multiplier;
      sendLog('info', '剑气化丝', '攻击距离倍率已更新: ' + multiplier + 'x');
    }
  };
})();
