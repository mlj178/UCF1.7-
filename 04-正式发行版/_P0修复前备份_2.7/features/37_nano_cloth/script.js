// ============================================================
// nano_cloth - 增加防化服
//
// feature_id: "nano_cloth"
// 功能目标：开启后，每次触发（按钮或快捷键）给本地玩家增加一次防化服，
//   增量为滑块设定的值（1~10，默认 10），可以无限累计（10+10+10…）。
//
// 实现原理：
//   1. Hook Player.Update（RVA 0xB551D0），短期捕获本地 Player。
//   2. 应用动作只设置 pending.applyCloth = true，不在 RPC 里直接写对象。
//   3. 下一次 Player.Update 命中时（主线程），确认 isMyPlayer 后调用原游戏
//      Player.AddNanoClothCount(count)（RVA 0xB4FA00，捡补给箱加防化服的原生
//      方法）。该方法内部完成：在当前数量上加密累加 + 虚分发 SetNanoClothUI
//      刷新游戏 HUD，因此不需要手动 XOR 写内存，也没有数量上限。
//
// RVA / 字段来源：dump.cs + IDA 汇编交叉验证
//   Player.Update:                    0x00B551D0  (protected override void Update)
//   Player.get_isMyPlayer:            0x00B55FD0  (bool (Player*, MethodInfo*))
//   Player.AddNanoClothCount:         0x00B4FA00  (void (Player*, int count, MethodInfo*))
//   GameManager.GameRoundEnd:         0x00AFAA40
//   GameManager.NewGameRoundStart:    0x00AEBCB0
//   GameManager.OnDestroy:            0x00AEBD40
//
//   Player.nanoClothCount 字段偏移 0xE4，类型 ObscuredInt（CodeStage AntiCheat）
//   ObscuredInt 布局（相对结构体起点，仅 status 读取当前值用）：
//     currentCryptoKey @ +0x00 (int)
//     hiddenValue      @ +0x04 (int)
//     inited           @ +0x08 (bool)
//   解密：real = hiddenValue ^ currentCryptoKey（IDA 确认 Encrypt = value ^ key）
//
//   游戏原生 UI 边界：SetNanoClothUI 的数字贴图只有 3 张（min(3,count)），
//   Nano4T 模式仅重写为图标显隐；数量超过 3 时判定值真实生效并持续累计，
//   游戏内 HUD 数字显示按游戏原生规则封顶显示。
// ============================================================

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';

    var RVA = {
        Player_Update: 0x00B551D0,
        Player_get_isMyPlayer: 0x00B55FD0,
        Player_AddNanoClothCount: 0x00B4FA00,
        GameManager_GameRoundEnd: 0x00AFAA40,
        GameManager_NewGameRoundStart: 0x00AEBCB0,
        GameManager_OnDestroy: 0x00AEBD40
    };

    var OFF = {
        nanoCloth: 0xE4,
        obscKey: 0x00,
        obscHidden: 0x04,
        obscInited: 0x08
    };

    var Runtime = {
        feature_id: "nano_cloth",
        enabled: false,
        initialized: false,
        generation: 0,
        module: null,
        base: ptr(0),
        hooks: [],
        config: {
            cloth_count: 10,
            min_cloth_count: 1,
            max_cloth_count: 10
        },
        cache: {
            localPlayer: ptr(0),
            localPlayerSeenAt: 0
        },
        pending: {
            applyCloth: false
        },
        stats: {
            hookHits: 0,
            localPlayerHits: 0,
            applyCount: 0,
            skippedNull: 0,
            skippedInvalid: 0,
            skippedDisabled: 0,
            errorCount: 0,
            cleanupCount: 0,
            lastError: "",
            lastResetReason: "",
            lastApplyResult: "",
            lastKnownClothCount: null
        }
    };

    var native = {
        ready: false,
        isMyPlayer: null,
        addNanoClothCount: null
    };

    var LogLimiter = {};

    function log(level, message) {
        try {
            var text = '[' + Runtime.feature_id + '][' + level + '] ' + message;
            console.log(text);
            send({ type: 'log', level: level, module: Runtime.feature_id, message: message });
        } catch (_) {
        }
    }

    // 状态回执：enable/disable/cleanup 后向中心广播真实状态。
    // 中心 on_feature_status 依赖此消息同步 UI 开关与内存 state，
    // 这是所有老功能（01-35）的既定模式，缺失会导致开关显示与实际状态脱钩。
    function sendStatus(enabled) {
        try {
            send({ type: 'status', feature: Runtime.feature_id, enabled: enabled });
        } catch (_) {
        }
    }

    function logLimited(key, level, message, intervalMs) {
        var now = Date.now();
        var wait = intervalMs || 1000;
        if (!LogLimiter[key] || now - LogLimiter[key] >= wait) {
            LogLimiter[key] = now;
            log(level, message);
        }
    }

    function setError(label, error) {
        Runtime.stats.errorCount += 1;
        Runtime.stats.lastError = label + (error && error.message ? ': ' + error.message : '');
        logLimited('error:' + label, 'error', Runtime.stats.lastError, 1500);
    }

    function isNull(p) {
        if (p === null || p === undefined) return true;
        try { return p.isNull(); } catch (_) { return true; }
    }

    function isReadablePtr(p) {
        try {
            if (isNull(p)) return false;
            p.readPointer();
            return true;
        } catch (_) {
            return false;
        }
    }

    function findGameAssembly() {
        if (Runtime.module) return Runtime.module;
        var mod = Process.findModuleByName(MODULE_NAME);
        if (!mod) {
            Runtime.stats.lastError = MODULE_NAME + ' not found';
            return null;
        }
        Runtime.module = mod;
        Runtime.base = mod.base;
        return mod;
    }

    function initNativeFunctions() {
        if (native.ready) return true;
        var mod = findGameAssembly();
        if (!mod) return false;

        if (Process.arch !== 'ia32' || Process.pointerSize !== 4) {
            Runtime.stats.lastError = 'unsupported process: arch=' + Process.arch + ', pointerSize=' + Process.pointerSize;
            log('error', Runtime.stats.lastError);
            return false;
        }

        try {
            native.isMyPlayer = new NativeFunction(
                Runtime.base.add(RVA.Player_get_isMyPlayer),
                'bool',
                ['pointer', 'pointer'],
                CALL_CONV
            );
            native.addNanoClothCount = new NativeFunction(
                Runtime.base.add(RVA.Player_AddNanoClothCount),
                'void',
                ['pointer', 'int', 'pointer'],
                CALL_CONV
            );
            native.ready = true;
            return true;
        } catch (error) {
            setError('initNativeFunctions failed', error);
            native.ready = false;
            return false;
        }
    }

    function isLocalPlayer(playerPtr) {
        if (isNull(playerPtr) || !isReadablePtr(playerPtr)) return false;
        if (!native.ready && !initNativeFunctions()) return false;
        try {
            return !!native.isMyPlayer(playerPtr, ptr(0));
        } catch (error) {
            setError('Player.get_isMyPlayer failed', error);
            return false;
        }
    }

    function captureLocalPlayer(player, reason) {
        if (isNull(player) || !isReadablePtr(player)) {
            Runtime.stats.skippedInvalid += 1;
            return false;
        }
        if (!isLocalPlayer(player)) return false;

        Runtime.cache.localPlayer = player;
        Runtime.cache.localPlayerSeenAt = Date.now();
        Runtime.stats.localPlayerHits += 1;
        return true;
    }

    function readClothValue(player) {
        if (isNull(player) || !isReadablePtr(player)) return null;
        try {
            var base = player.add(OFF.nanoCloth);
            if (base.add(OFF.obscInited).readU8() !== 1) return null;
            var key = base.add(OFF.obscKey).readS32();
            var hidden = base.add(OFF.obscHidden).readS32();
            return (hidden ^ key) >>> 0;
        } catch (e) {
            return null;
        }
    }

    function applyClothValue(player, value) {
        if (isNull(player) || !isReadablePtr(player)) return false;
        if (!native.ready) return false;
        try {
            // 调用原游戏方法：在当前数量上加密累加 + SetNanoClothUI 刷新 HUD。
            // 在 Player.Update Hook（主线程）里调用，Unity UI 操作线程安全。
            native.addNanoClothCount(player, value, ptr(0));
            return true;
        } catch (error) {
            setError('Player.AddNanoClothCount failed', error);
            return false;
        }
    }

    function attachHook(name, rva, callbacks) {
        var addr = Runtime.base.add(rva);
        var hook = Interceptor.attach(addr, callbacks);
        Runtime.hooks.push({ name: name, hook: hook });
        log('success', name + ' hook installed at ' + addr);
    }

    function attachHooks() {
        attachHook('Player.Update', RVA.Player_Update, {
            onEnter: function (args) {
                Runtime.stats.hookHits += 1;
                try {
                    var player = args[0];
                    if (captureLocalPlayer(player, 'Player.Update')) {
                        performPending(player);
                    }
                } catch (error) {
                    setError('Player.Update hook failed', error);
                }
            }
        });

        attachHook('GameManager.GameRoundEnd', RVA.GameManager_GameRoundEnd, {
            onEnter: function () {
                try { resetRuntime('game_round_end'); } catch (e) {}
            }
        });
        attachHook('GameManager.NewGameRoundStart', RVA.GameManager_NewGameRoundStart, {
            onEnter: function () {
                try { resetRuntime('new_game_round_start'); } catch (e) {}
            }
        });
        attachHook('GameManager.OnDestroy', RVA.GameManager_OnDestroy, {
            onEnter: function () {
                try { resetRuntime('game_manager_destroy'); } catch (e) {}
            }
        });
    }

    function cleanupHooks() {
        Runtime.hooks.forEach(function (item) {
            try { item.hook.detach(); } catch (_) {}
        });
        Runtime.hooks = [];
    }

    function resetRuntime(reason) {
        Runtime.generation += 1;
        Runtime.cache.localPlayer = ptr(0);
        Runtime.cache.localPlayerSeenAt = 0;
        Runtime.pending.applyCloth = false;
        Runtime.stats.lastResetReason = reason || 'unknown';
        logLimited('reset:' + reason, 'info', 'resetRuntime: ' + Runtime.stats.lastResetReason + ', gen=' + Runtime.generation, 1000);
    }

    function initializeFeature() {
        if (Runtime.initialized) return true;
        if (!initNativeFunctions()) return false;
        try {
            attachHooks();
            Runtime.initialized = true;
            return true;
        } catch (error) {
            setError('initializeFeature failed', error);
            cleanupHooks();
            Runtime.initialized = false;
            return false;
        }
    }

    function normalizeClothCount(value) {
        var n = Math.round(Number(value));
        if (!isFinite(n)) n = 1;
        if (n < Runtime.config.min_cloth_count) n = Runtime.config.min_cloth_count;
        if (n > Runtime.config.max_cloth_count) n = Runtime.config.max_cloth_count;
        return n;
    }

    function performPending(player) {
        if (isNull(player)) return;
        if (!Runtime.pending.applyCloth) return;
        if (!Runtime.enabled) return;

        Runtime.pending.applyCloth = false;
        var delta = normalizeClothCount(Runtime.config.cloth_count);
        var before = readClothValue(player);
        if (applyClothValue(player, delta)) {
            Runtime.stats.applyCount += 1;
            var afterText = before === null ? '' : '（' + before + ' → ' + (before + delta) + '）';
            Runtime.stats.lastApplyResult = 'added ' + delta + ' ' + afterText;
            log('info', '防化服已增加 ' + delta + ' 件' + afterText);
        } else {
            Runtime.stats.lastApplyResult = 'apply_failed';
            log('error', '增加防化服失败');
        }
    }

    function requestApply() {
        if (!initNativeFunctions()) {
            Runtime.stats.lastApplyResult = 'native_not_ready';
            return { ok: false, reason: 'native_not_ready' };
        }
        if (!Runtime.enabled) {
            Runtime.stats.skippedDisabled += 1;
            Runtime.stats.lastApplyResult = 'feature_disabled';
            return { ok: false, reason: 'feature_disabled' };
        }
        Runtime.pending.applyCloth = true;
        Runtime.stats.lastApplyResult = 'apply_pending';
        log('info', '防化服应用等待下一次 Player.Update');
        return { ok: true, reason: 'apply_pending' };
    }

    function enableFeature(config) {
        updateConfig(config);
        if (!initializeFeature()) return getStatus();
        Runtime.enabled = true;
        Runtime.stats.errorCount = 0;
        Runtime.stats.lastError = '';
        log('success', '防化服功能已开启, 每次增加=' + Runtime.config.cloth_count + ' 件（可累计）');
        sendStatus(true);
        return getStatus();
    }

    function disableFeature() {
        Runtime.enabled = false;
        Runtime.pending.applyCloth = false;
        resetRuntime('disable');
        log('info', '防化服功能已关闭');
        sendStatus(false);
        return getStatus();
    }

    function cleanupFeature() {
        Runtime.enabled = false;
        cleanupHooks();
        Runtime.initialized = false;
        resetRuntime('cleanup');
        Runtime.stats.cleanupCount += 1;
        native.ready = false;
        log('info', 'cleanup complete');
        sendStatus(false);
        return getStatus();
    }

    function updateConfig(config) {
        config = config || {};
        if (config.cloth_count !== undefined) {
            Runtime.config.cloth_count = normalizeClothCount(config.cloth_count);
        }
        if (config.min_cloth_count !== undefined) {
            Runtime.config.min_cloth_count = Math.round(Number(config.min_cloth_count)) || 1;
        }
        if (config.max_cloth_count !== undefined) {
            Runtime.config.max_cloth_count = Math.round(Number(config.max_cloth_count)) || 10;
        }
        return getStatus();
    }

    function getStatus() {
        var lp = Runtime.cache.localPlayer;
        var isCached = !isNull(lp);
        var count = isCached ? readClothValue(lp) : null;
        // 缓存最后一次成功读到的数量：即使切回合/退房后 localPlayer 暂时为空，
        // UI 也能显示上一次的值，避免出现无法解释的 "--"。
        if (count !== null) {
            Runtime.stats.lastKnownClothCount = count;
        }
        return {
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            generation: Runtime.generation,
            module_found: Runtime.module !== null,
            cloth_count: Runtime.config.cloth_count,
            min_cloth_count: Runtime.config.min_cloth_count,
            max_cloth_count: Runtime.config.max_cloth_count,
            hook_hits: Runtime.stats.hookHits,
            local_player_hits: Runtime.stats.localPlayerHits,
            apply_count: Runtime.stats.applyCount,
            skipped_null: Runtime.stats.skippedNull,
            skipped_invalid: Runtime.stats.skippedInvalid,
            skipped_disabled: Runtime.stats.skippedDisabled,
            error_count: Runtime.stats.errorCount,
            cleanup_count: Runtime.stats.cleanupCount,
            last_error: Runtime.stats.lastError,
            last_reset_reason: Runtime.stats.lastResetReason,
            last_apply_result: Runtime.stats.lastApplyResult,
            pending_apply: Runtime.pending.applyCloth,
            player_cached: isCached,
            current_cloth_count: count,
            last_known_cloth_count: Runtime.stats.lastKnownClothCount
        };
    }

    rpc.exports = {
        enable: function (config) {
            return enableFeature(config);
        },
        disable: function () {
            return disableFeature();
        },
        status: function () {
            if (!Runtime.module) findGameAssembly();
            return getStatus();
        },
        cleanup: function (payload) {
            return cleanupFeature();
        },
        setConfig: function (config) {
            return updateConfig(config);
        },
        set_config: function (config) {
            return updateConfig(config);
        },
        setconfig: function (config) {
            return updateConfig(config);
        },
        apply: function () {
            var result = requestApply();
            if (!result.ok) {
                log('warn', '应用防化服被拒绝: ' + result.reason);
            }
            return getStatus();
        }
    };
})();