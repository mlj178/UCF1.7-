// plan4_replace_consume.js
// 方案4：Interceptor.replace ConsumeAmmo → 直接返回 true
// 原理：用 Frida 的 Interceptor.replace 完全替换 ConsumeAmmo 函数
//       不修改 .text 段，纯 Frida 层拦截，最安全
//       替换 WPN_Gun.ConsumeAmmo + Weapon.ConsumeAmmo(基类)
// 优点：零性能开销、无状态、无需缓存指针、不怕切房间
// 注意：换弹动画不会触发（弹药永远不变空）

console.log("[*] ======================================");
console.log("[*]  PLAN 4: Interceptor.replace");
console.log("[*]  Replace ConsumeAmmo → return true");
console.log("[*]  No .text patch, pure Frida layer");
console.log("[*] ======================================");

(function () {
    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) { console.log("[-] GameAssembly.dll not found!"); return; }
    var base = mod.base;

    // 关键地址
    var ADDR_CONSUME_AMMO   = base.add(0xB61140);   // WPN_Gun.ConsumeAmmo
    var ADDR_CONSUME_BASE   = base.add(0xB6C310);   // Weapon.ConsumeAmmo（基类）
    var ADDR_GAME_ROUND_END = base.add(0xAFAA40);
    var ADDR_ON_START_ROUND = base.add(0xAF5B30);
    var ADDR_NANO_START     = base.add(0xAF15D0);

    // === 替换 WPN_Gun.ConsumeAmmo ===
    // 函数签名: bool WPN_Gun.ConsumeAmmo()
    // IL2CPP Native: bool (*)(this_ptr, methodInfo_ptr)
    try {
        Interceptor.replace(ADDR_CONSUME_AMMO, new NativeCallback(
            function (thisPtr, methodInfo) {
                // WPN_Gun 的 this 指针
                // 不做任何消耗，直接返回 true
                // 游戏内 HUD 可能需要额外刷新，但弹药值不会变
                return 1;
            },
            "bool", ["pointer", "pointer"]
        ));
        console.log("[+] Replaced WPN_Gun.ConsumeAmmo (0xB61140)");
    } catch (e) {
        console.log("[-] Failed to replace WPN_Gun.ConsumeAmmo: " + e);
    }

    // === 替换 Weapon.ConsumeAmmo（基类，兜底） ===
    try {
        Interceptor.replace(ADDR_CONSUME_BASE, new NativeCallback(
            function (thisPtr, methodInfo) {
                return 1;
            },
            "bool", ["pointer", "pointer"]
        ));
        console.log("[+] Replaced Weapon.ConsumeAmmo (0xB6C310)");
    } catch (e) {
        console.log("[*] Could not replace Weapon.ConsumeAmmo: " + e);
    }

    // === 房间切换日志 ===
    // Interceptor.replace 是永久的 → 不需要重新替换
    function onRoomSwitch() {
        console.log("[ROOM] Switched — replace hooks remain active");
    }
    Interceptor.attach(ADDR_GAME_ROUND_END, { onEnter: onRoomSwitch });
    try { Interceptor.attach(ADDR_ON_START_ROUND, { onEnter: onRoomSwitch }); } catch (e) {}
    try { Interceptor.attach(ADDR_NANO_START, { onEnter: onRoomSwitch }); } catch (e) {}
    console.log("[+] Room hooks installed (monitor only)");

    console.log("\n[+] PLAN4 ACTIVE — Zero ammo consumption");
    console.log("[+] No state, no cache, no memory leaks");
    console.log("[!] Note: Reload animation will NOT trigger");
})();
