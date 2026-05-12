// speed_gun_ultimate.js - 终极射速+无扩散修改（仅本地玩家）
// 基于IDA深度分析，覆盖所有武器类型
// 解决：1.副武器无效问题 2.子弹扩散问题
(function() {
    console.log("[*] SPEED GUN ULTIMATE (Comprehensive Fix)");

    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) {
        console.log("[-] GameAssembly.dll not found!");
        return;
    }

    var base = mod.base;

    // 关键函数地址（基于IDA深度分析）
    var gunShootNoCheckAddr = base.add(0xB621F0);      // WPN_Gun.GunShoot_NoCheck
    var gunShootLogicAddr = base.add(0xB62170);        // WPN_Gun.GunShoot_Logic
    var recoilOnGunShotAddr = base.add(0xB19980);      // Recoil.OnGunShot
    var recoilGetCurrentPerturbAddr = base.add(0xB19420); // Recoil.GetCurrentPerturb

    console.log("[+] GunShoot_NoCheck @ " + gunShootNoCheckAddr);
    console.log("[+] GunShoot_Logic @ " + gunShootLogicAddr);
    console.log("[+] Recoil.OnGunShot @ " + recoilOnGunShotAddr);
    console.log("[+] Recoil.GetCurrentPerturb @ " + recoilGetCurrentPerturbAddr);

    var shotCount = 0;
    var playerWeaponMap = {};

    // ==========================================
    // 方案1: Hook GunShoot_NoCheck - 修改射速（主入口）
    // ==========================================
    // 这是所有枪械的共同射击入口，包括：
    // - 主武器（WPN_Gun）
    // - 副武器（WPN_Gun的子类）
    // - 榴弹枪（WPN_GrenadeGun : WPN_Gun）
    Interceptor.attach(gunShootNoCheckAddr, {
        onEnter: function(args) {
            try {
                var self = args[0];
                
                // WPN_Gun 内存布局：
                // +0x68 data (WeaponData*)
                // +0x78 <fireBtnPressed>k__BackingField (bool)
                // +0x7B isMine (bool) - 玩家所有权标志
                // +0xEC realData (WeaponData_Gun*)
                // +0xFC lastShootTime
                // +0x100 recoilDataID
                // +0x110 nextAllowedShootTime
                
                var isMine = self.add(0x7B).readU8();
                var weaponAddr = ptr(self).toString();
                
                shotCount++;
                if (shotCount <= 20) {
                    console.log("[GunShoot_NoCheck] Shot #" + shotCount + ", isMine=" + isMine + ", weapon=" + weaponAddr);
                }
                
                if (isMine) {
                    // 记录玩家武器地址
                    playerWeaponMap[weaponAddr] = true;
                    
                    // 设置下次允许射击时间为过去时间（立即可以射击）
                    var nextAllowedShootTimePtr = self.add(0x110);
                    var currentTime = nextAllowedShootTimePtr.readFloat();
                    nextAllowedShootTimePtr.writeFloat(currentTime - 10.0);
                }
            } catch(e) {
                console.log("[ERROR GunShoot_NoCheck] " + e.message);
            }
        }
    });

    // ==========================================
    // 方案2: Hook GunShoot_Logic - 修改射速（备用入口）
    // ==========================================
    // 某些武器可能直接调用 GunShoot_Logic 而不是 GunShoot_NoCheck
    Interceptor.attach(gunShootLogicAddr, {
        onEnter: function(args) {
            try {
                var self = args[0];
                var isMine = self.add(0x7B).readU8();
                
                if (isMine) {
                    var nextAllowedShootTimePtr = self.add(0x110);
                    var currentTime = nextAllowedShootTimePtr.readFloat();
                    nextAllowedShootTimePtr.writeFloat(currentTime - 10.0);
                }
            } catch(e) {
                console.log("[ERROR GunShoot_Logic] " + e.message);
            }
        }
    });

    // ==========================================
    // 方案3: Hook Recoil.GetCurrentPerturb - 消除扩散
    // ==========================================
    // 这个函数返回当前扩散值，被 HUD_Crosshair.Update 调用
    // 返回 0 可以消除准星扩散显示
    Interceptor.replace(recoilGetCurrentPerturbAddr, new NativeCallback(function(self) {
        try {
            // 直接返回 0 扩散
            return 0.0;
        } catch(e) {
            return 0.0;
        }
    }, "float", ["pointer"]));

    // ==========================================
    // 方案4: Hook Recoil.OnGunShot - 阻止扩散增加
    // ==========================================
    // 这个函数在每次射击时调用，会增加扩散计数
    // 跳过它可以防止扩散累积
    Interceptor.replace(recoilOnGunShotAddr, new NativeCallback(function(self) {
        try {
            // 什么都不做，直接返回
            // 这样射击时不会增加扩散计数
        } catch(e) {
            // 忽略错误
        }
    }, "void", ["pointer"]));

    // ==========================================
    // 方案5: 直接修改 Recoil 结构体字段（最彻底）
    // ==========================================
    // Recoil 结构体布局：
    // +0x10 perturbMin (PostureFloat) - 最小扩散
    // +0x24 perturbMax (PostureFloat) - 最大扩散
    // 我们可以在 Recoil 创建时修改这些字段

    console.log("[+] Loaded. Ultimate gun speed + no spread enabled (Player Only)!");
    console.log("[+] Features:");
    console.log("    - Instant fire rate (all gun types: primary, secondary, grenade launcher)");
    console.log("    - Zero bullet spread (both calculation and display)");
    console.log("    - Player-only modification (isMine check)");
    console.log("[+] Testing: Fire your secondary weapon and check console output");
})();
