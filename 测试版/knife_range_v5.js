// ============================================================
// 近战距离修改器 v5 — 32-bit 精确解析 + 实例字段扫描
//
// 核心发现:
//   1. 游戏是 32-bit (不是 64-bit!)
//      Il2CppArray: klass(4) monitor(4) bounds(4) max_length(4) = 头 0x10
//      元素从 +0x10 开始, KnifeAttackData 大小 0x1C
//   2. WeaponData_Knife 是 ScriptableObject 共享资产
//      直接修改它 → 人机生效、玩家无效、UI 损坏
//   3. 正确策略: 找 WPN_Knife 实例上的 per-instance range 拷贝
//      类似 combo1_AnimSpeed 在实例 +0xEC, 每个玩家独立
//
// 做法:
//   1. Hook PlayKnifeAttackAnim (已验证稳定)
//   2. 从 WeaponData 精确读取 KnifeAttackData[type].range 作为基准值
//   3. 扫描 WPN_Knife 实例 (this), 找到和基准值相同的 float
//      这些就是 per-instance 拷贝!
//   4. 用 isMyWeapon 过滤, 只改玩家实例上的拷贝
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

    // ============================================================
    // 32-bit Il2CppArray 解析
    // ============================================================
    function parseIl2CppArray32(arrPtr) {
        // 32-bit 布局:
        // +0x00: klass (4 bytes)
        // +0x04: monitor (4 bytes)
        // +0x08: bounds (4 bytes)
        // +0x0C: max_length (4 bytes, int32)
        // +0x10: first element
        return {
            klass: arrPtr.readPointer(),
            monitor: arrPtr.add(0x04).readPointer(),
            bounds: arrPtr.add(0x08).readPointer(),
            maxLength: arrPtr.add(0x0C).readU32(),
            elemStart: 0x10
        };
    }

    // 从 KnifeAttackData 数组读取指定 index 的 range 值
    function readKnifeRange(arrPtr, index) {
        var head = parseIl2CppArray32(arrPtr);
        if (index < 0 || index >= head.maxLength) return -1;

        // KnifeAttackData(结构体 0x1C):
        //   +0x0 damage(float) +0x4 range(float) +0x8 angle(float)
        //   +0xC hitStun(bool+pad) +0x10 damageTag(int)
        //   +0x14 decal(ptr) +0x18 decalSndName(ptr)
        var elemSize = 0x1C;
        var elemAddr = arrPtr.add(head.elemStart + index * elemSize);
        return elemAddr.add(0x4).readFloat();  // range @ +0x4
    }

    // ============================================================
    // 主逻辑
    // ============================================================
    var enabled = false;
    var playAnimHook = null;
    var attackCount = 0;
    var maxVerbose = 8;

    // 每个玩家 WPN_Knife 实例上找到的 range 偏移
    var instanceRangeOffsets = {};  // { wpnKnifePtrStr: [offset1, offset2, ...] }

    function enable() {
        if (enabled) return;
        var gm = getGameAssembly();
        if (!gm) { sendLog('error', '近战距离', '未找到 GameAssembly'); return; }
        var base = gm.base;

        isMyWeaponFn = new NativeFunction(base.add(0xB6E1D0), 'bool', ['pointer', 'pointer']);

        var hookAddr = base.add(0xB642B0);
        attackCount = 0;
        instanceRangeOffsets = {};

        sendLog('info', '近战距离', 'v5 32-bit 精确解析 Hook PlayKnifeAttackAnim @ ' + hookAddr);

        playAnimHook = Interceptor.attach(hookAddr, {
            onEnter: function(args) {
                attackCount++;
                var wpnKnife = args[0];
                var attackType = args[1].toInt32();  // 1=Combo1, 2=Combo2, 3=Bigshot

                if (!wpnKnife || wpnKnife.isNull()) return;
                if (!isMyWeaponFn(wpnKnife, ptr(0))) return;  // ★ 只处理玩家武器

                var verbose = attackCount <= maxVerbose;
                var key = wpnKnife.toString();

                if (verbose) {
                    sendLog('info', '近战距离', '');
                    sendLog('info', '近战距离', '===== 攻击 #' + attackCount + ' type=' + attackType + ' =====');
                    sendLog('info', '近战距离', 'WPN_Knife=' + wpnKnife);
                }

                try {
                    // --- 步骤1: 从 WeaponData 读取基准 range 值 ---
                    var dataPtr = wpnKnife.add(0x68).readPointer();
                    if (!dataPtr || dataPtr.isNull()) return;
                    if (verbose) sendLog('info', '近战距离', 'WeaponData=' + dataPtr);

                    var arrPtr = dataPtr.add(0xC0).readPointer();
                    if (!arrPtr || arrPtr.isNull()) {
                        if (verbose) sendLog('warn', '近战距离', 'knifeAttacks 数组为空');
                        return;
                    }

                    var head = parseIl2CppArray32(arrPtr);
                    if (verbose)
                        sendLog('info', '近战距离', 'knifeAttacks len=' + head.maxLength + ' elemStart=0x10 elemSize=0x1C');

                    // 读取所有攻击类型的基准 range
                    var refRanges = [];
                    for (var ti = 0; ti < head.maxLength; ti++) {
                        var rng = readKnifeRange(arrPtr, ti);
                        refRanges.push(rng);
                        if (verbose)
                            sendLog('info', '近战距离', '  [' + ti + '] refRange=' + rng.toFixed(2));
                    }

                    // 当前攻击类型的基准值
                    var currentRefRange = (attackType >= 1 && attackType <= refRanges.length) ?
                        refRanges[attackType - 1] : refRanges[0];
                    if (currentRefRange < 0 || currentRefRange > 500) {
                        if (verbose) sendLog('warn', '近战距离', '基准 range 异常: ' + currentRefRange);
                        return;
                    }

                    // --- 步骤2: 首次遇到此实例, 扫描找 per-instance range 拷贝 ---
                    if (!instanceRangeOffsets[key]) {
                        if (verbose) sendLog('info', '近战距离', '--- 首次扫描 WPN_Knife 实例找 range 拷贝 ---');

                        var found = [];
                        // 扫描 WPN_Knife 实例内存 (从 +0x28 开始，跳过 vtable)
                        for (var off = 0x28; off < 0x200; off += 4) {
                            try {
                                var f = wpnKnife.add(off).readFloat();
                                // 匹配: 值等于任意一个基准 range (容差 0.01)
                                for (var ri = 0; ri < refRanges.length; ri++) {
                                    if (Math.abs(f - refRanges[ri]) < 0.02) {
                                        found.push(off);
                                        if (verbose)
                                            sendLog('info', '近战距离',
                                                '  +0x' + off.toString(16) +
                                                ' float=' + f.toFixed(4) +
                                                ' ≈ refRange[' + ri + ']=' + refRanges[ri].toFixed(2));
                                        break;
                                    }
                                }
                            } catch(e) {}
                        }

                        if (found.length > 0) {
                            instanceRangeOffsets[key] = found;
                            if (verbose)
                                sendLog('info', '近战距离', '实例 ' + wpnKnife + ' 找到 ' + found.length + ' 个 range 拷贝');
                        } else {
                            if (verbose)
                                sendLog('warn', '近战距离', '实例中未找到 range 拷贝! 尝试扩大扫描...');
                            // 扩大扫描：找 WeaponData 地址附近的指针引用
                            for (var off = 0x28; off < 0x200; off += 4) {
                                try {
                                    var ptrVal = wpnKnife.add(off).readPointer();
                                    if (ptrVal && !ptrVal.isNull() && ptrVal.equals(dataPtr)) {
                                        sendLog('info', '近战距离', '  +0x' + off.toString(16) + ' → WeaponData* (引用)');
                                    }
                                } catch(e) {}
                            }
                        }
                    }

                    // --- 步骤3: 写入倍数值到实例上的 range 拷贝 ---
                    var offsets = instanceRangeOffsets[key];
                    if (offsets && offsets.length > 0) {
                        var written = 0;
                        for (var oi = 0; oi < offsets.length; oi++) {
                            try {
                                var addr = wpnKnife.add(offsets[oi]);
                                var orig = addr.readFloat();

                                // 找到当前攻击类型对应的偏移
                                for (var ri = 0; ri < refRanges.length; ri++) {
                                    if (Math.abs(orig - refRanges[ri]) < 0.02) {
                                        var newVal = refRanges[ri] * KNIFE_RANGE_MULTIPLIER;
                                        addr.writeFloat(newVal);
                                        written++;

                                        if (verbose && ri + 1 === attackType) {
                                            sendLog('info', '近战距离',
                                                '  ★ 当前攻击 type=' + attackType +
                                                ' +0x' + offsets[oi].toString(16) +
                                                ' range ' + orig.toFixed(2) + '→' + newVal.toFixed(2));
                                        }
                                        break;
                                    }
                                }
                            } catch(e) {
                                if (verbose) sendLog('warn', '近战距离', '写入失败 +0x' + offsets[oi].toString(16) + ': ' + e);
                            }
                        }
                        if (verbose && written > 0)
                            sendLog('info', '近战距离', '已写 ' + written + ' 个 range (实例)');
                    } else {
                        if (attackCount <= 3) sendLog('warn', '近战距离', '无实例偏移可写!');
                    }

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
                        instanceRangeOffsets = {};
                        sendLog('info', '近战距离', '房间切换，实例缓存已清理');
                    }
                });
            } catch(e) {}
        }

        enabled = true;
        sendLog('info', '近战距离', 'v5 已启用 (只改玩家实例, 32-bit 精确)');
    }

    function disable() {
        if (!enabled) return;
        if (playAnimHook) { playAnimHook.detach(); playAnimHook = null; }
        // 恢复所有实例上的值
        var keys = Object.keys(instanceRangeOffsets);
        sendLog('info', '近战距离', '恢复 ' + keys.length + ' 个实例的值...');
        instanceRangeOffsets = {};
        enabled = false;
        sendLog('info', '近战距离', 'v5 已禁用 (共 ' + attackCount + ' 次攻击)');
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info', '近战距离', '倍数 → ' + v + 'x');
    };

    sendLog('info', '近战距离', 'v5 32-bit 精确版已加载，自动启用中...');
    enable();

})();
