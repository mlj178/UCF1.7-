// ============================================================
// AAAAA-hp_boost_probe.js — 增加血量 探测脚本（临时调试用，位于 dev/）
//
// feature_id: "hp_boost_probe"
//
// 探测目标：
//   1. 验证 HealthData.Heal(int) 是否被 maxHealth 封顶（IDA 解码结论：是）。
//   2. 验证 HealthData.AddHealthMax(addHP, heal) 能否真正提升血量上限并回血。
//   3. 记录 healthData 指针（字段直读 vs get_healthData() 交叉验证）、
//      rate / isMaxHP / isDead、三个 ObscuredInt 的原始字节（前后对比）。
//
// 执行方式：
//   RPC probe(action) 只投递 pending；全部读写都在 Player.Update 主线程
//   Hook 内按状态机执行：BEFORE 快照 -> 执行动作 -> 等待 N 帧 -> AFTER 快照 -> 对比。
//
// RVA / 字段来源（dump.cs + IDA 汇编 part3.chunk006 手动解码）：
//   Player_Update:            0x00B551D0
//   Player_get_isMyPlayer:    0x00B55FD0
//   Entity_get_healthData:    0x001D7B00
//   Entity_get_team:          0x001E0070
//   HealthData_Heal:          0x00AE44F0   // void Heal(int) 内部 min(value+cur, max)
//   HealthData_AddHealthMax:  0x00AE4260   // void AddHealthMax(int addHP, bool heal)
//   HealthData_get_rate:      0x00AE4950   // float = 解密(cur) / 解密(max)
//   HealthData_get_isMaxHP:   0x00AE48B0
//   HealthData_get_isDead:    0x00AE4830
//   Entity.healthData:        0x1C
//   HealthData.currentHealth: 0x8   (ObscuredInt, 20 字节)
//   HealthData.maxHealth:     0x1C  (ObscuredInt, 20 字节)
//   HealthData.tempHealth:    0x30  (ObscuredInt, 20 字节)
//   HealthData.invinsibleEndTime: 0x44 (float)
// ============================================================

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';

    var RVA = {
        Player_Update: 0x00B551D0,
        Player_get_isMyPlayer: 0x00B55FD0,
        Entity_get_healthData: 0x001D7B00,
        Entity_get_team: 0x001E0070,
        HealthData_Heal: 0x00AE44F0,
        HealthData_AddHealthMax: 0x00AE4260,
        HealthData_get_rate: 0x00AE4950,
        HealthData_get_isMaxHP: 0x00AE48B0,
        HealthData_get_isDead: 0x00AE4830
    };

    var OFF = {
        Player_healthData: 0x1C,
        HD_currentHealth: 0x8,
        HD_maxHealth: 0x1C,
        HD_tempHealth: 0x30,
        HD_invinsibleEndTime: 0x44,
        ObscuredInt_size: 0x14
    };

    var VALID_ACTIONS = {
        heal: true,
        addmax: true,
        readonly: true
    };

    var Runtime = {
        feature_id: "hp_boost_probe",
        enabled: false,
        initialized: false,
        generation: 0,
        module: null,
        base: ptr(0),
        hooks: [],
        config: {
            amount: 10,
            after_wait_frames: 5
        },
        probe: {
            pendingAction: "",   // "heal" | "addmax" | "readonly"
            phase: "idle",       // idle | before | after
            action: "",
            waitFrames: 0,
            beforeSnapshot: null
        },
        last: {
            rate: null,
            isMaxHP: null,
            isDead: null,
            player: "",
            healthData: ""
        },
        stats: {
            hookHits: 0,
            localPlayerHits: 0,
            probesStarted: 0,
            probesFinished: 0,
            healCalls: 0,
            addMaxCalls: 0,
            errorCount: 0,
            cleanupCount: 0,
            lastError: "",
            lastResetReason: ""
        }
    };

    var native = {
        ready: false,
        isMyPlayer: null,
        getHealthData: null,
        getTeam: null,
        heal: null,
        addHealthMax: null,
        getRate: null,
        getIsMaxHP: null,
        getIsDead: null
    };

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

    function setError(message, error) {
        Runtime.stats.errorCount += 1;
        Runtime.stats.lastError = message + (error && error.message ? ": " + error.message : "");
        log("error", Runtime.stats.lastError);
    }

    function initNativeFunctions() {
        if (native.ready) return true;

        Runtime.module = Process.findModuleByName(MODULE_NAME);
        if (!Runtime.module) {
            Runtime.stats.lastError = MODULE_NAME + " not found";
            return false;
        }
        if (Process.arch !== 'ia32' || Process.pointerSize !== 4) {
            Runtime.stats.lastError = "unsupported process: arch=" + Process.arch;
            return false;
        }

        Runtime.base = Runtime.module.base;
        try {
            native.isMyPlayer = new NativeFunction(Runtime.base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer'], CALL_CONV);
            native.getHealthData = new NativeFunction(Runtime.base.add(RVA.Entity_get_healthData), 'pointer', ['pointer', 'pointer'], CALL_CONV);
            native.getTeam = new NativeFunction(Runtime.base.add(RVA.Entity_get_team), 'int', ['pointer', 'pointer'], CALL_CONV);
            native.heal = new NativeFunction(Runtime.base.add(RVA.HealthData_Heal), 'void', ['pointer', 'int', 'pointer'], CALL_CONV);
            // AddHealthMax(int addHP, bool heal, MethodInfo*) 的 bool 参数走 4 字节栈槽，
            // 该版本 Frida x86 mscdecl 不接受 JS true/false，用 int 传 1/0。
            native.addHealthMax = new NativeFunction(Runtime.base.add(RVA.HealthData_AddHealthMax), 'void', ['pointer', 'int', 'int', 'pointer'], CALL_CONV);
            native.getRate = new NativeFunction(Runtime.base.add(RVA.HealthData_get_rate), 'float', ['pointer', 'pointer'], CALL_CONV);
            native.getIsMaxHP = new NativeFunction(Runtime.base.add(RVA.HealthData_get_isMaxHP), 'bool', ['pointer', 'pointer'], CALL_CONV);
            native.getIsDead = new NativeFunction(Runtime.base.add(RVA.HealthData_get_isDead), 'bool', ['pointer', 'pointer'], CALL_CONV);
            native.ready = true;
            log("info", "GameAssembly.dll base=" + Runtime.base);
            return true;
        } catch (error) {
            setError("initNativeFunctions failed", error);
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
        Runtime.probe.pendingAction = "";
        Runtime.probe.phase = "idle";
        Runtime.probe.action = "";
        Runtime.probe.waitFrames = 0;
        Runtime.probe.beforeSnapshot = null;
        Runtime.stats.lastResetReason = reason || "unknown";
        log("info", "resetRuntime: " + Runtime.stats.lastResetReason + ", gen=" + Runtime.generation);
    }

    // ---------- 快照与解码 ----------

    function dumpObscuredInt(base, fieldOffset) {
        // 返回 5 个 dword 的十六进制串（ObscuredInt = 20 字节）
        var words = [];
        try {
            for (var i = 0; i < 5; i += 1) {
                words.push(base.add(fieldOffset + i * 4).readU32().toString(16).toUpperCase());
            }
        } catch (e) {
            return "READ_FAIL";
        }
        return words.join(" ");
    }

    function takeSnapshot(tag, player) {
        var snap = {
            tag: tag,
            player: player.toString(),
            healthDataField: "",
            healthDataGetter: "",
            getterMatch: false,
            team: -999,
            rate: null,
            isMaxHP: null,
            isDead: null,
            curRaw: "",
            maxRaw: "",
            tempRaw: "",
            invinsibleEndTime: null
        };

        var hdField = player.add(OFF.Player_healthData).readPointer();
        snap.healthDataField = hdField.toString();

        var hdGetter = native.getHealthData(player, ptr(0));
        snap.healthDataGetter = isNull(hdGetter) ? "null" : hdGetter.toString();
        snap.getterMatch = !isNull(hdField) && !isNull(hdGetter) && hdField.equals(hdGetter);

        var hd = hdField;
        if (isNull(hd) || !isReadablePtr(hd)) {
            log("error", "[" + tag + "] healthData 指针不可读: " + snap.healthDataField);
            return null;
        }

        snap.team = native.getTeam(player, ptr(0));
        snap.rate = native.getRate(hd, ptr(0));
        snap.isMaxHP = !!native.getIsMaxHP(hd, ptr(0));
        snap.isDead = !!native.getIsDead(hd, ptr(0));
        snap.curRaw = dumpObscuredInt(hd, OFF.HD_currentHealth);
        snap.maxRaw = dumpObscuredInt(hd, OFF.HD_maxHealth);
        snap.tempRaw = dumpObscuredInt(hd, OFF.HD_tempHealth);
        try { snap.invinsibleEndTime = hd.add(OFF.HD_invinsibleEndTime).readFloat(); } catch (e) {}

        log("info", "[" + tag + "] player=" + snap.player +
            " hdField=" + snap.healthDataField +
            " hdGetter=" + snap.healthDataGetter +
            " match=" + snap.getterMatch +
            " team=" + snap.team);
        log("info", "[" + tag + "] rate=" + snap.rate.toFixed(4) +
            " isMaxHP=" + (snap.isMaxHP ? 1 : 0) +
            " isDead=" + (snap.isDead ? 1 : 0) +
            " invEnd=" + snap.invinsibleEndTime);
        log("info", "[" + tag + "] cur=[" + snap.curRaw + "]");
        log("info", "[" + tag + "] max=[" + snap.maxRaw + "]");
        log("info", "[" + tag + "] temp=[" + snap.tempRaw + "]");

        Runtime.last.rate = snap.rate;
        Runtime.last.isMaxHP = snap.isMaxHP;
        Runtime.last.isDead = snap.isDead;
        Runtime.last.player = snap.player;
        Runtime.last.healthData = snap.healthDataField;

        return snap;
    }

    function applyAction(hd, action, amount) {
        if (action === "heal") {
            native.heal(hd, amount, ptr(0));
            Runtime.stats.healCalls += 1;
            log("info", "已调用 Heal(" + amount + ")");
        } else if (action === "addmax") {
            native.addHealthMax(hd, amount, 1, ptr(0));
            Runtime.stats.addMaxCalls += 1;
            log("info", "已调用 AddHealthMax(" + amount + ", heal=1)");
        }
        // readonly: 不做任何写操作
    }

    function summarize(before, after) {
        if (!before || !after) return;

        if (before.player !== after.player) {
            log("warn", "对比无效：前后 player 指针变化 " + before.player + " -> " + after.player);
            return;
        }

        var rateDelta = after.rate - before.rate;
        var curChanged = before.curRaw !== after.curRaw;
        var maxChanged = before.maxRaw !== after.maxRaw;
        var tempChanged = before.tempRaw !== after.tempRaw;

        log("info", "======== 探测结果 ========");
        log("info", "rate: " + before.rate.toFixed(4) + " -> " + after.rate.toFixed(4) +
            " (delta=" + rateDelta.toFixed(4) + ")");
        log("info", "isMaxHP: " + (before.isMaxHP ? 1 : 0) + " -> " + (after.isMaxHP ? 1 : 0));
        log("info", "currentHealth 原始字节变化: " + (curChanged ? "是" : "否"));
        log("info", "maxHealth 原始字节变化: " + (maxChanged ? "是" : "否"));
        log("info", "tempHealth 原始字节变化: " + (tempChanged ? "是" : "否"));

        if (Runtime.probe.action === "heal") {
            if (before.isMaxHP) {
                log("warn", "结论线索: 探测前已满血(isMaxHP=1)，Heal 被 maxHealth 封顶(min(value+cur,max))，无变化属预期。请先受伤再测 Heal。");
            } else if (!curChanged && rateDelta === 0) {
                log("warn", "结论线索: 未满血但 Heal 完全无效果，需要进一步排查(healthData 对象/线程/加密)。");
            } else {
                log("info", "结论线索: Heal 在数据层生效，rate 已变化。");
            }
        } else if (Runtime.probe.action === "addmax") {
            if (maxChanged) {
                log("info", "结论线索: maxHealth 已变化，AddHealthMax 生效。");
            } else {
                log("warn", "结论线索: maxHealth 未变化，AddHealthMax 未生效。");
            }
        } else {
            if (curChanged || rateDelta !== 0) {
                log("info", "结论线索: 只读探测期间血量自然变化(回血/掉血)，对比 Heal 结果时注意干扰。");
            } else {
                log("info", "结论线索: 只读探测期间血量稳定。");
            }
        }
        log("info", "==========================");
    }

    // ---------- 主线程状态机 ----------

    function onPlayerUpdate(player) {
        Runtime.stats.hookHits += 1;

        // 空闲且无 pending 时不做任何本地玩家判断，降低每帧开销
        if (!Runtime.probe.pendingAction && Runtime.probe.phase === "idle") return;
        if (!Runtime.enabled) return;

        try {
            if (!native.ready && !initNativeFunctions()) return;

            if (isNull(player) || !isReadablePtr(player)) return;
            if (!native.isMyPlayer(player, ptr(0))) return;
            Runtime.stats.localPlayerHits += 1;

            // 1) 取出新动作
            if (Runtime.probe.pendingAction && Runtime.probe.phase === "idle") {
                Runtime.probe.action = Runtime.probe.pendingAction;
                Runtime.probe.pendingAction = "";
                Runtime.probe.phase = "before";
                Runtime.stats.probesStarted += 1;
                log("info", "---- 探测开始: action=" + Runtime.probe.action +
                    " amount=" + Runtime.config.amount + " ----");
            }

            if (Runtime.probe.phase === "before") {
                var before = takeSnapshot("BEFORE", player);
                if (before === null) {
                    Runtime.probe.phase = "idle";
                    return;
                }
                Runtime.probe.beforeSnapshot = before;

                if (Runtime.probe.action === "heal" && before.isMaxHP) {
                    log("warn", "提示: 当前已满血，Heal 预期无效果(min 封顶)，建议先受伤再点 Heal 探测。");
                }

                applyAction(player.add(OFF.Player_healthData).readPointer(), Runtime.probe.action, Runtime.config.amount);

                Runtime.probe.phase = "after";
                Runtime.probe.waitFrames = Math.max(1, Math.floor(Runtime.config.after_wait_frames));
            } else if (Runtime.probe.phase === "after") {
                if (Runtime.probe.waitFrames > 0) {
                    Runtime.probe.waitFrames -= 1;
                    return;
                }
                var after = takeSnapshot("AFTER", player);
                if (after !== null) {
                    summarize(Runtime.probe.beforeSnapshot, after);
                    Runtime.stats.probesFinished += 1;
                }
                Runtime.probe.phase = "idle";
                Runtime.probe.action = "";
                Runtime.probe.beforeSnapshot = null;
                log("info", "---- 探测结束 ----");
            }
        } catch (error) {
            setError("probe Player.Update failed", error);
            Runtime.probe.phase = "idle";
            Runtime.probe.action = "";
            Runtime.probe.beforeSnapshot = null;
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
            log("info", "Player.Update hook installed");
            return true;
        } catch (error) {
            setError("installHooks failed", error);
            cleanupHooks();
            return false;
        }
    }

    // ---------- 生命周期 ----------

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
        if (typeof config.amount !== 'undefined') {
            Runtime.config.amount = Math.max(1, Math.floor(Number(config.amount) || 10));
        }
        if (typeof config.after_wait_frames !== 'undefined') {
            Runtime.config.after_wait_frames = Math.max(1, Math.floor(Number(config.after_wait_frames) || 5));
        }
        return true;
    }

    function buildStatus() {
        return {
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            generation: Runtime.generation,
            probe_phase: Runtime.probe.phase,
            probe_action: Runtime.probe.action,
            pending_action: Runtime.probe.pendingAction,
            amount: Runtime.config.amount,
            last_rate: Runtime.last.rate,
            last_isMaxHP: Runtime.last.isMaxHP,
            last_isDead: Runtime.last.isDead,
            last_player: Runtime.last.player,
            last_healthData: Runtime.last.healthData,
            stats: Runtime.stats
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

        probe: function (action) {
            if (!VALID_ACTIONS[action]) {
                log("warn", "未知探测动作: " + action);
                return buildStatus();
            }
            if (!Runtime.enabled) {
                log("warn", "探测被拒绝: 功能未开启");
                return buildStatus();
            }
            if (Runtime.probe.phase !== "idle" || Runtime.probe.pendingAction) {
                log("warn", "探测被拒绝: 上一次探测还在进行中");
                return buildStatus();
            }
            Runtime.probe.pendingAction = action;
            log("info", "探测已排队: " + action + " (+" + Runtime.config.amount + ")");
            return buildStatus();
        }
    };

    log("info", "probe script loaded (heal/addmax/readonly)");
})();