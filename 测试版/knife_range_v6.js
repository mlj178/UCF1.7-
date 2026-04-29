// ============================================================
// 近战距离修改器 v6 — speed_knife_v5 玩家识别 + 32-bit 精确内存
//
// 玩家识别策略（来自 speed_knife_v5，已验证有效）:
//   前 MAX_PLAYER_WEAPONS=2 个出现的 WPN_Knife → 玩家武器
//   原理: 玩家总是第一个攻击的，前2把刀肯定是玩家的
//
// 内存路径（来自 v4 hex dump + dump.cs 验证）:
//   32-bit Il2CppArray: head=0x10, KnifeAttackData size=0x1C
//   WPN_Knife+0x68 → WeaponData_Knife*
//   WeaponData+0xC0 → KnifeAttackData[] (shared ScriptableObject)
//   arr[attackType-1]+0x04 → float range
//
// 写入策略:
//   onEnter: 写入倍数值 → 攻击判定读取到倍数值
//   onLeave: 恢复原始值 → Bot 攻击不受影响
//
// ★ 重要: 必须重启游戏测试，旧 v4 的写入会残留在堆内存中
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
        try { send(JSON.stringify({type:'log',level:level,module:module,message:msg})); } catch(e){}
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

    // ============================================================
    // 玩家识别（来自 speed_knife_v5 已验证策略）
    // ============================================================
    var playerWeapons = {};
    var playerWeaponCount = 0;
    var MAX_PLAYER_WEAPONS = 2;

    function isPlayerWeapon(wpnPtr) {
        if (!wpnPtr || wpnPtr.isNull()) return false;
        var key = wpnPtr.toString();
        if (playerWeapons[key]) return true;  // 已知玩家武器
        if (playerWeaponCount < MAX_PLAYER_WEAPONS) {
            playerWeapons[key] = true;
            playerWeaponCount++;
            sendLog('info', '近战距离', 'Player weapon #' + playerWeaponCount + ' → ' + wpnPtr);
            return true;
        }
        return false;  // Bot
    }

    // ============================================================
    // 32-bit Il2CppArray + KnifeAttackData 解析
    // ============================================================
    function getArrayLength32(arrPtr) {
        return arrPtr.add(0x0C).readU32();
    }

    // 从 WeaponData_Knife 读取指定 index 的 range
    function readKnifeRange32(dataPtr, index) {
        var arrPtr = dataPtr.add(0xC0).readPointer();
        if (!arrPtr || arrPtr.isNull()) return -1;
        var len = getArrayLength32(arrPtr);
        if (index < 0 || index >= len) return -1;
        // elemStart=0x10, elemSize=0x1C, range offset=+0x4
        return arrPtr.add(0x10 + index * 0x1C + 0x4).readFloat();
    }

    function getRangeAddr32(dataPtr, index) {
        var arrPtr = dataPtr.add(0xC0).readPointer();
        if (!arrPtr || arrPtr.isNull()) return null;
        return arrPtr.add(0x10 + index * 0x1C + 0x4);
    }

    // ============================================================
    // 主逻辑
    // ============================================================
    var enabled = false;
    var playAnimHook = null;
    var attackCount = 0;
    var maxVerbose = 10;

    // onEnter/onLeave 恢复机制
    var restoreAddr = null;
    var restoreValue = 0.0;

    function enable() {
        if (enabled) return;
        var gm = getGameAssembly();
        if (!gm) { sendLog('error', '近战距离', '未找到 GameAssembly'); return; }
        var base = gm.base;

        playerWeapons = {};
        playerWeaponCount = 0;
        attackCount = 0;

        var hookAddr = base.add(0xB642B0);
        sendLog('info', '近战距离', 'v6 玩家前' + MAX_PLAYER_WEAPONS + '把刀 Hook PlayKnifeAttackAnim @ ' + hookAddr);

        playAnimHook = Interceptor.attach(hookAddr, {
            onEnter: function(args) {
                attackCount++;
                var wpnKnife = args[0];
                var attackType = args[1].toInt32();  // 1=Combo1, 2=Combo2, 3=Bigshot

                var verbose = attackCount <= maxVerbose;

                if (!wpnKnife || wpnKnife.isNull()) return;

                // ★ speed_knife_v5 识别策略: 前2把刀 = 玩家
                if (!isPlayerWeapon(wpnKnife)) return;

                if (verbose) {
                    sendLog('info', '近战距离', '');
                    sendLog('info', '近战距离', '===== 攻击 #' + attackCount + ' type=' + attackType + ' =====');
                    sendLog('info', '近战距离', 'WPN_Knife=' + wpnKnife);
                }

                try {
                    var dataPtr = wpnKnife.add(0x68).readPointer();
                    if (!dataPtr || dataPtr.isNull()) {
                        if (verbose) sendLog('warn', '近战距离', 'WeaponData 为空');
                        return;
                    }

                    var arrPtr = dataPtr.add(0xC0).readPointer();
                    if (!arrPtr || arrPtr.isNull()) {
                        if (verbose) sendLog('warn', '近战距离', 'knifeAttacks 为空');
                        return;
                    }

                    var arrLen = getArrayLength32(arrPtr);
                    if (attackType < 1 || attackType > arrLen) {
                        if (verbose) sendLog('warn', '近战距离', 'attackType=' + attackType + ' 超出数组长度=' + arrLen);
                        return;
                    }

                    var rangeAddr = arrPtr.add(0x10 + (attackType - 1) * 0x1C + 0x4);
                    var originalRange = rangeAddr.readFloat();

                    if (originalRange <= 0 || originalRange > 500 || isNaN(originalRange)) {
                        if (verbose) sendLog('warn', '近战距离', '原始 range 异常: ' + originalRange);
                        return;
                    }

                    var newRange = originalRange * KNIFE_RANGE_MULTIPLIER;
                    rangeAddr.writeFloat(newRange);

                    restoreAddr = rangeAddr;
                    restoreValue = originalRange;

                    if (verbose) {
                        sendLog('info', '近战距离',
                            'type=' + attackType + ' range ' +
                            originalRange.toFixed(2) + ' → ' + newRange.toFixed(2) +
                            ' @ ' + rangeAddr);
                        sendLog('info', '近战距离', '(onLeave 时将恢复原始值)');
                    }

                    if (attackCount % 20 === 0 && attackCount > maxVerbose) {
                        sendLog('info', '近战距离', '已处理 ' + attackCount + ' 次攻击 (稳定运行)');
                    }

                } catch (e) {
                    if (verbose) sendLog('error', '近战距离', '异常: ' + e);
                }
            },
            onLeave: function(retval) {
                if (restoreAddr) {
                    try {
                        restoreAddr.writeFloat(restoreValue);
                    } catch(e) {}
                    restoreAddr = null;
                }
            }
        });

        // 切房间清理
        var cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
        for (var i = 0; i < cleanupAddrs.length; i++) {
            try {
                Interceptor.attach(base.add(cleanupAddrs[i]), {
                    onEnter: function() {
                        playerWeapons = {};
                        playerWeaponCount = 0;
                        restoreAddr = null;
                        sendLog('info', '近战距离', '房间切换，缓存与恢复状态已清理');
                    }
                });
            } catch(e) {}
        }

        enabled = true;
        sendLog('info', '近战距离', 'v6 已启用 (' + KNIFE_RANGE_MULTIPLIER + 'x, 前' + MAX_PLAYER_WEAPONS + '把刀=玩家)');
        sendLog('info', '近战距离', '★ 请确保已重启游戏（旧版本写入会残留）');
    }

    function disable() {
        if (!enabled) return;
        if (playAnimHook) { playAnimHook.detach(); playAnimHook = null; }
        playerWeapons = {};
        playerWeaponCount = 0;
        enabled = false;
        sendLog('info', '近战距离', 'v6 已禁用 (共 ' + attackCount + ' 次攻击)');
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info', '近战距离', '倍数 → ' + v + 'x');
    };

    sendLog('info', '近战距离', 'v6 已加载，自动启用中...');
    enable();

})();
