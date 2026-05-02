// ============================================================
// 近战距离修改器 v17 — 全面诊断版
// 目的: 找出 v16 无效果的原因
// 打印: self, owner, isMyPlayer结果, retbuf内容
// ============================================================

(function() {
    'use strict';

    var KNIFE_RANGE_MULTIPLIER = 50.0;

    function sendLog(level, module, msg) {
        var logMsg = '[' + module + '] ' + msg;
        if (level === 'error') console.error(logMsg);
        else if (level === 'warn') console.warn(msg);
        else console.log(logMsg);
    }

    var mod = Process.findModuleByName('GameAssembly.dll');
    if (!mod) { sendLog('error', '近战', 'GameAssembly.dll 未找到'); return; }
    var base = mod.base;

    var isMyPlayerFn = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
    var getKnifeAttackDataAddr = base.add(0xB63EC0);
    var originalFn = new NativeFunction(getKnifeAttackDataAddr, 'pointer', ['pointer', 'pointer', 'int', 'pointer']);

    sendLog('info', '近战', 'isMyPlayer @ ' + base.add(0xB55FD0));
    sendLog('info', '近战', 'GetKnifeAttackData @ ' + getKnifeAttackDataAddr);

    var logCount = 0;
    var maxDiag = 20;

    Interceptor.replace(getKnifeAttackDataAddr, new NativeCallback(function(retbuf, self, attackIdx, methodInfo) {
        var result = originalFn(retbuf, self, attackIdx, methodInfo);

        try {
            logCount++;
            if (logCount <= maxDiag) {
                sendLog('info', '近战',
                    '=== 调用#' + logCount + ' ===');
                sendLog('info', '近战',
                    'self=' + self +
                    ' attackIdx=' + attackIdx +
                    ' retbuf=' + retbuf);

                // 尝试多个可能的 owner 偏移
                var offsets = [0x8, 0x10, 0x14, 0x18, 0x28, 0x2C, 0x30, 0x48, 0x50, 0x68, 0x6C, 0x70, 0x80, 0x88, 0x90, 0x98, 0xA0, 0xA8];
                for (var i = 0; i < offsets.length; i++) {
                    try {
                        var off = offsets[i];
                        var ptr = self.add(off).readPointer();
                        if (ptr && !ptr.isNull()) {
                            var range = Process.findRangeByAddress(ptr);
                            if (range) {
                                var isMy = false;
                                try {
                                    isMy = isMyPlayerFn(ptr);
                                } catch(e) {
                                    isMy = false;
                                }
                                sendLog('info', '近战',
                                    '  +' + off.toString(16) + ' → ' + ptr +
                                    (isMy ? ' ★ isMyPlayer=true' : ''));
                            }
                        }
                    } catch(e) {}
                }

                // 打印 retbuf 内容
                try {
                    var dmg = retbuf.add(0x0).readFloat();
                    var rng = retbuf.add(0x4).readFloat();
                    var ang = retbuf.add(0x8).readFloat();
                    sendLog('info', '近战',
                        '  retbuf: damage=' + dmg.toFixed(2) +
                        ' range=' + rng.toFixed(2) +
                        ' angle=' + ang.toFixed(2));
                } catch(e) {
                    sendLog('info', '近战', '  retbuf 读取失败: ' + e.message);
                }

                // 尝试修改
                var rangeAddr = retbuf.add(0x4);
                var orig = rangeAddr.readFloat();
                if (orig > 0.3 && orig < 500) {
                    rangeAddr.writeFloat(orig * KNIFE_RANGE_MULTIPLIER);
                    sendLog('info', '近战',
                        '  修改 range: ' + orig.toFixed(2) + ' → ' + (orig * KNIFE_RANGE_MULTIPLIER).toFixed(2));
                }
            }
        } catch(e) {
            if (logCount < 3) {
                sendLog('error', '近战', '异常: ' + e.message);
            }
        }

        return result;
    }, 'pointer', ['pointer', 'pointer', 'int', 'pointer']));

    sendLog('info', '近战', 'v17 诊断版已启用，挥刀查看日志...');

})();
