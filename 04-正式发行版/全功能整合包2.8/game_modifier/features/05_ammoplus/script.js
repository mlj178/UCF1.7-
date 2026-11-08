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

// reload_speed.js - 快速换弹（GUN 走动画参数，RPG 走动画器速度；倍率 1.0~5.0）
//
// 一、GUN 与 RPG 是两条完全不同的实现路径（这是 v2 修 RPG 失效的根据）
//   · GUN（WPN_Gun 系）：WPN_Gun.Reload(0xB62CB0) 每次都算
//       GetAnimSpeed(reloadAnimRatio) × PlayerWeapons.ReloadSpeed
//     然后 CFAnimator.SetFloat("ReloadSpeed", v) 再播放 "reload" 动画 → 乘这个 v 即可。
//   · RPG（WPN_RPG）：换弹入口是 WPN_RPG.OnReloadBtnDown(0xB67AF0)，
//     它只做 PlayWeaponAnimWithSameTag("reload") + CharacterModel.PlayGunReloadAnim，
//     **完全不动 "ReloadSpeed" 参数**；该参数只在 Deploy 时由
//     Weapon.Deploy 的虚调用(Slot 23) → WPN_RPG.AnimSpeedSetting(0xB66CA0) 写一次。
//     → 实测：RPG 的换弹动画不吃这个参数，乘参数对 RPG 没有效果。
//   注：WPN_RPG.Reload(0xB67C40) 在 0xB67AF0 存在的情况下没有任何调用点（死代码），
//       所以 v2 早期把"刷新 RPG 参数"的钩子挂在 0xB67C40 上等于没挂（2.8 的 01_ammo 也踩了同一个坑）。
//
// 二、RPG 的正确做法：直接改动画器播放速度
//   · OnReloadBtnDown 里在游戏播放换弹动画之前，把
//       weapon.animator(CFAnimator+0x40) 与 owner.characterModel.handAnimator(+0x5C→+0x4C)
//     的 Animator.speed 设为倍率；换弹动画结束（OnAnimationEnd tag=="reload"）立刻复位 1.0。
//   · 游戏自己在每次 Deploy 的 CFAnimator.AnimatorInit 里也会把这两个 Animator.speed 复位成 1.0，
//     所以切枪/重部署天然是安全的兜底；另外再挂 5s 看门狗，防止换弹被打断时速度残留。
//   · RPG 不再乘 "ReloadSpeed" 参数，避免两种机制叠加成倍率平方。
//
// 三、关键地址（GameAssembly.dll，RVA；与 2.8 当前对应的游戏版本一致）
//   0xB34E40  CFAnimator.SetFloat(this, name, value, character, method)   GUN 落点
//   0xB6E1D0  Weapon.get_isMyWeapon(this)                                 本地玩家过滤
//   0xB67AF0  WPN_RPG.OnReloadBtnDown(this)                               RPG 换弹真实入口
//   0xB67640  WPN_RPG.OnAnimationEnd(this, animName, animTag)             换弹结束复位
//   0xB67030  WPN_RPG.Deploy(this)                                        重部署复位
//   0xAA8C30  UnityEngine.Animator.set_speed(animator, value, method)
//   0xB170E0  PlayerWeapons.get_ReloadSpeed                               老方案落点，已弃用
//
// 四、Frida 17 的注入脚本运行在严格模式：任何未声明变量赋值都会抛 ReferenceError
//     并让 enable() 中断（2.7/2.8 早期就是栽在 originalGetReloadSpeed 漏写 var）。
//     本文件所有跨闭包变量一律显式 var 声明；诊断日志走 log_file 通道，不受"每模块 10 条"上限影响。

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

  var rpgReloadHook = null;
  var rpgAnimEndHook = null;
  var rpgDeployHook = null;
  var rpgAnimators = [];
  var rpgRestoreTimer = null;

  var gunScaleCount = 0;
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

  // WPN_RPG 的判定：Weapon.data(+0x68) 与 WPN_RPG.realData(+0xF0) 是同一个 WD_RPG 实例。
  // WPN_Gun 的 +0xF0 是 bool（isSemiGun），不会是有效指针，因此不会误判。
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

  function collectRpgAnimators(weapon) {
    var list = [];
    var weaponAnimator = readPtr(weapon.add(0x40));            // CFAnimator.animator
    if (weaponAnimator) list.push(weaponAnimator);
    var owner = readPtr(weapon.add(0x30));                      // Weapon.owner
    var model = owner ? readPtr(owner.add(0x5C)) : null;        // Player.characterModel
    var handAnimator = model ? readPtr(model.add(0x4C)) : null; // CharacterModel.handAnimator
    if (handAnimator) list.push(handAnimator);
    return list;
  }

  function restoreRpgAnimators() {
    for (var i = 0; i < rpgAnimators.length; i++) {
      try { animatorSetSpeed(rpgAnimators[i], 1.0, ptr(0)); } catch (e) { errorCount++; }
    }
    rpgAnimators = [];
    if (rpgRestoreTimer) {
      try { clearTimeout(rpgRestoreTimer); } catch (e) {}
      rpgRestoreTimer = null;
    }
  }

  function tearDown() {
    try { restoreRpgAnimators(); } catch (e) {}
    if (setFloatAddr) { try { Interceptor.revert(setFloatAddr); } catch (e) {} }
    if (rpgReloadHook) { try { rpgReloadHook.detach(); } catch (e) {} }
    if (rpgAnimEndHook) { try { rpgAnimEndHook.detach(); } catch (e) {} }
    if (rpgDeployHook) { try { rpgDeployHook.detach(); } catch (e) {} }
    setFloatAddr = null;
    originalSetFloat = null;
    isMyWeapon = null;
    animatorSetSpeed = null;
    rpgReloadHook = null;
    rpgAnimEndHook = null;
    rpgDeployHook = null;
    rpgAnimators = [];
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

        // ---------- GUN：乘 "ReloadSpeed" 参数 ----------
        setFloatAddr = base.add(0xB34E40);
        originalSetFloat = new NativeFunction(setFloatAddr, 'void', ['pointer', 'pointer', 'float', 'int', 'pointer']);

        Interceptor.replace(setFloatAddr, new NativeCallback(function(self, name, value, character, method) {
          try {
            // 先按名字过滤，再做归属判断；RPG 不在这里处理（见下面的动画器速度方案），避免叠加成平方
            if (isReloadParamName(name) && isMyWeapon(self, ptr(0)) && !isRpgWeapon(self)) {
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

        // ---------- RPG：直接改动画器速度 ----------
        // 换弹真实入口。RPG 不写 "ReloadSpeed"，所以在这里把动画器速度设为倍率，
        // 游戏播放 reload 动画时长度即被缩短，动画结束事件（补弹）也同步提前。
        rpgReloadHook = Interceptor.attach(base.add(0xB67AF0), {
          onEnter: function(args) {
            try {
              var weapon = args[0];
              if (!weapon || weapon.isNull()) return;
              if (!isMyWeapon(weapon, ptr(0))) return;
              if (!isRpgWeapon(weapon)) return;
              if (multiplier <= 1.001) { restoreRpgAnimators(); return; }
              var list = collectRpgAnimators(weapon);
              if (!list.length) return;
              for (var i = 0; i < list.length; i++) animatorSetSpeed(list[i], multiplier, ptr(0));
              rpgAnimators = list;
              rpgScaleCount++;
              if (rpgScaleCount <= 8) {
                sendLogFile('info', '快速换弹',
                  'RPG 换弹加速 ×' + multiplier.toFixed(1) + '（动画器速度，共 ' + list.length + ' 个 animator）');
              }
              if (rpgRestoreTimer) { try { clearTimeout(rpgRestoreTimer); } catch (e) {} }
              // 换弹被打断（切枪/死亡）时兜底复位，避免武器后续动作一直加速
              rpgRestoreTimer = setTimeout(function() { restoreRpgAnimators(); }, 5000);
            } catch (e) {
              errorCount++;
            }
          }
        });

        // 换弹动画结束（tag == "reload"）→ 立即复位，和游戏给 GUN 的时机一致
        rpgAnimEndHook = Interceptor.attach(base.add(0xB67640), {
          onEnter: function(args) {
            try {
              var weapon = args[0];
              if (!weapon || weapon.isNull() || !rpgAnimators.length) return;
              if (readIl2CppString(args[2]) === 'reload') restoreRpgAnimators();
            } catch (e) {}
          }
        });

        // 重新部署 / 切枪 → 复位（游戏 AnimatorInit 也会把 speed 置 1.0，这里是双保险）
        rpgDeployHook = Interceptor.attach(base.add(0xB67030), {
          onEnter: function() {
            try { if (rpgAnimators.length) restoreRpgAnimators(); } catch (e) {}
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
      rpgScaleCount = 0;
      errorCount = 0;
      sendLogFile('success', '快速换弹', '已启用 — ' + multiplier.toFixed(1) + 'x（GUN=动画参数 / RPG=动画器速度）');
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
