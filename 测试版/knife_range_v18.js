// ============================================================
// 近战距离修改器 v18 — Interceptor.attach + 全面诊断
// 回到 v12 的 attach 模式（已验证有效），加诊断日志找 owner 偏移
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

    var hookList = [];
    var logCount = 0;
    var maxDiag = 15;
    var playerWeapons = {};
    var playerWeaponCount = 0;

    // ============================================================
    // Hook 1: WPN_Knife.GetKnifeAttackData (RVA 0xB63EC0)
    // ============================================================
    try {
        hookList.push(Interceptor.attach(base.add(0xB63EC0), {
            onEnter: function(args) {
                this.wpnSelf = args[1];
                this.attackIdx = args[2].toInt32();
            },
            onLeave: function(retval) {
                try {
                    logCount++;
                    if (logCount <= maxDiag) {
                        sendLog('info', '近战',
                            '=== 调用#' + logCount + ' ===');
                        sendLog('info', '近战',
                            'self=' + this.wpnSelf +
                            ' idx=' + this.attackIdx +
                            ' retval=' + retval);

                        // 扫描 owner 偏移
                        var offsets = [0x8, 0x10, 0x14, 0x18, 0x28, 0x2C, 0x30, 0x48, 0x50, 0x68, 0x6C, 0x70, 0x80, 0x88, 0x90, 0x98, 0xA0, 0xA8];
                        for (var i = 0; i < offsets.length; i++) {
                            try {
                                var off = offsets[i];
                                var ptr = this.wpnSelf.add(off).readPointer();
                                if (ptr && !ptr.isNull()) {
                                    var range = Process.findRangeByAddress(ptr);
                                    if (range) {
                                        var isMy = false;
                                        try { isMy = isMyPlayerFn(ptr); } catch(e) {}
                                        sendLog('info', '近战',
                                            '  +' + off.toString(16) + ' → ' + ptr +
                                            (isMy ? ' ★ isMyPlayer=true' : ''));
                                    }
                                }
                            } catch(e) {}
                        }

                        // 打印 retval 内容
                        try {
                            var dmg = retval.add(0x0).readFloat();
                            var rng = retval.add(0x4).readFloat();
                            var ang = retval.add(0x8).readFloat();
                            sendLog('info', '近战',
                                '  retval: damage=' + dmg.toFixed(2) +
                                ' range=' + rng.toFixed(2) +
                                ' angle=' + ang.toFixed(2));
                        } catch(e) {
                            sendLog('info', '近战', '  retval 读取失败: ' + e.message);
                        }
                    }

                    // 启发式玩家识别
                    var key = this.wpnSelf.toString();
                    if (playerWeapons[key]) {
                        modifyRange(retval, this.attackIdx);
                        return;
                    }
                    if (playerWeaponCount < 2) {
                        playerWeapons[key] = true;
                        playerWeaponCount++;
                        sendLog('info', '近战',
                            '发现玩家武器 #' + playerWeaponCount + ' @ ' + this.wpnSelf);
                        modifyRange(retval, this.attackIdx);
                        return;
                    }
                } catch(e) {
                    if (logCount < 2) {
                        sendLog('error', '近战', 'onLeave异常: ' + e.message);
                    }
                }
            }
        }));
        sendLog('info', '近战', 'Hook GetKnifeAttackData @ ' + base.add(0xB63EC0));
    } catch(e) { sendLog('error', '近战', 'Hook 1 失败: ' + e.message); }

    // ============================================================
    // Hook 2: Weapon.GetKnifeAttackData 基类兜底 (RVA 0xB79008)
    // ============================================================
    try {
        hookList.push(Interceptor.attach(base.add(0xB79008), {
            onEnter: function(args) {
                this.wpnSelf = args[1];
            },
            onLeave: function(retval) {
                try {
                    var key = this.wpnSelf.toString();
                    if (playerWeapons[key]) {
                        modifyRange(retval, -1);
                    }
                } catch(e) {}
            }
        }));
        sendLog('info', '近战', 'Hook Weapon.GetKnifeAttackData @ ' + base.add(0xB79008));
    } catch(e) {}

    // 房间切换重置
    var cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
    for (var i = 0; i < cleanupAddrs.length; i++) {
        try {
            Interceptor.attach(base.add(cleanupAddrs[i]), {
                onEnter: function() {
                    playerWeapons = {};
                    playerWeaponCount = 0;
                    logCount = 0;
                    sendLog('info', '近战', '房间切换，重置缓存');
                }
            });
        } catch(e) {}
    }

    function modifyRange(retval, attackIdx) {
        try {
            var rangeAddr = retval.add(0x4);
            var orig = rangeAddr.readFloat();
            if (!(orig > 0.3 && orig < 500)) return;
            rangeAddr.writeFloat(orig * KNIFE_RANGE_MULTIPLIER);
            sendLog('info', '近战',
                '[攻击] idx=' + attackIdx +
                ' range ' + orig.toFixed(2) +
                ' → ' + (orig * KNIFE_RANGE_MULTIPLIER).toFixed(2));
        } catch(e) {}
    }

    sendLog('info', '近战', 'v18 诊断版已启用 (attach模式, 启发式识别)');
    sendLog('info', '近战', '进入任意模式挥刀查看日志...');

})();
