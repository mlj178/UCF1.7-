// ============================================================
// 近战距离修改器 v16 — Interceptor.replace + isMyPlayer
//
// 策略: 完全参考 speed_knife_v16 的成功模式
//       Interceptor.replace GetKnifeAttackData
//       NativeCallback 在游戏线程运行 → isMyPlayer 安全
//       从 WPN_Knife 找 owner → isMyPlayer 判断
//
// 玩家识别路径 (参考 v16):
//   WPN_Knife → 继承链: WPN_Knife → Weapon → CFAnimator → Model
//   Model + 0x10 = owner (Player*)
//   isMyPlayer(owner) → true = 本地玩家
//
// 距离修改:
//   调用原始函数获取 KnifeAttackData
//   retbuf + 0x4 = range → 修改
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

    // Player.get_isMyPlayer (RVA 0xB55FD0)
    var isMyPlayerFn = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);

    // 原始 GetKnifeAttackData 函数
    // IL2CPP 32-bit struct return: 隐藏 retbuf 作为第一个参数
    // KnifeAttackData* GetKnifeAttackData(KnifeAttackData* retbuf, WPN_Knife* self, int attackIdx, MethodInfo* method)
    var getKnifeAttackDataAddr = base.add(0xB63EC0);
    var originalFn = new NativeFunction(getKnifeAttackDataAddr, 'pointer', ['pointer', 'pointer', 'int', 'pointer']);

    sendLog('info', '近战', 'isMyPlayer @ ' + base.add(0xB55FD0));
    sendLog('info', '近战', 'GetKnifeAttackData @ ' + getKnifeAttackDataAddr);

    var logCount = 0;

    // 替换 GetKnifeAttackData
    Interceptor.replace(getKnifeAttackDataAddr, new NativeCallback(function(retbuf, self, attackIdx, methodInfo) {
        // 先调用原始函数
        var result = originalFn(retbuf, self, attackIdx, methodInfo);

        try {
            // WPN_Knife 继承链: WPN_Knife → Weapon → CFAnimator → Model
            // Model + 0x10 = owner (Player*)
            var owner = self.add(0x10).readPointer();
            if (!owner || owner.isNull()) return result;

            if (isMyPlayerFn(owner)) {
                var rangeAddr = retbuf.add(0x4);
                var orig = rangeAddr.readFloat();
                if (orig > 0.3 && orig < 500) {
                    rangeAddr.writeFloat(orig * KNIFE_RANGE_MULTIPLIER);
                    logCount++;
                    if (logCount <= 10) {
                        sendLog('info', '近战',
                            '[玩家#' + logCount + '] idx=' + attackIdx +
                            ' range ' + orig.toFixed(2) +
                            ' → ' + (orig * KNIFE_RANGE_MULTIPLIER).toFixed(2));
                    }
                }
            }
        } catch(e) {
            if (logCount < 2) {
                sendLog('error', '近战', '异常: ' + e.message);
            }
        }

        return result;
    }, 'pointer', ['pointer', 'pointer', 'int', 'pointer']));

    sendLog('info', '近战', 'v16 已启用 (' + KNIFE_RANGE_MULTIPLIER + 'x, isMyPlayer精确识别, replace模式)');
    sendLog('info', '近战', '进入任意模式挥刀测试...');

})();
