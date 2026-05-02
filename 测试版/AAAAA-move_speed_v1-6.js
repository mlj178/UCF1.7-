// ============================================================
// 移动速度修改器 v1（已验证可用，从 move_speed.js 拆分）
// 原理: Hook PropertyModifier.Get (RVA 0xB17590)
//       拦截 MoveSpeedRatio Modifier 的查询，返回倍数后的值
// 内存路径: player + 0x8C → Modifier_MoveSpeedRatio
// ============================================================

(function() {
    'use strict';

    var MOVE_SPEED_MULTIPLIER = 6.0;
    var gameAssembly = null;
    var isMyPlayerFn = null;

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
    var hookAddr = null;
    var originalFn = null;
    var logCount = 0;

    function enable() {
        if (enabled) return;
        var gm = getGameAssembly(); if (!gm) {
            sendLog('error', '移动速度', '未找到 GameAssembly');
            return;
        }
        var base = gm.base;
        hookAddr = base.add(0xB17590);
        isMyPlayerFn = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
        originalFn = new NativeFunction(hookAddr, 'float', ['pointer', 'pointer']);
        logCount = 0;

        Interceptor.replace(hookAddr, new NativeCallback(function(self, player) {
            var result = originalFn(self, player);
            if (player && !player.isNull() && isMyPlayerFn(player)) {
                var moveMod = player.add(0x8C).readPointer();
                if (moveMod && !moveMod.isNull() && self.equals(moveMod)) {
                    logCount++;
                    if (logCount <= 10)
                        sendLog('info', '移动速度', '内存真实原值=' + result.toFixed(6) + ' 修改后=' + MOVE_SPEED_MULTIPLIER.toFixed(1) + 'x');
                    return MOVE_SPEED_MULTIPLIER;
                }
            }
            return result;
        }, 'float', ['pointer', 'pointer']));

        enabled = true;
        sendLog('info', '移动速度', 'v1 已启用 (' + MOVE_SPEED_MULTIPLIER + 'x) @ ' + hookAddr);
    }

    function disable() {
        if (!enabled || !hookAddr) return;
        Interceptor.revert(hookAddr);
        enabled = false;
        sendLog('info', '移动速度', '已禁用');
    }

    globalThis.enableMoveSpeed = enable;
    globalThis.disableMoveSpeed = disable;
    globalThis.setMoveSpeedMultiplier = function(v) {
        MOVE_SPEED_MULTIPLIER = v;
        sendLog('info', '移动速度', '倍数 → ' + v + 'x');
    };

    sendLog('info', '移动速度', 'v1 脚本已加载，自动启用中...');
    enable();

})();
