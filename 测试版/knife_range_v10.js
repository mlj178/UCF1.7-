// ============================================================
// 近战距离修改器 v10 — Interceptor.attach GetKnifeAttackData
//
// 原理: Hook WPN_Knife$$GetKnifeAttackData (RVA 0xB63EC0)
//       游戏每次攻击时调此函数获取 KnifeAttackData 结构体
//       在 onLeave 中修改返回结构体的 range 字段 (+0x4)
//
//       ★ 不写只读内存，不改 ScriptableObject
//         返回缓冲区是调用者分配的，写入安全
//         类似 speed_knife_v16 替换 get_KnifeSpeed，只影响玩家
//
// 玩家识别: 
//       WPN_Knife+0xA8 → PlayerWeapons
//       PlayerWeapons+0x8 → owner (Player)
//       isMyPlayer(owner) → true 才修改
// ============================================================

(function() {
    'use strict';

    var KNIFE_RANGE_MULTIPLIER = 5.0;
    var gameAssembly = null;

    function sendLog(level, module, msg) {
        var logMsg = '[' + module + '] ' + msg;
        if (level === 'error') console.error(logMsg);
        else if (level === 'warn') console.warn(logMsg);
        else console.log(logMsg);
    }

    function getGameAssembly() {
        if (gameAssembly) return gameAssembly;
        var mods = Process.enumerateModules();
        for (var i = 0; i < mods.length; i++) {
            if (mods[i].name.indexOf('GameAssembly') !== -1) {
                gameAssembly = mods[i];
                return gameAssembly;
            }
        }
        return null;
    }

    var enabled = false;
    var isMyWeaponFn = null;
    var logCount = 0;
    var maxLogs = 5;

    function enable() {
        if (enabled) return;
        var gm = getGameAssembly();
        if (!gm) { sendLog('error', '近战', 'GameAssembly 未找到'); return; }
        var base = gm.base;

        // Weapon.get_isMyWeapon (RVA 0xB6E1D0) — 判断武器是否属于本地玩家
        // 已在无限子弹 Plan1 中验证可靠
        isMyWeaponFn = new NativeFunction(base.add(0xB6E1D0), 'bool', ['pointer', 'pointer']);

        // ================================================================
        // Hook 1: WPN_Knife.GetKnifeAttackData (RVA 0xB63EC0)
        // IL2CPP 32-bit 结构体返回: eax = 指向 KnifeAttackData 的指针
        // KnifeAttackData: +0x0 damage, +0x4 range, +0x8 angle, ...
        // ================================================================
        var hookAddr = base.add(0xB63EC0);
        sendLog('info', '近战', 'Hook @ ' + hookAddr);

        Interceptor.attach(hookAddr, {
            onEnter: function(args) {
                // args[0] = retBuf (KnifeAttackData*), args[1] = this (WPN_Knife*)
                // args[2] = attackIndex, args[3] = methodInfo
                this.wpnSelf = args[1];
                this.attackIndex = args[2].toInt32();
            },
            onLeave: function(retval) {
                // retval = 指向 KnifeAttackData 的指针
                if (!this.wpnSelf || this.wpnSelf.isNull()) return;
                // isMyWeapon 过滤：只改本地玩家的武器
                if (!isMyWeaponFn(this.wpnSelf, ptr(0))) return;

                try {
                    var rangeAddr = retval.add(0x4);
                    var origRange = rangeAddr.readFloat();

                    if (!(origRange > 0.3 && origRange < 500)) return;

                    var newRange = origRange * KNIFE_RANGE_MULTIPLIER;
                    rangeAddr.writeFloat(newRange);

                    logCount++;
                    if (logCount <= maxLogs) {
                        sendLog('info', '近战', 'index=' + this.attackIndex +
                            ' range ' + origRange.toFixed(2) + ' → ' + newRange.toFixed(2));
                    }
                } catch(e) {
                    if (logCount <= 1) sendLog('error', '近战', '异常: ' + e.message);
                }
            }
        });

        // ================================================================
        // Hook 2: Weapon.GetKnifeAttackData (RVA 0xB79008) 基类兜底
        // ================================================================
        try {
            Interceptor.attach(base.add(0xB79008), {
                onEnter: function(args) {
                    this.wpnSelf = args[1];
                },
                onLeave: function(retval) {
                    if (!this.wpnSelf || this.wpnSelf.isNull()) return;
                    if (!isMyWeaponFn(this.wpnSelf, ptr(0))) return;
                    try {
                        var rangeAddr = retval.add(0x4);
                        var origRange = rangeAddr.readFloat();
                        if (origRange > 0.3 && origRange < 500) {
                            rangeAddr.writeFloat(origRange * KNIFE_RANGE_MULTIPLIER);
                        }
                    } catch(e) {}
                }
            });
        } catch(e) {}

        enabled = true;
        sendLog('info', '近战', 'v10 已启用 (' + KNIFE_RANGE_MULTIPLIER + 'x)');
    }

    function disable() {
        if (!enabled) return;
        var base = getGameAssembly().base;
        try { Interceptor.revert(base.add(0xB63EC0)); } catch(e) {}
        try { Interceptor.revert(base.add(0xB79008)); } catch(e) {}
        enabled = false;
        sendLog('info', '近战', 'v10 已禁用');
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info', '近战', '倍数 → ' + v + 'x');
    };

    sendLog('info', '近战', 'v10 已加载，自动启用...');
    enable();

})();
