// ============================================================
// 近战距离修改器 v11 — Interceptor.replace PlayerWeapons.get_KnifeRange
//
// 策略: 参考 speed_knife_v16 的成熟模式
//       替换 PlayerWeapons.get_KnifeRange (RVA 0xB170E0)
//       通过 Player.get_isMyPlayer(owner) 判定本地玩家
//
//       ★ 只影响玩家，不影响 Bot（每个 PlayerWeapons 有独立 owner）
//       ★ 全模式生效（get_KnifeRange 是通用底层 getter）
//       ★ 不写只读内存，不改 ScriptableObject，安全稳定
//
// 原理: PlayerWeapons 是每个玩家独立的实例
//       PlayerWeapons + 0x8 = owner (Player*)
//       get_KnifeRange 返回该玩家的近战攻击距离
//       对本地玩家返回 原始值 × 倍数，其他玩家返回原始值
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

    var originalGetKnifeRange = null;
    var isMyPlayerFn = null;
    var logCount = 0;
    var enabled = false;

    function enable() {
        if (enabled) return;

        var mod = Process.findModuleByName('GameAssembly.dll');
        if (!mod) {
            sendLog('error', '近战', 'GameAssembly.dll 未找到');
            return;
        }
        var base = mod.base;

        // Player.get_isMyPlayer (RVA 0xB55FD0)
        // 签名: bool isMyPlayer(Player_o* player)
        var isMyPlayerAddr = base.add(0xB55FD0);
        isMyPlayerFn = new NativeFunction(isMyPlayerAddr, 'bool', ['pointer']);
        sendLog('info', '近战', 'isMyPlayer @ ' + isMyPlayerAddr);

        // PlayerWeapons.get_KnifeRange (RVA 0xB170E0)
        // 签名: float get_KnifeRange(PlayerWeapons_o* this, MethodInfo* method)
        var getKnifeRangeAddr = base.add(0xB170E0);
        sendLog('info', '近战', 'get_KnifeRange @ ' + getKnifeRangeAddr);

        // 保存原始函数引用（在 replace 之前创建 NativeFunction）
        originalGetKnifeRange = new NativeFunction(getKnifeRangeAddr, 'float', ['pointer', 'pointer']);

        logCount = 0;

        Interceptor.replace(getKnifeRangeAddr, new NativeCallback(function(self, methodInfo) {
            try {
                // self = PlayerWeapons*
                // PlayerWeapons + 0x8 = owner (Player*)
                var owner = self.add(0x8).readPointer();

                // 调用原始函数获取基础值
                var baseRange = originalGetKnifeRange(self, methodInfo);

                if (!owner || owner.isNull()) {
                    return baseRange;
                }

                // 判断是否是本地玩家
                if (isMyPlayerFn(owner)) {
                    var newRange = baseRange * KNIFE_RANGE_MULTIPLIER;

                    logCount++;
                    sendLog('info', '近战',
                        '[玩家] 原始距离=' + baseRange.toFixed(2) +
                        ' → 修改后=' + newRange.toFixed(2) +
                        ' (' + KNIFE_RANGE_MULTIPLIER + 'x) [调用#' + logCount + ']');

                    return newRange;
                }

                // 非本地玩家，打印原始值
                logCount++;
                if (logCount <= 3) {
                    sendLog('info', '近战',
                        '[Bot/其他] 原始距离=' + baseRange.toFixed(2) + ' (未修改)');
                }
                return baseRange;
            } catch(e) {
                logCount++;
                if (logCount <= 2) {
                    sendLog('error', '近战', '异常: ' + e.message);
                }
                // 出错时尝试返回原始值
                try {
                    return originalGetKnifeRange(self, methodInfo);
                } catch(e2) {
                    return 1.0;
                }
            }
        }, 'float', ['pointer', 'pointer']));

        enabled = true;
        sendLog('info', '近战', 'v11 已启用 (' + KNIFE_RANGE_MULTIPLIER + 'x, 只影响玩家, 全模式)');
    }

    function disable() {
        if (!enabled) return;
        try {
            var mod = Process.findModuleByName('GameAssembly.dll');
            if (mod) {
                Interceptor.revert(mod.base.add(0xB170E0));
            }
        } catch(e) {
            sendLog('warn', '近战', '恢复失败: ' + e.message);
        }
        originalGetKnifeRange = null;
        isMyPlayerFn = null;
        enabled = false;
        sendLog('info', '近战', 'v11 已禁用');
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info', '近战', '倍数 → ' + v + 'x');
    };

    sendLog('info', '近战', 'v11 已加载，自动启用...');
    enable();

})();
