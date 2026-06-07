// ============================================================
// AAAAA-battle_round_always.js - 多人生化模式：每局强制决战回合
//
// 原理：
//   OnStartNewGameRound 中，roundCount%5==0 时写 static_fields[1]=1（决战回合）
//   StartGenerateSupplyBox 读取 static_fields[1] 决定是否进入决战分支
//   （决战分支启动 BattleTimer 协程，非决战分支启动普通补给箱生成器）
//
//   关键时序：
//     OnStartNewGameRound 内部：
//       1. 计算 %5 → 写 static_fields[1]
//       2. 调用 ModeBase_Nano.OnStartNewGameRound
//          → 内部调用 StartGenerateSupplyBox（虚函数）
//          → StartGenerateSupplyBox 读取 static_fields[1]
//
//   如果 Hook OnStartNewGameRound 的 onLeave，写入太晚！
//   因为 StartGenerateSupplyBox 已经在函数内部执行完毕了。
//
//   正确方案：Hook StartGenerateSupplyBox，在 onEnter 中写入 static_fields[1]=1
//   这样 StartGenerateSupplyBox 执行时读到的就是1，进入决战分支
//
// RVA地址（根据IDA分析）：
//   Mode_Nano4_Terminator_TypeInfo: 0xE2CCB4
//   StartGenerateSupplyBox:         0xB45AA0
// ============================================================

(function() {
    'use strict';

    // ==================== 1. 日志系统 ====================
    var MAX_LOGS_PER_MODULE = 100;
    var moduleLogCounts = {};

    function log(level, module, message) {
        if (!moduleLogCounts[module]) moduleLogCounts[module] = 0;
        if (moduleLogCounts[module] >= MAX_LOGS_PER_MODULE) return;
        moduleLogCounts[module]++;
        var fullMsg = '[' + module + '] ' + message;
        console.log('[' + level + '] ' + fullMsg);
        try {
            send({type: 'log', level: level, module: module, message: message});
        } catch(e) {}
    }

    // ==================== 2. 模块查找 ====================
    var _gameAssembly = null;

    function getGameAssembly() {
        if (_gameAssembly) return _gameAssembly;
        try {
            var mod = Process.findModuleByName('GameAssembly.dll');
            if (!mod) {
                log('error', '系统', '未找到 GameAssembly.dll');
                return null;
            }
            _gameAssembly = mod;
            log('success', '系统', 'GameAssembly.dll 基址: ' + mod.base);
            return mod;
        } catch(e) {
            log('error', '系统', '获取模块失败: ' + e.message);
            return null;
        }
    }

    // ==================== 3. RVA地址常量 ====================
    var RVA = {
        Mode_Nano4_Terminator_TypeInfo: 0xE2CCB4,
        StartGenerateSupplyBox:         0xB45AA0,
    };

    // ==================== 4. 字段偏移常量 ====================
    var OFF = {
        Klass_staticFields: 0x5C,   // klass->static_fields 指针偏移
        StaticField_isBattleRound: 1, // static_fields[1] = isBattleRound
    };

    // ==================== 5. 安全读取函数 ====================
    function readPtr(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            var v = addr.readPointer();
            return (v && !v.isNull()) ? v : null;
        } catch(e) {
            return null;
        }
    }

    function readU8(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readU8();
        } catch(e) {
            return null;
        }
    }

    // ==================== 6. 核心功能 ====================

    var _hookInstalled = false;
    var _enabled = false;  // 默认关闭，由UI控制开关

    // 获取 static_fields 指针
    function getStaticFields() {
        try {
            var mod = getGameAssembly();
            if (!mod) return null;
            var base = mod.base;

            // 读取 TypeInfo 槽位 → klass → static_fields
            var typeInfoSlot = base.add(RVA.Mode_Nano4_Terminator_TypeInfo);
            var klass = readPtr(typeInfoSlot);
            if (!klass) return null;

            var staticFields = readPtr(klass.add(OFF.Klass_staticFields));
            if (!staticFields) return null;

            return staticFields;
        } catch(e) {
            log('error', 'Core', '获取 static_fields 失败: ' + e.message);
            return null;
        }
    }

    // 读取当前 isBattleRound 值
    function readBattleRoundFlag() {
        var sf = getStaticFields();
        if (!sf) return -1;
        var val = readU8(sf.add(OFF.StaticField_isBattleRound));
        return val !== null ? val : -1;
    }

    // 强制写入 isBattleRound = 1
    function forceBattleRound() {
        var sf = getStaticFields();
        if (!sf) {
            log('error', 'Core', '无法写入：static_fields 为空');
            return false;
        }
        try {
            sf.add(OFF.StaticField_isBattleRound).writeU8(1);
            return true;
        } catch(e) {
            log('error', 'Core', '写入失败: ' + e.message);
            return false;
        }
    }

    // 安装 Hook
    function installHook() {
        if (_hookInstalled) return true;

        var mod = getGameAssembly();
        if (!mod) return false;
        var base = mod.base;

        var targetAddr = base.add(RVA.StartGenerateSupplyBox);

        try {
            Interceptor.attach(targetAddr, {
                onEnter: function(args) {
                    if (!_enabled) return;  // 未启用时透传

                    var sf = getStaticFields();
                    if (!sf) return;

                    // 读取原始值用于日志
                    var oldVal = readU8(sf.add(OFF.StaticField_isBattleRound));

                    // 在 StartGenerateSupplyBox 执行前，强制写入 isBattleRound = 1
                    // 这样函数内部读取 static_fields[1] 时就是1，进入决战分支
                    try {
                        sf.add(OFF.StaticField_isBattleRound).writeU8(1);
                        log('success', 'Hook', '决战回合已强制开启 (原值=' + oldVal + ' → 新值=1)');
                    } catch(e) {
                        log('error', 'Hook', '写入失败: ' + e.message);
                    }
                }
            });

            _hookInstalled = true;
            log('success', 'Hook', 'StartGenerateSupplyBox Hook 已安装 (RVA=0x' + RVA.StartGenerateSupplyBox.toString(16) + ')');
            return true;

        } catch(e) {
            log('error', 'Hook', 'Hook 安装失败: ' + e.message);
            return false;
        }
    }

    // ==================== 7. RPC接口导出 ====================
    // 注意：Frida Python端会自动将 snake_case 转为 camelCase 查找
    // 所以这里必须用 camelCase 命名
    rpc.exports = {
        // 启用强制决战回合
        enable: function() {
            if (!_hookInstalled) {
                var ok = installHook();
                if (!ok) return {ok: false, msg: 'Hook安装失败'};
            }
            _enabled = true;
            log('success', 'RPC', '强制决战回合已启用');
            return {ok: true, msg: '已启用'};
        },

        // 禁用强制决战回合（恢复原始随机逻辑）
        disable: function() {
            _enabled = false;
            log('info', 'RPC', '强制决战回合已禁用，恢复原始逻辑');
            return {ok: true, msg: '已禁用'};
        },

        // 查询当前状态
        getStatus: function() {
            var flag = readBattleRoundFlag();
            return {
                enabled: _enabled,
                hookInstalled: _hookInstalled,
                currentIsBattleRound: flag,
            };
        },

        // 立即强制写入一次（不依赖Hook触发）
        forceNow: function() {
            var ok = forceBattleRound();
            return {ok: ok, msg: ok ? '已强制写入' : '写入失败'};
        },
    };

    // ==================== 8. 初始化 ====================
    var mod = getGameAssembly();
    if (mod) {
        log('success', '系统', '决战回合修改器已加载');
        log('info', '系统', '点击UI按钮启用/禁用强制决战回合');
        log('info', '系统', 'StartGenerateSupplyBox RVA: 0x' + RVA.StartGenerateSupplyBox.toString(16));
        log('info', '系统', 'TypeInfo RVA: 0x' + RVA.Mode_Nano4_Terminator_TypeInfo.toString(16));

        // 预安装Hook（但不启用），避免首次回合触发时延迟
        installHook();
    }

})();
