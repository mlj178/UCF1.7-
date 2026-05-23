(function() {
    console.log("[*] speed_gun_final - Modular Version with Feature Toggles");

    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) { console.log("[-] GameAssembly.dll not found!"); return; }
    var base = mod.base;

    var isMyWeaponFn = new NativeFunction(base.add(0xB6E1D0), "bool", ["pointer"]);
    var getCharAnim  = new NativeFunction(base.add(0xB35310), "pointer", ["pointer"]);
    var setAnimSpeed = new NativeFunction(base.add(0xAA8C30), "void", ["pointer", "float"]);

    var isPlayerShooting = false;

    var CONFIG = {
        animSpeed: true,
        infiniteFireRate: true,
        noRecoil: true,
        noSpread: true
    };

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
    }

    function logHookEnter(hookName, self) {
        lastHookName = hookName + ".enter";
    }

    function logHookLeave(hookName) {
    }

    function logHookError(hookName, e, ctx) {
    }

    Process.setExceptionHandler(function(details) {
        return false;
    });

    Interceptor.attach(base.add(0xB624C0), {
        onEnter: function(args) {
            this.self = args[0];
            this.hookName = "GunShoot";
            try {
                logHookEnter(this.hookName, this.self);
                if (!isSafePointer(this.self)) {
                    return;
                }
                if (isMyWeaponFn(this.self)) {
                    isPlayerShooting = true;
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
                    if (CONFIG.infiniteFireRate) {
                        this.self.add(0x110).writeFloat(0.0);
                        this.self.add(0x108).writeS32(0);
                        this.self.add(0xF1).writeU8(1);
                        var realData = this.self.add(0xEC).readPointer();
                        if (!realData.isNull()) {
                            realData.add(0xCC).writeFloat(9999.0);
                            realData.add(0xD0).writeFloat(10.0);
                        }
                    }
                }
                logHookLeave(this.hookName);
            } catch(e) {
                logHookError(this.hookName + ".onLeave", e, this.context);
            }
            isPlayerShooting = false;
        }
    });

    if (CONFIG.animSpeed) {
        Interceptor.attach(base.add(0xB60B00), {
            onEnter: function(args) {
                this.self = args[0];
                this.hookName = "WPN_Gun.AnimSpeedSetting";
                try {
                    logHookEnter(this.hookName, this.self);
                    if (!isSafePointer(this.self)) {
                        return;
                    }
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
                        }
                    }
                    logHookLeave(this.hookName);
                } catch(e) {
                    logHookError(this.hookName, e, this.context);
                }
            }
        });

        Interceptor.attach(base.add(0xB66CA0), {
            onEnter: function(args) {
                this.self = args[0];
                this.hookName = "WPN_RPG.AnimSpeedSetting";
                try {
                    logHookEnter(this.hookName, this.self);
                    if (!isSafePointer(this.self)) {
                        return;
                    }
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
                        }
                    }
                    logHookLeave(this.hookName);
                } catch(e) {
                    logHookError(this.hookName, e, this.context);
                }
            }
        });

        Interceptor.attach(base.add(0xB5F7A0), {
            onEnter: function(args) {
                this.self = args[0];
                this.hookName = "WPN_GrenadeGun.AnimSpeedSetting";
                try {
                    logHookEnter(this.hookName, this.self);
                    if (!isSafePointer(this.self)) {
                        return;
                    }
                    if (isMyWeaponFn(this.self)) {
                        var realData = this.self.add(0xEC).readPointer();
                        if (!realData.isNull()) {
                            realData.add(0xD0).writeFloat(10.0);
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
                        }
                    }
                    logHookLeave(this.hookName);
                } catch(e) {
                    logHookError(this.hookName + ".onLeave", e, this.context);
                }
            }
        });

        Interceptor.attach(base.add(0xB62900), {
            onEnter: function(args) {
                this.self = args[0];
                this.hookName = "WPN_Gun.OnGenerateFromOwner";
                try {
                    logHookEnter(this.hookName, this.self);
                    if (!isSafePointer(this.self)) {
                        return;
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
                        }
                    }
                    logHookLeave(this.hookName);
                } catch(e) {
                    logHookError(this.hookName + ".onLeave", e, this.context);
                }
            }
        });

        Interceptor.attach(base.add(0xB6CDD0), {
            onEnter: function(args) {
                this.self = args[0];
                this.hookName = "WPN_Gun.PlayCharacterShootAnim";
                try {
                    logHookEnter(this.hookName, this.self);
                    if (!isSafePointer(this.self)) {
                        return;
                    }
                    if (isMyWeaponFn(this.self)) {
                        var anim = getCharAnim(this.self);
                        if (!anim.isNull()) {
                            setAnimSpeed(anim, 10.0);
                        }
                    }
                    logHookLeave(this.hookName);
                } catch(e) {
                    logHookError(this.hookName, e, this.context);
                }
            }
        });

        Interceptor.attach(base.add(0xB67740), {
            onEnter: function(args) {
                this.self = args[0];
                this.hookName = "WPN_RPG.OnGenerateFromOwner";
                try {
                    logHookEnter(this.hookName, this.self);
                    if (!isSafePointer(this.self)) {
                        return;
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
                        }
                    }
                    logHookLeave(this.hookName);
                } catch(e) {
                    logHookError(this.hookName + ".onLeave", e, this.context);
                }
            }
        });
    }

    if (CONFIG.infiniteFireRate) {
        Interceptor.attach(base.add(0xB62170), {
            onEnter: function(args) {
                this.self = args[0];
                this.hookName = "GunShoot_Logic";
                try {
                    logHookEnter(this.hookName, this.self);
                    if (!isSafePointer(this.self)) {
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
                    }
                } catch(e) {
                    logHookError(this.hookName, e, this.context);
                }
            }
        });
    }



    if (CONFIG.noRecoil) {
        Interceptor.attach(base.add(0xB19980), {
            onEnter: function(args) {
                this.self = args[0];
                this.hookName = "Recoil.OnGunShot";
                try {
                    logHookEnter(this.hookName, this.self);
                    if (!isSafePointer(this.self)) {
                        return;
                    }
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
                    logHookLeave(this.hookName);
                } catch(e) {
                    logHookError(this.hookName + ".onLeave", e, this.context);
                }
            }
        });
    }

    if (CONFIG.noSpread) {
        var perturbCallCount = 0;
        Interceptor.replace(base.add(0xB19420), new NativeCallback(function(self) {
            perturbCallCount++;
            if (!isSafePointer(self)) {
                return 0.0;
            }
            if (!isMyWeaponFn(self)) {
                var originalFn = new NativeFunction(base.add(0xB19420), 'float', ['pointer']);
                return originalFn(self);
            }
            return 0.0;
        }, 'float', ['pointer']));
    }

    console.log("[+] Loaded with feature toggles:");
    console.log("    - Anim Speed x10: " + (CONFIG.animSpeed ? "ON" : "OFF"));
    console.log("    - Infinite Fire Rate: " + (CONFIG.infiniteFireRate ? "ON" : "OFF"));
    console.log("    - No Recoil: " + (CONFIG.noRecoil ? "ON" : "OFF"));
    console.log("    - No Spread: " + (CONFIG.noSpread ? "ON" : "OFF"));
})();
