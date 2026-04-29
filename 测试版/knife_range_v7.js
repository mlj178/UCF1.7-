// ============================================================
// 近战距离修改器 v7 — 写入验证 + 内存读回对比
//
// 继承 v6 的玩家识别 and 32-bit 精确解析
// 新增: 每次写入后立即读回验证 + onLeave 验证恢复
//       定期打印内存中的当前 range 值
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

    // 玩家识别（前2把刀）
    var playerWeapons = {};
    var playerWeaponCount = 0;
    var MAX_PLAYER_WEAPONS = 2;

    function isPlayerWeapon(wpnPtr) {
        if (!wpnPtr || wpnPtr.isNull()) return false;
        var key = wpnPtr.toString();
        if (playerWeapons[key]) return true;
        if (playerWeaponCount < MAX_PLAYER_WEAPONS) {
            playerWeapons[key] = true;
            playerWeaponCount++;
            return true;
        }
        return false;
    }

    // 32-bit: 从 WeaponData 读 range
    function readKnifeRange32(dataPtr, index) {
        var arrPtr = dataPtr.add(0xC0).readPointer();
        if (!arrPtr || arrPtr.isNull()) return -1;
        var len = arrPtr.add(0x0C).readU32();
        if (index < 0 || index >= len) return -1;
        return arrPtr.add(0x10 + index * 0x1C + 0x4).readFloat();
    }

    function getRangeAddr32(dataPtr, index) {
        var arrPtr = dataPtr.add(0xC0).readPointer();
        if (!arrPtr || arrPtr.isNull()) return null;
        return arrPtr.add(0x10 + index * 0x1C + 0x4);
    }

    function getArrayLength32(arrPtr) {
        return arrPtr.add(0x0C).readU32();
    }

    // 读取所有攻击类型的 range（用于定期验证）
    function readAllRanges(dataPtr) {
        var arrPtr = dataPtr.add(0xC0).readPointer();
        if (!arrPtr || arrPtr.isNull()) return [];
        var len = getArrayLength32(arrPtr);
        var results = [];
        for (var i = 0; i < len; i++) {
            results.push(arrPtr.add(0x10 + i * 0x1C + 0x4).readFloat());
        }
        return results;
    }

    // ============================================================
    var enabled = false;
    var playAnimHook = null;
    var attackCount = 0;
    var playerAttackCount = 0;
    var maxVerbose = 8;

    var restoreAddr = null;
    var restoreValue = 0.0;

    // 定期验证用的武器数据指针
    var lastDataPtr = null;

    function enable() {
        if (enabled) return;
        var gm = getGameAssembly();
        if (!gm) { sendLog('error', '近战距离', '未找到 GameAssembly'); return; }
        var base = gm.base;

        playerWeapons = {};
        playerWeaponCount = 0;
        attackCount = 0;
        playerAttackCount = 0;

        var hookAddr = base.add(0xB642B0);
        sendLog('info', '近战距离', 'v7 写入验证版 Hook @ ' + hookAddr);

        playAnimHook = Interceptor.attach(hookAddr, {
            onEnter: function(args) {
                attackCount++;
                var wpnKnife = args[0];
                var attackType = args[1].toInt32();

                if (!wpnKnife || wpnKnife.isNull()) return;
                if (!isPlayerWeapon(wpnKnife)) return;

                playerAttackCount++;
                var verbose = playerAttackCount <= maxVerbose;

                if (verbose) {
                    sendLog('info', '近战距离', '');
                    sendLog('info', '近战距离', '========== 玩家攻击 #' + playerAttackCount + ' (总计#' + attackCount + ') type=' + attackType + ' ==========');
                    sendLog('info', '近战距离', 'WPN_Knife=' + wpnKnife);
                }

                try {
                    var dataPtr = wpnKnife.add(0x68).readPointer();
                    if (!dataPtr || dataPtr.isNull()) return;
                    lastDataPtr = dataPtr;

                    var arrPtr = dataPtr.add(0xC0).readPointer();
                    if (!arrPtr || arrPtr.isNull()) return;

                    var arrLen = getArrayLength32(arrPtr);
                    if (attackType < 1 || attackType > arrLen) return;

                    var rangeAddr = getRangeAddr32(dataPtr, attackType - 1);

                    // ==== 写入前读回 ====
                    var beforeWrite = rangeAddr.readFloat();
                    if (verbose)
                        sendLog('info', '近战距离', 'Step1 写入前range=' + beforeWrite.toFixed(4) + ' @ ' + rangeAddr);

                    // ==== 写入倍数值 ====
                    var newRange = beforeWrite * KNIFE_RANGE_MULTIPLIER;
                    rangeAddr.writeFloat(newRange);

                    // ==== 写入后立即读回验证 ====
                    var afterWrite = rangeAddr.readFloat();
                    restoreAddr = rangeAddr;
                    restoreValue = beforeWrite;

                    if (verbose) {
                        sendLog('info', '近战距离', 'Step2 写入后range=' + afterWrite.toFixed(4) +
                            ' (期望=' + newRange.toFixed(4) + ')');
                        if (Math.abs(afterWrite - newRange) < 0.01) {
                            sendLog('info', '近战距离', '  ✓ 写入成功');
                        } else {
                            sendLog('error', '近战距离', '  ✗ 写入失败! 差异=' + (afterWrite - newRange).toFixed(4));
                        }
                    }

                    // ==== 打印所有攻击类型的 range（验证数据完整性） ====
                    if (verbose) {
                        var allRanges = readAllRanges(dataPtr);
                        var rangeStr = '';
                        for (var ri = 0; ri < allRanges.length; ri++) {
                            var marker = (ri + 1 === attackType) ? '★' : ' ';
                            rangeStr += '[' + (ri+1) + ']=' + allRanges[ri].toFixed(4) + marker + ' ';
                        }
                        sendLog('info', '近战距离', 'Step3 全部range: ' + rangeStr);
                    }

                    if (playerAttackCount % 10 === 0 && playerAttackCount > maxVerbose) {
                        var curVal = rangeAddr.readFloat();
                        sendLog('info', '近战距离', '玩家攻击#' + playerAttackCount + ' 内存range=' + curVal.toFixed(4) +
                            ' (原始=' + restoreValue.toFixed(2) + ')');
                    }

                } catch (e) {
                    if (verbose) sendLog('error', '近战距离', '异常: ' + e + '\n' + e.stack);
                }
            },
            onLeave: function(retval) {
                if (restoreAddr) {
                    try {
                        // 恢复前读回
                        var beforeRestore = restoreAddr.readFloat();

                        // 恢复
                        restoreAddr.writeFloat(restoreValue);

                        // 恢复后读回验证
                        var afterRestore = restoreAddr.readFloat();
                        var verbose = playerAttackCount <= maxVerbose;
                        if (verbose) {
                            sendLog('info', '近战距离', 'Step4 onLeave: before=' + beforeRestore.toFixed(4) +
                                ' → restored=' + afterRestore.toFixed(4) +
                                ' (期望=' + restoreValue.toFixed(4) + ')');
                            if (Math.abs(afterRestore - restoreValue) < 0.01) {
                                sendLog('info', '近战距离', '  ✓ 恢复成功');
                            } else {
                                sendLog('warn', '近战距离', '  ✗ 恢复异常!');
                            }
                        }
                    } catch(e) {}
                    restoreAddr = null;
                }
            }
        });

        // ==== 定时器：每 3 秒读内存验证 range 是否被覆盖 ====
        setInterval(function() {
            if (!lastDataPtr || lastDataPtr.isNull()) return;
            try {
                var allRanges = readAllRanges(lastDataPtr);
                var rangeStr = '';
                for (var ri = 0; ri < allRanges.length; ri++) {
                    rangeStr += '[' + (ri+1) + ']=' + allRanges[ri].toFixed(4) + ' ';
                }
                sendLog('info', '近战距离', '[Timer] 内存 range: ' + rangeStr);
            } catch(e) {}
        }, 3000);

        // 切房间清理
        var cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
        for (var i = 0; i < cleanupAddrs.length; i++) {
            try {
                Interceptor.attach(base.add(cleanupAddrs[i]), {
                    onEnter: function() {
                        playerWeapons = {};
                        playerWeaponCount = 0;
                        restoreAddr = null;
                        lastDataPtr = null;
                        sendLog('info', '近战距离', '房间切换，全部缓存已清理');
                    }
                });
            } catch(e) {}
        }

        enabled = true;
        sendLog('info', '近战距离', 'v7 写入验证版已启用 (' + KNIFE_RANGE_MULTIPLIER + 'x)');
    }

    function disable() {
        if (!enabled) return;
        if (playAnimHook) { playAnimHook.detach(); playAnimHook = null; }
        playerWeapons = {};
        playerWeaponCount = 0;
        enabled = false;
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info', '近战距离', '倍数 → ' + v + 'x');
    };

    sendLog('info', '近战距离', 'v7 写入验证版已加载，自动启用中...');
    enable();

})();
