// skill_cd.js - 生化模式-英雄技能无冷却
// 3路Hook(isMyPlayer replace + Player.Update attach + get_nickName attach) + 200ms定时器调用 EndCold()

modules.skillcd = (function() {
  var enabled = false;
  var myPlayerPtr = null;
  var _endColdFn = null;
  var _noCdTimer = null;
  var hooks = [];

  function readPtr(addr) {
    try { if (!addr || addr.isNull()) return null; var v = addr.readPointer(); return (v && !v.isNull()) ? v : null; } catch (e) { return null; }
  }
  function readI32(addr) { try { return addr ? addr.readS32() : null; } catch (e) { return null; } }
  function readF32(addr) { try { return addr ? addr.readFloat() : null; } catch (e) { return null; } }
  function readU8(addr) { try { return addr ? addr.readU8() : null; } catch (e) { return null; } }

  function scanSkillSteps(pp) {
    var ps = readPtr(pp.add(0xB0));
    if (!ps) { sendLog('error', '技能CD', 'PlayerSkills 为空'); return; }
    var arr = readPtr(ps.add(0x08));
    if (!arr) { sendLog('error', '技能CD', 'Skill[] 为空'); return; }
    var len = readI32(arr.add(0x0C));
    if (!len || len <= 0 || len > 20) return;
    var found = 0;
    for (var i = 0; i < len; i++) {
      var sp = readPtr(arr.add(0x10 + 4 * i));
      if (!sp) continue;
      var coldFinish = readF32(sp.add(0x1C));
      var coldTime = readF32(sp.add(0x24));
      if (coldFinish !== null || coldTime !== null) {
        found++;
      }
    }
    if (found > 0) {
      sendLog('info', '技能CD', '找到 ' + found + ' 个技能');
    }
  }

  function scanAndEndCold() {
    if (!myPlayerPtr) return;
    var ps = readPtr(myPlayerPtr.add(0xB0));
    if (!ps) return;
    var arr = readPtr(ps.add(0x08));
    if (!arr) return;
    var len = readI32(arr.add(0x0C));
    if (!len || len <= 0 || len > 20) return;

    var called = 0;
    for (var i = 0; i < len; i++) {
      var sp = readPtr(arr.add(0x10 + 4 * i));
      if (!sp) continue;
      var coldFinish = readF32(sp.add(0x1C));
      var coldTime = readF32(sp.add(0x24));
      if (coldFinish !== null || coldTime !== null) {
        try {
          _endColdFn(sp);
          called++;
        } catch (e) {}
      }
    }
  }

  return {
    enable: function() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) { sendLog('error', '技能CD', '未找到 GameAssembly.dll'); return; }
      var base = mod.base;

      try {
        _endColdFn = new NativeFunction(base.add(0xAE1BC0), 'void', ['pointer']);
        sendLog('info', '技能CD', 'EndCold 函数就绪 (RVA 0xAE1BC0)');
      } catch (e) {
        sendLog('error', '技能CD', 'EndCold 创建失败: ' + e);
        return;
      }

      // Hook isMyPlayer 来捕获玩家指针（支持房间切换时自动更新）
      try {
        var addrIsMy = base.add(0xB55FD0);
        var origIsMy = new NativeFunction(addrIsMy, 'bool', ['pointer', 'pointer']);
        Interceptor.replace(addrIsMy, new NativeCallback(function (playerPtr, methodInfo) {
          try {
            var result = origIsMy(playerPtr, methodInfo);
            if (result) {
              if (!myPlayerPtr || !myPlayerPtr.equals(playerPtr)) {
                myPlayerPtr = playerPtr;
                scanSkillSteps(playerPtr);
                sendLog('info', '技能CD', '玩家指针已更新: ' + playerPtr);
              }
            }
            return result;
          } catch (e) { return false; }
        }, 'bool', ['pointer', 'pointer']));
        hooks.push({ type: 'replace', addr: addrIsMy, orig: origIsMy });
        sendLog('success', '技能CD', 'isMyPlayer Hook OK');
      } catch (e) { sendLog('error', '技能CD', 'isMyPlayer Hook 失败: ' + e); }

      // 兜底 Hook Player.Update 来捕获玩家（支持房间切换时自动更新）
      try {
        var addrUpdate = base.add(0xB551D0);
        hooks.push(Interceptor.attach(addrUpdate, {
          onEnter: function (args) {
            var p = args[0];
            if (!p || p.isNull()) return;
            var cd = readPtr(p.add(0x94));
            if (!cd) return;
            if (readU8(cd.add(0x1C))) return;
            if (!myPlayerPtr || !myPlayerPtr.equals(p)) {
              myPlayerPtr = p;
              scanSkillSteps(p);
            }
          }
        }));
        sendLog('success', '技能CD', 'Player.Update Hook OK');
      } catch (e) { sendLog('warn', '技能CD', 'Player.Update Hook 失败: ' + e); }

      // 兜底 Hook get_nickName 来捕获玩家（支持房间切换时自动更新）
      try {
        var addrNick = base.add(0xB50810);
        hooks.push(Interceptor.attach(addrNick, {
          onEnter: function (args) {
            var p = args[0];
            if (!p || p.isNull()) return;
            var cd = readPtr(p.add(0x94));
            if (!cd) return;
            if (readU8(cd.add(0x1C))) return;
            if (!myPlayerPtr || !myPlayerPtr.equals(p)) {
              myPlayerPtr = p;
              scanSkillSteps(p);
            }
          }
        }));
        sendLog('success', '技能CD', 'get_nickName Hook OK');
      } catch (e) { sendLog('warn', '技能CD', 'get_nickName Hook 失败: ' + e); }

      // 立即执行一次，然后设置定时器
      scanAndEndCold();
      _noCdTimer = setInterval(scanAndEndCold, 200);

      enabled = true;
      sendLog('success', '技能CD', '已开启 — 每 200ms 调用 EndCold()');
      sendStatus('skillcd', true);
    },
    disable: function() {
      if (!enabled) return;

      for (var i = 0; i < hooks.length; i++) {
        try {
          if (hooks[i].type === 'replace') {
            Interceptor.revert(hooks[i].addr);
          } else {
            hooks[i].detach();
          }
        } catch(e) {}
      }
      hooks = [];

      if (_noCdTimer) {
        clearInterval(_noCdTimer);
        _noCdTimer = null;
      }

      myPlayerPtr = null;
      enabled = false;
      sendLog('info', '技能CD', '已关闭');
      sendStatus('skillcd', false);
    },
    isEnabled: function() { return enabled; }
  };
})();
