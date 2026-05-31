// speed_gun.js - 射速变快 + 连狙 — 终极武器修改
// 10个Hook点：动画加速10x + 清除射击间隔 + 半自动→全自动 + 狙击镜不关闭 + RPG特殊处理 + 后坐力清零 + 扩散归零

modules.speedgun = (function() {
  var enabled = false;
  var hooks = [];
  var isMyWeaponFn = null;
  var getCharAnim = null;
  var setAnimSpeed = null;
  var isPlayerShooting = false;

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
            if (retVal.toInt32() !== 1) return;
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
      enabled = false;
      sendLog('info', '射速', '射速变快已禁用');
      sendStatus('speedgun', false);
    },
    isEnabled: function() { return enabled; }
  };
})();
