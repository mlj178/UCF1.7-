// speed_gun.js - 射速变快 + 连狙 — 终极武器修改
// 10个Hook点：动画加速10x + 清除射击间隔 + 半自动→全自动 + 狙击镜不关闭 + RPG特殊处理 + 后坐力清零 + 扩散归零

modules.speedgun = (function() {
  var enabled = false;
  var hooks = [];
  var isMyWeaponFn = null;
  var getCharAnim = null;
  var setAnimSpeed = null;
  var isPlayerShooting = false;
  var pendingWeaponSpeedTasks = [];
  var pendingWeaponSpeedMap = {};
  var pendingWeaponSpeedMaxFrames = 30;
  var modeBaseInstance = null;
  var modeSwitchGraceUntil = 0;
  var modeSwitchGraceMs = 800;

  function safeReadPointer(basePtr, offset) {
    try {
      if (!basePtr || basePtr.isNull()) return null;
      var value = basePtr.add(offset).readPointer();
      return (value && !value.isNull()) ? value : null;
    } catch(e) {
      return null;
    }
  }

  function applyGunDataSpeed(weapon) {
    try {
      var data = safeReadPointer(weapon, 0x68);
      var realData = safeReadPointer(weapon, 0xEC);
      if (data && realData && data.equals(realData)) {
        realData.add(0xD0).writeFloat(10.0); // WeaponData_Gun.fireAnimMultiplier
        weapon.add(0xF0).writeU8(0); // WPN_Gun.isSemiGun
        weapon.add(0x108).writeS32(0); // WPN_Gun.semiGunFireLinkState
        weapon.add(0x110).writeFloat(0.0); // WPN_Gun.nextAllowedShootTime
      }
    } catch(e) {}
  }

  function applyGrenadeGunSpeed(weapon) {
    try {
      applyGunDataSpeed(weapon);
    } catch(e) {}
  }

  function applyRpgSpeed(weapon) {
    try {
      var data = safeReadPointer(weapon, 0x68);
      var realData = safeReadPointer(weapon, 0xF0); // WPN_RPG.realData
      if (data && realData && data.equals(realData)) {
        realData.add(0xEC).writeFloat(10.0); // WD_RPG.reloadAnimRate
        realData.add(0xF0).writeFloat(10.0); // WD_RPG.fireAnimRate
        weapon.add(0xF8).writeS32(1); // WPN_RPG.fireState = Try
      }
    } catch(e) {}
  }

  function applyWeaponSpeed(weapon) {
    if (!enabled || !weapon || weapon.isNull()) return false;
    if (!isMyWeaponFn || !getCharAnim || !setAnimSpeed) return false;

    try {
      if (!isMyWeaponFn(weapon, ptr(0))) return false;

      var animApplied = false;
      var anim = getCharAnim(weapon, ptr(0));
      if (anim && !anim.isNull()) {
        setAnimSpeed(anim, 10.0, ptr(0));
        animApplied = true;
      }

      try {
        var data = weapon.add(0x68).readPointer();
        if (data && !data.isNull()) {
          var wpnClass = data.add(0x10).readU32();

          if (wpnClass === 5 || wpnClass === 0) {
            applyGunDataSpeed(weapon);
            applyGrenadeGunSpeed(weapon);
          }

          if (wpnClass === 1 || wpnClass === 2) {
            var realData = safeReadPointer(weapon, 0xEC);
            if (realData && !realData.isNull()) {
              realData.add(0x1BC).writeU8(0);
            }
          }
        }
      } catch(e) {}

      applyGunDataSpeed(weapon);
      applyGrenadeGunSpeed(weapon);
      applyRpgSpeed(weapon);

      return animApplied;
    } catch(e) {
      return false;
    }
  }

  function getWeaponKey(weapon) {
    try {
      if (!weapon || weapon.isNull()) return null;
      return weapon.toString();
    } catch(e) {
      return null;
    }
  }

  function queuePendingWeaponSpeed(weapon) {
    var key = getWeaponKey(weapon);
    if (!key) return;
    if (pendingWeaponSpeedMap[key]) return;
    pendingWeaponSpeedMap[key] = true;
    pendingWeaponSpeedTasks.push({
      key: key,
      weapon: weapon,
      framesLeft: pendingWeaponSpeedMaxFrames
    });
  }

  function clearPendingWeaponSpeed() {
    pendingWeaponSpeedTasks = [];
    pendingWeaponSpeedMap = {};
  }

  function handleModeBaseUpdate(instance) {
    var now = Date.now();
    if (!instance || instance.isNull()) {
      clearPendingWeaponSpeed();
      modeBaseInstance = null;
      modeSwitchGraceUntil = now + modeSwitchGraceMs;
      return false;
    }

    if (!modeBaseInstance) {
      modeBaseInstance = instance;
      modeSwitchGraceUntil = now + modeSwitchGraceMs;
      return false;
    }

    if (!instance.equals(modeBaseInstance)) {
      clearPendingWeaponSpeed();
      modeBaseInstance = instance;
      modeSwitchGraceUntil = now + modeSwitchGraceMs;
      return false;
    }

    return now >= modeSwitchGraceUntil;
  }

  function notifyWeaponAcquired(weapon) {
    try {
      if (!enabled || !weapon || weapon.isNull()) return;
      if (applyWeaponSpeed(weapon) === true) return;
      queuePendingWeaponSpeed(weapon);
    } catch(e) {}
  }

  function processPendingWeaponSpeed() {
    if (pendingWeaponSpeedTasks.length === 0) return;

    var next = [];
    for (var i = 0; i < pendingWeaponSpeedTasks.length; i++) {
      var task = pendingWeaponSpeedTasks[i];
      if (!task || !task.weapon || task.framesLeft <= 0) {
        if (task && task.key) delete pendingWeaponSpeedMap[task.key];
        continue;
      }

      try {
        if (task.weapon.isNull()) {
          delete pendingWeaponSpeedMap[task.key];
          continue;
        }

        if (applyWeaponSpeed(task.weapon) === true) {
          delete pendingWeaponSpeedMap[task.key];
          continue;
        }
      } catch(e) {
        delete pendingWeaponSpeedMap[task.key];
        continue;
      }

      task.framesLeft -= 1;
      if (task.framesLeft > 0) {
        next.push(task);
      } else {
        delete pendingWeaponSpeedMap[task.key];
      }
    }
    pendingWeaponSpeedTasks = next;
  }

  return {
    enable: function() {
      if (enabled) return;
      var mod = getGameAssembly();
      if (!mod) { sendLog('error', '射速', '未找到 GameAssembly.dll'); return; }
      var base = mod.base;

      try {
        isMyWeaponFn = new NativeFunction(base.add(0xB6E1D0), "bool", ["pointer", "pointer"]);
        getCharAnim = new NativeFunction(base.add(0xB35310), "pointer", ["pointer", "pointer"]);
        setAnimSpeed = new NativeFunction(base.add(0xAA8C30), "void", ["pointer", "float", "pointer"]);
      } catch(e) {
        sendLog('error', '射速', 'NativeFunction 初始化失败: ' + e.message);
        return;
      }

      // 0) ModeBase.Update — 统一处理新获得武器的射速应用时机
      try {
        hooks.push(Interceptor.attach(base.add(0xAF6A00), {
          onEnter: function(args) {
            try {
              if (handleModeBaseUpdate(args[0])) {
                processPendingWeaponSpeed();
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendLog('warn', '射速', 'ModeBase.Update Hook失败: ' + e.message); }

      try {
        hooks.push(Interceptor.attach(base.add(0xAFAA40), {
          onEnter: function() {
            clearPendingWeaponSpeed();
            modeBaseInstance = null;
            modeSwitchGraceUntil = Date.now() + modeSwitchGraceMs;
          }
        }));
      } catch(e) { sendLog('warn', '射速', '模式切换清理 Hook失败: ' + e.message); }

      // 1) WPN_Gun.AnimSpeedSetting — 枪械(背包)动画加速（改进：onEnter立即设置）
      try {
        hooks.push(Interceptor.attach(base.add(0xB60B00), {
          onEnter: function(args) {
            this.self = args[0];
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                applyWeaponSpeed(this.self);
              }
            } catch(e) {}
          },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                applyWeaponSpeed(this.self);
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendLog('warn', '射速', 'WPN_Gun.AnimSpeedSetting Hook失败: ' + e.message); }

      // 1.5) WPN_RPG.AnimSpeedSetting — RPG/AT4 动画加速（改进：onEnter立即设置）
      try {
        hooks.push(Interceptor.attach(base.add(0xB66CA0), {
          onEnter: function(args) {
            this.self = args[0];
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                applyWeaponSpeed(this.self);
              }
            } catch(e) {}
          },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                applyWeaponSpeed(this.self);
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendLog('warn', '射速', 'WPN_RPG.AnimSpeedSetting Hook失败: ' + e.message); }

      // 1.6) WPN_GrenadeGun.AnimSpeedSetting — 榴弹枪动画加速
      try {
        hooks.push(Interceptor.attach(base.add(0xB5F7A0), {
          onEnter: function(args) {
            this.self = args[0];
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                applyWeaponSpeed(this.self);
              }
            } catch(e) {}
          },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                applyWeaponSpeed(this.self);
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendLog('warn', '射速', 'WPN_GrenadeGun.AnimSpeedSetting Hook失败: ' + e.message); }

      // 2) GunShoot — 清除射击间隔 + 半自动 => 全自动（改进：onEnter立即修改）
      try {
        hooks.push(Interceptor.attach(base.add(0xB624C0), {
          onEnter: function(args) {
            this.self = args[0];
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                isPlayerShooting = true;
                this.self.add(0xF0).writeU8(0);
                this.self.add(0x110).writeFloat(0.0);
                this.self.add(0x108).writeS32(0);
                applyWeaponSpeed(this.self);
              }
            } catch(e) {}
          },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                this.self.add(0x110).writeFloat(0.0);
                this.self.add(0x108).writeS32(0);
              }
            } catch(e) {}
            isPlayerShooting = false;
          }
        }));
      } catch(e) { sendLog('warn', '射速', 'GunShoot Hook失败: ' + e.message); }

      // 2.5) WPN_Gun.get_isSemiGun — 半自动→全自动
      try {
        hooks.push(Interceptor.attach(base.add(0xB63AD0), {
          onLeave: function(retVal) { retVal.replace(0); }
        }));
      } catch(e) { sendLog('warn', '射速', 'get_isSemiGun Hook失败: ' + e.message); }

      // 2.6) WPN_Gun.CloseZoom — 狙击镜不关闭（新增：连狙功能）
      try {
        hooks.push(Interceptor.attach(base.add(0xB60F00), {
          onEnter: function(args) {
            this.self = args[0];
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                args[1] = ptr(0);
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendLog('warn', '射速', 'CloseZoom Hook失败: ' + e.message); }

      // 2.7) Player.TryPickUpWeapon — 捡武器时立即设置动画速度（新增：补给箱处理）
      try {
        hooks.push(Interceptor.attach(base.add(0xB53F50), {
          onEnter: function(args) {
            this.wpn = args[1];
          },
          onLeave: function(retVal) {
            if (!this.wpn) return;
            if (retVal.toInt32() !== 1) return;
            try {
              if (isMyWeaponFn(this.wpn, ptr(0))) {
                notifyWeaponAcquired(this.wpn);
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendLog('warn', '射速', 'TryPickUpWeapon Hook失败: ' + e.message); }

      // 3) WPN_Gun.OnGenerateFromOwner — 补给箱枪械创建时加速
      try {
        hooks.push(Interceptor.attach(base.add(0xB62900), {
          onEnter: function(args) { this.self = args[0]; },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                notifyWeaponAcquired(this.self);
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendLog('warn', '射速', 'OnGenerateFromOwner Hook失败: ' + e.message); }

      // 4) WPN_RPG.OnGenerateFromOwner — 补给箱RPG/AT4创建时加速
      try {
        hooks.push(Interceptor.attach(base.add(0xB67740), {
          onEnter: function(args) { this.self = args[0]; },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                notifyWeaponAcquired(this.self);
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendLog('warn', '射速', 'RPG OnGenerateFromOwner Hook失败: ' + e.message); }

      // 5) WPN_RPG.OnFireBtnPressed — RPG/AT4 半自动绕过
      try {
        hooks.push(Interceptor.attach(base.add(0xB67700), {
          onEnter: function(args) { this.self = args[0]; },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                this.self.add(0xF8).writeS32(1);
                applyRpgSpeed(this.self);
              }
            } catch(e) {}
          }
        }));
      } catch(e) { sendLog('warn', '射速', 'RPG OnFireBtnPressed Hook失败: ' + e.message); }

      // 6) Recoil.OnGunShot — 清零后坐力
      try {
        hooks.push(Interceptor.attach(base.add(0xB19980), {
          onEnter: function(args) { this.self = args[0]; },
          onLeave: function(retVal) {
            if (!isPlayerShooting || !this.self) return;
            this.self.add(0x68).writeFloat(0.0);
            this.self.add(0x6C).writeFloat(0.0);
            this.self.add(0x70).writeFloat(0.0);
            this.self.add(0x74).writeFloat(0.0);
            this.self.add(0xA8).writeS32(0);
          }
        }));
      } catch(e) { sendLog('warn', '射速', 'Recoil.OnGunShot Hook失败: ' + e.message); }

      // 7) Recoil.GetCurrentPerturb — 强制 0 扩散
      try {
        hooks.push(Interceptor.attach(base.add(0xB19420), {
          onLeave: function(retVal) { retVal.replace(0.0); }
        }));
      } catch(e) { sendLog('warn', '射速', 'Recoil.GetCurrentPerturb Hook失败: ' + e.message); }

      enabled = true;
      sendLog('success', '射速', '射速变快已启用');
      sendStatus('speedgun', true);
    },
    disable: function() {
      if (!enabled) return;
      for (var i = 0; i < hooks.length; i++) {
        try { hooks[i].detach(); } catch(e) {}
      }
      hooks = [];
      clearPendingWeaponSpeed();
      modeBaseInstance = null;
      modeSwitchGraceUntil = 0;
      enabled = false;
      sendLog('info', '射速', '射速变快已禁用');
      sendStatus('speedgun', false);
    },
    isEnabled: function() { return enabled; },
    applyToWeapon: applyWeaponSpeed,
    notifyWeaponAcquired: notifyWeaponAcquired,
    processPendingWeaponSpeed: processPendingWeaponSpeed
  };
})();
