// ============================================================
// AAAAA-debug_isMyPlayer_isMyWeapon.js - 调试脚本
//
// 功能：调试 get_isMyPlayer 和 get_isMyWeapon 方法
// 目的：验证这两个方法的返回值，分析为什么都返回0
//
// 输出内容：
//   1. 所有Player的地址
//   2. 每个Player调用get_isMyPlayer的返回值
//   3. 每个Player的当前武器地址
//   4. 每个武器调用get_isMyWeapon的返回值
//   5. GameManager.myPlayer地址
//   6. Weapon.owner字段值
//
// 使用方法：
//   方式1（推荐）：frida -n UnityCrossFire.exe -l AAAAA-debug_isMyPlayer_isMyWeapon.js
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
        GameManager_TypeInfo:             0x0E2933C,
        RuntimeClassInit:                0x108970,
        Player_get_isMyPlayer:           0xB55FD0,
        Weapon_get_isMyWeapon:           0xB6E1D0,
    };

    // ==================== 4. 字段偏移常量 ====================
    var OFF = {
        GM_allPlayers:      0x1C,
        GM_playersBL:       0x20,
        GM_playersGR:       0x28,
        GM_myPlayer:        0x00,

        P_wpns:             0xA0,
        PW_inUse:           0x18,
        PW_owner:           0x08,
        W_owner:            0x30,

        Arr_len:            0x0C,
        Arr_data:           0x10,
        List_items:         0x08,
        List_size:          0x0C,
        Klass_staticFields: 0x5C,
        Klass_parent:       0x2C,
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

    // ==================== 6. NativeFunction封装 ====================
    var _nativeFuncs = {};
    var _initialized = false;

    function initNativeFunctions() {
        if (_initialized) return true;
        
        var mod = getGameAssembly();
        if (!mod) return false;
        var base = mod.base;

        try {
            _nativeFuncs.classInit = new NativeFunction(
                base.add(RVA.RuntimeClassInit),
                'void',
                ['pointer']
            );
        } catch(e) {
            log('error', '初始化', 'classInit创建失败: ' + e.message);
            return false;
        }

        try {
            _nativeFuncs.isMyPlayer = new NativeFunction(
                base.add(RVA.Player_get_isMyPlayer),
                'bool',
                ['pointer', 'pointer']
            );
        } catch(e) {
            log('error', '初始化', 'isMyPlayer创建失败: ' + e.message);
            return false;
        }

        try {
            _nativeFuncs.isMyWeapon = new NativeFunction(
                base.add(RVA.Weapon_get_isMyWeapon),
                'bool',
                ['pointer', 'pointer']
            );
        } catch(e) {
            log('error', '初始化', 'isMyWeapon创建失败: ' + e.message);
            return false;
        }

        _initialized = true;
        log('success', '初始化', 'NativeFunction全部就绪');
        return true;
    }

    // ==================== 7. 获取GameManager实例 ====================
    function getGameManager() {
        if (!_initialized) {
            if (!initNativeFunctions()) return null;
        }

        try {
            var mod = getGameAssembly();
            if (!mod) return null;

            var gmKlass = readPtr(mod.base.add(RVA.GameManager_TypeInfo));
            if (!gmKlass) {
                log('error', 'GM', '无法获取 GameManager klass');
                return null;
            }

            var singletonDefKlass = readPtr(gmKlass.add(OFF.Klass_parent));
            if (!singletonDefKlass) {
                log('error', 'GM', 'parent klass 为 null');
                return null;
            }

            var genericClass = readPtr(singletonDefKlass.add(0x30));
            if (!genericClass) {
                log('error', 'GM', 'generic_class 为 null');
                return null;
            }

            var inflatedKlass = readPtr(genericClass.add(0x00));
            if (!inflatedKlass) {
                log('error', 'GM', 'inflated klass 为 null');
                return null;
            }

            try {
                _nativeFuncs.classInit(inflatedKlass);
            } catch(e) {}

            var sf = readPtr(inflatedKlass.add(OFF.Klass_staticFields));
            if (!sf) {
                log('error', 'GM', 'inflated klass static_fields 为 null');
                return null;
            }

            var instance = readPtr(sf);
            if (!instance) {
                log('error', 'GM', 'GameManager 实例为 null（请确认已进入对局）');
                return null;
            }
            return instance;
        } catch(e) {
            log('error', 'GM', '获取GameManager失败: ' + e.message);
            return null;
        }
    }

    // ==================== 8. 获取GameManager静态字段 ====================
    function getGameManagerStaticFields() {
        var mod = getGameAssembly();
        if (!mod) return null;

        var typeInfoSlot = mod.base.add(RVA.GameManager_TypeInfo);
        var klass = readPtr(typeInfoSlot);
        if (!klass) {
            log('error', 'GM', '无法获取 GameManager klass');
            return null;
        }

        var staticFields = readPtr(klass.add(OFF.Klass_staticFields));
        if (!staticFields) {
            log('error', 'GM', '无法获取 GameManager 静态字段');
            return null;
        }

        return staticFields;
    }

    // ==================== 8. 获取GameManager.myPlayer ====================
    function getMyPlayer() {
        var staticFields = getGameManagerStaticFields();
        if (!staticFields) return null;

        var myPlayer = readPtr(staticFields.add(OFF.GM_myPlayer));
        return myPlayer;
    }

    // ==================== 9. 读取数组 ====================
    function readArray(arrPtr) {
        var result = [];
        if (!arrPtr || arrPtr.isNull()) return result;
        
        var len = readS32(arrPtr.add(OFF.Arr_len));
        if (!len || len <= 0) return result;
        
        for (var i = 0; i < len; i++) {
            var item = readPtr(arrPtr.add(OFF.Arr_data).add(i * 4));
            if (item) result.push(item);
        }
        return result;
    }

    // ==================== 10. 读取List ====================
    function readList(listPtr) {
        var result = [];
        if (!listPtr || listPtr.isNull()) return result;
        
        var items = readPtr(listPtr.add(OFF.List_items));
        if (!items) return result;
        
        var size = readS32(listPtr.add(OFF.List_size));
        if (!size || size <= 0) return result;
        
        for (var i = 0; i < size; i++) {
            var item = readPtr(items.add(OFF.Arr_data).add(i * 4));
            if (item) result.push(item);
        }
        return result;
    }

    // ==================== 11. 获取所有Player ====================
    function getAllPlayers() {
        var gm = getGameManager();
        if (!gm) return [];

        var map = {};
        
        var arr = readArray(readPtr(gm.add(OFF.GM_allPlayers)));
        for (var i = 0; i < arr.length; i++) {
            map[arr[i].toString()] = arr[i];
        }
        
        var bl = readList(readPtr(gm.add(OFF.GM_playersBL)));
        for (var i = 0; i < bl.length; i++) {
            map[bl[i].toString()] = bl[i];
        }
        
        var gr = readList(readPtr(gm.add(OFF.GM_playersGR)));
        for (var i = 0; i < gr.length; i++) {
            map[gr[i].toString()] = gr[i];
        }
        
        return Object.values(map);
    }

    // ==================== 12. 调用get_isMyPlayer ====================
    function call_isMyPlayer(playerPtr) {
        if (!_initialized) {
            if (!initNativeFunctions()) return null;
        }

        try {
            return _nativeFuncs.isMyPlayer(playerPtr, ptr(0));
        } catch(e) {
            log('error', 'isMyPlayer', '调用失败: ' + e.message);
            return null;
        }
    }

    // ==================== 13. 调用get_isMyWeapon ====================
    function call_isMyWeapon(weaponPtr) {
        if (!_initialized) {
            if (!initNativeFunctions()) return null;
        }

        try {
            return _nativeFuncs.isMyWeapon(weaponPtr, ptr(0));
        } catch(e) {
            log('error', 'isMyWeapon', '调用失败: ' + e.message);
            return null;
        }
    }

    // ==================== 14. 主调试函数 ====================
    function debug() {
        log('info', '调试', '========== 开始调试 ==========');
        
        if (!initNativeFunctions()) {
            log('error', '调试', 'NativeFunction初始化失败');
            return;
        }

        var gm = getGameManager();
        if (!gm) {
            log('error', '调试', '无法获取GameManager实例');
            return;
        }
        log('success', 'GM', 'GameManager实例地址: ' + gm);
        
        var myPlayer = getMyPlayer();
        if (myPlayer) {
            log('success', 'GM', 'GameManager.myPlayer: ' + myPlayer);
        } else {
            log('error', 'GM', 'GameManager.myPlayer为null');
        }
        
        var allPlayers = getAllPlayers();
        log('info', 'Player', '找到 ' + allPlayers.length + ' 个Player');
        
        for (var i = 0; i < allPlayers.length; i++) {
            var player = allPlayers[i];
            log('info', 'Player', '----------------------------------------');
            log('info', 'Player', 'Player #' + i + ' 地址: ' + player);
            
            var isMyPlayer = call_isMyPlayer(player);
            log('info', 'Player', '  get_isMyPlayer() 返回: ' + isMyPlayer);
            
            var wpns = readPtr(player.add(OFF.P_wpns));
            if (wpns) {
                log('info', 'Weapon', '  PlayerWeapons地址: ' + wpns);
                
                var inUse = readPtr(wpns.add(OFF.PW_inUse));
                if (inUse) {
                    log('info', 'Weapon', '    当前武器(inUse)地址: ' + inUse);
                    
                    var isMyWeapon = call_isMyWeapon(inUse);
                    log('info', 'Weapon', '    get_isMyWeapon() 返回: ' + isMyWeapon);
                    
                    var owner = readPtr(inUse.add(OFF.W_owner));
                    if (owner) {
                        log('info', 'Weapon', '    Weapon.owner字段: ' + owner);
                    } else {
                        log('error', 'Weapon', '    Weapon.owner字段为null');
                    }
                } else {
                    log('error', 'Weapon', '    当前武器(inUse)为null');
                }
            } else {
                log('error', 'Weapon', '  PlayerWeapons为null');
            }
        }
        
        log('info', '调试', '========== 调试完成 ==========');
    }

    // ==================== 15. RPC导出 ====================
    rpc.exports = {
        debug: debug,
    };

    // ==================== 16. 自动执行 ====================
    setTimeout(function() {
        debug();
    }, 1000);

})();
