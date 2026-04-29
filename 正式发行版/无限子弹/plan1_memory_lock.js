// plan1_memory_lock.js
// 方案1：内存锁定 AmmoData.hiddenValue（ObscuredInt 加密值原样写回）
// 原理：锁定 clip.hiddenValue(+0x0C) 和 ammo.hiddenValue(+0x20)
//       不写裸数字，写第一次见到的加密值，每次定时器原样写回
// 参考：V6 经验 — ObscuredInt 不能写9999，必须锁定加密值
//       切房间清空缓存防闪退，isMyWeapon 过滤 Bot

console.log("[*] ======================================");
console.log("[*]  PLAN 1: Memory Lock (V6 approach)");
console.log("[*]  Lock ObscuredInt hiddenValue");
console.log("[*] ======================================");

(function () {
    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) { console.log("[-] GameAssembly.dll not found!"); return; }
    var base = mod.base;

    // 关键地址
    var ADDR_IS_MY_WEAPON     = base.add(0xB6E1D0);
    var ADDR_GAME_ROUND_END   = base.add(0xAFAA40);
    var ADDR_ON_START_ROUND   = base.add(0xAF5B30);
    var ADDR_NANO_START       = base.add(0xAF15D0);

    // 开火函数（用于发现新武器指针）
    var fireOffsets = [0xB624C0, 0xB621F0, 0xB62730, 0xAEA6B0];

    // 状态存储
    var wpnData  = {};   // { 指针字符串 → { ptr, cv, av } }  玩家武器白名单
    var notMine  = {};   // { 指针字符串 → true }              Bot武器黑名单
    var lockCount = 0;
    var cleanupCount = 0;

    // Native 调用：Weapon.get_isMyWeapon
    var isMyWeapon = new NativeFunction(ADDR_IS_MY_WEAPON, "bool", ["pointer", "pointer"]);

    function readable(p) {
        if (!p || p.isNull()) return false;
        try { return Process.findRangeByAddress(p) !== null; } catch (e) { return false; }
    }

    // === 开火 Hook：极速路径（V6 优化） ===
    for (var i = 0; i < fireOffsets.length; i++) {
        (function (off) {
            Interceptor.attach(base.add(off), {
                onEnter: function (args) {
                    var wpn = args[0];
                    if (!wpn || wpn.isNull()) return;

                    var k = wpn.toString();       // 纯JS字符串，极快

                    // 快速路径1：已知玩家武器 → 定时器会锁
                    if (wpnData[k]) return;

                    // 快速路径2：已知Bot武器 → 跳过
                    if (notMine[k]) return;

                    // 慢速路径：全新指针 → 验证一次
                    if (!readable(wpn)) return;

                    if (isMyWeapon(wpn, ptr(0))) {
                        try {
                            var adPtr = wpn.add(0xF4).readPointer();  // WPN_Gun.ammoData
                            if (!readable(adPtr)) return;
                            // ★ 关键：读 ObscuredInt.hiddenValue，不是 fakeValue
                            var cv = adPtr.add(0x0C).readInt();   // clip.hiddenValue
                            var av = adPtr.add(0x20).readInt();   // ammo.hiddenValue
                            wpnData[k] = { ptr: wpn, cv: cv, av: av };
                            lockCount++;
                            console.log("[Lock #" + lockCount + "] " + wpn +
                                " clip:" + cv + " ammo:" + av);
                        } catch (e) {}
                    } else {
                        notMine[k] = true;  // 加入黑名单，下次直接跳过
                    }
                }
            });
        })(fireOffsets[i]);
    }
    console.log("[+] Hooked " + fireOffsets.length + " fire functions");

    // === 房间切换清理（防闪退） ===
    function clearAll() {
        var total = Object.keys(wpnData).length + Object.keys(notMine).length;
        wpnData  = {};
        notMine  = {};
        console.log("[ROOM] Cleared " + total + " cached refs");
    }
    Interceptor.attach(ADDR_GAME_ROUND_END, { onEnter: clearAll });
    try { Interceptor.attach(ADDR_ON_START_ROUND, { onEnter: clearAll }); } catch (e) {}
    try { Interceptor.attach(ADDR_NANO_START, { onEnter: clearAll }); } catch (e) {}
    console.log("[+] Room cleanup hooks installed");

    // === 定时器：每2秒写回加密值（零验证，极速） ===
    setInterval(function () {
        var keys = Object.keys(wpnData);
        for (var i = keys.length - 1; i >= 0; i--) {
            var d = wpnData[keys[i]];
            try {
                var adPtr = d.ptr.add(0xF4).readPointer();
                adPtr.add(0x0C).writeInt(d.cv);   // 写回加密值，不写9999
                adPtr.add(0x20).writeInt(d.av);   // 写回加密值
            } catch (e) {
                // 写入失败 → 旧指针已失效 → 清理
                delete wpnData[keys[i]];
                cleanupCount++;
            }
        }
        if (cleanupCount > 0 && cleanupCount % 5 === 0) {
            console.log("[Cleanup] " + cleanupCount + " dead, active:" +
                Object.keys(wpnData).length);
        }
    }, 2000);

    console.log("\n[+] PLAN1 ACTIVE — 2s timer, no limit, triple cleanup");
})();
