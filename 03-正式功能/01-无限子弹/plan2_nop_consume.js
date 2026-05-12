// plan2_nop_consume.js
// 方案2：NOP ConsumeAmmo 入口 → 直接 ret true
// 原理：修改 WPN_Gun.ConsumeAmmo (0xB61140) 的函数入口指令
//       patch 为 mov eax,1; ret → 弹药永远不会减少
// 注意：会跳过换弹动画触发（弹药永远不会变空）
//       修改 .text 段可能被反外挂 CRC 检测

console.log("[*] ======================================");
console.log("[*]  PLAN 2: NOP ConsumeAmmo Entry");
console.log("[*]  Patch: mov eax,1; ret");
console.log("[*] ======================================");

(function () {
    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) { console.log("[-] GameAssembly.dll not found!"); return; }
    var base = mod.base;

    // 关键地址
    var ADDR_CONSUME_AMMO   = base.add(0xB61140);   // WPN_Gun.ConsumeAmmo
    var ADDR_CONSUME_BASE   = base.add(0xB6C310);    // Weapon.ConsumeAmmo（基类）
    var ADDR_GAME_ROUND_END = base.add(0xAFAA40);
    var ADDR_ON_START_ROUND = base.add(0xAF5B30);
    var ADDR_NANO_START     = base.add(0xAF15D0);

    // 备份原字节（用于恢复）
    var origBytes1 = ADDR_CONSUME_AMMO.readByteArray(6);
    var origBytes2 = ADDR_CONSUME_BASE.readByteArray(6);

    console.log("[*] Original ConsumeAmmo(WPN_Gun): " +
        Array.from(new Uint8Array(origBytes1))
            .map(function(b) { return b.toString(16).padStart(2, '0'); }).join(' '));
    console.log("[*] Original ConsumeAmmo(Weapon): " +
        Array.from(new Uint8Array(origBytes2))
            .map(function(b) { return b.toString(16).padStart(2, '0'); }).join(' '));

    // Patch: mov eax, 1; ret   (bool 返回值放在 eax)
    // 字节: B8 01 00 00 00 C3
    var patchBytes = [0xB8, 0x01, 0x00, 0x00, 0x00, 0xC3];

    function applyPatches() {
        try {
            Memory.protect(ADDR_CONSUME_AMMO, 6, 'rwx');
            ADDR_CONSUME_AMMO.writeByteArray(patchBytes);
            console.log("[+] Patched WPN_Gun.ConsumeAmmo");
        } catch (e) {
            console.log("[-] Failed to patch WPN_Gun.ConsumeAmmo: " + e);
        }
        try {
            Memory.protect(ADDR_CONSUME_BASE, 6, 'rwx');
            ADDR_CONSUME_BASE.writeByteArray(patchBytes);
            console.log("[+] Patched Weapon.ConsumeAmmo (base)");
        } catch (e) {
            console.log("[*] Could not patch Weapon.ConsumeAmmo: " + e);
        }
    }

    applyPatches();

    // === 房间切换：重新 patch（.text 段可能在切房时被重置？预防性） ===
    function onRoomSwitch() {
        console.log("[ROOM] Switched — verifying patches...");
        // 验证 patch 是否还在
        var b = ADDR_CONSUME_AMMO.readU8();
        if (b !== 0xB8) {
            console.log("[!] Patch lost! Re-applying...");
            applyPatches();
        }
    }
    Interceptor.attach(ADDR_GAME_ROUND_END, { onEnter: onRoomSwitch });
    try { Interceptor.attach(ADDR_ON_START_ROUND, { onEnter: onRoomSwitch }); } catch (e) {}
    try { Interceptor.attach(ADDR_NANO_START, { onEnter: onRoomSwitch }); } catch (e) {}

    console.log("[+] Room hooks installed (patch re-verify)");
    console.log("\n[+] PLAN2 ACTIVE — ConsumeAmmo returns true");
    console.log("[!] WARNING: Reload animation will never trigger");
})();
