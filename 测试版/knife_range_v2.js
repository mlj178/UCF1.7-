// ============================================================
// 近战距离修改器 v2（诊断版 — 只读不写，验证指针链）
// 原理: Hook WPN_Knife$$KnifeAttackEvent (RVA 0xB63DD0)
//       只读取并打印完整内存链，不写入任何值
//       用于验证指针路径是否正确、内存是否可写
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

    // 检查地址所在页面的内存保护属性
    function getMemoryProtection(addr) {
        try {
            var range = Process.getRangeByAddress(ptr(addr));
            if (range) {
                return 'base=' + range.base + ' size=' + ptr(range.size) + ' prot=' + range.protection;
            }
        } catch(e) {}
        return 'unknown';
    }

    var enabled = false;
    var hookListener = null;
    var attackCount = 0;
    var verbose = true;

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
        sendLog('info', '近战距离', '=== 诊断模式: 只读不写 ===');

        hookListener = Interceptor.attach(hookAddr, {
            onEnter: function(args) {
                attackCount++;
                var self = args[0];
                var rawArg1 = args[1];
                var index = rawArg1.toInt32();

                sendLog('info', '近战距离', '');
                sendLog('info', '近战距离', '========== 攻击 #' + attackCount + ' ==========');
                sendLog('info', '近战距离', 'WPN_Knife 指针: ' + self);
                sendLog('info', '近战距离', '攻击索引(原始): ' + rawArg1 + ' → int32=' + index);

                try {
                    // --- 第1步: 读取 WPN_Knife + 0x68 → WeaponData* ---
                    var dataPtr = self.add(0x68).readPointer();
                    sendLog('info', '近战距离', 'self+0x68 (WeaponData*): ' + dataPtr);
                    sendLog('info', '近战距离', '  页面属性: ' + getMemoryProtection(dataPtr));

                    if (!dataPtr || dataPtr.isNull()) {
                        sendLog('error', '近战距离', 'WeaponData 指针为空!');
                        return;
                    }

                    // --- 第2步: 尝试两种方式定位 KnifeAttackData ---
                    // 方式A: 直接偏移 (dataPtr + 0xC0 + index*0x10)
                    var directAddr = dataPtr.add(0xC0 + index * 0x10);
                    sendLog('info', '近战距离', '方式A: dataPtr+0xC0+index*0x10 = ' + directAddr);

                    var damageA = 0, rangeA = 0, angleA = 0, hitStunA = 0;
                    try {
                        damageA = directAddr.readFloat();
                        rangeA = directAddr.add(0x4).readFloat();
                        angleA = directAddr.add(0x8).readFloat();
                        hitStunA = directAddr.add(0xC).readU8();
                        sendLog('info', '近战距离', '  [直接偏移] damage=' + damageA.toFixed(1) +
                            ' range=' + rangeA.toFixed(2) +
                            ' angle=' + angleA.toFixed(2) +
                            ' hitStun=' + hitStunA +
                            ' prot=' + getMemoryProtection(directAddr));
                    } catch (e) {
                        sendLog('error', '近战距离', '  方式A读取失败: ' + e);
                    }

                    // 方式B: dataPtr+0xC0 先解引用为数组指针
                    try {
                        var arrayPtr = dataPtr.add(0xC0).readPointer();
                        sendLog('info', '近战距离', '方式B: dataPtr+0xC0 解引用 → ' + arrayPtr);
                        if (arrayPtr && !arrayPtr.isNull()) {
                            sendLog('info', '近战距离', '  页面属性: ' + getMemoryProtection(arrayPtr));

                            // 读取数组头部信息
                            sendLog('info', '近战距离', '  数组头部:');
                            for (var h = 0; h < 0x30; h += 4) {
                                try {
                                    var v32 = arrayPtr.add(h).readU32();
                                    var vf = arrayPtr.add(h).readFloat();
                                    sendLog('info', '近战距离', '    +0x' + h.toString(16) +
                                        ' u32=' + v32 + ' float=' + vf.toFixed(4));
                                } catch(e) {}
                            }

                            // 尝试从不同偏移读取元素
                            var headerOffsets = [0x10, 0x18, 0x20];
                            for (var hi = 0; hi < headerOffsets.length; hi++) {
                                var elemBase = arrayPtr.add(headerOffsets[hi]);
                                var elemAddr = elemBase.add(index * 0x10);
                                try {
                                    var d = elemAddr.readFloat();
                                    var r = elemAddr.add(0x4).readFloat();
                                    var a = elemAddr.add(0x8).readFloat();
                                    if (d > 0 && d < 10000 && r > 0 && r < 1000) {
                                        sendLog('info', '近战距离', '  [头部+0x' + headerOffsets[hi].toString(16) + '] 元素' + index +
                                            ' damage=' + d.toFixed(1) +
                                            ' range=' + r.toFixed(2) +
                                            ' angle=' + a.toFixed(2) +
                                            ' prot=' + getMemoryProtection(elemAddr));
                                    }
                                } catch(e) {}
                            }
                        }
                    } catch (e) {
                        sendLog('warn', '近战距离', '  方式B失败: ' + e);
                    }

                } catch (e) {
                    sendLog('error', '近战距离', '整体异常: ' + e + '\n' + e.stack);
                }

                if (attackCount >= 20) {
                    sendLog('info', '近战距离', '已记录20次攻击，关闭详细日志');
                    verbose = false;
                }
            }
        });

        enabled = true;
        sendLog('info', '近战距离', 'v2 诊断模式已启用');
        sendLog('info', '近战距离', '按近战攻击键查看内存链...');
    }

    function disable() {
        if (!enabled) return;
        if (hookListener) {
            hookListener.detach();
            hookListener = null;
        }
        enabled = false;
        sendLog('info', '近战距离', 'v2 已禁用 (共攻击 ' + attackCount + ' 次)');
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;

    sendLog('info', '近战距离', 'v2 诊断版已加载，自动启用中...');
    enable();

})();
