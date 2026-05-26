(function() {
    console.log("[*] speed_gun_final (Player Only)");

    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) { console.log("[-] GameAssembly.dll not found!"); return; }
    var base = mod.base;

    var isMyWeaponFn = new NativeFunction(base.add(0xB6E1D0), "bool", ["pointer", "pointer"]);
    var getCharAnim  = new NativeFunction(base.add(0xB35310), "pointer", ["pointer", "pointer"]);
    var setAnimSpeed = new NativeFunction(base.add(0xAA8C30), "void", ["pointer", "float", "pointer"]);

    var shootCount = 0;

    var weaponSet = {};
    var weaponSetMaxSize = 100;

    function logWpn(self, tag) {
        var addr = self.toString();
        if (!weaponSet[addr]) {
            if (Object.keys(weaponSet).length >= weaponSetMaxSize) {
                weaponSet = {};
            }
            weaponSet[addr] = true;
            var dataPtr = self.add(0x68).readPointer();
            console.log("[DBG " + tag + "] NEW weapon @" + addr + " data=" + dataPtr);
        }
    }

    // ====== 1) WPN_Gun.AnimSpeedSetting — 枪械(背包)动画加速 ======
    // 方案一：在onEnter中立即设置，确保第一发就生效
    Interceptor.attach(base.add(0xB60B00), {
        onEnter: function(args) {
            this.self = args[0];
            try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                    // 立即设置动画速度（在函数执行前）
                    var anim = getCharAnim(this.self, ptr(0));
                    if (!anim.isNull()) {
                        setAnimSpeed(anim, 10.0, ptr(0));
                    }
                }
            } catch(e) {}
        },
        onLeave: function(retVal) {
            // onLeave也设置一次，确保覆盖
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
    // 方案一：在onEnter中立即设置，确保第一发就生效
    Interceptor.attach(base.add(0xB66CA0), {
        onEnter: function(args) {
            this.self = args[0];
            try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                    // 立即设置动画速度（在函数执行前）
                    var anim = getCharAnim(this.self, ptr(0));
                    if (!anim.isNull()) {
                        setAnimSpeed(anim, 10.0, ptr(0));
                    }
                }
            } catch(e) {}
        },
        onLeave: function(retVal) {
            // onLeave也设置一次，确保覆盖
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
    // 方案一：在onEnter中立即设置，确保第一发就生效
    Interceptor.attach(base.add(0xB5F7A0), {
        onEnter: function(args) {
            this.self = args[0];
            try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                    // 立即设置realData中的动画速度
                    var realData = this.self.add(0xEC).readPointer();
                    if (!realData.isNull()) {
                        realData.add(0xD0).writeFloat(10.0);
                    }
                    
                    // 立即设置动画速度（在函数执行前）
                    var anim = getCharAnim(this.self, ptr(0));
                    if (!anim.isNull()) {
                        setAnimSpeed(anim, 10.0, ptr(0));
                    }
                }
            } catch(e) {}
        },
        onLeave: function(retVal) {
            // onLeave也设置一次，确保覆盖
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

    // ====== 2) GunShoot — 清除射击间隔 + 半自动 => 全自动 + 狙击镜不关闭 ======
    // 方案一：在onEnter中立即修改，确保第一发就生效
    Interceptor.attach(base.add(0xB624C0), {
        onEnter: function(args) {
            this.self = args[0];
            this.isMyWeapon = false;
            try {
                this.isMyWeapon = isMyWeaponFn(this.self, ptr(0));
                if (this.isMyWeapon) {
                    shootCount++;
                    logWpn(this.self, "GunShoot.onEnter");
                    
                    // 立即清除射击间隔（在射击前）
                    this.self.add(0xF0).writeU8(0);        // 清除某个标志
                    this.self.add(0x110).writeFloat(0.0);  // 清除射击间隔时间
                    this.self.add(0x108).writeS32(0);      // 清除射击计数
                    
                    // 立即设置动画速度（在射击前）
                    var anim = getCharAnim(this.self, ptr(0));
                    if (!anim.isNull()) {
                        setAnimSpeed(anim, 10.0, ptr(0));
                    }
                    
                    // 立即清除realData中的半自动标志
                    var realData = this.self.add(0xEC).readPointer();
                    if (!realData.isNull()) {
                        realData.add(0x1BC).writeU8(0);    // 清除半自动标志
                    }
                }
            } catch(e) {}
        },
        onLeave: function(retVal) {
            // onLeave保持为空，所有修改已在onEnter完成
        }
    });

    // ====== 2.5) WPN_Gun.get_isSemiGun — 半自动→全自动（返回false欺骗游戏）======
    Interceptor.attach(base.add(0xB63AD0), {
        onEnter: function(args) {
            logWpn(args[0], "get_isSemiGun");
        },
        onLeave: function(retVal) {
            retVal.replace(0);
        }
    });

    // ====== 2.6) WPN_Gun.CloseZoom — 狙击镜不关闭（阻止关闭瞄准镜函数执行）======
    Interceptor.attach(base.add(0xB60F00), {
        onEnter: function(args) {
            this.self = args[0];
            try {
                if (isMyWeaponFn(this.self, ptr(0))) {
                    args[1] = ptr(0);
                }
            } catch(e) {}
        }
    });

    // ====== 3) Player.TryPickUpWeapon — 补给箱捡武器时立即设置动画速度 ======
    Interceptor.attach(base.add(0xB53F50), {
        onEnter: function(args) {
            this.wpn = args[1];
        },
        onLeave: function(retVal) {
            if (!this.wpn) return;
            if (retVal.toInt32() !== 1) return;
            try {
                if (isMyWeaponFn(this.wpn, ptr(0))) {
                    logWpn(this.wpn, "TryPickUpWeapon");
                    
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
    });

    // ====== 4) PlayerWeapons.SetWeapon — 补给箱武器立即生效（临时修改slotType）======
    Interceptor.attach(base.add(0xB16BF0), {
        onEnter: function(args) {
            this.weapon = args[1];
            this.originalSlotType = -1;
            if (!this.weapon) return;
            try {
                var data = this.weapon.add(0x68).readPointer();
                if (!data.isNull()) {
                    var slotType = data.add(0x90).readU32();
                    if (slotType === 1) {
                        this.originalSlotType = slotType;
                        data.add(0x90).writeU32(0);
                        logWpn(this.weapon, "SetWeapon.fixSlotType");
                    }
                }
            } catch(e) {}
        },
        onLeave: function(retVal) {
            if (!this.weapon) return;
            if (this.originalSlotType === -1) return;
            try {
                var data = this.weapon.add(0x68).readPointer();
                if (!data.isNull()) {
                    data.add(0x90).writeU32(this.originalSlotType);
                }
            } catch(e) {}
        }
    });

    // ====== 5) WPN_RPG.OnFireBtnPressed — RPG/AT4 半自动绕过 ======
    // 方案一：在onEnter中立即修改，确保第一发就生效
    Interceptor.attach(base.add(0xB67700), {
        onEnter: function(args) {
            this.self = args[0];
            this.isMyWeapon = false;
            logWpn(this.self, "RPG.OnFireBtnPressed");
            try {
                this.isMyWeapon = isMyWeaponFn(this.self, ptr(0));
                if (this.isMyWeapon) {
                    // 立即修改RPG状态（在射击前）
                    this.self.add(0xF8).writeS32(1);
                    
                    // 立即设置realData中的动画速度
                    var realData = this.self.add(0xF0).readPointer();
                    if (!realData.isNull()) {
                        realData.add(0xF0).writeFloat(10.0);
                        realData.add(0xEC).writeFloat(10.0);
                    }
                    
                    // 立即设置动画速度（在射击前）
                    var anim = getCharAnim(this.self, ptr(0));
                    if (!anim.isNull()) {
                        setAnimSpeed(anim, 10.0, ptr(0));
                    }
                }
            } catch(e) {}
        },
        onLeave: function(retVal) {
            // onLeave保持为空，所有修改已在onEnter完成
        }
    });

    // ====== 5.5) WPN_RPG.Fire — RPG/AT4 发射时确保动画速度（补给箱立即生效）======
    Interceptor.attach(base.add(0xB670A0), {
        onEnter: function(args) {
            this.self = args[0];
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
    });

    // ====== 6) Recoil.OnGunShot — 清零后坐力 ======
    Interceptor.attach(base.add(0xB19980), {
        onEnter: function(args) {
            this.self = args[0];
            this.shootId = shootCount;
        },
        onLeave: function(retVal) {
            if (!this.self) return;
            if (this.shootId !== shootCount) return;
            try {
                this.self.add(0x68).writeFloat(0.0);
                this.self.add(0x6C).writeFloat(0.0);
                this.self.add(0x70).writeFloat(0.0);
                this.self.add(0x74).writeFloat(0.0);
                this.self.add(0xA8).writeS32(0);
            } catch(e) {}
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
    console.log("    - Semi-auto -> full-auto (sniper/pistol/RPG, player only)");
    console.log("    - Keep zoom (sniper scope stays open after shooting)");
    console.log("    - Supply box weapons instant effect (fix slotType)");
    console.log("    - No recoil (player only)");
    console.log("    - No spread (all)");
})();
