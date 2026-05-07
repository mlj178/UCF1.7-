// infinite_ammo_v6.js — V6 真正流畅版无限子弹
// V5 问题：
//   1. MAX_WPN=4 → 第5把枪开始无效
//   2. fire hook 中 readable() 对每次 Bot 开火都执行 → 掉帧
//   3. 定时器中 lockWeapon 做完整验证(3次 findRangeByAddress) → 掉帧
// V6 修复：
//   1. 移除 MAX_WPN 限制 → 所有玩家武器都有效
//   2. fire hook：先 toString 查 Map（纯JS操作，极快），命中则直接 return
//      只有全新指针才调用 readable+isMyWeapon
//   3. 定时器只写值不验证 → 零系统调用
//   4. 房间切换清空所有缓存
//   5. 黑名单缓存：已知非玩家武器直接跳过

console.log("[*] ======================================");
console.log("[*]  ALL WEAPONS INFINITE AMMO V6");
console.log("[*]  (Fast Path + No Limit)");
console.log("[*] ======================================");

(function () {
    var mod = Process.findModuleByName("GameAssembly.dll");
    if (!mod) { console.log("[-] GameAssembly.dll not found!"); return; }
    var base = mod.base;

    var ADDR_IS_MY_WEAPON             = base.add(0xB6E1D0);
    var ADDR_GAME_ROUND_END           = base.add(0xAFAA40);
    var ADDR_ON_START_NEW_ROUND       = base.add(0xAF5B30);
    var ADDR_NANO_ON_START_NEW_ROUND  = base.add(0xAF15D0);
    var fireOffsets = [0xB67AF0, 0xB62730, 0xB621F0, 0xAEA6B0];

    var wpnData = {};      // key → { ptr, clipVal, ammoVal }  仅玩家武器
    var notMine = {};      // key → true  已知的非玩家武器（黑名单）
    var lockCount = 0;
    var cleanupCount = 0;

    var isMyWeapon = new NativeFunction(ADDR_IS_MY_WEAPON, "bool", ["pointer", "pointer"]);

    function readable(p) {
        if (!p || p.isNull()) return false;
        try { return Process.findRangeByAddress(p) !== null; } catch (e) { return false; }
    }

    function checkIsMyWeapon(wpnPtr) {
        try { return isMyWeapon(wpnPtr, ptr(0)); } catch (e) { return false; }
    }

    // === 开火 hook：极速路径 ===
    for (var i = 0; i < fireOffsets.length; i++) {
        (function (off) {
            Interceptor.attach(base.add(off), {
                onEnter: function (args) {
                    var wpn = args[0];
                    if (wpn === null || wpn.isNull()) return;

                    var k = wpn.toString();       // 纯 JS 字符串操作，极快

                    // 快速路径1：已知玩家武器 → 什么都不做（定时器会锁）
                    if (wpnData[k]) return;

                    // 快速路径2：已知非玩家武器 → 直接跳过
                    if (notMine[k]) return;

                    // 慢速路径：全新指针 → 验证
                    if (!readable(wpn)) return;

                    if (checkIsMyWeapon(wpn)) {
                        // 玩家武器：记录加密值
                        try {
                            var adPtr = wpn.add(0xF4).readPointer();
                            if (!readable(adPtr)) return;
                            var cv = adPtr.add(0x0C).readInt();
                            var av = adPtr.add(0x20).readInt();
                            wpnData[k] = { ptr: wpn, cv: cv, av: av };
                            lockCount++;
                            console.log("[Lock #" + lockCount + "] " + wpn + " clip:" + cv + " ammo:" + av);
                        } catch (e) {}
                    } else {
                        // 非玩家武器：加入黑名单，下次直接跳过
                        notMine[k] = true;
                    }
                }
            });
        })(fireOffsets[i]);
    }
    console.log("[+] Hooked " + fireOffsets.length + " fire functions");

    // === 房间切换清理 ===
    function clearAll() {
        var total = Object.keys(wpnData).length + Object.keys(notMine).length;
        wpnData = {};
        notMine = {};
        console.log("[ROOM] Cleared " + total + " cached refs");
    }

    Interceptor.attach(ADDR_GAME_ROUND_END, { onEnter: clearAll });
    try { Interceptor.attach(ADDR_ON_START_NEW_ROUND, { onEnter: clearAll }); } catch (e) {}
    try { Interceptor.attach(ADDR_NANO_ON_START_NEW_ROUND, { onEnter: clearAll }); } catch (e) {}
    console.log("[+] Room cleanup hooks installed");

    // === 定时器：极速写值（不做任何验证，零系统调用） ===
    setInterval(function () {
        var keys = Object.keys(wpnData);
        for (var i = keys.length - 1; i >= 0; i--) {
            var d = wpnData[keys[i]];
            try {
                var adPtr = d.ptr.add(0xF4).readPointer();
                adPtr.add(0x0C).writeInt(d.cv);
                adPtr.add(0x20).writeInt(d.av);
            } catch (e) {
                // 写入失败 → 武器已释放 → 清理
                delete wpnData[keys[i]];
                cleanupCount++;
            }
        }
        if (cleanupCount > 0 && cleanupCount % 5 === 0) {
            console.log("[Cleanup] " + cleanupCount + " dead, active:" + Object.keys(wpnData).length);
        }
    }, 2000);

    console.log("\n[+] V6 ACTIVE — fast path, no limit, 2s timer");
})();
