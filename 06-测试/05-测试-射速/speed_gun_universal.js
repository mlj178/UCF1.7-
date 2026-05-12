// speed_gun_universal.js - 终极武器修改（仅玩家武器）
// IDA 验证的正确偏移
(function() {
    console.log("[*] SPEED GUN ULTIMATE v11 (Player Only)");

    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) {
        console.log("[-] GameAssembly.dll not found!");
        return;
    }

    var base = mod.base;

    // IDA 验证的函数地址
    var getShootIntervalTimeAddr = base.add(0xB78EF0);  // WeaponData_Gun.get_shootIntervalTime
    var gunFireCheckingAddr = base.add(0xB62050);       // WPN_Gun.GunFireChecking
    
    console.log("[+] get_shootIntervalTime @ " + getShootIntervalTimeAddr);
    console.log("[+] GunFireChecking @ " + gunFireCheckingAddr);

    var convertedWeapons = {};
    
    // 方案1: Hook get_shootIntervalTime - 通用射速修改
    Interceptor.attach(getShootIntervalTimeAddr, {
        onLeave: function(retval) {
            try {
                retval.replace(ptr(0x3C23D70A)); // 0.01秒 (float)
            } catch(e) {
                console.log("[ERROR get_shootIntervalTime] " + e.message);
            }
        }
    });
    
    console.log("[+] Hooked get_shootIntervalTime");

    var weaponClassNames = [
        "Rifle", "Sniper", "MachineGun", "SubmachineGun", "ShotGun",
        "Pistol", "Knife", "Grenade", "FlashBang", "SmokeGrenade"
    ];

    // 检查是否是玩家武器
    function checkIsPlayerWeapon(weaponPtr) {
        try {
            // WPN_Gun -> Model.owner (Player*) -> Player.clientData (ClientData*) -> ClientData.nickName
            // 从 dump.cs 验证：
            //   Model.owner = 0x30
            //   Player.clientData = 0x94  
            //   ClientData.nickName = 0x10
            var ownerPtr = weaponPtr.add(0x30).readPointer();
            
            if (!ownerPtr.isNull()) {
                var clientDataPtr = ownerPtr.add(0x94).readPointer();
                if (!clientDataPtr.isNull()) {
                    var namePtr = clientDataPtr.add(0x10).readPointer();
                    if (!namePtr.isNull()) {
                        var name = namePtr.readCString();
                        if (name && name.length > 0 && name.indexOf("BOT") === -1) {
                            console.log("[DEBUG] Found player weapon: " + name);
                            return true;
                        }
                    }
                }
            }
        } catch(e) {
            console.log("[ERROR checkIsPlayerWeapon] " + e.message);
        }
        return false;
    }

    // 方案2: Hook GunFireChecking - 强制全自动（仅玩家）
    // IDA 验证的偏移：
    // 0x68 - data (WeaponData*)
    // 0xF0 - _isSemiGun_k__BackingField
    // 0x108 - _semiGunFireLinkState_k__BackingField
    Interceptor.attach(gunFireCheckingAddr, {
        onEnter: function(args) {
            try {
                var self = args[0];
                
                if (self.isNull()) {
                    return;
                }
                
                var weaponAddr = ptr(self).toString();
                
                // 检查是否是玩家武器
                if (!checkIsPlayerWeapon(self)) {
                    return;
                }
                
                // 读取 isSemiGun (0xF0) - IDA 验证正确
                var isSemiGun = self.add(0xF0).readU8();
                
                // 如果不是半自动，跳过转换
                if (!isSemiGun) {
                    return;
                }
                
                // 检查是否已转换
                if (convertedWeapons[weaponAddr]) {
                    return;
                }
                
                // 获取武器数据 (0x68) - IDA 验证正确
                var dataPtr = self.add(0x68).readPointer();
                var wpnName = "Unknown";
                var wpnClass = -1;
                
                if (!dataPtr.isNull()) {
                    var namePtr = dataPtr.add(0x18).readPointer();
                    if (!namePtr.isNull()) {
                        try {
                            wpnName = namePtr.readCString();
                        } catch(e) {}
                    }
                    wpnClass = dataPtr.add(0x10).readU32();
                }
                
                var className = "Unknown";
                if (wpnClass >= 0 && wpnClass < weaponClassNames.length) {
                    className = weaponClassNames[wpnClass];
                }
                
                // 打印日志
                console.log("\n==========================================");
                console.log("[PLAYER WEAPON] Address: " + weaponAddr);
                console.log("[PLAYER WEAPON] Name: " + wpnName);
                console.log("[PLAYER WEAPON] Class: " + wpnClass + " (" + className + ")");
                console.log("[PLAYER WEAPON] isSemiGun: " + isSemiGun);
                
                // 修改为全自动
                self.add(0xF0).writeU8(0);           // isSemiGun = false
                self.add(0x108).writeU32(0);         // semiGunFireLinkState = 0
                
                console.log("[PLAYER WEAPON] -> Converted to FULL-AUTO!");
                console.log("==========================================");
                
                convertedWeapons[weaponAddr] = true;
                
            } catch(e) {
                console.log("[ERROR GunFireChecking] " + e.message);
            }
        }
    });
    
    console.log("[+] Hooked GunFireChecking");
    console.log("[+] Loaded successfully!");
})();