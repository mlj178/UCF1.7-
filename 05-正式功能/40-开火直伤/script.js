// ============================================================
// script.js — 开火直伤 (feature_id: "direct_damage")
//
// 功能目标
//   开火时不再依赖"子弹射线命中"，直接把伤害结算到选中的敌人身上。
//
//   原版链路：
//     开火 -> Recoil.GetShootRay 生成射线 -> WPN_Gun.Damage(Ray)
//          -> RaycastAll 找命中体 -> 构造 DamageEventData -> 结算伤害
//   本功能链路：
//     开火 -> WPN_Gun.Damage 被替换 -> 选目标 -> 构造 DamageEventData -> 结算伤害
//     （完全跳过射线，也不改相机/镜头）
//
// ------------------------------------------------------------------
// 设计说明一：打谁（目标选择）
// ------------------------------------------------------------------
//   1) 候选集
//      GameManager.allPlayers 数组 + playersBL/playersGR 两个 List 合并去重，
//      只保留"敌对 + 存活 + 位置有效"的 Player（人机也是 Player，用 team 区分敌我）。
//
//   2) 方向基准（准星方向）
//      读取本地玩家 Player.cameraRotation（+0x4C 的 yaw、+0x50 的 pitch），
//      这是"只读"，不会写回，也不控制镜头。
//      方向角约定与游戏一致：yaw = atan2(dx, dz)，
//      pitch = atan2(dy, sqrt(dx^2+dz^2))；夹角 = sqrt(yawDiff^2 + pitchDiff^2)。
//
//   3) 打分与排序（config.target_mode）
//      - "angle_then_distance"（默认）：
//          第一步 先卡准星锥：夹角 <= max_angle_deg 才算候选；
//          第二步 在锥内取"距离最近"的人。
//          => 完全对应"准星方向里的敌人 + 距离最近的人"。
//      - "weighted"：
//          score = 夹角(度) * angle_weight + 距离(米) * distance_weight，
//          取 score 最小。当距离权重调大时更偏"最近"，调小时更偏"最正对"。
//      - "nearest"：
//          忽略角度，直接取全场最近的敌人（只用于调试/对照）。
//
//   4) 目标命中点
//      优先胸部骨骼 spine1（character +0x60），退化到 spine（+0x5C），
//      最后退化到"玩家坐标 + 身高偏移"。命中点同时作为 DamageEventData.hitPos。
//
// ------------------------------------------------------------------
// 设计说明二：伤害怎么打进去（config.damage_entry）
// ------------------------------------------------------------------
//   DamageEventData 是 0x48 字节、按值压栈的 struct（x86 cdecl），
//   Frida 的 NativeFunction 不支持"按值结构体"参数，因此本文件用
//   "把 72 字节拆成 18 个 4 字节标量参数"的方式压栈（cdecl 下栈连续，
//   逐 4 字节完全相同），method 参数统一传 ptr(0)（与项目其它 NativeFunction 一致）。
//
//   可选入口：
//     "gamemanager"（默认）：GameManager.TakeDamage(DamageEventData)  静态统一伤害入口
//     "hurt"              ：victim.OnEntityHurt(DamageEventData)      实体受伤入口
//     "health"            ：HealthData.Hurt(int)                      只扣血的兜底入口
//     "dry_run"           ：不造成任何伤害，只选目标并记录日志（安全验证用）
//
// ------------------------------------------------------------------
// 设计说明三：三个独立开关
// ------------------------------------------------------------------
//   enable_guns              : 常规枪械直伤（主开关，替换 WPN_Gun.Damage）
//   enable_explosives        : 榴弹 / 手雷 / RPG 直伤（触发时追加直伤）
//   enable_skill_projectiles : 特殊技能弹直伤（奥术手雷 / 地狱终结者火球）
//
// ------------------------------------------------------------------
// 设计说明四：持久化日志与探针（排查"没有任何效果"用）
// ------------------------------------------------------------------
//   三路日志同时输出，任一路挂掉不影响其余：
//     1) 内存环形缓冲 Runtime.logRing  -> RPC logs() 拉取，不依赖文件权限
//     2) config.log_file 指向的文件     -> 磁盘持久化，每行 flush，崩溃也不丢
//        log_file 为空时自动写到 GameAssembly.dll 同目录（游戏目录）的
//        direct_damage_script.log，保证从整合包注入时也有持久化日志
//     3) send({type:'log'})            -> 05 调试 UI 的日志框
//
//   探针一律"只读"：不改参数、不改控制流，安装失败也只是一条 warn，
//   不会让 enable 整体失败（registerProbeAttach）。
//
//   关键探针（日志里搜这些前缀）：
//     [probe:load]        脚本是否被注入成功、模块基址、期望的 GameManager.dll md5
//     [probe:rva]         每个待 hook 地址是否落在可执行段（判断版本是否匹配）
//     [probe:enable]      enable() 的入参、钩子安装结果
//     [probe:snap:*]      世界快照：gm / staticFields / myPlayer / players / enemies
//     [probe:beat]        每 5 秒计数器快照（UI 不刷新也能看到卡在哪一步）
//     [probe:gunDamage#N] 第 N 次开火进了 WPN_Gun.Damage 替换（含射线原点/方向）
//     [probe:sel]         目标选择的候选集、准星度数、参数
//     [probe:candN]       第 N 个候选为什么被接受/拒绝
//     [probe:apply]       实际调用了哪个伤害入口
//     [probe:hp]          **最终判据**：伤害前后 HP 对照，成/败一行说清
//     [probe:gunShoot]    [probe:gmTakeDamage] [probe:entityHurt]
//     [probe:playerHurt]  [probe:healthHurt]  游戏自身伤害管线的观察点
//                                            （[ours]=我们调的，[game]=游戏自己的）
//
//   排查顺序建议：
//     先看 [probe:load]    -> 脚本没注入，后面全免谈
//     再看 [probe:rva]     -> 出现 NOT EXECUTABLE 就是版本/RVA 不匹配
//     再看 [probe:enable]  -> installHooks FAILED 则功能根本没开
//     开枪后看 [probe:beat] 的 gunCalls：
//       gunCalls=0                    -> WPN_Gun.Damage 不是这条版本的开火路径
//       gunCalls>0 但 selected=0      -> 目标选择问题（看 [probe:cand*]）
//       selected>0 但 hpDrop=0        -> 伤害入口不被接受（看 [probe:hp] / [probe:apply]）
//       hpDrop>0                      -> 功能本身是通的
// ------------------------------------------------------------------
// RVA / 字段来源：dump.cs + IDA 交叉验证 + 整合包 2.7 既有功能实测
// ------------------------------------------------------------------
//   WPN_Gun_Damage:                    0x00B613D0   (protected void Damage(Ray))
//   WPN_RPG_Fire:                      0x00B670A0
//   WPN_Throw_Throw:                   0x00B6AD80
//   WPN_GrenadeGun_GunShootFunction_lambda: 0x00B602A0  (<GunShootFunction>b__19_0)
//   WPN_Arcane_Throw:                  0x00B59640
//   WPN_EvilTerminator_ThrowFireBall:  0x00B5C600
//   GameManager_TakeDamage:            0x00AFC1C0   (static)
//   Entity_OnEntityHurt:               0x00B3F470
//   Player_OnEntityHurt:               0x00B516B0
//   HealthData_Hurt:                   0x00AE45B0
//   Weapon_get_isMyWeapon:             0x00B6E1D0
//   Entity_get_isDead:                 0x00B400E0
//   Entity_get_team:                   0x001E0070
//   Player_get_isMyPlayer:             0x00B55FD0
//   Singleton_GameManager_get_instance:0x004A8170
//   SingletonGameManager_MethodInfo:   0x00E1CE64
//   GameManager_TypeInfo:              0x00E2933C
//   Component_get_transform:           0x0032CF40
//   Transform_get_position_Injected:   0x003F4280   (this, out, method)
//
//   Il2CppClass.static_fields:         0x5C
//   GameManager.myPlayer:              0x00
//   GameManager.allPlayers:            0x1C
//   GameManager.playersBL:             0x20
//   GameManager.playersGR:             0x28
//   Entity.team:                       0x20
//   Entity.healthData:                 0x1C
//   Player.cameraRotation:             0x4C  (yaw float, pitch float)
//   Player.characterContainer:         0x58
//   Player.currentCharacter:           0x5C
//   Player.clientData:                 0x94
//   ClientData.nickname:               0x10
//   Weapon.data:                       0x68
//   WPN_Gun.realData:                  0xEC
//   WeaponData_Gun.ammoDamage:         0x14C
//   WD_RPG/WD_Missile.missileData:     0xB8  (MissileData.damage = +0x0C)
//   WD_GrenadeGun.missileData:         0x20C (MissileData.damage = +0x0C)
//   WD_EvilTerminator.missileData:     0xF8  (MissileData.damage = +0x0C)
//   DamageEventData:                   0x00 attacker / 0x04 victim / 0x08 damage
//                                      0x0C origin / 0x18 hitPos / 0x24 hitTag
//                                      0x28 hitSndName / 0x2C hitEffect / 0x30 wallThrough
//                                      0x34 type / 0x38 damageTag / 0x3C wpnIndex
//                                      0x40 wpnSprIndex / 0x44 ignoreDmgRate  (size 0x48)
//   DamageType.Gun = 1 / Knife = 2 / Grenade = 3 / Infect = 4 / Other = 5
// ============================================================

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';
    var MAX_PLAYER_SLOTS = 64;
    var POINTER_SIZE = 4;

    var TARGET_MODE = {
        ANGLE_THEN_DISTANCE: 'angle_then_distance',
        WEIGHTED: 'weighted',
        NEAREST: 'nearest'
    };

    var DAMAGE_ENTRY = {
        GAME_MANAGER: 'gamemanager',
        HURT: 'hurt',
        HEALTH: 'health',
        DRY_RUN: 'dry_run'
    };

    var RVA = {
        WPN_Gun_Damage: 0x00B613D0,
        WPN_RPG_Fire: 0x00B670A0,
        WPN_Throw_Throw: 0x00B6AD80,
        WPN_GrenadeGun_GunShootFunction_Lambda: 0x00B602A0,
        WPN_Arcane_Throw: 0x00B59640,
        WPN_EvilTerminator_ThrowFireBall: 0x00B5C600,

        GameManager_TakeDamage: 0x00AFC1C0,
        Entity_OnEntityHurt: 0x00B3F470,
        Player_OnEntityHurt: 0x00B516B0,
        HealthData_Hurt: 0x00AE45B0,

        Weapon_get_isMyWeapon: 0x00B6E1D0,
        Player_get_isMyPlayer: 0x00B55FD0,
        Entity_get_isDead: 0x00B400E0,
        Entity_get_team: 0x001E0070,

        Singleton_GameManager_get_instance: 0x004A8170,
        SingletonGameManager_MethodInfo: 0x00E1CE64,
        GameManager_TypeInfo: 0x00E2933C,

        Component_get_transform: 0x0032CF40,
        Transform_get_position_Injected: 0x003F4280,

        // ---- 诊断探针专用（只读观察，不参与功能逻辑） ----
        // 开火真正的入口：IDA 反汇编确认它内部 "call WPN_Gun$$Damage"（0x10B6214F）
        WPN_Gun_GunShootFunction: 0x00B62110,
        // HP 百分比 / 死亡判定：用来验证"伤害到底有没有落到血量上"
        HealthData_get_rate: 0x00AE4950,
        HealthData_get_isDead: 0x00AE4830
    };

    var OFF = {
        Klass_staticFields: 0x5C,

        GameManager_myPlayer: 0x00,
        GameManager_allPlayers: 0x1C,
        GameManager_playersBL: 0x20,
        GameManager_playersGR: 0x28,

        Entity_team: 0x20,
        Entity_healthData: 0x1C,

        Player_cameraRotation: 0x4C,
        Player_characterContainer: 0x58,
        Player_currentCharacter: 0x5C,
        Player_clientData: 0x94,

        ClientData_nickname: 0x10,

        Weapon_data: 0x68,
        WPN_Gun_realData: 0xEC,
        WeaponData_Gun_ammoDamage: 0x14C,

        // MissileData 是内联 struct，damage 在 missileData 起始 +0x0C
        MissileData_damage: 0x0C,
        WD_RPG_missileData: 0xB8,
        WD_Missile_missileData: 0xB8,
        WD_GrenadeGun_missileData: 0x20C,
        WD_EvilTerminator_missileData: 0xF8,

        CharacterModel_spine: 0x5C,
        CharacterModel_spine1: 0x60,

        Il2CppArray_length: 0x0C,
        Il2CppArray_items: 0x10,
        Il2CppList_items: 0x08,
        Il2CppList_size: 0x0C,

        // DamageEventData 字段
        Dmg_attacker: 0x00,
        Dmg_victim: 0x04,
        Dmg_damage: 0x08,
        Dmg_origin: 0x0C,
        Dmg_hitPos: 0x18,
        Dmg_hitTag: 0x24,
        Dmg_hitSndName: 0x28,
        Dmg_hitEffect: 0x2C,
        Dmg_wallThrough: 0x30,
        Dmg_type: 0x34,
        Dmg_damageTag: 0x38,
        Dmg_wpnIndex: 0x3C,
        Dmg_wpnSprIndex: 0x40,
        Dmg_ignoreDmgRate: 0x44,
        Dmg_size: 0x48,
        Dmg_dwordCount: 18
    };

    var DAMAGE_TYPE = {
        Gun: 1,
        Knife: 2,
        Grenade: 3,
        Infect: 4,
        Other: 5
    };

    var Runtime = {
        feature_id: 'direct_damage',
        enabled: false,
        initialized: false,
        generation: 0,
        inDirectDamage: false,

        // ---- 持久化日志状态（disable 时故意不清空，方便事后取证） ----
        logRing: [],            // 内存环形缓冲：RPC logs() 可直接拉取，不依赖文件权限
        logRingCap: 3000,
        logFilePath: '',
        logFileHandle: null,
        logFileTried: false,
        logFileFailed: '',
        heartbeat: null,
        heartbeatTicks: 0,

        module: null,
        base: ptr(0),
        attachHooks: [],
        replacedAddresses: [],
        config: {
            // 三个独立开关（默认全开，可在 UI/整合包面板里单独关闭）
            enable_guns: true,
            enable_explosives: true,
            enable_skill_projectiles: true,

            // 目标选择
            target_mode: TARGET_MODE.ANGLE_THEN_DISTANCE,
            max_angle_deg: 30.0,
            max_distance: 80.0,
            angle_weight: 1.0,
            distance_weight: 0.5,

            // 伤害注入
            // 默认走 "hurt"（Entity/Player.OnEntityHurt）：
            //   IDA 反汇编确认 Entity.OnEntityHurt 内部就是
            //     HealthData.Hurt(this.healthData, (int)eventData.damage)
            //   而且整合包 2.7 的"增加伤害倍率"功能就是挂在这个入口上工作的，
            //   是唯一被生产环境验证过的伤害入口，所以作为默认值。
            damage_entry: DAMAGE_ENTRY.HURT,
            damage_multiplier: 1.0,
            damage_override: 0.0,
            fallback_to_original: false,

            // 其它
            local_eye_height: 1.55,
            chest_fallback_height: 1.1,
            target_cache_ms: 25,

            // 调试
            diagnostic_log: true,
            log_every: 20,
            verbose_probe: true,    // 打开详细探针（目标候选、管线观察、HP 对照）
            log_to_file: true,      // 写磁盘持久化日志
            log_file: ''            // 由调用方下发；为空则只走内存缓冲 + UI
        },
        cache: {
            eventBuf: null,
            posBuf: null,
            emptyString: null,
            ownPlayer: ptr(0),
            hitTag: ptr(0),
            hitSnd: ptr(0),
            hitFx: ptr(0),
            capturedTag: false,
            selectedTarget: null,
            selectedAtMs: 0
        },
        stats: {
            gunDamageCalls: 0,
            localGunFires: 0,
            explosiveTriggers: 0,
            skillTriggers: 0,
            targetsSelected: 0,
            damageApplied: 0,
            noTarget: 0,
            skippedRemote: 0,
            fallbackOriginal: 0,
            stringCaptured: 0,

            // ---- 探针计数：用于定位"卡在哪一步" ----
            gunHookDisabled: 0,     // 进钩子但功能/枪械开关关闭
            gunHookReentry: 0,      // 进钩子但重入保护命中
            pipelineGunShoot: 0,    // 游戏开火入口命中次数
            pipelineTakeDamage: 0,  // GameManager.TakeDamage 被调用次数
            pipelineEntityHurt: 0,  // Entity.OnEntityHurt 被调用次数
            pipelinePlayerHurt: 0,  // Player.OnEntityHurt 被调用次数
            pipelineHealthHurt: 0,  // HealthData.Hurt 被调用次数（最底层扣血）
            hpChecks: 0,            // 伤害前后 HP 对照次数
            hpDropped: 0,           // 对照中确认 HP 真的下降的次数
            lastHpBefore: -1,
            lastHpAfter: -1,
            lastHpRawBefore: '',
            lastHpRawAfter: '',
            ownPlayerSource: '',    // 本地玩家是从哪条路径取到的

            errorCount: 0,
            cleanupCount: 0,
            lastDamage: 0,
            lastTargetAngle: -1,
            lastTargetDistance: -1,
            lastError: '',
            lastResult: ''
        }
    };

    var native = {
        ready: false,
        isMyWeapon: null,
        isMyPlayer: null,
        isDead: null,
        getTeam: null,
        getTransform: null,
        getPosition: null,
        getGameManager: null,
        healthRate: null,
        healthIsDead: null,
        gunDamageOriginal: null,
        gmTakeDamage: null,
        entityHurt: null,
        playerHurt: null,
        healthHurt: null
    };

    // ------------------------------------------------------------------
    // 日志与探针（持久化）
    // ------------------------------------------------------------------
    //   三路同时输出，任何一路挂掉都不影响另外两路：
    //     1) Runtime.logRing           内存环形缓冲，RPC logs() 拉取（不依赖文件权限）
    //     2) config.log_file 指向的文件  磁盘持久化，每行 flush（游戏崩了也不丢）
    //     3) send({type:'log'})        05 调试 UI 的日志框
    //
    //   探针（probe）是"带标签 + 带预算"的日志：
    //     每个标签前 PROBE_BUDGET 条全记，之后按 1/PROBE_TAIL 抽样，
    //     避免全自动武器每次开火刷爆日志，同时保证异常点一定被记下。
    // ------------------------------------------------------------------
    var LogLimiter = {};
    var ProbeCount = {};
    var PROBE_BUDGET = 40;
    var PROBE_TAIL = 200;

    function pad2(n) { return (n < 10 ? '0' : '') + n; }
    function pad3(n) { return (n < 10 ? '00' : (n < 100 ? '0' : '')) + n; }

    function stamp() {
        var d = new Date();
        return pad2(d.getHours()) + ':' + pad2(d.getMinutes()) + ':' + pad2(d.getSeconds()) +
            '.' + pad3(d.getMilliseconds());
    }

    function fmtPtr(p) {
        try {
            if (p === null || p === undefined) return 'null';
            if (typeof p === 'number') return '0x' + (p >>> 0).toString(16);
            return p.toString();
        } catch (_) { return '?'; }
    }

    function fmtVec(v) {
        if (!v) return 'null';
        try {
            return '(' + v.x.toFixed(2) + ',' + v.y.toFixed(2) + ',' + v.z.toFixed(2) + ')';
        } catch (_) { return '?'; }
    }

    function hex32(v) {
        try { return '0x' + (v >>> 0).toString(16); } catch (_) { return '?'; }
    }

    // ------------------------------------------------------------------
    // 关键坑：Frida 的 NativeFunction 对 'bool' 返回值给的是 **JS number(0/1)**，
    // 不是 JS boolean。实测 frida 17.9.1（ia32 与 x64 一致）：
    //     new NativeFunction(IsProcessorFeaturePresent, 'bool', ['int'])(10)
    //       -> 1, typeof "number", (v === true) === false
    // 所以「fn(...) === true」恒为 false，会让「是不是我的武器 / 是不是我」
    // 全部判定失败 —— 表现就是"功能开着但任何武器都没效果"。
    // 必须按真值判定。整合包里 26_grenade_mode 用的就是真值判定，
    // 29_bullet_wall_penetration 的钩子里也是直接 if (!native.isMyWeapon(...))。
    // ------------------------------------------------------------------
    function toFlag(value) {
        if (value === true) return true;
        if (value === false) return false;
        var n = Number(value);
        if (isFinite(n)) return n !== 0;
        return Boolean(value);
    }

    // 探针用：把原始返回值也打出来，避免再被类型问题骗到
    function safeBool(fn, arg) {
        if (!fn) return 'n/a';
        try {
            var raw = fn(arg, ptr(0));
            return String(toFlag(raw)) + '(raw=' + String(raw) + ')';
        } catch (_) { return 'err'; }
    }

    // 没有显式下发 log_file 时的兜底路径：
    // 写到 GameAssembly.dll 所在目录（也就是游戏目录），那里基本一定可写，
    // 这样即使从整合包/手工注入（不传 log_file）也能拿到持久化日志。
    function defaultLogPath() {
        try {
            var mod = Runtime.module || Process.findModuleByName(MODULE_NAME);
            if (mod && mod.path) {
                var full = String(mod.path).replace(/\\/g, '/');
                var slash = full.lastIndexOf('/');
                if (slash > 0) return full.substring(0, slash) + '/direct_damage_script.log';
            }
        } catch (_) {}
        return 'direct_damage_script.log';
    }

    // 打开持久化日志文件；写文件之前的缓冲内容会一次性补写进去，保证不丢启动日志。
    function openLogFile() {
        if (Runtime.logFileHandle) return true;
        if (Runtime.logFileTried) return false;
        Runtime.logFileTried = true;
        if (!Runtime.config.log_to_file) return false;
        if (typeof File === 'undefined') {
            Runtime.logFileFailed = 'Frida File API unavailable';
            return false;
        }
        try {
            var path = String(Runtime.config.log_file || defaultLogPath()).replace(/\\/g, '/');
            var handle = new File(path, 'a');
            Runtime.logFileHandle = handle;
            Runtime.logFilePath = path;
            handle.write('==== ' + new Date().toString() + ' | direct_damage script log opened' +
                ' | arch=' + Process.arch + ' ptrSize=' + Process.pointerSize +
                ' | moduleBase=' + fmtPtr(Runtime.base) +
                ' | modulePath=' + (Runtime.module ? Runtime.module.path : '?') + ' ====\n');
            for (var i = 0; i < Runtime.logRing.length; i += 1) {
                handle.write(Runtime.logRing[i] + '\n');
            }
            handle.flush();
            return true;
        } catch (error) {
            Runtime.logFileHandle = null;
            Runtime.logFilePath = '';
            Runtime.logFileFailed = (error && error.message) ? error.message : String(error);
            return false;
        }
    }

    function writeLogFile(text) {
        if (!Runtime.logFileHandle && !openLogFile()) return;
        try {
            Runtime.logFileHandle.write(text + '\n');
            Runtime.logFileHandle.flush();
        } catch (_) {
            Runtime.logFileHandle = null;
        }
    }

    function rememberLog(text) {
        try {
            Runtime.logRing.push(text);
            if (Runtime.logRing.length > Runtime.logRingCap) {
                Runtime.logRing.splice(0, Runtime.logRing.length - Runtime.logRingCap);
            }
        } catch (_) {}
    }

    // 唯一底层出口
    function logRaw(level, message) {
        var text = '[' + Runtime.feature_id + '] [' + stamp() + '] ' + message;
        rememberLog(text);
        writeLogFile(text);
        try {
            if (level === 'error') console.error(text);
            else if (level === 'warn') console.warn(text);
            else console.log(text);
        } catch (_) {}
        try { send({ type: 'log', level: level, module: Runtime.feature_id, message: message }); } catch (_) {}
    }

    function log(level, message) { logRaw(level, message); }

    function logLimited(key, level, message, intervalMs) {
        var now = Date.now();
        var wait = intervalMs || 1500;
        if (!LogLimiter[key] || now - LogLimiter[key] >= wait) {
            LogLimiter[key] = now;
            logRaw(level, message);
        }
    }

    // 标签额度：前 limit 次返回 true
    function probeBudget(tag, limit) {
        var cap = limit || PROBE_BUDGET;
        var n = (ProbeCount[tag] || 0) + 1;
        ProbeCount[tag] = n;
        return n <= cap;
    }

    // 带预算的探针
    function probe(tag, message) {
        if (!Runtime.config.verbose_probe) return;
        var n = ProbeCount[tag] || 0;
        ProbeCount[tag] = n + 1;
        if (n >= PROBE_BUDGET && ProbeCount[tag] % PROBE_TAIL !== 0) return;
        logRaw('info', '[probe:' + tag + '] ' + message);
    }

    function resetProbes() { ProbeCount = {}; LogLimiter = {}; }

    // 错误：前 30 条完整记录（不受限流影响），之后每 100 条记 1 条
    function fail(where, error) {
        Runtime.stats.errorCount += 1;
        Runtime.stats.lastError = where + ': ' + (error && error.message ? error.message : String(error));
        Runtime.stats.lastResult = 'error';
        var key = 'fail:' + where;
        var n = (ProbeCount[key] || 0) + 1;
        ProbeCount[key] = n;
        if (n <= 30 || n % 100 === 0) {
            logRaw('error', '[fail:' + where + '] ' + Runtime.stats.lastError + ' (x' + n + ')');
        }
    }

    function dumpLogs(count) {
        var n = (count && count > 0) ? Math.min(count, 1500) : 1500;
        return Runtime.logRing.slice(-n);
    }

    function sendStatus(featureId, enabled) {
        try { send({ type: 'status', feature: featureId, enabled: enabled }); } catch (_) {}
    }

    // ------------------------------------------------------------------
    // 指针工具
    // ------------------------------------------------------------------
    function isNull(p) {
        if (p === null || p === undefined) return true;
        try { return p.isNull(); } catch (_) { return true; }
    }

    function readable(p) {
        try {
            if (isNull(p)) return false;
            p.readPointer();
            return true;
        } catch (_) {
            return false;
        }
    }

    function isExecutable(p) {
        try {
            var range = Process.findRangeByAddress(p);
            return range !== null && range.protection.indexOf('x') !== -1;
        } catch (_) {
            return false;
        }
    }

    function samePointer(a, b) {
        try { return a.equals(b); } catch (_) { return false; }
    }

    function toNumber(value, fallback) {
        var n = Number(value);
        return isFinite(n) ? n : fallback;
    }

    function clampFloat(value, min, max) {
        if (!isFinite(value)) return min;
        if (value < min) return min;
        if (value > max) return max;
        return value;
    }

    // ------------------------------------------------------------------
    // NativeFunction 初始化
    // ------------------------------------------------------------------
    function ensureNative() {
        if (native.ready) return true;
        var mod = Runtime.module || Process.findModuleByName(MODULE_NAME);
        if (!mod) {
            Runtime.stats.lastError = MODULE_NAME + ' not found';
            return false;
        }
        Runtime.module = mod;
        Runtime.base = mod.base;

        if (Process.arch !== 'ia32' || Process.pointerSize !== POINTER_SIZE) {
            Runtime.stats.lastError = 'unsupported process: arch=' + Process.arch + ', pointerSize=' + Process.pointerSize;
            log('error', Runtime.stats.lastError);
            return false;
        }

        try {
            var base = Runtime.base;
            native.isMyWeapon = new NativeFunction(base.add(RVA.Weapon_get_isMyWeapon), 'bool', ['pointer', 'pointer'], CALL_CONV);
            native.isMyPlayer = new NativeFunction(base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer'], CALL_CONV);
            native.isDead = new NativeFunction(base.add(RVA.Entity_get_isDead), 'bool', ['pointer', 'pointer'], CALL_CONV);
            native.getTeam = new NativeFunction(base.add(RVA.Entity_get_team), 'int32', ['pointer', 'pointer'], CALL_CONV);
            native.getTransform = new NativeFunction(base.add(RVA.Component_get_transform), 'pointer', ['pointer', 'pointer'], CALL_CONV);
            native.getPosition = new NativeFunction(base.add(RVA.Transform_get_position_Injected), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
            native.getGameManager = new NativeFunction(base.add(RVA.Singleton_GameManager_get_instance), 'pointer', ['pointer'], CALL_CONV);

            // 诊断用：只读 HP 百分比 / 死亡标记，用来验证伤害是否真的落到血量上
            native.healthRate = new NativeFunction(base.add(RVA.HealthData_get_rate), 'float', ['pointer', 'pointer'], CALL_CONV);
            native.healthIsDead = new NativeFunction(base.add(RVA.HealthData_get_isDead), 'bool', ['pointer', 'pointer'], CALL_CONV);

            // DamageEventData 按值压栈：18 个 4 字节 + method
            native.gmTakeDamage = new NativeFunction(
                base.add(RVA.GameManager_TakeDamage), 'void',
                ['uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint',
                 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'pointer'],
                CALL_CONV
            );
            native.playerHurt = new NativeFunction(
                base.add(RVA.Player_OnEntityHurt), 'void',
                ['pointer', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint',
                 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'pointer'],
                CALL_CONV
            );
            native.entityHurt = new NativeFunction(
                base.add(RVA.Entity_OnEntityHurt), 'void',
                ['pointer', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint',
                 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'pointer'],
                CALL_CONV
            );
            native.healthHurt = new NativeFunction(base.add(RVA.HealthData_Hurt), 'void', ['pointer', 'int32', 'pointer'], CALL_CONV);

            native.ready = true;
            logHookAudit();
            return true;
        } catch (error) {
            fail('ensureNative', error);
            native.ready = false;
            return false;
        }
    }

    function clearNative() {
        Object.keys(native).forEach(function (key) {
            native[key] = key === 'ready' ? false : null;
        });
    }

    function ensureBuffers() {
        try {
            if (!Runtime.cache.eventBuf) Runtime.cache.eventBuf = Memory.alloc(OFF.Dmg_size + 16);
            if (!Runtime.cache.posBuf) Runtime.cache.posBuf = Memory.alloc(16);
            return true;
        } catch (error) {
            fail('ensureBuffers', error);
            return false;
        }
    }

    // ------------------------------------------------------------------
    // 游戏对象访问
    // ------------------------------------------------------------------
    function getGameManagerStaticFields() {
        try {
            var typeInfo = Runtime.base.add(RVA.GameManager_TypeInfo).readPointer();
            if (!readable(typeInfo)) return ptr(0);
            var staticFields = typeInfo.add(OFF.Klass_staticFields).readPointer();
            if (!readable(staticFields)) return ptr(0);
            return staticFields;
        } catch (error) {
            fail('GameManager static_fields', error);
            return ptr(0);
        }
    }

    function getGameManager() {
        try {
            var methodInfo = Runtime.base.add(RVA.SingletonGameManager_MethodInfo).readPointer();
            if (!readable(methodInfo)) return ptr(0);
            return native.getGameManager(methodInfo);
        } catch (error) {
            fail('Singleton<GameManager>.get_instance', error);
            return ptr(0);
        }
    }

    function getMyPlayer() {
        var cached = Runtime.cache.ownPlayer;
        try {
            if (!isNull(cached) && isLocalPlayer(cached) && !isDeadEntity(cached)) return cached;
        } catch (_) {}

        // 主路径：遍历玩家列表 + Player.get_isMyPlayer()
        // 这条取法与整合包 2.7 的自瞄功能完全一致，是目前唯一被实测验证过的路径。
        var gm = getGameManager();
        if (!isNull(gm)) {
            var all = getAllPlayers(gm);
            for (var i = 0; i < all.length; i++) {
                if (isLocalPlayer(all[i])) {
                    Runtime.cache.ownPlayer = all[i];
                    Runtime.stats.ownPlayerSource = 'list(' + all.length + ')';
                    return all[i];
                }
            }
            Runtime.stats.ownPlayerSource = 'list-miss(' + all.length + ')';
        } else {
            Runtime.stats.ownPlayerSource = 'gm-null';
        }

        // 退化路径：直接读 GameManager.myPlayer 静态字段。
        // 注意：这条路径没有被其它功能验证过，未初始化时读到的是 metadata usage
        // 编码值（形如 0x2000xxxx）而不是真的 Il2CppClass*，所以必须用
        // isMyPlayer 复核一次才敢返回，否则后面全链路都会拿着垃圾指针跑。
        try {
            var fields = getGameManagerStaticFields();
            if (!isNull(fields)) {
                var player = fields.add(OFF.GameManager_myPlayer).readPointer();
                if (readable(player) && isLocalPlayer(player)) {
                    Runtime.cache.ownPlayer = player;
                    Runtime.stats.ownPlayerSource = 'static-field';
                    return player;
                }
            }
        } catch (error) {
            fail('GameManager.myPlayer', error);
        }
        return ptr(0);
    }

    function readArray(arrayPtr) {
        var result = [];
        if (!readable(arrayPtr)) return result;
        try {
            var length = arrayPtr.add(OFF.Il2CppArray_length).readU32();
            if (length > 256) return result;
            for (var i = 0; i < length; i++) {
                var element = arrayPtr.add(OFF.Il2CppArray_items + i * POINTER_SIZE).readPointer();
                if (!isNull(element)) result.push(element);
            }
        } catch (_) {}
        return result;
    }

    function readList(listPtr) {
        var result = [];
        if (!readable(listPtr)) return result;
        try {
            var items = listPtr.add(OFF.Il2CppList_items).readPointer();
            if (!readable(items)) return result;
            var size = listPtr.add(OFF.Il2CppList_size).readS32();
            if (size < 0 || size > MAX_PLAYER_SLOTS) return result;
            for (var i = 0; i < size; i++) {
                var element = items.add(OFF.Il2CppArray_items + i * POINTER_SIZE).readPointer();
                if (!isNull(element)) result.push(element);
            }
        } catch (_) {}
        return result;
    }

    function isValidPlayer(player) {
        if (!readable(player)) return false;
        try {
            var team = player.add(OFF.Entity_team).readS32();
            return team === 0 || team === 1 || team === 2;
        } catch (_) {
            return false;
        }
    }

    function getAllPlayers(gm) {
        var map = {};
        if (isNull(gm)) return [];
        try {
            var array = readArray(gm.add(OFF.GameManager_allPlayers).readPointer());
            for (var i = 0; i < array.length; i++) {
                if (isValidPlayer(array[i])) map[array[i].toString()] = array[i];
            }
            var bl = readList(gm.add(OFF.GameManager_playersBL).readPointer());
            for (var j = 0; j < bl.length; j++) {
                if (isValidPlayer(bl[j])) map[bl[j].toString()] = bl[j];
            }
            var gr = readList(gm.add(OFF.GameManager_playersGR).readPointer());
            for (var k = 0; k < gr.length; k++) {
                if (isValidPlayer(gr[k])) map[gr[k].toString()] = gr[k];
            }
        } catch (error) {
            fail('getAllPlayers', error);
        }
        return Object.keys(map).map(function (key) { return map[key]; });
    }

    function isLocalPlayer(player) {
        if (!readable(player) || !native.isMyPlayer) return false;
        try { return toFlag(native.isMyPlayer(player, ptr(0))); } catch (_) { return false; }
    }

    function isLocalWeapon(weapon) {
        if (!readable(weapon) || !native.isMyWeapon) return false;
        try { return toFlag(native.isMyWeapon(weapon, ptr(0))); } catch (_) { return false; }
    }

    function isDeadEntity(entity) {
        if (readable(entity) && native.isDead) {
            try { return toFlag(native.isDead(entity, ptr(0))); } catch (_) {}
        }
        // 退化：拿不到原生 get_isDead 时，用 healthData 指针是否存在做粗略判断
        try {
            var health = entity.add(OFF.Entity_healthData).readPointer();
            return !readable(health);
        } catch (_) {
            return true;
        }
    }

    function readTeam(entity) {
        if (!readable(entity)) return -1;
        if (native.getTeam) {
            try { return native.getTeam(entity, ptr(0)); } catch (_) {}
        }
        try { return entity.add(OFF.Entity_team).readS32(); } catch (_) { return -1; }
    }

    // 阵营判定：2 = 自由混战（无阵营/生化），此时所有人都算敌人。
    function isEnemyTeam(myTeam, otherTeam) {
        if (myTeam < 0 || otherTeam < 0) return true;
        return (myTeam === 2) || (otherTeam === 2) || (myTeam !== otherTeam);
    }

    function isValidPos(pos) {
        return pos &&
            isFinite(pos.x) && isFinite(pos.y) && isFinite(pos.z) &&
            Math.abs(pos.x) < 5000 && Math.abs(pos.y) < 5000 && Math.abs(pos.z) < 5000;
    }

    function readTransformPosition(transformPtr) {
        if (!readable(transformPtr) || !native.getPosition || !Runtime.cache.posBuf) return null;
        try {
            var buffer = Runtime.cache.posBuf;
            native.getPosition(transformPtr, buffer, ptr(0));
            var pos = {
                x: buffer.readFloat(),
                y: buffer.add(4).readFloat(),
                z: buffer.add(8).readFloat()
            };
            return isValidPos(pos) ? pos : null;
        } catch (_) {
            return null;
        }
    }

    function getPlayerPos(player) {
        if (!readable(player)) return null;
        try {
            var transform = native.getTransform(player, ptr(0));
            var pos = readTransformPosition(transform);
            if (pos) return pos;

            var container = player.add(OFF.Player_characterContainer).readPointer();
            pos = readTransformPosition(container);
            if (pos) return pos;

            if (readable(container)) {
                var raw = {
                    x: container.add(0x38).readFloat(),
                    y: container.add(0x3C).readFloat(),
                    z: container.add(0x40).readFloat()
                };
                if (isValidPos(raw)) return raw;
            }
        } catch (_) {}
        return null;
    }

    // 目标命中点：优先胸部骨骼，退化到玩家坐标 + 高度偏移。
    function getAimPoint(player, playerPos) {
        var root = playerPos || getPlayerPos(player);
        if (!root) return null;
        try {
            var character = player.add(OFF.Player_currentCharacter).readPointer();
            if (readable(character)) {
                var spine1 = character.add(OFF.CharacterModel_spine1).readPointer();
                var pos = readTransformPosition(spine1);
                if (pos) return pos;
                var spine = character.add(OFF.CharacterModel_spine).readPointer();
                pos = readTransformPosition(spine);
                if (pos) return pos;
            }
        } catch (_) {}
        return {
            x: root.x,
            y: root.y + Runtime.config.chest_fallback_height,
            z: root.z
        };
    }

    function readCameraRotation(player) {
        try {
            var yaw = player.add(OFF.Player_cameraRotation).readFloat();
            var pitch = player.add(OFF.Player_cameraRotation + 4).readFloat();
            if (!isFinite(yaw) || !isFinite(pitch)) return null;
            return { yawDeg: yaw, pitchDeg: pitch };
        } catch (_) {
            return null;
        }
    }

    function getLocalEyePos(player) {
        var pos = getPlayerPos(player);
        if (!pos) return null;
        return { x: pos.x, y: pos.y + Runtime.config.local_eye_height, z: pos.z };
    }

    // ------------------------------------------------------------------
    // 角度计算（与游戏/自瞄一致的约定）
    // ------------------------------------------------------------------
    function normalizeAngleDeg(value) {
        while (value > 180) value -= 360;
        while (value < -180) value += 360;
        return value;
    }

    function calculateTargetAngles(from, to) {
        var dx = to.x - from.x;
        var dy = to.y - from.y;
        var dz = to.z - from.z;
        var hDist = Math.sqrt(dx * dx + dz * dz);
        if (hDist < 0.01) hDist = 0.01;
        return {
            targetYawDeg: Math.atan2(dx, dz) * 180.0 / Math.PI,
            targetPitchDeg: Math.atan2(dy, hDist) * 180.0 / Math.PI,
            dist: Math.sqrt(dx * dx + dy * dy + dz * dz)
        };
    }

    function angleDistanceDeg(targetYawDeg, targetPitchDeg, currentYawDeg, currentPitchDeg) {
        var yawDiff = normalizeAngleDeg(targetYawDeg - currentYawDeg);
        var pitchDiff = normalizeAngleDeg(targetPitchDeg - currentPitchDeg);
        return Math.sqrt(yawDiff * yawDiff + pitchDiff * pitchDiff);
    }

    // ------------------------------------------------------------------
    // 目标选择：准星方向 + 距离
    // ------------------------------------------------------------------
    function selectTarget(myPlayer, eyePos, rotation) {
        var gm = getGameManager();
        if (isNull(gm)) {
            Runtime.stats.lastResult = 'game manager unavailable';
            probe('sel', 'ABORT: GameManager singleton is null');
            return null;
        }

        var players = getAllPlayers(gm);
        var myTeam = readTeam(myPlayer);
        var best = null;
        var candidateCount = 0;
        var nearestDistance = -1;

        // 世界级探针：候选集多大、准星朝哪、用什么条件筛
        if (probeBudget('sel', 30)) {
            probe('sel', 'players=' + players.length + ' myPlayer=' + fmtPtr(myPlayer) +
                ' myTeam=' + myTeam + ' eye=' + fmtVec(eyePos) +
                ' rot=' + rotation.yawDeg.toFixed(1) + '/' + rotation.pitchDeg.toFixed(1) +
                ' mode=' + Runtime.config.target_mode +
                ' cone=' + Runtime.config.max_angle_deg + 'deg maxDist=' + Runtime.config.max_distance +
                ' enemies=' + countEnemies(myPlayer, players));
        }

        // 前 6 个候选逐条记录判定结果 —— 用来直接回答"为什么没选中"
        var detailLimit = 6;
        var note = function (index, text) {
            if (index < detailLimit) probe('cand' + index, text);
            else if (probeBudget('candMore', 6)) probe('candMore', '#' + index + ' ' + text);
        };

        for (var i = 0; i < players.length; i++) {
            var candidate = players[i];
            try {
                if (samePointer(candidate, myPlayer)) { note(i, 'self -> skip'); continue; }
                var otherTeam = readTeam(candidate);
                if (!isEnemyTeam(myTeam, otherTeam)) {
                    note(i, fmtPtr(candidate) + ' team=' + otherTeam + ' -> same team, skip');
                    continue;
                }
                if (isDeadEntity(candidate)) {
                    note(i, fmtPtr(candidate) + ' -> dead, skip');
                    continue;
                }

                var targetRoot = getPlayerPos(candidate);
                if (!targetRoot) {
                    note(i, fmtPtr(candidate) + ' -> position unreadable, skip');
                    continue;
                }
                var aimPoint = getAimPoint(candidate, targetRoot);
                if (!aimPoint) {
                    note(i, fmtPtr(candidate) + ' -> aim point unreadable, skip');
                    continue;
                }

                var angles = calculateTargetAngles(eyePos, aimPoint);
                if (!angles) { note(i, 'angle calc failed'); continue; }
                if (Runtime.config.max_distance > 0 && angles.dist > Runtime.config.max_distance) {
                    note(i, fmtPtr(candidate) + ' dist=' + angles.dist.toFixed(1) +
                        ' > maxDist=' + Runtime.config.max_distance + ' -> out of range, skip');
                    continue;
                }

                var angleDeg = angleDistanceDeg(
                    angles.targetYawDeg, angles.targetPitchDeg,
                    rotation.yawDeg, rotation.pitchDeg
                );
                if (!isFinite(angleDeg)) { note(i, 'angle not finite'); continue; }

                // angle_then_distance / nearest 都要先过准星锥，
                // 只有 nearest 模式才允许完全忽略角度。
                if (Runtime.config.target_mode !== TARGET_MODE.NEAREST &&
                    angleDeg > Runtime.config.max_angle_deg) {
                    note(i, fmtPtr(candidate) + ' angle=' + angleDeg.toFixed(1) +
                        ' > cone=' + Runtime.config.max_angle_deg + ' -> outside crosshair cone, skip');
                    continue;
                }
                note(i, fmtPtr(candidate) + ' ACCEPT angle=' + angleDeg.toFixed(1) +
                    ' dist=' + angles.dist.toFixed(1));

                candidateCount += 1;
                if (nearestDistance < 0 || angles.dist < nearestDistance) nearestDistance = angles.dist;

                var score;
                if (Runtime.config.target_mode === TARGET_MODE.WEIGHTED) {
                    score = angleDeg * Runtime.config.angle_weight +
                        angles.dist * Runtime.config.distance_weight;
                } else {
                    // angle_then_distance：角度已过筛，直接比距离
                    score = angles.dist;
                }

                if (best === null || score < best.score) {
                    best = {
                        player: candidate,
                        pos: aimPoint,
                        rootPos: targetRoot,
                        dist: angles.dist,
                        angleDeg: angleDeg,
                        score: score
                    };
                }
            } catch (_) {}
        }

        if (best) {
            Runtime.stats.targetsSelected += 1;
            Runtime.stats.lastTargetAngle = best.angleDeg;
            Runtime.stats.lastTargetDistance = best.dist;
        } else {
            Runtime.stats.noTarget += 1;
            probe('sel', 'NO TARGET: players=' + players.length +
                ' acceptedInCone=' + candidateCount +
                ' nearestAccepted=' + (nearestDistance < 0 ? '-' : nearestDistance.toFixed(1)) +
                ' cone=' + Runtime.config.max_angle_deg + 'deg maxDist=' + Runtime.config.max_distance +
                ' (把"打谁策略"切到"仅取最近(调试)"可确认是不是准星锥卡太死)');
        }
        Runtime.stats.lastResult = best
            ? ('target ok, angle=' + best.angleDeg.toFixed(1) + 'deg, dist=' + best.dist.toFixed(1) + 'm, candidates=' + candidateCount)
            : ('no target, candidatesWithinCone=' + candidateCount + ', nearest=' + (nearestDistance < 0 ? '-' : nearestDistance.toFixed(1)));
        return best;
    }

    function getSelectedTarget(myPlayer, eyePos, rotation) {
        var now = Date.now();
        var cached = Runtime.cache.selectedTarget;
        var ttl = Runtime.config.target_cache_ms;
        if (cached && ttl > 0 && (now - Runtime.cache.selectedAtMs) <= ttl) return cached;
        var target = selectTarget(myPlayer, eyePos, rotation);
        Runtime.cache.selectedTarget = target;
        Runtime.cache.selectedAtMs = now;
        return target;
    }

    // ------------------------------------------------------------------
    // DamageEventData 构造与伤害注入
    // ------------------------------------------------------------------
    // 制造一个合法的空 IL2CPP String，避免把 null 字符串交给游戏内部使用。
    function makeEmptyIl2CppString() {
        if (!isNull(Runtime.cache.emptyString)) return Runtime.cache.emptyString;
        try {
            var myPlayer = Runtime.cache.ownPlayer;
            if (isNull(myPlayer)) return ptr(0);
            var clientData = myPlayer.add(OFF.Player_clientData).readPointer();
            if (!readable(clientData)) return ptr(0);
            var nickname = clientData.add(OFF.ClientData_nickname).readPointer();
            if (!readable(nickname)) return ptr(0);
            var klass = nickname.readPointer();
            if (!readable(klass)) return ptr(0);

            var memory = Memory.alloc(0x10);
            memory.writePointer(klass);              // +0x00 klass
            memory.add(4).writePointer(ptr(0));      // +0x04 monitor
            memory.add(8).writeS32(0);               // +0x08 长度 0
            memory.add(0x0C).writeU16(0);            // +0x0C UTF-16 终止符
            Runtime.cache.emptyString = memory;
            return memory;
        } catch (error) {
            fail('makeEmptyIl2CppString', error);
            return ptr(0);
        }
    }

    function resolveStringPointers() {
        var empty = makeEmptyIl2CppString();
        return {
            tag: isNull(Runtime.cache.hitTag) ? empty : Runtime.cache.hitTag,
            snd: isNull(Runtime.cache.hitSnd) ? empty : Runtime.cache.hitSnd,
            fx: isNull(Runtime.cache.hitFx) ? empty : Runtime.cache.hitFx
        };
    }

    // 把 DamageEventData 写进缓冲区，再拆成 18 个 4 字节标量（cdecl 压栈布局）。
    function buildEventDwords(attacker, victim, damage, dmgType, origin, hitPos) {
        var buf = Runtime.cache.eventBuf;
        var strings = resolveStringPointers();

        buf.add(OFF.Dmg_attacker).writePointer(attacker);
        buf.add(OFF.Dmg_victim).writePointer(victim);
        buf.add(OFF.Dmg_damage).writeFloat(damage);

        buf.add(OFF.Dmg_origin).writeFloat(origin.x);
        buf.add(OFF.Dmg_origin + 4).writeFloat(origin.y);
        buf.add(OFF.Dmg_origin + 8).writeFloat(origin.z);

        buf.add(OFF.Dmg_hitPos).writeFloat(hitPos.x);
        buf.add(OFF.Dmg_hitPos + 4).writeFloat(hitPos.y);
        buf.add(OFF.Dmg_hitPos + 8).writeFloat(hitPos.z);

        buf.add(OFF.Dmg_hitTag).writePointer(strings.tag);
        buf.add(OFF.Dmg_hitSndName).writePointer(strings.snd);
        buf.add(OFF.Dmg_hitEffect).writePointer(strings.fx);

        buf.add(OFF.Dmg_wallThrough).writeU8(0);
        buf.add(OFF.Dmg_type).writeS32(dmgType);
        buf.add(OFF.Dmg_damageTag).writeS32(0);
        buf.add(OFF.Dmg_wpnIndex).writeS32(0);
        buf.add(OFF.Dmg_wpnSprIndex).writeS32(0);
        buf.add(OFF.Dmg_ignoreDmgRate).writeU8(0);

        var dwords = new Array(OFF.Dmg_dwordCount);
        for (var i = 0; i < OFF.Dmg_dwordCount; i += 1) {
            dwords[i] = buf.add(i * 4).readU32();
        }
        return dwords;
    }

    // 18 个 dword 按顺序展开成调用参数（cdecl 下即 struct 的 72 字节）
    function callGameManagerTakeDamage(d) {
        native.gmTakeDamage(
            d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8],
            d[9], d[10], d[11], d[12], d[13], d[14], d[15], d[16], d[17],
            ptr(0)
        );
    }

    function callPlayerHurt(victim, d) {
        native.playerHurt(
            victim,
            d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8],
            d[9], d[10], d[11], d[12], d[13], d[14], d[15], d[16], d[17],
            ptr(0)
        );
    }

    function callEntityHurt(victim, d) {
        native.entityHurt(
            victim,
            d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8],
            d[9], d[10], d[11], d[12], d[13], d[14], d[15], d[16], d[17],
            ptr(0)
        );
    }

    // HP 对照快照：直接回答"伤害到底有没有落到血量上"。
    //   rate = HealthData.get_rate()  HP 百分比（0~1），最直观
    //   raw  = currentHealth(ObscuredInt) 的原始字段 key/hidden/fake/inited
    //          即使 rate 取不到，raw 发生变化也足以证明血量被改写
    function readHealthSnapshot(victim) {
        var snap = { ptr: null, rate: -1, dead: null, raw: '-', err: '' };
        try {
            var health = victim.add(OFF.Entity_healthData).readPointer();
            snap.ptr = health;
            if (!readable(health)) { snap.err = 'healthData unreadable'; return snap; }
            if (native.healthRate) snap.rate = native.healthRate(health, ptr(0));
            if (native.healthIsDead) snap.dead = toFlag(native.healthIsDead(health, ptr(0)));
            snap.raw = hex32(health.add(0x08).readU32()) + '/' +
                hex32(health.add(0x0C).readU32()) + '/' +
                hex32(health.add(0x10).readU32()) + '/' +
                health.add(0x14).readU8();
        } catch (error) {
            snap.err = (error && error.message) ? error.message : String(error);
        }
        return snap;
    }

    function applyDamage(target, damage, dmgType, sourceLabel) {
        if (!target || damage <= 0) return false;
        var entry = Runtime.config.damage_entry;

        if (entry === DAMAGE_ENTRY.DRY_RUN) {
            Runtime.stats.lastResult = 'dry_run: would deal ' + damage.toFixed(1) +
                ' to ' + target.player + ' (' + sourceLabel + ')';
            probe('dryRun', 'WOULD DEAL ' + damage.toFixed(1) + ' -> ' + fmtPtr(target.player) +
                ' angle=' + target.angleDeg.toFixed(1) + ' dist=' + target.dist.toFixed(1) +
                ' (' + sourceLabel + ')');
            return false;
        }

        var myPlayer = getMyPlayer();
        if (isNull(myPlayer)) {
            probe('apply', 'ABORT: local player unavailable');
            return false;
        }

        var eyePos = getLocalEyePos(myPlayer) || target.rootPos || target.pos;
        var before = readHealthSnapshot(target.player);

        try {
            if (entry === DAMAGE_ENTRY.HEALTH) {
                var health = target.player.add(OFF.Entity_healthData).readPointer();
                if (!readable(health)) {
                    probe('apply', 'ABORT: healthData unreadable for ' + fmtPtr(target.player));
                    return false;
                }
                probe('apply', 'call HealthData.Hurt(hp=' + fmtPtr(health) + ', value=' + (damage | 0) + ')');
                native.healthHurt(health, damage | 0, ptr(0));
            } else {
                var dwords = buildEventDwords(
                    myPlayer, target.player, damage, dmgType, eyePos, target.pos
                );
                if (entry === DAMAGE_ENTRY.HURT) {
                    probe('apply', 'call Player.OnEntityHurt(victim=' + fmtPtr(target.player) +
                        ', damage=' + damage.toFixed(2) + ', type=' + dmgType + ')');
                    callPlayerHurt(target.player, dwords);
                } else {
                    probe('apply', 'call GameManager.TakeDamage(damage=' + damage.toFixed(2) +
                        ', type=' + dmgType + ')');
                    callGameManagerTakeDamage(dwords);
                }
            }

            var after = readHealthSnapshot(target.player);
            Runtime.stats.hpChecks += 1;
            Runtime.stats.lastHpBefore = before.rate;
            Runtime.stats.lastHpAfter = after.rate;
            Runtime.stats.lastHpRawBefore = before.raw;
            Runtime.stats.lastHpRawAfter = after.raw;

            var dropped;
            if (before.rate >= 0 && after.rate >= 0) {
                dropped = (after.rate < before.rate) || toFlag(after.dead);
            } else {
                dropped = before.raw !== after.raw;
            }
            if (dropped) Runtime.stats.hpDropped += 1;

            // 最终判据：这一行直接告诉我们是"成了"还是"没效果"
            if (Runtime.stats.hpChecks <= 25 || Runtime.stats.hpChecks % 25 === 0) {
                log(dropped ? 'info' : 'warn', '[probe:hp] entry=' + entry +
                    ' victim=' + fmtPtr(target.player) + ' hpPtr=' + fmtPtr(before.ptr) +
                    ' rate=' + before.rate.toFixed(3) + '->' + after.rate.toFixed(3) +
                    ' raw=' + before.raw + '->' + after.raw +
                    ' dead=' + String(before.dead) + '->' + String(after.dead) +
                    ' => ' + (dropped ? 'HP DROPPED **WORKS**' : 'HP UNCHANGED **NO EFFECT**') +
                    ' [dmg=' + damage.toFixed(2) + ' type=' + dmgType + ' ' + sourceLabel + ']' +
                    ((before.err || after.err) ? ' err=' + (before.err || after.err) : ''));
            }

            Runtime.stats.damageApplied += 1;
            Runtime.stats.lastDamage = damage;
            Runtime.stats.lastResult = 'damage ' + damage.toFixed(1) +
                ' -> ' + target.player + ' via ' + entry + ' (' + sourceLabel + ')' +
                (dropped ? ' [HP OK]' : ' [HP unchanged]');
            if (Runtime.config.diagnostic_log &&
                (Runtime.stats.damageApplied === 1 ||
                 Runtime.stats.damageApplied % Math.max(1, Runtime.config.log_every) === 0)) {
                log('info', Runtime.stats.lastResult);
            }
            return true;
        } catch (error) {
            fail('applyDamage:' + sourceLabel, error);
            probe('apply', 'EXCEPTION entry=' + entry + ': ' +
                (error && error.message ? error.message : String(error)));
            return false;
        }
    }

    // ------------------------------------------------------------------
    // 伤害数值读取
    // ------------------------------------------------------------------
    function readFloatSafe(pointer) {
        try {
            var value = pointer.readFloat();
            return isFinite(value) ? value : 0;
        } catch (_) {
            return 0;
        }
    }

    function readGunDamage(weapon) {
        try {
            var data = weapon.add(OFF.WPN_Gun_realData).readPointer();
            if (!readable(data)) data = weapon.add(OFF.Weapon_data).readPointer();
            if (!readable(data)) return 0;
            return readFloatSafe(data.add(OFF.WeaponData_Gun_ammoDamage));
        } catch (_) {
            return 0;
        }
    }

    function readMissileDamage(weapon, missileDataOffset) {
        try {
            var data = weapon.add(OFF.Weapon_data).readPointer();
            if (!readable(data)) return 0;
            return readFloatSafe(data.add(missileDataOffset + OFF.MissileData_damage));
        } catch (_) {
            return 0;
        }
    }

    function resolveDamage(baseDamage) {
        var damage = baseDamage;
        if (Runtime.config.damage_override > 0) damage = Runtime.config.damage_override;
        damage = damage * Runtime.config.damage_multiplier;
        if (!isFinite(damage) || damage <= 0) damage = 0;
        if (damage > 999999) damage = 999999;
        return damage;
    }

    // ------------------------------------------------------------------
    // 直伤主流程
    // ------------------------------------------------------------------
    // 返回 true 表示"已接管这次开火"，false 表示"没有可用目标"。
    function directDamage(weapon, dmgType, sourceLabel, baseDamage) {
        var myPlayer = getMyPlayer();
        if (isNull(myPlayer)) {
            Runtime.stats.lastResult = 'local player unavailable';
            probe('direct', 'ABORT: local player unavailable (' + sourceLabel + ')');
            return false;
        }
        var eyePos = getLocalEyePos(myPlayer);
        if (!eyePos) {
            Runtime.stats.lastResult = 'local eye position unavailable';
            probe('direct', 'ABORT: local eye position unavailable, myPlayer=' + fmtPtr(myPlayer) +
                ' healthData=' + fmtPtr(myPlayer.add(OFF.Entity_healthData).readPointer()));
            return false;
        }
        var rotation = readCameraRotation(myPlayer);
        if (!rotation) {
            Runtime.stats.lastResult = 'camera rotation unavailable';
            probe('direct', 'ABORT: camera rotation at myPlayer+0x4C unreadable');
            return false;
        }

        var target = getSelectedTarget(myPlayer, eyePos, rotation);
        if (!target) return false;

        var damage = resolveDamage(baseDamage);
        if (damage <= 0) {
            probe('direct', 'baseDamage=' + baseDamage + ' -> 0, fallback to 10');
            damage = resolveDamage(0) || 10; // 兜底：至少造成一点伤害，避免"打了没反应"
        }
        probe('direct', 'target=' + fmtPtr(target.player) + ' angle=' + target.angleDeg.toFixed(1) +
            ' dist=' + target.dist.toFixed(1) + ' damage=' + damage.toFixed(2) +
            ' entry=' + Runtime.config.damage_entry + ' (' + sourceLabel + ')');
        return applyDamage(target, damage, dmgType, sourceLabel);
    }

    // ------------------------------------------------------------------
    // Hook 安装
    // ------------------------------------------------------------------
    function registerAttach(name, rva, callbacks) {
        var address = Runtime.base.add(rva);
        if (!isExecutable(address)) throw new Error(name + ' address not executable: ' + address);
        var handle = Interceptor.attach(address, callbacks);
        Runtime.attachHooks.push({ name: name, handle: handle });
        log('info', 'hook installed: ' + name + ' @ 0x' + rva.toString(16));
        return handle;
    }

    function installGunHook() {
        var address = Runtime.base.add(RVA.WPN_Gun_Damage);
        if (!isExecutable(address)) throw new Error('WPN_Gun.Damage address not executable: ' + address);

        // 必须在 replace 之前创建，之后才能调用原函数。
        native.gunDamageOriginal = new NativeFunction(
            address, 'void',
            ['pointer', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'pointer'],
            CALL_CONV
        );

        var replacement = new NativeCallback(function (weapon, r0, r1, r2, r3, r4, r5, method) {
            try {
                Runtime.stats.gunDamageCalls += 1;

                // 第一次命中必须留下铁证：证明"钩子确实装上了、确实被开火走到了"
                if (Runtime.stats.gunDamageCalls <= 3) {
                    log('info', '[probe:gunDamage#' + Runtime.stats.gunDamageCalls + '] FIRED weapon=' +
                        fmtPtr(weapon) +
                        ' isMyWeapon=' + safeBool(native.isMyWeapon, weapon) +
                        ' rayOrigin=' + fmtVec({ x: u32ToFloat(r0), y: u32ToFloat(r1), z: u32ToFloat(r2) }) +
                        ' rayDir=' + fmtVec({ x: u32ToFloat(r3), y: u32ToFloat(r4), z: u32ToFloat(r5) }) +
                        ' enabled=' + Runtime.enabled +
                        ' guns=' + Runtime.config.enable_guns +
                        ' entry=' + Runtime.config.damage_entry);
                }

                // 重入保护：结算伤害过程中若又回到 Damage（例如死亡/掉落链），一律走原版，避免无限递归。
                if (Runtime.inDirectDamage) {
                    Runtime.stats.gunHookReentry += 1;
                    native.gunDamageOriginal(weapon, r0, r1, r2, r3, r4, r5, method);
                    return;
                }
                if (!Runtime.enabled || !Runtime.config.enable_guns) {
                    Runtime.stats.gunHookDisabled += 1;
                    if (probeBudget('gunDisabled', 3)) {
                        probe('gunDisabled', 'passthrough: enabled=' + Runtime.enabled +
                            ' guns=' + Runtime.config.enable_guns);
                    }
                    native.gunDamageOriginal(weapon, r0, r1, r2, r3, r4, r5, method);
                    return;
                }
                if (!isLocalWeapon(weapon)) {
                    Runtime.stats.skippedRemote += 1;
                    if (probeBudget('gunRemote', 5)) {
                        probe('gunRemote', 'passthrough: not my weapon ' + fmtPtr(weapon) +
                            ' isMyWeapon=' + safeBool(native.isMyWeapon, weapon));
                    }
                    native.gunDamageOriginal(weapon, r0, r1, r2, r3, r4, r5, method);
                    return;
                }

                Runtime.stats.localGunFires += 1;
                if (probeBudget('gunLocal', 5)) {
                    probe('gunLocal', 'taking over fire #' + Runtime.stats.localGunFires +
                        ' weapon=' + fmtPtr(weapon) + ' ammoDamage=' + readGunDamage(weapon).toFixed(2));
                }
                Runtime.inDirectDamage = true;
                var handled;
                try {
                    handled = directDamage(weapon, DAMAGE_TYPE.Gun, 'gun', readGunDamage(weapon));
                } finally {
                    Runtime.inDirectDamage = false;
                }
                if (!handled) {
                    probe('gunNoTarget', 'no direct-damage target; original ray ' +
                        (Runtime.config.fallback_to_original ? 'RESTORED' : 'SUPPRESSED (fallback off)'));
                    if (Runtime.config.fallback_to_original) {
                        Runtime.stats.fallbackOriginal += 1;
                        native.gunDamageOriginal(weapon, r0, r1, r2, r3, r4, r5, method);
                    }
                }
            } catch (error) {
                fail('WPN_Gun.Damage replacement', error);
                try { native.gunDamageOriginal(weapon, r0, r1, r2, r3, r4, r5, method); } catch (_) {}
            }
        }, 'void', ['pointer', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'pointer']);

        Interceptor.replace(address, replacement);
        Runtime.replacedAddresses.push({ name: 'WPN_Gun.Damage', address: address });
        log('info', 'WPN_Gun.Damage replaced @ 0x' + RVA.WPN_Gun_Damage.toString(16));
    }

    // 爆炸物：RPG / 手雷投掷 / 榴弹枪（榴弹模式）
    function installExplosiveHooks() {
        registerAttach('WPN_RPG.Fire', RVA.WPN_RPG_Fire, {
            onEnter: function (args) {
                handleTrigger(args[0], DAMAGE_TYPE.Grenade, 'rpg', OFF.WD_RPG_missileData);
            }
        });
        registerAttach('WPN_Throw.Throw', RVA.WPN_Throw_Throw, {
            onEnter: function (args) {
                handleTrigger(args[0], DAMAGE_TYPE.Grenade, 'throw', OFF.WD_Missile_missileData);
            }
        });
        registerAttach('WPN_GrenadeGun.b__19_0', RVA.WPN_GrenadeGun_GunShootFunction_Lambda, {
            onEnter: function (args) {
                handleTrigger(args[0], DAMAGE_TYPE.Grenade, 'grenade_gun', OFF.WD_GrenadeGun_missileData);
            }
        });
    }

    // 特殊技能弹：奥术手雷 / 地狱终结者火球
    function installSkillHooks() {
        registerAttach('WPN_Arcane.Throw', RVA.WPN_Arcane_Throw, {
            onEnter: function (args) {
                handleTrigger(args[0], DAMAGE_TYPE.Other, 'arcane', OFF.WD_Missile_missileData);
            }
        });
        registerAttach('WPN_EvilTerminator.ThrowFireBall', RVA.WPN_EvilTerminator_ThrowFireBall, {
            onEnter: function (args) {
                handleTrigger(args[0], DAMAGE_TYPE.Other, 'evil_terminator', OFF.WD_EvilTerminator_missileData);
            }
        });
    }

    function handleTrigger(weapon, dmgType, sourceLabel, missileDataOffset) {
        if (!Runtime.enabled) return;
        if (sourceLabel === 'arcane' || sourceLabel === 'evil_terminator') {
            if (!Runtime.config.enable_skill_projectiles) return;
        } else if (!Runtime.config.enable_explosives) {
            return;
        }
        try {
            if (!isLocalWeapon(weapon)) {
                if (probeBudget('trigRemote', 3)) {
                    probe('trigRemote', sourceLabel + ': not my weapon ' + fmtPtr(weapon));
                }
                return;
            }
            if (sourceLabel === 'arcane' || sourceLabel === 'evil_terminator') {
                Runtime.stats.skillTriggers += 1;
            } else {
                Runtime.stats.explosiveTriggers += 1;
            }
            if (Runtime.inDirectDamage) {
                probe('trigReentry', sourceLabel + ': re-entry, skipped');
                return;
            }
            var damage = readMissileDamage(weapon, missileDataOffset);
            probe('trig', sourceLabel + ' weapon=' + fmtPtr(weapon) +
                ' missileDamage=' + damage.toFixed(2) + ' offset=0x' + missileDataOffset.toString(16));
            // 直伤是"追加"结算：原版投射物仍会正常发射并爆炸。
            Runtime.inDirectDamage = true;
            try {
                directDamage(weapon, dmgType, sourceLabel, damage);
            } finally {
                Runtime.inDirectDamage = false;
            }
        } catch (error) {
            fail('handleTrigger:' + sourceLabel, error);
        }
    }

    // 只读观察钩子：从真实伤害事件里抓取合法的 hitTag/hitSndName/hitEffect 字符串指针，
    // 让本功能合成的事件带上原版字符串，避免传 null。
    function installStringCaptureHooks() {
        var capture = function () {
            try {
                if (Runtime.cache.capturedTag) return;
                var eventPtr = this.context.esp.add(8);
                var tag = eventPtr.add(OFF.Dmg_hitTag).readPointer();
                var snd = eventPtr.add(OFF.Dmg_hitSndName).readPointer();
                var fx = eventPtr.add(OFF.Dmg_hitEffect).readPointer();
                if (readable(snd) || readable(fx) || readable(tag)) {
                    Runtime.cache.hitTag = tag;
                    Runtime.cache.hitSnd = snd;
                    Runtime.cache.hitFx = fx;
                    Runtime.cache.capturedTag = true;
                    Runtime.stats.stringCaptured += 1;
                    log('info', 'captured real DamageEventData strings');
                }
            } catch (_) {}
        };
        registerAttach('Entity.OnEntityHurt(capture)', RVA.Entity_OnEntityHurt, { onEnter: capture });
        registerAttach('Player.OnEntityHurt(capture)', RVA.Player_OnEntityHurt, { onEnter: capture });
    }

    // ------------------------------------------------------------------
    // 诊断探针
    // ------------------------------------------------------------------
    //   设计原则：
    //     1) 探针只读，不修改任何参数、不改变控制流；
    //     2) 探针安装失败只记一条 warn，绝不会让 enable 整体失败；
    //     3) 所有探针写入同一个持久化日志文件，事后可离线分析。
    // ------------------------------------------------------------------

    // RVA 审计：确认每个将被 hook 的地址都落在可执行段。
    // 如果某个 RVA 与当前游戏版本对不上，这里会打出 *** NOT EXECUTABLE ***，
    // 一眼就能区分"代码写错"和"版本不匹配"。
    function logHookAudit() {
        try {
            var list = [
                ['WPN_Gun.Damage', RVA.WPN_Gun_Damage],
                ['WPN_Gun.GunShootFunction', RVA.WPN_Gun_GunShootFunction],
                ['WPN_RPG.Fire', RVA.WPN_RPG_Fire],
                ['WPN_Throw.Throw', RVA.WPN_Throw_Throw],
                ['WPN_GrenadeGun.lambda', RVA.WPN_GrenadeGun_GunShootFunction_Lambda],
                ['WPN_Arcane.Throw', RVA.WPN_Arcane_Throw],
                ['WPN_EvilTerminator.ThrowFireBall', RVA.WPN_EvilTerminator_ThrowFireBall],
                ['GameManager.TakeDamage', RVA.GameManager_TakeDamage],
                ['Entity.OnEntityHurt', RVA.Entity_OnEntityHurt],
                ['Player.OnEntityHurt', RVA.Player_OnEntityHurt],
                ['HealthData.Hurt', RVA.HealthData_Hurt],
                ['HealthData.get_rate', RVA.HealthData_get_rate]
            ];
            for (var i = 0; i < list.length; i += 1) {
                var address = Runtime.base.add(list[i][1]);
                log('info', '[probe:rva] ' + list[i][0] + ' @+0x' + list[i][1].toString(16) +
                    ' -> ' + fmtPtr(address) + (isExecutable(address) ? ' OK' : ' *** NOT EXECUTABLE ***'));
            }
            log('info', '[probe:module] base=' + fmtPtr(Runtime.base) +
                ' size=0x' + (Runtime.module ? Runtime.module.size.toString(16) : '?') +
                ' name=' + (Runtime.module ? Runtime.module.name : '?'));
        } catch (error) {
            fail('logHookAudit', error);
        }
    }

    // 探针专用 attach：失败不抛，避免一个坏 RVA 把整个功能带崩
    function registerProbeAttach(name, rva, callbacks) {
        try {
            return registerAttach(name, rva, callbacks);
        } catch (error) {
            log('warn', '[probe] attach failed (non-fatal): ' + name + ' @+0x' + rva.toString(16) +
                ' : ' + (error && error.message ? error.message : String(error)));
            return null;
        }
    }

    function u32ToFloat(v) {
        try {
            if (!Runtime.cache.floatBuf) Runtime.cache.floatBuf = Memory.alloc(4);
            Runtime.cache.floatBuf.writeU32(v >>> 0);
            return Runtime.cache.floatBuf.readFloat();
        } catch (_) { return 0; }
    }

    function countEnemies(myPlayer, players) {
        var n = 0;
        var myTeam = isNull(myPlayer) ? -1 : readTeam(myPlayer);
        for (var i = 0; i < players.length; i += 1) {
            try {
                if (samePointer(players[i], myPlayer)) continue;
                if (!isEnemyTeam(myTeam, readTeam(players[i]))) continue;
                if (isDeadEntity(players[i])) continue;
                n += 1;
            } catch (_) {}
        }
        return n;
    }

    // 世界快照：一次性回答"当前能不能看到世界数据"
    //   gm / staticFields / myPlayer 全为 0        -> 取对象这一步就失败了
    //   players=0                                  -> 玩家列表取不到
    //   players>0 但 enemies=0                     -> 阵营判定有问题
    function diagnosticSnapshot(tag) {
        try {
            var gm = getGameManager();
            var fields = getGameManagerStaticFields();
            var me = getMyPlayer();
            var players = isNull(gm) ? [] : getAllPlayers(gm);
            var rot = isNull(me) ? null : readCameraRotation(me);
            log('info', '[probe:snap:' + tag + '] base=' + fmtPtr(Runtime.base) +
                ' gm=' + fmtPtr(gm) + ' staticFields=' + fmtPtr(fields) +
                ' myPlayer=' + fmtPtr(me) + ' via=' + (Runtime.stats.ownPlayerSource || '-') +
                ' players=' + players.length + ' enemies=' + countEnemies(me, players) +
                ' enabled=' + Runtime.enabled + ' init=' + Runtime.initialized +
                ' attaches=' + Runtime.attachHooks.length + ' replaced=' + Runtime.replacedAddresses.length);
            if (!isNull(fields)) {
                log('info', '[probe:snap:' + tag + '] static GameManager.myPlayer raw=' +
                    fmtPtr(fields.add(OFF.GameManager_myPlayer).readPointer()));
            }
            if (!isNull(me)) {
                log('info', '[probe:snap:' + tag + '] me.pos=' + fmtVec(getPlayerPos(me)) +
                    ' me.rot=' + (rot ? (rot.yawDeg.toFixed(1) + '/' + rot.pitchDeg.toFixed(1)) : 'null') +
                    ' me.team=' + readTeam(me) +
                    ' me.isMy=' + safeBool(native.isMyPlayer, me) +
                    ' me.isDead=' + safeBool(native.isDead, me));
            }
            log('info', '[probe:snap:' + tag + '] logFile=' + (Runtime.logFilePath || '(none)') +
                ' logFileFailed=' + (Runtime.logFileFailed || '-') + ' ring=' + Runtime.logRing.length);
        } catch (error) {
            fail('diagnosticSnapshot', error);
        }
    }

    // 心跳：每 5 秒把计数器写进日志。
    // 这样即使 UI 不刷新，日志文件里也能看到"到底哪一步是 0"。
    function startHeartbeat() {
        stopHeartbeat();
        Runtime.heartbeat = setInterval(function () {
            try {
                if (!Runtime.enabled) return;
                var s = Runtime.stats;
                Runtime.heartbeatTicks += 1;
                log('info', '[probe:beat] gunCalls=' + s.gunDamageCalls +
                    ' hookFired=' + (s.gunDamageCalls > 0 ? 'YES' : 'NO') +
                    ' localFires=' + s.localGunFires +
                    ' selected=' + s.targetsSelected + ' noTarget=' + s.noTarget +
                    ' damage=' + s.damageApplied + ' hpDrop=' + s.hpDropped + '/' + s.hpChecks +
                    ' pipeShoot=' + s.pipelineGunShoot + ' pipeTake=' + s.pipelineTakeDamage +
                    ' pipeEntity=' + s.pipelineEntityHurt + ' pipePlayer=' + s.pipelinePlayerHurt +
                    ' pipeHP=' + s.pipelineHealthHurt +
                    ' errors=' + s.errorCount + ' lastError=' + (s.lastError || '-'));
                if (Runtime.heartbeatTicks % 3 === 1) diagnosticSnapshot('beat');
            } catch (_) {}
        }, 5000);
    }

    function stopHeartbeat() {
        if (Runtime.heartbeat) {
            try { clearInterval(Runtime.heartbeat); } catch (_) {}
            Runtime.heartbeat = null;
        }
    }

    // 游戏自身伤害管线的只读观察钩子。用来区分四类失败：
    //   A. 只有 pipeShoot 增长      -> 开火进了游戏，但 WPN_Gun.Damage 的替换没生效
    //   B. 只看到 [game]            -> 游戏自己在结算伤害，我们合成的没进去
    //   C. 看到 [ours] 但 HP 不变   -> 调用被接受了但没有实际扣血（入口选错）
    //   D. 什么都没有                -> 钩子没装上（对照 rva / attach 日志）
    function installPipelineProbes() {
        if (!Runtime.config.verbose_probe) return;

        // 开火真正入口：GunShootFunction -> GetShootRay -> WPN_Gun.Damage
        registerProbeAttach('WPN_Gun.GunShootFunction(probe)', RVA.WPN_Gun_GunShootFunction, {
            onEnter: function (args) {
                Runtime.stats.pipelineGunShoot += 1;
                if (probeBudget('gunShoot', 10)) {
                    probe('gunShoot', 'enter weapon=' + fmtPtr(args[0]) +
                        ' isMyWeapon=' + safeBool(native.isMyWeapon, args[0]) +
                        ' enabled=' + Runtime.enabled +
                        ' gunSwitch=' + Runtime.config.enable_guns);
                }
            }
        });

        // GameManager.TakeDamage(DamageEventData) 静态 + 按值结构体：
        // x86 cdecl 进入时 [esp]=返回地址，[esp+4] 起就是结构体本体。
        registerProbeAttach('GameManager.TakeDamage(probe)', RVA.GameManager_TakeDamage, {
            onEnter: function () {
                Runtime.stats.pipelineTakeDamage += 1;
                if (probeBudget('gmTakeDamage', 20)) {
                    try {
                        var b = this.context.esp.add(4);
                        probe('gmTakeDamage', 'victim=' + fmtPtr(b.add(OFF.Dmg_victim).readPointer()) +
                            ' attacker=' + fmtPtr(b.add(OFF.Dmg_attacker).readPointer()) +
                            ' damage=' + b.add(OFF.Dmg_damage).readFloat().toFixed(2) +
                            ' type=' + b.add(OFF.Dmg_type).readS32() +
                            (Runtime.inDirectDamage ? ' [ours]' : ' [game]'));
                    } catch (error) { probe('gmTakeDamage', 'read failed: ' + error.message); }
                }
            }
        });

        // 实例方法：this=[esp+4]，按值结构体=[esp+8]
        // （与整合包 2.7 的伤害倍率功能取同一个地址约定，那条路是已验证可用的）
        var hurtProbe = function (tag, isPlayer) {
            return function () {
                if (isPlayer) Runtime.stats.pipelinePlayerHurt += 1;
                else Runtime.stats.pipelineEntityHurt += 1;
                if (probeBudget(tag, 20)) {
                    try {
                        var sp = this.context.esp;
                        var b = sp.add(8);
                        probe(tag, 'self=' + fmtPtr(sp.add(4).readPointer()) +
                            ' victim=' + fmtPtr(b.add(OFF.Dmg_victim).readPointer()) +
                            ' damage=' + b.add(OFF.Dmg_damage).readFloat().toFixed(2) +
                            ' type=' + b.add(OFF.Dmg_type).readS32() +
                            (Runtime.inDirectDamage ? ' [ours]' : ' [game]'));
                    } catch (error) { probe(tag, 'read failed: ' + error.message); }
                }
            };
        };
        registerProbeAttach('Entity.OnEntityHurt(probe)', RVA.Entity_OnEntityHurt, { onEnter: hurtProbe('entityHurt', false) });
        registerProbeAttach('Player.OnEntityHurt(probe)', RVA.Player_OnEntityHurt, { onEnter: hurtProbe('playerHurt', true) });

        // 最底层扣血：Entity.OnEntityHurt 内部就是 "HealthData.Hurt(healthData, (int)damage)"
        registerProbeAttach('HealthData.Hurt(probe)', RVA.HealthData_Hurt, {
            onEnter: function (args) {
                Runtime.stats.pipelineHealthHurt += 1;
                if (probeBudget('healthHurt', 20)) {
                    try {
                        probe('healthHurt', 'hp=' + fmtPtr(args[0]) +
                            ' value=' + args[1].toInt32() +
                            (Runtime.inDirectDamage ? ' [ours]' : ' [game]'));
                    } catch (error) { probe('healthHurt', 'read failed: ' + error.message); }
                }
            }
        });
    }

    function installHooks() {
        if (Runtime.initialized) return true;
        if (!ensureNative()) return false;
        if (!ensureBuffers()) return false;
        try {
            installPipelineProbes();
            installGunHook();
            installExplosiveHooks();
            installSkillHooks();
            installStringCaptureHooks();
            Runtime.initialized = true;
            log('info', 'all hooks installed');
            return true;
        } catch (error) {
            fail('installHooks', error);
            cleanupHooks();
            return false;
        }
    }

    function cleanupHooks() {
        for (var i = 0; i < Runtime.attachHooks.length; i += 1) {
            try {
                if (Runtime.attachHooks[i].handle && Runtime.attachHooks[i].handle.detach) {
                    Runtime.attachHooks[i].handle.detach();
                }
            } catch (_) {}
        }
        Runtime.attachHooks = [];

        for (var j = 0; j < Runtime.replacedAddresses.length; j += 1) {
            try { Interceptor.revert(Runtime.replacedAddresses[j].address); } catch (_) {}
        }
        Runtime.replacedAddresses = [];
        Runtime.initialized = false;
    }

    function resetRuntime(reason) {
        stopHeartbeat();
        cleanupHooks();
        Runtime.inDirectDamage = false;
        Runtime.cache.ownPlayer = ptr(0);
        Runtime.cache.selectedTarget = null;
        Runtime.cache.selectedAtMs = 0;
        Runtime.cache.emptyString = null;
        Runtime.cache.hitTag = ptr(0);
        Runtime.cache.hitSnd = ptr(0);
        Runtime.cache.hitFx = ptr(0);
        Runtime.cache.capturedTag = false;
        Runtime.cache.eventBuf = null;
        Runtime.cache.posBuf = null;
        Runtime.generation += 1;
        Runtime.enabled = false;
        Runtime.module = null;
        Runtime.base = ptr(0);
        clearNative();
        log('info', 'resetRuntime: ' + reason);
    }

    // ------------------------------------------------------------------
    // 配置
    // ------------------------------------------------------------------
    function updateConfig(input) {
        input = input || {};
        var c = Runtime.config;

        if (input.enable_guns !== undefined) c.enable_guns = input.enable_guns !== false;
        if (input.enable_explosives !== undefined) c.enable_explosives = input.enable_explosives !== false;
        if (input.enable_skill_projectiles !== undefined) {
            c.enable_skill_projectiles = input.enable_skill_projectiles !== false;
        }

        if (input.target_mode !== undefined) {
            var mode = String(input.target_mode);
            if (mode === TARGET_MODE.ANGLE_THEN_DISTANCE ||
                mode === TARGET_MODE.WEIGHTED ||
                mode === TARGET_MODE.NEAREST) {
                c.target_mode = mode;
            }
        }
        if (input.max_angle_deg !== undefined) c.max_angle_deg = clampFloat(toNumber(input.max_angle_deg, c.max_angle_deg), 0, 180);
        if (input.max_distance !== undefined) c.max_distance = clampFloat(toNumber(input.max_distance, c.max_distance), 0, 1000);
        if (input.angle_weight !== undefined) c.angle_weight = clampFloat(toNumber(input.angle_weight, c.angle_weight), 0, 100);
        if (input.distance_weight !== undefined) c.distance_weight = clampFloat(toNumber(input.distance_weight, c.distance_weight), 0, 100);

        if (input.damage_entry !== undefined) {
            var entry = String(input.damage_entry);
            if (entry === DAMAGE_ENTRY.GAME_MANAGER || entry === DAMAGE_ENTRY.HURT ||
                entry === DAMAGE_ENTRY.HEALTH || entry === DAMAGE_ENTRY.DRY_RUN) {
                c.damage_entry = entry;
            }
        }
        if (input.damage_multiplier !== undefined) c.damage_multiplier = clampFloat(toNumber(input.damage_multiplier, c.damage_multiplier), 0, 100);
        if (input.damage_override !== undefined) c.damage_override = clampFloat(toNumber(input.damage_override, c.damage_override), 0, 999999);
        if (input.fallback_to_original !== undefined) c.fallback_to_original = input.fallback_to_original === true;
        if (input.local_eye_height !== undefined) c.local_eye_height = clampFloat(toNumber(input.local_eye_height, c.local_eye_height), 0, 5);
        if (input.target_cache_ms !== undefined) c.target_cache_ms = clampFloat(toNumber(input.target_cache_ms, c.target_cache_ms), 0, 1000);

        if (input.diagnostic_log !== undefined) c.diagnostic_log = input.diagnostic_log !== false;
        if (input.log_every !== undefined) c.log_every = Math.max(1, Math.floor(toNumber(input.log_every, c.log_every)));
        if (input.verbose_probe !== undefined) c.verbose_probe = input.verbose_probe !== false;
        if (input.log_to_file !== undefined) c.log_to_file = input.log_to_file !== false;
        if (input.log_file !== undefined && String(input.log_file) !== c.log_file) {
            // 换日志文件：关掉旧句柄，下次写日志时按新路径重新打开（并把内存缓冲补写进去）
            c.log_file = String(input.log_file);
            try { if (Runtime.logFileHandle) Runtime.logFileHandle.close(); } catch (_) {}
            Runtime.logFileHandle = null;
            Runtime.logFilePath = '';
            Runtime.logFileTried = false;
        }

        // 目标缓存与选择参数变了就失效，避免用到旧目标。
        Runtime.cache.selectedTarget = null;
        Runtime.cache.selectedAtMs = 0;

        log('info', '[probe:config] guns=' + c.enable_guns +
            ' explosives=' + c.enable_explosives +
            ' skills=' + c.enable_skill_projectiles +
            ' mode=' + c.target_mode +
            ' cone=' + c.max_angle_deg + ' maxDist=' + c.max_distance +
            ' entry=' + c.damage_entry +
            ' mult=' + c.damage_multiplier +
            ' fallbackToOriginal=' + c.fallback_to_original +
            ' verboseProbe=' + c.verbose_probe +
            ' logFile=' + (c.log_file || '(none)'));
        return getStatus();
    }

    // ------------------------------------------------------------------
    // RPC
    // ------------------------------------------------------------------
    function enableFeature(config) {
        if (config) updateConfig(config);

        // 首次 enable 时 config 里才带上 log_file，所以这里允许再尝试打开一次
        if (!Runtime.logFileHandle) {
            Runtime.logFileTried = false;
            openLogFile();
        }
        Runtime.stats.ownPlayerSource = '';

        log('info', '[probe:enable] enable() called | entry=' + Runtime.config.damage_entry +
            ' guns=' + Runtime.config.enable_guns +
            ' explosives=' + Runtime.config.enable_explosives +
            ' skills=' + Runtime.config.enable_skill_projectiles +
            ' cone=' + Runtime.config.max_angle_deg + ' maxDist=' + Runtime.config.max_distance +
            ' | logFile=' + (Runtime.logFilePath || '(none: ' + (Runtime.logFileFailed || 'not set') + ')'));

        if (!installHooks()) {
            log('error', '[probe:enable] installHooks FAILED -> 功能保持关闭. lastError=' +
                (Runtime.stats.lastError || '(none)') +
                ' | 若上面有 *** NOT EXECUTABLE *** 说明 RVA 与当前游戏版本不匹配');
            diagnosticSnapshot('enable-failed');
            return getStatus();
        }

        Runtime.enabled = true;
        Runtime.stats.lastError = '';
        sendStatus(Runtime.feature_id, true);
        log('info', '[probe:enable] hooks OK: attaches=' + Runtime.attachHooks.length +
            ' replaced=' + Runtime.replacedAddresses.length);
        diagnosticSnapshot('enabled');
        startHeartbeat();
        return getStatus();
    }

    function disableFeature() {
        resetRuntime('disabled');
        sendStatus(Runtime.feature_id, false);
        log('info', 'disabled');
        return getStatus();
    }

    function cleanupFeature() {
        Runtime.stats.cleanupCount += 1;
        resetRuntime('cleanup');
        return getStatus();
    }

    function getStatus() {
        return {
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            generation: Runtime.generation,
            config: Runtime.config,
            gun_damage_calls: Runtime.stats.gunDamageCalls,
            local_gun_fires: Runtime.stats.localGunFires,
            explosive_triggers: Runtime.stats.explosiveTriggers,
            skill_triggers: Runtime.stats.skillTriggers,
            targets_selected: Runtime.stats.targetsSelected,
            damage_applied: Runtime.stats.damageApplied,
            no_target: Runtime.stats.noTarget,
            skipped_remote_weapon: Runtime.stats.skippedRemote,
            fallback_original: Runtime.stats.fallbackOriginal,
            string_captured: Runtime.stats.stringCaptured,
            last_damage: Runtime.stats.lastDamage,
            last_target_angle: Runtime.stats.lastTargetAngle,
            last_target_distance: Runtime.stats.lastTargetDistance,
            error_count: Runtime.stats.errorCount,
            last_error: Runtime.stats.lastError,
            // ---- 探针字段 ----
            own_player_source: Runtime.stats.ownPlayerSource,
            gun_hook_disabled: Runtime.stats.gunHookDisabled,
            gun_hook_reentry: Runtime.stats.gunHookReentry,
            pipeline_gun_shoot: Runtime.stats.pipelineGunShoot,
            pipeline_take_damage: Runtime.stats.pipelineTakeDamage,
            pipeline_entity_hurt: Runtime.stats.pipelineEntityHurt,
            pipeline_player_hurt: Runtime.stats.pipelinePlayerHurt,
            pipeline_health_hurt: Runtime.stats.pipelineHealthHurt,
            hp_checks: Runtime.stats.hpChecks,
            hp_dropped: Runtime.stats.hpDropped,
            last_hp_before: Runtime.stats.lastHpBefore,
            last_hp_after: Runtime.stats.lastHpAfter,
            attach_hooks: Runtime.attachHooks.length,
            verbose_probe: Runtime.config.verbose_probe,
            log_file: Runtime.logFilePath,
            log_file_failed: Runtime.logFileFailed,
            log_lines: Runtime.logRing.length,
            last_result: Runtime.stats.lastResult
        };
    }

    rpc.exports = {
        enable: function (config) { return enableFeature(config); },
        disable: function () { return disableFeature(); },
        status: function () { return getStatus(); },
        cleanup: function () { return cleanupFeature(); },
        setConfig: function (config) { return updateConfig(config || {}); },
        set_config: function (config) { return updateConfig(config || {}); },
        setconfig: function (config) { return updateConfig(config || {}); },

        // ---- 诊断用 RPC ----
        // logs(count)    拉取内存环形缓冲（不依赖文件权限，UI 关闭前也能取到）
        // clearLogs()    清空缓冲 + 重置探针预算
        // setLogFile(p)  指定持久化日志文件
        // dump()         返回全量缓冲（并把文件打开，触发补写）
        // snapshot(tag)  强制打一份世界快照
        logs: function (count) { return dumpLogs(count); },
        get_logs: function (count) { return dumpLogs(count); },
        clearLogs: function () { Runtime.logRing = []; resetProbes(); return true; },
        clear_logs: function () { Runtime.logRing = []; resetProbes(); return true; },
        setLogFile: function (path) { return updateConfig({ log_file: path }); },
        set_log_file: function (path) { return updateConfig({ log_file: path }); },
        dump: function () { openLogFile(); return dumpLogs(0); },
        snapshot: function (tag) { diagnosticSnapshot(tag || 'rpc'); return getStatus(); }
    };

    // 脚本加载即写一条：这是"脚本到底有没有被注入"的第一证据
    try {
        var loadedModule = Process.findModuleByName(MODULE_NAME);
        log('info', '[probe:load] script loaded | arch=' + Process.arch +
            ' pointerSize=' + Process.pointerSize +
            ' | ' + MODULE_NAME + '=' + (loadedModule
                ? (fmtPtr(loadedModule.base) + ' size=0x' + loadedModule.size.toString(16))
                : '*** NOT FOUND ***') +
            ' | expected gc-module md5=fab04426db6a014c0129ef2001530908');
    } catch (loadError) {
        try { console.log('load probe failed: ' + loadError.message); } catch (_) {}
    }
})();
