// no_recoil_v14.js - 无后座力 v14 (replace OnGunShot + zero 4 fields)
// 从 game_modifier.py 提取的独立版本
(function() {
    'use strict';

    var MAX_LOGS_PER_MODULE = 10;
    var moduleLogCounts = {};

    function sendLog(level, module, message) {
        if (!moduleLogCounts[module]) moduleLogCounts[module] = 0;
        if (moduleLogCounts[module] >= MAX_LOGS_PER_MODULE) return;
        if (module !== '系统' && moduleLogCounts[module] === MAX_LOGS_PER_MODULE - 1) {
            moduleLogCounts[module]++;
            send({ type: 'log', level: 'info', module: module, message: message + ' (后续日志已静默)' });
            return;
        }
        moduleLogCounts[module]++;
        send({ type: 'log', level: level, module: module, message: message });
    }

    function getGameAssembly() {
        try {
            var mod = Process.findModuleByName('GameAssembly.dll');
            if (!mod) {
                sendLog('error', '系统', '未找到 GameAssembly.dll');
                return null;
            }
            sendLog('info', '系统', 'GameAssembly.dll: base=' + mod.base + ' size=' + mod.size);
            return mod;
        } catch(e) { sendLog('error', '系统', '获取模块失败: ' + e.message); return null; }
    }

    var replacedAddr = null;
    var callbackFunc = null;
    var enabled = false;
    var suppressCount = 0;

    function enable() {
        if (enabled) return;
        var mod = getGameAssembly();
        if (!mod) { sendLog('error', '无后座力', '无 GameAssembly.dll'); return; }

        var base = mod.base;
        replacedAddr = base.add(0xB19980);
        sendLog('info', '无后座力', 'Recoil$$OnGunShot @ ' + replacedAddr);

        suppressCount = 0;

        callbackFunc = new NativeCallback(function(recoilThis, methodInfo) {
            suppressCount++;
            try {
                recoilThis.add(0x68).writeFloat(0.0);
                recoilThis.add(0x6C).writeFloat(0.0);
                recoilThis.add(0x70).writeFloat(0.0);
                recoilThis.add(0x74).writeFloat(0.0);
            } catch (e) {}

            if (suppressCount <= 3) {
                sendLog('info', '无后座力', '[Suppress #' + suppressCount + '] ' + recoilThis);
            } else if (suppressCount === 4) {
                sendLog('info', '无后座力', '...suppressing silently');
            }
        }, 'void', ['pointer', 'pointer']);

        try {
            Interceptor.replace(replacedAddr, callbackFunc);
            sendLog('success', '无后座力', '已替换 Recoil.OnGunShot');
        } catch(e) {
            sendLog('error', '无后座力', '替换失败: ' + e.message);
            return;
        }

        enabled = true;
        sendLog('success', '无后座力', 'v14 已启用 (replace OnGunShot + zero 4 fields)');
    }

    enable();
    sendLog('info', '系统', '无后座力 v14 已加载，自动启用中...');
})();
