// ============================================================
// script.js — 开火直伤/弹体追踪 (feature_id: "direct_damage")
//
// 【C 路线 · 根治版】
//   本文件是 40_direct_damage 的"不碰死亡与复活"版本。
//   旧版（自己合成伤害 + 跳过原函数 + 死亡兜底）已整体备份到
//   04-正式发行版/_备份_40_direct_damage_注入版_2.7/40_direct_damage/，
//   需要对照旧行为时去那里看，不要在本文件里恢复注入路径。
//
// ------------------------------------------------------------------
// 本版本只做两件事
// ------------------------------------------------------------------
//   1) 常规枪械 —— 子弹方向修正（config.enable_guns 一个开关）
//        在 WPN_Gun.Damage 的 onEnter 里，把这一发的 rayDir 三个 float
//        改成"指向准星方向最近的敌人"，然后放行原函数。
//   2) 榴弹 / 手雷 / RPG / 榴弹枪 / 技能弹 —— 弹体追踪（homing）
//        在物理步末尾改写弹体 Rigidbody.velocity，让它拐向敌人。
//
// ------------------------------------------------------------------
// 本版本绝对不做的事（与旧版的分界线，也是"根治"的含义）
// ------------------------------------------------------------------
//   × 不合成 DamageEventData，不调用 GameManager.TakeDamage /
//     Entity.OnEntityHurt / Player.OnEntityHurt / HealthData.Hurt
//   × 不 Interceptor.replace，不做任何"跳过原函数"的栈操作
//   × 不碰死亡与复活：不补发 DeathEventBroadcast、不调 RespawnPlayer /
//     Player.Respawn、不挂 GameRoundEnd / NewGameRoundStart / OnDestroy
//   × 不清目标的复活无敌 / 减伤状态（那是复活系统的一部分，交给游戏；
//     2026-10-20 起唯一例外是 pierce_respawn_invincible：只结束「完全免疫」，见 clearDefenseBeforeShot）
//   × 不做"击杀后观察 N 秒看有没有复活"的兜底窗口
//
//   为什么这样就够（也是为什么旧版是越界）：
//     原版链路：开火 -> 射线 -> WPN_Gun.Damage 内 RaycastAll -> 命中体
//               -> 构造伤害事件 -> 结算 -> DeathEventBroadcast
//               -> 模式记账 -> 复活调度
//     我们只改写"射线方向"这一个输入，原函数一行不改地跑完 ——
//     伤害、击杀提示、死亡广播、复活计时全部还是游戏自己的代码。
//     旧版是自己合成伤害 + 跳过原函数，等于只跑了原函数的后半截，
//     于是"扣了血但死亡流程没走完"，表现就是躺尸不复活；
//     为了补这个洞才加了 death_fix_broadcast / death_fix_respawn。
//     本版本把注入链路整个删除，兜底自然不再需要。
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
//   3) 统一目标策略（与自瞄 11_aim/script.js 的 TARGET_POLICY 完全一致）
//      - 先卡外锥：夹角 <= target_outer_cone_deg 才算候选；
//      - 内锥 target_inner_cone_deg 有人时，只在内锥里选；
//      - 角度优先；角度差 <= target_angle_tie_deg 时再比距离；
//      - 当前目标轻粘滞：新目标角度优势 > target_switch_margin_deg，
//        且连续 target_switch_confirm_scans 次确认后才换；
//      - 枪械锥内没人默认不回退（可选近距保底）。
//
//   4) 目标命中点
//      优先胸部骨骼 spine1（character +0x60），退化到 spine（+0x5C），
//      最后退化到"玩家坐标 + 身高偏移"。
//
// ------------------------------------------------------------------
// 设计说明二：射线接管（常规枪械唯一的实现方式）
// ------------------------------------------------------------------
//   WPN_Gun.Damage(weapon, originX, originY, originZ, dirX, dirY, dirZ) 是 cdecl，
//   参数压在栈上：arg0 在 [esp+4]，arg1..arg6 在 [esp+8]..[esp+0x1C]。
//   在 onEnter 里改写 [esp+0x14]/[esp+0x18]/[esp+0x1C] 就等于改写了 rayDir。
//   写栈之前先校验"这 6 个数像不像一条射线"（起点分量有限、方向接近单位向量），
//   不像就一行都不写，让原版射线照原样跑。
//
//   ★ 关键：我们只写 rayDir，其余一切（命中判定、伤害数值、距离衰减、
//     无敌判定、死亡广播、击杀提示、复活调度）都由原函数完成。
//
// ------------------------------------------------------------------
// 设计说明三：开关划分
// ------------------------------------------------------------------
//   enable_guns              : 普通枪械自动跟枪（唯一用户开关）
//   enable_homing            : 投射物 追踪（制导）总开关
//   enable_explosives        : 榴弹 / 手雷 / RPG / 榴弹枪 弹体追踪（子开关）
//   enable_skill_projectiles : 特殊技能弹体追踪（奥术手雷 / 地狱终结者火球）（子开关）
//
//   为什么爆炸物 / 技能弹不做直伤：
//     它们的原版逻辑本来就是"弹体飞到 -> 命中判定 -> WPN_GRENADE.CreateExplosion
//     做范围伤害"。也就是说 **只要弹体能飞到敌人身上，原版自己就会把伤害算对**
//     （含爆炸范围、距离衰减、wpnIndex、死亡广播、击杀归属）。
//     所以这两类的正确做法是：**不注入任何伤害，只把弹体掰向敌人**，
//     伤害 100% 交给原版。
//
// ------------------------------------------------------------------
// 设计说明四：弹体追踪（制导）挂在哪、怎么拐
// ------------------------------------------------------------------
//   反汇编（GameAssembly.dll 0x10B6D080 = Weapon.ProjectMissile）确认了投射物
//   的完整生成链路：
//
//     missile = EffectManager.GetEffect(prefab)        // 从对象池取一颗
//     missile->owner          = weapon->owner          // +0x30  **直接写字段**
//     missile->ownerInitalTeam = owner->team           // +0x34
//     ... 位置 / 朝向 ...
//     callback.Invoke(missile)
//         -> WPN_Missile.SetWeaponData(missile, weapon.data, sprIndex)   // +0x38/+0x3C
//     RecyclableObject.Active(missile) -> Work()
//         -> Rigidbody.velocity = transform.forward * shootSpeed         // +0x4C
//
//   两个关键结论：
//     1) owner **不经过 WPN_Missile.SetOwner**：全二进制里对 SetOwner 的直接
//        call 有 0 处，所以"在 SetOwner 里登记制导"永远不会触发 —— 这正是
//        旧版追踪完全不生效的根因（homingArmed 永远是 0）。
//     2) 弹体是标准物理刚体：Work() 用 Rigidbody.velocity 发射，FixedUpdate()
//        （0x10B660C0）只做 Rigidbody.AddForce(extraGravity)，所以"改写
//        velocity"就能拐弯，不需要碰任何游戏逻辑。
//
//   因此登记挂点是 WPN_Missile.SetWeaponData（0x00B663C0）：
//     - 它由 ProjectMissile 的回调调用，5 种投射物（RPG / 手雷 / 榴弹枪 /
//       奥术手雷 / 地狱终结者火球）**全部**会走到；
//     - 进入时 owner 已经写好 -> 用 Player.get_isMyPlayer 判断"是不是自己发射的"；
//     - 进入时还没 Active()，属于"发射前登记"，随后 FixedUpdate 才开始拐；
//     - 对象池会复用弹体指针，所以每次 SetWeaponData **先无条件清掉旧记录**，
//       再决定要不要登记，避免"敌人的手雷被掰到我们的目标上"。
//
//   拐弯算法（挂在 WPN_Missile.FixedUpdate 的 onLeave，物理步末尾）：
//     1) 读弹体自身速度 shootSpeed(+0x4C)，读 Rigidbody.get_velocity 拿当前方向；
//     2) 目标方向 = normalize(敌人瞄准点 - 弹体位置)；
//     3) 新方向 = 当前方向与目标方向按 homing_turn 插值；
//     4) Rigidbody.set_velocity(新方向 * 速度)，同时把 transform 朝向也掰过去。
//
//   "打谁"策略（scanEnemies + 准星锥）：
//     与枪械/自瞄同一套：外锥 -> 内锥优先 -> 角度优先 -> 距离 tiebreak。
//     发射时锥轴 = 玩家相机朝向（锥心 = 眼睛位置）；
//     目标死亡后换目标时锥轴 = 弹体当前速度方向（锥心 = 弹体位置）。
//     锥内没人：missile_fallback_nearest=true（默认）回退最近，
//              可用 missile_fallback_max_distance 限制回退距离；
//              =false 则这颗弹不追踪、按原弹道直飞。
//
// ------------------------------------------------------------------
// 配置项速查
// ------------------------------------------------------------------
//   enable_guns / enable_homing / enable_explosives / enable_skill_projectiles
//   target_outer_cone_deg / target_inner_cone_deg / target_angle_tie_deg
//   target_switch_margin_deg / target_switch_confirm_scans / target_switch_cooldown_ms
//   max_distance / local_eye_height / chest_fallback_height / target_cache_ms
//   gun_fallback_nearest / gun_fallback_max_distance
//   homing_speed / homing_turn / homing_retarget / homing_max_ms
//   homing_pending_ms / missile_fallback_nearest / missile_fallback_max_distance
//   diagnostic_log / log_every / verbose_probe / log_to_file / log_file
//
//   注意：这里**没有任何** death_* / damage_entry / damage_override /
//   use_event_template / fallback_to_original / gun_hook_mode 配置 ——
//   那些键随注入链路一起删除了，旧 user_config.json 里若还留着也会被忽略。
// ============================================================

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';
    var MAX_PLAYER_SLOTS = 64;
    var POINTER_SIZE = 4;

    // 投射物类别（只决定"归哪个子开关管"，与伤害无关）
    var CATEGORY = {
        EXPLOSIVE: 'explosive',
        SKILL: 'skill'
    };

    // ------------------------------------------------------------------
    // RVA 表（GameAssembly.dll）
    // ------------------------------------------------------------------
    //   版本不匹配时，[probe:rva] 日志里的 *** NOT EXECUTABLE *** 就是第一证据。
    //   本表只保留本版本真正用到 / 需要审计的地址；
    //   GameManager.TakeDamage / DeathEventBroadcast / RespawnPlayer / HealthData.Hurt
    //   等"伤害-死亡"入口 **已全部删除** —— 本版本不碰它们。
    // ------------------------------------------------------------------
    var RVA = {
        // ---- 常规枪械（射线接管）----
        WPN_Gun_Damage: 0x00B613D0,

        // ---- 弹体发射入口（只登记"这颗弹是谁的、什么类别"，不注入伤害）----
        WPN_RPG_Fire: 0x00B670A0,
        WPN_Throw_Throw: 0x00B6AD80,
        WPN_GrenadeGun_GunShootFunction_Lambda: 0x00B602A0,
        WPN_Arcane_Throw: 0x00B59640,
        WPN_EvilTerminator_ThrowFireBall: 0x00B5C600,

        // ---- 只读的 IL2CPP 取值函数 ----
        Weapon_get_isMyWeapon: 0x00B6E1D0,
        Player_get_isMyPlayer: 0x00B55FD0,
        Entity_get_isDead: 0x00B400E0,
        Entity_get_team: 0x001E0070,

        // ---- GameManager 单例 ----
        Singleton_GameManager_get_instance: 0x004A8170,
        SingletonGameManager_MethodInfo: 0x00E1CE64,
        GameManager_TypeInfo: 0x00E2933C,

        // ---- Transform ----
        Component_get_transform: 0x0032CF40,
        Transform_get_position_Injected: 0x003F4280,

        // ---- 投射物（制导）----
        Weapon_ProjectMissile: 0x00B6D080,
        WPN_Missile_SetWeaponData: 0x00B663C0,
        WPN_Missile_FixedUpdate: 0x00B660C0,
        WPN_Missile_Work: 0x00B664D0,
        WPN_GRENADE_Work: 0x00B5D6C0,
        WPN_Missile_Recycle: 0x00B66240,
        // 所有爆炸结算的公共入口（WPN_GRENADE 及其子类 Msl_Arcane 等都走它）
        WPN_GRENADE_CreateExplosion: 0x00B5CC40,
        // 游戏统一的伤害入口（静态，DamageEventData 按值压栈）
        GameManager_TakeDamage: 0x00AFC1C0,
        WPN_Missile_OnCollisionEnter: 0x00B66100,
        WPN_GRENADE_OnCollisionEnter: 0x00B5D0F0,
        WPN_GRENADE_OnTriggerEnter: 0x00B5D270,
        RecyclableObject_Recycle: 0x00B1A5A0,

        // ---- 刚体 / 朝向 ----
        Rigidbody_get_velocity_Injected: 0x00ABBDC0,
        Rigidbody_set_velocity: 0x00ABC060,
        Quaternion_LookRotation: 0x004F1710,
        Transform_set_rotation: 0x003F48A0
    };

    // ------------------------------------------------------------------
    // 结构体字段偏移（全部只读，唯一例外是弹体 Rigidbody.velocity）
    // ------------------------------------------------------------------
    var OFF = {
        Klass_staticFields: 0x5C,

        // ---- GameManager ----
        GameManager_myPlayer: 0x00,
        GameManager_allPlayers: 0x1C,
        GameManager_playersBL: 0x20,
        GameManager_playersGR: 0x28,

        // ---- Entity ----
        Entity_team: 0x20,
        Entity_healthData: 0x1C,

        // ---- Entity 防御状态（复活无敌 / 完全免疫）----
        //   平时只读；唯一例外是「突破复活无敌」开着时，在放行原版射线前复位它们
        //   （见 clearDefenseBeforeShot）。偏移与 dump.cs / IDA 反汇编逐一核对过：
        //     Entity.<damageRate>k__BackingField   +0x14 (float)  get_damageRate: fld [eax+14h]
        //     Entity.<isInvincible>k__BackingField +0x18 (bool)   get_isInvincible: mov al,[eax+18h]
        //     HealthData.invinsibleEndTime         +0x44 (float)  复活无敌结束时间戳
        Entity_damageRate: 0x14,
        Entity_isInvincible: 0x18,
        HealthData_invinsibleEndTime: 0x44,

        // ---- Player ----
        Player_cameraRotation: 0x4C,
        Player_characterContainer: 0x58,
        Player_currentCharacter: 0x5C,

        // ---- Weapon / WeaponData ----
        Weapon_data: 0x68,
        WPN_Gun_realData: 0xEC,
        WeaponData_Gun_ammoDamage: 0x14C,

        // ---- MissileData（只读，仅用于日志"原生弹体伤害=N（只记录，不注入）"）----
        MissileData_damage: 0x0C,
        WD_RPG_missileData: 0xB8,
        WD_Missile_missileData: 0xB8,
        WD_GrenadeGun_missileData: 0x20C,
        WD_EvilTerminator_missileData: 0xF8,

        // ---- 弹体实例 ----
        Missile_owner: 0x30,
        Missile_weaponData: 0x38,
        Missile_rigidBody: 0x44,
        Missile_shootSpeed: 0x4C,

        // ---- 骨骼（瞄准点）----
        CharacterModel_spine: 0x5C,
        CharacterModel_spine1: 0x60,

        // ---- IL2CPP 容器 ----
        Il2CppArray_length: 0x0C,
        Il2CppArray_items: 0x10,
        Il2CppList_items: 0x08,
        Il2CppList_size: 0x0C
    };

    var Runtime = {
        feature_id: 'direct_damage',
        enabled: false,
        initialized: false,
        generation: 0,

        // 日志三路输出：内存环形缓冲 / 可选文件 / send() 给 UI
        logRing: [],
        logRingCap: 3000,
        logFilePath: '',
        logFileHandle: null,
        logFileTried: false,
        logFileFailed: '',
        heartbeat: null,
        heartbeatTicks: 0,

        // 弹体追踪：missile 指针 -> 制导记录
        missileTargets: {},
        // 开火钩子留下的"这颗弹属于哪个类别"，等 SetWeaponData 来配对
        pendingMissile: null,

        module: null,
        base: ptr(0),
        attachHooks: [],

        config: {
            // ---- 开关 ----
            enable_guns: true,               // 常规枪械：射线接管
            enable_homing: true,             // 弹体追踪总开关
            enable_explosives: true,         // 榴弹 / 手雷 / RPG / 榴弹枪
            enable_skill_projectiles: true,  // 奥术手雷 / 地狱终结者火球

            // 突破复活无敌：开火/爆炸前把目标的复活保护（完全免疫）复位，让伤害真的落地。
            //   只写防御状态字段，不碰血量、不合成伤害事件、不调用任何游戏函数；
            //   扣血 / 死亡广播 / 复活调度仍然全部由原版完成 ——
            //   这是「不会出现躺尸不复活」的前提（那条 bug 的成因是跳过原函数自己注入）。
            pierce_respawn_invincible: true,

            // ---- 统一目标策略（与 11_aim 的 TARGET_POLICY 同一套）----
            //   外锥 -> 内锥优先 -> 角度优先（角度差 <= tie 时比距离）-> 轻粘滞。
            //   枪械是"开火事件驱动"，确认帧用 1；自瞄是连续扫描，确认帧用 2。
            target_outer_cone_deg: 30.0,
            target_inner_cone_deg: 20.0,
            target_angle_tie_deg: 1.0,
            target_switch_margin_deg: 1.2,
            target_switch_confirm_scans: 1,
            target_switch_cooldown_ms: 100,
            max_distance: 0.0,          // 0 = 不限距离
            local_eye_height: 1.55,     // 准星锥的锥心 = 玩家坐标 + 该高度
            chest_fallback_height: 1.1, // 读不到骨骼时的瞄准点高度
            target_cache_ms: 15,        // 目标缓存（同一次开火/同一帧内不重复扫人）

            // 枪械锥内没人时：默认不回退，避免"对着空气开火却打最近的人"。
            // 需要保底命中可打开，并只回退到近距 target_fallback_max_distance 内。
            gun_fallback_nearest: false,
            gun_fallback_max_distance: 10.0,

            // ---- 弹体追踪 ----
            homing_speed: 0.0,          // 0 = 用弹体自身的 shootSpeed
            homing_turn: 1.0,           // 0.05~1.0，每个物理步把方向掰向目标的力度
            homing_retarget: true,      // 原目标死了自动改追（用同一套锥角/排序）
            homing_max_ms: 20000,       // 超过这个时间放弃制导（防指针复用/泄漏）
            homing_pending_ms: 800,     // "开火记录 -> 弹体生成"的最大配对时间差
            // 弹体发射时也走同一套准星锥；锥内没人时回退"全场最近"，
            // 保住"对着空气扔雷也能追到人"。
            missile_fallback_nearest: true,
            missile_fallback_max_distance: 0.0, // 0 = 不限距离

            // ---- 诊断 ----
            diagnostic_log: false,
            log_every: 20,
            verbose_probe: false,
            log_to_file: false,     // 默认不在游戏目录写日志文件
            log_file: ''            // 由调用方下发；为空则只走内存缓冲 + UI
        },
        cache: {
            posBuf: null,           // Vector3 回传缓冲
            quatBuf: null,          // Quaternion 回传缓冲
            floatBuf: null,         // u32 <-> float
            ownPlayer: ptr(0),
            selectedTarget: null,
            selectedAtMs: 0,
            rayWarnLogged: false,
            diagTd: 0,              // 伤害入口诊断：已经打过多少条
            diagTdForeign: 0,       // 爆炸伤害但 attacker 不是本地玩家：已经打过多少条
            diagExp: 0,             // 爆炸入口诊断：已经打过多少条
            myExplosionAt: 0        // 最近一次「自己的爆炸」的时间戳（伤害入口按它归因）
        },
        // 枪械专用的目标锁定状态。弹体每颗弹有独立 target，不复用这个状态。
        targetLock: null,
        stats: {
            // ---- 常规枪械 ----
            gunDamageCalls: 0,
            localGunFires: 0,
            skippedRemote: 0,       // Bot 开火（不是我的武器），原版直接跑
            gunHookDisabled: 0,     // 功能/枪械开关关着
            rayRedirectShots: 0,    // "把射线掰到目标身上"的成功次数
            rayRedirectBadArgs: 0,  // 参数不像射线 -> 一行没写
            rayRedirectSkip: 0,     // 没走到选目标就退出（没本地玩家 / 读不到相机朝向 / 距离过近）
            invincibleCleared: 0,   // 复位了目标的复活无敌/完全免疫（pierce_respawn_invincible）
            explosionDefenseCalls: 0,    // WPN_GRENADE.CreateExplosion 被调用次数（所有爆炸）
            explosionDefenseCleared: 0,  // 爆炸穿透真正复位的敌人数
            takeDamageCalls: 0,          // GameManager.TakeDamage 被调用次数（全场）
            takeDamageOurs: 0,           // 其中 attacker = 本地玩家的次数
            takeDamageCleared: 0,        // 伤害入口兜底真正复位的次数
            invincibleUnreadable: 0, // 目标防御状态读不到（指针不可读/HealthData 为空），一枚字节都没写
            targetsSelected: 0,
            noTarget: 0,
            targetLockReason: 'init',
            targetSwitchCount: 0,
            // ---- 弹体追踪 ----
            missileSpawns: 0,      // SetWeaponData 命中次数 = 观察到几颗弹生成
            missileNotMine: 0,     // 弹体是别人发射的（不制导）
            missileNoPending: 0,   // 弹体生成了但没抓到开火记录（配对失败）
            missileSwitchOff: 0,   // 类别子开关关掉了
            missileNoTarget: 0,    // 没有可选目标（场上没敌人）
            homingArmed: 0,        // 有多少颗自己的弹体被登记为"要制导"
            homingSteered: 0,      // 实际改写速度/朝向的次数
            homingDropped: 0,      // 目标死亡/超时后放弃的次数
            homingForgotten: 0,    // 弹体爆炸/回收/被复用，清掉记录次数
            missileLaunchSeen: 0,  // Work() 被调用次数（弹体真的发射了）
            missileHitSeen: 0,     // 弹体 OnCollisionEnter 次数（只记账）
            missileTriggerSeen: 0, // 弹体 OnTriggerEnter 次数（只记账）
            fixedUpdateCalls: 0,   // WPN_Missile.FixedUpdate 被调用总次数
            steerOff: 0,           // 总开关/类别开关关掉而跳过的帧数
            steerNoEntry: 0,       // 没有制导记录（记录已被清掉 / 不是我们的弹）
            steerNoPos: 0,         // 读不到弹体位置
            steerNoAim: 0,         // 读不到目标命中点
            steerTooClose: 0,      // 已贴脸，交给原版碰撞判定
            steerWrote: 0,         // 真的写进了 Rigidbody.velocity
            steerWriteSkip: 0,     // rb 不可读 / native 不可用
            steerLostTarget: 0,    // 目标死了但暂时没有新目标（保留记录继续飞）
            forgetReuse: 0,        // 记录被清掉的原因分布
            forgetRecycle: 0,
            forgetTimeout: 0,
            forgetLost: 0,
            forgetIdentity: 0,
            // ---- 弹体追踪的"打谁"策略计数（准星锥） ----
            coneHit: 0,            // 锥内选到目标
            coneEmpty: 0,          // 锥内一个敌人都没有
            coneFallback: 0,       // 锥内没人 -> 回退成全场最近
            coneEmptyStrict: 0,    // 锥内没人且关掉了回退 -> 放弃追踪
            coneOff: 0,            // target_outer_cone_deg = 0，没启用锥
            coneAxisFail: 0,       // 读不到相机朝向/弹体速度 -> 退回全场最近
            coneRetarget: 0,       // 中途换目标时用了锥并选中
            // ---- 通用 ----
            explosiveTriggers: 0,
            skillTriggers: 0,
            ownPlayerSource: '',
            errorCount: 0,
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
        getVelocity: null,
        setVelocity: null,
        lookRotation: null,
        setRotation: null
    };

    // ------------------------------------------------------------------
    // 日志与探针（持久化）
    // ------------------------------------------------------------------
    //   三路同时输出，任何一路挂掉都不影响另外两路：
    //     1) Runtime.logRing           内存环形缓冲，RPC logs() 拉取（不依赖文件权限）
    //     2) config.log_file 指向的文件  磁盘持久化，每行 flush（游戏崩了也不丢）
    //     3) send({type:'log'})        调试 UI 的日志框
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

            // 弹体追踪：Rigidbody.velocity / Quaternion.LookRotation / Transform.rotation
            //   Vector3(12B)、Quaternion(16B) 都是按值压栈的 struct，同样拆成 4 字节标量。
            //   get_velocity 走 Injected 版本（out Vector3*），避免按值返回 struct。
            native.getVelocity = new NativeFunction(
                base.add(RVA.Rigidbody_get_velocity_Injected), 'void',
                ['pointer', 'pointer', 'pointer'], CALL_CONV
            );
            native.setVelocity = new NativeFunction(
                base.add(RVA.Rigidbody_set_velocity), 'void',
                ['pointer', 'uint', 'uint', 'uint', 'pointer'], CALL_CONV
            );
            native.lookRotation = new NativeFunction(
                base.add(RVA.Quaternion_LookRotation), 'void',
                ['pointer', 'uint', 'uint', 'uint', 'pointer'], CALL_CONV
            );
            native.setRotation = new NativeFunction(
                base.add(RVA.Transform_set_rotation), 'void',
                ['pointer', 'uint', 'uint', 'uint', 'uint', 'pointer'], CALL_CONV
            );

            // 说明：旧版在这里还会构造 GameManager.TakeDamage / OnEntityHurt /
            // HealthData.Hurt / DeathEventBroadcast 的 NativeFunction。
            // C 路线把这些**全部删除** —— 本文件不再持有任何"造成伤害/处理死亡"的能力。

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
            if (!Runtime.cache.posBuf) Runtime.cache.posBuf = Memory.alloc(16);
            if (!Runtime.cache.quatBuf) Runtime.cache.quatBuf = Memory.alloc(16);   // Quaternion 回传缓冲
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
    // 统一目标策略（与 11_aim/script.js 的 TARGET_POLICY 保持一致）
    // ------------------------------------------------------------------
    function createTargetLockState() {
        return {
            current: null,
            pendingPlayer: null,
            pendingCount: 0,
            lastSwitchAtMs: 0,
            reason: 'init',
            switchCount: 0
        };
    }

    function resetTargetLock(state, reason) {
        var lock = state || Runtime.targetLock;
        if (!lock) return;
        lock.current = null;
        lock.pendingPlayer = null;
        lock.pendingCount = 0;
        lock.lastSwitchAtMs = 0;
        lock.reason = reason || 'reset';
        lock.switchCount = 0;
    }

    function sameTargetPlayer(a, b) {
        if (!a || !b) return false;
        if (a === b) return true;
        try { if (typeof a.equals === 'function') return a.equals(b); } catch (_) {}
        try { if (typeof b.equals === 'function') return b.equals(a); } catch (_) {}
        return false;
    }

    function targetPolicy() {
        var c = Runtime.config;
        return {
            outerConeDeg: c.target_outer_cone_deg,
            innerConeDeg: c.target_inner_cone_deg,
            angleTieDeg: c.target_angle_tie_deg,
            switchMarginDeg: c.target_switch_margin_deg,
            switchConfirmScans: c.target_switch_confirm_scans,
            switchCooldownMs: c.target_switch_cooldown_ms
        };
    }

    function candidateAngle(candidate) {
        return candidate && isFinite(candidate.angleDeg) ? candidate.angleDeg : Infinity;
    }

    function candidateIsBetter(a, b, angleTieDeg) {
        if (!a) return false;
        if (!b) return true;
        var aAngle = candidateAngle(a);
        var bAngle = candidateAngle(b);
        if (!isFinite(aAngle)) return false;
        if (!isFinite(bAngle)) return true;
        var tie = Math.max(0.0, angleTieDeg || 0.0);
        if (aAngle + tie < bAngle) return true;
        if (bAngle + tie < aAngle) return false;
        return a.dist < b.dist;
    }

    // 内锥优先；同一层里角度优先，角度差在 tie 内再比距离。
    function pickBestCandidate(candidates, innerConeDeg, angleTieDeg) {
        if (!candidates || candidates.length === 0) return null;
        var bestInner = null;
        var bestOuter = null;
        var innerLimit = Math.max(0.0, innerConeDeg || 0.0);
        for (var i = 0; i < candidates.length; i += 1) {
            var candidate = candidates[i];
            if (!candidate || !isFinite(candidate.angleDeg)) continue;
            if (!bestOuter || candidateIsBetter(candidate, bestOuter, angleTieDeg)) bestOuter = candidate;
            if (candidate.angleDeg <= innerLimit &&
                (!bestInner || candidateIsBetter(candidate, bestInner, angleTieDeg))) {
                bestInner = candidate;
            }
        }
        return bestInner || bestOuter;
    }

    function findCandidateByPlayer(candidates, player) {
        if (!candidates || !player) return null;
        for (var i = 0; i < candidates.length; i += 1) {
            if (candidates[i] && sameTargetPlayer(candidates[i].player, player)) return candidates[i];
        }
        return null;
    }

    // 统一目标选择：角度优先 + 内锥优先 + 轻粘滞。
    // 枪械是事件驱动（每发一次），switch_confirm_scans 默认 1；
    // 自瞄是连续扫描，默认 2。
    function selectTargetFromCandidates(candidates, nowMs) {
        if (!Runtime.targetLock) Runtime.targetLock = createTargetLockState();
        var lock = Runtime.targetLock;
        var policy = targetPolicy();
        var best = pickBestCandidate(candidates, policy.innerConeDeg, policy.angleTieDeg);

        if (!best) {
            lock.current = null;
            lock.pendingPlayer = null;
            lock.pendingCount = 0;
            lock.reason = 'no_candidate';
            return null;
        }

        var current = lock.current;
        var currentFresh = current ? findCandidateByPlayer(candidates, current.player) : null;

        if (!current) {
            lock.current = best;
            lock.pendingPlayer = null;
            lock.pendingCount = 0;
            lock.lastSwitchAtMs = nowMs;
            lock.reason = 'acquire';
            return best;
        }

        if (!currentFresh) {
            lock.current = best;
            lock.pendingPlayer = null;
            lock.pendingCount = 0;
            lock.lastSwitchAtMs = nowMs;
            lock.reason = 'current_lost';
            return best;
        }

        if (sameTargetPlayer(best.player, currentFresh.player)) {
            lock.current = currentFresh;
            lock.pendingPlayer = null;
            lock.pendingCount = 0;
            lock.reason = 'hold';
            return currentFresh;
        }

        var currentAngle = candidateAngle(currentFresh);
        var bestAngle = candidateAngle(best);
        var currentInner = currentAngle <= policy.innerConeDeg;
        var bestInner = bestAngle <= policy.innerConeDeg;
        var advantage = currentAngle - bestAngle;
        var wantSwitch = false;
        var switchReason = '';

        if (bestInner && !currentInner) {
            wantSwitch = true;
            switchReason = 'inner_override';
        } else if (advantage > policy.switchMarginDeg) {
            wantSwitch = true;
            switchReason = 'angle_advantage';
        }

        if (!wantSwitch) {
            lock.current = currentFresh;
            lock.pendingPlayer = null;
            lock.pendingCount = 0;
            lock.reason = 'hold';
            return currentFresh;
        }

        if ((nowMs - lock.lastSwitchAtMs) < policy.switchCooldownMs) {
            lock.current = currentFresh;
            lock.pendingPlayer = null;
            lock.pendingCount = 0;
            lock.reason = 'cooldown_hold';
            return currentFresh;
        }

        if (!lock.pendingPlayer || !sameTargetPlayer(lock.pendingPlayer, best.player)) {
            lock.pendingPlayer = best.player;
            lock.pendingCount = 1;
        } else {
            lock.pendingCount += 1;
        }
        if (lock.pendingCount < policy.switchConfirmScans) {
            lock.current = currentFresh;
            lock.reason = 'confirming';
            return currentFresh;
        }

        lock.current = best;
        lock.pendingPlayer = null;
        lock.pendingCount = 0;
        lock.lastSwitchAtMs = nowMs;
        lock.switchCount += 1;
        lock.reason = switchReason;
        return best;
    }

    function pickNearestCandidate(candidates, maxDistance) {
        if (!candidates || candidates.length === 0) return null;
        var limit = maxDistance > 0 ? maxDistance : Infinity;
        var best = null;
        for (var i = 0; i < candidates.length; i += 1) {
            var candidate = candidates[i];
            if (!candidate || !isFinite(candidate.dist) || candidate.dist > limit) continue;
            if (!best || candidate.dist < best.dist) best = candidate;
        }
        return best;
    }

    // ------------------------------------------------------------------
    // 枪械目标选择：准星锥 -> 内锥优先 -> 角度优先 -> 轻粘滞
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
        var policy = targetPolicy();
        var coneCandidates = [];
        var allCandidates = [];
        var best = null;
        var nearestDistance = -1;

        // 世界级探针：候选集多大、准星朝哪、用什么条件筛
        if (probeBudget('sel', 30)) {
            probe('sel', 'players=' + players.length + ' myPlayer=' + fmtPtr(myPlayer) +
                ' myTeam=' + myTeam + ' eye=' + fmtVec(eyePos) +
                ' rot=' + rotation.yawDeg.toFixed(1) + '/' + rotation.pitchDeg.toFixed(1) +
                ' outer=' + policy.outerConeDeg + 'deg inner=' + policy.innerConeDeg +
                ' maxDist=' + Runtime.config.max_distance +
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

                var entry = {
                    player: candidate,
                    pos: aimPoint,
                    rootPos: targetRoot,
                    dist: angles.dist,
                    angleDeg: angleDeg
                };
                allCandidates.push(entry);
                if (nearestDistance < 0 || angles.dist < nearestDistance) nearestDistance = angles.dist;

                if (angleDeg > policy.outerConeDeg) {
                    note(i, fmtPtr(candidate) + ' angle=' + angleDeg.toFixed(1) +
                        ' > outer=' + policy.outerConeDeg + ' -> outside crosshair cone, skip');
                    continue;
                }
                note(i, fmtPtr(candidate) + ' ACCEPT angle=' + angleDeg.toFixed(1) +
                    ' dist=' + angles.dist.toFixed(1));
                coneCandidates.push(entry);
            } catch (_) {}
        }

        best = selectTargetFromCandidates(coneCandidates, Date.now());

        // 可选保底：锥内没人时，只回退到近距最近；默认关闭。
        if (!best && Runtime.config.gun_fallback_nearest) {
            best = pickNearestCandidate(allCandidates, Runtime.config.gun_fallback_max_distance);
            if (best && Runtime.targetLock) {
                Runtime.targetLock.current = best;
                Runtime.targetLock.reason = 'fallback_nearest';
            }
        }

        Runtime.stats.targetLockReason = Runtime.targetLock ? Runtime.targetLock.reason : 'uninitialized';
        Runtime.stats.targetSwitchCount = Runtime.targetLock ? Runtime.targetLock.switchCount : 0;

        if (best) {
            Runtime.stats.targetsSelected += 1;
            Runtime.stats.lastTargetAngle = best.angleDeg;
            Runtime.stats.lastTargetDistance = best.dist;
        } else {
            Runtime.stats.noTarget += 1;
            probe('sel', 'NO TARGET: players=' + players.length +
                ' acceptedInCone=' + coneCandidates.length +
                ' nearest=' + (nearestDistance < 0 ? '-' : nearestDistance.toFixed(1)) +
                ' outer=' + policy.outerConeDeg + 'deg maxDist=' + Runtime.config.max_distance +
                ' fallback=' + (Runtime.config.gun_fallback_nearest ? 'on' : 'off'));
        }
        Runtime.stats.lastResult = best
            ? ('target ok, angle=' + best.angleDeg.toFixed(1) + 'deg, dist=' + best.dist.toFixed(1) +
                'm, candidates=' + coneCandidates.length + ', reason=' + Runtime.stats.targetLockReason)
            : ('no target, candidatesWithinCone=' + coneCandidates.length +
                ', nearest=' + (nearestDistance < 0 ? '-' : nearestDistance.toFixed(1)));
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
    // ------------------------------------------------------------------
    // WPN_Gun.Damage — 唯一挂法：attach + 射线接管
    // ------------------------------------------------------------------
    //   旧版还有 replace 模式（Interceptor.replace + 自己合成 DamageEventData +
    //   跳过原函数）。C 路线把那条路径整个删掉：只要"跳过原函数"还存在，
    //   "扣了血但死亡流程没走完 -> 躺尸不复活"就一定会以某种概率回来。
    //
    //   attach 模式只在 onEnter 里出现一次；Bot 开火（不是我的武器）一句 return，
    //   Frida 不留帧。★ 没有 onLeave：我们不核对血量，也就不需要"没掉血补一发"。
    function installGunHook() {
        registerAttach('WPN_Gun.Damage(ray-redirect)', RVA.WPN_Gun_Damage, {
            onEnter: function (args) {
                try {
                    Runtime.stats.gunDamageCalls += 1;
                    if (!Runtime.enabled || !Runtime.config.enable_guns) {
                        Runtime.stats.gunHookDisabled += 1;
                        return;                                   // 原版照常执行
                    }
                    var weapon = args[0];
                    if (!isLocalWeapon(weapon)) {
                        Runtime.stats.skippedRemote += 1;
                        if (probeBudget('gunRemote', 5)) {
                            probe('gunRemote', 'passthrough(native): not my weapon ' + fmtPtr(weapon) +
                                ' readable=' + readable(weapon) + ' isMyWeapon=' + safeBool(native.isMyWeapon, weapon));
                        }
                        return;                                   // ★ Bot 开火：JS 完全不介入
                    }

                    Runtime.stats.localGunFires += 1;
                    if (probeBudget('gunLocal', 5)) {
                        probe('gunLocal', 'ray-redirect fire #' + Runtime.stats.localGunFires +
                            ' weapon=' + fmtPtr(weapon) + ' ammoDamage=' + readGunDamage(weapon).toFixed(2));
                    }

                    // 只改这一发的射线方向；无论成功与否都不跳过原函数、不注入伤害。
                    redirectRayToTarget(this);
                } catch (error) {
                    fail('WPN_Gun.Damage onEnter', error);
                }
            }
        });
    }

    // ------------------------------------------------------------------
    // 原生射线接管（enable_guns）：把这一发的射线掰到目标身上
    // ------------------------------------------------------------------
    //   WPN_Gun.Damage(weapon, originX, originY, originZ, dirX, dirY, dirZ) 是 cdecl，
    //   参数压在栈上：arg0 在 [esp+4]，arg1..arg6 在 [esp+8]..[esp+0x1C]。
    //   在 onEnter 里改写 [esp+0x14]/[esp+0x18]/[esp+0x1C] 就等于改写了 rayDir ——
    //   原函数照常跑，命中判定/伤害/DeathEventBroadcast/复活调度全部走游戏自己的代码。
    //   写栈之前先校验"这 6 个数像不像一条射线"，不像就返回 false（调用方退回注入路径）。
    function readRayVec(sp) {
        try {
            var v = { x: sp.readFloat(), y: sp.add(4).readFloat(), z: sp.add(8).readFloat() };
            if (!isFinite(v.x) || !isFinite(v.y) || !isFinite(v.z)) return null;
            if (Math.abs(v.x) > 5000 || Math.abs(v.y) > 5000 || Math.abs(v.z) > 5000) return null;
            return v;
        } catch (_) { return null; }
    }

    // 返回 null = 参数布局不像 (weapon, origin(3), dir(3))
    function rayArgsLookSane(sp) {
        var origin = readRayVec(sp.add(8));     // args 1,2,3
        if (!origin) return null;
        var dir = readRayVec(sp.add(20));       // args 4,5,6
        if (!dir) return null;
        var len = Math.sqrt(dir.x * dir.x + dir.y * dir.y + dir.z * dir.z);
        // 方向必须是"像单位向量"的量级；不是 -> 说明参数不是我们以为的那样，绝不写栈
        if (!isFinite(len) || len < 0.3 || len > 2.0) return null;
        return { origin: origin, dir: dir };
    }
    // ------------------------------------------------------------------
    // 突破复活无敌（pierce_respawn_invincible）：放行原函数之前复位目标的防御状态
    // ------------------------------------------------------------------
    //   游戏在目标复活后会给一段保护：HealthData.invinsibleEndTime(+0x44) 是结束时间戳，
    //   Entity.damageRate(+0x14) 被压到 0，Entity.isInvincible(+0x18) 可能同时为 1。
    //   原版伤害链按这三样把这一发的伤害抹成 0 —— 射线明明命中了却不掉血。
    //   这里在**原函数还没执行**的时候把它们复位，然后原函数照常跑完。
    //
    //   ★ 边界（为什么它不会重现"死了不复活"）：
    //     只写三个防御状态字段 —— 不写 HP、不写任何对象指针、不合成 DamageEventData、
    //     不调用任何游戏函数、不跳过原函数。扣血、死亡广播、复活调度仍然 100% 是游戏自己的代码。
    //     旧版那条"躺尸不复活"的成因是"自己注入伤害 + 跳过原函数"，本函数一行都没碰。
    function readDefenseState(victim) {
        var info = { ok: false, health: ptr(0), invEnd: 0, damageRate: 1, isInvincible: 0, active: false, err: '' };
        try {
            if (isNull(victim) || !readable(victim)) return info;
            var health = victim.add(OFF.Entity_healthData).readPointer();
            if (isNull(health) || !readable(health)) return info;
            var invEnd = health.add(OFF.HealthData_invinsibleEndTime).readFloat();
            var damageRate = victim.add(OFF.Entity_damageRate).readFloat();
            var isInvincible = victim.add(OFF.Entity_isInvincible).readU8();
            if (!isFinite(invEnd) || !isFinite(damageRate)) return info;
            info.health = health;
            info.invEnd = invEnd;
            info.damageRate = damageRate;
            info.isInvincible = isInvincible >>> 0;
            // 合理性闸门：指针被回收/复用时，这三个字段读出来往往是天文数字。
            // 不合理就当作"读不到"处理 —— 宁可这一发不穿透，也不把字节写到别的对象上。
            if (!(damageRate >= 0 && damageRate <= 10) ||
                !(invEnd >= 0 && invEnd <= 10000000) ||
                info.isInvincible > 1) {
                info.err = 'implausible defense state';
                return info;
            }
            info.ok = true;
            // 「完全免疫」才算复活保护：复活时游戏把 damageRate 压到 0；
            // 部分减伤（0.03 终结者技能护盾 / 0.88 补给箱护盾）不在此列，绝不抹掉。
            info.active = invEnd > 0 || damageRate < 0.001 || info.isInvincible === 1;
        } catch (error) {
            info.ok = false;
            info.err = (error && error.message) ? String(error.message) : String(error);
        }
        return info;
    }

    // 复位目标的复活无敌（完全免疫）。返回复位前的值（日志/UI 里能直接看到是不是它在挡）。
    //   任何一项写失败都只吞掉，绝不让开火链路抛异常。
    function clearDefenseBeforeShot(victim) {
        var before = readDefenseState(victim);
        if (!before.ok) {
            Runtime.stats.invincibleUnreadable += 1;
            return before;
        }
        if (!before.active) return before;
        try {
            if (before.invEnd > 0) before.health.add(OFF.HealthData_invinsibleEndTime).writeFloat(0);
        } catch (_) {}
        try {
            // 只复位「完全免疫」（复活保护）。0<rate<1 是普通减伤/护盾 buff，
            // 抹掉它等于把别人的技能废掉 —— 那不是本功能要的东西。
            if (before.damageRate < 0.001) victim.add(OFF.Entity_damageRate).writeFloat(1.0);
        } catch (_) {}
        try {
            if (before.isInvincible === 1) victim.add(OFF.Entity_isInvincible).writeU8(0);
        } catch (_) {}
        Runtime.stats.invincibleCleared += 1;
        if (probeBudget('pierceInv', 20)) {
            probe('pierceInv', '目标处于复活无敌（完全免疫），已在放行原版射线前复位: isInvincible=' +
                before.isInvincible + ' invEnd=' + Number(before.invEnd).toFixed(2) +
                ' damageRate=' + Number(before.damageRate).toFixed(3) +
                ' -> 0/0/1');
        }
        return before;
    }

    // ------------------------------------------------------------------
    // 爆炸类（手雷 / 榴弹 / RPG / 技能弹）的复活无敌穿透
    // ------------------------------------------------------------------
    //   WPN_GRENADE.CreateExplosion 是所有爆炸结算的公共入口（Msl_Arcane 等子类也走它）。
    //   IDA 反汇编的栈布局（cdecl，参数从 [esp+4] 起）：
    //     [esp+0x04] worldPos.x   [esp+0x08] y   [esp+0x0C] z
    //     [esp+0x10] damage       [esp+0x14] range
    //     [esp+0x18] distanceDecay  [esp+0x1C] ignoreWall(byte)
    //     [esp+0x20] DamageEventData（0x48 字节，按值）  <- +0x00 就是 attacker
    //     [esp+0x68] damageCallBack  [esp+0x6C] method
    //
    //   ★ 只有「这颗雷 / 这发 RPG 是我们自己扔的」（attacker == 本地玩家）才动手：
    //     Bot 的爆炸绝不代劳，否则人机会无视别人的复活保护。
    //   ★ 写操作仍然只有 clearDefenseBeforeShot 的那三个防御字段。
    var EXPLOSION_RANGE_MARGIN = 0.5;

    // 命中点是否落在爆炸半径内（多用 0.5m 余量：玩家坐标在脚底，爆炸判定的是胶囊体）
    function explosionTouchesTarget(worldPos, aimPoint, range) {
        var dx = aimPoint.x - worldPos.x;
        var dy = aimPoint.y - worldPos.y;
        var dz = aimPoint.z - worldPos.z;
        var d2 = dx * dx + dy * dy + dz * dz;
        var r = range + EXPLOSION_RANGE_MARGIN;
        return isFinite(d2) && d2 <= r * r;
    }

    function pierceExplosionDefense(attacker, worldPos, range) {
        if (!Runtime.config.pierce_respawn_invincible) return 0;
        if (!(range > 0 && range <= 50)) return 0;
        if (!worldPos || !isFinite(worldPos.x) || !isFinite(worldPos.y) || !isFinite(worldPos.z)) return 0;
        if (Math.abs(worldPos.x) > 10000 || Math.abs(worldPos.y) > 10000 || Math.abs(worldPos.z) > 10000) return 0;
        var myPlayer = getMyPlayer();
        if (isNull(myPlayer)) return 0;
        if (isNull(attacker) || !samePointer(attacker, myPlayer)) return 0;
        var gm = getGameManager();
        if (isNull(gm)) return 0;
        var players = getAllPlayers(gm);
        var myTeam = readTeam(myPlayer);
        var cleared = 0;
        for (var i = 0; i < players.length; i += 1) {
            var candidate = players[i];
            try {
                if (samePointer(candidate, myPlayer)) continue;
                if (!isEnemyTeam(myTeam, readTeam(candidate))) continue;
                if (isDeadEntity(candidate)) continue;
                var pos = getPlayerPos(candidate);
                if (!pos) continue;
                var aim = getAimPoint(candidate, pos) || pos;
                if (!explosionTouchesTarget(worldPos, aim, range)) continue;
                var before = clearDefenseBeforeShot(candidate);
                if (before && before.active) cleared += 1;
            } catch (_) {}
        }
        if (cleared > 0) {
            Runtime.stats.explosionDefenseCleared += cleared;
            if (probeBudget('pierceExplosion', 10)) {
                probe('pierceExplosion', '爆炸中心 ' + fmtVec(worldPos) + ' r=' + Number(range).toFixed(2) +
                    ' 已复位 ' + cleared + ' 个敌人的复活无敌（完全免疫）');
            }
        }
        return cleared;
    }

    function installExplosionDefenseHook() {
        registerAttach('WPN_GRENADE.CreateExplosion(defense-pierce)', RVA.WPN_GRENADE_CreateExplosion, {
            onEnter: function () {
                try {
                    Runtime.stats.explosionDefenseCalls += 1;
                    if (!Runtime.enabled || !Runtime.config.pierce_respawn_invincible) return;
                    var sp = this.context ? this.context.esp : null;
                    if (!sp) return;
                    var worldPos = {
                        x: sp.add(4).readFloat(),
                        y: sp.add(8).readFloat(),
                        z: sp.add(12).readFloat()
                    };
                    var range = sp.add(0x14).readFloat();
                    var eventPtr = sp.add(0x20).readPointer();
                    if (isNull(eventPtr) || !readable(eventPtr)) return;
                    var attacker = eventPtr.readPointer();
                    var me = getMyPlayer();
                    if (!isNull(me) && samePointer(attacker, me)) Runtime.cache.myExplosionAt = Date.now();
                    var cleared = pierceExplosionDefense(attacker, worldPos, range);
                    if (Runtime.cache.diagExp < 5) {
                        Runtime.cache.diagExp += 1;
                        log('info', '[diag:explosion] #' + Runtime.cache.diagExp +
                            ' pos=' + fmtVec(worldPos) + ' range=' + Number(range).toFixed(2) +
                            ' attacker=' + fmtPtr(attacker) + ' me=' + fmtPtr(Runtime.cache.ownPlayer) +
                            ' 复位=' + cleared);
                    }
                } catch (error) {
                    fail('CreateExplosion defense-pierce', error);
                }
            }
        });
    }
    // ------------------------------------------------------------------
    // 伤害入口兜底：不管伤害来自枪、爆炸还是技能，都在游戏应用伤害之前复位 victim
    // ------------------------------------------------------------------
    //   GameManager.TakeDamage(DamageEventData data) 是静态入口，DamageEventData 按值压栈：
    //     [esp+0x00] attacker   [esp+0x04] victim   [esp+0x08] damage
    //     [esp+0x34] type（Gun=1 / Knife=2 / Grenade=3 / Infect=4 / Other=5）
    //   ★ 只 attach：不 replace、不跳过原函数、不合成事件、不调用任何游戏函数。
    //     看到 attacker 是本地玩家就复位 victim 的防御状态，然后原函数原样跑完。

    function installTakeDamageDefenseHook() {
        registerAttach('GameManager.TakeDamage(defense-pierce)', RVA.GameManager_TakeDamage, {
            onEnter: function () {
                try {
                    Runtime.stats.takeDamageCalls += 1;
                    if (!Runtime.enabled || !Runtime.config.pierce_respawn_invincible) return;
                    var sp = this.context ? this.context.esp : null;
                    if (!sp) return;
                    var attacker = sp.readPointer();
                    if (isNull(attacker)) return;
                    var victim = sp.add(4).readPointer();
                    if (isNull(victim)) return;
                    var dmgType = sp.add(0x34).readS32();
                    var me = Runtime.cache.ownPlayer;
                    if (isNull(me)) {
                        me = getMyPlayer();
                        if (isNull(me)) return;
                    }
                    var mine = samePointer(attacker, me) && isLocalPlayer(attacker);
                    // 兜底归因：爆炸事件里的 attacker 万一不是 Player，
                    // 只要最近 250ms 内我们自己的爆炸入口刚跑过，就仍算我们的伤害。
                    if (!mine && dmgType === 3 && Runtime.cache.myExplosionAt &&
                        Date.now() - Runtime.cache.myExplosionAt <= 250) {
                        mine = true;
                    }
                    if (!mine) {
                        // 诊断：爆炸伤害却认不出是我们 —— 说明 attacker 不是 Player（或字段偏移不符）
                        if (dmgType === 3 && Runtime.cache.diagTdForeign < 3) {
                            Runtime.cache.diagTdForeign += 1;
                            log('info', '[diag:takeDamage] 爆炸伤害但 attacker 不是本地玩家: attacker=' +
                                fmtPtr(attacker) + ' me=' + fmtPtr(me) + ' victim=' + fmtPtr(victim));
                        }
                        return;
                    }
                    Runtime.stats.takeDamageOurs += 1;
                    if (samePointer(victim, me)) return;
                    if (isDeadEntity(victim)) return;
                    if (!isEnemyTeam(readTeam(me), readTeam(victim))) return;
                    var before = clearDefenseBeforeShot(victim);
                    if (before && before.active) {
                        Runtime.stats.takeDamageCleared += 1;
                    }
                    if (Runtime.cache.diagTd < 5) {
                        Runtime.cache.diagTd += 1;
                        log('info', '[diag:takeDamage] 我方伤害 type=' + dmgType + ' victim=' + fmtPtr(victim) +
                            ' 防御[invEnd=' + Number(before && before.invEnd).toFixed(2) +
                            ' rate=' + Number(before && before.damageRate).toFixed(3) +
                            ' inv=' + (before && before.isInvincible) +
                            ' ok=' + (before && before.ok) + ' active=' + (before && before.active) + ']');
                    }
                } catch (_) {}
            }
        });
    }
    // ------------------------------------------------------------------
    // 原生射线接管：把这一发的射线掰到目标身上
    // ------------------------------------------------------------------
    //   WPN_Gun.Damage(weapon, originX, originY, originZ, dirX, dirY, dirZ) 是 cdecl，
    //   参数压在栈上：arg0 在 [esp+4]，arg1..arg6 在 [esp+8]..[esp+0x1C]。
    //   在 onEnter 里改写 [esp+0x14]/[esp+0x18]/[esp+0x1C] 就等于改写了 rayDir ——
    //   原函数照常跑，命中判定 / 伤害 / DeathEventBroadcast / 复活调度全是游戏自己的代码。
    //
    //   返回 true  = 已改写 rayDir（调用方放行原函数，什么都不用做）
    //   返回 false = 没目标 / 参数不像射线 / 开关关着（调用方同样放行原函数，
    //                这一发就等于原版）
    //
    //   ★ 平时只写三个 float。唯一例外：pierce_respawn_invincible 开着时，
    //     在写完之后把「选中目标」的复活无敌（完全免疫）复位（clearDefenseBeforeShot），
    //     否则原版会把命中伤害按复活保护抹成 0。伤害数值、死亡广播、复活调度仍然一行都不动。
    // ------------------------------------------------------------------
    function redirectRayToTarget(ctx) {
        try {
            if (!Runtime.config.enable_guns) return false;
            if (!ctx || !ctx.context || !ctx.context.esp) return false;   // 离线单测没有 context
            var sp = ctx.context.esp;
            var sane = rayArgsLookSane(sp);
            if (!sane) {
                Runtime.stats.rayRedirectBadArgs += 1;
                if (!Runtime.cache.rayWarnLogged) {
                    Runtime.cache.rayWarnLogged = true;
                    log('warn', '[rayRedirect] WPN_Gun.Damage 的参数不像 (weapon, origin, dir)，' +
                        '这一发不接管（原版射线照原样跑）sp=' + fmtPtr(sp));
                }
                return false;
            }
            var myPlayer = getMyPlayer();
            if (isNull(myPlayer)) { Runtime.stats.rayRedirectSkip += 1; return false; }
            var rotation = readCameraRotation(myPlayer);
            if (!rotation) { Runtime.stats.rayRedirectSkip += 1; return false; }
            var eyePos = getLocalEyePos(myPlayer);
            var target = getSelectedTarget(myPlayer, eyePos || sane.origin, rotation);
            // 注意：**不在这里**加 noTarget —— selectTarget() 选不到目标时已经计过一次，
            // 两边都加会让同一发失败被算成两次（2026-10-15 实测 noTarget=156 实际只有 78 次失败）。
            if (!target || !target.pos) return false;

            // 起点用游戏自己的（枪口/相机位置不变，手感不变），只把方向掰到目标命中点
            var aim = target.pos;
            var vx = aim.x - sane.origin.x;
            var vy = aim.y - sane.origin.y;
            var vz = aim.z - sane.origin.z;
            var len = Math.sqrt(vx * vx + vy * vy + vz * vz);
            if (!isFinite(len) || len < 0.01) { Runtime.stats.rayRedirectSkip += 1; return false; }

            sp.add(20).writeFloat(vx / len);
            sp.add(24).writeFloat(vy / len);
            sp.add(28).writeFloat(vz / len);

            // 突破复活无敌：只复位"防御状态"，让紧接着执行的原函数能真的打掉血。
            // 不做任何"跳过原函数/补伤害/兜底复活"的动作。
            if (Runtime.config.pierce_respawn_invincible) {
                clearDefenseBeforeShot(target.player);
            }

            Runtime.stats.rayRedirectShots += 1;
            if (probeBudget('rayAim', 20)) {
                probe('rayAim', '接管射线 #' + Runtime.stats.rayRedirectShots +
                    ' -> ' + fmtPtr(target.player) + ' aim=' + fmtVec(aim) + ' dist=' + len.toFixed(2));
            }
            return true;
        } catch (error) {
            Runtime.stats.rayRedirectBadArgs += 1;
            fail('rayRedirect', error);
            return false;
        }
    }

    // ------------------------------------------------------------------
    // 爆炸物 / 技能弹的开火钩子：**只登记"要追踪"，绝不注入伤害**
    // ------------------------------------------------------------------
    //   这 5 个函数都是"本地武器开火"的那一步，args[0] 就是武器对象，
    //   所以能用 Weapon.get_isMyWeapon 过滤掉别人的开火。
    //   它们内部会同步调用 Weapon.ProjectMissile -> 回调 -> SetWeaponData，
    //   所以在 onEnter 里写一条 Runtime.pendingMissile，SetWeaponData 立刻就能读到。
    //
    //   为什么不做直伤（重要）：
    //     原版投射物本来就会在命中时用 WPN_GRENADE.CreateExplosion 结算范围伤害，
    //     伤害数值、爆炸半径、距离衰减、wpnIndex、击杀归属全都是对的。
    //     再注入一份直伤 = 打两遍 + 绕过爆炸范围判定，既多余又破坏手感。
    //     需求是"弹体能追着敌人拐弯"，那就只做追踪，伤害交给原版。
    function installExplosiveHooks() {
        registerAttach('WPN_RPG.Fire', RVA.WPN_RPG_Fire, {
            onEnter: function (args) {
                handleTrigger(args[0], CATEGORY.EXPLOSIVE, 'rpg', OFF.WD_RPG_missileData);
            }
        });
        registerAttach('WPN_Throw.Throw', RVA.WPN_Throw_Throw, {
            onEnter: function (args) {
                handleTrigger(args[0], CATEGORY.EXPLOSIVE, 'throw', OFF.WD_Missile_missileData);
            }
        });
        registerAttach('WPN_GrenadeGun.b__19_0', RVA.WPN_GrenadeGun_GunShootFunction_Lambda, {
            onEnter: function (args) {
                handleTrigger(args[0], CATEGORY.EXPLOSIVE, 'grenade_gun', OFF.WD_GrenadeGun_missileData);
            }
        });
    }

    // 特殊技能弹：奥术手雷 / 地狱终结者火球
    function installSkillHooks() {
        registerAttach('WPN_Arcane.Throw', RVA.WPN_Arcane_Throw, {
            onEnter: function (args) {
                handleTrigger(args[0], CATEGORY.SKILL, 'arcane', OFF.WD_Missile_missileData);
            }
        });
        registerAttach('WPN_EvilTerminator.ThrowFireBall', RVA.WPN_EvilTerminator_ThrowFireBall, {
            onEnter: function (args) {
                handleTrigger(args[0], CATEGORY.SKILL, 'evil_terminator', OFF.WD_EvilTerminator_missileData);
            }
        });
    }

    // 类别子开关：爆炸物 / 技能弹各自独立，都还要过 enable_homing 总开关。
    function isCategoryHomingOn(category) {
        if (!Runtime.config.enable_homing) return false;
        if (category === CATEGORY.SKILL) return Runtime.config.enable_skill_projectiles;
        return Runtime.config.enable_explosives;
    }

    // 注意：这里**故意不检查开关**。开关只在登记时（armMissileHoming）判定，
    // 这样 [probe:trig] / trig 计数永远代表"开火钩子有没有命中"，
    // 不会因为开关关着就变成 0 而让人误判成 RVA 不匹配。
    function handleTrigger(weapon, category, sourceLabel, missileDataOffset) {
        if (!Runtime.enabled) return;
        try {
            if (!isLocalWeapon(weapon)) {
                if (probeBudget('trigRemote', 3)) {
                    probe('trigRemote', sourceLabel + ': not my weapon ' + fmtPtr(weapon));
                }
                return;
            }
            if (category === CATEGORY.SKILL) {
                Runtime.stats.skillTriggers += 1;
            } else {
                Runtime.stats.explosiveTriggers += 1;
            }
            // 只记录"这颗弹属于哪个类别"，真正的制导登记在 SetWeaponData 里做。
            // missileDataOffset 只用于日志（原生弹体伤害，纯参考，**不注入**）。
            Runtime.pendingMissile = {
                category: category,
                label: sourceLabel,
                at: Date.now()
            };
            var damage = readMissileDamage(weapon, missileDataOffset);
            probe('trig', sourceLabel + ' weapon=' + fmtPtr(weapon) +
                ' 原生弹体伤害=' + damage.toFixed(2) + '（只记录，不注入）' +
                ' category=' + category);
        } catch (error) {
            fail('handleTrigger:' + sourceLabel, error);
        }
    }
    function logHookAudit() {
        try {
            var list = [
                ['WPN_Gun.Damage', RVA.WPN_Gun_Damage],
                ['WPN_RPG.Fire', RVA.WPN_RPG_Fire],
                ['WPN_Throw.Throw', RVA.WPN_Throw_Throw],
                ['WPN_GrenadeGun.lambda', RVA.WPN_GrenadeGun_GunShootFunction_Lambda],
                ['WPN_Arcane.Throw', RVA.WPN_Arcane_Throw],
                ['WPN_EvilTerminator.ThrowFireBall', RVA.WPN_EvilTerminator_ThrowFireBall],
                // ---- 弹体追踪（制导）----
                // 这一组只要出现 NOT EXECUTABLE，追踪就一定不生效，
                // 所以全部列进审计，方便一眼区分"版本不匹配"和"逻辑没走到"。
                ['Weapon.ProjectMissile', RVA.Weapon_ProjectMissile],
                ['WPN_Missile.SetWeaponData', RVA.WPN_Missile_SetWeaponData],
                ['WPN_Missile.FixedUpdate', RVA.WPN_Missile_FixedUpdate],
                ['WPN_Missile.Work', RVA.WPN_Missile_Work],
                ['WPN_GRENADE.Work', RVA.WPN_GRENADE_Work],
                ['WPN_Missile.Recycle', RVA.WPN_Missile_Recycle],
                ['WPN_Missile.OnCollisionEnter', RVA.WPN_Missile_OnCollisionEnter],
                ['WPN_GRENADE.OnCollisionEnter', RVA.WPN_GRENADE_OnCollisionEnter],
                ['WPN_GRENADE.OnTriggerEnter', RVA.WPN_GRENADE_OnTriggerEnter],
                ['RecyclableObject.Recycle', RVA.RecyclableObject_Recycle],
                ['Rigidbody.get_velocity', RVA.Rigidbody_get_velocity_Injected],
                ['Rigidbody.set_velocity', RVA.Rigidbody_set_velocity]
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
                ' attaches=' + Runtime.attachHooks.length);
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
                log('info', '[probe:beat] gun: calls=' + s.gunDamageCalls +
                    ' hookFired=' + (s.gunDamageCalls > 0 ? 'YES' : 'NO') +
                    ' localFires=' + s.localGunFires +
                    ' rayRedirect=' + s.rayRedirectShots +
                    ' badArgs=' + s.rayRedirectBadArgs +
                    ' skip=' + s.rayRedirectSkip +
                    ' noTarget=' + s.noTarget +
                    ' selected=' + s.targetsSelected +
                    ' lockReason=' + s.targetLockReason + ' switches=' + s.targetSwitchCount +
                    ' passthrough(remote)=' + s.skippedRemote +
                    ' errors=' + s.errorCount + ' lastError=' + (s.lastError || '-'));
                // 弹体追踪单独一行，方便一眼判断"追踪到底卡在哪一步"：
                //   trig     = 开火钩子命中（爆炸物+技能弹）
                //   spawn    = SetWeaponData 命中（= 观察到几颗弹生成）
                //   launch   = Work() 命中（弹体真的被激活发射）
                //   arm      = 自己的弹登记成功（**追踪是否生效看这个**）
                //   steer    = 实际改写了速度（拐弯次数）
                //   notMine / noPending / off / noTarget = arm 没涨的原因
                log('info', '[probe:beat] missile: trig=' + (s.explosiveTriggers + s.skillTriggers) +
                    '(爆炸=' + s.explosiveTriggers + '/技能=' + s.skillTriggers + ')' +
                    ' spawn=' + s.missileSpawns + ' launch=' + s.missileLaunchSeen +
                    ' arm=' + s.homingArmed + ' steer=' + s.homingSteered +
                    ' tracked=' + Object.keys(Runtime.missileTargets).length +
                    ' | notMine=' + s.missileNotMine + ' noPending=' + s.missileNoPending +
                    ' off=' + s.missileSwitchOff + ' noTarget=' + s.missileNoTarget +
                    ' fu=' + s.fixedUpdateCalls + ' wrote=' + s.steerWrote +
                    ' drop=' + s.homingDropped + ' forget=' + s.homingForgotten);
                // 第二行：steer 为什么没写进去 / 记录是被谁清掉的 / 弹体撞了什么
                log('info', '[probe:beat] missile2: skip[off=' + s.steerOff +
                    ' noEntry=' + s.steerNoEntry + ' noPos=' + s.steerNoPos +
                    ' noAim=' + s.steerNoAim + ' close=' + s.steerTooClose +
                    ' writeSkip=' + s.steerWriteSkip + ' lostTarget=' + s.steerLostTarget + ']' +
                    ' forget[reuse=' + s.forgetReuse + ' recycle=' + s.forgetRecycle +
                    ' timeout=' + s.forgetTimeout +
                    ' lost=' + s.forgetLost +
                    ' ident=' + s.forgetIdentity + ']' +
                    ' touch[hit=' + s.missileHitSeen + ' trig=' + s.missileTriggerSeen + ']' +
                    ' cone[命中=' + s.coneHit + ' 锥内空=' + s.coneEmpty +
                    ' 回退=' + s.coneFallback + ' 严格放弃=' + s.coneEmptyStrict +
                    ' 关=' + s.coneOff + ' 轴失败=' + s.coneAxisFail +
                    ' 换目标=' + s.coneRetarget + ']');
                // ★ 本版本**不观察死亡与复活**。目标死了有没有复活、复活计时被谁重置，
                //   全部是游戏自己的事 —— 我们既不读也不写。
                // 顺手清理超时的弹体追踪记录：万一某颗弹没触发 Recycle/碰撞就消失，
                // 记录会一直留着；指针被复用后可能"打错人"。
                try {
                    var nowMs = Date.now();
                    var keys = Object.keys(Runtime.missileTargets);
                    for (var i = 0; i < keys.length; i += 1) {
                        if (nowMs - Runtime.missileTargets[keys[i]].at > Runtime.config.homing_max_ms) {
                            delete Runtime.missileTargets[keys[i]];
                            Runtime.stats.homingDropped += 1;
                        }
                    }
                } catch (_) {}

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

    // ------------------------------------------------------------------
    // 敌人扫描（弹体追踪的"打谁"基础）
    // ------------------------------------------------------------------
    //   与 selectTarget（枪械直伤）的区别：**不做任何视线判定**，
    //   敌我判定只保留两条硬规则：**敌对阵营 + 存活**，永远不打自己人。
    //
    //   scanEnemies(from, axis, policy) 一次扫完：
    //     allCandidates = 所有通过硬过滤的敌人（用于近距/全场回退）
    //     coneCandidates = 外锥内的敌人
    //     bestCone = 内锥优先 + 角度优先 + 距离 tiebreak 选出的目标
    //     bestAny  = 全场最近（仅用于回退）
    //
    //   axis = { yawDeg, pitchDeg }；policy = targetPolicy()。
    //   夹角算法与枪械直伤完全一致，所以"准星锥"在三条路径上的含义不会漂移。
    function scanEnemies(from, axis, policy) {
        var result = {
            bestCone: null,
            bestAny: null,
            allCandidates: [],
            coneCandidates: [],
            enemies: 0,
            inCone: 0,
            nearestAngle: -1,
            usedCone: !!(axis && policy && policy.outerConeDeg > 0)
        };
        if (!from) return result;
        var me = getMyPlayer();
        if (isNull(me)) return result;
        var gm = getGameManager();
        if (isNull(gm)) return result;
        var players = getAllPlayers(gm);
        var myTeam = readTeam(me);
        for (var i = 0; i < players.length; i += 1) {
            var candidate = players[i];
            try {
                if (samePointer(candidate, me)) continue;
                if (!isEnemyTeam(myTeam, readTeam(candidate))) continue;
                if (isDeadEntity(candidate)) continue;
                var pos = getPlayerPos(candidate);
                if (!pos) continue;
                var aim = getAimPoint(candidate, pos) || pos;
                var dx = aim.x - from.x, dy = aim.y - from.y, dz = aim.z - from.z;
                var dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
                result.enemies += 1;

                var ang = -1;
                if (result.usedCone) {
                    var angles = calculateTargetAngles(from, aim);
                    if (angles) {
                        var a = angleDistanceDeg(angles.targetYawDeg, angles.targetPitchDeg,
                            axis.yawDeg, axis.pitchDeg);
                        if (isFinite(a)) ang = a;
                    }
                }

                var entry = { player: candidate, dist: dist, angleDeg: ang };
                result.allCandidates.push(entry);
                if (result.bestAny === null || dist < result.bestAny.dist) {
                    result.bestAny = entry;
                    // nearestAngle = 全场最近的那个敌人的夹角（不是最小夹角）。
                    // 锥空时看它：若在 90° 以上，说明你是背对着最近的人，不是锥开小了。
                    if (result.usedCone) result.nearestAngle = ang;
                }

                if (!result.usedCone) {
                    result.inCone += 1;
                    result.coneCandidates.push(entry);
                    continue;
                }
                if (ang < 0 || ang > policy.outerConeDeg) continue;
                result.inCone += 1;
                result.coneCandidates.push(entry);
            } catch (_) {}
        }
        if (result.usedCone) {
            result.bestCone = pickBestCandidate(
                result.coneCandidates,
                policy.innerConeDeg,
                policy.angleTieDeg
            );
        } else {
            result.bestCone = result.bestAny;
        }
        return result;
    }

    // 纯"全场最近"（不启用准星锥）。
    function pickNearestEnemyFrom(from) {
        return scanEnemies(from, null, targetPolicy()).bestAny;
    }

    // ------------------------------------------------------------------
    // 弹体追踪的"打谁"策略：与外锥/内锥/角度排序完全同一套
    // ------------------------------------------------------------------
    //   发射时（armMissileHoming 调用）：
    //     锥轴 = 本地玩家相机朝向（readCameraRotation）
    //     锥心 = 眼睛位置（getLocalEyePos）—— 准星锥必须从眼睛量
    //   锥内有人 -> 取内锥优先、角度优先的那个；锥内没人 -> 按配置回退
    //   锥内没人 -> missile_fallback_nearest：
    //       true （默认）= 回退"全场最近"（可再用 max_distance 限制近距），
    //                       保住"对着空气扔雷也能追到人"；
    //       false        = 返回 null，这颗弹不追踪、按原弹道直飞。
    //   外锥 0 = 完全关闭锥（调试用），退回全场最近。
    function pickEnemyForLaunch() {
        var me = getMyPlayer();
        if (isNull(me)) return null;
        var eye = getLocalEyePos(me);
        if (!eye) return null;
        var policy = targetPolicy();

        if (!(policy.outerConeDeg > 0)) {
            Runtime.stats.coneOff += 1;
            return scanEnemies(eye, null, policy).bestAny;
        }
        var rot = readCameraRotation(me);
        if (!rot) {
            // 读不到相机朝向：宁可"追最近的"也不要完全不追
            Runtime.stats.coneAxisFail += 1;
            return scanEnemies(eye, null, policy).bestAny;
        }
        var scan = scanEnemies(eye, { yawDeg: rot.yawDeg, pitchDeg: rot.pitchDeg }, policy);
        if (scan.bestCone) {
            Runtime.stats.coneHit += 1;
            if (probeBudget('homingCone', 20)) {
                probe('homingCone', 'LAUNCH 锥内命中 target=' + fmtPtr(scan.bestCone.player) +
                    ' angle=' + scan.bestCone.angleDeg.toFixed(1) + '/' + policy.outerConeDeg.toFixed(0) + 'deg' +
                    ' dist=' + scan.bestCone.dist.toFixed(1) +
                    ' 锥内候选=' + scan.inCone + '/' + scan.enemies +
                    ' inner=' + policy.innerConeDeg.toFixed(1) + 'deg');
            }
            return scan.bestCone;
        }
        Runtime.stats.coneEmpty += 1;
        if (!Runtime.config.missile_fallback_nearest) {
            Runtime.stats.coneEmptyStrict += 1;
            probe('homingCone', 'LAUNCH 锥内无敌人 + 已关闭回退 -> 这颗弹不追踪' +
                ' 全场敌人=' + scan.enemies +
                ' 最近夹角=' + (scan.nearestAngle < 0 ? '-' : scan.nearestAngle.toFixed(1)) +
                ' (outer=' + policy.outerConeDeg.toFixed(0) + 'deg)');
            return null;
        }
        var fallback = pickNearestCandidate(scan.allCandidates, Runtime.config.missile_fallback_max_distance);
        if (!fallback) {
            Runtime.stats.coneEmptyStrict += 1;
            return null;
        }
        Runtime.stats.coneFallback += 1;
        probe('homingCone', 'LAUNCH 锥内无敌人 -> 回退最近' +
            ' 全场敌人=' + scan.enemies +
            ' 最近夹角=' + (scan.nearestAngle < 0 ? '-' : scan.nearestAngle.toFixed(1)) +
            ' (outer=' + policy.outerConeDeg.toFixed(0) + 'deg)');
        return fallback;
    }

    // 弹体飞行途中换目标（原目标死亡/读不到时）：
    //   锥轴 = 弹体当前速度方向（"继续朝前找"），锥心 = 弹体当前位置。
    //   用速度而不是玩家准星的理由：
    //     1) 弹体已经飞出去了，玩家可能早就看别处，用玩家准星会让弹体突然大幅掉头；
    //     2) 用速度天然避免弹体在半空 180° 掉头，飞行观感更自然。
    //   排序仍用同一套：内锥优先 -> 角度优先 -> 距离 tiebreak。
    function pickEnemyForMissileRetarget(mpos, rb) {
        if (!mpos) return null;
        var policy = targetPolicy();
        if (!(policy.outerConeDeg > 0)) {
            Runtime.stats.coneOff += 1;
            return scanEnemies(mpos, null, policy).bestAny;
        }
        var v = readRigidbodyVelocity(rb);
        var vlen = v ? Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z) : 0;
        if (!(vlen > 0.01)) {
            // 读不到速度（刚出膛/已停住）：退回全场最近
            Runtime.stats.coneAxisFail += 1;
            return scanEnemies(mpos, null, policy).bestAny;
        }
        var hDist = Math.sqrt(v.x * v.x + v.z * v.z);
        if (hDist < 0.01) hDist = 0.01;
        var scan = scanEnemies(mpos, {
            yawDeg: Math.atan2(v.x, v.z) * 180.0 / Math.PI,
            pitchDeg: Math.atan2(v.y, hDist) * 180.0 / Math.PI
        }, policy);
        if (scan.bestCone) {
            Runtime.stats.coneHit += 1;
            Runtime.stats.coneRetarget += 1;
            if (probeBudget('homingCone', 30)) {
                probe('homingCone', 'RETARGET 锥内命中 target=' + fmtPtr(scan.bestCone.player) +
                    ' angle=' + scan.bestCone.angleDeg.toFixed(1) + '/' + policy.outerConeDeg.toFixed(0) + 'deg' +
                    ' dist=' + scan.bestCone.dist.toFixed(1) +
                    ' 锥内候选=' + scan.inCone + '/' + scan.enemies +
                    ' inner=' + policy.innerConeDeg.toFixed(1) + 'deg');
            }
            return scan.bestCone;
        }
        Runtime.stats.coneEmpty += 1;
        if (!Runtime.config.missile_fallback_nearest) {
            Runtime.stats.coneEmptyStrict += 1;
            return null;
        }
        var fallback = pickNearestCandidate(scan.allCandidates, Runtime.config.missile_fallback_max_distance);
        if (!fallback) {
            Runtime.stats.coneEmptyStrict += 1;
            return null;
        }
        Runtime.stats.coneFallback += 1;
        Runtime.stats.coneRetarget += 1;
        return fallback;
    }

    // float -> u32 位模式（按值 struct 压栈时用）
    function floatToU32(value) {
        try {
            if (!Runtime.cache.floatBuf) Runtime.cache.floatBuf = Memory.alloc(4);
            Runtime.cache.floatBuf.writeFloat(value);
            return Runtime.cache.floatBuf.readU32();
        } catch (_) { return 0; }
    }

    // ------------------------------------------------------------------
    // 弹体追踪（制导）：让弹体朝敌人拐弯
    // ------------------------------------------------------------------
    //   完整设计见文件头"设计说明四"。实现要点：
    //     1) 登记（arm）：WPN_Missile.SetWeaponData 是 ProjectMissile 回调里
    //        被调用的那一步 —— owner 已经写好、弹体还没 Active() 发射。
    //        用 owner 判定"是不是自己发射的"，用 Runtime.pendingMissile 判定类别。
    //        **每次进入都先无条件清掉该指针的旧记录**（对象池复用防串味：
    //        否则敌人捡到同一颗弹，会被我们掰到自己的目标上）。
    //     2) 拐弯（steer）：WPN_Missile.FixedUpdate 的 onLeave —— 物理步末尾，
    //        游戏自己刚 AddForce(extraGravity) 完，此时改写 velocity 立刻生效。
    //     3) 清理：Recycle / OnCollisionEnter（基类 + 手雷重写的那个）/
    //        OnTriggerEnter 都要清，防止指针被复用后"打错人"。
    //     4) 兜底：心跳里按 homing_max_ms 清超时记录。

    // 读 Rigidbody.velocity（Injected 版本，out Vector3*，避免按值返回 struct）
    function readRigidbodyVelocity(rb) {
        if (!readable(rb) || !native.getVelocity || !Runtime.cache.posBuf) return null;
        try {
            var buffer = Runtime.cache.posBuf;
            native.getVelocity(rb, buffer, ptr(0));
            var v = { x: buffer.readFloat(), y: buffer.add(4).readFloat(), z: buffer.add(8).readFloat() };
            if (!isFinite(v.x) || !isFinite(v.y) || !isFinite(v.z)) return null;
            return v;
        } catch (_) { return null; }
    }

    // 记录被清掉的原因分布。排查「只拐了 1 次就不拐了」时看这一组计数：
    // 哪个字段大，就说明记录是被哪条路径清掉的。
    function countForgetReason(why) {
        var s = Runtime.stats;
        if (why === 'reused') s.forgetReuse += 1;
        else if (why === 'recycle') s.forgetRecycle += 1;
        else if (why === 'timeout') s.forgetTimeout += 1;
        else if (why === 'target-lost') s.forgetLost += 1;
        else if (why === 'identity') s.forgetIdentity += 1;
    }

    // 清掉某颗弹的制导记录（回池 / 被复用 / 超时 / 身份不符都走这里）
    function forgetMissile(missile, why) {
        try {
            if (!missile || isNull(missile)) return false;
            var key = missile.toString();
            if (!Runtime.missileTargets[key]) return false;
            delete Runtime.missileTargets[key];
            Runtime.stats.homingForgotten += 1;
            countForgetReason(why);
            if (why && probeBudget('missileForget', 12)) {
                probe('missileForget', fmtPtr(missile) + ' ' + why);
            }
            return true;
        } catch (_) { return false; }
    }

    // 登记：这颗弹是不是"我们发射的 + 该类别追踪开着"
    function armMissileHoming(missile) {
        try {
            if (isNull(missile)) return;
            // 对象池会复用指针：先无条件清掉旧记录，再决定要不要重新登记
            forgetMissile(missile, 'reused');
            if (!Runtime.enabled) return;
            // 计数放在开关判定之前："弹生成"是事实，和开关无关，
            // 这样排查时 spawn=0 就一定代表 SetWeaponData 钩子没命中。
            Runtime.stats.missileSpawns += 1;

            var owner = missile.add(OFF.Missile_owner).readPointer();
            if (!isLocalPlayer(owner)) {
                Runtime.stats.missileNotMine += 1;
                if (probeBudget('missileNotMine', 6)) {
                    probe('missileNotMine', 'missile=' + fmtPtr(missile) + ' owner=' + fmtPtr(owner) +
                        '（别人发射的，不制导）');
                }
                return;
            }
            // 配对：开火钩子（同一次调用栈里）刚写的类别记录
            var pending = Runtime.pendingMissile;
            Runtime.pendingMissile = null;
            if (!pending || (Date.now() - pending.at) > Runtime.config.homing_pending_ms) {
                Runtime.stats.missileNoPending += 1;
                if (probeBudget('missileNoPending', 6)) {
                    probe('missileNoPending', 'missile=' + fmtPtr(missile) + ' owner=' + fmtPtr(owner) +
                        ' pending=' + (pending ? pending.label : 'null') +
                        ' | 开火钩子没命中（查 [probe:trig] / [probe:rva]）');
                }
                return;
            }
            if (!isCategoryHomingOn(pending.category)) {
                Runtime.stats.missileSwitchOff += 1;
                return;
            }
            var best = pickEnemyForLaunch();
            if (!best) {
                Runtime.stats.missileNoTarget += 1;
                if (probeBudget('missileNoTarget', 6)) {
                    probe('missileNoTarget', 'missile=' + fmtPtr(missile) + ' 场上没有可选敌人');
                }
                return;
            }
            Runtime.missileTargets[missile.toString()] = {
                target: best.player,
                at: Date.now(),
                category: pending.category,
                label: pending.label,
                // 身份指纹：对象池会把同一个指针发给下一颗弹，指针相同不代表还是同一颗。
                // 每次拐弯前重新读一遍 owner + rigidBody，不一致就说明槽位换人了，
                // 立刻丢掉记录，避免「上一颗弹的记录把别人发射的弹拐走」。
                owner: owner,
                rb: missile.add(OFF.Missile_rigidBody).readPointer(),
                steers: 0
            };
            Runtime.stats.homingArmed += 1;
            probe('missileArm', 'ARM missile=' + fmtPtr(missile) + ' owner=' + fmtPtr(owner) +
                ' target=' + fmtPtr(best.player) + ' dist=' + best.dist.toFixed(1) +
                ' angle=' + (best.angleDeg >= 0 ? best.angleDeg.toFixed(1) : '-') +
                ' outer=' + Runtime.config.target_outer_cone_deg.toFixed(0) + 'deg' +
                ' inner=' + Runtime.config.target_inner_cone_deg.toFixed(0) + 'deg' +
                ' category=' + pending.category + ' via=' + pending.label +
                ' wpnData=' + fmtPtr(missile.add(OFF.Missile_weaponData).readPointer()));
        } catch (error) { fail('armMissileHoming', error); }
    }
    function steerMissile(missile) {
        // 每一次提前返回都记一个计数。排查「弹体不拐弯」时先看 [probe:beat] missile2 那行：
        //   noEntry 大  -> 记录被清掉了（看 forget[...] 是谁清的）
        //   noPos/noAim -> 读不到位置，属于数据取用问题
        //   wrote 不涨  -> 写速度那一步被跳过了（rb 不可读 / native 缺失）
        if (!Runtime.enabled || !Runtime.config.enable_homing) {
            Runtime.stats.steerOff += 1;
            return;
        }
        if (isNull(missile)) return;
        var key = missile.toString();
        var entry = Runtime.missileTargets[key];
        if (!entry) {
            Runtime.stats.steerNoEntry += 1;
            return;
        }
        // 身份校验：对象池复用会让同一个指针变成另一颗弹，必须先验 owner + rigidBody。
        try {
            if (entry.owner !== undefined) {
                var nowOwner = missile.add(OFF.Missile_owner).readPointer();
                var nowRb = missile.add(OFF.Missile_rigidBody).readPointer();
                if (!samePointer(nowOwner, entry.owner) || !samePointer(nowRb, entry.rb)) {
                    forgetMissile(missile, 'identity');
                    return;
                }
            }
        } catch (_) {}
        var nowMs = Date.now();
        if (nowMs - entry.at > Runtime.config.homing_max_ms) {
            forgetMissile(missile, 'timeout');
            Runtime.stats.homingDropped += 1;
            return;
        }
        // 先拿弹体位置：换目标时以"弹体当前位置"为参考点才算真的就近
        var transform = native.getTransform(missile, ptr(0));
        var mpos = readTransformPosition(transform);
        if (!mpos) { Runtime.stats.steerNoPos += 1; return; }

        var target = entry.target;
        if (!readable(target) || isDeadEntity(target)) {
            if (!Runtime.config.homing_retarget) {
                forgetMissile(missile, 'target-lost');
                Runtime.stats.homingDropped += 1;
                return;
            }
            var next = pickEnemyForMissileRetarget(
                mpos, missile.add(OFF.Missile_rigidBody).readPointer());
            if (!next) {
                // 这一刻没有可选目标：不清记录，让它先按原弹道飞。
                // 清掉的话这颗弹就永远直飞了；留着还有机会等到新目标，
                // 真正的兜底是 homing_max_ms 超时 + 回池时的 Recycle。
                Runtime.stats.steerLostTarget += 1;
                return;
            }
            entry.target = next.player;
            // 注意：不改 entry.at —— 它代表"这颗弹的出生时间"，
            // 用来算 homing_max_ms 总时限（换目标不应该续命）。
            target = next.player;
            if (probeBudget('homingRetarget', 10)) {
                probe('homingRetarget', 'missile=' + fmtPtr(missile) + ' -> ' + fmtPtr(target) +
                    ' dist=' + next.dist.toFixed(1));
            }
        }
        var aim = getAimPoint(target, getPlayerPos(target));
        if (!aim) { Runtime.stats.steerNoAim += 1; return; }
        var dx = aim.x - mpos.x, dy = aim.y - mpos.y, dz = aim.z - mpos.z;
        var len = Math.sqrt(dx * dx + dy * dy + dz * dz);
        if (len < 0.25) { Runtime.stats.steerTooClose += 1; return; }   // 已经贴脸：交给原版碰撞判定
        var speed = Runtime.config.homing_speed > 0
            ? Runtime.config.homing_speed
            : readFloatSafe(missile.add(OFF.Missile_shootSpeed));
        if (!(speed > 0) || speed > 500) speed = 30;
        var ux = dx / len, uy = dy / len, uz = dz / len;

        // 方向插值：homing_turn = 1 时就是"直接锁定目标方向"（命中率最高）。
        // 留这个旋钮是为了手感可选：调小一点，弹体会先保留一段原弹道再慢慢拐，
        // 视觉上更接近"会拐弯的抛物线"。
        var turn = clampFloat(Runtime.config.homing_turn, 0.05, 1);
        if (turn < 1) {
            var v = readRigidbodyVelocity(missile.add(OFF.Missile_rigidBody).readPointer());
            if (v) {
                var vlen = Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
                if (vlen > 0.01) {
                    var bx = (v.x / vlen) * (1 - turn) + ux * turn;
                    var by = (v.y / vlen) * (1 - turn) + uy * turn;
                    var bz = (v.z / vlen) * (1 - turn) + uz * turn;
                    var blen = Math.sqrt(bx * bx + by * by + bz * bz);
                    if (blen > 0.0001) { ux = bx / blen; uy = by / blen; uz = bz / blen; }
                }
            }
        }

        var rb = missile.add(OFF.Missile_rigidBody).readPointer();
        if (readable(rb) && native.setVelocity) {
            native.setVelocity(rb,
                floatToU32(ux * speed), floatToU32(uy * speed), floatToU32(uz * speed), ptr(0));
            Runtime.stats.steerWrote += 1;
        } else {
            Runtime.stats.steerWriteSkip += 1;
        }
        // 朝向也掰过去：弹头视觉朝前，同时兼容"用 transform.forward 推位移"的写法
        if (readable(transform) && native.lookRotation && native.setRotation && Runtime.cache.quatBuf) {
            native.lookRotation(Runtime.cache.quatBuf,
                floatToU32(ux), floatToU32(uy), floatToU32(uz), ptr(0));
            native.setRotation(transform,
                Runtime.cache.quatBuf.readU32(),
                Runtime.cache.quatBuf.add(4).readU32(),
                Runtime.cache.quatBuf.add(8).readU32(),
                Runtime.cache.quatBuf.add(12).readU32(),
                ptr(0));
        }
        Runtime.stats.homingSteered += 1;
        entry.steers = (entry.steers || 0) + 1;
        // 每颗弹的前 3 次拐弯把「弹体位置 + 写进去的速度 + 立刻读回来的速度」一起打出来。
        //   vReadBack 约等于 vWritten -> 速度写进去了，游戏也认（还是直飞就要看别处）
        //   vReadBack 和 vWritten 差很远 -> 游戏在覆盖我们的速度（说明弹体有别的驱动）
        if (entry.steers <= 3) {
            var vRead = readRigidbodyVelocity(rb);
            probe('homingSteer#' + entry.steers, 'missile=' + fmtPtr(missile) +
                ' mpos=' + fmtVec(mpos) + ' -> target=' + fmtPtr(target) +
                ' dist=' + len.toFixed(1) + ' speed=' + speed.toFixed(1) +
                ' turn=' + turn.toFixed(2) + ' cat=' + entry.category + ' rb=' + fmtPtr(rb) +
                ' vWritten=' + fmtVec({ x: ux * speed, y: uy * speed, z: uz * speed }) +
                ' vReadBack=' + (vRead ? fmtVec(vRead) : 'null'));
        }
    }

    function installHomingHooks() {
        // 登记点：ProjectMissile 的回调。5 种投射物（RPG / 手雷 / 榴弹枪 /
        // 奥术手雷 / 地狱终结者火球）全部会走到这里，所以一个钩子就够。
        registerProbeAttach('WPN_Missile.SetWeaponData(homing)', RVA.WPN_Missile_SetWeaponData, {
            onEnter: function (args) { armMissileHoming(args[0]); }
        });

        // FixedUpdate 的 onLeave：确保在游戏自己算完速度（AddForce extraGravity）之后再改写
        registerProbeAttach('WPN_Missile.FixedUpdate(homing)', RVA.WPN_Missile_FixedUpdate, {
            onEnter: function (args) {
                Runtime.stats.fixedUpdateCalls += 1;
                this.missile = args[0];
            },
            onLeave: function () {
                try { steerMissile(this.missile); } catch (error) { fail('homing.FixedUpdate', error); }
            }
        });

        // 发射（Work）：游戏在这里设初速 velocity = transform.forward * shootSpeed。
        // 调用顺序是 SetWeaponData（我们登记）-> Active() -> Work()，
        // 也就是说游戏会在我们之后把速度覆盖掉。
        // 所以 onLeave（游戏写完初速之后）立刻补一次制导，保证第一帧就朝目标。
        var workEnter = function (args) {
            Runtime.stats.missileLaunchSeen += 1;
            this.missile = args[0];
        };
        var workLeave = function () {
            try { steerMissile(this.missile); } catch (error) { fail('homing.Work', error); }
        };
        registerProbeAttach('WPN_Missile.Work(homing)', RVA.WPN_Missile_Work, {
            onEnter: workEnter, onLeave: workLeave
        });
        registerProbeAttach('WPN_GRENADE.Work(homing)', RVA.WPN_GRENADE_Work, {
            onEnter: workEnter, onLeave: workLeave
        });

        // 清理：只在「这颗弹真的回对象池了」的时候删记录。
        //
        // 早期版本把 OnCollisionEnter / OnTriggerEnter 也当成清理点，结果弹体一碰到
        // 任何东西（包括刚出膛时重叠到的碰撞体）记录就被删掉，制导只生效了 1 帧，
        // 之后整段飞行都是原版直线 —— 表现就是「完全不拐弯」。
        // 爆炸 / 命中本来就会走到 Recycle，所以只挂 Recycle 就够了；
        // 万一有漏网的，armMissileHoming 里的 reused 和 steerMissile 里的身份校验
        // 都会把过期记录清掉，不会拐错弹。
        registerProbeAttach('WPN_Missile.Recycle(homing)', RVA.WPN_Missile_Recycle, {
            onEnter: function (args) { forgetMissile(args[0], 'recycle'); }
        });
        registerProbeAttach('RecyclableObject.Recycle(homing)', RVA.RecyclableObject_Recycle, {
            onEnter: function (args) { forgetMissile(args[0], 'recycle'); }
        });
        // 碰撞 / 触发只记账，不再删记录（保留探针，方便确认弹体到底撞了什么）。
        registerProbeAttach('WPN_Missile.OnCollisionEnter(homing)', RVA.WPN_Missile_OnCollisionEnter, {
            onEnter: function (args) {
                Runtime.stats.missileHitSeen += 1;
                if (probeBudget('missileHit', 6)) probe('missileHit', fmtPtr(args[0]) + ' WPN_Missile.OnCollisionEnter');
            }
        });
        registerProbeAttach('WPN_GRENADE.OnCollisionEnter(homing)', RVA.WPN_GRENADE_OnCollisionEnter, {
            onEnter: function (args) {
                Runtime.stats.missileHitSeen += 1;
                if (probeBudget('missileHit', 6)) probe('missileHit', fmtPtr(args[0]) + ' WPN_GRENADE.OnCollisionEnter');
            }
        });
        registerProbeAttach('WPN_GRENADE.OnTriggerEnter(homing)', RVA.WPN_GRENADE_OnTriggerEnter, {
            onEnter: function (args) {
                Runtime.stats.missileTriggerSeen += 1;
                if (probeBudget('missileTrig', 6)) probe('missileTrig', fmtPtr(args[0]) + ' WPN_GRENADE.OnTriggerEnter');
            }
        });
    }
    function installHooks() {
        if (Runtime.initialized) return true;
        if (!ensureNative()) return false;
        if (!ensureBuffers()) return false;
        try {
            // 只装 5 组钩子，全部是"只读目标选择 + 改写射线/速度 + 爆炸前复位防御状态"：
            //   installGunHook             : WPN_Gun.Damage（改 rayDir）
            //   installExplosiveHooks      : 手雷/榴弹/RPG 开火（登记弹体类别）
            //   installSkillHooks          : 技能弹开火（登记弹体类别）
            //   installHomingHooks         : 弹体 SetWeaponData / FixedUpdate / Work / Recycle
            //   installExplosionDefenseHook: WPN_GRENADE.CreateExplosion（爆炸前复位范围内敌人的防御状态）
            //   installTakeDamageDefenseHook: GameManager.TakeDamage（伤害真正落地前复位 victim 的防御状态）
            // 旧版的 installPipelineProbes / installDeathDiagnostics /
            // installStringCaptureHooks / installEventTemplateCapture 已全部删除。
            installHomingHooks();
            installGunHook();
            installExplosiveHooks();
            installSkillHooks();
            installExplosionDefenseHook();
            installTakeDamageDefenseHook();
            Runtime.initialized = true;
            log('info', 'all hooks installed (ray-redirect + homing only; ' +
                'no damage injection, no death/respawn handling)');
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
        Runtime.initialized = false;
    }

    function resetRuntime(reason) {
        stopHeartbeat();
        cleanupHooks();
        Runtime.missileTargets = {};
        Runtime.pendingMissile = null;
        Runtime.cache.ownPlayer = ptr(0);
        Runtime.cache.selectedTarget = null;
        Runtime.cache.selectedAtMs = 0;
        Runtime.cache.rayWarnLogged = false;
        Runtime.targetLock = null;
        Runtime.stats.targetLockReason = 'init';
        Runtime.stats.targetSwitchCount = 0;
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
    //   注意这里**没有** death_* / damage_entry / gun_hook_mode / damage_override /
    //   use_event_template / fallback_to_original / entry_fallback / wpn_key_fallback
    //   这些键 —— 它们随注入链路一起删除了。旧 user_config.json 里若还留着，
    //   本函数会直接忽略（不会报错，也不会生效）。
    //
    //   钩子是 enable 时装的，但所有开关/参数都在钩子内部实时读取，
    //   所以改完立刻生效，不需要重新 enable。
    function updateConfig(input) {
        input = input || {};
        var c = Runtime.config;

        if (input.enable_guns !== undefined) c.enable_guns = input.enable_guns !== false;
        if (input.enable_homing !== undefined) c.enable_homing = input.enable_homing !== false;
        if (input.enable_explosives !== undefined) c.enable_explosives = input.enable_explosives !== false;
        if (input.enable_skill_projectiles !== undefined) {
            c.enable_skill_projectiles = input.enable_skill_projectiles !== false;
        }

        // ---- 统一目标策略 ----
        if (input.target_outer_cone_deg !== undefined) {
            c.target_outer_cone_deg = clampFloat(toNumber(input.target_outer_cone_deg, c.target_outer_cone_deg), 1, 90);
            c.target_inner_cone_deg = Math.min(c.target_inner_cone_deg, c.target_outer_cone_deg);
        }
        if (input.target_inner_cone_deg !== undefined) {
            c.target_inner_cone_deg = clampFloat(toNumber(input.target_inner_cone_deg, c.target_inner_cone_deg), 0, c.target_outer_cone_deg);
        }
        if (input.target_angle_tie_deg !== undefined) {
            c.target_angle_tie_deg = clampFloat(toNumber(input.target_angle_tie_deg, c.target_angle_tie_deg), 0, 15);
        }
        if (input.target_switch_margin_deg !== undefined) {
            c.target_switch_margin_deg = clampFloat(toNumber(input.target_switch_margin_deg, c.target_switch_margin_deg), 0, 15);
        }
        if (input.target_switch_confirm_scans !== undefined) {
            c.target_switch_confirm_scans = Math.max(1, Math.min(10, Math.round(toNumber(input.target_switch_confirm_scans, c.target_switch_confirm_scans))));
        }
        if (input.target_switch_cooldown_ms !== undefined) {
            c.target_switch_cooldown_ms = clampFloat(toNumber(input.target_switch_cooldown_ms, c.target_switch_cooldown_ms), 0, 2000);
        }
        if (input.max_distance !== undefined) c.max_distance = clampFloat(toNumber(input.max_distance, c.max_distance), 0, 1000);

        // 枪械锥内没人时的可选保底：只回退近距最近，默认关闭。
        if (input.gun_fallback_nearest !== undefined) c.gun_fallback_nearest = input.gun_fallback_nearest !== false;
        if (input.gun_fallback_max_distance !== undefined) {
            c.gun_fallback_max_distance = clampFloat(toNumber(input.gun_fallback_max_distance, c.gun_fallback_max_distance), 0, 1000);
        }

        if (input.local_eye_height !== undefined) c.local_eye_height = clampFloat(toNumber(input.local_eye_height, c.local_eye_height), 0, 5);
        if (input.chest_fallback_height !== undefined) c.chest_fallback_height = clampFloat(toNumber(input.chest_fallback_height, c.chest_fallback_height), 0, 5);
        if (input.target_cache_ms !== undefined) c.target_cache_ms = clampFloat(toNumber(input.target_cache_ms, c.target_cache_ms), 0, 1000);

        if (input.diagnostic_log !== undefined) c.diagnostic_log = input.diagnostic_log !== false;
        if (input.log_every !== undefined) c.log_every = Math.max(1, Math.floor(toNumber(input.log_every, c.log_every)));
        if (input.homing_speed !== undefined) c.homing_speed = clampFloat(toNumber(input.homing_speed, c.homing_speed), 0, 500);
        if (input.homing_turn !== undefined) c.homing_turn = clampFloat(toNumber(input.homing_turn, c.homing_turn), 0.05, 1);
        if (input.homing_retarget !== undefined) c.homing_retarget = input.homing_retarget !== false;
        if (input.homing_max_ms !== undefined) c.homing_max_ms = clampFloat(toNumber(input.homing_max_ms, c.homing_max_ms), 500, 120000);
        if (input.homing_pending_ms !== undefined) c.homing_pending_ms = clampFloat(toNumber(input.homing_pending_ms, c.homing_pending_ms), 50, 5000);
        // 弹体锥内没人时的回退：默认回退全场最近；可限制最大距离。
        if (input.missile_fallback_nearest !== undefined) c.missile_fallback_nearest = input.missile_fallback_nearest !== false;
        if (input.missile_fallback_max_distance !== undefined) {
            c.missile_fallback_max_distance = clampFloat(toNumber(input.missile_fallback_max_distance, c.missile_fallback_max_distance), 0, 1000);
        }
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
        resetTargetLock(Runtime.targetLock, 'config_changed');

        log('info', '[probe:config] guns=' + c.enable_guns +
            ' homing=' + c.enable_homing +
            ' explosives=' + c.enable_explosives +
            ' skills=' + c.enable_skill_projectiles +
            ' homingSpeed=' + c.homing_speed + ' homingTurn=' + c.homing_turn +
            ' retarget=' + c.homing_retarget + ' maxMs=' + c.homing_max_ms +
            ' outer=' + c.target_outer_cone_deg + 'deg inner=' + c.target_inner_cone_deg + 'deg' +
            ' margin=' + c.target_switch_margin_deg + 'deg confirm=' + c.target_switch_confirm_scans +
            ' gunFallback=' + c.gun_fallback_nearest +
            ' missileFallback=' + c.missile_fallback_nearest +
            ' maxDist=' + c.max_distance +
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

        log('info', '[probe:enable] enable() called | 本版本只做射线接管 + 弹体追踪，' +
            '不注入伤害、不处理死亡/复活' +
            ' | guns=' + Runtime.config.enable_guns +
            ' homing=' + Runtime.config.enable_homing +
            ' explosives=' + Runtime.config.enable_explosives +
            ' skills=' + Runtime.config.enable_skill_projectiles +
            ' homingTurn=' + Runtime.config.homing_turn +
            ' outer=' + Runtime.config.target_outer_cone_deg + 'deg' +
            ' inner=' + Runtime.config.target_inner_cone_deg + 'deg' +
            ' gunFallback=' + Runtime.config.gun_fallback_nearest +
            ' missileFallback=' + Runtime.config.missile_fallback_nearest +
            ' maxDist=' + Runtime.config.max_distance +
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
        log('info', '[probe:enable] hooks OK: attaches=' + Runtime.attachHooks.length);
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

            // ---- 常规枪械 ----
            gun_damage_calls: Runtime.stats.gunDamageCalls,
            local_gun_fires: Runtime.stats.localGunFires,
            skipped_remote_weapon: Runtime.stats.skippedRemote,
            gun_hook_disabled: Runtime.stats.gunHookDisabled,
            ray_redirect_shots: Runtime.stats.rayRedirectShots,
            ray_redirect_bad_args: Runtime.stats.rayRedirectBadArgs,
            ray_redirect_skip: Runtime.stats.rayRedirectSkip,
            invincible_cleared: Runtime.stats.invincibleCleared,
            invincible_unreadable: Runtime.stats.invincibleUnreadable,
            explosion_defense_calls: Runtime.stats.explosionDefenseCalls,
            explosion_defense_cleared: Runtime.stats.explosionDefenseCleared,
            take_damage_calls: Runtime.stats.takeDamageCalls,
            take_damage_ours: Runtime.stats.takeDamageOurs,
            take_damage_cleared: Runtime.stats.takeDamageCleared,
            targets_selected: Runtime.stats.targetsSelected,
            no_target: Runtime.stats.noTarget,
            target_lock_reason: Runtime.stats.targetLockReason,
            target_switch_count: Runtime.stats.targetSwitchCount,
            last_target_angle: Runtime.stats.lastTargetAngle,
            last_target_distance: Runtime.stats.lastTargetDistance,

            // ---- 弹体追踪 ----
            explosive_triggers: Runtime.stats.explosiveTriggers,
            skill_triggers: Runtime.stats.skillTriggers,
            missile_spawns: Runtime.stats.missileSpawns,
            missile_launch_seen: Runtime.stats.missileLaunchSeen,
            missile_not_mine: Runtime.stats.missileNotMine,
            missile_no_pending: Runtime.stats.missileNoPending,
            missile_switch_off: Runtime.stats.missileSwitchOff,
            missile_no_target: Runtime.stats.missileNoTarget,
            homing_armed: Runtime.stats.homingArmed,
            homing_steered: Runtime.stats.homingSteered,
            homing_dropped: Runtime.stats.homingDropped,
            homing_forgotten: Runtime.stats.homingForgotten,
            homing_tracked: Object.keys(Runtime.missileTargets).length,
            missile_fixed_update_calls: Runtime.stats.fixedUpdateCalls,
            steer_wrote: Runtime.stats.steerWrote,
            steer_off: Runtime.stats.steerOff,
            steer_no_entry: Runtime.stats.steerNoEntry,
            steer_no_pos: Runtime.stats.steerNoPos,
            steer_no_aim: Runtime.stats.steerNoAim,
            steer_too_close: Runtime.stats.steerTooClose,
            steer_write_skip: Runtime.stats.steerWriteSkip,
            steer_lost_target: Runtime.stats.steerLostTarget,
            missile_hit_seen: Runtime.stats.missileHitSeen,
            missile_trigger_seen: Runtime.stats.missileTriggerSeen,
            forget_reuse: Runtime.stats.forgetReuse,
            forget_recycle: Runtime.stats.forgetRecycle,
            forget_timeout: Runtime.stats.forgetTimeout,
            forget_identity: Runtime.stats.forgetIdentity,
            cone_hit: Runtime.stats.coneHit,
            cone_empty: Runtime.stats.coneEmpty,
            cone_fallback: Runtime.stats.coneFallback,
            cone_empty_strict: Runtime.stats.coneEmptyStrict,
            cone_off: Runtime.stats.coneOff,
            cone_axis_fail: Runtime.stats.coneAxisFail,
            cone_retarget: Runtime.stats.coneRetarget,

            // ---- 通用 ----
            own_player_source: Runtime.stats.ownPlayerSource,
            error_count: Runtime.stats.errorCount,
            last_error: Runtime.stats.lastError,
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
        clearLogs: function () { Runtime.logRing = []; resetProbes(); return true; },
        setLogFile: function (path) { return updateConfig({ log_file: path }); },
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
