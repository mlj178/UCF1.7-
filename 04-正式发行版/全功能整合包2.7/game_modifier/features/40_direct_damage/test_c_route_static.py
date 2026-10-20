"""开火直伤/弹体追踪 —— C 路线（根治版）静态回归。

把这条边界钉死在测试里：**本功能不注入伤害、不处理死亡与复活**。

唯一的写操作是「突破复活无敌」(`pierce_respawn_invincible`)：放行原版射线前，
把**选中目标**的三个防御字段（Entity.damageRate / Entity.isInvincible /
HealthData.invinsibleEndTime）复位。它不写血量、不写指针、不调游戏函数，
所以死亡广播与复活调度仍然由原版完成 —— 下面有独立用例锁住这条边界。
以后任何一次改动想恢复注入链路（自己合成 DamageEventData / 跳过原函数 /
死亡兜底），都会先在这里炸掉。

旧版（自己合成伤害 + Interceptor.replace 跳过原函数 + death_fix_broadcast /
death_fix_respawn 兜底）已整体备份到：
    04-正式发行版/_备份_40_direct_damage_注入版_2.7/40_direct_damage/

注释一律先剥掉再断言 —— 文件头的设计说明里会提到旧版做过什么，
那些是"历史"，不该被当成"现在的代码"。
"""

import json
import unittest
from pathlib import Path

FEATURE_DIR = Path(__file__).resolve().parent
SCRIPT_PATH = FEATURE_DIR / "script.js"
MANIFEST_PATH = FEATURE_DIR / "manifest.json"

# 只要这些名字出现在**代码**里，就说明注入/死亡处理回来了
FORBIDDEN_IN_CODE = (
    "Interceptor.replace",
    "Interceptor.revert",
    "GameManager_TakeDamage",
    "DeathEventBroadcast",
    "Entity_OnEntityHurt",
    "Player_OnEntityHurt",
    "HealthData_Hurt",
    "ModeBase_Nano_RespawnPlayer",
    "Player_Respawn",
    "DamageEventData",
    "callGameManagerTakeDamage",
    "callEntityHurt",
    "callPlayerHurt",
    "buildEventDwords",
    "buildDeathEventDwords",
    "applyDamage",
    "directDamage",
    "skipOriginalFromOnEnter",
    "installGunHookReplace",
    "clearTargetInvincibility",
    "readHealthSnapshot",
    "watchDeath",
    "checkDeathWatch",
    "registerDeathWatch",
    "deathRescueTick",
    "death_fix",
    "death_diag",
    "death_rescue",
    "rebroadcast",
    "inDirectDamage",
    "replacedAddresses",
)

# 已经删掉的配置键：manifest.config 和 script.js 里都不允许再出现
RETIRED_CONFIG_KEYS = (
    "damage_entry",
    "gun_hook_mode",
    "entry_fallback",
    "damage_override",
    "use_event_template",
    "fallback_to_original",
    "wpn_key_fallback",
    "death_diag",
    "death_diag_ms",
    "death_diag_detail",
    "death_diag_raise",
    "death_diag_chain",
    "death_fix_wpn",
    "death_fix_respawn",
    "death_fix_broadcast",
    "death_rescue_max_tries",
    "death_rescue_retry_gap_ms",
    "death_respawn_grace_ms",
    "gun_ray_redirect",
)

def script_text():
    return SCRIPT_PATH.read_text(encoding="utf-8")


def manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def strip_comments(text):
    """去掉 // 行注释与 /* */ 块注释。"""
    out = []
    in_block = False
    for line in text.splitlines():
        if in_block:
            if "*/" in line:
                line = line.split("*/", 1)[1]
                in_block = False
            else:
                continue
        while "/*" in line:
            head, rest = line.split("/*", 1)
            if "*/" in rest:
                line = head + rest.split("*/", 1)[1]
            else:
                line = head
                in_block = True
                break
        out.append(line.split("//")[0])
    return "\n".join(out)


def code():
    return strip_comments(script_text())


def block(text, start_marker, end_marker):
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[start:end]


def function_body(text, signature):
    """取一个顶层函数的正文（从签名到下一个顶层函数签名之前）。"""
    chunk = text.split(signature, 1)[1]
    return chunk.split("\n    function ", 1)[0]


def script_config_lines(text):
    """解析 script.js 里 Runtime.config 的字面量默认值，返回 {key: raw_value_text}。"""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == "config: {":
            start = index
            break
    if start is None:
        raise AssertionError("script.js 里找不到 Runtime.config 字面量")
    result = {}
    for line in lines[start + 1:]:
        stripped = line.strip()
        if stripped.startswith("}"):
            break
        if not stripped or stripped.startswith("//"):
            continue
        key, _, rest = stripped.partition(":")
        result[key.strip()] = rest.split("//")[0].strip().rstrip(",")
    return result


def normalize(raw):
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ("'", '"'):
        return raw[1:-1]
    if raw == "true":
        return True
    if raw == "false":
        return False
    try:
        return float(raw)
    except ValueError:
        return raw


class CrouteBoundaryTests(unittest.TestCase):

    def test_code_contains_no_damage_injection_or_death_handling(self):
        offenders = [token for token in FORBIDDEN_IN_CODE if token in code()]
        self.assertEqual(
            offenders, [],
            "C 路线不允许注入伤害/处理死亡复活，发现残留符号：%s" % offenders,
        )

    def test_rva_table_has_no_damage_or_death_entries(self):
        table = block(code(), "var RVA = {", "};")
        for token in (
            "TakeDamage",
            "DeathEventBroadcast",
            "OnEntityHurt",
            "HealthData_Hurt",
            "RespawnPlayer",
            "Player_Respawn",
            "GameRoundEnd",
            "NewGameRoundStart",
            "Il2Cpp_Exception_Raise",
        ):
            self.assertNotIn(token, table, "RVA 表里仍有 %s" % token)

    def test_offset_table_has_no_damage_event_or_death_structs(self):
        table = block(code(), "var OFF = {", "};")
        # 伤害事件结构 / 死亡结构一律不许回到偏移表
        for token in ("Dmg_", "Death_"):
            self.assertNotIn(token, table, "偏移表里仍有 %s" % token)

    def test_defense_state_offsets_are_pinned_to_the_dump(self):
        """防御状态三个偏移必须与 dump.cs / IDA 反汇编一致。

        Entity.<damageRate>k__BackingField    +0x14  (get_damageRate: fld [eax+14h])
        Entity.<isInvincible>k__BackingField  +0x18  (get_isInvincible: mov al,[eax+18h])
        HealthData.invinsibleEndTime          +0x44
        偏移一旦漂移，写出去的就是别的字段 —— 这是「突破复活无敌」唯一的危险点。
        """
        table = block(code(), "var OFF = {", "};")
        for name, value in (
            ("Entity_damageRate", "0x14"),
            ("Entity_isInvincible", "0x18"),
            ("HealthData_invinsibleEndTime", "0x44"),
        ):
            self.assertIn(name + ": " + value, table, "%s 偏移不对" % name)

    def test_native_bindings_cannot_deal_damage(self):
        table = block(code(), "var native = {", "};").lower()
        for token in ("takedamage", "hurt", "respawn", "deathbroadcast"):
            self.assertNotIn(token, table, "native 里仍有 %s" % token)

    def test_gun_hook_is_attach_only_and_never_skips_the_original(self):
        body = function_body(code(), "function installGunHook()")
        self.assertIn("registerAttach(", body)
        self.assertIn("RVA.WPN_Gun_Damage", body)
        self.assertIn("redirectRayToTarget(this)", body)
        # 没有 onLeave = 没有"打完核对血量、没掉血再补一发"的兜底
        self.assertNotIn("onLeave", body)

    def test_ray_redirect_writes_ray_dir_then_gated_defense_reset(self):
        body = function_body(code(), "function redirectRayToTarget(ctx)")
        for offset in ("sp.add(20).writeFloat(", "sp.add(24).writeFloat(", "sp.add(28).writeFloat("):
            self.assertIn(offset, body)
        # 防御复位必须被开关包住，并且只发生在"射线已经写成功"之后
        self.assertIn("if (Runtime.config.pierce_respawn_invincible) {", body)
        self.assertLess(body.index("sp.add(28).writeFloat("), body.index("clearDefenseBeforeShot("))
        for forbidden in ("writeU32", "writeS32", "writePointer", "Hurt", "TakeDamage",
                          "damageApplied", "HealthData_Hurt"):
            self.assertNotIn(forbidden, body, "射线接管只允许写 rayDir + 防御状态，出现了 %s" % forbidden)

    def test_defense_state_read_is_read_only(self):
        body = function_body(code(), "function readDefenseState(victim)")
        self.assertNotIn("write", body, "readDefenseState 必须是只读的")

    def test_defense_state_has_a_plausibility_gate(self):
        """指针被回收/复用时，字段会读成天文数字；必须拒绝，而不是照着写。"""
        body = function_body(code(), "function readDefenseState(victim)")
        self.assertIn("implausible defense state", body)
        self.assertIn("damageRate <= 10", body)

    def test_defense_reset_only_touches_three_fields(self):
        body = function_body(code(), "function clearDefenseBeforeShot(victim)")
        for token in ("writeFloat(0)", "writeFloat(1.0)", "writeU8(0)"):
            self.assertIn(token, body)
        # 只复位「完全免疫」（复活保护 rate=0），部分减伤/护盾必须原样保留
        self.assertIn("before.damageRate < 0.001", body)
        for forbidden in ("writePointer", "writeU32", "writeS32", "Hurt", "TakeDamage",
                          "NativeFunction", "Interceptor"):
            self.assertNotIn(forbidden, body, "突破复活无敌只允许写三个防御字段，出现了 %s" % forbidden)

    def test_defense_reset_skips_inactive_or_unreadable_targets(self):
        body = function_body(code(), "function clearDefenseBeforeShot(victim)")
        self.assertIn("if (!before.ok)", body)
        self.assertIn("if (!before.active) return before;", body)
        self.assertIn("invincibleUnreadable", body)

    def test_explosion_pierce_is_attach_only_and_ours_only(self):
        text = code()
        self.assertIn("WPN_GRENADE_CreateExplosion: 0x00B5CC40", block(text, "var RVA = {", "};"))
        hook = function_body(text, "function installExplosionDefenseHook()")
        self.assertIn("registerAttach(", hook)
        self.assertIn("sp.add(0x14).readFloat()", hook)   # range
        self.assertIn("sp.add(0x20).readPointer()", hook)  # DamageEventData
        self.assertNotIn("onLeave", hook)
        self.assertNotIn("Interceptor", hook)

        helper = function_body(text, "function pierceExplosionDefense(attacker, worldPos, range)")
        self.assertIn("samePointer(attacker, myPlayer)", helper, "必须只处理自己的爆炸")
        self.assertIn("isEnemyTeam", helper)
        self.assertIn("clearDefenseBeforeShot(candidate)", helper)
        for forbidden in ("writeFloat", "writeU8", "writePointer", "TakeDamage", "Hurt"):
            self.assertNotIn(forbidden, helper, "爆炸穿透只允许调用 clearDefenseBeforeShot，出现了 %s" % forbidden)

    def test_install_hooks_registers_the_explosion_pierce(self):
        body = function_body(code(), "function installHooks()")
        self.assertIn("installExplosionDefenseHook()", body)

    def test_pierce_respawn_invincible_is_a_manifest_switch_default_on(self):
        data = manifest()
        self.assertTrue(data["config"]["pierce_respawn_invincible"])
        labels = {c.get("key"): c.get("label") for c in data["controls"]}
        self.assertIn("复活", labels["pierce_respawn_invincible"])
        self.assertIn("pierce_respawn_invincible_var", data["ui_handles"])

    def test_explosive_and_skill_paths_never_inject_damage(self):
        text = code()
        for signature in (
            "function handleTrigger(weapon, category, sourceLabel, missileDataOffset)",
            "function installExplosiveHooks()",
            "function installSkillHooks()",
        ):
            body = function_body(text, signature)
            for forbidden in ("applyDamage", "directDamage", "TakeDamage", "Hurt"):
                self.assertNotIn(forbidden, body, "%s 里出现了 %s" % (signature, forbidden))

    def test_no_round_or_death_lifecycle_hooks_are_installed(self):
        text = code()
        install_body = function_body(text, "function installHooks()")
        for token in ("Death", "Round", "Respawn", "Pipeline", "Template", "StringCapture"):
            self.assertNotIn(token, install_body, "installHooks 里仍在安装 %s 相关钩子" % token)

    def test_retired_config_keys_are_gone_from_manifest_and_script(self):
        manifest_keys = set(manifest()["config"])
        script_keys = set(script_config_lines(script_text()))
        for key in RETIRED_CONFIG_KEYS:
            self.assertNotIn(key, manifest_keys, "manifest.config 仍有 %s" % key)
            self.assertNotIn(key, script_keys, "script.js 仍有 %s" % key)

    def test_manifest_config_matches_script_defaults(self):
        expected = manifest()["config"]
        actual = script_config_lines(script_text())
        for key, want in expected.items():
            self.assertIn(key, actual, "script.js 没有为 %s 提供默认值" % key)
            got = normalize(actual[key])
            if isinstance(want, (int, float)) and not isinstance(want, bool):
                self.assertAlmostEqual(float(got), float(want), places=4, msg="%s 默认值不一致" % key)
            else:
                self.assertEqual(got, want, "%s 默认值不一致" % key)

    def test_manifest_ui_handles_cover_every_setconfig_control(self):
        data = manifest()
        handles = data.get("ui_handles", {})
        for control in data["controls"]:
            if control.get("type") == "switch" and control.get("key"):
                self.assertIn(control["key"] + "_var", handles)
        self.assertIn("switch", handles)

    def test_rpc_surface_keeps_the_debug_entry_points(self):
        text = script_text()
        for name in (
            "enable:",
            "disable:",
            "status:",
            "cleanup:",
            "setConfig:",
            "logs:",
            "clearLogs:",
            "setLogFile:",
            "dump:",
            "snapshot:",
        ):
            self.assertIn(name, text, "RPC %s 被删掉了" % name)

    def test_script_still_implements_both_kept_routes(self):
        text = script_text()
        for token in (
            "enable_guns",
            "enable_explosives",
            "enable_skill_projectiles",
            "function armMissileHoming(",
            "function steerMissile(",
            "function redirectRayToTarget(",
        ):
            self.assertIn(token, text)

    def test_gun_switches_are_merged_into_one_user_facing_switch(self):
        data = manifest()
        controls = [c for c in data["controls"] if c.get("type") == "switch"]
        keys = [c.get("key") for c in controls if c.get("key")]
        self.assertIn("enable_guns", keys)
        self.assertNotIn("gun_ray_redirect", keys)
        self.assertNotIn("gun_ray_redirect", data["config"])
        self.assertNotIn("gun_ray_redirect", script_text())

        gun_control = [c for c in controls if c.get("key") == "enable_guns"][0]
        self.assertEqual(gun_control.get("label"), "普通枪械自动跟枪")
        self.assertIn("不额外改伤", data["desc"])
        self.assertIn("按准星方向射击", data["desc"])
        self.assertNotIn("射线接管", data["desc"])

    def test_unified_target_policy_matches_aim_and_replaces_distance_first_modes(self):
        text = code()
        for token in (
            "target_outer_cone_deg: 30.0",
            "target_inner_cone_deg: 20.0",
            "target_angle_tie_deg: 1.0",
            "target_switch_margin_deg: 1.2",
            "target_switch_confirm_scans: 1",
            "target_switch_cooldown_ms: 100",
            "function selectTargetFromCandidates(candidates, nowMs)",
            "function pickBestCandidate(candidates, innerConeDeg, angleTieDeg)",
            "function candidateIsBetter(a, b, angleTieDeg)",
            "function pickNearestCandidate(candidates, maxDistance)",
        ):
            self.assertIn(token, text)

        for retired in (
            "TARGET_MODE",
            "target_mode",
            "max_angle_deg",
            "angle_weight",
            "distance_weight",
            "homing_cone_deg",
            "homing_cone_fallback",
        ):
            self.assertNotIn(retired, text, "旧的距离优先目标策略残留：%s" % retired)

    def test_gun_and_missile_paths_use_the_same_cone_and_ranking(self):
        text = code()
        gun = function_body(text, "function selectTarget(myPlayer, eyePos, rotation)")
        self.assertIn("targetPolicy()", gun)
        self.assertIn("selectTargetFromCandidates(coneCandidates, Date.now())", gun)
        self.assertIn("pickNearestCandidate(allCandidates", gun)
        self.assertIn("angleDeg > policy.outerConeDeg", gun)

        launch = function_body(text, "function pickEnemyForLaunch()")
        self.assertIn("var policy = targetPolicy()", launch)
        self.assertIn("scanEnemies(eye, { yawDeg: rot.yawDeg, pitchDeg: rot.pitchDeg }, policy)", launch)
        self.assertIn("pickNearestCandidate(scan.allCandidates", launch)

        retarget = function_body(text, "function pickEnemyForMissileRetarget(mpos, rb)")
        self.assertIn("var policy = targetPolicy()", retarget)
        self.assertIn("pickNearestCandidate(scan.allCandidates", retarget)


if __name__ == "__main__":
    unittest.main()
