// ============================================================
// Unity时间加速 - Frida脚本（32位Windows IL2CPP）
//
// 原理（基于IDA反汇编验证）：
//   GameAssembly.dll中的get_timeScale是延迟解析桩：
//     cmp dword_10E64BDC, 0      ; 检查icall是否已解析
//     jnz short loc_xxx           ; 已解析则跳转
//     push offset "UnityEngine.Time::get_timeScale()"
//     call il2cpp_resolve_icall   ; 解析icall
//     add esp, 4                  ; cdecl清理栈
//     mov dword_10E64BDC, eax     ; 保存函数指针
//     jmp dword_10E64BDC          ; 跳转到引擎DLL中的真正实现
//
//   因此：
//   1. il2cpp_resolve_icall("UnityEngine.Time::get_timeScale()") 返回的是
//      引擎DLL（UnityPlayer.dll等）中的真正函数地址
//   2. 该引擎函数内部才有 fld dword ptr [addr] 模式，addr就是timeScale全局变量
//   3. dump.cs确认：Time类只有get_timeScale，没有set_timeScale
//   4. 所以必须通过分析引擎函数机器码定位变量地址，直接写内存
//
// 32位Windows注意事项：
//   - il2cpp_resolve_icall是cdecl导出，Frida默认stdcall会崩溃
//   - 引擎函数也是cdecl（float __cdecl返回值在FPU栈）
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

    // ==================== 3. 安全读写 ====================
    function readFloat(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readFloat();
        } catch(e) { return null; }
    }

    function writeFloat(addr, value) {
        try {
            if (!addr || addr.isNull()) return false;
            addr.writeFloat(value);
            return true;
        } catch(e) { return false; }
    }

    // ==================== 4. 核心逻辑 ====================

    var _timeScaleVarAddr = null;   // timeScale全局变量内存地址
    var _getTimeScaleFunc = null;   // NativeFunction包装的get_timeScale（引擎函数）
    var _locked = false;
    var _desiredScale = 1.0;
    var _refreshTimer = null;
    var _initialized = false;
    var _initError = null;

    // 分析引擎函数机器码，提取timeScale变量地址
    // 实际引擎函数字节码（32位x86，UnityPlayer.dll）：
    //   e8 bb d9 c9 ff          ; call GetTimeManager() → eax = 结构体指针
    //   d9 80 ec 00 00 00       ; fld dword ptr [eax+0xEC] → 读取timeScale
    //   c3                      ; ret
    // 模式: 先call获取对象指针(eax)，再从[eax+offset]读取float
    // 需要调用helper函数获取结构体指针，再+偏移得到变量地址
    function extractTimeScaleInfo(engineFuncAddr) {
        try {
            var bytes = engineFuncAddr.readByteArray(256);
            if (!bytes) {
                log('error', 'TimeScale', '无法读取引擎函数字节');
                return null;
            }

            var view = new DataView(bytes);

            // 输出前64字节供调试
            var hex = '';
            for (var i = 0; i < 64 && i < view.byteLength; i++) {
                hex += ('0' + view.getUint8(i).toString(16)).slice(-2) + ' ';
            }
            log('info', 'TimeScale', '引擎函数前64字节: ' + hex);

            // 确认所在模块
            var funcModule = Process.findModuleByAddress(engineFuncAddr);
            if (funcModule) {
                log('info', 'TimeScale', '引擎函数所在模块: ' + funcModule.name + ' 基址: ' + funcModule.base);
            }

            // 模式1: call helper; fld dword ptr [eax+disp32]; ret
            //   e8 xx xx xx xx          ; call helper → eax = 对象指针
            //   d9 80 yy yy yy yy       ; fld dword ptr [eax+offset]
            //   c3                      ; ret
            // D9 80 = fld dword ptr [eax+disp32], disp32在后面4字节
            if (view.getUint8(0) === 0xE8 && view.getUint8(5) === 0xD9 && view.getUint8(6) === 0x80) {
                var rel32 = view.getInt32(1, true);
                var helperAddr = engineFuncAddr.add(5 + rel32);
                var offset = view.getUint32(7, true);
                log('info', 'TimeScale', '匹配 call+fld[eax+disp32] 模式');
                log('info', 'TimeScale', 'helper函数地址: ' + helperAddr + ', 偏移: 0x' + offset.toString(16));
                return { helperAddr: helperAddr, offset: offset };
            }

            // 模式2: call helper; movss xmm0, [eax+disp32]; ret
            //   e8 xx xx xx xx             ; call helper → eax = 对象指针
            //   f3 0f 10 80 yy yy yy yy    ; movss xmm0, [eax+offset]
            if (view.getUint8(0) === 0xE8 &&
                view.getUint8(5) === 0xF3 && view.getUint8(6) === 0x0F &&
                view.getUint8(7) === 0x10 && view.getUint8(8) === 0x80) {
                var rel32 = view.getInt32(1, true);
                var helperAddr = engineFuncAddr.add(5 + rel32);
                var offset = view.getUint32(9, true);
                log('info', 'TimeScale', '匹配 call+movss[eax+disp32] 模式');
                log('info', 'TimeScale', 'helper函数地址: ' + helperAddr + ', 偏移: 0x' + offset.toString(16));
                return { helperAddr: helperAddr, offset: offset };
            }

            // 模式3: fld dword ptr [imm32] => D9 05 xx xx xx xx (全局变量)
            for (var i = 0; i < 200; i++) {
                if (view.getUint8(i) === 0xD9 && view.getUint8(i + 1) === 0x05) {
                    var addr = view.getUint32(i + 2, true);
                    log('info', 'TimeScale', '匹配 fld dword ptr [imm32] 偏移+' + i + ', 地址: 0x' + addr.toString(16));
                    return { globalAddr: ptr(addr) };
                }
            }

            // 模式4: movss xmm0, [addr] => F3 0F 10 05 xx xx xx xx (SSE全局变量)
            for (var i = 0; i < 200; i++) {
                if (view.getUint8(i) === 0xF3 && view.getUint8(i + 1) === 0x0F &&
                    view.getUint8(i + 2) === 0x10 && view.getUint8(i + 3) === 0x05) {
                    var addr = view.getUint32(i + 4, true);
                    log('info', 'TimeScale', '匹配 movss xmm0, [imm32] 偏移+' + i + ', 地址: 0x' + addr.toString(16));
                    return { globalAddr: ptr(addr) };
                }
            }

            // 模式5: 函数开头是jmp（跳转桩），跟踪跳转目标
            if (view.getUint8(0) === 0xE9) {
                var rel = view.getInt32(1, true);
                var jumpTarget = engineFuncAddr.add(5 + rel);
                log('info', 'TimeScale', '检测到E9跳转桩，目标: ' + jumpTarget);
                return extractTimeScaleInfo(jumpTarget);
            }

            // 模式6: FF 25 xx xx xx xx = jmp dword ptr [addr] (间接跳转)
            if (view.getUint8(0) === 0xFF && view.getUint8(1) === 0x25) {
                var ptrAddr = view.getUint32(2, true);
                var indirectTarget = ptr(ptrAddr).readPointer();
                log('info', 'TimeScale', '检测到间接跳转FF25，目标: ' + indirectTarget);
                if (indirectTarget && !indirectTarget.isNull()) {
                    return extractTimeScaleInfo(indirectTarget);
                }
            }

            // 输出更多字节供调试
            var hexFull = '';
            for (var i = 0; i < 128 && i < view.byteLength; i++) {
                hexFull += ('0' + view.getUint8(i).toString(16)).slice(-2) + ' ';
            }
            log('error', 'TimeScale', '未匹配已知模式，引擎函数前128字节: ' + hexFull);
            return null;

        } catch(e) {
            log('error', 'TimeScale', '分析引擎函数字节失败: ' + e.message);
            return null;
        }
    }

    // 初始化
    function initTimeScale() {
        if (_initialized) return _initError === null;
        if (_initError) return false;

        try {
            var mod = getGameAssembly();
            if (!mod) { _initError = '找不到GameAssembly.dll'; return false; }

            // 查找 il2cpp_resolve_icall 导出
            var resolveIcall = mod.findExportByName('il2cpp_resolve_icall');
            if (!resolveIcall) {
                _initError = '未找到 il2cpp_resolve_icall 导出';
                log('error', 'TimeScale', _initError);
                return false;
            }
            log('info', 'TimeScale', 'il2cpp_resolve_icall 地址: ' + resolveIcall);

            // 32位Windows: il2cpp_resolve_icall是cdecl导出
            // 依据：IDA反汇编中 call sub_10167DE0 后有 add esp, 4（cdecl清理栈）
            var resolveFunc = new NativeFunction(resolveIcall, 'pointer', ['pointer'], 'mscdecl');

            // 解析 get_timeScale icall
            // 依据：IDA反汇编确认字符串为 "UnityEngine.Time::get_timeScale()"
            var getIcallName = Memory.allocUtf8String('UnityEngine.Time::get_timeScale()');
            var engineFuncAddr = resolveFunc(getIcallName);

            if (!engineFuncAddr || engineFuncAddr.isNull()) {
                _initError = 'il2cpp_resolve_icall 返回NULL，get_timeScale icall不存在';
                log('error', 'TimeScale', _initError);
                return false;
            }

            log('success', 'TimeScale', 'get_timeScale 引擎函数地址: ' + engineFuncAddr);

            // 确认引擎函数所在模块
            var engineModule = Process.findModuleByAddress(engineFuncAddr);
            if (engineModule) {
                log('info', 'TimeScale', '引擎函数所在模块: ' + engineModule.name);
            }

            // 创建NativeFunction调用引擎函数
            // 依据：IDA反汇编 float __cdecl UnityEngine_Time__get_timeScale(const MethodInfo *method)
            // 但icall解析后的引擎函数签名可能不同，先尝试无参数版本
            _getTimeScaleFunc = new NativeFunction(engineFuncAddr, 'float', [], 'mscdecl');

            // 调用一次验证
            var currentVal = null;
            try {
                currentVal = _getTimeScaleFunc();
                log('success', 'TimeScale', 'get_timeScale() 当前值: ' + currentVal);
            } catch(e) {
                log('warn', 'TimeScale', 'get_timeScale() 无参调用失败: ' + e.message + '，尝试带MethodInfo参数');
                // 某些版本需要传MethodInfo*参数（可以为NULL）
                try {
                    _getTimeScaleFunc = new NativeFunction(engineFuncAddr, 'float', ['pointer'], 'mscdecl');
                    currentVal = _getTimeScaleFunc(ptr(0));
                    log('success', 'TimeScale', 'get_timeScale(NULL) 当前值: ' + currentVal);
                } catch(e2) {
                    _initError = 'get_timeScale() 调用失败: ' + e2.message;
                    log('error', 'TimeScale', _initError);
                    return false;
                }
            }

            // 分析引擎函数机器码，提取timeScale变量信息
            var info = extractTimeScaleInfo(engineFuncAddr);
            if (!info) {
                _initError = '无法从引擎函数机器码定位timeScale变量地址';
                log('error', 'TimeScale', _initError);
                return false;
            }

            if (info.globalAddr) {
                // 全局变量模式：直接使用地址
                _timeScaleVarAddr = info.globalAddr;
                log('success', 'TimeScale', 'timeScale全局变量地址: ' + _timeScaleVarAddr);
            } else if (info.helperAddr && info.offset !== undefined) {
                // 结构体成员模式：调用helper获取对象指针，再+偏移
                log('info', 'TimeScale', '调用helper函数获取结构体指针...');
                var helperFunc = new NativeFunction(info.helperAddr, 'pointer', [], 'mscdecl');
                var structPtr = helperFunc();
                if (!structPtr || structPtr.isNull()) {
                    _initError = 'helper函数返回NULL，无法获取结构体指针';
                    log('error', 'TimeScale', _initError);
                    return false;
                }
                log('success', 'TimeScale', '结构体指针: ' + structPtr + ', 偏移: 0x' + info.offset.toString(16));
                _timeScaleVarAddr = structPtr.add(info.offset);
                log('success', 'TimeScale', 'timeScale变量地址: ' + _timeScaleVarAddr);
            } else {
                _initError = 'extractTimeScaleInfo返回无效数据';
                log('error', 'TimeScale', _initError);
                return false;
            }

            // 验证：读取变量值，应该与get_timeScale()返回值一致
            var memVal = readFloat(_timeScaleVarAddr);
            if (memVal === null) {
                _initError = '变量地址不可读: ' + _timeScaleVarAddr;
                log('error', 'TimeScale', _initError);
                return false;
            }

            log('success', 'TimeScale', '内存值: ' + memVal + ', 函数返回值: ' + currentVal);

            // 如果内存值和函数返回值差异大，可能定位错误
            if (currentVal !== null && Math.abs(memVal - currentVal) > 0.01) {
                log('warn', 'TimeScale', '内存值(' + memVal + ')与函数返回值(' + currentVal + ')不一致，可能定位错误');
            }
            _initialized = true;
            log('success', 'TimeScale', '初始化成功！');
            return true;

        } catch(e) {
            _initError = '初始化异常: ' + e.message;
            log('error', 'TimeScale', _initError);
            return false;
        }
    }

    // 设置timeScale（直接写内存）
    function setTimeScale(value) {
        if (!_initialized) {
            if (!initTimeScale()) return false;
        }
        return writeFloat(_timeScaleVarAddr, value);
    }

    // 读取当前timeScale
    function getTimeScale() {
        if (!_initialized) {
            if (!initTimeScale()) return null;
        }
        return readFloat(_timeScaleVarAddr);
    }

    // 定时刷新（防止游戏覆盖timeScale）
    function startRefresh() {
        if (_refreshTimer) return;
        _refreshTimer = setInterval(function() {
            if (_locked && _timeScaleVarAddr) {
                var current = readFloat(_timeScaleVarAddr);
                if (current !== null && Math.abs(current - _desiredScale) > 0.001) {
                    writeFloat(_timeScaleVarAddr, _desiredScale);
                }
            }
        }, 500);
        log('info', 'TimeScale', '定时刷新已启动');
    }

    function stopRefresh() {
        if (_refreshTimer) {
            clearInterval(_refreshTimer);
            _refreshTimer = null;
        }
    }

    // ==================== 5. RPC接口 ====================

    // Frida Python绑定会自动将snake_case转为camelCase：
    //   Python: script.exports.setTimeScale() → JS: rpc.exports.setTimeScale
    // 所以JS端必须用camelCase命名，否则Python找不到方法
    rpc.exports = {

        setTimeScale: function(scale) {
            _desiredScale = scale;
            var ok = setTimeScale(scale);
            if (ok) {
                log('success', 'TimeScale', '时间倍速设为: ' + scale + 'x');
            } else {
                log('error', 'TimeScale', '设置失败，初始化错误: ' + (_initError || '未知'));
            }
            return ok;
        },

        getTimeScale: function() {
            return getTimeScale();
        },

        lockTimeScale: function(scale) {
            _desiredScale = scale;
            _locked = true;
            setTimeScale(scale);
            startRefresh();
            log('success', 'TimeScale', '锁定倍速: ' + scale + 'x');
            return true;
        },

        unlockTimeScale: function() {
            _locked = false;
            stopRefresh();
            setTimeScale(1.0);
            log('info', 'TimeScale', '已恢复正常速度');
            return true;
        },

        getLockStatus: function() {
            return {
                locked: _locked,
                desiredScale: _desiredScale,
                currentScale: getTimeScale()
            };
        }
    };

    // ==================== 6. 初始化 ====================
    log('success', '系统', 'Unity时间加速脚本已加载');

})();
