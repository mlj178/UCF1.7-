(function() {
    console.log("[*] speed_gun_final - Dynamic Speed Control Version");

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
        fastFireRate: true,
        animSpeed: true
    };

    var SPEED_CONFIG = {
        baseFireRate: 9999.0,
        baseAnimSpeed: 10.0,
        multiplier: 1.0
    };

    function getFireRate() {
        return SPEED_CONFIG.baseFireRate * SPEED_CONFIG.multiplier;
    }

    function getAnimSpeed() {
        return SPEED_CONFIG.baseAnimSpeed * SPEED_CONFIG.multiplier;
    }

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

    function safeIsMyWeapon(weapon) {
        if (!isSafePointer(weapon)) {
            return false;
        }
        try {
            var addr = weapon.and(0xFFFFFFFF);
            if (addr.compare(0x10000) < 0) {
                return false;
            }
            return isMyWeaponFn(weapon);
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

    Process.setExceptionHandler(function(details) {
        return false;
    });

    recv(function(message) {
        if (message.type === "set_speed") {
            SPEED_CONFIG.multiplier = message.multiplier;
            send("[+] Speed multiplier set to: " + message.multiplier.toFixed(2) + "x");
        }
    });

    Interceptor.attach(base.add(0xB624C0), {
        onEnter: function(args) {
            this.self = args[0];
            try {
                if (!isSafePointer(this.self)) {
                    return;
                }
                if (safeIsMyWeapon(this.self)) {
                    isPlayerShooting = true;
                }
            } catch(e) {}
        },
        onLeave: function(retVal) {
            try {
                if (!this.self) {
                    return;
                }
                if (safeIsMyWeapon(this.self) && isGunWeapon(this.self)) {
                    if (CONFIG.fastFireRate) {
                        this.self.add(0x110).writeFloat(0.0);
                        this.self.add(0x108).writeS32(0);
                        this.self.add(0xF1).writeU8(1);
                        var realData = this.self.add(0xEC).readPointer();
                        if (!realData.isNull()) {
                            realData.add(0xCC).writeFloat(getFireRate());
                        }
                    }
                    if (CONFIG.animSpeed) {
                        var realData = this.self.add(0xEC).readPointer();
                        if (!realData.isNull()) {
                            realData.add(0xD0).writeFloat(getAnimSpeed());
                        }
                    }
                    if (CONFIG.keepZoom) {
                        var realData = this.self.add(0xEC).readPointer();
                        if (!realData.isNull()) {
                            realData.add(0x1BC).writeU8(0);
                        }
                    }
                }
            } catch(e) {}
            isPlayerShooting = false;
        }
    });

    if (CONFIG.keepZoom || CONFIG.animSpeed || CONFIG.fastFireRate) {
        Interceptor.attach(base.add(0xB62900), {
            onEnter: function(args) {
                this.self = args[0];
            },
            onLeave: function(retVal) {
                try {
                    if (!this.self) {
                        return;
                    }
                    if (safeIsMyWeapon(this.self) && isGunWeapon(this.self)) {
                        if (CONFIG.fastFireRate) {
                            this.self.add(0x110).writeFloat(0.0);
                            this.self.add(0x108).writeS32(0);
                            this.self.add(0xF1).writeU8(1);
                            var realData = this.self.add(0xEC).readPointer();
                            if (!realData.isNull()) {
                                realData.add(0xCC).writeFloat(getFireRate());
                            }
                        }
                        if (CONFIG.keepZoom) {
                            var realData = this.self.add(0xEC).readPointer();
                            if (!realData.isNull()) {
                                realData.add(0x1BC).writeU8(0);
                            }
                        }
                    }
                    if (safeIsMyWeapon(this.self)) {
                        if (CONFIG.animSpeed) {
                            var anim = getCharAnim(this.self);
                            if (!anim.isNull()) {
                                setAnimSpeed(anim, getAnimSpeed());
                            }
                        }
                    }
                } catch(e) {}
            }
        });
    }

    if (CONFIG.semiToFullAuto) {
        Interceptor.attach(base.add(0xB63AD0), {
            onEnter: function(args) {
                this.self = args[0];
            },
            onLeave: function(retVal) {
                try {
                    if (this.self && safeIsMyWeapon(this.self)) {
                        retVal.replace(0);
                    }
                } catch(e) {}
            }
        });

        Interceptor.attach(base.add(0xB6CDA0), {
            onEnter: function(args) {
                var self = args[0];
                if (!isSafePointer(self)) {
                    return;
                }
                try {
                    if (safeIsMyWeapon(self) && isGunWeapon(self)) {
                        self.add(0xF0).writeU8(0);
                    }
                } catch(e) {}
            }
        });

        Interceptor.attach(base.add(0xB67700), {
            onEnter: function(args) {
                this.self = args[0];
            },
            onLeave: function(retVal) {
                try {
                    if (!this.self || !isSafePointer(this.self)) {
                        return;
                    }
                    if (safeIsMyWeapon(this.self)) {
                        this.self.add(0xF8).writeS32(1);
                        var realData = this.self.add(0xF0).readPointer();
                        if (!realData.isNull()) {
                            var speed = getAnimSpeed();
                            realData.add(0xF0).writeFloat(speed);
                            realData.add(0xEC).writeFloat(speed);
                        }
                    }
                } catch(e) {}
            }
        });
    }

    if (CONFIG.keepZoom) {
        Interceptor.attach(base.add(0xB60F00), {
            onEnter: function(args) {
                this.self = args[0];
                try {
                    if (!isSafePointer(this.self)) {
                        return;
                    }
                    if (safeIsMyWeapon(this.self)) {
                        args[1] = ptr(0);
                    }
                } catch(e) {}
            }
        });
    }

    if (CONFIG.noRecoil) {
        Interceptor.attach(base.add(0xB19980), {
            onEnter: function(args) {
                this.self = args[0];
            },
            onLeave: function(retVal) {
                try {
                    if (!isPlayerShooting || !this.self) {
                        return;
                    }
                    this.self.add(0x68).writeFloat(0.0);
                    this.self.add(0x6C).writeFloat(0.0);
                    this.self.add(0x70).writeFloat(0.0);
                    this.self.add(0x74).writeFloat(0.0);
                    this.self.add(0xA8).writeS32(0);
                } catch(e) {}
            }
        });
    }

    if (CONFIG.noSpread) {
        Interceptor.replace(base.add(0xB19420), new NativeCallback(function(self) {
            if (!isSafePointer(self)) {
                return 0.0;
            }
            if (!safeIsMyWeapon(self)) {
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
            },
            onLeave: function(retVal) {
                try {
                    if (!this.self) {
                        return;
                    }
                    if (safeIsMyWeapon(this.self)) {
                        var anim = getCharAnim(this.self);
                        if (!anim.isNull()) {
                            setAnimSpeed(anim, getAnimSpeed());
                        }
                    }
                } catch(e) {}
            }
        });

        Interceptor.attach(base.add(0xB66CA0), {
            onEnter: function(args) {
                this.self = args[0];
            },
            onLeave: function(retVal) {
                try {
                    if (!this.self) {
                        return;
                    }
                    if (safeIsMyWeapon(this.self)) {
                        var anim = getCharAnim(this.self);
                        if (!anim.isNull()) {
                            setAnimSpeed(anim, getAnimSpeed());
                        }
                    }
                } catch(e) {}
            }
        });

        Interceptor.attach(base.add(0xB5F7A0), {
            onEnter: function(args) {
                this.self = args[0];
                try {
                    if (!isSafePointer(this.self)) {
                        return;
                    }
                    if (safeIsMyWeapon(this.self)) {
                        var realData = this.self.add(0xEC).readPointer();
                        if (!realData.isNull()) {
                            realData.add(0xD0).writeFloat(getAnimSpeed());
                        }
                    }
                } catch(e) {}
            },
            onLeave: function(retVal) {
                try {
                    if (!this.self) {
                        return;
                    }
                    if (safeIsMyWeapon(this.self)) {
                        var anim = getCharAnim(this.self);
                        if (!anim.isNull()) {
                            setAnimSpeed(anim, getAnimSpeed());
                        }
                    }
                } catch(e) {}
            }
        });

        Interceptor.attach(base.add(0xB6CDD0), {
            onEnter: function(args) {
                this.self = args[0];
                try {
                    if (!isSafePointer(this.self)) {
                        return;
                    }
                    if (safeIsMyWeapon(this.self)) {
                        var anim = getCharAnim(this.self);
                        if (!anim.isNull()) {
                            setAnimSpeed(anim, getAnimSpeed());
                        }
                    }
                } catch(e) {}
            }
        });
    }

    if (CONFIG.animSpeed || CONFIG.fastFireRate) {
        Interceptor.attach(base.add(0xB67740), {
            onEnter: function(args) {
                this.self = args[0];
            },
            onLeave: function(retVal) {
                try {
                    if (!this.self) {
                        return;
                    }
                    if (safeIsMyWeapon(this.self)) {
                        if (CONFIG.fastFireRate) {
                            this.self.add(0x110).writeFloat(0.0);
                            this.self.add(0x108).writeS32(0);
                            this.self.add(0xF1).writeU8(1);
                            var realData = this.self.add(0xEC).readPointer();
                            if (!realData.isNull()) {
                                realData.add(0xCC).writeFloat(getFireRate());
                            }
                        }
                        if (CONFIG.animSpeed) {
                            var anim = getCharAnim(this.self);
                            if (!anim.isNull()) {
                                setAnimSpeed(anim, getAnimSpeed());
                            }
                        }
                    }
                } catch(e) {}
            }
        });
    }

    console.log("[+] Loaded with feature toggles:");
    console.log("    - Semi-auto -> Full-auto: " + (CONFIG.semiToFullAuto ? "ON" : "OFF"));
    console.log("    - Keep Zoom: " + (CONFIG.keepZoom ? "ON" : "OFF"));
    console.log("    - No Recoil: " + (CONFIG.noRecoil ? "ON" : "OFF"));
    console.log("    - No Spread: " + (CONFIG.noSpread ? "ON" : "OFF"));
    console.log("    - Fast Fire Rate: " + (CONFIG.fastFireRate ? "ON" : "OFF"));
    console.log("    - Anim Speed: " + (CONFIG.animSpeed ? "ON" : "OFF"));
    console.log("[+] Speed multiplier: " + SPEED_CONFIG.multiplier.toFixed(2) + "x (adjustable via UI)");
})();
