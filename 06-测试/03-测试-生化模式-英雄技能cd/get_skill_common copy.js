(function () {
    'use strict';

    function sendLog(level, module, message) {
        send({ type: 'log', level: level, module: module, message: message });
    }

    // ===== 工具函数 =====
    var _base = null;
    function initBase() {
        var mod = Process.findModuleByName("GameAssembly.dll");
        if (!mod) { sendLog('error', '初始化', 'GameAssembly.dll 未找到'); return false; }
        _base = mod.base;
        sendLog('info', '初始化', 'GameAssembly.dll base = ' + _base);
        return true;
    }
    function readPtr(addr) {
        try { if (!addr || addr.isNull()) return null; var v = addr.readPointer(); return (v && !v.isNull()) ? v : null; } catch (e) { return null; }
    }
    function readI32(addr) { try { return addr ? addr.readS32() : null; } catch (e) { return null; } }
    function readF32(addr) { try { return addr ? addr.readFloat() : null; } catch (e) { return null; } }
    function readU8(addr) { try { return addr ? addr.readU8() : null; } catch (e) { return null; } }
    function readStr(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            var p = addr.readPointer();
            if (!p || p.isNull()) return null;
            var len = p.add(-4).readS32();
            if (len < 0 || len > 200) return null;
            return p.readUtf8String(len);
        } catch (e) { return null; }
    }

    // ===== 全局状态 =====
    var myPlayerPtr = null;
    var _endColdFn = null;
    var _noCdTimer = null;

    if (!initBase()) return;

    // EndCold 函数指针 (RVA 0xAE1BC0, void EndCold())
    try {
        _endColdFn = new NativeFunction(_base.add(0xAE1BC0), 'void', ['pointer']);
        sendLog('info', '初始化', 'EndCold 函数就绪 (RVA 0xAE1BC0)');
    } catch (e) {
        sendLog('error', '初始化', 'EndCold 创建失败: ' + e);
        return;
    }

    // ============================================================
    // 步骤 1: 获取 Player 实例地址
    // ============================================================
    sendLog('info', '步骤1', '===== 获取 Player 实例地址 =====');

    try {
        var addrIsMy = _base.add(0xB55FD0);
        var origIsMy = new NativeFunction(addrIsMy, 'bool', ['pointer', 'pointer']);
        Interceptor.replace(addrIsMy, new NativeCallback(function (playerPtr, methodInfo) {
            try {
                var result = origIsMy(playerPtr, methodInfo);
                if (result && !myPlayerPtr) {
                    myPlayerPtr = playerPtr;
                    sendLog('success', '步骤1-A', 'isMyPlayer: ' + playerPtr);
                    scanSkillSteps(playerPtr);
                }
                return result;
            } catch (e) { return false; }
        }, 'bool', ['pointer', 'pointer']));
        sendLog('success', '步骤1-A', 'isMyPlayer Hook OK');
    } catch (e) { sendLog('error', '步骤1-A', '失败: ' + e); }

    try {
        var addrUpdate = _base.add(0xB551D0);
        Interceptor.attach(addrUpdate, {
            onEnter: function (args) {
                if (myPlayerPtr) return;
                var p = args[0];
                if (!p || p.isNull()) return;
                var cd = readPtr(p.add(0x94));
                if (!cd) return;
                if (readU8(cd.add(0x1C))) return;
                myPlayerPtr = p;
                sendLog('success', '步骤1-B', 'Player.Update: ' + p);
                scanSkillSteps(p);
            }
        });
        sendLog('success', '步骤1-B', 'Player.Update Hook OK');
    } catch (e) { sendLog('error', '步骤1-B', '失败: ' + e); }

    try {
        var addrNick = _base.add(0xB50810);
        Interceptor.attach(addrNick, {
            onEnter: function (args) {
                if (myPlayerPtr) return;
                var p = args[0];
                if (!p || p.isNull()) return;
                var cd = readPtr(p.add(0x94));
                if (!cd) return;
                if (readU8(cd.add(0x1C))) return;
                myPlayerPtr = p;
                sendLog('success', '步骤1-C', 'get_nickName: ' + p);
                scanSkillSteps(p);
            }
        });
        sendLog('success', '步骤1-C', 'get_nickName Hook OK');
    } catch (e) { sendLog('warn', '步骤1-C', '失败: ' + e); }

    // ============================================================
    // 扫描 Skill_Common 实例
    // ============================================================
    function scanSkillSteps(pp) {
        var ps = readPtr(pp.add(0xB0));
        if (!ps) { sendLog('error', '步骤2', 'PlayerSkills 为空'); return; }
        sendLog('success', '步骤2', 'PlayerSkills: ' + ps);
        var arr = readPtr(ps.add(0x08));
        if (!arr) { sendLog('error', '步骤3', 'Skill[] 为空'); return; }
        sendLog('success', '步骤3', 'Skill[]: ' + arr);
        var len = readI32(arr.add(0x0C));
        if (!len || len <= 0 || len > 20) { sendLog('warn', '步骤3', '长度: ' + len); return; }
        sendLog('info', '步骤4', '遍历识别 Skill_Common');
        var found = 0;
        for (var i = 0; i < len; i++) {
            var sp = readPtr(arr.add(0x10 + 4 * i));
            if (!sp) continue;
            var coldFinish = readF32(sp.add(0x1C));
            var coldTime = readF32(sp.add(0x24));
            if (coldFinish !== null || coldTime !== null) {
                sendLog('success', '步骤4', 'Skill_Common: ' + sp);
                found++;
            }
        }
        if (found === 0) sendLog('warn', '步骤4', '未找到');
    }

    // ============================================================
    // 扫描 + 调用 EndCold
    // ============================================================
    function scanAndEndCold() {
        if (!myPlayerPtr) return;
        var ps = readPtr(myPlayerPtr.add(0xB0));
        if (!ps) return;
        var arr = readPtr(ps.add(0x08));
        if (!arr) return;
        var len = readI32(arr.add(0x0C));
        if (!len || len <= 0 || len > 20) return;

        var called = 0; 
        for (var i = 0; i < len; i++) {
            var sp = readPtr(arr.add(0x10 + 4 * i));
            if (!sp) continue;
            var coldFinish = readF32(sp.add(0x1C));
            var coldTime = readF32(sp.add(0x24));
            if (coldFinish !== null || coldTime !== null) {
                try {
                    _endColdFn(sp);
                    called++;
                } catch (e) { /* 忽略 */ }
            }
        }
        if (called > 0) {
            sendLog('success', '无CD', '已调用 EndCold × ' + called);
        }
    }

    // ============================================================
    // 技能无冷却开关
    // ============================================================
    globalThis.noCd = function (enable) {
        if (enable) {
            if (_noCdTimer) return;
            sendLog('success', '无CD', '✅ 已开启 — 每 200ms 调用 EndCold()');
            // 先立即执行一次
            scanAndEndCold();
            _noCdTimer = setInterval(scanAndEndCold, 200);
        } else {
            if (!_noCdTimer) return;
            clearInterval(_noCdTimer);
            _noCdTimer = null;
            sendLog('success', '无CD', '⏹ 已关闭');
        }
    };

    // ============================================================
    // 全局命令
    // ============================================================
    globalThis.scanSkill = function () {
        if (myPlayerPtr) scanSkillSteps(myPlayerPtr);
        else sendLog('warn', '手动', '尚无玩家实例');
    };
    globalThis.getMyPlayer = function () { return myPlayerPtr; };

    // rpc 导出，供 Python launcher 调用
    rpc.exports = {
        noCd: function (enable) {
            if (enable) {
                if (_noCdTimer) return;
                scanAndEndCold();
                _noCdTimer = setInterval(scanAndEndCold, 200);
            } else {
                if (!_noCdTimer) return;
                clearInterval(_noCdTimer);
                _noCdTimer = null;
            }
        }
    };

    sendLog('info', '系统', '✅ 已加载');
    sendLog('info', '系统', '命令: noCd(true)  — 调用 EndCold 清 CD');
    sendLog('info', '系统', '命令: noCd(false) — 停止');
})();
