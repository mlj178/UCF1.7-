// 多人生化角色变身。
// RPC 线程只提交动作；所有游戏原生调用都由 ModeBase.Update 主线程钩子执行。

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';
    var MAX_PLAYER_SLOTS = 64;

    var RVA = {
        ModeBase_Update: 0x00AF6A00,
        GameManager_TypeInfo: 0x00E2933C,
        Singleton_GameManager_get_instance: 0x004A8170,
        SingletonGameManager_get_instance_Method: 0x00E1CE64,
        Mode_Nano4_get_instance3: 0x00B467A0,
        NanoRoleSelect_OpenMasterRole: 0x00B4ED30,
        Mode_Nano4_Terminator_BecomeRandomMasterHero: 0x00B42E90,
        Mode_Nano4_Terminator_TryBecomeRandomMasterTerminator: 0x00B45B90,
        Player_get_isMyPlayer: 0x00B55FD0,
        HealthData_get_isDead: 0x00AE4830
    };

    var OFF = {
        Il2CppClass_static_fields: 0x5C,
        GameManager_myPlayer: 0x00,
        GameManager_allPlayers: 0x1C,
        Player_healthData: 0x1C,
        Player_clientData: 0x94,
        Player_nanoRoleSelect: 0xA8,
        Player_isRespawning: 0xD8,
        ClientData_isBot: 0x1C,
        Il2CppArray_length: 0x0C,
        Il2CppArray_items: 0x10
    };

    var VALID_ACTIONS = {
        local_hero: true,
        local_terminator: true,
        bot_hero: true,
        bot_terminator: true
    };

    var Runtime = {
        feature_id: "role_transform",
        enabled: false,
        initialized: false,
        consuming: false,
        generation: 0,
        module: null,
        base: ptr(0),
        hooks: [],
        pendingAction: "",
        stats: {
            requests: 0,
            rejected: 0,
            main_thread_consumed: 0,
            local_hero_applied: 0,
            local_terminator_applied: 0,
            bot_hero_applied: 0,
            bot_terminator_applied: 0,
            bots_scanned: 0,
            bots_skipped: 0,
            error_count: 0,
            cleanup_count: 0,
            last_action: "",
            last_result: "",
            last_error: ""
        }
    };

    var Native = {
        ready: false,
        getGameManager: null,
        getModeNano4: null,
        openMasterRole: null,
        becomeRandomMasterHero: null,
        tryBecomeRandomMasterTerminator: null,
        isMyPlayer: null,
        isDead: null
    };

    function log(level, message) {
        console.log('[' + Runtime.feature_id + '][' + level + '] ' + message);
        try {
            send({ type: 'log', level: level, module: Runtime.feature_id, message: message });
        } catch (_) {}
    }

    function fail(where, error) {
        Runtime.stats.error_count += 1;
        Runtime.stats.last_error = where + ': ' + (error && error.message ? error.message : String(error));
        Runtime.stats.last_result = 'error';
        log('error', Runtime.stats.last_error);
    }

    function reject(reason) {
        Runtime.stats.rejected += 1;
        Runtime.stats.last_error = reason;
        Runtime.stats.last_result = 'rejected';
        log('warning', reason);
    }

    function isNull(value) {
        try { return !value || value.isNull(); } catch (_) { return true; }
    }

    function readable(value) {
        try {
            if (isNull(value)) return false;
            value.readPointer();
            return true;
        } catch (_) {
            return false;
        }
    }

    function ensureNative() {
        if (Native.ready) return true;
        Runtime.module = Process.findModuleByName(MODULE_NAME);
        if (!Runtime.module) {
            Runtime.stats.last_error = MODULE_NAME + ' not found';
            return false;
        }
        if (Process.arch !== 'ia32' || Process.pointerSize !== 4) {
            Runtime.stats.last_error = 'only 32-bit GameAssembly is supported';
            return false;
        }
        try {
            Runtime.base = Runtime.module.base;
            Native.getGameManager = new NativeFunction(Runtime.base.add(RVA.Singleton_GameManager_get_instance), 'pointer', ['pointer'], CALL_CONV);
            Native.getModeNano4 = new NativeFunction(Runtime.base.add(RVA.Mode_Nano4_get_instance3), 'pointer', ['pointer'], CALL_CONV);
            Native.openMasterRole = new NativeFunction(Runtime.base.add(RVA.NanoRoleSelect_OpenMasterRole), 'void', ['pointer', 'int', 'pointer'], CALL_CONV);
            Native.becomeRandomMasterHero = new NativeFunction(Runtime.base.add(RVA.Mode_Nano4_Terminator_BecomeRandomMasterHero), 'void', ['pointer', 'pointer', 'int', 'pointer'], CALL_CONV);
            Native.tryBecomeRandomMasterTerminator = new NativeFunction(Runtime.base.add(RVA.Mode_Nano4_Terminator_TryBecomeRandomMasterTerminator), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
            Native.isMyPlayer = new NativeFunction(Runtime.base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer'], CALL_CONV);
            Native.isDead = new NativeFunction(Runtime.base.add(RVA.HealthData_get_isDead), 'bool', ['pointer', 'pointer'], CALL_CONV);
            Native.ready = true;
            return true;
        } catch (error) {
            fail('ensureNative', error);
            return false;
        }
    }

    function getMyPlayer() {
        try {
            var typeInfo = Runtime.base.add(RVA.GameManager_TypeInfo).readPointer();
            if (!readable(typeInfo)) return ptr(0);
            var staticFields = typeInfo.add(OFF.Il2CppClass_static_fields).readPointer();
            if (!readable(staticFields)) return ptr(0);
            return staticFields.add(OFF.GameManager_myPlayer).readPointer();
        } catch (error) {
            fail('GameManager.myPlayer', error);
            return ptr(0);
        }
    }

    function getGameManager() {
        try {
            var methodInfo = Runtime.base.add(RVA.SingletonGameManager_get_instance_Method).readPointer();
            if (!readable(methodInfo)) return ptr(0);
            return Native.getGameManager(methodInfo);
        } catch (error) {
            fail('Singleton<GameManager>.get_instance', error);
            return ptr(0);
        }
    }

    function isLocalPlayer(player) {
        if (!readable(player)) return false;
        try {
            return !!Native.isMyPlayer(player, ptr(0));
        } catch (error) {
            fail('Player.get_isMyPlayer', error);
            return false;
        }
    }

    function isBotPlayer(player) {
        if (!readable(player)) return false;
        try {
            var clientData = player.add(OFF.Player_clientData).readPointer();
            return readable(clientData) && clientData.add(OFF.ClientData_isBot).readU8() !== 0;
        } catch (error) {
            fail('ClientData.isBot', error);
            return false;
        }
    }

    function isDeadPlayer(player) {
        if (!readable(player)) return true;
        try {
            var healthData = player.add(OFF.Player_healthData).readPointer();
            if (!readable(healthData)) return true;
            return !!Native.isDead(healthData, ptr(0));
        } catch (error) {
            fail('HealthData.get_isDead', error);
            return true;
        }
    }

    function isRespawningPlayer(player) {
        if (!readable(player)) return true;
        try {
            return player.add(OFF.Player_isRespawning).readU8() !== 0;
        } catch (error) {
            fail('Player.isRespawning', error);
            return true;
        }
    }

    function applyLocalSelection(isHero) {
        var player = getMyPlayer();
        if (!readable(player) || !isLocalPlayer(player)) {
            reject('local player is unavailable');
            return;
        }
        try {
            var selector = player.add(OFF.Player_nanoRoleSelect).readPointer();
            if (!readable(selector)) {
                reject('NanoRoleSelect is unavailable');
                return;
            }
            Native.openMasterRole(selector, isHero ? 1 : 0, ptr(0));
            var action = isHero ? 'local_hero' : 'local_terminator';
            Runtime.stats[action + '_applied'] += 1;
            Runtime.stats.last_result = 'native selector opened';
        } catch (error) {
            fail('NanoRoleSelect.OpenMasterRole', error);
        }
    }

    function forEachEligibleBot(callback) {
        var manager = getGameManager();
        if (!readable(manager)) {
            reject('GameManager is unavailable');
            return 0;
        }
        var applied = 0;
        try {
            var players = manager.add(OFF.GameManager_allPlayers).readPointer();
            if (!readable(players)) {
                reject('GameManager.allPlayers is unavailable');
                return 0;
            }
            var count = players.add(OFF.Il2CppArray_length).readU32();
            if (count > MAX_PLAYER_SLOTS) count = MAX_PLAYER_SLOTS;
            for (var index = 0; index < count; index += 1) {
                Runtime.stats.bots_scanned += 1;
                var player = players.add(OFF.Il2CppArray_items + index * Process.pointerSize).readPointer();
                if (!isBotPlayer(player) || isLocalPlayer(player) || isDeadPlayer(player) || isRespawningPlayer(player)) {
                    Runtime.stats.bots_skipped += 1;
                    continue;
                }
                try {
                    callback(player);
                    applied += 1;
                } catch (error) {
                    fail('bot transform index ' + index, error);
                }
            }
        } catch (error) {
            fail('GameManager.allPlayers', error);
        }
        return applied;
    }

    function applyBotTransform(mode, isHero) {
        var applied = forEachEligibleBot(function (player) {
            if (isHero) {
                Native.becomeRandomMasterHero(mode, player, 0, ptr(0));
            } else {
                Native.tryBecomeRandomMasterTerminator(mode, player, ptr(0));
            }
        });
        var action = isHero ? 'bot_hero' : 'bot_terminator';
        Runtime.stats[action + '_applied'] += applied;
        Runtime.stats.last_result = 'applied to ' + applied + ' bot(s)';
        log('info', action + ': ' + Runtime.stats.last_result);
    }

    function executeAction(action) {
        Runtime.stats.last_action = action;
        Runtime.stats.last_error = '';
        if (!Runtime.enabled || !ensureNative()) {
            reject('feature is not ready');
            return;
        }
        var mode = Native.getModeNano4(ptr(0));
        if (!readable(mode)) {
            reject('Mode_Nano4.instance3 is unavailable');
            return;
        }
        if (action === 'local_hero') {
            applyLocalSelection(true);
            return;
        }
        if (action === 'local_terminator') {
            applyLocalSelection(false);
            return;
        }
        applyBotTransform(mode, action === 'bot_hero');
    }

    function consumePendingAction() {
        if (!Runtime.enabled || Runtime.consuming) return;
        var action = Runtime.pendingAction;
        Runtime.pendingAction = "";
        if (!action) return;
        Runtime.consuming = true;
        Runtime.stats.main_thread_consumed += 1;
        try {
            executeAction(action);
        } catch (error) {
            fail('executeAction:' + action, error);
        } finally {
            Runtime.consuming = false;
        }
    }

    function attachHooks() {
        var updateHook = Interceptor.attach(Runtime.base.add(RVA.ModeBase_Update), {
            onEnter: function () {
                consumePendingAction();
            }
        });
        Runtime.hooks.push(updateHook);
        log('info', 'ModeBase.Update main-thread action hook installed');
    }

    function cleanupHooks() {
        Runtime.hooks.forEach(function (hook) {
            try { hook.detach(); } catch (_) {}
        });
        Runtime.hooks = [];
    }

    function clearNative() {
        Object.keys(Native).forEach(function (key) {
            Native[key] = key === 'ready' ? false : null;
        });
    }

    function resetRuntime(reason) {
        cleanupHooks();
        Runtime.pendingAction = "";
        Runtime.consuming = false;
        Runtime.initialized = false;
        Runtime.enabled = false;
        Runtime.generation += 1;
        Runtime.module = null;
        Runtime.base = ptr(0);
        clearNative();
        log('info', 'resetRuntime: ' + reason);
    }

    function enableFeature() {
        if (!Runtime.initialized) {
            if (!ensureNative()) return status();
            try {
                attachHooks();
                Runtime.initialized = true;
            } catch (error) {
                fail('attachHooks', error);
                resetRuntime('attach failed');
                return status();
            }
        }
        Runtime.enabled = true;
        Runtime.stats.last_error = '';
        log('info', 'enabled');
        return status();
    }

    function disableFeature() {
        resetRuntime('disabled');
        return status();
    }

    function cleanupFeature() {
        Runtime.stats.cleanup_count += 1;
        resetRuntime('cleanup');
        return status();
    }

    function updateConfig(_config) {
        return status();
    }

    function queueAction(action) {
        if (!VALID_ACTIONS[action]) {
            reject('unknown action: ' + action);
            return status();
        }
        if (!Runtime.enabled || !Runtime.initialized) {
            reject('feature is disabled');
            return status();
        }
        if (Runtime.pendingAction) {
            reject('another action is pending');
            return status();
        }
        Runtime.pendingAction = action;
        Runtime.stats.requests += 1;
        Runtime.stats.last_action = action;
        Runtime.stats.last_result = 'queued';
        return status();
    }

    function status() {
        return {
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            generation: Runtime.generation,
            pending: Runtime.pendingAction,
            stats: Runtime.stats
        };
    }

    rpc.exports = {
        enable: enableFeature,
        disable: disableFeature,
        status: status,
        cleanup: cleanupFeature,
        trigger: queueAction,
        setConfig: updateConfig,
        set_config: updateConfig,
        setconfig: updateConfig
    };
})();
