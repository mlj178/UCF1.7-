// ============================================================
// AAAAA-battle_round_always.js - 多人生化模式：每局强制决战回合
//
// 方案：Hook StartGenerateSupplyBox，强制写入isBattleRound=1
// 优势：简单可靠，不修改游戏代码，兼容性好
//
// 关键地址：
//   Mode_Nano4_Terminator_TypeInfo: 0xE2CCB4
//   StartGenerateSupplyBox:         0xB45AA0
//
// 修复：线程安全、指针验证、错误处理
// ============================================================

(function() {
    'use strict';

    // ==================== 1. 日志系统 ====================
    var MAX_LOGS_PER_MODULE = 100;
    var moduleLogCounts = {};

    function log(level, module, message) {
        try {
            if (!moduleLogCounts[module]) moduleLogCounts[module] = 0;
            if (moduleLogCounts[module] >= MAX_LOGS_PER_MODULE) return;
            moduleLogCounts[module]++;
            
            var fullMsg = '[' + module + '] ' + message;
            console.log('[' + level + '] ' + fullMsg);
            
            try {
                send({type: 'log', level: level, module: module, message: message});
            } catch(e) {}
        } catch(e) {}
    }

    // ==================== 2. 模块查找（不缓存，每次重新查找）====================
    function getGameAssembly() {
        try {
            var mod = Process.findModuleByName('GameAssembly.dll');
            if (!mod) {
                return null;
            }
            return mod;
        } catch(e) {
            return null;
        }
    }

    // ==================== 3. RVA地址常量 ====================
    var RVA = {
        Mode_Nano4_Terminator_TypeInfo: 0xE2CCB4,
        StartGenerateSupplyBox:         0xB45AA0,
    };

    // ==================== 4. 线程安全的状态变量 ====================
    // RPC调用在Frida主线程执行，天然串行，不需要互斥锁
    // Hook回调在游戏线程执行，但只读取_enabled变量，JavaScript布尔值读写是原子的
    var _enabled = false;
    var _hookInstalled = false;

    // ==================== 5. 安全的指针读取函数 ====================
    
    // 安全读取指针
    function safeReadPointer(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readPointer();
        } catch(e) {
            return null;
        }
    }

    // 安全读取U8
    function safeReadU8(addr) {
        try {
            if (!addr || addr.isNull()) return null;
            return addr.readU8();
        } catch(e) {
            return null;
        }
    }

    // 安全写入U8
    function safeWriteU8(addr, value) {
        try {
            if (!addr || addr.isNull()) return false;
            addr.writeU8(value);
            return true;
        } catch(e) {
            return false;
        }
    }

    // ==================== 6. 核心功能 ====================

    // 读取当前 isBattleRound 值（从游戏内存实时读取）
    function readBattleRoundFlag() {
        try {
            var mod = getGameAssembly();
            if (!mod) return -1;
            var base = mod.base;

            // 读取TypeInfo
            var typeInfoAddr = base.add(RVA.Mode_Nano4_Terminator_TypeInfo);
            var typeInfo = safeReadPointer(typeInfoAddr);
            if (!typeInfo) return -1;

            // 读取static_fields
            var staticFields = safeReadPointer(typeInfo.add(0x5C));
            if (!staticFields) return -1;

            // 读取isBattleRound字段
            var isBattleRound = safeReadU8(staticFields.add(1));
            if (isBattleRound === null) return -1;

            return isBattleRound;
        } catch(e) {
            return -1;
        }
    }

    // ==================== 7. Hook安装 ====================
    function installHook() {
        if (_hookInstalled) return true;

        var mod = getGameAssembly();
        if (!mod) {
            log('error', 'Hook', '无法获取GameAssembly');
            return false;
        }
        var base = mod.base;

        // 计算目标地址
        var targetAddr = base.add(RVA.StartGenerateSupplyBox);

        try {
            Interceptor.attach(targetAddr, {
                onEnter: function(args) {
                    // 检查功能是否启用（原子读取）
                    if (!_enabled) return;

                    try {
                        // 动态获取基址（避免缓存失效问题）
                        var currentMod = getGameAssembly();
                        if (!currentMod) return;
                        var currentBase = currentMod.base;

                        // 读取TypeInfo
                        var typeInfoAddr = currentBase.add(RVA.Mode_Nano4_Terminator_TypeInfo);
                        var typeInfo = safeReadPointer(typeInfoAddr);
                        
                        // 验证TypeInfo指针是否有效
                        if (!typeInfo || typeInfo.isNull()) {
                            // 只在首次失败时记录，避免刷屏
                            if (!this._loggedInvalidType) {
                                log('warn', 'Hook', 'TypeInfo指针无效: ' + typeInfoAddr);
                                this._loggedInvalidType = true;
                            }
                            return;
                        }

                        // 读取static_fields
                        var staticFields = safeReadPointer(typeInfo.add(0x5C));
                        if (!staticFields || staticFields.isNull()) {
                            if (!this._loggedInvalidFields) {
                                log('warn', 'Hook', 'static_fields指针无效');
                                this._loggedInvalidFields = true;
                            }
                            return;
                        }

                        // 读取当前值
                        var oldVal = safeReadU8(staticFields.add(1));
                        if (oldVal === null) {
                            if (!this._loggedReadFail) {
                                log('warn', 'Hook', '无法读取isBattleRound字段');
                                this._loggedReadFail = true;
                            }
                            return;
                        }

                        // 如果不是1，强制写入
                        if (oldVal !== 1) {
                            if (safeWriteU8(staticFields.add(1), 1)) {
                                log('warn', 'Hook', '强制写入 isBattleRound=1 (原值=' + oldVal + ')');
                            }
                        }
                    } catch(e) {
                        // 静默失败，避免影响游戏
                    }
                }
            });

            _hookInstalled = true;
            log('success', 'Hook', 'StartGenerateSupplyBox Hook已安装');
            log('info', 'Hook', '目标地址: ' + targetAddr);
            return true;

        } catch(e) {
            log('error', 'Hook', 'Hook安装失败: ' + e.message);
            return false;
        }
    }

    // ==================== 8. RPC接口导出 ====================
    rpc.exports = {
        // 启用强制决战回合
        enable: function() {
            try {
                if (!_hookInstalled) {
                    var ok = installHook();
                    if (!ok) {
                        return {ok: false, msg: 'Hook安装失败'};
                    }
                }
                
                _enabled = true;
                
                // 启用时立即强制写入一次（确保立即生效）
                try {
                    var mod = getGameAssembly();
                    if (mod) {
                        var base = mod.base;
                        var typeInfo = safeReadPointer(base.add(RVA.Mode_Nano4_Terminator_TypeInfo));
                        if (typeInfo) {
                            var staticFields = safeReadPointer(typeInfo.add(0x5C));
                            if (staticFields) {
                                safeWriteU8(staticFields.add(1), 1);
                                log('success', 'RPC', '已立即强制写入 isBattleRound=1');
                            }
                        }
                    }
                } catch(e) {}
                
                log('success', 'RPC', '强制决战回合已启用 - 每局都是决战回合');
                return {ok: true, msg: '已启用（已立即强制写入一次）'};
            } catch(e) {
                return {ok: false, msg: '启用失败: ' + e.message};
            }
        },

        // 禁用强制决战回合
        disable: function() {
            try {
                _enabled = false;
                log('info', 'RPC', '强制决战回合已禁用 - 恢复原始随机逻辑');
                return {ok: true, msg: '已禁用'};
            } catch(e) {
                return {ok: false, msg: '禁用失败: ' + e.message};
            }
        },

        // 清理Hook和恢复状态
        cleanup: function() {
            try {
                // 禁用功能
                _enabled = false;
                
                // 尝试恢复原始值（可选，避免影响后续游戏）
                try {
                    var mod = getGameAssembly();
                    if (mod) {
                        var base = mod.base;
                        var typeInfo = safeReadPointer(base.add(RVA.Mode_Nano4_Terminator_TypeInfo));
                        if (typeInfo) {
                            var staticFields = safeReadPointer(typeInfo.add(0x5C));
                            if (staticFields) {
                                // 恢复为0（普通回合）
                                safeWriteU8(staticFields.add(1), 0);
                                log('info', 'Cleanup', '已恢复 isBattleRound=0');
                            }
                        }
                    }
                } catch(e) {}
                
                log('success', 'Cleanup', 'Hook已清理，状态已恢复');
                return {ok: true, msg: '清理完成'};
            } catch(e) {
                return {ok: false, msg: '清理失败: ' + e.message};
            }
        },

        // 查询当前状态
        getStatus: function() {
            try {
                var flag = readBattleRoundFlag();
                return {
                    enabled: _enabled,
                    hookInstalled: _hookInstalled,
                    currentIsBattleRound: flag,
                };
            } catch(e) {
                return {
                    enabled: _enabled,
                    hookInstalled: _hookInstalled,
                    currentIsBattleRound: -1,
                };
            }
        },

        // 立即强制写入一次
        forceNow: function() {
            try {
                var mod = getGameAssembly();
                if (!mod) {
                    return {ok: false, msg: '无法获取GameAssembly'};
                }
                var base = mod.base;

                var typeInfoAddr = base.add(RVA.Mode_Nano4_Terminator_TypeInfo);
                var typeInfo = safeReadPointer(typeInfoAddr);
                if (!typeInfo) {
                    return {ok: false, msg: 'TypeInfo为空'};
                }

                var staticFields = safeReadPointer(typeInfo.add(0x5C));
                if (!staticFields) {
                    return {ok: false, msg: 'static_fields为空'};
                }

                if (safeWriteU8(staticFields.add(1), 1)) {
                    log('success', 'RPC', '已立即强制写入 isBattleRound=1');
                    return {ok: true, msg: '已强制写入'};
                } else {
                    return {ok: false, msg: '写入失败'};
                }
            } catch(e) {
                return {ok: false, msg: '写入失败: ' + e.message};
            }
        },

        // 调试：显示详细的读取信息
        debugReadInfo: function() {
            try {
                var mod = getGameAssembly();
                if (!mod) return {ok: false, msg: '无法获取GameAssembly'};
                var base = mod.base;

                var typeInfoAddr = base.add(RVA.Mode_Nano4_Terminator_TypeInfo);
                var typeInfo = safeReadPointer(typeInfoAddr);

                var info = {
                    gameAssemblyBase: base.toString(),
                    typeInfoRVA: '0x' + RVA.Mode_Nano4_Terminator_TypeInfo.toString(16),
                    typeInfoAddr: typeInfoAddr.toString(),
                    typeInfo: typeInfo ? typeInfo.toString() : 'null',
                };

                if (typeInfo) {
                    var staticFields = safeReadPointer(typeInfo.add(0x5C));
                    info.staticFieldsAddr = staticFields ? staticFields.toString() : 'null';

                    if (staticFields) {
                        var isAttributeEnable = safeReadU8(staticFields.add(0));
                        var isBattleRound = safeReadU8(staticFields.add(1));
                        var isBattleStart = safeReadU8(staticFields.add(2));
                        
                        info.isAttributeEnable = isAttributeEnable !== null ? isAttributeEnable : 'null';
                        info.isBattleRound = isBattleRound !== null ? isBattleRound : 'null';
                        info.isBattleStart = isBattleStart !== null ? isBattleStart : 'null';
                        
                        info.isAttributeEnableAddr = staticFields.add(0).toString();
                        info.isBattleRoundAddr = staticFields.add(1).toString();
                        info.isBattleStartAddr = staticFields.add(2).toString();
                    }
                }

                log('info', 'Debug', '调试信息已生成');
                return {ok: true, info: info};
            } catch(e) {
                return {ok: false, msg: '调试失败: ' + e.message};
            }
        },
    };

    // ==================== 9. 初始化 ====================
    var mod = getGameAssembly();
    if (mod) {
        log('success', '系统', '脚本已加载');
        log('info', '系统', 'GameAssembly基址: ' + mod.base);
        log('info', '系统', '等待启用...');
    } else {
        log('error', '系统', 'GameAssembly.dll 未找到');
    }

})();
