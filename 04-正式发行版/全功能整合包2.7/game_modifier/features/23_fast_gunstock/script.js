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
// - disable 只同步交还"自写锁"并清空运行态：不挂 pending、不在关闭后补调游戏函数；
//   所有 Hook 先判断 st.enabled，关闭后完全不介入（规范 §12.2）
// - 关闭后再开启等于全新一轮：enable 先 resetRuntime，不带上一轮状态
// ============================================================

(function () {
  'use strict';

  var ABI = 'mscdecl';
  var MAX_LOGS_PER_MODULE = 3;
  var gameModule = null;
  var pluginConfig = {};

  var RVA = {
    ModeBase_Update: 0xAF6A00,
    OnSpecialBtnDown: 0xB629F0,
    KnifeAttackEvent: 0xB62730,
    OnKnifeAttackExit: 0xB62990,
    OnAnimationExit: 0xB62800,
    Weapon_get_isMyWeapon: 0xB6E1D0,
    Player_get_isNanoGhost: 0xB56050,
    Player_set_nanoRole: 0xB56880,
    Weapon_OnFireBtnPressed: 0xB6CDA0,
    GameManager_TypeInfo: 0x00E2933C // GameManager 静态字段区（myPlayer@0x0 / static_fields@0x5C）
  };

  var OFF = {
    realData: 0xEC,
    knifeAttacks: 0x180,
    knifeAttackCount: 0x118,
    knifeAttackAnim: 0x11C,
    owner: 0x30
  };

  var CFG = {
    maxGuardMs: 900,
    callExitOnUnlock: true,
    observeNaturalAfterUnlockMs: 250,
    guardLockValue: 1,
    lockWatchdogMs: 1200
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
    ghostSkips: 0,
    maxGuardClears: 0,
    pendingForceUnlock: false,
    pendingForceClear: false,
    pendingRoleClear: false,
    lastRole: -1,

    lockedWeapon: null,
    lockedKlass: null,
    lockedAtMs: 0,
    stormClears: 0,

    lastError: null,

    isMyWeaponFn: null,
    onKnifeAttackExitFn: null,
    isNanoGhostFn: null,
    hooks: [],
    logCounter: {}
  };

  function nowMs() { return Date.now(); }

  // ===== 左键状态防卡死 =====
  // 近战攻击循环的唯一开关是 Weapon._fireBtnPressed(+0x78)：
  //   WPN_Knife.Update / WPN_Knife.OnKnifeAttackAnimEnd / WPN_Gun.OnSpecialBtnDown 都看它。
  // 它由 PlayerController.UseWeapon 每帧用 Input.GetKey(Mouse0=323) 刷新。
  // 一旦游戏侧左键状态卡在"按下"，攻击就会自己一直转下去（打到人后尤其明显），这里用 OS 物理按键状态兜底纠正。
  //
  // ⚠ 必须在 onLeave 里写 0：Weapon.OnFireBtnPressed(+0xB6CDA0) 的函数体就是
  //   `this->fields._fireBtnPressed = 1;`（IDA 反编译 0x10B6CDA0，全文一句话）。
  //   onEnter 里写的 0 会被紧跟着的本体覆盖，等于该保护从未生效（2026-10 定位）。
  var asyncKeyStateFn = null;

  // 诊断通道：raw send({type:'log_file'})，绕过 MAX_LOGS_PER_MODULE=3 的每模块上限
  var diag = { total: 0, keyed: {} };

  function sendDiag(message) {
    try {
      if (diag.total >= 120) return;
      diag.total++;
      send({ type: 'log_file', level: 'info', module: '极速枪托诊断', message: message + ' [#d' + diag.total + ']', audience: 'dev' });
    } catch (e) {}
  }

  function diagByKey(key, message, limit) {
    var n = diag.keyed[key] || 0;
    if (n >= limit) return;
    diag.keyed[key] = n + 1;
    sendDiag(message + ' [' + key + ' x' + (n + 1) + ']');
  }

  // 把返回地址翻译成「模块名+偏移」，用来指认"谁在调用它"
  function callerOf(addr) {
    try {
      if (!addr || addr.isNull()) return '?';
      var m = Process.findModuleByAddress(addr);
      if (m) return m.name + '+0x' + addr.sub(m.base).toString(16);
      var r = Process.findRangeByAddress(addr);
      return r ? ('anon@' + r.base + '+0x' + addr.sub(r.base).toString(16)) : ('raw:' + addr);
    } catch (e) { return 'err'; }
  }

  // OS 级物理左键：{ok:true,down:bool} / {ok:false,reason}
  //
  // ⚠⚠ 类型名必须是 'uint16'。Frida 17 里 'short' 不是合法类型名，
  //    new NativeFunction(fn, 'short', ['int']) 会抛 "invalid type specified"，
  //    异常被 catch 吞掉后本函数恒返回 null -> clearStuckFireBtn 的
  //    `if (physicalLeftDown() !== false) return false;` 永远成立 = 这道兜底从未生效过。
  //    实测：06-测试/frida-revert-probe/probe_async_keystate.py
  //      short=THROW(invalid type specified) | int16=OK | uint16=OK
  function readOsMouseLeft() {
    return readOsKeyState(0x01); // VK_LBUTTON
  }

  // 物理右键：重击（combo3 / OnSpecialBtnDown）对应的就是右键，判异常必须用它
  function readOsMouseRight() {
    return readOsKeyState(0x02); // VK_RBUTTON
  }

  function readOsKeyState(vk) {
    try {
      if (!asyncKeyStateFn) {
        var fn = null;
        try { if (typeof Module.getGlobalExportByName === 'function') fn = Module.getGlobalExportByName('GetAsyncKeyState'); } catch (e) {}
        if (!fn) {
          var u = Process.findModuleByName('user32.dll') || Process.findModuleByName('USER32.dll');
          if (u) { try { fn = u.findExportByName('GetAsyncKeyState'); } catch (e) {} }
        }
        if (!fn) return { ok: false, reason: 'no_export' };
        asyncKeyStateFn = new NativeFunction(fn, 'uint16', ['int']);
      }
      return { ok: true, down: ((asyncKeyStateFn(vk) & 0x8000) !== 0) };
    } catch (e) {
      return { ok: false, reason: 'throw:' + e.message };
    }
  }

  // 备选链路：原实现想用 UnityEngine.Input.GetKey(KeyCode.Mouse0) 兜底，**实测不可用，已移除**。
  // 2026-10 实测日志（13:12:02 自检）：Input.GetKey(Mouse0)=FAIL(throw:access violation accessing 0x4)
  // 原因：`UnityEngine.Input.GetKey` 是 icall 包装壳（0xACFA60 -> il2cpp_resolve_icall），
  // 从 Hook 里调用它会走进 il2cpp 的 icall 解析路径并抛访问违例。在游戏进程里制造访问违例
  // （哪怕被 Frida 捕获）是不可接受的：解析路径上的锁可能不被释放，之后任何一次
  // il2cpp_resolve_icall 都会永久阻塞 —— 表现就是"游戏停止响应"。
  // 结论：OS 链路读不到时什么都不做，不去碰游戏自己的输入状态。
  //
  // true=按下 / false=松开 / null=读不到
  function physicalLeftDown() {
    var os = readOsMouseLeft();
    if (os.ok) return os.down;
    diagByKey('os_fail', '物理按键读取失败(' + os.reason + ')，本次放弃纠正（不使用 Input.GetKey 兜底）', 2);
    return null;
  }

  // true=按下 / false=松开 / null=读不到
  function physicalRightDown() {
    var os = readOsMouseRight();
    if (os.ok) return os.down;
    diagByKey('os_fail', '物理按键读取失败(' + os.reason + ')，本次放弃纠正（不使用 Input.GetKey 兜底）', 2);
    return null;
  }

  function keyStateText(state) {
    if (state === false) return '松开';
    if (state === true) return '按下';
    return '读不到(null)';
  }

  // 物理左键已松开、游戏侧 +0x78 仍是 1 时撤销（本地玩家的武器才动）
  function clearStuckFireBtn(w) {
    try {
      if (!w || w.isNull()) return false;
      if (!initNative()) return false;
      if (w.add(0x78).readU8() !== 1) return false;      // 没卡就不用管
      var down = physicalLeftDown();
      if (down !== false) {                              // true=确实按着 / null=读不到，都不动
        diagByKey('key_' + (down === null ? 'unknown' : 'down'),
          'fireBtnPressed=1 但物理左键=' + (down === null ? '读不到' : '按下') + '，按设计不动', 2);
        return false;
      }
      if (!st.isMyWeaponFn(w, ptr(0))) {                 // 只纠正本地玩家的武器
        diagByKey('not_mine', 'fireBtnPressed=1 但不是本地玩家的武器', 2);
        return false;
      }
      w.add(0x78).writeU8(0);
      st.stormClears++;
      if (st.stormClears <= 8 || st.stormClears % 25 === 0) {
        sendDiag('已撤销 fireBtnPressed #' + st.stormClears + '（weapon=' + w + '）');
      }
      return true;
    } catch (e) { return false; }
  }

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

      st.isNanoGhostFn = new NativeFunction(
        m.base.add(RVA.Player_get_isNanoGhost),
        'bool',
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
      // P1：32 位 IL2CPP 字符串是 length@0x08 / chars@0x0C（原来按 64 位布局读，永远读不到内容）
      var len = p.add(0x08).readS32();
      if (len <= 0 || len > 256) return '';
      return p.add(0x0C).readUtf16String(len) || '';
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

  function isLocalPlayerNanoGhost(w) {
    if (!w || w.isNull()) return false;
    if (!initNative()) return false;

    var owner = rp(w.add(OFF.owner));
    if (!owner || owner.isNull()) return false;

    try {
      return st.isNanoGhostFn(owner, ptr(0)) ? true : false;
    } catch (e) {
      st.lastError = '判断生化幽灵身份失败：' + e.message;
      return false;
    }
  }

  // ===== 生化幽灵硬门控 =====
  // 需求：开了本功能后，如果本地玩家是生化幽灵，则完全不生效（幽灵状态下改写攻击/动画状态会出 bug）。
  var ghostStateCache = { value: false, at: 0 };

  function getMyPlayerPtr() {
    try {
      var m = getModule();
      if (!m) return null;
      var typeInfo = m.base.add(RVA.GameManager_TypeInfo).readPointer();
      if (!typeInfo || typeInfo.isNull()) return null;
      var staticFields = typeInfo.add(0x5C).readPointer();
      if (!staticFields || staticFields.isNull()) return null;
      var p = staticFields.add(0x0).readPointer();
      return (p && !p.isNull()) ? p : null;
    } catch (e) { return null; }
  }

  // 玩家维度判定：不依赖武器 owner，任何 hook 里都能用
  function isGhostLocalPlayer() {
    try {
      if (!initNative()) return false;
      var p = getMyPlayerPtr();
      if (!p) return false;
      return st.isNanoGhostFn(p, ptr(0)) ? true : false;
    } catch (e) {
      st.lastError = '判断生化幽灵身份失败：' + e.message;
      return false;
    }
  }

  function isGhostLocalPlayerCached() {
    var now = nowMs();
    if (now - ghostStateCache.at > 200) {
      ghostStateCache.value = isGhostLocalPlayer();
      ghostStateCache.at = now;
    }
    return ghostStateCache.value;
  }

  // ===== 武器指针 / 对象池复用防护 =====
  // Weapon 是对象池对象：变身时游戏会把旧武器全部回收（NanoRoleExpand.ShouldRemoveAllWpn），
  // 新武器很可能复用同一块内存。WPN_Gun.OnKnifeAttackExit 只有一句 w+0x11C = 0，
  // 而 WPN_Knife / WPN_*Terminator 的对象只到 ~0x110，对刀调用它会越界写。
  // 所以“还锁 / 调用游戏函数”之前必须核对 klass（对象池复用后 klass 会变成别的武器类）。
  function weaponKlassPtr(w) {
    try { return (w && !w.isNull()) ? w.readPointer() : null; } catch (e) { return null; }
  }

  function sameWeaponIdentity(w, klass) {
    if (!w || w.isNull() || !klass) return false;
    var k = weaponKlassPtr(w);
    return !!k && k.equals(klass);
  }

  // 把我们写进去的枪托锁还回去（直接写 0，与 WPN_Gun.OnKnifeAttackExit 等价，且不需要游戏线程）
  function releaseGuardLock(reason) {
    var w = st.lockedWeapon;
    var klass = st.lockedKlass;
    st.lockedWeapon = null;
    st.lockedKlass = null;
    st.lockedAtMs = 0;
    if (!w || w.isNull()) return false;
    try {
      if (!sameWeaponIdentity(w, klass) || !isWeaponStillOurs(w, klass)) {
        log('警告', '清锁', reason + '：武器已销毁或已被对象池复用（类型不符），跳过');
        return false;
      }
      if (wi(w.add(OFF.knifeAttackAnim), 0)) {
        log('信息', '清锁', reason + '：已还原 knifeAttackAnim=0');
        return true;
      }
      return false;
    } catch (e) {
      st.lastError = '清除枪托锁失败：' + e.message;
      return false;
    }
  }

  // 幽灵状态：放弃当前状态，但必须先把我们写进武器的锁还回去，否则该武器会永久无法枪托
  function blockGhostAttack(reason) {
    st.ghostSkips++;
    if (st.ghostSkips <= 3) {
      log('信息', '身份', '本地玩家为生化幽灵，极速枪托不生效（' + reason + '）');
    }
    releaseGuardLock('幽灵门控/' + reason);
    st.pendingForceUnlock = false;
    st.pendingForceClear = false;
    st.current = null;
    return true;
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
    if (ok) {
      if (value !== 0) {
        st.lockedWeapon = w;
        st.lockedKlass = weaponKlassPtr(w);
        st.lockedAtMs = nowMs();
      }
      log('信息', '状态锁', reason + '：knifeAttackAnim=' + value);
    }
    return ok;
  }

  function clearTimer(id) {
    try { if (id) clearTimeout(id); } catch (e) {}
  }

  // 关闭/重开都不带上一轮状态：只动 JS 状态，不调用任何游戏函数
  function resetRuntime(reason) {
    if (st.current && st.current.maxTimer) clearTimer(st.current.maxTimer);
    st.current = null;
    st.pendingForceUnlock = false;
    st.pendingForceClear = false;
    st.pendingRoleClear = false;
    st.observeWeaponKey = '';
    st.observeSeq = 0;
    st.observeUntilMs = 0;
    st.lastRole = -1;
    st.logCounter = {};
    ghostStateCache.value = false;
    ghostStateCache.at = 0;
    if (reason) log('信息', '状态', '运行态已重置：' + reason);
  }

  function detachHooks() {
    for (var i = 0; i < st.hooks.length; i++) {
      try { st.hooks[i].detach(); } catch (e) {}
    }
    st.hooks = [];
    st.installed = false;
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
      klass: weaponKlassPtr(w),
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
        // P0：定时器运行在 Frida JS 线程，不能直接调游戏函数（OnKnifeAttackExit）；只置标志，由主线程钩子执行
        st.pendingForceUnlock = true;
      }
    }, CFG.maxGuardMs);

  }

  function isWeaponStillOurs(w, expectKlass) {
    try {
      if (!w || w.isNull() || !st.isMyWeaponFn) return false;
      // P1：Weapon 是对象池对象，可能已被回收；m_CachedPtr(+0x8) 为 0 说明 native 侧已销毁
      var cached = w.add(0x8).readPointer();
      if (!cached || cached.isNull()) return false;
      // 对象池复用防护：复用后 klass 变成别的武器类（例如枪 -> 终结者的刀），
      // 此时绝不能对它调用 WPN_Gun.OnKnifeAttackExit（会越界写 w+0x11C）
      if (expectKlass && !sameWeaponIdentity(w, expectKlass)) return false;
      return !!st.isMyWeaponFn(w, ptr(0));
    } catch (e) { return false; }
  }

  function unlockAttack(atk, reason) {
    if (!atk || atk.unlocked) return;

    atk.unlocked = true;
    atk.phase = '已解锁';

    clearTimer(atk.maxTimer);

    if (CFG.callExitOnUnlock && initNative()) {
      try {
        // P1：只在武器仍属于本地玩家且未销毁时才调游戏函数，避免对已回收对象写动画/攻击状态
        if (!isWeaponStillOurs(atk.weapon, atk.klass)) {
          log('警告', '解锁', reason + '：武器已失效/已不属于本地玩家/已被对象池复用，跳过 OnKnifeAttackExit，seq=' + atk.seq);
        } else {
          st.manualCallingExit = true;
          st.onKnifeAttackExitFn(atk.weapon, ptr(0));
          log('信息', '解锁', reason + '：已调用 OnKnifeAttackExit，seq=' + atk.seq);
        }
      } catch (e) {
        st.lastError = '调用 OnKnifeAttackExit 失败：' + e.message;
        log('警告', '解锁', st.lastError);
      } finally {
        st.manualCallingExit = false;
      }
    }

    // 锁已被游戏函数清零，清掉跟踪
    if (st.lockedWeapon && atk.weapon && !atk.weapon.isNull() && st.lockedWeapon.equals(atk.weapon)) {
      st.lockedWeapon = null;
      st.lockedKlass = null;
      st.lockedAtMs = 0;
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
    // P0：本函数可能被 RPC 线程调用，只置标志，真正的解锁在主线程钩子里执行
    if (!st.enabled) {
      // 关闭状态下没有需要恢复的攻击状态：只清 JS 残留，不调游戏函数，也不留挂起动作
      st.current = null;
      st.pendingForceUnlock = false;
      st.pendingForceClear = false;
      return true;
    }
    st.pendingForceClear = true;
    return true;
  }

  function installHooks() {
    if (st.installed) return true;

    var m = getModule();
    if (!m) return false;
    if (!initNative()) return false;

    try {
      st.hooks.push(Interceptor.attach(m.base.add(RVA.ModeBase_Update), {
        onEnter: function () {
          try {
            // 关闭后完全不介入：不跑看门狗、不处理挂起、不跑幽灵门控（规范 §12.2：保留 Hook 必须判断 enabled）
            if (!st.enabled) return;

            // 1) 看门狗：我们写进去的锁最多持有 lockWatchdogMs，超时无条件还原（先于身份判断）
            if (st.lockedWeapon && (nowMs() - st.lockedAtMs) > CFG.lockWatchdogMs) {
              releaseGuardLock('看门狗超时');
            }

            // 2) 角色变化（变幽灵/终结者/复活）：先把锁还回去
            if (st.pendingRoleClear) {
              st.pendingRoleClear = false;
              releaseGuardLock('角色变化');
              st.pendingForceUnlock = false;
              st.pendingForceClear = false;
              st.current = null;
            }

            // 3) 挂起请求：必须无条件先处理，否则锁会永久留在武器上
            if (st.pendingForceClear || st.pendingForceUnlock) {
              var reason = st.pendingForceClear ? '手动强制恢复' : '最大保护窗口';
              st.pendingForceClear = false;
              st.pendingForceUnlock = false;
              if (isGhostLocalPlayerCached()) {
                releaseGuardLock(reason + '(幽灵)');
                st.current = null;
              } else if (st.current) {
                unlockAttack(st.current, reason);
              } else {
                releaseGuardLock(reason);
              }
            }

            // 4) 幽灵：只拦新攻击，不再跳过清理
            if (isGhostLocalPlayerCached()) blockGhostAttack('ModeBase.Update');
          } catch (e) {
            st.lastError = 'ModeBase.Update 解锁异常：' + e.message;
          }
        }
      }));

      // 变身（人类 <-> 幽灵 <-> 终结者）监听：角色一变就丢状态并把锁还回去
      st.hooks.push(Interceptor.attach(m.base.add(RVA.Player_set_nanoRole), {
        onEnter: function (args) {
          try {
            if (!st.enabled) return;
            var p = args[0];
            if (!p || p.isNull()) return;
            var my = getMyPlayerPtr();
            if (!my || !p.equals(my)) return;
            var role = 0;
            try { role = args[1].toInt32(); } catch (e) {}
            if (st.lastRole === role) return;
            st.lastRole = role;
            st.pendingRoleClear = true;
          } catch (e) {
            st.lastError = 'set_nanoRole 钩子异常：' + e.message;
          }
        }
      }));

      // 兜底：游戏置位 fireBtnPressed 时，等本体写完（onLeave）再核对 OS 物理按键；已经松开就直接撤销
      st.hooks.push(Interceptor.attach(m.base.add(RVA.Weapon_OnFireBtnPressed), {
        onEnter: function (args) {
          this.w = args[0];                 // 参数只能在 onEnter 取；判断/写回放到 onLeave
        },
        onLeave: function () {
          try {
            if (!st.enabled) return;
            clearStuckFireBtn(this.w);
          } catch (e) {}
        }
      }));

      // 只观测、不改游戏状态：量出"物理左键已松开、游戏还在播近战攻击动画"的次数，并记下调用者。
      // WPN_Knife.PlayKnifeAttackAnim(weapon, combo) @0xB642B0 是近战连招的唯一入口。
      st.hooks.push(Interceptor.attach(m.base.add(0xB642B0), {
        onEnter: function (args) {
          try {
            if (!st.enabled) return;
            var w = args[0];
            if (!w || w.isNull() || !st.isMyWeaponFn) return;
            if (!st.isMyWeaponFn(w, ptr(0))) return;       // 只看本地玩家的武器
            var combo = args[1].toInt32();
            // combo3 = 重击（右键/OnSpecialBtnDown）；combo1/2 = 轻击连招（左键）。
            // 上一轮这里用左键判 combo3，把"正常重击"误报成异常，必须按 combo 配对按键。
            var expectDown = (combo >= 3) ? physicalRightDown() : physicalLeftDown();
            var keyName = (combo >= 3) ? '物理右键' : '物理左键';
            st.combo3Seen = st.combo3Seen || 0;
            if (combo >= 3 && st.combo3Seen < 6) {
              st.combo3Seen++;
              sendDiag('combo=' + combo + ' 由 ' + callerOf(this.returnAddress) + ' 触发（weapon=' + w
                + '，fireBtn=' + w.add(0x78).readU8() + '，' + keyName + '=' + keyStateText(expectDown) + '）');
            }
            if (expectDown !== false) return;              // 对应的键真的按着 / 读不到 -> 正常
            st.animWhileUp = (st.animWhileUp || 0) + 1;
            if (st.animWhileUp <= 8) {
              sendDiag('异常：' + keyName + '已松开，游戏仍在播放近战攻击动画 combo=' + combo
                + '，调用者=' + callerOf(this.returnAddress) + '（weapon=' + w + '，fireBtn=' + w.add(0x78).readU8() + '）');
            }
          } catch (e) {}
        }
      }));

      st.hooks.push(Interceptor.attach(m.base.add(RVA.OnSpecialBtnDown), {
        onEnter: function (args) {
          try {
            if (!st.enabled) return;

            // 生化幽灵硬门控：放在最前面，不依赖武器判定
            if (isGhostLocalPlayer() || isGhostLocalPlayerCached()) {
              blockGhostAttack('OnSpecialBtnDown');
              return;
            }

            var w = args[0];

            if (!isLocalWeapon(w)) {
              st.nonLocalSkips++;
              return;
            }

            if (isLocalPlayerNanoGhost(w)) {
              blockGhostAttack('OnSpecialBtnDown.owner');
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
          this.local = st.enabled && !isGhostLocalPlayerCached() && isLocalWeapon(this.weapon);
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
            if (isGhostLocalPlayerCached()) { blockGhostAttack('OnKnifeAttackExit'); return; }

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
            if (isGhostLocalPlayerCached()) { blockGhostAttack('OnAnimationExit'); return; }

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
      // P1：部分安装失败时回滚已挂的 listener，避免再次 enable 时重复 attach
      detachHooks();
      return false;
    }
  }

  function enable() {
    if (st.enabled) return true;

    // 上一次开关残留的运行态不能带进本轮（否则第一下右键会被当成"上一击未结束"）
    resetRuntime('enable');

    if (!installHooks()) {
      st.enabled = false;
      return false;
    }

    st.enabled = true;

    // 自检：把左键读取链的结果写进日志（下次排查一眼看出链路有没有断）
    diag.total = 0;
    diag.keyed = {};
    st.animWhileUp = 0;
    var osProbe = readOsMouseLeft();
    sendDiag('左键读取链自检: GetAsyncKeyState=' + (osProbe.ok ? (osProbe.down ? 'down' : 'up') : ('FAIL(' + osProbe.reason + ')')));

    log('成功', '状态',
      '极速枪托 v3.2 已开启：仅在原始伤害事件完成后解锁；异常保护=' + CFG.maxGuardMs + 'ms'
    );
    sendStatus('fast_gunstock', true);
    return true;
  }

  function disable() {
    st.enabled = false;

    // 只归还"我们自己写进去的锁"（同步、只写 knifeAttackAnim=0，与 WPN_Gun.OnKnifeAttackExit 等价）
    releaseGuardLock('功能关闭');

    // 关键：不再挂 pendingForceClear。关闭后绝不补调 OnKnifeAttackExit ——
    // 那一下正是本功能的加速动作（提前解锁），会变成"关闭后仍然生效一次"。
    // 没打完的这一击交回游戏自己的动画退出回调（OnAnimationExit -> OnKnifeAttackExit）清理，
    // 与从未开过本功能时完全一致。
    resetRuntime('disable');

    log('信息', '状态', '极速枪托 v3.2 已关闭');
    sendStatus('fast_gunstock', false);
    return true;
  }

  function cleanup() {
    st.enabled = false;
    releaseGuardLock('cleanup');
    resetRuntime('cleanup');
    detachHooks();
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
      locked: st.lockedWeapon ? weaponKey(st.lockedWeapon) : '',
      lastRole: st.lastRole,
      stormClears: st.stormClears,
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
      ghostSkips: st.ghostSkips,
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
