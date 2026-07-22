import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FEATURES = ROOT / "features"
CHECK_ARCHITECTURE = ROOT / "tools" / "check_architecture.py"
CONFIG = ROOT / "core" / "config.py"
HOTKEY_MANAGER = ROOT / "core" / "hotkey_manager.py"
APP = ROOT / "ui" / "app.py"
SETTINGS_WINDOW = ROOT / "ui" / "settings_window.py"
REPO_ROOT = ROOT.parents[2]
DAMAGE_MULTIPLIER_DOC = REPO_ROOT / "05-正式功能" / "30-增加伤害倍率" / "增加伤害倍率-简要说明.md"


def read_text(path):
    return path.read_text(encoding="utf-8")


def read_json(path):
    return json.loads(read_text(path))


class Feature30And31PluginIntegrationTests(unittest.TestCase):
    def test_damage_multiplier_manifest_uses_stable_id_and_weapon_tab(self):
        plugin_dir = FEATURES / "30_damage_multiplier"
        manifest = read_json(plugin_dir / "manifest.json")

        self.assertEqual(manifest["feature_id"], "damage_multiplier")
        self.assertEqual(manifest["canonical_id"], "damage_multiplier")
        self.assertEqual(manifest["display_name"], "调整伤害倍率")
        self.assertEqual(manifest["desc"], "缩小/放大玩家造成的输出伤害。")
        self.assertEqual(manifest["tab"], "weapon_tab")
        self.assertEqual(manifest["tab_title"], "武器")
        self.assertEqual(manifest["script"], "script.js")
        self.assertEqual(manifest["runtime"]["type"], "plugin_script")
        self.assertEqual(manifest["layout"]["card_type"], "simple")
        self.assertEqual(manifest["layout"]["columnspan"], 1)
        self.assertTrue(manifest["state"]["sync_enabled_from_config"])
        self.assertEqual(manifest["config"]["multiplier"], 2.0)
        self.assertIn("setConfig", manifest["rpc"])
        self.assertIn("set_config", manifest["rpc"])
        self.assertIn("setconfig", manifest["rpc"])
        self.assertNotIn("resetstats", manifest["rpc"])
        self.assertNotIn("resetstats", manifest.get("actions", {}))
        self.assertNotIn("button", {control.get("type") for control in manifest["controls"]})
        self.assertNotIn("重置统计", read_text(plugin_dir / "panel.py"))
        self.assertNotIn("resetstats", read_text(plugin_dir / "script.js"))
        self.assertFalse(manifest["lifecycle"]["requires_room_ready_reapply"])
        self.assertFalse(manifest["lifecycle"]["room_ready_retry"])
        self.assertIn("room_ready_reapply_exempt_reason", manifest["lifecycle"])

    def test_fixed_point_teleport_manifest_uses_stable_id_and_point_actions(self):
        plugin_dir = FEATURES / "31_fixed_point_teleport"
        manifest = read_json(plugin_dir / "manifest.json")

        self.assertEqual(manifest["feature_id"], "fixed_point_teleport")
        self.assertEqual(manifest["canonical_id"], "fixed_point_teleport")
        self.assertEqual(manifest["display_name"], "定点瞬移")
        self.assertEqual(manifest["tab"], "other_tab")
        self.assertEqual(manifest["tab_title"], "其他")
        self.assertEqual(manifest["script"], "script.js")
        self.assertEqual(manifest["runtime"]["type"], "plugin_script")
        self.assertTrue(manifest["state"]["sync_enabled_from_config"])
        for rpc_name in ("savepoint", "teleporttopoint", "setConfig", "set_config", "setconfig"):
            self.assertIn(rpc_name, manifest["rpc"])
        for action_name in ("savepoint", "teleporttopoint"):
            self.assertIn(action_name, manifest["actions"])
        controls_by_action = {
            control.get("action"): control
            for control in manifest["controls"]
            if control.get("action")
        }
        self.assertEqual(controls_by_action["savepoint"]["label"], "保存当前位置  Alt+1")
        self.assertEqual(controls_by_action["teleporttopoint"]["label"], "瞬移到保存点  Alt+2")
        self.assertNotIn("clearpoint", manifest["rpc"])
        self.assertNotIn("clearpoint", manifest["actions"])
        self.assertNotIn("clearpoint", {control.get("action") for control in manifest["controls"]})
        panel_text = read_text(plugin_dir / "panel.py")
        self.assertIn("快捷键：Alt+1 保存当前位置，Alt+2 瞬移到保存点", panel_text)
        self.assertIn('text_color="#9aa3b2"', panel_text)
        self.assertNotIn("开启后等待进入房间并捕获本地玩家。", panel_text)
        self.assertNotIn("fixed_point_teleport_status_label", panel_text)
        self.assertNotIn("status_label", manifest.get("ui_handles", {}))
        self.assertNotIn("清除保存点", panel_text)
        self.assertNotIn("fixed_point_teleport_clear_btn", panel_text)
        self.assertTrue(manifest["lifecycle"]["requires_room_ready_reapply"])
        self.assertTrue(manifest["lifecycle"]["room_ready_retry"])

    def test_alt_1_and_alt_2_are_dedicated_fixed_point_teleport_actions(self):
        config_text = read_text(CONFIG)
        hotkey_text = read_text(HOTKEY_MANAGER)
        app_text = read_text(APP)
        settings_text = read_text(SETTINGS_WINDOW)

        self.assertIn("DEDICATED_HOTKEY_ACTIONS", config_text)
        self.assertRegex(config_text, r"'alt\+1':\s*\{[^}]*'feature_id':\s*'fixed_point_teleport'[^}]*'action':\s*'savepoint'")
        self.assertRegex(config_text, r"'alt\+2':\s*\{[^}]*'feature_id':\s*'fixed_point_teleport'[^}]*'action':\s*'teleporttopoint'")
        self.assertIn("if pos in DEDICATED_HOTKEY_ACTIONS", hotkey_text)
        self.assertIn("_on_dedicated_hotkey_triggered", hotkey_text)
        self.assertIn("DEDICATED_HOTKEY_ACTIONS", app_text)
        self.assertIn("self._feature_controller.trigger_feature_action(feature_id, action)", app_text)
        self.assertIn("固定绑定", settings_text)
        self.assertIn("DEDICATED_HOTKEY_ACTIONS", settings_text)

    def test_script_rpc_accepts_23_payload_shape_and_aliases(self):
        damage_script = read_text(FEATURES / "30_damage_multiplier" / "script.js")
        teleport_script = read_text(FEATURES / "31_fixed_point_teleport" / "script.js")

        for script in (damage_script, teleport_script):
            self.assertRegex(script, r"enable:\s*function\s*\(\s*config\s*\)")
            self.assertRegex(script, r"cleanup:\s*function\s*\(\s*payload\s*\)")
            self.assertRegex(script, r"setConfig:\s*function\s*\(\s*config\s*\)")
            self.assertRegex(script, r"set_config:\s*function\s*\(\s*config\s*\)")
            self.assertRegex(script, r"setconfig:\s*function\s*\(\s*config\s*\)")

        self.assertIn("lastApplyReason", teleport_script)
        self.assertIn("last_apply_reason", teleport_script)

    def test_feature_py_and_panel_py_stay_inside_plugin_boundary(self):
        expected = {
            "30_damage_multiplier": "damage_multiplier",
            "31_fixed_point_teleport": "fixed_point_teleport",
        }
        forbidden_panel_tokens = ("FridaManager", "core.frida_manager", "context._app", "app._")

        for dirname, feature_id in expected.items():
            plugin_dir = FEATURES / dirname
            feature_py = read_text(plugin_dir / "feature.py")
            panel_py = read_text(plugin_dir / "panel.py")

            self.assertIn("PluginFeatureBase", feature_py)
            self.assertIn(f'feature_id = "{feature_id}"', feature_py)
            self.assertIn('callbacks["toggle"]', panel_py)
            if dirname == "31_fixed_point_teleport":
                self.assertIn('callbacks["action"]', panel_py)
            for token in forbidden_panel_tokens:
                self.assertNotIn(token, panel_py)

    def test_damage_multiplier_doc_omits_infect_and_local_victim_default_notes(self):
        text = read_text(DAMAGE_MULTIPLIER_DOC)

        self.assertIn("# 调整伤害倍率 - 简要说明", text)
        self.assertIn("缩小/放大玩家造成的输出伤害", text)
        self.assertNotIn("# 增加伤害倍率 - 简要说明", text)
        self.assertNotIn("默认只放大本地玩家造成的输出伤害", text)
        self.assertNotIn("默认跳过本地玩家作为受害者", text)
        self.assertNotIn("默认跳过 `DamageType.Infect`", text)
        self.assertNotIn("你自己作为受害者", text)
        self.assertNotIn("感染伤害", text)
        self.assertNotIn("感染伤害暂不纳入倍率", text)

    def test_architecture_checker_knows_stable_ids_map_to_numbered_dirs(self):
        text = read_text(CHECK_ARCHITECTURE)

        self.assertRegex(text, r'"damage_multiplier":\s*"30_damage_multiplier"')
        self.assertRegex(text, r'"fixed_point_teleport":\s*"31_fixed_point_teleport"')


if __name__ == "__main__":
    unittest.main()
