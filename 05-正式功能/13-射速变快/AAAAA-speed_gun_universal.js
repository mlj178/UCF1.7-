(function() {
    console.log("[*] speed_gun + no_recoil + no_spread (Player Only)");

    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) { console.log("[-] GameAssembly.dll not found!"); return; }
    var base = mod.base;

    var isMyWeaponFn = new NativeFunction(base.add(0xB6E1D0), "bool", ["pointer", "pointer"]);
    var isPlayerShooting = false;

    // GunShoot (RVA: 0xB624C0) — 标记玩家射击 + 清除射击间隔
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
                    this.self.add(0x110).writeFloat(0.0);
                }
            } catch(e) {}
            isPlayerShooting = false;
        }
    });

    // Recoil.OnGunShot (RVA: 0xB19980) — 清零后坐力
    Interceptor.attach(base.add(0xB19980), {
        onEnter: function(args) {
            this.self = args[0];
        },
        onLeave: function(retVal) {
            if (!isPlayerShooting || !this.self) return;
            this.self.add(0x68).writeFloat(0.0);   // addYaw
            this.self.add(0x6C).writeFloat(0.0);   // addPitch
            this.self.add(0x70).writeFloat(0.0);   // addYaw_Target
            this.self.add(0x74).writeFloat(0.0);   // addPitch_Target
            this.self.add(0xA8).writeS32(0);       // shotRepeatCount
        }
    });

    // Recoil.GetCurrentPerturb (RVA: 0xB19420) — 强制返回 0 扩散
    Interceptor.attach(base.add(0xB19420), {
        onLeave: function(retVal) {
            retVal.replace(0.0);
        }
    });

    console.log("[+] Loaded:");
    console.log("    - Infinite fire rate (player only)");
    console.log("    - No recoil (player only)");
    console.log("    - No spread (all)");
})();
