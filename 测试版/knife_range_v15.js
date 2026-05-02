// ============================================================
// 近战距离修改器 v15 — retval修复 + 启发式 + 零NativeFunction
//
// 继承 v8 的稳定性: 启发式玩家识别（前2把刀=玩家），不调任何NativeFunction
// 继承 v12 的功能: Hook GetKnifeAttackData，在 onLeave 改 range
//
// ★ v12 闪退根因:
//   onEnter: this.retbuf = args[0] ← 在 IL2CPP 32-bit 中，Frida 可能
//           剥离了隐藏 retbuf 参数，args[0] 实际是 this(WPN_Knife*)
//   onLeave: this.retbuf.add(0x4).writeFloat(...) ← 写入武器对象内部
//           → 对象损坏 → 几次攻击后进程终止
//
// ★ v15 修复: 在 onLeave 中用 retval (Frida 保证指向返回结构体)
//
// ★ v14 闪退根因: isMyWeapon NativeFunction 在 onEnter 中被调用
//               游戏初始化期间 GetKnifeAttackData 被触发
//               → 武器未就绪 → NativeFunction 崩溃
//
// ★ v15 修复: 完全不用 NativeFunction
//           启发式（与 v8/speed_knife_v5 相同策略）
//
// 玩家识别: 前 2 个不同的 WPN_Knife 实例 → 假定为玩家武器
//          原因: 本地玩家先于 Bot 生成，且先按攻击键
//          新房间自动重置计数
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
    var rangeLogCount = 0;

    function enable() {
        if (enabled) return;

        var mod = Process.findModuleByName('GameAssembly.dll');
        if (!mod) { sendLog('error', '近战', 'GameAssembly.dll 未找到'); return; }
        var base = mod.base;

        playerWeapons = {};
        playerWeaponCount = 0;
        rangeLogCount = 0;

        // ============================================================
        // Hook 1: WPN_Knife.GetKnifeAttackData (RVA 0xB63EC0)
        // onEnter 仅记录 args[1]=wpn, args[2]=attackIdx
        // onLeave 用 retval (非 args[0]) 定位 KnifeAttackData
        // ============================================================
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
                            modifyRange(retval, this.attackIdx);
                            return;
                        }

                        if (playerWeaponCount < 2) {
                            playerWeapons[key] = true;
                            playerWeaponCount++;
                            sendLog('info', '近战',
                                '发现玩家武器 #' + playerWeaponCount +
                                ' @ ' + this.wpnSelf);
                            modifyRange(retval, this.attackIdx);
                            return;
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
        } catch(e) { sendLog('error', '近战', 'Hook 1 失败: ' + e.message); }

        // ============================================================
        // Hook 2: Weapon.GetKnifeAttackData 基类兜底 (RVA 0xB79008)
        // ============================================================
        try {
            hookList.push(Interceptor.attach(base.add(0xB79008), {
                onEnter: function(args) {
                    this.wpnSelf = args[1];
                },
                onLeave: function(retval) {
                    try {
                        var key = this.wpnSelf.toString();
                        if (playerWeapons[key]) {
                            modifyRange(retval, -1);
                        }
                    } catch(e) {}
                }
            }));
            sendLog('info', '近战', 'Hook Weapon.GetKnifeAttackData @ ' + base.add(0xB79008));
        } catch(e) {}

        // ============================================================
        // 房间切换 → 重置武器缓存
        // (v8 已验证的地址: GameRoundEnd, OnStartRound, NanoStart)
        // ============================================================
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
        sendLog('info', '近战', 'v15 已启用 (' + KNIFE_RANGE_MULTIPLIER +
            'x, 启发式玩家识别=2把, retval写入)');
    }

    // ================================================================
    // modifyRange: 用 retval(不是 args[0]) 定位返回结构体
    // retval = Frida 保证指向函数返回的 KnifeAttackData 结构体
    // +0x4 = range (float), 来自 il2cpp.h KnifeAttackData_Fields
    // ================================================================
    function modifyRange(retval, attackIdx) {
        try {
            var rangeAddr = retval.add(0x4);
            var orig = rangeAddr.readFloat();

            if (!(orig > 0.3 && orig < 500)) return;

            var newVal = orig * KNIFE_RANGE_MULTIPLIER;
            rangeAddr.writeFloat(newVal);

            rangeLogCount++;
            if (rangeLogCount <= 10) {
                sendLog('info', '近战',
                    '[攻击#' + rangeLogCount + '] idx=' + attackIdx +
                    ' range ' + orig.toFixed(2) +
                    ' → ' + newVal.toFixed(2));
            }
        } catch(e) {}
    }

    function disable() {
        for (var i = 0; i < hookList.length; i++) {
            try { hookList[i].detach(); } catch(e) {}
        }
        hookList = [];
        playerWeapons = {};
        playerWeaponCount = 0;
        enabled = false;
        sendLog('info', '近战', 'v15 已禁用');
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info', '近战', '倍数 → ' + v + 'x');
    };

    sendLog('info', '近战', 'v15 已加载，自动启用...');
    enable();

})();
