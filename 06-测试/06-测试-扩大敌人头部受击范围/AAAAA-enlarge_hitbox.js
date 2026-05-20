(function() {
    'use strict';

    // ================================================================
    // 扩大受击范围 v2.7 - 时间控制版（每3秒输出一次）
    // ================================================================

    // ================================================================
    // 日志系统
    // ================================================================
    function log(msg) {
        console.log('[v2.7] ' + msg);
        send({ type: 'log', level: 'info', module: 'v2.7', message: msg });
    }

    function sendStatus(feature, enabled) {
        console.log('[状态] ' + feature + ' -> ' + (enabled ? '开' : '关'));
        send({ type: 'status', feature: feature, enabled: enabled });
    }

    // ================================================================
    // 获取 GameAssembly.dll
    // ================================================================
    var _gameAssembly = null;
    function getGameAssembly() {
        if (_gameAssembly) return _gameAssembly;
        try {
            var mod = Process.findModuleByName('GameAssembly.dll');
            if (!mod) return null;
            _gameAssembly = mod;
            return mod;
        } catch(e) { return null; }
    }

    // ================================================================
    // RVA 常量
    // ================================================================
    var RVA = {
        SingletonGet: 0x4A8170,
        GM_Singleton_MethodInfo: 0xE1CE64,
        Player_get_isMyPlayer: 0xB55FD0,
        Player_Update: 0xB551D0,
        Transform_get_localScale_Injected: 0x3F4130,
        Transform_set_localScale_Injected: 0x3F4700,
        Entity_get_team: 0x1E0070,
        Entity_get_isDead: 0xB400E0,
        Component_get_transform: 0x32CF40,
        Transform_get_childCount: 0x3F3E80,
        Transform_GetChild: 0x3F3150,
    };

    // ================================================================
    // 字段偏移
    // ================================================================
    var OFF = {
        GM_allPlayers: 0x1C,
        GM_playersBL: 0x20,
        GM_playersGR: 0x28,
        Player_currentCharacter: 0x5C,
        Transform_localScale: 0x30,
        E_team: 0x20,
        Arr_len: 0x0C,
        Arr_data: 0x10,
        List_items: 0x08,
        List_size: 0x0C,
        ptrSize: 4,
    };

    // ================================================================
    // 状态
    // ================================================================
    var state = {
        enabled: false,
        hitboxScale: 1.5,
        targetEnemy: true,
        targetAlly: false
    };
    var myPlayer = null;
    var myTeam = -1;
    var processedEntities = {};
    var playerUpdateHook = null;
    var hasLogged = false;
    var lastLogTime = 0;
    var LOG_INTERVAL = 3000; // 3秒

    // ================================================================
    // 🔒 安全的内存操作
    // ================================================================
    function isPointerValid(ptr) {
        if (!ptr || ptr.isNull()) return false;
        try {
            Memory.readU8(ptr);
            return true;
        } catch(e) {
            return false;
        }
    }

    function safeReadPointer(ptr) {
        if (!ptr || ptr.isNull()) return null;
        try {
            return ptr.readPointer();
        } catch(e) {
            return null;
        }
    }

    function safeReadU32(ptr) {
        if (!ptr || ptr.isNull()) return 0;
        try {
            return ptr.readU32();
        } catch(e) {
            return 0;
        }
    }

    function safeReadFloat(ptr) {
        if (!ptr || ptr.isNull()) return 0;
        try {
            return ptr.readFloat();
        } catch(e) {
            return 0;
        }
    }

    function safeWriteFloat(ptr, value) {
        if (!ptr || ptr.isNull()) return false;
        try {
            if (!isPointerValid(ptr)) return false;
            ptr.writeFloat(value);
            return true;
        } catch(e) {
            return false;
        }
    }

    // ================================================================
    // 初始化
    // ================================================================
    var singletonGetter = null;
    var isMyPlayerFn = null;
    var getLocalScaleFn = null;
    var setLocalScaleFn = null;
    var scaleVecBuffer = null;
    var getTeamFn = null;
    var isDeadFn = null;
    var getTransformFn = null;
    var getChildCountFn = null;
    var getChildFn = null;

    function initNativeFunctions() {
        var mod = getGameAssembly();
        if (!mod) return false;
        var base = mod.base;

        try {
            singletonGetter = new NativeFunction(base.add(RVA.SingletonGet), 'pointer', ['pointer']);
            isMyPlayerFn = new NativeFunction(base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer']);
            getLocalScaleFn = new NativeFunction(base.add(RVA.Transform_get_localScale_Injected), 'void', ['pointer', 'pointer']);
            setLocalScaleFn = new NativeFunction(base.add(RVA.Transform_set_localScale_Injected), 'void', ['pointer', 'pointer']);
            scaleVecBuffer = Memory.alloc(12);
            try {
                getTeamFn = new NativeFunction(base.add(RVA.Entity_get_team), 'int32', ['pointer', 'pointer']);
            } catch(e) { getTeamFn = null; }
            try {
                isDeadFn = new NativeFunction(base.add(RVA.Entity_get_isDead), 'bool', ['pointer', 'pointer']);
            } catch(e) { isDeadFn = null; }
            getTransformFn = new NativeFunction(base.add(RVA.Component_get_transform), 'pointer', ['pointer', 'pointer']);
            getChildCountFn = new NativeFunction(base.add(RVA.Transform_get_childCount), 'int', ['pointer', 'pointer']);
            getChildFn = new NativeFunction(base.add(RVA.Transform_GetChild), 'pointer', ['pointer', 'int', 'pointer']);
            log('✅ 初始化完成');
            return true;
        } catch(e) {
            log('❌ 初始化失败: ' + e.message);
            return false;
        }
    }

    // ================================================================
    // 获取 GM
    // ================================================================
    function getGM() {
        try {
            var base = getGameAssembly().base;
            var mi = base.add(RVA.GM_Singleton_MethodInfo).readPointer();
            var gm = singletonGetter(mi);
            return gm;
        } catch(e) {
            return null;
        }
    }

    // ================================================================
    // 工具函数
    // ================================================================
    function readList(listPtr, name) {
        var result = [];
        if (!listPtr || listPtr.isNull()) return result;
        try {
            var items = safeReadPointer(listPtr.add(OFF.List_items));
            var count = safeReadU32(listPtr.add(OFF.List_size));
            
            for (var i = 0; i < count; i++) {
                var elem = safeReadPointer(items.add(OFF.Arr_data + i * OFF.ptrSize));
                if (elem && !elem.isNull()) result.push(elem);
            }
        } catch(e) {}
        return result;
    }

    function readArray(arrPtr, name) {
        var result = [];
        if (!arrPtr || arrPtr.isNull()) return result;
        try {
            var len = safeReadU32(arrPtr.add(OFF.Arr_len));
            
            for (var i = 0; i < len; i++) {
                var elem = safeReadPointer(arrPtr.add(OFF.Arr_data + i * OFF.ptrSize));
                if (elem && !elem.isNull()) result.push(elem);
            }
        } catch(e) {}
        return result;
    }

    function getAllPlayers(gm) {
        var map = {};
        
        var allPlayersPtr = safeReadPointer(gm.add(OFF.GM_allPlayers));
        var arr = readArray(allPlayersPtr, 'allPlayers');
        for (var i = 0; i < arr.length; i++) map[arr[i].toString()] = arr[i];
        
        var playersBLPtr = safeReadPointer(gm.add(OFF.GM_playersBL));
        var bl = readList(playersBLPtr, 'playersBL');
        for (var i = 0; i < bl.length; i++) map[bl[i].toString()] = bl[i];
        
        var playersGRPtr = safeReadPointer(gm.add(OFF.GM_playersGR));
        var gr = readList(playersGRPtr, 'playersGR');
        for (var i = 0; i < gr.length; i++) map[gr[i].toString()] = gr[i];
        
        var players = Object.values(map);
        return players;
    }

    // ================================================================
    // 核心逻辑 - 修改玩家（只在需要时打印）
    // ================================================================
    function getTeam(player) {
        try {
            if (getTeamFn) return getTeamFn(player, ptr(0));
            return player.add(OFF.E_team).readS32();
        } catch(e) {
            return -1;
        }
    }

    function isDead(player) {
        try {
            if (isDeadFn) return isDeadFn(player, ptr(0));
            return false;
        } catch(e) {
            return false;
        }
    }

    function recursiveScaleTransform(transform) {
        if (!transform || transform.isNull()) return;

        try {
            scaleVecBuffer.writeFloat(state.hitboxScale);
            scaleVecBuffer.add(4).writeFloat(state.hitboxScale);
            scaleVecBuffer.add(8).writeFloat(state.hitboxScale);
            setLocalScaleFn(transform, scaleVecBuffer);

            var count = getChildCountFn(transform, ptr(0));
            if (count > 0 && count < 200) {
                for (var i = 0; i < count; i++) {
                    var child = getChildFn(transform, i, ptr(0));
                    recursiveScaleTransform(child);
                }
            }
        } catch(e) {}
    }

    function processPlayer(player, playerIndex, shouldLog) {
        var key = player.toString();
        if (processedEntities[key]) {
            return;
        }

        if (shouldLog) {
            log('┌─────────────────────────────────────────────');
            log('│ 👤 玩家 ' + playerIndex + ': ' + key);
        }

        try {
            var isMy = false;
            try { isMy = isMyPlayerFn(player, ptr(0)); } catch(e) {}
            if (shouldLog) log('│ 🔍 isMyPlayer: ' + isMy);

            if (isMy) {
                if (shouldLog) {
                    log('│ ⏭️  跳过自己');
                    log('└─────────────────────────────────────────────');
                }
                return;
            }

            if (isDead(player)) {
                if (shouldLog) {
                    log('│ ⏭️  跳过死亡玩家');
                    log('└─────────────────────────────────────────────');
                }
                return;
            }

            var team = getTeam(player);
            var isEnemy = (myTeam === 2) || (team === 2) || (myTeam !== team);
            var isAlly = !isEnemy;

            if (shouldLog) log('│ 🔍 team: ' + team + ' isEnemy: ' + isEnemy);

            if (isEnemy && !state.targetEnemy) {
                if (shouldLog) {
                    log('│ ⏭️  跳过敌方');
                    log('└─────────────────────────────────────────────');
                }
                return;
            }

            if (isAlly && !state.targetAlly) {
                if (shouldLog) {
                    log('│ ⏭️  跳过我方');
                    log('└─────────────────────────────────────────────');
                }
                return;
            }

            var characterModelPtr = player.add(OFF.Player_currentCharacter);
            var characterModel = safeReadPointer(characterModelPtr);
            if (shouldLog) log('│ 🔍 CharacterModel: ' + characterModel + ' (valid: ' + isPointerValid(characterModel) + ')');

            if (!characterModel || characterModel.isNull()) {
                if (shouldLog) {
                    log('│ ❌ CharacterModel 为空');
                    log('└─────────────────────────────────────────────');
                }
                return;
            }

            var modelTransform = getTransformFn(characterModel, ptr(0));
            if (shouldLog) log('│ 🔍 modelTransform: ' + modelTransform + ' (valid: ' + isPointerValid(modelTransform) + ')');

            if (!modelTransform || modelTransform.isNull()) {
                if (shouldLog) {
                    log('│ ❌ 获取 Transform 失败');
                    log('└─────────────────────────────────────────────');
                }
                return;
            }

            if (shouldLog) log('│ 🔍 递归缩放全身（' + state.hitboxScale + 'x）');
            recursiveScaleTransform(modelTransform);
            processedEntities[key] = true;
            if (shouldLog) log('│ ✅ 全身缩放完成');
        } catch(e) {
            if (shouldLog) log('│ ❌ 异常: ' + e.message);
        }
        if (shouldLog) log('└─────────────────────────────────────────────');
    }

    // ================================================================
    // 主逻辑（每帧执行修改，但每3秒才输出日志）
    // ================================================================
    function mainLogic() {
        if (!state.enabled) return;

        try {
            var now = Date.now();
            var shouldLog = (now - lastLogTime) >= LOG_INTERVAL;
            if (shouldLog) lastLogTime = now;

            var gm = getGM();
            if (!gm || gm.isNull()) return;

            var allPlayers = getAllPlayers(gm);

            if (!myPlayer || myPlayer.isNull()) {
                for (var i = 0; i < allPlayers.length; i++) {
                    try {
                        if (isMyPlayerFn(allPlayers[i], ptr(0))) {
                            myPlayer = allPlayers[i];
                            myTeam = getTeam(myPlayer);
                            break;
                        }
                    } catch(e) {}
                }
                if (!myPlayer) return;
            }

            try {
                if (!isMyPlayerFn(myPlayer, ptr(0))) {
                    myPlayer = null;
                    myTeam = -1;
                    return;
                }
            } catch(e) {
                myPlayer = null;
                myTeam = -1;
                return;
            }

            if (shouldLog && !hasLogged) {
                log('📊 总玩家数: ' + allPlayers.length + ' (只打印前5个玩家的详情)');
                hasLogged = true;
            }

            for (var i = 0; i < allPlayers.length; i++) {
                var playerShouldLog = shouldLog && (i < 5);
                processPlayer(allPlayers[i], i, playerShouldLog);
            }
        } catch(e) {}
    }

    // ================================================================
    // 安装 Hook
    // ================================================================
    function installHook() {
        var mod = getGameAssembly();
        if (!mod) return false;
        var base = mod.base;

        try {
            var playerUpdateAddr = base.add(RVA.Player_Update);

            playerUpdateHook = Interceptor.attach(playerUpdateAddr, {
                onEnter: function(args) {
                    if (state.enabled) {
                        setTimeout(mainLogic, 0);
                    }
                }
            });

            log('✅ Player.Update Hook 已安装');
            return true;
        } catch(e) {
            log('❌ Hook 安装失败: ' + e.message);
            return false;
        }
    }

    // ================================================================
    // 公开接口
    // ================================================================
    rpc.exports = {
        installhook: function() {
            log('🚀 正在启动...');
            hasLogged = false;
            processedEntities = {};
            lastLogTime = 0;

            if (!initNativeFunctions()) {
                return { ok: false, error: '初始化失败' };
            }

            if (!playerUpdateHook) {
                if (!installHook()) {
                    return { ok: false, error: 'Hook 安装失败' };
                }
            }

            return { ok: true };
        },

        setconfig: function(hitboxScale, targetEnemy, targetAlly) {
            state.hitboxScale = hitboxScale;
            if (state.hitboxScale < 1.0) state.hitboxScale = 1.0;
            if (state.hitboxScale > 3.0) state.hitboxScale = 3.0;
            state.targetEnemy = targetEnemy;
            state.targetAlly = targetAlly;
            state.enabled = state.hitboxScale !== 1.0;

            processedEntities = {};
            hasLogged = false;
            lastLogTime = 0;

            var targetStr = '';
            if (state.targetEnemy) targetStr += '敌方';
            if (state.targetAlly) targetStr += (targetStr ? '+' : '') + '我方';

            log('⚙️ 配置已更新 - 缩放: ' + state.hitboxScale + 'x / 目标: ' + targetStr);
            sendStatus('扩大受击范围', state.enabled);

            return { ok: true };
        },

        resetall: function() {
            state.enabled = false;
            state.hitboxScale = 1.0;
            state.targetEnemy = true;
            state.targetAlly = false;
            processedEntities = {};
            hasLogged = false;
            lastLogTime = 0;
            log('🔄 已重置');
            sendStatus('扩大受击范围', false);
            return { ok: true };
        },

        getstatus: function() {
            return {
                enabled: state.enabled,
                hitboxScale: state.hitboxScale,
                targetEnemy: state.targetEnemy,
                targetAlly: state.targetAlly,
                haveGM: getGM() != null
            };
        },

        startmonitor: function() { return { ok: true }; },
        stopmonitor: function() { return { ok: true }; }
    };

    log('✅ 脚本加载完成 (v2.7 时间控制版)');
})();
