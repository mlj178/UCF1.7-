// ============================================================
// 近战距离修改器 v12 — Interceptor.attach WPN_Knife.GetKnifeAttackData
//
// 策略: Hook WPN_Knife.GetKnifeAttackData (RVA 0xB63EC0)
//       IL2CPP 32-bit struct by-value return: args[0] = retbuf 指针
//       在 onLeave 中直接修改 retbuf+0x4 (range 字段)
//       不调用任何 NativeFunction（避免跨线程崩溃）
//       使用"前N把刀=玩家"启发式（与 speed_knife_v5 相同的已验证策略）
//
//       ★ 不写只读内存（retbuf 是调用者栈上分配的）
//       ★ 不改 ScriptableObject（不影响其他玩家/Bot）
//       ★ 不跨线程调用 NativeFunction（避免 v10 式闪退）
//       ★ 全模式生效（WPN_Knife 是所有近战武器的基类）
//
// 为何 v10 闪退: 在 Interceptor.attach 的 onLeave 回调中
//               调用 NativeFunction(isMyWeapon) → Frida 线程执行
//               游戏代码 → 内存访问违规/GC冲突 → 闪退
//
// 为何 v8 影响Bot: 直接写入 WeaponData_Knife.knifeAttacks[].range
//                 → ScriptableObject 全局共享 → 全员生效
//
// 启发式原理: 玩家先于 Bot 生成，玩家先按攻击键
//           前 2~3 把触发 GetKnifeAttackData 的刀属于玩家
//           （已验证策略，参考 speed_knife_v5 / knife_range_v6~v7）
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
    var playerWeaponSet = {};
    var playerWeaponCount = 0;
    var MAX_PLAYER_WEAPONS = 3;
    var rangeLogCount = 0;

    function modifyRange(retbuf, attackIdx) {
        try {
            var rangeAddr = retbuf.add(0x4);
            var origRange = rangeAddr.readFloat();

            if (!(origRange > 0.3 && origRange < 500)) return false;

            var newRange = origRange * KNIFE_RANGE_MULTIPLIER;
            rangeAddr.writeFloat(newRange);

            rangeLogCount++;
            if (rangeLogCount <= 8) {
                sendLog('info', '近战',
                    '[攻击#' + rangeLogCount + '] idx=' + attackIdx +
                    ' range ' + origRange.toFixed(2) +
                    ' → ' + newRange.toFixed(2) +
                    ' (' + KNIFE_RANGE_MULTIPLIER + 'x)');
            }

            return true;
        } catch(e) {
            if (rangeLogCount <= 2) {
                sendLog('error', '近战', 'modifyRange异常: ' + e.message);
            }
            return false;
        }
    }

    function enable() {
        if (enabled) return;

        var mod = Process.findModuleByName('GameAssembly.dll');
        if (!mod) {
            sendLog('error', '近战', 'GameAssembly.dll 未找到');
            return;
        }
        var base = mod.base;

        playerWeaponSet = {};
        playerWeaponCount = 0;
        rangeLogCount = 0;

        // ================================================================
        // Hook 1: WPN_Knife.GetKnifeAttackData (RVA 0xB63EC0)
        // IL2CPP 32-bit struct return:
        //   args[0] = retbuf (KnifeAttackData_o*)
        //   args[1] = this   (WPN_Knife_o*)
        //   args[2] = attackIndex (int32_t)
        //   args[3] = methodInfo
        // ================================================================
        try {
            hookList.push({
                name: 'GetKnifeAttackData',
                listener: Interceptor.attach(base.add(0xB63EC0), {
                    onEnter: function(args) {
                        this.retbuf = args[0];
                        this.wpnSelf = args[1];
                        this.attackIdx = args[2].toInt32();
                    },
                    onLeave: function(retval) {
                        try {
                            var key = this.wpnSelf.toString();

                            if (playerWeaponSet[key]) {
                                modifyRange(this.retbuf, this.attackIdx);
                                return;
                            }

                            if (playerWeaponCount < MAX_PLAYER_WEAPONS) {
                                playerWeaponSet[key] = true;
                                playerWeaponCount++;
                                sendLog('info', '近战',
                                    '发现武器 #' + playerWeaponCount +
                                    ' @ ' + this.wpnSelf +
                                    ' (idx=' + this.attackIdx + ')');
                                modifyRange(this.retbuf, this.attackIdx);
                                return;
                            }

                            if (rangeLogCount < 2) {
                                sendLog('warn', '近战',
                                    'Bot武器跳过: ' + this.wpnSelf);
                                rangeLogCount++;
                            }
                        } catch(e) {
                            if (rangeLogCount < 2) {
                                sendLog('error', '近战', 'onLeave异常: ' + e.message);
                                rangeLogCount++;
                            }
                        }
                    }
                })
            });
            sendLog('info', '近战', 'Hook WPN_Knife.GetKnifeAttackData @ ' + base.add(0xB63EC0));
        } catch(e) {
            sendLog('error', '近战', 'Hook 1 失败: ' + e.message);
        }

        // ================================================================
        // Hook 2: Weapon.GetKnifeAttackData 基类兜底 (RVA 0xB79008)
        // 某些非 WPN_Knife 的近战子类走基类路径
        // ================================================================
        try {
            hookList.push({
                name: 'GetKnifeAttackData_Base',
                listener: Interceptor.attach(base.add(0xB79008), {
                    onEnter: function(args) {
                        this.retbuf = args[0];
                        this.wpnSelf = args[1];
                    },
                    onLeave: function(retval) {
                        try {
                            var key = this.wpnSelf.toString();
                            if (playerWeaponSet[key]) {
                                modifyRange(this.retbuf, -1);
                            }
                        } catch(e) {}
                    }
                })
            });
            sendLog('info', '近战', 'Hook Weapon.GetKnifeAttackData @ ' + base.add(0xB79008));
        } catch(e) {
            sendLog('warn', '近战', 'Hook 2 失败: ' + e.message);
        }

        // ================================================================
        // 房间切换 → 重置武器缓存
        // ================================================================
        var cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
        for (var i = 0; i < cleanupAddrs.length; i++) {
            try {
                Interceptor.attach(base.add(cleanupAddrs[i]), {
                    onEnter: function() {
                        playerWeaponSet = {};
                        playerWeaponCount = 0;
                        rangeLogCount = 0;
                        sendLog('info', '近战', '房间切换，重置武器缓存');
                    }
                });
            } catch(e) {}
        }

        enabled = true;
        sendLog('info', '近战', 'v12 已启用 (' + KNIFE_RANGE_MULTIPLIER +
            'x, 启发式玩家识别=' + MAX_PLAYER_WEAPONS + '把)');
    }

    function disable() {
        for (var i = 0; i < hookList.length; i++) {
            try { hookList[i].listener.detach(); } catch(e) {}
        }
        hookList = [];
        playerWeaponSet = {};
        playerWeaponCount = 0;
        enabled = false;
        sendLog('info', '近战', 'v12 已禁用');
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info', '近战', '倍数 → ' + v + 'x');
    };

    sendLog('info', '近战', 'v12 已加载，自动启用...');
    enable();

})();
