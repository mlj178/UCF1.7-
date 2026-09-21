import re
import json
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "script.js"
UI_FILE = BASE_DIR / "panel.py"
MANIFEST_FILE = BASE_DIR / "manifest.json"
FEATURE_FILE = BASE_DIR / "feature.py"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class DamageMultiplierStaticTests(unittest.TestCase):

    def test_js_contains_feature_id_rvas_and_damage_event_offsets(self):
        text = read_text(JS_FILE)

        required_tokens = [
            'feature_id: "damage_multiplier"',
            "Entity_OnEntityHurt: 0x00B3F470",
            "Player_OnEntityHurt: 0x00B516B0",
            "Player_get_isMyPlayer: 0x00B55FD0",
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

    def test_js_filters_local_attacker_and_skips_local_victim(self):
        text = read_text(JS_FILE)

        self.assertIn("isLocalPlayer(attacker)", text)
        self.assertIn("isLocalPlayer(victim)", text)
        self.assertIn("skip_local_victim", text)
        self.assertIn("include_infect: false", text)
        self.assertIn("allow_other_damage_type: true", text)

    def test_js_tracks_missile_and_sentry_owners_for_special_sources(self):
        text = read_text(JS_FILE)

        self.assertIn("Runtime.missileOwners", text)
        self.assertIn("Runtime.sentryOwners", text)
        self.assertIn("rememberOwner(Runtime.missileOwners", text)
        self.assertIn("rememberOwner(Runtime.sentryOwners", text)
        self.assertIn("resolveEffectiveAttacker", text)
        self.assertIn("missile_owner_hits", text)
        self.assertIn("sentry_owner_hits", text)

    def test_js_clears_owner_maps_on_round_boundaries_and_validates_owner_pointers(self):
        for path in [JS_FILE]:
            text = read_text(path)

            for token in [
                "GameManager_GameRoundEnd: 0x00AFAA40",
                "GameManager_NewGameRoundStart: 0x00AEBCB0",
                "GameManager_OnDestroy: 0x00AEBD40",
                "function clearOwnerMaps(reason)",
                'clearOwnerMaps("game_round_end")',
                'clearOwnerMaps("new_game_round_start")',
                'clearOwnerMaps("game_manager_destroy")',
            ]:
                self.assertIn(token, text, f"{path.name} missing {token}")

            is_local_fn = text.split("function isLocalPlayer(entityPtr)", 1)[1].split("function ptrKey", 1)[0]
            self.assertIn("!isReadablePtr(entityPtr)", is_local_fn)
            self.assertLess(
                is_local_fn.index("!isReadablePtr(entityPtr)"),
                is_local_fn.index("native.isMyPlayer(entityPtr, ptr(0))"),
            )

            remember_owner_fn = text.split("function rememberOwner", 1)[1].split("function getRememberedOwner", 1)[0]
            self.assertIn("!isReadablePtr(objectPtr)", remember_owner_fn)
            self.assertIn("!isReadablePtr(ownerPtr)", remember_owner_fn)

    def test_js_logs_damage_diagnostics_for_fractional_multiplier_analysis(self):
        for path in [JS_FILE]:
            text = read_text(path)

            for token in [
                "logDamageDiagnostic",
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
                self.assertIn(token, text, f"{path.name} missing {token}")

    def test_js_exports_standard_rpc_status_and_config(self):
        text = read_text(JS_FILE)

        self.assertIn("rpc.exports", text)
        for export_name in ["enable", "disable", "status", "cleanup", "setconfig"]:
            self.assertRegex(text, rf"\b{export_name}\s*:")

        for status_key in [
            "total_hurt_events",
            "multiplied_events",
            "skipped_not_local_attacker",
            "skipped_local_victim",
            "last_original_damage",
            "last_new_damage",
            "last_damage_type",
            "last_wpn_index",
            "multiplier",
        ]:
            self.assertIn(status_key, text)

    def test_panel_delegates_toggle_and_configuration_to_plugin_callbacks(self):
        text = read_text(UI_FILE)

        self.assertIn("import customtkinter as ctk", text)
        self.assertIn("ctk.CTkSwitch", text)
        self.assertIn("ctk.CTkSlider", text)
        self.assertIn('callbacks["toggle"](feature_id)', text)
        self.assertIn('callbacks["set_config"](feature_id, "multiplier", numeric)', text)

    def test_ui_does_not_offer_enemy_or_global_default(self):
        text = read_text(UI_FILE)
        manifest = json.loads(read_text(MANIFEST_FILE))

        self.assertNotRegex(text, re.compile(r"全局伤害|敌人伤害|所有玩家", re.I))
        self.assertEqual(manifest["display_name"], "调整伤害倍率")
        self.assertEqual(manifest["desc"], "放大玩家造成的输出伤害。")
        self.assertNotIn("缩小/放大", manifest["desc"])

    def test_multiplier_range_is_boost_only_in_ui_manifest_and_scripts(self):
        ui_text = read_text(UI_FILE)
        feature_text = read_text(FEATURE_FILE)
        js_texts = [read_text(JS_FILE)]
        manifest = json.loads(read_text(MANIFEST_FILE))
        slider = next(control for control in manifest["controls"] if control.get("key") == "multiplier")

        self.assertIn('from_=float(slider_control.get("min", 0.0))', ui_text)
        self.assertIn('to=float(slider_control.get("max", 20.0))', ui_text)
        self.assertIn("number_of_steps=_steps(slider_control)", ui_text)
        self.assertEqual(slider["min"], 1.0)
        self.assertEqual(slider["max"], 20.0)
        self.assertEqual(manifest["desc"], "放大玩家造成的输出伤害。")
        self.assertIn('desc = "放大玩家造成的输出伤害。"', feature_text)
        for js_text in js_texts:
            self.assertIn("min_multiplier: 1.0", js_text)
            self.assertIn("max_multiplier: 20.0", js_text)

    def test_panel_does_not_enable_the_feature_while_changing_the_slider(self):
        text = read_text(UI_FILE)

        on_change = text.split("def on_change(value):", 1)[1].split("slider = ctk.CTkSlider", 1)[0]
        self.assertIn('callbacks["set_config"](feature_id, "multiplier", numeric)', on_change)
        self.assertNotIn('callbacks["toggle"]', on_change)


if __name__ == "__main__":
    unittest.main()
