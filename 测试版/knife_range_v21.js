// ============================================================
// 近战距离修改器 v21 — v20去除写入延迟，从第1刀就生效
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
    var myPlayer = null;
    var myPlayerFound = false;

    var callCount = 0;
    var rangeLogCount = 0;

    // ============================================================
    // 步骤1: replace get_KnifeSpeed 捕获 myPlayer (v19验证可用)
    // ============================================================
    try {
        var getKnifeSpeedAddr = base.add(0xB170A0);
        var origGetKnifeSpeed = new NativeFunction(getKnifeSpeedAddr, 'float', ['pointer']);
        Interceptor.replace(getKnifeSpeedAddr, new NativeCallback(function(self) {
            var result = origGetKnifeSpeed(self);
            if (!myPlayerFound) {
                try {
                    var owner = self.add(0x8).readPointer();
                    if (owner && !owner.isNull() && isMyPlayerFn(owner)) {
                        myPlayer = owner;
                        myPlayerFound = true;
                        sendLog('info', '近战', '捕获myPlayer @ ' + myPlayer);
                    }
                } catch(e) {}
            }
            return result;
        }, 'float', ['pointer']));
        sendLog('info', '近战', 'get_KnifeSpeed replace @ ' + getKnifeSpeedAddr);
    } catch(e) {
        sendLog('warn', '近战', 'get_KnifeSpeed hook失败: ' + e.message);
    }

    // ============================================================
    // 步骤2: Hook GetKnifeAttackData（只Hook一个，避免双写冲突）
    // ============================================================
    try {
        Interceptor.attach(base.add(0xB63EC0), {
            onEnter: function(args) {
                this.wpnSelf = args[1];
                this.attackIdx = args[2].toInt32();
                try {
                    this.owner = args[1].add(0x30).readPointer();
                } catch(e) {
                    this.owner = null;
                }
            },
            onLeave: function(retval) {
                callCount++;

                if (callCount <= 20) {
                    sendLog('info', '近战',
                        '=== 调用#' + callCount + ' ===');
                    sendLog('info', '近战',
                        'self=' + this.wpnSelf +
                        ' owner=' + (this.owner || 'null') +
                        ' retval=' + retval);
                }

                try {
                    if (callCount <= 3) {
                        try {
                            var rng = Process.findRangeByAddress(retval);
                            if (rng) {
                                sendLog('info', '近战',
                                    '  retval区域: base=' + rng.base +
                                    ' size=' + rng.size +
                                    ' prot=' + rng.protection);
                            }
                        } catch(e) {}
                    }

                    var dmg = retval.add(0x0).readFloat();
                    var orig = retval.add(0x4).readFloat();
                    var ang = retval.add(0x8).readFloat();

                    if (callCount <= 20) {
                        sendLog('info', '近战',
                            '  retval: damage=' + dmg.toFixed(2) +
                            ' range=' + orig.toFixed(2) +
                            ' angle=' + ang.toFixed(2));
                    }

                    var isOwnerMine = myPlayerFound &&
                        this.owner && !this.owner.isNull() &&
                        this.owner.equals(myPlayer);

                    if (callCount <= 20 && isOwnerMine) {
                        sendLog('info', '近战', '  owner==myPlayer ✓');
                    }

                    if (!isOwnerMine) return;

                    if (!(orig > 0.3 && orig < 500)) return;

                    retval.add(0x4).writeFloat(orig * KNIFE_RANGE_MULTIPLIER);

                    var after = retval.add(0x4).readFloat();

                    rangeLogCount++;
                    if (rangeLogCount <= 10) {
                        sendLog('info', '近战',
                            '[玩家#' + rangeLogCount + '] idx=' + this.attackIdx +
                            ' range ' + orig.toFixed(2) +
                            ' → ' + after.toFixed(2));
                    }
                } catch(e) {
                    if (callCount <= 5) {
                        sendLog('error', '近战',
                            'onLeave异常(调用#' + callCount + '): ' + e.message);
                    }
                }
            }
        });
        sendLog('info', '近战', 'Hook GetKnifeAttackData @ ' + base.add(0xB63EC0));
    } catch(e) { sendLog('error', '近战', 'Hook 失败: ' + e.message); }

    // ============================================================
    // 房间切换
    // ============================================================
    var cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
    for (var i = 0; i < cleanupAddrs.length; i++) {
        try {
            Interceptor.attach(base.add(cleanupAddrs[i]), {
                onEnter: function() {
                    myPlayer = null;
                    myPlayerFound = false;
                    callCount = 0;
                    rangeLogCount = 0;
                    sendLog('info', '近战', '房间切换，全部重置');
                }
            });
        } catch(e) {}
    }

    sendLog('info', '近战', 'v21 已启用 (' + KNIFE_RANGE_MULTIPLIER + 'x)');

})();
