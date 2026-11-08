// ============================================================
// lifesteal / script.js  —— 伤害吸血（05 单功能：41-伤害吸血）
//
// feature_id: "lifesteal"
//
// 功能目标：
//   玩家对敌人造成生命伤害时，按「实际扣掉的血量 × 吸血比例」回复本地玩家血量。
//   吸血比例用一个 0% ~ 100% 的滑块调整；不同伤害来源可以分别开关。
//
// 核心取舍（为什么 Hook HealthData.Hurt，而不是在 OnEntityHurt 里改数据）：
//   1. 游戏最终扣血链路（IDA 反汇编确认）：
//        GameManager.TakeDamage(data)
//          -> damage = min((int)(data.damage * victim.damageRate), 剩余血量)   // 先乘防御率再钳血
//          -> victim.OnEntityHurt(data)
//               -> int dmg = (int)data.damage
//               -> HealthData.Hurt(healthData, dmg)                        // 真正扣血
//   2. HealthData.Hurt 的入参 dmg 就是「这一击实际扣掉的血量」：
//      已经过伤害倍率功能（TakeDamage 入口 / OnEntityHurt 收尾）、防御率、剩余血量钳制、
//      float -> int 截断。因此吸血量天然跟随「调整伤害倍率」「开火直伤」等功能的最终结果，
//      不需要知道伤害是怎么被改出来的。
//   3. 吸血动作在 HealthData.Hurt 的调用栈里执行，但只对「本地玩家自己的 HealthData」调用
//      HealthData.Heal，不写任何加密字段（currentHealth / maxHealth 是 ObscuredInt）。
//
// 伤害来源识别：
//   1. Hook Entity.OnEntityHurt / Player.OnEntityHurt，在 x86 cdecl 栈上定位按值传入的
//      DamageEventData（[esp+8] 起），读出 attacker / victim / type / damageTag / wpnIndex。
//   2. 攻击者先还原成真正的玩家（手雷/RPG 的 attacker 通常已经是玩家；
//      若 attacker 是 missile / 炮台实体，则读它自己的 owner 字段），
//      再和本地玩家指针比较；只有本地玩家造成的伤害才进入待结算队列。
//   3. HealthData.Hurt 命中时，用「受伤者 HealthData 指针 + 时间窗」匹配到刚才的
//      DamageEventData 上下文，拿到 type / wpnIndex，完成分类与过滤。
//
// 武器分类：
//   DamageEventData.type：Gun(1) / Knife(2) / Grenade(3) / Infect(4) / Other(5)
//   DamageEventData.wpnIndex：和 WeaponData.wpnIndex 同一个值（手雷 GetBasicDamageEventData 已确认）。
//   通过本地玩家 PlayerWeapons 里每把武器 Weapon.data -> WeaponData.wpnIndex / wpnClass
//   建立 wpnIndex -> WeaponClass 映射：
//     Rifle/Sniper/MachineGun/SubmachineGun/ShotGun -> 主武器
//     Pistol                                       -> 副武器
//     Gun 的 wpnIndex 映射到枪械类 + type=Knife    -> 枪托重击（枪械近战）
//     Knife 类（或映射不到）                       -> 近战武器
//     Grenade                                      -> 投掷 / 爆炸（含手雷、RPG/AT4、榴弹）
//     Other                                        -> 特殊 / 技能（炮台等）
//     Infect                                       -> 感染（默认关闭）
//
// RVA / 字段来源：dump.cs + IDA 反汇编（GameAssembly_part3/part4 .lst）+ 现有功能交叉验证
//   Entity_OnEntityHurt:           0x00B3F470   void OnEntityHurt(DamageEventData)
//   Player_OnEntityHurt:           0x00B516B0   void OnEntityHurt(DamageEventData)
//   HealthData_Hurt:               0x00AE45B0   void Hurt(int)
//   HealthData_Heal:               0x00AE44F0   void Heal(int)
//   HealthData_get_isDead:         0x00AE4830   bool get_isDead()
//   GameManager_TypeInfo:          0x00E2933C   Il2CppClass*（static_fields@0x5C, myPlayer@0x00）
//   Player.get_isMyPlayer:         0x00B55FD0   bool get_isMyPlayer()
//     —— 反汇编确认它内部就是 Object.op_Equality(GameManager.myPlayer, this)，
//        所以本地玩家身份改为纯内存读静态字段，不再从 JS 调用这个托管方法。
//   ObscuredInt_TypeInfo:          0x00E2D848   （key==0 时解密要读静态 cryptoKey）
//   GameManager_GameRoundEnd:      0x00AFAA40
//   GameManager_NewGameRoundStart: 0x00AEBCB0
//   GameManager_OnDestroy:         0x00AEBD40
//
//   DamageEventData.attacker   0x00
//   DamageEventData.victim     0x04
//   DamageEventData.damage     0x08
//   DamageEventData.type       0x34
//   DamageEventData.damageTag  0x38
//   DamageEventData.wpnIndex   0x3C
//   Entity.healthData          0x1C
//   Entity.team                0x20
//   Player.wpns                0xA0
//   PlayerWeapons.all          0x0C (List<Weapon>: items+0x08 / size+0x0C)
//   PlayerWeapons.inUse        0x18
//   PlayerWeapons.current      0x1C
//   PlayerWeapons.normal       0x20
//   PlayerWeapons.special      0x24
//   PlayerWeapons.temporaryWpn 0x28
//   PlayerWeapons.F_KeyWpn     0x2C
//   Weapon.data                0x68
//   WeaponData.wpnIndex        0x0C
//   WeaponData.wpnClass        0x10
//   WeaponData.weaponName      0x14
//   WPN_Missile.owner          0x30   （结算时只读，不 Hook SetWeaponData）
//   SentryGun.owner            0x64   （结算时只读，不 Hook SetData）
//   HealthData.currentHealth   0x08 (ObscuredInt: key+0 / hidden+4 / inited+8)
//   HealthData.maxHealth       0x1C
//
// 已知边界（详见「伤害吸血-简要说明.md」）：
//   - 感染伤害（DamageType.Infect）：Entity.OnEntityHurt 对 type==4 直接 return，不走
//     HealthData.Hurt；本功能默认不包含，也无法用通用链路吸血。
//   - SentryGun / TombStone 覆写了 OnEntityHurt 并自行改 damage / 调 Hurt，
//     不在本功能的上下文里，因此「打掉敌方炮台/墓碑」不产生吸血。
//   - 找不到归属（地图机关、环境伤害、非玩家来源的 missile）不吸血。
//   - 主武器 / 副武器 / 枪托重击的细分依赖 wpnIndex -> WeaponClass 映射；
//     映射缺失时，Gun 归入「主武器」，Knife 归入「近战武器」，不会丢失吸血。
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

    var WeaponClass = {
        Rifle: 0,
        Sniper: 1,
        MachineGun: 2,
        SubmachineGun: 3,
        ShotGun: 4,
        Pistol: 5,
        Knife: 6,
        Grenade: 7,
        FlashBang: 8,
        SmokeGrenade: 9
    };

    var CATEGORY_LABEL = {
        gun_primary: '主武器',
        gun_secondary: '副武器',
        gun_stock: '枪托重击',
        knife: '近战武器',
        grenade: '投掷/爆炸',
        special: '特殊/技能',
        infect: '感染'
    };

    var CATEGORY_KEYS = ['gun_primary', 'gun_secondary', 'gun_stock', 'knife', 'grenade', 'special', 'infect'];

    var RVA = {
        Entity_OnEntityHurt: 0x00B3F470,
        Player_OnEntityHurt: 0x00B516B0,
        HealthData_Hurt: 0x00AE45B0,
        HealthData_Heal: 0x00AE44F0,
        HealthData_get_isDead: 0x00AE4830,
        // 本地玩家 = GameManager.myPlayer 静态字段：
        //   [0x00E2933C] -> Il2CppClass* -> +0x5C static_fields -> +0x00 myPlayer
        // 纯内存读，任何线程（含 Frida RPC 线程）调用都安全。
        GameManager_TypeInfo: 0x00E2933C,
        ObscuredInt_TypeInfo: 0x00E2D848,
        GameManager_GameRoundEnd: 0x00AFAA40,
        GameManager_NewGameRoundStart: 0x00AEBCB0,
        GameManager_OnDestroy: 0x00AEBD40
    };

    var OFF = {
        Dmg_attacker: 0x00,
        Dmg_victim: 0x04,
        Dmg_type: 0x34,
        Dmg_damageTag: 0x38,
        Dmg_wpnIndex: 0x3C,

        Entity_healthData: 0x1C,
        Entity_team: 0x20,

        Il2CppClass_staticFields: 0x5C,
        GameManager_myPlayer: 0x00,

        Player_wpns: 0xA0,

        PW_all: 0x0C,
        PW_inUse: 0x18,
        PW_current: 0x1C,
        PW_normal: 0x20,
        PW_special: 0x24,
        PW_temporaryWpn: 0x28,
        PW_FKeyWpn: 0x2C,

        List_items: 0x08,
        List_size: 0x0C,

        Array_len: 0x0C,
        Array_data: 0x10,

        Weapon_data: 0x68,

        WeaponData_wpnIndex: 0x0C,
        WeaponData_wpnClass: 0x10,
        WeaponData_weaponName: 0x14,

        Missile_owner: 0x30,
        Sentry_owner: 0x64,

        Health_currentHealth: 0x08,
        Health_maxHealth: 0x1C,
        Obscured_inited: 0x08
    };

    var ConfigKeys = {
        percent: 'lifesteal_percent',
        onlyEnemy: 'only_enemy_victim',
        diagnostic: 'diagnostic_log',
        maxPending: 'max_pending_heal'
    };

    var Runtime = {
        feature_id: 'lifesteal',
        enabled: false,
        initialized: false,
        generation: 0,
        module: null,
        base: ptr(0),
        hooks: [],
        tokenSeq: 0,

        // 当前正在执行的 OnEntityHurt 上下文（栈式，支持嵌套伤害）
        contexts: [],

        // 本地玩家与缓存
        localPlayer: ptr(0),
        localPlayerAt: 0,
        localPlayerRefreshMs: 1000,

        // wpnIndex -> WeaponClass / 名称
        weaponMap: {},
        weaponMapAt: 0,
        weaponMapRefreshMs: 2000,
        weaponMapTtlMs: 60000,

        // 吸血量累积（float，满 1 点才真正回血，避免小伤害被截断丢失）
        pendingHeal: 0.0,

        config: {
            lifesteal_percent: 10.0,
            src_gun_primary_enabled: true,
            src_gun_secondary_enabled: true,
            src_gun_stock_enabled: true,
            src_knife_enabled: true,
            src_grenade_enabled: true,
            src_special_enabled: true,
            src_infect_enabled: false,
            only_enemy_victim: true,
            diagnostic_log: true,
            max_pending_heal: 5000.0
        },

        stats: {
            hurtEvents: 0,
            hurtHookHits: 0,
            localDamageEvents: 0,
            healedEvents: 0,
            healCalls: 0,
            healedTotal: 0,

            skippedDisabled: 0,
            skippedInvalidEvent: 0,
            skippedInvalidDamage: 0,
            skippedNotLocal: 0,
            skippedSelfVictim: 0,
            skippedMateVictim: 0,
            skippedCategoryDisabled: 0,
            skippedUnknownCategory: 0,
            skippedNoVictimHealth: 0,
            skippedNoLocal: 0,
            skippedDead: 0,
            skippedNoContext: 0,
            skippedDuplicate: 0,
            skippedZeroHeal: 0,

            // 攻击者还原统计（attacker 本身是 missile / 炮台实体时，从对象字段读到玩家）
            attackerMissileResolved: 0,
            attackerSentryResolved: 0,

            weaponMapRefreshes: 0,
            weaponMapMisses: 0,
            localPlayerRefreshes: 0,
            localPlayerMisses: 0,

            catHeals: {},
            catEvents: {},

            errorCount: 0,
            cleanupCount: 0,
            lastError: '',
            lastResetReason: '',

            lastDamage: 0,
            lastHeal: 0,
            lastHp: -1,
            lastMaxHp: -1,
            lastCategory: '',
            lastType: 0,
            lastTag: 0,
            lastWpnIndex: -1,
            lastWpnClass: -1,
            lastWpnName: '',
            lastDecision: ''
        }
    };

    // 只在游戏线程（Hook 回调）里调用的原生函数。
    // 本地玩家 / GameManager 不在这里——它们走静态字段内存读。
    var native = {
        ready: false,
        heal: null,
        isDead: null
    };

    var LogLimiter = {};

    // ------------------------------------------------------------------
    // 基础工具
    // ------------------------------------------------------------------

    function log(level, message) {
        try {
            var text = '[' + Runtime.feature_id + '][' + level + '] ' + message;
            console.log(text);
            send({ type: 'log', level: level, module: Runtime.feature_id, message: message });
        } catch (_) {
        }
    }

    function sendStatus(enabled) {
        try { send({ type: 'status', feature: Runtime.feature_id, enabled: enabled }); } catch (_) {}
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

        // 连续异常兜底：避免在坏指针上反复调用原生函数把游戏拖垮。
        if (Runtime.stats.errorCount >= 20 && Runtime.enabled) {
            Runtime.enabled = false;
            resetRuntime('too_many_errors');
            log('error', 'lifesteal auto-disabled after too many errors');
            sendStatus(false);
        }
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

    function samePtr(a, b) {
        if (isNull(a) || isNull(b)) return false;
        try { return a.equals(b); } catch (_) { return false; }
    }

    function ptrKey(p) {
        try { return p.toString(); } catch (_) { return '0x0'; }
    }

    function clampFloat(value, minValue, maxValue) {
        var n = Number(value);
        if (!isFinite(n)) return minValue;
        if (n < minValue) return minValue;
        if (n > maxValue) return maxValue;
        return n;
    }

    function toBool(value) {
        if (value === false || value === 0 || value === '0' || value === 'false' ||
            value === '' || value === null || value === undefined) {
            return false;
        }
        return true;
    }

    function formatFloat(value) {
        if (!isFinite(value)) return String(value);
        return value.toFixed(2);
    }

    function safeReadPointer(base, offset) {
        try {
            if (!isReadablePtr(base)) return ptr(0);
            var p = base.add(offset).readPointer();
            if (!isReadablePtr(p)) return ptr(0);
            return p;
        } catch (_) {
            return ptr(0);
        }
    }

    function safeReadS32(base, offset) {
        try {
            if (!isReadablePtr(base)) return 0;
            return base.add(offset).readS32();
        } catch (_) {
            return 0;
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

    // ------------------------------------------------------------------
    // 原生函数
    // ------------------------------------------------------------------

    function initNativeFunctions() {
        if (native.ready) return true;
        var mod = findGameAssembly();
        if (!mod) return false;

        if (Process.arch !== 'ia32' || Process.pointerSize !== 4) {
            Runtime.stats.lastError = 'unsupported process: arch=' + Process.arch + ', pointerSize=' + Process.pointerSize;
            log('error', Runtime.stats.lastError);
            return false;
        }

        // 注意：这里只保留「写入血量」和「读死亡状态」两个原生调用。
        // 本地玩家身份 / GameManager 实例一律走静态字段内存读，
        // 不在 Frida RPC 线程里调用游戏托管方法（线程安全红线）。
        try {
            native.heal = new NativeFunction(
                Runtime.base.add(RVA.HealthData_Heal),
                'void',
                ['pointer', 'int', 'pointer'],
                CALL_CONV
            );
            native.isDead = new NativeFunction(
                Runtime.base.add(RVA.HealthData_get_isDead),
                'bool',
                ['pointer', 'pointer'],
                CALL_CONV
            );
        } catch (error) {
            setError('initNativeFunctions failed', error);
            native.ready = false;
            return false;
        }

        native.ready = true;
        return true;
    }

    // ------------------------------------------------------------------
    // GameManager 静态字段 / 本地玩家
    // ------------------------------------------------------------------

    // 本地玩家 = GameManager.myPlayer 静态字段。
    // 反汇编 Player.get_isMyPlayer(0x00B55FD0) 确认它内部就是：
    //   Object.op_Equality(GameManager.static_fields.myPlayer, this)
    // 因此这里直接读静态字段，语义完全等价，且不调用任何游戏托管方法。
    function readStaticMyPlayer() {
        try {
            if (isNull(Runtime.base)) return ptr(0);
            var typeInfo = Runtime.base.add(RVA.GameManager_TypeInfo).readPointer();
            if (!isReadablePtr(typeInfo)) return ptr(0);
            var staticFields = typeInfo.add(OFF.Il2CppClass_staticFields).readPointer();
            if (!isReadablePtr(staticFields)) return ptr(0);
            var player = staticFields.add(OFF.GameManager_myPlayer).readPointer();
            if (!isReadablePtr(player)) return ptr(0);
            return player;
        } catch (_) {
            return ptr(0);
        }
    }

    function readArrayList(arrPtr) {
        var result = [];
        if (!isReadablePtr(arrPtr)) return result;
        try {
            var length = arrPtr.add(OFF.Array_len).readS32();
            if (length <= 0 || length > 512) return result;
            for (var i = 0; i < length; i++) {
                var elem = arrPtr.add(OFF.Array_data + i * Process.pointerSize).readPointer();
                if (isReadablePtr(elem)) result.push(elem);
            }
        } catch (_) {
            Runtime.stats.errorCount += 1;
        }
        return result;
    }

    function readWeaponList(listPtr) {
        var result = [];
        if (!isReadablePtr(listPtr)) return result;
        try {
            var items = listPtr.add(OFF.List_items).readPointer();
            if (!isReadablePtr(items)) return result;
            var count = listPtr.add(OFF.List_size).readS32();
            if (count <= 0 || count > 256) return result;
            for (var i = 0; i < count; i++) {
                var elem = items.add(OFF.Array_data + i * Process.pointerSize).readPointer();
                if (isReadablePtr(elem)) result.push(elem);
            }
        } catch (_) {
            Runtime.stats.errorCount += 1;
        }
        return result;
    }

    function readEntityTeam(entityPtr) {
        if (isNull(entityPtr) || !isReadablePtr(entityPtr)) return -1;
        try {
            var team = entityPtr.add(OFF.Entity_team).readS32();
            if (team < 0 || team > 2) return -1;
            return team;
        } catch (_) {
            return -1;
        }
    }

    function readHealthDataPtr(entityPtr) {
        return safeReadPointer(entityPtr, OFF.Entity_healthData);
    }

    // 刷新「谁是本地玩家」。只读 GameManager.myPlayer 静态字段：
    //   * 不遍历玩家列表，不调用 get_isMyPlayer / Singleton.get_instance；
    //   * 全程纯内存读，Frida RPC 线程调用也安全
    //     （2.7 修过的“在错误线程里调游戏函数”隐患，本功能不再重犯）。
    function refreshLocalPlayer(force) {
        var now = Date.now();
        if (!force && Runtime.localPlayerAt && (now - Runtime.localPlayerAt) < Runtime.localPlayerRefreshMs) {
            return;
        }
        Runtime.localPlayerAt = now;
        Runtime.stats.localPlayerRefreshes += 1;

        try {
            var found = readStaticMyPlayer();

            if (isNull(found)) {
                if (!isNull(Runtime.localPlayer)) {
                    logLimited('local_lost', 'info', 'local player lost, clear cache', 1000);
                }
                Runtime.localPlayer = ptr(0);
                Runtime.stats.localPlayerMisses += 1;
                return;
            }

            if (!samePtr(Runtime.localPlayer, found)) {
                logLimited('local_changed', 'info', 'local player = ' + ptrKey(found), 500);
                Runtime.localPlayer = found;
            }
        } catch (error) {
            setError('refreshLocalPlayer failed', error);
        }
    }

    function getValidLocalPlayer() {
        refreshLocalPlayer(false);

        if (isNull(Runtime.localPlayer)) return ptr(0);
        if (!isReadablePtr(Runtime.localPlayer)) {
            Runtime.localPlayer = ptr(0);
            return ptr(0);
        }
        return Runtime.localPlayer;
    }

    function isLocalAttacker(attacker) {
        if (isNull(attacker) || !isReadablePtr(attacker)) return false;

        var local = getValidLocalPlayer();
        return !isNull(local) && samePtr(attacker, local);
    }

    // ------------------------------------------------------------------
    // 攻击者归属还原（零 Hook，纯内存读）
    // ------------------------------------------------------------------
    //
    // 以前是 Hook WPN_Missile.SetWeaponData / SentryGun.SetData 记录映射，
    // 但 0x00B663C0 正好是「26 手雷模式」tuner 组改写 missile 字段的同一个地址，
    // 为彻底避免两个功能在同一函数上叠加监听，这里改成结算时直接读对象字段：
    //   1) attacker 本身就是 Player -> 直接用；
    //   2) attacker 是 missile / 炮台实体 -> 读 [attacker+0x30] / [attacker+0x64]，
    //      只有读出来的指针仍像 Player 才采用。
    // 代价：没有「先登记后结算」的缓存，但这几类伤害的 owner 在对象生命周期内是稳定的。
    function looksLikePlayer(p) {
        if (isNull(p) || !isReadablePtr(p)) return false;
        return !isNull(safeReadPointer(p, OFF.Player_wpns)) &&
            !isNull(safeReadPointer(p, OFF.Entity_healthData));
    }

    function resolveEffectiveAttacker(attacker) {
        if (isNull(attacker) || !isReadablePtr(attacker)) return attacker;

        if (looksLikePlayer(attacker)) return attacker;

        var owner = safeReadPointer(attacker, OFF.Missile_owner);
        if (looksLikePlayer(owner)) {
            Runtime.stats.attackerMissileResolved += 1;
            return owner;
        }

        owner = safeReadPointer(attacker, OFF.Sentry_owner);
        if (looksLikePlayer(owner)) {
            Runtime.stats.attackerSentryResolved += 1;
            return owner;
        }

        return attacker;
    }

    // ------------------------------------------------------------------
    // 武器分类映射
    // ------------------------------------------------------------------

    function readIl2CppString(strPtr) {
        try {
            if (isNull(strPtr) || !isReadablePtr(strPtr)) return '';
            var length = strPtr.add(8).readS32();
            if (length <= 0 || length > 128) return '';
            return strPtr.add(0x0C).readUtf16String(length);
        } catch (_) {
            return '';
        }
    }

    function registerWeapon(weaponPtr) {
        if (isNull(weaponPtr) || !isReadablePtr(weaponPtr)) return;

        var dataPtr = safeReadPointer(weaponPtr, OFF.Weapon_data);
        if (isNull(dataPtr)) return;

        var wpnIndex = safeReadS32(dataPtr, OFF.WeaponData_wpnIndex);
        if (wpnIndex < 0 || wpnIndex > 100000) return;

        var wpnClass = safeReadS32(dataPtr, OFF.WeaponData_wpnClass);
        if (wpnClass < WeaponClass.Rifle || wpnClass > WeaponClass.SmokeGrenade) wpnClass = -1;
        var name = readIl2CppString(safeReadPointer(dataPtr, OFF.WeaponData_weaponName));

        Runtime.weaponMap[wpnIndex] = {
            wpnIndex: wpnIndex,
            wpnClass: wpnClass,
            name: name,
            expiresAt: Date.now() + Runtime.weaponMapTtlMs
        };
    }

    function refreshWeaponMap(force) {
        var now = Date.now();
        if (!force && Runtime.weaponMapAt && (now - Runtime.weaponMapAt) < Runtime.weaponMapRefreshMs) {
            return;
        }
        Runtime.weaponMapAt = now;
        Runtime.stats.weaponMapRefreshes += 1;

        try {
            var local = getValidLocalPlayer();
            if (isNull(local)) return;

            var wpns = safeReadPointer(local, OFF.Player_wpns);
            if (isNull(wpns)) return;

            var weapons = readWeaponList(safeReadPointer(wpns, OFF.PW_all));

            var singlePtrs = [
                safeReadPointer(wpns, OFF.PW_inUse),
                safeReadPointer(wpns, OFF.PW_temporaryWpn),
                safeReadPointer(wpns, OFF.PW_FKeyWpn)
            ];
            for (var i = 0; i < singlePtrs.length; i++) {
                if (!isNull(singlePtrs[i])) weapons.push(singlePtrs[i]);
            }

            var arrayPtrs = [
                safeReadPointer(wpns, OFF.PW_current),
                safeReadPointer(wpns, OFF.PW_normal),
                safeReadPointer(wpns, OFF.PW_special)
            ];
            for (var a = 0; a < arrayPtrs.length; a++) {
                var arr = arrayPtrs[a];
                var list = readArrayList(arr);
                for (var j = 0; j < list.length; j++) weapons.push(list[j]);
            }

            for (var w = 0; w < weapons.length; w++) registerWeapon(weapons[w]);

            // 过期条目清理
            Object.keys(Runtime.weaponMap).forEach(function (key) {
                if (Runtime.weaponMap[key].expiresAt <= now) delete Runtime.weaponMap[key];
            });
        } catch (error) {
            setError('refreshWeaponMap failed', error);
        }
    }

    function getWeaponInfo(wpnIndex) {
        if (wpnIndex < 0) return null;
        refreshWeaponMap(false);
        var info = Runtime.weaponMap[wpnIndex];
        if (info && info.expiresAt > Date.now()) return info;
        Runtime.stats.weaponMapMisses += 1;
        return null;
    }

    function isGunClass(wpnClass) {
        return wpnClass === WeaponClass.Rifle ||
            wpnClass === WeaponClass.Sniper ||
            wpnClass === WeaponClass.MachineGun ||
            wpnClass === WeaponClass.SubmachineGun ||
            wpnClass === WeaponClass.ShotGun ||
            wpnClass === WeaponClass.Pistol;
    }

    // 把 DamageEventData 分类成 UI 上的「伤害来源」。
    function classifySource(type, wpnClass) {
        if (type === DamageType.Gun) {
            return wpnClass === WeaponClass.Pistol ? 'gun_secondary' : 'gun_primary';
        }
        if (type === DamageType.Knife) {
            return isGunClass(wpnClass) ? 'gun_stock' : 'knife';
        }
        if (type === DamageType.Grenade) return 'grenade';
        if (type === DamageType.Infect) return 'infect';
        if (type === DamageType.Other) {
            // 枪械近战在部分武器上会以 Other 出现；wpnIndex 指向枪械时归入枪托重击。
            return isGunClass(wpnClass) ? 'gun_stock' : 'special';
        }
        return '';
    }

    function isCategoryEnabled(category) {
        if (!category) return false;
        var key = 'src_' + category + '_enabled';
        return !!Runtime.config[key];
    }

    function isMateVictim(victim, localPlayer) {
        if (isNull(victim) || isNull(localPlayer)) return false;
        var victimTeam = readEntityTeam(victim);
        var localTeam = readEntityTeam(localPlayer);
        if (victimTeam < 0 || localTeam < 0) return false;
        // 与 ExpandUtil.IsSameTeam 一致：Neutral(2) 不算同队。
        return victimTeam !== 2 && localTeam !== 2 && victimTeam === localTeam;
    }

    // ------------------------------------------------------------------
    // DamageEventData 读取 / 上下文栈
    // ------------------------------------------------------------------

    function readDamageEvent(eventPtr) {
        if (isNull(eventPtr) || !isReadablePtr(eventPtr)) return null;
        try {
            return {
                attacker: eventPtr.add(OFF.Dmg_attacker).readPointer(),
                victim: eventPtr.add(OFF.Dmg_victim).readPointer(),
                type: eventPtr.add(OFF.Dmg_type).readS32(),
                damageTag: eventPtr.add(OFF.Dmg_damageTag).readS32(),
                wpnIndex: eventPtr.add(OFF.Dmg_wpnIndex).readS32()
            };
        } catch (error) {
            setError('read DamageEventData failed', error);
            return null;
        }
    }

    function trimContexts() {
        if (Runtime.contexts.length > 16) {
            Runtime.contexts.splice(0, Runtime.contexts.length - 16);
        }
        var now = Date.now();
        while (Runtime.contexts.length && (now - Runtime.contexts[0].at) > 2000) {
            Runtime.contexts.shift();
        }
    }

    function pushContextFromStack(stackContext) {
        Runtime.stats.hurtEvents += 1;

        if (!Runtime.enabled) {
            Runtime.stats.skippedDisabled += 1;
            return 0;
        }

        var data = readDamageEvent(stackContext.esp.add(8));
        if (!data) {
            Runtime.stats.skippedInvalidEvent += 1;
            return 0;
        }

        var effectiveAttacker = resolveEffectiveAttacker(data.attacker);
        if (!isLocalAttacker(effectiveAttacker)) {
            Runtime.stats.skippedNotLocal += 1;
            return 0;
        }

        var localPlayer = getValidLocalPlayer();
        if (isNull(localPlayer)) {
            Runtime.stats.skippedNoLocal += 1;
            return 0;
        }

        // 自己打自己（自己的手雷 / 摔伤等）不吸血
        if (samePtr(data.victim, localPlayer)) {
            Runtime.stats.skippedSelfVictim += 1;
            return 0;
        }

        if (Runtime.config.only_enemy_victim && isMateVictim(data.victim, localPlayer)) {
            Runtime.stats.skippedMateVictim += 1;
            return 0;
        }

        var victimHealth = readHealthDataPtr(data.victim);
        if (isNull(victimHealth)) {
            Runtime.stats.skippedNoVictimHealth += 1;
            return 0;
        }

        var info = getWeaponInfo(data.wpnIndex);
        var wpnClass = info ? info.wpnClass : -1;
        var category = classifySource(data.type, wpnClass);

        if (!category) {
            Runtime.stats.skippedUnknownCategory += 1;
            Runtime.stats.lastDecision = 'skip_unknown_category';
            return 0;
        }
        if (!isCategoryEnabled(category)) {
            Runtime.stats.skippedCategoryDisabled += 1;
            Runtime.stats.lastCategory = category;
            Runtime.stats.lastDecision = 'skip_' + category + '_disabled';
            return 0;
        }

        Runtime.tokenSeq += 1;
        var ctx = {
            token: Runtime.tokenSeq,
            victim: data.victim,
            victimHealth: victimHealth,
            type: data.type,
            damageTag: data.damageTag,
            wpnIndex: data.wpnIndex,
            wpnClass: wpnClass,
            wpnName: info ? info.name : '',
            category: category,
            at: Date.now(),
            consumed: false
        };

        Runtime.contexts.push(ctx);
        trimContexts();
        return ctx.token;
    }

    function popContextByToken(token) {
        if (!token) return;
        for (var i = Runtime.contexts.length - 1; i >= 0; i--) {
            if (Runtime.contexts[i].token === token) {
                Runtime.contexts.splice(i, 1);
                return;
            }
        }
    }

    function findContextForHealth(victimHealth) {
        var now = Date.now();
        for (var i = Runtime.contexts.length - 1; i >= 0; i--) {
            var ctx = Runtime.contexts[i];
            if ((now - ctx.at) > 2000) {
                Runtime.contexts.splice(i, 1);
                continue;
            }
            if (samePtr(ctx.victimHealth, victimHealth)) return ctx;
        }
        return null;
    }

    // ------------------------------------------------------------------
    // 血量读取（只读，不写 ObscuredInt 字段）
    // ------------------------------------------------------------------

    function readObscuredInt(basePtr, offset) {
        try {
            if (isNull(basePtr) || !isReadablePtr(basePtr)) return null;

            var key = basePtr.add(offset).readS32();
            var hidden = basePtr.add(offset + 4).readS32();
            var inited = basePtr.add(offset + 8).readU8();
            if (!inited) return null;

            var realKey = key;
            if (realKey === 0) {
                // 与游戏 Decrypt(value, key) 一致：key==0 时用 ObscuredInt 的静态 cryptoKey。
                var typeInfo = Runtime.base.add(RVA.ObscuredInt_TypeInfo).readPointer();
                if (isReadablePtr(typeInfo)) {
                    var staticFields = typeInfo.add(0x5C).readPointer();
                    if (isReadablePtr(staticFields)) realKey = staticFields.readS32();
                }
            }

            return (hidden ^ realKey) | 0;
        } catch (_) {
            return null;
        }
    }

    function readHealthPair(healthData) {
        var result = { hp: null, maxHp: null };
        if (isNull(healthData)) return result;
        result.hp = readObscuredInt(healthData, OFF.Health_currentHealth);
        result.maxHp = readObscuredInt(healthData, OFF.Health_maxHealth);
        return result;
    }

    // ------------------------------------------------------------------
    // 核心：HealthData.Hurt 命中后结算吸血
    // ------------------------------------------------------------------

    function recordLast(ctx, damage, heal, hp, maxHp, decision) {
        Runtime.stats.lastDamage = damage;
        Runtime.stats.lastHeal = heal;
        Runtime.stats.lastHp = hp === null || hp === undefined ? -1 : hp;
        Runtime.stats.lastMaxHp = maxHp === null || maxHp === undefined ? -1 : maxHp;
        Runtime.stats.lastCategory = ctx ? ctx.category : '';
        Runtime.stats.lastType = ctx ? ctx.type : 0;
        Runtime.stats.lastTag = ctx ? ctx.damageTag : 0;
        Runtime.stats.lastWpnIndex = ctx ? ctx.wpnIndex : -1;
        Runtime.stats.lastWpnClass = ctx ? ctx.wpnClass : -1;
        Runtime.stats.lastWpnName = ctx ? ctx.wpnName : '';
        Runtime.stats.lastDecision = decision || '';
    }

    function logDiagnostic(ctx, damage, heal, hpBefore, hpAfter) {
        if (!Runtime.config.diagnostic_log) return;
        var label = CATEGORY_LABEL[ctx.category] || ctx.category;
        var message = 'lifesteal_diag source=' + ctx.category + '(' + label + ')' +
            ' type=' + ctx.type +
            ' tag=' + ctx.damageTag +
            ' wpn=' + ctx.wpnIndex +
            ' wpn_class=' + ctx.wpnClass +
            ' wpn_name=' + (ctx.wpnName || '-') +
            ' damage=' + damage +
            ' heal=' + formatFloat(heal) +
            ' hp_before=' + (hpBefore === null ? '?' : hpBefore) +
            ' hp_after=' + (hpAfter === null ? '?' : hpAfter) +
            ' percent=' + formatFloat(Runtime.config.lifesteal_percent);
        logLimited('lifesteal_diag', 'info', message, 400);
    }

    function onHealthHurt(healthData, damage) {
        Runtime.stats.hurtHookHits += 1;

        if (!Runtime.enabled) {
            Runtime.stats.skippedDisabled += 1;
            return;
        }

        if (!isFinite(damage) || damage <= 0) {
            Runtime.stats.skippedInvalidDamage += 1;
            return;
        }

        var ctx = findContextForHealth(healthData);
        if (!ctx) {
            // 不是本地玩家发起的伤害（Bot 互殴、环境伤害、炮台自毁、墓碑回收等）
            Runtime.stats.skippedNoContext += 1;
            return;
        }

        if (ctx.consumed) {
            Runtime.stats.skippedDuplicate += 1;
            return;
        }
        ctx.consumed = true;

        // 同一个 DamageEventData 可能同时经过 Player.OnEntityHurt 与基类 Entity.OnEntityHurt
        // （两层上下文），但 HealthData.Hurt 只会命中一次；统计按「真正结算的伤害事件」计。
        Runtime.stats.localDamageEvents += 1;
        Runtime.stats.catEvents[ctx.category] = (Runtime.stats.catEvents[ctx.category] || 0) + 1;

        var localPlayer = getValidLocalPlayer();
        if (isNull(localPlayer)) {
            Runtime.stats.skippedNoLocal += 1;
            recordLast(ctx, damage, 0, null, null, 'skip_no_local');
            return;
        }

        var localHealth = readHealthDataPtr(localPlayer);
        if (isNull(localHealth)) {
            Runtime.stats.skippedNoLocal += 1;
            recordLast(ctx, damage, 0, null, null, 'skip_no_health');
            return;
        }

        var hpBefore = readHealthPair(localHealth);

        // 死亡状态下不调用 Heal：HealthData 只做数值加减，直接回血会绕过复活流程。
        try {
            if (native.ready && native.isDead(localHealth, ptr(0))) {
                Runtime.pendingHeal = 0.0;
                Runtime.stats.skippedDead += 1;
                recordLast(ctx, damage, 0, hpBefore.hp, hpBefore.maxHp, 'skip_dead');
                return;
            }
        } catch (error) {
            setError('HealthData.get_isDead failed', error);
            Runtime.stats.skippedDead += 1;
            recordLast(ctx, damage, 0, hpBefore.hp, hpBefore.maxHp, 'skip_dead_check_failed');
            return;
        }

        var percent = clampFloat(Runtime.config.lifesteal_percent, 0.0, 100.0);
        if (percent <= 0.0) {
            Runtime.stats.skippedZeroHeal += 1;
            recordLast(ctx, damage, 0, hpBefore.hp, hpBefore.maxHp, 'skip_percent_zero');
            return;
        }

        var healFloat = damage * percent / 100.0;
        Runtime.pendingHeal += healFloat;
        if (Runtime.pendingHeal > Runtime.config.max_pending_heal) {
            Runtime.pendingHeal = Runtime.config.max_pending_heal;
        }

        var amount = Math.floor(Runtime.pendingHeal);
        if (amount < 1) {
            recordLast(ctx, damage, 0, hpBefore.hp, hpBefore.maxHp, 'accumulate');
            return;
        }
        Runtime.pendingHeal -= amount;

        try {
            native.heal(localHealth, amount, ptr(0));
        } catch (error) {
            setError('HealthData.Heal failed', error);
            Runtime.pendingHeal += amount;
            recordLast(ctx, damage, 0, hpBefore.hp, hpBefore.maxHp, 'heal_failed');
            return;
        }

        var hpAfter = readHealthPair(localHealth);
        var actualHeal = amount;
        if (hpBefore.hp !== null && hpAfter.hp !== null) {
            actualHeal = Math.max(0, hpAfter.hp - hpBefore.hp);
        }

        Runtime.stats.healedEvents += 1;
        Runtime.stats.healCalls += 1;
        Runtime.stats.healedTotal += actualHeal;
        Runtime.stats.catHeals[ctx.category] = (Runtime.stats.catHeals[ctx.category] || 0) + actualHeal;

        recordLast(ctx, damage, actualHeal, hpAfter.hp, hpAfter.maxHp, 'healed');

        logDiagnostic(ctx, damage, actualHeal, hpBefore.hp, hpAfter.hp);
        logLimited(
            'healed',
            'info',
            'lifesteal [' + (CATEGORY_LABEL[ctx.category] || ctx.category) + '] damage=' + damage +
            ' -> heal +' + actualHeal + ' (percent=' + formatFloat(percent) + '%)',
            500
        );
    }

    // ------------------------------------------------------------------
    // Hooks
    // ------------------------------------------------------------------

    function attachHook(name, rva, callbacks) {
        try {
            var addr = Runtime.base.add(rva);
            var hook = Interceptor.attach(addr, callbacks);
            Runtime.hooks.push({ name: name, hook: hook });
            log('success', name + ' hook installed at ' + addr);
            return true;
        } catch (error) {
            setError('attach ' + name + ' failed', error);
            return false;
        }
    }

    function attachDamageContextHook(name, rva) {
        return attachHook(name, rva, {
            onEnter: function () {
                try {
                    this._lifestealToken = pushContextFromStack(this.context);
                } catch (error) {
                    setError(name + ' onEnter failed', error);
                    this._lifestealToken = 0;
                }
            },
            onLeave: function () {
                try {
                    popContextByToken(this._lifestealToken);
                } catch (_) {
                }
            }
        });
    }

    function attachHooks() {
        var critical = true;

        critical = attachDamageContextHook('Entity.OnEntityHurt', RVA.Entity_OnEntityHurt) && critical;
        critical = attachDamageContextHook('Player.OnEntityHurt', RVA.Player_OnEntityHurt) && critical;

        // 最终扣血入口：这里拿到的是真正扣掉的血量（已含伤害倍率 / 防御率 / 钳血 / 取整）
        critical = attachHook('HealthData.Hurt', RVA.HealthData_Hurt, {
            onEnter: function (args) {
                try {
                    // Frida 里 args[1] 是 NativePointer；这里兼容裸数字，方便脱离游戏做逻辑测试。
                    var raw = args[1];
                    var damage = (raw && typeof raw.toInt32 === 'function') ? raw.toInt32() : (Number(raw) | 0);
                    onHealthHurt(args[0], damage);
                } catch (error) {
                    setError('HealthData.Hurt onEnter failed', error);
                }
            }
        }) && critical;

        // 生命周期清理。
        // 注意：这里不再挂 WPN_Missile.SetWeaponData / SentryGun.SetData
        // （0x00B663C0 / 0x00B1E030 与「26 手雷模式」「30 伤害倍率」同址，本功能不需要）。
        var lifecycle = [
            ['GameManager.GameRoundEnd', RVA.GameManager_GameRoundEnd, 'game_round_end'],
            ['GameManager.NewGameRoundStart', RVA.GameManager_NewGameRoundStart, 'new_game_round_start'],
            ['GameManager.OnDestroy', RVA.GameManager_OnDestroy, 'game_manager_destroy']
        ];
        lifecycle.forEach(function (item) {
            attachHook(item[0], item[1], {
                onEnter: function () {
                    try {
                        resetRuntime(item[2]);
                    } catch (error) {
                        setError(item[0] + ' failed', error);
                    }
                }
            });
        });

        return critical;
    }

    function cleanupHooks() {
        Runtime.hooks.forEach(function (item) {
            try { item.hook.detach(); } catch (_) {}
        });
        Runtime.hooks = [];
        Runtime.initialized = false;
    }

    // ------------------------------------------------------------------
    // 生命周期
    // ------------------------------------------------------------------

    function resetRuntime(reason) {
        Runtime.generation += 1;
        Runtime.contexts = [];
        Runtime.pendingHeal = 0.0;
        Runtime.localPlayer = ptr(0);
        Runtime.localPlayerAt = 0;
        Runtime.weaponMap = {};
        Runtime.weaponMapAt = 0;
        Runtime.stats.lastResetReason = reason || 'unknown';
        log('info', 'resetRuntime: ' + Runtime.stats.lastResetReason + ', gen=' + Runtime.generation);
    }

    function initializeFeature() {
        if (Runtime.initialized) return true;
        if (!initNativeFunctions()) return false;

        if (!attachHooks()) {
            cleanupHooks();
            return false;
        }

        Runtime.initialized = true;
        return true;
    }

    function enableFeature() {
        if (!initializeFeature()) {
            log('error', 'enable failed: hooks not installed');
            return getStatus();
        }

        Runtime.enabled = true;
        Runtime.stats.errorCount = 0;
        Runtime.stats.lastError = '';
        Runtime.pendingHeal = 0.0;
        sendStatus(true);
        log('success', 'lifesteal enabled, percent=' + formatFloat(Runtime.config.lifesteal_percent) + '%');
        return getStatus();
    }

    function disableFeature() {
        Runtime.enabled = false;
        Runtime.contexts = [];
        Runtime.pendingHeal = 0.0;
        sendStatus(false);
        log('info', 'lifesteal disabled');
        return getStatus();
    }

    function cleanupFeature() {
        Runtime.enabled = false;
        cleanupHooks();
        resetRuntime('cleanup');
        Runtime.stats.cleanupCount += 1;
        log('info', 'cleanup complete');
        return getStatus();
    }

    // ------------------------------------------------------------------
    // 配置 / 状态
    // ------------------------------------------------------------------

    function updateConfig(config) {
        config = config || {};

        if (config.lifesteal_percent !== undefined) {
            Runtime.config.lifesteal_percent = clampFloat(config.lifesteal_percent, 0.0, 100.0);
        } else if (config.percent !== undefined) {
            Runtime.config.lifesteal_percent = clampFloat(config.percent, 0.0, 100.0);
        }

        CATEGORY_KEYS.forEach(function (key) {
            var cfgKey = 'src_' + key + '_enabled';
            if (config[cfgKey] !== undefined) {
                Runtime.config[cfgKey] = toBool(config[cfgKey]);
            }
        });

        if (config.only_enemy_victim !== undefined) {
            Runtime.config.only_enemy_victim = toBool(config.only_enemy_victim);
        }
        if (config.diagnostic_log !== undefined) {
            Runtime.config.diagnostic_log = toBool(config.diagnostic_log);
        }
        if (config.max_pending_heal !== undefined) {
            Runtime.config.max_pending_heal = clampFloat(config.max_pending_heal, 100.0, 1000000.0);
        }

        return getStatus();
    }

    function buildCategoryStatus() {
        var result = {};
        CATEGORY_KEYS.forEach(function (key) {
            result['src_' + key + '_enabled'] = !!Runtime.config['src_' + key + '_enabled'];
            result['healed_' + key] = Runtime.stats.catHeals[key] || 0;
            result['events_' + key] = Runtime.stats.catEvents[key] || 0;
        });
        return result;
    }

    function getStatus() {
        if (!Runtime.module) findGameAssembly();

        var local = getValidLocalPlayer();
        var localHealth = readHealthDataPtr(local);
        var hp = readHealthPair(localHealth);

        var status = {
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            generation: Runtime.generation,
            module_found: Runtime.module !== null,

            lifesteal_percent: Runtime.config.lifesteal_percent,
            only_enemy_victim: Runtime.config.only_enemy_victim,
            diagnostic_log: Runtime.config.diagnostic_log,
            max_pending_heal: Runtime.config.max_pending_heal,

            local_player_ready: !isNull(local),
            local_player: ptrKey(local),
            local_team: readEntityTeam(local),
            local_hp: hp.hp === null ? -1 : hp.hp,
            local_max_hp: hp.maxHp === null ? -1 : hp.maxHp,
            pending_heal: Runtime.pendingHeal,
            weapon_map_size: Object.keys(Runtime.weaponMap).length,
            context_depth: Runtime.contexts.length,

            hook_hits: Runtime.stats.hurtEvents,
            hurt_events: Runtime.stats.hurtEvents,
            hurt_hook_hits: Runtime.stats.hurtHookHits,
            local_damage_events: Runtime.stats.localDamageEvents,
            healed_events: Runtime.stats.healedEvents,
            heal_calls: Runtime.stats.healCalls,
            healed_total: Runtime.stats.healedTotal,

            skipped_disabled: Runtime.stats.skippedDisabled,
            skipped_invalid_event: Runtime.stats.skippedInvalidEvent,
            skipped_invalid_damage: Runtime.stats.skippedInvalidDamage,
            skipped_not_local: Runtime.stats.skippedNotLocal,
            skipped_self_victim: Runtime.stats.skippedSelfVictim,
            skipped_mate_victim: Runtime.stats.skippedMateVictim,
            skipped_category_disabled: Runtime.stats.skippedCategoryDisabled,
            skipped_unknown_category: Runtime.stats.skippedUnknownCategory,
            skipped_no_victim_health: Runtime.stats.skippedNoVictimHealth,
            skipped_no_local: Runtime.stats.skippedNoLocal,
            skipped_dead: Runtime.stats.skippedDead,
            skipped_no_context: Runtime.stats.skippedNoContext,
            skipped_duplicate: Runtime.stats.skippedDuplicate,
            skipped_zero_heal: Runtime.stats.skippedZeroHeal,

            attacker_missile_resolved: Runtime.stats.attackerMissileResolved,
            attacker_sentry_resolved: Runtime.stats.attackerSentryResolved,

            weapon_map_refreshes: Runtime.stats.weaponMapRefreshes,
            weapon_map_misses: Runtime.stats.weaponMapMisses,
            local_player_refreshes: Runtime.stats.localPlayerRefreshes,
            local_player_misses: Runtime.stats.localPlayerMisses,

            error_count: Runtime.stats.errorCount,
            cleanup_count: Runtime.stats.cleanupCount,
            last_error: Runtime.stats.lastError,
            last_reset_reason: Runtime.stats.lastResetReason,

            last_damage: Runtime.stats.lastDamage,
            last_heal: Runtime.stats.lastHeal,
            last_hp: Runtime.stats.lastHp,
            last_max_hp: Runtime.stats.lastMaxHp,
            last_category: Runtime.stats.lastCategory,
            last_type: Runtime.stats.lastType,
            last_tag: Runtime.stats.lastTag,
            last_wpn_index: Runtime.stats.lastWpnIndex,
            last_wpn_class: Runtime.stats.lastWpnClass,
            last_wpn_name: Runtime.stats.lastWpnName,
            last_decision: Runtime.stats.lastDecision
        };

        var categoryStatus = buildCategoryStatus();
        Object.keys(categoryStatus).forEach(function (key) {
            status[key] = categoryStatus[key];
        });
        return status;
    }

    // ------------------------------------------------------------------
    // RPC
    // ------------------------------------------------------------------

    rpc.exports = {
        enable: function (config) {
            updateConfig(config);
            return enableFeature();
        },

        disable: function () {
            return disableFeature();
        },

        status: function () {
            // 已开启但模块还没加载好时，借 UI 的状态轮询自动补装一次 Hook。
            if (Runtime.enabled && !Runtime.initialized) {
                initializeFeature();
            }
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
        },

        reset: function (reason) {
            resetRuntime(reason || 'manual');
            return getStatus();
        }
    };

    // 加载即初始化一次映射用的数据结构
    CATEGORY_KEYS.forEach(function (key) {
        Runtime.stats.catHeals[key] = 0;
        Runtime.stats.catEvents[key] = 0;
    });

    log('info', 'script loaded');
})();
