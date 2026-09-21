import json
import tempfile
import unittest
from pathlib import Path
import sys


FEATURES_DIR = Path(__file__).resolve().parent
PROJECT_DIR = FEATURES_DIR.parent
sys.path.insert(0, str(PROJECT_DIR))

from core.plugin.manifest_loader import ManifestLoader  # noqa: E402
from core.plugin.module_loader import load_plugin_module  # noqa: E402
from ui.controllers.action_router import ActionRouter  # noqa: E402

PROFILE_MODULE = load_plugin_module(FEATURES_DIR / "33_player_profile_editor", "feature")
PluginFeature = PROFILE_MODULE.PluginFeature


class Feature3233IntegrationTests(unittest.TestCase):
    def test_manifests_register_both_features_in_game_parameters_tab(self):
        manifests = {item["feature_id"]: item for item in ManifestLoader(FEATURES_DIR).load()}
        self.assertIn("brightness_probe", manifests)
        self.assertIn("player_profile_editor", manifests)
        for feature_id in ("brightness_probe", "player_profile_editor"):
            manifest = manifests[feature_id]
            self.assertEqual(manifest["tab"], "game_parameters_tab")
            self.assertEqual(manifest["layout"]["columnspan"], 2)
            self.assertTrue(manifest["display_name"])
        brightness = manifests["brightness_probe"]
        self.assertIn("applybrightness", brightness["rpc"])
        self.assertIn("resetbrightness", brightness["rpc"])
        profile = manifests["player_profile_editor"]
        self.assertFalse(profile["actions"]["load_profile"]["requires_connection"])
        self.assertFalse(profile["actions"]["save_profile"]["requires_connection"])

    def test_card_names_and_path_display_contract(self):
        brightness = json.loads(
            (FEATURES_DIR / "32_brightness_probe" / "manifest.json").read_text(encoding="utf-8")
        )
        profile = json.loads(
            (FEATURES_DIR / "33_player_profile_editor" / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(brightness["display_name"], "亮度调节")
        self.assertEqual(profile["display_name"], "玩家信息修改")
        self.assertEqual(profile["desc"], "读取和修改本地 PlayerData.dat 的昵称、等级和 VIP 等级；修改后，重启游戏生效。")
        brightness_panel = (FEATURES_DIR / "32_brightness_probe" / "panel.py").read_text(encoding="utf-8")
        profile_panel = (FEATURES_DIR / "33_player_profile_editor" / "panel.py").read_text(encoding="utf-8")
        self.assertNotIn("等待连接游戏", brightness_panel)
        self.assertNotIn("需连接游戏后应用", brightness_panel)
        self.assertIn("ctk.CTkLabel(frame, text=path_text", profile_panel)
        self.assertIn("wraplength=", profile_panel)
        self.assertIn("read()", profile_panel)
        self.assertNotIn("CTkEntry(frame, textvariable=path_var", profile_panel)
        self.assertNotIn('state="readonly"', profile_panel)
        self.assertNotIn("askopenfilename", profile_panel)
        self.assertNotIn("备份", profile_panel)
        self.assertNotIn("backup_path", profile_panel)
        self.assertNotIn('text="选择"', profile_panel)

    def test_player_profile_plugin_action_uses_payload_without_game_connection(self):
        feature = PluginFeature()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "PlayerData.dat"
            path.write_text("[Inven]\nDefaultBag=4\n", encoding="utf-8")
            result = feature.save_profile({"path": str(path), "nickname": "测试", "level": 40, "vip_level": 3})
            self.assertTrue(result["ok"])
            self.assertEqual(result["message"], "保存成功，重启游戏后生效")
            loaded = feature.load_profile({"path": str(path)})
            self.assertEqual(loaded["profile"]["nickname"], "测试")
            self.assertEqual(loaded["profile"]["level"], 40)

    def test_player_profile_plugin_returns_validation_error_result(self):
        feature = PluginFeature()
        with tempfile.TemporaryDirectory() as temp_dir:
            result = feature.save_profile({"path": str(Path(temp_dir) / "PlayerData.dat"), "nickname": "", "level": -1, "vip_level": 0})
            self.assertFalse(result["ok"])
            self.assertIn("昵称", result["message"])

    def test_app_syncs_keyed_switch_config_to_plugin_handle(self):
        app_text = (PROJECT_DIR / "ui" / "app.py").read_text(encoding="utf-8")
        self.assertIn('control_type == "switch"', app_text)
        self.assertIn("handle.set(bool(config.get(key", app_text)

    def test_action_router_forwards_local_payload_without_feature_service(self):
        profile_manifest = json.loads(
            (FEATURES_DIR / "33_player_profile_editor" / "manifest.json").read_text(encoding="utf-8")
        )
        feature = PluginFeature(profile_manifest)

        class Registry:
            def get(self, feature_id):
                return feature if feature_id == "player_profile_editor" else None

        class Service:
            def __getattr__(self, name):
                raise AssertionError(f"local action must not call feature service: {name}")

        router = ActionRouter(
            registry=Registry(),
            feature_service=Service(),
            config_manager=None,
            state={},
            is_connected=lambda: False,
            logger=lambda _message: None,
            update_switch=lambda _feature_id: None,
            sync_config=lambda *_args: None,
            schedule_save=lambda: None,
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "PlayerData.dat"
            result = router.action(
                "player_profile_editor",
                "save_profile",
                {"path": str(path), "nickname": "路由测试", "level": 7, "vip_level": 1},
            )
            self.assertTrue(result["ok"])


if __name__ == "__main__":
    unittest.main()
