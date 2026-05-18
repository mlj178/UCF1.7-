// infinite_ammo_rapid_reload_test.js - 全模式通用无限子弹 + 快速换弹
// 基于IDA反编译分析的通用BUFF字段实现
// 
// 实现方案：
// 1. 无限子弹：直接替换 get_isInfinityAmmo() 函数，始终返回1 (true)
// 2. 快速换弹：Hook get_ReloadSpeed() 函数，返回加速后的值
//
// 通用字段说明：
// - Player.Buff_InfinityAmmo (偏移0x128) - 无限子弹BUFF标志
// - PlayerWeapons.Modifier_ReloadSpeed (偏移0x3C) - 换弹速度修改器
//
// 这些字段定义在Player和PlayerWeapons类中，在所有游戏模式下都有效

console.log("[*] ======================================");
console.log("[*]  INFINITE AMMO + RAPID RELOAD (ALL MODES)");
console.log("[*]  全模式通用 - 无限子弹 + 快速换弹");
console.log("[*] ======================================");

(function () {
    var RELOAD_SPEED_MULTIPLIER = 2.0;  // 换弹速度倍数（2倍）
    
    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) { 
        console.log("[-] GameAssembly.dll not found!"); 
        return; 
    }
    var base = mod.base;

    // PlayerWeapons.get_isInfinityAmmo (RVA 0xB17120)
    var getIsInfinityAmmoAddr = base.add(0xB17120);

    // PlayerWeapons.get_ReloadSpeed (RVA 0xB170E0)
    var getReloadSpeedAddr = base.add(0xB170E0);

    console.log("[+] get_isInfinityAmmo @ " + getIsInfinityAmmoAddr);
    console.log("[+] get_ReloadSpeed @ " + getReloadSpeedAddr);
    console.log("[+] Reload Speed Multiplier: " + RELOAD_SPEED_MULTIPLIER + "x");

    var infinityAmmoLogCount = 0;
    var reloadSpeedLogCount = 0;

    // 直接替换 get_isInfinityAmmo - 始终返回1 (true)
    Interceptor.replace(getIsInfinityAmmoAddr, new NativeCallback(function(self) {
        infinityAmmoLogCount++;
        if (infinityAmmoLogCount <= 10) {
            console.log("[InfinityAmmo] Returning 1 (call #" + infinityAmmoLogCount + ")");
        }
        return 1;  // 无限子弹 (IL2CPP bool用int表示)
    }, "int", ["pointer"]));

    console.log("[+] Infinity Ammo hook installed");

    // Hook get_ReloadSpeed - 让本地玩家返回加速后的值
    // Player.get_isMyPlayer (RVA 0xB55FD0) - 判断是否是本地玩家
    var isMyPlayerAddr = base.add(0xB55FD0);
    var isMyPlayer = new NativeFunction(isMyPlayerAddr, "bool", ["pointer"]);

    Interceptor.replace(getReloadSpeedAddr, new NativeCallback(function(self) {
        try {
            // PlayerWeapons + 0x8 = owner (Player)
            var owner = self.add(0x8).readPointer();
            if (!owner || owner.isNull()) {
                return RELOAD_SPEED_MULTIPLIER;
            }

            // 判断是否是本地玩家
            if (isMyPlayer(owner)) {
                reloadSpeedLogCount++;
                if (reloadSpeedLogCount <= 5) {
                    console.log("[ReloadSpeed] Local player detected, returning " + RELOAD_SPEED_MULTIPLIER + "x");
                }
                return RELOAD_SPEED_MULTIPLIER;  // 快速换弹
            }

            // 不是本地玩家，返回默认值
            return 1.0;
        } catch(e) {
            return RELOAD_SPEED_MULTIPLIER;
        }
    }, "float", ["pointer"]));

    console.log("[+] Rapid Reload hook installed");

    console.log("\n[+] TEST SCRIPT ACTIVE");
    console.log("[+] 进入任意模式即可自动生效");
    console.log("[+] 无限子弹: ON");
    console.log("[+] 快速换弹: " + RELOAD_SPEED_MULTIPLIER + "x");

})();
