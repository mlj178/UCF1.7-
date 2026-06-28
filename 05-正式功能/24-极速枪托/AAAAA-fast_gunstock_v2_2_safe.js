// AAAAA-fast_gunstock_v2_2_safe.js
// 极速枪托 v2.2 安全防打断版
// 修复点：不再 replace 游戏函数；拖动 UI 滑块不再高频 RPC；保护中参数暂存。

(function () {
  'use strict';

  var ABI = 'mscdecl';
  var mod = null;

  var RVA = {
    onSpecial: 0xB629F0,      // WPN_Gun.OnSpecialBtnDown()
    getData: 0xB61F90,        // WPN_Gun.GetKnifeAttackData(int)
    damage: 0xB62730,         // WPN_Gun.KnifeAttackEvent(int)
    exit: 0xB62990,           // WPN_Gun.OnKnifeAttackExit()
    isMine: 0xB6E1D0          // Weapon.get_isMyWeapon()
  };

  var OFF = {
    realData: 0xEC,
    knifeAttacks: 0x180,
    knifeCount: 0x118,
    knifeLock: 0x11C
  };

  var P = {
    earlyDelay: 120,
    unlockDelay: 40,
    guardTimeout: 650,
    attackIndex: 0,
    blockLockValue: 1
  };

  var pendingParams = null;
  var logCount = {};
  var LOG_LIMIT = 180;

  var S = {
    enabled: false,
    initialized: false,
    hooksInstalled: false,
    hooks: [],
    current: null,
    seq: 0,
    callingEarlyDamage: false,

    rightHits: 0,
    allowedHits: 0,
    protectedHits: 0,
    skippedNotMine: 0,
    skippedNoGunstock: 0,
    staleLockClears: 0,

    earlyDamageHits: 0,
    naturalDamageHits: 0,
    duplicateNaturalSeen: 0,
    unlockHits: 0,
    guardTimeoutHits: 0,
    paramApplyHits: 0,
    paramQueuedHits: 0,

    lastError: null,

    fnIsMine: null,
    fnDamage: null,
    fnExit: null
  };

  function log(level, tag, msg) {
    logCount[tag] = (logCount[tag] || 0) + 1;
    if (logCount[tag] > LOG_LIMIT) return;
    var text = '[极速枪托v2.2][' + tag + '] ' + msg;
    console.log('[' + level + '] ' + text);
    try { send({ type: '日志', level: level, module: '极速枪托/' + tag, message: msg }); } catch (e) {}
  }

  function now() { return Date.now(); }

  function module_() {
    if (mod) return mod;
    try {
      mod = Process.findModuleByName('GameAssembly.dll');
      if (!mod) {
        S.lastError = '没有找到 GameAssembly.dll';
        log('错误', '初始化', S.lastError);
        return null;
      }
      log('成功', '初始化', 'GameAssembly 基址=' + mod.base);
      return mod;
    } catch (e) {
      S.lastError = '获取 GameAssembly.dll 失败：' + e.message;
      log('错误', '初始化', S.lastError);
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

  function writeI32(addr, value) {
    try {
      if (!addr || addr.isNull()) return false;
      addr.writeS32(value);
      return true;
    } catch (e) {
      S.lastError = '写入整数失败：' + e.message;
      return false;
    }
  }

  function initFns() {
    if (S.initialized) return true;
    var m = module_();
    if (!m) return false;
    try {
      S.fnIsMine = new NativeFunction(m.base.add(RVA.isMine), 'bool', ['pointer', 'pointer'], ABI);
      S.fnDamage = new NativeFunction(m.base.add(RVA.damage), 'void', ['pointer', 'int', 'pointer'], ABI);
      S.fnExit = new NativeFunction(m.base.add(RVA.exit), 'void', ['pointer', 'pointer'], ABI);
      S.initialized = true;
      log('成功', '初始化', 'NativeFunction 初始化完成');
      return true;
    } catch (e) {
      S.lastError = 'NativeFunction 初始化失败：' + e.message;
      log('错误', '初始化', S.lastError);
      return false;
    }
  }

  function isMine(weapon) {
    if (!weapon || weapon.isNull()) return false;
    if (!initFns()) return false;
    try { return S.fnIsMine(weapon, ptr(0)) ? true : false; }
    catch (e) {
      S.lastError = '判断本地武器失败：' + e.message;
      return false;
    }
  }

  function hasGunstock(weapon) {
    if (!weapon || weapon.isNull()) return false;
    var count = readI32(weapon.add(OFF.knifeCount), 0);
    if (count > 0) return true;
    var realData = readPtr(weapon.add(OFF.realData));
    if (!realData) return false;
    var arr = readPtr(realData.add(OFF.knifeAttacks));
    if (!arr) return false;
    return readI32(arr.add(0x0C), 0) > 0;
  }

  function keyOf(p) {
    try { return p.toString(); } catch (e) { return ''; }
  }

  function currentIs(weapon) {
    return S.current && weapon && !weapon.isNull() && S.current.weaponKey === keyOf(weapon);
  }

  function applyPendingParams() {
    if (!pendingParams || S.current) return;
    var p = pendingParams;
    pendingParams = null;
    applyParamsNow(p, '暂存参数');
  }

  function clearCurrent(reason) {
    if (S.current) log('信息', '保护', '清理当前攻击：' + reason);
    S.current = null;
    applyPendingParams();
  }

  function unlockWeapon(weapon, reason) {
    if (!weapon || weapon.isNull()) return false;
    if (!initFns()) return false;
    var ok = false;
    try {
      S.fnExit(weapon, ptr(0));
      ok = true;
    } catch (e) {
      S.lastError = '调用 OnKnifeAttackExit 失败：' + e.message;
      log('警告', '解锁', S.lastError);
    }
    if (writeI32(weapon.add(OFF.knifeLock), 0)) ok = true;
    S.unlockHits++;
    log('信息', '解锁', reason + '：已尝试退出并清零 knifeAttackAnim');
    return ok;
  }

  function guardAlive() {
    if (!S.current) return false;
    var age = now() - S.current.startMs;
    if (age > P.guardTimeout) {
      S.guardTimeoutHits++;
      log('警告', '保护', '保护窗口超时，自动恢复，耗时=' + age + 'ms');
      unlockWeapon(S.current.weapon, '保护超时恢复');
      clearCurrent('保护超时');
      return false;
    }
    return true;
  }

  function scheduleUnlock(seq, weapon, reason) {
    var delay = Math.max(0, P.unlockDelay | 0);
    setTimeout(function () {
      try {
        if (!S.enabled || !S.current || S.current.seq !== seq) return;
        unlockWeapon(weapon, reason + '，延迟=' + delay + 'ms');
        if (S.current && S.current.seq === seq) {
          S.current.unlockDone = true;
          clearCurrent('伤害完成并解锁');
        }
      } catch (e) {
        S.lastError = '延迟解锁异常：' + e.message;
        log('错误', '解锁', S.lastError);
        clearCurrent('解锁异常');
      }
    }, delay);
  }

  function markDamage(seq, weapon, reason) {
    if (!S.current || S.current.seq !== seq || S.current.damageDone) return;
    S.current.damageDone = true;
    S.current.damageMs = now();
    log('成功', '伤害', reason + '完成，准备解锁。seq=' + seq);
    scheduleUnlock(seq, weapon, reason);
  }

  function doEarlyDamage(seq) {
    try {
      if (!S.enabled || !S.current || S.current.seq !== seq) return;
      var atk = S.current;
      if (atk.damageDone) return;

      var weapon = atk.weapon;
      if (!weapon || weapon.isNull()) {
        clearCurrent('武器指针无效');
        return;
      }

      S.callingEarlyDamage = true;
      try {
        S.fnDamage(weapon, atk.attackIndex, ptr(0));
        S.earlyDamageHits++;
        log('成功', '提前伤害',
          '已触发 KnifeAttackEvent，延迟=' + atk.earlyDelay +
          'ms，attackIndex=' + atk.attackIndex + '，seq=' + seq);
      } finally {
        S.callingEarlyDamage = false;
      }
      markDamage(seq, weapon, '提前伤害');
    } catch (e) {
      S.callingEarlyDamage = false;
      S.lastError = '提前伤害异常：' + e.message;
      log('错误', '提前伤害', S.lastError);
      clearCurrent('提前伤害异常');
    }
  }

  function startFirstAttack(weapon) {
    S.seq++;
    var seq = S.seq;
    S.current = {
      seq: seq,
      weapon: weapon,
      weaponKey: keyOf(weapon),
      startMs: now(),
      attackIndex: P.attackIndex | 0,
      earlyDelay: P.earlyDelay | 0,
      damageDone: false,
      unlockDone: false
    };
    S.allowedHits++;
    log('信息', '右键',
      '首次枪托放行，进入保护窗口。seq=' + seq +
      '，提前伤害=' + P.earlyDelay + 'ms，伤害后解锁=' + P.unlockDelay + 'ms');
    setTimeout(function () { doEarlyDamage(seq); }, Math.max(30, P.earlyDelay | 0));
  }

  function protectSecondRightClick(weapon) {
    var lockAddr = weapon.add(OFF.knifeLock);
    var old = readI32(lockAddr, 0);
    if (old === 0) writeI32(lockAddr, P.blockLockValue);
    S.protectedHits++;
    if (S.protectedHits <= 30 || S.protectedHits % 50 === 0) {
      var age = S.current ? (now() - S.current.startMs) : 0;
      log('信息', '保护', '过早第二次右键已加锁保护，等待第一次伤害完成，已等待=' + age + 'ms');
    }
  }

  function installHooks() {
    if (S.hooksInstalled) return true;
    var m = module_();
    if (!m || !initFns()) return false;
    try {
      var h1 = Interceptor.attach(m.base.add(RVA.onSpecial), {
        onEnter: function (args) {
          try {
            if (!S.enabled) return;
            var weapon = args[0];
            if (!weapon || weapon.isNull()) return;

            S.rightHits++;

            if (!isMine(weapon)) { S.skippedNotMine++; return; }
            if (!hasGunstock(weapon)) { S.skippedNoGunstock++; return; }

            if (guardAlive()) {
              protectSecondRightClick(weapon);
              return;
            }

            var lockValue = readI32(weapon.add(OFF.knifeLock), 0);
            if (lockValue !== 0) {
              S.staleLockClears++;
              writeI32(weapon.add(OFF.knifeLock), 0);
              log('信息', '右键', '发现旧锁残留，已清零后放行');
            }

            startFirstAttack(weapon);
          } catch (e) {
            S.lastError = '右键入口 Hook 异常：' + e.message;
            log('错误', '右键', S.lastError);
          }
        }
      });
      S.hooks.push(h1);

      var h2 = Interceptor.attach(m.base.add(RVA.damage), {
        onEnter: function (args) {
          try {
            if (!S.enabled || S.callingEarlyDamage) return;
            var weapon = args[0];
            var attackIndex = args[1].toInt32();

            if (currentIs(weapon)) {
              var atk = S.current;
              if (!atk.damageDone) {
                S.naturalDamageHits++;
                log('成功', '自然伤害',
                  '原游戏自然伤害先到，取消等待提前伤害。attackIndex=' + attackIndex + '，seq=' + atk.seq);
                markDamage(atk.seq, weapon, '自然伤害');
              } else {
                S.duplicateNaturalSeen++;
                if (S.duplicateNaturalSeen <= 20 || S.duplicateNaturalSeen % 50 === 0) {
                  log('信息', '观察',
                    '提前伤害后又观察到自然伤害事件。安全版不强行吞掉，只记录。seq=' + atk.seq);
                }
              }
            }
          } catch (e) {
            S.lastError = '伤害事件 Hook 异常：' + e.message;
            log('错误', '伤害', S.lastError);
          }
        }
      });
      S.hooks.push(h2);

      var h3 = Interceptor.attach(m.base.add(RVA.getData), {
        onEnter: function (args) {
          try {
            if (!S.enabled || !S.current) return;
            var weapon = args[0];
            var attackIndex = args[1].toInt32();
            if (currentIs(weapon) && attackIndex !== S.current.attackIndex) {
              log('信息', '攻击数据',
                '原游戏 attackIndex=' + attackIndex + '，当前手动 attackIndex=' + S.current.attackIndex);
            }
          } catch (e) {}
        }
      });
      S.hooks.push(h3);

      S.hooksInstalled = true;
      log('成功', 'Hook', '安全 attach Hook 已安装，没有 replace 游戏函数');
      return true;
    } catch (e) {
      S.lastError = 'Hook 安装失败：' + e.message;
      log('错误', 'Hook', S.lastError);
      return false;
    }
  }

  function clamp(v, def, min, max) {
    v = parseInt(v, 10);
    if (isNaN(v)) v = def;
    if (v < min) v = min;
    if (v > max) v = max;
    return v;
  }

  function applyParamsNow(p, source) {
    P.earlyDelay = clamp(p.提前伤害延迟ms, P.earlyDelay, 30, 300);
    P.unlockDelay = clamp(p.伤害后解锁延迟ms, P.unlockDelay, 0, 200);
    P.guardTimeout = clamp(p.保护超时ms, P.guardTimeout, 300, 1500);
    P.attackIndex = clamp(p.attackIndex, P.attackIndex, 0, 5);
    S.paramApplyHits++;

    var msg = source + '已应用：提前伤害=' + P.earlyDelay +
      'ms，伤害后解锁=' + P.unlockDelay +
      'ms，保护超时=' + P.guardTimeout +
      'ms，attackIndex=' + P.attackIndex;
    log('成功', '参数', msg);
    return { ok: true, queued: false, message: msg };
  }

  function setparams(p) {
    try {
      if (S.current) {
        pendingParams = p;
        S.paramQueuedHits++;
        var msg = '当前攻击保护中，参数已暂存，本次攻击结束后自动应用';
        log('信息', '参数', msg);
        return { ok: true, queued: true, message: msg };
      }
      return applyParamsNow(p || {}, '手动参数');
    } catch (e) {
      S.lastError = '设置参数失败：' + e.message;
      log('错误', '参数', S.lastError);
      return { ok: false, queued: false, message: S.lastError };
    }
  }

  function enable() {
    try {
      if (!installHooks()) {
        S.enabled = false;
        return false;
      }
      S.enabled = true;
      log('成功', '状态', '已开启安全防打断版。拖动滑块不会写入游戏，必须点击“应用参数”。');
      return true;
    } catch (e) {
      S.enabled = false;
      S.lastError = '开启失败：' + e.message;
      log('错误', '状态', S.lastError);
      return false;
    }
  }

  function disable() {
    S.enabled = false;
    if (S.current) unlockWeapon(S.current.weapon, '手动关闭');
    clearCurrent('手动关闭');
    log('信息', '状态', '已关闭');
    return true;
  }

  function cleanup() {
    disable();
    for (var i = 0; i < S.hooks.length; i++) {
      try { S.hooks[i].detach(); } catch (e) {}
    }
    S.hooks = [];
    S.hooksInstalled = false;
    log('成功', '状态', 'Hook 已 detach，脚本清理完成');
    return true;
  }

  function status() {
    var c = S.current;
    return {
      已开启: S.enabled,
      已初始化: S.initialized,
      已安装: S.hooksInstalled,

      提前伤害延迟ms: P.earlyDelay,
      伤害后解锁延迟ms: P.unlockDelay,
      保护超时ms: P.guardTimeout,
      attackIndex: P.attackIndex,

      正在保护: c ? true : false,
      当前已出伤害: c ? c.damageDone : false,
      当前已解锁: c ? c.unlockDone : false,
      当前序号: c ? c.seq : 0,

      右键进入次数: S.rightHits,
      首次放行次数: S.allowedHits,
      过早右键保护次数: S.protectedHits,
      非枪托跳过次数: S.skippedNoGunstock,
      非本地跳过次数: S.skippedNotMine,
      旧锁清理次数: S.staleLockClears,

      提前伤害次数: S.earlyDamageHits,
      自然伤害次数: S.naturalDamageHits,
      重复自然伤害观察次数: S.duplicateNaturalSeen,
      解锁次数: S.unlockHits,
      保护超时次数: S.guardTimeoutHits,
      参数应用次数: S.paramApplyHits,
      参数暂存次数: S.paramQueuedHits,

      最后错误: S.lastError
    };
  }

  rpc.exports = {
    enable: enable,
    disable: disable,
    cleanup: cleanup,
    status: status,
    setparams: setparams
  };

  log('成功', '初始化', '极速枪托 v2.2 安全防打断脚本已加载');
})();
