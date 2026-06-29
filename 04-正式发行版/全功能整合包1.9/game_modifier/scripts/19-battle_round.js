// battle_round_always.js - 多人生化模式：强制决战回合
// Hook ModeBase_Nano.OnStartNewGameRound，在补给箱流程启动前强制写入 isBattleRound=1

modules.battle_round_always = (function() {
    // RVA 地址常量
    // ===== 配置与运行状态 =====
    var RVA = {
        Mode_Nano4_Terminator_TypeInfo: 0xE2CCB4,
        ModeBase_Nano_OnStartNewGameRound: 0xAF15D0,
        Mode_Nano4_Terminator_OnDestroy: 0xB44320,
    };

    // 状态变量
    var _enabled = false;
    var _hookInstalled = false;
    var _hookListener = null;
    var _exitHookListener = null;
    var _cachedBase = null;  // 缓存 GameAssembly.base，供 Hook 回调核对模块地址
    var _modeActive = false;

    // 日志去重标志（模块级闭包变量，跨 Hook 调用持久化）
    var _loggedInvalidType = false;
    var _loggedInvalidFields = false;
    var _loggedReadFail = false;

    // 调试计数器
    var _hookCallCount = 0;

    // 安全读取指针
    // ===== 指针读写工具 =====
    function safeReadPointer(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readPointer();
        } catch(e) {
            return null;
        }
    }

    // 安全读取 U8
    function safeReadU8(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readU8();
        } catch(e) {
            return null;
        }
    }

    // 安全写入 U8
    function safeWriteU8(addr, value) {
        try {
            if (!addr || addr.isNull()) return false;
            addr.writeU8(value);
            return true;
        } catch(e) {
            return false;
        }
    }

    // 读取当前 isBattleRound 值
    // ===== 状态读取与回合事件 =====
    function readBattleRoundFlag() {
        try {
            var mod = getGameAssembly();
            if (!mod) return -1;
            var base = mod.base;

            var typeInfoAddr = base.add(RVA.Mode_Nano4_Terminator_TypeInfo);
            var typeInfo = safeReadPointer(typeInfoAddr);
            if (!typeInfo) return -1;

            var staticFields = safeReadPointer(typeInfo.add(0x5C));
            if (!staticFields) return -1;

            var isBattleRound = safeReadU8(staticFields.add(1));
            if (isBattleRound === null) return -1;

            return isBattleRound;
        } catch(e) {
            return -1;
        }
    }

    function sendRoundEvent(enabled, applied, currentIsBattleRound) {
        send(JSON.stringify({
            type: 'battle_round_round',
            enabled: enabled,
            applied: applied,
            currentIsBattleRound: currentIsBattleRound
        }));
    }

    function markModeEnter() {
        if (_modeActive) return;
        _modeActive = true;
        send(JSON.stringify({ type: 'battle_round_mode_enter' }));
    }

    function markModeExit() {
        if (!_modeActive) return;
        _modeActive = false;
        send(JSON.stringify({ type: 'battle_round_mode_exit' }));
    }

    function syncNano4TOnRound() {
        // 进入正确模式时再初始化Buff模块；不需要Python定时轮询。
        try {
            if (modules.nano4t) {
                modules.nano4t.onModeRound();
            }
        } catch(e) {}
    }

    function resolveTerminatorTypeInfo(currentBase, callId) {
        var typeInfoAddr = currentBase.add(RVA.Mode_Nano4_Terminator_TypeInfo);
        var typeInfo = safeReadPointer(typeInfoAddr);

        sendLogFile('info', 'BattleRound', '[HOOK#' + callId + '] typeInfoAddr=' + typeInfoAddr + ', typeInfo=' + typeInfo);

        if (!typeInfo || typeInfo.isNull()) {
            if (!_loggedInvalidType) {
                sendLogFile('warn', 'BattleRound', '[HOOK#' + callId + '] TypeInfo 指针无效');
                _loggedInvalidType = true;
            }
            return null;
        }
        return typeInfo;
    }

    function isTerminatorModeInstance(modeInstance, typeInfo, callId) {
        // ModeBase_Nano 被多个生化模式共用，只允许精确的多人生化 Terminator 实例通过
        var instanceClass = safeReadPointer(modeInstance);
        if (!instanceClass || !instanceClass.equals(typeInfo)) {
            sendLogFile('info', 'BattleRound', '[HOOK#' + callId + '] 非 Mode_Nano4_Terminator 实例，跳过');
            return false;
        }
        sendLogFile('info', 'BattleRound', '[HOOK#' + callId + '] Mode_Nano4_Terminator 类指针校验通过');
        return true;
    }

    function resolveStaticFields(typeInfo, callId) {
        var staticFields = safeReadPointer(typeInfo.add(0x5C));
        sendLogFile('info', 'BattleRound', '[HOOK#' + callId + '] staticFields=' + staticFields);

        if (!staticFields || staticFields.isNull()) {
            if (!_loggedInvalidFields) {
                sendLogFile('warn', 'BattleRound', '[HOOK#' + callId + '] static_fields 指针无效');
                _loggedInvalidFields = true;
            }
            return null;
        }
        return staticFields;
    }

    function applyBattleRoundFlag(staticFields, callId) {
        var oldVal = safeReadU8(staticFields.add(1));
        sendLogFile('info', 'BattleRound', '[HOOK#' + callId + '] isBattleRound 当前值=' + oldVal);

        if (oldVal === null) {
            if (!_loggedReadFail) {
                sendLogFile('warn', 'BattleRound', '[HOOK#' + callId + '] 无法读取 isBattleRound 字段');
                _loggedReadFail = true;
            }
            return false;
        }

        if (oldVal !== 1) {
            if (safeWriteU8(staticFields.add(1), 1)) {
                sendLogFile('success', 'BattleRound', '[HOOK#' + callId + '] 强制写入 isBattleRound=1 (原值=' + oldVal + ')');
            } else {
                sendLogFile('error', 'BattleRound', '[HOOK#' + callId + '] 写入失败');
                return false;
            }
        } else {
            sendLogFile('info', 'BattleRound', '[HOOK#' + callId + '] isBattleRound 已是 1，无需写入');
        }
        return true;
    }

    // 安装 Hook
    // ===== Hook 安装与回调 =====
    function installHook() {
        if (_hookInstalled) return true;

        var mod = getGameAssembly();
        if (!mod) {
            sendLogFile('error', 'BattleRound', '无法获取 GameAssembly');
            return false;
        }
        var base = mod.base;
        _cachedBase = base;  // 缓存 base 供 Hook 回调核对
        var targetAddr = base.add(RVA.ModeBase_Nano_OnStartNewGameRound);

        sendLogFile('info', 'BattleRound', '[INSTALL] GameAssembly base=' + base + ', cachedBase=' + _cachedBase);

        try {
            _hookListener = Interceptor.attach(targetAddr, {
                onEnter: function(args) {
                    _hookCallCount++;
                    var callId = _hookCallCount;

                    try {
                        // 每次动态获取模块和类型信息，不缓存 TypeInfo/static_fields 指针
                        var currentMod = getGameAssembly();
                        if (!currentMod) {
                            sendLogFile('warn', 'BattleRound', '[HOOK#' + callId + '] getGameAssembly 返回 null');
                            return;
                        }
                        var currentBase = currentMod.base;

                        sendLogFile('info', 'BattleRound', '[HOOK#' + callId + '] currentBase=' + currentBase + ', cachedBase=' + _cachedBase + ', 相同=' + (currentBase.equals(_cachedBase)));

                        var typeInfo = resolveTerminatorTypeInfo(currentBase, callId);
                        if (!typeInfo) return;

                        if (!isTerminatorModeInstance(args[0], typeInfo, callId)) return;

                        markModeEnter();
                        syncNano4TOnRound();

                        if (!_enabled) {
                            sendRoundEvent(false, false, -1);
                            return;
                        }

                        var staticFields = resolveStaticFields(typeInfo, callId);
                        if (!staticFields) return;

                        if (!applyBattleRoundFlag(staticFields, callId)) return;

                        sendRoundEvent(true, true, 1);
                    } catch(e) {
                        sendLogFile('error', 'BattleRound', '[HOOK#' + callId + '] 异常: ' + e.message);
                    }
                }
            });

            _exitHookListener = Interceptor.attach(base.add(RVA.Mode_Nano4_Terminator_OnDestroy), {
                onEnter: function() {
                    markModeExit();
                }
            });

            _hookInstalled = true;
            sendLogFile('success', 'BattleRound', 'Hook 已安装 @ ' + targetAddr);
            return true;

        } catch(e) {
            if (_hookListener) {
                try { _hookListener.detach(); } catch(detachError) {}
                _hookListener = null;
            }
            if (_exitHookListener) {
                try { _exitHookListener.detach(); } catch(detachError) {}
                _exitHookListener = null;
            }
            sendLogFile('error', 'BattleRound', 'Hook 安装失败: ' + e.message);
            return false;
        }
    }

    // 清理函数：在 Frida 会话断开时调用
    // ===== 清理与状态重置 =====
    function cleanup() {
        sendLogFile('info', 'BattleRound', '[CLEANUP] 开始清理');

        if (_hookListener) {
            try {
                _hookListener.detach();
                sendLogFile('info', 'BattleRound', '[CLEANUP] Hook 已解除');
            } catch(e) {
                sendLogFile('warn', 'BattleRound', '[CLEANUP] Hook 解除失败: ' + e.message);
            }
            _hookListener = null;
        }
        if (_exitHookListener) {
            try { _exitHookListener.detach(); } catch(e) {}
            _exitHookListener = null;
        }

        // 重置状态
        _enabled = false;
        _hookInstalled = false;
        _cachedBase = null;
        _modeActive = false;

        // 重置日志去重标志
        _loggedInvalidType = false;
        _loggedInvalidFields = false;
        _loggedReadFail = false;

        // 重置计数器
        _hookCallCount = 0;

        sendLogFile('info', 'BattleRound', '[CLEANUP] 清理完成');
    }

    // ===== 功能开关与 RPC 边界 =====
    function enableFeature() {
            try {
                sendLogFile('info', 'BattleRound', '[ENABLE] 开始启用, _hookInstalled=' + _hookInstalled);

                if (!_hookInstalled) {
                    var ok = installHook();
                    if (!ok) {
                        sendLogFile('error', 'BattleRound', '[ENABLE] Hook 安装失败');
                        return;
                    }
                }

                _enabled = true;
                sendLogFile('info', 'BattleRound', '[ENABLE] _enabled 已设为 true');
                sendDevLog('success', 'BattleRound', '[ENABLE] 已预约，仅在多人生化新回合写入', 'BattleRound enabled and waiting for next Nano4T round');
            } catch(e) {
                sendBothLog('error', 'BattleRound', '决战回合启用失败，请重新连接游戏后重试', 'BattleRound enable failed: ' + e.message);
            }
    }

    function disableFeature() {
            try {
                sendLogFile('info', 'BattleRound', '[DISABLE] 开始禁用');

                _enabled = false;
                sendDevLog('info', 'BattleRound', '[DISABLE] 已停止后续回合写入', 'BattleRound disabled');
            } catch(e) {
                sendBothLog('error', 'BattleRound', '决战回合关闭失败，请稍后重试', 'BattleRound disable failed: ' + e.message);
            }
    }

    function getStatus() {
        try {
            var flag = readBattleRoundFlag();
            return JSON.stringify({
                enabled: _enabled,
                hookInstalled: _hookInstalled,
                modeActive: _modeActive,
                currentIsBattleRound: flag,
                cachedBase: _cachedBase ? _cachedBase.toString() : null,
                hookCallCount: _hookCallCount
            });
        } catch(e) {
            return JSON.stringify({
                enabled: _enabled,
                hookInstalled: _hookInstalled,
                currentIsBattleRound: -1
            });
        }
    }

    return {
        enable: enableFeature,
        disable: disableFeature,
        cleanup: cleanup,
        startMonitor: installHook,
        getStatus: getStatus
    };
})();

// 注册清理函数
if (typeof registerCleanup === 'function' && modules.battle_round_always) {
    registerCleanup(modules.battle_round_always.cleanup);
}

// Frida连接后立即安装低频生命周期监听；未启用时只识别模式，不写字段。
modules.battle_round_always.startMonitor();
