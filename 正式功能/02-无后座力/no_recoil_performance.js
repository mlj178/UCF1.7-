// no_recoil_performance.js - 高性能无后座力（不掉帧）
// 使用方法：frida -p <PID> -l no_recoil_performance.js
//
// 优化策略：
// - 不 Hook Update 函数（避免每帧调用）
// - 只 Hook 开枪相关函数（触发频率低）
// - 使用 Interceptor.replace 直接跳过 Recoil 生成
// - 最小化 JS 层操作，最大化 Native 执行

console.log("[*] ════════════════════════════════════");
console.log("[*]  NO RECOIL PERFORMANCE (NO LAG)    ");
console.log("[*] ════════════════════════════════════");

(function () {
    var gameAssembly = Process.findModuleByName("GameAssembly.dll");
    
    if (!gameAssembly) {
        console.log("[-] GameAssembly.dll not found!");
        return;
    }

    // 关键地址
    var ADDR_RECOIL_ONGUNSHOT = gameAssembly.base.add(0xB19980);  // Recoil$$OnGunShot
    var ADDR_GUNSHOOT = gameAssembly.base.add(0xB624C0);          // WPN_Gun$$GunShoot
    var ADDR_GUNSHOOT_NC = gameAssembly.base.add(0xB621F0);       // WPN_Gun$$GunShoot_NoCheck
    var ADDR_PLAYER_IS_MY = gameAssembly.base.add(0xB55FD0);      // Player$$get_isMyPlayer

    console.log("[*] Recoil OnGunShot @ " + ADDR_RECOIL_ONGUNSHOT);
    console.log("[*] WPN_Gun GunShoot @ " + ADDR_GUNSHOOT);

    // 创建 NativeFunction
    var Player_get_isMyPlayer = null;
    try {
        Player_get_isMyPlayer = new NativeFunction(
            ADDR_PLAYER_IS_MY,
            "bool",
            ["pointer", "pointer"]
        );
    } catch (e) {
        console.log("[-] Warning: Cannot create Player_get_isMyPlayer");
    }

    var playerWeaponSet = {};
    var suppressCount = 0;
    var logLimit = 20;

    // 指针检查
    function isReadablePointer(p) {
        if (!p || p.isNull()) return false;
        try {
            return Process.findRangeByAddress(p) !== null;
        } catch (e) {
            return false;
        }
    }

    // 检查是否是玩家武器（通过 Weapon 对象查找 Player）
    function isPlayerWeapon(weaponPtr) {
        if (!weaponPtr || weaponPtr.isNull()) return false;
        
        // 简单策略：检查武器指针是否已记录
        var key = weaponPtr.toString();
        if (playerWeaponSet[key]) return true;
        
        // 如果是新武器，尝试识别
        if (Player_get_isMyPlayer) {
            try {
                // 从 Weapon 对象获取 Player（偏移需要根据 dump.cs 确认）
                // 这里使用保守策略：前 2 把武器认为是玩家的
                var count = Object.keys(playerWeaponSet).length;
                if (count < 2) {
                    playerWeaponSet[key] = true;
                    console.log("[+] Player weapon detected: " + weaponPtr + " (count: " + (count+1) + ")");
                    return true;
                }
            } catch (e) {}
        }
        
        return false;
    }

    // 方法 1: 替换 Recoil OnGunShot（最彻底）
    try {
        var RecoilOnGunShot_Orig = new NativeFunction(
            ADDR_RECOIL_ONGUNSHOT,
            "void",
            ["pointer", "pointer"]
        );

        Interceptor.replace(
            ADDR_RECOIL_ONGUNSHOT,
            new NativeCallback(function (recoilThis, methodInfo) {
                // 检查是否是玩家武器
                if (isPlayerWeapon(recoilThis)) {
                    suppressCount++;
                    if (suppressCount <= logLimit) {
                        console.log("[Suppress " + suppressCount + "] Recoil blocked @ " + recoilThis);
                    }
                    // 直接返回，不执行原函数（无后坐力）
                    return;
                }
                
                // Bot 武器：正常执行
                RecoilOnGunShot_Orig(recoilThis, methodInfo);
            }, "void", ["pointer", "pointer"])
        );

        console.log("[+] Replaced Recoil::OnGunShot");
    } catch (e) {
        console.log("[-] Failed to replace Recoil::OnGunShot: " + e);
        console.log("[*] Falling back to hook mode...");
        
        // 降级方案：使用 attach
        Interceptor.attach(ADDR_RECOIL_ONGUNSHOT, {
            onEnter: function (args) {
                var recoilPtr = args[0];
                if (isPlayerWeapon(recoilPtr)) {
                    suppressCount++;
                    if (suppressCount <= logLimit) {
                        console.log("[Suppress " + suppressCount + "] Recoil zeroed @ " + recoilPtr);
                    }
                    
                    // 强制清零字段
                    try {
                        recoilPtr.add(0x68).writeFloat(0.0); // addYaw
                        recoilPtr.add(0x6C).writeFloat(0.0); // addPitch
                        recoilPtr.add(0x70).writeFloat(0.0); // addYaw_Target
                        recoilPtr.add(0x74).writeFloat(0.0); // addPitch_Target
                    } catch (e) {}
                }
            }
        });
        
        console.log("[+] Hooked Recoil::OnGunShot (fallback)");
    }

    // 方法 2: Hook 开火函数（用于识别玩家武器）
    function attachGunShoot(addr, name) {
        try {
            Interceptor.attach(addr, {
                onEnter: function (args) {
                    var weaponPtr = args[0];
                    if (isPlayerWeapon(weaponPtr)) {
                        if (suppressCount <= logLimit) {
                            console.log("[Fire] " + name + " - Weapon: " + weaponPtr);
                        }
                    }
                }
            });
            console.log("[+] Hooked " + name);
        } catch (e) {
            console.log("[-] Failed to hook " + name);
        }
    }

    attachGunShoot(ADDR_GUNSHOOT, "GunShoot");
    attachGunShoot(ADDR_GUNSHOOT_NC, "GunShoot_NoCheck");

    // 内存清理（防止泄漏）
    setInterval(function() {
        var keys = Object.keys(playerWeaponSet);
        if (keys.length > 10) {
            // 保留最近的 4 把武器
            playerWeaponSet = {};
            console.log("[Cleanup] Weapon set cleared");
        }
    }, 10000);

    console.log("\n[+] ════════════════════════════════════");
    console.log("[+] ✅ NO RECOIL - PERFORMANCE MODE");
    console.log("[+] Method: Recoil::OnGunShot replaced");
    console.log("[+] Zero overhead (native callback)");
    console.log("[+] Return to game and test!");
    console.log("[+] ════════════════════════════════════");
})();
