// round_skip.js - 回合跳过 (Round Skip)
// 将 ModeBase.restGameTime 设为 0:00 触发回合结束
// 冲突处理: 写入 0:00 前调用 timeModule.pauseFor(1000) 暂停无限时间 1 秒

modules.roundskip = (function() {
  var modeBaseInstance = null;
  var skipCount = 0, skipErrorCount = 0, roundActive = false, currentRound = 0;
  var inHook = false, skipGuard = false;
  var hooks = [];

  function pad2(n) { return n < 10 ? "0" + n : "" + n; }
  function addDevLog(level, message, detail) { sendDevLog(level, '回合跳过', message, detail || 'RoundSkip internal'); }
  function addUserLog(level, message) { sendUserLog(level, '回合跳过', message); }

  function isValidInstance(instance) {
    try { if (!instance || instance.equals(ptr(0))) return false; if (instance.compare(ptr(0x10000)) < 0) return false; instance.readU8(); return true; } catch (e) { return false; }
  }

  function skipRound() {
    if (skipGuard) return { ok: false, reason: 'guard_active' };
    var instance = modeBaseInstance;
    if (!isValidInstance(instance)) { skipErrorCount++; return { ok: false, reason: 'no_instance' }; }
    var minute = 0, second = 0;
    try { minute = instance.add(0x34).readS32(); second = instance.add(0x38).readS32(); } catch (e) { return { ok: false, reason: 'read_failed' }; }
    if (minute === 0 && second === 0) return { ok: false, reason: 'already_zero' };
    try {
      skipGuard = true;
      try { if (modules.time) modules.time.pauseFor(1000); } catch(e) {}
      instance.add(0x34).writeS32(0); instance.add(0x38).writeS32(0);
      skipCount++; roundActive = false;
      addDevLog('info', 'SKIP! ' + minute + ':' + pad2(second) + ' -> 0:00 (total:' + skipCount + ')', 'RoundSkip wrote restGameTime to 0:00');
      send({ type: 'round_skipped', from: minute + ':' + pad2(second), count: skipCount });
      skipGuard = false;
      return { ok: true };
    } catch (e) { skipGuard = false; skipErrorCount++; return { ok: false, reason: 'write_failed' }; }
  }

  function installHooks() {
    var mod = getGameAssembly();
    if (!mod) {
      addUserLog('error', '回合跳过暂未就绪，请重新连接游戏后重试');
      addDevLog('error', '无 GameAssembly.dll', 'RoundSkip installHooks failed: GameAssembly.dll missing');
      return false;
    }
    var base = mod.base;
    try { var h1 = Interceptor.attach(base.add(0xAF6930), { onEnter: function(args) { if (inHook) return; inHook = true; var instance = args[0]; if (!isValidInstance(instance)) { inHook = false; return; } if (!modeBaseInstance || !instance.equals(modeBaseInstance)) { modeBaseInstance = instance; try { currentRound = instance.add(0x14).readS32(); } catch(e) {} roundActive = true; addDevLog('info', '新回合 #' + currentRound, 'RoundSkip captured ModeBase instance'); } inHook = false; }, onLeave: function(retval) { inHook = false; } }); hooks.push(h1); } catch(e) {}
    try { var h2 = Interceptor.attach(base.add(0xAFAA40), { onEnter: function() { addDevLog('info', 'GameRoundEnd', 'RoundSkip cleared ModeBase instance on round end'); modeBaseInstance = null; roundActive = false; } }); hooks.push(h2); } catch(e) {}
    try { var h3 = Interceptor.attach(base.add(0xAF1920), { onEnter: function() { addDevLog('info', 'OnTimeOut', 'RoundSkip detected timeout'); roundActive = false; } }); hooks.push(h3); } catch(e) {}
    return true;
  }

  return {
    enable: function() { if (hooks.length > 0) return; installHooks(); },
    disable: function() { for (var i = 0; i < hooks.length; i++) { try { hooks[i].detach(); } catch(e) {} } hooks = []; modeBaseInstance = null; roundActive = false; addDevLog('info', '已卸载', 'RoundSkip hooks detached'); },
    skipround: function() { var result = skipRound(); return { ok: result.ok, reason: result.reason }; },
    getstatus: function() {
      var timeStr = null;
      if (isValidInstance(modeBaseInstance)) { try { var m = modeBaseInstance.add(0x34).readS32(); var s = modeBaseInstance.add(0x38).readS32(); if (m >= 0 && m <= 200 && s >= 0 && s <= 59) timeStr = m + ":" + pad2(s); } catch(e) {} }
      return { ok: true, roundActive: roundActive, currentRound: currentRound, skipCount: skipCount, skipErrorCount: skipErrorCount, hasInstance: !!modeBaseInstance, restGameTime: timeStr };
    },
    reset: function() { modeBaseInstance = null; roundActive = false; currentRound = 0; skipCount = 0; skipErrorCount = 0; skipGuard = false; inHook = false; return { ok: true }; }
  };
})();
