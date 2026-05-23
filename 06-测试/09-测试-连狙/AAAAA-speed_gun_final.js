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
        semiToFullAuto: true,
        keepZoom: true,
        noRecoil: true,
        noSpread: true,
        animSpeed: true
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

    function isGunWeapon(weapon) {
        try {
            var data = weapon.add(0x68).readPointer();
            if (!isSafePointer(data)) {
                return false;
            }
            var wpnClass = data.add(0x10).readS32();
            return wpnClass >= 0 && wpnClass <= 5;
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
                if (isMyWeaponFn(this.self) && isGunWeapon(this.self)) {
                    this.self.add(0x110).writeFloat(0.0);
                    this.self.add(0x108).writeS32(0);
                    this.self.add(0xF1).writeU8(1);
                    var realData = this.self.add(0xEC).readPointer();
                    if (!realData.isNull()) {
                        realData.add(0xCC).writeFloat(9999.0);
                        realData.add(0xD0).writeFloat(10.0);
                        if (CONFIG.keepZoom) {
                            realData.add(0x1BC).writeU8(0);
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

    if (CONFIG.keepZoom || CONFIG.animSpeed) {
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
                    if (isMyWeaponFn(this.self) && isGunWeapon(this.self)) {
                        if (CONFIG.keepZoom) {
                            var realData = this.self.add(0xEC).readPointer();
                            if (!realData.isNull()) {
                                realData.add(0x1BC).writeU8(0);
                            }
                        }
                    }
                    if (isMyWeaponFn(this.self)) {
                        if (CONFIG.animSpeed) {
                            var anim = getCharAnim(this.self);
                            if (!anim.isNull()) {
                                setAnimSpeed(anim, 10.0);
                            }
                        }
                    }
                    logHookLeave(this.hookName);
                } catch(e) {
                    logHookError(this.hookName + ".onLeave", e, this.context);
                }
            }
        });
    }

    if (CONFIG.semiToFullAuto) {
        Interceptor.attach(base.add(0xB63AD0), {
            onEnter: function(args) {
                this.self = args[0];
                this.hookName = "WPN_Gun.get_isSemiGun";
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
                    if (this.self && isMyWeaponFn(this.self)) {
                        retVal.replace(0);
                    }
                    logHookLeave(this.hookName);
                } catch(e) {
                    logHookError(this.hookName + ".onLeave", e, this.context);
                }
            }
        });

        Interceptor.attach(base.add(0xB6CDA0), {
            onEnter: function(args) {
                var self = args[0];
                if (!isSafePointer(self)) {
                    return;
                }
                try {
                    if (isMyWeaponFn(self) && isGunWeapon(self)) {
                        self.add(0xF0).writeU8(0);
                    }
                } catch(e) {}
            }
        });

        Interceptor.attach(base.add(0xB67700), {
            onEnter: function(args) {
                this.self = args[0];
                this.hookName = "WPN_RPG.OnFireBtnPressed";
                try {
                    logHookEnter(this.hookName, this.self);
                } catch(e) {
                    logHookError(this.hookName + ".onEnter", e, this.context);
                }
            },
            onLeave: function(retVal) {
                try {
                    if (!this.self || !isSafePointer(this.self)) {
                        logHookLeave(this.hookName);
                        return;
                    }
                    if (isMyWeaponFn(this.self)) {
                        this.self.add(0xF8).writeS32(1);
                        var realData = this.self.add(0xF0).readPointer();
                        if (!realData.isNull()) {
                            realData.add(0xF0).writeFloat(10.0);
                            realData.add(0xEC).writeFloat(10.0);
                        }
                    }
                    logHookLeave(this.hookName);
                } catch(e) {
                    logHookError(this.hookName + ".onLeave", e, this.context);
                }
            }
        });
    }

    if (CONFIG.keepZoom) {
        Interceptor.attach(base.add(0xB60F00), {
            onEnter: function(args) {
                this.self = args[0];
                this.hookName = "WPN_Gun.CloseZoom";
                try {
                    logHookEnter(this.hookName, this.self);
                    if (!isSafePointer(this.self)) {
                        return;
                    }
                    if (isMyWeaponFn(this.self)) {
                        args[1] = ptr(0);
                    }
                    logHookLeave(this.hookName);
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

    function initWeaponOnStartup() {
        try {
            var getModeBase = new NativeFunction(base.add(0x4A8170), "pointer", []);
            var modeBase = getModeBase();
            
            if (!isSafePointer(modeBase)) {
                console.log("[-] ModeBase not found, skip init");
                return;
            }
            
            var myPlayer = modeBase.add(0x6C).readPointer();
            if (!isSafePointer(myPlayer)) {
                console.log("[-] myPlayer not found, skip init");
                return;
            }
            
            var wpns = myPlayer.add(0xA0).readPointer();
            if (!isSafePointer(wpns)) {
                console.log("[-] PlayerWeapons not found, skip init");
                return;
            }
            
            var weapon = wpns.add(0x18).readPointer();
            if (!isSafePointer(weapon)) {
                console.log("[-] No weapon in use, skip init");
                return;
            }
            
            if (!isMyWeaponFn(weapon)) {
                console.log("[-] Not player weapon, skip init");
                return;
            }
            
            if (!isGunWeapon(weapon)) {
                console.log("[-] Not gun weapon, skip init");
                return;
            }
            
            var realData = weapon.add(0xEC).readPointer();
            if (realData.isNull()) {
                console.log("[-] realData is null, skip init");
                return;
            }
            
            if (CONFIG.keepZoom) {
                realData.add(0x1BC).writeU8(0);
                console.log("[+] KeepZoom initialized on startup");
            }
            
            if (CONFIG.semiToFullAuto) {
                weapon.add(0xF0).writeU8(0);
                console.log("[+] SemiToFullAuto initialized on startup");
            }
            
            weapon.add(0x110).writeFloat(0.0);
            weapon.add(0x108).writeS32(0);
            weapon.add(0xF1).writeU8(1);
            realData.add(0xCC).writeFloat(9999.0);
            realData.add(0xD0).writeFloat(10.0);
            console.log("[+] FireRate and AnimSpeed initialized on startup");
            
        } catch(e) {
            console.log("[-] initWeaponOnStartup error: " + e);
        }
    }

    initWeaponOnStartup();

    console.log("[+] Loaded with feature toggles:");
    console.log("    - Semi-auto → Full-auto: " + (CONFIG.semiToFullAuto ? "ON" : "OFF"));
    console.log("    - Keep Zoom: " + (CONFIG.keepZoom ? "ON" : "OFF"));
    console.log("    - No Recoil: " + (CONFIG.noRecoil ? "ON" : "OFF"));
    console.log("    - No Spread: " + (CONFIG.noSpread ? "ON" : "OFF"));
    console.log("    - Anim Speed x10: " + (CONFIG.animSpeed ? "ON" : "OFF"));
})();
