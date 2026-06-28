// AAAAA-fast_gunstock_v2_2_1_safe.js
// 极速枪托 v2.2.1 安全防打断版
// 不修改 Animator.speed；不 replace 函数；只 attach 观察 + 保护窗口。

(function () {
  'use strict';

  var ABI = 'mscdecl';
  var mod = null;
  var logCount = {};
  var maxLog = 220;

  var RVA = {
    OnSpecialBtnDown: 0xB629F0,
    GetKnifeAttackData: 0xB61F90,
    KnifeAttackEvent: 0xB62730,
    OnKnifeAttackExit: 0xB62990,
    Weapon_get_isMyWeapon: 0xB6E1D0
  };

  var OFF = {
    realData: 0xEC,
    knifeAttacks: 0x180,
    knifeAttackCount: 0x118,
    knifeAttackAnim: 0x11C
  };

  var cfg = {
    earlyDelayMs: 120,
    unlockDelayMs: 40,
    guardTimeoutMs: 650,
    attackIndex: 0,
    guardLockValue: 1
  };

  var pendingCfg = null;

  var st = {
    enabled: false,
    initialized: false,
    installed: false,
    hooks: [],
    current: null,
    seq: 0,
    manualDamage: false,

    rightHits: 0,
    firstAllowed: 0,
    protectedRights: 0,
    skipNoGunstock: 0,
    skipNotLocal: 0,
    oldLockClears: 0,
    earlyDamageCalls: 0,
    naturalDamageHits: 0,
    duplicateNaturalObserved: 0,
    unlockCalls: 0,
    guardTimeouts: 0,
    paramsQueued: 0,
    paramsApplied: 0,
    lastError: null,

    fnIsMyWeapon: null,
    fnKnifeAttackEvent: null,
    fnOnKnifeAttackExit: null
  };

  function log(level, module, msg) {
    if (!logCount[module]) logCount[module] = 0;
    if (logCount[module] >= maxLog) return;
    logCount[module]++;
    console.log('[极速枪托v2.2.1][' + level + '][' + module + '] ' + msg);
    try { send({ type: '日志', level: level, module: '极速枪托/' + module, message: msg }); } catch (e) {}
  }

  function now() { return Date.now(); }

  function getModule() {
    if (mod) return mod;
    try {
      mod = Process.findModuleByName('GameAssembly.dll');
      if (!mod) {
        st.lastError = '没有找到 GameAssembly.dll';
        log('错误', '初始化', st.lastError);
        return null;
      }
      log('成功', '初始化', 'GameAssembly 基址=' + mod.base);
      return mod;
    } catch (e) {
      st.lastError = '获取 GameAssembly.dll 失败：' + e.message;
      log('错误', '初始化', st.lastError);
      return null;
    }
  }

  function readPtr(addr) {
    try {
      if (!addr || addr.isNull()) return null;
      var p = addr.readPointer();
      if (!p || p.isNull()) return null;
      return p;
    } catch (e) { return null; }
  }

  function readI32(addr, def) {
    try {
      if (!addr || addr.isNull()) return def;
      return addr.readS32();
    } catch (e) { return def; }
  }

  function writeI32(addr, val) {
    try {
      if (!addr || addr.isNull()) return false;
      addr.writeS32(val);
      return true;
    } catch (e) {
      st.lastError = '写入内存失败：' + e.message;
      return false;
    }
  }

  function initFunctions() {
    if (st.initialized) return true;
    var m = getModule();
    if (!m) return false;
    try {
      st.fnIsMyWeapon = new NativeFunction(m.base.add(RVA.Weapon_get_isMyWeapon), 'bool', ['pointer', 'pointer'], ABI);
      st.fnKnifeAttackEvent = new NativeFunction(m.base.add(RVA.KnifeAttackEvent), 'void', ['pointer', 'int', 'pointer'], ABI);
      st.fnOnKnifeAttackExit = new NativeFunction(m.base.add(RVA.OnKnifeAttackExit), 'void', ['pointer', 'pointer'], ABI);
      st.initialized = true;
      log('成功', '初始化', 'NativeFunction 初始化完成');
      return true;
    } catch (e) {
      st.lastError = 'NativeFunction 初始化失败：' + e.message;
      log('错误', '初始化', st.lastError);
      return false;
    }
  }

  function isLocalWeapon(weapon) {
    if (!weapon || weapon.isNull()) return false;
    if (!initFunctions()) return false;
    try { return st.fnIsMyWeapon(weapon, ptr(0)) ? true : false; }
    catch (e) { st.lastError = '判断本地武器失败：' + e.message; return false; }
  }

  function hasGunstock(weapon) {
    if (!weapon || weapon.isNull()) return false;
    var count = readI32(weapon.add(OFF.knifeAttackCount), 0);
    if (count > 0) return true;
    var realData = readPtr(weapon.add(OFF.realData));
    if (!realData) return false;
    var arr = readPtr(realData.add(OFF.knifeAttacks));
    if (!arr) return false;
    return readI32(arr.add(0x0C), 0) > 0;
  }

  function keyOf(weapon) {
    try { return weapon.toString(); } catch (e) { return ''; }
  }

  function belongsToCurrent(weapon) {
    return st.current && weapon && !weapon.isNull() && st.current.weaponKey === keyOf(weapon);
  }

  function clearCurrent(reason) {
    if (st.current) log('信息', '保护', '清理当前攻击：' + reason);
    st.current = null;
    applyQueuedParams();
  }

  function unlockWeapon(weapon, source) {
    if (!weapon || weapon.isNull()) return false;
    if (!initFunctions()) return false;
    var ok = false;
    try {
      st.fnOnKnifeAttackExit(weapon, ptr(0));
      ok = true;
    } catch (e) {
      st.lastError = '调用 OnKnifeAttackExit 失败：' + e.message;
      log('警告', '解锁', st.lastError);
    }
    if (writeI32(weapon.add(OFF.knifeAttackAnim), 0)) ok = true;
    st.unlockCalls++;
    log('信息', '解锁', source + '：已尝试退出并清零 knifeAttackAnim');
    return ok;
  }

  function guardActive() {
    if (!st.current) return false;
    var age = now() - st.current.startMs;
    if (age > cfg.guardTimeoutMs) {
      st.guardTimeouts++;
      log('警告', '保护', '保护超时，自动恢复。耗时=' + age + 'ms');
      unlockWeapon(st.current.weapon, '保护超时恢复');
      clearCurrent('保护超时');
      return false;
    }
    return true;
  }

  function scheduleUnlock(seq, weapon, source) {
    var delay = Math.max(0, cfg.unlockDelayMs | 0);
    setTimeout(function () {
      try {
        if (!st.enabled || !st.current || st.current.seq !== seq) return;
        unlockWeapon(weapon, source + '，延迟=' + delay + 'ms');
        if (st.current && st.current.seq === seq) {
          st.current.unlockDone = true;
          clearCurrent('伤害完成并解锁');
        }
      } catch (e) {
        st.lastError = '延迟解锁异常：' + e.message;
        log('错误', '解锁', st.lastError);
        clearCurrent('解锁异常');
      }
    }, delay);
  }

  function markDamageDone(seq, weapon, source) {
    if (!st.current || st.current.seq !== seq || st.current.damageDone) return;
    st.current.damageDone = true;
    st.current.damageMs = now();
    log('成功', '伤害', source + '完成，准备解锁。seq=' + seq);
    scheduleUnlock(seq, weapon, source);
  }

  function doEarlyDamage(seq) {
    try {
      if (!st.enabled || !st.current || st.current.seq !== seq) return;
      var atk = st.current;
      if (atk.damageDone) return;
      var weapon = atk.weapon;
      if (!weapon || weapon.isNull()) { clearCurrent('武器指针无效'); return; }

      st.manualDamage = true;
      try {
        st.fnKnifeAttackEvent(weapon, atk.attackIndex, ptr(0));
        st.earlyDamageCalls++;
        log('成功', '提前伤害', '已触发 KnifeAttackEvent，延迟=' + atk.earlyDelay + 'ms，attackIndex=' + atk.attackIndex + '，seq=' + seq);
      } finally {
        st.manualDamage = false;
      }
      markDamageDone(seq, weapon, '提前伤害');
    } catch (e) {
      st.manualDamage = false;
      st.lastError = '提前伤害异常：' + e.message;
      log('错误', '提前伤害', st.lastError);
      clearCurrent('提前伤害异常');
    }
  }

  function startAttack(weapon) {
    st.seq++;
    var seq = st.seq;
    st.current = {
      seq: seq,
      weapon: weapon,
      weaponKey: keyOf(weapon),
      startMs: now(),
      attackIndex: cfg.attackIndex | 0,
      earlyDelay: cfg.earlyDelayMs | 0,
      damageDone: false,
      unlockDone: false
    };
    st.firstAllowed++;
    log('信息', '右键', '首次枪托放行，进入保护窗口。seq=' + seq + '，提前伤害=' + cfg.earlyDelayMs + 'ms，伤害后解锁=' + cfg.unlockDelayMs + 'ms');
    setTimeout(function () { doEarlyDamage(seq); }, Math.max(30, cfg.earlyDelayMs | 0));
  }

  function protectEarlyRight(weapon) {
    var lockAddr = weapon.add(OFF.knifeAttackAnim);
    if (readI32(lockAddr, 0) === 0) writeI32(lockAddr, cfg.guardLockValue);
    st.protectedRights++;
    if (st.protectedRights <= 30 || st.protectedRights % 50 === 0) {
      var age = st.current ? (now() - st.current.startMs) : 0;
      log('信息', '保护', '过早第二次右键已加锁保护，等待第一次伤害完成。已等待=' + age + 'ms');
    }
  }

  function installHooks() {
    if (st.installed) return true;
    var m = getModule();
    if (!m || !initFunctions()) return false;
    try {
      var h1 = Interceptor.attach(m.base.add(RVA.OnSpecialBtnDown), {
        onEnter: function (args) {
          try {
            if (!st.enabled) return;
            var weapon = args[0];
            if (!weapon || weapon.isNull()) return;
            st.rightHits++;
            if (!isLocalWeapon(weapon)) { st.skipNotLocal++; return; }
            if (!hasGunstock(weapon)) { st.skipNoGunstock++; return; }

            if (guardActive()) {
              protectEarlyRight(weapon);
              return;
            }

            var oldLock = readI32(weapon.add(OFF.knifeAttackAnim), 0);
            if (oldLock !== 0) {
              st.oldLockClears++;
              writeI32(weapon.add(OFF.knifeAttackAnim), 0);
              log('信息', '右键', '发现旧锁残留，已清零后放行');
            }
            startAttack(weapon);
          } catch (e) {
            st.lastError = '右键入口 Hook 异常：' + e.message;
            log('错误', '右键', st.lastError);
          }
        }
      });
      st.hooks.push(h1);

      var h2 = Interceptor.attach(m.base.add(RVA.KnifeAttackEvent), {
        onEnter: function (args) {
          try {
            if (!st.enabled || st.manualDamage) return;
            var weapon = args[0];
            var attackIndex = args[1].toInt32();
            if (belongsToCurrent(weapon)) {
              var atk = st.current;
              if (!atk.damageDone) {
                st.naturalDamageHits++;
                log('成功', '自然伤害', '原游戏自然伤害先到。attackIndex=' + attackIndex + '，seq=' + atk.seq);
                markDamageDone(atk.seq, weapon, '自然伤害');
              } else {
                st.duplicateNaturalObserved++;
                if (st.duplicateNaturalObserved <= 20 || st.duplicateNaturalObserved % 50 === 0) {
                  log('信息', '观察', '提前伤害后又观察到自然伤害事件。attach 版只记录，不强行吞掉。seq=' + atk.seq);
                }
              }
            }
          } catch (e) {
            st.lastError = '伤害事件 Hook 异常：' + e.message;
            log('错误', '伤害', st.lastError);
          }
        }
      });
      st.hooks.push(h2);

      var h3 = Interceptor.attach(m.base.add(RVA.GetKnifeAttackData), {
        onEnter: function (args) {
          try {
            if (!st.enabled) return;
            var weapon = args[0];
            var attackIndex = args[1].toInt32();
            if (belongsToCurrent(weapon) && attackIndex !== st.current.attackIndex) {
              log('信息', '攻击数据', '原游戏 attackIndex=' + attackIndex + '，手动 attackIndex=' + st.current.attackIndex);
            }
          } catch (e) {}
        }
      });
      st.hooks.push(h3);

      st.installed = true;
      log('成功', 'Hook', '安全 attach Hook 已安装');
      return true;
    } catch (e) {
      st.lastError = 'Hook 安装失败：' + e.message;
      log('错误', 'Hook', st.lastError);
      return false;
    }
  }

  function clamp(v, oldValue, min, max) {
    v = parseInt(v, 10);
    if (isNaN(v)) v = oldValue;
    if (v < min) v = min;
    if (v > max) v = max;
    return v;
  }

  function applyParamsDirect(p, source) {
    cfg.earlyDelayMs = clamp(p['提前伤害延迟ms'], cfg.earlyDelayMs, 30, 300);
    cfg.unlockDelayMs = clamp(p['伤害后解锁延迟ms'], cfg.unlockDelayMs, 0, 200);
    cfg.guardTimeoutMs = clamp(p['保护超时ms'], cfg.guardTimeoutMs, 300, 1500);
    cfg.attackIndex = clamp(p['attackIndex'], cfg.attackIndex, 0, 5);
    st.paramsApplied++;
    var msg = source + '已应用：提前伤害=' + cfg.earlyDelayMs + 'ms，伤害后解锁=' + cfg.unlockDelayMs + 'ms，保护超时=' + cfg.guardTimeoutMs + 'ms，attackIndex=' + cfg.attackIndex;
    log('成功', '参数', msg);
    return { ok: true, queued: false, message: msg };
  }

  function applyQueuedParams() {
    if (!pendingCfg || st.current) return;
    var p = pendingCfg;
    pendingCfg = null;
    applyParamsDirect(p, '暂存参数');
  }

  function setparams(p) {
    try {
      if (!p) return { ok: false, queued: false, message: '参数为空' };
      if (st.current) {
        pendingCfg = p;
        st.paramsQueued++;
        var msg = '当前正在攻击保护中，参数已暂存，本次攻击结束后自动应用';
        log('信息', '参数', msg);
        return { ok: true, queued: true, message: msg };
      }
      return applyParamsDirect(p, '手动参数');
    } catch (e) {
      st.lastError = '设置参数失败：' + e.message;
      log('错误', '参数', st.lastError);
      return { ok: false, queued: false, message: st.lastError };
    }
  }

  function enable() {
    if (!installHooks()) { st.enabled = false; return false; }
    st.enabled = true;
    log('成功', '状态', '已开启安全防打断版');
    return true;
  }

  function disable() {
    st.enabled = false;
    if (st.current) unlockWeapon(st.current.weapon, '手动关闭');
    clearCurrent('手动关闭');
    log('信息', '状态', '已关闭');
    return true;
  }

  function cleanup() {
    disable();
    for (var i = 0; i < st.hooks.length; i++) {
      try { st.hooks[i].detach(); } catch (e) {}
    }
    st.hooks = [];
    st.installed = false;
    log('成功', '状态', 'Hook 已 detach，脚本清理完成');
    return true;
  }

  function status() {
    var atk = st.current;
    return {
      已开启: st.enabled,
      已初始化: st.initialized,
      已安装: st.installed,
      提前伤害延迟ms: cfg.earlyDelayMs,
      伤害后解锁延迟ms: cfg.unlockDelayMs,
      保护超时ms: cfg.guardTimeoutMs,
      attackIndex: cfg.attackIndex,
      正在保护: atk ? true : false,
      当前已出伤害: atk ? atk.damageDone : false,
      当前已解锁: atk ? atk.unlockDone : false,
      当前序号: atk ? atk.seq : 0,
      右键进入次数: st.rightHits,
      首次放行次数: st.firstAllowed,
      过早右键保护次数: st.protectedRights,
      非枪托跳过次数: st.skipNoGunstock,
      非本地跳过次数: st.skipNotLocal,
      旧锁清理次数: st.oldLockClears,
      提前伤害次数: st.earlyDamageCalls,
      自然伤害次数: st.naturalDamageHits,
      重复自然伤害观察次数: st.duplicateNaturalObserved,
      解锁次数: st.unlockCalls,
      保护超时次数: st.guardTimeouts,
      参数暂存次数: st.paramsQueued,
      参数应用次数: st.paramsApplied,
      最后错误: st.lastError
    };
  }

  rpc.exports = {
    enable: enable,
    disable: disable,
    cleanup: cleanup,
    status: status,
    setparams: setparams
  };

  log('成功', '初始化', '极速枪托 v2.2.1 安全防打断脚本已加载');
})();
