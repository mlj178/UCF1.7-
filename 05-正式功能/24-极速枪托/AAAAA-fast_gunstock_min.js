// ============================================================
// AAAAA-fast_gunstock_min.js - 24 极速枪托最小实现
//
// 目标：
//   加快部分主武器/副武器的右键枪托攻击。
//
// 已定位：
//   “枪托”就是 WPN_Gun 里的右键近战攻击。
//   它使用 WeaponData_Gun.knifeAttacks，不是普通刀，也不是左键开火。
//
// 最小实现：
//   1. Hook WPN_Gun.OnSpecialBtnDown。
//   2. 只处理本地玩家武器。
//   3. 设置角色/手部 Animator speed，加快枪托动作。
//   4. 记录 WPN_Gun.KnifeAttackEvent，但不改变伤害和解锁流程。
//   5. 等原游戏 WPN_Gun.OnAnimationExit(tag=knifeAttack) 结束后，只恢复 Animator speed。
//   6. 不 replace 原函数，不重写伤害，不改普通射击。
// ============================================================

(function() {
  'use strict';

  var CALL_CONV = 'mscdecl';
  var MAX_LOGS_PER_MODULE = 100;
  var moduleLogCounts = {};

  var RVA = {
    WpnGunOnSpecialBtnDown: 0xB629F0,
    WpnGunGetKnifeAttackData: 0xB61F90,
    WpnGunKnifeAttackEvent: 0xB62730,
    WpnGunOnAnimationExit: 0xB62800,
    WeaponGetIsMyWeapon: 0xB6E1D0,
    CFAnimatorGetCharacterAnimator: 0xB35310,
    CFAnimatorGetHandAnimator: 0xB35330,
    AnimatorSetSpeed: 0xAA8C30
  };

  var OFF = {
    WpnGun_realData: 0xEC,
    WeaponDataGun_knifeAttacks: 0x180,
    WpnGun_knifeAttackCount: 0x118,
    WpnGun_knifeAttackAnim: 0x11C
  };

  var state = {
    enabled: false,
    initialized: false,
    multiplier: 4.0,
    hooksInstalled: false,
    onSpecialHook: null,
    getAttackDataHook: null,
    knifeEventHook: null,
    onAnimationExitHook: null,
    isMyWeaponFn: null,
    getCharacterAnimatorFn: null,
    getHandAnimatorFn: null,
    setAnimatorSpeedFn: null,
    specialHits: 0,
    attackDataHits: 0,
    damageEventHits: 0,
    knifeExitHits: 0,
    speedSetCount: 0,
    skippedNoGunstock: 0,
    skippedLocked: 0,
    lastError: null
  };

  var activeGunstockWeapons = {};
  var _gameAssembly = null;

  function log(level, module, message) {
    if (!moduleLogCounts[module]) moduleLogCounts[module] = 0;
    if (moduleLogCounts[module] >= MAX_LOGS_PER_MODULE) return;
    moduleLogCounts[module]++;

    var fullMsg = '[极速枪托][' + module + '] ' + message;
    console.log('[' + level + '] ' + fullMsg);
    try {
      send({ type: 'log', level: level, module: '极速枪托/' + module, message: message });
    } catch(e) {}
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
    } catch(e) {
      state.lastError = '获取 GameAssembly.dll 失败: ' + e.message;
      log('error', 'INIT', state.lastError);
      return null;
    }
  }

  function readPtr(addr) {
    try {
      if (!addr || addr.isNull()) return null;
      var value = addr.readPointer();
      return value && !value.isNull() ? value : null;
    } catch(e) {
      return null;
    }
  }

  function readS32(addr, fallbackValue) {
    try {
      if (!addr || addr.isNull()) return fallbackValue;
      return addr.readS32();
    } catch(e) {
      return fallbackValue;
    }
  }

  function readIl2CppString(str) {
    try {
      if (!str || str.isNull()) return '';
      var length = str.add(0x08).readS32();
      if (length <= 0 || length > 256) return '';
      return str.add(0x0C).readUtf16String(length);
    } catch(e) {
      return '';
    }
  }

  function initNativeFunctions() {
    if (state.initialized) return true;

    var mod = getGameAssembly();
    if (!mod) return false;

    try {
      state.isMyWeaponFn = new NativeFunction(
        mod.base.add(RVA.WeaponGetIsMyWeapon),
        'bool',
        ['pointer', 'pointer'],
        CALL_CONV
      );
      state.getCharacterAnimatorFn = new NativeFunction(
        mod.base.add(RVA.CFAnimatorGetCharacterAnimator),
        'pointer',
        ['pointer', 'pointer'],
        CALL_CONV
      );
      state.getHandAnimatorFn = new NativeFunction(
        mod.base.add(RVA.CFAnimatorGetHandAnimator),
        'pointer',
        ['pointer', 'pointer'],
        CALL_CONV
      );
      state.setAnimatorSpeedFn = new NativeFunction(
        mod.base.add(RVA.AnimatorSetSpeed),
        'void',
        ['pointer', 'float', 'pointer'],
        CALL_CONV
      );

      state.initialized = true;
      log('success', 'INIT', 'NativeFunction 初始化成功');
      return true;
    } catch(e) {
      state.lastError = 'NativeFunction 初始化失败: ' + e.message;
      log('error', 'INIT', state.lastError);
      return false;
    }
  }

  function isLocalWeapon(weapon) {
    if (!weapon || weapon.isNull()) return false;
    if (!initNativeFunctions()) return false;

    try {
      return state.isMyWeaponFn(weapon, ptr(0)) ? true : false;
    } catch(e) {
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

  function setAnimatorSpeed(animator, speed, source, verbose) {
    if (!animator || animator.isNull()) return false;
    if (!initNativeFunctions()) return false;

    try {
      state.setAnimatorSpeedFn(animator, speed, ptr(0));
      state.speedSetCount++;
      if (verbose) {
        log('success', 'ANIM', source + ' animator=' + animator + ' speed=' + speed);
      }
      return true;
    } catch(e) {
      state.lastError = '设置 Animator speed 失败: ' + e.message;
      log('warn', 'ANIM', state.lastError);
      return false;
    }
  }

  function speedUpGunstockAnimators(weapon, source, verbose) {
    if (!weapon || weapon.isNull()) return false;
    if (!initNativeFunctions()) return false;

    var any = false;
    try {
      var characterAnimator = state.getCharacterAnimatorFn(weapon, ptr(0));
      any = setAnimatorSpeed(characterAnimator, state.multiplier, source + '/character', verbose) || any;
    } catch(e) {
      log('warn', 'ANIM', '设置角色 Animator 失败: ' + e.message);
    }

    try {
      var handAnimator = state.getHandAnimatorFn(weapon, ptr(0));
      any = setAnimatorSpeed(handAnimator, state.multiplier, source + '/hand', verbose) || any;
    } catch(e2) {
      log('warn', 'ANIM', '设置手部 Animator 失败: ' + e2.message);
    }

    return any;
  }

  function restoreGunstockAnimators(weapon, source, verbose) {
    if (!weapon || weapon.isNull()) return false;
    if (!initNativeFunctions()) return false;

    var any = false;
    try {
      var characterAnimator = state.getCharacterAnimatorFn(weapon, ptr(0));
      any = setAnimatorSpeed(characterAnimator, 1.0, source + '/character', verbose) || any;
    } catch(e) {
      log('warn', 'ANIM', 'restore character Animator failed: ' + e.message);
    }

    try {
      var handAnimator = state.getHandAnimatorFn(weapon, ptr(0));
      any = setAnimatorSpeed(handAnimator, 1.0, source + '/hand', verbose) || any;
    } catch(e2) {
      log('warn', 'ANIM', 'restore hand Animator failed: ' + e2.message);
    }

    return any;
  }

  function rememberActiveWeapon(weapon) {
    try {
      activeGunstockWeapons[weapon.toString()] = weapon;
    } catch(e) {}
  }

  function isRememberedActiveWeapon(weapon) {
    try {
      return !!activeGunstockWeapons[weapon.toString()];
    } catch(e) {
      return false;
    }
  }

  function forgetActiveWeapon(weapon) {
    try {
      delete activeGunstockWeapons[weapon.toString()];
    } catch(e) {}
  }

  function restoreAllActiveGunstockAnimators(source) {
    try {
      for (var key in activeGunstockWeapons) {
        if (!activeGunstockWeapons.hasOwnProperty(key)) continue;
        var weapon = activeGunstockWeapons[key];
        restoreGunstockAnimators(weapon, source, false);
      }
      activeGunstockWeapons = {};
    } catch(e) {
      log('warn', 'ANIM', 'restore active gunstock animators failed: ' + e.message);
    }
  }

  function installHooks() {
    if (state.hooksInstalled) return true;

    var mod = getGameAssembly();
    if (!mod) return false;
    if (!initNativeFunctions()) return false;

    try {
      state.onSpecialHook = Interceptor.attach(mod.base.add(RVA.WpnGunOnSpecialBtnDown), {
        onEnter: function(args) {
          if (!state.enabled) return;

          this.weapon = args[0];
          this.local = false;
          this.hasGunstock = false;

          if (!isLocalWeapon(this.weapon)) return;
          this.local = true;

          if (!hasGunstockAttacks(this.weapon)) {
            state.skippedNoGunstock++;
            return;
          }
          this.hasGunstock = true;

          var lockValue = readS32(this.weapon.add(OFF.WpnGun_knifeAttackAnim), 0);
          if (lockValue !== 0) {
            state.skippedLocked++;
            return;
          }

          state.specialHits++;
          rememberActiveWeapon(this.weapon);

          var verbose = state.specialHits <= 20 || state.specialHits % 50 === 0;
          speedUpGunstockAnimators(this.weapon, 'OnSpecialBtnDown.onEnter', verbose);
        }
      });

      state.getAttackDataHook = Interceptor.attach(mod.base.add(RVA.WpnGunGetKnifeAttackData), {
        onEnter: function(args) {
          if (!state.enabled) return;

          this.weapon = args[1];
          this.attackIndex = args[2].toInt32();
          this.active = isRememberedActiveWeapon(this.weapon);

          if (this.active) {
            state.attackDataHits++;
            if (state.attackDataHits <= 20 || state.attackDataHits % 50 === 0) {
              log('info', 'DATA', 'GetKnifeAttackData weapon=' + this.weapon + ' attackIndex=' + this.attackIndex);
            }
          }
        }
      });

      state.knifeEventHook = Interceptor.attach(mod.base.add(RVA.WpnGunKnifeAttackEvent), {
        onEnter: function(args) {
          if (!state.enabled) return;

          this.weapon = args[0];
          this.attackIndex = args[1].toInt32();
          this.active = isRememberedActiveWeapon(this.weapon);

          if (this.active) {
            state.damageEventHits++;
            if (state.damageEventHits <= 20 || state.damageEventHits % 50 === 0) {
              log('success', 'DAMAGE', 'KnifeAttackEvent weapon=' + this.weapon + ' attackIndex=' + this.attackIndex);
            }
          }
        }
      });

      state.onAnimationExitHook = Interceptor.attach(mod.base.add(RVA.WpnGunOnAnimationExit), {
        onEnter: function(args) {
          this.weapon = args[0];
          this.animTag = readIl2CppString(args[2]);
          this.active = this.animTag === 'knifeAttack' && isRememberedActiveWeapon(this.weapon);
          if (!this.active) return;

          state.knifeExitHits++;
          if (state.knifeExitHits <= 20 || state.knifeExitHits % 50 === 0) {
            log('info', 'EXIT', 'OnAnimationExit knifeAttack weapon=' + this.weapon);
          }
        },
        onLeave: function() {
          if (!this.active) return;

          var weapon = this.weapon;
          var verbose = state.knifeExitHits <= 20 || state.knifeExitHits % 50 === 0;
          restoreGunstockAnimators(weapon, 'OnAnimationExit.knifeAttack', verbose);
          forgetActiveWeapon(weapon);
        }
      });

      state.hooksInstalled = true;
      log('success', 'HOOK', 'WPN_Gun 枪托 Hook 已安装');
      return true;
    } catch(e) {
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
      log('success', 'STATE', '极速枪托已开启，倍率=' + state.multiplier);
      return true;
    } catch(e) {
      state.enabled = false;
      state.lastError = '开启失败: ' + e.message;
      log('error', 'STATE', state.lastError);
      return false;
    }
  }

  function disable() {
    restoreAllActiveGunstockAnimators('disable');
    state.enabled = false;
    log('info', 'STATE', '极速枪托已关闭');
    return true;
  }

  function cleanup() {
    disable();

    try {
      if (state.onSpecialHook) {
        state.onSpecialHook.detach();
        state.onSpecialHook = null;
      }
      if (state.getAttackDataHook) {
        state.getAttackDataHook.detach();
        state.getAttackDataHook = null;
      }
      if (state.knifeEventHook) {
        state.knifeEventHook.detach();
        state.knifeEventHook = null;
      }
      if (state.onAnimationExitHook) {
        state.onAnimationExitHook.detach();
        state.onAnimationExitHook = null;
      }

      state.hooksInstalled = false;
      activeGunstockWeapons = {};
      log('success', 'STATE', 'Hook 已清理');
      return true;
    } catch(e) {
      state.lastError = '清理失败: ' + e.message;
      log('error', 'STATE', state.lastError);
      return false;
    }
  }

  function setMultiplier(value) {
    var next = parseFloat(value);
    if (!(next >= 1.0 && next <= 30.0)) {
      log('warn', 'STATE', '倍率必须在 1 到 30 之间');
      return false;
    }

    state.multiplier = next;
    log('success', 'STATE', '倍率已设置为 ' + state.multiplier);
    return true;
  }

  function status() {
    return {
      enabled: state.enabled,
      initialized: state.initialized,
      hooksInstalled: state.hooksInstalled,
      multiplier: state.multiplier,
      specialHits: state.specialHits,
      attackDataHits: state.attackDataHits,
      damageEventHits: state.damageEventHits,
      knifeExitHits: state.knifeExitHits,
      speedSetCount: state.speedSetCount,
      skippedNoGunstock: state.skippedNoGunstock,
      skippedLocked: state.skippedLocked,
      rememberedWeapons: Object.keys(activeGunstockWeapons).length,
      lastError: state.lastError
    };
  }

  rpc.exports = {
    enable: enable,
    disable: disable,
    status: status,
    cleanup: cleanup,
    setmultiplier: setMultiplier
  };

  log('success', 'INIT', '极速枪托最小脚本已加载');
  log('info', 'INIT', '调用 enable() 后生效；只处理 WPN_Gun 右键枪托攻击');

})();
