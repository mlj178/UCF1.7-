// ============================================================
// script.js — 开火直伤/弹体追踪 (feature_id: "direct_damage")
//
// 【2.7 整合包版本】由 05-正式功能/40-开火直伤/script.js 迁移而来。
// 与源文件的差异只有 4 处（其余逐字一致，方便两边对照排查）：
//   1) target_mode 默认 = angle_then_distance（准星方向 + 距离最近）
//   2) verbose_probe 默认 = false（不装诊断管线钩子）
//   3) diagnostic_log 默认 = false
//   4) log_to_file 默认 = false（不在游戏目录写日志文件）
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
// 设计说明三：开关划分（枪械走直伤，投射物走追踪）
// ------------------------------------------------------------------
//   enable_guns              : 常规枪械 **直伤**（替换 WPN_Gun.Damage）
//   enable_homing            : 投射物 **追踪（制导）总开关**
//   enable_explosives        : 榴弹 / 手雷 / RPG / 榴弹枪 弹体追踪（子开关）
//   enable_skill_projectiles : 特殊技能弹体追踪（奥术手雷 / 地狱终结者火球）（子开关）
//
//   为什么爆炸物 / 技能弹不做直伤：
//     它们的原版逻辑本来就是"弹体飞到 -> 命中判定 -> WPN_GRENADE.CreateExplosion
//     做范围伤害"。也就是说 **只要弹体能飞到敌人身上，原版自己就会把伤害算对**
//     （含爆炸范围、距离衰减、wpnIndex、死亡广播、击杀归属）。再额外注入一份
//     直伤等于"打两遍"，而且绕过了爆炸范围判定，手感很怪。
//     所以这两类的正确做法是：**不注入任何伤害，只把弹体掰向敌人**（追踪/拐弯），
//     伤害 100% 交给原版。枪械才走直伤。
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
//   因此新的登记挂点是 WPN_Missile.SetWeaponData（0x00B663C0）：
//     - 它由 ProjectMissile 的回调调用，5 种投射物（RPG / 手雷 / 榴弹枪 /
//       奥术手雷 / 地狱终结者火球）**全部**会走到；
//     - 进入时 owner 已经写好 -> 用 Player.get_isMyPlayer 判断"是不是自己发射的"；
//     - 进入时还没 Active()，属于"发射前登记"，随后 FixedUpdate 才开始拐。
//     - 对象池会复用弹体指针，所以每次 SetWeaponData **先无条件清掉旧记录**，
//       再决定要不要登记，避免"敌人的手雷被掰到我们的目标上"。
//
//   拐弯算法（挂在 WPN_Missile.FixedUpdate 的 onLeave，物理步末尾）：
//     1) 读弹体自身速度 shootSpeed(+0x4C)，读 Rigidbody.get_velocity 拿当前方向；
//     2) 目标方向 = normalize(敌人瞄准点 - 弹体位置)；
//     3) 新方向 = 当前方向与目标方向按 homing_turn 插值
//        （1.0 = 每个物理步直接锁定，弹体立刻拐向敌人；
//          <1 = 保留一部分原弹道，抛物弧线更自然）；
//     4) Rigidbody.set_velocity(新方向 * 速度)，同时把 transform 朝向也掰过去
//        （视觉上弹头朝前，也兼容"用 transform.forward 推位移"的写法）。
//
//   **"打谁"策略（scanEnemies + 准星锥）**：
//     与枪械直伤不同，弹体追踪**不读 config.target_mode**，它只认两个键：
//       homing_cone_deg      = 0 -> 关闭准星锥，退回旧的"全场最近"
//                            > 0 -> 先只保留「锥轴 与 参考点->目标 夹角 <= 该值」的敌人，
//                                   锥内再比距离取最近的那个
//       homing_cone_fallback = true （默认）锥内没人 -> 回退成"全场最近"
//                            = false          锥内没人 -> 这颗弹不追踪、按原弹道直飞
//     锥轴 / 锥心：
//       发射时（SetWeaponData -> armMissileHoming -> pickEnemyForLaunch）
//         锥轴 = 本地玩家相机朝向 Player.cameraRotation(+0x4C/+0x50)
//         锥心 = 眼睛位置 getLocalEyePos = 玩家坐标 + local_eye_height(1.55)
//                （准星锥必须从眼睛量，用脚底量在几何上不成立）
//       飞行途中换目标（目标死亡/读不到 -> pickEnemyForMissileRetarget）
//         锥轴 = 弹体当前速度方向，锥心 = 弹体当前位置
//                用速度而不是玩家准星：弹体已经飞出去了，玩家可能早就看别处；
//                用速度还能避免弹体在半空 180° 掉头，飞行观感更自然。
//     排序依据 = 到参考点的 3D 直线距离，量到**胸口**（getAimPoint，取不到才退到脚底）。
//     硬过滤永远只有两条：**敌对阵营 + 存活**，永远不打自己人。
//     夹角算法与枪械直伤完全一致（calculateTargetAngles + angleDistanceDeg），
//     所以"准星锥"在两条路径上的含义不会漂移。
//
//   注意：追踪**没有寻路**。弹体只会沿直线朝敌人飞，中间隔墙就会打在墙上爆炸
//   （原版行为）。这是刻意保留的——不改变原版的命中判定规则。
//   "绕墙"的可行性评估（含 Physics.Raycast/SphereCast/NavMesh 的可用地址）见
//   同目录《开火直伤-简要说明.md》的 §8。
//
// ------------------------------------------------------------------
// 设计说明五：持久化日志与探针（排查"没有任何效果"用）
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
//     [probe:trig]        爆炸物/技能弹开火（只记录，不再注入伤害）
//     [probe:missileArm]  **弹体追踪的最终判据**：这颗弹被登记为"要制导"
//     [probe:missileNotMine] 弹体是别人发射的（不制导）
//     [probe:missileNoPending] 没抓到对应的开火记录（开火钩子没命中）
//     [probe:missileForget]   弹体爆炸/回收，清掉制导记录
//     [probe:homingSteer] 实际改写弹体速度（拐弯）的次数
//     [probe:homingCone]  准星锥的目标选择：锥内候选数/夹角，锥空时是回退还是放弃
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
//     扔手雷/RPG 后看 [probe:beat] 的 missile：
//       trig=0                        -> 开火钩子没命中（RVA 不匹配）
//       spawn=0                       -> SetWeaponData 钩子没命中
//       spawn>0 但 arm=0              -> 看是 notMine（不是自己发射）还是
//                                        noPending（开火记录没接上）
//       arm>0 但 steer=0              -> 弹体没有 FixedUpdate（被回收/未激活）
//       steer>0                       -> 弹体正在拐弯
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
//   ---- 弹体追踪（制导）----
//   Weapon_ProjectMissile:             0x00B6D080   **投射物统一生成入口**
//                                                  (missile = GetEffect(prefab);
//                                                   missile.owner = weapon.owner;
//                                                   callback.Invoke(missile);
//                                                   missile.Active() -> Work())
//   WPN_Missile_SetWeaponData:         0x00B663C0   **制导登记点**（回调里被调用）
//   WPN_Missile_FixedUpdate:           0x00B660C0   只做 AddForce(extraGravity)
//   WPN_Missile_Work:                  0x00B664D0   velocity = forward * shootSpeed
//   WPN_GRENADE_Work:                  0x00B5D6C0   （手雷重写了 Work，逻辑同上）
//   WPN_Missile_Recycle:               0x00B66240   velocity = zero（回池）
//   WPN_Missile_OnCollisionEnter:      0x00B66100   （基类；手雷重写了它）
//   WPN_GRENADE_OnCollisionEnter:      0x00B5D0F0
//   WPN_GRENADE_OnTriggerEnter:        0x00B5D270
//   Rigidbody_get_velocity_Injected:   0x00ABBDC0   (this, out Vector3, method)
//   Rigidbody_set_velocity:            0x00ABC060   (this, x, y, z, method)
//   Quaternion_LookRotation:           0x004F1710   (out, x, y, z, method)
//   Transform_set_rotation:            0x003F48A0   (this, x, y, z, w, method)
//
//   注意：WPN_Missile.SetOwner(0x00B66390) 在这份二进制里**没有任何直接调用点**
//   （全 il2cpp 段扫描 0 处），owner 是 ProjectMissile 直接写字段的。
//   所以不要再把制导登记挂在 SetOwner 上 —— 那是旧版追踪不生效的根因。
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
        // 用游戏自己的武器表查询来"验证" wpnIndex 是不是合法 key。
        // 反汇编（0x10AFB130）确认它内部是 Dictionary.TryGetValue：
        //   key 不存在 -> *data = 0 且 return false，不会抛异常。
        // 有了它就能在注入之前把不合法的 wpnIndex 挡掉，而不是等死亡广播里炸。
        GameManager_GetWpnData: 0x00AFB130,
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
        HealthData_get_isDead: 0x00AE4830,
        // ---- 真实伤害事件底板（修"敌人死了不复活 / 多人生化闪退"的核心）----
        //   DamageEventData.TakePlace() 是值类型实例方法，this 就是结构体指针，
        //   原版每次开火（哪怕打空、打墙）都会走到它 —— 在这里把整份 0x48 字节的
        //   原版事件抄下来当"底板"，合成事件时只改 victim/damage/origin/hitPos。
        //   原因：GameManager.DeathEventBroadcast -> HUD_KillMark -> 
        //         DeathEventData.get_wpnName()/get_killMsgIcon() 内部是
        //         GameManager.WpnDataDictionary[wpnIndex] 字典查找，
        //         我们自己填的 wpnIndex=0 不在字典里 -> KeyNotFoundException ->
        //         异常打断死亡广播 -> 敌人 isDead=true 但永远不复活；
        //         多人生化模式下同一条异常直接把游戏带崩。
        DamageEventData_TakePlace: 0x00B3D0D0,
        // 死亡广播 / 命中特效音效：只挂 onEnter+onLeave 探针，
        // 用来确认"异常到底停在哪一步"（onEnter 有、onLeave 没有 = 抛在这里）。
        GameManager_DeathEventBroadcast: 0x00AFA400,
        GameManager_PlayHitFxAndSnd: 0x00AFB970,
        // ---- 死亡→复活链诊断（death_diag；只读观察，不改变游戏行为）----
        // ModeBase_Nano.RespawnPlayer(Player,int,bool,bool)：生化模式“复活调度”的唯一入口，
        //   普通幽灵与终结者（含 Mode_Nano4_Terminator 的墓碑复活，最后都会调基类）都会走到。
        // Player.Respawn(float,float)：真正把玩家排进复活协程。
        // Player.get_nanoRole()：读复活时的纳米角色，用来区分普通幽灵/终结者/高阶终结者。
        ModeBase_Nano_RespawnPlayer: 0x00AF2670,
        Player_Respawn: 0x00B527A0,
        Player_get_nanoRole: 0x00B56200,
        // 托管异常的"唯一漏斗"：il2cpp_raise_exception 以及所有托管 throw 最终都会进
        //   sub_1013FF10(Il2CppException* ex, MethodInfo*, ...) -> _CxxThrowException。
        //   钩它就能在"死亡广播被打断"的那一毫秒拿到异常类型 + 调用栈 RVA。
        Il2Cpp_Exception_Raise: 0x0013FF10,
        // ModeBase_Nano.DeathEvent(this, DeathEventData, MethodInfo)：抓死亡链上的 mode 实例，
        //   复活兜底要用它当 this。
        ModeBase_Nano_DeathEvent: 0x00AEF9E0,

        // ---- 弹体追踪（制导）----
        //   WPN_Missile 是手雷/RPG/榴弹枪/奥术手雷/火球共用的投射物基类，
        //   WPN_GRENADE 继承它。FixedUpdate 只有基类定义（手雷没重写），
        //   所以挂基类这一个就覆盖全部弹体。
        //
        //   登记点选 WPN_Missile.SetWeaponData 而不是 SetOwner：
        //     SetOwner 在这份二进制里 0 个直接调用点（owner 由 ProjectMissile
        //     直接写字段），挂它等于永远不触发。
        //   ProjectMissile 的调用顺序是：
        //     owner 赋值 -> 回调(SetWeaponData) -> Active()->Work() 发射
        //   所以 SetWeaponData 里 owner 已经可用，且早于发射，正好用来登记。
        WPN_Missile_SetWeaponData: 0x00B663C0,
        WPN_Missile_FixedUpdate: 0x00B660C0,
        WPN_Missile_Work: 0x00B664D0,
        WPN_GRENADE_Work: 0x00B5D6C0,
        WPN_Missile_Recycle: 0x00B66240,
        WPN_Missile_OnCollisionEnter: 0x00B66100,
        // 手雷重写了 OnCollisionEnter / 另有 OnTriggerEnter，必须单独挂。
        WPN_GRENADE_OnCollisionEnter: 0x00B5D0F0,
        WPN_GRENADE_OnTriggerEnter: 0x00B5D270,
        // 基类回收：WPN_Missile.Recycle 是重写，但有些路径会直接调基类那一份，
        // 两边都挂才能保证「弹体回池一定清记录」。
        RecyclableObject_Recycle: 0x00B1A5A0,
        // 投射物统一生成入口（只进 RVA 审计 + 探针，不挂功能钩子）
        Weapon_ProjectMissile: 0x00B6D080,
        // 读写速度/朝向用（Vector3 与 Quaternion 都是按值压栈的 struct）
        Rigidbody_get_velocity_Injected: 0x00ABBDC0,
        Rigidbody_set_velocity: 0x00ABC060,
        Quaternion_LookRotation: 0x004F1710,
        Transform_set_rotation: 0x003F48A0
    };

    var OFF = {
        Klass_staticFields: 0x5C,

        GameManager_myPlayer: 0x00,
        GameManager_allPlayers: 0x1C,
        GameManager_playersBL: 0x20,
        GameManager_playersGR: 0x28,

        Entity_team: 0x20,
        Entity_healthData: 0x1C,
        // Entity 字段（dump.cs 确认）：
        //   damageRate   +0x14  减伤倍率（SetDamageRate 的产物；复活无敌会把它压到 0）
        //   isInvincible +0x18  无敌标记（InvincibleBuff 通过 RefBool 写它）
        Entity_damageRate: 0x14,
        Entity_isInvincible: 0x18,
        // HealthData.invinsibleEndTime（dump.cs: 0x44）复活无敌的结束时间戳
        HealthData_invinsibleEndTime: 0x44,

        Player_cameraRotation: 0x4C,
        Player_characterContainer: 0x58,
        Player_currentCharacter: 0x5C,
        Player_clientData: 0x94,

        ClientData_nickname: 0x10,

        Weapon_data: 0x68,
        // WeaponData.wpnIndex（dump.cs: 0xC）= WpnDataDictionary 的合法 key
        WeaponData_wpnIndex: 0x0C,
        // WeaponData.hitEffectName（dump.cs: 0xA8）= 原版命中特效名（合法字符串）
        WeaponData_hitEffectName: 0xA8,
        WPN_Gun_realData: 0xEC,
        WeaponData_Gun_ammoDamage: 0x14C,

        // MissileData 是内联 struct，damage 在 missileData 起始 +0x0C
        MissileData_damage: 0x0C,
        WD_RPG_missileData: 0xB8,
        WD_Missile_missileData: 0xB8,
        WD_GrenadeGun_missileData: 0x20C,
        WD_EvilTerminator_missileData: 0xF8,

        // WPN_Missile 字段（dump.cs + 反汇编双重确认）
        //   owner            0x30  Entity/Player（ProjectMissile 直接写字段）
        //   ownerInitalTeam  0x34  Team 快照
        //   weaponData       0x38  SetWeaponData 写入
        //   sprIndex         0x3C  SetWeaponData 写入
        //   rigidBody        0x44  Unity Rigidbody（物理驱动）
        //   shootSpeed       0x4C  = MissileData.velocity（Work 用它发射）
        Missile_owner: 0x30,
        Missile_ownerInitalTeam: 0x34,
        Missile_weaponData: 0x38,
        Missile_sprIndex: 0x3C,
        Missile_rigidBody: 0x44,
        Missile_shootSpeed: 0x4C,

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
        Dmg_dwordCount: 18,

        // ---- DeathEventData（0x38 字节，按值传播；死亡广播的参数）----
        Death_killer: 0x00,
        Death_dead: 0x04,
        Death_headShot: 0x08,
        Death_wallThrough: 0x0C,
        Death_damageType: 0x10,
        Death_damageOrigin: 0x14,
        Death_specialKill: 0x20,
        Death_nanoKill: 0x24,
        Death_revenge: 0x28,
        Death_damageTag: 0x2C,
        Death_wpnIndex: 0x30,
        Death_wpnSprIndex: 0x34,
        Death_size: 0x38,

        // ---- Player 复活状态（dump.cs 确认）----
        Player_nano4TData: 0xAC,
        Player_respawnType: 0xD0,
        Player_isRespawning: 0xD8,
        Nano4TData_canUseGrave: 0x14,
        Nano4TData_graveCount: 0x18,

        // ---- GameManager 武器表 & Dictionary/Entry/Array 内部布局 ----
        //   死亡广播里的 get_wpnName/get_killMsgIcon/get_isVVIP 查的是
        //   GameManager.WpnDataDictionary（static +0x1C）；下面这些偏移由 dump.cs + IDA 类型双重确认。
        GM_WpnDataDictionary: 0x1C,   // Dictionary<int, WeaponData>
        Dict_entries: 0x0C,           // Dictionary.entries 数组
        Dict_count: 0x10,             // Dictionary.count（已用条目数）
        Dict_version: 0x14,           // Dictionary.version（变化 = 需要重建 key 缓存）
        Arr_maxLength: 0x0C,          // Il2CppArray.max_length
        Arr_items: 0x10,              // Il2CppArray 数据区起点
        Entry_size: 0x10,             // Entry{hashCode,next,key,value} = 16 字节
        Entry_key: 0x08               // Entry.key
    };

    var DAMAGE_TYPE = {
        Gun: 1,
        Knife: 2,
        Grenade: 3,
        Infect: 4,
        Other: 5
    };

    // 投射物类别：决定"追踪"归哪个子开关管。
    // 由 5 个开火钩子写入 Runtime.pendingMissile，再由 SetWeaponData 消费。
    // 之所以要这个中间状态：SetWeaponData 只知道"哪颗弹 + 哪份 WeaponData"，
    // 分不清这颗弹是榴弹还是技能弹；而开火钩子知道自己在哪个武器类里。
    // 两者在同一次调用栈内先后发生（ProjectMissile 里同步回调），所以用
    // 一个"待消费"记录最稳，不依赖任何猜测。
    var CATEGORY = {
        EXPLOSIVE: 'explosive',
        SKILL: 'skill'
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

        // ---- 弹体追踪状态 ----
        //   missileTargets: missile 指针字符串 -> { target, at, category, label }
        //     at = 这颗弹被登记的时间（= 出生时间），用于 homing_max_ms 总时限与心跳清理；
        //          换目标时**不**刷新它。
        //   pendingMissile: 开火钩子写、SetWeaponData 读的"这颗弹是什么类别"
        missileTargets: {},
        pendingMissile: null,

        // death_diag：击杀后观察窗口
        //   key = 目标指针字符串 -> { victim, at, label, note, scheduled }
        deathWatch: {},

        // death_fix_wpn：最近一次确认「在 WpnDataDictionary 里存在」的 wpnIndex，
        // 作为坏 key 的兜底（没有就退化成字典里最小的合法 key）。
        lastValidWpnIndex: -1,

        // death_diag：当前"进了还没出"的那次死亡广播。
        //   下一次死亡广播进入时它还在 = 上一次被托管异常打断（目标不会复活）。
        pendingDeath: null,
        // death_fix_respawn：复活兜底用的生化模式实例（从 RespawnPlayer / DeathEvent 钩子里抓）
        modeBase: null,
        lastRescueTick: 0,
        lastRaiseLogAt: 0,
        // 当前正在飞的死亡广播登记的目标 key（onLeave 用它把 bcDone 置 true）
        currentDeathKey: null,

        // 死亡链观察（death_diag_chain）：GameManager.TakeDamage 进出的嵌套深度 +
        // "这一次 TakeDamage 调用里发生了多少次死亡广播" —— 用来直接回答
        // "我们的注入到底有没有触发游戏自己的死亡流程"。
        chain: { depth: 0, inCallBroadcasts: 0 },

        module: null,
        base: ptr(0),
        attachHooks: [],
        replacedAddresses: [],
        config: {
            // 开关（默认全开，可在 UI/整合包面板里单独关闭）
            //   enable_guns              : 常规枪械直伤
            //   enable_homing            : 投射物追踪总开关
            //   enable_explosives        : 榴弹/手雷/RPG/榴弹枪 弹体追踪
            //   enable_skill_projectiles : 奥术手雷/地狱终结者火球 弹体追踪
            enable_guns: true,
            enable_homing: true,
            enable_explosives: true,
            enable_skill_projectiles: true,

            // 目标选择（**2.7 正式版默认 = 准星方向 + 距离最近**）
            //   先卡准星锥（max_angle_deg），再在锥内取距离最近的那个。
            //   锥内没人 -> selectTarget 返回 null -> fallback_to_original 走原版射线，
            //   所以"对着空气开火"时是原版弹道，不会凭空掉血。
            //   想回到"完全不看准星、全场最近"就把下面改成 TARGET_MODE.NEAREST。
            target_mode: TARGET_MODE.ANGLE_THEN_DISTANCE,
            max_angle_deg: 30.0,        // 准星锥角度（angle_then_distance / weighted 生效）
            max_distance: 0.0,          // 0 = 不限距离
            angle_weight: 1.0,
            distance_weight: 0.5,

            // 伤害注入
            // 默认必须走 "gamemanager"（GameManager.TakeDamage）。证据链（IDA 反汇编）：
            //   1) DamageEventData.TakePlace()（游戏自己的"结算这个伤害事件"）反汇编就是：
            //        if (victim == null) return;
            //        if (victim.healthData == null) return;
            //        if (victim.healthData.isDead) return;
            //        GameManager.TakeDamage(this);
            //   2) GameManager.TakeDamage 内部依次调用：
            //        GameManager.DamageEvent$$Invoke ×6  (InvalidCheck/PreCal/PostCal/Post/...)
            //        GameManager.PlayHitFxAndSnd         (命中特效/音效)
            //        HealthData.get_isDead               (判定是否死亡)
            //        GameManager.DeathEventBroadcast     (**真正把敌人打死**)
            //   3) 而 Player.OnEntityHurt / HealthData.Hurt 只做 HP 相减：
            //        Entity.OnEntityHurt = if (type != Infect) HealthData.Hurt(healthData, (int)damage)
            //      完全不碰 DeathEventBroadcast。
            //   ==> 用 hurt/health 的结果是"敌人 HP 归零、isDead=true，但永远不会死"，
            //       画面上就是敌人站着不动、打不死 —— 即"敌人无敌"。
            damage_entry: DAMAGE_ENTRY.GAME_MANAGER,
            // ★2026-10-14 修复：WPN_Gun.Damage 的挂法（attach / replace）★
            //   实证链（测试会话 7da632fc，日志一一对应）：
            //     Bot 打死终结者时，游戏自己的"伤害->死亡广播"链内部会抛一个托管异常
            //     （il2cpp 的 C++ EH，0xE06D7363）。这种异常游戏日常一直在抛、也一直是
            //     游戏自己的异常帧收掉的（19:21 会话 raises=14，全部被游戏消化）。
            //     但只要 WPN_Gun.Damage 被我们 Interceptor.replace、原函数又是从 JS 用
            //     NativeFunction 回call 的，这个异常就会在"跨回 JS"的边界上被 Frida 抢先
            //     捕获（JS 只看到 "system error"），游戏自己的异常帧再也收不到 ->
            //     死亡广播进入后不返回 -> ModeBase_Nano.RespawnPlayer 一次都没被调用 ->
            //     终结者躺尸，只能等 death_fix_respawn 兜底（延迟约 7 秒）。
            //   日志指纹：每个 [deathDiag:abort] 之前 0~40ms 必有一条
            //     [fail:WPN_Gun.Damage replacement] ... system error (x1..x9)，9 对 9 全部对应。
            //   修法（与 26_grenade_mode v2.13 同一条硬规则：能 attach 就不 replace）：
            //     'attach'  = 只挂 onEnter。不是本地武器的开火（Bot 开火）直接放行，
            //                 原函数完全原生执行、Frida 不留帧在调用链上 -> 托管异常照常
            //                 交给游戏自己处理；是本地武器时我们自己结算直伤，再用
            //                 "模拟 ret"（弹掉返回地址 + 跳回调用方）跳过原函数。
            //     'replace' = 旧行为（replace + 回call），仅用于 A/B 对照或回退排障。
            //   注意：改这个键需要重新 enable（钩子在 enable 时安装）。
            gun_hook_mode: 'attach',
            // 统一入口万一被 InvalidCheck 观察者否决（HP 完全没变），是否自动降级补一次 hurt。
            // 只是"至少掉血"的保险，日志会明确写出来。
            entry_fallback: true,
            // 注意：本功能**不提供**伤害倍率/伤害覆盖给用户调节（已按需求移除倍率）。
            // damage_override 仅作为内部调试手段保留，默认 0 = 关闭。
            damage_override: 0.0,
            // 用"原版真实事件底板"合成伤害事件（默认开，强烈建议保持开启）。
            //   true  = 抄一份原版 DamageEventData，只改 victim/damage/origin/hitPos；
            //           wpnIndex/wpnSprIndex/damageTag/hitTag/hitSndName/hitEffect 全部是
            //           原版值 -> 死亡广播能跑完 -> 敌人正常复活、多人模式不闪退。
            //   false = 退回旧的手工合成（wpnIndex=0），只用于 A/B 对照，
            //           实测会抛 KeyNotFoundException 并导致"死了不复活"。
            use_event_template: true,
            // 没有可选目标时是否回退原版射线（实测后改的默认值）：
            //   true（默认）= 无目标时原版弹道照常走 -> 墙上照常有弹孔/着弹特效，手感自然；
            //                 false 时打完所有敌人后每次开火都是"子弹凭空消失"，
            //                 玩家会以为功能完全没生效（就是这么被误判的）。
            //   false       = 无目标时什么都不做（纯直伤，子弹彻底不飞）。
            fallback_to_original: true,

            // ---- ★2026-10-15 根因修复：原生射线接管（gun_ray_redirect）★ ----
            //   session 1e44becf 实测（53 笔死亡广播，其中 0 笔是我们打出来的）：
            //     [ours] 死亡登记 = 0 —— 我们 16 次"击杀"（目标确实 isDead=true）里，
            //     没有任何一次触发游戏自己的 DeathEventBroadcast；同一个目标要等到
            //     十几秒后"被别人再打死一次"才出现死亡广播。
            //   原因：attach 模式的"模拟 ret"把整个 WPN_Gun.Damage 跳过了，而注入只补了
            //     它的前半截 GameManager.TakeDamage（扣血）。击杀提示 / 模式记账 /
            //     ModeBase_Nano.RespawnPlayer 复活调度都在 TakeDamage 之后的原函数里，
            //     跳过原函数 = 这笔死亡的游戏流程一步都没跑 -> 目标躺尸（只能等兜底）。
            //   修法：不再"自己注入 + 跳过原函数"，而是**把这一发的射线掰到目标身上**
            //     （改写 WPN_Gun.Damage 的 rayDir 参数），原函数原样跑完 ——
            //     命中判定 / 伤害 / DeathEventBroadcast / 击杀提示 / 复活调度
            //     全部是游戏自己的代码，我们一行都不再插手伤害与死亡。
            //   保险（不会双倍伤害）：onLeave 里核对目标血量，只有原版这一发真的没打掉血
            //     （被墙挡 / 目标无敌 / 没命中）才用老的注入路径补一发。
            //   安全：写栈之前先校验参数"像不像 (weapon, origin, dir)"，不像就自动退回注入。
            //   false = 回到旧行为（自己注入 + 跳过原函数）。
            gun_ray_redirect: true,

            // ---- 复活兜底的重试策略（2026-10-15：不再"调用成功就算成功"）----
            //   实测 bug：兜底调用没抛异常就置 rescued=true，目标其实还死着也不再补 ->
            //   日志指纹 "兜底=已补发但没活 tries=1"，目标一直躺到本局结束。
            //   现在改成"isDead 真的变 false 才算成功"，否则按间隔继续补。
            death_rescue_max_tries: 6,       // 同一个目标最多补几次
            death_rescue_retry_gap_ms: 3000, // 两次补之间的最小间隔（别把游戏自己的复活计时重置掉）
            // 死亡链观察：在 GameManager.TakeDamage 上装只读进出钩子（默认关，取证才开）。
            //   开了以后日志里会出现 [deathDiag:chain] "本次调用内死亡广播次数=N"，
            //   N=0 就是我们注入的伤害没有触发游戏死亡流程的铁证。
            death_diag_chain: false,

            // 其它
            local_eye_height: 1.55,
            chest_fallback_height: 1.1,
            target_cache_ms: 25,

            // ---- 弹体追踪（制导）：让手雷/RPG/榴弹枪/奥术手雷/火球朝敌人拐弯 ----
            // 注意：这一组只控制"拐弯"，**不注入任何伤害**。
            // 伤害完全交给原版：弹体撞到人/墙 -> WPN_GRENADE.CreateExplosion 结算。
            homing_speed: 0.0,          // 0 = 用弹体自身的 shootSpeed（MissileData.velocity）
            homing_turn: 1.0,           // 0.05~1.0，每个物理步把方向掰向目标的力度
                                        //   1.0 = 直接锁定（立刻拐弯，命中率最高）
                                        //   0.4 = 慢慢拐（保留抛物弧线，更像原版手感）
            homing_retarget: true,      // 原目标死了自动改追最近的敌人
            homing_max_ms: 20000,       // 超过这个时间放弃制导（防指针复用/泄漏）
            homing_pending_ms: 800,     // "开火记录 -> 弹体生成"的最大时间差（配对窗口）

            // ---- 弹体追踪的"打谁"策略：**准星锥内距离最近的敌人** ----
            //   弹体追踪**不读** config.target_mode（那是枪械直伤用的），只认下面两个键。
            //
            //   homing_cone_deg = 0  -> 关闭准星锥，回到旧的"全场最近"
            //   homing_cone_deg > 0  -> 先只保留「锥轴 与 参考点->目标 夹角 <= 该值」的敌人，
            //                          锥内再比距离取最近的那个。
            //
            //   锥轴（发射时）  = 本地玩家相机朝向，锥心 = 眼睛位置
            //                     （准星锥必须从眼睛量；用脚底量在几何上不成立）
            //   锥轴（中途换目标）= 弹体当前速度方向，锥心 = 弹体位置
            //                     用速度而不是玩家准星：弹体已经飞出去了，玩家可能早就看别处；
            //                     用速度还能避免弹体在半空 180° 掉头，观感更自然。
            homing_cone_deg: 30.0,
            // 锥内一个敌人都没有时怎么办：
            //   true （默认）= 回退成"全场最近"，保住"对着空气扔雷也能追到人"
            //   false        = 这颗弹不追踪，按原弹道直飞（严格"只追我瞄的人"）
            homing_cone_fallback: true,

            // ---- death_diag：击杀之后“到底有没有复活” ----
            //   2.7 实测日志指纹：[fail:applyDamage:gun] system error
            //   —— 我们合成的 GameManager.TakeDamage 在被击杀那一刻抛托管异常，
            //      按 §3.2 的结论会打断 DeathEventBroadcast -> 目标 isDead=true 但
            //      “复活调度”没跑 -> 死了不复活、模型卡在原地。
            //   所以默认开启这一组只读诊断：死亡广播进出 / RespawnPlayer / Player.Respawn
            //   + 击杀后观察窗口。全部只读，不改变任何游戏行为。
            death_diag: true,          // 总开关（关掉后连诊断钩子都不装）
            death_diag_ms: 20000,      // 击杀后观察窗口：超过这个时间还没复活就报“不复活”
            death_diag_detail: false,  // true = 每次死亡广播/复活调度都逐条打印（很吵）
            // ★2026-10-14 闪退修复：托管异常漏斗探针默认关闭。
            //   true = 在 il2cpp::vm::Exception::Raise(+0x13FF10) 上装 Frida 钩子（取证用），
            //   会让本该 unwind 的托管异常直接返回 -> int 3 -> 0x80000003 秒退。
            //   详见 installRaiseProbe() 上方注释与 06-测试/_crash18_26/。
            death_diag_raise: false,
            // ---- death_fix_wpn：已被 20261014 日志证伪，默认关闭 ----
            //   IDA 实测 DeathEventData.get_wpnName(+0xB3D6C0)：查的就是
            //     GameManager.WpnDataDictionary[eventData.wpnIndex]。
            //   但 20261014 13:29:53.235 的 wpnIndex=341 炸了，13:29:54.231 的同一个
            //   341 却正常返回；而且 wpnFix=0（341 在字典里查得到）——
            //   说明"wpnIndex 非法"不是这次广播被打断的原因。改它只会污染击杀提示，
            //   所以代码保留、默认关掉，要复现旧实验时手动打开。
            death_fix_wpn: false,
            // ---- death_fix_respawn：复活兜底（默认开）----
            //   死亡广播一旦被异常打断，ModeBase_Nano.RespawnPlayer 根本不会被调用，
            //   目标会一直 isDead=true 躺在原地直到本局结束（20261014 实测 4 次）。
            //   这里在"目标死亡超过 death_respawn_grace_ms 还没排进复活"时，
            //   由我们补一次 ModeBase_Nano.RespawnPlayer，把它拉回战场。
            //   只在游戏主线程（开火钩子 / 死亡广播 onLeave）里跑，每次都会写 [deathFix] 日志。
            death_fix_respawn: true,
            death_respawn_grace_ms: 6000,  // 等多久还没复活才兜底（毫秒）
            // ---- death_fix_broadcast：补发死亡广播（2026-10-15 新增，默认开）----
            //   2026-10-15 实测（08:48:03 / 08:48:04 两次）：
            //     [fail:applyDamage:gun@takeDamage] applyDamage:gun@takeDamage: system error
            //   即我们合成的 GameManager.TakeDamage 在击杀那一刻抛了托管异常，而且异常发生在
            //   GameManager.DeathEventBroadcast 之前 —— 那一次死亡的游戏流程一步都没跑：
            //   没有 deathIn / deathOut，也没有 ModeBase_Nano.RespawnPlayer 调度，
            //   目标就永远 isDead=true 卡在原地（21 笔死亡里 3 笔，全是"不复活"的那 3 笔）。
            //   修法：既然这笔死亡的游戏流程被异常跳过了，就用同一份字段把游戏自己的
            //   GameManager.DeathEventBroadcast(eventData) 补调一次（cdecl + 0x38 字节按值结构体，
            //   数据布局和游戏广播出来的一模一样）——击杀提示 / 模式记账 / 复活调度全部
            //   回到游戏原流程，不需要我们代劳复活。
            //   false = 只靠 death_fix_respawn 兜底（复活慢 6 秒）。
            death_fix_broadcast: true,

            // 调试（2.7 正式版默认全部关闭；出问题时用 setConfig 临时打开取证）
            diagnostic_log: false,
            log_every: 20,
            // verbose_probe=false 时 installPipelineProbes() 连钩子都不装 -> 钩子更少更稳
            verbose_probe: false,
            log_to_file: false,     // 不在游戏目录写日志文件
            log_file: ''            // 由调用方下发；为空则只走内存缓冲 + UI
        },
        cache: {
            eventBuf: null,
            posBuf: null,
            // 原版 DamageEventData 底板（0x48 字节），由 DamageEventData.TakePlace 钩子写入
            eventTemplate: null,
            eventTemplateValid: false,
            eventTemplateAt: 0,
            eventTemplateWpnIndex: -1,
            outDataBuf: null,
            wpnIndexWarned: false,
            emptyString: null,
            ownPlayer: ptr(0),
            hitTag: ptr(0),
            hitSnd: ptr(0),
            hitFx: ptr(0),
            capturedTag: false,
            selectedTarget: null,
            selectedAtMs: 0,
            // death_fix_broadcast：当场补发失败（抛异常）的死亡广播先排队，
            // 等下一个"游戏主线程、且不在异常栈上"的时机再补一次。
            rebroadcastQueue: null,
            // 游戏自己调用 DeathEventBroadcast 时压栈的 MethodInfo*（结构体后面那个）。
            // 补发时带上真实值，少一个未知量。
            deathMethodInfo: null,
            // 原生射线接管：参数不像射线时只记一次告警日志
            rayWarnLogged: false
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
            gunSkipped: 0,          // attach 模式：成功"模拟 ret"跳过原函数（= 我们接管了这发）
            gunSkipFailed: 0,       // attach 模式：返回地址校验失败没跳过（原函数照跑，最多多打一遍，不冒险跳栈）
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
            ownPlayerSource: '',
            // ---- 弹体追踪计数器（日志里搜 [probe:beat] 的 missile= 段） ----
            missileSpawns: 0,      // SetWeaponData 被调用次数 = 观察到几颗弹生成
            missileNotMine: 0,     // 弹体是别人发射的（不制导）
            missileNoPending: 0,   // 弹体生成了但没抓到开火记录（配对失败）
            missileSwitchOff: 0,   // 类别子开关关掉了
            missileNoTarget: 0,    // 没有可选目标（场上没敌人）
            homingArmed: 0,        // 有多少颗自己的弹体被登记为"要制导"
            homingSteered: 0,      // 实际改写速度/朝向的次数
            homingDropped: 0,      // 目标死亡/超时后放弃的次数
            homingForgotten: 0,    // 弹体爆炸/回收/被复用，清掉记录次数
            missileLaunchSeen: 0,  // Work() 被调用次数（弹体真的发射了）
            missileHitSeen: 0,     // 弹体 OnCollisionEnter 次数（只记账，不再清记录）
            missileTriggerSeen: 0, // 弹体 OnTriggerEnter 次数（只记账）
            // ---- 追踪排查：steer 为什么没写进去 / 记录被什么清掉 ----
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
            forgetHit: 0,
            forgetHitGrenade: 0,
            forgetTrigger: 0,
            forgetTimeout: 0,
            forgetLost: 0,
            forgetNoNext: 0,
            forgetIdentity: 0,
            // ---- 弹体追踪的"打谁"策略计数（准星锥） ----
            coneHit: 0,            // 锥内选到目标（发射时 + 中途换目标都算）
            coneEmpty: 0,          // 锥内一个敌人都没有
            coneFallback: 0,       // 锥内没人 -> 回退成全场最近
            coneEmptyStrict: 0,    // 锥内没人且关掉了回退 -> 放弃追踪
            coneOff: 0,            // homing_cone_deg = 0，没启用锥
            coneAxisFail: 0,       // 读不到相机朝向/弹体速度 -> 退回全场最近
            coneRetarget: 0,       // 中途换目标时用了锥并选中
            entryFallback: 0,      // 统一入口没生效、自动降级用 hurt 的次数
            templateCaptured: 0,   // 抄到原版事件底板的次数
            templateUsed: 0,       // 用底板合成事件的次数
            templateRejected: 0,   // 底板不可用 / wpnIndex 非法而拒绝注入的次数
            invincibleCleared: 0,  // 注入前清掉目标无敌/减伤状态的次数
            deathIn: 0,            // DeathEventBroadcast 进入次数
            deathOut: 0,           // DeathEventBroadcast 正常返回次数（<deathIn 就是抛异常了）
            respawnScheduled: 0,   // ModeBase_Nano.RespawnPlayer 命中次数（复活调度有没有被调用）
            playerRespawnCalls: 0, // Player.Respawn 命中次数（真正排进复活协程）
            halfDeadWatched: 0,    // 击杀后进入观察窗口的目标数
            halfDeadRecovered: 0,  // 观察窗口内确认复活的目标数
            halfDeadConfirmed: 0,  // 观察窗口结束仍未复活的目标数（=“不复活”的直接证据）
            halfDeadActive: 0,     // 当前仍在观察的目标数
            lastFailPhase: '',     // 最近一次 applyDamage 异常发生在哪一步
            deathWpnFixed: 0,      // 死亡广播里被修正掉的非法 wpnIndex 次数（旧假设，默认关闭）
            deathAborted: 0,       // 死亡广播「进了没出」的次数（= 被托管异常打断，目标不会复活）
            deathRescued: 0,       // 复活兜底真正补发 RespawnPlayer 的次数
            deathRescueRejected: 0,  // 兜底前被"不是有效玩家"闸门拦下的次数（2026-10-14 新增）
            deathRebroadcast: 0,   // 死亡广播"根本没跑"时由我们补发的次数（2026-10-15 新增）
            deathRescueFailed: 0,  // 复活兜底调用抛异常的次数
            // ---- 2026-10-15 原生射线接管（gun_ray_redirect） ----
            rayRedirectShots: 0,   // "把射线掰到目标身上"的尝试次数
            rayRedirectHits: 0,    // 接管后原版真的打掉了血 = 这一发走的是完整游戏流程
            rayRedirectMiss: 0,    // 接管后原版没打掉血 -> 退回我们自己的注入
            rayRedirectBadArgs: 0, // 参数不像一条射线 -> 不写栈，直接退回注入
            // ---- 2026-10-15 复活兜底重试 ----
            deathRescueAttempts: 0, // 兜底实际调用次数（含重试；旧版只调用一次就不再管）
            // ---- 2026-10-15 补发广播队列 ----
            rebroadcastDeferred: 0,   // 当场补发失败、排进队列的次数
            rebroadcastDeferredOk: 0, // 延迟补发真正成功的次数
            // ---- 2026-10-15 死亡链观察（death_diag_chain） ----
            chainTakeDamageCalls: 0,  // 我们注入的 TakeDamage 调用次数
            chainBroadcastInside: 0,  // 上述调用内部真的发生了死亡广播的次数
            raiseCount: 0,         // 托管异常抛出次数（Il2Cpp_Exception_Raise 命中）
            hitFxIn: 0,            // PlayHitFxAndSnd 进入次数
            hitFxOut: 0,           // PlayHitFxAndSnd 正常返回次数

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
        getNanoRole: null,
        getWpnData: null,
        getVelocity: null,
        setVelocity: null,
        lookRotation: null,
        setRotation: null,
        gunDamageOriginal: null,
        gmTakeDamage: null,
        entityHurt: null,
        playerHurt: null,
        healthHurt: null,
        deathBroadcast: null
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
            // 诊断用：Player.get_nanoRole()，复活时区分幽灵/终结者
            native.getNanoRole = new NativeFunction(base.add(RVA.Player_get_nanoRole), 'int32', ['pointer', 'pointer'], CALL_CONV);
            // GameManager.GetWpnData(int weaponIndex, out WeaponData data)
            //   -> bool，内部是 Dictionary.TryGetValue，查不到只返回 false
            native.getWpnData = new NativeFunction(
                base.add(RVA.GameManager_GetWpnData), 'bool', ['int32', 'pointer', 'pointer'], CALL_CONV
            );

            // 弹体追踪：Rigidbody.velocity / Quaternion.LookRotation / Transform.rotation
            // Vector3(12B)、Quaternion(16B) 都是按值压栈的 struct，同样拆成 4 字节标量。
            // get_velocity 走 Injected 版本（out Vector3*），避免按值返回 struct。
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

            // 复活兜底用的两个入口（只在 death_fix_respawn 打开时才会被调用）
            //   ModeBase_Nano.RespawnPlayer(ModeBase_Nano*, Player*, int respawnTime, bool isNormal, bool clearExp)
            native.respawnPlayer = new NativeFunction(
                base.add(RVA.ModeBase_Nano_RespawnPlayer), 'void',
                ['pointer', 'pointer', 'int32', 'uint', 'uint', 'pointer'], CALL_CONV
            );
            //   Player.Respawn(Player*, float respawnTime, float invisibleTime)
            native.playerRespawn = new NativeFunction(
                base.add(RVA.Player_Respawn), 'void',
                ['pointer', 'float', 'float', 'pointer'], CALL_CONV
            );

            // 死亡广播补发（death_fix_broadcast 用）：
            //   GameManager.DeathEventBroadcast(DeathEventData eventData, const MethodInfo* method)
            //   IDA 实测签名：void __cdecl GameManager__DeathEventBroadcast(DeathEventData_o eventData,
            //   const MethodInfo *method) —— 无 this（静态），0x38 字节结构体按值压栈
            //   = 14 个 dword + method。字段顺序与 deathEventFields() 读的 OFF.Death_* 完全一致。
            native.deathBroadcast = new NativeFunction(
                base.add(RVA.GameManager_DeathEventBroadcast), 'void',
                ['uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint',
                 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'pointer'],
                CALL_CONV
            );

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

    // ------------------------------------------------------------------
    // 合成事件里"必须合法"的字段 —— 本轮真正的修复点
    // ------------------------------------------------------------------
    //   事故（日志 + IDA 反汇编共同定位）：手工合成事件时 wpnIndex 填了 0，于是
    //     GameManager.DeathEventBroadcast -> GameManager_DeathEvent$$Invoke
    //       -> HUD_KillMark -> DeathEventData.get_wpnName()/get_killMsgIcon()
    //   内部做的是字典查找 GameManager.WpnDataDictionary[wpnIndex]
    //   （Dictionary<int, WeaponData>），反汇编就是
    //     if (!dict || get_Item(dict, wpnIndex) == 0) il2cpp_raise_exception();
    //   key 不在字典里 -> KeyNotFoundException；这条异常从 HUD 订阅者冒出来，
    //   直接打断整条死亡广播链，后果：
    //     a) 敌人 HP 归零、isDead=true，但复活调度没跑 -> 敌人死了不复活；
    //     b) 多人生化模式下同一条异常把游戏带崩 -> 闪退。
    //   ==> wpnIndex 必须填 WeaponData.wpnIndex（字典里真实存在的 key）；
    //       wpnSprIndex 可以留 0（WeaponData.GetKillMsgIcon 反汇编直接
    //       return spriteAsset.killMsgIcon，没用这个参数）；
    //       hitTag / hitSndName 留 null 也安全（原版 WPN_Gun.Damage 自己就是先
    //       memset(event, 0, 0x48) 再按需填，null 正是原版默认值）。
    function readWeaponWpnIndex(weapon) {
        try {
            if (isNull(weapon)) return -1;
            var data = weapon.add(OFF.Weapon_data).readPointer();
            if (!readable(data)) return -1;
            return data.add(OFF.WeaponData_wpnIndex).readS32();
        } catch (_) { return -1; }
    }

    function readWeaponHitEffectName(weapon) {
        try {
            if (isNull(weapon)) return ptr(0);
            var data = weapon.add(OFF.Weapon_data).readPointer();
            if (!readable(data)) return ptr(0);
            // hitEffectName 挂在 WeaponData(ScriptableObject) 上，是常驻资源对象，
            // 生命周期远长于一次伤害事件，不会 use-after-free。
            var name = data.add(OFF.WeaponData_hitEffectName).readPointer();
            return readable(name) ? name : ptr(0);
        } catch (_) { return ptr(0); }
    }

    // 原版事件底板：**只抄标量 wpnIndex**。
    // 不抄结构体里的字符串指针 —— 那些指针的生命周期不由我们掌握，
    // 缓存下来当长期值用有 use-after-free 风险。
    //   来源 1：DamageEventData.TakePlace(this) —— 原版每次开火都会走到（this 就是结构体指针）
    //   来源 2：GameManager.TakeDamage 入口（[esp+4] 就是按值传入的结构体本体）
    function captureEventTemplate(eventPtr, from) {
        try {
            if (!Runtime.config.use_event_template) return false;
            if (Runtime.inDirectDamage) return false;   // 我们自己合成的事件不算原版
            if (!readable(eventPtr)) return false;
            var attacker = eventPtr.add(OFF.Dmg_attacker).readPointer();
            if (isNull(attacker)) return false;
            var wpnIndex = eventPtr.add(OFF.Dmg_wpnIndex).readS32();
            if (wpnIndex <= 0 || wpnIndex > 0xFFFF) return false;
            Runtime.cache.eventTemplateValid = true;
            Runtime.cache.eventTemplateAt = Date.now();
            Runtime.cache.eventTemplateWpnIndex = wpnIndex;
            Runtime.stats.templateCaptured += 1;
            if (Runtime.stats.templateCaptured <= 3) {
                probe('tpl', '原版事件 wpnIndex=' + wpnIndex + ' from ' + from +
                    ' (wpnSprIndex=' + eventPtr.add(OFF.Dmg_wpnSprIndex).readS32() +
                    ' damageTag=0x' + hex32(eventPtr.add(OFF.Dmg_damageTag).readU32()) +
                    ' type=' + eventPtr.add(OFF.Dmg_type).readS32() +
                    ' hitTag=' + fmtPtr(eventPtr.add(OFF.Dmg_hitTag).readPointer()) +
                    ' hitEffect=' + fmtPtr(eventPtr.add(OFF.Dmg_hitEffect).readPointer()) + ')');
            }
            return true;
        } catch (error) {
            fail('captureEventTemplate', error);
            return false;
        }
    }

    // 取一个"字典里一定存在"的 wpnIndex：
    //   1) 首选当前武器的 Weapon.data.wpnIndex（谁开的枪就用谁的武器）
    //   2) 读不到就用 5 秒内抄到的原版事件底板里的 wpnIndex
    //   3) 都拿不到 -> -1，调用方放弃这次注入
    // 用游戏自己的武器表验证 wpnIndex 是不是合法 key（见 RVA.GameManager_GetWpnData 注释）。
    //   true  = 字典里存在这个 key，可以安全注入
    //   false = 不存在，必须丢掉这个候选
    //   null  = 校验不可用（拿不到原生函数 / 调用异常），此时不拦截
    function checkWpnIndex(index) {
        try {
            if (!native.getWpnData) return null;
            if (!Runtime.cache.outDataBuf) Runtime.cache.outDataBuf = Memory.alloc(8);
            Runtime.cache.outDataBuf.writePointer(ptr(0));
            var raw = native.getWpnData(index | 0, Runtime.cache.outDataBuf, ptr(0));
            return toFlag(raw) ? true : false;
        } catch (error) {
            if (!Runtime.cache.wpnIndexWarned) {
                Runtime.cache.wpnIndexWarned = true;
                log('warn', '[probe:tpl] GameManager.GetWpnData 调用失败，本次跳过 wpnIndex 校验：' +
                    (error && error.message ? error.message : String(error)));
            }
            return null;
        }
    }

    // 选一个"游戏武器表里确实存在"的 wpnIndex：
    //   候选 1：当前武器的 Weapon.data(0x68) -> WeaponData.wpnIndex(0x0C)
    //           （Weapon.data 是游戏自己在用的：WPN_Gun.Damage 第一句就是 if (this->fields.data)）
    //   候选 2：5 秒内抄到的原版伤害事件里的 wpnIndex（原版自己填的，一定是合法 key）
    //   两个候选都会被 GameManager.GetWpnData 实查一遍，查不到就丢；全丢光就返回 -1，
    //   调用方放弃这次注入（宁可不打，也绝不让死亡广播里 WpnDataDictionary[wpnIndex] 抛异常）。
    function resolveWpnIndex(weapon) {
        var candidates = [];
        var fromWeapon = readWeaponWpnIndex(weapon);
        if (fromWeapon > 0 && fromWeapon <= 0xFFFF) {
            candidates.push({ value: fromWeapon, from: 'Weapon.data' });
        }
        if (Runtime.cache.eventTemplateValid &&
            Runtime.cache.eventTemplateWpnIndex > 0 &&
            (Date.now() - Runtime.cache.eventTemplateAt) <= 5000) {
            candidates.push({ value: Runtime.cache.eventTemplateWpnIndex, from: '原版事件' });
        }
        for (var i = 0; i < candidates.length; i += 1) {
            var valid = checkWpnIndex(candidates[i].value);
            if (valid === false) {
                probe('tpl', 'wpnIndex=' + candidates[i].value + '（来源 ' + candidates[i].from +
                    '）不在 GameManager.WpnDataDictionary 里 -> 丢弃这个候选');
                continue;
            }
            return candidates[i].value;
        }
        return -1;
    }

    // ------------------------------------------------------------------
    // 复活无敌（本轮修复：复活后打不动 / 掉血却不死）
    // ------------------------------------------------------------------
    //   实测日志（09:27:32 复活之后那一段）：
    //     [probe:gmTakeDamage] damage=105.00 type=1 [ours]   <- 我们传进去的是 105
    //     [probe:playerHurt]   damage=0.00   type=1 [ours]   <- 观察者链把它改成了 0
    //     [probe:healthHurt]   value=0                       <- Hurt(health, 0) 自然不掉血
    //   即：游戏自己的 DamageEvent 观察者链把伤害抹成了 0。dump.cs 里对应三样东西：
    //     Entity.damageRate(+0x14)             SetDamageRate() 产生的减伤倍率
    //     Entity.isInvincible(+0x18)           InvincibleBuff 通过 RefBool 写的无敌标记
    //     HealthData.invinsibleEndTime(+0x44)  复活无敌的结束时间戳
    //   而 DamageEventData 里游戏自己留了一个开关 ignoreDmgRate(+0x44)，
    //   语义就是"这次伤害忽略目标的减伤"—— 我们直接用它。
    //   同时在注入前把目标的无敌状态清掉，保证第一次走完整入口就能把人打死。
    function readTargetDefense(victim) {
        var info = { isInvincible: -1, invEnd: -1, damageRate: -1, err: '' };
        try {
            info.isInvincible = victim.add(OFF.Entity_isInvincible).readU8();
            info.damageRate = victim.add(OFF.Entity_damageRate).readFloat();
            var hp = victim.add(OFF.Entity_healthData).readPointer();
            if (readable(hp)) info.invEnd = hp.add(OFF.HealthData_invinsibleEndTime).readFloat();
        } catch (error) {
            info.err = (error && error.message) ? error.message : String(error);
        }
        return info;
    }

    // 清掉目标的无敌状态（复活无敌）。返回清除前的值，日志里能直接看到是不是它在挡。
    function clearTargetInvincibility(victim) {
        var before = readTargetDefense(victim);
        try { victim.add(OFF.Entity_isInvincible).writeU8(0); } catch (_) {}
        try {
            var hp = victim.add(OFF.Entity_healthData).readPointer();
            if (readable(hp)) hp.add(OFF.HealthData_invinsibleEndTime).writeFloat(0);
        } catch (_) {}
        return before;
    }

    // 把 DamageEventData 写进缓冲区，再拆成 18 个 4 字节标量（cdecl 压栈布局）。
    // 返回 null = 合成不出安全事件，调用方必须放弃注入走原版弹道。
    function buildEventDwords(attacker, victim, damage, dmgType, origin, hitPos, weapon) {
        var buf = Runtime.cache.eventBuf;

        var wpnIndex = resolveWpnIndex(weapon);
        if (wpnIndex <= 0) {
            Runtime.stats.templateRejected += 1;
            probe('tpl', 'refuse to inject: no valid wpnIndex, weapon=' + fmtPtr(weapon));
            return null;
        }

        buf.add(OFF.Dmg_attacker).writePointer(attacker);
        buf.add(OFF.Dmg_victim).writePointer(victim);
        buf.add(OFF.Dmg_damage).writeFloat(damage);

        buf.add(OFF.Dmg_origin).writeFloat(origin.x);
        buf.add(OFF.Dmg_origin + 4).writeFloat(origin.y);
        buf.add(OFF.Dmg_origin + 8).writeFloat(origin.z);

        buf.add(OFF.Dmg_hitPos).writeFloat(hitPos.x);
        buf.add(OFF.Dmg_hitPos + 4).writeFloat(hitPos.y);
        buf.add(OFF.Dmg_hitPos + 8).writeFloat(hitPos.z);

        // hitTag/hitSndName 用 null（原版 memset 之后的默认值）；
        // hitEffect 用武器自己的常驻特效名（WeaponData.hitEffectName）。
        buf.add(OFF.Dmg_hitTag).writePointer(ptr(0));
        buf.add(OFF.Dmg_hitSndName).writePointer(ptr(0));
        buf.add(OFF.Dmg_hitEffect).writePointer(readWeaponHitEffectName(weapon));

        buf.add(OFF.Dmg_wallThrough).writeU8(0);
        buf.add(OFF.Dmg_type).writeS32(dmgType);
        buf.add(OFF.Dmg_damageTag).writeS32(0);
        buf.add(OFF.Dmg_wpnIndex).writeS32(wpnIndex);   // <-- 本轮修复核心
        buf.add(OFF.Dmg_wpnSprIndex).writeS32(0);
        // <-- 本轮修复：让这次伤害忽略目标的减伤/复活无敌（Entity.damageRate）。
        //     复活后游戏会把目标的 damageRate 压到 0，观察者链随即把 data.damage 抹成 0，
        //     表现就是"打中了但不掉血"。ignoreDmgRate 是游戏自己留的开关。
        buf.add(OFF.Dmg_ignoreDmgRate).writeU8(1);

        Runtime.stats.templateUsed += 1;
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

    // ------------------------------------------------------------------
    // DeathEventData（0x38 字节）合成 + 死亡广播补发
    // ------------------------------------------------------------------
    //   字段顺序完全照 deathEventFields() 读的那套 OFF.Death_*（也就是游戏自己
    //   广播出来的结构）。wpnIndex 必须是 WpnDataDictionary 里查得到的 key ——
    //   广播里的 HUD_KillMark/HUD_KillMsg 会查它，查不到会抛 KeyNotFoundException
    //   （和 DamageEventData 是同一条经验，见 buildEventDwords 的注释）。
    function buildDeathEventDwords(attacker, victim, dmgType, origin, weapon) {
        if (!Runtime.cache.deathBuf) Runtime.cache.deathBuf = Memory.alloc(OFF.Death_size + 16);
        var buf = Runtime.cache.deathBuf;
        var wpnIndex = resolveWpnIndex(weapon);
        if (wpnIndex <= 0) return null;
        var o = origin || { x: 0, y: 0, z: 0 };
        buf.add(OFF.Death_killer).writePointer(attacker);
        buf.add(OFF.Death_dead).writePointer(victim);
        buf.add(OFF.Death_headShot).writeS32(0);
        buf.add(OFF.Death_wallThrough).writeU8(0);
        buf.add(OFF.Death_damageType).writeS32(dmgType);
        buf.add(OFF.Death_damageOrigin).writeFloat(o.x);
        buf.add(OFF.Death_damageOrigin + 4).writeFloat(o.y);
        buf.add(OFF.Death_damageOrigin + 8).writeFloat(o.z);
        buf.add(OFF.Death_specialKill).writeS32(0);
        buf.add(OFF.Death_nanoKill).writeS32(0);
        buf.add(OFF.Death_revenge).writeU8(0);
        buf.add(OFF.Death_damageTag).writeU32(0);
        buf.add(OFF.Death_wpnIndex).writeS32(wpnIndex);
        buf.add(OFF.Death_wpnSprIndex).writeS32(0);
        var dwords = new Array(14);
        for (var i = 0; i < 14; i += 1) dwords[i] = buf.add(i * 4).readU32();
        return dwords;
    }

    // ------------------------------------------------------------------
    // 死亡广播补发（death_fix_broadcast）
    // ------------------------------------------------------------------
    //   为什么需要：buildEventDwords 走的是 WPN_Gun.Damage 的前半截
    //   （GameManager.TakeDamage = 扣血），"击杀提示/模式记账/复活调度"在原函数后半截。
    //   2026-10-15 实测：当场补发 100% 抛 system error，而且目标连广播的 onEnter 都没进。
    //   所以现在是两段式：
    //     1) 当场补一次（能成最好）；
    //     2) 失败就排队（rebroadcastQueue），在下一个"游戏主线程、且不在异常栈上"的
    //        时机（开火钩子 / 广播 onLeave）再补；
    //   并且用 [fail:deathFix:broadcast@step] 把"到底哪一句抛的"记进日志名（step =
    //   noKiller / build / call），下一次测试一眼定案。
    // ------------------------------------------------------------------
    function doRebroadcast(rec, tag) {
        var step = 'getMine';
        try {
            var killer = getMyPlayer();
            if (isNull(killer)) { step = 'noKiller'; return false; }
            step = 'build';
            var dd = buildDeathEventDwords(rec.attacker || killer, rec.victim, rec.dmgType, rec.origin, rec.weapon);
            if (!dd) {
                log('warn', '[deathFix] 死亡广播被异常跳过，但 wpnIndex 不可用，放弃补发: victim=' + fmtPtr(rec.victim));
                return false;
            }
            step = 'call';
            // method 参数优先用"游戏自己调用时压栈的那一个"（广播 onEnter 里抄下来的），
            // 抄不到才退回 NULL —— 少一个未知量。
            var method = Runtime.cache.deathMethodInfo || ptr(0);
            native.deathBroadcast(
                dd[0], dd[1], dd[2], dd[3], dd[4], dd[5], dd[6],
                dd[7], dd[8], dd[9], dd[10], dd[11], dd[12], dd[13], method
            );
            Runtime.stats.deathRebroadcast += 1;
            log('warn', '[deathFix] 已补发游戏自己的 DeathEventBroadcast（' + tag + '）: victim=' +
                fmtPtr(rec.victim) + '（击杀提示/模式记账/复活调度走游戏原流程）');
            return true;
        } catch (error) {
            fail('deathFix:broadcast@' + step, error);
            return false;
        }
    }

    function queueRebroadcast(rec) {
        try {
            if (!Runtime.cache.rebroadcastQueue) Runtime.cache.rebroadcastQueue = [];
            var q = Runtime.cache.rebroadcastQueue;
            for (var i = 0; i < q.length; i += 1) {
                if (samePointer(q[i].victim, rec.victim)) { q[i] = rec; return; }   // 同一目标只留最新一条
            }
            q.push(rec);
            if (q.length > 8) q.splice(0, q.length - 8);
            Runtime.stats.rebroadcastDeferred += 1;
            log('warn', '[deathFix] 当场补发失败，已排队稍后重试（队列=' + q.length + '）: victim=' +
                fmtPtr(rec.victim));
        } catch (error) { fail('deathFix:queue', error); }
    }

    // 在"游戏主线程、且不在异常栈上"的时机处理补发队列
    function drainRebroadcastQueue() {
        try {
            var q = Runtime.cache.rebroadcastQueue;
            if (!q || !q.length) return 0;
            if (!native.deathBroadcast) { Runtime.cache.rebroadcastQueue = null; return 0; }
            var now = Date.now();
            var keep = [];
            var done = 0;
            for (var i = 0; i < q.length; i += 1) {
                var rec = q[i];
                if (now - rec.at > 30000 || rec.tries >= 3) continue;      // 过期 / 试够了
                var deadNow = null;
                try { deadNow = toFlag(native.isDead(rec.victim, ptr(0))); } catch (_) { deadNow = null; }
                if (deadNow !== true) continue;                            // 已经活了 / 读不到 -> 不动手
                if (Runtime.currentDeathKey === rec.victim.toString()) { keep.push(rec); continue; }
                if (!isPlausibleVictim(rec.victim)) continue;              // 指针已被回收 -> 丢掉
                rec.tries += 1;
                rec.at = now;
                if (doRebroadcast(rec, 'deferred#' + rec.tries)) {
                    Runtime.stats.rebroadcastDeferredOk += 1;
                    done += 1;
                } else if (rec.tries < 3) {
                    keep.push(rec);
                }
            }
            Runtime.cache.rebroadcastQueue = keep;
            return done;
        } catch (error) {
            fail('deathFix:drain', error);
            return 0;
        }
    }

    // GameManager.TakeDamage 抛异常 -> 这笔死亡的广播可能压根没跑 -> 补一次
    //   只在同时满足下面几条时才补（任何一条不满足都宁可不补，交给 death_fix_respawn 兜底）：
    //     1) death_fix_broadcast + death_diag 都开着；
    //     2) 异常发生在"完整入口"阶段（takeDamage / retryTakeDamage）——
    //        只有这条路会经过死亡广播，其它入口本来就不广播；
    //     3) 这笔死亡确实"没广播过"：currentDeathKey 不是它，观察窗口里也没有 note='deathIn'；
    //     4) 目标通过 isPlausibleVictim 硬闸门（防止把哨戒炮/已回收指针塞进游戏函数）。
    function maybeBroadcastSkippedDeath(victim, dmgType, origin, weapon, phase) {
        if (!Runtime.config.death_fix_broadcast) return false;
        if (!Runtime.config.death_diag) return false;
        if (isNull(victim) || !native.deathBroadcast) return false;
        if (phase !== 'takeDamage' && phase !== 'retryTakeDamage') return false;
        var key = victim.toString();
        if (Runtime.currentDeathKey === key) return false;
        var entry = Runtime.deathWatch[key];
        if (entry && entry.note === 'deathIn') return false;
        if (!isPlausibleVictim(victim)) return false;
        var rec = { victim: victim, dmgType: dmgType, origin: origin, weapon: weapon, at: Date.now(), tries: 0 };
        if (doRebroadcast(rec, 'phase=' + phase)) return true;
        queueRebroadcast(rec);
        return false;
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

    // 判定"这次伤害有没有让目标掉血/死亡"
    function hpDroppedBetween(before, after) {
        if (before.rate >= 0 && after.rate >= 0) {
            return (after.rate < before.rate) || toFlag(after.dead);
        }
        return before.raw !== after.raw;
    }

    function applyDamage(target, damage, dmgType, sourceLabel, weapon) {
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
        var defense = null;
        // 异常定位用：记录最近一次进入的子步骤，catch 时写进 [fail:...] 名字里。
        var phase = 'init';

        try {
            // 只有走完整入口（GameManager.TakeDamage）时才需要处理复活无敌：
            // 观察者链会按目标的 damageRate / isInvincible 把 data.damage 抹成 0。
            if (entry === DAMAGE_ENTRY.GAME_MANAGER) {
                phase = 'clearInvincible';
                defense = clearTargetInvincibility(target.player);
                // 计数只在"确实清掉了东西"时 +1，这样 UI 上的「清无敌」才有意义
                if (defense.isInvincible === 1 || defense.invEnd > 0 ||
                    (defense.damageRate >= 0 && defense.damageRate < 0.999)) {
                    Runtime.stats.invincibleCleared += 1;
                    probe('inv', '目标处于减伤/无敌状态，已清除: isInvincible=' + defense.isInvincible +
                        ' invinsibleEndTime=' + defense.invEnd.toFixed(2) +
                        ' damageRate=' + defense.damageRate.toFixed(3) +
                        ' victim=' + fmtPtr(target.player));
                }
            }
            if (entry === DAMAGE_ENTRY.HEALTH) {
                var health = target.player.add(OFF.Entity_healthData).readPointer();
                if (!readable(health)) {
                    probe('apply', 'ABORT: healthData unreadable for ' + fmtPtr(target.player));
                    return false;
                }
                probe('apply', 'call HealthData.Hurt(hp=' + fmtPtr(health) + ', value=' + (damage | 0) + ')');
                native.healthHurt(health, damage | 0, ptr(0));
            } else {
                phase = 'buildEvent';
                var dwords = buildEventDwords(
                    myPlayer, target.player, damage, dmgType, eyePos, target.pos, weapon
                );
                // 合成不出安全事件（读不到合法的 wpnIndex）时宁可不打这一枪：
                // 把 wpnIndex=0 丢进死亡广播会抛 KeyNotFoundException，
                // 后果就是敌人死了不复活 / 多人生化闪退。
                if (!dwords) {
                    Runtime.stats.lastResult = 'refused: no valid wpnIndex (' + sourceLabel + ')';
                    probe('apply', 'ABORT: buildEventDwords returned null (no valid wpnIndex)');
                    return false;
                }
                if (entry === DAMAGE_ENTRY.HURT) {
                    phase = 'callPlayerHurt';
                    probe('apply', 'call Player.OnEntityHurt(victim=' + fmtPtr(target.player) +
                        ', damage=' + damage.toFixed(2) + ', type=' + dmgType + ')');
                    callPlayerHurt(target.player, dwords);
                } else {
                    phase = 'takeDamage';
                    probe('apply', 'call GameManager.TakeDamage(damage=' + damage.toFixed(2) +
                        ', type=' + dmgType + ')');
                    callGameManagerTakeDamage(dwords);
                }
            }

            phase = 'snapshot';
            var after = readHealthSnapshot(target.player);
            var dropped = hpDroppedBetween(before, after);

            // 保险：统一入口被观察者否决时（HP 完全没变）**用完整入口再试一次**。
            //   ★ 绝对不要再退回 Player.OnEntityHurt / HealthData.Hurt：那条路只扣血、
            //     不走 DeathEventBroadcast，会把敌人打成"HP=0、isDead=true，但永远不死、
            //     也永远不复活"的幽灵；之后选目标逻辑把它当死人跳过，
            //     表现就是用户报的"敌人复活之后打不到、也不掉血"。
            //   重试前再清一次无敌状态，避免在两次调用之间 Buff 又把 isInvincible 写回去。
            if (!dropped && entry === DAMAGE_ENTRY.GAME_MANAGER &&
                Runtime.config.entry_fallback && dwords) {
                Runtime.stats.entryFallback += 1;
                phase = 'retryClearInvincible';
                var retryDefense = clearTargetInvincibility(target.player);
                log('warn', '[probe:hp] GameManager.TakeDamage 未生效（HP 没变），' +
                    '清一次无敌状态后用完整入口重试（不会再产生半死敌人）: isInvincible=' +
                    retryDefense.isInvincible + ' damageRate=' + retryDefense.damageRate.toFixed(3));
                phase = 'retryTakeDamage';
                callGameManagerTakeDamage(dwords);
                phase = 'retrySnapshot';
                after = readHealthSnapshot(target.player);
                dropped = hpDroppedBetween(before, after);
            }

            Runtime.stats.hpChecks += 1;
            Runtime.stats.lastHpBefore = before.rate;
            Runtime.stats.lastHpAfter = after.rate;
            Runtime.stats.lastHpRawBefore = before.raw;
            Runtime.stats.lastHpRawAfter = after.raw;
            if (dropped) Runtime.stats.hpDropped += 1;
            // 这一击把目标打成“死亡” -> 纳入观察窗口，心跳里确认到底有没有复活。
            if (!toFlag(before.dead) && toFlag(after.dead)) {
                watchDeath(target.player, before, after, sourceLabel, 'killed');
            }

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
            Runtime.stats.lastFailPhase = phase;
            // 名字里带上 phase：下次一眼就能看出异常是 clearInvincible / buildEvent /
            // takeDamage / snapshot / retry... 里哪一步抛的。
            fail('applyDamage:' + sourceLabel + '@' + phase, error);
            probe('apply', 'EXCEPTION entry=' + entry + ' phase=' + phase + ': ' +
                (error && error.message ? error.message : String(error)));
            // 异常可能发生在“血已经扣到 0、但死亡广播没跑”之后 -> 目标会变成
            // isDead=true 却永不复活的“半死幽灵”。这里主动补一次快照并纳入观察，
            // 让日志明确抓出这种情况（而不是只有一句 system error）。
            try {
                var crashedSnap = readHealthSnapshot(target.player);
                if (toFlag(crashedSnap.dead)) {
                    // 先登记（这样补发的广播里 RespawnPlayer 命中时能把 scheduled 标上），
                    // 再补发游戏自己的死亡广播 —— 2026-10-15：这一步才是"死亡不复活"的正解。
                    watchDeath(target.player, before, crashedSnap, sourceLabel, 'exception@' + phase);
                    maybeBroadcastSkippedDeath(target.player, dmgType, eyePos, weapon, phase);
                }
            } catch (_) {}
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
        // 不做任何倍率放大：直接用武器的基础伤害（damage_override 仅调试用）。
        var damage = baseDamage;
        if (Runtime.config.damage_override > 0) damage = Runtime.config.damage_override;
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
        return applyDamage(target, damage, dmgType, sourceLabel, weapon);
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
    // WPN_Gun.Damage 挂法（config.gun_hook_mode）
    // ------------------------------------------------------------------
    //   attach（默认）：JS 只在 onEnter 里出现一次；别人的开火（Bot）完全不经过 JS。
    //     这是"托管异常被 Frida 抢走 -> 死亡广播不返回 -> 终结者不复活"的根因修复，
    //     详见 config.gun_hook_mode 上方的注释。
    //   replace（旧）：保留原实现，仅用于对照/回退。
    function installGunHook() {
        var address = Runtime.base.add(RVA.WPN_Gun_Damage);
        if (!isExecutable(address)) throw new Error('WPN_Gun.Damage address not executable: ' + address);
        if (Runtime.config.gun_hook_mode === 'replace') {
            installGunHookReplace(address);
            return;
        }
        installGunHookAttach(address);
    }

    // ------------------------------------------------------------------
    // 原生射线接管（gun_ray_redirect）：把这一发的射线掰到目标身上
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

    // true = 已把这一发的射线改到目标身上，原函数照常跑（调用方不要跳过原函数）
    function redirectRayToTarget(ctx, weapon) {
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
                        '已自动退回注入路径（不写栈）sp=' + fmtPtr(sp));
                }
                return false;
            }
            var myPlayer = getMyPlayer();
            if (isNull(myPlayer)) return false;
            var rotation = readCameraRotation(myPlayer);
            if (!rotation) return false;
            var eyePos = getLocalEyePos(myPlayer);
            var target = getSelectedTarget(myPlayer, eyePos || sane.origin, rotation);
            if (!target || !target.pos) return false;

            // 起点用游戏自己的（枪口/相机位置不变，手感不变），只把方向掰到目标命中点
            var aim = target.pos;
            var vx = aim.x - sane.origin.x;
            var vy = aim.y - sane.origin.y;
            var vz = aim.z - sane.origin.z;
            var len = Math.sqrt(vx * vx + vy * vy + vz * vz);
            if (!isFinite(len) || len < 0.01) return false;

            sp.add(20).writeFloat(vx / len);
            sp.add(24).writeFloat(vy / len);
            sp.add(28).writeFloat(vz / len);

            var damage = resolveDamage(readGunDamage(weapon));
            if (!(damage > 0)) damage = resolveDamage(0) || 10;
            ctx.dd_target = {
                player: target.player,
                target: target,
                weapon: weapon,
                damage: damage,
                before: readHealthSnapshot(target.player)
            };
            Runtime.stats.rayRedirectShots += 1;
            return true;
        } catch (error) {
            Runtime.stats.rayRedirectBadArgs += 1;
            fail('rayRedirect', error);
            return false;
        }
    }

    // attach 版：把 JS 从游戏的伤害链里摘出去
    //   本地武器（我开火）**优先"原生射线接管"**：把这一发的射线掰到目标身上 -> 原函数原样跑完，
    //     命中判定 / 伤害 / DeathEventBroadcast / 击杀提示 / 复活调度全是游戏自己的代码；
    //     没有目标 / 参数不像射线 / 接管后原版没打掉血 -> 退回"自己注入直伤 + 跳过原函数"。
    //   其它武器（Bot 开火）→ 一句 return，原函数原生跑完，Frida 不留帧。
    //   跳过原函数的手法（x86 mscdecl）：
    //     参数由调用方清理，所以"跳过"= 弹出返回地址 + 跳回调用方，
    //     等价于让这个函数什么都没做就返回。
    //     返回地址先做"必须落在 GameAssembly 可执行区间"的校验；校验不过就不跳过
    //     （宁可这一发多打一遍，也绝不乱跳栈）。
    function installGunHookAttach(address) {
        var handle = Interceptor.attach(address, {
            onEnter: function (args) {
                this.dd_target = null;   // 非空 = 这一发我们改过射线，等 onLeave 核对血量
                try {
                    Runtime.stats.gunDamageCalls += 1;
                    // 复活兜底 / 补发广播的心跳：这里一定是游戏主线程，
                    // 而且每一发枪（含 Bot）都会进来 —— 比绑在"别人的死亡广播 onLeave"上可靠得多。
                    try { drainRebroadcastQueue(); } catch (_) {}
                    try { deathRescueTick(); } catch (_) {}
                    if (!Runtime.enabled || !Runtime.config.enable_guns) {
                        Runtime.stats.gunHookDisabled += 1;
                        return;                                   // 原版照常执行
                    }
                    if (Runtime.inDirectDamage) {
                        Runtime.stats.gunHookReentry += 1;
                        return;                                   // 结算过程中又回到 Damage -> 原版照常执行
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
                        probe('gunLocal', 'taking over fire #' + Runtime.stats.localGunFires +
                            ' weapon=' + fmtPtr(weapon) + ' ammoDamage=' + readGunDamage(weapon).toFixed(2));
                    }

                    // ---- 首选：原生射线接管（把射线掰到目标身上，其余全部交给游戏原版）----
                    //   这是"走游戏正常死亡/复活流程"的唯一正解：DeathEventBroadcast /
                    //   击杀提示 / 模式记账 / 复活调度全都在原函数里，我们一行都不插手。
                    if (Runtime.config.gun_ray_redirect && redirectRayToTarget(this, weapon)) {
                        return;                                   // ★ 原函数原样跑完（不跳过！）
                    }

                    // ---- 退路：自己注入直伤，然后跳过原函数（旧行为）----
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
                            return;                               // 原版射线照常走
                        }
                    }
                    skipOriginalFromOnEnter(this);
                } catch (error) {
                    fail('WPN_Gun.Damage onEnter', error);
                }
            },
            onLeave: function () {
                // 只处理"我们改过射线"的那一发：原版已经跑完，核对目标血量。
                //   掉血了 -> 这一发完全走的是游戏自己的流程（伤害/死亡广播/复活调度都在里面）
                //   没掉血 -> 原版射线被挡住/没命中/被无敌吃掉 -> 用注入补一发
                //             （血确实没掉，所以不会双倍伤害）
                if (!this.dd_target) return;
                var rec = this.dd_target;
                this.dd_target = null;
                try {
                    try { drainRebroadcastQueue(); } catch (_) {}
                    var after = readHealthSnapshot(rec.player);
                    if (hpDroppedBetween(rec.before, after)) {
                        Runtime.stats.rayRedirectHits += 1;
                        // 原版把它打死了 -> 游戏自己已经广播了死亡、排了复活，我们什么都不做
                        if (!toFlag(rec.before.dead) && toFlag(after.dead)) {
                            watchDeath(rec.player, rec.before, after, 'gun:ray', 'nativeRayKill');
                        }
                        return;
                    }
                    Runtime.stats.rayRedirectMiss += 1;
                    Runtime.inDirectDamage = true;
                    try {
                        applyDamage(rec.target, rec.damage, DAMAGE_TYPE.Gun, 'gun:ray-miss', rec.weapon);
                    } finally {
                        Runtime.inDirectDamage = false;
                    }
                } catch (error) {
                    fail('WPN_Gun.Damage onLeave', error);
                }
            }
        });
        Runtime.attachHooks.push({ name: 'WPN_Gun.Damage(attach)', handle: handle });
        log('info', 'WPN_Gun.Damage attached @ 0x' + RVA.WPN_Gun_Damage.toString(16) +
            '（attach 模式：Bot 开火完全原生；本地开火优先"原生射线接管"' +
            (Runtime.config.gun_ray_redirect ? '已开' : '已关，走注入') + '）');
    }

    // 模拟 ret：弹出返回地址并跳回"调用方"（mscdecl 由调用方清栈，所以不用动参数）
    //   要点：入口 [esp] 里那个值不一定就是游戏调用方 —— 如果同一个地址上还有别的
    //   Interceptor.attach 监听者带 onLeave，Frida 会把返回地址换成它自己的返回 thunk。
    //   我们要跳到"当前 [esp] 里的那个值"（不管是谁的），Frida 的 onLeave 链才照常会跑；
    //   同时 esp 前进 4，语义上完全等价于一次 ret。
    //   放行条件只有一个：目标必须在可执行页（游戏调用方 / Frida thunk 都满足）。
    //   不可执行就拒绝跳过（原函数照跑，最多这一发多打一遍，绝不乱跳栈）。
    function skipOriginalFromOnEnter(ctx) {
        try {
            var sp = ctx.context.esp;
            var retAddr = null;
            try { retAddr = sp.readPointer(); } catch (_) { retAddr = null; }
            if (!retAddr || isNull(retAddr)) {
                try { retAddr = ctx.returnAddress; } catch (_) { retAddr = null; }
            }
            var mod = null;
            try { mod = Process.findModuleByAddress(retAddr); } catch (_) { mod = null; }
            var modName = mod ? String(mod.name) : 'null';
            var inGameAssembly = modName.toLowerCase().indexOf('gameassembly') >= 0;
            if (!retAddr || isNull(retAddr) || !isExecutable(retAddr)) {
                Runtime.stats.gunSkipFailed += 1;
                fail('gunHook:skip', new Error('return address not executable: ' + retAddr +
                    ' (mod=' + modName + ', esp=' + sp + ')'));
                return;
            }
            if (!inGameAssembly && Runtime.stats.gunSkipped === 0) {
                // 不是游戏模块 -> 这个地址上还有别的钩子（Frida 返回 thunk），跳过手势照样生效
                log('info', '[gunHook:skip] 返回地址指向 ' + modName +
                    '（Frida 返回 thunk，说明 WPN_Gun.Damage 上还有别的 attach/onLeave 监听者）；模拟 ret 照常执行');
            }
            ctx.context.esp = sp.add(4);
            ctx.context.pc = retAddr;
            // 读回校验：万一某个 Frida 版本不接受 context.pc 写入，我们要能在日志里立刻看到，
            // 而不是"以为跳过了、其实原函数又打了一遍"（表现为同一发双倍伤害）。
            var backPc = null;
            try { backPc = ctx.context.pc; } catch (_) { backPc = null; }
            if (backPc && !isNull(backPc) && !samePointer(backPc, retAddr)) {
                Runtime.stats.gunSkipFailed += 1;
                fail('gunHook:skip', new Error('Frida refused context.pc write: want ' +
                    retAddr + ' got ' + backPc));
                return;
            }
            Runtime.stats.gunSkipped += 1;
        } catch (error) {
            Runtime.stats.gunSkipFailed += 1;
            fail('gunHook:skip', error);
        }
    }

    // 旧实现（gun_hook_mode='replace'）：replace + NativeFunction 回call
    function installGunHookReplace(address) {

        // 必须在 replace 之前创建，之后才能调用原函数。
        native.gunDamageOriginal = new NativeFunction(
            address, 'void',
            ['pointer', 'uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'pointer'],
            CALL_CONV
        );

        var replacement = new NativeCallback(function (weapon, r0, r1, r2, r3, r4, r5, method) {
            try {
                Runtime.stats.gunDamageCalls += 1;
                // 复活兜底的心跳：这里是游戏主线程，而且每一发枪（含 Bot）都会进来，
                // 内部 1 秒只真正跑一次 -> 死亡广播被打断的目标能在 1 秒内被发现。
                try { deathRescueTick(); } catch (_) {}

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
        log('warn', 'WPN_Gun.Damage replaced @ 0x' + RVA.WPN_Gun_Damage.toString(16) +
            '（旧模式：Bot 开火会经 JS 回call，原函数内部的托管异常会被 Frida 抢走 -> 终结者可能不复活）');
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
                weapon: weapon,
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

    // 只读观察钩子：从真实伤害事件里抓取合法的 hitTag/hitSndName/hitEffect 字符串指针，
    // 让本功能合成的事件带上原版字符串，避免传 null。
    function installStringCaptureHooks() {
        var capture = function () {
            try {
                // 我们自己合成的事件不算"原版"，否则会把空的 hitTag/hitEffect
                // 当成真实值缓存起来，自我污染。
                if (Runtime.inDirectDamage) return;
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

    // 原版事件底板采集：DamageEventData.TakePlace 是值类型实例方法，
    // 进入时 args[0] 就是结构体指针；原版每次开火（含打空、打墙）都会走到它，
    // 所以这里能稳定抄到 wpnIndex / wpnSprIndex / damageTag 这些标量字段。
    function installEventTemplateCapture() {
        registerProbeAttach('DamageEventData.TakePlace(template)', RVA.DamageEventData_TakePlace, {
            onEnter: function (args) {
                captureEventTemplate(args[0], 'TakePlace');
            }
        });
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
                ['HealthData.get_rate', RVA.HealthData_get_rate],
                ['DamageEventData.TakePlace', RVA.DamageEventData_TakePlace],
                ['GameManager.DeathEventBroadcast', RVA.GameManager_DeathEventBroadcast],
                ['GameManager.PlayHitFxAndSnd', RVA.GameManager_PlayHitFxAndSnd],
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
                    ' tpl=' + s.templateCaptured + '/' + s.templateUsed +
                    ' refused=' + s.templateRejected + ' inv=' + s.invincibleCleared +
                    ' death=' + s.deathIn + '->' + s.deathOut +
                    ' hitFx=' + s.hitFxIn + '->' + s.hitFxOut +
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
                    ' hit=' + s.forgetHit + ' hitG=' + s.forgetHitGrenade +
                    ' trig=' + s.forgetTrigger + ' timeout=' + s.forgetTimeout +
                    ' lost=' + s.forgetLost + ' noNext=' + s.forgetNoNext +
                    ' ident=' + s.forgetIdentity + ']' +
                    ' touch[hit=' + s.missileHitSeen + ' trig=' + s.missileTriggerSeen + ']' +
                    ' cone[命中=' + s.coneHit + ' 锥内空=' + s.coneEmpty +
                    ' 回退=' + s.coneFallback + ' 严格放弃=' + s.coneEmptyStrict +
                    ' 关=' + s.coneOff + ' 轴失败=' + s.coneAxisFail +
                    ' 换目标=' + s.coneRetarget + ']');
                // 死亡/复活链：death=in->out（不相等=死亡广播抛异常）；
                //   respawnPlayer / playerRespawn 有没有涨 = 复活调度到底有没有被调用；
                //   watch[...] = 击杀后观察窗口的结果（noRevive>0 就是“死了不复活”）。
                log('info', '[probe:beat] deathDiag: death=' + s.deathIn + '->' + s.deathOut +
                    ' aborted=' + s.deathAborted + ' rebroadcast=' + s.deathRebroadcast +
                    '(defer=' + s.rebroadcastDeferredOk + '/' + s.rebroadcastDeferred + ')' +
                    ' rescued=' + s.deathRescued + '/' + s.deathRescueAttempts +
                    ' respawnPlayer=' + s.respawnScheduled + ' playerRespawn=' + s.playerRespawnCalls +
                    ' wpnFix=' + s.deathWpnFixed + ' raises=' + s.raiseCount +
                    ' ray=' + s.rayRedirectHits + '/' + s.rayRedirectShots +
                    '(miss=' + s.rayRedirectMiss + ' badArgs=' + s.rayRedirectBadArgs + ')' +
                    ' chain=' + s.chainBroadcastInside + '/' + s.chainTakeDamageCalls +
                    ' watch[active=' + s.halfDeadActive + ' recovered=' + s.halfDeadRecovered +
                    ' noRevive=' + s.halfDeadConfirmed + ']');
                try { checkDeathWatch(); } catch (errWatch) {}
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

    // 游戏自身伤害管线的只读观察钩子。用来区分四类失败：
    //   A. 只有 pipeShoot 增长      -> 开火进了游戏，但 WPN_Gun.Damage 的替换没生效
    //   B. 只看到 [game]            -> 游戏自己在结算伤害，我们合成的没进去
    //   C. 看到 [ours] 但 HP 不变   -> 调用被接受了但没有实际扣血（入口选错）
    //   D. 什么都没有                -> 钩子没装上（对照 rva / attach 日志）

    // ------------------------------------------------------------------
    // death_diag：击杀之后“到底有没有复活”
    // ------------------------------------------------------------------
    //   背景（2.7 实测日志指纹）：
    //     [fail:applyDamage:gun] applyDamage:gun: system error
    //   即我们合成的 GameManager.TakeDamage 在被击杀那一刻抛出了托管异常。
    //   按 §3.2 的结论，这条异常会打断 GameManager.DeathEventBroadcast，
    //   结果 victim 已经是 isDead=true，但“复活调度”根本没跑 ——
    //   画面上就是“死了不复活、模型卡在原地”。
    //
    //   这一组诊断全部只读（不改参数、不改控制流），默认开启：
    //     1) DeathEventBroadcast 进出 —— deathIn 有、deathOut 没有 = 异常现场；
    //     2) ModeBase_Nano.RespawnPlayer —— 复活调度有没有被调用；
    //     3) Player.Respawn —— 真正排进复活协程；
    //     4) 击杀后观察窗口 —— 目标 N 秒内没活过来就报 *** 击杀后未复活 ***。
    // ------------------------------------------------------------------
    function readU8Safe(addr) {
        try { return addr.readU8(); } catch (_) { return -1; }
    }

    function readI32Safe(addr) {
        try { return addr.readS32(); } catch (_) { return -1; }
    }

    function readNanoRoleDiag(player) {
        try {
            if (isNull(player) || !native.getNanoRole) return -1;
            return toNumber(native.getNanoRole(player, ptr(0)), -1);
        } catch (_) { return -1; }
    }

    // 把一个玩家的复活相关状态打包，日志里一行能看全
    function playerRespawnState(player) {
        var info = { role: -1, respawnType: -1, isRespawning: -1, graveCount: -1, canUseGrave: -1, dead: null };
        try {
            if (isNull(player)) return info;
            info.role = readNanoRoleDiag(player);
            info.respawnType = readI32Safe(player.add(OFF.Player_respawnType));
            info.isRespawning = readU8Safe(player.add(OFF.Player_isRespawning));
            info.dead = toFlag(native.isDead(player, ptr(0)));
            var data = player.add(OFF.Player_nano4TData).readPointer();
            if (readable(data)) {
                info.canUseGrave = data.add(OFF.Nano4TData_canUseGrave).readU8();
                info.graveCount = data.add(OFF.Nano4TData_graveCount).readS32();
            }
        } catch (_) {}
        return info;
    }

    function fmtRespawnState(info) {
        return 'role=' + info.role + ' respawnType=' + info.respawnType +
            ' isRespawning=' + info.isRespawning + ' grave=' + info.graveCount +
            '/canUseGrave=' + info.canUseGrave + ' isDead=' + String(info.dead);
    }

    // ------------------------------------------------------------------
    // 兜底前的硬闸门：只认"看起来确实是玩家"的目标
    // ------------------------------------------------------------------
    //   2026-10-14 22:25 闪退复盘（0xC0000005）：
    //     死亡事件里的 dead **不一定是 Player**（哨戒炮 / 可破坏实体 / 已经被回收的指针），
    //     我们当时把它直接喂给 ModeBase_Nano.RespawnPlayer，游戏按 Player 结构往这块内存写
    //     -> 某个对象的 klass 指针被写成 2 -> 12 秒后游戏自己的 Bot 技能链上访问 [klass+0xB4] 崩溃。
    //   所以：role / respawnType / isRespawning / healthData 任何一个离谱，就绝不下手。
    //   （日志里的指纹就是这四个字段一起读出天文数字，例如 role=126398040 respawnType=282994032）
    //   ★2026-10-15 追加最后一道：指针还必须真的在"当前这一帧的玩家列表"里。
    //     闪电回收/reuse 的指针字段有可能暂时还"看着合理"，只有"在列表里"才能证明
    //     它现在就是一个活着的 Player 对象 —— 这是防 22:25 那类写坏内存最硬的一条。
    function isListedPlayer(player) {
        try {
            if (isNull(player)) return false;
            var now = Date.now();
            var cache = Runtime.cache.playerListCache;
            if (!cache || now - cache.at > 250) {
                var gm = getGameManager();
                if (isNull(gm)) return false;
                cache = { at: now, keys: {} };
                var list = getAllPlayers(gm);
                for (var i = 0; i < list.length; i += 1) cache.keys[list[i].toString()] = true;
                Runtime.cache.playerListCache = cache;
            }
            return cache.keys[player.toString()] === true;
        } catch (_) { return false; }
    }

    function isPlausibleVictim(player) {
        try {
            if (!readable(player)) return false;
            if (!isValidPlayer(player)) return false;                 // team 必须是 0/1/2
            if (!isListedPlayer(player)) return false;                // 必须在当前玩家列表里
            if (!readable(player.add(OFF.Entity_healthData).readPointer())) return false;
            var info = playerRespawnState(player);
            if (info.role < 0 || info.role > 63) return false;         // NanoRole 0..27
            if (info.respawnType < 0 || info.respawnType > 8) return false;
            if (info.isRespawning !== 0 && info.isRespawning !== 1) return false;
            return true;
        } catch (_) { return false; }
    }

    // 这一击把目标打死了 -> 登记进观察窗口，心跳里再确认它有没有复活。
    function watchDeath(victim, before, after, sourceLabel, note) {
        try {
            if (!Runtime.config.death_diag) return;
            if (isNull(victim) || !after || !toFlag(after.dead)) return;
            registerDeathWatch(victim, sourceLabel, note);
        } catch (_) {}
    }

    // 心跳（5 秒一次）里跑：目标活过来 = 复活成功；超时仍 isDead = 不复活（直接证据）。
    //   ★2026-10-15：只要兜底次数还没用完，超时就不删记录、只把观察窗口往后挪
    //   （旧版 20 秒就删，兜底跟着停，目标躺到本局结束）。
    function checkDeathWatch() {
        if (!Runtime.config.death_diag) return;
        var keys = Object.keys(Runtime.deathWatch);
        for (var i = 0; i < keys.length; i += 1) {
            var key = keys[i];
            var entry = Runtime.deathWatch[key];
            if (!entry) continue;
            if (!entry.windowAt) entry.windowAt = entry.at;
            var nowWatch = Date.now();
            var elapsed = nowWatch - entry.at;
            var deadNow = null;
            try { deadNow = toFlag(native.isDead(entry.victim, ptr(0))); } catch (_) { deadNow = null; }
            if (deadNow === false) {
                Runtime.stats.halfDeadRecovered += 1;
                Runtime.stats.halfDeadActive = Math.max(0, Runtime.stats.halfDeadActive - 1);
                // 每次死亡都登记 -> 正常复活太多，只前 60 条逐条打；兜底过的必打
                if (entry.tries > 0 || probeBudget('deathWatchOk', 60)) {
                    log('info', '[deathDiag] 目标已复活: victim=' + key + ' elapsed=' + elapsed + 'ms' +
                        ' 复活调度=' + (entry.scheduled ? '已命中' : '未观察到') +
                        (entry.tries > 0 ? ' 兜底=已生效(第' + entry.tries + '次)' : '') +
                        ' [' + fmtRespawnState(playerRespawnState(entry.victim)) + ']' +
                        ' source=' + entry.label + ' note=' + entry.note);
                }
                delete Runtime.deathWatch[key];
            } else if (deadNow === null || nowWatch - entry.windowAt > Runtime.config.death_diag_ms) {
                var keepRetrying = (deadNow !== null &&
                    !entry.rescued &&
                    Runtime.config.death_fix_respawn &&
                    entry.tries < Runtime.config.death_rescue_max_tries);
                if (!entry.reported) {
                    entry.reported = true;
                    Runtime.stats.halfDeadConfirmed += 1;
                    log('error', '[deathDiag] *** 击杀后未复活（半死/幽灵）*** victim=' + key +
                        ' elapsed=' + elapsed + 'ms 复活调度=' + (entry.scheduled ? '已命中' : '未命中') +
                        ' 兜底=' + (entry.tries > 0 ? '已补发但没活' : '未触发') + ' tries=' + entry.tries +
                        ' [' + fmtRespawnState(playerRespawnState(entry.victim)) + ']' +
                        ' source=' + entry.label + ' note=' + entry.note +
                        (keepRetrying ? ' -> 继续兜底重试' : ''));
                }
                if (keepRetrying) {
                    entry.windowAt = nowWatch;   // 不删、不重复计数，把窗口往后挪继续等兜底
                    continue;
                }
                Runtime.stats.halfDeadActive = Math.max(0, Runtime.stats.halfDeadActive - 1);
                delete Runtime.deathWatch[key];
            }
        }
    }


    // ------------------------------------------------------------------
    // 死亡事件全字段 dump + 死亡观察登记（death_diag）
    // ------------------------------------------------------------------
    //   DeathEventData 一共 12 个字段（0x38 字节，按值压栈，[esp+4] 起）。
    //   20261014 的日志已经证明"wpIndex 非法"这条旧假设不成立（同一个 341 一炸一好），
    //   所以这里把整份结构体打平成一行：配合 [deathDiag:abort] / [deathDiag:raise]
    //   就能直接对比"被打断的那一次"和正常死亡到底哪个字段不一样。
    // ------------------------------------------------------------------
    function deathEventFields(b) {
        var f = [];
        function add(name, fn) {
            try { f.push(name + '=' + fn()); } catch (_) { f.push(name + '=?'); }
        }
        add('killer', function () { return fmtPtr(b.add(OFF.Death_killer).readPointer()); });
        add('dead', function () { return fmtPtr(b.add(OFF.Death_dead).readPointer()); });
        add('headShot', function () { return b.add(OFF.Death_headShot).readS32(); });
        add('wallThrough', function () { return b.add(OFF.Death_wallThrough).readU8(); });
        add('dmgType', function () { return b.add(OFF.Death_damageType).readS32(); });
        add('origin', function () {
            return b.add(OFF.Death_damageOrigin).readFloat().toFixed(1) + ',' +
                b.add(OFF.Death_damageOrigin + 4).readFloat().toFixed(1) + ',' +
                b.add(OFF.Death_damageOrigin + 8).readFloat().toFixed(1);
        });
        add('specialKill', function () { return b.add(OFF.Death_specialKill).readS32(); });
        add('nanoKill', function () { return b.add(OFF.Death_nanoKill).readS32(); });
        add('revenge', function () { return b.add(OFF.Death_revenge).readU8(); });
        add('dmgTag', function () { return hex32(b.add(OFF.Death_damageTag).readU32()); });
        add('wpn', function () { return b.add(OFF.Death_wpnIndex).readS32(); });
        add('wpnSpr', function () { return b.add(OFF.Death_wpnSprIndex).readS32(); });
        return f.join(' ');
    }

    // 死亡事件里所有"看着像索引"的字段，逐个拿 WpnDataDictionary 实查一遍。
    //   :MISS = 这个值不在武器字典里。get_wpnName/get_killMsgIcon/get_isVVIP 查的
    //   就是 wpn，所以 wpn:OK 而广播仍然炸 -> 异常来自别的字段/别的字典。
    function deathIndexPresence(b) {
        var out = [];
        try {
            var cand = [
                ['wpn', b.add(OFF.Death_wpnIndex).readS32()],
                ['wpnSpr', b.add(OFF.Death_wpnSprIndex).readS32()],
                ['specialKill', b.add(OFF.Death_specialKill).readS32()],
                ['nanoKill', b.add(OFF.Death_nanoKill).readS32()],
                ['dmgTag', b.add(OFF.Death_damageTag).readU32()]
            ];
            for (var i = 0; i < cand.length; i += 1) {
                out.push(cand[i][0] + '=' + cand[i][1] + (isValidWpnKey(cand[i][1]) ? ':OK' : ':MISS'));
            }
        } catch (_) {}
        return out.join(' ');
    }

    // 登记"这个人死了，盯它有没有复活"（deathIn 和 applyDamage 共用）
    //   fromBroadcast=true = 这笔登记发生在死亡广播 onEnter 里（广播正在飞）。
    //   只有这种登记才可能在广播被打断时留下 bcDone=false；其它来源（我们自己补刀）
    //   一律按"广播会正常跑完"处理，绝不代劳复活。
    function registerDeathWatch(victim, label, note, fromBroadcast) {
        try {
            if (!Runtime.config.death_diag) return;
            if (isNull(victim)) return;
            var key = victim.toString();
            if (Runtime.deathWatch[key]) {
                // 同一个人再次死亡：重置窗口（上一轮要么已经复活、要么还在观察）
                Runtime.deathWatch[key].at = Date.now();
                Runtime.deathWatch[key].label = label;
                if (fromBroadcast) {
                    Runtime.deathWatch[key].bcDone = false;
                    Runtime.currentDeathKey = key;
                }
                return;
            }
            Runtime.deathWatch[key] = {
                victim: victim, at: Date.now(), label: label,
                windowAt: Date.now(), reported: false, lastTryAt: 0,
                note: note || '', scheduled: false, rescued: false, tries: 0,
                respawnTimeMs: 0,   // 游戏自己排的复活时间（RespawnPlayer/Player.Respawn 钩子填）
                // 广播是否完整返回：onEnter 登记时先 false，onLeave 才置 true。
                // 只有 bcDone === false（= 广播真的被打断）才允许兜底。
                bcDone: fromBroadcast ? false : true
            };
            if (fromBroadcast) Runtime.currentDeathKey = key;
            Runtime.stats.halfDeadWatched += 1;
            Runtime.stats.halfDeadActive += 1;
            if (probeBudget('deathWatchReg', 60)) {
                log('info', '[deathDiag] 死亡登记: victim=' + key + ' (' + label + ' ' + (note || '') + ') [' +
                    fmtRespawnState(playerRespawnState(victim)) + ']');
            }
        } catch (_) {}
    }

    // ------------------------------------------------------------------
    // 复活兜底（death_fix_respawn）
    // ------------------------------------------------------------------
    //   要解决的问题：击杀之后目标 isDead=true 卡在原地，直到本局结束都不复活。
    //   2026-10-15 实测出两种成因（session bc03bc81，21 笔死亡里 3 笔不复活）：
    //     A. GameManager.TakeDamage 抛异常 -> 死亡广播根本没跑
    //        （日志指纹：[fail:applyDamage:gun@takeDamage] system error、
    //          登记 note=exception@takeDamage、复活调度=未命中）
    //        -> 首选 death_fix_broadcast 补发广播，补不上才走这里兜底；
    //     B. 死亡广播进了没出（[deathDiag:abort]）：ModeBase_Nano.RespawnPlayer
    //        被调用过（复活调度=已命中）但目标始终没活过来。
    //   所以判定条件只剩一条："宽限期过了，目标还是死的" —— 不再看广播是否完整
    //   （bcDone），也不再要求游戏"没排过复活"（scheduled）：2026-10-14 加的这两把锁
    //   太紧，正好把 A 和 B 两种不复活的情况全挡在门外，反而退化成"死了不复活"。
    //   动手前两道硬闸门（防 2026-10-14 22:25 那次 0xC0000005）：
    //     1) isPlausibleVictim()：dead 不一定是 Player（哨戒炮/可破坏实体/已回收指针），
    //        字段必须全部合理，而且必须真的在当前玩家列表里；
    //     2) native.isDead(victim) === true：已经活了 / 读不到 -> 绝不动手。
    //   只在游戏主线程调用（开火钩子 / 死亡广播 onLeave），每次都会写 [deathFix] 日志。
    // ------------------------------------------------------------------
    function deathRescueTick() {
        try {
            if (!Runtime.config.death_fix_respawn || !Runtime.config.death_diag) return 0;
            if (!Runtime.enabled || !Runtime.initialized) return 0;
            var now = Date.now();
            if (now - Runtime.lastRescueTick < 1000) return 0;
            Runtime.lastRescueTick = now;
            var keys = Object.keys(Runtime.deathWatch);
            if (!keys.length) return 0;
            var grace = Runtime.config.death_respawn_grace_ms;
            var maxTries = Runtime.config.death_rescue_max_tries;
            var gap = Runtime.config.death_rescue_retry_gap_ms;
            var mode = Runtime.modeBase;
            var attempted = 0;
            for (var i = 0; i < keys.length; i += 1) {
                var key = keys[i];
                var entry = Runtime.deathWatch[key];
                if (!entry || entry.rescued) continue;
                if (entry.tries >= maxTries) continue;
                // ★2026-10-15 修（这是"兜底也没效果"的真正原因）：
                //   旧版是"调用没抛异常就 entry.rescued=true"，而下一轮又拿 rescued 直接跳过，
                //   于是目标其实还死着也永远不再补 —— 日志指纹 "兜底=已补发但没活 tries=1"。
                //   现在只有 native.isDead 真的变 false 才算成功，否则按 gap 间隔继续补。
                if (entry.lastTryAt && now - entry.lastTryAt < gap) continue;
                // 第一次动手要等够时间（之后按 gap 重试，不再重新等一遍宽限期）：
                //   · 游戏一次都没排复活（scheduled=false）-> 基础宽限期；
                //   · 游戏排过（scheduled=true）-> 再给 respawnTime + 5 秒余量，
                //     免得把一个"只是慢一点"的正常复活抢先了。
                if (!entry.lastTryAt) {
                    var wait = grace;
                    if (entry.scheduled && entry.respawnTimeMs > 0) {
                        wait = Math.max(wait, entry.respawnTimeMs + 5000);
                    }
                    if (now - entry.at < wait) continue;
                }
                // ★硬闸门 1：dead 不一定是 Player（哨戒炮/可破坏实体/已被回收的指针），
                //   喂给 RespawnPlayer 会把游戏内存写坏（2026-10-14 22:25 闪退就是这个）。
                if (!isPlausibleVictim(entry.victim)) {
                    delete Runtime.deathWatch[key];
                    Runtime.stats.halfDeadActive = Math.max(0, Runtime.stats.halfDeadActive - 1);
                    Runtime.stats.deathRescueRejected += 1;
                    if (probeBudget('deathWatchReject', 40)) {
                        log('warn', '[deathDiag] 放弃兜底：目标 ' + key +
                            ' 不是有效玩家（dead 不是 Player / 不在当前玩家列表 / 指针已被回收），已从观察窗口移除 [' +
                            fmtRespawnState(playerRespawnState(entry.victim)) + ']');
                    }
                    continue;
                }
                // ★硬闸门 2：只有"确实还死着"才补。已经活过来（哪怕我们没看到复活调度）
                //   也绝不动手 —— 正常死亡（游戏自己会复活）因此不会被抢先。
                var deadNow = null;
                try { deadNow = toFlag(native.isDead(entry.victim, ptr(0))); } catch (_) { deadNow = null; }
                if (deadNow === false) { entry.rescued = true; continue; }
                if (deadNow !== true) continue;
                entry.tries += 1;
                entry.lastTryAt = now;
                Runtime.stats.deathRescueAttempts += 1;
                attempted += 1;
                var via = '';
                try {
                    if (entry.tries >= 3) {
                        // 第三次起：先清掉无敌/减伤（"复活了又立刻躺下 / 打不动"的常见成因）
                        try { clearTargetInvincibility(entry.victim); } catch (_) {}
                    }
                    if (!isNull(mode)) {
                        via = 'ModeBase_Nano.RespawnPlayer';
                        native.respawnPlayer(mode, entry.victim, 1, 1, 0, ptr(0));
                        // 第二次起再叠一次 Player.Respawn（真正"排进复活协程"的那一步）：
                        // 有些目标（终结者/墓碑复活）只走 RespawnPlayer 不会真的活过来。
                        if (entry.tries >= 2 && native.playerRespawn) {
                            via += ' + Player.Respawn';
                            try { native.playerRespawn(entry.victim, 1.0, 0.0, ptr(0)); } catch (_) {}
                        }
                    } else {
                        via = 'Player.Respawn';
                        native.playerRespawn(entry.victim, 1.0, 0.0, ptr(0));
                    }
                } catch (error) {
                    Runtime.stats.deathRescueFailed += 1;
                    fail('deathFix:respawn', error);
                }
                // ★调用成功 ≠ 目标活了：只有 isDead 真的变 false 才算成功。
                var aliveNow = null;
                try { aliveNow = toFlag(native.isDead(entry.victim, ptr(0))); } catch (_) { aliveNow = null; }
                if (aliveNow === false) {
                    entry.rescued = true;
                    Runtime.stats.deathRescued += 1;
                }
                log('warn', '[deathFix] 复活兜底 #' + entry.tries + '：目标 ' + key + ' 死亡 ' +
                    (now - entry.at) + 'ms 后仍未复活（复活调度=' +
                    (entry.scheduled ? '已命中但没生效' : '未命中') +
                    ' bcDone=' + String(entry.bcDone) + '），已手动调用 ' + via +
                    (aliveNow === false
                        ? ' -> 目标已活'
                        : ' -> ★目标仍是死的，' + gap + 'ms 后重试（上限 ' + maxTries + ' 次）') +
                    '（source=' + entry.label + ' note=' + entry.note + '）[' +
                    fmtRespawnState(playerRespawnState(entry.victim)) + ']');
            }
            return attempted;
        } catch (error) {
            fail('deathRescueTick', error);
            return 0;
        }
    }

    // ------------------------------------------------------------------
    // 托管异常漏斗探针（Il2Cpp_Exception_Raise）
    // ------------------------------------------------------------------
    //   IDA 实测：il2cpp_raise_exception 和所有托管 throw 最终都走
    //     sub_1013FF10(Il2CppException* ex, MethodInfo*, ...) -> _CxxThrowException。
    //   ex 是 Il2CppException*（+0x00 = klass），klass+0x08 = 类名 char*。
    //   这里只关心"死亡广播正在飞的时候"那一下：异常类型 + 调用栈 RVA。
    //   拿到 RVA 后用 IDA 对函数名就能定位是哪一个 observer 抛的。
    // ------------------------------------------------------------------
    //   ★★ 2026-10-14 闪退修复：本探针默认关闭（death_diag_raise=false）★★
    //   为什么必须关：这个钩子打在 il2cpp::vm::Exception::Raise(+0x13FF10) 上，而它是
    //   noreturn 的 C++ throw 漏斗（内部 -> __CxxThrowException@8）。Frida 内联钩子一旦
    //   挂在抛出点上，Frida 自己的异常处理器会先把 0xE06D7363 抓走（同 26_grenade_mode
    //   v2.13 注释里的同一条根因），游戏自己的异常帧收不到 -> RaiseException 直接返回 ->
    //   控制流落回调用点 sub_10140190 后面编译器填的 int 3(0xCC) ->
    //   进程 0x80000003 @ GameAssembly+0x1401A6 秒退。
    //   实证：2026-10-14 18:26:12.720 多人生化(终结者)模式，探针 [deathDiag:raise]
    //   与崩溃同一毫秒（见 06-测试/_crash18_26/崩溃分析-2026-10-14-1826.md）。
    //   → "死亡广播有没有被打断"仍可判：deathIn/deathOut 计数 + [deathDiag:abort]
    //     现场字段，都不需要碰异常漏斗。
    // ------------------------------------------------------------------
    function installRaiseProbe() {
        if (!Runtime.config.death_diag) return;
        if (!Runtime.config.death_diag_raise) return;   // ★默认关闭：取证专用，会闪退
        try {
            var handle = Interceptor.attach(Runtime.base.add(RVA.Il2Cpp_Exception_Raise), {
                onEnter: function (args) {
                    try {
                        Runtime.stats.raiseCount += 1;
                        var inFlight = Runtime.pendingDeath;
                        if (!inFlight && !probeBudget('raise', 10)) return;
                        var now = Date.now();
                        // 同一次异常可能被多层包装各抛一次，5ms 内只记第一条
                        if (Runtime.lastRaiseLogAt && now - Runtime.lastRaiseLogAt < 5) return;
                        Runtime.lastRaiseLogAt = now;
                        var excName = '?';
                        try {
                            var klass = args[0].readPointer();
                            if (readable(klass)) {
                                var namePtr = klass.add(0x08).readPointer();
                                if (readable(namePtr)) excName = namePtr.readUtf8String(96);
                            }
                        } catch (_) {}
                        var bt = [];
                        try {
                            var frames = Thread.backtrace(this.context, Backtracer.FUZZY);
                            for (var i = 0; i < frames.length && i < 12; i += 1) {
                                var off = frames[i].sub(Runtime.base);
                                if (off.compare(0) >= 0 && off.compare(Runtime.module.size) < 0) {
                                    bt.push('+' + off.toString(16));
                                }
                            }
                        } catch (_) {}
                        log('error', '[deathDiag:raise] ' + excName +
                            ' inBroadcast=' + (inFlight ? 'YES' : 'no') +
                            (inFlight ? ' event={' + inFlight.fields + '}' : '') +
                            ' bt=' + bt.join(','));
                    } catch (_) {}
                }
            });
            Runtime.attachHooks.push({ name: 'Il2Cpp.Exception.Raise(deathDiag)', handle: handle });
            log('info', '[deathDiag] 托管异常探针已安装 @+0x' + RVA.Il2Cpp_Exception_Raise.toString(16));
        } catch (error) {
            log('warn', '[deathDiag] 托管异常探针安装失败: ' +
                (error && error.message ? error.message : String(error)));
        }
    }

    // ------------------------------------------------------------------
    // 死亡广播 wpnIndex 兜底（death_fix_wpn，默认关闭）
    // ------------------------------------------------------------------
    //   2026-10-14 实测（logs/game_modifier.log）：
    //     41 次死亡广播里有 3 次「onEnter 之后没有 onLeave」，且这 3 次都没有
    //     ModeBase_Nano.RespawnPlayer -> 目标永远不复活。3 次的 wpnIndex =
    //     938 / 183 / 2759，其余 38 次全部正常；同一毫秒还伴随
    //     [fail:WPN_Gun.Damage replacement] system error。
    //   反汇编确认死亡广播里 HUD_KillMark 会调
    //     DeathEventData.get_wpnName()/get_killMsgIcon()/get_isVVIP()，
    //   三个都是 GameManager.WpnDataDictionary[wpnIndex]；key 不存在 ->
    //   il2cpp_raise_exception -> 整条死亡广播（含复活调度）被打断。
    //   所以这里在广播入口把查不到的 key 换成一个存在的 key，让广播能跑完。
    //
    //   布局（IDA 类型确认，32 位 IL2CPP）：
    //     Dictionary: +0x0C entries / +0x10 count / +0x14 version
    //     Il2CppArray: +0x0C max_length / +0x10 items
    //     Entry: 16 字节，key 在 +0x08
    // ------------------------------------------------------------------
    var wpnKeyCache = { version: -2, keys: null };

    function getWpnDataDictionary() {
        try {
            var typeInfo = Runtime.base.add(RVA.GameManager_TypeInfo).readPointer();
            if (!readable(typeInfo)) return null;
            var staticFields = typeInfo.add(OFF.Klass_staticFields).readPointer();
            if (!readable(staticFields)) return null;
            var dict = staticFields.add(OFF.GM_WpnDataDictionary).readPointer();
            return readable(dict) ? dict : null;
        } catch (_) { return null; }
    }

    // 把 WpnDataDictionary 的所有 key 抄进 JS 对象；Dictionary.version 没变就不重扫。
    function refreshWpnKeyCache() {
        try {
            var dict = getWpnDataDictionary();
            if (!dict) return false;
            var version = dict.add(OFF.Dict_version).readS32();
            if (version === wpnKeyCache.version && wpnKeyCache.keys) return true;
            var entries = dict.add(OFF.Dict_entries).readPointer();
            var count = dict.add(OFF.Dict_count).readS32();
            if (!readable(entries) || count <= 0 || count > 20000) {
                wpnKeyCache = { version: version, keys: null };
                return false;   // 读不到 -> 不拦截，别把正常死亡也改了
            }
            var keys = {};
            var items = entries.add(OFF.Arr_items);
            for (var i = 0; i < count; i += 1) {
                var key = items.add(i * OFF.Entry_size + OFF.Entry_key).readS32();
                if (key > 0) keys[key] = true;
            }
            wpnKeyCache = { version: version, keys: keys };
            return true;
        } catch (error) {
            fail('refreshWpnKeyCache', error);
            return false;
        }
    }

    // true = 字典里存在（或读不到字典、无法判断 -> 不拦截）；false = 确实不存在
    function isValidWpnKey(index) {
        if (!(index > 0)) return false;
        if (!refreshWpnKeyCache()) return true;
        return wpnKeyCache.keys[index] === true;
    }

    function firstValidWpnKey() {
        var keys = wpnKeyCache.keys;
        var best = -1;
        for (var k in keys) {
            var n = parseInt(k, 10);
            if (isFinite(n) && n > 0 && (best < 0 || n < best)) best = n;
        }
        return best;
    }

    function installDeathDiagnostics() {
        if (!Runtime.config.death_diag) return;

        // 1) 死亡广播：onEnter 有、onLeave 没有 = 死亡链被异常打断（不复活/闪退的现场）
        registerProbeAttach('GameManager.DeathEventBroadcast(deathDiag)', RVA.GameManager_DeathEventBroadcast, {
            onEnter: function () {
                Runtime.stats.deathIn += 1;
                // DeathEventData 是 0x38 字节「按值」压在栈上的：
                //   [esp]=返回地址，[esp+4] 起才是结构体本体（与 GameManager.TakeDamage 同一约定）。
                // 注意不能拿 args[0] —— 那只是结构体前 4 字节（killer），不是结构体地址。
                var b = this.context.esp.add(4);
                var fields = '';
                var presence = '';
                var dead = null;
                var wpnIndex = -1;
                var fixNote = '';
                var callerRva = '';
                try {
                    fields = deathEventFields(b);
                    presence = deathIndexPresence(b);
                    dead = b.add(OFF.Death_dead).readPointer();
                    wpnIndex = b.add(OFF.Death_wpnIndex).readS32();
                } catch (error) {
                    fields = 'read failed: ' + (error && error.message ? error.message : String(error));
                }
                // 调用方 RVA：区分"游戏自己的哪条链在广播死亡"和"我们补发的"。
                try {
                    var ret = this.returnAddress;
                    if (ret && !isNull(ret)) {
                        var retOff = ret.sub(Runtime.base);
                        if (retOff.compare(0) >= 0 && retOff.compare(Runtime.module.size) < 0) {
                            callerRva = '+' + retOff.toString(16);
                        }
                    }
                } catch (_) {}
                // 游戏自己调用时压栈的 MethodInfo*（结构体 0x38 字节后面那个）。
                // 补发广播时带上真实值，少一个未知量。
                try {
                    var mi = b.add(OFF.Death_size).readPointer();
                    if (readable(mi)) Runtime.cache.deathMethodInfo = mi;
                } catch (_) {}
                // 死亡链观察：这次死亡广播是不是发生在我们注入的 TakeDamage 调用里
                if (Runtime.chain.depth > 0) Runtime.chain.inCallBroadcasts += 1;
                // 上一次死亡广播"进了没出" = 上一次被托管异常打断（那一次的目标不会复活）。
                // 这条日志一定会打在"下一次死亡"上，也就是异常现场本身。
                if (Runtime.pendingDeath) {
                    Runtime.stats.deathAborted += 1;
                    log('error', '[deathDiag:abort] 上一次死亡广播进入后没有返回（被异常打断 -> 目标不会复活）: ' +
                        Runtime.pendingDeath.fields);
                }
                Runtime.pendingDeath = { at: Date.now(), fields: fields, dead: dead };
                // 每一笔死亡都登记观察窗口：谁没复活，心跳里会报 *** 击杀后未复活 ***
                registerDeathWatch(dead, Runtime.inDirectDamage ? '[ours]' : '[game]', 'deathIn', true);
                // ---- death_fix_wpn（旧假设，默认关闭，见 config 注释）----
                if (Runtime.config.death_fix_wpn && wpnIndex > 0) {
                    if (isValidWpnKey(wpnIndex)) {
                        Runtime.lastValidWpnIndex = wpnIndex;
                    } else {
                        var fallback = Runtime.lastValidWpnIndex > 0
                            ? Runtime.lastValidWpnIndex
                            : firstValidWpnKey();
                        if (fallback > 0 && fallback !== wpnIndex) {
                            // 结构体是「按值」传进来的：写 [esp+4+0x30] 就是改这次广播看到的值。
                            b.add(OFF.Death_wpnIndex).writeS32(fallback);
                            fixNote = ' ->fix:' + fallback;
                            Runtime.stats.deathWpnFixed += 1;
                            log('warn', '[deathFix] 死亡广播 wpnIndex=' + wpnIndex +
                                ' 不在 WpnDataDictionary，已改为 ' + fallback + '；dead=' + fmtPtr(dead));
                        } else {
                            fixNote = ' (无可用兜底 key)';
                        }
                    }
                }
                if (Runtime.config.death_diag_detail || probeBudget('deathDiagIn', 150)) {
                    log('info', '[deathDiag:deathIn] ' + fields +
                        (presence ? ' | dict: ' + presence : '') +
                        ' | caller=' + (callerRva || '-') + ' m=' + fmtPtr(Runtime.cache.deathMethodInfo) +
                        fixNote);
                }
            },
            onLeave: function () {
                Runtime.stats.deathOut += 1;
                Runtime.pendingDeath = null;
                // 广播完整返回 -> 这次登记的目标不需要兜底
                if (Runtime.currentDeathKey && Runtime.deathWatch[Runtime.currentDeathKey]) {
                    Runtime.deathWatch[Runtime.currentDeathKey].bcDone = true;
                }
                Runtime.currentDeathKey = null;
                if (Runtime.config.death_diag_detail || probeBudget('deathDiagOut', 40)) {
                    log('info', '[deathDiag:deathOut] 死亡广播完整返回');
                }
                // 主线程里顺手跑一次复活兜底 + 补发队列（这里不在任何异常栈上）
                try { drainRebroadcastQueue(); } catch (_) {}
                try { deathRescueTick(); } catch (_) {}
            }
        });

        // 2) 复活调度入口：ModeBase_Nano.RespawnPlayer(this, dead, respawnTime, isNormalRespawn, clearExp)
        //    （终结者的墓碑复活也走这里：Mode_Nano4_Terminator.RespawnPlayer 最后会调基类）
        registerProbeAttach('ModeBase_Nano.RespawnPlayer(deathDiag)', RVA.ModeBase_Nano_RespawnPlayer, {
            onEnter: function () {
                Runtime.stats.respawnScheduled += 1;
                try {
                    var sp = this.context.esp;
                    // this = mode 实例（复活兜底要拿它当 this 调 RespawnPlayer）
                    Runtime.modeBase = sp.add(4).readPointer();
                    var dead = sp.add(8).readPointer();
                    var respawnTime = sp.add(12).readS32();
                    var isNormal = sp.add(16).readU8();
                    var clearExp = sp.add(20).readU8();
                    var key = dead.toString();
                    if (Runtime.deathWatch[key]) {
                        Runtime.deathWatch[key].scheduled = true;
                        // 游戏自己排的复活时间（秒）-> 兜底要让开这段时间，别抢先复活
                        Runtime.deathWatch[key].respawnTimeMs = respawnTime > 0 ? respawnTime * 1000 : 0;
                    }
                    log('info', '[deathDiag:respawnPlayer] dead=' + key +
                        ' respawnTime=' + respawnTime + ' isNormalRespawn=' + isNormal +
                        ' clearExp=' + clearExp + ' [' + fmtRespawnState(playerRespawnState(dead)) + ']');
                } catch (error) {
                    log('warn', '[deathDiag:respawnPlayer] read failed: ' +
                        (error && error.message ? error.message : String(error)));
                }
            }
        });

        // 3) Player.Respawn(float respawnTime, float invisibleTime)：this=[esp+4]
        registerProbeAttach('Player.Respawn(deathDiag)', RVA.Player_Respawn, {
            onEnter: function () {
                Runtime.stats.playerRespawnCalls += 1;
                try {
                    var sp = this.context.esp;
                    var player = sp.add(4).readPointer();
                    var key = player.toString();
                    if (Runtime.deathWatch[key]) {
                        Runtime.deathWatch[key].scheduled = true;
                        var rtSec = sp.add(8).readFloat();
                        if (rtSec > 0 && rtSec < 600) Runtime.deathWatch[key].respawnTimeMs = rtSec * 1000;
                    }
                    log('info', '[deathDiag:playerRespawn] player=' + key +
                        ' respawnTime=' + sp.add(8).readFloat().toFixed(2) +
                        ' invisibleTime=' + sp.add(12).readFloat().toFixed(2));
                } catch (_) {}
            }
        });

        // 4) 受击特效/音效：判断异常是在“命中处理”还是“死亡广播”那一段抛的
        registerProbeAttach('GameManager.PlayHitFxAndSnd(deathDiag)', RVA.GameManager_PlayHitFxAndSnd, {
            onEnter: function () { Runtime.stats.hitFxIn += 1; },
            onLeave: function () { Runtime.stats.hitFxOut += 1; }
        });

        // 5) mode 实例（复活兜底的 this）：死亡链上任意一次调用都能抓到
        registerProbeAttach('ModeBase_Nano.DeathEvent(deathDiag)', RVA.ModeBase_Nano_DeathEvent, {
            onEnter: function () {
                try { Runtime.modeBase = this.context.esp.add(4).readPointer(); } catch (_) {}
            }
        });

        // 6) 死亡链观察（death_diag_chain，默认关）：GameManager.TakeDamage 只读进出钩子。
        //    开了它日志里会出现 [deathDiag:chain] "本次调用内死亡广播次数=N"，
        //    N=0 就是"我们注入的这半截伤害没有触发游戏死亡流程"的铁证。
        //    默认关，是为了不给游戏最热的伤害函数多挂一层 trampoline。
        if (Runtime.config.death_diag_chain) {
            registerProbeAttach('GameManager.TakeDamage(chain)', RVA.GameManager_TakeDamage, {
                onEnter: function () {
                    Runtime.chain.depth += 1;
                    Runtime.chain.inCallBroadcasts = 0;
                },
                onLeave: function () {
                    var inside = Runtime.chain.inCallBroadcasts;
                    Runtime.chain.depth = Math.max(0, Runtime.chain.depth - 1);
                    if (!Runtime.inDirectDamage) return;
                    Runtime.stats.chainTakeDamageCalls += 1;
                    if (inside > 0) Runtime.stats.chainBroadcastInside += 1;
                    if (Runtime.stats.chainTakeDamageCalls <= 20) {
                        log('warn', '[deathDiag:chain] 我们的 TakeDamage 注入返回: 本次调用内死亡广播次数=' + inside +
                            (inside > 0 ? '（完整游戏流程）' : '（★游戏没有广播死亡 -> 目标会躺尸，需要补发/兜底）'));
                    }
                }
            });
        }

        // 7) 托管异常漏斗：默认不装（只有显式 death_diag_raise=true 才装，见上方长注释）
        installRaiseProbe();

        log('info', '[deathDiag] 死亡/复活链诊断已安装（death_diag=true，全部只读；含全字段 dump' +
            (Runtime.config.death_diag_raise ? ' + 托管异常探针(已显式开启，危险)' : '；托管异常探针已禁用(防闪退)') + '）');
    }

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
                // 底板来源 2：TakeDamage 入口的 [esp+4] 就是按值传入的结构体本体
                captureEventTemplate(this.context.esp.add(4), 'TakeDamage');
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
        // onLeave 探针：本轮定位"异常到底停在哪一步"的关键工具。
        // 某函数 onEnter 有日志、onLeave 没有 => 异常就是在它内部抛出来的。
        var leaveProbe = function (tag) {
            return function () {
                if (probeBudget(tag, 30)) probe(tag, 'returned normally');
            };
        };
        registerProbeAttach('Entity.OnEntityHurt(probe)', RVA.Entity_OnEntityHurt, {
            onEnter: hurtProbe('entityHurt', false),
            onLeave: leaveProbe('entityHurtLeave')
        });
        registerProbeAttach('Player.OnEntityHurt(probe)', RVA.Player_OnEntityHurt, {
            onEnter: hurtProbe('playerHurt', true),
            onLeave: leaveProbe('playerHurtLeave')
        });

        // 死亡广播 / PlayHitFxAndSnd 的探针已统一搬到 installDeathDiagnostics()
        // （death_diag 默认开启，无论 verbose_probe 开关都会装），这里不再重复安装，
        // 否则 deathIn/deathOut 会被两个钩子各加一次。
        // 最底层扣血：Entity.OnEntityHurt 内部就是 "HealthData.Hurt(healthData, (int)damage)"
        registerProbeAttach('HealthData.Hurt(probe)', RVA.HealthData_Hurt, {
            onLeave: leaveProbe('healthHurtLeave'),
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

    // ------------------------------------------------------------------
    // 敌人扫描（弹体追踪的"打谁"基础）
    // ------------------------------------------------------------------
    //   与 selectTarget（枪械直伤）的区别：**不做任何视线判定**，
    //   敌我判定只保留两条硬规则：**敌对阵营 + 存活**，永远不打自己人。
    //
    //   scanEnemies(from, cone) 一次扫完，同时给出两个结果：
    //     bestCone = 锥内最近的敌人（cone 为 null 时 = bestAny）
    //     bestAny  = 全场最近的敌人
    //   这样"锥内没人就回退全场最近"不用扫两遍。
    //
    //   cone = { yawDeg, pitchDeg, deg } 就是"准星锥"：
    //     先只保留「参考点 -> 目标」方向与锥轴夹角 <= deg 的敌人，锥内再比距离。
    //     夹角算法与枪械直伤用的完全一致（calculateTargetAngles + angleDistanceDeg），
    //     所以"准星锥"在两条路径上的含义不会漂移。
    //
    //   排序依据 = 到参考点的 3D 直线距离，量到**胸口**（getAimPoint，取不到才退到脚底）。
    //   早期版本量的是"脚底到脚底"，已改成胸口：命中点在胸口，排序和拐弯用同一个点更一致。
    function scanEnemies(from, cone) {
        var result = {
            bestCone: null, bestAny: null,
            enemies: 0,          // 通过硬过滤的敌人总数
            inCone: 0,           // 其中落在准星锥内的数量
            nearestAngle: -1,    // 全场最近的那个敌人与锥轴的夹角（锥空时看它，判断是"背对"还是"锥太小"）
            usedCone: !!(cone && cone.deg > 0)
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
                // 夹角只在启用锥时才算（关锥时这个数没有意义，省一次三角运算）
                var ang = -1;
                if (result.usedCone) {
                    var angles = calculateTargetAngles(from, aim);
                    if (angles) {
                        var a = angleDistanceDeg(angles.targetYawDeg, angles.targetPitchDeg,
                            cone.yawDeg, cone.pitchDeg);
                        if (isFinite(a)) ang = a;
                    }
                }
                if (result.bestAny === null || dist < result.bestAny.dist) {
                    result.bestAny = { player: candidate, dist: dist, angleDeg: ang };
                    // nearestAngle = **全场最近的那个敌人**的夹角（不是"最小夹角"）。
                    // 锥空时看它：若在 90° 以上，说明你是背对着最近的人，不是锥开小了。
                    if (result.usedCone) result.nearestAngle = ang;
                }
                if (!result.usedCone) { result.inCone += 1; continue; }
                if (ang < 0 || ang > cone.deg) continue;   // 锥外 / 夹角读不到：淘汰
                result.inCone += 1;
                if (result.bestCone === null || dist < result.bestCone.dist) {
                    result.bestCone = { player: candidate, dist: dist, angleDeg: ang };
                }
            } catch (_) {}
        }
        if (!result.usedCone) result.bestCone = result.bestAny;
        return result;
    }

    // 纯"全场最近"（不启用准星锥）。
    function pickNearestEnemyFrom(from) {
        return scanEnemies(from, null).bestCone;
    }

    // ------------------------------------------------------------------
    // 弹体追踪的"打谁"策略：**准星锥内距离最近的敌人**
    // ------------------------------------------------------------------
    //   发射时（armMissileHoming 调用）：
    //     锥轴 = 本地玩家相机朝向（readCameraRotation）
    //     锥心 = 眼睛位置（getLocalEyePos）—— 准星锥必须从眼睛量
    //   锥内有人 -> 取锥内最近的那个
    //   锥内没人 -> homing_cone_fallback：
    //       true （默认）= 回退成"全场最近"，保住"对着空气扔雷也能追到人"
    //       false        = 返回 null，这颗弹不追踪、按原弹道直飞
    //   homing_cone_deg = 0 -> 完全关闭锥，等于旧行为（全场最近）
    function pickEnemyForLaunch() {
        var me = getMyPlayer();
        if (isNull(me)) return null;
        var eye = getLocalEyePos(me);
        if (!eye) return null;

        var coneDeg = Runtime.config.homing_cone_deg;
        if (!(coneDeg > 0)) {
            Runtime.stats.coneOff += 1;
            return scanEnemies(eye, null).bestCone;
        }
        var rot = readCameraRotation(me);
        if (!rot) {
            // 读不到相机朝向：宁可"追最近的"也不要完全不追
            Runtime.stats.coneAxisFail += 1;
            return scanEnemies(eye, null).bestCone;
        }
        var scan = scanEnemies(eye, { yawDeg: rot.yawDeg, pitchDeg: rot.pitchDeg, deg: coneDeg });
        if (scan.bestCone) {
            Runtime.stats.coneHit += 1;
            if (probeBudget('homingCone', 20)) {
                probe('homingCone', 'LAUNCH 锥内命中 target=' + fmtPtr(scan.bestCone.player) +
                    ' angle=' + scan.bestCone.angleDeg.toFixed(1) + '/' + coneDeg.toFixed(0) + 'deg' +
                    ' dist=' + scan.bestCone.dist.toFixed(1) +
                    ' 锥内候选=' + scan.inCone + '/' + scan.enemies);
            }
            return scan.bestCone;
        }
        Runtime.stats.coneEmpty += 1;
        if (!Runtime.config.homing_cone_fallback) {
            Runtime.stats.coneEmptyStrict += 1;
            probe('homingCone', 'LAUNCH 锥内无敌人 + 已关闭回退 -> 这颗弹不追踪' +
                ' 全场敌人=' + scan.enemies +
                ' 最近夹角=' + (scan.nearestAngle < 0 ? '-' : scan.nearestAngle.toFixed(1)) +
                ' (锥=' + coneDeg.toFixed(0) + 'deg)');
            return null;
        }
        Runtime.stats.coneFallback += 1;
        probe('homingCone', 'LAUNCH 锥内无敌人 -> 回退全场最近' +
            ' 全场敌人=' + scan.enemies +
            ' 最近夹角=' + (scan.nearestAngle < 0 ? '-' : scan.nearestAngle.toFixed(1)) +
            ' (锥=' + coneDeg.toFixed(0) + 'deg，调大锥角或关掉回退可改行为)');
        return scan.bestAny;
    }

    // 弹体飞行途中换目标（原目标死亡/读不到时）：
    //   锥轴 = 弹体当前速度方向（"继续朝前找"），锥心 = 弹体当前位置。
    //   用速度而不是玩家准星的理由：
    //     1) 弹体已经飞出去了，玩家可能早就看别处，用玩家准星会让弹体突然大幅掉头；
    //     2) 用速度天然避免弹体在半空 180° 掉头，飞行观感更自然。
    //   回退规则与发射时一致（homing_cone_fallback）。
    function pickEnemyForMissileRetarget(mpos, rb) {
        if (!mpos) return null;
        var coneDeg = Runtime.config.homing_cone_deg;
        if (!(coneDeg > 0)) {
            Runtime.stats.coneOff += 1;
            return scanEnemies(mpos, null).bestCone;
        }
        var v = readRigidbodyVelocity(rb);
        var vlen = v ? Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z) : 0;
        if (!(vlen > 0.01)) {
            // 读不到速度（刚出膛/已停住）：退回全场最近
            Runtime.stats.coneAxisFail += 1;
            return scanEnemies(mpos, null).bestCone;
        }
        var hDist = Math.sqrt(v.x * v.x + v.z * v.z);
        if (hDist < 0.01) hDist = 0.01;
        var scan = scanEnemies(mpos, {
            yawDeg: Math.atan2(v.x, v.z) * 180.0 / Math.PI,
            pitchDeg: Math.atan2(v.y, hDist) * 180.0 / Math.PI,
            deg: coneDeg
        });
        if (scan.bestCone) {
            Runtime.stats.coneHit += 1;
            Runtime.stats.coneRetarget += 1;
            if (probeBudget('homingCone', 30)) {
                probe('homingCone', 'RETARGET 锥内命中 target=' + fmtPtr(scan.bestCone.player) +
                    ' angle=' + scan.bestCone.angleDeg.toFixed(1) + '/' + coneDeg.toFixed(0) + 'deg' +
                    ' dist=' + scan.bestCone.dist.toFixed(1) +
                    ' 锥内候选=' + scan.inCone + '/' + scan.enemies);
            }
            return scan.bestCone;
        }
        Runtime.stats.coneEmpty += 1;
        if (!Runtime.config.homing_cone_fallback) {
            Runtime.stats.coneEmptyStrict += 1;
            return null;
        }
        Runtime.stats.coneFallback += 1;
        Runtime.stats.coneRetarget += 1;
        return scan.bestAny;
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
        else if (why === 'hit') s.forgetHit += 1;
        else if (why === 'hit(grenade)') s.forgetHitGrenade += 1;
        else if (why === 'trigger') s.forgetTrigger += 1;
        else if (why === 'timeout') s.forgetTimeout += 1;
        else if (why === 'target-lost') s.forgetLost += 1;
        else if (why === 'no-new-target') s.forgetNoNext += 1;
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
                ' cone=' + Runtime.config.homing_cone_deg.toFixed(0) + 'deg' +
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
            installPipelineProbes();
            installDeathDiagnostics();
            installHomingHooks();
            installGunHook();
            installExplosiveHooks();
            installSkillHooks();
            installStringCaptureHooks();
            installEventTemplateCapture();
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
        Runtime.missileTargets = {};
        Runtime.pendingMissile = null;
        Runtime.cache.ownPlayer = ptr(0);
        Runtime.cache.selectedTarget = null;
        Runtime.cache.selectedAtMs = 0;
        Runtime.cache.emptyString = null;
        Runtime.cache.hitTag = ptr(0);
        Runtime.cache.hitSnd = ptr(0);
        Runtime.cache.hitFx = ptr(0);
        Runtime.cache.capturedTag = false;
        Runtime.cache.eventTemplateValid = false;
        Runtime.cache.eventTemplateWpnIndex = -1;
        Runtime.cache.eventBuf = null;        Runtime.cache.posBuf = null;
        Runtime.cache.rebroadcastQueue = null;
        Runtime.cache.deathMethodInfo = null;
        Runtime.cache.rayWarnLogged = false;
        Runtime.chain.depth = 0;
        Runtime.chain.inCallBroadcasts = 0;
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
        if (input.enable_homing !== undefined) c.enable_homing = input.enable_homing !== false;
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
        if (input.gun_hook_mode !== undefined) {
            // WPN_Gun.Damage 的挂法：attach(默认，推荐) / replace(旧行为)。
            // 钩子是 enable 时装的，改完要重新 enable 才生效。
            var hookMode = String(input.gun_hook_mode);
            if (hookMode === 'attach' || hookMode === 'replace') c.gun_hook_mode = hookMode;
        }
        if (input.damage_override !== undefined) c.damage_override = clampFloat(toNumber(input.damage_override, c.damage_override), 0, 999999);
        if (input.fallback_to_original !== undefined) c.fallback_to_original = input.fallback_to_original === true;
        if (input.gun_ray_redirect !== undefined) c.gun_ray_redirect = input.gun_ray_redirect !== false;
        if (input.death_rescue_max_tries !== undefined) {
            c.death_rescue_max_tries = Math.max(1, Math.floor(toNumber(input.death_rescue_max_tries, c.death_rescue_max_tries)));
        }
        if (input.death_rescue_retry_gap_ms !== undefined) {
            c.death_rescue_retry_gap_ms = clampFloat(toNumber(input.death_rescue_retry_gap_ms, c.death_rescue_retry_gap_ms), 500, 60000);
        }
        if (input.death_diag_chain !== undefined) c.death_diag_chain = input.death_diag_chain === true;
        if (input.entry_fallback !== undefined) c.entry_fallback = input.entry_fallback !== false;
        if (input.use_event_template !== undefined) c.use_event_template = input.use_event_template !== false;
        if (input.local_eye_height !== undefined) c.local_eye_height = clampFloat(toNumber(input.local_eye_height, c.local_eye_height), 0, 5);
        if (input.target_cache_ms !== undefined) c.target_cache_ms = clampFloat(toNumber(input.target_cache_ms, c.target_cache_ms), 0, 1000);

        if (input.diagnostic_log !== undefined) c.diagnostic_log = input.diagnostic_log !== false;
        if (input.log_every !== undefined) c.log_every = Math.max(1, Math.floor(toNumber(input.log_every, c.log_every)));
        if (input.homing_speed !== undefined) c.homing_speed = clampFloat(toNumber(input.homing_speed, c.homing_speed), 0, 500);
        if (input.homing_turn !== undefined) c.homing_turn = clampFloat(toNumber(input.homing_turn, c.homing_turn), 0.05, 1);
        if (input.homing_retarget !== undefined) c.homing_retarget = input.homing_retarget !== false;
        if (input.homing_max_ms !== undefined) c.homing_max_ms = clampFloat(toNumber(input.homing_max_ms, c.homing_max_ms), 500, 120000);
        if (input.homing_pending_ms !== undefined) c.homing_pending_ms = clampFloat(toNumber(input.homing_pending_ms, c.homing_pending_ms), 50, 5000);
        // 弹体追踪的"打谁"策略：准星锥角度（0=关闭，回到全场最近）+ 锥内没人是否回退
        if (input.homing_cone_deg !== undefined) c.homing_cone_deg = clampFloat(toNumber(input.homing_cone_deg, c.homing_cone_deg), 0, 180);
        if (input.homing_cone_fallback !== undefined) c.homing_cone_fallback = input.homing_cone_fallback !== false;
        if (input.death_diag !== undefined) c.death_diag = input.death_diag !== false;
        if (input.death_diag_ms !== undefined) c.death_diag_ms = clampFloat(toNumber(input.death_diag_ms, c.death_diag_ms), 3000, 120000);
        if (input.death_diag_detail !== undefined) c.death_diag_detail = input.death_diag_detail === true;
        // ★默认关闭的"托管异常漏斗探针"；改完要重新 enable 才会重装钩子
        if (input.death_diag_raise !== undefined) c.death_diag_raise = input.death_diag_raise === true;
        if (input.death_fix_wpn !== undefined) c.death_fix_wpn = input.death_fix_wpn === true;
        if (input.death_fix_respawn !== undefined) c.death_fix_respawn = input.death_fix_respawn !== false;
        if (input.death_respawn_grace_ms !== undefined) c.death_respawn_grace_ms = clampFloat(toNumber(input.death_respawn_grace_ms, c.death_respawn_grace_ms), 1000, 120000);
        if (input.death_fix_broadcast !== undefined) c.death_fix_broadcast = input.death_fix_broadcast !== false;
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
            ' homing=' + c.enable_homing +
            ' explosives=' + c.enable_explosives +
            ' skills=' + c.enable_skill_projectiles +
            ' homingSpeed=' + c.homing_speed + ' homingTurn=' + c.homing_turn +
            ' retarget=' + c.homing_retarget + ' maxMs=' + c.homing_max_ms +
            ' homingCone=' + c.homing_cone_deg + 'deg coneFallback=' + c.homing_cone_fallback +
            ' mode=' + c.target_mode +
            ' cone=' + c.max_angle_deg + ' maxDist=' + c.max_distance +
            ' entry=' + c.damage_entry +
            ' gunHookMode=' + c.gun_hook_mode +
            ' rayRedirect=' + c.gun_ray_redirect +
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
            ' gunHookMode=' + Runtime.config.gun_hook_mode +
            ' guns=' + Runtime.config.enable_guns +
            ' homing=' + Runtime.config.enable_homing +
            ' explosives=' + Runtime.config.enable_explosives +
            ' skills=' + Runtime.config.enable_skill_projectiles +
            ' homingTurn=' + Runtime.config.homing_turn +
            ' homingCone=' + Runtime.config.homing_cone_deg + 'deg fallback=' + Runtime.config.homing_cone_fallback +
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
            template_captured: Runtime.stats.templateCaptured,
            template_used: Runtime.stats.templateUsed,
            template_rejected: Runtime.stats.templateRejected,
            invincible_cleared: Runtime.stats.invincibleCleared,
            event_template_wpn_index: Runtime.cache.eventTemplateWpnIndex,
            death_in: Runtime.stats.deathIn,
            death_out: Runtime.stats.deathOut,
            death_aborted: Runtime.stats.deathAborted,
            death_rescued: Runtime.stats.deathRescued,
            death_rebroadcast: Runtime.stats.deathRebroadcast,
            death_rebroadcast_deferred: Runtime.stats.rebroadcastDeferred,
            death_rebroadcast_deferred_ok: Runtime.stats.rebroadcastDeferredOk,
            death_rescue_attempts: Runtime.stats.deathRescueAttempts,
            ray_redirect_shots: Runtime.stats.rayRedirectShots,
            ray_redirect_hits: Runtime.stats.rayRedirectHits,
            ray_redirect_miss: Runtime.stats.rayRedirectMiss,
            ray_redirect_bad_args: Runtime.stats.rayRedirectBadArgs,
            chain_take_damage_calls: Runtime.stats.chainTakeDamageCalls,
            chain_broadcast_inside: Runtime.stats.chainBroadcastInside,
            death_rescue_failed: Runtime.stats.deathRescueFailed,
            death_rescue_rejected: Runtime.stats.deathRescueRejected,
            death_raise_calls: Runtime.stats.raiseCount,
            respawn_scheduled: Runtime.stats.respawnScheduled,
            player_respawn_calls: Runtime.stats.playerRespawnCalls,
            half_dead_watched: Runtime.stats.halfDeadWatched,
            half_dead_recovered: Runtime.stats.halfDeadRecovered,
            half_dead_no_revive: Runtime.stats.halfDeadConfirmed,
            last_fail_phase: Runtime.stats.lastFailPhase,
            death_wpn_fixed: Runtime.stats.deathWpnFixed,
            hit_fx_in: Runtime.stats.hitFxIn,
            hit_fx_out: Runtime.stats.hitFxOut,
            last_damage: Runtime.stats.lastDamage,
            last_target_angle: Runtime.stats.lastTargetAngle,
            last_target_distance: Runtime.stats.lastTargetDistance,
            error_count: Runtime.stats.errorCount,
            last_error: Runtime.stats.lastError,
            // ---- 探针字段 ----
            own_player_source: Runtime.stats.ownPlayerSource,
            // ---- 弹体追踪 ----
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
            entry_fallback_count: Runtime.stats.entryFallback,
            gun_hook_disabled: Runtime.stats.gunHookDisabled,
            gun_skipped: Runtime.stats.gunSkipped,
            gun_skip_failed: Runtime.stats.gunSkipFailed,
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
