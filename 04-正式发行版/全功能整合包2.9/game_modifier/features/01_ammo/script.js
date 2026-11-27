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

// ammo.js - 无限子弹 / 无限弹药
// 无限子弹：替换 ConsumeAmmo，开火不扣弹，不需要换弹。
// 无限弹药：Hook Player.UpdateBuffProperty，每帧把 Player.Buff_InfinityAmmo(+0x128) 置 1。
//   这是游戏原生 InfinityAmmoBuff 的实现方式，复用其换弹逻辑：
//   - WPN_Gun.CanReload：备弹为 0 时也允许换弹；
//   - WPN_Gun.ReloadOver：直接把 clip 填到 maxClip，不扣备弹；
//   - PlayerWeapons.get_isInfinityAmmo：HUD 显示无限弹药图标。
// 依据：InfinityAmmoBuff..ctor 0x10AE7990 / Player.UpdateBuffProperty 0x10B547F0 /
//       WPN_Gun.CanReload 0x10B60E30 / WPN_Gun.ReloadOver 0x10B62C10。

modules.ammo = (function() {
  var enabled = false;
  var hooks = [];
  var originalConsumeAmmo = null;
  var originalConsumeBase = null;
  var isMyPlayer = null;
  var isMyWeapon = null;
  var rpgIsMaxClip = null;
  var rpgCanReload = null;
  var rpgAnimEmptyTag = null;
  var rpgHudLogged = false;

  // 无限子弹（原来的 ConsumeAmmo 方案）
  var bulletEnabled = true;
  var bulletScope = 'player_only';

  // 无限弹药（复用游戏 Buff_InfinityAmmo 标志位）
  var ammoEnabled = false;
  var ammoScope = 'player_only';

  function writeObscuredInt(fieldPtr, value) {
    try {
      if (!fieldPtr || fieldPtr.isNull()) return false;
      var key = fieldPtr.readS32();
      var encrypted = value ^ key;
      fieldPtr.add(0x4).writeS32(encrypted);
      fieldPtr.add(0x8).writeU8(1);
      fieldPtr.add(0xC).writeS32(value);
      fieldPtr.add(0x10).writeU8(0);
      return fieldPtr.add(0x4).readS32() === encrypted;
    } catch (e) {
      return false;
    }
  }

  function isReadablePtr(p) {
    try {
      if (!p || p.isNull()) return false;
      p.readPointer();
      return true;
    } catch (e) {
      return false;
    }
  }

  function isAllScope(scope) {
    return scope === 'all_players' || scope === 'all';
  }

  function normalizeScope(scope) {
    return (scope === 'all_players' || scope === 'all') ? 'all_players' : 'player_only';
  }

  function scopeLabel(scope) {
    return isAllScope(scope) ? '玩家和所有人机' : '仅限玩家';
  }

  function isLocalWeapon(weaponPtr) {
    if (!weaponPtr || weaponPtr.isNull()) return false;

    // 路径1：优先使用游戏自己的 Weapon.get_isMyWeapon。
    try {
      if (isMyWeapon && isMyWeapon(weaponPtr, ptr(0))) return true;
    } catch (e1) {}

    // 路径2：兜底尝试 Weapon/PlayerWeapons 常见 owner 字段。
    try {
      if (!isMyPlayer || !isReadablePtr(weaponPtr)) return false;
      // Weapon : CFAnimator : Model；owner 是 Model.owner(+0x30)。
      var owner = weaponPtr.add(0x30).readPointer();
      if (owner && !owner.isNull() && isReadablePtr(owner)) {
        return !!isMyPlayer(owner, ptr(0));
      }
    } catch (e2) {}

    return false;
  }

  function shouldAffectWeapon(weaponPtr, scope) {
    if (!weaponPtr || weaponPtr.isNull()) return false;
    if (isAllScope(scope)) return true;
    return isLocalWeapon(weaponPtr);
  }

  // RPG/AT4 不走 ConsumeAmmo，单独维持弹匣。
  function setLocalRpgClip10(weaponPtr) {
    try {
      if (!bulletEnabled) return false;
      if (!weaponPtr || weaponPtr.isNull() || !shouldAffectWeapon(weaponPtr, bulletScope)) return false;
      var ammo = weaponPtr.add(0xEC).readPointer();
      if (!ammo || ammo.isNull() || !isReadablePtr(ammo)) return false;
      var clipOk = writeObscuredInt(ammo.add(0x08), 10);
      var maxClipOk = writeObscuredInt(ammo.add(0x30), 10);
      return clipOk && maxClipOk;
    } catch (e) {
      return false;
    }
  }

  // WPN_RPG 的弹药对象：WPN_RPG.ammo(+0xEC)，不是 WPN_Gun.ammoData(+0xF4)。
  function readRpgAmmo(weaponPtr) {
    try {
      if (!weaponPtr || weaponPtr.isNull()) return null;
      var ammo = weaponPtr.add(0xEC).readPointer();
      if (!ammo || ammo.isNull() || !isReadablePtr(ammo)) return null;
      return ammo;
    } catch (e) {
      return null;
    }
  }

  // 与 WPN_Gun.ReloadOver 的 buff 分支一致：20 字节 ObscuredInt 原样拷贝 maxClip -> clip。
  function copyAmmoClipToMax(ammoPtr) {
    try {
      if (!ammoPtr || ammoPtr.isNull() || !isReadablePtr(ammoPtr)) return false;
      var maxClipBytes = ammoPtr.add(0x30).readByteArray(0x14);
      if (!maxClipBytes) return false;
      ammoPtr.add(0x08).writeByteArray(maxClipBytes);
      return true;
    } catch (e) {
      return false;
    }
  }

  // il2cpp 对象 -> 类名（Il2CppClass.name 在 klass+0x8）。
  function classNameOf(objPtr) {
    try {
      if (!objPtr || objPtr.isNull()) return '';
      var klass = objPtr.readPointer();
      if (!klass || klass.isNull()) return '';
      var namePtr = klass.add(0x8).readPointer();
      if (!namePtr || namePtr.isNull()) return '';
      return namePtr.readUtf8String() || '';
    } catch (e) {
      return '';
    }
  }

  // 仅用于 HUD 判断：优先按 IL2CPP 类名识别 WPN_RPG（AT4 / Nano AT4 同一组件），
  // 不依赖 +0xF0(realData) / +0xF4(gunfire) 是否已在预制体上序列化。
  // 类名读取失败时退回原来的字段探测。
  function looksLikeRpgByFields(weaponPtr) {
    try {
      if (!weaponPtr || weaponPtr.isNull()) return false;
      var ammo = weaponPtr.add(0xEC).readPointer();
      var realData = weaponPtr.add(0xF0).readPointer();
      var gunfire = weaponPtr.add(0xF4).readPointer();
      if (!ammo || ammo.isNull() || !realData || realData.isNull()) return false;
      if (!isReadablePtr(ammo) || !isReadablePtr(realData) || !isReadablePtr(gunfire)) return false;
      return true;
    } catch (e) {
      return false;
    }
  }

  function isRpgWeapon(weaponPtr) {
    try {
      if (!weaponPtr || weaponPtr.isNull()) return false;
      var cls = classNameOf(weaponPtr);
      if (cls) return cls.indexOf('WPN_RPG') === 0;
      return looksLikeRpgByFields(weaponPtr);
    } catch (e) {
      return false;
    }
  }

  // 每帧在 Player.UpdateBuffProperty 返回后写 1。
  // 该函数会先把 Buff_InfinityAmmo 清 0，再调用所有 RefBool 回调；
  // 我们在 onLeave 写入，等价于身上一直挂着 InfinityAmmoBuff。
  function applyInfinityAmmoFlag(playerPtr) {
    if (!ammoEnabled) return;
    if (!playerPtr || playerPtr.isNull()) return;
    try {
      if (!isAllScope(ammoScope)) {
        if (!isMyPlayer || !isMyPlayer(playerPtr, ptr(0))) return;
      }
      playerPtr.add(0x128).writeU8(1);
    } catch (e) {}
  }

  return {
    enable: function() {
      if (enabled) return;
      var mod = Process.findModuleByName('GameAssembly.dll');
      if (!mod) { sendBothLog('error', '无限子弹', '无限子弹暂未就绪，请重新连接游戏后重试', 'Ammo GameAssembly.dll not found'); return; }
      enabled = true;
      var base = mod.base;

      try {
        var addrConsumeAmmo = base.add(0xB61140);
        var addrConsumeBase = base.add(0xB6C310);
        var addrIsMyPlayer = base.add(0xB55FD0);
        var addrIsMyWeapon = base.add(0xB6E1D0);

        originalConsumeAmmo = new NativeFunction(addrConsumeAmmo, 'bool', ['pointer', 'pointer']);
        originalConsumeBase = new NativeFunction(addrConsumeBase, 'bool', ['pointer', 'pointer']);
        isMyPlayer = new NativeFunction(addrIsMyPlayer, 'bool', ['pointer', 'pointer']);
        isMyWeapon = new NativeFunction(addrIsMyWeapon, 'bool', ['pointer', 'pointer']);

        Interceptor.replace(addrConsumeAmmo, new NativeCallback(function(thisPtr, methodInfo) {
          if (bulletEnabled && shouldAffectWeapon(thisPtr, bulletScope)) {
            return 1;
          }
          if (!originalConsumeAmmo) return 0;
          return originalConsumeAmmo(thisPtr, methodInfo);
        }, 'bool', ['pointer', 'pointer']));
        hooks.push({ type: 'replace', addr: addrConsumeAmmo });
        sendLog('info', '无限子弹', 'WPN_Gun.ConsumeAmmo 已替换（无限子弹=' + (bulletEnabled ? '开' : '关') + '，' + scopeLabel(bulletScope) + '）');
      } catch (e) {
        sendBothLog('error', '无限子弹', '无限子弹初始化失败，请稍后重试', 'Ammo replace WPN_Gun.ConsumeAmmo failed: ' + e);
      }

      // WPN_RPG 补充所需的原生辅助函数。
      try {
        rpgIsMaxClip = new NativeFunction(base.add(0xB6EEA0), 'bool', ['pointer', 'pointer']);
        rpgCanReload = new NativeFunction(base.add(0xB6EBD0), 'bool', ['pointer', 'pointer']);
        rpgAnimEmptyTag = new NativeFunction(base.add(0xB35350), 'bool', ['pointer', 'pointer']);
      } catch (e) {
        sendDevLog('warn', '无限弹药', 'RPG 弹药辅助函数初始化失败: ' + e, 'RPG ammo helpers failed: ' + e);
      }

      try {
        var addrConsumeBaseFallback = base.add(0xB6C310);
        Interceptor.replace(addrConsumeBaseFallback, new NativeCallback(function(thisPtr, methodInfo) {
          if (bulletEnabled && shouldAffectWeapon(thisPtr, bulletScope)) {
            return 1;
          }
          if (!originalConsumeBase) return 0;
          return originalConsumeBase(thisPtr, methodInfo);
        }, 'bool', ['pointer', 'pointer']));
        hooks.push({ type: 'replace', addr: addrConsumeBaseFallback });
        sendLog('info', '无限子弹', 'Weapon.ConsumeAmmo 已替换（兜底）');
      } catch (e) {
        sendDevLog('warn', '无限子弹', '替换 Weapon.ConsumeAmmo 失败: ' + e, 'Ammo fallback replace failed');
      }

      try {
        var addrRpgFire = base.add(0xB670A0);
        var addrRpgFillAmmo = base.add(0xB67070);
        var rpgFillAmmoFn = new NativeFunction(addrRpgFillAmmo, 'void', ['pointer', 'pointer']);

        var rpgFireHook = Interceptor.attach(addrRpgFire, {
          onEnter: function(args) {
            try {
              var self = args[0];
              if (self && !self.isNull() && bulletEnabled && shouldAffectWeapon(self, bulletScope)) {
                rpgFillAmmoFn(self, ptr(0));
                setLocalRpgClip10(self);
                this.rpgSelf = self;
              }
            } catch (e) {}
          },
          onLeave: function() {
            try {
              if (this.rpgSelf) setLocalRpgClip10(this.rpgSelf);
            } catch (e) {}
          }
        });
        hooks.push({ type: 'attach', handle: rpgFireHook });
        sendLog('info', '无限子弹', 'RPG/AT4 无限子弹已启用（' + (bulletEnabled ? '开' : '关') + '，' + scopeLabel(bulletScope) + '）');
      } catch (e) {
        sendDevLog('warn', '无限子弹', 'RPG/AT4 初始化失败: ' + e, 'Ammo RPG/AT4 hook init failed');
      }

      try {
        var addrRpgReload = base.add(0xB67C40);
        var rpgReloadHook = Interceptor.attach(addrRpgReload, {
          onEnter: function(args) {
            this.rpgSelf = args[0];
          },
          onLeave: function() {
            try {
              if (this.rpgSelf) setLocalRpgClip10(this.rpgSelf);
            } catch (e) {}
          }
        });
        hooks.push({ type: 'attach', handle: rpgReloadHook });
        sendLog('info', '无限子弹', 'RPG/AT4 弹匣已维持为10（' + scopeLabel(bulletScope) + '）');
      } catch (e) {
        sendDevLog('warn', '无限子弹', 'RPG/AT4 换弹挂钩失败: ' + e, 'Ammo RPG/AT4 reload hook init failed');
      }

      // 无限弹药：WPN_RPG / AT4 / Nano AT4。
      // WPN_RPG 不读 Player.Buff_InfinityAmmo，单独补：
      // - CanReload：备弹为 0 时仍允许自动换弹；
      // - OnReloadBtnDown：手动换弹时临时补 1 发备弹让原逻辑启动，随后把 clip 填满并恢复备弹；
      // - Reload：自动换弹路径启动时把 clip 填满。
      // 填满 clip 后，后续 AmmoData.Reload 的 need=0，不会扣备弹。
      try {
        if (!rpgIsMaxClip || !rpgCanReload || !rpgAnimEmptyTag) throw new Error('rpg helpers not ready');

        var rpgCanReloadHook = Interceptor.attach(base.add(0xB66E80), {
          onEnter: function(args) {
            this.weapon = args[0];
          },
          onLeave: function(retval) {
            try {
              if (!ammoEnabled || retval.toInt32() !== 0) return;
              var self = this.weapon;
              if (!self || !shouldAffectWeapon(self, ammoScope)) return;
              var ammo = readRpgAmmo(self);
              if (!ammo) return;
              if (rpgIsMaxClip(ammo, ptr(0))) return;
              if (!rpgAnimEmptyTag(self, ptr(0))) return;
              retval.replace(1);
              sendDevLog('info', '无限弹药', 'RPG CanReload 放行（备弹=0）');
            } catch (e) {}
          }
        });
        hooks.push({ type: 'attach', handle: rpgCanReloadHook });

        var rpgReloadBtnHook = Interceptor.attach(base.add(0xB67AF0), {
          onEnter: function(args) {
            this.weapon = args[0];
            this.ammo = null;
            this.injected = false;
            try {
              if (!ammoEnabled) return;
              var self = this.weapon;
              if (!self || !shouldAffectWeapon(self, ammoScope)) return;
              var ammo = readRpgAmmo(self);
              if (!ammo) return;
              if (rpgIsMaxClip(ammo, ptr(0))) return;
              if (!rpgAnimEmptyTag(self, ptr(0))) return;
              this.ammo = ammo;
              if (!rpgCanReload(ammo, ptr(0))) {
                if (writeObscuredInt(ammo.add(0x1C), 1)) {
                  this.injected = true;
                } else {
                  this.ammo = null;
                }
              }
            } catch (e) {
              this.ammo = null;
            }
          },
          onLeave: function() {
            var ammo = this.ammo;
            if (!ammo) return;
            try {
              copyAmmoClipToMax(ammo);
              if (this.injected) writeObscuredInt(ammo.add(0x1C), 0);
              sendDevLog('info', '无限弹药', 'RPG 换弹启动：clip=max，injected=' + this.injected);
            } catch (e) {}
          }
        });
        hooks.push({ type: 'attach', handle: rpgReloadBtnHook });

        var rpgAmmoReloadHook = Interceptor.attach(base.add(0xB67C40), {
          onEnter: function(args) {
            this.weapon = args[0];
          },
          onLeave: function() {
            try {
              if (!ammoEnabled) return;
              var self = this.weapon;
              if (!self || !shouldAffectWeapon(self, ammoScope)) return;
              var ammo = readRpgAmmo(self);
              if (!ammo) return;
              if (!rpgIsMaxClip(ammo, ptr(0))) { copyAmmoClipToMax(ammo); sendDevLog('info', '无限弹药', 'RPG Reload 填满弹夹'); }
            } catch (e) {}
          }
        });
        hooks.push({ type: 'attach', handle: rpgAmmoReloadHook });

        // 换弹完成事件（AnimationEventReceiver.AE_ReloadOver -> WPN_RPG.ReloadOver）也兜底填满。
        var rpgReloadOverHook = Interceptor.attach(base.add(0xB67BC0), {
          onEnter: function(args) {
            try {
              if (!ammoEnabled) return;
              var self = args[0];
              if (!self || !shouldAffectWeapon(self, ammoScope)) return;
              var ammo = readRpgAmmo(self);
              if (!ammo) return;
              if (!rpgIsMaxClip(ammo, ptr(0))) { copyAmmoClipToMax(ammo); sendDevLog('info', '无限弹药', 'RPG ReloadOver 填满弹夹'); }
            } catch (e) {}
          }
        });
        hooks.push({ type: 'attach', handle: rpgReloadOverHook });

        sendLog('info', '无限弹药', 'WPN_RPG/AT4 已挂钩（无限弹药=' + (ammoEnabled ? '开' : '关') + '，' + scopeLabel(ammoScope) + '）');
      } catch (e) {
        sendBothLog('error', '无限弹药', 'RPG/AT4 无限弹药初始化失败，请稍后重试', 'RPG infinite ammo hook failed: ' + e);
      }

      // 仅 UI：让 WPN_RPG/AT4 的 HUD 也显示无限弹药。WPN_RPG 的 CanGetInfinityAmmo 仍返回 false，
      // 但 HUD_Weapon.Update 只读 PlayerWeapons.get_isInfinityAmmo，所以在这里放行即可。
      try {
        var rpgHudProbePtr = null;
        var rpgHudHook = Interceptor.attach(base.add(0xB17120), {
          onEnter: function(args) {
            this.wpns = args[0];
          },
          onLeave: function(retval) {
            try {
              if (!ammoEnabled) return;
              var wpns = this.wpns;
              if (!wpns || wpns.isNull()) return;
              var inUse = wpns.add(0x18).readPointer();
              if (!inUse || inUse.isNull()) return;
              var cls = classNameOf(inUse);
              var isRpg = isRpgWeapon(inUse);
              // 首次见到某把 RPG 时输出一条不受「每模块 10 条」限制的诊断。
              if (isRpg && (!rpgHudProbePtr || !rpgHudProbePtr.equals(inUse))) {
                rpgHudProbePtr = inUse;
                sendLogFile('info', '无限弹药HUD', 'HUD 诊断 inUse=' + inUse + ' class=' + cls
                  + ' ret=' + (retval.toInt32() & 0xff) + ' scope=' + ammoScope
                  + ' scopeOk=' + shouldAffectWeapon(inUse, ammoScope));
              }
              if ((retval.toInt32() & 0xff) !== 0) return;
              if (!isRpg) return;
              if (!shouldAffectWeapon(inUse, ammoScope)) return;
              retval.replace(1);
              if (!rpgHudLogged) {
                rpgHudLogged = true;
                sendLogFile('info', '无限弹药HUD', 'HUD 已强制显示无限弹药图标 class=' + cls + ' inUse=' + inUse);
              }
            } catch (e) {}
          }
        });
        hooks.push({ type: 'attach', handle: rpgHudHook });
        sendLog('info', '无限弹药', 'RPG/AT4 HUD 无限弹药图标已挂钩');
      } catch (e) {
        sendDevLog('warn', '无限弹药', 'RPG/AT4 HUD 挂钩失败: ' + e, 'RPG HUD hook failed: ' + e);
      }

      // 无限弹药：复用游戏原生 Buff_InfinityAmmo 标志位。
      try {
        var addrUpdateBuffProperty = base.add(0xB547F0);
        var buffHook = Interceptor.attach(addrUpdateBuffProperty, {
          onEnter: function(args) {
            this.player = args[0];
          },
          onLeave: function() {
            applyInfinityAmmoFlag(this.player);
          }
        });
        hooks.push({ type: 'attach', handle: buffHook });
        sendLog('info', '无限弹药', 'Player.UpdateBuffProperty 已挂钩（无限弹药=' + (ammoEnabled ? '开' : '关') + '，' + scopeLabel(ammoScope) + '）');
      } catch (e) {
        sendBothLog('error', '无限弹药', '无限弹药初始化失败，请稍后重试', 'Ammo buff flag hook failed: ' + e);
      }

      if (!hooks.length) {
        enabled = false;
        sendBothLog('error', '无限子弹', '无限子弹初始化失败，请稍后重试', 'Ammo no hooks installed');
        return;
      }

      sendLog('success', '无限子弹', '已启用（无限子弹=' + (bulletEnabled ? '开' : '关') + '，无限弹药=' + (ammoEnabled ? '开' : '关') + '）');
      sendStatus('ammo', true);
    },
    disable: function() {
      if (!enabled) return;
      for (var i = 0; i < hooks.length; i++) {
        try {
          if (hooks[i].type === 'replace') {
            Interceptor.revert(hooks[i].addr);
          } else {
            hooks[i].handle.detach();
          }
        } catch (e) {}
      }
      hooks = [];
      originalConsumeAmmo = null;
      originalConsumeBase = null;
      isMyPlayer = null;
      isMyWeapon = null;
      rpgIsMaxClip = null;
      rpgCanReload = null;
      rpgAnimEmptyTag = null;
      rpgHudLogged = false;
      enabled = false;
      sendLog('info', '无限子弹', '已禁用');
      sendStatus('ammo', false);
    },
    setconfig: function(payload) {
      if (typeof payload === 'string') {
        bulletScope = normalizeScope(payload);
        ammoScope = bulletScope;
      } else if (payload && typeof payload === 'object') {
        if (payload.scope !== undefined) {
          bulletScope = normalizeScope(payload.scope);
        }
        if (payload.infinite_bullet_scope !== undefined) {
          bulletScope = normalizeScope(payload.infinite_bullet_scope);
        }
        if (payload.infinite_ammo_scope !== undefined) {
          ammoScope = normalizeScope(payload.infinite_ammo_scope);
        }
        if (payload.infinite_bullet_enabled !== undefined) {
          bulletEnabled = !!payload.infinite_bullet_enabled;
        }
        if (payload.infinite_ammo_enabled !== undefined) {
          ammoEnabled = !!payload.infinite_ammo_enabled;
        }
      }
      sendLog('info', '无限子弹', '设置已更新：无限子弹=' + (bulletEnabled ? '开' : '关') + '（' + scopeLabel(bulletScope) + '），无限弹药=' + (ammoEnabled ? '开' : '关') + '（' + scopeLabel(ammoScope) + '）');
      return {
        ok: true,
        infinite_bullet_enabled: bulletEnabled,
        infinite_bullet_scope: bulletScope,
        infinite_ammo_enabled: ammoEnabled,
        infinite_ammo_scope: ammoScope
      };
    },
    getstatus: function() {
      return {
        enabled: enabled,
        hooks: hooks.length,
        infinite_bullet_enabled: bulletEnabled,
        infinite_bullet_scope: bulletScope,
        infinite_ammo_enabled: ammoEnabled,
        infinite_ammo_scope: ammoScope
      };
    }
  };
})();


// Plugin RPC wrapper. Hook internals above are copied unchanged from the legacy script.
var __pluginFeatureId = "ammo";
var __pluginModuleName = "ammo";
var __pluginEnabled = false;
var __pluginConfig = {
  scope: "player_only",
  infinite_bullet_enabled: true,
  infinite_bullet_scope: "player_only",
  infinite_ammo_enabled: false,
  infinite_ammo_scope: "player_only"
};

function __pluginModule() {
  return modules[__pluginModuleName];
}

function __pluginApplyConfig(config) {
  if (config) {
    // 旧版只有 scope 键，迁移到无限子弹的范围，避免被新键默认值覆盖。
    if (config.scope !== undefined && config.infinite_bullet_scope === undefined) {
      __pluginConfig.infinite_bullet_scope = config.scope;
    }
    for (var key in config) {
      if (Object.prototype.hasOwnProperty.call(config, key)) __pluginConfig[key] = config[key];
    }
  }
  var module = __pluginModule();
  if (!module) return { ok: false, reason: 'module_not_loaded', config: __pluginConfig };
  if (typeof module.setconfig === 'function') module.setconfig(__pluginConfig);
  return { ok: true, config: __pluginConfig };
}

function __pluginEnable(config) {
  if (config) __pluginApplyConfig(config);
  var module = __pluginModule();
  if (!module || typeof module.enable !== 'function') return { ok: false, reason: 'enable_missing' };
  var result = module.enable();
  __pluginEnabled = true;
  return result || { ok: true, enabled: true };
}

function __pluginDisable() {
  var module = __pluginModule();
  if (module && typeof module.disable === 'function') module.disable();
  __pluginEnabled = false;
  return { ok: true, enabled: false };
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