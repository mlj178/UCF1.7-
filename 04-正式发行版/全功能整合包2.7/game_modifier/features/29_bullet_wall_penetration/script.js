// ============================================================
// AAAAA-bullet_wall_penetration_min.js
//
// feature_id: "bullet_wall_penetration"
// 卡片名：子弹穿墙/弹体穿墙
//
// 功能目标
//   A) 子弹穿墙（原逻辑，本次未改）
//      仿原版穿透版。子弹可以穿墙命中墙后的 HitBox，但仍让 WPN_Gun.Damage 的
//      原逻辑调用 WeaponLogic.CheckWall，使用 WeaponData_Gun.wallShotDamageRatio
//      做伤害衰减，并保留 wallThrough 命中/击杀标记。
//
//   B) 弹体穿墙（本次新增）
//      本地玩家发射的投射物（手雷 / 榴弹枪 / RPG / 奥术手雷 / 地狱终结者火球）
//      撞到"墙面"时不再被墙挡住，直接穿过去。范围与 40-开火直伤/弹体追踪 的
//      "5 种投射物"一致（它们共用 WPN_Missile / WPN_GRENADE 这一套基类）。
//
// ------------------------------------------------------------------
// A. 子弹穿墙实现原理（保持原样）
// ------------------------------------------------------------------
//   1. Hook WPN_Gun.Damage，不替换原伤害流程。
//   2. 仅当本地玩家武器进入 Damage 时，临时把 LayerConstant.LM_GunShoot
//      改成 HitBox-only mask，让原 RaycastAll 可拿到墙后的 hitbox。
//   3. Damage 返回后立刻恢复 LM_GunShoot。
//   4. WeaponLogic.CheckWall 保持原样，只记录状态；墙体判定、伤害衰减、
//      wallThrough 标记继续由游戏原版代码执行。
//
// ------------------------------------------------------------------
// B. 弹体穿墙实现原理（本次新增，反汇编结论见下）
// ------------------------------------------------------------------
//   IDA 0x10B5D0F0（WPN_GRENADE.OnCollisionEnter）尾部实测机器码：
//       mov edi,[esi+44h] / test edi,edi / jz ret
//       call Rigidbody.get_velocity ...
//       call Rigidbody.set_velocity          ; 原版自己改速度（弹体靠物理撞墙）
//       cmp byte [esi+74h],0                 ; expWhenTouchSth
//       jz  ret
//       push [eax+118h] / push esi / call eax ; vtable slot11 = TryExplosion
//   结论：**撞墙就会走 TryExplosion**（"撞墙即爆"的真凶），所以只"放开门掩码"
//   是不够的，必须在这一次碰撞里把爆炸和物理阻挡一起摘掉。
//
//   因此弹体穿墙分四步（全部在 OnCollisionEnter 的 onEnter/onLeave 窗口内）：
//     1) 判定：本地玩家发射（WPN_Missile.owner + Player.get_isMyPlayer）
//        + 撞的是墙面（collider 所在 GameObject 的 layer == LayerConstant.Environment
//          且接触法线偏水平 |normal.y| < projectileWallMaxNormalY）。
//        地板/天花板/斜坡（法线朝上下）不处理 -> 滚雷、落地行为保持原版。
//     2) 抑制爆炸：onEnter 里把 WPN_GRENADE.expWhenTouchSth(+0x74) 临时写 0，
//        onLeave 里按保存的原始字节原样写回。原版本体在这次调用里读到的就是 0，
//        于是 vtable._11_TryExplosion 不会被调用（不替换函数、不动控制流）。
//     3) 摘掉物理阻挡：Physics.IgnoreCollision(弹体自身 collider, 墙 collider, true)。
//        弹体的 collider 用 Physics.OverlapSphere(接触点附近) + Collider.attachedRigidbody
//        == 弹体 Rigidbody 反查得到（不依赖泛型 GetComponent<Collider>，它在本
//        二进制里没有独立函数体）。
//     4) 速度写回：碰撞已经被物理求解器削弱/清零，onLeave 里把碰撞前缓存的速度
//        写回 Rigidbody.set_velocity；缓存来自 WPN_Missile.FixedUpdate（物理步开始，
//        一定早于碰撞回调）。拿不到缓存时退化用 Collision.relativeVelocity（+0x14），
//        再退化用 transform.forward * WPN_Missile.shootSpeed(+0x4C)。
//
//   **忽略是"带窗口"的**（关键安全设计）：
//     永久 IgnoreCollision 在"整张关卡是同一个 MeshCollider"的地图里会把地板
//     一起忽略（手雷会掉出地图）。所以：
//       经过 projectileIgnoreMinMs（默认 80ms）之后，每一物理步检查
//         Physics.OverlapSphere(弹体中心, 0.08, Environment层掩码)
//         └─ 过滤掉 attachedRigidbody == 弹体 Rigidbody 的自身 collider
//       —— 附近还压着"不是自己"的关卡几何就继续忽略，一旦中心离开墙体就立刻
//       IgnoreCollision(..., false) 还原；
//       同时有 projectileIgnoreMaxMs（默认 1200ms）硬上限兜底。
//     用 OverlapSphere 而不是 Physics.CheckSphere：CheckSphere 只看 layerMask，
//     会把弹体自己的 collider 也算进去（弹体多半就在 layer 0=Environment），
//     于是永远返回 true、永远不还原。
//     薄墙（<1m）通常 1~2 个物理步就穿过，还原窗口只有几十毫秒。
//
//   **只处理 Environment 层**：AirWall（layer 2）不穿，避免弹体飞出地图边界。
//   只处理本地玩家弹体：人机/远程玩家的弹体保持原版（撞墙即爆）。
//
// RVA / 字段来源：dump.cs + IDA 汇编交叉验证
//   Weapon_get_isMyWeapon:                 0x00B6E1D0
//   WPN_Gun_Damage:                        0x00B613D0
//   WeaponLogic_CheckWall:                 0x00B78F80
//   LayerConstant_cctor:                   0x00AE7CD0
//   LayerConstant_TypeInfo:                0x0E2BE3C
//   LayerConstant.Environment:             0x0 = 0（layer 0，关卡几何）
//   LayerConstant.AirWall:                 0x4 = 2
//   LayerConstant.HitBox:                  0x8 = 3
//   LayerConstant.LM_GunShoot:             0x38
//   Weapon.data:                           0x68
//   WPN_Gun.realData:                      0xEC
//   WeaponData_Gun.wallShotDamageRatio:    0x158
//
//   ---- 弹体穿墙（本次新增）----
//   WPN_Missile_SetWeaponData:             0x00B663C0   对象池复用点：清旧状态
//   WPN_Missile_FixedUpdate:               0x00B660C0   物理步：缓存速度/位置 + 处理还原窗口
//   WPN_Missile_OnCollisionEnter:          0x00B66100   基类碰撞（无爆炸字段）
//   WPN_GRENADE_OnCollisionEnter:          0x00B5D0F0   手雷/榴弹/RPG/技能弹的碰撞 + 撞墙爆炸
//   WPN_Missile_Recycle:                   0x00B66240   回池：清状态 + 立刻还原忽略
//   Player_get_isMyPlayer:                 0x00B55FD0
//   WPN_Missile.owner:                     0x30
//   WPN_Missile.rigidBody:                 0x44
//   WPN_Missile.shootSpeed:                0x4C
//   WPN_GRENADE.expWhenTouchSth:           0x74
//   UnityEngine.Collision.m_Collider:      0x24
//   UnityEngine.ContactPoint.m_Normal:     0x0C（数组元素内偏移）
//   Il2CppArray.max_length / items:        0x0C / 0x10
//   UnityEngine.Component.get_transform:   0x0032CF40
//   UnityEngine.Component.get_gameObject:  0x0032CEB0
//   Transform.get_position_Injected:       0x003F4280
//   GameObject.get_layer:                  0x00331FB0
//   Collision.get_contacts:                0x00AB8710
//   Collider.get_attachedRigidbody:        0x00AB85B0
//   Physics.IgnoreCollision:               0x00AB9A00
//   Physics.OverlapSphere:                 0x00AB9F00
//   Rigidbody.get_velocity (Injected):     0x00ABBDC0
//   Rigidbody.set_velocity:                 0x00ABC060
// ============================================================

(function () {
    'use strict';

    var MODULE_NAME = 'GameAssembly.dll';
    var CALL_CONV = 'mscdecl';

    var RVA = {
        Weapon_get_isMyWeapon: 0x00B6E1D0,
        WPN_Gun_Damage: 0x00B613D0,
        WeaponLogic_CheckWall: 0x00B78F80,
        LayerConstant_cctor: 0x00AE7CD0,
        LayerConstant_TypeInfo: 0x0E2BE3C,

        // ---- 弹体穿墙（投射物）----
        WPN_Missile_SetWeaponData: 0x00B663C0,
        WPN_Missile_FixedUpdate: 0x00B660C0,
        WPN_Missile_OnCollisionEnter: 0x00B66100,
        WPN_GRENADE_OnCollisionEnter: 0x00B5D0F0,
        WPN_Missile_Recycle: 0x00B66240,
        Player_get_isMyPlayer: 0x00B55FD0,
        Component_get_transform: 0x0032CF40,
        Component_get_gameObject: 0x0032CEB0,
        Transform_get_position_Injected: 0x003F4280,
        GameObject_get_layer: 0x00331FB0,
        Collision_get_contacts: 0x00AB8710,
        Collider_get_attachedRigidbody: 0x00AB85B0,
        Physics_IgnoreCollision: 0x00AB9A00,
        Physics_OverlapSphere: 0x00AB9F00,
        Physics_Raycast: 0x00ABAC10,
        Object_FindObjectFromInstanceID: 0x004E9570,
        Object_get_name: 0x004EA1B0,
        LayerMask_LayerToName: 0x00336790,
        Rigidbody_get_velocity_Injected: 0x00ABBDC0,
        Rigidbody_set_velocity: 0x00ABC060,
        Rigidbody_set_detectCollisions: 0x00ABBF00
    };

    var OFF = {
        Weapon_data: 0x68,
        WPN_Gun_realData: 0xEC,
        WeaponData_Gun_wallShotDamageRatio: 0x158,
        Klass_staticFields: 0x5C,
        LayerConstant_Environment: 0x00,
        LayerConstant_AirWall: 0x04,
        LayerConstant_HitBox: 0x08,
        LayerConstant_LM_GunShoot: 0x38,

        // ---- 弹体穿墙（投射物）----
        Missile_owner: 0x30,
        Missile_rigidBody: 0x44,
        Missile_shootSpeed: 0x4C,
        WPN_GRENADE_expWhenTouchSth: 0x74,
        Collision_collider: 0x24,
        Collision_relativeVelocity: 0x14,
        ContactPoint_normal: 0x0C,
        RaycastHit_point: 0x00,
        RaycastHit_normal: 0x0C,
        RaycastHit_distance: 0x1C,
        RaycastHit_collider: 0x28,
        Il2CppArray_length: 0x0C,
        Il2CppArray_items: 0x10
    };

    var Runtime = {
        feature_id: "bullet_wall_penetration",
        enabled: false,
        initialized: false,
        module: null,
        base: ptr(0),
        hooks: [],
        damageDepth: 0,
        activeDamageWeapon: ptr(0),
        layerInitialized: false,
        currentPatch: null,
        // 弹体状态：key = WPN_Missile 指针。对象池会复用指针，SetWeaponData/Recycle 都要清。
        missiles: {},
        heartbeat: null,
        cache: {
            floatBuf: null,
            vecBuf: null,
            hitBuf: null
        },
        config: {
            forceHitboxOnlyDuringLocalDamage: true,
            logEveryDamageHits: 25,
            projectileWallPenetration: true,
            // 可穿透层掩码。默认 = 全部 32 层，**只排除角色/命中盒相关层**：
            //   bit3  HitBox / PlayerViewModel
            //   bit7  Entity
            //   bit8  DeadEntity / CharacterModel
            //   bit10 GhostEntity
            // => 0xFFFFFA77。
            // 为什么要这么宽：实测这张图的物理阻挡不止落在 Environment(0) 上
            // （layer 2 上大量命中），只认 layer 0 会导致"怎么都不穿"。
            // 地板不会被误伤：主动探路只对"法线偏水平"的面生效，地板法线朝上下会被拒。
            // 要收窄就改这个掩码（例如只留 0 和 2 => 5）。
            projectilePenetrableLayers: 0xFFFFFA77,
            // 兼容旧键：true 时额外把 AirWall 位打开
            projectilePenetrateAirWall: false,
            projectileWallMaxNormalY: 0.6,
            projectileProbeLookahead: 3.5,   // 主动探路距离(m)：这个距离内发现"墙面"就提前关碰撞
            projectileGhostExtra: 0.8,       // 需要再往前走多少米才算穿过这面墙

            projectileIgnoreMinMs: 80,
            projectileIgnoreMaxMs: 1200
        },
        stats: {
            damageHits: 0,
            localDamageHits: 0,
            checkWallHits: 0,
            layerPatchCount: 0,
            layerRestoreCount: 0,
            skippedRemoteWeapon: 0,
            skippedInvalid: 0,
            errorCount: 0,
            cleanupCount: 0,
            lastWallRatio: -1.0,
            lastCheckWallResult: null,
            lastHitBoxLayer: -1,
            lastOriginalGunShootMask: 0,
            lastPatchedGunShootMask: 0,
            lastError: "",
            lastPatchReason: "",
            lastRestoreReason: "",

            // ---- 弹体穿墙 ----
            projectileCollisions: 0,     // 进入弹体碰撞回调整体次数（含非本地）
            projectileLocalCollisions: 0,// 本地玩家弹体的碰撞次数
            projectileWallHits: 0,       // 判定为"墙面"的次数
            projectilePenetrated: 0,     // 真正执行"忽略墙 + 写回速度"的次数
            projectileTriedExplosion: 0, // 原版本来会撞墙爆炸（expWhenTouchSth=1）的次数
            projectileIgnoredPairs: 0,
            projectileReleasedPairs: 0,
            projectileOverlapMiss: 0,    // 没反查到弹体自身 collider 的次数
            projectileVelFallback: 0,    // 用 relativeVelocity / forward 兜底的次数
            projectileSweepRemoved: 0,   // 心跳清理掉的僵尸记录
            projectileRayHits: 0,         // 主动探路射线命中总次数
            projectileRayWallHits: 0,     // 其中判定为"墙面"的次数
            projectileRayFloorLikes: 0,   // 其中判定为"地板/斜面"的次数
            projectileGhostStarts: 0,     // 主动穿墙开始次数
            projectileGhostEnds: 0,       // 主动穿墙结束次数
            projectileGhostForceEnds: 0,  // 因硬上限强制的结束次数
            projectileGhostRestores: 0,   // 回池/关闭时被动还原 detectCollisions 的次数
            projectileGhostFail: 0,       // set_detectCollisions 调用失败次数
            projectileProactiveIgnores: 0,// 主动阶段"提前忽略这一面墙"的次数
            projectileFixedSeen: 0,       // FixedUpdate 里见过的弹体总数（含人机的）
            projectileFixedLocal: 0,      // 其中判定为本地的
            projectileFixedNotMine: 0,    // 判定为不是自己的
            projectileRayOtherLayers: 0,  // 探路打到了"不可穿透层"的次数（层判定不对时看这个）
            lastProbeLayer: -1,           // 探路打到的对象所在层（诊断用）
            lastWallLayer: -1,
            lastWallNormalY: -2.0,
            lastIsMyRaw: '',               // 最近一次 isMyPlayer 的原始返回值（typeof:值）
            lastWallObject: '',            // 撞到的对象名（诊断）
            probeLayerHistogram: '',       // 探路命中层分布 "层号:次数 ..."（诊断用，beat 里可见）
            probeLayerCounts: {},
            lastProbeLayer: -1,
            lastReject: ""
        }
    };

    var native = {
        ready: false,
        isMyWeapon: null,
        layerConstantCctor: null,
        isMyPlayer: null,
        getTransform: null,
        getGameObject: null,
        getPosition: null,
        getLayer: null,
        getContacts: null,
        getAttachedRigidbody: null,
        ignoreCollision: null,
        overlapSphere: null,
        raycast: null,
        findObjectFromInstanceID: null,
        getName: null,
        layerToName: null,
        getVelocity: null,
        setVelocity: null,
        setDetectCollisions: null
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

    // ------------------------------------------------------------------
    // Frida 的 'bool' 返回值**不保证是 JS 的 true**（可能是 1 / 其它真值）。
    // 用 `=== true` 判定原生 bool 是本项目已经踩过的坑（见 40_direct_damage
    // 里同名的 toFlag），表现就是"功能开着但任何判定都失败"。
    // 所有原生 bool 一律走这里。
    // ------------------------------------------------------------------
    function toFlag(value) {
        if (value === true) return true;
        if (value === false) return false;
        var n = Number(value);
        if (isFinite(n)) return n !== 0;
        return Boolean(value);
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

    function samePointer(a, b) {
        try { return a.equals(b); } catch (_) { return false; }
    }

    function isExecutable(p) {
        try {
            var range = Process.findRangeByAddress(p);
            return range !== null && range.protection.indexOf('x') !== -1;
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

    function ensureCache() {
        if (!Runtime.cache.floatBuf) Runtime.cache.floatBuf = Memory.alloc(4);
        if (!Runtime.cache.vecBuf) Runtime.cache.vecBuf = Memory.alloc(12);
        if (!Runtime.cache.hitBuf) Runtime.cache.hitBuf = Memory.alloc(0x30);   // RaycastHit(0x2C)
    }

    // float -> u32 位模式：按值 struct / float 参数在 cdecl 下就是 4 字节标量，
    // 统一走 uint 传位模式，避免不同 Frida 版本对 'float' 的 ABI 处理差异。
    function floatToU32(value) {
        try {
            ensureCache();
            Runtime.cache.floatBuf.writeFloat(value);
            return Runtime.cache.floatBuf.readU32();
        } catch (_) {
            return 0;
        }
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
            var base = Runtime.base;
            native.isMyWeapon = new NativeFunction(
                base.add(RVA.Weapon_get_isMyWeapon), 'bool', ['pointer', 'pointer'], CALL_CONV);
            native.layerConstantCctor = new NativeFunction(
                base.add(RVA.LayerConstant_cctor), 'void', ['pointer'], CALL_CONV);

            // ---- 弹体穿墙 ----
            native.isMyPlayer = new NativeFunction(
                base.add(RVA.Player_get_isMyPlayer), 'bool', ['pointer', 'pointer'], CALL_CONV);
            native.getTransform = new NativeFunction(
                base.add(RVA.Component_get_transform), 'pointer', ['pointer', 'pointer'], CALL_CONV);
            native.getGameObject = new NativeFunction(
                base.add(RVA.Component_get_gameObject), 'pointer', ['pointer', 'pointer'], CALL_CONV);
            native.getPosition = new NativeFunction(
                base.add(RVA.Transform_get_position_Injected), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
            native.getLayer = new NativeFunction(
                base.add(RVA.GameObject_get_layer), 'int32', ['pointer', 'pointer'], CALL_CONV);
            native.getContacts = new NativeFunction(
                base.add(RVA.Collision_get_contacts), 'pointer', ['pointer', 'pointer'], CALL_CONV);
            native.getAttachedRigidbody = new NativeFunction(
                base.add(RVA.Collider_get_attachedRigidbody), 'pointer', ['pointer', 'pointer'], CALL_CONV);
            native.ignoreCollision = new NativeFunction(
                base.add(RVA.Physics_IgnoreCollision), 'void', ['pointer', 'pointer', 'int', 'pointer'], CALL_CONV);
            native.overlapSphere = new NativeFunction(
                base.add(RVA.Physics_OverlapSphere), 'pointer',
                ['uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'pointer'], CALL_CONV);
            native.getVelocity = new NativeFunction(
                base.add(RVA.Rigidbody_get_velocity_Injected), 'void', ['pointer', 'pointer', 'pointer'], CALL_CONV);
            native.setVelocity = new NativeFunction(
                base.add(RVA.Rigidbody_set_velocity), 'void',
                ['pointer', 'uint', 'uint', 'uint', 'pointer'], CALL_CONV);
            // 主动探路：Physics.Raycast(origin, direction, out RaycastHit, maxDistance, layerMask)
            // Vector3 按值压栈 -> 6 个 4 字节标量；out 参数是 RaycastHit*。
            // 6 参版：可传 QueryTriggerInteraction，探路时用 Ignore 避免打到 trigger
            native.raycast = new NativeFunction(
                base.add(RVA.Physics_Raycast), 'bool',
                ['uint', 'uint', 'uint', 'uint', 'uint', 'uint', 'pointer', 'uint', 'uint', 'uint', 'pointer'],
                CALL_CONV);
            native.findObjectFromInstanceID = new NativeFunction(
                base.add(RVA.Object_FindObjectFromInstanceID), 'pointer', ['int', 'pointer'], CALL_CONV);
            native.getName = new NativeFunction(
                base.add(RVA.Object_get_name), 'pointer', ['pointer', 'pointer'], CALL_CONV);
            native.layerToName = new NativeFunction(
                base.add(RVA.LayerMask_LayerToName), 'pointer', ['int', 'pointer'], CALL_CONV);
            native.setDetectCollisions = new NativeFunction(
                base.add(RVA.Rigidbody_set_detectCollisions), 'void',
                ['pointer', 'int', 'pointer'], CALL_CONV);

            native.ready = true;
            return true;
        } catch (error) {
            setError('initNativeFunctions failed', error);
            native.ready = false;
            return false;
        }
    }

    // ==================================================================
    // A. 子弹穿墙（原逻辑，未改）
    // ==================================================================

    function initializeLayerConstant() {
        if (Runtime.layerInitialized) return true;
        try {
            native.layerConstantCctor(ptr(0));
            Runtime.layerInitialized = true;
            return true;
        } catch (error) {
            setError('LayerConstant..cctor failed', error);
            return false;
        }
    }

    function getLayerStaticFields() {
        if (!native.ready && !initNativeFunctions()) return ptr(0);
        if (!Runtime.layerInitialized && !initializeLayerConstant()) return ptr(0);

        try {
            var klassPtr = Runtime.base.add(RVA.LayerConstant_TypeInfo).readPointer();
            if (isNull(klassPtr) || !isReadablePtr(klassPtr)) return ptr(0);
            return klassPtr.add(OFF.Klass_staticFields).readPointer();
        } catch (error) {
            setError('get LayerConstant static fields failed', error);
            return ptr(0);
        }
    }

    function readLayerValue(offset) {
        try {
            var fields = getLayerStaticFields();
            if (isNull(fields)) return null;
            return fields.add(offset).readS32();
        } catch (error) {
            setError('read LayerConstant field failed', error);
            return null;
        }
    }

    function writeLayerValue(offset, value) {
        try {
            var fields = getLayerStaticFields();
            if (isNull(fields)) return false;
            fields.add(offset).writeS32(value | 0);
            return true;
        } catch (error) {
            setError('write LayerConstant field failed', error);
            return false;
        }
    }

    function buildHitBoxOnlyMask() {
        var hitBoxLayer = readLayerValue(OFF.LayerConstant_HitBox);
        if (hitBoxLayer === null || hitBoxLayer < 0 || hitBoxLayer > 30) {
            Runtime.stats.skippedInvalid += 1;
            logLimited('hitbox-layer-invalid', 'warn', 'invalid LayerConstant.HitBox=' + hitBoxLayer, 2000);
            return null;
        }
        Runtime.stats.lastHitBoxLayer = hitBoxLayer;
        return 1 << hitBoxLayer;
    }

    function patchGunShootLayerMask(reason) {
        if (!Runtime.enabled || !Runtime.config.forceHitboxOnlyDuringLocalDamage) return false;
        if (Runtime.currentPatch !== null) {
            Runtime.currentPatch.depth += 1;
            return true;
        }

        var originalMask = readLayerValue(OFF.LayerConstant_LM_GunShoot);
        var patchedMask = buildHitBoxOnlyMask();
        if (originalMask === null || patchedMask === null) return false;
        if (originalMask === patchedMask) {
            Runtime.currentPatch = {
                depth: 1,
                originalMask: originalMask,
                patchedMask: patchedMask,
                alreadyMatched: true
            };
            return true;
        }

        if (!writeLayerValue(OFF.LayerConstant_LM_GunShoot, patchedMask)) return false;

        Runtime.currentPatch = {
            depth: 1,
            originalMask: originalMask,
            patchedMask: patchedMask,
            alreadyMatched: false
        };
        Runtime.stats.layerPatchCount += 1;
        Runtime.stats.lastOriginalGunShootMask = originalMask;
        Runtime.stats.lastPatchedGunShootMask = patchedMask;
        Runtime.stats.lastPatchReason = reason || '';
        logLimited('layer-patch', 'info', 'LM_GunShoot patched 0x' +
            (originalMask >>> 0).toString(16) + ' -> 0x' + (patchedMask >>> 0).toString(16), 1000);
        return true;
    }

    function writeOriginalMaskAndClearPatch(reason) {
        if (Runtime.currentPatch === null) return false;

        var patch = Runtime.currentPatch;
        Runtime.stats.lastRestoreReason = reason || '';

        if (patch.alreadyMatched) {
            Runtime.currentPatch = null;
            return true;
        }

        if (!writeLayerValue(OFF.LayerConstant_LM_GunShoot, patch.originalMask)) {
            patch.depth = Math.max(patch.depth, 1);
            setError('restore LM_GunShoot failed', { message: 'write original mask failed' });
            return false;
        }

        var readbackMask = readLayerValue(OFF.LayerConstant_LM_GunShoot);
        if (readbackMask !== patch.originalMask) {
            patch.depth = Math.max(patch.depth, 1);
            setError('restore LM_GunShoot readback mismatch', {
                message: 'expected 0x' + (patch.originalMask >>> 0).toString(16) +
                    ', got 0x' + ((readbackMask || 0) >>> 0).toString(16)
            });
            return false;
        }

        Runtime.currentPatch = null;

        Runtime.stats.layerRestoreCount += 1;
        logLimited('layer-restore', 'info', 'LM_GunShoot restored to 0x' +
            (patch.originalMask >>> 0).toString(16), 1000);
        return true;
    }

    function restoreGunShootLayerMask(reason) {
        if (Runtime.currentPatch === null) return false;

        if (Runtime.currentPatch.depth > 1) {
            Runtime.currentPatch.depth -= 1;
            return true;
        }

        Runtime.currentPatch.depth = 1;
        return writeOriginalMaskAndClearPatch(reason);
    }

    function forceRestoreGunShootLayerMask(reason) {
        if (Runtime.currentPatch === null) return false;

        Runtime.currentPatch.depth = 1;
        return writeOriginalMaskAndClearPatch(reason);
    }

    function readWallShotDamageRatio(wpnGun) {
        try {
            if (isNull(wpnGun)) return null;

            var data = wpnGun.add(OFF.WPN_Gun_realData).readPointer();
            if (isNull(data)) {
                data = wpnGun.add(OFF.Weapon_data).readPointer();
            }
            if (isNull(data)) return null;

            var wallShotDamageRatio = data.add(OFF.WeaponData_Gun_wallShotDamageRatio).readFloat();
            if (!isFinite(wallShotDamageRatio)) return null;

            Runtime.stats.lastWallRatio = wallShotDamageRatio;
            return wallShotDamageRatio;
        } catch (error) {
            setError('readWallShotDamageRatio failed', error);
            return null;
        }
    }

    function isLocalWeapon(weapon) {
        if (isNull(weapon) || !native.ready) return false;
        try {
            return toFlag(native.isMyWeapon(weapon, ptr(0)));
        } catch (error) {
            setError('Weapon.get_isMyWeapon failed', error);
            return false;
        }
    }

    // ==================================================================
    // B. 弹体穿墙（投射物）
    // ==================================================================

    function isLocalPlayer(player) {
        if (!isReadablePtr(player) || !native.isMyPlayer) return false;
        try { return toFlag(native.isMyPlayer(player, ptr(0))); } catch (_) { return false; }
    }

    // 弹体是不是"本地玩家发射的"。owner 由 Weapon.ProjectMissile 直接写字段(+0x30)，
    // 早于 SetWeaponData / Work，所以物理步里读是可靠的。
    function isLocalMissile(missile) {
        if (!isReadablePtr(missile)) return false;
        try {
            var owner = missile.add(OFF.Missile_owner).readPointer();
            if (!isReadablePtr(owner)) {
                Runtime.stats.lastIsMyRaw = 'owner=null';
                return false;
            }
            if (!native.isMyPlayer) {
                Runtime.stats.lastIsMyRaw = 'no native';
                return false;
            }
            // 把原生 bool 的原始返回值记下来：排查"类型不对导致全部判定失败"时，
            // beat 日志里的 isMy原始= 会直接给出 typeof + 值。
            var raw = native.isMyPlayer(owner, ptr(0));
            Runtime.stats.lastIsMyRaw = typeof raw + ':' + String(raw);
            return toFlag(raw);
        } catch (error) {
            Runtime.stats.lastIsMyRaw = 'err';
            return false;
        }
    }

    function penetrableLayerText() {
        var parts = [];
        for (var i = 0; i <= 31; i++) {
            if (((Runtime.config.projectilePenetrableLayers >>> i) & 1) === 1) {
                parts.push(i + '(' + layerName(i) + ')');
            }
        }
        return parts.length ? parts.join(' ') : '无';
    }

    // 一次性列出本工程所有非空层名：搞清楚"layer 2 到底是什么"最直接的办法
    function allLayerNamesText() {
        var parts = [];
        for (var i = 0; i <= 31; i++) {
            var name = layerName(i);
            if (name && name !== String(i)) parts.push(i + '=' + name);
        }
        return parts.join(' ');
    }

    function environmentLayer() {
        var layer = readLayerValue(OFF.LayerConstant_Environment);
        return (layer === null || layer < 0 || layer > 31) ? 0 : layer;
    }

    // "还在墙里吗"用的层掩码 = 可穿透层掩码（同一套层，避免口径不一致）
    function environmentMask() {
        return Runtime.config.projectilePenetrableLayers >>> 0;
    }

    function missileState(missile, create) {
        var key;
        try { key = missile.toString(); } catch (_) { return null; }
        var st = Runtime.missiles[key];
        if (!st && create) {
            st = Runtime.missiles[key] = {
                at: Date.now(),
                rb: null,
                v: null,
                pos: null,
                ignores: [],
                tries: 0,
                ghost: false,
                ghostAt: 0,
                ghostNeed: 0,
                ghostTravel: 0,
                ghostLastPos: null
            };
        }
        return st || null;
    }

    function dropMissileState(missile, reason, releaseIgnores) {
        var key;
        try { key = missile.toString(); } catch (_) { return false; }
        var st = Runtime.missiles[key];
        if (!st) return false;
        // 关键：回池/复用前必须把 detectCollisions 还原，否则下一颗弹会继承
        // "什么都不碰"的状态，直接飞穿全场。
        restoreGhost(st, reason || 'drop');
        if (releaseIgnores !== false) releaseAllIgnores(st, reason || 'drop');
        delete Runtime.missiles[key];
        return true;
    }

    function readRigidbodyVelocity(rb) {
        if (!isReadablePtr(rb) || !native.getVelocity) return null;
        try {
            ensureCache();
            var buf = Runtime.cache.vecBuf;
            native.getVelocity(rb, buf, ptr(0));
            var v = { x: buf.readFloat(), y: buf.add(4).readFloat(), z: buf.add(8).readFloat() };
            if (!isFinite(v.x) || !isFinite(v.y) || !isFinite(v.z)) return null;
            return v;
        } catch (_) {
            return null;
        }
    }

    function writeRigidbodyVelocity(rb, v) {
        if (!isReadablePtr(rb) || !native.setVelocity || !v) return false;
        try {
            native.setVelocity(rb, floatToU32(v.x), floatToU32(v.y), floatToU32(v.z), ptr(0));
            return true;
        } catch (error) {
            setError('Rigidbody.set_velocity failed', error);
            return false;
        }
    }

    function readMissilePosition(missile) {
        try {
            if (!native.getTransform || !native.getPosition) return null;
            var transform = native.getTransform(missile, ptr(0));
            if (!isReadablePtr(transform)) return null;
            ensureCache();
            var buf = Runtime.cache.vecBuf;
            native.getPosition(transform, buf, ptr(0));
            var pos = { x: buf.readFloat(), y: buf.add(4).readFloat(), z: buf.add(8).readFloat() };
            if (!isFinite(pos.x) || !isFinite(pos.y) || !isFinite(pos.z)) return null;
            return pos;
        } catch (_) {
            return null;
        }
    }

    function velocityLength(v) {
        if (!v) return 0;
        return Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
    }

    // 接触法线：Collision.get_contacts() 返回 ContactPoint[]（值类型内联），
    // 元素 0 的 m_Normal 在 items + 0x0C。
    // 读不到时返回 null（宁可"按地板处理、不穿透"，也不要误把地板当墙）。
    function readContactNormalY(collision) {
        try {
            if (!native.getContacts) return null;
            var contacts = native.getContacts(collision, ptr(0));
            if (!isReadablePtr(contacts)) return null;
            var len = contacts.add(OFF.Il2CppArray_length).readS32();
            if (len <= 0) return null;
            var items = contacts.add(OFF.Il2CppArray_items);
            var ny = items.add(OFF.ContactPoint_normal + 4).readFloat();
            if (!isFinite(ny)) return null;
            return ny;
        } catch (_) {
            return null;
        }
    }

    // 可穿透的层：默认只有 Environment(layer 0，关卡几何)；
    // AirWall(layer 2，地图边界隐形墙) 默认不穿，否则弹体会飞出地图
    // （可用 config.projectilePenetrateAirWall 打开）。
    function isPenetrableWallLayer(layer) {
        if (!(layer >= 0 && layer <= 31)) return false;
        return ((Runtime.config.projectilePenetrableLayers >>> layer) & 1) === 1;
    }

    // Il2CppString：klass(4) + monitor(4) + length(4) + UTF-16 数据(0xC 起)
    function readIl2CppString(strPtr) {
        try {
            if (!isReadablePtr(strPtr)) return '';
            var len = strPtr.add(8).readS32();
            if (len <= 0 || len > 128) return '';
            var out = '';
            for (var i = 0; i < len; i++) {
                var code = strPtr.add(12 + i * 2).readU16();
                if (code === 0) break;
                out += String.fromCharCode(code);
            }
            return out;
        } catch (_) {
            return '';
        }
    }

    // 层号 -> 层名（诊断用："层=2" 一眼看不出是什么，加上名字就清楚了）
    function layerName(layer) {
        try {
            if (!native.layerToName) return String(layer);
            return readIl2CppString(native.layerToName(layer | 0, ptr(0))) || String(layer);
        } catch (_) {
            return String(layer);
        }
    }

    function objectName(obj) {
        try {
            if (!native.getName) return '';
            return readIl2CppString(native.getName(obj, ptr(0)));
        } catch (_) {
            return '';
        }
    }

    function isEnvironmentCollider(collider) {
        try {
            if (!isReadablePtr(collider) || !native.getGameObject || !native.getLayer) return false;
            var go = native.getGameObject(collider, ptr(0));
            if (!isReadablePtr(go)) return false;
            var layer = native.getLayer(go, ptr(0));
            Runtime.stats.lastWallLayer = layer;
            Runtime.stats.lastWallObject = objectName(go);
            return isPenetrableWallLayer(layer);
        } catch (_) {
            return false;
        }
    }

    // Physics.OverlapSphere(接触点, 1.2m) + Collider.attachedRigidbody == 弹体 Rigidbody，
    // 反查弹体自身的 collider（含子物体上的 collider）。不依赖 GetComponent<Collider>：
    // 这个泛型实例在本二进制里没有独立函数体，只能从 MethodInfo 走，风险更高。
    function collectMissileColliders(rb, pos) {
        var found = [];
        if (!native.overlapSphere || !native.getAttachedRigidbody || !pos || !isReadablePtr(rb)) return found;
        try {
            var arr = native.overlapSphere(
                floatToU32(pos.x), floatToU32(pos.y), floatToU32(pos.z),
                floatToU32(1.2), 0xFFFFFFFF, 2, ptr(0));
            if (!isReadablePtr(arr)) return found;
            var len = arr.add(OFF.Il2CppArray_length).readS32();
            if (len <= 0 || len > 4096) return found;
            var items = arr.add(OFF.Il2CppArray_items);
            for (var i = 0; i < len; i++) {
                var c = items.add(i * 4).readPointer();
                if (!isReadablePtr(c)) continue;
                var crb = native.getAttachedRigidbody(c, ptr(0));
                if (samePointer(crb, rb)) found.push(c);
            }
        } catch (error) {
            setError('collectMissileColliders failed', error);
        }
        return found;
    }

    function ignoreWallForMissile(missile, rb, pos, wall, st, plane) {
        if (!st) return 0;
        if (!isReadablePtr(wall)) return 0;
        // 同一面墙不要重复忽略（每物理步都会探到它）。
        // 返回 -1 表示"本来就已经忽略了" —— 调用方要把它当成成功，
        // 否则会掉进 detectCollisions 备选分支，把整颗弹的碰撞也关掉。
        for (var k = 0; k < st.ignores.length; k++) {
            if (samePointer(st.ignores[k].wall, wall)) return -1;
        }
        var mine = collectMissileColliders(rb, pos);
        if (!mine.length) {
            Runtime.stats.projectileOverlapMiss += 1;
            logLimited('overlap-miss', 'warn',
                '反查弹体自身 collider 失败（弹体=' + missile + ' 墙=' + wall + '），本次不忽略', 2000);
            return 0;
        }
        var applied = [];
        for (var i = 0; i < mine.length; i++) {
            try {
                native.ignoreCollision(mine[i], wall, 1, ptr(0));
                applied.push(mine[i]);
                Runtime.stats.projectileIgnoredPairs += 1;
            } catch (error) {
                setError('Physics.IgnoreCollision(true) failed', error);
            }
        }
        if (applied.length) {
            st.ignores.push({
                wall: wall,
                mine: applied,
                at: Date.now(),
                // 主动阶段带上"墙面平面"：还原必须由"真的穿过去了"触发，不能只看时间。
                px: plane ? plane.px : undefined,
                py: plane ? plane.py : undefined,
                pz: plane ? plane.pz : undefined,
                nx: plane ? plane.nx : undefined,
                ny: plane ? plane.ny : undefined,
                nz: plane ? plane.nz : undefined
            });
        }
        return applied.length;
    }

    function releaseIgnore(entry, reason) {
        var released = 0;
        for (var i = 0; i < entry.mine.length; i++) {
            try {
                native.ignoreCollision(entry.mine[i], entry.wall, 0, ptr(0));
                released += 1;
                Runtime.stats.projectileReleasedPairs += 1;
            } catch (error) {
                setError('Physics.IgnoreCollision(false) failed', error);
            }
        }
        if (released) {
            logLimited('release-ignore', 'info',
                '还原墙碰撞忽略（' + (reason || '') + '）：' + released + ' 对', 1500);
        }
        return released;
    }

    function releaseAllIgnores(st, reason) {
        if (!st || !st.ignores || !st.ignores.length) return 0;
        var total = 0;
        for (var i = 0; i < st.ignores.length; i++) {
            total += releaseIgnore(st.ignores[i], reason);
        }
        st.ignores = [];
        return total;
    }

    // 弹体中心附近还压着"不是自己"的关卡几何吗？
    //   —— 用 OverlapSphere + attachedRigidbody 过滤，而不是 Physics.CheckSphere：
    //      CheckSphere 只看 layerMask，会把弹体自己的 collider 也算进去
    //      （弹体多半就在 layer 0 = Environment），于是永远返回 true、永远不还原。
    //   半径取很小(0.08)：只要"中心"离开墙体就算出来了，避免贴着地板被误判成
    //   "还在墙里"从而一直保持忽略（那会让手雷掉出地板）。
    function insideEnvironment(pos, rb) {
        if (!pos || !native.overlapSphere || !native.getAttachedRigidbody) return false;
        try {
            var arr = native.overlapSphere(
                floatToU32(pos.x), floatToU32(pos.y), floatToU32(pos.z),
                floatToU32(0.08), environmentMask(), 1, ptr(0));
            if (!isReadablePtr(arr)) return false;
            var len = arr.add(OFF.Il2CppArray_length).readS32();
            if (len <= 0 || len > 4096) return false;
            var items = arr.add(OFF.Il2CppArray_items);
            for (var i = 0; i < len; i++) {
                var c = items.add(i * 4).readPointer();
                if (!isReadablePtr(c)) continue;
                var crb = native.getAttachedRigidbody(c, ptr(0));
                if (isReadablePtr(rb) && samePointer(crb, rb)) continue;   // 自己的 collider，跳过
                return true;
            }
            return false;
        } catch (_) {
            return false;
        }
    }

    // 每一物理步处理"还原窗口"：满足最短窗口 且 (不再重叠墙体 或 到达硬上限) 就还原。
    function tickMissileIgnores(st, pos) {
        if (!st || !st.ignores || !st.ignores.length) return;
        var rb = st.rb;
        var now = Date.now();
        var keep = [];
        for (var i = 0; i < st.ignores.length; i++) {
            var entry = st.ignores[i];
            var elapsed = now - entry.at;
            if (elapsed < Runtime.config.projectileIgnoreMinMs) {
                keep.push(entry);
                continue;
            }
            if (elapsed >= Runtime.config.projectileIgnoreMaxMs) {
                releaseIgnore(entry, '硬上限');
                continue;
            }
            // 主动阶段记录的墙面：必须"已经从墙外侧走到墙后 0.3m"才算穿过。
            // 只按时间会误判 —— 手雷 80ms 才走 0.8m，墙还有 2m 远就被还原了。
            var crossed = true;
            if (entry.nx !== undefined && pos) {
                var ox = pos.x - entry.px;
                var oy = pos.y - entry.py;
                var oz = pos.z - entry.pz;
                crossed = (ox * entry.nx + oy * entry.ny + oz * entry.nz) < -0.30;
            }
            if (crossed && !insideEnvironment(pos, rb)) {
                releaseIgnore(entry, '已穿过墙体');
                continue;
            }
            keep.push(entry);
        }
        st.ignores = keep;
    }

    function setDetectCollisions(rb, on) {
        if (!isReadablePtr(rb) || !native.setDetectCollisions) return false;
        try {
            native.setDetectCollisions(rb, on ? 1 : 0, ptr(0));
            return true;
        } catch (error) {
            Runtime.stats.projectileGhostFail += 1;
            setError('Rigidbody.set_detectCollisions failed', error);
            return false;
        }
    }

    // 沿飞行方向往前探路。返回 {distance, normalY} / null。
    // 起点前移 0.35m：即使弹体自己的 collider 也在 Environment 层，射线起点在
    // 自身体内时不会命中背面，前移再保险一点。
    function probeAhead(pos, v, maxDistance) {
        if (!pos || !v || !native.raycast) return null;
        var speed = velocityLength(v);
        if (!(speed > 0.05)) return null;
        var dx = v.x / speed, dy = v.y / speed, dz = v.z / speed;
        var ox = pos.x + dx * 0.35, oy = pos.y + dy * 0.35, oz = pos.z + dz * 0.35;
        try {
            ensureCache();
            var hit = Runtime.cache.hitBuf;
            var ok = native.raycast(
                floatToU32(ox), floatToU32(oy), floatToU32(oz),
                floatToU32(dx), floatToU32(dy), floatToU32(dz),
                hit, floatToU32(maxDistance), 0xFFFFFFFF, 1 /* QueryTriggerInteraction.Ignore */, ptr(0));
            if (!toFlag(ok)) return null;
            var dist = hit.add(OFF.RaycastHit_distance).readFloat();
            var ny = hit.add(OFF.RaycastHit_normal + 4).readFloat();
            if (!isFinite(dist) || !isFinite(ny)) return null;
            // 撞点 + 法线：用来判断"到底有没有真的穿过这面墙"（慢速弹体只按时间会误判）
            var plane = {
                px: hit.add(OFF.RaycastHit_point).readFloat(),
                py: hit.add(OFF.RaycastHit_point + 4).readFloat(),
                pz: hit.add(OFF.RaycastHit_point + 8).readFloat(),
                nx: hit.add(OFF.RaycastHit_normal).readFloat(),
                ny: ny,
                nz: hit.add(OFF.RaycastHit_normal + 8).readFloat()
            };

            // 全层射线 + 反查命中物的层：这样"墙到底在哪个层"能直接从日志里看出来，
            // 不用靠猜 mask。命中物的 collider 在 RaycastHit 里存的是 instanceID，
            // 必须走 Object.FindObjectFromInstanceID 才能变成对象指针。
            var layer = -1;
            try {
                var id = hit.add(OFF.RaycastHit_collider).readS32();
                var obj = native.findObjectFromInstanceID ? native.findObjectFromInstanceID(id, ptr(0)) : null;
                if (isReadablePtr(obj)) {
                    var go = native.getGameObject(obj, ptr(0));
                    if (isReadablePtr(go)) layer = native.getLayer(go, ptr(0));
                }
            } catch (_) {}
            Runtime.stats.lastProbeLayer = layer;
            try {
                var hist = Runtime.stats.probeLayerCounts;
                hist[layer] = (hist[layer] || 0) + 1;
            } catch (_) {}
            var probeObjectName = '';
            try {
                if (isReadablePtr(obj)) {
                    var probeGo = native.getGameObject(obj, ptr(0));
                    probeObjectName = objectName(isReadablePtr(probeGo) ? probeGo : obj);
                }
            } catch (_) {}
            return {
                distance: dist + 0.35,
                normalY: ny,
                layer: layer,
                objectName: probeObjectName,
                plane: plane,
                collider: isReadablePtr(obj) ? obj : null,
                penetrable: isPenetrableWallLayer(layer)
            };
        } catch (error) {
            setError('Physics.Raycast failed', error);
            return null;
        }
    }

    // ---------------- 主动穿墙（主路径）----------------
    // 为什么是主动的：只靠 OnCollisionEnter 兜底时，一旦那次回调没进来（或判定被
    // 某个字段读失败挡掉），弹药就会照原版撞墙爆炸。物理步里提前 3.5m 探路，
    // 在真正接触之前把这一颗弹体的物理碰撞关掉，就根本不会产生这次碰撞，
    // 也就不会触发原版的"撞墙即爆"。离开墙体后立刻恢复 detectCollisions。
    //
    // 穿墙态的三个结束条件（任一）：
    //   1) 已经走过"入态时到墙面的距离 + projectileGhostExtra"且中心已不在关卡几何里；
    //   2) 到达 projectileIgnoreMaxMs 硬上限（保证不会永久关着碰撞）；
    //   3) 弹体回池/功能关闭（dropMissileState / releaseEveryIgnore 里强制还原）。
    function tickMissileGhost(st, missile, rb, pos, v) {
        var now = Date.now();
        if (!st.ghost) {
            if (!pos || !v) return;
            var hit = probeAhead(pos, v, Runtime.config.projectileProbeLookahead);
            if (!hit) return;
            Runtime.stats.projectileRayHits += 1;
            if (!hit.penetrable) {
                Runtime.stats.projectileRayOtherLayers += 1;
                return;
            }
            if (Math.abs(hit.normalY) >= Runtime.config.projectileWallMaxNormalY) {
                Runtime.stats.projectileRayFloorLikes += 1;
                return;
            }
            Runtime.stats.projectileRayWallHits += 1;

            // 主选：只忽略"这一颗弹 × 这一面墙"。作用域最小，地板完全不受影响。
            // 返回值：>0 新忽略了几对；-1 这面墙早就忽略过了（也算成功）；0 失败。
            var applied = hit.collider
                ? ignoreWallForMissile(missile, rb, pos, hit.collider, st, hit.plane)
                : 0;
            if (applied !== 0) {
                if (applied > 0) {
                    Runtime.stats.projectileProactiveIgnores += 1;
                    logLimited('proactive-ignore', 'info',
                        '弹体穿墙（主动）：提前忽略前方墙面 missile=' + missile +
                        ' 距=' + hit.distance.toFixed(2) + 'm 层=' + hit.layer + '(' + layerName(hit.layer) + ')' +
                        ' 对象=' + (hit.objectName || '?') +
                        ' normalY=' + hit.normalY.toFixed(2), 200);
                }
                return;
            }

            // 备选：拿不到墙 collider / 反查不到弹体自身 collider 时，退化成
            // "关掉这一颗弹体的全部碰撞"（有窗口、必定还原；滚地雷场景才会走这里）。
            if (!setDetectCollisions(rb, 0)) return;
            st.ghost = true;
            st.ghostAt = now;
            st.ghostNeed = hit.distance + Runtime.config.projectileGhostExtra;
            st.ghostTravel = 0;
            st.ghostLastPos = pos;
            Runtime.stats.projectileGhostStarts += 1;
            logLimited('ghost-start', 'info',
                '弹体穿墙开始：missile=' + missile + ' 前方墙距=' + hit.distance.toFixed(2) +
                'm normalY=' + hit.normalY.toFixed(2) + ' 需要走过=' + st.ghostNeed.toFixed(2) + 'm', 200);
            return;
        }

        if (st.ghostLastPos && pos) {
            var ddx = pos.x - st.ghostLastPos.x;
            var ddy = pos.y - st.ghostLastPos.y;
            var ddz = pos.z - st.ghostLastPos.z;
            st.ghostTravel += Math.sqrt(ddx * ddx + ddy * ddy + ddz * ddz);
        }
        st.ghostLastPos = pos;

        var elapsed = now - st.ghostAt;
        var hardEnd = elapsed >= Runtime.config.projectileIgnoreMaxMs;
        var enough = st.ghostTravel >= st.ghostNeed;
        var clear = !insideEnvironment(pos, rb);
        if (hardEnd || (elapsed >= Runtime.config.projectileIgnoreMinMs && enough && clear)) {
            setDetectCollisions(rb, 1);
            st.ghost = false;
            if (hardEnd && !(enough && clear)) {
                Runtime.stats.projectileGhostForceEnds += 1;
            }
            Runtime.stats.projectileGhostEnds += 1;
            logLimited('ghost-end', 'info',
                '弹体穿墙结束：missile=' + missile + ' 走过=' + st.ghostTravel.toFixed(2) +
                'm 用时=' + elapsed + 'ms' + (hardEnd ? '（硬上限）' : ''), 200);
        }
    }

    function restoreGhost(st, reason) {
        if (!st || !st.ghost) return false;
        setDetectCollisions(st.rb, 1);
        st.ghost = false;
        Runtime.stats.projectileGhostRestores += 1;
        return true;
    }

    // 判定"这一次碰撞要不要按穿墙处理"，并给出原因（只用于日志/统计）。
    function classifyMissileWallHit(missile, collision) {
        if (!Runtime.enabled || !Runtime.config.projectileWallPenetration) {
            Runtime.stats.lastReject = 'off';
            return null;
        }
        if (!isReadablePtr(missile) || !isReadablePtr(collision)) {
            Runtime.stats.lastReject = 'unreadable';
            return null;
        }
        if (!isLocalMissile(missile)) {
            Runtime.stats.lastReject = 'notMine';
            return null;
        }
        Runtime.stats.projectileLocalCollisions += 1;

        var wall = null;
        try { wall = collision.add(OFF.Collision_collider).readPointer(); } catch (_) {}
        if (!isReadablePtr(wall)) {
            Runtime.stats.lastReject = 'noCollider';
            return null;
        }
        Runtime.stats.lastReject = 'layer';
        if (!isEnvironmentCollider(wall)) return null;

        var ny = readContactNormalY(collision);
        Runtime.stats.lastWallNormalY = (ny === null ? -2.0 : ny);
        if (ny === null) {
            // 读不到接触点：保守按地板处理，不穿透（保证滚雷/落地行为不被误伤）。
            Runtime.stats.lastReject = 'noNormal';
            return null;
        }
        if (Math.abs(ny) >= Runtime.config.projectileWallMaxNormalY) {
            Runtime.stats.lastReject = 'floorLike';
            return null;
        }

        Runtime.stats.lastReject = '';
        return { wall: wall, normalY: ny };
    }

    // 每一次本地弹体碰撞都记一行（限频）。这是"反应式兜底到底有没有被走到"的唯一证据。
    function logMissileCollision(missile, hit) {
        try {
            var layer = Runtime.stats.lastWallLayer;
            var ny = Runtime.stats.lastWallNormalY;
            var who = Runtime.stats.lastWallObject || '';
            logLimited('missile-collision', 'info',
                '弹体碰撞：missile=' + missile +
                ' 层=' + layer + '(' + layerName(layer) + ')' +
                (who ? ' 对象=' + who : '') +
                ' normalY=' + (hit ? ny.toFixed(2) : 'n/a') +
                ' 判定=' + (hit ? '墙面→穿墙' : ('不穿墙/' + Runtime.stats.lastReject)), 200);
        } catch (_) {}
    }

    // 真正做"穿墙"：写回速度 + 忽略这一面墙。
    function completeWallPenetration(missile, collision) {
        try {
            if (!isReadablePtr(missile) || !isReadablePtr(collision)) return false;
            var rb = missile.add(OFF.Missile_rigidBody).readPointer();
            if (!isReadablePtr(rb)) return false;

            var st = missileState(missile, true);
            if (!st) return false;
            st.rb = rb;

            var wall = null;
            try { wall = collision.add(OFF.Collision_collider).readPointer(); } catch (_) {}
            if (!isReadablePtr(wall)) return false;

            // 1) 速度写回（碰撞前缓存优先）
            var v = st.v;
            var source = 'cache';
            if (!v || velocityLength(v) < 0.05) {
                v = null;
                try {
                    var rv = collision.add(OFF.Collision_relativeVelocity);
                    var cand = { x: rv.readFloat(), y: rv.add(4).readFloat(), z: rv.add(8).readFloat() };
                    if (isFinite(cand.x) && isFinite(cand.y) && isFinite(cand.z) && velocityLength(cand) >= 0.05) {
                        v = cand;
                        source = 'relativeVelocity';
                    }
                } catch (_) {}
            }
            // 两个来源都拿不到就**不动速度**：宁可这一发被墙挡一下，
            // 也不要凭猜测写一个方向过去（写错方向比不写更糟）。
            var wroteVelocity = false;
            if (v) {
                wroteVelocity = writeRigidbodyVelocity(rb, v);
                if (source !== 'cache') Runtime.stats.projectileVelFallback += 1;
            }

            // 2) 忽略这一面墙（弹体自己的 collider 由 OverlapSphere 反查）
            var pos = st.pos || readMissilePosition(missile);
            var applied = ignoreWallForMissile(missile, rb, pos, wall, st);

            Runtime.stats.projectilePenetrated += 1;
            st.tries += 1;
            logLimited('penetrate', 'info',
                '弹体穿墙：missile=' + missile + ' wall=' + wall +
                ' layer=' + Runtime.stats.lastWallLayer +
                ' normalY=' + Runtime.stats.lastWallNormalY.toFixed(2) +
                ' 忽略=' + applied + '对 速度=' + (wroteVelocity ? '写回(' + source + ')' : '未变'),
                300);
            return applied > 0 || wroteVelocity;
        } catch (error) {
            setError('completeWallPenetration failed', error);
            return false;
        }
    }

    function attachHook(name, rva, callbacks) {
        var address = Runtime.base.add(rva);
        if (!isExecutable(address)) throw new Error(name + ' address is not executable: ' + address);
        var handle = Interceptor.attach(address, callbacks);
        Runtime.hooks.push(handle);
        log('info', 'hook installed: ' + name + ' @ 0x' + rva.toString(16));
    }

    // ==================================================================
    // Hook 安装
    // ==================================================================

    function installHooks() {
        if (Runtime.initialized) return true;
        if (!initNativeFunctions()) return false;

        try {
            // ---------------- A. 子弹穿墙 ----------------
            attachHook('WPN_Gun.Damage', RVA.WPN_Gun_Damage, {
                onEnter: function (args) {
                    Runtime.stats.damageHits += 1;
                    this.localDamage = false;
                    this.weapon = args[0];

                    if (!Runtime.enabled) return;

                    try {
                        if (!toFlag(native.isMyWeapon(args[0], ptr(0)))) {
                            Runtime.stats.skippedRemoteWeapon += 1;
                            return;
                        }

                        this.localDamage = true;
                        Runtime.stats.localDamageHits += 1;
                        Runtime.damageDepth += 1;
                        Runtime.activeDamageWeapon = args[0];
                        readWallShotDamageRatio(args[0]);
                        patchGunShootLayerMask('WPN_Gun.Damage onEnter');

                        if (Runtime.stats.localDamageHits === 1 ||
                            Runtime.stats.localDamageHits % Runtime.config.logEveryDamageHits === 0) {
                            log('info', 'local WPN_Gun.Damage #' + Runtime.stats.localDamageHits +
                                ', wallShotDamageRatio=' + Runtime.stats.lastWallRatio);
                        }
                    } catch (error) {
                        setError('WPN_Gun.Damage onEnter failed', error);
                    }
                },

                onLeave: function () {
                    if (!this.localDamage) return;

                    try {
                        restoreGunShootLayerMask('WPN_Gun.Damage onLeave');
                    } catch (error) {
                        setError('WPN_Gun.Damage onLeave restore failed', error);
                    } finally {
                        Runtime.damageDepth -= 1;
                        if (Runtime.damageDepth <= 0) {
                            Runtime.damageDepth = 0;
                            Runtime.activeDamageWeapon = ptr(0);
                        }
                    }
                }
            });

            attachHook('WeaponLogic.CheckWall', RVA.WeaponLogic_CheckWall, {
                onEnter: function () {
                    this.track = Runtime.enabled && Runtime.damageDepth > 0;
                },

                onLeave: function (retval) {
                    if (!this.track) return;
                    Runtime.stats.checkWallHits += 1;
                    Runtime.stats.lastCheckWallResult = (retval.toInt32() & 0xFF) !== 0; // P1：bool 只看 AL
                }
            });

            // ---------------- B. 弹体穿墙 ----------------
            // 对象池复用：进 SetWeaponData 先无条件清掉这颗指针的旧状态，
            // 否则上一颗弹的"忽略墙"记录会串到下一颗弹上。
            attachHook('WPN_Missile.SetWeaponData', RVA.WPN_Missile_SetWeaponData, {
                onEnter: function (args) {
                    if (!Runtime.enabled) return;
                    try { dropMissileState(args[0], 'reused'); } catch (_) {}
                }
            });

            // 物理步：缓存碰撞前速度/位置（FixedUpdate 一定早于本次物理步的碰撞回调），
            // 并处理忽略窗口的还原。
            attachHook('WPN_Missile.FixedUpdate', RVA.WPN_Missile_FixedUpdate, {
                onEnter: function (args) {
                    Runtime.stats.projectileFixedSeen += 1;
                    if (!Runtime.enabled || !Runtime.config.projectileWallPenetration) return;
                    var missile = args[0];
                    try {
                        if (!isReadablePtr(missile)) return;
                        if (!isLocalMissile(missile)) {
                            Runtime.stats.projectileFixedNotMine += 1;
                            return;
                        }
                        Runtime.stats.projectileFixedLocal += 1;
                        var rb = missile.add(OFF.Missile_rigidBody).readPointer();
                        if (!isReadablePtr(rb)) return;
                        var st = missileState(missile, true);
                        if (!st) return;
                        st.rb = rb;
                        var pos = readMissilePosition(missile);
                        var v = readRigidbodyVelocity(rb);
                        if (pos) st.pos = pos;
                        if (v && velocityLength(v) >= 0.05) st.v = v;
                        tickMissileIgnores(st, pos);
                        tickMissileGhost(st, missile, rb, pos, v);
                    } catch (error) {
                        setError('WPN_Missile.FixedUpdate onEnter failed', error);
                    }
                }
            });

            // 基类碰撞（WPN_Missile 本身没有 expWhenTouchSth 字段，只能处理物理部分）
            attachHook('WPN_Missile.OnCollisionEnter', RVA.WPN_Missile_OnCollisionEnter, {
                onEnter: function (args) {
                    this.missile = null;
                    this.collision = null;
                    Runtime.stats.projectileCollisions += 1;
                    var hit = classifyMissileWallHit(args[0], args[1]);
                    logMissileCollision(args[0], hit);
                    if (!hit) return;
                    Runtime.stats.projectileWallHits += 1;
                    this.missile = args[0];
                    this.collision = args[1];
                },

                onLeave: function () {
                    if (!this.missile) return;
                    try { completeWallPenetration(this.missile, this.collision); } catch (_) {}
                }
            });

            // 手雷/榴弹/RPG/技能弹走的是这一份重写（vtable slot 9）：
            // 它会读 expWhenTouchSth(+0x74) 决定要不要 TryExplosion。
            // 在 onEnter 把它临时写 0，onLeave 按原字节写回 —— 不替换函数、不改控制流。
            attachHook('WPN_GRENADE.OnCollisionEnter', RVA.WPN_GRENADE_OnCollisionEnter, {
                onEnter: function (args) {
                    this.missile = null;
                    this.collision = null;
                    this.savedFlag = -1;
                    Runtime.stats.projectileCollisions += 1;
                    var hit = classifyMissileWallHit(args[0], args[1]);
                    logMissileCollision(args[0], hit);
                    if (!hit) return;

                    var missile = args[0];
                    var flagAddr = missile.add(OFF.WPN_GRENADE_expWhenTouchSth);
                    var flag = -1;
                    try { flag = flagAddr.readU8(); } catch (_) { return; }

                    Runtime.stats.projectileWallHits += 1;
                    if (flag !== 0) {
                        Runtime.stats.projectileTriedExplosion += 1;
                        flagAddr.writeU8(0);
                        this.savedFlag = flag;
                    }
                    this.missile = missile;
                    this.collision = args[1];
                },

                onLeave: function () {
                    if (!this.missile) return;
                    if (this.savedFlag >= 0) {
                        try { this.missile.add(OFF.WPN_GRENADE_expWhenTouchSth).writeU8(this.savedFlag); } catch (_) {}
                    }
                    try { completeWallPenetration(this.missile, this.collision); } catch (_) {}
                }
            });

            // 回池：立刻还原忽略 + 清状态
            attachHook('WPN_Missile.Recycle', RVA.WPN_Missile_Recycle, {
                onEnter: function (args) {
                    if (!Runtime.enabled) return;
                    try { dropMissileState(args[0], 'recycle'); } catch (_) {}
                }
            });

            startHeartbeat();

            Runtime.initialized = true;
            log('info', 'hooks installed');
            return true;
        } catch (error) {
            setError('installHooks failed', error);
            cleanupHooks();
            return false;
        }
    }

    function startHeartbeat() {
        if (Runtime.heartbeat) return;
        Runtime.heartbeat = setInterval(function () {
            try {
                if (!Runtime.enabled) return;
                sweepMissileStates();
                Runtime.beatTicks = (Runtime.beatTicks || 0) + 1;
                if (Runtime.beatTicks % 5 === 0) logProjectileBeat();
            } catch (error) {
                setError('heartbeat failed', error);
            }
        }, 1000);
    }

    function stopHeartbeat() {
        if (!Runtime.heartbeat) return;
        try { clearInterval(Runtime.heartbeat); } catch (_) {}
        Runtime.heartbeat = null;
    }

    // 探路命中层分布（带层名），排查"墙到底在哪层"
    function probeHistogramText() {
        try {
            var hist = Runtime.stats.probeLayerCounts;
            var keys = Object.keys(hist);
            if (!keys.length) return '无';
            keys.sort(function (a, b) { return hist[b] - hist[a]; });
            var parts = [];
            for (var i = 0; i < keys.length && i < 5; i++) {
                parts.push(keys[i] + '(' + layerName(Number(keys[i])) + '):' + hist[keys[i]]);
            }
            return parts.join(' ');
        } catch (_) {
            return '?';
        }
    }

    // 5 秒一条的弹体穿墙汇总。排查"没生效"时先看这一行：
    //   探路射线=0            -> FixedUpdate 钩子没进本地弹体（owner 判定/开关）
    //   探路射线>0 墙=0       -> 射线一直把前方判成地板/斜面（法线阈值问题）
    //   主动穿墙=0            -> 射线没命中（层不对：看 lastReject/layer）
    //   主动穿墙>0 但没效果   -> detectCollisions 写入没被游戏接受
    //   碰撞=0                -> OnCollisionEnter 那条路根本没被走到（正常，主动穿墙会先接管）
    function logProjectileBeat() {
        var keys = Object.keys(Runtime.missiles);
        var liveGhosts = 0;
        for (var i = 0; i < keys.length; i++) {
            if (Runtime.missiles[keys[i]] && Runtime.missiles[keys[i]].ghost) liveGhosts += 1;
        }
        var s = Runtime.stats;
        log('info', '[beat] 弹体穿墙 碰撞=' + s.projectileCollisions + '(本地' + s.projectileLocalCollisions + ')' +
            ' 墙面=' + s.projectileWallHits +
            ' | 探路射线=' + s.projectileRayHits + '(墙' + s.projectileRayWallHits + '/地' + s.projectileRayFloorLikes +
            '/其他层' + s.projectileRayOtherLayers + ' 命中层=' + s.lastProbeLayer + ')' +
            ' 主动忽略=' + s.projectileProactiveIgnores +
            ' 主动穿墙=' + s.projectileGhostStarts + '/结束' + s.projectileGhostEnds + '(强制' + s.projectileGhostForceEnds + ')' +
            ' | 反应式穿透=' + s.projectilePenetrated + ' 忽略=' + s.projectileIgnoredPairs + '/还原' + s.projectileReleasedPairs +
            ' | FixedUpdate=' + s.projectileFixedSeen + '(本地' + s.projectileFixedLocal + '/非我' + s.projectileFixedNotMine + ')' +
            ' 追踪弹=' + keys.length + ' 穿墙中=' + liveGhosts +
            ' 还原失败=' + s.projectileGhostFail +
            ' isMy原始=' + (s.lastIsMyRaw || '-') +
            ' 探路层分布=' + probeHistogramText() +
            ' lastReject=' + s.lastReject + ' layer=' + s.lastWallLayer +
            ' normalY=' + s.lastWallNormalY.toFixed(2));
    }

    // 兜底清理：万一某颗弹没触发 Recycle（场景卸载/异常）就消失了，
    // 记录不会永远堆在内存里，忽略也不会永远留着。
    function sweepMissileStates() {
        var now = Date.now();
        var keys = Object.keys(Runtime.missiles);
        for (var i = 0; i < keys.length; i++) {
            var st = Runtime.missiles[keys[i]];
            if (!st) continue;
            var expired = (now - st.at) > 60000;
            var hardIgnores = false;
            for (var j = 0; j < st.ignores.length; j++) {
                if (now - st.ignores[j].at >= Runtime.config.projectileIgnoreMaxMs) { hardIgnores = true; break; }
            }
            if (expired || hardIgnores) {
                restoreGhost(st, 'sweep');
                releaseAllIgnores(st, 'sweep');
                delete Runtime.missiles[keys[i]];
                Runtime.stats.projectileSweepRemoved += 1;
            }
        }
    }

    function releaseEveryIgnore(reason) {
        var keys = Object.keys(Runtime.missiles);
        for (var i = 0; i < keys.length; i++) {
            var st = Runtime.missiles[keys[i]];
            if (!st) continue;
            restoreGhost(st, reason);
            releaseAllIgnores(st, reason);
        }
        Runtime.missiles = {};
    }

    function cleanupHooks() {
        for (var i = 0; i < Runtime.hooks.length; i++) {
            try {
                if (Runtime.hooks[i] && Runtime.hooks[i].detach) Runtime.hooks[i].detach();
            } catch (_) {
            }
        }
        Runtime.hooks = [];
        Runtime.initialized = false;
        stopHeartbeat();
    }

    function enableFeature() {
        if (!installHooks()) {
            return {
                ok: false,
                feature_id: Runtime.feature_id,
                enabled: Runtime.enabled,
                initialized: Runtime.initialized,
                error: Runtime.stats.lastError || 'installHooks failed'
            };
        }

        Runtime.enabled = true;
        startHeartbeat();
        sendStatus('29_bullet_wall_penetration', true);
        Runtime.stats.errorCount = 0;
        Runtime.stats.lastError = '';
        log('info', 'enabled: bullet wall penetration (original damage flow) + projectile wall penetration');
        log('info', '弹体穿墙参数：Environment层=' + environmentLayer() +
            ' 掩码=0x' + environmentMask().toString(16) +
            ' 探路=' + Runtime.config.projectileProbeLookahead + 'm 法线阈值=' + Runtime.config.projectileWallMaxNormalY +
            ' 窗口=' + Runtime.config.projectileIgnoreMinMs + '~' + Runtime.config.projectileIgnoreMaxMs + 'ms' +
            ' AirWall穿透=' + Runtime.config.projectilePenetrateAirWall +
            ' | raycast=' + (native.raycast ? 'OK' : 'MISSING') +
            ' findObject=' + (native.findObjectFromInstanceID ? 'OK' : 'MISSING') +
            ' detectCollisions=' + (native.setDetectCollisions ? 'OK' : 'MISSING') +
            ' ignoreCollision=' + (native.ignoreCollision ? 'OK' : 'MISSING'));
        log('info', '可穿透层掩码=0x' + (Runtime.config.projectilePenetrableLayers >>> 0).toString(16) +
            ' -> ' + penetrableLayerText());
        log('info', '本工程层名表：' + allLayerNamesText());
        return getStatus();
    }

    function disableFeature() {
        Runtime.enabled = false;
        sendStatus('29_bullet_wall_penetration', false);
        forceRestoreGunShootLayerMask('disable');
        releaseEveryIgnore('disable');
        stopHeartbeat();   // enableFeature 会重新 startHeartbeat（installHooks 里那次只在首次安装时执行）
        Runtime.damageDepth = 0;
        Runtime.activeDamageWeapon = ptr(0);
        log('info', 'disabled');
        return getStatus();
    }

    function cleanupFeature() {
        Runtime.enabled = false;
        Runtime.stats.cleanupCount += 1;
        forceRestoreGunShootLayerMask('cleanup');
        releaseEveryIgnore('cleanup');
        cleanupHooks();
        Runtime.damageDepth = 0;
        Runtime.activeDamageWeapon = ptr(0);
        log('info', 'cleanup done');
        return getStatus();
    }

    function toBoundedNumber(value, min, max, fallback) {
        var n = Number(value);
        if (!isFinite(n)) return fallback;
        if (n < min) return min;
        if (n > max) return max;
        return n;
    }

    function updateConfig(input) {
        input = input || {};
        if (input.forceHitboxOnlyDuringLocalDamage !== undefined) {
            Runtime.config.forceHitboxOnlyDuringLocalDamage =
                input.forceHitboxOnlyDuringLocalDamage !== false;
        }
        if (input.logEveryDamageHits !== undefined) {
            var every = Number(input.logEveryDamageHits);
            if (isFinite(every) && every >= 1 && every <= 1000) {
                Runtime.config.logEveryDamageHits = Math.floor(every);
            }
        }
        if (input.projectileWallPenetration !== undefined) {
            Runtime.config.projectileWallPenetration = input.projectileWallPenetration !== false;
            if (!Runtime.config.projectileWallPenetration) releaseEveryIgnore('config-off');
        }
        if (input.projectilePenetrableLayers !== undefined) {
            var mask = Number(input.projectilePenetrableLayers);
            if (isFinite(mask) && mask >= 0) {
                Runtime.config.projectilePenetrableLayers = Math.floor(mask) >>> 0;
            }
        }
        if (input.projectilePenetrateAirWall !== undefined) {
            Runtime.config.projectilePenetrateAirWall = input.projectilePenetrateAirWall === true;
            if (Runtime.config.projectilePenetrateAirWall) {
                // 兼容旧键：打开 AirWall 位
                Runtime.config.projectilePenetrableLayers =
                    (Runtime.config.projectilePenetrableLayers | (1 << 2)) >>> 0;
            }
        }
        if (input.projectileProbeLookahead !== undefined) {
            Runtime.config.projectileProbeLookahead =
                toBoundedNumber(input.projectileProbeLookahead, 0.5, 20, Runtime.config.projectileProbeLookahead);
        }
        if (input.projectileGhostExtra !== undefined) {
            Runtime.config.projectileGhostExtra =
                toBoundedNumber(input.projectileGhostExtra, 0.05, 10, Runtime.config.projectileGhostExtra);
        }
        if (input.projectileWallMaxNormalY !== undefined) {
            Runtime.config.projectileWallMaxNormalY =
                toBoundedNumber(input.projectileWallMaxNormalY, 0.05, 1.0, Runtime.config.projectileWallMaxNormalY);
        }
        if (input.projectileIgnoreMinMs !== undefined) {
            Runtime.config.projectileIgnoreMinMs =
                Math.round(toBoundedNumber(input.projectileIgnoreMinMs, 0, 2000, Runtime.config.projectileIgnoreMinMs));
        }
        if (input.projectileIgnoreMaxMs !== undefined) {
            Runtime.config.projectileIgnoreMaxMs =
                Math.round(toBoundedNumber(input.projectileIgnoreMaxMs, 50, 10000, Runtime.config.projectileIgnoreMaxMs));
        }
        if (Runtime.config.projectileIgnoreMaxMs < Runtime.config.projectileIgnoreMinMs) {
            Runtime.config.projectileIgnoreMaxMs = Runtime.config.projectileIgnoreMinMs;
        }
        log('info', 'config changed: forceHitboxOnlyDuringLocalDamage=' +
            Runtime.config.forceHitboxOnlyDuringLocalDamage +
            ', projectileWallPenetration=' + Runtime.config.projectileWallPenetration +
            ', projectilePenetrableLayers=0x' + (Runtime.config.projectilePenetrableLayers >>> 0).toString(16) +
            ' ' + penetrableLayerText() +
            ', projectilePenetrateAirWall=' + Runtime.config.projectilePenetrateAirWall +
            ', projectileWallMaxNormalY=' + Runtime.config.projectileWallMaxNormalY +
            ', projectileProbeLookahead=' + Runtime.config.projectileProbeLookahead +
            ', projectileGhostExtra=' + Runtime.config.projectileGhostExtra +
            ', projectileIgnoreMinMs=' + Runtime.config.projectileIgnoreMinMs +
            ', projectileIgnoreMaxMs=' + Runtime.config.projectileIgnoreMaxMs);
        return getStatus();
    }

    function getStatus() {
        var liveIgnores = 0;
        var keys = Object.keys(Runtime.missiles);
        for (var i = 0; i < keys.length; i++) {
            var st = Runtime.missiles[keys[i]];
            if (st && st.ignores) liveIgnores += st.ignores.length;
        }
        return {
            ok: Runtime.stats.lastError === '',
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            damage_depth: Runtime.damageDepth,
            active_weapon: isNull(Runtime.activeDamageWeapon) ? '' : Runtime.activeDamageWeapon.toString(),
            current_patch_active: Runtime.currentPatch !== null,
            config: Runtime.config,
            damage_hits: Runtime.stats.damageHits,
            local_damage_hits: Runtime.stats.localDamageHits,
            layer_patch_count: Runtime.stats.layerPatchCount,
            layer_restore_count: Runtime.stats.layerRestoreCount,
            check_wall_hits: Runtime.stats.checkWallHits,
            last_wall_ratio: Runtime.stats.lastWallRatio,
            last_check_wall_result: Runtime.stats.lastCheckWallResult,
            last_hitbox_layer: Runtime.stats.lastHitBoxLayer,
            last_original_gunshoot_mask: Runtime.stats.lastOriginalGunShootMask,
            last_patched_gunshoot_mask: Runtime.stats.lastPatchedGunShootMask,
            skipped_remote_weapon: Runtime.stats.skippedRemoteWeapon,
            error_count: Runtime.stats.errorCount,
            last_error: Runtime.stats.lastError,

            // ---- 弹体穿墙 ----
            projectile_collisions: Runtime.stats.projectileCollisions,
            projectile_local_collisions: Runtime.stats.projectileLocalCollisions,
            projectile_wall_hits: Runtime.stats.projectileWallHits,
            projectile_penetrated: Runtime.stats.projectilePenetrated,
            projectile_tried_explosion: Runtime.stats.projectileTriedExplosion,
            projectile_ignored_pairs: Runtime.stats.projectileIgnoredPairs,
            projectile_released_pairs: Runtime.stats.projectileReleasedPairs,
            projectile_overlap_miss: Runtime.stats.projectileOverlapMiss,
            projectile_vel_fallback: Runtime.stats.projectileVelFallback,
            projectile_sweep_removed: Runtime.stats.projectileSweepRemoved,
            projectile_ray_hits: Runtime.stats.projectileRayHits,
            projectile_ray_wall_hits: Runtime.stats.projectileRayWallHits,
            projectile_ray_floor_likes: Runtime.stats.projectileRayFloorLikes,
            projectile_ghost_starts: Runtime.stats.projectileGhostStarts,
            projectile_ghost_ends: Runtime.stats.projectileGhostEnds,
            projectile_ghost_force_ends: Runtime.stats.projectileGhostForceEnds,
            projectile_ghost_restores: Runtime.stats.projectileGhostRestores,
            projectile_ghost_fail: Runtime.stats.projectileGhostFail,
            projectile_proactive_ignores: Runtime.stats.projectileProactiveIgnores,
            projectile_fixed_seen: Runtime.stats.projectileFixedSeen,
            projectile_fixed_local: Runtime.stats.projectileFixedLocal,
            projectile_fixed_not_mine: Runtime.stats.projectileFixedNotMine,
            projectile_ray_other_layers: Runtime.stats.projectileRayOtherLayers,
            last_probe_layer: Runtime.stats.lastProbeLayer,
            projectile_live_ignores: liveIgnores,
            projectile_tracked: keys.length,
            last_wall_layer: Runtime.stats.lastWallLayer,
            last_wall_normal_y: Runtime.stats.lastWallNormalY,
            last_reject: Runtime.stats.lastReject,
            last_is_my_raw: Runtime.stats.lastIsMyRaw,

            stats: Runtime.stats
        };
    }

    rpc.exports = {
        enable: function (config) {
            if (config) updateConfig(config || {});
            return enableFeature();
        },

        disable: function () {
            return disableFeature();
        },

        status: function () {
            return getStatus();
        },

        cleanup: function () {
            return cleanupFeature();
        },

        setconfig: function (config) {
            return updateConfig(config || {});
        },

        setConfig: function (config) {
            return updateConfig(config || {});
        },

        set_config: function (config) {
            return updateConfig(config || {});
        }
    };

    log('info', 'script loaded; pointerSize=' + Process.pointerSize + ', arch=' + Process.arch);
})();
