// time_scale.js - Unity时间加速模块
//
// 原理（基于IDA反汇编验证）：
//   GameAssembly.dll中的get_timeScale是延迟解析桩：
//     cmp dword_10E64BDC, 0      ; 检查icall是否已解析
//     jnz short loc_xxx           ; 已解析则跳转
//     push offset "UnityEngine.Time::get_timeScale()"
//     call il2cpp_resolve_icall   ; 解析icall
//     add esp, 4                  ; mscdecl清理栈
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
//   - il2cpp_resolve_icall是mscdecl导出（实测验证，非cdecl）
//   - 引擎函数也是mscdecl（float __mscdecl返回值在FPU栈）
//
// 安全设计（参照项目中gravity.js的hasGm/tryGetGM模式）：
//   - 结构体成员模式下，TimeManager实例可能在场景切换时被重建
//   - 因此不缓存最终变量地址，而是缓存helperAddr+offset
//   - 每次写操作前重新调用helper获取最新实例指针（类似gravity.js的tryGetGM）
//   - 对实例指针做最低地址校验（参照time_freeze.js的safeModifyTime）

modules.timescale = (function() {
  var enabled = false;
  var currentSpeed = 1.0;
  var _getTimeScaleFunc = null;
  var _initialized = false;
  var _initError = null;

  // 地址解析模式
  var _mode = null;  // 'global' 或 'struct'
  // 全局变量模式
  var _globalAddr = null;
  // 结构体成员模式
  var _helperAddr = null;
  var _offset = 0;
  var _helperFunc = null;
  var _hooks = [];
  var _hookInstalled = false;
  var _activeModeBase = null;
  var _exitingModeBase = null;
  var _roomShuttingDown = false;
  var _pendingSpeed = null;
  var _restorePending = false;
  var _lastApplyAt = 0;
  var _nextRetryAt = 0;
  var _modeReadyAt = 0;
  var REAPPLY_INTERVAL_MS = 1000;
  var MODE_READY_DELAY_MS = 750;

  function resetInitCache() {
    _getTimeScaleFunc = null;
    _initialized = false;
    _initError = null;
    _mode = null;
    _globalAddr = null;
    _helperAddr = null;
    _offset = 0;
    _helperFunc = null;
  }

  function isFiniteNumber(value) {
    return typeof value === 'number' && isFinite(value);
  }

  function normalizeSpeed(speed) {
    speed = Number(speed);
    if (!isFiniteNumber(speed)) return currentSpeed;
    if (speed < 0.1) return 0.1;
    if (speed > 10.0) return 10.0;
    return Math.round(speed * 10) / 10;
  }

  function isPlausibleTimeScale(value) {
    return isFiniteNumber(value) && value >= 0.0 && value <= 100.0;
  }

  function hasMemoryProtection(addr, needWrite) {
    try {
      if (!addr || addr.isNull()) return false;
      if (addr.compare(ptr(0x10000)) < 0) return false;
      var range = Process.findRangeByAddress(addr);
      if (!range) return false;
      if (range.base.add(range.size).compare(addr.add(4)) < 0) return false;
      if (range.protection.indexOf('r') === -1) return false;
      if (needWrite && range.protection.indexOf('w') === -1) return false;
      return true;
    } catch(e) { return false; }
  }

  function isExecutablePtr(addr) {
    try {
      if (!hasMemoryProtection(addr, false)) return false;
      var range = Process.findRangeByAddress(addr);
      return range && range.protection.indexOf('x') !== -1;
    } catch(e) { return false; }
  }

  function isValidTimeScaleAddress(addr) {
    if (!hasMemoryProtection(addr, true)) return false;
    var value = readF32(addr);
    return value !== null && isPlausibleTimeScale(value);
  }

  // 安全写float
  function writeFloat(addr, value) {
    try {
      if (!addr || addr.isNull()) return false;
      if (!isPlausibleTimeScale(value)) return false;
      if (!isValidTimeScaleAddress(addr)) return false;
      addr.writeFloat(value);
      return true;
    } catch(e) { return false; }
  }

  // 验证指针有效性（参照time_freeze.js的safeModifyTime最低地址检查）
  function isValidPtr(p) {
    try {
      if (!p || p.isNull()) return false;
      if (p.compare(ptr(0x10000)) < 0) return false;
      if (!hasMemoryProtection(p, false)) return false;
      return true;
    } catch(e) { return false; }
  }

  // 解析当前timeScale变量地址
  // 结构体成员模式下每次重新调用helper获取最新实例指针（参照gravity.js的tryGetGM）
  function resolveVarAddr() {
    if (_mode === 'global') {
      return _globalAddr;
    }
    if (_mode === 'struct' && _helperFunc) {
      try {
        if (!isExecutablePtr(_helperAddr)) return null;
        var structPtr = _helperFunc();
        if (!isValidPtr(structPtr)) return null;
        return structPtr.add(_offset);
      } catch(e) {
        return null;
      }
    }
    return null;
  }

  // 分析引擎函数机器码，提取timeScale变量地址
  // 实际引擎函数字节码（32位x86，UnityPlayer.dll）：
  //   e8 bb d9 c9 ff          ; call GetTimeManager() → eax = 结构体指针
  //   d9 80 ec 00 00 00       ; fld dword ptr [eax+0xEC] → 读取timeScale
  //   c3                      ; ret
  // 模式: 先call获取对象指针(eax)，再从[eax+offset]读取float
  // 需要调用helper函数获取结构体指针，再+偏移得到变量地址
  function extractTimeScaleInfo(engineFuncAddr, depth) {
    depth = depth || 0;
    if (depth > 4) {
      sendDevLog('error', '时间加速', '跳转桩层级过深，停止解析');
      return null;
    }
    try {
      if (!isExecutablePtr(engineFuncAddr)) {
        sendDevLog('error', '时间加速', '引擎函数地址不可执行: ' + engineFuncAddr);
        return null;
      }
      var bytes = engineFuncAddr.readByteArray(256);
      if (!bytes) {
        sendDevLog('error', '时间加速', '无法读取引擎函数字节');
        return null;
      }

      var view = new DataView(bytes);

      // 输出前64字节供调试
      var hex = '';
      for (var i = 0; i < 64 && i < view.byteLength; i++) {
        hex += ('0' + view.getUint8(i).toString(16)).slice(-2) + ' ';
      }
      sendDevLog('info', '时间加速', '引擎函数前64字节: ' + hex);

      // 确认所在模块
      var funcModule = Process.findModuleByAddress(engineFuncAddr);
      if (funcModule) {
        sendDevLog('info', '时间加速', '引擎函数所在模块: ' + funcModule.name + ' 基址: ' + funcModule.base);
      }

      // 模式1: call helper; fld dword ptr [eax+disp32]; ret
      //   e8 xx xx xx xx          ; call helper → eax = 对象指针
      //   d9 80 yy yy yy yy       ; fld dword ptr [eax+offset]
      //   c3                      ; ret
      if (view.getUint8(0) === 0xE8 && view.getUint8(5) === 0xD9 && view.getUint8(6) === 0x80) {
        var rel32 = view.getInt32(1, true);
        var helperAddr = engineFuncAddr.add(5 + rel32);
        var offset = view.getInt32(7, true);
        if (offset < 0 || offset > 0x4000 || !isExecutablePtr(helperAddr)) return null;
        sendDevLog('info', '时间加速', '匹配 call+fld[eax+disp32] 模式');
        sendDevLog('info', '时间加速', 'helper函数地址: ' + helperAddr + ', 偏移: 0x' + offset.toString(16));
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
        var offset = view.getInt32(9, true);
        if (offset < 0 || offset > 0x4000 || !isExecutablePtr(helperAddr)) return null;
        sendDevLog('info', '时间加速', '匹配 call+movss[eax+disp32] 模式');
        sendDevLog('info', '时间加速', 'helper函数地址: ' + helperAddr + ', 偏移: 0x' + offset.toString(16));
        return { helperAddr: helperAddr, offset: offset };
      }

      // 模式3: fld dword ptr [imm32] => D9 05 xx xx xx xx (全局变量)
      for (var i = 0; i < 200; i++) {
        if (view.getUint8(i) === 0xD9 && view.getUint8(i + 1) === 0x05) {
          var addr = view.getUint32(i + 2, true);
          sendDevLog('info', '时间加速', '匹配 fld dword ptr [imm32] 偏移+' + i + ', 地址: 0x' + addr.toString(16));
          return { globalAddr: ptr(addr) };
        }
      }

      // 模式4: movss xmm0, [addr] => F3 0F 10 05 xx xx xx xx (SSE全局变量)
      for (var i = 0; i < 200; i++) {
        if (view.getUint8(i) === 0xF3 && view.getUint8(i + 1) === 0x0F &&
            view.getUint8(i + 2) === 0x10 && view.getUint8(i + 3) === 0x05) {
          var addr = view.getUint32(i + 4, true);
          sendDevLog('info', '时间加速', '匹配 movss xmm0, [imm32] 偏移+' + i + ', 地址: 0x' + addr.toString(16));
          return { globalAddr: ptr(addr) };
        }
      }

      // 模式5: 函数开头是jmp（跳转桩），跟踪跳转目标
      if (view.getUint8(0) === 0xE9) {
        var rel = view.getInt32(1, true);
        var jumpTarget = engineFuncAddr.add(5 + rel);
        sendDevLog('info', '时间加速', '检测到E9跳转桩，目标: ' + jumpTarget);
        return extractTimeScaleInfo(jumpTarget, depth + 1);
      }

      // 模式6: FF 25 xx xx xx xx = jmp dword ptr [addr] (间接跳转)
      if (view.getUint8(0) === 0xFF && view.getUint8(1) === 0x25) {
        var ptrAddr = view.getUint32(2, true);
        var indirectTarget = ptr(ptrAddr).readPointer();
        sendDevLog('info', '时间加速', '检测到间接跳转FF25，目标: ' + indirectTarget);
        if (indirectTarget && !indirectTarget.isNull()) {
          return extractTimeScaleInfo(indirectTarget, depth + 1);
        }
      }

      // 输出更多字节供调试
      var hexFull = '';
      for (var i = 0; i < 128 && i < view.byteLength; i++) {
        hexFull += ('0' + view.getUint8(i).toString(16)).slice(-2) + ' ';
      }
      sendDevLog('error', '时间加速', '未匹配已知模式，引擎函数前128字节: ' + hexFull);
      return null;

    } catch(e) {
      sendDevLog('error', '时间加速', '分析引擎函数字节失败: ' + e.message);
      return null;
    }
  }

  // 初始化
  function initTimeScale() {
    if (_initialized) return _initError === null;

    try {
      _initError = null;
      var mod = getGameAssembly();
      if (!mod) { _initError = '找不到GameAssembly.dll'; return false; }

      // 查找 il2cpp_resolve_icall 导出
      var resolveIcall = mod.findExportByName('il2cpp_resolve_icall');
      if (!resolveIcall) {
        _initError = '未找到 il2cpp_resolve_icall 导出';
        sendDevLog('error', '时间加速', _initError);
        return false;
      }
      sendDevLog('info', '时间加速', 'il2cpp_resolve_icall 地址: ' + resolveIcall);

      // 32位Windows: il2cpp_resolve_icall是mscdecl导出（实测验证）
      var resolveFunc = new NativeFunction(resolveIcall, 'pointer', ['pointer'], 'mscdecl');

      // 解析 get_timeScale icall
      var getIcallName = Memory.allocUtf8String('UnityEngine.Time::get_timeScale()');
      var engineFuncAddr = resolveFunc(getIcallName);

      if (!engineFuncAddr || engineFuncAddr.isNull()) {
        _initError = 'il2cpp_resolve_icall 返回NULL，get_timeScale icall不存在';
        sendDevLog('error', '时间加速', _initError);
        return false;
      }

      sendDevLog('success', '时间加速', 'get_timeScale 引擎函数地址: ' + engineFuncAddr);

      // 确认引擎函数所在模块
      var engineModule = Process.findModuleByAddress(engineFuncAddr);
      if (engineModule) {
        sendDevLog('info', '时间加速', '引擎函数所在模块: ' + engineModule.name);
      }

      // 不直接调用 get_timeScale() 验证。场景切换/房间切换瞬间调用游戏原生函数
      // 可能触发不稳定状态，改为只通过机器码解析和内存页校验确认地址。
      var currentVal = null;

      // 分析引擎函数机器码，提取timeScale变量信息
      var info = extractTimeScaleInfo(engineFuncAddr);
      if (!info) {
        _initError = '无法从引擎函数机器码定位timeScale变量地址';
        sendDevLog('error', '时间加速', _initError);
        return false;
      }

      if (info.globalAddr) {
        // 全局变量模式：地址固定，不会失效
        _mode = 'global';
        _globalAddr = info.globalAddr;
        sendDevLog('success', '时间加速', 'timeScale全局变量地址: ' + _globalAddr);
      } else if (info.helperAddr && info.offset !== undefined) {
        // 结构体成员模式：缓存helperAddr+offset，每次写操作时重新获取实例指针
        // 参照gravity.js的tryGetGM模式，不信任缓存的实例指针
        _mode = 'struct';
        _helperAddr = info.helperAddr;
        _offset = info.offset;
        if (!isExecutablePtr(info.helperAddr)) {
          _initError = 'helper函数地址不可执行: ' + info.helperAddr;
          sendDevLog('error', '时间加速', _initError);
          return false;
        }
        _helperFunc = new NativeFunction(info.helperAddr, 'pointer', [], 'mscdecl');
        sendDevLog('success', '时间加速', '结构体模式: helper=' + _helperAddr + ', 偏移=0x' + _offset.toString(16));
      } else {
        _initError = 'extractTimeScaleInfo返回无效数据';
        sendDevLog('error', '时间加速', _initError);
        return false;
      }

      // 验证：通过resolveVarAddr获取地址并读取，应该与get_timeScale()返回值一致
      var varAddr = resolveVarAddr();
      if (!varAddr) {
        _initError = '初始化时无法解析变量地址';
        sendDevLog('error', '时间加速', _initError);
        return false;
      }
      var memVal = readF32(varAddr);
      if (memVal === null || !isValidTimeScaleAddress(varAddr)) {
        _initError = '变量地址不可安全读写: ' + varAddr;
        sendDevLog('error', '时间加速', _initError);
        return false;
      }

      sendDevLog('success', '时间加速', '内存值: ' + memVal + ', 函数返回值: ' + currentVal);

      // 如果内存值和函数返回值差异大，可能定位错误
      if (currentVal !== null && Math.abs(memVal - currentVal) > 0.01) {
        sendDevLog('warn', '时间加速', '内存值(' + memVal + ')与函数返回值(' + currentVal + ')不一致，可能定位错误');
      }
      _initialized = true;
      sendDevLog('success', '时间加速', '初始化成功！');
      return true;

    } catch(e) {
      _initError = '初始化异常: ' + e.message;
      sendDevLog('error', '时间加速', _initError);
      return false;
    }
  }

  // 安全写入timeScale：每次重新解析地址，确保地址有效
  function safeWriteTimeScale(value) {
    value = normalizeSpeed(value);
    var addr = resolveVarAddr();
    if (!addr) {
      resetInitCache();
      if (!initTimeScale()) {
        sendDevLog('warn', '时间加速', '无法解析变量地址，跳过写入');
        return false;
      }
      addr = resolveVarAddr();
    }
    if (!isValidTimeScaleAddress(addr)) {
      resetInitCache();
      if (!initTimeScale()) {
        sendDevLog('warn', '时间加速', '变量地址失效，等待下次重试');
        return false;
      }
      addr = resolveVarAddr();
      if (!isValidTimeScaleAddress(addr)) return false;
    }
    return writeFloat(addr, value);
  }

  function beginRoomShutdown(modeBase) {
    var exitingModeBase = isValidPtr(modeBase) ? modeBase : _activeModeBase;
    if (exitingModeBase) _exitingModeBase = exitingModeBase;
    _roomShuttingDown = true;
    _activeModeBase = null;
    _modeReadyAt = 0;
    _nextRetryAt = 0;
    resetInitCache();
  }

  function processPendingTimeScaleWrite(modeBase) {
    if (!isValidPtr(modeBase)) return;

    var now = Date.now();
    if (_roomShuttingDown) {
      if (_exitingModeBase && _exitingModeBase.equals(modeBase)) return;
      _roomShuttingDown = false;
      _exitingModeBase = null;
    }

    if (!_activeModeBase || !_activeModeBase.equals(modeBase)) {
      _activeModeBase = modeBase;
      _modeReadyAt = now + MODE_READY_DELAY_MS;
      _nextRetryAt = 0;
      resetInitCache();
      if (enabled) _pendingSpeed = currentSpeed;
    }

    if (_roomShuttingDown || now < _modeReadyAt || now < _nextRetryAt) return;

    var targetSpeed = _pendingSpeed;
    if (targetSpeed === null && enabled && now - _lastApplyAt >= REAPPLY_INTERVAL_MS) {
      targetSpeed = currentSpeed;
    }
    if (targetSpeed === null) return;

    if (!initTimeScale() || !safeWriteTimeScale(targetSpeed)) {
      _nextRetryAt = now + REAPPLY_INTERVAL_MS;
      return;
    }

    _pendingSpeed = null;
    _nextRetryAt = 0;
    _lastApplyAt = now;
    if (_restorePending && targetSpeed === 1.0) _restorePending = false;
  }

  function detachHooks(hooks) {
    for (var i = 0; i < hooks.length; i++) {
      try { hooks[i].detach(); } catch(e) {}
    }
  }

  function installMainThreadHook() {
    if (_hookInstalled) return true;

    var mod = getGameAssembly();
    if (!mod || !mod.base) return false;
    var base = mod.base;
    var installed = [];

    try {
      installed.push(Interceptor.attach(base.add(0xAF6A00), {
        onEnter: function(args) {
          processPendingTimeScaleWrite(args[0]);
        }
      }));

      installed.push(Interceptor.attach(base.add(0xAEE850), {
        onEnter: function(args) {
          beginRoomShutdown(args[0]);
        }
      }));

      installed.push(Interceptor.attach(base.add(0xAFB6F0), {
        onEnter: function() {
          beginRoomShutdown();
        }
      }));

      _hooks = installed;
      _hookInstalled = true;
      sendDevLog('success', '时间加速', '主线程与退出保护Hook安装成功');
      return true;
    } catch(e) {
      detachHooks(installed);
      sendBothLog('error', '时间加速', '时间加速启用失败，请稍后重试', 'TimeScale hook install failed: ' + e.message);
      return false;
    }
  }

  return {
    setSpeed: function(speed) {
      currentSpeed = normalizeSpeed(speed);
      if (enabled) {
        _pendingSpeed = currentSpeed;
        _nextRetryAt = 0;
        sendDevLog('info', '时间加速', '倍速已切换: ' + currentSpeed + 'x');
      } else {
        sendDevLog('info', '时间加速', '倍速已预选: ' + speed + 'x（开启后生效）');
      }
    },
    enable: function() {
      if (enabled) return;
      if (!installMainThreadHook()) {
        sendStatus('timescale', false);
        return;
      }
      enabled = true;
      _restorePending = false;
      _pendingSpeed = currentSpeed;
      _nextRetryAt = 0;
      sendDevLog('success', '时间加速', '已启用 (' + currentSpeed + 'x)，等待主线程应用');
      sendStatus('timescale', true);
    },
    disable: function() {
      if (!enabled) return;
      enabled = false;
      _restorePending = true;
      _pendingSpeed = 1.0;
      _nextRetryAt = 0;
      sendDevLog('info', '时间加速', '已禁用，等待主线程恢复1.0x');
      sendStatus('timescale', false);
    }
  };
})();
