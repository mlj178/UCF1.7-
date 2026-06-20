// speed_gun.js - 射速变快 + 连狙 — 终极武器修改
// 10个Hook点：动画加速10x + 清除射击间隔 + 半自动→全自动 + 狙击镜不关闭 + RPG特殊处理 + 后坐力清零 + 扩散归零

modules.speedgun = (function() {
  var enabled = false;
  var hooks = [];
  var isMyWeaponFn = null;
  var getCharAnim = null;
  var setAnimSpeed = null;
  var rpgAnimSpeedFn = null;
  var grenadeAnimSpeedFn = null;
  var classGetNameFn = null;
  var isPlayerShooting = false;
  var pendingAcquiredWeapons = [];
  var acquiredWeaponRetryFrames = 3;

  function safeReadPointer(basePtr, offset) {
    try {
      if (!basePtr || basePtr.isNull()) return null;
      var value = basePtr.add(offset).readPointer();
      return (value && !value.isNull()) ? value : null;
    } catch(e) {
      return null;
    }
  }

  function getObjectClassName(object) {
    try {
      if (!classGetNameFn || !object || object.isNull()) return null;
      var klass = object.readPointer();
      if (!klass || klass.isNull()) return null;
      var name = classGetNameFn(klass);
      return (name && !name.isNull()) ? name.readUtf8String() : null;
    } catch(e) {
      return null;
    }
  }

  // 只处理 GiveWeapon 明确返回的新武器；数据对象就绪后写入一次，不扫描武器列表。
  function applyAcquiredWeaponSpeed(weapon, weaponId) {
    if (!enabled || !weapon || weapon.isNull()) return false;
    if (!isMyWeaponFn || !getCharAnim || !setAnimSpeed) return false;

    try {
      weapon.readU8();
      if (!isMyWeaponFn(weapon, ptr(0))) return false;

      var data = safeReadPointer(weapon, 0x68);
      if (!data) return false;

      var applied = false;
      var gunApplied = false;
      var rpgApplied = false;
      var gunData = safeReadPointer(weapon, 0xEC);
      if (gunData && gunData.equals(data)) {
        gunData.add(0xD0).writeFloat(10.0);
        weapon.add(0xF0).writeU8(0);
        weapon.add(0x108).writeS32(0);
        weapon.add(0x110).writeFloat(0.0);
        applied = true;
        gunApplied = true;
      }

      var rpgData = safeReadPointer(weapon, 0xF0);
      if (rpgData && rpgData.equals(data)) {
        rpgData.add(0xEC).writeFloat(10.0);
        rpgData.add(0xF0).writeFloat(10.0);
        weapon.add(0xF8).writeS32(1);
        applied = true;
        rpgApplied = true;
      }

      if (!applied) return false;

      var anim = getCharAnim(weapon, ptr(0));
      if (anim && !anim.isNull()) {
        setAnimSpeed(anim, 10.0, ptr(0));
      }

      // 特殊武器需要重新执行各自的动画倍率设置，效果才会立即反映到当前武器。
      if (weaponId === 3494 && rpgApplied && rpgAnimSpeedFn) {
        rpgAnimSpeedFn(weapon, ptr(0));
      } else if (weaponId === 2978 && gunApplied && grenadeAnimSpeedFn &&
                 getObjectClassName(data) === 'WD_GrenadeGun') {
        grenadeAnimSpeedFn(weapon, ptr(0));
      }
      return true;
    } catch(e) {
      return false;
    }
  }

  function clearAcquiredWeaponTasks() {
    pendingAcquiredWeapons = [];
  }

  function notifyWeaponAcquired(weapon, weaponId) {
    if (!enabled || !weapon || weapon.isNull()) return;

    // 只保留最后一次 GiveWeapon 返回值；双次赋予可能使第一次的对象立即失效。
    pendingAcquiredWeapons = [{
      weapon: weapon,
      weaponId: weaponId,
      delayFrames: 1,
      framesLeft: acquiredWeaponRetryFrames
    }];
  }

  function processPendingWeaponSpeed() {
    if (!enabled || pendingAcquiredWeapons.length === 0) return;

    var remaining = [];
    for (var i = 0; i < pendingAcquiredWeapons.length; i++) {
      var task = pendingAcquiredWeapons[i];
      if (!task || !task.weapon || task.weapon.isNull()) continue;

      if (task.delayFrames > 0) {
        task.delayFrames -= 1;
        remaining.push(task);
        continue;
      }

      if (applyAcquiredWeaponSpeed(task.weapon, task.weaponId)) continue;

      task.framesLeft -= 1;
      if (task.framesLeft > 0) remaining.push(task);
    }
    pendingAcquiredWeapons = remaining;
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
        rpgAnimSpeedFn = new NativeFunction(base.add(0xB66CA0), "void", ["pointer", "pointer"]);
        grenadeAnimSpeedFn = new NativeFunction(base.add(0xB5F7A0), "void", ["pointer", "pointer"]);
      } catch(e) {
        sendLog('error', '射速', 'NativeFunction 初始化失败: ' + e.message);
        return;
      }

      try {
        var classGetNameAddr = mod.findExportByName('il2cpp_class_get_name');
        if (classGetNameAddr) {
          classGetNameFn = new NativeFunction(classGetNameAddr, "pointer", ["pointer"]);
        }
      } catch(e) {
        classGetNameFn = null;
      }

      // 1) WPN_Gun.AnimSpeedSetting — 枪械(背包)动画加速（改进：onEnter立即设置）
      try {
        hooks.push(Interceptor.attach(base.add(0xB60B00), {
          onEnter: function(args) {
            this.self = args[0];
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  setAnimSpeed(anim, 10.0, ptr(0));
                }
              }
            } catch(e) {}
          },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  setAnimSpeed(anim, 10.0, ptr(0));
                }
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
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  setAnimSpeed(anim, 10.0, ptr(0));
                }
              }
            } catch(e) {}
          },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  setAnimSpeed(anim, 10.0, ptr(0));
                }
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
                var realData = this.self.add(0xEC).readPointer();
                if (!realData.isNull()) {
                  realData.add(0xD0).writeFloat(10.0);
                }
              }
            } catch(e) {}
          },
          onLeave: function(retVal) {
            if (!this.self) return;
            try {
              if (isMyWeaponFn(this.self, ptr(0))) {
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  setAnimSpeed(anim, 10.0, ptr(0));
                }
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
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  setAnimSpeed(anim, 10.0, ptr(0));
                }
                var realData = this.self.add(0xEC).readPointer();
                if (!realData.isNull()) {
                  realData.add(0x1BC).writeU8(0);
                }
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
            if ((retVal.toUInt32() & 0xFF) === 0) return;
            try {
              if (isMyWeaponFn(this.wpn, ptr(0))) {
                var anim = getCharAnim(this.wpn, ptr(0));
                if (!anim.isNull()) {
                  setAnimSpeed(anim, 10.0, ptr(0));
                }
                var data = this.wpn.add(0x68).readPointer();
                if (!data.isNull()) {
                  var wpnClass = data.add(0x10).readU32();
                  if (wpnClass === 5) {
                    var realData = this.wpn.add(0xEC).readPointer();
                    if (!realData.isNull()) {
                      realData.add(0xD0).writeFloat(10.0);
                    }
                  }
                  if (wpnClass === 1 || wpnClass === 2) {
                    var realData = this.wpn.add(0xEC).readPointer();
                    if (!realData.isNull()) {
                      realData.add(0x1BC).writeU8(0);
                    }
                  }
                }
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
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  setAnimSpeed(anim, 10.0, ptr(0));
                }
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
                var anim = getCharAnim(this.self, ptr(0));
                if (!anim.isNull()) {
                  setAnimSpeed(anim, 10.0, ptr(0));
                }
                var realData = this.self.add(0xF0).readPointer();
                if (!realData.isNull()) {
                  realData.add(0xF0).writeFloat(10.0);
                  realData.add(0xEC).writeFloat(10.0);
                }
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
                var realData = this.self.add(0xF0).readPointer();
                if (!realData.isNull()) {
                  realData.add(0xF0).writeFloat(10.0);
                  realData.add(0xEC).writeFloat(10.0);
                }
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
      clearAcquiredWeaponTasks();
      rpgAnimSpeedFn = null;
      grenadeAnimSpeedFn = null;
      classGetNameFn = null;
      enabled = false;
      sendLog('info', '射速', '射速变快已禁用');
      sendStatus('speedgun', false);
    },
    // 由武器赋予模块的 ModeBase.Update 在主线程下一帧处理。
    clearRoomState: function() {
      isPlayerShooting = false;
      clearAcquiredWeaponTasks();
    },
    notifyWeaponAcquired: notifyWeaponAcquired,
    processPendingWeaponSpeed: processPendingWeaponSpeed,
    isEnabled: function() { return enabled; }
  };
})();
