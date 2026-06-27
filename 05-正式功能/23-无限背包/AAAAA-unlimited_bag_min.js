// ============================================================
// AAAAA-unlimited_bag_min.js - 23 无限背包最小实现
//
// 目标：
//   任何位置、尽量任何状态下都能切换背包武器。
//
// 原理：
//   不替换 Player.SelectWeaponBag，不自己发武器。
//   只在原函数执行前清掉 WeaponBag.disabled 和 tooFarFromSpawnPos，
//   然后继续走游戏自己的 SelectWeaponBag -> GiveWeaponByBag 流程。
//
// 已确认关键点：
//   Player.SelectWeaponBag      RVA 0xB52830
//   HUD_Bag.Update              RVA 0xB00360
//   ObscuredBool.Encrypt        RVA 0x7F93D0
//   Player.weaponBag            offset 0xA4
//   WeaponBag.disabled          offset 0x8
//   WeaponBag.tooFarFromSpawnPos offset 0x14
//   HUD_Bag.bag                 offset 0x2C
// ============================================================

(function() {
  'use strict';

  var CALL_CONV = 'mscdecl';
  var MAX_LOGS_PER_MODULE = 80;
  var moduleLogCounts = {};

  var RVA = {
    SelectWeaponBag: 0xB52830,
    HudBagUpdate: 0xB00360,
    ObscuredBoolEncrypt: 0x7F93D0
  };

  var OFF = {
    Player_weaponBag: 0xA4,
    WeaponBag_disabled: 0x8,
    WeaponBag_tooFarFromSpawnPos: 0x14,
    HudBag_bag: 0x2C,

    ObscuredBool_currentCryptoKey: 0x0,
    ObscuredBool_hiddenValue: 0x4,
    ObscuredBool_inited: 0x8,
    ObscuredBool_fakeValue: 0x9,
    ObscuredBool_fakeValueActive: 0xA
  };

  var state = {
    enabled: false,
    initialized: false,
    selectHook: null,
    hudUpdateHook: null,
    encryptBool: null,
    selectHits: 0,
    hudHits: 0,
    patchedCount: 0,
    lastError: null
  };

  var _gameAssembly = null;

  function log(level, module, message) {
    if (!moduleLogCounts[module]) moduleLogCounts[module] = 0;
    if (moduleLogCounts[module] >= MAX_LOGS_PER_MODULE) return;
    moduleLogCounts[module]++;

    var fullMsg = '[无限背包][' + module + '] ' + message;
    console.log('[' + level + '] ' + fullMsg);
    try {
      send({ type: 'log', level: level, module: '无限背包/' + module, message: message });
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

  function readU8(addr, fallbackValue) {
    try {
      if (!addr || addr.isNull()) return fallbackValue;
      return addr.readU8();
    } catch(e) {
      return fallbackValue;
    }
  }

  function writeU8(addr, value) {
    try {
      if (!addr || addr.isNull()) return false;
      addr.writeU8(value);
      return true;
    } catch(e) {
      return false;
    }
  }

  function writeS32(addr, value) {
    try {
      if (!addr || addr.isNull()) return false;
      addr.writeS32(value);
      return true;
    } catch(e) {
      return false;
    }
  }

  function initNativeFunctions() {
    if (state.initialized) return true;

    var mod = getGameAssembly();
    if (!mod) return false;

    try {
      state.encryptBool = new NativeFunction(
        mod.base.add(RVA.ObscuredBoolEncrypt),
        'int',
        ['int', 'uint8', 'pointer'],
        CALL_CONV
      );
      state.initialized = true;
      log('success', 'INIT', 'ObscuredBool.Encrypt 初始化成功');
      return true;
    } catch(e) {
      state.lastError = 'ObscuredBool.Encrypt 初始化失败: ' + e.message;
      log('error', 'INIT', state.lastError);
      return false;
    }
  }

  function writeObscuredBoolFalse(fieldAddr) {
    if (!fieldAddr || fieldAddr.isNull()) return false;
    if (!initNativeFunctions()) return false;

    try {
      var key = readU8(fieldAddr.add(OFF.ObscuredBool_currentCryptoKey), 0);
      var encrypted = state.encryptBool(0, key, ptr(0));

      var ok = true;
      ok = writeS32(fieldAddr.add(OFF.ObscuredBool_hiddenValue), encrypted) && ok;
      ok = writeU8(fieldAddr.add(OFF.ObscuredBool_inited), 1) && ok;
      ok = writeU8(fieldAddr.add(OFF.ObscuredBool_fakeValue), 0) && ok;
      ok = writeU8(fieldAddr.add(OFF.ObscuredBool_fakeValueActive), 0) && ok;

      return ok;
    } catch(e) {
      state.lastError = '写 ObscuredBool=false 失败: ' + e.message;
      log('error', 'PATCH', state.lastError);
      return false;
    }
  }

  function clearWeaponBagLimits(weaponBag, source, verbose) {
    if (!weaponBag || weaponBag.isNull()) return false;

    var disabledAddr = weaponBag.add(OFF.WeaponBag_disabled);
    var tooFarAddr = weaponBag.add(OFF.WeaponBag_tooFarFromSpawnPos);

    var disabledOk = writeObscuredBoolFalse(disabledAddr);
    var tooFarOk = writeObscuredBoolFalse(tooFarAddr);

    if (disabledOk || tooFarOk) {
      state.patchedCount++;
      if (verbose) {
        log(
          'success',
          'PATCH',
          source + ' bag=' + weaponBag + ' disabled=false tooFar=false'
        );
      }
      return true;
    }

    if (verbose) {
      log('warn', 'PATCH', source + ' bag=' + weaponBag + ' 清限制失败');
    }
    return false;
  }

  function installSelectWeaponBagHook(mod) {
    if (state.selectHook) return true;

    try {
      var hookAddr = mod.base.add(RVA.SelectWeaponBag);
      state.selectHook = Interceptor.attach(hookAddr, {
        onEnter: function(args) {
          if (!state.enabled) return;

          state.selectHits++;
          this._ubPlayer = args[0];
          this._ubIndex = args[1].toInt32();
          this._ubBag = readPtr(this._ubPlayer.add(OFF.Player_weaponBag));

          if (!this._ubBag) {
            log('warn', 'BAG', 'SelectWeaponBag player=' + this._ubPlayer + ' weaponBag=null');
            return;
          }

          var verbose = state.selectHits <= 20 || state.selectHits % 50 === 0;
          clearWeaponBagLimits(this._ubBag, 'SelectWeaponBag index=' + this._ubIndex, verbose);
        },
        onLeave: function(retval) {
          if (!state.enabled) return;

          var result = retval.toInt32() !== 0;
          if (!result) {
            log(
              'warn',
              'RESULT',
              'SelectWeaponBag index=' + this._ubIndex + ' return=false，可能还有 available/UI/射击状态限制'
            );
          } else if (state.selectHits <= 20 || state.selectHits % 50 === 0) {
            log('success', 'RESULT', 'SelectWeaponBag index=' + this._ubIndex + ' return=true');
          }
        }
      });

      log('success', 'HOOK', 'Player.SelectWeaponBag installed at ' + hookAddr);
      return true;
    } catch(e) {
      state.lastError = 'Player.SelectWeaponBag Hook 安装失败: ' + e.message;
      log('error', 'HOOK', state.lastError);
      return false;
    }
  }

  function installHudBagUpdateHook(mod) {
    if (state.hudUpdateHook) return true;

    try {
      var hookAddr = mod.base.add(RVA.HudBagUpdate);
      state.hudUpdateHook = Interceptor.attach(hookAddr, {
        onEnter: function(args) {
          if (!state.enabled) return;

          state.hudHits++;
          var hudBag = args[0];
          var weaponBag = readPtr(hudBag.add(OFF.HudBag_bag));
          if (!weaponBag) return;

          var verbose = state.hudHits <= 5 || state.hudHits % 600 === 0;
          clearWeaponBagLimits(weaponBag, 'HUD_Bag.Update', verbose);
        }
      });

      log('success', 'HOOK', 'HUD_Bag.Update installed at ' + hookAddr);
      return true;
    } catch(e) {
      state.lastError = 'HUD_Bag.Update Hook 安装失败: ' + e.message;
      log('error', 'HOOK', state.lastError);
      return false;
    }
  }

  function installHooks() {
    var mod = getGameAssembly();
    if (!mod) return false;
    if (!initNativeFunctions()) return false;

    var selectOk = installSelectWeaponBagHook(mod);
    var hudOk = installHudBagUpdateHook(mod);
    return selectOk && hudOk;
  }

  function enable() {
    try {
      if (!installHooks()) {
        state.enabled = false;
        return false;
      }

      state.enabled = true;
      log('success', 'STATE', '无限背包已开启');
      return true;
    } catch(e) {
      state.enabled = false;
      state.lastError = '开启失败: ' + e.message;
      log('error', 'STATE', state.lastError);
      return false;
    }
  }

  function disable() {
    state.enabled = false;
    log('info', 'STATE', '无限背包已关闭（不主动恢复背包字段）');
    return true;
  }

  function cleanup() {
    disable();

    try {
      if (state.selectHook) {
        state.selectHook.detach();
        state.selectHook = null;
      }
      if (state.hudUpdateHook) {
        state.hudUpdateHook.detach();
        state.hudUpdateHook = null;
      }

      log('success', 'STATE', 'Hook 已清理');
      return true;
    } catch(e) {
      state.lastError = '清理 Hook 失败: ' + e.message;
      log('error', 'STATE', state.lastError);
      return false;
    }
  }

  function status() {
    return {
      enabled: state.enabled,
      initialized: state.initialized,
      selectHookInstalled: !!state.selectHook,
      hudUpdateHookInstalled: !!state.hudUpdateHook,
      selectHits: state.selectHits,
      hudHits: state.hudHits,
      patchedCount: state.patchedCount,
      lastError: state.lastError
    };
  }

  rpc.exports = {
    enable: enable,
    disable: disable,
    status: status,
    cleanup: cleanup
  };

  log('success', 'INIT', '无限背包最小脚本已加载');
  log('info', 'INIT', '调用 enable() 后生效；原理是清 WeaponBag.disabled / tooFarFromSpawnPos');

})();
