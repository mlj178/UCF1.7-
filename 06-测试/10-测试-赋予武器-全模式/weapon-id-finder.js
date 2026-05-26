// ============================================================
// weapon-id-finder.js - 武器ID查找工具
//
// 功能：
//   1. Hook GiveWeapon 方法，记录武器ID
//   2. 遍历武器字典，列出所有武器
//   3. 测试武器ID范围，获取有效武器
//
// 使用方法：
//   1. 在游戏中正常选择武器
//   2. 脚本会自动记录武器ID
//   3. 使用 RPC 接口查询武器信息
// ============================================================

(function() {
    'use strict';

    // ==================== 1. 日志系统 ====================
    var MAX_LOGS_PER_MODULE = 100;
    var moduleLogCounts = {};
    var weaponLog = [];

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
        GameManager_TypeInfo: 0x0E2933C,
        GiveWeapon: 0xAFB390,
        GetWpnName: 0xAFB1F0,
        GetWpnData: 0xAFB130,
    };

    // ==================== 4. 字段偏移常量 ====================
    var OFF = {
        Klass_staticFields: 0x5C,
        GM_WpnDictionary: 0x18,
        GM_WpnDataDictionary: 0x1C,
        WD_wpnIndex: 0xC,
        WD_weaponName: 0x14,
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

    function readUtf8String(addr, length) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readUtf8String(length);
        } catch(e) {
            return null;
        }
    }

    // ==================== 6. Hook GiveWeapon 方法 ====================
    function hookGiveWeapon() {
        try {
            var mod = getGameAssembly();
            if (!mod) return false;
            var base = mod.base;

            var giveWeaponAddr = base.add(RVA.GiveWeapon);
            
            Interceptor.attach(giveWeaponAddr, {
                onEnter: function(args) {
                    var player = args[0];
                    var weaponIndex = args[1].toInt32();
                    var autoGiveUp = args[2].toInt32();
                    var autoSelect = args[3].toInt32();
                    
                    var timestamp = new Date().toISOString();
                    var logEntry = {
                        time: timestamp,
                        weaponIndex: weaponIndex,
                        autoGiveUp: autoGiveUp,
                        autoSelect: autoSelect
                    };
                    
                    weaponLog.push(logEntry);
                    
                    log('info', 'Hook', 'GiveWeapon 被调用');
                    log('info', 'Hook', '  武器ID: ' + weaponIndex);
                    log('info', 'Hook', '  自动放弃: ' + (autoGiveUp ? '是' : '否'));
                    log('info', 'Hook', '  自动选择: ' + (autoSelect ? '是' : '否'));
                    
                    var weaponName = getWeaponName(weaponIndex);
                    if (weaponName) {
                        log('success', 'Hook', '  武器名称: ' + weaponName);
                    }
                }
            });
            
            log('success', 'Hook', '已 Hook GiveWeapon 方法');
            return true;
            
        } catch(e) {
            log('error', 'Hook', 'Hook GiveWeapon 失败: ' + e.message);
            return false;
        }
    }

    // ==================== 7. 获取武器名称 ====================
    function getWeaponName(weaponIndex) {
        try {
            var mod = getGameAssembly();
            if (!mod) return null;
            var base = mod.base;

            var getWpnNameFunc = new NativeFunction(
                base.add(RVA.GetWpnName),
                'pointer',
                ['int']
            );

            var namePtr = getWpnNameFunc(weaponIndex);
            if (!namePtr || namePtr.isNull()) {
                return null;
            }

            return readUtf8String(namePtr);

        } catch(e) {
            return null;
        }
    }

    // ==================== 8. 批量测试武器ID ====================
    function testWeaponRange(startId, endId) {
        try {
            var results = [];
            
            log('info', 'Test', '开始测试武器ID范围: ' + startId + ' - ' + endId);
            
            for (var i = startId; i <= endId; i++) {
                var name = getWeaponName(i);
                if (name) {
                    results.push({
                        id: i,
                        name: name
                    });
                    log('success', 'Test', 'ID ' + i + ': ' + name);
                }
            }
            
            log('info', 'Test', '测试完成，找到 ' + results.length + ' 个有效武器');
            return results;
            
        } catch(e) {
            log('error', 'Test', '测试异常: ' + e.message);
            return [];
        }
    }

    // ==================== 9. 获取武器日志 ====================
    function getWeaponLog() {
        return weaponLog;
    }

    // ==================== 10. 清空武器日志 ====================
    function clearWeaponLog() {
        weaponLog = [];
        log('info', 'Log', '武器日志已清空');
    }

    // ==================== 11. 遍历武器字典 ====================
    function listWeaponsFromDict() {
        try {
            var mod = getGameAssembly();
            if (!mod) return null;
            var base = mod.base;

            var typeInfoSlot = base.add(RVA.GameManager_TypeInfo);
            var klass = readPtr(typeInfoSlot);
            if (!klass) {
                log('error', 'Dict', '无法获取 GameManager klass');
                return null;
            }

            var staticFields = readPtr(klass.add(OFF.Klass_staticFields));
            if (!staticFields) {
                log('error', 'Dict', '无法获取 GameManager 静态字段');
                return null;
            }

            var wpnDict = readPtr(staticFields.add(OFF.GM_WpnDictionary));
            if (!wpnDict) {
                log('error', 'Dict', 'WpnDictionary 为空');
                return null;
            }

            log('info', 'Dict', '武器字典地址: ' + wpnDict);
            log('info', 'Dict', '提示: 需要进一步分析字典结构');
            
            return wpnDict.toString();

        } catch(e) {
            log('error', 'Dict', '遍历武器字典异常: ' + e.message);
            return null;
        }
    }

    // ==================== 12. RPC接口导出 ====================
    rpc.exports = {
        hook_give_weapon: hookGiveWeapon,
        get_weapon_name: getWeaponName,
        test_weapon_range: testWeaponRange,
        get_weapon_log: getWeaponLog,
        clear_weapon_log: clearWeaponLog,
        list_weapons_from_dict: listWeaponsFromDict,
    };

    // ==================== 13. 初始化完成 ====================
    log('success', '系统', '武器ID查找工具已加载');
    log('info', '系统', '可用命令:');
    log('info', '系统', '  - hook_give_weapon()         Hook GiveWeapon 方法');
    log('info', '系统', '  - get_weapon_name(id)        获取武器名称');
    log('info', '系统', '  - test_weapon_range(start, end)  批量测试武器ID');
    log('info', '系统', '  - get_weapon_log()           获取武器日志');
    log('info', '系统', '  - clear_weapon_log()         清空武器日志');
    log('info', '系统', '  - list_weapons_from_dict()   遍历武器字典');
    log('info', '系统', '');
    log('info', '系统', '使用方法:');
    log('info', '系统', '  1. 调用 hook_give_weapon() 开始监听');
    log('info', '系统', '  2. 在游戏中正常选择武器');
    log('info', '系统', '  3. 调用 get_weapon_log() 查看记录的武器ID');
    log('info', '系统', '  4. 或使用 test_weapon_range(1, 100) 批量测试');

})();
