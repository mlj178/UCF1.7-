// battle_round_always.js - 多人生化模式：强制决战回合
// Hook StartGenerateSupplyBox，强制写入 isBattleRound=1

modules.battle_round_always = (function() {
    // RVA 地址常量
    var RVA = {
        Mode_Nano4_Terminator_TypeInfo: 0xE2CCB4,
        StartGenerateSupplyBox: 0xB45AA0,
    };

    // 状态变量
    var _enabled = false;
    var _hookInstalled = false;
    var _cachedBase = null;  // 缓存 GameAssembly.base，避免 onEnter 每次调用 getGameAssembly

    // 日志去重标志（模块级闭包变量，跨 Hook 调用持久化）
    var _loggedInvalidType = false;
    var _loggedInvalidFields = false;
    var _loggedReadFail = false;

    // 调试计数器
    var _hookCallCount = 0;

    // 安全读取指针
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

    // 安装 Hook
    function installHook() {
        if (_hookInstalled) return true;

        var mod = getGameAssembly();
        if (!mod) {
            sendLogFile('error', 'BattleRound', '无法获取 GameAssembly');
            return false;
        }
        var base = mod.base;
        _cachedBase = base;  // 缓存 base 供 onEnter 复用
        var targetAddr = base.add(RVA.StartGenerateSupplyBox);

        sendLogFile('info', 'BattleRound', '[INSTALL] GameAssembly base=' + base + ', cachedBase=' + _cachedBase);

        try {
            Interceptor.attach(targetAddr, {
                onEnter: function(args) {
                    _hookCallCount++;
                    var callId = _hookCallCount;

                    sendLogFile('info', 'BattleRound', '[HOOK#' + callId + '] onEnter 触发, _enabled=' + _enabled);

                    if (!_enabled) {
                        sendLogFile('info', 'BattleRound', '[HOOK#' + callId + '] 功能未启用，跳过');
                        return;
                    }

                    try {
                        // 方案1：用缓存的 base（可能导致闪退）
                        // var currentBase = _cachedBase;

                        // 方案2：每次动态获取（AAAAA版本的做法）
                        var currentMod = getGameAssembly();
                        if (!currentMod) {
                            sendLogFile('warn', 'BattleRound', '[HOOK#' + callId + '] getGameAssembly 返回 null');
                            return;
                        }
                        var currentBase = currentMod.base;

                        sendLogFile('info', 'BattleRound', '[HOOK#' + callId + '] currentBase=' + currentBase + ', cachedBase=' + _cachedBase + ', 相同=' + (currentBase.equals(_cachedBase)));

                        var typeInfoAddr = currentBase.add(RVA.Mode_Nano4_Terminator_TypeInfo);
                        var typeInfo = safeReadPointer(typeInfoAddr);

                        sendLogFile('info', 'BattleRound', '[HOOK#' + callId + '] typeInfoAddr=' + typeInfoAddr + ', typeInfo=' + typeInfo);

                        if (!typeInfo || typeInfo.isNull()) {
                            if (!_loggedInvalidType) {
                                sendLogFile('warn', 'BattleRound', '[HOOK#' + callId + '] TypeInfo 指针无效');
                                _loggedInvalidType = true;
                            }
                            return;
                        }

                        var staticFields = safeReadPointer(typeInfo.add(0x5C));
                        sendLogFile('info', 'BattleRound', '[HOOK#' + callId + '] staticFields=' + staticFields);

                        if (!staticFields || staticFields.isNull()) {
                            if (!_loggedInvalidFields) {
                                sendLogFile('warn', 'BattleRound', '[HOOK#' + callId + '] static_fields 指针无效');
                                _loggedInvalidFields = true;
                            }
                            return;
                        }

                        var oldVal = safeReadU8(staticFields.add(1));
                        sendLogFile('info', 'BattleRound', '[HOOK#' + callId + '] isBattleRound 当前值=' + oldVal);

                        if (oldVal === null) {
                            if (!_loggedReadFail) {
                                sendLogFile('warn', 'BattleRound', '[HOOK#' + callId + '] 无法读取 isBattleRound 字段');
                                _loggedReadFail = true;
                            }
                            return;
                        }

                        if (oldVal !== 1) {
                            if (safeWriteU8(staticFields.add(1), 1)) {
                                sendLogFile('success', 'BattleRound', '[HOOK#' + callId + '] 强制写入 isBattleRound=1 (原值=' + oldVal + ')');
                            } else {
                                sendLogFile('error', 'BattleRound', '[HOOK#' + callId + '] 写入失败');
                            }
                        } else {
                            sendLogFile('info', 'BattleRound', '[HOOK#' + callId + '] isBattleRound 已是 1，无需写入');
                        }
                    } catch(e) {
                        sendLogFile('error', 'BattleRound', '[HOOK#' + callId + '] 异常: ' + e.message);
                    }
                }
            });

            _hookInstalled = true;
            sendLogFile('success', 'BattleRound', 'Hook 已安装 @ ' + targetAddr);
            return true;

        } catch(e) {
            sendLogFile('error', 'BattleRound', 'Hook 安装失败: ' + e.message);
            return false;
        }
    }

    // 清理函数：在 Frida 会话断开时调用
    function cleanup() {
        sendLogFile('info', 'BattleRound', '[CLEANUP] 开始清理');

        // 重置状态
        _enabled = false;
        _hookInstalled = false;
        _cachedBase = null;

        // 重置日志去重标志
        _loggedInvalidType = false;
        _loggedInvalidFields = false;
        _loggedReadFail = false;

        // 重置计数器
        _hookCallCount = 0;

        sendLogFile('info', 'BattleRound', '[CLEANUP] 清理完成');
    }

    return {
        enable: function() {
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

                // 启用时立即强制写入一次
                try {
                    var mod = getGameAssembly();
                    if (mod) {
                        var base = mod.base;
                        sendLogFile('info', 'BattleRound', '[ENABLE] 立即写入: base=' + base);

                        var typeInfo = safeReadPointer(base.add(RVA.Mode_Nano4_Terminator_TypeInfo));
                        if (typeInfo) {
                            var staticFields = safeReadPointer(typeInfo.add(0x5C));
                            if (staticFields) {
                                var oldVal = safeReadU8(staticFields.add(1));
                                sendLogFile('info', 'BattleRound', '[ENABLE] 立即写入: oldVal=' + oldVal);

                                safeWriteU8(staticFields.add(1), 1);
                                sendLogFile('success', 'BattleRound', '[ENABLE] 已立即强制写入 isBattleRound=1');
                            } else {
                                sendLogFile('warn', 'BattleRound', '[ENABLE] staticFields 为 null');
                            }
                        } else {
                            sendLogFile('warn', 'BattleRound', '[ENABLE] typeInfo 为 null');
                        }
                    } else {
                        sendLogFile('warn', 'BattleRound', '[ENABLE] getGameAssembly 返回 null');
                    }
                } catch(e) {
                    sendLogFile('error', 'BattleRound', '[ENABLE] 立即写入异常: ' + e.message);
                }

                sendLogFile('success', 'BattleRound', '[ENABLE] 强制决战回合已启用');
            } catch(e) {
                sendLogFile('error', 'BattleRound', '[ENABLE] 启用失败: ' + e.message);
            }
        },

        disable: function() {
            try {
                sendLogFile('info', 'BattleRound', '[DISABLE] 开始禁用');

                _enabled = false;

                // 禁用时恢复 isBattleRound 为 0，清理残留标志
                try {
                    var mod = getGameAssembly();
                    if (mod) {
                        var base = mod.base;
                        sendLogFile('info', 'BattleRound', '[DISABLE] 恢复写入: base=' + base + ', cachedBase=' + _cachedBase);

                        var typeInfo = safeReadPointer(base.add(RVA.Mode_Nano4_Terminator_TypeInfo));
                        if (typeInfo) {
                            var staticFields = safeReadPointer(typeInfo.add(0x5C));
                            if (staticFields) {
                                var oldVal = safeReadU8(staticFields.add(1));
                                sendLogFile('info', 'BattleRound', '[DISABLE] 恢复写入: oldVal=' + oldVal);

                                safeWriteU8(staticFields.add(1), 0);
                                sendLogFile('info', 'BattleRound', '[DISABLE] 已恢复 isBattleRound=0');
                            }
                        }
                    }
                } catch(e) {
                    sendLogFile('error', 'BattleRound', '[DISABLE] 恢复异常: ' + e.message);
                }

                sendLogFile('info', 'BattleRound', '[DISABLE] 强制决战回合已禁用');
            } catch(e) {
                sendLogFile('error', 'BattleRound', '[DISABLE] 禁用失败: ' + e.message);
            }
        },

        cleanup: cleanup,

        getStatus: function() {
            try {
                var flag = readBattleRoundFlag();
                return JSON.stringify({
                    enabled: _enabled,
                    hookInstalled: _hookInstalled,
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
    };
})();

// 注册清理函数
if (typeof registerCleanup === 'function' && modules.battle_round_always) {
    registerCleanup(modules.battle_round_always.cleanup);
}
