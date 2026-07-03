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

FEATURE_DIR_NAMES = {
    "ammo": "01_ammo",
    "recoil": "02_recoil",
    "time": "03_time",
    "knife": "04_knife",
    "ammoplus": "05_ammoplus",
    "movespeed": "06_movespeed",
    "range": "07_range",
    "gather": "08_gather",
    "gravity": "09_gravity",
    "roundskip": "10_roundskip",
    "aim": "11_aim",
    "godmode": "12_godmode",
    "speedgun": "13_speedgun",
    "isbot": "14_isbot",
    "nano4t": "15_nano4t",
    "weapon_giver": "16_weapon_giver",
    "skillcd": "17_skillcd",
    "esp_box": "18_esp_box",
    "battle_round": "19_battle_round",
    "timescale": "20_timescale",
    "third_person_camera": "21_third_person_camera",
    "unlimited_bag": "22_unlimited_bag",
    "fast_gunstock": "23_fast_gunstock",
}


def feature_dir(feature_id):
    return PROJECT_DIR / "features" / FEATURE_DIR_NAMES.get(feature_id, feature_id)


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
            "tab_title": "Weapon",
            "tab_order": 10,
            "state": {"sync_enabled_from_config": True},
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

    def test_setup_logging_skips_log_dir_and_file_handler_when_frozen(self):
        import logging
        from core import log_manager

        app_dir = self.root / "app"
        app_dir.mkdir()
        logger = logging.getLogger("game_modifier")
        original_handlers = list(logger.handlers)
        original_initialized = log_manager._initialized
        original_app_dir = log_manager.APP_DIR
        had_frozen = hasattr(sys, "frozen")
        original_frozen = getattr(sys, "frozen", None)

        try:
            for handler in original_handlers:
                logger.removeHandler(handler)
            log_manager._initialized = False
            log_manager.APP_DIR = str(app_dir)
            sys.frozen = True

            log_manager.setup_logging()

            self.assertFalse((app_dir / "logs").exists())
            self.assertFalse(
                any(isinstance(handler, log_manager.RotatingFileHandler) for handler in logger.handlers)
            )
        finally:
            for handler in list(logger.handlers):
                logger.removeHandler(handler)
                handler.close()
            for handler in original_handlers:
                logger.addHandler(handler)
            log_manager._initialized = original_initialized
            log_manager.APP_DIR = original_app_dir
            if had_frozen:
                sys.frozen = original_frozen
            else:
                delattr(sys, "frozen")

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

    def test_script_manager_tries_lowercase_rpc_alias_after_camel_and_snake(self):
        from core.frida_runtime.script_manager import ScriptManager

        calls = []

        class FakeScript:
            def __init__(self, exports):
                self.exports_sync = exports

        cases = [
            ("nano4t", "nano4tInit", "nano4tinit"),
            ("battle_round", "battleRoundGetStatus", "battleroundgetstatus"),
            ("weapon_giver", "giveWeapon", "giveweapon"),
            ("third_person_camera", "setConfig", "setconfig"),
        ]
        manager = ScriptManager(session_manager=None, manifests=[], logger=None)
        for feature_id, action, lowercase_action in cases:
            with self.subTest(feature_id=feature_id, action=action):
                exports = type("FakeExports", (), {})()

                def _make_rpc(name):
                    def _rpc(payload):
                        calls.append((name, payload))
                        return {"ok": True}

                    return _rpc

                setattr(exports, lowercase_action, _make_rpc(lowercase_action))
                manager._scripts[feature_id] = FakeScript(exports)

                payload = {"source": "test", "feature": feature_id}
                self.assertEqual(manager.call(feature_id, action, payload), {"ok": True})
                self.assertEqual(calls[-1], (lowercase_action, payload))

    def test_script_manager_reports_rpc_candidates_when_all_methods_are_missing(self):
        from core.frida_runtime.script_manager import ScriptManager

        logs = []

        class FakeLogger:
            def error(self, message):
                logs.append(("error", message))

            def warning(self, message):
                logs.append(("warning", message))

            def debug(self, message):
                logs.append(("debug", message))

        class MissingFridaExports:
            def __getattr__(self, name):
                def _missing(*_args):
                    raise Exception(f"unable to find method '{name.lower()}'")

                return _missing

        class FakeScript:
            exports_sync = MissingFridaExports()

        manager = ScriptManager(session_manager=None, manifests=[], logger=FakeLogger())
        manager._scripts["battle_round"] = FakeScript()

        with self.assertRaises(AttributeError) as ctx:
            manager.call("battle_round", "battleRoundGetStatus", {})

        message = str(ctx.exception)
        self.assertIn("feature_id=battle_round", message)
        self.assertIn("action=battleRoundGetStatus", message)
        self.assertIn("battleRoundGetStatus", message)
        self.assertIn("battle_round_get_status", message)
        self.assertIn("battleroundgetstatus", message)
        self.assertTrue(any(level == "error" and "candidates=" in text for level, text in logs))

    def test_cleanup_all_does_not_warn_for_already_destroyed_scripts(self):
        from core.frida_runtime.script_manager import ScriptManager

        logs = []

        class FakeLogger:
            def warning(self, message):
                logs.append(("warning", message))

            def debug(self, message):
                logs.append(("debug", message))

            def error(self, message):
                logs.append(("error", message))

        class FakeExports:
            def cleanup(self, payload):
                raise Exception("script has been destroyed")

        class FakeScript:
            exports_sync = FakeExports()

            def unload(self):
                pass

        manager = ScriptManager(session_manager=None, manifests=[], logger=FakeLogger())
        manager._scripts["sample"] = FakeScript()

        manager.cleanup_all("test_shutdown")

        self.assertFalse([entry for entry in logs if entry[0] == "warning"])

    def test_plugin_scripts_and_manifests_expose_lowercase_rpc_aliases(self):
        expected = {
            "nano4t": {
                "manifest": ["nano4tinit", "nano4tset", "nano4tgetcurrent", "nano4thealthcheck", "setconfig"],
                "script": [
                    "rpc.exports.nano4tinit = rpc.exports.nano4tInit",
                    "rpc.exports.nano4tset = rpc.exports.nano4tSet",
                    "rpc.exports.nano4tgetcurrent = rpc.exports.nano4tGetCurrent",
                    "rpc.exports.nano4thealthcheck = rpc.exports.nano4tHealthCheck",
                    "rpc.exports.setconfig = rpc.exports.setConfig",
                ],
            },
            "battle_round": {
                "manifest": ["battleroundgetstatus"],
                "script": ["rpc.exports.battleroundgetstatus = rpc.exports.battleRoundGetStatus"],
            },
            "weapon_giver": {
                "manifest": ["giveweapon", "setrespawnweapon", "clearrespawnweapon", "setconfig"],
                "script": [
                    "rpc.exports.giveweapon = rpc.exports.giveWeapon",
                    "rpc.exports.setrespawnweapon = rpc.exports.setRespawnWeapon",
                    "rpc.exports.clearrespawnweapon = rpc.exports.clearRespawnWeapon",
                    "rpc.exports.setconfig = rpc.exports.setConfig",
                ],
            },
            "third_person_camera": {
                "manifest": ["setconfig", "getstatus"],
                "script": [
                    "rpc.exports.setconfig = rpc.exports.setConfig",
                    "rpc.exports.getstatus = rpc.exports.status",
                ],
            },
        }
        for feature_id, aliases in expected.items():
            with self.subTest(feature_id=feature_id):
                plugin_dir = feature_dir(feature_id)
                manifest = json.loads((plugin_dir / "manifest.json").read_text(encoding="utf-8"))
                script = (plugin_dir / "script.js").read_text(encoding="utf-8")
                for action in aliases["manifest"]:
                    self.assertIn(action, manifest["rpc"])
                for line in aliases["script"]:
                    self.assertIn(line, script)

    def test_third_person_defaults_and_cleanup_match_plugin_lifecycle(self):
        plugin_dir = feature_dir("third_person_camera")
        manifest = json.loads((plugin_dir / "manifest.json").read_text(encoding="utf-8"))
        script = (plugin_dir / "script.js").read_text(encoding="utf-8")

        self.assertEqual(manifest["desc"], "切换成第三人称视角")
        sliders = {
            item["key"]: item
            for item in manifest["controls"]
            if item.get("type") == "slider"
        }
        self.assertEqual(manifest["config"], {"distance": 3.0, "pivotHeight": 1.35})
        self.assertIs(manifest.get("lifecycle", {}).get("restore"), True)
        self.assertEqual(sliders["distance"]["default"], 3.0)
        self.assertEqual(sliders["pivotHeight"]["default"], 1.35)
        default_config_path = PROJECT_DIR / "data" / "default_config.json"
        if default_config_path.exists():
            persisted = json.loads(default_config_path.read_text(encoding="utf-8")).get("third_person_camera", {})
            if persisted:
                self.assertEqual(persisted.get("distance"), 3.0, msg=str(default_config_path))
                self.assertEqual(persisted.get("pivotHeight"), 1.35, msg=str(default_config_path))
        self.assertIn("distance: 3.0", script)
        self.assertIn("pivotHeight: 1.35", script)
        self.assertIn("shoulder: 'center'", script)
        self.assertIn("invertY: false", script)
        self.assertIn("var desiredPitch = runtime.cameraInput.pitch;", script)
        self.assertIn("if (!config.invertY) desiredPitch = -desiredPitch;", script)
        self.assertIn("invertY: config.invertY", script)
        self.assertIn("if (input.invertY !== undefined)", script)
        request_enable_body = script.split("function requestEnable(input)", 1)[1].split("function requestDisable()", 1)[0]
        self.assertIn("var validation = validateConfig(input || {})", request_enable_body)
        self.assertIn("config = validation.config", request_enable_body)
        self.assertIn("pendingEnable = true", request_enable_body)

        cleanup_body = script.split("function cleanup(payload)", 1)[1].split("rpc.exports = {", 1)[0]
        self.assertIn("performDisable()", cleanup_body)
        self.assertNotIn("queuedDisable", cleanup_body)

    def test_third_person_panel_suppresses_programmatic_slider_sync(self):
        panel = (feature_dir("third_person_camera") / "panel.py").read_text(encoding="utf-8")
        script = (feature_dir("third_person_camera") / "script.js").read_text(encoding="utf-8")

        self.assertIn("class _SyncedSliderVar", panel)
        self.assertIn("self._syncing = True", panel)
        self.assertIn("if sync_guard[\"value\"]:", panel)
        self.assertIn("callbacks[\"set_config\"]", panel)
        self.assertIn("scheduleRefresh(", script)
        self.assertIn("'config_changed'", script)

    def test_timescale_cleanup_restores_normal_speed_before_script_unload(self):
        script = (feature_dir("timescale") / "script.js").read_text(encoding="utf-8")

        self.assertIn("function restoreNormalTimeScaleNow()", script)
        restore_body = script.split("function restoreNormalTimeScaleNow()", 1)[1].split("function disableFeature", 1)[0]
        self.assertIn("safeWriteTimeScale(1.0)", restore_body)

        cleanup_body = script.split("function __pluginCleanup(payload)", 1)[1].split("rpc.exports = {", 1)[0]
        self.assertIn("disable({ restoreNow: true })", cleanup_body)

    def test_speedgun_uses_rpg_fire_data_rates_without_direct_anim_speed(self):
        script = (feature_dir("speedgun") / "script.js").read_text(encoding="utf-8")

        self.assertIn("'WPN_RPG.Fire'", script)
        self.assertIn("base.add(0xB670A0)", script)
        self.assertIn("applyRpgDataSpeed(this.self)", script)
        self.assertIn("RPG Fire Hook失败", script)
        self.assertIsNone(re.search(r"^\s*setAnimSpeed\(anim,\s*10\.0,\s*ptr\(0\)\);", script, re.M))

    def test_weapon_giver_bridges_acquired_weapons_to_speedgun_plugin_rpc(self):
        weapon_script = (feature_dir("weapon_giver") / "script.js").read_text(encoding="utf-8")
        weapon_events = (feature_dir("weapon_giver") / "events.py").read_text(encoding="utf-8")
        speedgun_script = (feature_dir("speedgun") / "script.js").read_text(encoding="utf-8")

        self.assertNotIn("modules.speedgun", weapon_script)
        self.assertIn("event: 'weapon_acquired'", weapon_script)
        self.assertIn("weaponPtr: weapon.toString()", weapon_script)
        self.assertIn("context.feature_service.call_action(", weapon_events)
        self.assertIn('"speedgun"', weapon_events)
        self.assertIn('"notifyWeaponAcquired"', weapon_events)
        self.assertIn("function __pluginNotifyWeaponAcquired(payload)", speedgun_script)
        self.assertIn("var weapon = ptr(payload.weaponPtr)", speedgun_script)
        self.assertIn("ModeBase_Update: 0xAF6A00", speedgun_script)
        self.assertIn("processPendingWeaponSpeed()", speedgun_script)
        self.assertIn("notifyWeaponAcquired: __pluginNotifyWeaponAcquired", speedgun_script)

    def test_rpc_error_logging_is_throttled_by_feature_action_and_error(self):
        from core.frida_manager import FridaManager

        manager = FridaManager()
        error = Exception("unable to find method 'setconfig'")

        self.assertTrue(manager._should_log_rpc_error("sample", "setConfig", error))
        self.assertFalse(manager._should_log_rpc_error("sample", "setConfig", error))
        self.assertTrue(manager._should_log_rpc_error("sample", "status", error))

    def test_script_manager_rpc_candidates_cover_snake_case_frida_names(self):
        from core.frida_runtime.script_manager import ScriptManager

        self.assertEqual(
            ScriptManager._rpc_candidates("skip_round"),
            ["skip_round", "skipRound", "skipround"],
        )
        self.assertIn("battle_round_get_status", ScriptManager._rpc_candidates("battleRoundGetStatus"))
        self.assertIn("battleroundgetstatus", ScriptManager._rpc_candidates("battleRoundGetStatus"))

    def test_unload_does_not_warn_for_script_is_destroyed_variant(self):
        from core.frida_runtime.script_manager import ScriptManager

        logs = []

        class FakeLogger:
            def warning(self, message):
                logs.append(("warning", message))

            def debug(self, message):
                logs.append(("debug", message))

        class FakeScript:
            def unload(self):
                raise Exception("script is destroyed")

        manager = ScriptManager(session_manager=None, manifests=[], logger=FakeLogger())
        manager._scripts["sample"] = FakeScript()

        manager.unload("sample")

        self.assertFalse([entry for entry in logs if entry[0] == "warning"])

    def test_log_regressions_from_game_modifier_log_are_fixed_in_scripts(self):
        gather_script = (feature_dir("gather") / "script.js").read_text(encoding="utf-8")
        roundskip_script = (feature_dir("roundskip") / "script.js").read_text(encoding="utf-8")
        roundskip_manifest = json.loads(
            (feature_dir("roundskip") / "manifest.json").read_text(encoding="utf-8")
        )
        weapon_script = (feature_dir("weapon_giver") / "script.js").read_text(encoding="utf-8")
        weapon_events = (feature_dir("weapon_giver") / "events.py").read_text(encoding="utf-8")

        self.assertNotIn("type:'done'", gather_script)
        self.assertNotIn('type:"done"', gather_script)
        self.assertIn("type: 'plugin_event'", gather_script)
        self.assertIn("event: 'done'", gather_script)

        self.assertNotIn("return __pluginEnable(payload || {});", roundskip_script)
        self.assertIn("rpc.exports.skipRound = rpc.exports.skip_round", roundskip_script)
        self.assertIn("rpc.exports.skipround = rpc.exports.skip_round", roundskip_script)
        self.assertIn("skipRound", roundskip_manifest["rpc"])
        self.assertIn("skipround", roundskip_manifest["rpc"])

        is_valid_match = re.search(
            r"function isPlayerValid\(player\) \{(?P<body>.*?)\n  \}",
            weapon_script,
            re.S,
        )
        self.assertIsNotNone(is_valid_match)
        self.assertNotIn("!isMyPlayer(player)", is_valid_match.group("body"))
        self.assertIn("reason", weapon_script)
        self.assertIn('"warning"', weapon_events)

    def test_gather_caps_game_thread_player_scan(self):
        gather_script = (feature_dir("gather") / "script.js").read_text(encoding="utf-8")

        self.assertIn("MAX_PLAYERS_PER_GATHER", gather_script)
        self.assertIn("GATHER_FRAME_BUDGET_MS", gather_script)
        self.assertIn("Math.min(t, MAX_PLAYERS_PER_GATHER)", gather_script)
        self.assertIn("聚怪玩家列表数量异常", gather_script)
        self.assertIn("聚怪本帧预算已用尽", gather_script)

    def test_weapon_giver_spreads_native_calls_and_logs_duration(self):
        weapon_script = (feature_dir("weapon_giver") / "script.js").read_text(encoding="utf-8")

        self.assertIn("_nativeCallCooldownMs", weapon_script)
        self.assertIn("_lastGiveWeaponCallAt", weapon_script)
        self.assertIn("GiveWeapon即将执行", weapon_script)
        self.assertIn("GiveWeapon耗时", weapon_script)
        self.assertIn("now - _lastGiveWeaponCallAt < _nativeCallCooldownMs", weapon_script)

    def test_roundskip_uses_legacy_immediate_write_semantics(self):
        roundskip_script = (feature_dir("roundskip") / "script.js").read_text(encoding="utf-8")
        roundskip_panel = (feature_dir("roundskip") / "panel.py").read_text(encoding="utf-8")
        time_script = (feature_dir("time") / "script.js").read_text(encoding="utf-8")
        time_manifest = json.loads((feature_dir("time") / "manifest.json").read_text(encoding="utf-8"))
        skip_round = re.search(r"function skipRound\(\) \{(?P<body>.*?)\n  \}", roundskip_script, re.S)

        self.assertIsNotNone(skip_round)
        body = skip_round.group("body")
        self.assertLess(
            body.index("if (modeBaseGeneration !== roomGeneration)"),
            body.index("if (!isValidInstance(instance))"),
        )
        self.assertIn('reason == "stale_room_generation"', roundskip_panel)
        self.assertNotIn("pendingSkip", roundskip_script)
        self.assertNotIn("skip_unconfirmed", roundskip_script)
        self.assertNotIn("skip_requested", roundskip_script)
        self.assertNotIn("modules.time", body)
        self.assertIn("emitEvent('skipped'", roundskip_script)
        self.assertIn('callbacks["is_enabled"]("time")', roundskip_panel)
        self.assertIn('callbacks["action"]("time", "pauseFor", {"ms": 2000})', roundskip_panel)
        self.assertIn('log("✅ 回合跳过成功！")', roundskip_panel)
        self.assertIn("pauseFor: function(payload)", time_script)
        self.assertIn("module.pauseFor(ms)", time_script)
        self.assertIn("pauseFor", time_manifest["rpc"])
        self.assertIn("pausefor", time_manifest["rpc"])
        self.assertIn('event == "skipped"', (feature_dir("roundskip") / "events.py").read_text(encoding="utf-8"))
        self.assertNotIn('event == "skip_unconfirmed"', (feature_dir("roundskip") / "events.py").read_text(encoding="utf-8"))

    def test_migrated_plugin_feature_files_do_not_call_legacy_exports(self):
        for feature_path in (PROJECT_DIR / "features").glob("*/feature.py"):
            text = feature_path.read_text(encoding="utf-8")
            self.assertNotIn("call_export", text, msg=str(feature_path))

    def test_battle_round_syncs_nano4t_through_plugin_events(self):
        battle_script = (feature_dir("battle_round") / "script.js").read_text(encoding="utf-8")
        battle_events = (feature_dir("battle_round") / "events.py").read_text(encoding="utf-8")
        nano_events = (feature_dir("nano4t") / "events.py").read_text(encoding="utf-8")

        self.assertNotIn("modules.nano4t", battle_script)
        self.assertIn('context.feature_event("mode_detected", {}, feature_id="nano4t")', battle_events)
        self.assertIn('event == "mode_detected"', nano_events)
        self.assertIn("runtime.auto_init_if_needed_async()", nano_events)

    def test_isbot_state_matches_legacy_room_lifecycle_without_panel_module_split(self):
        isbot_script = (feature_dir("isbot") / "script.js").read_text(encoding="utf-8")
        isbot_panel = (feature_dir("isbot") / "panel.py").read_text(encoding="utf-8")
        isbot_events = (feature_dir("isbot") / "events.py").read_text(encoding="utf-8")
        isbot_state = (feature_dir("isbot") / "state.py").read_text(encoding="utf-8")

        self.assertIn("roomCaptureCount >= 2 ? 'active' : 'awaiting_reenter'", isbot_script)
        self.assertIn("isbot_state.status_label = status", isbot_panel)
        self.assertIn("status_label = None", isbot_state)
        self.assertNotIn("from features.isbot.panel import", isbot_events)
        self.assertIn("isbot_state.status_label", isbot_events)
        self.assertIn("def handle_lifecycle(context, event, payload):", isbot_events)
        self.assertIn('event in {"game_connected", "game_disconnected"}', isbot_events)
        self.assertIn('context.is_enabled()', isbot_events)
        self.assertIn("def toggle_isbot():", isbot_panel)
        self.assertNotIn('command=lambda: callbacks["toggle"](feature_id)', isbot_panel)

    def test_isbot_keeps_reenter_progress_across_room_exit_until_disabled(self):
        isbot_script = (feature_dir("isbot") / "script.js").read_text(encoding="utf-8")
        clear_room = re.search(
            r"function clearRoomState\(reason\) \{(?P<body>.*?)\n  \}",
            isbot_script,
            re.S,
        )
        disable = re.search(
            r"disable: function\([^)]*\) \{(?P<body>.*?)\n    \},",
            isbot_script,
            re.S,
        )

        self.assertIsNotNone(clear_room)
        self.assertIsNotNone(disable)
        self.assertNotIn("roomCaptureCount = 0", clear_room.group("body"))
        self.assertIn("roomCaptureCount = 0", disable.group("body"))
        self.assertIn("roomCaptureCount >= 2 ? 'active' : 'awaiting_reenter'", isbot_script)
        self.assertIn("lastCaptureAtMs = Date.now()", isbot_script)
        self.assertIn("shouldIgnoreLateGameManagerDestroy()", isbot_script)

    def test_isbot_disabled_state_restores_next_capture_before_uninstalling_hook(self):
        isbot_script = (feature_dir("isbot") / "script.js").read_text(encoding="utf-8")
        capture = re.search(
            r"function handlePlayerCapture\(playerPtr\) \{(?P<body>.*?)\n  \}",
            isbot_script,
            re.S,
        )
        disable = re.search(
            r"disable: function\([^)]*\) \{(?P<body>.*?)\n    \},",
            isbot_script,
            re.S,
        )

        self.assertIsNotNone(capture)
        self.assertIsNotNone(disable)
        self.assertIn("pendingRestoreOnCapture", isbot_script)
        self.assertIn("restoreBotOnNextCapture()", capture.group("body"))
        self.assertIn("pendingRestoreOnCapture = true", disable.group("body"))
        self.assertIn("if (options && options.cleanup)", disable.group("body"))
        self.assertNotIn("if (restored) uninstallHook()", disable.group("body"))

    def test_isbot_disable_force_restores_current_client_data_on_cleanup(self):
        isbot_script = (feature_dir("isbot") / "script.js").read_text(encoding="utf-8")
        disable = re.search(
            r"disable: function\([^)]*\) \{(?P<body>.*?)\n    \},",
            isbot_script,
            re.S,
        )

        self.assertIsNotNone(disable)
        self.assertIn("function forceWriteBot(val)", isbot_script)
        self.assertIn("Process.findRangeByAddress", isbot_script)
        self.assertIn("writeBot(0) || forceWriteBot(0)", disable.group("body"))
        cleanup_body = isbot_script.split("function __pluginCleanup(payload)", 1)[1].split("rpc.exports = {", 1)[0]
        self.assertIn("module.disable({ cleanup: true })", cleanup_body)

    def test_weapon_giver_normal_failures_are_throttled(self):
        from core.plugin.module_loader import load_plugin_module

        events = load_plugin_module(feature_dir("weapon_giver"), "events")
        events = importlib.reload(events)
        emitted = []

        class FakeBus:
            def emit(self, event_name, **payload):
                emitted.append((event_name, payload))

        class FakeContext:
            event_bus = FakeBus()

        payload = {"taskId": 1, "success": False, "reason": "invalid_player"}

        events.handle_event(FakeContext(), "giveWeaponResult", payload)
        events.handle_event(FakeContext(), "giveWeaponResult", payload)

        self.assertEqual(len(emitted), 1)
        self.assertEqual(emitted[0][1]["level"], "warning")

    def test_weapon_giver_panel_resumes_hotkeys_when_built_after_connection(self):
        from core.plugin.module_loader import load_plugin_module

        events = load_plugin_module(feature_dir("weapon_giver"), "events")
        events = importlib.reload(events)
        sync_hotkeys = getattr(events, "sync_hotkeys_for_current_connection", None)
        self.assertTrue(callable(sync_hotkeys))

        calls = []

        class FakeContext:
            def __init__(self, connected):
                self._connected = connected

            def is_connected(self):
                return self._connected

        class FakeController:
            def init_hotkey_manager(self):
                calls.append("init")

        sync_hotkeys(FakeContext(True), FakeController())
        self.assertEqual(calls, ["init"])

        calls.clear()
        sync_hotkeys(FakeContext(False), FakeController())
        self.assertEqual(calls, [])

        panel_text = (feature_dir("weapon_giver") / "panel.py").read_text(encoding="utf-8")
        self.assertIn("sync_hotkeys_for_current_connection(context, controller)", panel_text)

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
        "unlimited_bag",
        "fast_gunstock",
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
                plugin_dir = feature_dir(feature_id)
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
            feature_text = (feature_dir(feature_id) / "feature.py").read_text(encoding="utf-8")
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
            "unlimited_bag": ("无限背包", "🎒", "在远离出生点时也能切换背包武器"),
            "fast_gunstock": ("极速枪托", "⚡", "枪托右键重击攻击速度更快"),
        }
        for feature_id, values in expected.items():
            with self.subTest(feature_id=feature_id):
                manifest = json.loads(
                    (feature_dir(feature_id) / "manifest.json").read_text(encoding="utf-8")
                )
                self.assertEqual(
                    (manifest["display_name"], manifest["icon"], manifest["desc"]),
                    values,
                )
                self.assertNotIn("?", manifest["display_name"] + manifest["icon"] + manifest["desc"])

    def test_unlimited_bag_and_fast_gunstock_manifest_integration(self):
        expected = {
            "unlimited_bag": {
                "category": "other",
                "tab": "other_tab",
                "tab_title": "其他",
                "rpc": ["enable", "disable", "setConfig", "status", "cleanup"],
                "handles": ["unlimited_bag_switch"],
                "desc": "在远离出生点时也能切换背包武器",
                "lines": [
                    "在远离出生点时也能切换背包武器。",
                ],
                "script_needles": [
                    "Player.SelectWeaponBag",
                    "HUD_Bag.Update",
                    "ObscuredBool.Encrypt",
                    "GameManager_TypeInfo: 0x0E2933C",
                    "GameManager_OnDestroy: 0xAFB6F0",
                    "function refreshLocalPlayerCache()",
                    "function clearLocalPlayerCache(reason)",
                    "function isLocalPlayer(player)",
                    "if (!isLocalPlayer(this._ubPlayer))",
                    "isKnownLocalWeaponBag(weaponBag)",
                    "var MAX_LOGS_PER_MODULE = 3",
                    "sendStatus('unlimited_bag', true)",
                    "setConfig: __pluginApplyConfig",
                    "cleanup: __pluginCleanup",
                ],
                "panel_needles": [
                    'fg_color="transparent"',
                    "callbacks[\"toggle\"](feature_id)",
                    "unlimited_bag_switch",
                ],
            },
            "fast_gunstock": {
                "category": "weapon",
                "tab": "weapon_tab",
                "tab_title": "武器",
                "rpc": ["enable", "disable", "setConfig", "status", "cleanup", "forceclear", "forceClear"],
                "handles": ["fast_gunstock_switch"],
                "desc": "枪托右键重击攻击速度更快",
                "lines": [
                    "枪托右键重击攻击速度更快。",
                ],
                "script_needles": [
                    "OnSpecialBtnDown",
                    "KnifeAttackEvent",
                    "OnKnifeAttackExit",
                    "var MAX_LOGS_PER_MODULE = 3",
                    "sendStatus('fast_gunstock', true)",
                    "forceClear: __pluginForceClear",
                    "rpc.exports.forceclear = rpc.exports.forceClear",
                ],
                "panel_needles": [
                    'fg_color="transparent"',
                    "callbacks[\"toggle\"](feature_id)",
                ],
            },
        }

        for feature_id, values in expected.items():
            with self.subTest(feature_id=feature_id):
                plugin_dir = feature_dir(feature_id)
                manifest = json.loads((plugin_dir / "manifest.json").read_text(encoding="utf-8"))
                script = (plugin_dir / "script.js").read_text(encoding="utf-8")
                panel = (plugin_dir / "panel.py").read_text(encoding="utf-8")

                self.assertEqual(manifest["category"], values["category"])
                self.assertEqual(manifest["tab"], values["tab"])
                self.assertEqual(manifest["tab_title"], values["tab_title"])
                self.assertEqual(manifest["desc"], values["desc"])
                self.assertEqual(manifest.get("ui_text", {}).get("lines"), values["lines"])
                self.assertEqual(manifest["controls"], [{"type": "switch", "action": "enable"}])
                self.assertNotIn("actions", manifest)
                self.assertNotIn("button", manifest.get("ui_handles", {}))
                for action in values["rpc"]:
                    self.assertIn(action, manifest["rpc"])
                for handle in values["handles"]:
                    self.assertIn(handle, manifest["ui_handles"].values())
                for needle in values["script_needles"]:
                    self.assertIn(needle, script)
                for needle in values["panel_needles"]:
                    self.assertIn(needle, panel)
                self.assertNotIn("CTkButton", panel)
                self.assertNotIn("threading", panel)
                self.assertNotIn('callbacks["action"]', panel)

    def test_unlimited_bag_uses_cached_gamemanager_myplayer_in_19_only(self):
        script_path = feature_dir("unlimited_bag") / "script.js"
        script = script_path.read_text(encoding="utf-8")
        self.assertIn("GameManager_TypeInfo: 0x0E2933C", script)
        self.assertIn("GameManager_OnDestroy: 0xAFB6F0", script)
        self.assertIn("Klass_staticFields: 0x5C", script)
        self.assertIn("GM_myPlayer: 0x00", script)
        self.assertIn("cachedMyPlayer: null", script)
        self.assertIn("cachedWeaponBag: null", script)
        self.assertIn("function getMyPlayer()", script)
        self.assertIn("function refreshLocalPlayerCache()", script)
        self.assertIn("function clearLocalPlayerCache(reason)", script)
        self.assertIn("function isLocalPlayer(player)", script)
        self.assertIn("player.equals(state.cachedMyPlayer)", script)
        self.assertIn("if (!isLocalPlayer(this._ubPlayer))", script)
        self.assertNotIn("Player_get_isMyPlayer", script)
        self.assertNotIn("state.isMyPlayerFn", script)
        self.assertIn("rememberLocalWeaponBag(this._ubBag)", script)
        self.assertIn("if (!isKnownLocalWeaponBag(weaponBag)) return;", script)
        self.assertIn("installGameManagerLifecycleHook(mod)", script)
        self.assertIn("clearLocalPlayerCache('GameManager.OnDestroy')", script)
        self.assertIn("clearLocalPlayerCache('cleanup')", script)
        self.assertLess(
            script.index("if (!isKnownLocalWeaponBag(weaponBag)) return;"),
            script.index("clearWeaponBagLimits(weaponBag, 'HUD_Bag.Update', verbose)"),
        )

    def test_formal_unlimited_bag_source_matches_cached_gamemanager_filter(self):
        workspace_root = PROJECT_DIR.parents[2]
        script_path = workspace_root / "05-正式功能" / "22-无限背包" / "AAAAA-unlimited_bag_min.js"
        script = script_path.read_text(encoding="utf-8")
        self.assertIn("GameManager_TypeInfo: 0x0E2933C", script)
        self.assertIn("GameManager_OnDestroy: 0xAFB6F0", script)
        self.assertIn("Klass_staticFields: 0x5C", script)
        self.assertIn("GM_myPlayer: 0x00", script)
        self.assertIn("cachedMyPlayer: null", script)
        self.assertIn("cachedWeaponBag: null", script)
        self.assertIn("function getMyPlayer()", script)
        self.assertIn("function refreshLocalPlayerCache()", script)
        self.assertIn("function clearLocalPlayerCache(reason)", script)
        self.assertIn("player.equals(state.cachedMyPlayer)", script)
        self.assertNotIn("Player_get_isMyPlayer", script)
        self.assertIn("installGameManagerLifecycleHook(mod)", script)
        self.assertIn("clearLocalPlayerCache('GameManager.OnDestroy')", script)
        self.assertIn("clearLocalPlayerCache('cleanup')", script)

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
        self.assertNotIn("LegacyMessageAdapter", frida_manager)
        self.assertNotIn("legacy_message_adapter", frida_manager)
        self.assertIn('"plugin_event"', app_events)
        for old_event in ("gather_result", "round_skipped", "nano4t_event", "battle_round_event", "isbot_event"):
            self.assertNotIn(f'"{old_event}"', frida_manager)
            self.assertNotIn(f'"{old_event}"', app_events)

    def test_panels_use_panel_context_not_full_app(self):
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
                self.assertIsNone(re.search(pattern, panel_text), msg=f"{panel_path}: {label}")

    def test_app_state_has_only_global_fields(self):
        state_text = (PROJECT_DIR / "core" / "state" / "app_state.py").read_text(encoding="utf-8")
        fields = set(re.findall(r"^\s{4}([a-zA-Z_][a-zA-Z0-9_]*)\s*:", state_text, re.MULTILINE))
        self.assertEqual(fields, {"features"})

    def test_safe_panel_context_has_no_legacy_methods(self):
        panel_context = (PROJECT_DIR / "ui" / "panel_context.py").read_text(encoding="utf-8")
        self.assertNotIn("LegacyPanelContext", panel_context)
        self.assertNotIn("legacy_for", panel_context)
        self.assertNotIn("context.legacy", panel_context)
        safe_match = re.search(
            r"class PanelContext\b(?P<body>.*?)(?=^class FeaturePanelContext\b)",
            panel_context,
            re.S | re.M,
        )
        self.assertIsNotNone(safe_match)
        safe_body = safe_match.group("body")
        for method in ("get_state", "set_state", "get_handle", "set_handle", "controller", "service"):
            self.assertIsNone(re.search(rf"^\s+def\s+{method}\b", safe_body, re.M))

    def test_startup_ui_events_are_queued_until_mainloop_is_ready(self):
        app_text = (PROJECT_DIR / "ui" / "app.py").read_text(encoding="utf-8")
        panel_context = (PROJECT_DIR / "ui" / "panel_context.py").read_text(encoding="utf-8")
        app_events = (PROJECT_DIR / "ui" / "controllers" / "app_event_controller.py").read_text(encoding="utf-8")

        self.assertIn("def _safe_after", app_text)
        self.assertIn("_mainloop_ready", app_text)
        self.assertIn("_pending_ui_callbacks", app_text)
        self.assertIn("main thread is not in main loop", app_text)
        self.assertIn('getattr(app, "_safe_after", app.after)', panel_context)
        self.assertNotIn("app.after(0, update)", app_events)
        self.assertNotIn("app.after(0, lambda: app._update_switch(feature_id))", app_events)

    def test_sound_manager_suppresses_pygame_support_prompt(self):
        sound_manager = (PROJECT_DIR / "core" / "sound_manager.py").read_text(encoding="utf-8")
        self.assertIn("PYGAME_HIDE_SUPPORT_PROMPT", sound_manager)

    def test_legacy_message_adapter_is_removed(self):
        self.assertFalse((PROJECT_DIR / "core" / "frida_runtime" / "legacy_message_adapter.py").exists())

    def test_future_feature_id_does_not_leak_into_center_files(self):
        center_paths = [
            PROJECT_DIR / "ui" / "app.py",
            PROJECT_DIR / "core" / "frida_manager.py",
            PROJECT_DIR / "ui" / "controllers" / "feature_action_controller.py",
            PROJECT_DIR / "ui" / "controllers" / "action_router.py",
            PROJECT_DIR / "core" / "state" / "app_state.py",
            PROJECT_DIR / "core" / "config.py",
        ]
        for path in center_paths:
            self.assertNotIn("third_person_camera", path.read_text(encoding="utf-8"), msg=str(path))

    def test_app_and_app_event_controller_have_no_special_feature_state(self):
        app_text = (PROJECT_DIR / "ui" / "app.py").read_text(encoding="utf-8")
        app_events = (PROJECT_DIR / "ui" / "controllers" / "app_event_controller.py").read_text(encoding="utf-8")
        all_feature_ids = self.ORDINARY_FEATURES | {"nano4t", "weapon_giver", "battle_round"}
        for needle in (
            "_nano4t_",
            "_battle_round",
            "_battle_mode",
            "_weapon_giver",
            "_isbot_state",
            "_weapon_hotkey_badges",
            "_weapon_top_frames",
            "_roundskip_monitor",
            "_weapon_controller",
            "_build_special_plugin_panel",
        ):
            self.assertNotIn(needle, app_text)
        self.assertNotIn("if fid ==", app_text)
        self.assertNotIn("if feature_id ==", app_text)
        for needle in all_feature_ids | {"third_person_camera"}:
            self.assertNotIn(f'"{needle}"', app_text)
            self.assertNotIn(f"'{needle}'", app_text)
        for needle in ("nano4t", "weapon_giver", "battle_round", "roundskip"):
            self.assertNotIn(needle, app_events)
        for event_name in ("game_connected", "game_disconnected", "game_not_found"):
            self.assertIn(event_name, app_events)

    def test_plugin_tab_builder_uses_manifest_tab_metadata(self):
        builder_text = (PROJECT_DIR / "ui" / "views" / "plugin_tab_builder.py").read_text(encoding="utf-8")
        for needle in ("weapon_tab", "player_tab", "other_tab", "武器", "人物属性", "其他", "ORDINARY_TABS"):
            self.assertNotIn(needle, builder_text)
        self.assertIn("tab_title", builder_text)
        self.assertIn("tab_order", builder_text)

    def test_all_manifests_have_tab_metadata_and_state_sync_rule(self):
        for manifest_path in (PROJECT_DIR / "features").glob("*/manifest.json"):
            if manifest_path.parent.name.startswith("_"):
                continue
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertIn("tab", manifest, msg=str(manifest_path))
            self.assertIn("tab_title", manifest, msg=str(manifest_path))
            self.assertIn("tab_order", manifest, msg=str(manifest_path))
            self.assertIn("state", manifest, msg=str(manifest_path))
            self.assertIn("sync_enabled_from_config", manifest["state"], msg=str(manifest_path))
            if manifest.get("ui", {}).get("mode") == "special_page":
                self.assertIn("tab_title", manifest["ui"], msg=str(manifest_path))
                self.assertIn("tab_order", manifest["ui"], msg=str(manifest_path))
                self.assertIn("lazy_build", manifest["ui"], msg=str(manifest_path))

    def test_plugin_routers_isolate_handler_and_import_failures(self):
        event_router = (PROJECT_DIR / "ui" / "controllers" / "plugin_event_router.py").read_text(encoding="utf-8")
        lifecycle_router = (PROJECT_DIR / "ui" / "controllers" / "plugin_lifecycle_router.py").read_text(encoding="utf-8")
        for text in (event_router, lifecycle_router):
            self.assertIn("try:", text)
            self.assertIn("except Exception as exc", text)
            self.assertIn("dev_detail=str(exc)", text)
            self.assertIn("log_message", text)
            self.assertRegex(text, r"self\._handlers\[feature_id\]\s*=\s*None")

    def test_feature_specific_controllers_moved_to_feature_dirs(self):
        for path in (
            PROJECT_DIR / "ui" / "controllers" / "battle_round_controller.py",
            PROJECT_DIR / "ui" / "controllers" / "nano4t_runtime_controller.py",
            PROJECT_DIR / "ui" / "controllers" / "nano4t_selection_controller.py",
            PROJECT_DIR / "ui" / "controllers" / "weapon_interaction_controller.py",
            PROJECT_DIR / "ui" / "controllers" / "round_skip_monitor.py",
            PROJECT_DIR / "core" / "services" / "game_action_service.py",
            PROJECT_DIR / "core" / "services" / "weapon_giver_service.py",
        ):
            self.assertFalse(path.exists(), msg=str(path))
        for path in (
            feature_dir("weapon_giver") / "controller.py",
            feature_dir("weapon_giver") / "service.py",
            feature_dir("weapon_giver") / "hotkeys.py",
            feature_dir("nano4t") / "runtime.py",
            feature_dir("nano4t") / "selection.py",
            feature_dir("battle_round") / "controller.py",
            feature_dir("roundskip") / "monitor.py",
        ):
            self.assertTrue(path.exists(), msg=str(path))

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

