// speed_gun_universal.js - 终极武器修改（射速+无扩散+装填速度+半自动改全自动）
// 基于IDA深度分析，覆盖所有武器类型
(function() {
    console.log("[*] SPEED GUN ULTIMATE v4 (安全版本)");

    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) {
        console.log("[-] GameAssembly.dll not found!");
        return;
    }

    var base = mod.base;

    // 核心函数地址 - 从dump.cs确认
    var getShootIntervalTimeAddr = base.add(0xB78EF0);      // WeaponData_Gun.get_shootIntervalTime
    var gunShootNoCheckAddr = base.add(0xB621F0);           // WPN_Gun.GunShoot_NoCheck
    
    console.log("[+] get_shootIntervalTime @ " + getShootIntervalTimeAddr);
    console.log("[+] GunShoot_NoCheck @ " + gunShootNoCheckAddr);

    var convertedWeapons = {};
    var weaponProcessedMap = {};
    
    // ==========================================
    // 方案1: Hook get_shootIntervalTime - 通用射速修改
    // 使用Interceptor.attach更安全
    // ==========================================
    Interceptor.attach(getShootIntervalTimeAddr, {
        onLeave: function(retval) {
            try {
                // 将返回值修改为0.01秒（每秒6000发）
                retval.replace(ptr(0x3C23D70A)); // 0.01 in float hex
            } catch(e) {
                console.log("[ERROR get_shootIntervalTime] " + e.message);
            }
        }
    });
    
    console.log("[+] Hooked get_shootIntervalTime");

    // ==========================================
    // 方案2: Hook GunShoot_NoCheck - 半自动改全自动 + 修改装填速度
    // ==========================================
    Interceptor.attach(gunShootNoCheckAddr, {
        onEnter: function(args) {
            try {
                var self = args[0]; // WPN_Gun 实例指针
                var weaponAddr = ptr(self).toString();
                
                // 安全检查：确保指针有效
                if (self.isNull() || weaponAddr === "0x0") {
                    return;
                }
                
                // WPN_Gun 字段偏移（经过验证）:
                // +0x68 data (WeaponData*)
                // +0xEC realData (WeaponData_Gun*)
                // +0xF0 isSemiGun (bool)
                // +0x108 semiGunFireLinkState (int)
                
                // 读取 isSemiGun
                var isSemiGun = self.add(0xF0).readU8();
                
                // 只处理半自动武器，且只处理一次
                if (isSemiGun && !convertedWeapons[weaponAddr]) {
                    // 从 dump.cs 确认：semiGunFireLinkState 偏移是 0x108
                    var semiGunFireLinkState = self.add(0x108).readU32();
                    
                    // 获取武器数据
                    var dataPtr = self.add(0x68).readPointer();
                    var weaponName = "Unknown";
                    var weaponType = "Unknown";
                    
                    if (!dataPtr.isNull()) {
                        var wpnClassVal = dataPtr.add(0x10).readU32();
                        var namePtr = dataPtr.add(0x18).readPointer();
                        
                        if (!namePtr.isNull()) {
                            try {
                                weaponName = namePtr.readCString();
                            } catch(e) {
                                weaponName = "ReadError";
                            }
                        }
                        
                        var classNames = ["Rifle", "Sniper", "MachineGun", "SubmachineGun", "ShotGun", "Pistol", "Knife", "Grenade", "FlashBang", "SmokeGrenade"];
                        if (wpnClassVal >= 0 && wpnClassVal < classNames.length) {
                            weaponType = classNames[wpnClassVal];
                        } else {
                            weaponType = "Unknown(" + wpnClassVal + ")";
                        }
                    }
                    
                    console.log("[SEMI-AUTO CONVERSION] =====================");
                    console.log("[SEMI-AUTO CONVERSION] Instance: " + weaponAddr);
                    console.log("[SEMI-AUTO CONVERSION] Weapon Name: " + weaponName);
                    console.log("[SEMI-AUTO CONVERSION] Weapon Type: " + weaponType);
                    console.log("[SEMI-AUTO CONVERSION] isSemiGun: " + isSemiGun + " -> 0");
                    console.log("[SEMI-AUTO CONVERSION] semiGunFireLinkState: " + semiGunFireLinkState + " -> 0");
                    console.log("[SEMI-AUTO CONVERSION] =====================");
                    
                    // 修改为全自动
                    self.add(0xF0).writeU8(0);      // isSemiGun = false
                    self.add(0x108).writeU32(0);    // semiGunFireLinkState = None
                    
                    convertedWeapons[weaponAddr] = true;
                }
                
                // 修改装填速度（每个武器只修改一次）
                if (!weaponProcessedMap[weaponAddr]) {
                    weaponProcessedMap[weaponAddr] = true;
                    
                    // 获取 realData (WeaponData_Gun*)
                    var realData = self.add(0xEC).readPointer();
                    if (!realData.isNull()) {
                        // 修改 reloadAnimRatio (0xD4) - 装填动画速度比例
                        var reloadAnimRatioPtr = realData.add(0xD4);
                        var currentReloadRatio = reloadAnimRatioPtr.readFloat();
                        if (currentReloadRatio > 0 && currentReloadRatio < 100) {
                            reloadAnimRatioPtr.writeFloat(5.0);
                            console.log("[GunShoot_NoCheck] Set reloadAnimRatio: " + currentReloadRatio + " -> 5.0");
                        }
                        
                        // 修改 perturbMin 和 perturbMax 为0
                        var perturbMinPtr = realData.add(0xF8).readPointer();
                        var perturbMaxPtr = realData.add(0xFC).readPointer();
                        
                        if (!perturbMinPtr.isNull()) {
                            for (var i = 0; i < 5; i++) {
                                perturbMinPtr.add(i * 4).writeFloat(0.0);
                            }
                            console.log("[GunShoot_NoCheck] Set perturbMin to 0");
                        }
                        
                        if (!perturbMaxPtr.isNull()) {
                            for (var i = 0; i < 5; i++) {
                                perturbMaxPtr.add(i * 4).writeFloat(0.0);
                            }
                            console.log("[GunShoot_NoCheck] Set perturbMax to 0");
                        }
                    }
                }
            } catch(e) {
                // 忽略错误，避免影响游戏运行
                console.log("[ERROR GunShoot_NoCheck] " + e.message);
            }
        }
    });
    
    console.log("[+] Hooked GunShoot_NoCheck");
    console.log("[+] Loaded successfully!");
    console.log("[+] Features enabled:");
    console.log("    - Instant fire rate");
    console.log("    - Zero bullet spread");
    console.log("    - Semi-auto to full-auto conversion");
    console.log("    - Fast reload");
})();
