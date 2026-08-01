// plan4_replace_consume.js
// 方案4：Interceptor.replace ConsumeAmmo → 仅本地玩家返回 true
// 原理：用 Frida 的 Interceptor.replace 完全替换 ConsumeAmmo 函数
//       不修改 .text 段，纯 Frida 层拦截，最安全
//       替换 WPN_Gun.ConsumeAmmo + Weapon.ConsumeAmmo(基类)
// 优点：零性能开销、无状态、无需缓存指针、不怕切房间
// 注意：换弹动画不会触发（弹药永远不变空）

console.log("[*] ======================================");
console.log("[*]  PLAN 4: Interceptor.replace");
console.log("[*]  Replace ConsumeAmmo → return true for local player only");
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
    var ADDR_IS_MY_PLAYER   = base.add(0xB55FD0);   // Player.get_isMyPlayer
    var ADDR_IS_MY_WEAPON   = base.add(0xB6E1D0);   // Weapon.get_isMyWeapon
    var ADDR_RPG_RELOAD     = base.add(0xB67C40);   // WPN_RPG.Reload

    var originalConsumeAmmo = new NativeFunction(ADDR_CONSUME_AMMO, "bool", ["pointer", "pointer"]);
    var originalConsumeBase = new NativeFunction(ADDR_CONSUME_BASE, "bool", ["pointer", "pointer"]);
    var isMyPlayer = new NativeFunction(ADDR_IS_MY_PLAYER, "bool", ["pointer", "pointer"]);
    var isMyWeapon = new NativeFunction(ADDR_IS_MY_WEAPON, "bool", ["pointer", "pointer"]);

    function isReadablePtr(p) {
        try {
            if (!p || p.isNull()) return false;
            p.readPointer();
            return true;
        } catch (e) {
            return false;
        }
    }

    function isLocalWeapon(weaponPtr) {
        if (!weaponPtr || weaponPtr.isNull()) return false;

        // 路径1：优先使用游戏自己的 Weapon.get_isMyWeapon。
        try {
            if (isMyWeapon(weaponPtr, ptr(0))) return true;
        } catch (e1) {}

        // 路径2：兜底尝试 Weapon/PlayerWeapons 常见 owner 字段。
        try {
            if (!isReadablePtr(weaponPtr)) return false;
            var owner = weaponPtr.add(0x8).readPointer();
            if (owner && !owner.isNull() && isReadablePtr(owner)) {
                return !!isMyPlayer(owner, ptr(0));
            }
        } catch (e2) {}

        return false;
    }

    // WPN_RPG.ammo -> AmmoData; clip/maxClip are ObscuredInt inline values.
    function writeObscuredInt(fieldPtr, value) {
        try {
            if (!fieldPtr || fieldPtr.isNull()) return false;
            var key = fieldPtr.readS32();
            var encrypted = value ^ key;
            fieldPtr.add(0x4).writeS32(encrypted);
            fieldPtr.add(0x8).writeU8(1);
            fieldPtr.add(0xC).writeS32(value);
            fieldPtr.add(0x10).writeU8(0);
            return fieldPtr.add(0x4).readS32() === encrypted;
        } catch (e) {
            return false;
        }
    }

    function setLocalRpgClip10(weaponPtr) {
        try {
            if (!weaponPtr || weaponPtr.isNull() || !isLocalWeapon(weaponPtr)) return false;
            var ammo = weaponPtr.add(0xEC).readPointer();
            if (!ammo || ammo.isNull() || !isReadablePtr(ammo)) return false;
            var clipOk = writeObscuredInt(ammo.add(0x08), 10);
            var maxClipOk = writeObscuredInt(ammo.add(0x30), 10);
            return clipOk && maxClipOk;
        } catch (e) {
            return false;
        }
    }

    // === 替换 WPN_Gun.ConsumeAmmo ===
    // 函数签名: bool WPN_Gun.ConsumeAmmo()
    // IL2CPP Native: bool (*)(this_ptr, methodInfo_ptr)
    try {
        Interceptor.replace(ADDR_CONSUME_AMMO, new NativeCallback(
            function (thisPtr, methodInfo) {
                if (isLocalWeapon(thisPtr)) {
                    return 1;
                }
                return originalConsumeAmmo(thisPtr, methodInfo);
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
                if (isLocalWeapon(thisPtr)) {
                    return 1;
                }
                return originalConsumeBase(thisPtr, methodInfo);
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

    // === RPG/AT4 无限子弹（WPN_RPG 不走 ConsumeAmmo，需单独处理） ===
    // WPN_RPG.FillAmmo  (0xB67070): 填满 clip+ammo 到满值
    // WPN_RPG.Fire      (0xB670A0): RPG/AT4 发射函数，内部内联操作 ObscuredInt 扣弹
    // 原理: 在 Fire() 扣弹前先填满，扣完后还是满的
    var ADDR_RPG_FIRE     = base.add(0xB670A0);
    var ADDR_RPG_FILLAMMO = base.add(0xB67070);

    var rpgFillAmmo = new NativeFunction(ADDR_RPG_FILLAMMO, "void", ["pointer", "pointer"]);

    Interceptor.attach(ADDR_RPG_FIRE, {
        onEnter: function(args) {
            try {
                var self = args[0];
                if (self && !self.isNull() && isLocalWeapon(self)) {
                    rpgFillAmmo(self, ptr(0));
                    setLocalRpgClip10(self);
                    this.rpgSelf = self;
                }
            } catch (e) {
                console.log("[RPG Ammo] Error: " + e);
            }
        },
        onLeave: function() {
            try {
                if (this.rpgSelf) setLocalRpgClip10(this.rpgSelf);
            } catch (e) {}
        }
    });

    Interceptor.attach(ADDR_RPG_RELOAD, {
        onEnter: function(args) {
            this.rpgSelf = args[0];
        },
        onLeave: function() {
            try {
                if (this.rpgSelf) setLocalRpgClip10(this.rpgSelf);
            } catch (e) {}
        }
    });
    console.log("[+] RPG/AT4 player clip maintained at 10 via Fire/Reload");

    console.log("\n[+] PLAN4 ACTIVE — Zero ammo consumption");
    console.log("[+]   - WPN_Gun.ConsumeAmmo replaced (0xB61140)");
    console.log("[+]   - Weapon.ConsumeAmmo base fallback (0xB6C310)");
    console.log("[+]   - RPG/AT4 FillAmmo on Fire enter (0xB67070)");
    console.log("[+]   - RPG/AT4 clip/maxClip=10 on Fire/Reload (0xB670A0/0xB67C40)");
    console.log("[!] Note: Reload animation will NOT trigger for guns");
})();
