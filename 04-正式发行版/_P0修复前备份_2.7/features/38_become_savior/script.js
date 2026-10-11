// ============================================================
// script.js — 直接变身救世主 (feature_id: "become_savior")
//
// 功能目标：多人生化模式下，一键让本地玩家/存活 Bot 变成救世主。
//
// 实现原理：
//   1. RPC 只提交 pending 动作；所有原生调用在 ModeBase.Update 主线程执行。
//   2. 变身走游戏自带 Mode_Nano4_Terminator.BecomeSavior：
//      当前 nanoRole == Soldier(0) 时 BecomeHero(18) 并送武器 4270。
//
// RVA / 字段来源（dump.cs + IDA 已确认）：
//   ModeBase_Update:                     0x00AF6A00
//   GameManager_TypeInfo:               0x00E2933C
//   Singleton_GameManager_get_instance: 0x004A8170
//   SingletonGameManager_get_instance:   0x00E1CE64
//   Mode_Nano4_get_instance3:            0x00B467A0
//   Mode_Nano4_Terminator_BecomeSavior:  0x00B42F60
//   Player_get_isMyPlayer:               0x00B55FD0
//   HealthData_get_isDead:               0x00AE4830
//   GameManager.myPlayer:                +0x00
//   GameManager.gameMode:                +0x04
//   GameManager.allPlayers:              +0x1C
//   Player.healthData:                   +0x1C
//   Player.clientData:                   +0x94
//   Player.playerData:                   +0x98
//   ClientData.isBot:                    +0x1C
//   PlayerData.nanoRole:                 +0x60
//   SubscribeableProperty.value:         +0x00
//   NanoRole.Savior = 18
//
// 限制：
//   - 仅多人生化相关 nano 模式（gameMode 3-6）。
//   - 目标当前必须是佣兵（nanoRole==0），已是英雄/终结者会跳过。
// ============================================================

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';
    var MAX_PLAYER_SLOTS = 64;
    var NANO_MODE_MIN = 3;
    var NANO_MODE_MAX = 6;
    var NANO_ROLE_SOLDIER = 0;
    var NANO_ROLE_SAVIOR = 18;
    var SAVIOR_WEAPON_ID = 4270;

    var RVA = {
        ModeBase_Update: 0x00AF6A00,
        GameManager_TypeInfo: 0x00E2933C,
        Singleton_GameManager_get_instance: 0x004A8170,
        SingletonGameManager_get_instance_Method: 0x00E1CE64,
        Mode_Nano4_get_instance3: 0x00B467A0,
        ModeBase_Nano_UpdateNanoRole: 0x00AF4FF0,
        GameManager_GiveWeapon: 0x00AFB390,
        Player_get_isMyPlayer: 0x00B55FD0,
        Player_get_nanoRole: 0x00B56200,
        HealthData_get_isDead: 0x00AE4830
    };

    var OFF = {
        Il2CppClass_static_fields: 0x5C,
        GameManager_myPlayer: 0x00,
        GameManager_gameMode: 0x04,
        GameManager_allPlayers: 0x1C,
        Player_healthData: 0x1C,
        Player_clientData: 0x94,
        Player_playerData: 0x98,
        ClientData_isBot: 0x1C,
        // PlayerData.nanoRole -> SubscribeableProperty 对象；value 在对象头(klass+monitor=8)之后
        PlayerData_nanoRole: 0x60,
        SubscribeableProperty_value: 0x08,
        Il2CppArray_length: 0x0C,
        Il2CppArray_items: 0x10
    };

    var VALID_ACTIONS = {
        local_savior: true,
        bot_savior: true
    };

    var Runtime = {
        feature_id: 'become_savior',
        enabled: false,
        initialized: false,
        consuming: false,
        generation: 0,
        module: null,
        base: ptr(0),
        hooks: [],
        pendingAction: '',
        config: {
            require_enabled_for_actions: true
        },
        stats: {
            requests: 0,
            rejected: 0,
            main_thread_consumed: 0,
            local_savior_applied: 0,
            bot_savior_applied: 0,
            bots_scanned: 0,
            bots_skipped: 0,
            error_count: 0,
            cleanup_count: 0,
            last_action: '',
            last_result: '',
            last_error: ''
        }
    };

    var Native = {
        ready: false,
        getGameManager: null,
        getModeNano4: null,
        updateNanoRole: null,
        giveWeapon: null,
        isMyPlayer: null,
        getNanoRole: null,
        isDead: null
    };

    function log(level, message) {
        var text = '[' + Runtime.feature_id + '] ' + message;
        if (level === 'error') console.error(text);
        else if (level === 'warn') console.warn(text);
        else console.log(text);
        try {
            send({ type: 'log', level: level, module: Runtime.feature_id, message: message });
        } catch (_) {}
    }

    function sendStatus(feature, enabled) {
        try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (_) {}
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
        log('warn', reason);
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
            Native.updateNanoRole = new NativeFunction(Runtime.base.add(RVA.ModeBase_Nano_UpdateNanoRole), 'void', ['pointer', 'pointer', 'int', 'pointer'], CALL_CONV);
            // GiveWeapon(Player, int, bool autoGiveUp, bool autoSelect, MethodInfo*) -> Weapon*
            Native.giveWeapon = new NativeFunction(Runtime.base.add(RVA.GameManager_GiveWeapon), 'pointer', ['pointer', 'int', 'int', 'int', 'pointer'], CALL_CONV);
            Native.isMyPlayer = new NativeFunction(Runtime.base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer'], CALL_CONV);
            Native.getNanoRole = new NativeFunction(Runtime.base.add(RVA.Player_get_nanoRole), 'int', ['pointer', 'pointer'], CALL_CONV);
            Native.isDead = new NativeFunction(Runtime.base.add(RVA.HealthData_get_isDead), 'bool', ['pointer', 'pointer'], CALL_CONV);
            Native.ready = true;
            return true;
        } catch (error) {
            fail('ensureNative', error);
            return false;
        }
    }

    function getGameMode() {
        try {
            var typeInfo = Runtime.base.add(RVA.GameManager_TypeInfo).readPointer();
            if (!readable(typeInfo)) return -1;
            var staticFields = typeInfo.add(OFF.Il2CppClass_static_fields).readPointer();
            if (!readable(staticFields)) return -1;
            return staticFields.add(OFF.GameManager_gameMode).readS32();
        } catch (error) {
            fail('GameManager.gameMode', error);
            return -1;
        }
    }

    function isNanoGameMode() {
        var gameMode = getGameMode();
        return gameMode >= NANO_MODE_MIN && gameMode <= NANO_MODE_MAX;
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

    function getNanoRole(player) {
        if (!readable(player)) return -1;
        // 优先走原生 getter，避免 SubscribeableProperty 对象头偏移踩坑
        if (Native.getNanoRole) {
            try {
                return Native.getNanoRole(player, ptr(0));
            } catch (error) {
                fail('Player.get_nanoRole', error);
            }
        }
        try {
            var playerData = player.add(OFF.Player_playerData).readPointer();
            if (!readable(playerData)) return -1;
            var nanoRole = playerData.add(OFF.PlayerData_nanoRole).readPointer();
            if (!readable(nanoRole)) return -1;
            return nanoRole.add(OFF.SubscribeableProperty_value).readS32();
        } catch (error) {
            fail('PlayerData.nanoRole', error);
            return -1;
        }
    }

    function tryBecomeSavior(player) {
        var role = getNanoRole(player);
        var mode = Native.getModeNano4(ptr(0));
        if (!readable(mode)) {
            reject('Mode_Nano4.instance3 is unavailable');
            return false;
        }

        // 已是救世主：尝试补枪，不再改角色
        if (role === NANO_ROLE_SAVIOR) {
            try {
                Native.giveWeapon(player, SAVIOR_WEAPON_ID, 0, 1, ptr(0));
                Runtime.stats.last_result = 'already savior, weapon re-given';
                return true;
            } catch (error) {
                fail('GameManager.GiveWeapon(already savior)', error);
                return false;
            }
        }

        if (role !== NANO_ROLE_SOLDIER) {
            Runtime.stats.last_result = 'skipped: nanoRole=' + role + ' (need Soldier=0)';
            logOnceSkip(role);
            return false;
        }

        try {
            Native.updateNanoRole(mode, player, NANO_ROLE_SAVIOR, ptr(0));
        } catch (error) {
            fail('ModeBase_Nano.UpdateNanoRole', error);
            return false;
        }

        try {
            Native.giveWeapon(player, SAVIOR_WEAPON_ID, 0, 1, ptr(0));
        } catch (error) {
            // 角色已改成功，武器失败不整体判负
            fail('GameManager.GiveWeapon', error);
            Runtime.stats.last_result = 'role set, weapon failed';
            return true;
        }

        var after = getNanoRole(player);
        if (after === NANO_ROLE_SAVIOR) {
            Runtime.stats.last_result = 'became savior + weapon';
            return true;
        }
        Runtime.stats.last_result = 'UpdateNanoRole returned, role=' + after;
        return false;
    }

    var _lastSkipRoleLogged = -999;
    function logOnceSkip(role) {
        if (role === _lastSkipRoleLogged) return;
        _lastSkipRoleLogged = role;
        log('warn', 'skip transform: nanoRole=' + role + ' (need Soldier=0); first time only per value');
    }

    function applyLocalSavior() {
        var player = getMyPlayer();
        if (!readable(player) || !isLocalPlayer(player)) {
            reject('local player is unavailable');
            return;
        }
        if (tryBecomeSavior(player)) {
            Runtime.stats.local_savior_applied += 1;
            Runtime.stats.last_result = 'local became savior';
            log('info', 'local_savior applied');
        } else {
            log('warn', 'local_savior failed: ' + Runtime.stats.last_result);
        }
    }

    function applyBotSaviors() {
        var manager = getGameManager();
        if (!readable(manager)) {
            reject('GameManager is unavailable');
            return;
        }
        var applied = 0;
        try {
            var players = manager.add(OFF.GameManager_allPlayers).readPointer();
            if (!readable(players)) {
                reject('GameManager.allPlayers is unavailable');
                return;
            }
            var count = players.add(OFF.Il2CppArray_length).readU32();
            if (count > MAX_PLAYER_SLOTS) count = MAX_PLAYER_SLOTS;
            for (var index = 0; index < count; index += 1) {
                Runtime.stats.bots_scanned += 1;
                var player = players.add(OFF.Il2CppArray_items + index * Process.pointerSize).readPointer();
                if (!isBotPlayer(player) || isLocalPlayer(player) || isDeadPlayer(player)) {
                    Runtime.stats.bots_skipped += 1;
                    continue;
                }
                if (tryBecomeSavior(player)) {
                    applied += 1;
                }
            }
        } catch (error) {
            fail('GameManager.allPlayers', error);
        }
        Runtime.stats.bot_savior_applied += applied;
        Runtime.stats.last_result = 'applied to ' + applied + ' bot(s)';
        log('info', 'bot_savior: ' + Runtime.stats.last_result);
    }

    function executeAction(action) {
        Runtime.stats.last_action = action;
        Runtime.stats.last_error = '';
        if (!Runtime.enabled || !ensureNative()) {
            reject('feature is not ready');
            return;
        }
        if (!isNanoGameMode()) {
            reject('not in multiplayer-nano mode');
            return;
        }
        if (action === 'local_savior') {
            applyLocalSavior();
            return;
        }
        applyBotSaviors();
    }

    function consumePendingAction() {
        if (!Runtime.enabled || Runtime.consuming) return;
        var action = Runtime.pendingAction;
        Runtime.pendingAction = '';
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
        Runtime.pendingAction = '';
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
        sendStatus(Runtime.feature_id, true);
        log('info', 'enabled');
        return status();
    }

    function disableFeature() {
        resetRuntime('disabled');
        sendStatus(Runtime.feature_id, false);
        log('info', 'disabled');
        return status();
    }

    function cleanupFeature() {
        Runtime.stats.cleanup_count += 1;
        resetRuntime('cleanup');
        return status();
    }

    function updateConfig(config) {
        config = config || {};
        if (typeof config.require_enabled_for_actions !== 'undefined') {
            Runtime.config.require_enabled_for_actions = !!config.require_enabled_for_actions;
        }
        return status();
    }

    function queueAction(actionOrPayload) {
        var action = typeof actionOrPayload === 'string'
            ? actionOrPayload
            : actionOrPayload && actionOrPayload.action;
        if (!VALID_ACTIONS[action]) {
            reject('unknown action: ' + action);
            return status();
        }
        if (Runtime.config.require_enabled_for_actions && (!Runtime.enabled || !Runtime.initialized)) {
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
            local_savior_applied: Runtime.stats.local_savior_applied,
            bot_savior_applied: Runtime.stats.bot_savior_applied,
            bots_scanned: Runtime.stats.bots_scanned,
            bots_skipped: Runtime.stats.bots_skipped,
            error_count: Runtime.stats.error_count,
            last_error: Runtime.stats.last_error,
            last_result: Runtime.stats.last_result,
            last_action: Runtime.stats.last_action
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

    log('info', 'script loaded');
})();
