// ============================================================
// AAAAA-fast_gunstock_v3_2_natural_damage.js
// 极速枪托 v3.2：原始伤害事件完成后解锁
//
// 行为：
// - 不主动调用 KnifeAttackEvent，不伪造或补发伤害
// - 本次原始 KnifeAttackEvent 完整返回后才解除枪托锁
// - 最大保护窗口只处理异常中断（切枪、死亡、动画异常）
//
// 安全策略：
// - attach-only，不 replace KnifeAttackEvent
// - 不改 Animator.speed
// - 不合并 v2.9 动画加速
// - 关闭/异常/强制恢复时清状态锁
// ============================================================

(function () {
  'use strict';

  var ABI = 'mscdecl';
  var MAX_LOGS_PER_MODULE = 3;
  var gameModule = null;
  var pluginConfig = {};

  var RVA = {
    OnSpecialBtnDown: 0xB629F0,
    KnifeAttackEvent: 0xB62730,
    OnKnifeAttackExit: 0xB62990,
    OnAnimationExit: 0xB62800,
    Weapon_get_isMyWeapon: 0xB6E1D0
  };

  var OFF = {
    realData: 0xEC,
    knifeAttacks: 0x180,
    knifeAttackCount: 0x118,
    knifeAttackAnim: 0x11C
  };

  var CFG = {
    maxGuardMs: 900,
    callExitOnUnlock: true,
    observeNaturalAfterUnlockMs: 250,
    guardLockValue: 1
  };

  var st = {
    enabled: false,
    installed: false,
    initialized: false,

    seq: 0,
    current: null,

    manualCallingExit: false,

    observeWeaponKey: '',
    observeSeq: 0,
    observeUntilMs: 0,

    rightHits: 0,
    firstAllowed: 0,
    guardedRights: 0,
    naturalDamageHits: 0,
    duplicateNaturalHits: 0,
    exitHits: 0,
    animExitHits: 0,
    unlocks: 0,
    forceClears: 0,
    staleLockClears: 0,
    nonLocalSkips: 0,
    noKnifeSkips: 0,
    maxGuardClears: 0,

    lastError: null,

    isMyWeaponFn: null,
    onKnifeAttackExitFn: null,
    hooks: [],
    logCounter: {}
  };

  function nowMs() { return Date.now(); }

  function log(level, mod, msg) {
    if (!st.logCounter[mod]) st.logCounter[mod] = 0;
    st.logCounter[mod]++;
    if (st.logCounter[mod] > MAX_LOGS_PER_MODULE) return;

    var text = '[极速枪托v3.2][' + mod + '] ' + msg;
    console.log('[' + level + '] ' + text);
    try {
      var mappedLevel = {
        '成功': 'success',
        '信息': 'info',
        '警告': 'warn',
        '错误': 'error'
      }[level] || level;
      send({ type: 'log', level: mappedLevel, module: '极速枪托v3.2/' + mod, message: msg, audience: 'both' });
    } catch (e) {}
  }

  function sendStatus(feature, enabled) {
    try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (e) {}
  }

  function getModule() {
    if (gameModule) return gameModule;

    try {
      gameModule = Process.findModuleByName('GameAssembly.dll');
      if (!gameModule) {
        st.lastError = '没有找到 GameAssembly.dll';
        log('错误', '初始化', st.lastError);
        return null;
      }
      log('成功', '初始化', 'GameAssembly 基址=' + gameModule.base);
      return gameModule;
    } catch (e) {
      st.lastError = '获取 GameAssembly.dll 失败：' + e.message;
      log('错误', '初始化', st.lastError);
      return null;
    }
  }

  function initNative() {
    if (st.initialized) return true;

    var m = getModule();
    if (!m) return false;

    try {
      st.isMyWeaponFn = new NativeFunction(
        m.base.add(RVA.Weapon_get_isMyWeapon),
        'bool',
        ['pointer', 'pointer'],
        ABI
      );

      st.onKnifeAttackExitFn = new NativeFunction(
        m.base.add(RVA.OnKnifeAttackExit),
        'void',
        ['pointer', 'pointer'],
        ABI
      );

      st.initialized = true;
      log('成功', '初始化', 'NativeFunction 初始化完成');
      return true;
    } catch (e) {
      st.lastError = 'NativeFunction 初始化失败：' + e.message;
      log('错误', '初始化', st.lastError);
      return false;
    }
  }

  function rp(addr) {
    try {
      if (!addr || addr.isNull()) return ptr(0);
      return addr.readPointer();
    } catch (e) {
      return ptr(0);
    }
  }

  function ri(addr, def) {
    try {
      if (!addr || addr.isNull()) return def;
      return addr.readS32();
    } catch (e) {
      return def;
    }
  }

  function wi(addr, value) {
    try {
      if (!addr || addr.isNull()) return false;
      addr.writeS32(value);
      return true;
    } catch (e) {
      st.lastError = '写入字段失败：' + e.message;
      return false;
    }
  }

  function rstr(p) {
    try {
      if (!p || p.isNull()) return '';
      var len = p.add(0x10).readS32();
      if (len <= 0 || len > 256) return '';
      return p.add(0x14).readUtf16String(len) || '';
    } catch (e) {
      return '';
    }
  }

  function weaponKey(w) {
    try { return w.toString(); } catch (e) { return ''; }
  }

  function isLocalWeapon(w) {
    if (!w || w.isNull()) return false;
    if (!initNative()) return false;

    try {
      return st.isMyWeaponFn(w, ptr(0)) ? true : false;
    } catch (e) {
      st.lastError = '判断本地武器失败：' + e.message;
      return false;
    }
  }

  function hasKnifeAttack(w) {
    if (!w || w.isNull()) return false;

    var count = ri(w.add(OFF.knifeAttackCount), 0);
    if (count > 0) return true;

    var realData = rp(w.add(OFF.realData));
    if (!realData || realData.isNull()) return false;

    var arr = rp(realData.add(OFF.knifeAttacks));
    if (!arr || arr.isNull()) return false;

    return ri(arr.add(0x0C), 0) > 0;
  }

  function readLock(w) {
    return ri(w.add(OFF.knifeAttackAnim), 0);
  }

  function writeLock(w, value, reason) {
    if (!w || w.isNull()) return false;
    var ok = wi(w.add(OFF.knifeAttackAnim), value);
    if (ok) log('信息', '状态锁', reason + '：knifeAttackAnim=' + value);
    return ok;
  }

  function clearTimer(id) {
    try { if (id) clearTimeout(id); } catch (e) {}
  }

  function currentBelongs(w) {
    return st.current && w && !w.isNull() && st.current.weaponKey === weaponKey(w);
  }

  function beginObserve(atk) {
    st.observeWeaponKey = atk.weaponKey;
    st.observeSeq = atk.seq;
    st.observeUntilMs = nowMs() + CFG.observeNaturalAfterUnlockMs;
  }

  function isInObserveWindow(w) {
    if (!w || w.isNull()) return false;
    if (!st.observeWeaponKey) return false;
    if (weaponKey(w) !== st.observeWeaponKey) return false;
    return nowMs() <= st.observeUntilMs;
  }

  function startAttack(w) {
    st.seq++;

    var atk = {
      seq: st.seq,
      weapon: w,
      weaponKey: weaponKey(w),
      startMs: nowMs(),
      phase: '等待伤害',
      damageDone: false,
      unlocked: false,
      maxTimer: null
    };

    st.current = atk;
    st.firstAllowed++;

    log('成功', '右键', '放行第一次右键，seq=' + atk.seq + '，weapon=' + w);

    atk.maxTimer = setTimeout(function () {
      if (st.current === atk && !atk.unlocked) {
        st.maxGuardClears++;
        log('警告', '最大保护', '达到最大保护窗口，强制恢复，seq=' + atk.seq);
        unlockAttack(atk, '最大保护窗口');
      }
    }, CFG.maxGuardMs);

  }

  function unlockAttack(atk, reason) {
    if (!atk || atk.unlocked) return;

    atk.unlocked = true;
    atk.phase = '已解锁';

    clearTimer(atk.maxTimer);

    if (CFG.callExitOnUnlock && initNative()) {
      try {
        st.manualCallingExit = true;
        st.onKnifeAttackExitFn(atk.weapon, ptr(0));
        log('信息', '解锁', reason + '：已调用 OnKnifeAttackExit，seq=' + atk.seq);
      } catch (e) {
        st.lastError = '调用 OnKnifeAttackExit 失败：' + e.message;
        log('警告', '解锁', st.lastError);
      } finally {
        st.manualCallingExit = false;
      }
    }

    beginObserve(atk);

    if (st.current === atk) st.current = null;
    st.unlocks++;

    log('成功', '解锁',
      reason + '：已恢复空闲，seq=' + atk.seq +
      '；后续 ' + CFG.observeNaturalAfterUnlockMs + 'ms 内仅观察自然重复伤害'
    );
  }

  function protectReentry(w) {
    if (!st.current || st.current.unlocked) return;

    var oldLock = readLock(w);
    if (oldLock === 0) {
      writeLock(w, CFG.guardLockValue | 0, '防打断保护');
    }

    st.guardedRights++;

    if (st.guardedRights <= 30 || st.guardedRights % 20 === 0) {
      log('信息', '防打断',
        '上一击未结束，本次右键进入保护。phase=' +
        st.current.phase + '，oldLock=' + oldLock +
        '，次数=' + st.guardedRights
      );
    }
  }

  function handleOriginalEnd(w, source) {
    if (!currentBelongs(w)) return;

    var atk = st.current;

    if (!atk.damageDone) {
      log('信息', '原始结束',
        source + ' 在原始伤害事件前到达，暂不解锁，等待 KnifeAttackEvent，seq=' + atk.seq
      );
      return;
    }

    log('信息', '原始结束',
      source + ' 在原始伤害事件后到达，当前攻击已按原始事件处理，seq=' + atk.seq
    );
  }

  function forceClear() {
    st.forceClears++;

    if (st.current) {
      unlockAttack(st.current, '手动强制恢复');
    } else {
      log('信息', '强制恢复', '当前没有正在保护的攻击状态');
    }

    return true;
  }

  function installHooks() {
    if (st.installed) return true;

    var m = getModule();
    if (!m) return false;
    if (!initNative()) return false;

    try {
      st.hooks.push(Interceptor.attach(m.base.add(RVA.OnSpecialBtnDown), {
        onEnter: function (args) {
          try {
            if (!st.enabled) return;

            var w = args[0];

            if (!isLocalWeapon(w)) {
              st.nonLocalSkips++;
              return;
            }

            if (!hasKnifeAttack(w)) {
              st.noKnifeSkips++;
              return;
            }

            st.rightHits++;

            if (st.current && !st.current.unlocked) {
              protectReentry(w);
              return;
            }

            var lockValue = readLock(w);
            if (lockValue !== 0) {
              st.staleLockClears++;
              log('信息', '右键', '上一击仍处于游戏锁定状态，拒绝本次右键，lock=' + lockValue);
              return;
            }

            startAttack(w);
          } catch (e) {
            st.lastError = 'OnSpecialBtnDown 异常：' + e.message;
            log('错误', '右键', st.lastError);
          }
        }
      }));

      st.hooks.push(Interceptor.attach(m.base.add(RVA.KnifeAttackEvent), {
        onEnter: function (args) {
          this.weapon = args[0];
          this.local = st.enabled && isLocalWeapon(this.weapon);
          this.attackIndex = 0;
          try { this.attackIndex = args[1].toInt32(); } catch (e) {}
        },
        onLeave: function () {
          try {
            if (!this.local) return;
            var w = this.weapon;
            var idx = this.attackIndex;

            if (currentBelongs(w)) {
              var atk = st.current;

              if (!atk.damageDone) {
                atk.damageDone = true;
                atk.phase = '等待解锁';
                st.naturalDamageHits++;

                var used = nowMs() - atk.startMs;
                log('成功', '自然伤害',
                  '原游戏 KnifeAttackEvent 先到，attackIndex=' + idx +
                  '，距右键=' + used + 'ms，seq=' + atk.seq
                );

                unlockAttack(atk, '自然伤害完成');
              } else {
                st.duplicateNaturalHits++;
                log('信息', '重复自然伤害',
                  '当前攻击内观察到重复自然 KnifeAttackEvent，attach-only 只记录不吞，seq=' +
                  atk.seq + '，attackIndex=' + idx
                );
              }

              return;
            }

            if (isInObserveWindow(w)) {
              st.duplicateNaturalHits++;
              log('信息', '重复自然伤害',
                '自然伤害解锁后观察到自然 KnifeAttackEvent，视为重复自然伤害观察，seq=' +
                st.observeSeq + '，attackIndex=' + idx
              );
              return;
            }

            st.naturalDamageHits++;
            log('信息', '自然伤害',
              '观察到自然 KnifeAttackEvent，但无当前保护状态，attackIndex=' + idx
            );
          } catch (e) {
            st.lastError = 'KnifeAttackEvent Hook 异常：' + e.message;
            log('错误', '伤害', st.lastError);
          }
        }
      }));

      st.hooks.push(Interceptor.attach(m.base.add(RVA.OnKnifeAttackExit), {
        onEnter: function (args) {
          try {
            if (!st.enabled) return;
            if (st.manualCallingExit) return;

            var w = args[0];
            if (!isLocalWeapon(w)) return;

            st.exitHits++;
            handleOriginalEnd(w, 'OnKnifeAttackExit');
          } catch (e) {
            st.lastError = 'OnKnifeAttackExit Hook 异常：' + e.message;
            log('错误', '退出', st.lastError);
          }
        }
      }));

      st.hooks.push(Interceptor.attach(m.base.add(RVA.OnAnimationExit), {
        onEnter: function (args) {
          try {
            if (!st.enabled) return;

            var w = args[0];
            if (!isLocalWeapon(w)) return;

            var animName = rstr(args[1]);
            var animTag = rstr(args[2]);

            st.animExitHits++;
            handleOriginalEnd(w, 'OnAnimationExit:' + (animTag || animName || 'empty'));
          } catch (e) {
            st.lastError = 'OnAnimationExit Hook 异常：' + e.message;
            log('错误', '动画退出', st.lastError);
          }
        }
      }));

      st.installed = true;
      log('成功', 'Hook', 'v3.2 Hook 已安装：attach-only，保留原始伤害事件，不碰动画');
      return true;
    } catch (e) {
      st.lastError = 'Hook 安装失败：' + e.message;
      log('错误', 'Hook', st.lastError);
      return false;
    }
  }

  function enable() {
    if (!installHooks()) {
      st.enabled = false;
      return false;
    }

    st.enabled = true;
    log('成功', '状态',
      '极速枪托 v3.2 已开启：仅在原始伤害事件完成后解锁；异常保护=' + CFG.maxGuardMs + 'ms'
    );
    sendStatus('fast_gunstock', true);
    return true;
  }

  function disable() {
    st.enabled = false;
    if (st.current) forceClear();
    log('信息', '状态', '极速枪托 v3.2 已关闭');
    sendStatus('fast_gunstock', false);
    return true;
  }

  function cleanup() {
    disable();

    for (var i = 0; i < st.hooks.length; i++) {
      try { st.hooks[i].detach(); } catch (e) {}
    }

    st.hooks = [];
    st.installed = false;
    log('成功', '状态', 'Hook 已清理');
    return true;
  }

  function status() {
    var phase = '空闲';
    if (st.current) phase = st.current.phase;

    return {
      enabled: st.enabled,
      installed: st.installed,
      initialized: st.initialized,

      maxGuardMs: CFG.maxGuardMs,
      callExitOnUnlock: CFG.callExitOnUnlock,

      protecting: st.current ? true : false,
      phase: phase,
      currentSeq: st.current ? st.current.seq : 0,
      currentDamageDone: st.current ? st.current.damageDone : false,

      rightHits: st.rightHits,
      firstAllowed: st.firstAllowed,
      guardedRights: st.guardedRights,
      naturalDamageHits: st.naturalDamageHits,
      duplicateNaturalHits: st.duplicateNaturalHits,
      exitHits: st.exitHits,
      animExitHits: st.animExitHits,
      unlocks: st.unlocks,
      forceClears: st.forceClears,
      staleLockClears: st.staleLockClears,
      maxGuardClears: st.maxGuardClears,
      nonLocalSkips: st.nonLocalSkips,
      noKnifeSkips: st.noKnifeSkips,
      config: pluginConfig,

      lastError: st.lastError
    };
  }

  function __pluginApplyConfig(config) {
    if (config) {
      for (var key in config) {
        if (Object.prototype.hasOwnProperty.call(config, key)) pluginConfig[key] = config[key];
      }
    }
    return { ok: true, config: pluginConfig };
  }

  function __pluginEnable(config) {
    if (config) __pluginApplyConfig(config);
    var ok = enable();
    return { ok: ok === true, enabled: st.enabled, status: status() };
  }

  function __pluginDisable() {
    var ok = disable();
    return { ok: ok === true, enabled: false, status: status() };
  }

  function __pluginStatus() {
    return status();
  }

  function __pluginCleanup(payload) {
    var ok = cleanup();
    return { ok: ok === true, reason: payload && payload.reason ? payload.reason : 'cleanup' };
  }

  function __pluginForceClear() {
    var ok = forceClear();
    return { ok: ok === true, status: status() };
  }

  rpc.exports = {
    enable: __pluginEnable,
    disable: __pluginDisable,
    setConfig: __pluginApplyConfig,
    cleanup: __pluginCleanup,
    status: __pluginStatus,
    forceClear: __pluginForceClear
  };

  rpc.exports.setconfig = rpc.exports.setConfig;
  rpc.exports.forceclear = rpc.exports.forceClear;

  log('成功', '初始化', '极速枪托 v3.2 原始伤害完成后解锁脚本已加载');
})();
