// ============================================================
// 近战距离修改器 v8 — 一次写入，永久生效
//
// 策略: Hook PlayKnifeAttackAnim → 发现 WeaponData → 改一次 range
//       不改写，不恢复，不重复写入
//       WeaponData_Knife 是静态 ScriptableObject，游戏不会覆盖
//
// ★ 说明: WeaponData_Knife 是共享 ScriptableObject
//       所有玩家+Bot 共用同一份数据，物理上无法独立修改
//       Bot 也会受影响（和快刀改 attackSpeed 一样的共享特性）
// ============================================================

(function() {
    'use strict';

    var KNIFE_RANGE_MULTIPLIER = 50.0;
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
    var playAnimHook = null;
    var discovered = {};  // { dataPtrStr: true }

    function lockWeaponData(dataPtr) {
        var arrPtr = dataPtr.add(0xC0).readPointer();
        if (!arrPtr || arrPtr.isNull()) return;

        var arrLen = arrPtr.add(0x0C).readU32();
        if (arrLen < 1 || arrLen > 20) return;

        var count = 0;
        for (var i = 0; i < arrLen; i++) {
            var addr = arrPtr.add(0x10 + i * 0x1C + 0x4);
            try {
                var orig = addr.readFloat();
                if (orig > 0.5 && orig < 500) {
                    addr.writeFloat(orig * KNIFE_RANGE_MULTIPLIER);
                    count++;
                }
            } catch(e) {}
        }

        sendLog('info', '近战', '已锁定 ' + count + '/' + arrLen + ' 个攻击类型 @ ' + dataPtr + ' (' + KNIFE_RANGE_MULTIPLIER + 'x)');
    }

    function enable() {
        if (enabled) return;
        var gm = getGameAssembly();
        if (!gm) { sendLog('error', '近战', 'GameAssembly 未找到'); return; }
        var base = gm.base;

        discovered = {};

        playAnimHook = Interceptor.attach(base.add(0xB642B0), {
            onEnter: function(args) {
                var wpnKnife = args[0];
                if (!wpnKnife || wpnKnife.isNull()) return;

                try {
                    var dataPtr = wpnKnife.add(0x68).readPointer();
                    if (!dataPtr || dataPtr.isNull()) return;

                    var key = dataPtr.toString();
                    if (discovered[key]) return;
                    discovered[key] = true;

                    lockWeaponData(dataPtr);
                } catch(e) {}
            }
        });

        // 切房间清理（新房间新武器）
        var cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
        for (var i = 0; i < cleanupAddrs.length; i++) {
            try {
                Interceptor.attach(base.add(cleanupAddrs[i]), {
                    onEnter: function() {
                        discovered = {};
                        sendLog('info', '近战', '房间切换，等待新武器...');
                    }
                });
            } catch(e) {}
        }

        enabled = true;
        sendLog('info', '近战', 'v8 已启用 (' + KNIFE_RANGE_MULTIPLIER + 'x, 无timer)');
    }

    function disable() {
        if (!enabled) return;
        if (playAnimHook) { playAnimHook.detach(); playAnimHook = null; }
        discovered = {};
        enabled = false;
        sendLog('info', '近战', 'v8 已禁用');
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info', '近战', '倍数 → ' + v + 'x（重启游戏后生效）');
    };

    sendLog('info', '近战', 'v8 已加载，自动启用...');
    enable();

})();
