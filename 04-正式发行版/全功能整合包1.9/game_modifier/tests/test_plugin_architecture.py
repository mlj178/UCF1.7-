import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))


class PluginArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.features_dir = self.root / "features"
        self.data_dir = self.root / "data"
        self.features_dir.mkdir()
        self.data_dir.mkdir()
        (self.features_dir / "__init__.py").write_text("", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def _write_plugin(self, feature_id="sample", tab="weapon_tab"):
        plugin_dir = self.features_dir / feature_id
        plugin_dir.mkdir()
        (plugin_dir / "__init__.py").write_text("", encoding="utf-8")
        manifest = {
            "feature_id": feature_id,
            "canonical_id": "sample_feature",
            "display_name": "Sample",
            "category": "weapon",
            "tab": tab,
            "order": 10,
            "icon": "*",
            "desc": "sample plugin",
            "script": "script.js",
            "layout": {"type": "simple"},
            "controls": [],
            "config": {"enabled": False},
            "rpc": ["enable", "disable", "setConfig", "status", "cleanup"],
            "lifecycle": {"cleanup": True},
        }
        (plugin_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (plugin_dir / "script.js").write_text(
            "rpc.exports = { enable(){}, disable(){}, setConfig(){}, status(){}, cleanup(){} };",
            encoding="utf-8",
        )
        (plugin_dir / "feature.py").write_text(
            "from core.plugin.plugin_base import PluginFeatureBase\n\n"
            "class PluginFeature(PluginFeatureBase):\n"
            "    pass\n",
            encoding="utf-8",
        )
        return manifest

    def test_manifest_loader_skips_template_and_bad_json(self):
        from core.plugin.manifest_loader import ManifestLoader

        manifest = self._write_plugin()
        template_dir = self.features_dir / "_template"
        template_dir.mkdir()
        (template_dir / "manifest.json").write_text("{}", encoding="utf-8")
        bad_dir = self.features_dir / "bad"
        bad_dir.mkdir()
        (bad_dir / "manifest.json").write_text("{bad json", encoding="utf-8")

        loaded = ManifestLoader(self.features_dir).load()

        self.assertEqual([item["feature_id"] for item in loaded], [manifest["feature_id"]])

    def test_contract_warns_but_reports_missing_fields(self):
        from core.plugin.plugin_contract import PluginContract

        warnings = []
        ok = PluginContract(logger=lambda message: warnings.append(message)).validate(
            {"feature_id": "broken"}
        )

        self.assertFalse(ok)
        self.assertTrue(any("display_name" in message for message in warnings))

    def test_registry_loads_feature_instances_by_tab(self):
        from core.plugin.plugin_registry import PluginRegistry

        manifest = self._write_plugin("sample", tab="other_tab")

        registry = PluginRegistry(self.features_dir)
        registry.load()

        feature = registry.get("sample")
        self.assertIsNotNone(feature)
        self.assertEqual(feature.manifest["display_name"], manifest["display_name"])
        self.assertEqual(registry.by_tab("other_tab"), [feature])
        self.assertEqual(registry.enabled_features(), [])

    def test_rpc_client_allows_only_standard_actions(self):
        from core.frida_runtime.rpc_client import RpcClient

        calls = []

        class FakeScriptManager:
            def call(self, feature_id, action, payload=None):
                calls.append((feature_id, action, payload))
                return {"ok": True}

        client = RpcClient(FakeScriptManager())

        self.assertEqual(client.call("sample", "enable"), {"ok": True})
        self.assertEqual(calls, [("sample", "enable", None)])
        with self.assertRaises(ValueError):
            client.call("sample", "rawNativeCall")

    def test_config_manager_merges_default_and_user_by_feature(self):
        from core.config_runtime.config_manager import ConfigManager

        (self.data_dir / "default_config.json").write_text(
            json.dumps({"sample": {"speed": 1, "enabled": False}}),
            encoding="utf-8",
        )
        (self.data_dir / "user_config.json").write_text(
            json.dumps({"sample": {"enabled": True}}),
            encoding="utf-8",
        )

        manager = ConfigManager(self.data_dir)

        self.assertEqual(manager.get("sample"), {"speed": 1, "enabled": True})
        manager.set("sample", {"speed": 2})
        self.assertEqual(manager.get("sample"), {"speed": 2, "enabled": True})


class MigratedOrdinaryFeatureTests(unittest.TestCase):
    ORDINARY_FEATURES = {
        "knife": ("features/feature_04_fast_knife.py", "scripts/04-fast_knife.js"),
        "recoil": ("features/feature_02_no_recoil.py", "scripts/02-no_recoil.js"),
        "ammo": ("features/feature_01_unlimited_ammo.py", "scripts/01-unlimited_ammo.js"),
        "ammoplus": ("features/feature_05_fast_reload_buff.py", "scripts/05-fast_reload_buff.js"),
        "range": ("features/feature_07_knife_attack_range.py", "scripts/07-knife_attack_range.js"),
        "aim": ("features/feature_11_auto_aim.py", "scripts/11-auto_aim.js"),
        "speedgun": ("features/feature_13_fire_rate_auto_sniper.py", "scripts/13-fire_rate_auto_sniper.js"),
        "movespeed": ("features/feature_06_movement_speed.py", "scripts/06-movement_speed.js"),
        "time": ("features/feature_03_unlimited_time.py", "scripts/03-unlimited_time.js"),
        "gravity": ("features/feature_09_high_jump_low_gravity.py", "scripts/09-high_jump_low_gravity.js"),
        "godmode": ("features/feature_12_invincibility.py", "scripts/12-invincibility.js"),
        "skillcd": ("features/feature_17_skill_no_cooldown.py", "scripts/17-skill_no_cooldown.js"),
        "gather": ("features/feature_08_gather_enemies.py", "scripts/08-gather_enemies.js"),
        "isbot": ("features/feature_14_become_bot.py", "scripts/14-become_bot.js"),
        "roundskip": ("features/feature_10_skip_round.py", "scripts/10-skip_round.js"),
        "esp_box": ("features/feature_18_universal_esp_box.py", None),
        "timescale": ("features/feature_20_unity_time_acceleration.py", "scripts/20-unity_time_acceleration.js"),
    }

    REQUIRED_MANIFEST_FIELDS = {
        "feature_id",
        "canonical_id",
        "display_name",
        "category",
        "tab",
        "order",
        "icon",
        "desc",
        "script",
        "layout",
        "controls",
        "config",
        "rpc",
        "lifecycle",
    }

    def test_all_ordinary_features_have_plugin_files_and_real_sources(self):
        for feature_id, (feature_source, script_source) in self.ORDINARY_FEATURES.items():
            with self.subTest(feature_id=feature_id):
                plugin_dir = PROJECT_DIR / "features" / feature_id
                self.assertTrue((plugin_dir / "manifest.json").exists())
                self.assertTrue((plugin_dir / "feature.py").exists())
                self.assertTrue((plugin_dir / "script.js").exists())
                self.assertTrue((plugin_dir / "panel.py").exists())

                manifest = json.loads((plugin_dir / "manifest.json").read_text(encoding="utf-8"))
                self.assertEqual(manifest["feature_id"], feature_id)
                self.assertTrue(self.REQUIRED_MANIFEST_FIELDS.issubset(manifest.keys()))

                feature_text = (plugin_dir / "feature.py").read_text(encoding="utf-8")
                self.assertIn("PluginFeatureBase", feature_text)
                self.assertIn(
                    (PROJECT_DIR / feature_source).read_text(encoding="utf-8").split("class ", 1)[1].split(":", 1)[0].split("(", 1)[0],
                    feature_text,
                )

                script_text = (plugin_dir / "script.js").read_text(encoding="utf-8")
                self.assertIn("rpc.exports", script_text)
                if script_source:
                    original_script = (PROJECT_DIR / script_source).read_text(encoding="utf-8")
                    self.assertIn(original_script, script_text)
                else:
                    self.assertIn("Universal-ImGui-Hook.dll", script_text)

    def test_old_ordinary_feature_modules_are_not_imported_for_registration(self):
        init_text = (PROJECT_DIR / "features" / "__init__.py").read_text(encoding="utf-8")
        for feature_id, (feature_source, _script_source) in self.ORDINARY_FEATURES.items():
            if feature_id in {"nano4t", "weapon_giver"}:
                continue
            self.assertNotIn(Path(feature_source).stem, init_text)
            feature_text = (PROJECT_DIR / "features" / feature_id / "feature.py").read_text(encoding="utf-8")
            self.assertNotIn("@register_feature", feature_text)
            self.assertNotIn("register_feature", feature_text)

    def test_phase3_ui_and_services_use_plugin_runtime_boundaries(self):
        feature_tabs = (PROJECT_DIR / "ui" / "views" / "feature_tabs_view.py").read_text(encoding="utf-8")
        plugin_page = (PROJECT_DIR / "ui" / "pages" / "plugin_feature_page.py")
        feature_service = (PROJECT_DIR / "core" / "services" / "feature_command_service.py").read_text(encoding="utf-8")
        frida_manager = (PROJECT_DIR / "core" / "frida_manager.py").read_text(encoding="utf-8")

        self.assertTrue(plugin_page.exists())
        plugin_page_text = plugin_page.read_text(encoding="utf-8")
        self.assertIn(".by_tab(", plugin_page_text)
        self.assertIn("manifest.get(\"layout\"", plugin_page_text)
        self.assertIn("order", plugin_page_text)

        for feature_id in self.ORDINARY_FEATURES:
            self.assertNotIn(f'"{feature_id}"', feature_service)
            self.assertNotIn(f"'{feature_id}'", feature_service)
            if feature_id != "esp_box":
                self.assertNotIn(f"modules.{feature_id}", frida_manager)

        self.assertNotIn("_make_feature_card(", feature_tabs)
        self.assertNotIn("_build_weapon_tab", feature_tabs)
        self.assertNotIn("_build_player_tab", feature_tabs)
        self.assertNotIn("_build_other_tab", feature_tabs)

    def test_check_architecture_script_exists(self):
        self.assertTrue((PROJECT_DIR / "tools" / "check_architecture.py").exists())

    def test_no_manual_ordinary_imports_or_central_panel_branches(self):
        main_text = (PROJECT_DIR / "main.py").read_text(encoding="utf-8")
        init_text = (PROJECT_DIR / "features" / "__init__.py").read_text(encoding="utf-8")
        window_contract = (PROJECT_DIR / "ui" / "window_contract.py").read_text(encoding="utf-8")
        plugin_page = (PROJECT_DIR / "ui" / "pages" / "plugin_feature_page.py").read_text(encoding="utf-8")

        self.assertNotIn("import features", main_text)
        self.assertIn('APP_VERSION = "v1.9"', window_contract)
        for feature_id, (feature_source, _script_source) in self.ORDINARY_FEATURES.items():
            self.assertNotIn(Path(feature_source).stem, init_text)
            self.assertNotIn(f'feature_id == "{feature_id}"', plugin_page)
        self.assertIn("build_card", plugin_page)
        self.assertIn("panel.py", plugin_page)

    def test_manifest_text_is_utf8_chinese_not_mojibake(self):
        expected = {
            "knife": ("快刀", "🔪", "提升挥刀速度（人类 / 生化幽灵通用）"),
            "recoil": ("无后座力", "🎯", "消除所有枪械后座力"),
            "ammo": ("无限子弹", "🔫", "子弹永不消耗"),
            "ammoplus": ("快速换弹", "⚡", "换弹速度加快"),
            "range": ("剑气化丝", "⚔️", "扩大近战攻击距离（人类 / 生化幽灵通用）"),
            "aim": ("自瞄", "🎯", "自动瞄准敌方玩家"),
            "speedgun": ("射速变快 / 连狙", "⚡", "射速10倍 | 半自动→全自动 | 狙击镜常开 | 后坐力清零"),
            "movespeed": ("滑板鞋", "👟", "提升移动速度"),
            "time": ("无限时间", "⏰", "设定时间为 9:59"),
            "gravity": ("轻重力 / 高跳", "🌌", "调整重力与跳跃倍率"),
            "godmode": ("金刚不坏", "🛡️", "角色受到攻击时不会受伤"),
            "skillcd": ("技能无冷却", "✨", "生化模式，所有技能无冷却"),
            "gather": ("聚怪", "👾", "将所有人机聚集到佣兵出生点"),
            "isbot": ("天机傀儡", "🧠", "玩家由人机控制"),
            "roundskip": ("回合跳过", "⏭️", "结束当前回合"),
            "esp_box": ("方框透视", "📦", "通过 Universal DLL 显示方框透视"),
            "timescale": ("时间加速", "⏩", "调整游戏时间倍率"),
        }
        for feature_id, values in expected.items():
            with self.subTest(feature_id=feature_id):
                manifest = json.loads(
                    (PROJECT_DIR / "features" / feature_id / "manifest.json").read_text(encoding="utf-8")
                )
                self.assertEqual(
                    (manifest["display_name"], manifest["icon"], manifest["desc"]),
                    values,
                )
                self.assertNotIn("?", manifest["display_name"] + manifest["icon"] + manifest["desc"])


if __name__ == "__main__":
    unittest.main()
