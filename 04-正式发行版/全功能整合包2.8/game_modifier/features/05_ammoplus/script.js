// Local helpers for this feature only.
var modules = {};
var __localMaxLogsPerModule = 10;
var __localModuleLogCounts = {};

function sendRoutedLog(level, module, message, audience, devDetail) {
  try {
    if (!__localModuleLogCounts[module]) __localModuleLogCounts[module] = 0;
    if (__localModuleLogCounts[module] >= __localMaxLogsPerModule) return;
    if (module !== '??' && __localModuleLogCounts[module] === __localMaxLogsPerModule - 1) {
      __localModuleLogCounts[module]++;
      send({ type: 'log', level: 'info', module: module, message: message + ' (???????)', audience: audience || 'dev', dev_detail: devDetail || '' });
      return;
    }
    __localModuleLogCounts[module]++;
    send({ type: 'log', level: level, module: module, message: message, audience: audience || 'dev', dev_detail: devDetail || '' });
  } catch (_) {}
}

function sendUserLog(level, module, message) {
  sendRoutedLog(level, module, message, 'user', '');
}

function sendDevLog(level, module, message, devDetail) {
  sendRoutedLog(level, module, message, 'dev', devDetail || '');
}

function sendBothLog(level, module, message, devDetail) {
  sendRoutedLog(level, module, message, 'both', devDetail || '');
}

function sendLog(level, module, message) {
  sendDevLog(level, module, message);
}

function sendLogFile(level, module, message) {
  try { send({ type: 'log_file', level: level, module: module, message: message, audience: 'dev' }); } catch (_) {}
}

function sendStatus(feature, enabled) {
  try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (_) {}
}

var __localGameAssemblyCache = null;
var __localGameAssemblyLogged = false;

function getGameAssembly() {
  try {
    if (__localGameAssemblyCache) return __localGameAssemblyCache;
    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) {
      sendDevLog('error', '??', '??? GameAssembly.dll', 'GameAssembly.dll not found');
      return null;
    }
    __localGameAssemblyCache = mod;
    if (!__localGameAssemblyLogged) {
      __localGameAssemblyLogged = true;
      sendDevLog('info', '??', 'GameAssembly.dll: base=' + mod.base + ' size=' + mod.size, 'GameAssembly module located');
    }
    return mod;
  } catch (e) {
    sendDevLog('error', '??', '??????: ' + e.message, 'getGameAssembly failed: ' + e.message);
    return null;
  }
}

function readPtr(addr) {
  try { if (!addr || addr.isNull()) return null; var v = addr.readPointer(); return (v && !v.isNull()) ? v : null; } catch (_) { return null; }
}

function readI32(addr) { try { return addr ? addr.readS32() : null; } catch (_) { return null; } }
function readF32(addr) { try { return addr ? addr.readFloat() : null; } catch (_) { return null; } }
function readU8(addr) { try { return addr ? addr.readU8() : null; } catch (_) { return null; } }

var __localCleanupCallbacks = [];
function registerCleanup(callback) {
  if (typeof callback !== 'function') return false;
  __localCleanupCallbacks.push(callback);
  return true;
}

// reload_speed.js - 快速换弹（普通枪械=动画参数；榴弹模式 & RPG=动画器速度；倍率 1.0~5.0）
//
// 一、三种武器形态、两条实现路径
//   A) 普通枪械（WPN_Gun 系，含榴弹枪的步枪模式）
//        WPN_Gun.Reload(0xB62CB0) 每次都算
//          GetAnimSpeed(reloadAnimRatio) × PlayerWeapons.ReloadSpeed
//        再 CFAnimator.SetFloat("ReloadSpeed", v) → 播放 "reload" → 乘这个 v 即可。
//   B) 步枪的「榴弹模式」（WPN_GrenadeGun 的 changeMode 状态，CFAnimator+0x54）
//        换弹仍走 WPN_Gun.Reload，但 CFAnimator.AnimName_Modifier(WPN_GrenadeGun 版 0xB602D0)
//        会把动画名 "reload" 改写成 "reload_A"（后缀 StringLiteral 0x10E28EB8 = "_A"），
//        换弹状态变成另一条 clip，实测不吃 "ReloadSpeed" 参数 → 乘参数无效。
//        → 在 Reload 入口把武器/手部 Animator.speed 设为倍率，动画结束复位。
//   C) WPN_RPG（火箭筒 / AT4）
//        换弹入口是 WPN_RPG.OnReloadBtnDown(0xB67AF0)，只播放动画、从不写 "ReloadSpeed"。
//        → 同样改 Animator.speed。
//   注：WPN_RPG.Reload(0xB67C40) 没有被任何地方调用（死代码），不要挂钩子。
//
// 二、动画器速度方案的复位时机（缺一不可）
//   · 换弹动画结束：WPN_Gun.OnAnimationEnd(0xB627A0) tag=="reload" / WPN_RPG.OnAnimationEnd(0xB67640)
//   · 榴弹模式切换：WPN_GrenadeGun.OnSpecialBtnDown(0xB5FCF0)
//   · 重新部署：WPN_RPG.Deploy(0xB67030)；普通枪械由游戏 CFAnimator.AnimatorInit 每次部署置 1.0
//   · 关闭功能 / 5s 看门狗（换弹被打断时的兜底）
//
// 三、参数路径与动画器速度路径互斥：changeMode!=0 或 RPG 时不再乘 "ReloadSpeed"，
//     否则两种机制会叠成倍率平方。
//
// 四、关键地址（GameAssembly.dll，RVA；与 2.8 当前对应的游戏版本一致）
//   0xB34E40  CFAnimator.SetFloat(this, name, value, character, method)   参数路径落点
//   0xB6E1D0  Weapon.get_isMyWeapon(this)                                  本地玩家过滤
//   0xB62CB0  WPN_Gun.Reload(this)                                         枪械换弹入口
//   0xB627A0  WPN_Gun.OnAnimationEnd(this, animName, animTag)              枪械换弹结束
//   0xB5FCF0  WPN_GrenadeGun.OnSpecialBtnDown(this)                        榴弹模式切换
//   0xB67AF0  WPN_RPG.OnReloadBtnDown(this)                                RPG 换弹入口
//   0xB67640  WPN_RPG.OnAnimationEnd(this, animName, animTag)              RPG 换弹结束
//   0xB67030  WPN_RPG.Deploy(this)                                         RPG 重新部署
//   0xAA8C30  UnityEngine.Animator.set_speed(animator, value, method)      改动画器速度
//
// 五、Frida 17 注入脚本运行在严格模式：未声明变量赋值会抛 ReferenceError 让 enable() 中断。
//     本文件所有跨闭包变量都显式 var；诊断日志走 log_file 通道，不受"每模块 10 条"上限影响。

modules.ammoplus = (function() {
  var MIN_MULTIPLIER = 1.0;
  var MAX_MULTIPLIER = 5.0;
  var DEFAULT_MULTIPLIER = 4.0;
  var RELOAD_PARAM = 'ReloadSpeed';

  var enabled = false;
  var multiplier = DEFAULT_MULTIPLIER;

  var setFloatAddr = null;
  var originalSetFloat = null;
  var isMyWeapon = null;
  var animatorSetSpeed = null;

  var gunReloadHook = null;
  var gunAnimEndHook = null;
  var grenadeModeHook = null;
  var rpgReloadHook = null;
  var rpgAnimEndHook = null;
  var rpgDeployHook = null;

  var speedTargets = [];
  var speedRestoreTimer = null;

  var gunScaleCount = 0;
  var grenadeScaleCount = 0;
  var rpgScaleCount = 0;
  var errorCount = 0;

  function clampMultiplier(value) {
    var v = parseFloat(value);
    if (!isFinite(v)) return multiplier;
    if (v < MIN_MULTIPLIER) v = MIN_MULTIPLIER;
    if (v > MAX_MULTIPLIER) v = MAX_MULTIPLIER;
    return Math.round(v * 10) / 10;
  }

  function readPtr(addr) {
    try {
      if (!addr || addr.isNull()) return null;
      var v = addr.readPointer();
      return (v && !v.isNull()) ? v : null;
    } catch (e) {
      return null;
    }
  }

  // Il2CppString 布局：+0x08 length(int32)，+0x0C UTF-16 字符
  function readIl2CppString(ptrValue) {
    try {
      if (!ptrValue || ptrValue.isNull()) return '';
      var len = ptrValue.add(8).readS32();
      if (len <= 0 || len > 64) return '';
      var out = '';
      for (var i = 0; i < len; i++) out += String.fromCharCode(ptrValue.add(12 + i * 2).readU16());
      return out;
    } catch (e) {
      return '';
    }
  }

  function isReloadParamName(namePtr) {
    try {
      if (!namePtr || namePtr.isNull()) return false;
      if (namePtr.add(8).readS32() !== RELOAD_PARAM.length) return false;
      var chars = namePtr.add(12);
      for (var i = 0; i < RELOAD_PARAM.length; i++) {
        if (chars.add(i * 2).readU16() !== RELOAD_PARAM.charCodeAt(i)) return false;
      }
      return true;
    } catch (e) {
      return false;
    }
  }

  // WPN_RPG 判定：Weapon.data(+0x68) 与 WPN_RPG.realData(+0xF0) 指向同一个 WD_RPG 实例
  function isRpgWeapon(weapon) {
    try {
      if (!weapon || weapon.isNull()) return false;
      var realData = readPtr(weapon.add(0xF0));
      if (!realData) return false;
      var data = readPtr(weapon.add(0x68));
      if (!data) return false;
      return data.equals(realData);
    } catch (e) {
      return false;
    }
  }

  // 榴弹模式：CFAnimator.changeMode(+0x54)，WPN_GrenadeGun 切模式时置位
  function isGrenadeMode(weapon) {
    try {
      if (!weapon || weapon.isNull()) return false;
      return weapon.add(0x54).readU8() !== 0;
    } catch (e) {
      return false;
    }
  }

  function collectAnimators(weapon) {
    var list = [];
    var weaponAnimator = readPtr(weapon.add(0x40));            // CFAnimator.animator
    if (weaponAnimator) list.push(weaponAnimator);
    var owner = readPtr(weapon.add(0x30));                      // Weapon.owner
    var model = owner ? readPtr(owner.add(0x5C)) : null;        // Player.characterModel
    var handAnimator = model ? readPtr(model.add(0x4C)) : null; // CharacterModel.handAnimator
    if (handAnimator) list.push(handAnimator);
    return list;
  }

  function restoreAnimatorSpeed() {
    for (var i = 0; i < speedTargets.length; i++) {
      try { animatorSetSpeed(speedTargets[i], 1.0, ptr(0)); } catch (e) { errorCount++; }
    }
    speedTargets = [];
    if (speedRestoreTimer) {
      try { clearTimeout(speedRestoreTimer); } catch (e) {}
      speedRestoreTimer = null;
    }
  }

  function applyAnimatorSpeed(weapon) {
    if (multiplier <= 1.001) { restoreAnimatorSpeed(); return false; }
    var list = collectAnimators(weapon);
    if (!list.length) return false;
    for (var i = 0; i < list.length; i++) animatorSetSpeed(list[i], multiplier, ptr(0));
    speedTargets = list;
    if (speedRestoreTimer) { try { clearTimeout(speedRestoreTimer); } catch (e) {} }
    // 换弹被切枪/死亡打断时兜底复位，避免武器后续动作一直加速
    speedRestoreTimer = setTimeout(function() { restoreAnimatorSpeed(); }, 5000);
    return true;
  }

  function tearDown() {
    try { restoreAnimatorSpeed(); } catch (e) {}
    if (setFloatAddr) { try { Interceptor.revert(setFloatAddr); } catch (e) {} }
    if (gunReloadHook) { try { gunReloadHook.detach(); } catch (e) {} }
    if (gunAnimEndHook) { try { gunAnimEndHook.detach(); } catch (e) {} }
    if (grenadeModeHook) { try { grenadeModeHook.detach(); } catch (e) {} }
    if (rpgReloadHook) { try { rpgReloadHook.detach(); } catch (e) {} }
    if (rpgAnimEndHook) { try { rpgAnimEndHook.detach(); } catch (e) {} }
    if (rpgDeployHook) { try { rpgDeployHook.detach(); } catch (e) {} }
    setFloatAddr = null;
    originalSetFloat = null;
    isMyWeapon = null;
    animatorSetSpeed = null;
    gunReloadHook = null;
    gunAnimEndHook = null;
    grenadeModeHook = null;
    rpgReloadHook = null;
    rpgAnimEndHook = null;
    rpgDeployHook = null;
    speedTargets = [];
  }

  return {
    // 滑块实时下发：改的是闭包里的 multiplier，下一次换弹即生效，无需重装 Hook
    setConfig: function(config) {
      if (config && config.multiplier !== undefined && config.multiplier !== null) {
        var next = clampMultiplier(config.multiplier);
        if (next !== multiplier) {
          multiplier = next;
          sendLogFile('info', '快速换弹', '倍率调整为 ' + multiplier.toFixed(1) + 'x');
        }
      }
      return { ok: true, multiplier: multiplier };
    },

    enable: function() {
      if (enabled) return { ok: true, enabled: true, multiplier: multiplier };
      var mod = getGameAssembly();
      if (!mod) {
        sendBothLog('error', '快速换弹', '快速换弹暂未就绪，请先连接游戏后重试', 'FastReload GameAssembly.dll not found');
        return { ok: false, reason: 'gameassembly_not_found' };
      }

      var base = mod.base;
      try {
        isMyWeapon = new NativeFunction(base.add(0xB6E1D0), 'bool', ['pointer', 'pointer']);
        animatorSetSpeed = new NativeFunction(base.add(0xAA8C30), 'void', ['pointer', 'float', 'pointer']);

        // ---------- A) 普通枪械：乘 "ReloadSpeed" 参数 ----------
        setFloatAddr = base.add(0xB34E40);
        originalSetFloat = new NativeFunction(setFloatAddr, 'void', ['pointer', 'pointer', 'float', 'int', 'pointer']);

        Interceptor.replace(setFloatAddr, new NativeCallback(function(self, name, value, character, method) {
          try {
            // 榴弹模式与 RPG 不吃这个参数，走动画器速度路径；先判名字再判归属，避免对非 Weapon 解引用
            if (isReloadParamName(name) && isMyWeapon(self, ptr(0)) &&
                !isGrenadeMode(self) && !isRpgWeapon(self)) {
              var scaled = value * multiplier;
              gunScaleCount++;
              if (gunScaleCount <= 8) {
                sendLogFile('info', '快速换弹',
                  'GUN 换弹动画速度 ' + value.toFixed(2) + ' → ' + scaled.toFixed(2) +
                  '（' + multiplier.toFixed(1) + 'x）');
              }
              value = scaled;
            }
          } catch (e) {
            errorCount++;
          }
          return originalSetFloat(self, name, value, character, method);
        }, 'void', ['pointer', 'pointer', 'float', 'int', 'pointer']));

        // ---------- B) 榴弹模式：改动画器速度 ----------
        // 换弹仍走 WPN_Gun.Reload，但动画名被改写成 "reload_A"，不吃 ReloadSpeed 参数
        gunReloadHook = Interceptor.attach(base.add(0xB62CB0), {
          onEnter: function(args) {
            try {
              var weapon = args[0];
              if (!weapon || weapon.isNull()) return;
              if (!isMyWeapon(weapon, ptr(0))) return;
              if (isRpgWeapon(weapon)) return;
              if (!isGrenadeMode(weapon)) return;
              if (applyAnimatorSpeed(weapon)) {
                grenadeScaleCount++;
                if (grenadeScaleCount <= 8) {
                  sendLogFile('info', '快速换弹',
                    '榴弹模式换弹加速 ×' + multiplier.toFixed(1) + '（动画器速度）');
                }
              }
            } catch (e) {
              errorCount++;
            }
          }
        });

        gunAnimEndHook = Interceptor.attach(base.add(0xB627A0), {
          onEnter: function(args) {
            try {
              if (!speedTargets.length) return;
              if (readIl2CppString(args[2]) === 'reload') restoreAnimatorSpeed();
            } catch (e) {}
          }
        });

        // 榴弹模式开关（步枪 ↔ 榴弹）时复位，避免打断换弹后速度残留
        grenadeModeHook = Interceptor.attach(base.add(0xB5FCF0), {
          onEnter: function() {
            try { if (speedTargets.length) restoreAnimatorSpeed(); } catch (e) {}
          }
        });

        // ---------- C) RPG / AT4：改动画器速度 ----------
        rpgReloadHook = Interceptor.attach(base.add(0xB67AF0), {
          onEnter: function(args) {
            try {
              var weapon = args[0];
              if (!weapon || weapon.isNull()) return;
              if (!isMyWeapon(weapon, ptr(0))) return;
              if (!isRpgWeapon(weapon)) return;
              if (applyAnimatorSpeed(weapon)) {
                rpgScaleCount++;
                if (rpgScaleCount <= 8) {
                  sendLogFile('info', '快速换弹',
                    'RPG 换弹加速 ×' + multiplier.toFixed(1) + '（动画器速度，共 ' + speedTargets.length + ' 个 animator）');
                }
              }
            } catch (e) {
              errorCount++;
            }
          }
        });

        rpgAnimEndHook = Interceptor.attach(base.add(0xB67640), {
          onEnter: function(args) {
            try {
              if (!speedTargets.length) return;
              if (readIl2CppString(args[2]) === 'reload') restoreAnimatorSpeed();
            } catch (e) {}
          }
        });

        rpgDeployHook = Interceptor.attach(base.add(0xB67030), {
          onEnter: function() {
            try { if (speedTargets.length) restoreAnimatorSpeed(); } catch (e) {}
          }
        });
      } catch (e) {
        tearDown();
        sendBothLog('error', '快速换弹', '快速换弹启用失败：' + (e.message || e),
          'FastReload enable failed: ' + (e.message || e));
        return { ok: false, reason: 'hook_failed', detail: String(e && e.message || e) };
      }

      enabled = true;
      gunScaleCount = 0;
      grenadeScaleCount = 0;
      rpgScaleCount = 0;
      errorCount = 0;
      sendLogFile('success', '快速换弹',
        '已启用 — ' + multiplier.toFixed(1) + 'x（枪械=动画参数 / 榴弹模式+RPG=动画器速度）');
      sendStatus('ammoplus', true);
      return { ok: true, enabled: true, multiplier: multiplier };
    },

    disable: function() {
      tearDown();
      if (enabled) {
        enabled = false;
        sendLogFile('info', '快速换弹', '已禁用');
      }
      sendStatus('ammoplus', false);
      return { ok: true, enabled: false };
    },

    getstatus: function() {
      return {
        enabled: enabled,
        multiplier: multiplier,
        gunScaled: gunScaleCount,
        grenadeScaled: grenadeScaleCount,
        rpgScaled: rpgScaleCount,
        errors: errorCount
      };
    }
  };
})();


// Plugin RPC wrapper.
var __pluginFeatureId = "ammoplus";
var __pluginModuleName = "ammoplus";
var __pluginEnabled = false;
var __pluginConfig = {};

function __pluginModule() {
  return modules[__pluginModuleName];
}

function __pluginApplyConfig(config) {
  if (config) {
    for (var key in config) {
      if (Object.prototype.hasOwnProperty.call(config, key)) __pluginConfig[key] = config[key];
    }
  }
  var module = __pluginModule();
  if (!module) return { ok: false, reason: 'module_not_loaded', config: __pluginConfig };
  if (typeof module.setConfig === 'function') {
    try {
      var applied = module.setConfig(__pluginConfig);
      if (applied && typeof applied === 'object') return applied;
    } catch (e) {
      return { ok: false, reason: 'set_config_failed', detail: String(e && e.message || e), config: __pluginConfig };
    }
  }
  return { ok: true, config: __pluginConfig };
}

function __pluginEnable(config) {
  __pluginApplyConfig(config);
  var module = __pluginModule();
  if (!module || typeof module.enable !== 'function') return { ok: false, reason: 'enable_missing' };
  var result = module.enable();
  if (result && result.ok === false) {
    __pluginEnabled = false;
    return result;
  }
  __pluginEnabled = true;
  return result || { ok: true, enabled: true };
}

function __pluginDisable() {
  var module = __pluginModule();
  var result = null;
  if (module && typeof module.disable === 'function') {
    try {
      result = module.disable();
    } catch (e) {
      result = { ok: false, reason: 'disable_failed', detail: String(e && e.message || e) };
    }
  }
  __pluginEnabled = false;
  return result || { ok: true, enabled: false };
}

function __pluginStatus() {
  var module = __pluginModule();
  var stats = {};
  try {
    if (module && typeof module.getstatus === 'function') stats = module.getstatus();
    else if (module && typeof module.getStatus === 'function') stats = module.getStatus();
  } catch (_) {}
  return { enabled: __pluginEnabled, config: __pluginConfig, stats: stats };
}

function __pluginCleanup(payload) {
  __pluginDisable();
  return { ok: true, reason: payload && payload.reason ? payload.reason : 'cleanup' };
}

rpc.exports = {
  enable: __pluginEnable,
  disable: __pluginDisable,
  setConfig: __pluginApplyConfig,
  status: __pluginStatus,
  cleanup: __pluginCleanup
};
