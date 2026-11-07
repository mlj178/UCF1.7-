// ============================================================
// AAAAA-bot_pause_min.js - Bot pause minimum implementation
// v1.2-no-il2cpp-api
//
// Goal:
//   Toggle Bot.stopAllBot by fixed RVA + static field pointer chain.
//
// User rule:
//   Do NOT call IL2CPP API / reflection API.
//   No class init API.
//   No runtime metadata API.
//
// Verified data:
//   Bot_TypeInfo:    GameAssembly.dll + 0xE25F44
//   static_fields:   Bot_TypeInfo + 0x5C
//   Bot.stopAllBot:  static_fields + 0xC
//
// Safety fixes:
//   1. Resolve pointers on every operation; never keep stale pointers.
//   2. Validate pointer size and every pointer read.
//   3. Read before write; skip duplicate writes.
//   4. Write then read back to verify.
//   5. If the room is not ready yet, keep user intent and retry until Bot.stopAllBot is writable.
// ============================================================

(function () {
  'use strict';

  var RVA = {
    Bot_TypeInfo: 0xE25F44,
    Bot_Update: 0xB33370,
    GameManager_Awake: 0xAFA250,
    GameManager_OnDestroy: 0xAFB6F0,
    ModeBase_Update: 0xAF6A00,
    ModeBase_ExitGame: 0xAEE850
  };

  var OFF = {
    Il2CppClass_static_fields: 0x5C,
    Bot_stopAllBot: 0xC
  };

  var state = {
    enabled: false,
    pendingApply: false,
    applied: false,
    retryTimer: null,
    retryCount: 0,
    hooksInstalled: false,
    hooks: [],
    roomGeneration: 0,
    lastRoomReadyApplyAt: 0,
    lastApplyReason: '',
    lastError: null,
    writeCount: 0,
    pointerSize: Process.pointerSize,
    lastResolved: null
  };

  function safeString(x) {
    try {
      if (x === null || x === undefined) return String(x);
      return x.toString();
    } catch (_) {
      return '<unprintable>';
    }
  }

  function setError(msg, e) {
    state.lastError = msg + (e && e.message ? ': ' + e.message : '');
    return state.lastError;
  }

  function sendLog(level, message) {
    try {
      var text = '[bot_pause][' + level + '] ' + message;
      console.log(text);
      send({ type: 'log', level: level, module: 'bot_pause', message: message });
    } catch (_) {
    }
  }

  function sendStatus(feature, enabled) {
    try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (_) {}
  }

  function clearRoomReadyRetry() {
    if (state.retryTimer !== null) {
      try { clearInterval(state.retryTimer); } catch (_) {}
      state.retryTimer = null;
    }
  }

  function detachRoomReadyHooks() {
    for (var i = 0; i < state.hooks.length; i++) {
      try { state.hooks[i].detach(); } catch (_) {}
    }
    state.hooks = [];
    state.hooksInstalled = false;
  }

  function isExecutable(addr) {
    try {
      var range = Process.findRangeByAddress(addr);
      return range !== null && range.protection.indexOf('x') !== -1;
    } catch (_) {
      return false;
    }
  }

  // ===== 卡死看门狗（2026-10 临时诊断，务必常开）=====
  // 为什么需要它：游戏"停止响应"时进程里什么都不写了，日志上只留下"某一行之后突然没有下文"，
  // 完全看不出卡在哪；Windows 的 AppHang 事件不带调用栈，WER/CrashDumps 里也没有 dump（已确认）。
  //
  // 做法（只用 Interceptor + JS 线程，实测可靠）：
  //   1) ModeBase.Update 当每帧心跳 —— 主线程活着就一定会跑；
  //   2) 在一批"可疑函数"上留面包屑（环形缓冲，最近 64 次：时间/函数/线程号）；
  //   3) Frida JS 线程每秒巡检：超过 HANG_IDLE_MS 没有心跳 => 判定卡死，把面包屑倒进日志。
  //      （JS 线程是独立的，主线程卡死它照样跑；这一点已用 probe_hang_watchdog.py 实测。）
  // 为什么不用 Process.enumerateThreads().context 抓栈：实测在 32 位目标上拿到的是**别的线程
  //   （或当前线程）的栈**，会把死循环线程漏掉 —— 宁可不给，也不给错的数据。
  var HANG_IDLE_MS = 6000;

  var watch = {
    lastPulseAt: 0, pulses: 0, dumped: false, busy: false, timer: null,
    hook: null, hooks: [], buf: [], seq: 0, lastAt: {}, inRoom: false
  };

  // 同一观测点的留痕限频（毫秒）。
  // 上一轮实测踩过坑：WPN_Knife.Update 每帧都会被所有玩家的武器调用，限频 10ms 时它一个点
  // 就把 64 条缓冲占满（窗口只剩 ~1s），别的信号全被挤掉。50ms（20 次/秒）足够看清"卡死前最后
  // 一串动作"，缓冲窗口也放宽到 ~3s。
  var WATCH_MIN_INTERVAL_MS = 50;

  // 面包屑盯的函数（RVA = 地址 - GameAssembly 基址）：
  //   il2cpp_resolve_icall 0x107960 ← 取自 时间加速 的实测日志 0x6c078960 - 0x6bf70000
  //   PlayerWeapons.Remove/RemoveAll、GameManager.GiveWeapon ← 变身换武器（手雷模式也 replace 了它们）
  //   Player.set_nanoRole ← 变身；CFAnimator.SetFloat / WPN_Knife.* ← 近战连招
  var WATCH_TARGETS = [
    ['il2cpp_resolve_icall', 0x107960],
    ['PlayerWeapons.RemoveAll', 0xB15EB0],
    ['PlayerWeapons.Remove', 0xB15FD0],
    ['GameManager.GiveWeapon', 0xAFB390],
    ['Player.set_nanoRole', 0xB56880],
    ['CFAnimator.SetFloat', 0xB34E40],
    ['WPN_Knife.OnKnifeAttackAnimEnd', 0xB64150],
    ['WPN_Knife.PlayKnifeAttackAnim', 0xB642B0],
    ['WPN_Knife.Update', 0xB64610],
    ['Weapon.OnFireBtnPressed', 0xB6CDA0]
  ];

  function watchPulse() {
    watch.lastPulseAt = Date.now();
    watch.pulses++;
  }

  function sendWatchLog(message) {
    try {
      send({ type: 'log_file', level: 'warn', module: '卡死看门狗', message: message, audience: 'dev' });
    } catch (_) {}
  }

  function noteBreadcrumb(name) {
    try {
      var now = Date.now();
      if (now - (watch.lastAt[name] || 0) < WATCH_MIN_INTERVAL_MS) return;   // 限频
      watch.lastAt[name] = now;
      watch.buf.push({ t: now, n: name, tid: Process.getCurrentThreadId(), s: ++watch.seq });
      if (watch.buf.length > 64) watch.buf.shift();
    } catch (_) {}
  }

  function flushBreadcrumbs(idleMs) {
    try {
      if (!watch.buf.length) {
        sendWatchLog('卡死前没有任何面包屑（可疑函数一个都没被调用过）');
        return;
      }
      var first = watch.buf[0].t;
      var last = watch.buf[watch.buf.length - 1];
      var lines = [];
      for (var i = 0; i < watch.buf.length; i++) {
        var e = watch.buf[i];
        lines.push('#' + e.s + ' +' + (e.t - first) + 'ms ' + e.n + ' tid' + e.tid);
      }
      for (var j = 0; j < lines.length; j += 4) {
        sendWatchLog('面包屑[' + (Math.floor(j / 4) + 1) + ']: ' + lines.slice(j, j + 4).join(' | '));
      }
      sendWatchLog('最后一次面包屑 = ' + last.n + '，距今 ' + (Date.now() - last.t) + 'ms；主线程已静默 ' + idleMs + 'ms');
    } catch (e) {
      sendWatchLog('倒面包屑失败: ' + (e && e.message ? e.message : e));
    }
  }

  function startHangWatchdog() {
    if (watch.timer) return;
    watch.timer = setInterval(function () {
      try {
        // 脚本加载时 GameAssembly 可能还没就绪：前几次巡检顺手补装（最多 5 次）
        if ((!watch.hooks.length || !watch.hook) && (watch.hookAttempts || 0) < 5) {
          watch.hookAttempts = (watch.hookAttempts || 0) + 1;
          installWatchdogPulseHook();
          installBreadcrumbHooks();
        }
        if (watch.busy || watch.dumped || !watch.lastPulseAt) return;
        // ⚠ 只在"房间里"判定卡死：ModeBase.Update 只在**对局内**跑，回到大厅/结算时它天然不跑。
        //   上一轮实测就吃过这个假警报：13:57:02 报了"静默 6981ms"，其实是 13:56:56 房间已销毁。
        if (!watch.inRoom) return;
        var idle = Date.now() - watch.lastPulseAt;
        if (idle < HANG_IDLE_MS) return;
        watch.busy = true;
        watch.dumped = true;
        sendWatchLog('!!! 主线程已经 ' + idle + 'ms 没跑过 ModeBase.Update（累计心跳 ' + watch.pulses
          + ' 次）—— 判定卡死/死锁，倒出卡死前的面包屑');
        flushBreadcrumbs(idle);
        watch.busy = false;
      } catch (_) {}
    }, 1000);
  }

  // 面包屑钩子：与功能开关解耦，脚本加载即安装（关掉 bot_pause 也照样留痕）
  function installBreadcrumbHooks() {
    try {
      var mod = getGameAssembly();
      if (!mod) return 0;
      var count = 0;
      for (var i = 0; i < WATCH_TARGETS.length; i++) {
        var name = WATCH_TARGETS[i][0];
        var addr = mod.base.add(WATCH_TARGETS[i][1]);
        try {
          var range = Process.findRangeByAddress(addr);
          if (!range || range.protection.indexOf('x') === -1) {
            sendWatchLog('面包屑跳过（地址不可执行）: ' + name);
            continue;
          }
          // 用工厂函数包一层，避免闭包捕获循环变量导致所有面包屑都变成最后一个名字
          (function (label, target) {
            watch.hooks.push(Interceptor.attach(target, {
              onEnter: function () { noteBreadcrumb(label); }
            }));
          })(name, addr);
          count += 1;
        } catch (e) {
          sendWatchLog('面包屑安装失败 ' + name + ': ' + (e && e.message ? e.message : e));
        }
      }
      sendWatchLog('面包屑已安装 ' + count + '/' + WATCH_TARGETS.length + ' 个观测点');
      return count;
    } catch (e) {
      sendWatchLog('面包屑安装整体失败: ' + (e && e.message ? e.message : e));
      return 0;
    }
  }

  // 看门狗自己的心跳钩子：**与功能开关解耦**（bot_pause 关掉、hooks 被 detach 之后也要能抓到卡死）
  function installWatchdogPulseHook() {
    if (watch.hook) return true;
    try {
      var mod = getGameAssembly();
      if (!mod) {
        sendWatchLog('看门狗心跳钩子暂时装不上（GameAssembly 未就绪），巡检时会重试');
        return false;
      }
      watch.hook = Interceptor.attach(mod.base.add(RVA.ModeBase_Update), {
        onEnter: function () { watchPulse(); }
      });
      sendWatchLog('看门狗已就绪：心跳=ModeBase.Update，超时阈值=' + HANG_IDLE_MS + 'ms');
      return true;
    } catch (e) {
      sendWatchLog('看门狗心跳钩子安装失败: ' + (e && e.message ? e.message : e));
      return false;
    }
  }

  function attachRoomHook(mod, name, rva, callbacks) {
    var addr = mod.base.add(rva);
    if (!isExecutable(addr)) {
      sendLog('warn', name + ' hook skipped; address is not executable: ' + safeString(addr));
      return false;
    }
    try {
      state.hooks.push(Interceptor.attach(addr, callbacks));
      sendLog('info', 'room-ready hook installed: ' + name);
      return true;
    } catch (e) {
      sendLog('warn', name + ' hook install failed: ' + (e && e.message ? e.message : safeString(e)));
      return false;
    }
  }

  function triggerRoomReadyApply(reason, force) {
    // 对局内：ModeBase.Update 只在房间/对局内跑，所以只要它还在被调用，就说明在看门狗的有效区间内
    if (!watch.inRoom) {
      watch.inRoom = true;
      watch.dumped = false;        // 新的一局允许再报一次卡死
    }
    if (!state.enabled) return;
    var now = Date.now();
    // P1：失败态（pendingApply=true）原来会绕过限频，导致 ModeBase.Update / Bot.Update 每帧都跑完整解析链；统一最小间隔
    var minInterval = (state.applied && !state.pendingApply) ? 1000 : 500;
    if (!force && now - state.lastRoomReadyApplyAt < minInterval) return;
    state.lastRoomReadyApplyAt = now;
    var result = applyEnabledState(reason || 'room_ready_hook');
    if (result.ok) {
      if (reason !== 'ModeBase.Update' || state.retryCount === 0 || state.retryCount % 30 === 0) {
        sendLog('info', 'room-ready apply ok: ' + (reason || 'hook'));
      }
    } else {
      startRoomReadyRetry(reason || 'room_ready_hook');
    }
  }

  function clearRoomState(reason) {
    state.roomGeneration += 1;
    state.applied = false;
    state.pendingApply = !!state.enabled;
    state.lastApplyReason = reason || 'room_destroyed';
    state.lastRoomReadyApplyAt = 0;
    watch.inRoom = false;          // 离开对局后不要再判定"主线程卡死"（ModeBase.Update 本来就不跑）
    watch.lastPulseAt = 0;
    watch.dumped = false;
    if (state.enabled) startRoomReadyRetry(reason || 'room_destroyed');
  }

  function installRoomReadyHooks() {
    if (state.hooksInstalled) return true;

    var mod = getGameAssembly();
    if (!mod) return false;

    var installed = 0;
    if (attachRoomHook(mod, 'GameManager.Awake', RVA.GameManager_Awake, {
      onLeave: function () { triggerRoomReadyApply('GameManager.Awake', true); }
    })) installed += 1;

    if (attachRoomHook(mod, 'ModeBase.Update', RVA.ModeBase_Update, {
      onEnter: function () { triggerRoomReadyApply('ModeBase.Update', false); }
    })) installed += 1;

    if (attachRoomHook(mod, 'Bot.Update', RVA.Bot_Update, {
      onEnter: function () { triggerRoomReadyApply('Bot.Update', false); }
    })) installed += 1;

    if (attachRoomHook(mod, 'ModeBase.ExitGame', RVA.ModeBase_ExitGame, {
      onEnter: function () { clearRoomState('ModeBase.ExitGame'); }
    })) installed += 1;

    if (attachRoomHook(mod, 'GameManager.OnDestroy', RVA.GameManager_OnDestroy, {
      onEnter: function () { clearRoomState('GameManager.OnDestroy'); }
    })) installed += 1;

    state.hooksInstalled = installed > 0;
    if (!state.hooksInstalled) {
      state.lastError = 'no room-ready hooks installed';
      return false;
    }
    return true;
  }

  function applyEnabledState(reason) {
    if (!state.enabled) {
      state.pendingApply = false;
      state.applied = false;
      state.lastApplyReason = reason || 'disabled';
      clearRoomReadyRetry();
      return { ok: true, enabled: false, pendingApply: false, applied: false };
    }

    var result = writeStopAllBot(true);
    state.lastApplyReason = reason || 'apply_enabled_state';
    if (result.ok) {
      state.pendingApply = false;
      state.applied = true;
      clearRoomReadyRetry();
      return result;
    }

    state.pendingApply = true;
    state.applied = false;
    return result;
  }

  function startRoomReadyRetry(reason) {
    state.pendingApply = true;
    state.lastApplyReason = reason || 'room_ready_retry';
    if (state.retryTimer !== null) return;

    state.retryTimer = setInterval(function () {
      if (!state.enabled) {
        clearRoomReadyRetry();
        return;
      }
      state.retryCount += 1;
      // P1：重试上限（约 5 分钟），避免无休止重试
      if (state.retryCount > 600) {
        sendLog('warn', 'room-ready retry 次数超限，已停止重试');
        clearRoomReadyRetry();
        return;
      }
      var result = applyEnabledState('room_ready_retry');
      if (result.ok) {
        sendLog('info', 'room-ready retry applied Bot.stopAllBot = true');
      } else if (state.retryCount === 1 || state.retryCount % 10 === 0) {
        sendLog('warn', 'waiting for Bot.stopAllBot to become writable: ' + (result.msg || 'unknown'));
      }
    }, 500);
  }

  function getGameAssembly() {
    try {
      var mod = Process.findModuleByName('GameAssembly.dll');
      if (!mod) {
        state.lastError = 'GameAssembly.dll not found';
        return null;
      }
      return mod;
    } catch (e) {
      setError('find GameAssembly failed', e);
      return null;
    }
  }

  function readPointerAt(addr, label) {
    try {
      if (!addr || addr.isNull()) {
        state.lastError = label + ' address is null';
        return null;
      }
      var value = addr.readPointer();
      if (!value || value.isNull()) {
        state.lastError = label + ' pointer is null';
        return null;
      }
      return value;
    } catch (e) {
      setError('readPointer failed at ' + label + ' ' + safeString(addr), e);
      return null;
    }
  }

  function readU8(addr, label) {
    try {
      if (!addr || addr.isNull()) {
        state.lastError = label + ' address is null';
        return null;
      }
      return addr.readU8();
    } catch (e) {
      setError('readU8 failed at ' + label + ' ' + safeString(addr), e);
      return null;
    }
  }

  function writeU8(addr, value, label) {
    try {
      if (!addr || addr.isNull()) {
        state.lastError = label + ' address is null';
        return false;
      }
      addr.writeU8(value);
      var readBack = addr.readU8();
      if (readBack !== value) {
        state.lastError = label + ' verify failed: wrote=' + value + ', readBack=' + readBack;
        return false;
      }
      state.writeCount += 1;
      return true;
    } catch (e) {
      setError('writeU8 failed at ' + label + ' ' + safeString(addr), e);
      return false;
    }
  }

  function resolveStopAllBot() {
    var mod = getGameAssembly();
    if (!mod) return { ok: false, msg: state.lastError || 'GameAssembly.dll not found' };

    var warnings = [];
    if (Process.pointerSize !== 4) {
      warnings.push('unexpected pointerSize=' + Process.pointerSize + ', offsets were verified for 32-bit GameAssembly');
    }

    var typeInfoPtrAddr = mod.base.add(RVA.Bot_TypeInfo);
    var typeInfo = readPointerAt(typeInfoPtrAddr, 'Bot_TypeInfo');
    if (!typeInfo) return { ok: false, msg: state.lastError || 'Bot_TypeInfo pointer is null' };

    var staticFieldsAddr = typeInfo.add(OFF.Il2CppClass_static_fields);
    var staticFields = readPointerAt(staticFieldsAddr, 'Bot.static_fields');
    if (!staticFields) {
      return {
        ok: false,
        msg: state.lastError || 'Bot static_fields pointer is null',
        base: mod.base.toString(),
        pointerSize: Process.pointerSize,
        typeInfoPtrAddr: typeInfoPtrAddr.toString(),
        typeInfo: typeInfo.toString(),
        staticFieldsAddr: staticFieldsAddr.toString(),
        warning: 'static_fields is null. This version does not call any runtime metadata API by user rule.'
      };
    }

    var fieldAddr = staticFields.add(OFF.Bot_stopAllBot);
    var resolved = {
      ok: true,
      base: mod.base.toString(),
      pointerSize: Process.pointerSize,
      typeInfoPtrAddr: typeInfoPtrAddr.toString(),
      typeInfo: typeInfo.toString(),
      staticFieldsAddr: staticFieldsAddr.toString(),
      staticFields: staticFields.toString(),
      staticFieldsPtr: staticFields,
      fieldAddrPtr: fieldAddr,
      fieldAddr: fieldAddr.toString(),
      warnings: warnings
    };

    state.lastResolved = {
      base: resolved.base,
      typeInfoPtrAddr: resolved.typeInfoPtrAddr,
      typeInfo: resolved.typeInfo,
      staticFieldsAddr: resolved.staticFieldsAddr,
      staticFields: resolved.staticFields,
      fieldAddr: resolved.fieldAddr
    };
    return resolved;
  }

  function readStopAllBot() {
    var resolved = resolveStopAllBot();
    if (!resolved.ok) {
      return {
        ok: false,
        msg: resolved.msg,
        enabled: state.enabled,
        writeCount: state.writeCount,
        lastError: state.lastError,
        pointerSize: Process.pointerSize,
        lastResolved: state.lastResolved,
        warning: resolved.warning
      };
    }

    var currentValue = readU8(resolved.fieldAddrPtr, 'Bot.stopAllBot');
    if (currentValue === null) {
      return {
        ok: false,
        msg: state.lastError || 'failed to read Bot.stopAllBot',
        enabled: state.enabled,
        writeCount: state.writeCount,
        lastError: state.lastError,
        lastResolved: state.lastResolved
      };
    }

    return {
      ok: true,
      currentValue: currentValue,
      paused: currentValue !== 0,
      enabled: state.enabled,
      writeCount: state.writeCount,
      lastError: state.lastError,
      base: resolved.base,
      pointerSize: resolved.pointerSize,
      typeInfoPtrAddr: resolved.typeInfoPtrAddr,
      typeInfo: resolved.typeInfo,
      staticFieldsAddr: resolved.staticFieldsAddr,
      staticFields: resolved.staticFields,
      fieldAddr: resolved.fieldAddr,
      warnings: resolved.warnings
    };
  }

  function writeStopAllBot(paused) {
    var resolved = resolveStopAllBot();
    if (!resolved.ok) return resolved;

    var target = paused ? 1 : 0;
    var current = readU8(resolved.fieldAddrPtr, 'Bot.stopAllBot(before write)');
    if (current === null) {
      return { ok: false, msg: state.lastError || 'failed to read Bot.stopAllBot before write' };
    }

    if (current === target) {
      state.enabled = paused;
      state.applied = paused;
      state.pendingApply = false;
      state.lastError = null;
      return {
        ok: true,
        changed: false,
        msg: paused ? 'bots already paused' : 'bots already resumed',
        currentValue: current,
        paused: paused,
        enabled: state.enabled,
        writeCount: state.writeCount,
        fieldAddr: resolved.fieldAddr,
        warnings: resolved.warnings
      };
    }

    if (!writeU8(resolved.fieldAddrPtr, target, 'Bot.stopAllBot')) {
      return { ok: false, msg: state.lastError || 'failed to write Bot.stopAllBot' };
    }

    state.enabled = paused;
    state.applied = paused;
    state.pendingApply = false;
    state.lastError = null;
    return {
      ok: true,
      changed: true,
      msg: paused ? 'bots paused' : 'bots resumed',
      currentValue: target,
      paused: paused,
      enabled: state.enabled,
      writeCount: state.writeCount,
      fieldAddr: resolved.fieldAddr,
      warnings: resolved.warnings
    };
  }

  function applyConfig(config) {
    return { ok: true, config: config || {} };
  }

  rpc.exports = {
    enable: function () {
      state.enabled = true;
      sendStatus('bot_pause', true);
      installRoomReadyHooks();
      var result = applyEnabledState('enable');
      if (!result.ok) startRoomReadyRetry('enable');
      sendLog(result.ok ? 'success' : 'warn', result.msg || safeString(result));
      return result;
    },

    disable: function () {
      clearRoomReadyRetry();
      detachRoomReadyHooks();
      state.enabled = false;
      sendStatus('bot_pause', false);
      state.pendingApply = false;
      state.applied = false;
      var result = writeStopAllBot(false);
      sendLog(result.ok ? 'info' : 'error', result.msg || safeString(result));
      return result;
    },

    status: function () {
      var result = readStopAllBot();
      result.pendingApply = state.pendingApply;
      result.applied = state.applied;
      result.retryCount = state.retryCount;
      result.hooksInstalled = state.hooksInstalled;
      result.roomGeneration = state.roomGeneration;
      result.lastApplyReason = state.lastApplyReason;
      return result;
    },

    setConfig: function (config) {
      return applyConfig(config);
    },

    setconfig: function (config) {
      return applyConfig(config);
    },

    cleanup: function (payload) {
      clearRoomReadyRetry();
      detachRoomReadyHooks();
      state.pendingApply = false;
      state.applied = false;
      var result = writeStopAllBot(false);
      state.enabled = false;
      if (result.ok) sendLog('info', 'cleanup restored Bot.stopAllBot = false');
      else sendLog('warn', 'cleanup failed: ' + (result.msg || 'unknown'));
      return result;
    },

    dispose: function (payload) {
      // P1：原来依赖 this=exports，直接调用时 this 是 undefined 会 TypeError
      return rpc.exports.cleanup(payload);
    }
  };

  sendLog('info', 'script loaded; no runtime metadata API; pointerSize=' + Process.pointerSize);

  // 脚本一加载就启动看门狗（不依赖功能是否开启），游戏卡死时它会倒出面包屑
  startHangWatchdog();
  installWatchdogPulseHook();
  installBreadcrumbHooks();
})();
