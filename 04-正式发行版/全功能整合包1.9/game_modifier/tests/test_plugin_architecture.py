import importlib
import json
import re
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
        legacy_dir = self.features_dir / "_legacy_archive"
        legacy_dir.mkdir()
        (legacy_dir / "manifest.json").write_text(
            json.dumps({"feature_id": "legacy_should_not_load"}),
            encoding="utf-8",
        )
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

    def test_rpc_client_allows_manifest_rpc_actions(self):
        from core.frida_runtime.rpc_client import RpcClient

        calls = []

        class FakeScriptManager:
            manifests = {
                "sample": {
                    "feature_id": "sample",
                    "display_name": "Sample",
                    "rpc": ["enable", "customAction"],
                    "_manifest_path": "features/sample/manifest.json",
                }
            }

            def call(self, feature_id, action, payload=None):
                calls.append((feature_id, action, payload))
                return {"ok": True}

        client = RpcClient(FakeScriptManager())

        self.assertEqual(client.call("sample", "enable"), {"ok": True})
        self.assertEqual(client.call("sample", "customAction"), {"ok": True})
        self.assertEqual(calls, [("sample", "enable", None), ("sample", "customAction", None)])
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
        "knife",
        "recoil",
        "ammo",
        "ammoplus",
        "range",
        "aim",
        "speedgun",
        "movespeed",
        "time",
        "gravity",
        "godmode",
        "skillcd",
        "gather",
        "isbot",
        "roundskip",
        "esp_box",
        "timescale",
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

    def test_all_ordinary_features_have_self_contained_plugin_files(self):
        for feature_id in self.ORDINARY_FEATURES:
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
                self.assertNotIn("_legacy_archive", feature_text)

                script_text = (plugin_dir / "script.js").read_text(encoding="utf-8")
                self.assertIn("rpc.exports", script_text)
                self.assertNotIn("_legacy_archive", script_text)
                self.assertNotIn("TODO", script_text)

    def test_old_ordinary_feature_modules_are_not_imported_for_registration(self):
        init_text = (PROJECT_DIR / "features" / "__init__.py").read_text(encoding="utf-8")
        for feature_id in self.ORDINARY_FEATURES:
            if feature_id in {"nano4t", "weapon_giver"}:
                continue
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
        for feature_id in self.ORDINARY_FEATURES:
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

    def test_feature_tabs_use_generic_plugin_callbacks(self):
        feature_tabs = (PROJECT_DIR / "ui" / "views" / "feature_tabs_view.py").read_text(encoding="utf-8")
        plugin_page = (PROJECT_DIR / "ui" / "pages" / "plugin_feature_page.py").read_text(encoding="utf-8")
        app_text = (PROJECT_DIR / "ui" / "app.py").read_text(encoding="utf-8")
        handles_text = (PROJECT_DIR / "ui" / "views" / "common.py").read_text(encoding="utf-8")
        controller = (PROJECT_DIR / "ui" / "controllers" / "feature_action_controller.py").read_text(encoding="utf-8")
        frida_manager = (PROJECT_DIR / "core" / "frida_manager.py").read_text(encoding="utf-8")

        self.assertNotIn("@dataclass", feature_tabs)
        self.assertNotIn("class FeatureTabsHandles", feature_tabs)
        self.assertNotIn("FeatureTabsHandles(", feature_tabs)
        for legacy_callback in (
            "on_knife_speed_change",
            "on_move_speed_change",
            "on_range_change",
            "on_timescale_change",
            "on_gravity_change",
            "on_jump_change",
            "on_gravity_mode_change",
            "on_gather",
            "on_skip_round",
        ):
            self.assertNotIn(legacy_callback, feature_tabs)
            self.assertNotIn(legacy_callback, app_text)

        self.assertIn('"set_config"', feature_tabs)
        self.assertIn('"action"', feature_tabs)
        self.assertIn('callbacks["set_config"]', plugin_page)
        self.assertIn('callbacks["action"]', plugin_page)
        self.assertNotIn('callbacks["slider"]', plugin_page)
        self.assertIn("isinstance(handles, dict)", handles_text)
        self.assertIn("def set_feature_config", controller)
        self.assertIn("def trigger_feature_action", controller)
        self.assertNotIn("_build_js_code", frida_manager)
        self.assertNotIn("_build_dispatcher", frida_manager)
        self.assertNotIn("_build_rpc_exports", frida_manager)
        self.assertNotIn("send_toggle", frida_manager)
        self.assertNotIn("call_export", frida_manager)

        for panel_path in (PROJECT_DIR / "features").glob("*/panel.py"):
            panel_text = panel_path.read_text(encoding="utf-8")
            self.assertNotIn('callbacks["slider"]', panel_text, msg=str(panel_path))
            self.assertNotIn('callbacks["gravity"]', panel_text, msg=str(panel_path))
            self.assertNotIn('callbacks["jump"]', panel_text, msg=str(panel_path))
            self.assertNotIn('callbacks["gravity_mode"]', panel_text, msg=str(panel_path))
            self.assertNotIn('callbacks["gather"]', panel_text, msg=str(panel_path))
            self.assertNotIn('callbacks["skip_round"]', panel_text, msg=str(panel_path))

    def test_core_config_uses_manifest_generated_feature_info(self):
        config_text = (PROJECT_DIR / "core" / "config.py").read_text(encoding="utf-8")
        self.assertNotRegex(config_text, r"FEATURES_INFO\s*=\s*\{")
        self.assertIn("manifest.json", config_text)
        self.assertIn("_build_features_info", config_text)

    def test_center_runtime_files_do_not_branch_on_feature_ids(self):
        targets = [
            PROJECT_DIR / "core" / "frida_manager.py",
            PROJECT_DIR / "ui" / "controllers" / "feature_action_controller.py",
            PROJECT_DIR / "ui" / "controllers" / "action_router.py",
        ]
        all_features = set(self.ORDINARY_FEATURES) | {"nano4t", "weapon_giver", "battle_round"}
        for path in targets:
            text = path.read_text(encoding="utf-8")
            for feature_id in all_features:
                self.assertNotIn(f'"{feature_id}"', text, msg=str(path))
                self.assertNotIn(f"'{feature_id}'", text, msg=str(path))

    def test_plugin_events_are_routed_generically(self):
        frida_manager = (PROJECT_DIR / "core" / "frida_manager.py").read_text(encoding="utf-8")
        app_events = (PROJECT_DIR / "ui" / "controllers" / "app_event_controller.py").read_text(encoding="utf-8")

        self.assertIn('"plugin_event"', frida_manager)
        self.assertIn("LegacyMessageAdapter", frida_manager)
        self.assertIn('"plugin_event"', app_events)
        for old_event in ("gather_result", "round_skipped", "nano4t_event", "battle_round_event", "isbot_event"):
            self.assertNotIn(f'"{old_event}"', frida_manager)
            self.assertNotIn(f'"{old_event}"', app_events)

    def test_panels_use_panel_context_not_full_app(self):
        legacy_panel_features = {
            "weapon_giver",
            "nano4t",
            "battle_round",
            "gather",
            "roundskip",
            "esp_box",
            "isbot",
        }
        forbidden_patterns = {
            "context._app": r"context\._app",
            "app._": r"app\._",
            "FridaManager": r"\bFridaManager\b|core\.frida_manager",
            "get_state": r"\.get_state\s*\(",
            "set_state": r"\.set_state\s*\(",
            "get_handle": r"\.get_handle\s*\(",
            "set_handle": r"\.set_handle\s*\(",
            "controller": r"\.controller\s*\(",
            "service": r"\.service\s*\(",
            "legacy": r"context\.legacy\b",
        }
        for panel_path in (PROJECT_DIR / "features").glob("*/panel.py"):
            panel_text = panel_path.read_text(encoding="utf-8")
            self.assertNotIn("build_panel(app", panel_text, msg=str(panel_path))
            for label, pattern in forbidden_patterns.items():
                if panel_path.parent.name in legacy_panel_features:
                    continue
                self.assertIsNone(re.search(pattern, panel_text), msg=f"{panel_path}: {label}")

    def test_app_state_concrete_fields_are_legacy_only(self):
        state_text = (PROJECT_DIR / "core" / "state" / "app_state.py").read_text(encoding="utf-8")
        self.assertIn("LEGACY_COMPAT_ONLY", state_text)
        allowed_fields = {
            "features",
            "knife_speed",
            "move_speed",
            "range_mult",
            "gravity",
            "jump",
            "gravity_mode",
            "timescale",
            "battle_round_enabled",
            "weapon_giver_respawn_enabled",
            "nano4t_ghost",
            "nano4t_human",
        }
        fields = set(re.findall(r"^\s{4}([a-zA-Z_][a-zA-Z0-9_]*)\s*:", state_text, re.MULTILINE))
        self.assertEqual(fields, allowed_fields)

    def test_safe_panel_context_has_no_legacy_methods(self):
        panel_context = (PROJECT_DIR / "ui" / "panel_context.py").read_text(encoding="utf-8")
        self.assertIn("LEGACY_COMPAT_ONLY", panel_context)
        safe_match = re.search(
            r"class PanelContext\b(?P<body>.*?)(?=^class FeaturePanelContext\b)",
            panel_context,
            re.S | re.M,
        )
        self.assertIsNotNone(safe_match)
        safe_body = safe_match.group("body")
        for method in ("get_state", "set_state", "get_handle", "set_handle", "controller", "service"):
            self.assertIsNone(re.search(rf"^\s+def\s+{method}\b", safe_body, re.M))

    def test_legacy_message_adapter_is_whitelisted(self):
        adapter_text = (PROJECT_DIR / "core" / "frida_runtime" / "legacy_message_adapter.py").read_text(encoding="utf-8")
        self.assertIn("LEGACY_COMPAT_ONLY", adapter_text)
        self.assertIn("Do not add new feature branches here", adapter_text)
        self.assertIn("LEGACY_FEATURE_IDS", adapter_text)
        self.assertIn("LEGACY_MESSAGE_TYPES", adapter_text)
        self.assertNotIn("third_person_camera", adapter_text)

        from core.frida_runtime.legacy_message_adapter import (
            LEGACY_FEATURE_IDS,
            LEGACY_MESSAGE_TYPES,
            LEGACY_MESSAGE_PREFIXES,
            LegacyMessageAdapter,
        )

        self.assertEqual(
            LEGACY_FEATURE_IDS,
            {"gather", "roundskip", "weapon_giver", "nano4t", "battle_round", "isbot"},
        )
        self.assertIn("gather_result", LEGACY_MESSAGE_TYPES)
        self.assertIn("nano4t_", LEGACY_MESSAGE_PREFIXES)
        self.assertIsNone(LegacyMessageAdapter.adapt({"type": "third_person_camera_event"}))
        self.assertEqual(
            LegacyMessageAdapter.adapt({"type": "gather_result", "data": {"ok": True}})["audience"],
            "user",
        )

    def test_future_feature_id_does_not_leak_into_center_files(self):
        center_paths = [
            PROJECT_DIR / "ui" / "app.py",
            PROJECT_DIR / "core" / "frida_manager.py",
            PROJECT_DIR / "ui" / "controllers" / "feature_action_controller.py",
            PROJECT_DIR / "ui" / "controllers" / "action_router.py",
            PROJECT_DIR / "core" / "frida_runtime" / "legacy_message_adapter.py",
            PROJECT_DIR / "core" / "state" / "app_state.py",
            PROJECT_DIR / "core" / "config.py",
        ]
        for path in center_paths:
            self.assertNotIn("third_person_camera", path.read_text(encoding="utf-8"), msg=str(path))

    def test_template_includes_events_and_plugin_event_example(self):
        template_dir = PROJECT_DIR / "features" / "_template"
        self.assertTrue((template_dir / "events.py").exists())
        self.assertIn("handle_event", (template_dir / "events.py").read_text(encoding="utf-8"))
        self.assertIn("plugin_event", (template_dir / "script.js").read_text(encoding="utf-8"))
        self.assertIn("events.py", (template_dir / "README.md").read_text(encoding="utf-8"))

    def test_legacy_archive_is_not_required_or_referenced_by_runtime(self):
        self.assertFalse((PROJECT_DIR / "features" / "_legacy_archive").exists())
        for path in (PROJECT_DIR / "features").glob("*/manifest.json"):
            if path.parent.name.startswith("_"):
                continue
            self.assertNotIn("_legacy_archive", path.read_text(encoding="utf-8"), msg=str(path))


if __name__ == "__main__":
    unittest.main()

