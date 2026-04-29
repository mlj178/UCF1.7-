// ============================================================
// 近战距离修改器 v4 — Plan1 内存锁定 + 全量扫描
// 参考: 无限子弹 plan1_memory_lock.js
//
// Hook: PlayKnifeAttackAnim (RVA 0xB642B0) ← 已验证稳定
// 内存策略:
//   1. 首次攻击 → 打印 raw hex dump 看清数组结构
//   2. 全量扫描 WeaponData_Knife 找出所有 range 候选值
//   3. 每次攻击 → 写入倍数值到所有候选偏移
//   4. 不再 onLeave 恢复（连续锁定，参考 plan1 定时写回）
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
    var attackCount = 0;
    var maxVerbose = 6;

    // 持续锁定列表: { addr, original }
    var lockedRanges = [];     // 已发现的所有 range 候选地址
    var lockInterval = null;   // 定时器 ID
    var activeWeaponData = null;

    function enable() {
        if (enabled) return;
        var gm = getGameAssembly();
        if (!gm) { sendLog('error', '近战距离', '未找到 GameAssembly'); return; }
        var base = gm.base;

        isMyWeaponFn = new NativeFunction(base.add(0xB6E1D0), 'bool', ['pointer', 'pointer']);

        var hookAddr = base.add(0xB642B0);
        attackCount = 0;

        sendLog('info', '近战距离', 'v4 内存锁定 Hook PlayKnifeAttackAnim @ ' + hookAddr);

        playAnimHook = Interceptor.attach(hookAddr, {
            onEnter: function(args) {
                attackCount++;
                var self = args[0];
                var attackType = args[1].toInt32();

                if (!self || self.isNull()) return;
                if (!isMyWeaponFn(self, ptr(0))) return;

                var verbose = attackCount <= maxVerbose;

                if (verbose) {
                    sendLog('info', '近战距离', '');
                    sendLog('info', '近战距离', '===== 攻击 #' + attackCount + ' type=' + attackType + ' =====');
                    sendLog('info', '近战距离', 'WPN_Knife: ' + self);
                }

                try {
                    var dataPtr = self.add(0x68).readPointer();
                    if (!dataPtr || dataPtr.isNull()) return;
                    if (verbose) sendLog('info', '近战距离', 'WeaponData: ' + dataPtr);

                    // 如果武器数据变了（换刀），重新扫描
                    if (!activeWeaponData || !activeWeaponData.equals(dataPtr)) {
                        activeWeaponData = dataPtr;
                        lockedRanges = [];

                        // ===== 阶段 1: 全量扫描 WeaponData_Knife =====
                        if (verbose) sendLog('info', '近战距离', '--- WeaponData_Knife 全量 float 扫描 ---');

                        for (var off = 0x28; off < 0x160; off += 4) {
                            try {
                                var f = dataPtr.add(off).readFloat();
                                if (f > 0.5 && f < 500 && !isNaN(f)) {
                                    if (verbose)
                                        sendLog('info', '近战距离', '  +0x' + off.toString(16) + ' float=' + f.toFixed(4));

                                    // 收录可能是 range 的值（排除明显的 speed、damage 等）
                                    if (f > 0.5 && f < 100) {
                                        lockedRanges.push({addr: dataPtr.add(off), original: f});
                                    }
                                }
                            } catch(e) {}
                        }

                        // ===== 阶段 2: 解析 knifeAttacks 数组 =====
                        var arrPtr = dataPtr.add(0xC0).readPointer();
                        if (arrPtr && !arrPtr.isNull()) {
                            if (verbose) sendLog('info', '近战距离', 'knifeAttacks 数组: ' + arrPtr);

                            // 打印 raw hex
                            if (verbose && attackCount <= 2) {
                                sendLog('info', '近战距离', '--- 数组 raw hex (前 0x100 字节) ---');
                                var hexStr = '';
                                for (var h = 0; h < 0x100 && h < 512; h++) {
                                    try {
                                        var b = arrPtr.add(h).readU8();
                                        hexStr += ('0' + b.toString(16)).slice(-2);
                                        if ((h + 1) % 16 === 0) {
                                            sendLog('info', '近战距离', '  +' + h.toString(16).padStart(3,'0') + ': ' + hexStr);
                                            hexStr = '';
                                        } else if ((h + 1) % 8 === 0) {
                                            hexStr += ' ';
                                        }
                                    } catch(e) { break; }
                                }
                                if (hexStr) sendLog('info', '近战距离', '  (truncated)');
                            }

                            // 尝试多种元素大小解析
                            var elemSizes = [0x10, 0x18, 0x20, 0x24];
                            for (var esIdx = 0; esIdx < elemSizes.length; esIdx++) {
                                var es = elemSizes[esIdx];
                                if (verbose)
                                    sendLog('info', '近战距离', '--- 尝试 elemSize=0x' + es.toString(16) + ' ---');

                                for (var ei = 0; ei < 8; ei++) {
                                    var ea = arrPtr.add(0x20 + ei * es);
                                    try {
                                        var dmg = ea.add(0x0).readFloat();
                                        var rng = ea.add(0x4).readFloat();
                                        var ang = ea.add(0x8).readFloat();

                                        if (rng > 0.3 && rng < 200 && dmg >= 0 && dmg < 10000) {
                                            if (verbose)
                                                sendLog('info', '近战距离',
                                                    '  [elemSize=0x' + es.toString(16) + ' idx=' + ei + ']' +
                                                    ' dmg=' + dmg.toFixed(1) +
                                                    ' range=' + rng.toFixed(2) +
                                                    ' angle=' + ang.toFixed(2) +
                                                    ' @ ' + ea);

                                            // 纳入锁定列表
                                            lockedRanges.push({addr: ea.add(0x4), original: rng});
                                        }
                                    } catch(e) {}
                                }
                            }
                        }

                        if (verbose)
                            sendLog('info', '近战距离', '共发现 ' + lockedRanges.length + ' 个 range 候选');

                        // 启动持续锁定定时器
                        startLockTimer();
                    }

                    // ===== 立即写入倍数值 =====
                    writeAllRanges();

                } catch (e) {
                    if (verbose) sendLog('error', '近战距离', '异常: ' + e);
                }
            }
        });

        // 切房间清理
        var cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
        for (var i = 0; i < cleanupAddrs.length; i++) {
            try {
                Interceptor.attach(base.add(cleanupAddrs[i]), {
                    onEnter: function() {
                        lockedRanges = [];
                        activeWeaponData = null;
                        sendLog('info', '近战距离', '房间切换，缓存已清理');
                    }
                });
            } catch(e) {}
        }

        enabled = true;
        sendLog('info', '近战距离', 'v4 内存锁定已启用 (' + KNIFE_RANGE_MULTIPLIER + 'x)');
    }

    function writeAllRanges() {
        var written = 0;
        for (var i = 0; i < lockedRanges.length; i++) {
            try {
                lockedRanges[i].addr.writeFloat(lockedRanges[i].original * KNIFE_RANGE_MULTIPLIER);
                written++;
            } catch(e) {
                // 尝试 Memory.protect
                try {
                    var page = lockedRanges[i].addr.and(ptr(0xFFFFFFFFFFFFF000));
                    Memory.protect(page, 0x1000, 'rwx');
                    lockedRanges[i].addr.writeFloat(lockedRanges[i].original * KNIFE_RANGE_MULTIPLIER);
                    Memory.protect(page, 0x1000, 'rw-');
                    written++;
                } catch(e2) {}
            }
        }
        if (attackCount <= maxVerbose && written > 0)
            sendLog('info', '近战距离', '已写入 ' + written + ' 个 range 值');
    }

    function startLockTimer() {
        if (lockInterval) clearInterval(lockInterval);
        lockInterval = setInterval(function() {
            if (lockedRanges.length > 0) writeAllRanges();
        }, 500);  // 每 500ms 锁定一次
    }

    function disable() {
        if (!enabled) return;
        if (playAnimHook) { playAnimHook.detach(); playAnimHook = null; }
        if (lockInterval) { clearInterval(lockInterval); lockInterval = null; }
        // 恢复所有原始值
        for (var i = 0; i < lockedRanges.length; i++) {
            try { lockedRanges[i].addr.writeFloat(lockedRanges[i].original); } catch(e) {}
        }
        lockedRanges = [];
        enabled = false;
        sendLog('info', '近战距离', 'v4 已禁用，值已恢复 (共 ' + attackCount + ' 次攻击)');
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info', '近战距离', '倍数 → ' + v + 'x');
        writeAllRanges();
    };

    sendLog('info', '近战距离', 'v4 内存锁定已加载，自动启用中...');
    enable();

})();
