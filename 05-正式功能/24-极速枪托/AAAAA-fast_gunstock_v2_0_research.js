// ============================================================
// AAAAA-fast_gunstock_v2_0_research.js
// 24-极速枪托 v2.0 研究/重构版
//
// 重要变化：
//   1. 不再修改 characterAnimator / handAnimator speed。
//      旧方案会破坏手部模型动作同步，且实测不能加快枪托攻击速度。
//   2. 先做链路探针，再做“伤害后解锁/提前伤害实验”。
//   3. 只处理本地玩家 WPN_Gun 右键枪托/刺刀近战。
//   4. 默认模式 unlock_after_damage：等原游戏 KnifeAttackEvent 发生后，提前清理枪托锁，缩短下一次右键等待。
//   5. early_damage_unlock 是实验模式，可能导致重复伤害/动画重叠，只用于离线验证。
//
// 已知 RVA/字段来自当前项目 dump.cs/IDA 索引：
//   WPN_Gun.OnSpecialBtnDown        0xB629F0
//   WPN_Gun.GetKnifeAttackData      0xB61F90
//   WPN_Gun.KnifeAttackEvent        0xB62730
//   WPN_Gun.OnAnimationExit         0xB62800
//   WPN_Gun.OnKnifeAttackExit       0xB62990
//   Weapon.get_isMyWeapon           0xB6E1D0
//   WPN_Gun.realData                0xEC
//   WeaponData_Gun.knifeAttacks     0x180
//   WPN_Gun.knifeAttackCount        0x118
//   WPN_Gun.knifeAttackAnim         0x11C
// ============================================================

(function () {
  'use strict';

  var CALL_CONV = 'mscdecl';

  var RVA = {
    WpnGunGetKnifeAttackData: 0xB61F90,
    WpnGunKnifeAttackEvent: 0xB62730,
    WpnGunOnAnimationExit: 0xB62800,
    WpnGunOnKnifeAttackExit: 0xB62990,
    WpnGunOnSpecialBtnDown: 0xB629F0,
    WeaponGetIsMyWeapon: 0xB6E1D0
  };

  var OFF = {
    WpnGun_realData: 0xEC,
    WeaponDataGun_knifeAttacks: 0x180,
    WpnGun_knifeAttackCount: 0x118,
    WpnGun_knifeAttackAnim: 0x11C
  };

  var MODE = {
    TRACE_ONLY: 'trace_only',
    UNLOCK_AFTER_DAMAGE: 'unlock_after_damage',
    EARLY_DAMAGE_UNLOCK: 'early_damage_unlock'
  };

  var UNLOCK_METHOD = {
    CALL_EXIT: 'call_exit',
    WRITE_LOCK_ZERO: 'write_lock_zero',
    CALL_EXIT_THEN_WRITE: 'call_exit_then_write'
  };

  var config = {
    mode: MODE.UNLOCK_AFTER_DAMAGE,
    unlockMethod: UNLOCK_METHOD.CALL_EXIT,
    unlockDelayMs: 25,
    earlyDamageDelayMs: 90,
    earlyUnlockDelayMs: 15,
    earlyAttackIndex: 0,
    cleanupAfterMs: 2500,
    maxLogsPerModule: 300,
    verboseTrace: true
  };

  var state = {
    enabled: false,
    initialized: false,
    hooksInstalled: false,
    sequence: 0,
    specialHits: 0,
    skippedNoGunstock: 0,
    skippedNotLocal: 0,
    skippedLocked: 0,
    attackDataHits: 0,
    naturalDamageHits: 0,
    earlyDamageCalls: 0,
    originalExitHits: 0,
    animationExitHits: 0,
    unlockCalls: 0,
    unlockWriteCalls: 0,
    unlockFailures: 0,
    staleCleanups: 0,
    lastError: null,
    lastEvent: null
  };

  var hooks = {
    onSpecial: null,
    getAttackData: null,
    knifeEvent: null,
    onAnimationExit: null,
    onKnifeAttackExit: null
  };

  var fn = {
    isMyWeapon: null,
    knifeAttackEvent: null,
    onKnifeAttackExit: null
  };

  var moduleLogCounts = {};
  var active = {};
  var _gameAssembly = null;
  var _cleanupTimer = null;

  function nowMs() {
    return Date.now();
  }

  function log(level, module, message) {
    if (!moduleLogCounts[module]) moduleLogCounts[module] = 0;
    if (moduleLogCounts[module] >= config.maxLogsPerModule) return;
    moduleLogCounts[module]++;

    var line = '[极速枪托v2][' + module + '] ' + message;
    state.lastEvent = module + ': ' + message;
    console.log('[' + level + '] ' + line);
    try {
      send({ type: 'log', level: level, module: '极速枪托v2/' + module, message: message });
    } catch (e) {}
  }

  function safeToString(p) {
    try { return p ? p.toString() : '0x0'; } catch (e) { return '0x?'; }
  }

  function readPtr(addr) {
    try {
      if (!addr || addr.isNull()) return null;
      var p = addr.readPointer();
      if (!p || p.isNull()) return null;
      return p;
    } catch (e) {
      return null;
    }
  }

  function readS32(addr, fallbackValue) {
    try {
      if (!addr || addr.isNull()) return fallbackValue;
      return addr.readS32();
    } catch (e) {
      return fallbackValue;
    }
  }

  function writeS32(addr, value) {
    try {
      if (!addr || addr.isNull()) return false;
      addr.writeS32(value);
      return true;
    } catch (e) {
      state.lastError = 'writeS32 failed: ' + e.message;
      return false;
    }
  }

  function readIl2CppString(str) {
    try {
      if (!str || str.isNull()) return '';
      var length = str.add(0x08).readS32();
      if (length <= 0 || length > 256) return '';
      return str.add(0x0C).readUtf16String(length);
    } catch (e) {
      return '';
    }
  }

  function getGameAssembly() {
    if (_gameAssembly) return _gameAssembly;
    try {
      var mod = Process.findModuleByName('GameAssembly.dll');
      if (!mod) {
        state.lastError = '未找到 GameAssembly.dll';
        log('error', 'INIT', state.lastError);
        return null;
      }
      _gameAssembly = mod;
      log('success', 'INIT', 'GameAssembly base=' + mod.base);
      return mod;
    } catch (e) {
      state.lastError = '获取 GameAssembly.dll 失败: ' + e.message;
      log('error', 'INIT', state.lastError);
      return null;
    }
  }

  function initNativeFunctions() {
    if (state.initialized) return true;
    var mod = getGameAssembly();
    if (!mod) return false;

    try {
      fn.isMyWeapon = new NativeFunction(
        mod.base.add(RVA.WeaponGetIsMyWeapon),
        'bool',
        ['pointer', 'pointer'],
        CALL_CONV
      );
      fn.knifeAttackEvent = new NativeFunction(
        mod.base.add(RVA.WpnGunKnifeAttackEvent),
        'void',
        ['pointer', 'int', 'pointer'],
        CALL_CONV
      );
      fn.onKnifeAttackExit = new NativeFunction(
        mod.base.add(RVA.WpnGunOnKnifeAttackExit),
        'void',
        ['pointer', 'pointer'],
        CALL_CONV
      );

      state.initialized = true;
      log('success', 'INIT', 'NativeFunction 初始化成功；本版不使用 Animator.set_speed');
      return true;
    } catch (e) {
      state.lastError = 'NativeFunction 初始化失败: ' + e.message;
      log('error', 'INIT', state.lastError);
      return false;
    }
  }

  function isLocalWeapon(weapon) {
    if (!weapon || weapon.isNull()) return false;
    if (!initNativeFunctions()) return false;
    try {
      return fn.isMyWeapon(weapon, ptr(0)) ? true : false;
    } catch (e) {
      state.lastError = '判断本地武器失败: ' + e.message;
      return false;
    }
  }

  function hasGunstockAttacks(weapon) {
    if (!weapon || weapon.isNull()) return false;

    var count = readS32(weapon.add(OFF.WpnGun_knifeAttackCount), 0);
    if (count > 0) return true;

    var realData = readPtr(weapon.add(OFF.WpnGun_realData));
    if (!realData) return false;

    var attacks = readPtr(realData.add(OFF.WeaponDataGun_knifeAttacks));
    if (!attacks) return false;

    var length = readS32(attacks.add(0x0C), 0);
    return length > 0;
  }

  function lockValue(weapon) {
    return readS32(weapon.add(OFF.WpnGun_knifeAttackAnim), -9999);
  }

  function keyOf(weapon) {
    return safeToString(weapon);
  }

  function getActiveSession(weapon) {
    return active[keyOf(weapon)] || null;
  }

  function createSession(weapon, lockBefore) {
    var seq = ++state.sequence;
    var item = {
      seq: seq,
      weapon: weapon,
      key: keyOf(weapon),
      t0: nowMs(),
      lockBefore: lockBefore,
      lastAttackIndex: config.earlyAttackIndex | 0,
      naturalDamage: false,
      earlyDamage: false,
      originalExit: false,
      animExit: false,
      unlocked: false
    };
    active[item.key] = item;
    return item;
  }

  function cleanupSession(key, reason) {
    if (active[key]) {
      delete active[key];
      if (config.verboseTrace) log('info', 'CLEAN', 'session removed key=' + key + ' reason=' + reason);
    }
  }

  function cleanupStaleSessions() {
    try {
      var t = nowMs();
      for (var k in active) {
        if (!active.hasOwnProperty(k)) continue;
        var s = active[k];
        if (t - s.t0 > config.cleanupAfterMs) {
          state.staleCleanups++;
          cleanupSession(k, 'stale_' + (t - s.t0) + 'ms');
        }
      }
    } catch (e) {}
  }

  function startCleanupTimer() {
    if (_cleanupTimer) return;
    _cleanupTimer = setInterval(cleanupStaleSessions, 1000);
  }

  function stopCleanupTimer() {
    if (!_cleanupTimer) return;
    try { clearInterval(_cleanupTimer); } catch (e) {}
    _cleanupTimer = null;
  }

  function doWriteLockZero(weapon, reason) {
    var before = lockValue(weapon);
    var ok = writeS32(weapon.add(OFF.WpnGun_knifeAttackAnim), 0);
    var after = lockValue(weapon);
    if (ok) {
      state.unlockWriteCalls++;
      log('success', 'UNLOCK', 'write knifeAttackAnim=0 reason=' + reason + ' lock ' + before + ' -> ' + after);
    } else {
      state.unlockFailures++;
      log('warn', 'UNLOCK', 'write knifeAttackAnim failed reason=' + reason + ' before=' + before);
    }
    return ok;
  }

  function doCallOnKnifeAttackExit(weapon, reason) {
    if (!initNativeFunctions()) return false;
    try {
      var before = lockValue(weapon);
      fn.onKnifeAttackExit(weapon, ptr(0));
      var after = lockValue(weapon);
      state.unlockCalls++;
      log('success', 'UNLOCK', 'call OnKnifeAttackExit reason=' + reason + ' lock ' + before + ' -> ' + after);
      return true;
    } catch (e) {
      state.unlockFailures++;
      state.lastError = 'call OnKnifeAttackExit failed: ' + e.message;
      log('warn', 'UNLOCK', state.lastError + ' reason=' + reason);
      return false;
    }
  }

  function performUnlock(weapon, reason) {
    if (!weapon || weapon.isNull()) return false;

    if (config.unlockMethod === UNLOCK_METHOD.WRITE_LOCK_ZERO) {
      return doWriteLockZero(weapon, reason);
    }
    if (config.unlockMethod === UNLOCK_METHOD.CALL_EXIT_THEN_WRITE) {
      var okExit = doCallOnKnifeAttackExit(weapon, reason + '/call_exit');
      var okWrite = doWriteLockZero(weapon, reason + '/write_zero');
      return okExit || okWrite;
    }
    return doCallOnKnifeAttackExit(weapon, reason);
  }

  function scheduleUnlock(session, delayMs, reason) {
    if (!session) return;
    var seq = session.seq;
    var key = session.key;
    var delay = Math.max(0, delayMs | 0);

    setTimeout(function () {
      var s = active[key];
      if (!s || s.seq !== seq) return;
      if (s.unlocked) return;

      s.unlocked = true;
      performUnlock(s.weapon, reason + '/seq=' + seq + '/delay=' + delay);
    }, delay);
  }

  function callEarlyDamage(session) {
    if (!session || !initNativeFunctions()) return false;
    if (session.naturalDamage) {
      if (config.verboseTrace) log('info', 'EARLY', 'skip early damage because natural damage already happened seq=' + session.seq);
      return false;
    }
    if (session.earlyDamage) return false;

    try {
      var idx = session.lastAttackIndex | 0;
      session.earlyDamage = true;
      state.earlyDamageCalls++;
      log('warn', 'EARLY', 'call KnifeAttackEvent early seq=' + session.seq + ' attackIndex=' + idx + ' elapsed=' + (nowMs() - session.t0) + 'ms');
      fn.knifeAttackEvent(session.weapon, idx, ptr(0));
      return true;
    } catch (e) {
      state.lastError = 'early KnifeAttackEvent failed: ' + e.message;
      log('error', 'EARLY', state.lastError);
      return false;
    }
  }

  function scheduleEarlyDamage(session) {
    if (!session) return;
    var seq = session.seq;
    var key = session.key;
    var delay = Math.max(0, config.earlyDamageDelayMs | 0);

    setTimeout(function () {
      var s = active[key];
      if (!s || s.seq !== seq) return;
      callEarlyDamage(s);
      scheduleUnlock(s, config.earlyUnlockDelayMs, 'after_early_damage');
    }, delay);
  }

  function installHooks() {
    if (state.hooksInstalled) return true;
    var mod = getGameAssembly();
    if (!mod) return false;
    if (!initNativeFunctions()) return false;

    try {
      hooks.onSpecial = Interceptor.attach(mod.base.add(RVA.WpnGunOnSpecialBtnDown), {
        onEnter: function (args) {
          if (!state.enabled) return;

          this.weapon = args[0];
          this.session = null;

          if (!isLocalWeapon(this.weapon)) {
            state.skippedNotLocal++;
            return;
          }

          if (!hasGunstockAttacks(this.weapon)) {
            state.skippedNoGunstock++;
            return;
          }

          var before = lockValue(this.weapon);
          if (before !== 0) {
            state.skippedLocked++;
            if (config.verboseTrace && (state.skippedLocked <= 20 || state.skippedLocked % 50 === 0)) {
              log('info', 'SPECIAL', 'right click skipped by original lock weapon=' + safeToString(this.weapon) + ' lock=' + before);
            }
            return;
          }

          state.specialHits++;
          this.session = createSession(this.weapon, before);

          if (state.specialHits <= 30 || state.specialHits % 50 === 0) {
            log('success', 'SPECIAL', 'OnSpecialBtnDown seq=' + this.session.seq + ' weapon=' + safeToString(this.weapon) + ' mode=' + config.mode + ' lock=' + before);
          }
        },
        onLeave: function () {
          if (!state.enabled || !this.session) return;
          if (config.mode === MODE.EARLY_DAMAGE_UNLOCK) {
            scheduleEarlyDamage(this.session);
          }
        }
      });

      hooks.getAttackData = Interceptor.attach(mod.base.add(RVA.WpnGunGetKnifeAttackData), {
        onEnter: function (args) {
          if (!state.enabled) return;

          // 修正旧版 bug：实例方法参数应为 args[0]=this/weapon, args[1]=attackIndex, args[2]=MethodInfo*。
          this.weapon = args[0];
          this.attackIndex = args[1].toInt32();
          this.session = getActiveSession(this.weapon);

          if (this.session) {
            this.session.lastAttackIndex = this.attackIndex;
            state.attackDataHits++;
            if (state.attackDataHits <= 30 || state.attackDataHits % 50 === 0) {
              log('info', 'DATA', 'GetKnifeAttackData seq=' + this.session.seq + ' attackIndex=' + this.attackIndex + ' elapsed=' + (nowMs() - this.session.t0) + 'ms');
            }
          }
        }
      });

      hooks.knifeEvent = Interceptor.attach(mod.base.add(RVA.WpnGunKnifeAttackEvent), {
        onEnter: function (args) {
          if (!state.enabled) return;

          this.weapon = args[0];
          this.attackIndex = args[1].toInt32();
          this.session = getActiveSession(this.weapon);

          if (this.session) {
            this.session.naturalDamage = true;
            this.session.lastAttackIndex = this.attackIndex;
            state.naturalDamageHits++;
            log('success', 'DAMAGE', 'natural KnifeAttackEvent seq=' + this.session.seq + ' attackIndex=' + this.attackIndex + ' elapsed=' + (nowMs() - this.session.t0) + 'ms');
          }
        },
        onLeave: function () {
          if (!state.enabled || !this.session) return;

          if (config.mode === MODE.UNLOCK_AFTER_DAMAGE || config.mode === MODE.EARLY_DAMAGE_UNLOCK) {
            scheduleUnlock(this.session, config.unlockDelayMs, 'after_natural_damage');
          }
        }
      });

      hooks.onAnimationExit = Interceptor.attach(mod.base.add(RVA.WpnGunOnAnimationExit), {
        onEnter: function (args) {
          if (!state.enabled) return;

          this.weapon = args[0];
          this.animName = readIl2CppString(args[1]);
          this.animTag = readIl2CppString(args[2]);
          this.session = getActiveSession(this.weapon);

          if (this.session && this.animTag === 'knifeAttack') {
            this.session.animExit = true;
            state.animationExitHits++;
            log('info', 'ANIM_EXIT', 'OnAnimationExit seq=' + this.session.seq + ' name=' + this.animName + ' tag=' + this.animTag + ' elapsed=' + (nowMs() - this.session.t0) + 'ms lock=' + lockValue(this.weapon));
          }
        },
        onLeave: function () {
          if (!state.enabled || !this.session) return;
          if (this.animTag === 'knifeAttack') {
            cleanupSession(this.session.key, 'animation_exit');
          }
        }
      });

      hooks.onKnifeAttackExit = Interceptor.attach(mod.base.add(RVA.WpnGunOnKnifeAttackExit), {
        onEnter: function (args) {
          if (!state.enabled) return;

          this.weapon = args[0];
          this.session = getActiveSession(this.weapon);
          if (this.session) {
            this.session.originalExit = true;
            state.originalExitHits++;
            log('info', 'ORIG_EXIT', 'OnKnifeAttackExit seq=' + this.session.seq + ' elapsed=' + (nowMs() - this.session.t0) + 'ms lockBefore=' + lockValue(this.weapon));
          }
        }
      });

      state.hooksInstalled = true;
      startCleanupTimer();
      log('success', 'HOOK', 'v2 hooks installed; Animator speed is NOT touched');
      return true;
    } catch (e) {
      state.lastError = 'Hook 安装失败: ' + e.message;
      log('error', 'HOOK', state.lastError);
      return false;
    }
  }

  function enable() {
    try {
      if (!installHooks()) {
        state.enabled = false;
        return false;
      }
      state.enabled = true;
      log('success', 'STATE', '已开启 mode=' + config.mode + ' unlockMethod=' + config.unlockMethod + ' unlockDelayMs=' + config.unlockDelayMs);
      return true;
    } catch (e) {
      state.enabled = false;
      state.lastError = '开启失败: ' + e.message;
      log('error', 'STATE', state.lastError);
      return false;
    }
  }

  function disable() {
    state.enabled = false;
    active = {};
    log('info', 'STATE', '已关闭；不会修改 Animator，不会保留活动 session');
    return true;
  }

  function cleanup() {
    disable();
    stopCleanupTimer();

    try {
      if (hooks.onSpecial) { hooks.onSpecial.detach(); hooks.onSpecial = null; }
      if (hooks.getAttackData) { hooks.getAttackData.detach(); hooks.getAttackData = null; }
      if (hooks.knifeEvent) { hooks.knifeEvent.detach(); hooks.knifeEvent = null; }
      if (hooks.onAnimationExit) { hooks.onAnimationExit.detach(); hooks.onAnimationExit = null; }
      if (hooks.onKnifeAttackExit) { hooks.onKnifeAttackExit.detach(); hooks.onKnifeAttackExit = null; }
      state.hooksInstalled = false;
      log('success', 'STATE', 'Hook 已清理');
      return true;
    } catch (e) {
      state.lastError = '清理失败: ' + e.message;
      log('error', 'STATE', state.lastError);
      return false;
    }
  }

  function setConfig(next) {
    try {
      if (!next || typeof next !== 'object') return false;

      if (next.mode === MODE.TRACE_ONLY || next.mode === MODE.UNLOCK_AFTER_DAMAGE || next.mode === MODE.EARLY_DAMAGE_UNLOCK) {
        config.mode = next.mode;
      }
      if (next.unlockMethod === UNLOCK_METHOD.CALL_EXIT || next.unlockMethod === UNLOCK_METHOD.WRITE_LOCK_ZERO || next.unlockMethod === UNLOCK_METHOD.CALL_EXIT_THEN_WRITE) {
        config.unlockMethod = next.unlockMethod;
      }
      if (typeof next.unlockDelayMs === 'number') config.unlockDelayMs = Math.max(0, Math.min(1000, next.unlockDelayMs | 0));
      if (typeof next.earlyDamageDelayMs === 'number') config.earlyDamageDelayMs = Math.max(0, Math.min(2000, next.earlyDamageDelayMs | 0));
      if (typeof next.earlyUnlockDelayMs === 'number') config.earlyUnlockDelayMs = Math.max(0, Math.min(1000, next.earlyUnlockDelayMs | 0));
      if (typeof next.earlyAttackIndex === 'number') config.earlyAttackIndex = Math.max(0, Math.min(10, next.earlyAttackIndex | 0));
      if (typeof next.verboseTrace === 'boolean') config.verboseTrace = next.verboseTrace;

      log('success', 'CONFIG', JSON.stringify(config));
      return true;
    } catch (e) {
      state.lastError = 'setConfig failed: ' + e.message;
      log('error', 'CONFIG', state.lastError);
      return false;
    }
  }

  function forceUnlock() {
    var count = 0;
    try {
      for (var k in active) {
        if (!active.hasOwnProperty(k)) continue;
        performUnlock(active[k].weapon, 'manual_force_unlock');
        active[k].unlocked = true;
        count++;
      }
      log('warn', 'UNLOCK', 'manual force unlock count=' + count);
      return count;
    } catch (e) {
      state.lastError = 'forceUnlock failed: ' + e.message;
      log('error', 'UNLOCK', state.lastError);
      return -1;
    }
  }

  function status() {
    return {
      enabled: state.enabled,
      initialized: state.initialized,
      hooksInstalled: state.hooksInstalled,
      mode: config.mode,
      unlockMethod: config.unlockMethod,
      unlockDelayMs: config.unlockDelayMs,
      earlyDamageDelayMs: config.earlyDamageDelayMs,
      earlyUnlockDelayMs: config.earlyUnlockDelayMs,
      earlyAttackIndex: config.earlyAttackIndex,
      specialHits: state.specialHits,
      attackDataHits: state.attackDataHits,
      naturalDamageHits: state.naturalDamageHits,
      earlyDamageCalls: state.earlyDamageCalls,
      originalExitHits: state.originalExitHits,
      animationExitHits: state.animationExitHits,
      unlockCalls: state.unlockCalls,
      unlockWriteCalls: state.unlockWriteCalls,
      unlockFailures: state.unlockFailures,
      skippedNoGunstock: state.skippedNoGunstock,
      skippedNotLocal: state.skippedNotLocal,
      skippedLocked: state.skippedLocked,
      activeSessions: Object.keys(active).length,
      staleCleanups: state.staleCleanups,
      lastError: state.lastError,
      lastEvent: state.lastEvent
    };
  }

  rpc.exports = {
    enable: enable,
    disable: disable,
    cleanup: cleanup,
    status: status,
    setconfig: setConfig,
    forceunlock: forceUnlock
  };

  log('success', 'INIT', '极速枪托 v2.0 研究脚本已加载');
  log('info', 'INIT', '本版不改 Animator.speed；建议先 trace_only，再 unlock_after_damage，最后才测 early_damage_unlock');
})();
