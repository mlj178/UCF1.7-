// infinite_ammo_all_weapons.js - 全武器无限子弹
// 使用方法：frida -p <PID> -l infinite_ammo_all_weapons.js
// 功能：锁定玩家所有武器的弹药（主武器 1/2、副武器 1/2）

console.log("[*] === ALL WEAPONS Infinite Ammo ===");
console.log("[*] Will lock ammo for ALL player weapons");

(function() {
    var gameAssembly = Process.findModuleByName("GameAssembly.dll");

    if (!gameAssembly) {
        console.log("[-] GameAssembly.dll not found!");
        return;
    }

    // 存储所有玩家武器的数组
    var playerWeapons = [];
    var targetValues = {};  // 存储每把枪的目标弹药值

    // 锁定一把武器的弹药
    function lockWeapon(weaponPtr, index) {
        try {
            var ammoDataPtr = weaponPtr.add(0xF4).readPointer();
            
            if (!ammoDataPtr.isNull()) {
                var clipPtr = ammoDataPtr.add(0x0C);
                var ammoPtr = ammoDataPtr.add(0x20);
                
                // 读取当前值作为目标值
                if (!targetValues[index]) {
                    targetValues[index] = {
                        clip: clipPtr.readInt(),
                        ammo: ammoPtr.readInt()
                    };
                    console.log("[*] Weapon " + index + " - Initial clip: " + targetValues[index].clip + ", ammo: " + targetValues[index].ammo);
                }
                
                // 强制写入目标值（9999）
                clipPtr.writeInt(9999);
                ammoPtr.writeInt(9999);
            }
        } catch (e) {
            // 静默失败
        }
    }

    // 方法 1: Hook 开火函数来收集所有武器
    var fireFunctions = [0xB67AF0, 0xB62730, 0xB621F0, 0xAEA6B0];

    for (var i = 0; i < fireFunctions.length; i++) {
        var addr = gameAssembly.base.add(fireFunctions[i]);

        Interceptor.attach(addr, {
            onEnter: function(args) {
                var thisPtr = args[0];
                
                if (thisPtr === null || thisPtr.isNull()) {
                    return;
                }

                // 检查是否已经记录过这把武器
                var weaponKey = thisPtr.toString();
                var alreadyRecorded = false;
                
                for (var j = 0; j < playerWeapons.length; j++) {
                    if (playerWeapons[j].toString() === weaponKey) {
                        alreadyRecorded = true;
                        break;
                    }
                }
                
                // 如果是新武器，添加到数组
                if (!alreadyRecorded) {
                    var weaponIndex = playerWeapons.length;
                    playerWeapons.push(thisPtr);
                    console.log("\n[+] Found weapon #" + weaponIndex + ": " + thisPtr);
                    
                    // 立即锁定这把武器的弹药
                    lockWeapon(thisPtr, weaponIndex);
                }
            }
        });
    }

    // 方法 2: 定时扫描所有可能的武器槽位
    // 假设玩家最多有 4 把武器（2 主武器 + 2 副武器）
    var MAX_WEAPONS = 4;
    
    // 每 50ms 强制锁定所有武器
    setInterval(function() {
        // 锁定已发现的所有武器
        for (var i = 0; i < playerWeapons.length; i++) {
            lockWeapon(playerWeapons[i], i);
        }
    }, 50);

    console.log("[+] Hooks applied!");
    console.log("[*] Continuous lock enabled for all weapons (every 50ms)");
    console.log("[*] Return to game and test - ALL weapons should have INFINITE ammo!");
    console.log("[*] Switch weapons in-game to test different slots");
})();
