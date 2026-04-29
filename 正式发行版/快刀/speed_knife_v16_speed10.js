// speed_knife_v16_speed10.js - 方案5修复版：使用 NativeCallback 替换 get_KnifeSpeed
// 直接替换函数实现

(function() {
    var SPEED = 10.0;

    console.log("[*] SPEED KNIFE V16 (NativeCallback Replace)");

    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) {
        console.log("[-] GameAssembly.dll not found!");
        return;
    }

    var base = mod.base;

    // Player.get_isMyPlayer (RVA 0xB55FD0)
    var isMyPlayerAddr = base.add(0xB55FD0);
    var isMyPlayer = new NativeFunction(isMyPlayerAddr, "bool", ["pointer"]);

    // 获取原始的 get_KnifeSpeed 函数
    var getKnifeSpeedAddr = base.add(0xB170A0);
    var originalGetKnifeSpeed = new NativeFunction(getKnifeSpeedAddr, "float", ["pointer"]);

    console.log("[+] isMyPlayer @ " + isMyPlayerAddr);
    console.log("[+] get_KnifeSpeed @ " + getKnifeSpeedAddr);

    var logCount = 0;

    // 替换 get_KnifeSpeed 实现
    Interceptor.replace(getKnifeSpeedAddr, new NativeCallback(function(self) {
        try {
            // PlayerWeapons + 0x8 = owner (Player)
            var owner = self.add(0x8).readPointer();
            if (!owner || owner.isNull()) {
                return originalGetKnifeSpeed(self);
            }

            // 判断是否是本地玩家
            if (isMyPlayer(owner)) {
                logCount++;
                if (logCount <= 10) {
                    console.log("[KnifeSpeed] Player detected, returning " + SPEED);
                }
                return SPEED;
            }

            // 不是本地玩家，调用原始函数
            return originalGetKnifeSpeed(self);
        } catch(e) {
            console.log("[ERROR] " + e.message);
            return originalGetKnifeSpeed(self);
        }
    }, "float", ["pointer"]));

    console.log("[+] V16 Loaded. All knife attacks accelerated (Player Only)!");
    console.log("[+] Speed: " + SPEED + "x");
    console.log("[*] 挥刀测试...");

})();
