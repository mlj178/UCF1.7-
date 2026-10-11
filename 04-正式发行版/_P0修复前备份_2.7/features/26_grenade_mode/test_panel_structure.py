import importlib.util
import json
import sys
import types
import unittest
from pathlib import Path


FEATURE_DIR = Path(__file__).parent
PANEL_PATH = FEATURE_DIR / "panel.py"
MANIFEST_PATH = FEATURE_DIR / "manifest.json"


def load_panel_module():
    sys.modules.setdefault("customtkinter", types.SimpleNamespace())
    spec = importlib.util.spec_from_file_location("grenade_panel_under_test", PANEL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GrenadePanelStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel = load_panel_module()
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.control_keys = {item["key"] for item in cls.manifest["controls"]}

    def test_exposes_three_independent_card_groups(self):
        self.assertEqual(
            self.panel.CARD_GROUPS,
            (
                "手雷模式",
                "无限手雷",
                "手雷强化",
            ),
        )

    def test_user_switches_cover_each_card(self):
        for key in (
            "lock999_enabled",
            "enable_damage",
            "enable_range",
            "enable_shoot_speed",
            "bot_grenade_mode_enabled",
        ):
            self.assertIn(key, self.control_keys)

    def test_only_grenade_mode_switch_is_session_only(self):
        self.assertFalse(self.panel.should_persist_config("bot_grenade_mode_enabled"))
        self.assertTrue(self.panel.should_persist_config("lock999_enabled"))
        self.assertTrue(self.panel.should_persist_config("enable_damage"))

        config = {
            "bot_grenade_mode_enabled": True,
            "lock999_enabled": True,
            "damage_value": 32.0,
        }
        self.panel.apply_session_defaults(config)
        self.assertFalse(config["bot_grenade_mode_enabled"])
        self.assertTrue(config["lock999_enabled"])
        self.assertEqual(config["damage_value"], 32.0)

    def test_player_chain_throw_is_removed_but_bot_ready_drive_is_preserved(self):
        controls = {
            item["key"]: item
            for item in self.manifest["controls"]
        }
        script = (FEATURE_DIR / "script.js").read_text(encoding="utf-8")

        self.assertNotIn("force_throw_ready_enabled", controls)
        self.assertNotIn("force_throw_ready_scope", controls)
        self.assertFalse(any(key.startswith("force_throw_ready_") for key in self.manifest["config"]))
        self.assertNotIn("forceThrowReady", script)
        self.assertNotIn("pendingThrowReadyTimers", script)
        self.assertNotIn("forceThrowReadyWindows", script)
        self.assertIn("function forceBotThrowReadyDirect", script)
        self.assertIn("bot_throw_drive_force_ready", script)

    def test_dependent_features_require_infinite_grenade(self):
        self.assertTrue(self.panel.requires_infinite_grenade("bot_grenade_mode_enabled"))
        self.assertFalse(self.panel.requires_infinite_grenade("enable_damage"))

    def test_enhancement_rows_keep_slider_and_scope_together(self):
        self.assertEqual(
            self.panel.ENHANCEMENT_GROUPS,
            (
                ("enable_damage", "damage_value", "damage_apply_scope"),
                ("enable_range", "range_value", "range_apply_scope"),
                ("enable_shoot_speed", "shoot_speed_value", "shoot_speed_apply_scope"),
            ),
        )

    def test_page_auto_starts_shared_runtime_when_a_function_is_enabled(self):
        config = {"enable_damage": True}
        self.assertTrue(self.panel.should_auto_start(config, is_enabled=False))
        self.assertFalse(self.panel.should_auto_start(config, is_enabled=True))

    def test_runtime_starts_only_after_connection_is_ready(self):
        config = {"lock999_enabled": True}
        self.assertFalse(self.panel.should_start_runtime(config, is_connected=False, is_enabled=False))
        self.assertTrue(self.panel.should_start_runtime(config, is_connected=True, is_enabled=False))

        disabled_config = {"enable_damage": False, "enable_range": False, "enable_shoot_speed": False, "bot_grenade_mode_enabled": False}
        self.assertFalse(self.panel.should_auto_start(disabled_config, is_enabled=False))

    def test_grenade_mode_is_first(self):
        self.assertEqual(self.manifest["tab_order"], 60)
        self.assertEqual(self.manifest["ui"]["tab_order"], 60)
        self.assertEqual(self.manifest["tab_title"], "手雷功能")
        self.assertEqual(self.manifest["ui"]["tab_title"], "手雷功能")


if __name__ == "__main__":
    unittest.main()
