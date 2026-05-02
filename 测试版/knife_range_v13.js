// ============================================================
// 近战距离修改器 v13 — 修复版: retval + 启发式 + 三重Hook
//
// ★ v12 闪退根因: 在 onLeave 中用了 this.retbuf=args[0] 来定位
//    KnifeAttackData。Frida 可能剥离了 IL2CPP struct return 的
//    隐藏 retbuf 参数，导致 args[0] 实际指向 WPN_Knife* (this)，
//    写入 this+0x4 损坏了武器对象 → 几次攻击后进程终止。
//
// ★ 修复: onLeave 中使用 retval (Frida 保证指向返回结构体)
//    onEnter 只用 args[1]=this 做武器识别，不用 args[0]。
//
// ★ 玩家识别: speed_knife_v5 已验证策略 → 前 2 把刀 = 玩家
//    原理: 本地玩家先于 Bot 生成，且玩家先按攻击键。
//    不调用任何 NativeFunction（避免 v10 式跨线程崩溃）。
//
// ★ 全模式: 三重 Hook
//    - WPN_Knife.GetKnifeAttackData   (0xB63EC0) 主路径
//    - Weapon.GetKnifeAttackData      (0xB79008) 基类兜底
//    - WPN_Knife.OnSpecialBtnDown     (0xB64240) 最早触发（用于发现）
//
// KnifeAttackData 结构体 (il2cpp.h:164007):
//   +0x0  float  damage
//   +0x4  float  range      ← 修改目标
//   +0x8  float  angle
// ============================================================

(function() {
    'use strict';

    var KNIFE_RANGE_MULTIPLIER = 50.0;

    function sendLog(level, module, msg) {
        var logMsg = '[' + module + '] ' + msg;
        if (level === 'error') console.error(logMsg);
        else if (level === 'warn') console.warn(logMsg);
        else console.log(logMsg);
    }

    var enabled = false;
    var hookList = [];
    var playerWeapons = {};
    var playerWeaponCount = 0;
    var MAX_PLAYER_WEAPONS = 2;
    var rangeLogCount = 0;

    function enable() {
        if (enabled) return;

        var mod = Process.findModuleByName('GameAssembly.dll');
        if (!mod) {
            sendLog('error', '近战', 'GameAssembly.dll 未找到');
            return;
        }
        var base = mod.base;

        playerWeapons = {};
        playerWeaponCount = 0;
        rangeLogCount = 0;

        // ================================================================
        // Hook 1: WPN_Knife.GetKnifeAttackData (RVA 0xB63EC0)
        // IL2CPP 32-bit struct return → onLeave retval = KnifeAttackData*
        // args[1] = this (WPN_Knife*), args[2] = attackIndex
        // ================================================================
        try {
            hookList.push(Interceptor.attach(base.add(0xB63EC0), {
                onEnter: function(args) {
                    this.wpnSelf = args[1];
                    this.attackIdx = args[2].toInt32();
                },
                onLeave: function(retval) {
                    try {
                        var key = this.wpnSelf.toString();

                        if (playerWeapons[key]) {
                            var rangeAddr = retval.add(0x4);
                            var orig = rangeAddr.readFloat();
                            if (orig > 0.3 && orig < 500) {
                                rangeAddr.writeFloat(orig * KNIFE_RANGE_MULTIPLIER);
                                rangeLogCount++;
                                if (rangeLogCount <= 10) {
                                    sendLog('info', '近战',
                                        '[玩家#' + rangeLogCount + '] idx=' + this.attackIdx +
                                        ' range ' + orig.toFixed(2) +
                                        ' → ' + (orig * KNIFE_RANGE_MULTIPLIER).toFixed(2) +
                                        ' (' + KNIFE_RANGE_MULTIPLIER + 'x)');
                                }
                            }
                            return;
                        }

                        if (playerWeaponCount < MAX_PLAYER_WEAPONS) {
                            playerWeapons[key] = true;
                            playerWeaponCount++;
                            sendLog('info', '近战',
                                '发现武器 #' + playerWeaponCount +
                                ' @ ' + this.wpnSelf);

                            var rangeAddr = retval.add(0x4);
                            var orig = rangeAddr.readFloat();
                            if (orig > 0.3 && orig < 500) {
                                rangeAddr.writeFloat(orig * KNIFE_RANGE_MULTIPLIER);
                                rangeLogCount++;
                                sendLog('info', '近战',
                                    '[首次#' + rangeLogCount + '] idx=' + this.attackIdx +
                                    ' range ' + orig.toFixed(2) +
                                    ' → ' + (orig * KNIFE_RANGE_MULTIPLIER).toFixed(2) +
                                    ' (' + KNIFE_RANGE_MULTIPLIER + 'x)');
                            }
                            return;
                        }

                        if (rangeLogCount < 1) {
                            sendLog('warn', '近战', 'Bot跳过: ' + this.wpnSelf);
                            rangeLogCount++;
                        }
                    } catch(e) {
                        if (rangeLogCount < 2) {
                            sendLog('error', '近战', 'onLeave异常: ' + e.message);
                            rangeLogCount++;
                        }
                    }
                }
            }));
            sendLog('info', '近战', 'Hook GetKnifeAttackData @ ' + base.add(0xB63EC0));
        } catch(e) {
            sendLog('error', '近战', 'Hook 1 失败: ' + e.message);
        }

        // ================================================================
        // Hook 2: Weapon.GetKnifeAttackData 基类兜底 (RVA 0xB79008)
        // ================================================================
        try {
            hookList.push(Interceptor.attach(base.add(0xB79008), {
                onEnter: function(args) {
                    this.wpnSelf = args[1];
                },
                onLeave: function(retval) {
                    try {
                        var key = this.wpnSelf.toString();
                        if (!playerWeapons[key]) return;

                        var rangeAddr = retval.add(0x4);
                        var orig = rangeAddr.readFloat();
                        if (orig > 0.3 && orig < 500) {
                            rangeAddr.writeFloat(orig * KNIFE_RANGE_MULTIPLIER);
                        }
                    } catch(e) {}
                }
            }));
            sendLog('info', '近战', 'Hook Weapon.GetKnifeAttackData @ ' + base.add(0xB79008));
        } catch(e) {
            sendLog('warn', '近战', 'Hook 2 失败: ' + e.message);
        }

        // ================================================================
        // Hook 3: WPN_Knife.OnSpecialBtnDown (RVA 0xB64240)
        // 最早触发点，用于兜底发现（某些模式可能先走这条路）
        // ================================================================
        try {
            hookList.push(Interceptor.attach(base.add(0xB64240), {
                onEnter: function(args) {
                    var wpnSelf = args[0];
                    if (!wpnSelf || wpnSelf.isNull()) return;
                    var key = wpnSelf.toString();
                    if (playerWeapons[key]) return;
                    if (playerWeaponCount >= MAX_PLAYER_WEAPONS) return;

                    playerWeapons[key] = true;
                    playerWeaponCount++;
                    sendLog('info', '近战',
                        '发现武器 #' + playerWeaponCount +
                        ' @ ' + wpnSelf + ' (via OnSpecialBtnDown)');
                }
            }));
            sendLog('info', '近战', 'Hook OnSpecialBtnDown @ ' + base.add(0xB64240));
        } catch(e) {}

        // ================================================================
        // 房间切换 → 重置武器缓存
        // ================================================================
        var cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
        for (var i = 0; i < cleanupAddrs.length; i++) {
            try {
                Interceptor.attach(base.add(cleanupAddrs[i]), {
                    onEnter: function() {
                        playerWeapons = {};
                        playerWeaponCount = 0;
                        rangeLogCount = 0;
                        sendLog('info', '近战', '房间切换，重置武器缓存');
                    }
                });
            } catch(e) {}
        }

        enabled = true;
        sendLog('info', '近战', 'v13 已启用 (' + KNIFE_RANGE_MULTIPLIER +
            'x, 玩家识别=' + MAX_PLAYER_WEAPONS + '把, retval写入)');
    }

    function disable() {
        for (var i = 0; i < hookList.length; i++) {
            try { hookList[i].detach(); } catch(e) {}
        }
        hookList = [];
        playerWeapons = {};
        playerWeaponCount = 0;
        enabled = false;
        sendLog('info', '近战', 'v13 已禁用');
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info', '近战', '倍数 → ' + v + 'x');
    };

    sendLog('info', '近战', 'v13 已加载，自动启用...');
    enable();

})();
