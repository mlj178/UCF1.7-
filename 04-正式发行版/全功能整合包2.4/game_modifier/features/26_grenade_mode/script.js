"use strict";

/*
 * feature_id: grenade_mode_lock999_keep_weapon_tuner
 * version: 2.12.8
 *
 * 基于 lock999_keep_weapon v1.1：
 * - 保留锁定 WPN_Throw.ammoData 数量。
 * - 保留只保护当前 WPN_Throw 对象不被 PlayerWeapons.Remove 删除。
 *
 * 新增运行时手雷参数修改：
 * - 只追踪 WPN_Throw.<Throw>b__10_0 捕获到的 missile。
 * - RPG / AT4 / Nano 不会进入 trackedMissiles，不修改。
 * - Bot 是否修改由 owner_filter 控制。
 * - v1.3 删除：穿墙、碰撞爆炸、距离衰减。
 * - v1.3 增加：CreateExplosion 参数级 damage/range 修改。
 * - v1.4 新增：throwReady 写入开关，命名为“连投就绪开关”。
 * - v1.4 新增：投掷动作加速，投掷上下文内临时调用 Animator.set_speed。
 * - v2.0 新增：VirtualGrenadeMode Observer，只观察 PlayerWeapons 切枪链路，不拦截。
 * - v2.1 新增：无限手雷作用范围下拉框 local_only / all_players。
 * - v2.1 新增：Bot 手雷行为观察，只统计 bot 是否拥有/选择/投掷手雷，不强制投掷。
 * - v2.2 新增：Bot 攻击入口观察，记录 WPN_Gun/WPN_RPG 的 BotControl 与 Fire/GunShoot 链路。
 * - v2.3 新增：Bot 只允许手雷手雷模式，记录 bot 手雷并在 bot 切枪后纠正回 slot=3。
 * - v2.4 新增：Bot 切枪入口强重定向，在 Select/SetCurrentWeapon onEnter 直接改为 slot=3 手雷。
 * - v2.5 新增：BotGrenadeRecord，只允许 Grenade，不包含 FlashBang / SmokeGrenade；主控 Bot.SelectWeapon + GetValidSlot，GiveWeapon 可选拦截非手雷。
 * - v2.5.1 修复：彻底禁用 v2.4 旧入口改 args 重定向，避免 RangeError 自动关闭导致玩家锁999失效。
 * - v2.6 新增：Bot.UseWeapon 投掷驱动，在bot攻击入口用已缓存Grenade调用 WPN_Throw.Throw。
 * - v2.7 新增：VirtualBotControl，替换枪/RPG的BotControl，在官方bot攻击控制层转为手雷Throw。
 * - v2.8 新增：BotAI Probe，观察/接管 UpdateAction、CheckAttackTarget、FindAttackTarget，并可在UpdateAction后置驱动手雷投掷。
 * - v2.9 新增：根据v2.8日志改用 CheckAttackTarget / CameraRotation onLeave 作为手雷投掷触发点。
 * - v2.10.3 调整：删除v2.10.2可见性强化内容；Bot手雷模式UI默认开启；AI驱动冷却默认1000ms。
 * - v2.10.4 新增：Bot投掷状态机，IDLE/SELECTING/READY/THROWING/COOLDOWN，避免每次AI命中直接裸Throw。
 * - v2.11.0 调整：默认不再阻止Bot获得非Grenade武器，保留官方武器/模型/动作状态，减少木桩、空枪、聚堆。
 * - v2.11.1 调整：修正UI仍默认拦截非Grenade发枪的问题；伤害/爆炸范围/飞行速度新增应用对象下拉框。
 * - v2.11.2 调整：官方选武器优先，默认关闭Bot.SelectWeapon/GetValidSlot全局强制slot=3；仅状态机投掷阶段临时Select(3)。
 * - v2.11.3 调整：伤害/范围/速度作用对象改为my_player/all_players；默认禁止Bot枪械原BotControl开火。
 * - v2.11.4 新增：Bot出生/首次识别保护时间与attackTarget稳定时间，避免刚出生马上扔雷。
 * - v2.11.5 修复：统一Bot投掷许可层，拦截AI状态机/Bot.UseWeapon/VirtualBotControl/底层Throw驱动所有路径。
 * - v2.11.6 修复：复活/重新发枪时重置Bot生命周期，让后续复活也重新触发出生保护。
 * - v2.12.0 终版清理：删除旧重定向/手雷模式纠正/全局选雷/GetValidSlot强制/发枪拦截/旧局部出生保护等失败方案。
 * - v2.12.1 精简：删除死统计、UpdateAction残留、SmartAI/v2.10.1路径/距离/抛物线实验残留，并统一命名。
 * - v2.12.2 UI清理：删除界面和启动说明里的v2.10/v2.10.1 SmartAI实验文案。
 * - v2.12.3 修复：删除_collect_config中残留的旧距离参数旧距离配置，修复开启失败。
 */

const FEATURE_ID = "grenade_mode_lock999_keep_weapon_tuner";
const VERSION = "2.12.8";
const MODULE_NAME = "GameAssembly.dll";
const CALL_CONV = "mscdecl";

const RVA = {
    WPN_Throw_Throw_b__10_0: 0x00B597B0,
    WPN_Throw_Throw: 0x00B6AD80,
    WPN_Throw_UnDeploy: 0x00B6B010,
    WPN_Throw_Deploy: 0x00B6A6F0,
    WPN_Throw_Init: 0x00B6A7F0,
    WPN_Throw_OnAnimationEnd: 0x00B6A930,
    WPN_Throw_OnFireAnimEnd: 0x00B6AA90,
    WPN_Throw_OnGenerateFromOwner: 0x00B6AB70,

    PlayerWeapons_AutoSelect: 0x00B15A90,
    PlayerWeapons_GetValidSlot: 0x00B15CE0,
    PlayerWeapons_RemoveAll: 0x00B15EB0,
    PlayerWeapons_Remove: 0x00B15FD0,
    PlayerWeapons_SelectByMouseRoll: 0x00B164E0,
    PlayerWeapons_SelectFKeyWeapon: 0x00B16540,
    PlayerWeapons_SelectLastOrAutoSelect: 0x00B16650,
    PlayerWeapons_SelectLast: 0x00B16680,
    PlayerWeapons_Select: 0x00B166A0,
    PlayerWeapons_SetCurrentWeapon: 0x00B16A70,
    PlayerWeapons_SetWeapon: 0x00B16BF0,
    Player_get_isMyPlayer: 0x00B55FD0,
    Player_get_wpns: 0x001CF190,
    Weapon_get_isMyWeapon: 0x00B6E1D0,
    CFAnimator_PlayWeaponAnimWithSameTag: 0x00B34DE0,
    UnityEngine_Animator_PlayInFixedTime_279610832: 0x00AA85D0,
    UnityEngine_Animator_set_speed: 0x00AA8C30,

    WPN_Gun_BotControl: 0x00B60C20,
    WPN_Gun_SniperBotControl: 0x00B632B0,
    WPN_Gun_GunShootFunction: 0x00B62110,
    WPN_Gun_GunShoot_Logic: 0x00B62170,
    WPN_Gun_GunShoot_NoCheck: 0x00B621F0,
    WPN_Gun_GunShoot: 0x00B624C0,
    WPN_Gun_GenerateBullet: 0x00B61F40,
    WPN_RPG_BotControl: 0x00B66D70,
    WPN_RPG_Fire: 0x00B670A0,
    WPN_RPG_OnFireBtnPressed: 0x00B67700,
    WPN_RPG_OnFireBtnUnPressed: 0x00B67720,

    GameManager_GetWeapon: 0x00AFADB0,
    GameManager_GiveWeapon: 0x00AFB390,
    Bot_SelectWeapon: 0x00B32250,
    Bot_UseWeapon: 0x00B33BD0,
    Bot_CheckAttackTarget: 0x00B2DD80,
    Bot_CheckHitBox: 0x00B2E150,
    Bot_FindAttackTarget: 0x00B2E840,
    Bot_TrySetAttackTarget: 0x00B32800,
    Bot_AddSelectWpnAction: 0x00B2CE00,
    Bot_CameraRotation: 0x00B2D670,

    UnityEngine_Component_get_transform: 0x0032CF40,
    UnityEngine_Transform_get_position_Injected: 0x003F4280,

    WPN_GRENADE_CreateExplosion: 0x00B5CC40,
    WPN_GRENADE_Damage: 0x00B5CFB0,
    WPN_GRENADE_OnLifeTimerEnd: 0x00B5D240,
    WPN_GRENADE_SetMissileData: 0x00B5D3F0,
    WPN_GRENADE_TryExplosion: 0x00B5D4A0,
    WPN_GRENADE_Work: 0x00B5D6C0,

    WPN_Missile_FixedUpdate: 0x00B660C0,
    WPN_Missile_Recycle: 0x00B66240,
    WPN_Missile_SetOwner: 0x00B66390,
    WPN_Missile_SetWeaponData: 0x00B663C0,
    WPN_Missile_Work: 0x00B664D0
};

const Offsets = {
    WPN_Throw_ammoData: 0xF0,
    WPN_Throw_throwReady: 0xF4,
    CFAnimator_animator: 0x40,
    Weapon_data: 0x68,
    WeaponData_wpnClass: 0x10,
    PlayerWeapons_owner: 0x08,
    Bot_thisPlayer: 0x24,
    Bot_attackTarget: 0x2C, // 从 CheckAttackTarget 汇编观察：esi+2C 被当作当前攻击目标指针
    WeaponData_slot: 0x8C,
    Ammo_key: 0x08,
    Ammo_hidden: 0x0C,
    Ammo_plain_or_fake: 0x10,

    Missile_owner: 0x30,
    Missile_ownerInitalTeam: 0x34,
    Missile_weaponData: 0x38,
    Missile_shootSpeed: 0x4C,

    Grenade_expRange: 0x5C,
    Grenade_expDamage: 0x60
};

const DefaultConfig = {
    lock999_enabled: true,
    infinite_grenade_scope: "all_players", // local_only 或 all_players
    target_count: 999,
    sync_plain_value: false,

    force_throw_ready_enabled: true,
    force_throw_ready_scope: "local_only",
    force_throw_ready_value: true,
    force_throw_ready_on_throw_leave: true,
    force_throw_ready_on_deploy: true,
    force_throw_ready_on_animation_end: true,
    force_throw_ready_max_per_second: 10,
    force_throw_ready_window_ms: 1000,

    throw_anim_speed_enabled: false,
    throw_anim_speed_value: 1.6,
    throw_anim_speed_restore_value: 1.0,
    throw_anim_speed_restore_on_end: true,

    lock_on_throw_enter: true,
    lock_on_throw_leave: true,
    lock_on_deploy: true,
    lock_on_unDeploy: true,
    lock_on_animation_end: true,
    lock_on_init: true,
    lock_on_generate_from_owner: true,

    protect_weapon_remove: true,
    protect_ttl_ms: 5000,
    max_protected_weapons: 64,

    runtime_tuner_enabled: true,
    owner_filter: "local_only",
    missile_ttl_ms: 8000,
    max_tracked_missiles: 128,

    enable_damage: true,
    damage_value: 25.0,
    damage_apply_scope: "my_player",
    enable_range: true,
    range_value: 2.5,
    range_apply_scope: "my_player",
    enable_shoot_speed: true,
    shoot_speed_value: 5.0,
    shoot_speed_apply_scope: "my_player",

    tune_on_capture: true,
    tune_on_set_missile_data: true,
    tune_on_try_explosion: true,
    tune_on_damage: true,
    tune_on_life_timer_end: true,
    tune_on_work: true,
    tune_on_fixed_update: true,

    virtual_grenade_observer_enabled: false,
    virtual_grenade_observer_verbose: false,
    bot_grenade_behavior_observer_enabled: false,
    bot_attack_observer_enabled: false,
    bot_grenade_mode_enabled: false,
    bot_grenade_throw_slot: 3,
    bot_grenade_force_scope_all_players: true,
    bot_grenade_record_enabled: true,
    bot_grenade_active_give_enabled: true,
    bot_grenade_active_give_cooldown_ms: 1500,
    virtual_grenade_giveweapon_enabled: true,
    virtual_grenade_preserve_original_weapons: true,
    virtual_grenade_log_interval_ms: 1000,
    bot_throw_drive_enabled: true,
    bot_throw_drive_useweapon_enabled: true,
    bot_throw_drive_skip_original_useweapon_on_success: true,
    bot_throw_drive_cooldown_ms: 2500,
    bot_throw_drive_force_ready: true,
    bot_throw_drive_lock_before_after: true,
    bot_throw_drive_log_interval_ms: 1000,
    virtual_botcontrol_enabled: true,
    virtual_botcontrol_replace_botcontrol: true,
    virtual_botcontrol_gun_enabled: true,
    virtual_botcontrol_sniper_enabled: true,
    virtual_botcontrol_rpg_enabled: true,
    virtual_botcontrol_skip_original_on_success: true,
    bot_suppress_gun_fire_enabled: true,
    bot_suppress_gun_fire_when_no_grenade: true,
    virtual_botcontrol_log_interval_ms: 1000,
    bot_ai_probe_enabled: false,
    bot_ai_probe_verbose: false,
    bot_ai_hook_drive_enabled: true,
    bot_ai_checkattack_drive_enabled: true,
    bot_ai_camerarotation_drive_enabled: true,
    bot_ai_trysettarget_drive_enabled: false,
    bot_ai_hook_drive_require_target: true,
    bot_ai_hook_drive_cooldown_ms: 1000,
    bot_throw_state_machine_enabled: true,
    bot_throw_state_select_delay_ms: 80,
    bot_throw_state_ready_delay_ms: 0,
    bot_throw_state_timeout_ms: 1200,
    bot_throw_state_log_interval_ms: 500,
    bot_throw_unified_gate_enabled: true,
    bot_throw_spawn_grace_enabled: true,
    bot_throw_spawn_grace_ms: 3000,
    bot_throw_target_stable_enabled: true,
    bot_throw_target_stable_ms: 700,
    bot_throw_first_throw_extra_delay_ms: 1000,
    bot_throw_respawn_reset_enabled: true,
    bot_throw_respawn_reset_on_removeall: true,
    bot_throw_respawn_reset_on_giveweapon: true,
    bot_throw_respawn_reset_on_grenade_change: true,
    bot_throw_respawn_reset_cooldown_ms: 1500,

    smart_grenade_ai_enabled: true,
    smart_grenade_require_official_visible: true,
    smart_grenade_recent_visible_ms: 350,

    bot_ai_probe_log_interval_ms: 1000,
    bot_attack_summary_interval_ms: 5000,
    bot_grenade_summary_interval_ms: 5000,
    observe_set_current_weapon: false,
    verbose_log_enabled: false,
    log_interval_ms: 1000,
    max_error_before_disable: 14
};

const Runtime = {
    enabled: false,
    initialized: false,
    generation: 0,
    moduleBase: ptr(0),
    hooks: [],
    replacements: [],
    config: Object.assign({}, DefaultConfig),
    natives: {},
    protectedWeapons: {},
    trackedMissiles: {},
    explosionContexts: {},
    throwAnimContexts: {},
    touchedAnimators: {},
    botGrenadeWeapons: {},
    botGrenadeWeaponAliases: {},
    botGrenadeWeaponIndex: {},
    knownGrenadeWeaponIndexes: {},
    lastBotGrenadeWeaponIndex: -1,
    botGrenadeGiveLast: {},
    botThrowDriveLast: {},
    botAiLastDrive: {},
    botAiOfficialVisible: {},
    botThrowStates: {},
    botLifeStates: {},
    forceThrowReadyWindows: {},
    pendingThrowReadyTimers: {},
    stats: {
        hook_hits: 0,
        lock_attempts: 0,
        lock_writes: 0,
        lock_skipped_same: 0,
        sync_plain_writes: 0,
        throw_hits: 0,
        onFireAnimEnd_hits: 0,
        throw_ready_writes: 0,
        throw_ready_skipped: 0,
        throw_anim_context_push: 0,
        throw_anim_context_pop: 0,
        playWeaponAnim_hits: 0,
        playInFixedTime_hits: 0,
        anim_speed_writes: 0,
        anim_speed_restores: 0,
        deploy_hits: 0,
        unDeploy_hits: 0,
        init_hits: 0,
        generate_hits: 0,
        animationEnd_hits: 0,
        protected_count: 0,
        protected_expired: 0,
        remove_hits: 0,
        remove_blocked: 0,
        remove_allowed: 0,
        observer_hits: 0,
        observer_select_hits: 0,
        observer_setCurrent_hits: 0,
        observer_setWeapon_hits: 0,
        observer_autoSelect_hits: 0,
        observer_getValidSlot_hits: 0,
        observer_mouseRoll_hits: 0,
        observer_fKey_hits: 0,
        observer_selectLast_hits: 0,
        observer_selectLastOrAuto_hits: 0,
        observer_removeAll_hits: 0,
        observer_local_owner_hits: 0,
        observer_nonlocal_owner_hits: 0,
        infinite_scope_local_skip: 0,
        infinite_scope_all_apply: 0,
        infinite_scope_local_apply: 0,
        bot_throw_weapon_seen: 0,
        bot_throw_weapon_selected: 0,
        bot_throw_method_hits: 0,
        bot_missile_captured: 0,
        bot_remove_throw_hits: 0,
        bot_summary_count: 0,
        bot_attack_summary_count: 0,
        gun_bot_control_hits: 0,
        gun_sniper_bot_control_hits: 0,
        gun_shoot_hits: 0,
        gun_shoot_botlike_hits: 0,
        gun_generate_bullet_hits: 0,
        gun_generate_bullet_botlike_hits: 0,
        rpg_bot_control_hits: 0,
        rpg_fire_hits: 0,
        rpg_fire_botlike_hits: 0,
        rpg_on_fire_pressed_hits: 0,
        bot_attack_entry_hits: 0,
        bot_grenade_records: 0,
        bot_grenade_multikey_records: 0,
        bot_grenade_alias_hits: 0,
        bot_grenade_reacquire_attempts: 0,
        bot_grenade_reacquire_success: 0,
        bot_grenade_reacquire_failed: 0,
        bot_grenade_reacquire_select_calls: 0,
        bot_grenade_known_index_hits: 0,
        bot_grenade_active_give_attempts: 0,
        bot_grenade_active_give_success: 0,
        bot_grenade_active_give_failed: 0,
        bot_grenade_active_give_cooldown: 0,
        bot_grenade_temp_select_calls: 0,
        bot_grenade_temp_select_skipped_no_grenade: 0,
        vg_giveweapon_hits: 0,
        vg_giveweapon_bot_hits: 0,
        vg_giveweapon_allowed_grenade: 0,
        vg_giveweapon_preserved_nongrenade: 0,
        vg_giveweapon_observed_nongrenade: 0,
        vg_giveweapon_errors: 0,
        bot_useweapon_hits: 0,
        bot_throw_drive_attempts: 0,
        bot_throw_drive_success: 0,
        bot_throw_drive_original_useweapon: 0,
        bot_throw_drive_skipped_disabled: 0,
        bot_throw_drive_skipped_no_pw: 0,
        bot_throw_drive_skipped_no_grenade: 0,
        bot_throw_drive_skipped_cooldown: 0,
        bot_throw_drive_skipped_not_bot: 0,
        bot_throw_drive_force_ready_writes: 0,
        bot_throw_drive_errors: 0,
        vbc_gun_botcontrol_hits: 0,
        vbc_sniper_botcontrol_hits: 0,
        vbc_rpg_botcontrol_hits: 0,
        vbc_attempts: 0,
        vbc_success: 0,
        vbc_original_calls: 0,
        vbc_suppressed_original_calls: 0,
        vbc_suppress_no_grenade: 0,
        vbc_suppress_cooldown: 0,
        vbc_skipped_disabled: 0,
        vbc_skipped_no_bot: 0,
        vbc_skipped_no_pw: 0,
        vbc_skipped_no_grenade: 0,
        vbc_skipped_cooldown: 0,
        vbc_errors: 0,
        bot_ai_checkattack_hits: 0,
        bot_ai_checkhitbox_hits: 0,
        bot_ai_findtarget_hits: 0,
        bot_ai_trysettarget_hits: 0,
        bot_ai_addselect_hits: 0,
        bot_ai_camerarotation_hits: 0,
        bot_ai_target_seen: 0,
        bot_ai_target_missing: 0,
        bot_ai_hook_drive_attempts: 0,
        bot_ai_hook_drive_success: 0,
        bot_ai_checkattack_drive_success: 0,
        bot_ai_camerarotation_drive_success: 0,
        bot_ai_trysettarget_drive_success: 0,
        bot_ai_hook_drive_skipped_disabled: 0,
        bot_ai_hook_drive_skipped_no_target: 0,
        bot_ai_hook_drive_skipped_no_pw: 0,
        bot_ai_hook_drive_skipped_no_grenade: 0,
        bot_ai_hook_drive_skipped_cooldown: 0,
        bot_throw_sm_eval: 0,
        bot_throw_sm_started: 0,
        bot_throw_sm_selecting: 0,
        bot_throw_sm_ready: 0,
        bot_throw_sm_throwing: 0,
        bot_throw_sm_success: 0,
        bot_throw_sm_cooldown: 0,
        bot_throw_sm_reset: 0,
        bot_throw_sm_timeout: 0,
        bot_throw_sm_select_fail: 0,
        bot_throw_sm_throw_fail: 0,
        bot_throw_sm_invalid: 0,
        bot_throw_spawn_first_seen: 0,
        bot_throw_spawn_grace_skipped: 0,
        bot_throw_target_changed: 0,
        bot_throw_target_stable_skipped: 0,
        bot_life_first_seen: 0,
        bot_throw_gate_eval: 0,
        bot_throw_gate_allowed: 0,
        bot_throw_gate_block_spawn: 0,
        bot_throw_gate_block_first_extra: 0,
        bot_throw_gate_block_target_unstable: 0,
        bot_throw_gate_block_cooldown: 0,
        bot_throw_gate_block_no_grenade: 0,
        bot_throw_gate_block_unknown_bot: 0,
        bot_throw_gate_block_not_bot: 0,
        bot_life_respawn_reset: 0,
        bot_life_reset_removeall: 0,
        bot_life_reset_giveweapon: 0,
        bot_life_reset_grenade_change: 0,
        bot_life_reset_cooldown_skip: 0,
        smart_ai_eval: 0,
        smart_ai_allowed: 0,
        smart_ai_skipped_official_visibility: 0,
        smart_ai_official_visible_true: 0,
        smart_ai_official_visible_false: 0,
        smart_ai_position_ok: 0,
        smart_ai_position_unknown: 0,
        bot_ai_errors: 0,
        observer_grenade_class_hits: 0,
        observer_non_grenade_class_hits: 0,
        setCurrent_hits: 0,
        setCurrent_slot3_clear: 0,
        capture_hits: 0,
        tracked_count: 0,
        tracked_expired: 0,
        owner_local_pass: 0,
        owner_local_fail: 0,
        owner_unknown: 0,
        tune_attempts: 0,
        tune_applied: 0,
        tune_skipped_not_tracked: 0,
        tune_skipped_owner: 0,
        grenade_field_writes: 0,
        missile_speed_writes: 0,
        setMissileData_hits: 0,
        createExplosion_hits: 0,
        createExplosion_param_writes: 0,
        tryExplosion_hits: 0,
        damage_hits: 0,
        lifeTimer_hits: 0,
        grenadeWork_hits: 0,
        missileWork_hits: 0,
        fixedUpdate_hits: 0,
        setOwner_hits: 0,
        setWeaponData_hits: 0,
        recycle_hits: 0,
        skipped_null: 0,
        skipped_invalid: 0,
        error_count: 0,
        last_error: "",
        last_hook: "",
        cleanup_count: 0
    },
    logLimiter: {}
};

function nowIso() { try { return (new Date()).toISOString(); } catch (e) { return "" + Date.now(); } }
const NoisyInfoMessages = {
    "Hook 已安装": true,
    "Replace 已安装": true,
    "配置已更新": true,
    "运行状态已重置": true,
    "已记录当前手雷武器保护对象": true,
    "手雷数量已锁定并保护武器对象": true,
    "Bot统一投掷许可拦截": true,
    "Bot手雷记录": true,
    "BotAI触发投掷跳过": true,
    "BotGrenadeRecord.GiveWeapon": true,
    "Bot主动补发Grenade成功": true,
    "Bot投掷驱动跳过": true,
    "Bot枪械开火已禁止": true,
    "Bot主动补发Grenade失败": true,
    "Bot手雷补记录失败": true,
    "VirtualBotControl未接管": true,
    "BotGrenadeRecord跳过": true,
    "Bot生命周期已重置": true,
    "Bot目标变化": true
};
function normalizeLogLevel(level) {
    const text = (level || "INFO").toString().toLowerCase();
    if (text === "warn") return "warning";
    if (text === "error") return "error";
    return "info";
}
function shouldEmitLog(level, message) {
    if ((level || "INFO").toString().toUpperCase() !== "INFO") return true;
    if (Runtime.config.verbose_log_enabled) return true;
    return !NoisyInfoMessages[message || ""];
}
function emit(level, message, data) {
    try {
        const msg = message || "";
        if (!shouldEmitLog(level, msg)) return;
        send({
            type: "log",
            level: normalizeLogLevel(level),
            module: "手雷模式",
            message: msg,
            audience: "dev",
            dev_detail: JSON.stringify({
                feature_id: FEATURE_ID,
                version: VERSION,
                time: nowIso(),
                data: data || {}
            })
        });
    } catch (e) {}
}
function log(message, data) { emit("INFO", message, data || {}); }
function warn(message, data) { emit("WARN", message, data || {}); }
function recordError(where, e) {
    Runtime.stats.error_count += 1;
    Runtime.stats.last_error = where + ": " + e;
    emit("ERROR", "异常：" + where, { where: where, error: "" + e, error_count: Runtime.stats.error_count });
    const maxErrors = Math.max(1, parseInt(Runtime.config.max_error_before_disable, 10) || 14);
    if (Runtime.stats.error_count >= maxErrors) {
        recoverRuntimeAfterErrorThreshold(where);
    }
}
function logOnce(key, message, intervalMs, data) {
    const now = Date.now();
    const wait = intervalMs || Runtime.config.log_interval_ms || 1000;
    const last = Runtime.logLimiter[key] || 0;
    if (now - last < wait) return;
    Runtime.logLimiter[key] = now;
    log(message, data || {});
}
function ptrStr(p) { try { return p ? p.toString() : "0x0"; } catch (e) { return "invalid"; } }
function isReadablePtr(p) { try { if (!p || p.isNull()) return false; p.readU8(); return true; } catch (e) { return false; } }
function ensureModule() {
    if (!Runtime.moduleBase.isNull()) return Runtime.moduleBase;
    const m = Process.findModuleByName(MODULE_NAME);
    if (!m) throw new Error(MODULE_NAME + " not found");
    Runtime.moduleBase = m.base;
    log("找到 GameAssembly.dll", { base: Runtime.moduleBase.toString() });
    return Runtime.moduleBase;
}
function addrOf(rva) { return ensureModule().add(rva); }
function addHook(name, rva, callbacks) {
    const address = addrOf(rva);
    const h = Interceptor.attach(address, callbacks);
    Runtime.hooks.push({ name: name, handle: h, address: address });
    log("Hook 已安装", { name: name, address: address.toString() });
}
function readPointer(base, offset) { try { if (!isReadablePtr(base)) return ptr(0); return base.add(offset).readPointer(); } catch (e) { return ptr(0); } }
function safeReadPointer(base, offset, reason) {
    try {
        if (!isReadablePtr(base)) { Runtime.stats.skipped_null += 1; return ptr(0); }
        const p = base.add(offset).readPointer();
        if (!isReadablePtr(p)) { Runtime.stats.skipped_invalid += 1; return ptr(0); }
        return p;
    } catch (e) { Runtime.stats.skipped_invalid += 1; recordError("safeReadPointer:" + reason, e); return ptr(0); }
}
function safeReadU32(p, offset, reason) { try { if (!isReadablePtr(p)) return null; return p.add(offset).readU32(); } catch (e) { recordError("safeReadU32:" + reason, e); return null; } }
function safeWriteU32(p, offset, value, reason) { try { if (!isReadablePtr(p)) return false; p.add(offset).writeU32(value >>> 0); return true; } catch (e) { recordError("safeWriteU32:" + reason, e); return false; } }
function safeReadU8(p, offset, reason) { try { if (!isReadablePtr(p)) return null; return p.add(offset).readU8(); } catch (e) { recordError("safeReadU8:" + reason, e); return null; } }

function getAmmoSnapshot(wpnThrowPtr) {
    const ammoData = safeReadPointer(wpnThrowPtr, Offsets.WPN_Throw_ammoData, "WPN_Throw.ammoData");
    if (ammoData.isNull()) return { ok: false, ammoData: "0x0" };
    const key = safeReadU32(ammoData, Offsets.Ammo_key, "ammo.key");
    const hidden = safeReadU32(ammoData, Offsets.Ammo_hidden, "ammo.hidden");
    const plain = safeReadU32(ammoData, Offsets.Ammo_plain_or_fake, "ammo.plain_or_fake");
    const ready = safeReadU8(wpnThrowPtr, Offsets.WPN_Throw_throwReady, "throwReady");
    let value = null;
    if (key !== null && hidden !== null) value = (key ^ hidden) >>> 0;
    return { ok: key !== null && hidden !== null, throwPtr: ptrStr(wpnThrowPtr), ammoDataPtr: ammoData, ammoData: ptrStr(ammoData), key: key, hidden: hidden, plain_or_fake: plain, value: value, throwReady: ready };
}
function publicSnap(s) { if (!s) return null; return { ok: s.ok, throwPtr: s.throwPtr, ammoData: s.ammoData, key: s.key, hidden: s.hidden, plain_or_fake: s.plain_or_fake, value: s.value, throwReady: s.throwReady }; }
function targetCount() { let n = parseInt(Runtime.config.target_count, 10); if (isNaN(n) || n < 1) n = 999; if (n > 9999) n = 9999; return n >>> 0; }

function shouldForceThrowReady(name, phase) {
    if (!Runtime.config.force_throw_ready_enabled) return false;
    if (name === "WPN_Throw.Throw" && phase === "onLeave") return Runtime.config.force_throw_ready_on_throw_leave;
    if ((name === "WPN_Throw.Deploy" || name === "WPN_Throw.UnDeploy") && Runtime.config.force_throw_ready_on_deploy) return true;
    if ((name === "WPN_Throw.OnAnimationEnd" || name === "WPN_Throw.OnFireAnimEnd") && Runtime.config.force_throw_ready_on_animation_end) return true;
    return false;
}

function forceThrowReadyBucket(scopeInfo) {
    if (scopeInfo && scopeInfo.isMyWeapon === true) return "local_player";
    if (scopeInfo && scopeInfo.isMyWeapon === false) return "bot_or_remote";
    return "unknown";
}

function getForceThrowReadyWindow(scopeInfo) {
    const bucket = forceThrowReadyBucket(scopeInfo);
    let item = Runtime.forceThrowReadyWindows[bucket];
    if (!item) {
        item = { start: 0, count: 0 };
        Runtime.forceThrowReadyWindows[bucket] = item;
    }
    return item;
}

function canForceThrowReadyNow(scopeInfo) {
    const now = Date.now();
    const windowMs = Math.max(100, parseInt(Runtime.config.force_throw_ready_window_ms, 10) || 1000);
    const maxPerWindow = Math.max(1, parseInt(Runtime.config.force_throw_ready_max_per_second, 10) || 10);
    const item = getForceThrowReadyWindow(scopeInfo);
    if (!item.start || now - item.start >= windowMs) {
        item.start = now;
        item.count = 0;
    }
    if (item.count >= maxPerWindow) {
        Runtime.stats.throw_ready_skipped += 1;
        return false;
    }
    item.count += 1;
    return true;
}

function forceThrowReadyRetryDelayMs(scopeInfo) {
    const now = Date.now();
    const windowMs = Math.max(100, parseInt(Runtime.config.force_throw_ready_window_ms, 10) || 1000);
    const item = getForceThrowReadyWindow(scopeInfo);
    if (!item.start) return 0;
    const elapsed = now - item.start;
    if (elapsed >= windowMs) return 0;
    return Math.max(1, windowMs - elapsed + 5);
}

function scheduleForceThrowReadyRetry(wpnThrowPtr, reason, scopeInfo) {
    try {
        if (!Runtime.enabled || !Runtime.config.force_throw_ready_enabled) return false;
        if (!isReadablePtr(wpnThrowPtr)) return false;
        const key = ptrStr(wpnThrowPtr);
        if (Runtime.pendingThrowReadyTimers[key]) return false;
        const generation = Runtime.generation;
        Runtime.pendingThrowReadyTimers[key] = setTimeout(function() {
            delete Runtime.pendingThrowReadyTimers[key];
            try {
                if (!Runtime.enabled || Runtime.generation !== generation || !Runtime.config.force_throw_ready_enabled) return;
                if (!isReadablePtr(wpnThrowPtr)) { Runtime.stats.throw_ready_skipped += 1; return; }
                forceThrowReady(wpnThrowPtr, reason + ".retry");
            } catch (e) { recordError("forceThrowReady.retry:" + reason, e); }
        }, forceThrowReadyRetryDelayMs(scopeInfo));
        return true;
    } catch (e) { recordError("scheduleForceThrowReadyRetry:" + reason, e); return false; }
}

function clearPendingThrowReadyTimers() {
    for (const key of Object.keys(Runtime.pendingThrowReadyTimers)) {
        try { clearTimeout(Runtime.pendingThrowReadyTimers[key]); } catch (e) {}
        delete Runtime.pendingThrowReadyTimers[key];
    }
}

function forceThrowReady(wpnThrowPtr, reason) {
    try {
        if (!Runtime.enabled || !Runtime.config.force_throw_ready_enabled) return false;
        const scopeInfo = throwReadyAllowedByScope(wpnThrowPtr, reason + '.throwReady');
        if (!scopeInfo.allowedByInfiniteScope) return false;
        if (!isReadablePtr(wpnThrowPtr)) { Runtime.stats.throw_ready_skipped += 1; return false; }
        const value = Runtime.config.force_throw_ready_value ? 1 : 0;
        const before = wpnThrowPtr.add(Offsets.WPN_Throw_throwReady).readU8();
        if (before === value) { Runtime.stats.throw_ready_skipped += 1; return true; }
        if (!canForceThrowReadyNow(scopeInfo)) { scheduleForceThrowReadyRetry(wpnThrowPtr, reason, scopeInfo); return false; }
        wpnThrowPtr.add(Offsets.WPN_Throw_throwReady).writeU8(value);
        Runtime.stats.throw_ready_writes += 1;
        log("连投就绪开关已写入 throwReady", { reason: reason, throwPtr: ptrStr(wpnThrowPtr), before: before, after: value, writes: Runtime.stats.throw_ready_writes, note: "该开关可能导致连续投掷，默认关闭" });
        return true;
    } catch (e) { recordError("forceThrowReady:" + reason, e); return false; }
}

function getThreadKey() {
    try { return String(Process.getCurrentThreadId()); } catch (e) { return "main"; }
}
function pushThrowAnimContext(throwPtr, reason) {
    if (!Runtime.config.throw_anim_speed_enabled) return false;
    const k = getThreadKey();
    Runtime.throwAnimContexts[k] = { throwPtr: ptrStr(throwPtr), start: Date.now(), reason: reason };
    Runtime.stats.throw_anim_context_push += 1;
    return true;
}
function popThrowAnimContext(reason) {
    const k = getThreadKey();
    if (Runtime.throwAnimContexts[k]) {
        delete Runtime.throwAnimContexts[k];
        Runtime.stats.throw_anim_context_pop += 1;
        return true;
    }
    return false;
}
function hasThrowAnimContext() {
    if (!Runtime.config.throw_anim_speed_enabled) return false;
    const ctx = Runtime.throwAnimContexts[getThreadKey()];
    if (!ctx) return false;
    if (Date.now() - ctx.start > 3000) { delete Runtime.throwAnimContexts[getThreadKey()]; return false; }
    return true;
}
function setAnimatorSpeed(animator, speed, reason) {
    try {
        if (!Runtime.enabled || !Runtime.config.throw_anim_speed_enabled) return false;
        if (!isReadablePtr(animator)) return false;
        setupNatives();
        const v = Number(speed);
        if (!isFinite(v) || v <= 0) return false;
        Runtime.natives.Animator_set_speed(animator, v, ptr(0));
        const k = ptrStr(animator);
        Runtime.touchedAnimators[k] = { ptr: k, last: Date.now(), reason: reason };
        Runtime.stats.anim_speed_writes += 1;
        logOnce("anim_speed:" + k, "投掷动作加速已设置 Animator.speed", Runtime.config.log_interval_ms, { animator: k, speed: v, reason: reason, writes: Runtime.stats.anim_speed_writes });
        return true;
    } catch (e) { recordError("setAnimatorSpeed:" + reason, e); return false; }
}
function setCFAnimatorSpeed(cfAnimator, reason) {
    try {
        if (!hasThrowAnimContext()) return false;
        if (!isReadablePtr(cfAnimator)) return false;
        const animator = readPointer(cfAnimator, Offsets.CFAnimator_animator);
        return setAnimatorSpeed(animator, Runtime.config.throw_anim_speed_value, reason);
    } catch (e) { recordError("setCFAnimatorSpeed:" + reason, e); return false; }
}
function restoreTouchedAnimatorSpeeds(reason) {
    try {
        if (!Runtime.config.throw_anim_speed_restore_on_end) return;
        setupNatives();
        const restoreValue = Number(Runtime.config.throw_anim_speed_restore_value || 1.0);
        for (const k of Object.keys(Runtime.touchedAnimators)) {
            const p = ptr(k);
            if (isReadablePtr(p)) {
                Runtime.natives.Animator_set_speed(p, restoreValue, ptr(0));
                Runtime.stats.anim_speed_restores += 1;
            }
            delete Runtime.touchedAnimators[k];
        }
        logOnce("anim_restore", "投掷动作加速已恢复 Animator.speed", Runtime.config.log_interval_ms, { reason: reason, restore_value: restoreValue, restores: Runtime.stats.anim_speed_restores });
    } catch (e) { recordError("restoreTouchedAnimatorSpeeds:" + reason, e); }
}

function cleanupProtectedWeapons(reason) {
    const now = Date.now();
    const ttl = Runtime.config.protect_ttl_ms || 5000;
    let expired = 0;
    for (const k of Object.keys(Runtime.protectedWeapons)) {
        const item = Runtime.protectedWeapons[k];
        if (!item || now - item.lastSeen > ttl) { delete Runtime.protectedWeapons[k]; expired += 1; }
    }
    const keys = Object.keys(Runtime.protectedWeapons);
    const max = Runtime.config.max_protected_weapons || 64;
    if (keys.length > max) {
        keys.sort(function(a,b){ return (Runtime.protectedWeapons[a].lastSeen||0) - (Runtime.protectedWeapons[b].lastSeen||0); });
        for (let i = 0; i < keys.length - max; i++) { delete Runtime.protectedWeapons[keys[i]]; expired += 1; }
    }
    if (expired > 0) { Runtime.stats.protected_expired += expired; logOnce("protected_expired", "已清理过期手雷保护对象", Runtime.config.log_interval_ms, { reason: reason, expired: expired }); }
}
function rememberProtectedThrow(wpnThrowPtr, snap, reason) {
    if (!wpnThrowPtr || wpnThrowPtr.isNull()) return;
    cleanupProtectedWeapons("remember");
    const k = ptrStr(wpnThrowPtr);
    Runtime.protectedWeapons[k] = { ptr: k, ammoData: snap && snap.ammoData ? snap.ammoData : "unknown", lastSeen: Date.now(), reason: reason };
    Runtime.stats.protected_count = Object.keys(Runtime.protectedWeapons).length;
    logOnce("remember:" + k, "已记录当前手雷武器保护对象", Runtime.config.log_interval_ms, { weapon: k, reason: reason, protected_count: Runtime.stats.protected_count });
}
function isProtectedThrowWeapon(weaponPtr) { if (!weaponPtr || weaponPtr.isNull()) return false; cleanupProtectedWeapons("check"); return Runtime.protectedWeapons[ptrStr(weaponPtr)] !== undefined; }

function getThrowWeaponLocalInfo(wpnThrowPtr, scopeOverride) {
    const info = { weapon: ptrStr(wpnThrowPtr), isReadable: false, isMyWeapon: null, allowedByInfiniteScope: false, scope: scopeOverride || Runtime.config.infinite_grenade_scope || "local_only" };
    try {
        if (!wpnThrowPtr || wpnThrowPtr.isNull() || !isReadablePtr(wpnThrowPtr)) return info;
        info.isReadable = true;
        setupNatives();
        info.isMyWeapon = Runtime.natives.Weapon_get_isMyWeapon(wpnThrowPtr, ptr(0)) ? true : false;
        if (info.scope === "all_players") {
            info.allowedByInfiniteScope = true;
            Runtime.stats.infinite_scope_all_apply += 1;
            return info;
        }
        if (info.isMyWeapon) { info.allowedByInfiniteScope = true; Runtime.stats.infinite_scope_local_apply += 1; }
        else { Runtime.stats.infinite_scope_local_skip += 1; }
        return info;
    } catch (e) {
        Runtime.stats.infinite_scope_local_skip += 1;
        return info;
    }
}

function throwWeaponAllowedByScope(wpnThrowPtr, reason) {
    const info = getThrowWeaponLocalInfo(wpnThrowPtr);
    if (!info.allowedByInfiniteScope) {
        logOnce("scope_skip:" + ptrStr(wpnThrowPtr), "跳过非作用范围内的手雷武器", Runtime.config.log_interval_ms, {
            reason: reason, scope: info.scope, weapon: info.weapon, isMyWeapon: info.isMyWeapon,
            note: "local_only=只给玩家自己；all_players=玩家和bot都给"
        });
    }
    return info;
}

function throwReadyAllowedByScope(wpnThrowPtr, reason) {
    const info = getThrowWeaponLocalInfo(wpnThrowPtr, Runtime.config.force_throw_ready_scope || "local_only");
    if (!info.allowedByInfiniteScope) {
        logOnce("throw_ready_scope_skip:" + ptrStr(wpnThrowPtr), "跳过非连投作用范围内的手雷武器", Runtime.config.log_interval_ms, {
            reason: reason, scope: info.scope, weapon: info.weapon, isMyWeapon: info.isMyWeapon,
            note: "local_only=只给玩家自己；all_players=玩家和人机都给"
        });
    }
    return info;
}

function lockAmmo(wpnThrowPtr, reason) {
    if (!Runtime.enabled || !Runtime.config.lock999_enabled) return false;
    const scopeInfo = throwWeaponAllowedByScope(wpnThrowPtr, reason);
    if (!scopeInfo.allowedByInfiniteScope) return false;
    Runtime.stats.lock_attempts += 1;
    const before = getAmmoSnapshot(wpnThrowPtr);
    if (!before || !before.ok) { Runtime.stats.skipped_invalid += 1; return false; }
    rememberProtectedThrow(wpnThrowPtr, before, reason);
    const target = targetCount();
    if (before.value === target) { Runtime.stats.lock_skipped_same += 1; return true; }
    const newHidden = (before.key ^ target) >>> 0;
    const okHidden = safeWriteU32(before.ammoDataPtr, Offsets.Ammo_hidden, newHidden, "lock999.hidden");
    let okPlain = false;
    if (Runtime.config.sync_plain_value) {
        okPlain = safeWriteU32(before.ammoDataPtr, Offsets.Ammo_plain_or_fake, target, "lock999.plain_or_fake");
        if (okPlain) Runtime.stats.sync_plain_writes += 1;
    }
    const after = getAmmoSnapshot(wpnThrowPtr);
    if (okHidden) {
        Runtime.stats.lock_writes += 1;
        rememberProtectedThrow(wpnThrowPtr, after, reason + ".after");
        log("手雷数量已锁定并保护武器对象", { reason: reason, before: publicSnap(before), after: publicSnap(after), target_count: target, sync_plain_value: Runtime.config.sync_plain_value, sync_plain_ok: okPlain, lock_writes: Runtime.stats.lock_writes });
        return true;
    }
    return false;
}

function setupNatives() {
    if (!Runtime.natives.Player_get_isMyPlayer) {
        Runtime.natives.Player_get_isMyPlayer = new NativeFunction(addrOf(RVA.Player_get_isMyPlayer), "bool", ["pointer", "pointer"], CALL_CONV);
    }
    if (!Runtime.natives.Weapon_get_isMyWeapon) {
        Runtime.natives.Weapon_get_isMyWeapon = new NativeFunction(addrOf(RVA.Weapon_get_isMyWeapon), "bool", ["pointer", "pointer"], CALL_CONV);
    }
    if (!Runtime.natives.Animator_set_speed) {
        Runtime.natives.Animator_set_speed = new NativeFunction(addrOf(RVA.UnityEngine_Animator_set_speed), "void", ["pointer", "float", "pointer"], CALL_CONV);
    }
    if (!Runtime.natives.PlayerWeapons_SetCurrentWeapon_Original) {
        Runtime.natives.PlayerWeapons_SetCurrentWeapon_Original = new NativeFunction(addrOf(RVA.PlayerWeapons_SetCurrentWeapon), "void", ["pointer", "int", "pointer", "pointer"], CALL_CONV);
    }
    if (!Runtime.natives.Player_get_wpns) {
        Runtime.natives.Player_get_wpns = new NativeFunction(addrOf(RVA.Player_get_wpns), "pointer", ["pointer", "pointer"], CALL_CONV);
    }
    if (!Runtime.natives.PlayerWeapons_Select_Original) {
        Runtime.natives.PlayerWeapons_Select_Original = new NativeFunction(addrOf(RVA.PlayerWeapons_Select), "bool", ["pointer", "int", "pointer"], CALL_CONV);
    }
    if (!Runtime.natives.GameManager_GetWeapon_Original) {
        Runtime.natives.GameManager_GetWeapon_Original = new NativeFunction(addrOf(RVA.GameManager_GetWeapon), "pointer", ["int", "pointer"], CALL_CONV);
    }
    if (!Runtime.natives.WPN_Throw_Throw_Original) {
        Runtime.natives.WPN_Throw_Throw_Original = new NativeFunction(addrOf(RVA.WPN_Throw_Throw), "void", ["pointer", "pointer"], CALL_CONV);
    }
    if (!Runtime.natives.UnityEngine_Component_get_transform) {
        Runtime.natives.UnityEngine_Component_get_transform = new NativeFunction(addrOf(RVA.UnityEngine_Component_get_transform), "pointer", ["pointer", "pointer"], CALL_CONV);
    }
    if (!Runtime.natives.UnityEngine_Transform_get_position_Injected) {
        Runtime.natives.UnityEngine_Transform_get_position_Injected = new NativeFunction(addrOf(RVA.UnityEngine_Transform_get_position_Injected), "void", ["pointer", "pointer", "pointer"], CALL_CONV);
    }
}
function isOwnerLocalPlayer(missile) {
    try {
        const owner = readPointer(missile, Offsets.Missile_owner);
        if (!owner || owner.isNull()) { Runtime.stats.owner_unknown += 1; return false; }
        setupNatives();
        const ok = Runtime.natives.Player_get_isMyPlayer(owner, ptr(0)) ? true : false;
        if (ok) Runtime.stats.owner_local_pass += 1; else Runtime.stats.owner_local_fail += 1;
        return ok;
    } catch (e) { Runtime.stats.owner_local_fail += 1; return false; }
}
function ownerAllowed(missile) { const mode = Runtime.config.owner_filter || "local_only"; if (mode === "all_throw") return true; return isOwnerLocalPlayer(missile); }

function fieldScopeAllowed(missile, scope) {
    const mode = scope || "my_player";
    // my_player / local_player：只作用于本机玩家自己的手雷
    // all_players：作用于所有人，包括myPlayer和所有bot
    if (mode === "all" || mode === "all_throw" || mode === "all_players") return true;
    const isLocal = isOwnerLocalPlayer(missile);
    if (mode === "all_bots" || mode === "bots_only" || mode === "bot_only") return !isLocal; // 旧配置兼容，UI不再使用
    return isLocal;
}

function fieldScopeName(scope) {
    const mode = scope || "my_player";
    if (mode === "all" || mode === "all_throw" || mode === "all_players") return "所有人";
    if (mode === "all_bots" || mode === "bots_only" || mode === "bot_only") return "所有Bot";
    return "myPlayer";
}
function cleanupTrackedMissiles(reason) {
    const now = Date.now();
    const ttl = Runtime.config.missile_ttl_ms || 8000;
    let expired = 0;
    for (const k of Object.keys(Runtime.trackedMissiles)) {
        const item = Runtime.trackedMissiles[k];
        if (!item || now - item.lastSeen > ttl) { delete Runtime.trackedMissiles[k]; expired += 1; }
    }
    const keys = Object.keys(Runtime.trackedMissiles);
    const max = Runtime.config.max_tracked_missiles || 128;
    if (keys.length > max) {
        keys.sort(function(a,b){ return (Runtime.trackedMissiles[a].lastSeen||0) - (Runtime.trackedMissiles[b].lastSeen||0); });
        for (let i = 0; i < keys.length - max; i++) { delete Runtime.trackedMissiles[keys[i]]; expired += 1; }
    }
    if (expired > 0) Runtime.stats.tracked_expired += expired;
    Runtime.stats.tracked_count = Object.keys(Runtime.trackedMissiles).length;
}
function markGrenadeMissile(missile, throwPtr, reason) {
    if (!missile || missile.isNull() || !isReadablePtr(missile)) { Runtime.stats.skipped_invalid += 1; return false; }
    cleanupTrackedMissiles("mark");
    const k = ptrStr(missile);
    const owner = readPointer(missile, Offsets.Missile_owner);
    const item = Runtime.trackedMissiles[k] || {};
    item.ptr = k; item.throwPtr = ptrStr(throwPtr); item.owner = ptrStr(owner); item.firstSeen = item.firstSeen || Date.now(); item.lastSeen = Date.now(); item.reason = reason; item.ownerAllowed = ownerAllowed(missile);
    Runtime.trackedMissiles[k] = item;
    Runtime.stats.tracked_count = Object.keys(Runtime.trackedMissiles).length;
    log("已捕获 WPN_Throw 生成的 missile", { missile: k, throwPtr: ptrStr(throwPtr), owner: item.owner, owner_filter: Runtime.config.owner_filter, owner_allowed: item.ownerAllowed, tracked_count: Runtime.stats.tracked_count, note: "普通手雷 missile 已进表；RPG/AT4/Nano 不进表" });
    return true;
}
function isTrackedMissile(missile) { if (!missile || missile.isNull()) return false; cleanupTrackedMissiles("check"); const item = Runtime.trackedMissiles[ptrStr(missile)]; if (!item) return false; item.lastSeen = Date.now(); return true; }
function getTrackedMissileItem(missile) { if (!missile || missile.isNull()) return null; const item = Runtime.trackedMissiles[ptrStr(missile)]; if (item) item.lastSeen = Date.now(); return item || null; }

function writeFloatIfNeeded(base, offset, value, label, scaleValue) {
    try {
        if (!isReadablePtr(base)) { Runtime.stats.skipped_invalid += 1; return false; }
        const v = Number(value); if (!isFinite(v)) return false;
        const actual = scaleValue ? (v * 10) : v;
        const old = base.add(offset).readFloat();
        if (Math.abs(old - actual) < 0.0001) return false;
        base.add(offset).writeFloat(actual);
        Runtime.stats.grenade_field_writes += 1;
        return true;
    } catch (e) { recordError("writeFloat:" + label, e); return false; }
}

function writeShootSpeedIfNeeded(missile, reason) {
    if (!Runtime.config.enable_shoot_speed) return false;
    try {
        if (!isReadablePtr(missile)) return false;
        const v = Number(Runtime.config.shoot_speed_value); if (!isFinite(v)) return false;
        const actual = v * 10;
        const old = missile.add(Offsets.Missile_shootSpeed).readFloat();
        if (Math.abs(old - actual) < 0.0001) return false;
        missile.add(Offsets.Missile_shootSpeed).writeFloat(actual);
        Runtime.stats.missile_speed_writes += 1;
        logOnce("shootSpeed:" + ptrStr(missile), "已修改手雷 missile 飞行速度", Runtime.config.log_interval_ms, { missile: ptrStr(missile), reason: reason, before: old, ui: v, after: actual });
        return true;
    } catch (e) { recordError("writeShootSpeed:" + reason, e); return false; }
}
function tuneGrenadeRuntimeFields(grenade, reason, allowLog) {
    Runtime.stats.tune_attempts += 1;
    if (!Runtime.enabled || !Runtime.config.runtime_tuner_enabled) return false;
    if (!isTrackedMissile(grenade)) { Runtime.stats.tune_skipped_not_tracked += 1; return false; }
    const item = getTrackedMissileItem(grenade);
    let owner = "0x0";
    try { owner = ptrStr(readPointer(grenade, Offsets.Missile_owner)); } catch (e) {}
    if (item) { item.owner = owner; }

    const allowDamage = Runtime.config.enable_damage && fieldScopeAllowed(grenade, Runtime.config.damage_apply_scope);
    const allowRange = Runtime.config.enable_range && fieldScopeAllowed(grenade, Runtime.config.range_apply_scope);
    const allowSpeed = Runtime.config.enable_shoot_speed && fieldScopeAllowed(grenade, Runtime.config.shoot_speed_apply_scope);
    if (item) {
        item.damageAllowed = allowDamage;
        item.rangeAllowed = allowRange;
        item.speedAllowed = allowSpeed;
    }
    if (!allowDamage && !allowRange && !allowSpeed) { Runtime.stats.tune_skipped_owner += 1; return false; }

    let writes = 0;
    if (allowDamage && writeFloatIfNeeded(grenade, Offsets.Grenade_expDamage, Runtime.config.damage_value, "expDamage", true)) writes++;
    if (allowRange && writeFloatIfNeeded(grenade, Offsets.Grenade_expRange, Runtime.config.range_value, "expRange", true)) writes++;
    if (allowSpeed && writeShootSpeedIfNeeded(grenade, reason)) writes++;
    if (writes > 0) {
        Runtime.stats.tune_applied += 1;
        if (allowLog !== false) log("已修改手雷 missile 运行时字段", {
            missile: ptrStr(grenade), reason: reason, owner: owner, writes: writes,
            damage: Runtime.config.damage_value, range: Runtime.config.range_value, speed: Runtime.config.shoot_speed_value,
            damage_scope: Runtime.config.damage_apply_scope, range_scope: Runtime.config.range_apply_scope, speed_scope: Runtime.config.shoot_speed_apply_scope
        });
        return true;
    }
    return false;
}
function tuneMissileOnlyFields(missile, reason) {
    Runtime.stats.tune_attempts += 1;
    if (!Runtime.enabled || !Runtime.config.runtime_tuner_enabled) return false;
    if (!isTrackedMissile(missile)) { Runtime.stats.tune_skipped_not_tracked += 1; return false; }
    const allowSpeed = Runtime.config.enable_shoot_speed && fieldScopeAllowed(missile, Runtime.config.shoot_speed_apply_scope);
    if (!allowSpeed) { Runtime.stats.tune_skipped_owner += 1; return false; }
    let changed = writeShootSpeedIfNeeded(missile, reason);
    if (changed) Runtime.stats.tune_applied += 1;
    return changed;
}

function getThreadKey() {
    try { return Process.getCurrentThreadId().toString(); } catch (e) { return "0"; }
}
function pushExplosionContext(missile, reason) {
    if (!Runtime.enabled || !Runtime.config.runtime_tuner_enabled) return false;
    if (!isTrackedMissile(missile)) return false;
    const allowDamage = Runtime.config.enable_damage && fieldScopeAllowed(missile, Runtime.config.damage_apply_scope);
    const allowRange = Runtime.config.enable_range && fieldScopeAllowed(missile, Runtime.config.range_apply_scope);
    if (!allowDamage && !allowRange) { Runtime.stats.tune_skipped_owner += 1; return false; }
    const key = getThreadKey();
    const list = Runtime.explosionContexts[key] || [];
    list.push({ missile: ptrStr(missile), ts: Date.now(), reason: reason, allowDamage: allowDamage, allowRange: allowRange,
        damage_scope: Runtime.config.damage_apply_scope, range_scope: Runtime.config.range_apply_scope });
    Runtime.explosionContexts[key] = list;
    return true;
}
function popExplosionContext() {
    const key = getThreadKey();
    const list = Runtime.explosionContexts[key];
    if (!list || list.length === 0) return;
    list.pop();
    if (list.length === 0) delete Runtime.explosionContexts[key];
}
function peekExplosionContext() {
    const key = getThreadKey();
    const list = Runtime.explosionContexts[key];
    if (!list || list.length === 0) return null;
    const item = list[list.length - 1];
    if (!item || Date.now() - item.ts > 1500) {
        delete Runtime.explosionContexts[key];
        return null;
    }
    return item;
}
function writeCreateExplosionArgs(ctx, reason) {
    try {
        const item = peekExplosionContext();
        if (!item) return false;
        if (!ctx || !ctx.esp) return false;
        let writes = 0;
        let damageBefore = null;
        let rangeBefore = null;
        let damageAfter = null;
        let rangeAfter = null;

        // x86 cdecl，CreateExplosion 是静态方法：
        // esp+04 worldPos.x, esp+08 worldPos.y, esp+0C worldPos.z,
        // esp+10 damage, esp+14 range, esp+18 distanceDecay, esp+1C ignoreWall。
        if (Runtime.config.enable_damage && item.allowDamage !== false) {
            const pDamage = ctx.esp.add(0x10);
            damageBefore = pDamage.readFloat();
            const v = Number(Runtime.config.damage_value);
            const actual = v * 10;
            if (isFinite(v) && Math.abs(damageBefore - actual) > 0.0001) {
                pDamage.writeFloat(actual);
                damageAfter = actual;
                writes++;
            } else {
                damageAfter = damageBefore;
            }
        }
        if (Runtime.config.enable_range && item.allowRange !== false) {
            const pRange = ctx.esp.add(0x14);
            rangeBefore = pRange.readFloat();
            const v = Number(Runtime.config.range_value);
            const actual = v * 10;
            if (isFinite(v) && Math.abs(rangeBefore - actual) > 0.0001) {
                pRange.writeFloat(actual);
                rangeAfter = actual;
                writes++;
            } else {
                rangeAfter = rangeBefore;
            }
        }
        if (writes > 0) {
            Runtime.stats.createExplosion_param_writes += writes;
            Runtime.stats.tune_applied += 1;
            log("已修改 CreateExplosion 参数", {
                missile: item.missile,
                reason: reason,
                ctx_reason: item.reason,
                writes: writes,
                damage_before: damageBefore,
                damage_ui: Runtime.config.damage_value,
                damage_after: damageAfter,
                range_before: rangeBefore,
                range_ui: Runtime.config.range_value,
                range_after: rangeAfter,
                damage_scope: item.damage_scope,
                range_scope: item.range_scope,
                note: "只在 tracked 手雷爆炸上下文里按字段作用对象修改；RPG/AT4/Nano 不进上下文"
            });
            return true;
        }
    } catch (e) {
        recordError("writeCreateExplosionArgs:" + reason, e);
    }
    return false;
}

function hookThrowLike(name, rva, statName, enterConfigName, leaveConfigName) {
    addHook(name, rva, {
        onEnter(args) {
            Runtime.stats.hook_hits += 1;
            Runtime.stats[statName] += 1;
            Runtime.stats.last_hook = name;
            this.self = args[0];
            try {
                if (Runtime.enabled && Runtime.config.bot_grenade_behavior_observer_enabled && name === "WPN_Throw.Throw") {
                    const scopeInfoForBot = getThrowWeaponLocalInfo(this.self);
                    if (scopeInfoForBot.isMyWeapon === false) {
                        Runtime.stats.bot_throw_method_hits += 1;
                        logOnce("bot_throw_method:" + ptrStr(this.self), "Bot进入WPN_Throw.Throw", Runtime.config.log_interval_ms, {
                            weapon: ptrStr(this.self), scope: Runtime.config.infinite_grenade_scope,
                            note: "这说明bot不只是拿到手雷，而是真的执行了投掷入口"
                        });
                    }
                }
            } catch (e) {}
            this.pushedThrowAnimCtx = false;
            if (name === "WPN_Throw.Throw" && Runtime.enabled && Runtime.config.throw_anim_speed_enabled) {
                this.pushedThrowAnimCtx = pushThrowAnimContext(this.self, "WPN_Throw.Throw.onEnter");
            }
            if (Runtime.enabled && Runtime.config[enterConfigName]) {
                try { lockAmmo(this.self, name + ".onEnter"); } catch (e) { recordError(name + ".onEnter", e); }
            }
            if (Runtime.enabled && shouldForceThrowReady(name, "onEnter")) {
                try { forceThrowReady(this.self, name + ".onEnter"); } catch (e) { recordError(name + ".forceReadyEnter", e); }
            }
        },
        onLeave(retval) {
            if (Runtime.enabled && Runtime.config[leaveConfigName]) {
                try { lockAmmo(this.self, name + ".onLeave"); } catch (e) { recordError(name + ".onLeave", e); }
            }
            if (Runtime.enabled && shouldForceThrowReady(name, "onLeave")) {
                try { forceThrowReady(this.self, name + ".onLeave"); } catch (e) { recordError(name + ".forceReadyLeave", e); }
            }
            if (name === "WPN_Throw.OnAnimationEnd" || name === "WPN_Throw.OnFireAnimEnd") {
                if (Runtime.config.throw_anim_speed_enabled) restoreTouchedAnimatorSpeeds(name + ".onLeave");
            }
            if (this.pushedThrowAnimCtx) popThrowAnimContext(name + ".onLeave");
        }
    });
}


function safeReadI32(base, offset, reason) {
    try {
        if (!isReadablePtr(base)) return null;
        return base.add(offset).readS32();
    } catch (e) {
        Runtime.stats.skipped_invalid += 1;
        return null;
    }
}

function weaponClassName(cls) {
    const names = {
        0: "Rifle",
        1: "Sniper",
        2: "MachineGun",
        3: "SubmachineGun",
        4: "ShotGun",
        5: "Pistol",
        6: "Knife",
        7: "Grenade",
        8: "FlashBang",
        9: "SmokeGrenade"
    };
    if (cls === null || cls === undefined) return "Unknown";
    return names[cls] || ("Unknown(" + cls + ")");
}

function isThrowWeaponClass(cls) {
    return cls === 7 || cls === 8 || cls === 9;
}

function readWeaponInfo(weapon) {
    const info = {
        weapon: ptrStr(weapon),
        data: "0x0",
        wpnClass: null,
        className: "null",
        isThrowClass: false,
        isMyWeapon: null
    };

    try {
        if (!weapon || weapon.isNull() || !isReadablePtr(weapon)) return info;
        const data = readPointer(weapon, Offsets.Weapon_data);
        info.data = ptrStr(data);
        if (data && !data.isNull() && isReadablePtr(data)) {
            const cls = safeReadI32(data, Offsets.WeaponData_wpnClass, "WeaponData.wpnClass");
            info.wpnClass = cls;
            info.className = weaponClassName(cls);
            info.isThrowClass = isThrowWeaponClass(cls);
        }
        try {
            setupNatives();
            info.isMyWeapon = Runtime.natives.Weapon_get_isMyWeapon(weapon, ptr(0)) ? true : false;
        } catch (e) {
            info.isMyWeapon = null;
        }
        return info;
    } catch (e) {
        recordError("readWeaponInfo", e);
        return info;
    }
}

function readPlayerWeaponsInfo(thisPtr) {
    const info = {
        thisPtr: ptrStr(thisPtr),
        owner: "0x0",
        ownerIsLocal: null
    };
    try {
        if (!thisPtr || thisPtr.isNull() || !isReadablePtr(thisPtr)) return info;
        const owner = readPointer(thisPtr, Offsets.PlayerWeapons_owner);
        info.owner = ptrStr(owner);
        if (owner && !owner.isNull() && isReadablePtr(owner)) {
            try {
                setupNatives();
                info.ownerIsLocal = Runtime.natives.Player_get_isMyPlayer(owner, ptr(0)) ? true : false;
                if (info.ownerIsLocal) Runtime.stats.observer_local_owner_hits += 1;
                else Runtime.stats.observer_nonlocal_owner_hits += 1;
            } catch (e) {
                info.ownerIsLocal = null;
            }
        }
    } catch (e) {
        recordError("readPlayerWeaponsInfo", e);
    }
    return info;
}


function botSoftLockAllowedClass(cls) {
    // v2.5：按用户要求，只允许普通 Grenade。FlashBang / SmokeGrenade 不再纳入。
    return cls === 7;
}

function makeBotGrenadeRecord(playerWeaponsPtr, pwInfo, weaponInfo, reason, botPtr) {
    return {
        playerWeapons: ptrStr(playerWeaponsPtr),
        owner: pwInfo ? (pwInfo.owner || "0x0") : "0x0",
        bot: ptrStr(botPtr || ptr(0)),
        grenadeWeapon: weaponInfo.weapon,
        className: weaponInfo.className,
        wpnClass: weaponInfo.wpnClass,
        lastSeen: Date.now(),
        reason: reason
    };
}

function isValidBotGrenadeRecord(rec, reason) {
    try {
        if (!rec || !rec.grenadeWeapon || rec.grenadeWeapon === "0x0") return false;
        const p = ptr(rec.grenadeWeapon);
        if (!p || p.isNull() || !isReadablePtr(p)) return false;
        const wi = readWeaponInfo(p);
        if (!botSoftLockAllowedClass(wi.wpnClass)) return false;
        return true;
    } catch (e) {
        recordError("isValidBotGrenadeRecord:" + reason, e);
        return false;
    }
}

function botGrenadeAliasKeys(playerWeaponsPtr, pwInfo, botPtr, reason) {
    const keys = [];
    function add(prefix, val) {
        try {
            if (!val) return;
            const s = (typeof val === "string") ? val : ptrStr(val);
            if (!s || s === "0x0" || s === "null" || s === "undefined") return;
            const k = prefix + ":" + s;
            if (keys.indexOf(k) < 0) keys.push(k);
        } catch (e) {}
    }

    add("pw", playerWeaponsPtr);
    if (pwInfo) add("owner", pwInfo.owner);
    add("bot", botPtr);

    try {
        if (botPtr && !botPtr.isNull() && isReadablePtr(botPtr)) {
            const player = readPointer(botPtr, Offsets.Bot_thisPlayer);
            add("playerFromBot", player);
        }
    } catch (e) {}

    return keys;
}

function storeBotGrenadeRecordAliases(playerWeaponsPtr, pwInfo, weaponInfo, reason, botPtr) {
    try {
        const rec = makeBotGrenadeRecord(playerWeaponsPtr, pwInfo, weaponInfo, reason, botPtr);
        const keys = botGrenadeAliasKeys(playerWeaponsPtr, pwInfo, botPtr, reason);
        const baseKey = ptrStr(playerWeaponsPtr);

        if (keys.indexOf("pw:" + baseKey) < 0) keys.unshift("pw:" + baseKey);
        for (const k of keys) Runtime.botGrenadeWeapons[k] = rec;
        Runtime.botGrenadeWeapons[baseKey] = rec; // 兼容旧代码，保留裸 playerWeapons key

        if (rec.grenadeWeapon && rec.grenadeWeapon !== "0x0") {
            Runtime.botGrenadeWeaponIndex[rec.grenadeWeapon] = {
                keys: keys,
                playerWeapons: baseKey,
                owner: rec.owner,
                bot: rec.bot,
                lastSeen: rec.lastSeen,
                reason: reason
            };
        }

        Runtime.stats.bot_grenade_multikey_records += 1;
        return { rec: rec, keys: keys };
    } catch (e) {
        recordError("storeBotGrenadeRecordAliases:" + reason, e);
        return null;
    }
}

function recordBotGrenadeWeapon(playerWeaponsPtr, pwInfo, weaponInfo, reason, botPtr) {
    try {
        if (!Runtime.enabled) return false;
        if (!pwInfo || pwInfo.ownerIsLocal !== false) return false;
        if (!weaponInfo || !botSoftLockAllowedClass(weaponInfo.wpnClass)) return false;
        if (!weaponInfo.weapon || weaponInfo.weapon === "0x0") return false;

        const key = ptrStr(playerWeaponsPtr);
        try { updateBotLifeState(botPtr || ptr(0), playerWeaponsPtr, null, reason + ".grenadeRecord"); } catch (e) {}

        const old = Runtime.botGrenadeWeapons[key] || Runtime.botGrenadeWeapons["pw:" + key];
        if (old && old.grenadeWeapon && old.grenadeWeapon !== weaponInfo.weapon && Runtime.config.bot_throw_respawn_reset_on_grenade_change) {
            resetBotLifeState(playerWeaponsPtr, botPtr || ptr(0), reason + ".grenade_change", false);
        }

        const stored = storeBotGrenadeRecordAliases(playerWeaponsPtr, pwInfo, weaponInfo, reason, botPtr);
        if (!stored || !stored.rec) return false;

        if (!old || old.grenadeWeapon !== weaponInfo.weapon) Runtime.stats.bot_grenade_records += 1;

        logOnce("bot_grenade_record:" + key + ":" + weaponInfo.weapon, "Bot手雷记录", Runtime.config.log_interval_ms, {
            playerWeapons: key,
            owner: pwInfo.owner,
            bot: ptrStr(botPtr || ptr(0)),
            grenadeWeapon: weaponInfo.weapon,
            className: weaponInfo.className,
            aliasKeys: stored.keys,
            reason: reason,
            records: Runtime.stats.bot_grenade_records,
            multikeyRecords: Runtime.stats.bot_grenade_multikey_records,
            enabled: Runtime.config.bot_grenade_mode_enabled,
            note: "v2.12.5：同一个Bot Grenade同时按playerWeapons/owner/bot多key缓存，减少VBC投掷前查不到Grenade"
        });
        return true;
    } catch (e) {
        recordError("recordBotGrenadeWeapon", e);
        return false;
    }
}

function getBotGrenadeRecordEx(playerWeaponsPtr, botPtr, pwInfo, reason) {
    const candidates = [];

    function addRaw(k) {
        if (!k || k === "0x0" || k === "null" || k === "undefined") return;
        if (candidates.indexOf(k) < 0) candidates.push(k);
    }
    function addPtr(prefix, p) {
        try {
            const s = (typeof p === "string") ? p : ptrStr(p);
            if (!s || s === "0x0" || s === "null" || s === "undefined") return;
            addRaw(prefix + ":" + s);
        } catch (e) {}
    }

    const pwKey = ptrStr(playerWeaponsPtr);
    addRaw(pwKey);              // 旧裸key兼容
    addPtr("pw", playerWeaponsPtr);

    if (pwInfo) addPtr("owner", pwInfo.owner);
    addPtr("bot", botPtr);

    try {
        if (botPtr && !botPtr.isNull() && isReadablePtr(botPtr)) {
            const player = readPointer(botPtr, Offsets.Bot_thisPlayer);
            addPtr("playerFromBot", player);
        }
    } catch (e) {}

    for (const k of candidates) {
        const rec = Runtime.botGrenadeWeapons[k];
        if (!rec) continue;
        if (isValidBotGrenadeRecord(rec, reason + ".key:" + k)) {
            if (k !== pwKey && k !== ("pw:" + pwKey)) Runtime.stats.bot_grenade_alias_hits += 1;
            return rec;
        }
        delete Runtime.botGrenadeWeapons[k];
    }

    return null;
}

function getBotGrenadeRecord(playerWeaponsPtr) {
    return getBotGrenadeRecordEx(playerWeaponsPtr, ptr(0), null, "legacy");
}


function rememberGrenadeWeaponIndex(weaponIndex, weaponInfo, reason) {
    try {
        const idx = parseInt(weaponIndex);
        if (!Number.isFinite(idx) || idx < 0) return false;
        if (!weaponInfo || !botSoftLockAllowedClass(weaponInfo.wpnClass)) return false;
        Runtime.knownGrenadeWeaponIndexes["" + idx] = {
            weaponIndex: idx,
            className: weaponInfo.className,
            wpnClass: weaponInfo.wpnClass,
            lastSeen: Date.now(),
            reason: reason
        };
        Runtime.lastBotGrenadeWeaponIndex = idx;
        Runtime.stats.bot_grenade_known_index_hits += 1;
        logOnce("known_grenade_index:" + idx, "已记录普通Grenade weaponIndex", Runtime.config.virtual_grenade_log_interval_ms || 1000, {
            weaponIndex: idx,
            className: weaponInfo.className,
            reason: reason,
            knownCount: Object.keys(Runtime.knownGrenadeWeaponIndexes).length,
            note: "v2.12.6：后续某个Bot没有Grenade指针时，可用该index主动补发真实Grenade"
        });
        return true;
    } catch (e) {
        recordError("rememberGrenadeWeaponIndex:" + reason, e);
        return false;
    }
}

function getKnownGrenadeWeaponIndex(reason) {
    try {
        if (Runtime.lastBotGrenadeWeaponIndex >= 0) return Runtime.lastBotGrenadeWeaponIndex;
        const keys = Object.keys(Runtime.knownGrenadeWeaponIndexes || {});
        if (keys.length <= 0) return -1;
        let best = null;
        for (const k of keys) {
            const item = Runtime.knownGrenadeWeaponIndexes[k];
            if (!best || (item.lastSeen || 0) > (best.lastSeen || 0)) best = item;
        }
        return best ? best.weaponIndex : -1;
    } catch (e) {
        recordError("getKnownGrenadeWeaponIndex:" + reason, e);
        return -1;
    }
}

function tryGiveBotGrenadeForThrow(botPtr, playerWeaponsPtr, pwInfo, reason) {
    Runtime.stats.bot_grenade_active_give_attempts += 1;
    try {
        if (!Runtime.config.bot_grenade_active_give_enabled) {
            Runtime.stats.bot_grenade_active_give_failed += 1;
            return null;
        }
        if (!pwInfo || pwInfo.ownerIsLocal !== false || !pwInfo.owner || pwInfo.owner === "0x0") {
            Runtime.stats.bot_grenade_active_give_failed += 1;
            return null;
        }

        const idx = (getKnownGrenadeWeaponIndex(reason) | 0);
        if (idx < 0) {
            Runtime.stats.bot_grenade_active_give_failed += 1;
            logOnce("bot_grenade_active_give_no_index:" + ptrStr(playerWeaponsPtr), "Bot主动补发Grenade失败", Runtime.config.bot_throw_drive_log_interval_ms || 1000, {
                reason: reason,
                bot: ptrStr(botPtr || ptr(0)),
                playerWeapons: ptrStr(playerWeaponsPtr),
                owner: pwInfo.owner,
                note: "还没有记录到任何普通Grenade weaponIndex，不能主动补发"
            });
            return null;
        }

        const key = ptrStr(playerWeaponsPtr);
        const now = Date.now();
        const cd = Runtime.config.bot_grenade_active_give_cooldown_ms || 1500;
        const last = Runtime.botGrenadeGiveLast[key] || 0;
        if (now - last < cd) {
            Runtime.stats.bot_grenade_active_give_cooldown += 1;
            return null;
        }
        Runtime.botGrenadeGiveLast[key] = now;

        setupNatives();
        const playerPtr = ptr(pwInfo.owner);
        if (!playerPtr || playerPtr.isNull() || !isReadablePtr(playerPtr)) {
            Runtime.stats.bot_grenade_active_give_failed += 1;
            return null;
        }

        const ret = Runtime.natives.GameManager_GiveWeapon_Original(playerPtr, (idx | 0), 0, 0, ptr(0));
        const retInfo = readWeaponInfo(ret);
        rememberGrenadeWeaponIndex(idx, retInfo, reason + ".activeGive.return");

        if (!ret || ret.isNull() || !botSoftLockAllowedClass(retInfo.wpnClass)) {
            Runtime.stats.bot_grenade_active_give_failed += 1;
            logOnce("bot_grenade_active_give_bad_return:" + key + ":" + idx, "Bot主动补发Grenade失败", Runtime.config.bot_throw_drive_log_interval_ms || 1000, {
                reason: reason,
                bot: ptrStr(botPtr || ptr(0)),
                playerWeapons: key,
                owner: pwInfo.owner,
                weaponIndex: idx,
                returnWeapon: ptrStr(ret),
                className: retInfo.className,
                wpnClass: retInfo.wpnClass,
                note: "GameManager.GiveWeapon返回的不是普通Grenade，不能Throw；v2.12.7已修复补发调用参数类型"
            });
            return null;
        }

        recordBotGrenadeWeapon(playerWeaponsPtr, pwInfo, retInfo, reason + ".activeGive", botPtr || ptr(0));
        const rec = getBotGrenadeRecordEx(playerWeaponsPtr, botPtr || ptr(0), pwInfo, reason + ".afterActiveGive");
        if (rec) {
            Runtime.stats.bot_grenade_active_give_success += 1;
            log("Bot主动补发Grenade成功", {
                reason: reason,
                bot: ptrStr(botPtr || ptr(0)),
                playerWeapons: key,
                owner: pwInfo.owner,
                weaponIndex: idx,
                grenadeWeapon: rec.grenadeWeapon,
                success: Runtime.stats.bot_grenade_active_give_success,
                note: "v2.12.6：该Bot原本无可用Grenade指针，已用已知普通Grenade index补发真实Grenade"
            });
            return rec;
        }

        Runtime.stats.bot_grenade_active_give_failed += 1;
        return null;
    } catch (e) {
        Runtime.stats.bot_grenade_active_give_failed += 1;
        recordError("tryGiveBotGrenadeForThrow:" + reason, e);
        return null;
    }
}

function ensureBotGrenadeBeforeThrow(botPtr, playerWeaponsPtr, pwInfo, reason) {
    Runtime.stats.bot_grenade_reacquire_attempts += 1;

    let rec = getBotGrenadeRecordEx(playerWeaponsPtr, botPtr || ptr(0), pwInfo, reason + ".initial");
    if (rec) {
        Runtime.stats.bot_grenade_reacquire_success += 1;
        return rec;
    }

    try {
        const got = getPlayerWeaponsFromBot(botPtr || ptr(0), reason + ".reacquireFromBot");
        if (got && got.pwPtr && !got.pwPtr.isNull() && got.pwInfo && got.pwInfo.ownerIsLocal === false) {
            rec = getBotGrenadeRecordEx(got.pwPtr, botPtr || ptr(0), got.pwInfo, reason + ".fromBot");
            if (rec) {
                Runtime.stats.bot_grenade_reacquire_success += 1;
                return rec;
            }
        }
    } catch (e) {
        recordError("ensureBotGrenadeBeforeThrow.fromBot:" + reason, e);
    }

    try {
        // 仍然禁枪，但在投掷前主动尝试临时Select(3)，让SetCurrentWeapon/SetWeapon观察点有机会补记录。
        Runtime.stats.bot_grenade_reacquire_select_calls += 1;
        maybeSelectBotGrenadeSlot(playerWeaponsPtr, reason + ".reacquireSelect3", true);
        rec = getBotGrenadeRecordEx(playerWeaponsPtr, botPtr || ptr(0), pwInfo, reason + ".afterSelect3");
        if (rec) {
            Runtime.stats.bot_grenade_reacquire_success += 1;
            return rec;
        }
    } catch (e) {
        recordError("ensureBotGrenadeBeforeThrow.select3:" + reason, e);
    }

    try {
        rec = tryGiveBotGrenadeForThrow(botPtr || ptr(0), playerWeaponsPtr, pwInfo, reason + ".activeGive");
        if (rec) {
            Runtime.stats.bot_grenade_reacquire_success += 1;
            return rec;
        }
    } catch (e) {
        recordError("ensureBotGrenadeBeforeThrow.activeGive:" + reason, e);
    }

    Runtime.stats.bot_grenade_reacquire_failed += 1;
    logOnce("bot_grenade_reacquire_failed:" + ptrStr(playerWeaponsPtr) + ":" + ptrStr(botPtr || ptr(0)), "Bot手雷补记录失败", Runtime.config.bot_throw_drive_log_interval_ms || 1000, {
        reason: reason,
        bot: ptrStr(botPtr || ptr(0)),
        playerWeapons: ptrStr(playerWeaponsPtr),
        owner: pwInfo ? pwInfo.owner : "0x0",
        knownGrenadeWeaponIndex: Runtime.lastBotGrenadeWeaponIndex,
        knownGrenadeIndexes: Object.keys(Runtime.knownGrenadeWeaponIndexes || {}),
        attempts: Runtime.stats.bot_grenade_reacquire_attempts,
        failed: Runtime.stats.bot_grenade_reacquire_failed,
        activeGiveFailed: Runtime.stats.bot_grenade_active_give_failed,
        note: "v2.12.6：保持禁枪，不放行原BotControl；缓存/Select(3)/主动补发都失败时才等待下一次机会"
    });
    return null;
}
function isBotGrenadeModeActive() {
    return Runtime.enabled && Runtime.config.bot_grenade_mode_enabled && Runtime.config.bot_grenade_record_enabled;
}

function getPlayerWeaponsFromBot(botPtr, reason) {
    const out = { bot: ptrStr(botPtr), player: "0x0", playerWeapons: "0x0", pwPtr: ptr(0), pwInfo: null };
    try {
        if (!botPtr || botPtr.isNull() || !isReadablePtr(botPtr)) return out;
        const player = readPointer(botPtr, Offsets.Bot_thisPlayer);
        out.player = ptrStr(player);
        if (!player || player.isNull() || !isReadablePtr(player)) return out;
        setupNatives();
        const pw = Runtime.natives.Player_get_wpns(player, ptr(0));
        out.playerWeapons = ptrStr(pw);
        out.pwPtr = pw;
        if (pw && !pw.isNull() && isReadablePtr(pw)) {
            out.pwInfo = readPlayerWeaponsInfo(pw);
            if (out.pwInfo && out.pwInfo.ownerIsLocal === false) updateBotLifeState(botPtr, pw, null, reason);
        }
        return out;
    } catch (e) {
        recordError("getPlayerWeaponsFromBot:" + reason, e);
        return out;
    }
}

function getWeaponDataSlot(weaponInfo) {
    try {
        if (!weaponInfo || !weaponInfo.data || weaponInfo.data === "0x0") return null;
        const data = ptr(weaponInfo.data);
        if (!data || data.isNull() || !isReadablePtr(data)) return null;
        return safeReadI32(data, Offsets.WeaponData_slot, "WeaponData.slot");
    } catch (e) {
        return null;
    }
}

function maybeSelectBotGrenadeSlot(playerWeaponsPtr, reason, forceForStateMachine) {
    if (!isBotGrenadeModeActive()) return false;
    if (!forceForStateMachine /* v2.12: global Bot.SelectWeapon forcing removed */) return false;
    try {
        const rec = getBotGrenadeRecordEx(playerWeaponsPtr, ptr(0), null, reason + ".select");
        if (!rec) {
            Runtime.stats.bot_grenade_temp_select_skipped_no_grenade += 1;
            logOnce("vg_select_no_grenade:" + ptrStr(playerWeaponsPtr), "BotGrenadeRecord跳过", Runtime.config.virtual_grenade_log_interval_ms || 1000, {
                reason: reason,
                playerWeapons: ptrStr(playerWeaponsPtr),
                forceForStateMachine: !!forceForStateMachine,
                note: "该bot还没有缓存到Grenade weapon ptr；保持禁枪，等待补记录"
            });
            return false;
        }
        setupNatives();
        const ok = Runtime.natives.PlayerWeapons_Select_Original(playerWeaponsPtr, 3, ptr(0)) ? true : false;
        Runtime.stats.bot_grenade_temp_select_calls += 1;
        log(forceForStateMachine ? "投掷前临时选择Bot手雷" : "BotGrenadeRecord强制Bot选手雷", {
            reason: reason,
            playerWeapons: ptrStr(playerWeaponsPtr),
            grenadeWeapon: rec.grenadeWeapon,
            slot: 3,
            selectReturn: ok,
            forced: Runtime.stats.bot_grenade_temp_select_calls,
            forceForStateMachine: !!forceForStateMachine,
            note: forceForStateMachine ? "v2.12.5：仅投掷前临时Select(3)，平时不干预官方选武器" : "全局Bot.SelectWeapon强制slot=3；默认关闭"
        });
        return true;
    } catch (e) {
        recordError("maybeSelectBotGrenadeSlot:" + reason, e);
        return false;
    }
}

function maybeForceScopeAllPlayersForBotLock(reason) {
    try {
        if (!Runtime.enabled || !Runtime.config.bot_grenade_mode_enabled || !Runtime.config.bot_grenade_force_scope_all_players) return;
        if (Runtime.config.infinite_grenade_scope !== "all_players") {
            Runtime.config.infinite_grenade_scope = "all_players";
            logOnce("force_scope_all_players", "Bot手雷模式自动切换作用范围", Runtime.config.log_interval_ms, {
                reason: reason,
                infinite_grenade_scope: Runtime.config.infinite_grenade_scope,
                note: "开启Bot手雷手雷模式时自动把无限手雷作用范围改为 all_players，保证bot也锁999/保护Remove"
            });
        }
    } catch (e) {}
}
function observeWeaponClass(info) {
    try {
        const name = info && info.className ? info.className : "Unknown";
        Runtime.classCounts[name] = (Runtime.classCounts[name] || 0) + 1;
        if (info && info.isThrowClass) Runtime.stats.observer_grenade_class_hits += 1;
        else if (info && info.wpnClass !== null) Runtime.stats.observer_non_grenade_class_hits += 1;
    } catch (e) {}
}


function observeBotGrenadeBehavior(name, details) {
    if (!Runtime.enabled || !Runtime.config.bot_grenade_behavior_observer_enabled) return;
    try {
        const d = details || {};
        const pw = d.playerWeapons || {};
        const wi = d.weaponInfo || {};
        if (pw.ownerIsLocal !== false) return;
        if (wi && wi.isThrowClass) {
            Runtime.stats.bot_throw_weapon_seen += 1;
            if (name.indexOf("SetCurrentWeapon") >= 0 || name.indexOf("Select") >= 0 || name.indexOf("SetWeapon") >= 0) Runtime.stats.bot_throw_weapon_selected += 1;
            logOnce("bot_throw_seen:" + name + ":" + wi.weapon, "Bot手雷行为观察", Runtime.config.log_interval_ms, {
                name: name, owner: pw.owner, weapon: wi.weapon, className: wi.className,
                note: "bot 已拥有/选择手雷类武器；后续要继续确认是否进入 WPN_Throw.Throw"
            });
        }
    } catch (e) {}
}

function maybeLogBotSummary(force) {
    if (!Runtime.enabled || !Runtime.config.bot_grenade_behavior_observer_enabled) return;
    try {
        const now = Date.now();
        const wait = Runtime.config.bot_grenade_summary_interval_ms || 5000;
        const last = Runtime.logLimiter["bot_summary"] || 0;
        if (!force && now - last < wait) return;
        Runtime.logLimiter["bot_summary"] = now;
        Runtime.stats.bot_summary_count += 1;
        log("Bot手雷行为汇总", {
            bot_throw_weapon_seen: Runtime.stats.bot_throw_weapon_seen,
            bot_throw_weapon_selected: Runtime.stats.bot_throw_weapon_selected,
            bot_throw_method_hits: Runtime.stats.bot_throw_method_hits,
            bot_missile_captured: Runtime.stats.bot_missile_captured,
            bot_remove_throw_hits: Runtime.stats.bot_remove_throw_hits,
            note: "seen/selected有数但throw=0，说明bot拿到或切到手雷，但AI没有执行投掷动作"
        });
    } catch (e) {}
}


function observeBotAttackEntry(name, weaponPtr, botPtr, extra) {
    if (!Runtime.enabled || !Runtime.config.bot_attack_observer_enabled) return;
    try {
        const wi = readWeaponInfo(weaponPtr);
        const isBotLike = wi.isMyWeapon === false;
        const data = Object.assign({
            name: name,
            weaponInfo: wi,
            bot: ptrStr(botPtr || ptr(0)),
            botLike: isBotLike
        }, extra || {});

        if (isBotLike) Runtime.stats.bot_attack_entry_hits += 1;

        if (name.indexOf("GunShoot") >= 0) {
            Runtime.stats.gun_shoot_hits += 1;
            if (isBotLike) Runtime.stats.gun_shoot_botlike_hits += 1;
        }
        if (name.indexOf("GenerateBullet") >= 0) {
            Runtime.stats.gun_generate_bullet_hits += 1;
            if (isBotLike) Runtime.stats.gun_generate_bullet_botlike_hits += 1;
        }
        if (name.indexOf("WPN_RPG.Fire") >= 0 || name.indexOf("WPN_RPG.OnFireBtn") >= 0) {
            if (name.indexOf("WPN_RPG.Fire") >= 0) Runtime.stats.rpg_fire_hits += 1;
            if (name.indexOf("WPN_RPG.OnFireBtnPressed") >= 0) Runtime.stats.rpg_on_fire_pressed_hits += 1;
            if (isBotLike) Runtime.stats.rpg_fire_botlike_hits += 1;
        }

        if (isBotLike || Runtime.config.virtual_grenade_observer_verbose) {
            logOnce("bot_attack:" + name + ":" + wi.weapon, "Bot攻击入口观察", Runtime.config.log_interval_ms, data);
        }
        maybeLogBotAttackSummary(false);
    } catch (e) {
        recordError("observeBotAttackEntry:" + name, e);
    }
}

function maybeLogBotAttackSummary(force) {
    if (!Runtime.enabled || !Runtime.config.bot_attack_observer_enabled) return;
    try {
        const now = Date.now();
        const wait = Runtime.config.bot_attack_summary_interval_ms || 5000;
        const last = Runtime.logLimiter["bot_attack_summary"] || 0;
        if (!force && now - last < wait) return;
        Runtime.logLimiter["bot_attack_summary"] = now;
        Runtime.stats.bot_attack_summary_count += 1;
        log("Bot攻击入口汇总", {
            gun_bot_control_hits: Runtime.stats.gun_bot_control_hits,
            gun_sniper_bot_control_hits: Runtime.stats.gun_sniper_bot_control_hits,
            gun_shoot_hits: Runtime.stats.gun_shoot_hits,
            gun_shoot_botlike_hits: Runtime.stats.gun_shoot_botlike_hits,
            gun_generate_bullet_hits: Runtime.stats.gun_generate_bullet_hits,
            gun_generate_bullet_botlike_hits: Runtime.stats.gun_generate_bullet_botlike_hits,
            rpg_bot_control_hits: Runtime.stats.rpg_bot_control_hits,
            rpg_fire_hits: Runtime.stats.rpg_fire_hits,
            rpg_fire_botlike_hits: Runtime.stats.rpg_fire_botlike_hits,
            rpg_on_fire_pressed_hits: Runtime.stats.rpg_on_fire_pressed_hits,
            bot_attack_entry_hits: Runtime.stats.bot_attack_entry_hits,
            bot_throw_weapon_seen: Runtime.stats.bot_throw_weapon_seen,
            bot_throw_weapon_selected: Runtime.stats.bot_throw_weapon_selected,
            bot_throw_method_hits: Runtime.stats.bot_throw_method_hits,
            note: "如果Gun/RPG攻击入口有数但WPN_Throw.Throw=0，说明bot AI攻击链路只驱动枪/RPG，不驱动手雷Throw"
        });
    } catch (e) {}
}

function hookBotControlObserver(name, rva, statName) {
    addHook(name, rva, {
        onEnter(args) {
            Runtime.stats.hook_hits += 1;
            Runtime.stats[statName] += 1;
            Runtime.stats.last_hook = name;
            observeBotAttackEntry(name + ".onEnter", args[0], args[1], { phase: "BotControl" });
        }
    });
}

function hookAttackNoArgObserver(name, rva) {
    addHook(name, rva, {
        onEnter(args) {
            Runtime.stats.hook_hits += 1;
            Runtime.stats.last_hook = name;
            observeBotAttackEntry(name + ".onEnter", args[0], ptr(0), { phase: "AttackNoArg" });
        }
    });
}

function installBotAttackObserverHooks() {
    if (!Runtime.config.virtual_botcontrol_replace_botcontrol) {
        hookBotControlObserver("WPN_Gun.BotControl", RVA.WPN_Gun_BotControl, "gun_bot_control_hits");
        hookBotControlObserver("WPN_Gun.SniperBotControl", RVA.WPN_Gun_SniperBotControl, "gun_sniper_bot_control_hits");
    }
    hookAttackNoArgObserver("WPN_Gun.GunShootFunction", RVA.WPN_Gun_GunShootFunction);
    hookAttackNoArgObserver("WPN_Gun.GunShoot_Logic", RVA.WPN_Gun_GunShoot_Logic);
    hookAttackNoArgObserver("WPN_Gun.GunShoot_NoCheck", RVA.WPN_Gun_GunShoot_NoCheck);
    hookAttackNoArgObserver("WPN_Gun.GunShoot", RVA.WPN_Gun_GunShoot);
    hookAttackNoArgObserver("WPN_Gun.GenerateBullet", RVA.WPN_Gun_GenerateBullet);
    if (!Runtime.config.virtual_botcontrol_replace_botcontrol) {
        hookBotControlObserver("WPN_RPG.BotControl", RVA.WPN_RPG_BotControl, "rpg_bot_control_hits");
    }
    hookAttackNoArgObserver("WPN_RPG.Fire", RVA.WPN_RPG_Fire);
    hookAttackNoArgObserver("WPN_RPG.OnFireBtnPressed", RVA.WPN_RPG_OnFireBtnPressed);
    hookAttackNoArgObserver("WPN_RPG.OnFireBtnUnPressed", RVA.WPN_RPG_OnFireBtnUnPressed);
}

function logWeaponObserver(name, details, useOnce) {
    if (!Runtime.enabled || !Runtime.config.virtual_grenade_observer_enabled) return;
    Runtime.stats.observer_hits += 1;
    const data = details || {};
    data.name = name;
    data.observer_hits = Runtime.stats.observer_hits;
    Runtime.observerLast = data;
    observeBotGrenadeBehavior(name, data);
    maybeLogBotSummary(false);
    if (useOnce) {
        logOnce("observer:" + name + ":" + JSON.stringify(data).slice(0, 120), "VirtualGrenadeMode观察", Runtime.config.log_interval_ms, data);
    } else {
        log("VirtualGrenadeMode观察", data);
    }
}

function hookPlayerWeaponsObserverVoid(name, rva, statName) {
    addHook(name, rva, {
        onEnter(args) {
            Runtime.stats.hook_hits += 1;
            Runtime.stats[statName] += 1;
            Runtime.stats.last_hook = name;
            if (!Runtime.enabled || !Runtime.config.virtual_grenade_observer_enabled) return;
            this.pwInfo = readPlayerWeaponsInfo(args[0]);
            logWeaponObserver(name + ".onEnter", { playerWeapons: this.pwInfo }, true);
        },
        onLeave(retval) {
            if (!Runtime.enabled || !Runtime.config.virtual_grenade_observer_enabled) return;
            logWeaponObserver(name + ".onLeave", { playerWeapons: this.pwInfo, retval: ptrStr(retval) }, true);
        }
    });
}

function installVirtualGrenadeObserverHooks() {
    hookPlayerWeaponsObserverVoid("PlayerWeapons.AutoSelect", RVA.PlayerWeapons_AutoSelect, "observer_autoSelect_hits");

    addHook("PlayerWeapons.GetValidSlot", RVA.PlayerWeapons_GetValidSlot, {
        onEnter(args) {
            Runtime.stats.hook_hits += 1;
            Runtime.stats.observer_getValidSlot_hits += 1;
            Runtime.stats.last_hook = "PlayerWeapons.GetValidSlot";
            this.self = args[0];
            this.pwInfo = readPlayerWeaponsInfo(args[0]);
        },
        onLeave(retval) {
            if (!Runtime.enabled) return;
            let slot = null;
            try { slot = retval.toInt32(); } catch (e) { slot = "read_failed"; }

            let forced = false;
            // v2.12终版：GetValidSlot强制返回3方案已删除，只保留观察日志。

            if (Runtime.config.virtual_grenade_observer_enabled) {
                logWeaponObserver("PlayerWeapons.GetValidSlot.onLeave", { playerWeapons: this.pwInfo, returnSlot: slot, forcedToGrenade: forced }, false);
            }
        }
    });

    addHook("PlayerWeapons.Select", RVA.PlayerWeapons_Select, {
        onEnter(args) {
            Runtime.stats.hook_hits += 1;
            Runtime.stats.observer_select_hits += 1;
            Runtime.stats.last_hook = "PlayerWeapons.Select";
            this.self = args[0];
            this.methodInfo = args[2] || ptr(0);
            let slot = null;
            try { slot = args[1].toInt32(); } catch (e) { slot = "read_failed"; }
            this.slot = slot;
            this.pwInfo = readPlayerWeaponsInfo(args[0]);
            if (!Runtime.enabled || !Runtime.config.virtual_grenade_observer_enabled) return;
            logWeaponObserver("PlayerWeapons.Select.onEnter", { playerWeapons: this.pwInfo, slot: slot }, false);
        },
        onLeave(retval) {
            if (!Runtime.enabled) return;
            let ok = null;
            try { ok = retval.toInt32() !== 0; } catch (e) { ok = "read_failed"; }
            if (Runtime.config.virtual_grenade_observer_enabled) {
                logWeaponObserver("PlayerWeapons.Select.onLeave", { playerWeapons: this.pwInfo, slot: this.slot, returnBool: ok }, false);
            }
            // v2.12终版：不再在Select.onLeave后自动纠正非手雷。
        }
    });

    addHook("PlayerWeapons.SelectByMouseRoll", RVA.PlayerWeapons_SelectByMouseRoll, {
        onEnter(args) {
            Runtime.stats.hook_hits += 1;
            Runtime.stats.observer_mouseRoll_hits += 1;
            Runtime.stats.last_hook = "PlayerWeapons.SelectByMouseRoll";
            if (!Runtime.enabled || !Runtime.config.virtual_grenade_observer_enabled) return;
            let forward = null;
            try { forward = args[1].toInt32() !== 0; } catch (e) { forward = "read_failed"; }
            this.pwInfo = readPlayerWeaponsInfo(args[0]);
            this.forward = forward;
            logWeaponObserver("PlayerWeapons.SelectByMouseRoll.onEnter", { playerWeapons: this.pwInfo, forward: forward }, false);
        },
        onLeave(retval) {
            if (!Runtime.enabled || !Runtime.config.virtual_grenade_observer_enabled) return;
            let ok = null;
            try { ok = retval.toInt32() !== 0; } catch (e) { ok = "read_failed"; }
            logWeaponObserver("PlayerWeapons.SelectByMouseRoll.onLeave", { playerWeapons: this.pwInfo, forward: this.forward, returnBool: ok }, false);
        }
    });

    hookPlayerWeaponsObserverVoid("PlayerWeapons.SelectFKeyWeapon", RVA.PlayerWeapons_SelectFKeyWeapon, "observer_fKey_hits");
    hookPlayerWeaponsObserverVoid("PlayerWeapons.SelectLastOrAutoSelect", RVA.PlayerWeapons_SelectLastOrAutoSelect, "observer_selectLastOrAuto_hits");

    addHook("PlayerWeapons.SelectLast", RVA.PlayerWeapons_SelectLast, {
        onEnter(args) {
            Runtime.stats.hook_hits += 1;
            Runtime.stats.observer_selectLast_hits += 1;
            Runtime.stats.last_hook = "PlayerWeapons.SelectLast";
            if (!Runtime.enabled || !Runtime.config.virtual_grenade_observer_enabled) return;
            this.pwInfo = readPlayerWeaponsInfo(args[0]);
        },
        onLeave(retval) {
            if (!Runtime.enabled || !Runtime.config.virtual_grenade_observer_enabled) return;
            let ok = null;
            try { ok = retval.toInt32() !== 0; } catch (e) { ok = "read_failed"; }
            logWeaponObserver("PlayerWeapons.SelectLast.onLeave", { playerWeapons: this.pwInfo, returnBool: ok }, false);
        }
    });

    addHook("PlayerWeapons.SetWeapon", RVA.PlayerWeapons_SetWeapon, {
        onEnter(args) {
            Runtime.stats.hook_hits += 1;
            Runtime.stats.observer_setWeapon_hits += 1;
            Runtime.stats.last_hook = "PlayerWeapons.SetWeapon";
            const weaponInfo = readWeaponInfo(args[1]);
            const pwInfo = readPlayerWeaponsInfo(args[0]);
            observeWeaponClass(weaponInfo);
            recordBotGrenadeWeapon(args[0], pwInfo, weaponInfo, "PlayerWeapons.SetWeapon.onEnter");
            if (!Runtime.enabled || !Runtime.config.virtual_grenade_observer_enabled) return;
            logWeaponObserver("PlayerWeapons.SetWeapon.onEnter", { playerWeapons: pwInfo, weaponInfo: weaponInfo }, false);
        }
    });

    addHook("PlayerWeapons.RemoveAll", RVA.PlayerWeapons_RemoveAll, {
        onEnter(args) {
            Runtime.stats.hook_hits += 1;
            Runtime.stats.observer_removeAll_hits += 1;
            Runtime.stats.last_hook = "PlayerWeapons.RemoveAll";
            try {
                const pwInfo = readPlayerWeaponsInfo(args[0]);
                if (pwInfo && pwInfo.ownerIsLocal === false && Runtime.config.bot_throw_respawn_reset_on_removeall) {
                    resetBotLifeState(args[0], ptr(0), "PlayerWeapons.RemoveAll.onEnter", true);
                }
            } catch (e) {}
            try { delete Runtime.botGrenadeWeapons[ptrStr(args[0])]; } catch (e) {}
            if (!Runtime.enabled || !Runtime.config.virtual_grenade_observer_enabled) return;
            logWeaponObserver("PlayerWeapons.RemoveAll.onEnter", { playerWeapons: readPlayerWeaponsInfo(args[0]) }, false);
        }
    });
}

function installRemoveGuard() {
    const address = addrOf(RVA.PlayerWeapons_Remove);
    Runtime.natives.PlayerWeapons_Remove_Original = new NativeFunction(address, "void", ["pointer", "pointer", "bool", "pointer"], CALL_CONV);
    const replacement = new NativeCallback(function(thisPtr, weapon, recycle, methodInfo) {
        Runtime.stats.remove_hits += 1; Runtime.stats.last_hook = "PlayerWeapons.Remove";
        try {
            if (Runtime.enabled && Runtime.config.virtual_grenade_observer_enabled) {
                const weaponInfo = readWeaponInfo(weapon);
                const pwInfo = readPlayerWeaponsInfo(thisPtr);
                observeWeaponClass(weaponInfo);
                recordBotGrenadeWeapon(thisPtr, pwInfo, weaponInfo, "PlayerWeapons.Remove.onEnter");
                logWeaponObserver("PlayerWeapons.Remove.onEnter", { playerWeapons: pwInfo, weaponInfo: weaponInfo, recycle: !!recycle }, false);
            }
            if (Runtime.enabled && Runtime.config.protect_weapon_remove && isProtectedThrowWeapon(weapon)) {
                const scopeInfo = throwWeaponAllowedByScope(weapon, "PlayerWeapons.Remove.guard");
                const weaponInfoForRemove = readWeaponInfo(weapon);
                if (scopeInfo.isMyWeapon === false && weaponInfoForRemove && weaponInfoForRemove.isThrowClass) Runtime.stats.bot_remove_throw_hits += 1;
                if (scopeInfo.allowedByInfiniteScope) {
                    Runtime.stats.remove_blocked += 1;
                    log("已阻止删除当前手雷武器对象", {
                        thisPtr: ptrStr(thisPtr), weapon: ptrStr(weapon), recycle: !!recycle, blocked: Runtime.stats.remove_blocked,
                        scope: scopeInfo.scope, isMyWeapon: scopeInfo.isMyWeapon
                    });
                    return;
                }
            }
            Runtime.stats.remove_allowed += 1;
            Runtime.natives.PlayerWeapons_Remove_Original(thisPtr, weapon, recycle, methodInfo);
        } catch (e) {
            recordError("PlayerWeapons.Remove.replacement", e);
            try { Runtime.natives.PlayerWeapons_Remove_Original(thisPtr, weapon, recycle, methodInfo); } catch (e2) { recordError("PlayerWeapons.Remove.original_after_error", e2); }
        }
    }, "void", ["pointer", "pointer", "bool", "pointer"], CALL_CONV);
    Interceptor.replace(address, replacement);
    Runtime.replacements.push({ name: "PlayerWeapons.Remove", address: address, replacement: replacement });
    log("Replace 已安装", { name: "PlayerWeapons.Remove", address: address.toString(), mode: "仅保护当前手雷对象" });
}



function isBotThrowDriveActive() {
    return Runtime.enabled && Runtime.config.bot_grenade_mode_enabled && Runtime.config.bot_throw_drive_enabled;
}

function forceBotThrowReadyDirect(grenadePtr, reason) {
    try {
        if (!Runtime.config.bot_throw_drive_force_ready) return false;
        if (!grenadePtr || grenadePtr.isNull() || !isReadablePtr(grenadePtr)) return false;
        const before = safeReadU8(grenadePtr, Offsets.WPN_Throw_throwReady, reason + ".before");
        try { grenadePtr.add(Offsets.WPN_Throw_throwReady).writeU8(1); } catch(e) {}
        Runtime.stats.bot_throw_drive_force_ready_writes += 1;
        logOnce("bot_throw_ready_direct:" + ptrStr(grenadePtr), "Bot投掷驱动就绪", Runtime.config.bot_throw_drive_log_interval_ms || 1000, {
            grenadeWeapon: ptrStr(grenadePtr),
            before: before,
            after: safeReadU8(grenadePtr, Offsets.WPN_Throw_throwReady, reason + ".after"),
            reason: reason,
            writes: Runtime.stats.bot_throw_drive_force_ready_writes
        });
        return true;
    } catch (e) {
        Runtime.stats.bot_throw_drive_errors += 1;
        recordError("forceBotThrowReadyDirect:" + reason, e);
        return false;
    }
}

function driveBotThrowFromPlayerWeapons(playerWeaponsPtr, reason, methodInfo, botPtr) {
    if (!isBotThrowDriveActive()) {
        Runtime.stats.bot_throw_drive_skipped_disabled += 1;
        return false;
    }
    Runtime.stats.bot_throw_drive_attempts += 1;

    try {
        if (!playerWeaponsPtr || playerWeaponsPtr.isNull() || !isReadablePtr(playerWeaponsPtr)) {
            Runtime.stats.bot_throw_drive_skipped_no_pw += 1;
            return false;
        }

        const pwInfo = readPlayerWeaponsInfo(playerWeaponsPtr);
        if (!pwInfo || pwInfo.ownerIsLocal !== false) {
            Runtime.stats.bot_throw_drive_skipped_not_bot += 1;
            return false;
        }

        const rec = ensureBotGrenadeBeforeThrow(botPtr || ptr(0), playerWeaponsPtr, pwInfo, reason);
        if (!rec) {
            Runtime.stats.bot_throw_drive_skipped_no_grenade += 1;
            Runtime.stats.bot_throw_gate_block_no_grenade += 1;
            logOnce("bot_throw_drive_no_grenade:" + ptrStr(playerWeaponsPtr), "Bot投掷驱动跳过", Runtime.config.bot_throw_drive_log_interval_ms || 1000, {
                reason: reason,
                bot: ptrStr(botPtr || ptr(0)),
                playerWeapons: ptrStr(playerWeaponsPtr),
                note: "v2.12.5：当前还没有可安全调用的Grenade weapon ptr；保持禁枪，不调用空指针Throw，等待补记录"
            });
            return false;
        }

        const key = ptrStr(playerWeaponsPtr);
        const now = Date.now();
        const cd = Runtime.config.bot_throw_drive_cooldown_ms || 2500;

        const gate = canBotThrowNow(botPtr || ptr(0), playerWeaponsPtr, reason + ".HardGate", null, rec, { cooldownMs: cd });
        if (!gate.allow) {
            if (gate.reason === "cooldown") Runtime.stats.bot_throw_drive_skipped_cooldown += 1;
            if (gate.reason === "no_grenade") Runtime.stats.bot_throw_drive_skipped_no_grenade += 1;
            logBotThrowGateBlocked(gate, reason + ".HardGate", Runtime.config.bot_throw_drive_log_interval_ms || 1000);
            return false;
        }

        const last = Runtime.botThrowDriveLast[key] || 0;
        if (now - last < cd) {
            Runtime.stats.bot_throw_drive_skipped_cooldown += 1;
            Runtime.stats.bot_throw_gate_block_cooldown += 1;
            return false;
        }

        const grenadePtr = ptr(rec.grenadeWeapon);
        if (!grenadePtr || grenadePtr.isNull() || !isReadablePtr(grenadePtr)) {
            delete Runtime.botGrenadeWeapons[key];
            Runtime.stats.bot_throw_drive_skipped_no_grenade += 1;
            return false;
        }

        const wi = readWeaponInfo(grenadePtr);
        if (!botSoftLockAllowedClass(wi.wpnClass)) {
            Runtime.stats.bot_throw_drive_skipped_no_grenade += 1;
            return false;
        }

        Runtime.botThrowDriveLast[key] = now;
        markBotThrowCommitted(playerWeaponsPtr, botPtr || ptr(0), reason);

        try { maybeSelectBotGrenadeSlot(playerWeaponsPtr, reason + ".directPreSelect", true); } catch (e) {}

        if (Runtime.config.bot_throw_drive_lock_before_after) {
            try { lockAmmo(grenadePtr, reason + ".beforeThrow"); } catch (e) {}
        }
        forceBotThrowReadyDirect(grenadePtr, reason + ".forceReady");

        setupNatives();
        Runtime.natives.WPN_Throw_Throw_Original(grenadePtr, methodInfo || ptr(0));

        if (Runtime.config.bot_throw_drive_lock_before_after) {
            try { lockAmmo(grenadePtr, reason + ".afterThrow"); } catch (e) {}
        }

        Runtime.stats.bot_throw_drive_success += 1;
        log("Bot投掷驱动成功", {
            reason: reason,
            playerWeapons: key,
            owner: rec.owner,
            grenadeWeapon: rec.grenadeWeapon,
            cooldown_ms: cd,
            success: Runtime.stats.bot_throw_drive_success,
            note: "已在bot攻击入口直接调用WPN_Throw.Throw；是否生成missile看bot_missile_captured/capture_hits"
        });
        return true;
    } catch (e) {
        Runtime.stats.bot_throw_drive_errors += 1;
        recordError("driveBotThrowFromPlayerWeapons:" + reason, e);
        logOnce("bot_throw_drive_error:" + reason, "Bot投掷驱动失败", Runtime.config.bot_throw_drive_log_interval_ms || 1000, {
            reason: reason,
            error: "" + e,
            errors: Runtime.stats.bot_throw_drive_errors
        });
        return false;
    }
}


function isVirtualBotControlActive() {
    return Runtime.enabled && Runtime.config.bot_grenade_mode_enabled && Runtime.config.virtual_botcontrol_enabled;
}

function tryVirtualBotControl(botPtr, weaponPtr, name, methodInfo) {
    Runtime.stats.vbc_attempts += 1;
    try {
        if (!isVirtualBotControlActive()) {
            Runtime.stats.vbc_skipped_disabled += 1;
            return false;
        }
        if (!botPtr || botPtr.isNull() || !isReadablePtr(botPtr)) {
            Runtime.stats.vbc_skipped_no_bot += 1;
            return false;
        }

        const got = getPlayerWeaponsFromBot(botPtr, name + ".VirtualBotControl");
        if (!got.pwPtr || got.pwPtr.isNull() || !got.pwInfo || got.pwInfo.ownerIsLocal !== false) {
            Runtime.stats.vbc_skipped_no_pw += 1;
            return false;
        }

        const beforeNoGrenade = Runtime.stats.bot_throw_drive_skipped_no_grenade;
        const beforeCooldown = Runtime.stats.bot_throw_drive_skipped_cooldown;
        const ok = driveBotThrowFromPlayerWeapons(got.pwPtr, name + ".VirtualBotControl", methodInfo || ptr(0), botPtr);
        if (ok) {
            Runtime.stats.vbc_success += 1;
            log("VirtualBotControl投掷接管成功", {
                name: name,
                bot: ptrStr(botPtr),
                gunWeapon: ptrStr(weaponPtr),
                playerWeapons: ptrStr(got.pwPtr),
                success: Runtime.stats.vbc_success,
                note: "已在官方BotControl层接管，转为Grenade的WPN_Throw.Throw"
            });
            return true;
        }

        if (Runtime.stats.bot_throw_drive_skipped_no_grenade > beforeNoGrenade) Runtime.stats.vbc_skipped_no_grenade += 1;
        if (Runtime.stats.bot_throw_drive_skipped_cooldown > beforeCooldown) Runtime.stats.vbc_skipped_cooldown += 1;

        logOnce("vbc_not_ready:" + name + ":" + ptrStr(got.pwPtr), "VirtualBotControl未接管", Runtime.config.virtual_botcontrol_log_interval_ms || 1000, {
            name: name,
            bot: ptrStr(botPtr),
            gunWeapon: ptrStr(weaponPtr),
            playerWeapons: ptrStr(got.pwPtr),
            note: "未能投掷，可能原因：没有缓存Grenade或冷却中；v2.11.3默认会禁止原枪械BotControl开火"
        });
        return false;
    } catch (e) {
        Runtime.stats.vbc_errors += 1;
        recordError("tryVirtualBotControl:" + name, e);
        return false;
    }
}

function installVirtualBotControlControls() {
    function replaceBotControl(name, rva, statName, configName) {
        try {
            const address = addrOf(rva);
            const nativeName = name.replace(/[^A-Za-z0-9_]/g, "_") + "_Original";
            Runtime.natives[nativeName] = new NativeFunction(address, "void", ["pointer", "pointer", "pointer"], CALL_CONV);
            const replacement = new NativeCallback(function(weaponPtr, botPtr, methodInfo) {
                Runtime.stats[statName] += 1;
                Runtime.stats.hook_hits += 1;
                Runtime.stats.last_hook = name + ".VirtualBotControl";
                try {
                    if (Runtime.config.bot_attack_observer_enabled) {
                        observeBotAttackEntry(name + ".VirtualBotControl", weaponPtr, botPtr, { phase: "VirtualBotControl" });
                    }

                    if (isVirtualBotControlActive() && Runtime.config[configName]) {
                        const beforeNoGrenade = Runtime.stats.vbc_skipped_no_grenade;
                        const beforeCooldown = Runtime.stats.vbc_skipped_cooldown;
                        const ok = tryVirtualBotControl(botPtr, weaponPtr, name, methodInfo || ptr(0));
                        const noGrenadeDelta = Runtime.stats.vbc_skipped_no_grenade - beforeNoGrenade;
                        const cooldownDelta = Runtime.stats.vbc_skipped_cooldown - beforeCooldown;
                        if (ok && Runtime.config.virtual_botcontrol_skip_original_on_success) {
                            return;
                        }
                        if (!ok && Runtime.config.bot_suppress_gun_fire_enabled) {
                            if (noGrenadeDelta > 0 && Runtime.config.bot_suppress_gun_fire_when_no_grenade) Runtime.stats.vbc_suppress_no_grenade += 1;
                            if (cooldownDelta > 0) Runtime.stats.vbc_suppress_cooldown += 1;
                            Runtime.stats.vbc_suppressed_original_calls += 1;
                            logOnce("vbc_suppress_original:" + name + ":" + ptrStr(botPtr), "Bot枪械开火已禁止", Runtime.config.virtual_botcontrol_log_interval_ms || 1000, {
                                name: name,
                                bot: ptrStr(botPtr),
                                weapon: ptrStr(weaponPtr),
                                noGrenadeDelta: noGrenadeDelta,
                                cooldownDelta: cooldownDelta,
                                suppressed: Runtime.stats.vbc_suppressed_original_calls,
                                note: "v2.11.3：BotControl未能转手雷时，默认不再调用原枪械BotControl，避免bot先开枪再扔雷"
                            });
                            return;
                        }
                    } else {
                        Runtime.stats.vbc_skipped_disabled += 1;
                    }

                    Runtime.stats.vbc_original_calls += 1;
                    Runtime.natives[nativeName](weaponPtr, botPtr, methodInfo);
                } catch (e) {
                    Runtime.stats.vbc_errors += 1;
                    recordError(name + ".VirtualBotControl.replacement", e);
                    try { Runtime.natives[nativeName](weaponPtr, botPtr, methodInfo); } catch (e2) { recordError(name + ".VirtualBotControl.original_after_error", e2); }
                }
            }, "void", ["pointer", "pointer", "pointer"], CALL_CONV);
            Interceptor.replace(address, replacement);
            Runtime.replacements.push({ name: name, address: address, replacement: replacement });
            log("Replace 已安装", { name: name, address: address.toString(), mode: "VirtualBotControl: BotControl层转手雷Throw" });
        } catch (e) {
            Runtime.stats.vbc_errors += 1;
            recordError("installVirtualBotControlControls:" + name, e);
        }
    }

    if (Runtime.config.virtual_botcontrol_replace_botcontrol) {
        replaceBotControl("WPN_Gun.BotControl", RVA.WPN_Gun_BotControl, "vbc_gun_botcontrol_hits", "virtual_botcontrol_gun_enabled");
        replaceBotControl("WPN_Gun.SniperBotControl", RVA.WPN_Gun_SniperBotControl, "vbc_sniper_botcontrol_hits", "virtual_botcontrol_sniper_enabled");
        replaceBotControl("WPN_RPG.BotControl", RVA.WPN_RPG_BotControl, "vbc_rpg_botcontrol_hits", "virtual_botcontrol_rpg_enabled");
    }
}



function readBotAIInfo(botPtr, reason) {
    const out = {
        bot: ptrStr(botPtr),
        player: "0x0",
        playerWeapons: "0x0",
        ownerIsLocal: null,
        attackTarget: "0x0",
        hasAttackTarget: false,
        hasGrenadeRecord: false,
        grenadeWeapon: "0x0"
    };
    try {
        if (!botPtr || botPtr.isNull() || !isReadablePtr(botPtr)) return out;
        const target = readPointer(botPtr, Offsets.Bot_attackTarget);
        out.attackTarget = ptrStr(target);
        out.hasAttackTarget = !!(target && !target.isNull() && isReadablePtr(target));
        if (out.hasAttackTarget) Runtime.stats.bot_ai_target_seen += 1;
        else Runtime.stats.bot_ai_target_missing += 1;

        const got = getPlayerWeaponsFromBot(botPtr, reason + ".readBotAIInfo");
        out.player = got.player;
        out.playerWeapons = got.playerWeapons;
        if (got.pwInfo) out.ownerIsLocal = got.pwInfo.ownerIsLocal;
        if (got.pwPtr && !got.pwPtr.isNull()) {
            const rec = getBotGrenadeRecord(got.pwPtr);
            if (rec) {
                out.hasGrenadeRecord = true;
                out.grenadeWeapon = rec.grenadeWeapon;
            }
        }
        return out;
    } catch (e) {
        Runtime.stats.bot_ai_errors += 1;
        recordError("readBotAIInfo:" + reason, e);
        return out;
    }
}

function logBotAIProbe(name, botPtr, extra) {
    if (!Runtime.enabled || !Runtime.config.bot_ai_probe_enabled) return;
    try {
        const info = readBotAIInfo(botPtr, name);
        const data = Object.assign({ name: name, botAI: info }, extra || {});
        if (Runtime.config.bot_ai_probe_verbose || info.hasGrenadeRecord || info.hasAttackTarget) {
            logOnce("bot_ai_probe:" + name + ":" + info.bot + ":" + info.attackTarget, "BotAI观察", Runtime.config.bot_ai_probe_log_interval_ms || 1000, data);
        }
    } catch (e) {
        Runtime.stats.bot_ai_errors += 1;
        recordError("logBotAIProbe:" + name, e);
    }
}




function boolRetval(retval) {
    try {
        if (!retval) return false;
        // IL2CPP bool 在 x86 上通常只看 AL；日志里可能出现 0x86dde01 这种高位脏值。
        return ((retval.toInt32() & 0xFF) !== 0);
    } catch (e) {
        return !!retval;
    }
}

function evaluateSmartGrenadeAI(botPtr, got, info, name, retval) {
    const result = {
        allow: true,
        reason: "ok",
        name: name,
        officialVisible: null,
        officialVisibilityFresh: false
    };

    if (!Runtime.config.smart_grenade_ai_enabled) return result;
    Runtime.stats.smart_ai_eval += 1;

    try {
        const now = Date.now();
        const botKey = ptrStr(botPtr);

        // v2.12.1终版：只保留官方可见/无遮挡判断。
        if (name === "Bot.CheckAttackTarget.onLeave") {
            let ok = false;
            try { ok = retval ? (retval.toInt32() !== 0) : false; } catch (e) { ok = false; }
            Runtime.botAiOfficialVisible[botKey] = { ok: ok, ts: now };
            result.officialVisible = ok;
            result.officialVisibilityFresh = true;
            if (ok) Runtime.stats.smart_ai_official_visible_true += 1;
            else Runtime.stats.smart_ai_official_visible_false += 1;

            if (Runtime.config.smart_grenade_require_official_visible && !ok) {
                Runtime.stats.smart_ai_skipped_official_visibility += 1;
                result.allow = false;
                result.reason = "official_checkattack_false";
                return result;
            }
        } else if (Runtime.config.smart_grenade_require_official_visible) {
            const last = Runtime.botAiOfficialVisible[botKey];
            const freshMs = Runtime.config.smart_grenade_recent_visible_ms || 350;
            if (!last || !last.ok || (now - last.ts) > freshMs) {
                Runtime.stats.smart_ai_skipped_official_visibility += 1;
                result.allow = false;
                result.reason = "no_recent_official_visible";
                return result;
            }
            result.officialVisible = last.ok;
            result.officialVisibilityFresh = true;
        }

        Runtime.stats.smart_ai_allowed += 1;
        return result;
    } catch (e) {
        Runtime.stats.bot_ai_errors += 1;
        recordError("evaluateSmartGrenadeAI:" + name, e);
        result.allow = true;
        result.reason = "smart_ai_error_allow:" + e;
        return result;
    }
}

function getBotThrowStateKey(botPtr, pwPtr) {
    return ptrStr(botPtr || ptr(0)) + "|" + ptrStr(pwPtr || ptr(0));
}

function getBotThrowState(botPtr, pwPtr) {
    const key = getBotThrowStateKey(botPtr, pwPtr);
    let st = Runtime.botThrowStates[key];
    if (!st) {
        st = { state: "IDLE", key: key, bot: ptrStr(botPtr), playerWeapons: ptrStr(pwPtr), firstSeenAt: 0, targetFirstSeenAt: 0, lastStableTarget: "0x0", startedAt: 0, nextAt: 0, cooldownUntil: 0, attempts: 0, lastReason: "", attackTarget: "0x0", grenadeWeapon: "0x0" };
        Runtime.botThrowStates[key] = st;
    }
    return st;
}

function resetBotThrowState(st, reason) {
    if (!st) return;
    st.state = "IDLE";
    st.startedAt = 0;
    st.nextAt = 0;
    st.lastReason = reason || "";
    Runtime.stats.bot_throw_sm_reset += 1;
}

function cleanupBotThrowStates(reason) {
    try {
        const now = Date.now();
        const ttl = Math.max(3000, Runtime.config.bot_throw_state_timeout_ms || 1200) + Math.max(1000, Runtime.config.bot_ai_hook_drive_cooldown_ms || 1000) + 3000;
        for (const k of Object.keys(Runtime.botThrowStates)) {
            const st = Runtime.botThrowStates[k];
            const t = Math.max(st.startedAt || 0, st.cooldownUntil || 0, st.nextAt || 0);
            if (t > 0 && now - t > ttl) delete Runtime.botThrowStates[k];
        }
    } catch (e) {}
}

function logBotThrowState(st, message, data) {
    try {
        logOnce("bot_throw_state:" + st.key + ":" + st.state + ":" + message, "Bot投掷状态机", Runtime.config.bot_throw_state_log_interval_ms || 500, Object.assign({
            state: st.state,
            bot: st.bot,
            playerWeapons: st.playerWeapons,
            attackTarget: st.attackTarget,
            grenadeWeapon: st.grenadeWeapon,
            attempts: st.attempts
        }, data || {}));
    } catch (e) {}
}
function getBotLifeKey(playerWeaponsPtr, botPtr) {
    const pw = ptrStr(playerWeaponsPtr || ptr(0));
    if (pw && pw !== "0x0" && pw !== "invalid") return pw;
    return "bot:" + ptrStr(botPtr || ptr(0));
}

function updateBotLifeState(botPtr, playerWeaponsPtr, info, reason) {
    const now = Date.now();
    const key = getBotLifeKey(playerWeaponsPtr, botPtr);
    let st = Runtime.botLifeStates[key];
    if (!st) {
        st = {
            key: key,
            firstSeenAt: now,
            lastSeenAt: now,
            bot: ptrStr(botPtr || ptr(0)),
            playerWeapons: ptrStr(playerWeaponsPtr || ptr(0)),
            lastTarget: "0x0",
            targetFirstSeenAt: 0,
            lastThrowAt: 0,
            firstThrowDone: false,
            lastReason: reason || "",
            lastRespawnResetAt: 0,
            respawnCount: 0
        };
        Runtime.botLifeStates[key] = st;
        Runtime.stats.bot_life_first_seen += 1;
        Runtime.stats.bot_throw_spawn_first_seen += 1;
        logOnce("bot_life_first_seen:" + key, "Bot生命周期首次识别", Runtime.config.bot_throw_state_log_interval_ms || 500, {
            key: key,
            bot: st.bot,
            playerWeapons: st.playerWeapons,
            reason: reason,
            spawn_grace_ms: Runtime.config.bot_throw_spawn_grace_ms || 3000,
            first_extra_ms: Runtime.config.bot_throw_first_throw_extra_delay_ms || 1000
        });
    }

    st.lastSeenAt = now;
    if (botPtr && !botPtr.isNull()) st.bot = ptrStr(botPtr);
    if (playerWeaponsPtr && !playerWeaponsPtr.isNull()) st.playerWeapons = ptrStr(playerWeaponsPtr);
    st.lastReason = reason || st.lastReason || "";

    let target = null;
    if (info && info.attackTarget) target = info.attackTarget;
    else if (botPtr && !botPtr.isNull() && isReadablePtr(botPtr)) {
        try { target = ptrStr(readPointer(botPtr, Offsets.Bot_attackTarget)); } catch (e) { target = null; }
    }
    if (!target) target = st.lastTarget || "0x0";

    if (target !== st.lastTarget) {
        st.lastTarget = target;
        st.targetFirstSeenAt = now;
        Runtime.stats.bot_throw_target_changed += 1;
        logOnce("bot_life_target_changed:" + key + ":" + target, "Bot目标变化", Runtime.config.bot_throw_state_log_interval_ms || 500, {
            key: key,
            bot: st.bot,
            playerWeapons: st.playerWeapons,
            attackTarget: target,
            reason: reason
        });
    }

    return st;
}


function resetBotLifeState(playerWeaponsPtr, botPtr, reason, force) {
    if (!Runtime.config.bot_throw_respawn_reset_enabled && !force) return null;
    try {
        const now = Date.now();
        const key = getBotLifeKey(playerWeaponsPtr || ptr(0), botPtr || ptr(0));
        let st = Runtime.botLifeStates[key];
        const cd = Runtime.config.bot_throw_respawn_reset_cooldown_ms || 1500;

        if (st && !force && st.lastRespawnResetAt && now - st.lastRespawnResetAt < cd) {
            Runtime.stats.bot_life_reset_cooldown_skip += 1;
            return st;
        }

        if (!st) {
            st = {
                key: key,
                firstSeenAt: now,
                lastSeenAt: now,
                bot: ptrStr(botPtr || ptr(0)),
                playerWeapons: ptrStr(playerWeaponsPtr || ptr(0)),
                lastTarget: "0x0",
                targetFirstSeenAt: 0,
                lastThrowAt: 0,
                firstThrowDone: false,
                lastReason: reason || "",
                lastRespawnResetAt: now,
                respawnCount: 0
            };
            Runtime.botLifeStates[key] = st;
            Runtime.stats.bot_life_first_seen += 1;
            Runtime.stats.bot_throw_spawn_first_seen += 1;
        }

        st.firstSeenAt = now;
        st.lastSeenAt = now;
        st.targetFirstSeenAt = 0;
        st.lastTarget = "0x0";
        st.lastThrowAt = 0;
        st.firstThrowDone = false;
        st.lastReason = reason || "";
        st.lastRespawnResetAt = now;
        st.respawnCount = (st.respawnCount || 0) + 1;
        if (botPtr && !botPtr.isNull()) st.bot = ptrStr(botPtr);
        if (playerWeaponsPtr && !playerWeaponsPtr.isNull()) st.playerWeapons = ptrStr(playerWeaponsPtr);

        Runtime.stats.bot_life_respawn_reset += 1;
        if ((reason || "").indexOf("RemoveAll") >= 0) Runtime.stats.bot_life_reset_removeall += 1;
        else if ((reason || "").indexOf("GiveWeapon") >= 0) Runtime.stats.bot_life_reset_giveweapon += 1;
        else if ((reason || "").indexOf("grenade_change") >= 0) Runtime.stats.bot_life_reset_grenade_change += 1;

        logOnce("bot_life_respawn_reset:" + key + ":" + (reason || ""), "Bot生命周期已重置", Runtime.config.bot_throw_state_log_interval_ms || 500, {
            key: key,
            bot: st.bot,
            playerWeapons: st.playerWeapons,
            reason: reason,
            respawnCount: st.respawnCount,
            spawn_grace_ms: Runtime.config.bot_throw_spawn_grace_ms || 3000,
            first_extra_ms: Runtime.config.bot_throw_first_throw_extra_delay_ms || 1000,
            note: "v2.11.6：检测到复活/重新发枪/手雷对象变化，重新应用出生保护"
        });

        return st;
    } catch (e) {
        recordError("resetBotLifeState:" + reason, e);
        return null;
    }
}


function canBotThrowNow(botPtr, playerWeaponsPtr, reason, info, rec, opts) {
    Runtime.stats.bot_throw_gate_eval += 1;

    if (!Runtime.config.bot_throw_unified_gate_enabled) {
        Runtime.stats.bot_throw_gate_allowed += 1;
        return { allow: true, reason: "gate_disabled" };
    }

    const now = Date.now();
    const key = getBotLifeKey(playerWeaponsPtr, botPtr);
    const st = updateBotLifeState(botPtr || ptr(0), playerWeaponsPtr || ptr(0), info || null, reason || "");

    try {
        if (!playerWeaponsPtr || playerWeaponsPtr.isNull() || !isReadablePtr(playerWeaponsPtr)) {
            Runtime.stats.bot_throw_gate_block_unknown_bot += 1;
            return { allow: false, reason: "unknown_playerWeapons", key: key, life: st };
        }

        const pwInfo = readPlayerWeaponsInfo(playerWeaponsPtr);
        if (!pwInfo || pwInfo.ownerIsLocal !== false) {
            Runtime.stats.bot_throw_gate_block_not_bot += 1;
            return { allow: false, reason: "not_bot", key: key, life: st };
        }

        const age = now - (st.firstSeenAt || now);
        if (Runtime.config.bot_throw_spawn_grace_enabled) {
            const grace = Runtime.config.bot_throw_spawn_grace_ms || 3000;
            if (age < grace) {
                Runtime.stats.bot_throw_gate_block_spawn += 1;
                Runtime.stats.bot_throw_spawn_grace_skipped += 1;
                return { allow: false, reason: "spawn_grace", key: key, life: st, ageMs: age, needMs: grace };
            }
        }

        const extra = Runtime.config.bot_throw_first_throw_extra_delay_ms || 0;
        if (!st.firstThrowDone && extra > 0) {
            const grace = Runtime.config.bot_throw_spawn_grace_enabled ? (Runtime.config.bot_throw_spawn_grace_ms || 3000) : 0;
            const need = grace + extra;
            if (age < need) {
                Runtime.stats.bot_throw_gate_block_first_extra += 1;
                return { allow: false, reason: "first_throw_extra_delay", key: key, life: st, ageMs: age, needMs: need };
            }
        }

        if (Runtime.config.bot_throw_target_stable_enabled) {
            const target = st.lastTarget || "0x0";
            const stableMs = Runtime.config.bot_throw_target_stable_ms || 700;
            const tAge = now - (st.targetFirstSeenAt || now);
            if (target && target !== "0x0" && tAge < stableMs) {
                Runtime.stats.bot_throw_gate_block_target_unstable += 1;
                Runtime.stats.bot_throw_target_stable_skipped += 1;
                return { allow: false, reason: "target_not_stable", key: key, life: st, targetAgeMs: tAge, needMs: stableMs, attackTarget: target };
            }
        }

        const realRec = rec || getBotGrenadeRecord(playerWeaponsPtr);
        if (!realRec || !realRec.grenadeWeapon || realRec.grenadeWeapon === "0x0") {
            Runtime.stats.bot_throw_gate_block_no_grenade += 1;
            return { allow: false, reason: "no_grenade", key: key, life: st };
        }

        const cd = (opts && opts.cooldownMs) || Runtime.config.bot_throw_drive_cooldown_ms || Runtime.config.bot_ai_hook_drive_cooldown_ms || 2500;
        const last = st.lastThrowAt || 0;
        if (last && now - last < cd) {
            Runtime.stats.bot_throw_gate_block_cooldown += 1;
            return { allow: false, reason: "cooldown", key: key, life: st, ageMs: now - last, needMs: cd };
        }

        Runtime.stats.bot_throw_gate_allowed += 1;
        return { allow: true, reason: "ok", key: key, life: st, rec: realRec, ageMs: age };
    } catch (e) {
        // 统一许可层异常时保守阻止Bot投掷，避免重新出现刚出生即投掷。
        Runtime.stats.bot_throw_gate_block_unknown_bot += 1;
        recordError("canBotThrowNow:" + reason, e);
        return { allow: false, reason: "gate_error:" + e, key: key, life: st };
    }
}

function markBotThrowCommitted(playerWeaponsPtr, botPtr, reason) {
    try {
        const st = updateBotLifeState(botPtr || ptr(0), playerWeaponsPtr || ptr(0), null, reason || "throw_committed");
        st.lastThrowAt = Date.now();
        st.firstThrowDone = true;
    } catch (e) {}
}

function logBotThrowGateBlocked(gate, reason, intervalMs) {
    try {
        if (!gate || gate.allow) return;
        const key = gate.key || "unknown";
        logOnce("bot_throw_gate_block:" + key + ":" + gate.reason + ":" + reason, "Bot统一投掷许可拦截", intervalMs || Runtime.config.bot_throw_state_log_interval_ms || 500, {
            reason: reason,
            blockReason: gate.reason,
            key: key,
            ageMs: gate.ageMs,
            targetAgeMs: gate.targetAgeMs,
            needMs: gate.needMs,
            attackTarget: gate.attackTarget,
            note: "v2.11.5：所有Bot投掷路径都必须先通过统一许可层"
        });
    } catch (e) {}
}


function driveBotThrowByStateMachine(botPtr, got, rec, info, name, methodInfo, smartEval) {
    Runtime.stats.bot_throw_sm_eval += 1;
    cleanupBotThrowStates("drive");

    const pwPtr = got.pwPtr;
    const key = getBotThrowStateKey(botPtr, pwPtr);
    const st = getBotThrowState(botPtr, pwPtr);
    const now = Date.now();
    const cd = Runtime.config.bot_ai_hook_drive_cooldown_ms || Runtime.config.bot_throw_drive_cooldown_ms || 1000;
    const selectDelay = Runtime.config.bot_throw_state_select_delay_ms || 0;
    const readyDelay = Runtime.config.bot_throw_state_ready_delay_ms || 0;
    const timeout = Runtime.config.bot_throw_state_timeout_ms || 1200;

    st.bot = ptrStr(botPtr);
    st.playerWeapons = ptrStr(pwPtr);
    st.attackTarget = info ? info.attackTarget : "0x0";
    st.grenadeWeapon = rec ? rec.grenadeWeapon : "0x0";
    st.lastReason = name;

    const unifiedGate = canBotThrowNow(botPtr, pwPtr, name + ".StateMachine.gate", info, rec, { cooldownMs: cd });
    if (!unifiedGate.allow) {
        logBotThrowGateBlocked(unifiedGate, name + ".StateMachine", Runtime.config.bot_throw_state_log_interval_ms || 500);
        return false;
    }

    if (!rec || !rec.grenadeWeapon || rec.grenadeWeapon === "0x0") {
        Runtime.stats.bot_throw_sm_invalid += 1;
        resetBotThrowState(st, "no_grenade");
        return false;
    }

    if (st.state !== "IDLE" && st.state !== "COOLDOWN" && st.startedAt && now - st.startedAt > timeout) {
        Runtime.stats.bot_throw_sm_timeout += 1;
        logBotThrowState(st, "timeout_reset", { reason: name, timeout_ms: timeout, age_ms: now - st.startedAt });
        resetBotThrowState(st, "timeout");
    }

    if (st.state === "COOLDOWN") {
        if (now < (st.cooldownUntil || 0)) {
            Runtime.stats.bot_throw_sm_cooldown += 1;
            Runtime.stats.bot_ai_hook_drive_skipped_cooldown += 1;
            return false;
        }
        resetBotThrowState(st, "cooldown_done");
    }

    // 兼容旧的 botAiLastDrive 冷却，避免状态机之外的路径刚投过又马上投。
    const last = Runtime.botAiLastDrive["sm:" + key] || 0;
    if (st.state === "IDLE" && now - last < cd) {
        Runtime.stats.bot_throw_sm_cooldown += 1;
        Runtime.stats.bot_ai_hook_drive_skipped_cooldown += 1;
        return false;
    }

    if (st.state === "IDLE") {
        st.state = "SELECTING";
        st.startedAt = now;
        st.nextAt = now + selectDelay;
        st.attempts += 1;
        Runtime.stats.bot_throw_sm_started += 1;
        logBotThrowState(st, "IDLE->SELECTING", { reason: name, next_delay_ms: selectDelay, smartEval: smartEval });
        return false;
    }

    if (st.state === "SELECTING") {
        if (now < st.nextAt) {
            Runtime.stats.bot_throw_sm_selecting += 1;
            return false;
        }
        try {
            const selected = maybeSelectBotGrenadeSlot(pwPtr, name + ".StateMachine.select", true);
            st.state = "READY";
            st.nextAt = now + readyDelay;
            Runtime.stats.bot_throw_sm_ready += 1;
            logBotThrowState(st, "SELECTING->READY", { reason: name, selected: selected, next_delay_ms: readyDelay });
            return false;
        } catch (e) {
            Runtime.stats.bot_throw_sm_select_fail += 1;
            logBotThrowState(st, "select_failed", { reason: name, error: "" + e });
            resetBotThrowState(st, "select_failed");
            return false;
        }
    }

    if (st.state === "READY") {
        if (now < st.nextAt) {
            Runtime.stats.bot_throw_sm_ready += 1;
            return false;
        }
        st.state = "THROWING";
        Runtime.stats.bot_throw_sm_throwing += 1;
        logBotThrowState(st, "READY->THROWING", { reason: name });

        const ok = driveBotThrowFromPlayerWeapons(pwPtr, name + ".StateMachine.throw", methodInfo || ptr(0), botPtr);
        Runtime.botAiLastDrive["sm:" + key] = Date.now();

        if (ok) {
            Runtime.stats.bot_throw_sm_success += 1;
            st.state = "COOLDOWN";
            st.cooldownUntil = Date.now() + cd;
            st.nextAt = st.cooldownUntil;
            logBotThrowState(st, "THROWING->COOLDOWN", { reason: name, cooldown_ms: cd, success: Runtime.stats.bot_throw_sm_success });
            return true;
        } else {
            Runtime.stats.bot_throw_sm_throw_fail += 1;
            logBotThrowState(st, "throw_failed_reset", { reason: name });
            resetBotThrowState(st, "throw_failed");
            return false;
        }
    }

    Runtime.stats.bot_throw_sm_invalid += 1;
    resetBotThrowState(st, "unknown_state:" + st.state);
    return false;
}


function driveBotThrowFromAIHook(botPtr, name, methodInfo, retval) {
    if (!Runtime.enabled || !Runtime.config.bot_ai_hook_drive_enabled || !Runtime.config.bot_grenade_mode_enabled) {
        Runtime.stats.bot_ai_hook_drive_skipped_disabled += 1;
        return false;
    }

    if (name.indexOf("Bot.CheckAttackTarget") >= 0 && !Runtime.config.bot_ai_checkattack_drive_enabled) {
        Runtime.stats.bot_ai_hook_drive_skipped_disabled += 1;
        return false;
    }
    if (name.indexOf("Bot.CameraRotation") >= 0 && !Runtime.config.bot_ai_camerarotation_drive_enabled) {
        Runtime.stats.bot_ai_hook_drive_skipped_disabled += 1;
        return false;
    }
    if (name.indexOf("Bot.TrySetAttackTarget") >= 0 && !Runtime.config.bot_ai_trysettarget_drive_enabled) {
        Runtime.stats.bot_ai_hook_drive_skipped_disabled += 1;
        return false;
    }

    Runtime.stats.bot_ai_hook_drive_attempts += 1;

    try {
        const info = readBotAIInfo(botPtr, name + ".hookDrive");
        if (Runtime.config.bot_ai_hook_drive_require_target && !info.hasAttackTarget) {
            Runtime.stats.bot_ai_hook_drive_skipped_no_target += 1;
            return false;
        }

        const got = getPlayerWeaponsFromBot(botPtr, name + ".hookDrive");
        if (!got.pwPtr || got.pwPtr.isNull() || !got.pwInfo || got.pwInfo.ownerIsLocal !== false) {
            Runtime.stats.bot_ai_hook_drive_skipped_no_pw += 1;
            return false;
        }

        const rec = getBotGrenadeRecord(got.pwPtr);
        if (!rec) {
            Runtime.stats.bot_ai_hook_drive_skipped_no_grenade += 1;
            logOnce("bot_ai_hook_no_grenade:" + name + ":" + ptrStr(got.pwPtr), "BotAI触发投掷跳过", Runtime.config.bot_ai_probe_log_interval_ms || 1000, {
                name: name,
                bot: ptrStr(botPtr),
                playerWeapons: ptrStr(got.pwPtr),
                attackTarget: info.attackTarget,
                note: "AI触发点命中，但该bot还没有缓存Grenade"
            });
            return false;
        }

        const smartEval = Runtime.config.smart_grenade_ai_enabled ? evaluateSmartGrenadeAI(botPtr, info, got, name, retval) : { allow: true, reason: "disabled" };
        if (!smartEval.allow) {
            logOnce("smart_grenade_skip:" + name + ":" + ptrStr(got.pwPtr) + ":" + smartEval.reason, "SmartGrenadeAI跳过", Runtime.config.bot_ai_probe_log_interval_ms || 1000, {
                name: name,
                bot: ptrStr(botPtr),
                playerWeapons: ptrStr(got.pwPtr),
                attackTarget: info.attackTarget,
                reason: smartEval.reason,
                eval: smartEval
            });
            return false;
        }

        const cd = Runtime.config.bot_ai_hook_drive_cooldown_ms || Runtime.config.bot_throw_drive_cooldown_ms || 1000;
        let ok = false;
        if (Runtime.config.bot_throw_state_machine_enabled) {
            ok = driveBotThrowByStateMachine(botPtr, got, rec, info, name, methodInfo || ptr(0), smartEval);
        } else {
            const key = "hook:" + ptrStr(got.pwPtr);
            const now = Date.now();
            const last = Runtime.botAiLastDrive[key] || 0;
            if (now - last < cd) {
                Runtime.stats.bot_ai_hook_drive_skipped_cooldown += 1;
                return false;
            }
            Runtime.botAiLastDrive[key] = now;
            ok = driveBotThrowFromPlayerWeapons(got.pwPtr, name + ".HookDrive", methodInfo || ptr(0));
        }

        if (ok) {
            Runtime.stats.bot_ai_hook_drive_success += 1;
            if (name.indexOf("Bot.CheckAttackTarget") >= 0) Runtime.stats.bot_ai_checkattack_drive_success += 1;
            if (name.indexOf("Bot.CameraRotation") >= 0) Runtime.stats.bot_ai_camerarotation_drive_success += 1;
            if (name.indexOf("Bot.TrySetAttackTarget") >= 0) Runtime.stats.bot_ai_trysettarget_drive_success += 1;
            log("BotAI触发投掷成功", {
                name: name,
                bot: ptrStr(botPtr),
                playerWeapons: ptrStr(got.pwPtr),
                attackTarget: info.attackTarget,
                hasAttackTarget: info.hasAttackTarget,
                grenadeWeapon: rec.grenadeWeapon,
                cooldown_ms: cd,
                success: Runtime.stats.bot_ai_hook_drive_success,
                smartEval: smartEval,
                stateMachine: Runtime.config.bot_throw_state_machine_enabled,
                note: "v2.12终版：已删除旧重定向/手雷模式纠正/全局选雷/GetValidSlot强制/发枪拦截，只保留稳定主路径"
            });
        }
        return ok;
    } catch (e) {
        Runtime.stats.bot_ai_errors += 1;
        recordError("driveBotThrowFromAIHook:" + name, e);
        return false;
    }
}


function installBotAIProbeControls() {
    // v2.12.1：UpdateAction入口已删除，稳定入口使用CheckAttackTarget/CameraRotation。

    function hookBotAI(name, rva, statName, hasTargetArg) {
        try {
            addHook(name, rva, {
                onEnter(args) {
                    Runtime.stats.hook_hits += 1;
                    Runtime.stats[statName] += 1;
                    Runtime.stats.last_hook = name;
                    this.botPtr = args[0];
                    this.target = hasTargetArg ? args[1] : ptr(0);
                    this.methodInfo = hasTargetArg ? args[2] : args[1];
                    logBotAIProbe(name + ".onEnter", args[0], hasTargetArg ? { argTarget: ptrStr(args[1]) } : {});
                },
                onLeave(retval) {
                    let rv = null;
                    try { rv = retval ? retval.toString() : null; } catch (e) {}
                    if (Runtime.enabled && Runtime.config.bot_ai_probe_enabled) {
                        logBotAIProbe(name + ".onLeave", this.botPtr, { argTarget: ptrStr(this.target || ptr(0)), retval: rv });
                    }
                    if (Runtime.enabled && Runtime.config.bot_ai_hook_drive_enabled) {
                        if (name === "Bot.CheckAttackTarget" || name === "Bot.CameraRotation" || name === "Bot.TrySetAttackTarget") {
                            driveBotThrowFromAIHook(this.botPtr, name + ".onLeave", this.methodInfo || ptr(0), retval);
                        }
                    }
                }
            });
            log("Hook 已安装", { name: name, address: addrOf(rva).toString(), mode: "BotAI Probe" });
        } catch (e) {
            Runtime.stats.bot_ai_errors += 1;
            recordError("installBotAIProbeControls:" + name, e);
        }
    }

    hookBotAI("Bot.CheckAttackTarget", RVA.Bot_CheckAttackTarget, "bot_ai_checkattack_hits", false);
    hookBotAI("Bot.CheckHitBox", RVA.Bot_CheckHitBox, "bot_ai_checkhitbox_hits", true);
    hookBotAI("Bot.FindAttackTarget", RVA.Bot_FindAttackTarget, "bot_ai_findtarget_hits", false);
    hookBotAI("Bot.TrySetAttackTarget", RVA.Bot_TrySetAttackTarget, "bot_ai_trysettarget_hits", true);
    hookBotAI("Bot.AddSelectWpnAction", RVA.Bot_AddSelectWpnAction, "bot_ai_addselect_hits", true);
    hookBotAI("Bot.CameraRotation", RVA.Bot_CameraRotation, "bot_ai_camerarotation_hits", false);
}


function installBotThrowDriveControls() {
    try {
        const useAddr = addrOf(RVA.Bot_UseWeapon);
        Runtime.natives.Bot_UseWeapon_Original = new NativeFunction(useAddr, "void", ["pointer", "pointer"], CALL_CONV);
        const replacement = new NativeCallback(function(botPtr, methodInfo) {
            Runtime.stats.bot_useweapon_hits += 1;
            Runtime.stats.last_hook = "Bot.UseWeapon";
            try {
                if (isBotThrowDriveActive() && Runtime.config.bot_throw_drive_useweapon_enabled) {
                    const got = getPlayerWeaponsFromBot(botPtr, "Bot.UseWeapon");
                    if (got.pwPtr && !got.pwPtr.isNull() && got.pwInfo && got.pwInfo.ownerIsLocal === false) {
                        const ok = driveBotThrowFromPlayerWeapons(got.pwPtr, "Bot.UseWeapon.replacement", methodInfo || ptr(0), botPtr);
                        if (ok && Runtime.config.bot_throw_drive_skip_original_useweapon_on_success) {
                            return;
                        }
                    } else {
                        Runtime.stats.bot_throw_drive_skipped_no_pw += 1;
                    }
                }
                Runtime.stats.bot_throw_drive_original_useweapon += 1;
                Runtime.natives.Bot_UseWeapon_Original(botPtr, methodInfo);
            } catch (e) {
                Runtime.stats.bot_throw_drive_errors += 1;
                recordError("Bot.UseWeapon.replacement", e);
                try { Runtime.natives.Bot_UseWeapon_Original(botPtr, methodInfo); } catch (e2) { recordError("Bot.UseWeapon.original_after_error", e2); }
            }
        }, "void", ["pointer", "pointer"], CALL_CONV);
        Interceptor.replace(useAddr, replacement);
        Runtime.replacements.push({ name: "Bot.UseWeapon", address: useAddr, replacement: replacement });
        log("Replace 已安装", { name: "Bot.UseWeapon", address: useAddr.toString(), mode: "Bot投掷驱动: 调用WPN_Throw.Throw" });
    } catch (e) {
        recordError("installBotThrowDriveControls.Bot.UseWeapon", e);
    }
}


function installBotGrenadeRecordControls() {
    // Bot.SelectWeapon 全局强制slot=3方案已删除；终版只在状态机投掷阶段临时Select(3)。

    // GameManager.GiveWeapon：终版只观察并记录bot的Grenade，不再拦截非Grenade发枪。
    try {
        const giveAddr = addrOf(RVA.GameManager_GiveWeapon);
        Runtime.natives.GameManager_GiveWeapon_Original = new NativeFunction(giveAddr, "pointer", ["pointer", "int", "bool", "bool", "pointer"], CALL_CONV);
        const giveReplacement = new NativeCallback(function(playerPtr, weaponIndex, autoGiveUp, autoSelect, methodInfo) {
            Runtime.stats.vg_giveweapon_hits += 1;
            Runtime.stats.last_hook = "GameManager.GiveWeapon";
            try {
                if (isBotGrenadeModeActive() && Runtime.config.virtual_grenade_giveweapon_enabled) {
                    setupNatives();
                    const pw = Runtime.natives.Player_get_wpns(playerPtr, ptr(0));
                    const pwInfo = (!pw || pw.isNull()) ? null : readPlayerWeaponsInfo(pw);
                    const isBotPlayer = pwInfo && pwInfo.ownerIsLocal === false;
                    if (isBotPlayer) {
                        Runtime.stats.vg_giveweapon_bot_hits += 1;
                        if (Runtime.config.bot_throw_respawn_reset_on_giveweapon) {
                            resetBotLifeState(pw, ptr(0), "GameManager.GiveWeapon.bot", false);
                        }
                        const previewWeapon = Runtime.natives.GameManager_GetWeapon_Original(weaponIndex, ptr(0));
                        const previewInfo = readWeaponInfo(previewWeapon);
                        const previewSlot = getWeaponDataSlot(previewInfo);
                        if (botSoftLockAllowedClass(previewInfo.wpnClass)) {
                            rememberGrenadeWeaponIndex(weaponIndex, previewInfo, "GameManager.GiveWeapon.preview");
                        }
                        if (!botSoftLockAllowedClass(previewInfo.wpnClass)) {
                            Runtime.stats.vg_giveweapon_observed_nongrenade += 1;
                            Runtime.stats.vg_giveweapon_preserved_nongrenade += 1;
                            logOnce("vg_give_non_grenade:" + weaponIndex + ":" + previewInfo.className, "BotGrenadeRecord.GiveWeapon", Runtime.config.virtual_grenade_log_interval_ms || 1000, {
                                player: ptrStr(playerPtr),
                                playerWeapons: ptrStr(pw),
                                weaponIndex: weaponIndex,
                                className: previewInfo.className,
                                wpnClass: previewInfo.wpnClass,
                                slot: previewSlot,
                                note: "v2.12终版：只观察并保留bot官方武器，不再拦截非Grenade发枪"
                            });
                        } else {
                            Runtime.stats.vg_giveweapon_allowed_grenade += 1;
                        }

                        const ret = Runtime.natives.GameManager_GiveWeapon_Original(playerPtr, weaponIndex, autoGiveUp, autoSelect, methodInfo);
                        const retInfo = readWeaponInfo(ret);
                        rememberGrenadeWeaponIndex(weaponIndex, retInfo, "GameManager.GiveWeapon.return");
                        recordBotGrenadeWeapon(pw, pwInfo, retInfo, "GameManager.GiveWeapon.return");
                        return ret;
                    }
                }
                return Runtime.natives.GameManager_GiveWeapon_Original(playerPtr, weaponIndex, autoGiveUp, autoSelect, methodInfo);
            } catch (e) {
                Runtime.stats.vg_giveweapon_errors += 1;
                recordError("GameManager.GiveWeapon.replacement", e);
                try { return Runtime.natives.GameManager_GiveWeapon_Original(playerPtr, weaponIndex, autoGiveUp, autoSelect, methodInfo); }
                catch (e2) { recordError("GameManager.GiveWeapon.original_after_error", e2); return ptr(0); }
            }
        }, "pointer", ["pointer", "int", "bool", "bool", "pointer"], CALL_CONV);
        Interceptor.replace(giveAddr, giveReplacement);
        Runtime.replacements.push({ name: "GameManager.GiveWeapon", address: giveAddr, replacement: giveReplacement });
        log("Replace 已安装", { name: "GameManager.GiveWeapon", address: giveAddr.toString(), mode: "BotGrenadeRecord: bot只允许Grenade" });
    } catch (e) {
        recordError("installBotGrenadeRecordControls.GameManager.GiveWeapon", e);
    }
}


function installHooks() {
    if (Runtime.initialized) return true;
    ensureModule(); setupNatives();

    hookThrowLike("WPN_Throw.Throw", RVA.WPN_Throw_Throw, "throw_hits", "lock_on_throw_enter", "lock_on_throw_leave");
    hookThrowLike("WPN_Throw.Deploy", RVA.WPN_Throw_Deploy, "deploy_hits", "lock_on_deploy", "lock_on_deploy");
    hookThrowLike("WPN_Throw.UnDeploy", RVA.WPN_Throw_UnDeploy, "unDeploy_hits", "lock_on_unDeploy", "lock_on_unDeploy");
    hookThrowLike("WPN_Throw.Init", RVA.WPN_Throw_Init, "init_hits", "lock_on_init", "lock_on_init");
    hookThrowLike("WPN_Throw.OnGenerateFromOwner", RVA.WPN_Throw_OnGenerateFromOwner, "generate_hits", "lock_on_generate_from_owner", "lock_on_generate_from_owner");
    hookThrowLike("WPN_Throw.OnAnimationEnd", RVA.WPN_Throw_OnAnimationEnd, "animationEnd_hits", "lock_on_animation_end", "lock_on_animation_end");
    hookThrowLike("WPN_Throw.OnFireAnimEnd", RVA.WPN_Throw_OnFireAnimEnd, "onFireAnimEnd_hits", "lock_on_animation_end", "lock_on_animation_end");
    installRemoveGuard();
    installBotGrenadeRecordControls();
    installBotThrowDriveControls();
    installVirtualBotControlControls();
    installBotAIProbeControls();
    installVirtualGrenadeObserverHooks();
    installBotAttackObserverHooks();

    addHook("WPN_Throw.<Throw>b__10_0", RVA.WPN_Throw_Throw_b__10_0, { onEnter(args) { Runtime.stats.hook_hits += 1; Runtime.stats.capture_hits += 1; Runtime.stats.last_hook = "WPN_Throw.<Throw>b__10_0"; if (!Runtime.enabled || !Runtime.config.runtime_tuner_enabled) return; try { const throwPtr = args[0]; const missile = args[1]; if (markGrenadeMissile(missile, throwPtr, "WPN_Throw.<Throw>b__10_0") && Runtime.config.tune_on_capture) tuneMissileOnlyFields(missile, "capture"); } catch (e) { recordError("WPN_Throw.<Throw>b__10_0", e); } } });
    addHook("CFAnimator.PlayWeaponAnimWithSameTag", RVA.CFAnimator_PlayWeaponAnimWithSameTag, { onEnter(args){ Runtime.stats.hook_hits += 1; Runtime.stats.playWeaponAnim_hits += 1; Runtime.stats.last_hook = "CFAnimator.PlayWeaponAnimWithSameTag"; if (Runtime.enabled && hasThrowAnimContext()) { try { setCFAnimatorSpeed(args[0], "CFAnimator.PlayWeaponAnimWithSameTag.onEnter"); } catch(e){ recordError("PlayWeaponAnimWithSameTag.onEnter", e); } } } });
    addHook("UnityEngine.Animator.PlayInFixedTime_279610832", RVA.UnityEngine_Animator_PlayInFixedTime_279610832, { onEnter(args){ Runtime.stats.hook_hits += 1; Runtime.stats.playInFixedTime_hits += 1; Runtime.stats.last_hook = "UnityEngine.Animator.PlayInFixedTime"; if (Runtime.enabled && hasThrowAnimContext()) { try { setAnimatorSpeed(args[0], Runtime.config.throw_anim_speed_value, "Animator.PlayInFixedTime.onEnter"); } catch(e){ recordError("PlayInFixedTime.onEnter", e); } } } });
    addHook("WPN_GRENADE.SetMissileData", RVA.WPN_GRENADE_SetMissileData, { onEnter(args){ Runtime.stats.hook_hits += 1; Runtime.stats.setMissileData_hits += 1; Runtime.stats.last_hook = "WPN_GRENADE.SetMissileData"; this.self = args[0]; }, onLeave(retval){ if (Runtime.enabled && Runtime.config.tune_on_set_missile_data) { try { tuneGrenadeRuntimeFields(this.self, "WPN_GRENADE.SetMissileData.onLeave"); } catch(e){ recordError("SetMissileData.onLeave", e); } } } });
    addHook("WPN_GRENADE.CreateExplosion", RVA.WPN_GRENADE_CreateExplosion, { onEnter(args){ Runtime.stats.hook_hits += 1; Runtime.stats.createExplosion_hits += 1; Runtime.stats.last_hook = "WPN_GRENADE.CreateExplosion"; if (Runtime.enabled && Runtime.config.runtime_tuner_enabled) { try { writeCreateExplosionArgs(this.context, "WPN_GRENADE.CreateExplosion.onEnter"); } catch(e){ recordError("CreateExplosion.onEnter", e); } } } });
    addHook("WPN_GRENADE.TryExplosion", RVA.WPN_GRENADE_TryExplosion, { onEnter(args){ Runtime.stats.hook_hits += 1; Runtime.stats.tryExplosion_hits += 1; Runtime.stats.last_hook = "WPN_GRENADE.TryExplosion"; this.pushedExplosionCtx = false; if (Runtime.enabled && Runtime.config.tune_on_try_explosion) { try { tuneGrenadeRuntimeFields(args[0], "WPN_GRENADE.TryExplosion.onEnter"); this.pushedExplosionCtx = pushExplosionContext(args[0], "WPN_GRENADE.TryExplosion"); } catch(e){ recordError("TryExplosion.onEnter", e); } } }, onLeave(retval){ if (this.pushedExplosionCtx) popExplosionContext(); } });
    addHook("WPN_GRENADE.Damage", RVA.WPN_GRENADE_Damage, { onEnter(args){ Runtime.stats.hook_hits += 1; Runtime.stats.damage_hits += 1; Runtime.stats.last_hook = "WPN_GRENADE.Damage"; if (Runtime.enabled && Runtime.config.tune_on_damage) { try { tuneGrenadeRuntimeFields(args[0], "WPN_GRENADE.Damage.onEnter"); } catch(e){ recordError("Damage.onEnter", e); } } } });
    addHook("WPN_GRENADE.OnLifeTimerEnd", RVA.WPN_GRENADE_OnLifeTimerEnd, { onEnter(args){ Runtime.stats.hook_hits += 1; Runtime.stats.lifeTimer_hits += 1; Runtime.stats.last_hook = "WPN_GRENADE.OnLifeTimerEnd"; this.pushedExplosionCtx = false; if (Runtime.enabled && Runtime.config.tune_on_life_timer_end) { try { tuneGrenadeRuntimeFields(args[0], "WPN_GRENADE.OnLifeTimerEnd.onEnter"); this.pushedExplosionCtx = pushExplosionContext(args[0], "WPN_GRENADE.OnLifeTimerEnd"); } catch(e){ recordError("LifeTimer.onEnter", e); } } }, onLeave(retval){ if (this.pushedExplosionCtx) popExplosionContext(); } });
    addHook("WPN_GRENADE.Work", RVA.WPN_GRENADE_Work, { onEnter(args){ Runtime.stats.hook_hits += 1; Runtime.stats.grenadeWork_hits += 1; Runtime.stats.last_hook = "WPN_GRENADE.Work"; if (Runtime.enabled && Runtime.config.tune_on_work) { try { tuneGrenadeRuntimeFields(args[0], "WPN_GRENADE.Work.onEnter", false); } catch(e){ recordError("GrenadeWork.onEnter", e); } } } });
    addHook("WPN_Missile.Work", RVA.WPN_Missile_Work, { onEnter(args){ Runtime.stats.hook_hits += 1; Runtime.stats.missileWork_hits += 1; Runtime.stats.last_hook = "WPN_Missile.Work"; if (Runtime.enabled && Runtime.config.tune_on_work) { try { tuneMissileOnlyFields(args[0], "WPN_Missile.Work.onEnter"); } catch(e){ recordError("MissileWork.onEnter", e); } } } });
    addHook("WPN_Missile.FixedUpdate", RVA.WPN_Missile_FixedUpdate, { onEnter(args){ Runtime.stats.hook_hits += 1; Runtime.stats.fixedUpdate_hits += 1; Runtime.stats.last_hook = "WPN_Missile.FixedUpdate"; if (Runtime.enabled && Runtime.config.tune_on_fixed_update) { try { tuneMissileOnlyFields(args[0], "WPN_Missile.FixedUpdate.onEnter"); } catch(e){ recordError("FixedUpdate.onEnter", e); } } } });
    addHook("WPN_Missile.SetOwner", RVA.WPN_Missile_SetOwner, { onEnter(args){ Runtime.stats.hook_hits += 1; Runtime.stats.setOwner_hits += 1; Runtime.stats.last_hook = "WPN_Missile.SetOwner"; this.self = args[0]; }, onLeave(retval){ if (Runtime.enabled && isTrackedMissile(this.self)) { try { tuneMissileOnlyFields(this.self, "WPN_Missile.SetOwner.onLeave"); } catch(e){ recordError("SetOwner.onLeave", e); } } } });
    addHook("WPN_Missile.SetWeaponData", RVA.WPN_Missile_SetWeaponData, { onEnter(args){ Runtime.stats.hook_hits += 1; Runtime.stats.setWeaponData_hits += 1; Runtime.stats.last_hook = "WPN_Missile.SetWeaponData"; if (Runtime.enabled && isTrackedMissile(args[0])) { try { tuneMissileOnlyFields(args[0], "WPN_Missile.SetWeaponData.onEnter"); } catch(e){ recordError("SetWeaponData.onEnter", e); } } } });
    addHook("WPN_Missile.Recycle", RVA.WPN_Missile_Recycle, { onEnter(args){ Runtime.stats.hook_hits += 1; Runtime.stats.recycle_hits += 1; Runtime.stats.last_hook = "WPN_Missile.Recycle"; try { const k = ptrStr(args[0]); if (Runtime.trackedMissiles[k]) { delete Runtime.trackedMissiles[k]; Runtime.stats.tracked_count = Object.keys(Runtime.trackedMissiles).length; log("手雷 missile 已回收，移除跟踪记录", { missile: k, tracked_count: Runtime.stats.tracked_count }); } } catch(e){ recordError("Recycle.onEnter", e); } } });

    addHook("PlayerWeapons.SetCurrentWeapon", RVA.PlayerWeapons_SetCurrentWeapon, {
    onEnter(args) {
        Runtime.stats.hook_hits += 1;
        Runtime.stats.setCurrent_hits += 1;
        Runtime.stats.observer_setCurrent_hits += 1;
        Runtime.stats.last_hook = "PlayerWeapons.SetCurrentWeapon";
        this.self = args[0];
        this.methodInfo = args[3] || ptr(0);
        let slot = null;
        try { slot = args[1].toInt32(); } catch(e) { slot = "read_failed"; }
        this.slot = slot;
        if (slot === 3 && args[2].isNull()) Runtime.stats.setCurrent_slot3_clear += 1;
        let weaponInfo = readWeaponInfo(args[2]);
        const pwInfo = readPlayerWeaponsInfo(args[0]);
        this.weaponInfo = weaponInfo;
        this.pwInfo = pwInfo;
        observeWeaponClass(weaponInfo);
        recordBotGrenadeWeapon(args[0], pwInfo, weaponInfo, "PlayerWeapons.SetCurrentWeapon.onEnter");
        if (!Runtime.enabled || !Runtime.config.observe_set_current_weapon) return;
        if (Runtime.config.virtual_grenade_observer_enabled) {
            logWeaponObserver("PlayerWeapons.SetCurrentWeapon.onEnter", {
                playerWeapons: pwInfo,
                slot: slot,
                weaponInfo: weaponInfo,
                slot3_clear_count: Runtime.stats.setCurrent_slot3_clear,
            }, false);
        } else {
            logOnce("SetCurrentWeapon", "观察：PlayerWeapons.SetCurrentWeapon", Runtime.config.log_interval_ms, { slot: slot, weapon: ptrStr(args[2]), slot3_clear_count: Runtime.stats.setCurrent_slot3_clear });
        }
    },
    onLeave(retval) {
        // v2.12终版：不再在SetCurrentWeapon.onLeave后自动纠正非手雷。
    }
});

    Runtime.initialized = true;
    log("全部 Hook/Replace 已安装", { hooks: Runtime.hooks.length, replacements: Runtime.replacements.length, config: Runtime.config });
    return true;
}

function cleanupHooks() {
    for (const item of Runtime.hooks) { try { if (item && item.handle && item.handle.detach) item.handle.detach(); } catch(e){ recordError("cleanupHook:" + (item ? item.name : "unknown"), e); } }
    Runtime.hooks = [];
    for (const item of Runtime.replacements) { try { if (item && item.address) Interceptor.revert(item.address); } catch(e){ recordError("cleanupReplace:" + (item ? item.name : "unknown"), e); } }
    Runtime.replacements = [];
    Runtime.initialized = false;
    try { Interceptor.flush(); } catch(e) {}
}
function resetVolatileRuntimeState(reason, options) {
    const keepKnownGrenadeIndexes = !!(options && options.keepKnownGrenadeIndexes);
    Runtime.generation += 1;
    clearPendingThrowReadyTimers();
    Runtime.protectedWeapons = {};
    Runtime.trackedMissiles = {};
    Runtime.explosionContexts = {};
    Runtime.throwAnimContexts = {};
    Runtime.touchedAnimators = {};
    Runtime.botGrenadeWeapons = {};
    Runtime.botGrenadeWeaponAliases = {};
    Runtime.botGrenadeWeaponIndex = {};
    if (!keepKnownGrenadeIndexes) {
        Runtime.knownGrenadeWeaponIndexes = {};
        Runtime.lastBotGrenadeWeaponIndex = -1;
    }
    Runtime.botGrenadeGiveLast = {};
    Runtime.forceThrowReadyWindows = {};
    Runtime.classCounts = {};
    Runtime.observerLast = {};
    Runtime.stats.protected_count = 0;
    Runtime.stats.tracked_count = 0;
    Runtime.stats.last_hook = "";
    log("运行状态已重置", { reason: reason, generation: Runtime.generation, keepKnownGrenadeIndexes: keepKnownGrenadeIndexes });
}
function resetRuntime(reason) { resetVolatileRuntimeState(reason); }
function recoverRuntimeAfterErrorThreshold(reason) { const count = Runtime.stats.error_count; resetVolatileRuntimeState("error_threshold:" + reason, { keepKnownGrenadeIndexes: true }); Runtime.stats.error_count = 0; Runtime.stats.last_error = ""; warn("错误过多，已清理本局运行缓存并继续保持功能开启", { reason: reason, error_count: count, enabled: Runtime.enabled }); }
function enableFeature(config) { setConfig(config); installHooks(); Runtime.enabled = true; Runtime.stats.error_count = 0; Runtime.stats.last_error = ""; resetRuntime("enable"); log("手雷模式v2.12.8 final-clean-ui版已开启", { config: Runtime.config }); return true; }
function disableFeature() { Runtime.enabled = false; resetRuntime("disable"); log("功能已关闭"); return true; }
function cleanupFeature() { Runtime.enabled = false; Runtime.stats.cleanup_count += 1; resetRuntime("cleanup"); cleanupHooks(); Runtime.moduleBase = ptr(0); log("cleanup 完成", { cleanup_count: Runtime.stats.cleanup_count }); return true; }
function setConfig(config) { try { if (!config) return true; for (const k in config) { if (Object.prototype.hasOwnProperty.call(DefaultConfig, k)) Runtime.config[k] = config[k]; } log("配置已更新", { config: Runtime.config }); return true; } catch(e){ recordError("setConfig", e); return false; } }
function getStatus() {
    cleanupProtectedWeapons("status"); cleanupTrackedMissiles("status");
    return {
        feature_id: FEATURE_ID, version: VERSION, enabled: Runtime.enabled, initialized: Runtime.initialized, generation: Runtime.generation, config: Runtime.config,
        hook_count: Runtime.hooks.length, replacement_count: Runtime.replacements.length,
        hook_hits: Runtime.stats.hook_hits,
        lock_attempts: Runtime.stats.lock_attempts, lock_writes: Runtime.stats.lock_writes, lock_skipped_same: Runtime.stats.lock_skipped_same, throw_ready_writes: Runtime.stats.throw_ready_writes, throw_ready_skipped: Runtime.stats.throw_ready_skipped,
        remove_hits: Runtime.stats.remove_hits, remove_blocked: Runtime.stats.remove_blocked, remove_allowed: Runtime.stats.remove_allowed,
        protected_count: Runtime.stats.protected_count,
        capture_hits: Runtime.stats.capture_hits, tracked_count: Runtime.stats.tracked_count, tracked_expired: Runtime.stats.tracked_expired,
        owner_local_pass: Runtime.stats.owner_local_pass, owner_local_fail: Runtime.stats.owner_local_fail, owner_unknown: Runtime.stats.owner_unknown,
        tune_attempts: Runtime.stats.tune_attempts, tune_applied: Runtime.stats.tune_applied, tune_skipped_not_tracked: Runtime.stats.tune_skipped_not_tracked, tune_skipped_owner: Runtime.stats.tune_skipped_owner,
        grenade_field_writes: Runtime.stats.grenade_field_writes, missile_speed_writes: Runtime.stats.missile_speed_writes,
        playWeaponAnim_hits: Runtime.stats.playWeaponAnim_hits, playInFixedTime_hits: Runtime.stats.playInFixedTime_hits, anim_speed_writes: Runtime.stats.anim_speed_writes, anim_speed_restores: Runtime.stats.anim_speed_restores, onFireAnimEnd_hits: Runtime.stats.onFireAnimEnd_hits, setMissileData_hits: Runtime.stats.setMissileData_hits, createExplosion_hits: Runtime.stats.createExplosion_hits, createExplosion_param_writes: Runtime.stats.createExplosion_param_writes, tryExplosion_hits: Runtime.stats.tryExplosion_hits, damage_hits: Runtime.stats.damage_hits, lifeTimer_hits: Runtime.stats.lifeTimer_hits,
        missileWork_hits: Runtime.stats.missileWork_hits, fixedUpdate_hits: Runtime.stats.fixedUpdate_hits, recycle_hits: Runtime.stats.recycle_hits,
        setCurrent_hits: Runtime.stats.setCurrent_hits, setCurrent_slot3_clear: Runtime.stats.setCurrent_slot3_clear,
        infinite_scope_local_skip: Runtime.stats.infinite_scope_local_skip, infinite_scope_all_apply: Runtime.stats.infinite_scope_all_apply, infinite_scope_local_apply: Runtime.stats.infinite_scope_local_apply,
        bot_throw_weapon_seen: Runtime.stats.bot_throw_weapon_seen, bot_throw_weapon_selected: Runtime.stats.bot_throw_weapon_selected, bot_throw_method_hits: Runtime.stats.bot_throw_method_hits, bot_missile_captured: Runtime.stats.bot_missile_captured, bot_remove_throw_hits: Runtime.stats.bot_remove_throw_hits, bot_summary_count: Runtime.stats.bot_summary_count,
        bot_attack_summary_count: Runtime.stats.bot_attack_summary_count, gun_bot_control_hits: Runtime.stats.gun_bot_control_hits, gun_sniper_bot_control_hits: Runtime.stats.gun_sniper_bot_control_hits, gun_shoot_hits: Runtime.stats.gun_shoot_hits, gun_shoot_botlike_hits: Runtime.stats.gun_shoot_botlike_hits, gun_generate_bullet_hits: Runtime.stats.gun_generate_bullet_hits, gun_generate_bullet_botlike_hits: Runtime.stats.gun_generate_bullet_botlike_hits, rpg_bot_control_hits: Runtime.stats.rpg_bot_control_hits, rpg_fire_hits: Runtime.stats.rpg_fire_hits, rpg_fire_botlike_hits: Runtime.stats.rpg_fire_botlike_hits, rpg_on_fire_pressed_hits: Runtime.stats.rpg_on_fire_pressed_hits, bot_attack_entry_hits: Runtime.stats.bot_attack_entry_hits,
        bot_useweapon_hits: Runtime.stats.bot_useweapon_hits, bot_throw_drive_attempts: Runtime.stats.bot_throw_drive_attempts, bot_throw_drive_success: Runtime.stats.bot_throw_drive_success, bot_throw_drive_original_useweapon: Runtime.stats.bot_throw_drive_original_useweapon, bot_throw_drive_skipped_disabled: Runtime.stats.bot_throw_drive_skipped_disabled, bot_throw_drive_skipped_no_pw: Runtime.stats.bot_throw_drive_skipped_no_pw, bot_throw_drive_skipped_no_grenade: Runtime.stats.bot_throw_drive_skipped_no_grenade, bot_throw_drive_skipped_cooldown: Runtime.stats.bot_throw_drive_skipped_cooldown, bot_throw_drive_skipped_not_bot: Runtime.stats.bot_throw_drive_skipped_not_bot, bot_throw_drive_force_ready_writes: Runtime.stats.bot_throw_drive_force_ready_writes, bot_throw_drive_errors: Runtime.stats.bot_throw_drive_errors,
        bot_grenade_known_index_hits: Runtime.stats.bot_grenade_known_index_hits, bot_grenade_active_give_attempts: Runtime.stats.bot_grenade_active_give_attempts, bot_grenade_active_give_success: Runtime.stats.bot_grenade_active_give_success, bot_grenade_active_give_failed: Runtime.stats.bot_grenade_active_give_failed, bot_grenade_active_give_cooldown: Runtime.stats.bot_grenade_active_give_cooldown,
        bot_grenade_reacquire_attempts: Runtime.stats.bot_grenade_reacquire_attempts, bot_grenade_reacquire_success: Runtime.stats.bot_grenade_reacquire_success, bot_grenade_reacquire_failed: Runtime.stats.bot_grenade_reacquire_failed,
        vbc_gun_botcontrol_hits: Runtime.stats.vbc_gun_botcontrol_hits, vbc_sniper_botcontrol_hits: Runtime.stats.vbc_sniper_botcontrol_hits, vbc_rpg_botcontrol_hits: Runtime.stats.vbc_rpg_botcontrol_hits, vbc_attempts: Runtime.stats.vbc_attempts, vbc_success: Runtime.stats.vbc_success, vbc_original_calls: Runtime.stats.vbc_original_calls, vbc_suppressed_original_calls: Runtime.stats.vbc_suppressed_original_calls, vbc_suppress_no_grenade: Runtime.stats.vbc_suppress_no_grenade, vbc_suppress_cooldown: Runtime.stats.vbc_suppress_cooldown, vbc_skipped_disabled: Runtime.stats.vbc_skipped_disabled, vbc_skipped_no_bot: Runtime.stats.vbc_skipped_no_bot, vbc_skipped_no_pw: Runtime.stats.vbc_skipped_no_pw, vbc_skipped_no_grenade: Runtime.stats.vbc_skipped_no_grenade, vbc_skipped_cooldown: Runtime.stats.vbc_skipped_cooldown, vbc_errors: Runtime.stats.vbc_errors,
        bot_ai_hook_drive_attempts: Runtime.stats.bot_ai_hook_drive_attempts, bot_ai_hook_drive_success: Runtime.stats.bot_ai_hook_drive_success, bot_ai_checkattack_drive_success: Runtime.stats.bot_ai_checkattack_drive_success, bot_ai_camerarotation_drive_success: Runtime.stats.bot_ai_camerarotation_drive_success, bot_ai_trysettarget_drive_success: Runtime.stats.bot_ai_trysettarget_drive_success, bot_ai_hook_drive_skipped_disabled: Runtime.stats.bot_ai_hook_drive_skipped_disabled, bot_ai_hook_drive_skipped_no_target: Runtime.stats.bot_ai_hook_drive_skipped_no_target, bot_ai_hook_drive_skipped_no_pw: Runtime.stats.bot_ai_hook_drive_skipped_no_pw, bot_ai_hook_drive_skipped_no_grenade: Runtime.stats.bot_ai_hook_drive_skipped_no_grenade, bot_ai_hook_drive_skipped_cooldown: Runtime.stats.bot_ai_hook_drive_skipped_cooldown,
        bot_throw_sm_eval: Runtime.stats.bot_throw_sm_eval, bot_throw_sm_started: Runtime.stats.bot_throw_sm_started, bot_throw_sm_ready: Runtime.stats.bot_throw_sm_ready, bot_throw_sm_success: Runtime.stats.bot_throw_sm_success, bot_throw_sm_cooldown: Runtime.stats.bot_throw_sm_cooldown, bot_throw_sm_timeout: Runtime.stats.bot_throw_sm_timeout, bot_throw_sm_select_fail: Runtime.stats.bot_throw_sm_select_fail, bot_throw_sm_throw_fail: Runtime.stats.bot_throw_sm_throw_fail, bot_throw_spawn_first_seen: Runtime.stats.bot_throw_spawn_first_seen, bot_throw_spawn_grace_skipped: Runtime.stats.bot_throw_spawn_grace_skipped, bot_throw_target_changed: Runtime.stats.bot_throw_target_changed, bot_throw_target_stable_skipped: Runtime.stats.bot_throw_target_stable_skipped, bot_life_first_seen: Runtime.stats.bot_life_first_seen, bot_throw_gate_eval: Runtime.stats.bot_throw_gate_eval, bot_throw_gate_allowed: Runtime.stats.bot_throw_gate_allowed, bot_throw_gate_block_spawn: Runtime.stats.bot_throw_gate_block_spawn, bot_throw_gate_block_first_extra: Runtime.stats.bot_throw_gate_block_first_extra, bot_throw_gate_block_target_unstable: Runtime.stats.bot_throw_gate_block_target_unstable, bot_throw_gate_block_cooldown: Runtime.stats.bot_throw_gate_block_cooldown, bot_throw_gate_block_no_grenade: Runtime.stats.bot_throw_gate_block_no_grenade, bot_throw_gate_block_unknown_bot: Runtime.stats.bot_throw_gate_block_unknown_bot, bot_life_respawn_reset: Runtime.stats.bot_life_respawn_reset, bot_life_reset_removeall: Runtime.stats.bot_life_reset_removeall, bot_life_reset_giveweapon: Runtime.stats.bot_life_reset_giveweapon, bot_life_reset_grenade_change: Runtime.stats.bot_life_reset_grenade_change, bot_life_reset_cooldown_skip: Runtime.stats.bot_life_reset_cooldown_skip, botThrowStates: Runtime.botThrowStates, botLifeStates: Runtime.botLifeStates,
        botGrenadeWeapons: Runtime.botGrenadeWeapons, botGrenadeWeaponIndex: Runtime.botGrenadeWeaponIndex, knownGrenadeWeaponIndexes: Runtime.knownGrenadeWeaponIndexes, lastBotGrenadeWeaponIndex: Runtime.lastBotGrenadeWeaponIndex,
        skipped_invalid: Runtime.stats.skipped_invalid, error_count: Runtime.stats.error_count, last_error: Runtime.stats.last_error, last_hook: Runtime.stats.last_hook,
        trackedMissiles: Runtime.trackedMissiles, protectedWeapons: Runtime.protectedWeapons,
        cleanup_count: Runtime.stats.cleanup_count
    };
}

rpc.exports = { enable(config){ return enableFeature(config); }, disable(){ return disableFeature(); }, status(){ return getStatus(); }, cleanup(){ return cleanupFeature(); }, setConfig(config){ return setConfig(config); }, set_config(config){ return setConfig(config); }, debugDump(){ return getStatus(); }, debug_dump(){ return getStatus(); } };
log("锁999+保护武器+手雷伤害范围速度+连投就绪/动作加速脚本已加载", { version: VERSION });
