"""子弹穿墙/弹体穿墙 —— 静态护栏。

只做"源码里该有什么、不该有什么"的静态断言，不连接游戏。
重点锁死几件容易回归的事：
    1) 主动穿墙（主路径）：物理步里提前射线探路 -> 关掉这一颗弹体的 detectCollisions
       -> 离开墙体后必须还原。绝不能只关不还原（下一颗弹会飞穿全场）。
    2) 反应式兜底：临时抑制 expWhenTouchSth + Physics.IgnoreCollision 单面墙 + 写回速度，
       而不是 Interceptor.replace（和 40 的诊断探针共用同一批地址，replace 会抢控制流）。
    3) 必须有可观测的诊断（[beat] 汇总 + 每次弹体碰撞一行日志），否则"没生效"只能猜。
    4) 卡片标题「子弹穿墙/弹体穿墙」和 40 面板里用来找本卡开关的标题必须一致
       （40 面板按可见标题反查开关，改名不同步会让联动提示永远查不到开关）。
"""

import json
import unittest
from pathlib import Path


FEATURE_DIR = Path(__file__).resolve().parent
SCRIPT_PATH = FEATURE_DIR / "script.js"
MANIFEST_PATH = FEATURE_DIR / "manifest.json"
PANEL_40_PATH = FEATURE_DIR.parent / "40_direct_damage" / "panel.py"


def script_text():
    return SCRIPT_PATH.read_text(encoding="utf-8")


class ProjectileWallPenetrationStaticTests(unittest.TestCase):

    def test_script_keeps_bullet_wall_penetration_untouched(self):
        text = script_text()
        for token in [
            "WPN_Gun_Damage: 0x00B613D0",
            "WeaponLogic_CheckWall: 0x00B78F80",
            "LayerConstant_LM_GunShoot: 0x38",
            "patchGunShootLayerMask",
            "restoreGunShootLayerMask",
            "forceRestoreGunShootLayerMask",
            "readWallShotDamageRatio",
        ]:
            self.assertIn(token, text)
        # 子弹穿墙依旧复用原版伤害流程，不许改成 replace
        self.assertNotIn("Interceptor.replace", text)

    def test_projectile_rvas_are_pinned(self):
        text = script_text()
        for token in [
            "WPN_Missile_SetWeaponData: 0x00B663C0",
            "WPN_Missile_FixedUpdate: 0x00B660C0",
            "WPN_Missile_OnCollisionEnter: 0x00B66100",
            "WPN_GRENADE_OnCollisionEnter: 0x00B5D0F0",
            "WPN_Missile_Recycle: 0x00B66240",
            "Player_get_isMyPlayer: 0x00B55FD0",
            "Physics_IgnoreCollision: 0x00AB9A00",
            "Physics_OverlapSphere: 0x00AB9F00",
            "Collider_get_attachedRigidbody: 0x00AB85B0",
            "Collision_get_contacts: 0x00AB8710",
            "GameObject_get_layer: 0x00331FB0",
            "Rigidbody_set_velocity: 0x00ABC060",
            "Physics_Raycast: 0x00ABAC10",
            "Rigidbody_set_detectCollisions: 0x00ABBF00",
            "Object_FindObjectFromInstanceID: 0x004E9570",
        ]:
            self.assertIn(token, text)

    def test_suppresses_wall_explosion_without_replacing_the_function(self):
        text = script_text()
        self.assertIn("WPN_GRENADE_expWhenTouchSth: 0x74", text)
        # 原版 OnCollisionEnter 尾部：cmp byte [esi+74h],0 -> jz ret，否则 TryExplosion
        self.assertIn("projectileTriedExplosion", text)
        grenade_hook = text.split("attachHook('WPN_GRENADE.OnCollisionEnter'", 1)[1].split("});", 1)[0]
        self.assertIn("readU8()", grenade_hook)
        self.assertIn("writeU8(0)", grenade_hook)
        self.assertIn("writeU8(this.savedFlag)", grenade_hook)

    def test_only_local_player_projectiles_and_only_side_walls(self):
        text = script_text()
        self.assertIn("function isLocalMissile(missile)", text)
        self.assertIn("native.isMyPlayer", text)
        self.assertIn("LayerConstant_Environment: 0x00", text)
        self.assertIn("function readContactNormalY(collision)", text)
        self.assertIn("projectileWallMaxNormalY", text)
        # 读不到接触法线时保守按地板处理（不穿透），避免误伤滚雷/落地逻辑
        self.assertIn("Runtime.stats.lastReject = 'noNormal'", text)

    def test_native_bool_is_never_compared_with_strict_true(self):
        """原生 bool 返回值不保证是 JS 的 true —— 本项目已踩过这个坑。

        表现：功能显示"已启用"，但所有身份/探路判定全部失败（isLocalMissile 恒 false、
        raycast 恒"没命中"），日志里全是 notMine / 探路射线=0，看起来像"钩子没生效"。
        40_direct_damage 里同名的 toFlag() 就是为这个问题加的。
        """
        text = script_text()
        self.assertIn("function toFlag(value)", text)
        self.assertIn("return toFlag(native.isMyPlayer(player, ptr(0)));", text)
        self.assertIn("return toFlag(native.isMyWeapon(weapon, ptr(0)));", text)
        self.assertIn("if (!toFlag(ok)) return null;", text)
        offenders = []
        for number, line in enumerate(text.splitlines(), 1):
            code = line.split("//")[0]
            if "native." in code and ("=== true" in code or "!== true" in code):
                offenders.append("%d: %s" % (number, line.strip()))
        self.assertEqual(
            offenders, [],
            "原生 bool 不能用 === true 判定，请统一走 toFlag()：%s" % offenders,
        )

    def test_proactive_ghost_mode_stops_and_restores_collisions(self):
        text = script_text()
        # 主路径：物理步里提前探路，命中墙面就关掉该弹体的物理碰撞
        self.assertIn("function tickMissileGhost(st, missile, rb, pos, v)", text)
        self.assertIn("function probeAhead(pos, v, maxDistance)", text)
        self.assertIn("native.raycast(", text)
        self.assertIn("RaycastHit_normal: 0x0C", text)
        self.assertIn("RaycastHit_collider: 0x28", text)
        self.assertIn("native.setDetectCollisions(rb, on ? 1 : 0, ptr(0))", text)
        self.assertIn("setDetectCollisions(rb, 0)", text)
        self.assertIn("setDetectCollisions(rb, 1)", text)
        self.assertIn("projectileProbeLookahead", text)
        self.assertIn("projectileGhostExtra", text)
        # 探路必须反查"命中物在哪一层"，不能只靠 mask 猜
        self.assertIn("native.findObjectFromInstanceID", text)
        self.assertIn("isPenetrableWallLayer(layer)", text)
        # 主选必须是"只忽略这一颗弹 × 这一面墙"（作用域最小，地板不受影响），
        # detectCollisions 只能作为拿不到 collider 时的备选
        ghost_fn = text.split("function tickMissileGhost(st, missile, rb, pos, v)", 1)[1].split("function restoreGhost", 1)[0]
        self.assertIn("ignoreWallForMissile(missile, rb, pos, hit.collider, st, hit.plane)", ghost_fn)
        # 返回值语义：>0 新忽略 / -1 早就忽略过（都算成功）/ 0 失败
        self.assertIn("if (samePointer(st.ignores[k].wall, wall)) return -1;", text)
        self.assertIn("if (applied !== 0) {", ghost_fn)
        self.assertLess(
            ghost_fn.index("if (applied !== 0) {"),
            ghost_fn.index("setDetectCollisions(rb, 0)"),
            "主选必须是 IgnoreCollision，detectCollisions 只能在后面兜底",
        )
        self.assertIn("projectileProactiveIgnores", text)
        # 还原必须由"真的穿过墙面"触发：主动忽略会带上墙面平面（撞点+法线）
        self.assertIn("RaycastHit_point: 0x00", text)
        self.assertIn("plane: plane", text)
        self.assertIn("crossed = (ox * entry.nx + oy * entry.ny + oz * entry.nz) < -0.30;", text)
        # 物理步钩子必须真的调用主动穿墙
        fixed_update = text.split("attachHook('WPN_Missile.FixedUpdate'", 1)[1].split("// 基类碰撞", 1)[0]
        self.assertIn("tickMissileGhost(st, missile, rb, pos, v)", fixed_update)

    def test_ghost_mode_is_always_restored(self):
        text = script_text()
        drop_fn = text.split("function dropMissileState(missile, reason, releaseIgnores)", 1)[1].split("function readRigidbodyVelocity", 1)[0]
        self.assertIn("restoreGhost(st, reason || 'drop')", drop_fn)
        release_fn = text.split("function releaseEveryIgnore(reason)", 1)[1].split("function cleanupHooks", 1)[0]
        self.assertIn("restoreGhost(st, reason)", release_fn)
        sweep_fn = text.split("function sweepMissileStates()", 1)[1].split("function releaseEveryIgnore", 1)[0]
        self.assertIn("restoreGhost(st, 'sweep')", sweep_fn)
        # 关掉弹体穿墙开关时也要还原
        config_fn = text.split("function updateConfig(input)", 1)[1].split("function getStatus", 1)[0]
        self.assertIn("releaseEveryIgnore('config-off')", config_fn)

    def test_has_observable_diagnostics(self):
        text = script_text()
        self.assertIn("function logProjectileBeat()", text)
        self.assertIn("[beat] 弹体穿墙", text)
        self.assertIn("function logMissileCollision(missile, hit)", text)
        self.assertIn("logMissileCollision(args[0], hit)", text)
        for key in [
            "projectile_ray_hits",
            "projectile_ray_wall_hits",
            "projectile_ray_other_layers",
            "projectile_ghost_starts",
            "projectile_ghost_ends",
            "projectile_ghost_restores",
            "projectile_fixed_seen",
            "last_probe_layer",
        ]:
            self.assertIn(key, text)

    def test_ignore_is_windowed_and_always_reversible(self):
        text = script_text()
        self.assertIn("function releaseIgnore(entry, reason)", text)
        self.assertIn("function releaseAllIgnores(st, reason)", text)
        self.assertIn("function tickMissileIgnores(st, pos)", text)
        self.assertIn("projectileIgnoreMinMs", text)
        self.assertIn("projectileIgnoreMaxMs", text)
        # IgnoreCollision(true) 与 (false) 必须成对出现
        self.assertIn("native.ignoreCollision(mine[i], wall, 1, ptr(0));", text)
        self.assertIn("native.ignoreCollision(entry.mine[i], entry.wall, 0, ptr(0));", text)
        # 关闭 / 卸载 / 回池 / 心跳都要还原
        disable_fn = text.split("function disableFeature()", 1)[1].split("function cleanupFeature()", 1)[0]
        cleanup_fn = text.split("function cleanupFeature()", 1)[1].split("function updateConfig", 1)[0]
        self.assertIn("releaseEveryIgnore('disable')", disable_fn)
        self.assertIn("releaseEveryIgnore('cleanup')", cleanup_fn)
        self.assertIn("dropMissileState(args[0], 'recycle')", text)
        self.assertIn("releaseAllIgnores(st, 'sweep')", text)

    def test_inside_wall_test_filters_out_the_missile_own_collider(self):
        text = script_text()
        # Physics.CheckSphere 只看 layerMask，会把弹体自己的 collider 也算进去，
        # 导致"永远还在墙里"、永远不还原 —— 必须用 OverlapSphere + attachedRigidbody 过滤。
        self.assertNotIn("Physics_CheckSphere", text)
        self.assertNotIn("native.checkSphere", text)
        inside_fn = text.split("function insideEnvironment(pos, rb)", 1)[1].split("function tickMissileIgnores", 1)[0]
        self.assertIn("native.overlapSphere", inside_fn)
        self.assertIn("native.getAttachedRigidbody", inside_fn)
        self.assertIn("samePointer(crb, rb)", inside_fn)

    def test_velocity_cache_is_taken_in_fixed_update(self):
        text = script_text()
        self.assertIn("function readRigidbodyVelocity(rb)", text)
        self.assertIn("function writeRigidbodyVelocity(rb, v)", text)
        fixed_update = text.split("attachHook('WPN_Missile.FixedUpdate'", 1)[1].split("// 基类碰撞", 1)[0]
        self.assertIn("st.v = v", fixed_update)
        self.assertIn("st.rb = rb", fixed_update)
        # 速度写回必须能退化成 Collision.relativeVelocity
        self.assertIn("Collision_relativeVelocity: 0x14", text)
        self.assertIn("source = 'relativeVelocity'", text)

    def test_rpc_and_status_surface(self):
        text = script_text()
        self.assertIn("rpc.exports", text)
        for export_name in ["enable", "disable", "status", "cleanup", "setconfig"]:
            self.assertRegex(text, rf"\b{export_name}\s*:")
        for key in [
            "projectile_wall_hits",
            "projectile_penetrated",
            "projectile_ignored_pairs",
            "projectile_released_pairs",
            "projectile_live_ignores",
            "projectile_vel_fallback",
            "last_reject",
        ]:
            self.assertIn(key, text)

    def test_manifest_rename_and_config_defaults(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest["display_name"], "子弹穿墙/弹体穿墙")
        self.assertEqual(manifest["feature_id"], "29_bullet_wall_penetration")
        self.assertEqual(manifest["script"], "script.js")
        config = manifest["config"]
        self.assertTrue(config["projectileWallPenetration"])
        self.assertFalse(config["projectilePenetrateAirWall"])   # 兼容键
        # 默认可穿透层 = 除角色/命中盒层外全部（0xFFFFFA77）；收窄靠这个掩码
        self.assertEqual(config["projectilePenetrableLayers"], 0xFFFFFA77)
        self.assertIn("projectilePenetrateAirWall", SCRIPT_PATH.read_text(encoding="utf-8"))
        self.assertLessEqual(config["projectileIgnoreMinMs"], config["projectileIgnoreMaxMs"])

    def test_link_hint_card_title_matches_the_29_manifest(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        panel_40 = PANEL_40_PATH.read_text(encoding="utf-8")
        self.assertIn(
            'WALL_CARD_TITLE = "%s"' % manifest["display_name"],
            panel_40,
            "40 面板按可见标题反查本卡开关，改名后必须同步 WALL_CARD_TITLE",
        )


if __name__ == "__main__":
    unittest.main()
