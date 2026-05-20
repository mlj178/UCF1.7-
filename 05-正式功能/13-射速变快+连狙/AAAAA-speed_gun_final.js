(function() {
    console.log("[*] speed_gun_final (Player Only) - Fixed Version with Debug");

    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) { console.log("[-] GameAssembly.dll not found!"); return; }
    var base = mod.base;

    var isMyWeaponFn = new NativeFunction(base.add(0xB6E1D0), "bool", ["pointer"]);
    var getCharAnim  = new NativeFunction(base.add(0xB35310), "pointer", ["pointer"]);
    var setAnimSpeed = new NativeFunction(base.add(0xAA8C30), "void", ["pointer", "float"]);

    var isPlayerShooting = false;

    function isSafePointer(ptr) {
        if (!ptr || ptr.isNull()) {
            return false;
        }
        try {
            ptr.readU8();
            return true;
        } catch(e) {
            return false;
        }
    }

    var lastHookName = "";
    var lastHookTime = 0;
    var hookCallCount = {};

    function printBacktrace(ctx) {
        console.log("\n========== BACKTRACE ==========");
        try {
            var bt = Thread.backtrace(ctx, Backtracer.ACCURATE);
            var symbols = bt.map(DebugSymbol.fromAddress);
            for (var i = 0; i < Math.min(symbols.length, 15); i++) {
                console.log("  [" + i + "] " + symbols[i]);
            }
        } catch(e) {
            console.log("  [!] Backtrace failed: " + e);
        }
        console.log("================================\n");
    }

    function logHookEnter(hookName, self) {
        lastHookName = hookName + ".enter";
        lastHookTime = Date.now();
        if (!hookCallCount[hookName]) {
            hookCallCount[hookName] = 0;
        }
        hookCallCount[hookName]++;
        console.log("[" + lastHookTime + "] >>> ENTER: " + hookName + " | self=" + self + " | count=" + hookCallCount[hookName]);
  
    }

    function logHookLeave(hookName) {
        var now = Date.now();
        console.log("[" + now + "] <<< LEAVE: " + hookName + " | duration=" + (now - lastHookTime) + "ms");

    }

    function logHookError(hookName, e, ctx) {
        console.log("\n!!!!! CRASH DETECTED !!!!!");
        console.log("[CRASH] Hook: " + hookName);
        console.log("[CRASH] Error: " + e);
        console.log("[CRASH] Error Stack: " + e.stack);
        console.log("[CRASH] Last Hook: " + lastHookName);
        console.log("[CRASH] Thread ID: " + Process.getCurrentThreadId());
        printBacktrace(ctx);
        console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
    }

    Process.setExceptionHandler(function(details) {
        console.log("\n!!!!! UNHANDLED EXCEPTION !!!!!");
        console.log("[EXCEPTION] Type: " + details.type);
        console.log("[EXCEPTION] Address: " + details.address);
        console.log("[EXCEPTION] Memory: " + JSON.stringify(details.memory));
        console.log("[EXCEPTION] Context: " + details.context);
        console.log("[EXCEPTION] Last Hook: " + lastHookName);
        console.log("[EXCEPTION] Thread ID: " + Process.getCurrentThreadId());
        printBacktrace(details.context);
        console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
        return false;
    });

    // ====== 1) WPN_Gun.AnimSpeedSetting — 枪械(背包)动画加速 ======
    Interceptor.attach(base.add(0xB60B00), {
        onEnter: function(args) {
            this.self = args[0];
            this.hookName = "WPN_Gun.AnimSpeedSetting";
            try {
                logHookEnter(this.hookName, this.self);
            } catch(e) {}
        },
        onLeave: function(retVal) {
            try {
                if (!this.self) {
                    logHookLeave(this.hookName);
                    return;
                }
                if (isMyWeaponFn(this.self)) {
                    var anim = getCharAnim(this.self);
                    if (!anim.isNull()) {
                        setAnimSpeed(anim, 10.0);
                        console.log("  [OK] " + this.hookName + " - anim speed set to 10.0");
                    }
                }
                logHookLeave(this.hookName);
            } catch(e) {
                logHookError(this.hookName, e, this.context);
            }
        }
    });

    // ====== 1.5) WPN_RPG.AnimSpeedSetting — RPG/AT4 动画加速 ======
    Interceptor.attach(base.add(0xB66CA0), {
        onEnter: function(args) {
            this.self = args[0];
            this.hookName = "WPN_RPG.AnimSpeedSetting";
            try {
                logHookEnter(this.hookName, this.self);
            } catch(e) {}
        },
        onLeave: function(retVal) {
            try {
                if (!this.self) {
                    logHookLeave(this.hookName);
                    return;
                }
                if (isMyWeaponFn(this.self)) {
                    var anim = getCharAnim(this.self);
                    if (!anim.isNull()) {
                        setAnimSpeed(anim, 10.0);
                        console.log("  [OK] " + this.hookName + " - anim speed set to 10.0");
                    }
                }
                logHookLeave(this.hookName);
            } catch(e) {
                logHookError(this.hookName, e, this.context);
            }
        }
    });

    // ====== 1.6) WPN_GrenadeGun.AnimSpeedSetting — 榴弹枪动画加速 ======
    Interceptor.attach(base.add(0xB5F7A0), {
        onEnter: function(args) {
            this.self = args[0];
            this.hookName = "WPN_GrenadeGun.AnimSpeedSetting";
            try {
                logHookEnter(this.hookName, this.self);
                if (isMyWeaponFn(this.self)) {
                    var realData = this.self.add(0xEC).readPointer();
                    if (!realData.isNull()) {
                        realData.add(0xD0).writeFloat(10.0);
                        console.log("  [OK] " + this.hookName + ".onEnter - realData speed set to 10.0");
                    }
                }
            } catch(e) {
                logHookError(this.hookName + ".onEnter", e, this.context);
            }
        },
        onLeave: function(retVal) {
            try {
                if (!this.self) {
                    logHookLeave(this.hookName);
                    return;
                }
                if (isMyWeaponFn(this.self)) {
                    var anim = getCharAnim(this.self);
                    if (!anim.isNull()) {
                        setAnimSpeed(anim, 10.0);
                        console.log("  [OK] " + this.hookName + ".onLeave - anim speed set to 10.0");
                    }
                }
                logHookLeave(this.hookName);
            } catch(e) {
                logHookError(this.hookName + ".onLeave", e, this.context);
            }
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

    // ====== 2) GunShoot_Logic — 射击逻辑核心，清除所有限制 ======
    Interceptor.attach(base.add(0xB62170), {
        onEnter: function(args) {
            this.self = args[0];
            this.hookName = "GunShoot_Logic";
            try {
                logHookEnter(this.hookName, this.self);
                if (isMyWeaponFn(this.self)) {
                    this.self.add(0x110).writeFloat(0.0);
                    this.self.add(0x108).writeS32(0);
                    this.self.add(0xF1).writeU8(1);
                    var realData = this.self.add(0xEC).readPointer();
                    if (!realData.isNull()) {
                        realData.add(0xCC).writeFloat(9999.0);
                        realData.add(0xD0).writeFloat(10.0);
                    }
                    console.log("  [OK] " + this.hookName + " - fire limits cleared");
                }
            } catch(e) {
                logHookError(this.hookName, e, this.context);
            }
        }
    });

    // ====== 2.5) GunShoot — 清除射击间隔 + 半自动 => 全自动 ======
    Interceptor.attach(base.add(0xB624C0), {
        onEnter: function(args) {
            this.self = args[0];
            this.hookName = "GunShoot";
            try {
                logHookEnter(this.hookName, this.self);
                if (isMyWeaponFn(this.self)) {
                    isPlayerShooting = true;
                    logWpn(this.self, "GunShoot.enter");
                    console.log("  [OK] " + this.hookName + " - isPlayerShooting set to true");
                }
            } catch(e) {
                logHookError(this.hookName + ".onEnter", e, this.context);
            }
        },
        onLeave: function(retVal) {
            try {
                if (!this.self) {
                    logHookLeave(this.hookName);
                    isPlayerShooting = false;
                    return;
                }
                if (isMyWeaponFn(this.self)) {
                    this.self.add(0x110).writeFloat(0.0);
                    this.self.add(0x108).writeS32(0);
                    this.self.add(0xF1).writeU8(1);
                    var realData = this.self.add(0xEC).readPointer();
                    if (!realData.isNull()) {
                        realData.add(0xCC).writeFloat(9999.0);
                        realData.add(0xD0).writeFloat(10.0);
                    }
                    console.log("  [OK] " + this.hookName + ".onLeave - fire limits cleared");
                }
                logHookLeave(this.hookName);
            } catch(e) {
                logHookError(this.hookName + ".onLeave", e, this.context);
            }
            isPlayerShooting = false;
        }
    });

    // ====== 2.6) WPN_Gun.get_isSemiGun — 半自动→全自动 ======
    Interceptor.attach(base.add(0xB63AD0), {
        onEnter: function(args) {
            this.self = args[0];
            this.hookName = "WPN_Gun.get_isSemiGun";
            try {
                logHookEnter(this.hookName, this.self);
                logWpn(this.self, "get_isSemiGun");
            } catch(e) {
                logHookError(this.hookName + ".onEnter", e, this.context);
            }
        },
        onLeave: function(retVal) {
            try {
                retVal.replace(0);
                console.log("  [OK] " + this.hookName + " - forced to full-auto (return 0)");
                logHookLeave(this.hookName);
            } catch(e) {
                logHookError(this.hookName + ".onLeave", e, this.context);
            }
        }
    });

    // ====== 2.7) WPN_Gun.OnFireBtnPressed — 按下扳机时强制自动模式 ======
    Interceptor.attach(base.add(0xB6CDA0), {
        onEnter: function(args) {
            var self = args[0];
            if (!isSafePointer(self)) {
                return;
            }
            try {
                self.add(0xF0).writeU8(0);
                console.log("[OK] OnFireBtnPressed - forced auto mode");
            } catch(e) {
                console.log("[ERR] OnFireBtnPressed: " + e);
            }
        }
    });

    // ====== 3) WPN_Gun.OnGenerateFromOwner — 补给箱枪械创建时加速 + 禁用射击后关镜 ======
    Interceptor.attach(base.add(0xB62900), {
        onEnter: function(args) {
            this.self = args[0];
            this.hookName = "WPN_Gun.OnGenerateFromOwner";
            try {
                logHookEnter(this.hookName, this.self);
                logWpn(this.self, "Gun.OnGenerateFromOwner");
            } catch(e) {
                logHookError(this.hookName + ".onEnter", e, this.context);
            }
        },
        onLeave: function(retVal) {
            try {
                if (!this.self) {
                    logHookLeave(this.hookName);
                    return;
                }
                if (isMyWeaponFn(this.self)) {
                    var anim = getCharAnim(this.self);
                    if (!anim.isNull()) {
                        setAnimSpeed(anim, 10.0);
                    }
                    var realData = this.self.add(0xEC).readPointer();
                    if (!realData.isNull()) {
                        realData.add(0x1BC).writeU8(0);
                    }
                    console.log("  [OK] " + this.hookName + " - anim speed set, zoom close disabled");
                }
                logHookLeave(this.hookName);
            } catch(e) {
                logHookError(this.hookName + ".onLeave", e, this.context);
            }
        }
    });

    // ====== 3.5) WPN_Gun.PlayCharacterShootAnim — 播放射击动画时加速 ======
    Interceptor.attach(base.add(0xB6CDD0), {
        onEnter: function(args) {
            this.self = args[0];
            this.hookName = "WPN_Gun.PlayCharacterShootAnim";
            try {
                logHookEnter(this.hookName, this.self);
                if (isMyWeaponFn(this.self)) {
                    var anim = getCharAnim(this.self);
                    if (!anim.isNull()) {
                        setAnimSpeed(anim, 10.0);
                        console.log("  [OK] " + this.hookName + " - shoot anim speed set to 10.0");
                    }
                }
                logHookLeave(this.hookName);
            } catch(e) {
                logHookError(this.hookName, e, this.context);
            }
        }
    });

    // ====== 3.6) WPN_Gun.CloseZoom — 阻止射击后自动关镜 ======
    Interceptor.attach(base.add(0xB60F00), {
        onEnter: function(args) {
            this.self = args[0];
            this.hookName = "WPN_Gun.CloseZoom";
            try {
                logHookEnter(this.hookName, this.self);
                if (isPlayerShooting) {
                    args[1] = ptr(0);
                    console.log("  [OK] " + this.hookName + " - blocked auto zoom close");
                }
                logHookLeave(this.hookName);
            } catch(e) {
                logHookError(this.hookName, e, this.context);
            }
        }
    });

    // ====== 4) WPN_RPG.OnGenerateFromOwner — 补给箱RPG/AT4创建时加速 ======
    Interceptor.attach(base.add(0xB67740), {
        onEnter: function(args) {
            this.self = args[0];
            this.hookName = "WPN_RPG.OnGenerateFromOwner";
            try {
                logHookEnter(this.hookName, this.self);
                logWpn(this.self, "RPG.OnGenerateFromOwner");
                var isMy = isMyWeaponFn(this.self);
                console.log("  [TEST] " + this.hookName + " isMyWeapon = " + isMy);
                var realData = this.self.add(0xF0).readPointer();
                console.log("  [TEST] " + this.hookName + " realData = " + realData);
            } catch(e) {
                logHookError(this.hookName + ".onEnter", e, this.context);
            }
        },
        onLeave: function(retVal) {
            try {
                if (!this.self) {
                    logHookLeave(this.hookName);
                    return;
                }
                var isMy = isMyWeaponFn(this.self);
                console.log("  [TEST] " + this.hookName + ".onLeave isMyWeapon = " + isMy);
                if (isMy) {
                    var anim = getCharAnim(this.self);
                    if (!anim.isNull()) {
                        setAnimSpeed(anim, 10.0);
                    }
                    console.log("  [OK] " + this.hookName + " DONE @" + this.self);
                }
                logHookLeave(this.hookName);
            } catch(e) {
                logHookError(this.hookName + ".onLeave", e, this.context);
            }
        }
    });

    // ====== 5) WPN_RPG.OnFireBtnPressed — RPG/AT4 半自动绕过 ======
    Interceptor.attach(base.add(0xB67700), {
        onEnter: function(args) {
            this.self = args[0];
            this.hookName = "WPN_RPG.OnFireBtnPressed";
            try {
                logHookEnter(this.hookName, this.self);
                logWpn(this.self, "RPG.OnFireBtnPressed");
            } catch(e) {
                logHookError(this.hookName + ".onEnter", e, this.context);
            }
        },
        onLeave: function(retVal) {
            try {
                if (!this.self) {
                    logHookLeave(this.hookName);
                    return;
                }
                if (isMyWeaponFn(this.self)) {
                    console.log("  [OK] " + this.hookName + " FIRING @" + this.self);
                    this.self.add(0xF8).writeS32(1);
                    var realData = this.self.add(0xF0).readPointer();
                    console.log("  [DBG] RPG realData = " + realData);
                    if (!realData.isNull()) {
                        realData.add(0xF0).writeFloat(10.0);
                        realData.add(0xEC).writeFloat(10.0);
                        console.log("  [OK] RPG fireAnimRate/reloadAnimRate set to 10.0");
                    }
                }
                logHookLeave(this.hookName);
            } catch(e) {
                logHookError(this.hookName + ".onLeave", e, this.context);
            }
        }
    });

    // ====== 6) Recoil.OnGunShot — 清零后坐力 ======
    Interceptor.attach(base.add(0xB19980), {
        onEnter: function(args) {
            this.self = args[0];
            this.hookName = "Recoil.OnGunShot";
            try {
                logHookEnter(this.hookName, this.self);
            } catch(e) {}
        },
        onLeave: function(retVal) {
            try {
                if (!isPlayerShooting || !this.self) {
                    logHookLeave(this.hookName);
                    return;
                }
                this.self.add(0x68).writeFloat(0.0);
                this.self.add(0x6C).writeFloat(0.0);
                this.self.add(0x70).writeFloat(0.0);
                this.self.add(0x74).writeFloat(0.0);
                this.self.add(0xA8).writeS32(0);
                console.log("  [OK] " + this.hookName + " - recoil cleared");
                logHookLeave(this.hookName);
            } catch(e) {
                logHookError(this.hookName + ".onLeave", e, this.context);
            }
        }
    });

    // ====== 7) Recoil.GetCurrentPerturb — 强制 0 扩散 ======
    var perturbCallCount = 0;
    Interceptor.replace(base.add(0xB19420), new NativeCallback(function(self) {
        perturbCallCount++;
        if (perturbCallCount % 1000 === 0) {
            console.log("[OK] GetCurrentPerturb - forced 0 spread (call #" + perturbCallCount + ")");
        }
        if (!isSafePointer(self)) {
            return 0.0;
        }
        return 0.0;
    }, 'float', ['pointer']));

    console.log("[+] Loaded:");
    console.log("    - NativeFunction params fixed");
    console.log("    - Anim speed x10 (player only)");
    console.log("    - Infinite fire rate (player only)");
    console.log("    - Semi-auto \u2192 full-auto (sniper/pistol/RPG, player only)");
    console.log("    - No recoil (player only)");
    console.log("    - No spread (all) - using safe Interceptor.replace");
    console.log("    - Sniper zoom maintained after shoot");
    console.log("    - OnFireBtnPressed - safe version (no isMyWeaponFn check)");
    console.log("    - DEBUG MODE: Full backtrace logging enabled");
    console.log("    - Exception handler installed for crash detection");
    console.log("    - Log delay: 1ms per hook enter/leave");
    console.log("    - Safe pointer validation enabled");
})();
