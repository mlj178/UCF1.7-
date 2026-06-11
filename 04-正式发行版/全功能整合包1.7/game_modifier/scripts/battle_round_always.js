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
            sendLog('error', 'BattleRound', '无法获取 GameAssembly');
            return false;
        }
        var base = mod.base;
        var targetAddr = base.add(RVA.StartGenerateSupplyBox);

        try {
            Interceptor.attach(targetAddr, {
                onEnter: function(args) {
                    if (!_enabled) return;

                    try {
                        var currentMod = getGameAssembly();
                        if (!currentMod) return;
                        var currentBase = currentMod.base;

                        var typeInfoAddr = currentBase.add(RVA.Mode_Nano4_Terminator_TypeInfo);
                        var typeInfo = safeReadPointer(typeInfoAddr);
                        
                        if (!typeInfo || typeInfo.isNull()) {
                            if (!this._loggedInvalidType) {
                                sendLog('warn', 'BattleRound', 'TypeInfo 指针无效');
                                this._loggedInvalidType = true;
                            }
                            return;
                        }

                        var staticFields = safeReadPointer(typeInfo.add(0x5C));
                        if (!staticFields || staticFields.isNull()) {
                            if (!this._loggedInvalidFields) {
                                sendLog('warn', 'BattleRound', 'static_fields 指针无效');
                                this._loggedInvalidFields = true;
                            }
                            return;
                        }

                        var oldVal = safeReadU8(staticFields.add(1));
                        if (oldVal === null) {
                            if (!this._loggedReadFail) {
                                sendLog('warn', 'BattleRound', '无法读取 isBattleRound 字段');
                                this._loggedReadFail = true;
                            }
                            return;
                        }

                        if (oldVal !== 1) {
                            if (safeWriteU8(staticFields.add(1), 1)) {
                                sendLog('success', 'BattleRound', '强制写入 isBattleRound=1 (原值=' + oldVal + ')');
                            }
                        }
                    } catch(e) {
                        // 静默失败
                    }
                }
            });

            _hookInstalled = true;
            sendLog('success', 'BattleRound', 'Hook 已安装 @ ' + targetAddr);
            return true;

        } catch(e) {
            sendLog('error', 'BattleRound', 'Hook 安装失败: ' + e.message);
            return false;
        }
    }

    return {
        enable: function() {
            try {
                if (!_hookInstalled) {
                    var ok = installHook();
                    if (!ok) {
                        sendLog('error', 'BattleRound', 'Hook 安装失败');
                        return;
                    }
                }
                
                _enabled = true;
                
                // 启用时立即强制写入一次
                try {
                    var mod = getGameAssembly();
                    if (mod) {
                        var base = mod.base;
                        var typeInfo = safeReadPointer(base.add(RVA.Mode_Nano4_Terminator_TypeInfo));
                        if (typeInfo) {
                            var staticFields = safeReadPointer(typeInfo.add(0x5C));
                            if (staticFields) {
                                safeWriteU8(staticFields.add(1), 1);
                                sendLog('success', 'BattleRound', '已立即强制写入 isBattleRound=1');
                            }
                        }
                    }
                } catch(e) {}
                
                sendLog('success', 'BattleRound', '强制决战回合已启用');
            } catch(e) {
                sendLog('error', 'BattleRound', '启用失败: ' + e.message);
            }
        },

        disable: function() {
            try {
                _enabled = false;
                sendLog('info', 'BattleRound', '强制决战回合已禁用');
            } catch(e) {
                sendLog('error', 'BattleRound', '禁用失败: ' + e.message);
            }
        },

        getStatus: function() {
            try {
                var flag = readBattleRoundFlag();
                return JSON.stringify({
                    enabled: _enabled,
                    hookInstalled: _hookInstalled,
                    currentIsBattleRound: flag
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
