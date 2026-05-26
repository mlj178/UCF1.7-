// ============================================================
// weapon-hero-giver-fixed-v2.js - 武器赋予脚本（修复版v5）
//
// 修复历史：
//   v2: 使用有效的 MethodInfo 指针
//   v3: 改用直接原生调用，但缺少 cdecl 声明导致崩溃
//   v4: 修复 ABI 名称 cdecl→mscdecl，但仍然 access violation 0x8
//   v5: 根因修复 - GiveWeapon 必须在游戏主线程执行
//       原因：GiveWeapon 内部调用 Unity API（Instantiate/GetComponent）
//       这些 API 只能在主线程调用，Frida RPC 运行在独立线程
//       方案：Hook ModeBase$$Update（主线程每帧调用），通过任务队列
//       将 GiveWeapon 调度到主线程执行
//
// IDA确认的函数签名：
//   Weapon_o *__cdecl GameManager__GiveWeapon(
//       Player_o *player, int32_t weaponIndex,
//       bool autoGiveUp, bool autoSelect,
//       const MethodInfo *method)
//   void __cdecl ModeBase__Update(
//       ModeBase_o *__this, const MethodInfo *method)
// ============================================================

(function() {
    'use strict';

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

    var RVA = {
        GameManager_TypeInfo: 0x0E2933C,
        ModeBase_TypeInfo: 0x0E2CC54,
        GiveWeapon: 0xAFB390,
        GetWpnName: 0xAFB1F0,
        ModeBase_Update: 0xAF6A00,
    };

    var OFF = {
        Klass_staticFields: 0x5C,
        GM_myPlayer: 0x00,
    };

    function readPtr(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            var v = addr.readPointer();
            return (v && !v.isNull()) ? v : null;
        } catch(e) {
            return null;
        }
    }

    var _giveWeaponFunc = null;
    var _il2cpp_runtime_invoke = null;
    var _giveWeaponMethodInfo = null;
    var _initialized = false;
    var _hookInstalled = false;

    var _pendingTasks = [];
    var _taskResults = {};
    var _taskIdCounter = 0;

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
                ['pointer', 'int', 'int', 'int', 'pointer'],
                'mscdecl'
            );
            log('success', 'Init', 'GiveWeapon NativeFunction 初始化成功 (mscdecl)');
        } catch(e) {
            log('warn', 'Init', 'GiveWeapon 直接调用初始化失败: ' + e.message);
            _giveWeaponFunc = null;
        }

        _initialized = true;
        return true;
    }

    function getMyPlayer() {
        try {
            var mod = getGameAssembly();
            if (!mod) return null;
            var base = mod.base;

            var typeInfoSlot = base.add(RVA.GameManager_TypeInfo);
            var klass = readPtr(typeInfoSlot);
            if (!klass) return null;

            var staticFields = readPtr(klass.add(OFF.Klass_staticFields));
            if (!staticFields) return null;

            var myPlayer = readPtr(staticFields.add(OFF.GM_myPlayer));
            if (!myPlayer) return null;

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
            if (!klass) return false;

            var staticFields = readPtr(klass.add(OFF.Klass_staticFields));
            if (!staticFields) return false;

            return true;

        } catch(e) {
            return false;
        }
    }

    function executeGiveWeaponOnMainThread(wpnId, giveUpInt, selectInt) {
        var myPlayer = getMyPlayer();
        if (!myPlayer) {
            log('error', 'Weapon', '主线程: 无法获取玩家实例');
            return false;
        }
        log('success', 'Weapon', '主线程: 获取玩家实例: ' + myPlayer);

        if (_giveWeaponFunc) {
            try {
                var methodInfo = getGiveWeaponMethodInfo();
                var methodArg = methodInfo ? methodInfo : ptr(0);

                log('info', 'Weapon', '主线程: 直接调用 GiveWeapon(player=' + myPlayer + ', wpnId=' + wpnId + ', giveUp=' + giveUpInt + ', select=' + selectInt + ', method=' + methodArg + ')');

                var weapon = _giveWeaponFunc(myPlayer, wpnId, giveUpInt, selectInt, methodArg);

                if (weapon && !weapon.isNull()) {
                    log('success', 'Weapon', '✅ 主线程直接调用成功! weapon=' + weapon);
                    return true;
                } else {
                    log('error', 'Weapon', '❌ 主线程直接调用返回null');
                    return false;
                }
            } catch(e) {
                log('error', 'Weapon', '❌ 主线程直接调用异常: ' + e.message);
            }
        }

        if (_il2cpp_runtime_invoke) {
            try {
                var methodInfo = getGiveWeaponMethodInfo();
                if (!methodInfo) {
                    log('error', 'Weapon', '主线程: 无法获取MethodInfo');
                    return false;
                }

                var playerBuf = Memory.alloc(Process.pointerSize);
                playerBuf.writePointer(myPlayer);

                var wpnIdBuf = Memory.alloc(4);
                wpnIdBuf.writeS32(wpnId);

                var giveUpBuf = Memory.alloc(4);
                giveUpBuf.writeU8(giveUpInt);

                var selectBuf = Memory.alloc(4);
                selectBuf.writeU8(selectInt);

                var params = Memory.alloc(Process.pointerSize * 4);
                params.writePointer(playerBuf);
                params.add(Process.pointerSize).writePointer(wpnIdBuf);
                params.add(Process.pointerSize * 2).writePointer(giveUpBuf);
                params.add(Process.pointerSize * 3).writePointer(selectBuf);

                var exc = Memory.alloc(Process.pointerSize);
                exc.writePointer(ptr(0));

                log('info', 'Weapon', '主线程: il2cpp_runtime_invoke 调用中...');

                var weapon = _il2cpp_runtime_invoke(methodInfo, ptr(0), params, exc);

                var excVal = exc.readPointer();
                if (!excVal.isNull()) {
                    log('error', 'Weapon', '❌ 主线程 IL2CPP 异常! exc=' + excVal);
                    try {
                        var excMsg = readPtr(excVal.add(0x0C));
                        if (excMsg) {
                            var msgLen = excMsg.add(0x08).readS32();
                            var msgStr = excMsg.add(0x0C).readUtf16String(msgLen);
                            log('error', 'Weapon', '异常消息: ' + msgStr);
                        }
                    } catch(e2) {}
                    return false;
                }

                if (weapon && !weapon.isNull()) {
                    log('success', 'Weapon', '✅ 主线程 invoke 成功! weapon=' + weapon);
                    return true;
                } else {
                    log('error', 'Weapon', '❌ 主线程 invoke 返回null');
                    return false;
                }
            } catch(e) {
                log('error', 'Weapon', '❌ 主线程 invoke 异常: ' + e.message);
                return false;
            }
        }

        log('error', 'Weapon', '无可用的调用方式');
        return false;
    }

    function installMainThreadHook() {
        if (_hookInstalled) return true;

        var mod = getGameAssembly();
        if (!mod) {
            log('error', 'Hook', '无法获取 GameAssembly.dll');
            return false;
        }

        var updateAddr = mod.base.add(RVA.ModeBase_Update);

        try {
            Interceptor.attach(updateAddr, {
                onEnter: function(args) {
                    while (_pendingTasks.length > 0) {
                        var task = _pendingTasks.shift();
                        log('info', 'Hook', '主线程拾取任务: taskId=' + task.id + ', wpnId=' + task.wpnId);

                        var result = executeGiveWeaponOnMainThread(task.wpnId, task.giveUp, task.select);
                        _taskResults[task.id] = result;

                        send({
                            type: 'giveWeaponResult',
                            taskId: task.id,
                            success: result
                        });
                    }
                }
            });

            _hookInstalled = true;
            log('success', 'Hook', '✅ ModeBase$$Update Hook 安装成功（主线程调度）');
            return true;

        } catch(e) {
            log('error', 'Hook', 'Hook 安装失败: ' + e.message);
            return false;
        }
    }

    function giveWeapon(weaponIndex, autoGiveUp, autoSelect) {
        try {
            log('info', 'Weapon', '=== 开始赋予武器（主线程调度）===');

            var wpnId = parseInt(weaponIndex) || 0;
            var giveUpInt = (autoGiveUp === true || autoGiveUp === 1 || autoGiveUp === 'true') ? 1 : 0;
            var selectInt = (autoSelect === true || autoSelect === 1 || autoSelect === 'true') ? 1 : 0;

            log('info', 'Weapon', '参数: weaponIndex=' + wpnId + ', autoGiveUp=' + giveUpInt + ', autoSelect=' + selectInt);

            if (!initNativeFunctions()) {
                log('error', 'Weapon', 'NativeFunction 初始化失败');
                return false;
            }

            if (!checkGameManagerInit()) {
                log('error', 'Weapon', '❌ GameManager 未初始化！请确保已进入游戏房间');
                return false;
            }

            if (!installMainThreadHook()) {
                log('error', 'Weapon', '主线程 Hook 安装失败');
                return false;
            }

            var taskId = ++_taskIdCounter;
            _pendingTasks.push({
                id: taskId,
                wpnId: wpnId,
                giveUp: giveUpInt,
                select: selectInt
            });

            log('info', 'Weapon', '任务已入队: taskId=' + taskId + ', 等待主线程执行...');
            log('info', 'Weapon', '当前线程: ' + Process.getCurrentThreadId() + '（非游戏主线程）');

            return 'pending:' + taskId;

        } catch(e) {
            log('error', 'Weapon', '❌ 异常: ' + e.message);
            log('error', 'Weapon', '异常堆栈: ' + e.stack);
            return false;
        }
    }

    function getWeaponName(weaponIndex) {
        return null;
    }

    rpc.exports = {
        giveweapon: giveWeapon,
        getmyplayer: getMyPlayer,
        getweaponname: getWeaponName,
    };

    log('success', '系统', '武器赋予脚本已加载（修复版v5：主线程调度）');
    log('info', '系统', '游戏进程: UnityCrossFire.exe');
    log('info', '系统', '');
    log('warn', '系统', 'v5修复说明：');
    log('warn', '系统', '  1. 根因：GiveWeapon内部调用Unity API（Instantiate/GetComponent）');
    log('warn', '系统', '     这些API只能在游戏主线程调用');
    log('warn', '系统', '  2. Frida RPC运行在独立线程，直接调用会触发access violation');
    log('warn', '系统', '  3. 方案：Hook ModeBase$$Update（主线程每帧执行）');
    log('warn', '系统', '     RPC请求入队 → 主线程Update回调拾取并执行GiveWeapon');
    log('warn', '系统', '  4. 结果通过send()消息返回给Python端');

})();
