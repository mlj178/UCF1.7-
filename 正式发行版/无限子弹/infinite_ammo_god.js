// infinite_ammo_god.js - 上帝模式，每帧强制锁定
// 使用方法：frida -p <PID> -l infinite_ammo_god.js

console.log("[*] === GOD MODE Infinite Ammo ===");
console.log("[*] Will force-lock ammo values continuously");

(function() {
    var gameAssembly = Process.findModuleByName("GameAssembly.dll");

    if (!gameAssembly) {
        console.log("[-] GameAssembly.dll not found!");
        return;
    }

    var playerGun = null;
    var targetClip = 9999;  // 直接设置为很大的值
    var targetAmmo = 9999;

    // Hook 开火函数来识别玩家的枪
    var fireFunctions = [0xB67AF0, 0xB62730, 0xB621F0, 0xAEA6B0];

    for (var i = 0; i < fireFunctions.length; i++) {
        var addr = gameAssembly.base.add(fireFunctions[i]);

        Interceptor.attach(addr, {
            onEnter: function(args) {
                var thisPtr = args[0];
                
                if (thisPtr === null || thisPtr.isNull()) {
                    return;
                }

                // 第一把枪 = 玩家的枪
                if (playerGun === null) {
                    playerGun = thisPtr;
                    console.log("\n[+] Player gun: " + playerGun);
                    
                    // 设置目标值为当前值（这样不会太明显）
                    try {
                        var ammoDataPtr = thisPtr.add(0xF4).readPointer();
                        if (!ammoDataPtr.isNull()) {
                            targetClip = ammoDataPtr.add(0x0C).readInt();
                            targetAmmo = ammoDataPtr.add(0x20).readInt();
                            console.log("[*] Target clip_h: " + targetClip);
                            console.log("[*] Target ammo_h: " + targetAmmo);
                        }
                    } catch (e) {
                        console.log("[-] Error: " + e);
                    }
                }
            }
        });
    }

    // 每 50ms 强制设置一次（比游戏更新频率快）
    setInterval(function() {
        if (playerGun !== null) {
            try {
                var ammoDataPtr = playerGun.add(0xF4).readPointer();
                
                if (!ammoDataPtr.isNull()) {
                    // 强制写入目标值
                    ammoDataPtr.add(0x0C).writeInt(targetClip);
                    ammoDataPtr.add(0x20).writeInt(targetAmmo);
                }
            } catch (e) {
                // 静默失败
            }
        }
    }, 50);

    console.log("[+] Hooks applied!");
    console.log("[*] Continuous lock enabled (every 50ms)");
    console.log("[*] Return to game and test - should be INFINITE now!");
})();
