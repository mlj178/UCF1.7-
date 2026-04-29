// ============================================================
// 近战距离修改器 v9 — 全模式适配（3 Hook + Memory.protect）
//
// 策略: 参考 speed_knife_v5 的三重 Hook 实现全模式覆盖
//       OnSpecialBtnDown (0xB64240) — 最早触发，按攻击键
//       PlayKnifeAttackAnim (0xB642B0) — 动画触发
//       AnimSpeedSetting (0xB63BD0) — 速度设置时兜底
//
//       首次发现新武器时:
//         1. Memory.protect 解锁只读页
//         2. 一次性写入倍数值到 knifeAttacks[0~2].range
//         3. 不重复写入，不 Timer
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

    var discovered = {};
    var discoveredCount = 0;

    function unlockAndWriteAll(dataPtr) {
        var key = dataPtr.toString();
        if (discovered[key]) return;
        discovered[key] = true;
        discoveredCount++;

        var arrPtr = dataPtr.add(0xC0).readPointer();
        if (!arrPtr || arrPtr.isNull()) {
            sendLog('warn', '近战', 'knifeAttacks 为空, dataPtr=' + dataPtr);
            return;
        }

        var arrLen = arrPtr.add(0x0C).readU32();
        if (arrLen < 1 || arrLen > 20) return;

        var successCount = 0;
        for (var i = 0; i < arrLen; i++) {
            var rangeAddr = arrPtr.add(0x10 + i * 0x1C + 0x4);
            try {
                var orig = rangeAddr.readFloat();
                if (!(orig > 0.3 && orig < 500)) continue;

                // Memory.protect 解锁只读页
                var pageAddr = rangeAddr.and(ptr(0xFFFFF000));
                Memory.protect(pageAddr, 0x1000, 'rwx');

                var newVal = orig * KNIFE_RANGE_MULTIPLIER;
                rangeAddr.writeFloat(newVal);

                Memory.protect(pageAddr, 0x1000, 'r-x');

                successCount++;
                if (successCount <= 3) {
                    sendLog('info', '近战', '[' + i + '] range ' + orig.toFixed(2) + ' → ' + newVal.toFixed(2));
                }
            } catch(e) {
                if (successCount === 0) {
                    sendLog('warn', '近战', '写入失败 +0x' + (0x10 + i * 0x1C + 0x4).toString(16) + ': ' + e.message);
                }
            }
        }

        if (successCount > 0) {
            sendLog('info', '近战', '已锁定 ' + successCount + '/' + arrLen + ' @ ' + dataPtr + ' (' + KNIFE_RANGE_MULTIPLIER + 'x)');
        }
    }

    function onKnifeAttack(wpnKnife, source) {
        if (!wpnKnife || wpnKnife.isNull()) return;
        try {
            var dataPtr = wpnKnife.add(0x68).readPointer();
            if (!dataPtr || dataPtr.isNull()) return;
            var key = dataPtr.toString();
            if (discovered[key]) return;
            if (discoveredCount < 3) sendLog('info', '近战', '发现武器 ' + source + ' @ ' + wpnKnife);
            unlockAndWriteAll(dataPtr);
        } catch(e) {}
    }

    var hookList = [];

    function enable() {
        if (hookList.length > 0) return;
        var gm = getGameAssembly();
        if (!gm) { sendLog('error', '近战', 'GameAssembly 未找到'); return; }
        var base = gm.base;

        discovered = {};
        discoveredCount = 0;

        // Hook 1: OnSpecialBtnDown — 最早触发
        try {
            hookList.push({
                name: 'OnSpecialBtnDown',
                listener: Interceptor.attach(base.add(0xB64240), {
                    onEnter: function(args) {
                        onKnifeAttack(args[0], 'OnSpecialBtnDown');
                    }
                })
            });
        } catch(e) {}

        // Hook 2: PlayKnifeAttackAnim — 动画触发
        try {
            hookList.push({
                name: 'PlayKnifeAttackAnim',
                listener: Interceptor.attach(base.add(0xB642B0), {
                    onEnter: function(args) {
                        onKnifeAttack(args[0], 'PlayAnim');
                    }
                })
            });
        } catch(e) {}

        // Hook 3: AnimSpeedSetting — 兜底
        try {
            hookList.push({
                name: 'AnimSpeedSetting',
                listener: Interceptor.attach(base.add(0xB63BD0), {
                    onEnter: function(args) {
                        onKnifeAttack(args[0], 'AnimSpeed');
                    }
                })
            });
        } catch(e) {}

        sendLog('info', '近战', '已 Hook ' + hookList.length + ' 个函数，自动解锁只读页');

        // 切房间清理
        var cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
        for (var i = 0; i < cleanupAddrs.length; i++) {
            try {
                Interceptor.attach(base.add(cleanupAddrs[i]), {
                    onEnter: function() {
                        discovered = {};
                        discoveredCount = 0;
                    }
                });
            } catch(e) {}
        }
    }

    function disable() {
        for (var i = 0; i < hookList.length; i++) {
            try { hookList[i].listener.detach(); } catch(e) {}
        }
        hookList = [];
        discovered = {};
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info', '近战', '倍数 → ' + v + 'x（重启游戏后生效）');
    };

    sendLog('info', '近战', 'v9 全模式已加载，自动启用...');
    enable();

})();
