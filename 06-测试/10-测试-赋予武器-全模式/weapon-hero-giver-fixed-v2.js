// ============================================================
// weapon-hero-giver-fixed-v2.js - 武器赋予脚本（修复版）
//
// 修复：使用有效的 MethodInfo 指针，而不是 ptr(0)
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
        GameManager_TypeInfo: 0x0E2933C,
        GiveWeapon: 0xAFB390,
        GetWpnName: 0xAFB1F0,
    };

    // ==================== 4. 字段偏移常量 ====================
    var OFF = {
        Klass_staticFields: 0x5C,
        GM_myPlayer: 0x00,
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

    // ==================== 6. NativeFunction 缓存 ====================
    var _giveWeaponFunc = null;
    var _getWpnNameFunc = null;
    var _giveWeaponMethodInfo = null;
    var _il2cpp_runtime_invoke = null;
    var _initialized = false;

    // ==================== 7. 获取 MethodInfo（关键修复）====================
    function getGameManagerKlass() {
        try {
            var mod = getGameAssembly();
            if (!mod) return null;
            
            var typeInfoSlot = mod.base.add(RVA.GameManager_TypeInfo);
            return readPtr(typeInfoSlot);
        } catch(e) {
            log('error', 'MethodInfo', '获取GameManager klass失败: ' + e.message);
            return null;
        }
    }

    function getGiveWeaponMethodInfo() {
        if (_giveWeaponMethodInfo) return _giveWeaponMethodInfo;
        
        var mod = getGameAssembly();
        if (!mod) return null;
        
        var klass = getGameManagerKlass();
        if (!klass) {
            log('error', 'MethodInfo', '无法获取GameManager klass');
            return null;
        }
        
        try {
            // 使用 IL2CPP API 获取 MethodInfo
            var exportAddr = mod.getExportByName('il2cpp_class_get_method_from_name');
            if (!exportAddr) {
                log('error', 'MethodInfo', '未找到il2cpp_class_get_method_from_name导出');
                return null;
            }
            
            var getClassMethod = new NativeFunction(exportAddr, 'pointer', ['pointer', 'pointer', 'uint32']);
            var methodName = Memory.allocUtf8String('GiveWeapon');
            var methodInfo = getClassMethod(klass, methodName, 4);
            
            if (methodInfo && !methodInfo.isNull()) {
                _giveWeaponMethodInfo = methodInfo;
                log('success', 'MethodInfo', '✅ 成功获取GiveWeapon MethodInfo: ' + methodInfo);
                return methodInfo;
            }
            
            log('error', 'MethodInfo', 'il2cpp_class_get_method_from_name返回null');
            return null;
            
        } catch(e) {
            log('error', 'MethodInfo', '获取MethodInfo失败: ' + e.message);
            return null;
        }
    }

    // ==================== 8. 初始化 NativeFunction ====================
    function initNativeFunctions() {
        if (_initialized) return true;
        
        var mod = getGameAssembly();
        if (!mod) {
            log('error', 'Init', '无法获取 GameAssembly.dll');
            return false;
        }
        var base = mod.base;
        
        try {
            var exportInvoke = mod.getExportByName('il2cpp_runtime_invoke');
            if (!exportInvoke) {
                log('error', 'Init', '未找到 il2cpp_runtime_invoke');
                return false;
            }
            _il2cpp_runtime_invoke = new NativeFunction(
                exportInvoke,
                'pointer',
                ['pointer', 'pointer', 'pointer', 'pointer']
            );
            log('success', 'Init', 'il2cpp_runtime_invoke 初始化成功');
        } catch(e) {
            log('error', 'Init', 'il2cpp_runtime_invoke 初始化失败: ' + e.message);
            return false;
        }
        
        try {
            _giveWeaponFunc = new NativeFunction(
                base.add(RVA.GiveWeapon),
                'pointer',
                ['pointer', 'int', 'int', 'int', 'pointer']
            );
            log('success', 'Init', 'GiveWeapon NativeFunction 初始化成功');
        } catch(e) {
            log('error', 'Init', 'GiveWeapon NativeFunction 初始化失败: ' + e.message);
            return false;
        }
        
        try {
            _getWpnNameFunc = new NativeFunction(
                base.add(RVA.GetWpnName),
                'pointer',
                ['int', 'pointer']
            );
            log('success', 'Init', 'GetWpnName NativeFunction 初始化成功');
        } catch(e) {
            log('error', 'Init', 'GetWpnName NativeFunction 初始化失败: ' + e.message);
            return false;
        }
        
        _initialized = true;
        return true;
    }

    // ==================== 9. 核心功能 ====================
    function getMyPlayer() {
        try {
            var mod = getGameAssembly();
            if (!mod) return null;
            var base = mod.base;

            var typeInfoSlot = base.add(RVA.GameManager_TypeInfo);
            var klass = readPtr(typeInfoSlot);
            if (!klass) {
                log('error', 'Player', '无法获取 GameManager klass');
                return null;
            }

            var staticFields = readPtr(klass.add(OFF.Klass_staticFields));
            if (!staticFields) {
                log('error', 'Player', '无法获取 GameManager 静态字段');
                return null;
            }

            var myPlayer = readPtr(staticFields.add(OFF.GM_myPlayer));
            if (!myPlayer) {
                log('error', 'Player', 'myPlayer 为空（可能未进入游戏）');
                return null;
            }

            return myPlayer;

        } catch(e) {
            log('error', 'Player', '异常: ' + e.message);
            return null;
        }
    }

    function checkGameManagerInit() {
        try {
            var mod = getGameAssembly();
            if (!mod) return false;
            
            var typeInfoSlot = mod.base.add(RVA.GameManager_TypeInfo);
            var klass = readPtr(typeInfoSlot);
            if (!klass) {
                log('error', 'Init', 'GameManager klass 未初始化');
                return false;
            }
            
            var staticFields = readPtr(klass.add(OFF.Klass_staticFields));
            if (!staticFields) {
                log('error', 'Init', 'GameManager 静态字段未初始化');
                return false;
            }
            
            return true;
            
        } catch(e) {
            log('error', 'Init', '检查GameManager初始化失败: ' + e.message);
            return false;
        }
    }

    function giveWeapon(weaponIndex, autoGiveUp, autoSelect) {
        try {
            log('info', 'Weapon', '=== 开始赋予武器 ===');
            
            var wpnId = parseInt(weaponIndex) || 0;
            var giveUpInt = (autoGiveUp === true || autoGiveUp === 1 || autoGiveUp === 'true') ? 1 : 0;
            var selectInt = (autoSelect === true || autoSelect === 1 || autoSelect === 'true') ? 1 : 0;
            
            log('info', 'Weapon', '参数: weaponIndex=' + wpnId + ', autoGiveUp=' + giveUpInt + ', autoSelect=' + selectInt);
            
            if (!initNativeFunctions()) {
                log('error', 'Weapon', 'NativeFunction 初始化失败');
                return false;
            }

            if (!checkGameManagerInit()) {
                log('error', 'Weapon', '❌ GameManager 未初始化！');
                log('error', 'Weapon', '可能的原因：');
                log('error', 'Weapon', '  1. 游戏未完全加载');
                log('error', 'Weapon', '  2. 未进入游戏场景');
                log('error', 'Weapon', '  3. GameManager 单例未创建');
                log('error', 'Weapon', '');
                log('error', 'Weapon', '请确保：');
                log('error', 'Weapon', '  - 已进入游戏房间');
                log('error', 'Weapon', '  - 游戏已完全加载');
                return false;
            }

            var myPlayer = getMyPlayer();
            if (!myPlayer) {
                log('error', 'Weapon', '无法获取玩家实例（可能未进入游戏）');
                return false;
            }
            log('success', 'Weapon', '成功获取玩家实例: ' + myPlayer);

            var methodInfo = getGiveWeaponMethodInfo();
            if (!methodInfo) {
                log('error', 'Weapon', '❌ 无法获取 MethodInfo');
                return false;
            }
            
            log('success', 'Weapon', '✅ 成功获取 MethodInfo: ' + methodInfo);

            log('info', 'Weapon', '正在准备参数...');
            
            var params = Memory.alloc(Process.pointerSize * 4);
            params.writePointer(myPlayer);
            params.add(Process.pointerSize).writeU32(wpnId);
            params.add(Process.pointerSize * 2).writeU32(giveUpInt);
            params.add(Process.pointerSize * 3).writeU32(selectInt);
            
            log('info', 'Weapon', '参数数组: ' + params);
            log('info', 'Weapon', '正在调用 il2cpp_runtime_invoke...');
            
            var exc = Memory.alloc(Process.pointerSize);
            exc.writePointer(ptr(0));
            
            var weapon = _il2cpp_runtime_invoke(methodInfo, ptr(0), params, exc);
            
            var excVal = exc.readPointer();
            if (!excVal.isNull()) {
                log('error', 'Weapon', '❌ IL2CPP 异常发生！');
                return false;
            }

            log('info', 'Weapon', '调用完成，返回值: ' + weapon);

            if (weapon && !weapon.isNull()) {
                log('success', 'Weapon', '✅ 成功赋予武器!');
                return true;
            } else {
                log('error', 'Weapon', '❌ 赋予武器失败');
                log('error', 'Weapon', '可能的原因：');
                log('error', 'Weapon', '  1. 武器ID不存在');
                log('error', 'Weapon', '  2. 游戏状态不允许');
                log('error', 'Weapon', '  3. GameManager 武器字典未加载');
                return false;
            }

        } catch(e) {
            log('error', 'Weapon', '❌ 异常: ' + e.message);
            log('error', 'Weapon', '异常堆栈: ' + e.stack);
            return false;
        }
    }

    function getWeaponName(weaponIndex) {
        try {
            var wpnId = parseInt(weaponIndex) || 0;
            
            if (!initNativeFunctions()) {
                return null;
            }

            var namePtr = _getWpnNameFunc(wpnId, ptr(0));
            if (!namePtr || namePtr.isNull()) {
                return null;
            }

            try {
                return namePtr.readUtf8String();
            } catch(e) {
                return null;
            }

        } catch(e) {
            log('error', 'Weapon', '获取武器名称异常: ' + e.message);
            return null;
        }
    }

    // ==================== 10. RPC接口导出 ====================
    rpc.exports = {
        giveweapon: giveWeapon,
        getmyplayer: getMyPlayer,
        getweaponname: getWeaponName,
    };

    // ==================== 11. 初始化完成 ====================
    log('success', '系统', '武器赋予脚本已加载（修复版：使用有效MethodInfo）');
    log('info', '系统', '游戏进程: UnityCrossFire.exe');
    log('info', '系统', '');
    log('warn', '系统', '重要修复：');
    log('warn', '系统', '  - 使用有效的 MethodInfo 指针，而不是 ptr(0)');
    log('warn', '系统', '  - 这解决了 "access violation accessing 0x8" 错误');

})();
