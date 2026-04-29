// ============================================================
// 近战距离修改器 v3 — Plan1 风格（内存锁定）
// 参考: 无限子弹 plan1_memory_lock.js 的成功模式
//
// 策略映射:
//   无限子弹  → Hook 开火函数 → 发现 WPN_Gun → 锁定 AmmoData
//   近战距离  → Hook PlayKnifeAttackAnim → 发现 WPN_Knife → 锁定 KnifeAttackData.range
//
// Hook 点: PlayKnifeAttackAnim (RVA 0xB642B0) ← speed_knife_v5 已验证稳定
//   (不是 v1/v2 的 KnifeAttackEvent 0xB63DD0, 那个会闪退!)
//
// 内存路径:
//   args[0] (WPN_Knife*.this) + 0x68 → WeaponData_Knife*
//   WeaponData_Knife + 0xC0 → KnifeAttackData[] (Il2CppArray)
//   Il2CppArray + 0x20 + type*0x10 → KnifeAttackData[type]
//   KnifeAttackData + 0x4 → float range ← 锁定目标
//
// 生命周期:
//   - 每次 PlayKnifeAttackAnim 被调用时，锁定对应攻击类型的 range
//   - onLeave 恢复原始值（只影响攻击瞬间，不永久修改 ScriptableObject）
//   - 切房间时清空缓存（防闪退）
// ============================================================

(function() {
    'use strict';

    var KNIFE_RANGE_MULTIPLIER = 5.0;
    var gameAssembly = null;
    var isMyWeaponFn = null;

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
    var playAnimHook = null;
    var restoreList = [];    // [{addr, originalValue}] 用于 onLeave 恢复
    var attackCount = 0;
    var maxVerbose = 10;

    // 缓存已发现的武器数据和 range 地址
    var knownWeaponData = {};  // { dataPtrStr: { rangeAddrs: { typeIndex: addr } } }

    function enable() {
        if (enabled) return;
        var gm = getGameAssembly();
        if (!gm) { sendLog('error', '近战距离', '未找到 GameAssembly'); return; }
        var base = gm.base;

        isMyWeaponFn = new NativeFunction(base.add(0xB6E1D0), 'bool', ['pointer', 'pointer']);

        // ★ 使用 PlayKnifeAttackAnim 而不是 KnifeAttackEvent
        //   这个是快刀 speed_knife_v5 已验证稳定的 hook 点
        var hookAddr = base.add(0xB642B0);
        attackCount = 0;

        sendLog('info', '近战距离', 'v3 Plan1 风格 Hook PlayKnifeAttackAnim @ ' + hookAddr);

        playAnimHook = Interceptor.attach(hookAddr, {
            onEnter: function(args) {
                attackCount++;
                var self = args[0];        // WPN_Knife*
                var attackType = args[1].toInt32(); // 1=Combo1, 2=Combo2, 3=Bigshot
                restoreList = [];

                if (!self || self.isNull()) return;
                if (!isMyWeaponFn(self, ptr(0))) return;  // 过滤 Bot

                if (attackCount <= maxVerbose) {
                    sendLog('info', '近战距离', '========== 攻击 #' + attackCount + ' type=' + attackType + ' self=' + self + ' ==========');
                }

                try {
                    // 步骤1: WPN_Knife + 0x68 → WeaponData_Knife*
                    var dataPtr = self.add(0x68).readPointer();
                    if (!dataPtr || dataPtr.isNull()) {
                        if (attackCount <= 3) sendLog('warn', '近战距离', 'WeaponData 为空!');
                        return;
                    }
                    if (attackCount <= maxVerbose)
                        sendLog('info', '近战距离', 'Step1: WeaponData=' + dataPtr);

                    // 步骤2: WeaponData_Knife + 0xC0 → knifeAttacks (Il2CppArray)
                    var arrPtr = dataPtr.add(0xC0).readPointer();
                    if (!arrPtr || arrPtr.isNull()) {
                        if (attackCount <= 3) sendLog('warn', '近战距离', 'knifeAttacks 数组为空!');
                        return;
                    }
                    if (attackCount <= maxVerbose)
                        sendLog('info', '近战距离', 'Step2: knifeAttacks[]=' + arrPtr);

                    // 步骤3: 读取 Il2CppArray 头部找元素起始偏移
                    // Il2CppArray: +0x00 klass, +0x08 monitor, +0x10 bounds, +0x18 max_length, +0x20 elements
                    var arrLen = 0;
                    var elemStart = 0x20;

                    // 先读 +0x18 看是不是长度（max_length 在 64 位）
                    try {
                        var v18 = arrPtr.add(0x18).readU64();
                        var v1C = arrPtr.add(0x1C).readU32();
                        if (v18.toNumber() > 0 && v18.toNumber() < 100) {
                            arrLen = v18.toNumber();
                        } else {
                            // 尝试其他位置
                            var v10 = arrPtr.add(0x10).readU32();
                            if (v10 > 0 && v10 < 100) arrLen = v10;
                            else arrLen = 5; // 假设最多5种攻击类型
                        }
                    } catch (e) { arrLen = 5; }

                    if (attackCount <= maxVerbose)
                        sendLog('info', '近战距离', 'Step3: arrayLen=' + arrLen + ' elemStart推算=0x20');

                    // 步骤4: 扫描全部 KnifeAttackData 元素
                    // KnifeAttackData: +0x0 damage(float), +0x4 range(float), +0x8 angle(float), +0xC hitStun(bool)
                    var foundValid = false;
                    for (var ti = 0; ti < arrLen; ti++) {
                        var elemAddr = arrPtr.add(elemStart + ti * 0x10);

                        try {
                            var dmg = elemAddr.add(0x0).readFloat();
                            var rng = elemAddr.add(0x4).readFloat();
                            var ang = elemAddr.add(0x8).readFloat();

                            // 过滤合法值
                            if (dmg > 0 && dmg < 10000 && rng > 0.5 && rng < 100 && ang > 0 && ang < 360) {
                                foundValid = true;
                                var newRange = rng * KNIFE_RANGE_MULTIPLIER;

                                if (attackCount <= maxVerbose) {
                                    sendLog('info', '近战距离',
                                        '  [' + ti + '] damage=' + dmg.toFixed(1) +
                                        ' range=' + rng.toFixed(2) + '→' + newRange.toFixed(2) +
                                        ' angle=' + ang.toFixed(1) +
                                        ' @ ' + elemAddr);
                                }

                                // 尝试写入
                                var rangeAddr = elemAddr.add(0x4);
                                try {
                                    rangeAddr.writeFloat(newRange);
                                    restoreList.push({addr: rangeAddr, original: rng});
                                    if (ti + 1 === attackType && attackCount <= maxVerbose) {
                                        sendLog('info', '近战距离',
                                            '  ★ 当前攻击 type=' + attackType + ' range已锁定 ' + rng.toFixed(2) + '→' + newRange.toFixed(2));
                                    }
                                } catch (e) {
                                    // 可能只读内存，用 Memory.protect
                                    if (attackCount <= 3)
                                        sendLog('warn', '近战距离', '  写入失败(可能只读): ' + e.message);
                                    // 尝试 Memory.protect
                                    try {
                                        var pageAddr = rangeAddr.and(ptr(0xFFFFFFFFFFFFF000));
                                        Memory.protect(pageAddr, 4096, 'rwx');
                                        rangeAddr.writeFloat(newRange);
                                        restoreList.push({addr: rangeAddr, original: rng});
                                        Memory.protect(pageAddr, 4096, 'rw-'); // 恢复
                                        if (attackCount <= 3)
                                            sendLog('info', '近战距离', '  Memory.protect 解锁后写入成功!');
                                    } catch (e2) {
                                        if (attackCount <= 3)
                                            sendLog('error', '近战距离', '  无法写入: ' + e2.message);
                                    }
                                }
                            }
                        } catch (e) {
                            // 读取越界，跳过
                        }
                    }

                    if (!foundValid && attackCount <= 3) {
                        sendLog('warn', '近战距离', '未找到有效 KnifeAttackData, 尝试偏移扫描...');
                        // 后备：扫描 dataPtr 内所有 float 找 range 候选
                        for (var off = 0; off < 0x160; off += 4) {
                            try {
                                var f = dataPtr.add(off).readFloat();
                                if (f > 0.5 && f < 20) {
                                    sendLog('info', '近战距离', '  dataPtr+0x' + off.toString(16) + ' float=' + f.toFixed(4));
                                }
                            } catch(e) {}
                        }
                    }

                } catch (e) {
                    if (attackCount <= 3)
                        sendLog('error', '近战距离', '异常: ' + e + '\n' + e.stack);
                }

                if (attackCount >= maxVerbose + 1 && attackCount % 20 === 0) {
                    sendLog('info', '近战距离', '已处理 ' + attackCount + ' 次攻击 (稳定运行中)');
                }
            },
            onLeave: function(retval) {
                // 恢复所有被修改的值
                for (var i = 0; i < restoreList.length; i++) {
                    try {
                        restoreList[i].addr.writeFloat(restoreList[i].original);
                    } catch(e) {}
                }
                restoreList = [];
            }
        });

        // 切房间清理钩子（防闪退）
        var cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
        for (var i = 0; i < cleanupAddrs.length; i++) {
            try {
                Interceptor.attach(base.add(cleanupAddrs[i]), {
                    onEnter: function() {
                        knownWeaponData = {};
                        sendLog('info', '近战距离', '房间切换，缓存已清理');
                    }
                });
            } catch(e) {}
        }

        enabled = true;
        sendLog('info', '近战距离', 'v3 Plan1 风格已启用 (' + KNIFE_RANGE_MULTIPLIER + 'x)');
        sendLog('info', '近战距离', '进入游戏按近战攻击键测试...');
    }

    function disable() {
        if (!enabled) return;
        if (playAnimHook) { playAnimHook.detach(); playAnimHook = null; }
        enabled = false;
        sendLog('info', '近战距离', 'v3 已禁用 (共 ' + attackCount + ' 次攻击)');
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info', '近战距离', '倍数 → ' + v + 'x');
    };

    sendLog('info', '近战距离', 'v3 Plan1 风格已加载，自动启用中...');
    enable();

})();
