(function() {
    console.log("[*] speed_gun_final (Player Only)");

    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) { console.log("[-] GameAssembly.dll not found!"); return; }
    var base = mod.base;

    var isMyWeaponFn = new NativeFunction(base.add(0xB6E1D0), "bool", ["pointer", "pointer"]);
    var getCharAnim  = new NativeFunction(base.add(0xB35310), "pointer", ["pointer", "pointer"]);
    var setAnimSpeed = new NativeFunction(base.add(0xAA8C30), "void", ["pointer", "float", "pointer"]);

    var isPlayerShooting = false;

    // ====== 1) AnimSpeedSetting — 所有武器动画加速 ======
    Interceptor.attach(base.add(0xB6B2D0), {
        onEnter: function(args) {
            this.self = args[0];
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
    });

    // ====== 2) GunShoot — 清除射击间隔 + 半自动 => 全自动 ======
    Interceptor.attach(base.add(0xB624C0), {
        onEnter: function(args) {
            this.self = args[0];
            try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                    isPlayerShooting = true;
                }
            } catch(e) {}
        },
        onLeave: function(retVal) {
            if (!this.self) return;
            try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                    this.self.add(0x110).writeFloat(0.0);   // nextAllowedShootTime
                    this.self.add(0x108).writeS32(0);       // semiGunFireLinkState = None
                    this.self.add(0xF0).writeU8(0);         // isSemiGun = false
                }
            } catch(e) {}
            isPlayerShooting = false;
        }
    });

    // ====== 3) WPN_Gun.OnGenerateFromOwner — 补给箱枪械创建时加速 ======
    // 补给箱武器不走 AnimSpeedSetting（跳过部署流程）
    // 这里在武器创建时补设 Animator.speed，覆盖 crate 来源
    Interceptor.attach(base.add(0xB62900), {
        onEnter: function(args) {
            this.self = args[0];
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
    });

    // ====== 4) WPN_RPG.OnGenerateFromOwner — 补给箱RPG/AT4创建时加速 ======
    // RPG 继承 Weapon 而非 WPN_Gun，独立 Hook
    Interceptor.attach(base.add(0xB67740), {
        onEnter: function(args) {
            this.self = args[0];
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
    });

    // ====== 5) WPN_RPG.OnFireBtnPressed — RPG/AT4 半自动绕过 ======
    // RPG 不走 GunShoot（WPN_RPG 继承 Weapon，不是 WPN_Gun）
    // 阻塞点：fireState 状态机（+0xF8）+ fireAnimRate 动画长
    Interceptor.attach(base.add(0xB67700), {
        onEnter: function(args) {
            this.self = args[0];
        },
        onLeave: function(retVal) {
            if (!this.self) return;
            try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                    this.self.add(0xF8).writeS32(0);       // fireState = None（绕过状态机）
                    var realData = this.self.add(0xF0).readPointer();
                    if (!realData.isNull()) {
                        realData.add(0xF0).writeFloat(10.0); // WD_RPG.fireAnimRate
                        realData.add(0xEC).writeFloat(10.0); // WD_RPG.reloadAnimRate
                    }
                }
            } catch(e) {}
        }
    });

    // ====== 6) Recoil.OnGunShot — 清零后坐力 ======
    Interceptor.attach(base.add(0xB19980), {
        onEnter: function(args) {
            this.self = args[0];
        },
        onLeave: function(retVal) {
            if (!isPlayerShooting || !this.self) return;
            this.self.add(0x68).writeFloat(0.0);    // addYaw
            this.self.add(0x6C).writeFloat(0.0);    // addPitch
            this.self.add(0x70).writeFloat(0.0);    // addYaw_Target
            this.self.add(0x74).writeFloat(0.0);    // addPitch_Target
            this.self.add(0xA8).writeS32(0);        // shotRepeatCount
        }
    });

    // ====== 7) Recoil.GetCurrentPerturb — 强制 0 扩散 ======
    Interceptor.attach(base.add(0xB19420), {
        onLeave: function(retVal) {
            retVal.replace(0.0);
        }
    });

    console.log("[+] Loaded:");
    console.log("    - Anim speed x10 (player only)");
    console.log("    - Infinite fire rate (player only)");
    console.log("    - Semi-auto \u2192 full-auto (sniper/pistol/RPG, player only)");
    console.log("    - No recoil (player only)");
    console.log("    - No spread (all)");
})();
