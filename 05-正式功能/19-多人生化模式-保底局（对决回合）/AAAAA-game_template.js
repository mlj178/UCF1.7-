// ============================================================
// AAAAA-game_template.js - 游戏功能修改模板
//
// 功能：通过 GameManager → myPlayer → clientData → nickname 链式访问
// 特点：
//   - 同步查找GameAssembly.dll（Frida注入时游戏已运行）
//   - 完整的安全检查（指针验证、异常处理）
//   - 分级日志系统（带模块计数限制，防止日志洪泛）
//   - RPC接口导出（rpc.exports本身保持脚本活跃）
//   - 链式访问模式（不使用Hook）
//
// 使用方法：
//   1. 修改RVA地址常量（根据游戏版本）
//   2. 修改字段偏移常量（根据dump.cs）
//   3. 添加自定义功能函数
//   4. 导出RPC接口
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

    // ==================== 2. 模块查找（同步） ====================
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
        GameManager_TypeInfo: 0x0E2933C,
    };

    // ==================== 4. 字段偏移常量 ====================
    var OFF = {
        Klass_staticFields: 0x5C,
        String_length: 0x08,
        String_data: 0x0C,

        GM_myPlayer: 0x00,
        P_clientData: 0x94,
        CD_nickName: 0x10,
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

    function readS32(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readS32();
        } catch(e) {
            return null;
        }
    }

    function readUtf16String(addr, length) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readUtf16String(length);
        } catch(e) {
            return null;
        }
    }

    function readFloat(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readFloat();
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

    function getNickname() {
        try {
            var mod = getGameAssembly();
            if (!mod) return null;
            var base = mod.base;

            var typeInfoSlot = base.add(RVA.GameManager_TypeInfo);
            var klass = readPtr(typeInfoSlot);
            if (!klass) {
                log('error', 'Nickname', '无法获取 GameManager klass');
                return null;
            }

            var staticFields = readPtr(klass.add(OFF.Klass_staticFields));
            if (!staticFields) {
                log('error', 'Nickname', '无法获取 GameManager 静态字段');
                return null;
            }

            var myPlayer = readPtr(staticFields.add(OFF.GM_myPlayer));
            if (!myPlayer) {
                log('error', 'Nickname', 'myPlayer 为空（可能未进入游戏）');
                return null;
            }

            var clientData = readPtr(myPlayer.add(OFF.P_clientData));
            if (!clientData) {
                log('error', 'Nickname', 'clientData 为空');
                return null;
            }

            var nickNameObj = readPtr(clientData.add(OFF.CD_nickName));
            if (!nickNameObj) {
                log('error', 'Nickname', 'nickName 对象为空');
                return null;
            }

            var len = readS32(nickNameObj.add(OFF.String_length));
            if (len === null || len < 0 || len > 500) {
                log('error', 'Nickname', '字符串长度异常: ' + len);
                return null;
            }

            var nickname = readUtf16String(nickNameObj.add(OFF.String_data), len * 2);
            if (!nickname) {
                log('error', 'Nickname', '读取字符串内容失败');
                return null;
            }

            log('success', 'Nickname', '玩家昵称: "' + nickname + '"');
            return nickname;

        } catch(e) {
            log('error', 'Nickname', '异常: ' + e.message);
            return null;
        }
    }

    function getPlayerInstances() {
        try {
            var mod = getGameAssembly();
            if (!mod) return null;
            var base = mod.base;

            var typeInfoSlot = base.add(RVA.GameManager_TypeInfo);
            var klass = readPtr(typeInfoSlot);
            if (!klass) {
                log('error', 'Instance', '无法获取 GameManager klass');
                return null;
            }

            var staticFields = readPtr(klass.add(OFF.Klass_staticFields));
            if (!staticFields) {
                log('error', 'Instance', '无法获取 GameManager 静态字段');
                return null;
            }

            var myPlayer = readPtr(staticFields.add(OFF.GM_myPlayer));
            if (!myPlayer) {
                log('error', 'Instance', 'myPlayer 为空');
                return null;
            }

            var clientData = readPtr(myPlayer.add(OFF.P_clientData));

            var result = {
                myPlayer: myPlayer.toString(),
                clientData: clientData ? clientData.toString() : null,
            };

            log('success', 'Instance', 'myPlayer: ' + result.myPlayer);
            log('success', 'Instance', 'clientData: ' + result.clientData);

            return result;

        } catch(e) {
            log('error', 'Instance', '异常: ' + e.message);
            return null;
        }
    }

    // ==================== 7. RPC接口导出 ====================
    rpc.exports = {
        getNickname: getNickname,
        get_nickname: getNickname,
        getPlayerInstances: getPlayerInstances,
        get_player_instances: getPlayerInstances,
    };

    // ==================== 8. 初始化完成 ====================
    log('success', '系统', '模板已加载');
    log('info', '系统', '可用命令:');
    log('info', '系统', '  - get_nickname()         获取玩家昵称');
    log('info', '系统', '  - get_player_instances()  获取玩家实例地址');
    log('info', '系统', '');
    log('info', '系统', '提示：请根据游戏版本更新RVA地址和字段偏移');

})();
