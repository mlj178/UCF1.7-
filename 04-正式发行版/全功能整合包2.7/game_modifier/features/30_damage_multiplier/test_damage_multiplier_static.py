import json
import re
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "script.js"
UI_FILE = BASE_DIR / "panel.py"
MANIFEST_FILE = BASE_DIR / "manifest.json"
FEATURE_FILE = BASE_DIR / "feature.py"

MULTIPLIER_KEYS = ("enemy_multiplier", "self_multiplier", "mate_multiplier")
ENABLED_KEYS = ("enemy_enabled", "self_enabled", "mate_enabled")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class DamageMultiplierStaticTests(unittest.TestCase):

    def setUp(self):
        self.manifest = json.loads(read_text(MANIFEST_FILE))

    def test_js_contains_feature_id_rvas_and_damage_event_offsets(self):
        text = read_text(JS_FILE)

        required_tokens = [
            'feature_id: "damage_multiplier"',
            "Entity_OnEntityHurt: 0x00B3F470",
            "Player_OnEntityHurt: 0x00B516B0",
            "Player_get_isMyPlayer: 0x00B55FD0",
            "Entity_get_team: 0x001E0070",
            "SingletonGet: 0x004A8170",
            "GM_Singleton_MethodInfo: 0x00E1CE64",
            "SentryGun_SetData: 0x00B1E030",
            "WPN_Missile_SetOwner: 0x00B66390",
            "Dmg_attacker: 0x00",
            "Dmg_victim: 0x04",
            "Dmg_damage: 0x08",
            "Dmg_type: 0x34",
            "Dmg_damageTag: 0x38",
            "Dmg_wpnIndex: 0x3C",
            "Dmg_wpnSprIndex: 0x40",
            "Dmg_ignoreDmgRate: 0x44",
            "Entity_team: 0x20",
            "GM_allPlayers: 0x1C",
            "GM_playersBL: 0x20",
            "GM_playersGR: 0x28",
        ]

        for token in required_tokens:
            self.assertIn(token, text)

    def test_js_uses_attach_and_modifies_only_damage_field(self):
        text = read_text(JS_FILE)

        self.assertIn("Interceptor.attach", text)
        self.assertNotIn("Interceptor.replace", text)
        self.assertIn("multiplyDamageEvent", text)
        self.assertIn("damageAddr.writeFloat(newDamage)", text)
        self.assertNotIn("Dmg_type).writeS32(4)", text)
        self.assertNotIn("DamageEventData$$TakePlace", text)

    def test_js_supports_enemy_self_and_mate_multipliers(self):
        text = read_text(JS_FILE)

        for token in [
            "enemy_multiplier: 1.0",
            "self_multiplier: 2.0",
            "mate_multiplier: 1.0",
            "enemy_enabled: true",
            "self_enabled: true",
            "mate_enabled: true",
            "function categoryMultiplierKey(category)",
            "function categoryEnabledKey(category)",
            "Runtime.config[categoryMultiplierKey(category)]",
            "Runtime.config[categoryEnabledKey(category)]",
            "SELF: 'self'",
            "MATE: 'mate'",
            "ENEMY: 'enemy'",
        ]:
            self.assertIn(token, text, f"script.js missing {token}")

    def test_js_multiplier_can_go_below_one_and_never_zero(self):
        text = read_text(JS_FILE)
        manifest = self.manifest

        self.assertIn("min_multiplier: 0.1", text)
        self.assertIn("max_multiplier: 10.0", text)
        self.assertNotIn("min_multiplier: 0.0", text)
        self.assertNotIn("min_multiplier: 0,", text)

        for control in manifest["controls"]:
            if control.get("type") == "slider":
                self.assertEqual(control["min"], 0.1, control.get("key"))
                self.assertGreater(control["min"], 0.0, "倍率不允许调到 0")

    def test_js_classifies_attacker_by_team(self):
        text = read_text(JS_FILE)

        for token in [
            "function classifyAttacker(attacker)",
            "function readEntityTeam(entityPtr)",
            "function refreshPlayerCache(force)",
            "function collectPlayers(gm)",
            "function getGameManager()",
            "isLocalPlayer(attacker)",
            "Runtime.localTeam",
            "Runtime.playerCache",
            "Category.UNKNOWN",
            "team !== 2 && Runtime.localTeam !== 2 && team === Runtime.localTeam",
        ]:
            self.assertIn(token, text, f"script.js missing {token}")

        # 邻居阵营逻辑必须与 ExpandUtil.IsSameTeam 一致
        self.assertIn("IsSameTeam", text)

    def test_js_keeps_owner_mapping_for_special_sources(self):
        text = read_text(JS_FILE)

        for token in [
            "Runtime.missileOwners",
            "Runtime.sentryOwners",
            "rememberOwner(Runtime.missileOwners",
            "rememberOwner(Runtime.sentryOwners",
            "resolveEffectiveAttacker",
            "missile_owner_hits",
            "sentry_owner_hits",
        ]:
            self.assertIn(token, text)

    def test_js_clears_owner_maps_and_player_cache_on_round_boundaries(self):
        text = read_text(JS_FILE)

        for token in [
            "GameManager_GameRoundEnd: 0x00AFAA40",
            "GameManager_NewGameRoundStart: 0x00AEBCB0",
            "GameManager_OnDestroy: 0x00AEBD40",
            "function clearOwnerMaps(reason)",
            "function clearPlayerCache(reason)",
            'clearOwnerMaps("game_round_end")',
            'clearPlayerCache("game_round_end")',
            'clearOwnerMaps("new_game_round_start")',
            'clearPlayerCache("new_game_round_start")',
            'clearOwnerMaps("game_manager_destroy")',
            'clearPlayerCache("game_manager_destroy")',
        ]:
            self.assertIn(token, text)

        is_local_fn = text.split("function isLocalPlayer(entityPtr)", 1)[1].split("function readEntityTeam", 1)[0]
        self.assertIn("!isReadablePtr(entityPtr)", is_local_fn)
        self.assertLess(
            is_local_fn.index("!isReadablePtr(entityPtr)"),
            is_local_fn.index("native.isMyPlayer(entityPtr, ptr(0))"),
        )

        remember_owner_fn = text.split("function rememberOwner", 1)[1].split("function getRememberedOwner", 1)[0]
        self.assertIn("!isReadablePtr(objectPtr)", remember_owner_fn)
        self.assertIn("!isReadablePtr(ownerPtr)", remember_owner_fn)

    def test_js_skips_self_inflicted_damage_only_for_self_category(self):
        text = read_text(JS_FILE)

        self.assertIn("skip_local_victim", text)
        self.assertIn("category === Category.SELF", text)
        self.assertIn("skippedLocalVictim", text)

    def test_js_logs_damage_diagnostics_for_fractional_multiplier_analysis(self):
        text = read_text(JS_FILE)

        for token in [
            "logDamageDiagnostic",
            "category=",
            "raw_damage=",
            "multiplier=",
            "new_damage=",
            "trunc=",
            "floor=",
            "round=",
            "ceil=",
            "below_one=",
            "attacker=",
            "effective_attacker=",
            "victim=",
            "victim_is_local=",
            "ignoreDmgRate=",
        ]:
            self.assertIn(token, text)

    def test_js_exports_standard_rpc_status_and_config(self):
        text = read_text(JS_FILE)

        self.assertIn("rpc.exports", text)
        for export_name in ["enable", "disable", "status", "cleanup", "setconfig"]:
            self.assertRegex(text, rf"\b{export_name}\s*:")

        for status_key in [
            "enemy_multiplier",
            "self_multiplier",
            "mate_multiplier",
            "multiplied_enemy",
            "multiplied_self",
            "multiplied_mate",
            "skipped_unknown_attacker",
            "skipped_category_disabled",
            "last_category",
            "local_player_ready",
        ]:
            self.assertIn(status_key, text)

    def test_js_migrates_legacy_single_multiplier_key(self):
        text = read_text(JS_FILE)

        self.assertIn("config.multiplier !== undefined", text)
        self.assertIn("Runtime.config.self_multiplier = clampFloat(", text)

    def test_panel_builds_three_category_rows_with_slider_and_switch(self):
        text = read_text(UI_FILE)

        self.assertIn("import customtkinter as ctk", text)
        self.assertIn("ctk.CTkSwitch", text)
        self.assertIn("ctk.CTkSlider", text)
        self.assertIn('callbacks["toggle"](feature_id)', text)
        self.assertIn('("enemy", "敌人"', text)
        self.assertIn('("self", "自己"', text)
        self.assertIn('("mate", "队友"', text)

        for key in MULTIPLIER_KEYS:
            for suffix in ("_var", "_slider", "_label"):
                handle = key + suffix
                self.assertIn(handle, self.manifest["ui_handles"], f"manifest ui_handles 缺 {handle}")
        for key in ENABLED_KEYS:
            handle = key + "_var"
            self.assertIn(handle, self.manifest["ui_handles"], f"manifest ui_handles 缺 {handle}")

        self.assertIn('cfg_key=key + "_multiplier"', text)
        self.assertIn('cfg_key=key + "_enabled"', text)

    def test_panel_supports_nudging_and_resetting_multipliers(self):
        text = read_text(UI_FILE)

        self.assertIn("slider.set(numeric)", text)
        self.assertIn("NUDGE_STEP = 0.1", text)
        self.assertIn('text="全部 1.0x"', text)
        self.assertIn("refresh_summary", text)

    def test_panel_does_not_enable_the_feature_while_changing_the_slider(self):
        text = read_text(UI_FILE)

        on_change = text.split("def on_slider_change(value", 1)[1].split("slider = ctk.CTkSlider", 1)[0]
        self.assertIn("callbacks[\"set_config\"]", on_change)
        self.assertNotIn('callbacks["toggle"]', on_change)

    def test_panel_marks_weaken_and_boost_values_differently(self):
        text = read_text(UI_FILE)

        self.assertIn("def _value_color(value):", text)
        self.assertIn("if value < 1.0:", text)
        self.assertIn("if value > 1.0:", text)

    def test_manifest_declares_wide_card_and_three_sliders(self):
        manifest = self.manifest

        self.assertEqual(manifest["display_name"], "调整伤害倍率")
        self.assertEqual(manifest["layout"]["card_type"], "wide")
        self.assertEqual(manifest["layout"]["columnspan"], 2)

        sliders = [c for c in manifest["controls"] if c.get("type") == "slider"]
        self.assertEqual([c["key"] for c in sliders], list(MULTIPLIER_KEYS))
        for control in sliders:
            self.assertEqual(control["min"], 0.1)
            self.assertEqual(control["max"], 10.0)
            self.assertEqual(control["step"], 0.1)

        self.assertEqual(manifest["config"]["enemy_multiplier"], 1.0)
        self.assertEqual(manifest["config"]["self_multiplier"], 2.0)
        self.assertEqual(manifest["config"]["mate_multiplier"], 1.0)

    def test_manifest_declares_per_category_enable_switches(self):
        manifest = self.manifest
        keyed_switches = [c for c in manifest["controls"] if c.get("type") == "switch" and c.get("key")]

        self.assertEqual([c["key"] for c in keyed_switches], list(ENABLED_KEYS))
        for control in keyed_switches:
            self.assertTrue(control.get("default"))
            self.assertIn(control["key"], manifest["config"])

        # 总开关必须保留（没有 key 的那一个）
        self.assertTrue(any(c.get("type") == "switch" and not c.get("key") for c in manifest["controls"]))

    def test_manifest_desc_and_feature_desc_mention_three_categories(self):
        manifest = self.manifest
        desc = manifest["desc"]
        for word in ("敌人", "自己", "队友"):
            self.assertIn(word, desc)
        self.assertIn("1.0", desc)

        feature_text = read_text(FEATURE_FILE)
        self.assertIn("敌人 / 自己 / 队友", feature_text)


if __name__ == "__main__":
    unittest.main()
