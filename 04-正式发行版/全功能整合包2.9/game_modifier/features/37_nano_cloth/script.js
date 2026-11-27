// ============================================================
// nano_cloth - 增加防化服
//
// feature_id: "nano_cloth"
// 功能目标：开启后，每次触发（按钮或快捷键）增加一次防化服，
//   增量为滑块设定的值（1~10，默认 10），同一回合内可反复触发叠加。
//   应用对象由下拉框 cloth_target 选择：
//     local_player —— 只加给本地玩家（默认，原有行为）
//     all_humans   —— 加给房间内所有"人类"阵营玩家（用 Player.get_isNanoGhost
//                     排除生化幽灵/终结者；本地玩家也在其中）
//   回合边界（GameManager.GameRoundEnd / NewGameRoundStart）会把"不是游戏原生拥有"
//   的防化服清零（含本地玩家），避免跨回合越叠越多；游戏自己发放过防化服的人类
//   （ClientData.haveNanoCloth=true）不动，出生时仍由游戏重置为 1。
//
// 实现原理：
//   1. Hook Player.Update（RVA 0xB551D0），短期捕获本地 Player；
//      应用对象为 all_humans 时不需要本地 Player，但同样只在 Player.Update
//      命中时（游戏主线程）执行，保证 Unity/IL2CPP 调用线程安全。
//   2. 应用动作只设置 pending.applyCloth = true，不在 RPC 里直接写对象。
//   3. 下一次 Player.Update 命中时（主线程）：
//      - local_player：确认 isMyPlayer 后调用原游戏 Player.AddNanoClothCount(count)
//        （RVA 0xB4FA00，捡补给箱加防化服的原生方法）。
//      - all_humans：用 Singleton<GameManager>.get_instance 取 GameManager，
//        遍历 GameManager.allPlayers（+0x1C，Il2CppArray：count@+0xC，
//        items@+0x10），对每个非幽灵玩家调用同一个 AddNanoClothCount。
//      该方法内部完成：在当前数量上加密累加 + 虚分发 SetNanoClothUI
//      刷新游戏 HUD，因此不需要手动 XOR 写内存，也没有数量上限。
//      游戏原生 ModeBase_Nano.OnPlayerPickUpSupplyBox 也是对"拾取者"调用它，
//      对非本地玩家调用属于复刻原生行为，不是越界写法。
//
// RVA / 字段来源：dump.cs + IDA 汇编交叉验证
//   Player.Update:                    0x00B551D0  (protected override void Update)
//   Player.get_isMyPlayer:            0x00B55FD0  (bool (Player*, MethodInfo*))
//   Player.get_isNanoGhost:           0x00B56050  (bool (Player*, MethodInfo*))
//   Player.AddNanoClothCount:         0x00B4FA00  (void (Player*, int count, MethodInfo*))
//   Player.SetNanoClothCount:         0x00B533A0  (void (Player*, int count, MethodInfo*))
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
//   AddNanoClothCount / SetNanoClothCount 末尾都用 Player.get_isFocusPlayer 门控
//   SetNanoClothUI：只有当前聚焦玩家（本地玩家）才会刷新 HUD，所以给队友/Bot
//   写数量不会污染本地 HUD。
//
//   游戏原生 UI 边界：SetNanoClothUI 的数字贴图只有 3 张（min(3,count)），
//   Nano4T 模式仅重写为图标显隐；数量超过 3 时判定值真实生效并持续累计，
//   游戏内 HUD 数字显示按游戏原生规则封顶显示。
// ============================================================

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';

    var MAX_PLAYER_SLOTS = 64;
    var TARGET_LOCAL = 'local_player';
    var TARGET_ALL_HUMANS = 'all_humans';

    var RVA = {
        Player_Update: 0x00B551D0,
        Player_get_isMyPlayer: 0x00B55FD0,
        Player_get_isNanoGhost: 0x00B56050,
        Player_AddNanoClothCount: 0x00B4FA00,
        Player_SetNanoClothCount: 0x00B533A0,
        Singleton_GameManager_get_instance: 0x004A8170,
        SingletonGameManager_get_instance_Method: 0x00E1CE64,
        GameManager_GameRoundEnd: 0x00AFAA40,
        GameManager_NewGameRoundStart: 0x00AEBCB0,
        GameManager_OnDestroy: 0x00AEBD40
    };

    var OFF = {
        nanoCloth: 0xE4,
        obscKey: 0x00,
        obscHidden: 0x04,
        obscInited: 0x08,
        // 玩家阵营/补给标记：Player.clientData@0x94，ClientData.haveNanoCloth@0x2C
        playerClientData: 0x94,
        clientDataHaveNanoCloth: 0x2C,
        // GameManager.allPlayers：Il2CppArray<Player*>（与 34-角色变身 / 08-聚怪 一致）
        gmAllPlayers: 0x1C,
        arrayLength: 0x0C,
        arrayItems: 0x10
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
            cloth_target: TARGET_LOCAL,
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
        applying: false,
        clearing: false,
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
            lastApplyTarget: "",
            lastKnownClothCount: null,
            allHumansApplyCount: 0,
            allHumansTargets: 0,
            allHumansSkipped: 0,
            allHumansFailed: 0,
            clearedHumans: 0
        }
    };

    var native = {
        ready: false,
        isMyPlayer: null,
        isNanoGhost: null,
        getGameManager: null,
        addNanoClothCount: null,
        setNanoClothCount: null
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
            native.isNanoGhost = new NativeFunction(
                Runtime.base.add(RVA.Player_get_isNanoGhost),
                'bool',
                ['pointer', 'pointer'],
                CALL_CONV
            );
            native.getGameManager = new NativeFunction(
                Runtime.base.add(RVA.Singleton_GameManager_get_instance),
                'pointer',
                ['pointer'],
                CALL_CONV
            );
            native.setNanoClothCount = new NativeFunction(
                Runtime.base.add(RVA.Player_SetNanoClothCount),
                'void',
                ['pointer', 'int', 'pointer'],
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
                    var localUpdate = captureLocalPlayer(player, 'Player.Update');
                    // all_humans 目标不依赖本地玩家，remote 玩家的 Update 也可以消费挂起动作；
                    // local_player 目标在 performPending 内仍会要求 localUpdate 为真。
                    if (Runtime.pending.applyCloth) {
                        performPending(player, localUpdate);
                    }
                } catch (error) {
                    setError('Player.Update hook failed', error);
                }
            }
        });

        attachHook('GameManager.GameRoundEnd', RVA.GameManager_GameRoundEnd, {
            onEnter: function () {
                try { clearHumanClothAtRoundBoundary('game_round_end'); } catch (e) {}
                try { resetRuntime('game_round_end'); } catch (e) {}
            }
        });
        attachHook('GameManager.NewGameRoundStart', RVA.GameManager_NewGameRoundStart, {
            onEnter: function () {
                try { clearHumanClothAtRoundBoundary('new_game_round_start'); } catch (e) {}
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
        Runtime.applying = false;
        Runtime.clearing = false;
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

    function normalizeTarget(value) {
        return String(value === undefined || value === null ? '' : value).trim() === TARGET_ALL_HUMANS
            ? TARGET_ALL_HUMANS
            : TARGET_LOCAL;
    }

    // Singleton<GameManager>.get_instance：静态方法，MethodInfo 指针存在 base+0xE1CE64。
    function getGameManager() {
        if (!native.ready) return ptr(0);
        try {
            var methodInfo = Runtime.base.add(RVA.SingletonGameManager_get_instance_Method).readPointer();
            if (isNull(methodInfo)) return ptr(0);
            return native.getGameManager(methodInfo);
        } catch (error) {
            setError('Singleton<GameManager>.get_instance failed', error);
            return ptr(0);
        }
    }

    function isValidPlayer(player) {
        if (isNull(player)) return false;
        try {
            var klass = player.readPointer();
            return !isNull(klass);
        } catch (_) {
            return false;
        }
    }

    // 人类阵营判定：Player.get_isNanoGhost = isNanoMode && Entity._team == 0，
    // 为假即视为人类（非生化模式同样返回假，所以非生化模式等价于"所有玩家"）。
    function isHumanPlayer(player) {
        if (!isValidPlayer(player)) return false;
        if (!native.ready) return false;
        try {
            return !native.isNanoGhost(player, ptr(0));
        } catch (error) {
            setError('Player.get_isNanoGhost failed', error);
            return false;
        }
    }

    // 遍历 GameManager.allPlayers（Il2CppArray<Player*>），对所有人类玩家加密累加防化服。
    // 只在 Player.Update 主线程钩子里调用。
    function applyClothToHumans() {
        var summary = { available: false, applied: 0, skipped: 0, failed: 0 };
        if (Runtime.applying) return summary;
        if (!native.ready && !initNativeFunctions()) return summary;

        Runtime.applying = true;
        try {
            var manager = getGameManager();
            if (isNull(manager) || !isReadablePtr(manager)) return summary;
            var players = manager.add(OFF.gmAllPlayers).readPointer();
            if (isNull(players) || !isReadablePtr(players)) return summary;

            summary.available = true;
            var count = players.add(OFF.arrayLength).readU32();
            if (count > MAX_PLAYER_SLOTS) count = MAX_PLAYER_SLOTS;
            var delta = normalizeClothCount(Runtime.config.cloth_count);
            for (var index = 0; index < count; index += 1) {
                var player = null;
                try {
                    player = players.add(OFF.arrayItems + index * Process.pointerSize).readPointer();
                } catch (_) {
                    player = null;
                }
                if (!isHumanPlayer(player)) {
                    summary.skipped += 1;
                    continue;
                }
                if (applyClothValue(player, delta)) summary.applied += 1;
                else summary.failed += 1;
            }
        } catch (error) {
            setError('applyClothToHumans failed', error);
        } finally {
            Runtime.applying = false;
        }
        return summary;
    }

    // 游戏对防化服的“正常重置”只有两处（IDA 实证）：
    //   1. ModeBase_Nano.SpawnEvent：人类(nanoRole==0) 且 clientData.haveNanoCloth==true 时
    //      SetNanoClothCount(player, 1)；
    //   2. ModeBase_Nano.UpdateNanoRole：变成幽灵(Team 0) 时 SetNanoClothCount(player, 0)。
    // 我们用 AddNanoClothCount 额外加出来的数量没有 haveNanoCloth 标记，游戏出生时不会重置它，
    // 于是跨回合越叠越多。这里在回合边界把“非游戏原生拥有”的人类（含本地玩家）清零；
    // 游戏正常的 haveNanoCloth 玩家保持原样，由游戏自己在出生时重置为 1。
    function hasNativeNanoCloth(player) {
        if (isNull(player) || !isReadablePtr(player)) return true;
        try {
            var clientData = player.add(OFF.playerClientData).readPointer();
            if (isNull(clientData) || !isReadablePtr(clientData)) return true;
            return clientData.add(OFF.clientDataHaveNanoCloth).readU8() !== 0;
        } catch (_) {
            return true; // 读不到就保守跳过，绝不清除不确定的状态
        }
    }

    function clearHumanClothAtRoundBoundary(reason) {
        var everApplied = Runtime.stats.applyCount > 0 || Runtime.stats.allHumansApplyCount > 0;
        if (!everApplied) return 0;
        if (Runtime.clearing) return 0;
        if (!native.ready && !initNativeFunctions()) return 0;

        Runtime.clearing = true;
        var cleared = 0;
        var scanned = 0;
        try {
            var manager = getGameManager();
            if (isNull(manager) || !isReadablePtr(manager)) return 0;
            var players = manager.add(OFF.gmAllPlayers).readPointer();
            if (isNull(players) || !isReadablePtr(players)) return 0;
            var count = players.add(OFF.arrayLength).readU32();
            if (count > MAX_PLAYER_SLOTS) count = MAX_PLAYER_SLOTS;
            for (var index = 0; index < count; index += 1) {
                var player = null;
                try {
                    player = players.add(OFF.arrayItems + index * Process.pointerSize).readPointer();
                } catch (_) {
                    player = null;
                }
                if (!isHumanPlayer(player)) continue;
                scanned += 1;
                if (hasNativeNanoCloth(player)) continue;
                try {
                    native.setNanoClothCount(player, 0, ptr(0));
                    cleared += 1;
                } catch (error) {
                    setError('clearHumanClothAtRoundBoundary failed', error);
                }
            }
        } catch (error) {
            setError('clearHumanClothAtRoundBoundary failed', error);
        } finally {
            Runtime.clearing = false;
        }
        Runtime.stats.clearedHumans += cleared;
        if (cleared > 0) {
            log('info', '回合边界清理：已清零 ' + cleared + ' 名人类的防化服（' + reason +
                '，扫描人类 ' + scanned + '）');
        }
        return cleared;
    }

    function performPending(player, localUpdate) {
        if (!Runtime.pending.applyCloth) return;
        if (!Runtime.enabled) return;

        var target = normalizeTarget(Runtime.config.cloth_target);
        if (target === TARGET_ALL_HUMANS) {
            Runtime.pending.applyCloth = false;
            Runtime.stats.lastApplyTarget = TARGET_ALL_HUMANS;
            var deltaAll = normalizeClothCount(Runtime.config.cloth_count);
            var summary = applyClothToHumans();
            Runtime.stats.allHumansApplyCount += 1;
            Runtime.stats.allHumansTargets = summary.applied;
            Runtime.stats.allHumansSkipped = summary.skipped;
            Runtime.stats.allHumansFailed = summary.failed;
            if (!summary.available) {
                Runtime.stats.lastApplyResult = 'all_players_unavailable';
                log('warn', '未取到玩家列表，防化服未应用（请在房间内重试）');
                return;
            }
            if (summary.applied > 0) {
                Runtime.stats.lastApplyResult = 'added ' + deltaAll + '（全体人类 ' + summary.applied + ' 人）';
                log('info', '防化服已增加 ' + deltaAll + ' 件（全体人类 ' + summary.applied +
                    ' 人，跳过 ' + summary.skipped + '，失败 ' + summary.failed + '）');
            } else {
                Runtime.stats.lastApplyResult = 'no_human_found';
                log('warn', '未找到可增加防化服的人类目标（扫描槽位 ' +
                    (summary.applied + summary.skipped + summary.failed) + '）');
            }
            return;
        }

        // local_player：保持原行为，必须等到本地玩家的 Update
        if (!localUpdate) return;
        if (isNull(player)) return;

        Runtime.pending.applyCloth = false;
        Runtime.stats.lastApplyTarget = TARGET_LOCAL;
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
        log('info', '防化服应用等待下一次 Player.Update（对象：' +
            (normalizeTarget(Runtime.config.cloth_target) === TARGET_ALL_HUMANS ? '全体人类' : '仅本地玩家') + '）');
        return { ok: true, reason: 'apply_pending' };
    }

    function enableFeature(config) {
        updateConfig(config);
        if (!initializeFeature()) return getStatus();
        Runtime.enabled = true;
        Runtime.stats.errorCount = 0;
        Runtime.stats.lastError = '';
        log('success', '防化服功能已开启, 每次增加=' + Runtime.config.cloth_count + ' 件, 应用对象=' +
            (Runtime.config.cloth_target === TARGET_ALL_HUMANS ? '全体人类' : '仅本地玩家') + '（可累计）');
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
        if (config.cloth_target !== undefined) {
            Runtime.config.cloth_target = normalizeTarget(config.cloth_target);
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
            cloth_target: Runtime.config.cloth_target,
            min_cloth_count: Runtime.config.min_cloth_count,
            max_cloth_count: Runtime.config.max_cloth_count,
            all_humans_apply_count: Runtime.stats.allHumansApplyCount,
            all_humans_targets: Runtime.stats.allHumansTargets,
            all_humans_skipped: Runtime.stats.allHumansSkipped,
            all_humans_failed: Runtime.stats.allHumansFailed,
            cleared_humans: Runtime.stats.clearedHumans,
            last_apply_target: Runtime.stats.lastApplyTarget,
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