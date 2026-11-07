// ============================================================
// script.js — 增加血量 (feature_id: "hp_boost")
//
// 功能目标：开启开关后，每触发一次快捷键(F3)/点一次按钮，就为本地玩家加一次血
//          （同时提升 maxHealth 上限，满血也能往上加）。
//
// 实现原理：
//   1. Hook Player.Update（主线程），拿到每帧的 Player* 参数。
//   2. addhp RPC 只设置 pending.addHp = true（不直接写游戏对象）。
//   3. Player.Update 命中本地玩家(get_isMyPlayer)后，读 healthData(0x1C)，
//      调用原游戏 HealthData.AddHealthMax(add_amount, heal=1)，并立即清 pending。
//   4. 不用 HealthData.Heal(int)：IDA 解码确认其内部 Math.Min(新血量, maxHealth)
//      封顶，满血时调用无效（游戏内实测验证）。AddHealthMax 会同时提升
//      currentHealth 和 maxHealth，可无限叠加。
//   5. 不直接写 currentHealth/maxHealth（ObscuredInt 加密值），走游戏原生方法。
//
// RVA / 字段来源（dump.cs + IDA 汇编 + dev/ 探测日志 2026-09-09 实测验证）：
//   Player_Update:                0x00B551D0
//   Player_get_isMyPlayer:        0x00B55FD0
//   HealthData_AddHealthMax:      0x00AE4260   // void AddHealthMax(int addHP, bool heal)
//   Entity.healthData:            0x1C         // HealthData*
//
// 踩坑记录：
//   - AddHealthMax 的 bool 参数在 NativeFunction 签名里必须声明 'int' 并传 1/0，
//     本版 Frida x86 mscdecl 不接受 JS true/false（否则抛 expected an integer）。
// ============================================================

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';

    var RVA = {
        Player_Update: 0x00B551D0,
        Player_get_isMyPlayer: 0x00B55FD0,
        HealthData_AddHealthMax: 0x00AE4260
    };

    var OFF = {
        Player_healthData: 0x1C
    };

    var Runtime = {
        feature_id: "hp_boost",
        enabled: false,
        initialized: false,
        generation: 0,
        module: null,
        base: ptr(0),
        hooks: [],
        config: {
            add_amount: 10,
            require_enabled_for_actions: true
        },
        pending: {
            addHp: false
        },
        stats: {
            hookHits: 0,
            isMyPlayerHits: 0,
            healCount: 0,
            skippedNull: 0,
            skippedDisabled: 0,
            errorCount: 0,
            cleanupCount: 0,
            lastError: "",
            lastResetReason: "",
            lastResult: ""
        }
    };

    var native = {
        ready: false,
        isMyPlayer: null,
        addHealthMax: null
    };

    var LogLimiter = {};

    function log(level, message) {
        var text = "[" + Runtime.feature_id + "] " + message;
        if (level === 'error') console.error(text);
        else if (level === 'warn') console.warn(text);
        else console.log(text);
        try {
            send({ type: 'log', level: level, module: Runtime.feature_id, message: message });
        } catch (e) {}
    }

    function sendStatus(feature, enabled) {
        try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (_) {}
    }

    function logOnce(key, level, message, intervalMs) {
        var now = Date.now();
        var wait = intervalMs || 1000;
        if (!LogLimiter[key] || now - LogLimiter[key] >= wait) {
            LogLimiter[key] = now;
            log(level, message);
        }
    }

    function setError(message, error) {
        Runtime.stats.errorCount += 1;
        Runtime.stats.lastError = message + (error && error.message ? ": " + error.message : "");
        logOnce("error:" + message, "error", Runtime.stats.lastError, 1500);
    }

    function isNull(p) {
        return !p || p.isNull();
    }

    function isReadablePtr(p) {
        try {
            if (isNull(p)) return false;
            p.readPointer();
            return true;
        } catch (e) {
            return false;
        }
    }

    function initNativeFunctions() {
        if (native.ready) return true;

        Runtime.module = Process.findModuleByName(MODULE_NAME);
        if (!Runtime.module) {
            Runtime.stats.lastError = MODULE_NAME + " not found";
            return false;
        }

        if (Process.arch !== 'ia32' || Process.pointerSize !== 4) {
            Runtime.stats.lastError = "unsupported process: arch=" + Process.arch + ", pointerSize=" + Process.pointerSize;
            log("error", Runtime.stats.lastError);
            return false;
        }

        Runtime.base = Runtime.module.base;
        try {
            native.isMyPlayer = new NativeFunction(
                Runtime.base.add(RVA.Player_get_isMyPlayer),
                'bool',
                ['pointer', 'pointer'],
                CALL_CONV
            );
            // AddHealthMax(int addHP, bool heal, MethodInfo*) 的 bool 参数走 4 字节栈槽，
            // 本版 Frida x86 mscdecl 只认整数参数，签名声明 'int'、调用传 1。
            native.addHealthMax = new NativeFunction(
                Runtime.base.add(RVA.HealthData_AddHealthMax),
                'void',
                ['pointer', 'int', 'int', 'pointer'],
                CALL_CONV
            );
            native.ready = true;
            return true;
        } catch (error) {
            setError("initNativeFunctions failed", error);
            native.ready = false;
            return false;
        }
    }

    function cleanupHooks() {
        for (var i = 0; i < Runtime.hooks.length; i += 1) {
            try {
                if (Runtime.hooks[i] && Runtime.hooks[i].detach) Runtime.hooks[i].detach();
            } catch (e) {}
        }
        Runtime.hooks = [];
        Runtime.initialized = false;
    }

    function resetRuntime(reason) {
        Runtime.generation += 1;
        Runtime.pending.addHp = false;
        Runtime.stats.lastResetReason = reason || "unknown";
        log("info", "resetRuntime: " + Runtime.stats.lastResetReason + ", gen=" + Runtime.generation);
    }

    function isLocalPlayer(player) {
        if (isNull(player) || !native.ready) {
            Runtime.stats.skippedNull += 1;
            return false;
        }
        if (!isReadablePtr(player)) {
            Runtime.stats.skippedNull += 1;
            return false;
        }
        try {
            if (native.isMyPlayer(player, ptr(0))) {
                Runtime.stats.isMyPlayerHits += 1;
                return true;
            }
            return false;
        } catch (error) {
            setError("isLocalPlayer failed", error);
            return false;
        }
    }

    function healLocalPlayer(player) {
        var healthData = player.add(OFF.Player_healthData).readPointer();
        if (isNull(healthData) || !isReadablePtr(healthData)) {
            Runtime.stats.skippedNull += 1;
            Runtime.stats.lastResult = "health_data_unavailable";
            logOnce("heal:null", "warn", "healthData unavailable", 1500);
            return false;
        }

        var amount = Math.max(1, Math.floor(Number(Runtime.config.add_amount) || 10));
        try {
            native.addHealthMax(healthData, amount, 1, ptr(0));
            Runtime.stats.healCount += 1;
            Runtime.stats.lastResult = "healed +" + amount;
            log("info", "player healed +" + amount + " (max hp +)");
            return true;
        } catch (error) {
            setError("HealthData.AddHealthMax failed", error);
            Runtime.stats.lastResult = "heal_failed";
            return false;
        }
    }

    function onPlayerUpdate(player) {
        Runtime.stats.hookHits += 1;
        if (!Runtime.enabled) return;
        if (!Runtime.pending.addHp) return;

        try {
            if (!native.ready && !initNativeFunctions()) return;
            if (!isLocalPlayer(player)) return;

            // 命中本地玩家，消费本次动作（无论加血是否成功都清 pending，避免卡住）
            Runtime.pending.addHp = false;
            healLocalPlayer(player);
        } catch (error) {
            setError("Player.Update hook failed", error);
        }
    }

    function installHooks() {
        if (Runtime.initialized) return true;
        if (!initNativeFunctions()) return false;

        try {
            var hook = Interceptor.attach(Runtime.base.add(RVA.Player_Update), {
                onEnter: function (args) {
                    onPlayerUpdate(args[0]);
                }
            });
            Runtime.hooks.push(hook);
            Runtime.initialized = true;
            log("info", "Player.Update hook installed @ " + Runtime.base.add(RVA.Player_Update));
            return true;
        } catch (error) {
            setError("installHooks failed", error);
            cleanupHooks();
            return false;
        }
    }

    function enableFeature() {
        if (!installHooks()) return false;
        Runtime.enabled = true;
        Runtime.stats.errorCount = 0;
        Runtime.stats.lastError = "";
        sendStatus(Runtime.feature_id, true);
        log("info", "enabled");
        return true;
    }

    function disableFeature() {
        Runtime.enabled = false;
        sendStatus(Runtime.feature_id, false);
        resetRuntime("disable");
        log("info", "disabled");
        return true;
    }

    function cleanupFeature() {
        Runtime.enabled = false;
        Runtime.stats.cleanupCount += 1;
        try { cleanupHooks(); } catch (e) {}
        resetRuntime("cleanup");
        native.ready = false;
        log("info", "cleanup done");
        return true;
    }

    function updateConfig(config) {
        config = config || {};
        if (typeof config.add_amount !== 'undefined') {
            Runtime.config.add_amount = Math.max(1, Math.floor(Number(config.add_amount) || 10));
        }
        if (typeof config.require_enabled_for_actions !== 'undefined') {
            Runtime.config.require_enabled_for_actions = !!config.require_enabled_for_actions;
        }
        log("info", "config changed: add_amount=" + Runtime.config.add_amount);
        return true;
    }

    function buildStatus() {
        return {
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            generation: Runtime.generation,
            hook_hits: Runtime.stats.hookHits,
            is_my_player_hits: Runtime.stats.isMyPlayerHits,
            heal_count: Runtime.stats.healCount,
            skipped_null: Runtime.stats.skippedNull,
            skipped_disabled: Runtime.stats.skippedDisabled,
            error_count: Runtime.stats.errorCount,
            last_error: Runtime.stats.lastError,
            last_reset_reason: Runtime.stats.lastResetReason,
            last_result: Runtime.stats.lastResult,
            add_amount: Runtime.config.add_amount,
            require_enabled_for_actions: Runtime.config.require_enabled_for_actions,
            pending_add_hp: Runtime.pending.addHp
        };
    }

    rpc.exports = {
        enable: function (config) {
            updateConfig(config);
            enableFeature();
            return buildStatus();
        },

        disable: function () {
            disableFeature();
            return buildStatus();
        },

        status: function () {
            return buildStatus();
        },

        cleanup: function (payload) {
            cleanupFeature();
            return buildStatus();
        },

        setConfig: function (config) {
            updateConfig(config);
            return buildStatus();
        },

        set_config: function (config) {
            updateConfig(config);
            return buildStatus();
        },

        setconfig: function (config) {
            updateConfig(config);
            return buildStatus();
        },

        addhp: function () {
            if (!Runtime.enabled && Runtime.config.require_enabled_for_actions) {
                Runtime.stats.skippedDisabled += 1;
                Runtime.stats.lastResult = "feature_disabled";
                log("warn", "addhp rejected: feature disabled");
                return buildStatus();
            }
            if (!Runtime.initialized && !installHooks()) {
                Runtime.stats.lastResult = "hooks_not_ready";
                return buildStatus();
            }
            Runtime.pending.addHp = true;
            Runtime.stats.lastResult = "pending";
            log("info", "add hp queued (+" + Runtime.config.add_amount + ")");
            return buildStatus();
        }
    };

    log("info", "script loaded");
})();