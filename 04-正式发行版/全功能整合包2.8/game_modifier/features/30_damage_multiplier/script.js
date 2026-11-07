// ============================================================
// damage_multiplier / script.js
//
// feature_id: "damage_multiplier"
// 功能目标：分别调整「敌人 / 自己 / 队友」造成的最终生命伤害，
//           倍率可调高（>1.0x）也可调低（<1.0x，最低 0.1x，不允许 0）。
//
// 实现原理（两段式）：
//   1. 【入口段·枪/雷/技能/炮台】Hook GameManager.TakeDamage（RVA 0xAFC1C0）。
//      游戏在这个函数里才做「×受害者防御率 → min(剩余血量) → Hurt」，
//      所以在入口先乘倍率，最终伤害 = 原始伤害 × 倍率（防御和血量上限照旧），
//      与目标剩余血量无关。这是「伤害只由倍率决定」的关键。
//   2. 【收尾段·刀】Hook Entity.OnEntityHurt / Player.OnEntityHurt。
//      生化模式的 ModeBase_Nano.PreDamageEvent 会调 CalKnifeDmg，按攻击者
//      NanoRole 把刀伤重写成固定值（1000/1500/2500/3000/8000…），把入口段
//      乘好的倍率覆盖掉；只有最后一步乘才保得住刀伤倍率。
//   3. 解析真正的伤害来源（attacker 本体，或导弹/炮台的 owner），
//      再按阵营把来源分成 self（本地玩家）/ mate（队友）/ enemy（敌人）。
//   4. 记录 WPN_Missile.SetOwner / SentryGun.SetData，用于导弹、RPG、
//      榴弹和炮台这类特殊来源的归属判断。
//   5. 保底 1 点伤害：游戏会把 float damage 截断成 int，倍率 <1 时必须保证
//      「原本能造成伤害的一击」至少还是 1 点，否则最后一击会被截断成 0，
//      出现「敌人一直剩一滴血、打不死人」的问题。
//
// 关于「斩杀线不做几何衰减」（2026-11 修复）：
//   GameManager.TakeDamage 在调用 OnEntityHurt 之前就执行了
//     damage = Mathf.Max(0, Mathf.Min((int)(damage * victim.damageRate),
//                                      decrypt(victim.healthData.currentHealth)))
//   也就是说 OnEntityHurt 里拿到的 damage 已经是 min(伤害, 剩余血量)。
//   如果直接在 OnEntityHurt 里乘 <1 的倍率，到了斩杀线就变成
//     「这一击只扣 剩余血量 × 倍率」，下一击再按新的剩余血量算 →
//     血量几何级衰减，永远磨到 1 滴血才死。
//   所以：枪/雷/技能/炮台在入口（钳血之前）乘；刀留在 OnEntityHurt，
//   但如果这一刀已经被钳成「致死一击」（damage >= 剩余血量），就不再削弱。
//
// 关于 1 点保底（IDA 反汇编核对 Entity.OnEntityHurt）：
//   movss  xmm0, [ebp+eventData.damage]   ; 读 float damage
//   cvtps2pd xmm0, xmm0
//   cvttsd2si eax, xmm0                   ; float -> int，向零截断
//   call   HealthData.Hurt                ; int 直接相减，没有任何下限钳制
//   所以 damage < 1.0 时游戏实际收到 0 点伤害。
//
// 血量读取（ObscuredInt，与 18 方框透视同口径）：
//   victim(+0x1C) -> HealthData
//   HealthData+0x08 = currentCryptoKey(int)
//   HealthData+0x0C = hiddenValue(int)
//   明文 = hiddenValue ^ (currentCryptoKey || 0x6C81C)
//
// 阵营判定来源（IDA 反编译核对）：
//   Entity.get_team()            -> Entity.team（+0x20）
//   ExpandUtil.IsEnemy(a, b)     -> a.team==2 || b.team==2 || a.team!=b.team
//   ExpandUtil.IsSameTeam(a, b)  -> a!=2 && b!=2 && a==b
//   即 team==2（Neutral）永远算敌对，同队同阵营才叫队友。
//
//   变身/换队：人类 <-> 生化幽灵在 ModeBase_Nano.UpdateNanoRole 里
//   SetTeam(NanoRoleExpand.GetTeam(role))：人类 = GlobalRisk(1)、幽灵 = BlackList(0)；
//   Player.get_isNanoGhost() 本身就是 team == BlackList。
//   所以阵营按"实时读取的 team"判断（不用缓存快照），变身当帧就跟着变。
//
// RVA / 字段来源：dump.cs + script.json + 现有功能脚本交叉验证
//   GameManager_TakeDamage:     0x00AFC1C0   （入口段：枪/雷/技能/炮台）
//   Entity_OnEntityHurt:        0x00B3F470   （收尾段：刀）
//   Player_OnEntityHurt:        0x00B516B0
//   Player_get_isMyPlayer:      0x00B55FD0
//   Entity_get_team:            0x001E0070
//   SentryGun_SetData:          0x00B1E030
//   WPN_Missile_SetOwner:       0x00B66390
//   Singleton_get_instance:     0x004A8170
//   GameManager_Singleton_MI:   0x00E1CE64
//   GameManager_GameRoundEnd:   0x00AFAA40
//   GameManager_NewGameRoundStart: 0x00AEBCB0
//   GameManager_OnDestroy:      0x00AEBD40
//   DamageEventData.attacker:   0x00
//   DamageEventData.victim:     0x04
//   DamageEventData.damage:     0x08
//   DamageEventData.type:       0x34
//   DamageEventData.damageTag:  0x38
//   DamageEventData.wpnIndex:   0x3C
//   DamageEventData.wpnSprIndex:0x40
//   DamageEventData.ignoreDmgRate: 0x44
//   Entity.team:                0x20
//   Entity.healthData:          0x1C
//   HealthData.currentHealth:   0x08 (ObscuredInt: key +0x00, hidden +0x04)
//   GameManager.allPlayers:     0x1C (Il2Cpp array)
//   GameManager.playersBL:      0x20 (List<Player>)
//   GameManager.playersGR:      0x28 (List<Player>)
// ============================================================

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';

    var DamageType = {
        Gun: 1,
        Knife: 2,
        Grenade: 3,
        Infect: 4,
        Other: 5
    };

    // 阵营分类：自己 / 队友 / 敌人 / 无法判断
    var Category = {
        SELF: 'self',
        MATE: 'mate',
        ENEMY: 'enemy',
        UNKNOWN: 'unknown'
    };

    // 伤害事件阶段：
    //   PRE_CAP  = GameManager.TakeDamage 入口（游戏还没做「×防御率 / 钳到剩余血量」）
    //   POST_CAP = Entity.OnEntityHurt / Player.OnEntityHurt（游戏已经钳到剩余血量）
    var DamageStage = {
        PRE_CAP: 'pre_cap',
        POST_CAP: 'post_cap'
    };

    // CodeStage AntiCheat ObscuredInt：currentCryptoKey 为 0 时使用静态密钥。
    // 与 18 方框透视读取 HealthData 的口径一致。
    var OBSCURED_INT_STATIC_KEY = 0x6C81C;

    var RVA = {
        Entity_OnEntityHurt: 0x00B3F470,
        Player_OnEntityHurt: 0x00B516B0,
        GameManager_TakeDamage: 0x00AFC1C0,
        Player_get_isMyPlayer: 0x00B55FD0,
        Entity_get_team: 0x001E0070,
        SingletonGet: 0x004A8170,
        GM_Singleton_MethodInfo: 0x00E1CE64,
        SentryGun_SetData: 0x00B1E030,
        WPN_Missile_SetOwner: 0x00B66390,
        GameManager_GameRoundEnd: 0x00AFAA40,
        GameManager_NewGameRoundStart: 0x00AEBCB0,
        GameManager_OnDestroy: 0x00AEBD40
    };

    var OFF = {
        Dmg_attacker: 0x00,
        Dmg_victim: 0x04,
        Dmg_damage: 0x08,
        Dmg_type: 0x34,
        Dmg_damageTag: 0x38,
        Dmg_wpnIndex: 0x3C,
        Dmg_wpnSprIndex: 0x40,
        Dmg_ignoreDmgRate: 0x44,
        Entity_team: 0x20,
        Entity_healthData: 0x1C,
        HealthData_currentHealthKey: 0x08,
        HealthData_currentHealthHidden: 0x0C,
        GM_allPlayers: 0x1C,
        GM_playersBL: 0x20,
        GM_playersGR: 0x28,
        Array_len: 0x0C,
        Array_data: 0x10,
        List_items: 0x08,
        List_size: 0x0C
    };

    var Runtime = {
        feature_id: "damage_multiplier",
        enabled: false,
        initialized: false,
        // GameManager.TakeDamage 入口钩子是否安装成功：
        // 安装失败时退回旧行为（全部在 OnEntityHurt 收尾段处理，含致死一击跳过）。
        preCapHookInstalled: false,
        module: null,
        base: ptr(0),
        hooks: [],
        playerHurtDepth: 0,
        missileOwners: {},
        sentryOwners: {},
        ownerTtlMs: 15000,
        // 玩家缓存：用于把 attacker 归到 self / mate / enemy
        playerCache: {},
        playerCacheAt: 0,
        playerCacheMissAt: 0,
        playerCacheTtlMs: 2000,
        localPlayer: ptr(0),
        localTeam: -1,
        config: {
            enemy_multiplier: 1.0,
            self_multiplier: 2.0,
            mate_multiplier: 1.0,
            enemy_enabled: true,
            self_enabled: true,
            mate_enabled: true,
            min_multiplier: 0.1,
            max_multiplier: 10.0,
            max_damage: 999999.0,
            min_applied_damage: 1.0,
            skip_local_victim: true,
            include_infect: false,
            allow_other_damage_type: true,
            enable_owner_mapping: true,
            diagnostic_log: true
        },
        stats: {
            totalHurtEvents: 0,
            entityHurtEvents: 0,
            playerHurtEvents: 0,
            takeDamageCalls: 0,
            preCapHurtEvents: 0,
            preCapMultiplied: 0,
            postCapMultiplied: 0,
            skippedKnifeAtPreCap: 0,
            skippedNonKnifeAtPostCap: 0,
            skippedLethalCapped: 0,
            victimHpReadFailures: 0,
            multipliedEvents: 0,
            multipliedEnemy: 0,
            multipliedSelf: 0,
            multipliedMate: 0,
            flooredToMin: 0,
            skippedDisabled: 0,
            skippedPlayerBaseDepth: 0,
            skippedInvalidEvent: 0,
            skippedInvalidDamage: 0,
            skippedDamageType: 0,
            skippedInfect: 0,
            skippedUnknownAttacker: 0,
            skippedCategoryDisabled: 0,
            skippedLocalVictim: 0,
            missileOwnerHits: 0,
            sentryOwnerHits: 0,
            missileOwnerRecords: 0,
            sentryOwnerRecords: 0,
            playerCacheRefreshes: 0,
            playerCacheMisses: 0,
            errorCount: 0,
            cleanupCount: 0,
            lastOriginalDamage: 0.0,
            lastNewDamage: 0.0,
            lastDamageType: 0,
            lastDamageTag: 0,
            lastWpnIndex: -1,
            lastWpnSprIndex: -1,
            lastIgnoreDmgRate: false,
            lastCategory: "",
            lastMultiplier: 0.0,
            lastSource: "",
            lastDecision: "",
            lastError: ""
        }
    };

    var native = {
        ready: false,
        isMyPlayer: null,
        singletonGetter: null
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

    function sendStatus(feature, enabled) {
        try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (_) {}
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

    function clampFloat(value, minValue, maxValue) {
        var n = Number(value);
        if (!isFinite(n)) return minValue;
        if (n < minValue) return minValue;
        if (n > maxValue) return maxValue;
        return n;
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
        } catch (error) {
            setError('initNativeFunctions failed', error);
            native.ready = false;
            return false;
        }

        // 单人实例 getter 是可选的：拿不到 GameManager 时，阵营判定退回直接读 team 字段。
        try {
            native.singletonGetter = new NativeFunction(
                Runtime.base.add(RVA.SingletonGet),
                'pointer',
                ['pointer'],
                CALL_CONV
            );
        } catch (error) {
            native.singletonGetter = null;
            setError('init singletonGetter failed', error);
        }

        native.ready = true;
        return true;
    }

    function isLocalPlayer(entityPtr) {
        if (isNull(entityPtr) || !isReadablePtr(entityPtr)) return false;
        if (!native.ready && !initNativeFunctions()) return false;
        try {
            return !!native.isMyPlayer(entityPtr, ptr(0));
        } catch (error) {
            setError('Player.get_isMyPlayer failed', error);
            return false;
        }
    }

    // Entity.get_team() 只是返回 +0x20 的字段；直接读内存比调 NativeFunction 安全，
    // Frida 的非法内存访问会抛 JS 异常，而 NativeFunction 调坏指针会直接崩进程。
    function readEntityTeam(entityPtr) {
        if (isNull(entityPtr) || !isReadablePtr(entityPtr)) return -1;
        try {
            var team = entityPtr.add(OFF.Entity_team).readS32();
            if (team < 0 || team > 2) return -1;
            return team;
        } catch (error) {
            return -1;
        }
    }

    // 读受害者当前血量（HealthData.currentHealth 是 CodeStage ObscuredInt）。
    // 只用于「刀的致死一击判定」：当 data.damage 已经被游戏钳到剩余血量时，
    // 说明这一刀本来就致死，再乘 <1 的倍率会让血量按比例几何衰减。
    // 读不到返回 -1，调用方退回正常乘算——绝不因为读血量失败而漏改伤害。
    function readVictimCurrentHealth(victimPtr) {
        try {
            if (isNull(victimPtr) || !isReadablePtr(victimPtr)) return -1;
            var health = victimPtr.add(OFF.Entity_healthData).readPointer();
            if (isNull(health) || !isReadablePtr(health)) return -1;
            var key = health.add(OFF.HealthData_currentHealthKey).readS32();
            var hidden = health.add(OFF.HealthData_currentHealthHidden).readS32();
            var resolvedKey = key !== 0 ? key : OBSCURED_INT_STATIC_KEY;
            var hp = (hidden ^ resolvedKey) >>> 0;
            if (hp > 1000000) return -1;
            return hp;
        } catch (error) {
            return -1;
        }
    }

    function ptrKey(p) {
        try { return p.toString(); } catch (_) { return '0x0'; }
    }

    function pruneOwners(map) {
        var now = Date.now();
        Object.keys(map).forEach(function (key) {
            if (!map[key] || map[key].expiresAt <= now) delete map[key];
        });
    }

    function rememberOwner(map, objectPtr, ownerPtr, kind) {
        if (!Runtime.config.enable_owner_mapping) return;
        if (isNull(objectPtr) || isNull(ownerPtr)) return;
        if (!isReadablePtr(objectPtr) || !isReadablePtr(ownerPtr)) return;
        pruneOwners(map);
        map[ptrKey(objectPtr)] = {
            owner: ownerPtr,
            expiresAt: Date.now() + Runtime.ownerTtlMs
        };
        if (kind === 'missile') Runtime.stats.missileOwnerRecords += 1;
        if (kind === 'sentry') Runtime.stats.sentryOwnerRecords += 1;
    }

    function getRememberedOwner(map, objectPtr) {
        if (!Runtime.config.enable_owner_mapping || isNull(objectPtr)) return ptr(0);
        pruneOwners(map);
        var item = map[ptrKey(objectPtr)];
        if (!item) return ptr(0);
        if (isNull(item.owner) || !isReadablePtr(item.owner)) {
            delete map[ptrKey(objectPtr)];
            return ptr(0);
        }
        return item.owner || ptr(0);
    }

    function clearOwnerMaps(reason) {
        Runtime.missileOwners = {};
        Runtime.sentryOwners = {};
        // P1：不能在这里重置重入计数——本函数可能由"回合结束"在伤害调用栈内触发，
        // 清零会让 Entity 钩子的重入跳过失效，同一个 DamageEventData 被乘两次。
        // playerHurtDepth 由伤害钩子自己配对增减。
        logLimited('owner_clear:' + reason, 'info', 'owner maps cleared: ' + reason, 1000);
    }

    function clearPlayerCache(reason) {
        Runtime.playerCache = {};
        Runtime.playerCacheAt = 0;
        Runtime.localPlayer = ptr(0);
        Runtime.localTeam = -1;
        logLimited('player_cache_clear:' + reason, 'info', 'player cache cleared: ' + reason, 1000);
    }

    // ------------------------------------------------------------------
    // GameManager / 玩家列表
    // ------------------------------------------------------------------
    function getGameManager() {
        if (!native.ready && !initNativeFunctions()) return null;
        if (!native.singletonGetter) return null;
        try {
            var methodInfo = Runtime.base.add(RVA.GM_Singleton_MethodInfo).readPointer();
            if (!isReadablePtr(methodInfo)) return null;
            var gm = native.singletonGetter(methodInfo);
            if (isNull(gm)) return null;
            return gm;
        } catch (error) {
            return null;
        }
    }

    function readArrayList(arrPtr) {
        var result = [];
        if (!isReadablePtr(arrPtr)) return result;
        try {
            var length = arrPtr.add(OFF.Array_len).readU32();
            if (length < 0 || length > 256) return result;
            for (var i = 0; i < length; i++) {
                var elem = arrPtr.add(OFF.Array_data + i * Process.pointerSize).readPointer();
                if (isReadablePtr(elem)) result.push(elem);
            }
        } catch (error) {
            setError('readArrayList failed', error);
        }
        return result;
    }

    function readPlayerList(listPtr) {
        var result = [];
        if (!isReadablePtr(listPtr)) return result;
        try {
            var items = listPtr.add(OFF.List_items).readPointer();
            if (!isReadablePtr(items)) return result;
            var count = listPtr.add(OFF.List_size).readS32();
            if (count < 0 || count > 256) return result;
            for (var i = 0; i < count; i++) {
                var elem = items.add(OFF.Array_data + i * Process.pointerSize).readPointer();
                if (isReadablePtr(elem)) result.push(elem);
            }
        } catch (error) {
            setError('readPlayerList failed', error);
        }
        return result;
    }

    function collectPlayers(gm) {
        var map = {};
        var all = readArrayList(gm.add(OFF.GM_allPlayers).readPointer());
        var bl = readPlayerList(gm.add(OFF.GM_playersBL).readPointer());
        var gr = readPlayerList(gm.add(OFF.GM_playersGR).readPointer());
        [all, bl, gr].forEach(function (list) {
            for (var i = 0; i < list.length; i++) {
                map[ptrKey(list[i])] = list[i];
            }
        });
        return Object.keys(map).map(function (key) { return map[key]; });
    }

    // 刷新玩家缓存：谁是自己、每个人属于哪个队伍。
    // 只在缓存过期或遇到没见过的 attacker 时刷新，不在每次伤害里遍历。
    function refreshPlayerCache(force) {
        var now = Date.now();
        if (!force && Runtime.playerCacheAt && now - Runtime.playerCacheAt < Runtime.playerCacheTtlMs) {
            return;
        }
        Runtime.playerCacheAt = now;
        Runtime.stats.playerCacheRefreshes += 1;
        try {
            var gm = getGameManager();
            if (!gm) return;
            var players = collectPlayers(gm);
            var cache = {};
            var localPtr = ptr(0);
            var localTeam = -1;
            for (var i = 0; i < players.length; i++) {
                var p = players[i];
                var team = readEntityTeam(p);
                if (team < 0) continue;
                var mine = isLocalPlayer(p);
                cache[ptrKey(p)] = { ptr: p, team: team, isLocal: mine };
                if (mine) {
                    localPtr = p;
                    localTeam = team;
                }
            }
            Runtime.playerCache = cache;
            if (!isNull(localPtr)) {
                Runtime.localPlayer = localPtr;
                Runtime.localTeam = localTeam;
            }
        } catch (error) {
            setError('refreshPlayerCache failed', error);
        }
    }

    // 把伤害来源（已解析 owner 之后）归到 self / mate / enemy。
    //
    // 队伍必须"实时读"，不能用玩家缓存里的快照：
    // 游戏在 ModeBase_Nano.UpdateNanoRole 里每次换角色都会 set_nanoRole 之后
    // 调用 SetTeam(NanoRoleExpand.GetTeam(role))，也就是"人类 <-> 生化幽灵"
    // 一变身就立刻改写 Entity.team。缓存带 2s TTL，变身那一瞬间还是旧阵营，
    // 会把刚变幽灵的队友/自己判错，所以要按当前 team 现算。
    function classifyAttacker(attacker) {
        if (isNull(attacker) || !isReadablePtr(attacker)) return Category.UNKNOWN;

        if (isLocalPlayer(attacker)) {
            Runtime.localPlayer = attacker;
            return Category.SELF;
        }

        if (isNull(Runtime.localPlayer) || !isLocalPlayer(Runtime.localPlayer)) {
            refreshPlayerCache(true);
        } else if (!Runtime.playerCacheAt || Date.now() - Runtime.playerCacheAt >= Runtime.playerCacheTtlMs) {
            refreshPlayerCache(false);
        }
        if (isNull(Runtime.localPlayer)) return Category.UNKNOWN;

        var team = readEntityTeam(attacker);
        var localTeam = readEntityTeam(Runtime.localPlayer);

        if (team < 0 || localTeam < 0) {
            // 刚加入房间、还没进过玩家缓存的对象：限频刷新一次玩家列表再试。
            Runtime.stats.playerCacheMisses += 1;
            var now = Date.now();
            if (!Runtime.playerCacheMissAt || now - Runtime.playerCacheMissAt > 1000) {
                Runtime.playerCacheMissAt = now;
                refreshPlayerCache(true);
            }
            team = readEntityTeam(attacker);
            localTeam = readEntityTeam(Runtime.localPlayer);
            if (team < 0 || localTeam < 0) return Category.UNKNOWN;
        }

        Runtime.localTeam = localTeam;

        // 与 ExpandUtil.IsSameTeam 一致：Neutral(2) 不算同队。
        if (team !== 2 && localTeam !== 2 && team === localTeam) {
            return Category.MATE;
        }
        return Category.ENEMY;
    }

    function categoryMultiplierKey(category) {
        return category + '_multiplier';
    }

    function categoryEnabledKey(category) {
        return category + '_enabled';
    }

    function resolveEffectiveAttacker(attacker) {
        if (isNull(attacker)) return ptr(0);

        var missileOwner = getRememberedOwner(Runtime.missileOwners, attacker);
        if (!isNull(missileOwner)) {
            Runtime.stats.missileOwnerHits += 1;
            return missileOwner;
        }

        var sentryOwner = getRememberedOwner(Runtime.sentryOwners, attacker);
        if (!isNull(sentryOwner)) {
            Runtime.stats.sentryOwnerHits += 1;
            return sentryOwner;
        }

        return attacker;
    }

    function isSupportedDamageType(type) {
        if (type === DamageType.Gun || type === DamageType.Knife || type === DamageType.Grenade) return true;
        if (type === DamageType.Other && Runtime.config.allow_other_damage_type) return true;
        return false;
    }

    function readDamageEvent(eventPtr) {
        if (isNull(eventPtr) || !isReadablePtr(eventPtr)) return null;
        try {
            return {
                attacker: eventPtr.add(OFF.Dmg_attacker).readPointer(),
                victim: eventPtr.add(OFF.Dmg_victim).readPointer(),
                damage: eventPtr.add(OFF.Dmg_damage).readFloat(),
                type: eventPtr.add(OFF.Dmg_type).readS32(),
                damageTag: eventPtr.add(OFF.Dmg_damageTag).readS32(),
                wpnIndex: eventPtr.add(OFF.Dmg_wpnIndex).readS32(),
                wpnSprIndex: eventPtr.add(OFF.Dmg_wpnSprIndex).readS32(),
                ignoreDmgRate: eventPtr.add(OFF.Dmg_ignoreDmgRate).readU8() !== 0
            };
        } catch (error) {
            setError('read DamageEventData failed', error);
            return null;
        }
    }

    function recordLast(data, source, decision, newDamage, category, multiplier) {
        Runtime.stats.lastOriginalDamage = data ? data.damage : 0.0;
        Runtime.stats.lastNewDamage = newDamage === undefined ? 0.0 : newDamage;
        Runtime.stats.lastDamageType = data ? data.type : 0;
        Runtime.stats.lastDamageTag = data ? data.damageTag : 0;
        Runtime.stats.lastWpnIndex = data ? data.wpnIndex : -1;
        Runtime.stats.lastWpnSprIndex = data ? data.wpnSprIndex : -1;
        Runtime.stats.lastIgnoreDmgRate = data ? data.ignoreDmgRate : false;
        Runtime.stats.lastCategory = category || "";
        Runtime.stats.lastMultiplier = multiplier === undefined ? 0.0 : multiplier;
        Runtime.stats.lastSource = source || "";
        Runtime.stats.lastDecision = decision || "";
    }

    function formatFloat(value) {
        if (!isFinite(value)) return String(value);
        return value.toFixed(3);
    }

    function logDamageDiagnostic(data, source, stage, category, multiplier, newDamage, effectiveAttacker, victim, victimIsLocal, flooredToMin, victimHp) {
        if (!Runtime.config.diagnostic_log) return;

        var truncDamage = newDamage < 0 ? Math.ceil(newDamage) : Math.floor(newDamage);
        var message = 'damage_diag source=' + source +
            ' stage=' + stage +
            ' category=' + category +
            ' raw_damage=' + formatFloat(data.damage) +
            ' multiplier=' + formatFloat(multiplier) +
            ' new_damage=' + formatFloat(newDamage) +
            ' trunc=' + truncDamage +
            ' floor=' + Math.floor(newDamage) +
            ' round=' + Math.round(newDamage) +
            ' ceil=' + Math.ceil(newDamage) +
            ' below_one=' + (newDamage > 0 && newDamage < 1) +
            ' floored_to_min=' + flooredToMin +
            ' victim_hp=' + victimHp +
            ' type=' + data.type +
            ' tag=' + data.damageTag +
            ' wpn=' + data.wpnIndex +
            ' spr=' + data.wpnSprIndex +
            ' attacker=' + ptrKey(data.attacker) +
            ' effective_attacker=' + ptrKey(effectiveAttacker) +
            ' victim=' + ptrKey(victim) +
            ' victim_is_local=' + victimIsLocal +
            ' ignoreDmgRate=' + data.ignoreDmgRate;

        logLimited('damage_diagnostic', 'info', message, 300);
    }

    // stage:
    //   DamageStage.PRE_CAP  — GameManager.TakeDamage 入口。damage 还是原始伤害，
    //                          游戏随后才会 ×防御率、min(剩余血量)。只处理非刀伤害。
    //   DamageStage.POST_CAP — Entity/Player.OnEntityHurt。游戏已经做完防御/钳血。
    //                          只处理刀（生化模式会在 TakeDamage 内部按角色重写刀伤），
    //                          并且对“已经被钳成致死一击”的刀不再削弱。
    function multiplyDamageEvent(eventPtr, source, stage) {
        Runtime.stats.totalHurtEvents += 1;
        if (!Runtime.enabled) {
            Runtime.stats.skippedDisabled += 1;
            return false;
        }

        var data = readDamageEvent(eventPtr);
        if (!data) {
            Runtime.stats.skippedInvalidEvent += 1;
            recordLast(null, source, 'invalid_event');
            return false;
        }

        var isPreCap = (stage === DamageStage.PRE_CAP);

        // 阶段路由：
        //   入口段不碰刀——生化模式的 CalKnifeDmg 会按角色把刀伤重写成固定值，
        //   在入口乘的倍率会被覆盖，只能在 OnEntityHurt 收尾段乘。
        //   收尾段不碰非刀——它们在入口段已经乘过，这里再乘会变成平方。
        if (isPreCap) {
            Runtime.stats.preCapHurtEvents += 1;
            if (data.type === DamageType.Knife) {
                Runtime.stats.skippedKnifeAtPreCap += 1;
                return false;
            }
        } else if (Runtime.preCapHookInstalled && data.type !== DamageType.Knife) {
            Runtime.stats.skippedNonKnifeAtPostCap += 1;
            return false;
        }

        if (!isFinite(data.damage) || data.damage <= 0) {
            Runtime.stats.skippedInvalidDamage += 1;
            recordLast(data, source, 'invalid_damage');
            return false;
        }

        if (data.type === DamageType.Infect && !Runtime.config.include_infect) {
            Runtime.stats.skippedInfect += 1;
            recordLast(data, source, 'skip_infect');
            return false;
        }

        if (!isSupportedDamageType(data.type)) {
            Runtime.stats.skippedDamageType += 1;
            recordLast(data, source, 'skip_damage_type');
            return false;
        }

        var effectiveAttacker = resolveEffectiveAttacker(data.attacker);
        var category = classifyAttacker(effectiveAttacker);
        if (category === Category.UNKNOWN) {
            Runtime.stats.skippedUnknownAttacker += 1;
            recordLast(data, source, 'skip_unknown_attacker');
            return false;
        }

        var victim = data.victim;
        var victimIsLocal = isLocalPlayer(victim);

        // 只拦"自己打自己"（自己的手雷炸自己），不拦敌人/队友打本地玩家。
        if (category === Category.SELF && Runtime.config.skip_local_victim && victimIsLocal) {
            Runtime.stats.skippedLocalVictim += 1;
            recordLast(data, source, 'skip_self_victim', undefined, category);
            return false;
        }

        if (!Runtime.config[categoryEnabledKey(category)]) {
            Runtime.stats.skippedCategoryDisabled += 1;
            recordLast(data, source, 'skip_' + category + '_disabled', undefined, category);
            return false;
        }

        var multiplier = clampFloat(
            Runtime.config[categoryMultiplierKey(category)],
            Runtime.config.min_multiplier,
            Runtime.config.max_multiplier
        );

        var victimHp = -1; // 入口段不读血量（用不到），日志里显示 -1
        var newDamage;
        var flooredToMin = false;

        if (!isPreCap) {
            // 收尾段（刀；或入口钩子安装失败时兜底处理全部伤害）：
            // data.damage 在 TakeDamage 里已经被钳到 min(伤害, 剩余血量)。
            // 当它 >= 剩余血量，说明这一击本来就是致死一击；再乘 <1 的倍率会变成
            // “按剩余血量比例扣血”，血量几何级衰减，永远磨到 1 滴血才死。
            victimHp = readVictimCurrentHealth(victim);
            if (victimHp < 0) Runtime.stats.victimHpReadFailures += 1;
            if (multiplier < 1.0 && victimHp > 0 && data.damage + 0.001 >= victimHp) {
                Runtime.stats.skippedLethalCapped += 1;
                recordLast(data, source, 'skip_lethal_capped', undefined, category, multiplier);
                logLimited(
                    'skip_lethal_capped',
                    'info',
                    'lethal blow not weakened: source=' + source + ' category=' + category +
                    ' damage=' + data.damage.toFixed(2) + ' victim_hp=' + victimHp +
                    ' multiplier=' + multiplier.toFixed(2),
                    500
                );
                return false;
            }
        }

        newDamage = data.damage * multiplier;
        if (newDamage > Runtime.config.max_damage) newDamage = Runtime.config.max_damage;
        if (newDamage < 0) newDamage = 0;

        // 保底 1 点：游戏用 cvttsd2si 把 float damage 截断成 int，
        // 倍率 <1 时若把一击压到 1 点以下，游戏会收到 0 点伤害，
        // 导致目标永远卡在最后一滴血。原本 >=1 点的一击至少保留 1 点。
        // 入口段之后游戏还会 ×防御率（正常为 1.0），所以正常场景下保底有效。
        if (data.damage >= Runtime.config.min_applied_damage &&
            newDamage < Runtime.config.min_applied_damage) {
            newDamage = Runtime.config.min_applied_damage;
            flooredToMin = true;
            Runtime.stats.flooredToMin += 1;
        }

        logDamageDiagnostic(data, source, stage, category, multiplier, newDamage, effectiveAttacker, victim, victimIsLocal, flooredToMin, victimHp);

        try {
            var damageAddr = eventPtr.add(OFF.Dmg_damage);
            damageAddr.writeFloat(newDamage);
            Runtime.stats.multipliedEvents += 1;
            if (isPreCap) Runtime.stats.preCapMultiplied += 1;
            else Runtime.stats.postCapMultiplied += 1;
            if (category === Category.SELF) Runtime.stats.multipliedSelf += 1;
            else if (category === Category.MATE) Runtime.stats.multipliedMate += 1;
            else if (category === Category.ENEMY) Runtime.stats.multipliedEnemy += 1;
            recordLast(data, source, 'multiplied', newDamage, category, multiplier);
            if (Runtime.config.diagnostic_log) {
                logLimited(
                    'multiplied',
                    'info',
                    source + ' [' + category + '] damage ' + data.damage.toFixed(2) + ' -> ' + newDamage.toFixed(2) +
                    ', type=' + data.type + ', wpn=' + data.wpnIndex + ', stage=' + stage,
                    500
                );
            }
            return true;
        } catch (error) {
            setError('write damage failed', error);
            recordLast(data, source, 'write_failed', undefined, category);
            return false;
        }
    }

    function eventDataFromOnEntityHurtStack(context) {
        // x86 cdecl: [ESP+4] = this, [ESP+8] = DamageEventData.attacker.
        return context.esp.add(8);
    }

    function eventDataFromTakeDamageStack(context) {
        // GameManager.TakeDamage 是静态方法：x86 cdecl 下 [ESP+4] 就是
        // DamageEventData.attacker（没有 this）。40 开火直伤已验证过这个 ABI，
        // 注意 onEnter 的 esp 指向返回地址，所以是 +4 而不是 +0。
        return context.esp.add(4);
    }

    function attachHook(name, rva, callbacks) {
        var addr = Runtime.base.add(rva);
        var hook = Interceptor.attach(addr, callbacks);
        Runtime.hooks.push({ name: name, hook: hook });
        log('success', name + ' hook installed at ' + addr);
    }

    function attachHooks() {
        attachHook('Player.OnEntityHurt', RVA.Player_OnEntityHurt, {
            onEnter: function () {
                Runtime.playerHurtDepth += 1;
                Runtime.stats.playerHurtEvents += 1;
                this.depthEntered = true;
                try {
                    multiplyDamageEvent(eventDataFromOnEntityHurtStack(this.context), 'Player.OnEntityHurt', DamageStage.POST_CAP);
                } catch (error) {
                    setError('Player.OnEntityHurt onEnter failed', error);
                }
            },
            onLeave: function () {
                if (this.depthEntered) Runtime.playerHurtDepth = Math.max(0, Runtime.playerHurtDepth - 1);
            }
        });

        attachHook('Entity.OnEntityHurt', RVA.Entity_OnEntityHurt, {
            onEnter: function () {
                Runtime.stats.entityHurtEvents += 1;
                if (Runtime.playerHurtDepth > 0) {
                    Runtime.stats.skippedPlayerBaseDepth += 1;
                    return;
                }
                try {
                    multiplyDamageEvent(eventDataFromOnEntityHurtStack(this.context), 'Entity.OnEntityHurt', DamageStage.POST_CAP);
                } catch (error) {
                    setError('Entity.OnEntityHurt onEnter failed', error);
                }
            }
        });

        attachHook('WPN_Missile.SetOwner', RVA.WPN_Missile_SetOwner, {
            onEnter: function (args) {
                try {
                    rememberOwner(Runtime.missileOwners, args[0], args[1], 'missile');
                } catch (error) {
                    setError('WPN_Missile.SetOwner failed', error);
                }
            }
        });

        attachHook('SentryGun.SetData', RVA.SentryGun_SetData, {
            onEnter: function (args) {
                try {
                    rememberOwner(Runtime.sentryOwners, args[0], args[1], 'sentry');
                } catch (error) {
                    setError('SentryGun.SetData failed', error);
                }
            }
        });

        attachHook('GameManager.GameRoundEnd', RVA.GameManager_GameRoundEnd, {
            onEnter: function () {
                try {
                    clearOwnerMaps("game_round_end");
                    clearPlayerCache("game_round_end");
                } catch (error) {
                    setError('GameManager.GameRoundEnd failed', error);
                }
            }
        });

        attachHook('GameManager.NewGameRoundStart', RVA.GameManager_NewGameRoundStart, {
            onEnter: function () {
                try {
                    clearOwnerMaps("new_game_round_start");
                    clearPlayerCache("new_game_round_start");
                } catch (error) {
                    setError('GameManager.NewGameRoundStart failed', error);
                }
            }
        });

        attachHook('GameManager.OnDestroy', RVA.GameManager_OnDestroy, {
            onEnter: function () {
                try {
                    clearOwnerMaps("game_manager_destroy");
                    clearPlayerCache("game_manager_destroy");
                } catch (error) {
                    setError('GameManager.OnDestroy failed', error);
                }
            }
        });

        // 入口段：枪/雷/技能/炮台在游戏「×防御率 → min(剩余血量)」之前乘倍率，
        // 这样最终伤害 = 原始伤害 × 倍率，和受害者剩余血量无关。
        // 安装失败不阻断功能：退回「全部在 OnEntityHurt 收尾段处理」（含致死一击跳过）。
        try {
            attachHook('GameManager.TakeDamage', RVA.GameManager_TakeDamage, {
                onEnter: function () {
                    Runtime.stats.takeDamageCalls += 1;
                    try {
                        multiplyDamageEvent(
                            eventDataFromTakeDamageStack(this.context),
                            'GameManager.TakeDamage',
                            DamageStage.PRE_CAP
                        );
                    } catch (error) {
                        setError('GameManager.TakeDamage onEnter failed', error);
                    }
                }
            });
            Runtime.preCapHookInstalled = true;
        } catch (error) {
            Runtime.preCapHookInstalled = false;
            setError('GameManager.TakeDamage hook install failed', error);
            log('info', 'GameManager.TakeDamage hook failed; fallback to OnEntityHurt-only mode');
        }
    }

    function cleanupHooks() {
        Runtime.hooks.forEach(function (item) {
            try { item.hook.detach(); } catch (_) {}
        });
        Runtime.hooks = [];
    }

    function resetRuntimeStats() {
        Object.keys(Runtime.stats).forEach(function (key) {
            if (typeof Runtime.stats[key] === 'number') Runtime.stats[key] = 0;
            else if (typeof Runtime.stats[key] === 'boolean') Runtime.stats[key] = false;
            else Runtime.stats[key] = "";
        });
        Runtime.stats.lastWpnIndex = -1;
        Runtime.stats.lastWpnSprIndex = -1;
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

    function enableFeature() {
        if (!initializeFeature()) return getStatus();
        Runtime.enabled = true;
        sendStatus('damage_multiplier', true);
        log('success', 'damage multiplier enabled, enemy=' + Runtime.config.enemy_multiplier +
            ' self=' + Runtime.config.self_multiplier + ' mate=' + Runtime.config.mate_multiplier);
        return getStatus();
    }

    function disableFeature() {
        Runtime.enabled = false;
        sendStatus('damage_multiplier', false);
        log('info', 'damage multiplier disabled');
        return getStatus();
    }

    function cleanupFeature() {
        Runtime.enabled = false;
        cleanupHooks();
        Runtime.initialized = false;
        Runtime.preCapHookInstalled = false;
        clearOwnerMaps("cleanup");
        clearPlayerCache("cleanup");
        Runtime.stats.cleanupCount += 1;
        log('info', 'cleanup complete');
        return getStatus();
    }

    function updateConfig(config) {
        config = config || {};

        // 兼容旧配置：老的单倍率 key「multiplier」等同「自己」倍率。
        if (config.self_multiplier === undefined && config.multiplier !== undefined) {
            Runtime.config.self_multiplier = clampFloat(
                config.multiplier,
                Runtime.config.min_multiplier,
                Runtime.config.max_multiplier
            );
        }

        ['enemy_multiplier', 'self_multiplier', 'mate_multiplier'].forEach(function (key) {
            if (config[key] !== undefined) {
                Runtime.config[key] = clampFloat(
                    config[key],
                    Runtime.config.min_multiplier,
                    Runtime.config.max_multiplier
                );
            }
        });

        [
            'enemy_enabled',
            'self_enabled',
            'mate_enabled',
            'skip_local_victim',
            'include_infect',
            'allow_other_damage_type',
            'enable_owner_mapping',
            'diagnostic_log'
        ].forEach(function (key) {
            if (config[key] !== undefined) Runtime.config[key] = !!config[key];
        });

        if (config.max_damage !== undefined) {
            Runtime.config.max_damage = clampFloat(config.max_damage, 1.0, 99999999.0);
        }
        if (config.min_applied_damage !== undefined) {
            Runtime.config.min_applied_damage = clampFloat(
                config.min_applied_damage,
                0.0,
                Runtime.config.max_damage
            );
        }
        return getStatus();
    }

    function getStatus() {
        return {
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            pre_cap_hook_installed: Runtime.preCapHookInstalled,
            module_found: Runtime.module !== null,
            enemy_multiplier: Runtime.config.enemy_multiplier,
            self_multiplier: Runtime.config.self_multiplier,
            mate_multiplier: Runtime.config.mate_multiplier,
            enemy_enabled: Runtime.config.enemy_enabled,
            self_enabled: Runtime.config.self_enabled,
            mate_enabled: Runtime.config.mate_enabled,
            multiplier: Runtime.config.self_multiplier,
            min_multiplier: Runtime.config.min_multiplier,
            max_multiplier: Runtime.config.max_multiplier,
            min_applied_damage: Runtime.config.min_applied_damage,
            local_player_ready: !isNull(Runtime.localPlayer),
            local_team: Runtime.localTeam,
            cached_player_count: Object.keys(Runtime.playerCache).length,
            skip_local_victim: Runtime.config.skip_local_victim,
            include_infect: Runtime.config.include_infect,
            allow_other_damage_type: Runtime.config.allow_other_damage_type,
            enable_owner_mapping: Runtime.config.enable_owner_mapping,
            diagnostic_log: Runtime.config.diagnostic_log,
            total_hurt_events: Runtime.stats.totalHurtEvents,
            entity_hurt_events: Runtime.stats.entityHurtEvents,
            player_hurt_events: Runtime.stats.playerHurtEvents,
            take_damage_calls: Runtime.stats.takeDamageCalls,
            pre_cap_hurt_events: Runtime.stats.preCapHurtEvents,
            pre_cap_multiplied: Runtime.stats.preCapMultiplied,
            post_cap_multiplied: Runtime.stats.postCapMultiplied,
            skipped_knife_precap: Runtime.stats.skippedKnifeAtPreCap,
            skipped_non_knife_postcap: Runtime.stats.skippedNonKnifeAtPostCap,
            skipped_lethal_capped: Runtime.stats.skippedLethalCapped,
            victim_hp_read_failures: Runtime.stats.victimHpReadFailures,
            multiplied_events: Runtime.stats.multipliedEvents,
            multiplied_enemy: Runtime.stats.multipliedEnemy,
            multiplied_self: Runtime.stats.multipliedSelf,
            multiplied_mate: Runtime.stats.multipliedMate,
            floored_to_min: Runtime.stats.flooredToMin,
            skipped_disabled: Runtime.stats.skippedDisabled,
            skipped_player_base_depth: Runtime.stats.skippedPlayerBaseDepth,
            skipped_invalid_event: Runtime.stats.skippedInvalidEvent,
            skipped_invalid_damage: Runtime.stats.skippedInvalidDamage,
            skipped_damage_type: Runtime.stats.skippedDamageType,
            skipped_infect: Runtime.stats.skippedInfect,
            skipped_unknown_attacker: Runtime.stats.skippedUnknownAttacker,
            skipped_category_disabled: Runtime.stats.skippedCategoryDisabled,
            skipped_local_victim: Runtime.stats.skippedLocalVictim,
            missile_owner_hits: Runtime.stats.missileOwnerHits,
            sentry_owner_hits: Runtime.stats.sentryOwnerHits,
            missile_owner_records: Runtime.stats.missileOwnerRecords,
            sentry_owner_records: Runtime.stats.sentryOwnerRecords,
            player_cache_refreshes: Runtime.stats.playerCacheRefreshes,
            player_cache_misses: Runtime.stats.playerCacheMisses,
            error_count: Runtime.stats.errorCount,
            cleanup_count: Runtime.stats.cleanupCount,
            last_original_damage: Runtime.stats.lastOriginalDamage,
            last_new_damage: Runtime.stats.lastNewDamage,
            last_damage_type: Runtime.stats.lastDamageType,
            last_damage_tag: Runtime.stats.lastDamageTag,
            last_wpn_index: Runtime.stats.lastWpnIndex,
            last_wpn_spr_index: Runtime.stats.lastWpnSprIndex,
            last_ignore_dmg_rate: Runtime.stats.lastIgnoreDmgRate,
            last_category: Runtime.stats.lastCategory,
            last_multiplier: Runtime.stats.lastMultiplier,
            last_source: Runtime.stats.lastSource,
            last_decision: Runtime.stats.lastDecision,
            last_error: Runtime.stats.lastError
        };
    }

    rpc.exports = {
        enable: function (config) {
            updateConfig(config);
            return enableFeature();
        },
        disable: function () {
            return disableFeature();
        },
        status: function () {
            if (!Runtime.module) findGameAssembly();
            return getStatus();
        },
        cleanup: function () {
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
        }
    };
})();
