// ============================================================
// 移动速度 + 近战距离 修改器 v3
// 原理:
//   1. MoveSpeed: Hook PropertyModifier.Get (RVA 0xB17590) ✓ 已验证有效
//   2. KnifeRange: Hook WPN_Knife$$KnifeAttackEvent (RVA 0xB63DD0)
//      进入攻击时扫描 WPN_Knife 对象查找 range 字段并直接修改内存
//   3. 备用: Hook get_KnifeRange (RVA 0xB17060) 如果被调用则拦截
//   4. 所有 Hook 点都打印内存真实值
// ============================================================

(function() {
    'use strict';

    var KNIFE_RANGE_MULTIPLIER = 5.0;
    var MOVE_SPEED_MULTIPLIER = 3.0;

    var gameAssembly = null;
    var isMyPlayerFn = null;

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
    // 模块 1: 移动速度 - Hook PropertyModifier.Get
    // ============================================================
    var moveSpeedMod = (function() {
        var enabled = false, hookAddr = null, originalFn = null, logCount = 0;

        return {
            enable: function() {
                if (enabled) return;
                var gm = getGameAssembly(); if (!gm) return;
                var base = gm.base;
                hookAddr = base.add(0xB17590);
                isMyPlayerFn = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);
                originalFn = new NativeFunction(hookAddr, 'float', ['pointer','pointer']);
                logCount = 0;

                Interceptor.replace(hookAddr, new NativeCallback(function(self, player) {
                    var result = originalFn(self, player);
                    if (player && !player.isNull() && isMyPlayerFn(player)) {
                        var moveMod = player.add(0x8C).readPointer();
                        if (moveMod && !moveMod.isNull() && self.equals(moveMod)) {
                            logCount++;
                            if (logCount <= 10)
                                sendLog('info','移动速度','内存真实原值=' + result.toFixed(3) + ' 修改后=' + MOVE_SPEED_MULTIPLIER.toFixed(1) + 'x');
                            return MOVE_SPEED_MULTIPLIER;
                        }
                    }
                    return result;
                }, 'float', ['pointer','pointer']));

                enabled = true;
                sendLog('info','移动速度','已启用 (' + MOVE_SPEED_MULTIPLIER + 'x)');
            },
            disable: function() {
                if (!enabled || !hookAddr) return;
                Interceptor.revert(hookAddr); enabled = false;
            }
        };
    })();

    // ============================================================
    // 模块 2: 近战距离 - Hook KnifeAttackEvent + 备用 get_KnifeRange
    // ============================================================
    var knifeRangeMod = (function() {
        var enabled = false;
        var getKnifeRangeHookAddr = null, getKnifeRangeOrig = null, getKnifeRangeLogCount = 0;
        var knifeAttackHookAddr = null, knifeAttackLogCount = 0;
        var playerWeaponsOffset = 0xA0;
        var knifeRangeModOffset = 0x40;

        // 扫描 WPN_Knife 对象的武器数据来找 range
        function scanWpnKnifeForRange(wpnKnife) {
            send('=== WPN_Knife 对象扫描 (' + wpnKnife + ') ===');
            
            // 先找 WeaponData_Knife (通常是 wpnKnife + offset)
            // WPN_Knife 继承自 Weapon, 武器数据在 +0x28 (realData)
            // 或者通过 this->data
            var offsets_to_try = [0x28, 0x2C, 0x30, 0x34, 0x38, 0x3C, 0x40, 0x48, 0x50, 0x58];
            
            for (var di = 0; di < offsets_to_try.length; di++) {
                try {
                    var dataPtr = wpnKnife.add(offsets_to_try[di]).readPointer();
                    if (!dataPtr || dataPtr.isNull()) continue;
                    send('  dataPtr @ +0x' + offsets_to_try[di].toString(16) + ': ' + dataPtr);
                    
                    // 扫描 dataPtr 中的 float 值
                    send('  --- ' + dataPtr + ' 内存内容 ---');
                    for (var i = 0; i < 0x80; i += 4) {
                        try {
                            var f = dataPtr.add(i).readFloat();
                            if (f >= 0.01 && f <= 100.0) {
                                send('    +0x' + i.toString(16) + ' float=' + f.toFixed(4));
                            }
                        } catch(e) {}
                    }
                } catch(e) {}
            }
            
            // 也扫描 wpnKnife 自身
            send('  --- WPN_Knife 自身内存 ---');
            for (var i = 0; i < 0x100; i += 4) {
                try {
                    var f = wpnKnife.add(i).readFloat();
                    if (f >= 0.1 && f <= 1000.0 && f !== 1.0) {
                        send('    +0x' + i.toString(16) + ' float=' + f.toFixed(4));
                    }
                } catch(e) {}
            }
        }

        // 扫描本地玩家的 PlayerWeapons 和 Modifier
        function scanPlayerKnifeMod() {
            send('=== 本地玩家 KnifeRange Modifier 内存 ===');
            var gm = getGameAssembly(); if (!gm) return;
            var base = gm.base;
            
            try {
                // 找本地玩家
                var playerMgr = base.add(0xE25410).readPointer();
                if (!playerMgr || playerMgr.isNull()) return;
                
                var localPlayer = null;
                for (var off = 0; off <= 0x20; off += 4) {
                    try {
                        var p = playerMgr.add(off).readPointer();
                        if (p && !p.isNull() && isMyPlayerFn && isMyPlayerFn(p)) {
                            localPlayer = p; break;
                        }
                    } catch(e) {}
                }
                if (!localPlayer) return;
                
                var pw = localPlayer.add(playerWeaponsOffset).readPointer();
                if (!pw || pw.isNull()) return;
                
                var km = pw.add(knifeRangeModOffset).readPointer();
                if (!km || km.isNull()) return;
                
                send('KnifeRange Modifier: ' + km);
                for (var i = 0; i < 0x60; i += 4) {
                    try {
                        var f = km.add(i).readFloat();
                        if (f >= 0.01 && f <= 100.0) {
                            send('  +0x' + i.toString(16) + ' float=' + f.toFixed(6));
                        }
                    } catch(e) {}
                }
            } catch(e) {}
        }

        return {
            enable: function() {
                if (enabled) return;
                var gm = getGameAssembly(); if (!gm) return;
                var base = gm.base;

                if (!isMyPlayerFn)
                    isMyPlayerFn = new NativeFunction(base.add(0xB55FD0), 'bool', ['pointer']);

                // --- Hook 1: KnifeAttackEvent (RVA 0xB63DD0) ---
                // 这是每次近战攻击必然调用的函数
                knifeAttackHookAddr = base.add(0xB63DD0);
                sendLog('info','近战距离','Hook KnifeAttackEvent @ ' + knifeAttackHookAddr);
                knifeAttackLogCount = 0;

                Interceptor.attach(knifeAttackHookAddr, {
                    onEnter: function(args) {
                        knifeAttackLogCount++;
                        var self = args[0]; // WPN_Knife pointer
                        
                        if (knifeAttackLogCount <= 3) {
                            sendLog('info','近战距离','[KnifeAttackEvent 被调用!] self=' + self + ' #' + knifeAttackLogCount);
                            // 扫描武器对象找 range
                            scanWpnKnifeForRange(self);
                            // 同时扫描 KnifeRange Modifier
                            scanPlayerKnifeMod();
                        }
                        
                        // 每次攻击都强制写入 Modifier 值
                        scanAndWriteModifier();
                    }
                });

                // --- Hook 2: get_KnifeRange (RVA 0xB17060) 作为备用 ---
                getKnifeRangeHookAddr = base.add(0xB17060);
                getKnifeRangeOrig = new NativeFunction(getKnifeRangeHookAddr, 'float', ['pointer']);
                getKnifeRangeLogCount = 0;
                sendLog('info','近战距离','Hook get_KnifeRange (备用) @ ' + getKnifeRangeHookAddr);

                Interceptor.replace(getKnifeRangeHookAddr, new NativeCallback(function(self) {
                    var result = getKnifeRangeOrig(self);
                    getKnifeRangeLogCount++;
                    if (getKnifeRangeLogCount <= 10) {
                        sendLog('info','近战距离','[get_KnifeRange] self=' + self + ' 内存真实值=' + result.toFixed(3) + ' 修改后=' + KNIFE_RANGE_MULTIPLIER.toFixed(1));
                    }
                    return KNIFE_RANGE_MULTIPLIER;
                }, 'float', ['pointer']));

                enabled = true;
                sendLog('info','近战距离','已启用 (' + KNIFE_RANGE_MULTIPLIER + 'x)');
                sendLog('info','近战距离','请按近战攻击键触发扫描...');
            },
            disable: function() {
                if (!enabled) return;
                if (getKnifeRangeHookAddr)
                    Interceptor.revert(getKnifeRangeHookAddr);
                if (knifeAttackHookAddr)
                    Interceptor.detachAll();
                enabled = false;
                sendLog('info','近战距离','已禁用');
            }
        };
    })();

    // 强制扫描并写入 Modifier
    function scanAndWriteModifier() {
        var gm = getGameAssembly(); if (!gm) return;
        var base = gm.base;
        try {
            var playerMgr = base.add(0xE25410).readPointer();
            if (!playerMgr || playerMgr.isNull()) return;
            
            var localPlayer = null;
            for (var off = 0; off <= 0x20; off += 4) {
                try {
                    var p = playerMgr.add(off).readPointer();
                    if (p && !p.isNull() && isMyPlayerFn && isMyPlayerFn(p)) {
                        localPlayer = p; break;
                    }
                } catch(e) {}
            }
            if (!localPlayer) return;
            
            var pw = localPlayer.add(0xA0).readPointer();
            if (!pw || pw.isNull()) return;
            
            var km = pw.add(0x40).readPointer();
            if (!km || km.isNull()) return;
            
            // 写入可能的 range 偏移
            for (var i = 0x20; i < 0x50; i += 4) {
                try {
                    km.add(i).writeFloat(KNIFE_RANGE_MULTIPLIER);
                } catch(e) {}
            }
        } catch(e) {}
    }

    // ============================================================
    // 全局命令
    // ============================================================
    globalThis.enableAll = function() {
        moveSpeedMod.enable();
        knifeRangeMod.enable();
    };
    globalThis.disableAll = function() {
        moveSpeedMod.disable();
        knifeRangeMod.disable();
    };
    globalThis.setMoveSpeedMultiplier = function(v) {
        MOVE_SPEED_MULTIPLIER = v;
        sendLog('info','系统','移动速度倍数 → ' + v + 'x');
    };
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info','系统','近战距离倍数 → ' + v + 'x');
    };

    sendLog('info','系统','移动速度+近战距离修改器 v3 已加载');
    sendLog('info','系统','enableAll() 启用 / disableAll() 停用 / setKnifeRangeMultiplier(n)');

})();
