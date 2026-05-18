(function() {
    console.log("[*] speed_gun_final (Player Only)");

    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) { console.log("[-] GameAssembly.dll not found!"); return; }
    var base = mod.base;

    var isMyWeaponFn = new NativeFunction(base.add(0xB6E1D0), "bool", ["pointer", "pointer"]);
    var getCharAnim  = new NativeFunction(base.add(0xB35310), "pointer", ["pointer", "pointer"]);
    var setAnimSpeed = new NativeFunction(base.add(0xAA8C30), "void", ["pointer", "float", "pointer"]);

    var isPlayerShooting = false;

    // ====== 1) WPN_Gun.AnimSpeedSetting — 枪械(背包)动画加速 ======
    Interceptor.attach(base.add(0xB60B00), {
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

    // ====== 1.5) WPN_RPG.AnimSpeedSetting — RPG/AT4 动画加速 ======
    Interceptor.attach(base.add(0xB66CA0), {
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

    // ====== 1.6) WPN_GrenadeGun.AnimSpeedSetting — 榴弹枪动画加速 ======
    Interceptor.attach(base.add(0xB5F7A0), {
        onEnter: function(args) {
            this.self = args[0];
            try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                    var realData = this.self.add(0xEC).readPointer();
                    if (!realData.isNull()) {
                        realData.add(0xD0).writeFloat(10.0); // fireAnimMultiplier
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
    });

    var weaponSet = {};

    function logWpn(self, tag) {
        var addr = self.toString();
        if (!weaponSet[addr]) {
            weaponSet[addr] = true;
            var rdp = self.add(0xF0).readPointer();
            var dataPtr = self.add(0x68).readPointer();
            console.log("[DBG " + tag + "] NEW weapon @" + addr + " data=" + dataPtr + " +0xF0_val=" + rdp);
        }
    }

    // ====== 2) GunShoot — 清除射击间隔 + 半自动 => 全自动 ======
    Interceptor.attach(base.add(0xB624C0), {
        onEnter: function(args) {
            this.self = args[0];
            try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                    isPlayerShooting = true;
                    logWpn(this.self, "GunShoot.enter");
                }
            } catch(e) {}
        },
        onLeave: function(retVal) {
            if (!this.self) return;
            try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                    this.self.add(0x110).writeFloat(0.0);   // nextAllowedShootTime
                    this.self.add(0x108).writeS32(0);       // semiGunFireLinkState = None
                }
            } catch(e) {}
            isPlayerShooting = false;
        }
    });

    // ====== 2.5) WPN_Gun.get_isSemiGun — 半自动→全自动（不写内存，不影响 RPG 的 realData 指针）======
    Interceptor.attach(base.add(0xB63AD0), {
        onEnter: function(args) {
            logWpn(args[0], "get_isSemiGun");
        },
        onLeave: function(retVal) {
            retVal.replace(0);
        }
    });

    // ====== 3) WPN_Gun.OnGenerateFromOwner — 补给箱枪械创建时加速 ======
    Interceptor.attach(base.add(0xB62900), {
        onEnter: function(args) {
            this.self = args[0];
            logWpn(this.self, "Gun.OnGenerateFromOwner");
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
    Interceptor.attach(base.add(0xB67740), {
        onEnter: function(args) {
            this.self = args[0];
            logWpn(this.self, "RPG.OnGenerateFromOwner");
            try {
                var isMy = isMyWeaponFn(this.self, ptr(0));
                console.log("[TEST] RPG.OnGenerateFromOwner isMyWeapon = " + isMy);
                var realData = this.self.add(0xF0).readPointer();
                console.log("[TEST] RPG.OnGenerateFromOwner realData = " + realData);
            } catch(e) {
                console.log("[TEST] RPG.OnGenerateFromOwner ERROR: " + e);
            }
        },
        onLeave: function(retVal) {
            if (!this.self) return;
            try {
                var isMy = isMyWeaponFn(this.self, ptr(0));
                console.log("[TEST] RPG.OnGenerateFromOwner onLeave isMyWeapon = " + isMy);
                if (isMy) {
                    var anim = getCharAnim(this.self, ptr(0));
                    if (!anim.isNull()) {
                        setAnimSpeed(anim, 10.0, ptr(0));
                    }
                    console.log("[DBG] RPG.OnGenerateFromOwner DONE @" + this.self);
                }
            } catch(e) {}
        }
    });

    // ====== 5) WPN_RPG.OnFireBtnPressed — RPG/AT4 半自动绕过 ======
    Interceptor.attach(base.add(0xB67700), {
        onEnter: function(args) {
            this.self = args[0];
            logWpn(this.self, "RPG.OnFireBtnPressed");
        },
        onLeave: function(retVal) {
            if (!this.self) return;
            try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                    console.log("[DBG] RPG.OnFireBtnPressed FIRING @" + this.self);
                    this.self.add(0xF8).writeS32(1);       // fireState = Firing (保持触发)
                    var realData = this.self.add(0xF0).readPointer();
                    console.log("[DBG] RPG realData = " + realData);
                    if (!realData.isNull()) {
                        realData.add(0xF0).writeFloat(10.0); // WD_RPG.fireAnimRate
                        realData.add(0xEC).writeFloat(10.0); // WD_RPG.reloadAnimRate
                        console.log("[DBG] RPG fireAnimRate/reloadAnimRate set to 10.0");
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
            this.self.add(0x68).writeFloat(0.0);
            this.self.add(0x6C).writeFloat(0.0);
            this.self.add(0x70).writeFloat(0.0);
            this.self.add(0x74).writeFloat(0.0);
            this.self.add(0xA8).writeS32(0);
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
