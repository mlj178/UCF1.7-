// ============================================================
// 近战距离修改器 v14 — isMyWeapon(onEnter) + retval(onLeave)
//
// 策略: 合并 speed_knife_v16 的玩家识别 + v12 的 retval 修改
//
// 玩家识别 (参考 speed_knife_v16):
//   Weapon.get_isMyWeapon (RVA 0xB6E1D0) — 游戏内建判断
//   在 onEnter 中调用（与 infinite_ammo_v6 相同验证策略）
//   每个武器实例只调一次，结果缓存到 wpnIsMine
//
// 距离修改 (参考 v12 终端已验证有效):
//   Hook WPN_Knife.GetKnifeAttackData (RVA 0xB63EC0)
//   在 onLeave 中用 retval+0x4 写 range
//
// v12→v14 变更:
//   - 启发式"前N把" → 替换为 isMyWeapon 精确识别
//   - onEnter 调 NativeFunction (infinite_ammo_v6 验证可行)
//   - 加 Process.findRangeByAddress 安全检查
//   - 保留双重 Hook 但加防重复处理
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

    var hookList = [];
    var rangeLogCount = 0;

    // 缓存: { weaponPtrStr → true=玩家, false=Bot }
    var wpnIsMine = {};
    var isMyWeaponFn = null;

    function isReadable(p) {
        if (!p || p.isNull()) return false;
        try { return Process.findRangeByAddress(p) !== null; }
        catch(e) { return false; }
    }

    function isPlayerWeapon(wpnPtr) {
        var key = wpnPtr.toString();
        if (wpnIsMine.hasOwnProperty(key)) return wpnIsMine[key];

        if (!isMyWeaponFn || !isReadable(wpnPtr)) {
            wpnIsMine[key] = false;
            return false;
        }

        try {
            var result = isMyWeaponFn(wpnPtr, ptr(0));
            wpnIsMine[key] = !!result;
            if (result) {
                sendLog('info', '近战', '识别玩家武器 @ ' + wpnPtr);
            }
            return !!result;
        } catch(e) {
            wpnIsMine[key] = false;
            return false;
        }
    }

    function modifyRange(retval) {
        var rangeAddr = retval.add(0x4);
        var orig = rangeAddr.readFloat();
        if (!(orig > 0.3 && orig < 500)) return;
        rangeAddr.writeFloat(orig * KNIFE_RANGE_MULTIPLIER);
        rangeLogCount++;
        if (rangeLogCount <= 10) {
            sendLog('info', '近战',
                '[攻击#' + rangeLogCount + '] range ' + orig.toFixed(2) +
                ' → ' + (orig * KNIFE_RANGE_MULTIPLIER).toFixed(2));
        }
    }

    function enable() {
        if (hookList.length > 0) return;

        var mod = Process.findModuleByName('GameAssembly.dll');
        if (!mod) { sendLog('error', '近战', 'GameAssembly.dll 未找到'); return; }
        var base = mod.base;

        // Weapon.get_isMyWeapon (RVA 0xB6E1D0)
        isMyWeaponFn = new NativeFunction(base.add(0xB6E1D0), 'bool', ['pointer', 'pointer']);
        sendLog('info', '近战', 'isMyWeapon @ ' + base.add(0xB6E1D0));

        wpnIsMine = {};
        rangeLogCount = 0;

        // ============================================================
        // Hook 1: WPN_Knife.GetKnifeAttackData (RVA 0xB63EC0)
        // ============================================================
        try {
            hookList.push(Interceptor.attach(base.add(0xB63EC0), {
                onEnter: function(args) {
                    var wpn = args[1];
                    if (!wpn || wpn.isNull()) {
                        this.skip = true;
                        return;
                    }
                    this.wpn = wpn;
                    this.attackIdx = args[2].toInt32();
                    this.isMine = isPlayerWeapon(wpn);
                    this.skip = false;
                },
                onLeave: function(retval) {
                    if (this.skip || !this.isMine) return;
                    try { modifyRange(retval); }
                    catch(e) {}
                }
            }));
            sendLog('info', '近战', 'Hook GetKnifeAttackData @ ' + base.add(0xB63EC0));
        } catch(e) { sendLog('error', '近战', 'Hook 1 失败: ' + e.message); }

        // ============================================================
        // Hook 2: Weapon.GetKnifeAttackData 基类兜底 (RVA 0xB79008)
        // 防重复: 同一调用链中 WPN_Knife hook 已处理 → 跳过
        // ============================================================
        try {
            hookList.push(Interceptor.attach(base.add(0xB79008), {
                onEnter: function(args) {
                    var wpn = args[1];
                    if (!wpn || wpn.isNull()) {
                        this.skip = true;
                        return;
                    }
                    // 如果 WPN_Knife hook 已识别并会处理，跳过
                    var key = wpn.toString();
                    if (wpnIsMine.hasOwnProperty(key) && wpnIsMine[key]) {
                        this.isMine = true;
                    } else {
                        this.isMine = isPlayerWeapon(wpn);
                    }
                    this.skip = false;
                },
                onLeave: function(retval) {
                    if (this.skip || !this.isMine) return;
                    try { modifyRange(retval); }
                    catch(e) {}
                }
            }));
            sendLog('info', '近战', 'Hook Weapon.GetKnifeAttackData @ ' + base.add(0xB79008));
        } catch(e) {}

        // ============================================================
        // 房间切换 → 重置缓存
        // ============================================================
        var cleanupAddrs = [0xAFAA40, 0xAF5B30, 0xAF15D0];
        for (var i = 0; i < cleanupAddrs.length; i++) {
            try {
                Interceptor.attach(base.add(cleanupAddrs[i]), {
                    onEnter: function() {
                        wpnIsMine = {};
                        rangeLogCount = 0;
                        sendLog('info', '近战', '房间切换，重置缓存');
                    }
                });
            } catch(e) {}
        }

        sendLog('info', '近战', 'v14 已启用 (' + KNIFE_RANGE_MULTIPLIER +
            'x, isMyWeapon精确识别)');
    }

    function disable() {
        for (var i = 0; i < hookList.length; i++) {
            try { hookList[i].detach(); } catch(e) {}
        }
        hookList = [];
        wpnIsMine = {};
        sendLog('info', '近战', 'v14 已禁用');
    }

    globalThis.enableKnifeRange = enable;
    globalThis.disableKnifeRange = disable;
    globalThis.setKnifeRangeMultiplier = function(v) {
        KNIFE_RANGE_MULTIPLIER = v;
        sendLog('info', '近战', '倍数 → ' + v + 'x');
    };

    sendLog('info', '近战', 'v14 已加载，自动启用...');
    enable();

})();
