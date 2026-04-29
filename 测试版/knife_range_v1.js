// ============================================================
// 近战距离修改器 v1
// 原理: Hook WPN_Knife$$KnifeAttackEvent (RVA 0xB63DD0)
//       利用 args[1] 攻击索引精确定位 KnifeAttackData.range 并修改
// 内存路径:
//   WPN_Knife (+0x68) → WeaponData_Knife* (+0xC0 + index*0x10) → KnifeAttackData
//   KnifeAttackData + 0x4 → float range  ← 写入目标
// 生命周期:
//   onEnter: 保存原始值 → 写入倍数值
//   onLeave: 恢复原始值（只影响自己的攻击瞬间，不影响机器人）
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

    var enabled = false;
    var hookListener = null;
    var savedOriginalRange = 0.0;
    var savedRangeAddr = null;
    var attackCount = 0;

    function enable() {
        if (enabled) return;
        var gm = getGameAssembly();
        if (!gm) {
            sendLog('error', '近战距离', '未找到 GameAssembly');
            return;
        }

        var base = gm.base;
        var hookAddr = base.add(0xB63DD0);
        attackCount = 0;

        sendLog('info', '近战距离', 'Hook KnifeAttackEvent @ ' + hookAddr);

        hookListener = Interceptor.attach(hookAddr, {
            onEnter: function(args) {
                attackCount++;
                var self = args[0];
                var index = args[1].toInt32();

                if (attackCount <= 5) {
                    sendLog('info', '近战距离', '[KnifeAttackEvent] self=' + self + ' 攻击索引=' + index + ' #' + attackCount);
                }

                try {
                    var dataPtr = self.add(0x68).readPointer();
                    if (!dataPtr || dataPtr.isNull()) {
                        if (attackCount <= 3)
                            sendLog('warn', '近战距离', 'WeaponData 指针为空! self=' + self);
                        return;
                    }

                    var rangeAddr = dataPtr.add(0xC0 + index * 0x10 + 0x4);
                    savedOriginalRange = rangeAddr.readFloat();
                    savedRangeAddr = rangeAddr;

                    if (isNaN(savedOriginalRange) || savedOriginalRange <= 0) {
                        if (attackCount <= 3)
                            sendLog('warn', '近战距离', '原始 range 异常: ' + savedOriginalRange + ' dataPtr=' + dataPtr + ' index=' + index);
                        savedRangeAddr = null;
                        return;
                    }

                    var newRange = savedOriginalRange * KNIFE_RANGE_MULTIPLIER;
                    rangeAddr.writeFloat(newRange);

                    if (attackCount <= 5) {
                        sendLog('info', '近战距离', '攻击#' + index + ': range ' +
                            savedOriginalRange.toFixed(2) + ' → ' + newRange.toFixed(2) +
                            ' @ ' + rangeAddr + ' (data=' + dataPtr + ')');
                    }
                } catch (e) {
                    if (attackCount <= 3)
                        sendLog('error', '近战距离', '内存操作异常: ' + e);
                }
            },
            onLeave: function(retval) {
                if (savedRangeAddr && savedOriginalRange > 0) {
                    try {
                        savedRangeAddr.writeFloat(savedOriginalRange);
                    } catch (e) {}
                    savedRangeAddr = null;
                    savedOriginalRange = 0;
                }
            }
        });

        enabled = true;
        sendLog('info', '近战距离', 'v1 已启用 (' + KNIFE_RANGE_MULTIPLIER + 'x)');
        sendLog('info', '近战距离', '按近战攻击键测试效果...');
    }

    function disable() {
        if (!enabled) return;
        if (hookListener) {
            hookListener.detach();
            hookListener = null;
        }
        enabled = false;
        sendLog('info', '近战距离', '已禁用 (共攻击 ' + attackCount + ' 次)');
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info', '近战距离', '倍数 → ' + v + 'x');
    };

    sendLog('info', '近战距离', 'v1 脚本已加载');
    sendLog('info', '近战距离', 'enableKnifeRange() 启用 / disableKnifeRange() 禁用 / setKnifeRangeMultiplier(n)');

})();
