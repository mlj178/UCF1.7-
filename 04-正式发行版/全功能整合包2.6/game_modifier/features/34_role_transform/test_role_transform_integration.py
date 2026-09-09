import importlib.util
import json
import unittest
from pathlib import Path

from core.plugin.manifest_loader import ManifestLoader
from ui.controllers.action_router import ActionRouter


ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "script.js"
MANIFEST = ROOT / "manifest.json"
PANEL = ROOT / "panel.py"
EXPECTED_ACTIONS = {
    "local_hero",
    "local_terminator",
    "bot_hero",
    "bot_terminator",
}
SOURCE_DIR = ROOT.parents[4] / "05-正式功能" / "34-角色变身"
SOURCE_SCRIPT = SOURCE_DIR / "AAAAA-role_transform_min.js"
PERSISTENCE_RECORD = (
    ROOT.parents[4]
    / "02-开发规范"
    / "20-整合包接入"
    / "22-功能开关与参数持久化记录.md"
)


def load_panel_module():
    spec = importlib.util.spec_from_file_location("role_transform_panel_test", PANEL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RoleTransformIntegrationTests(unittest.TestCase):
    def test_plugin_delivery_files_exist(self):
        expected_files = {
            "__init__.py",
            "events.py",
            "feature.py",
            "manifest.json",
            "panel.py",
            "script.js",
        }

        missing = sorted(name for name in expected_files if not (ROOT / name).is_file())

        self.assertEqual([], missing)

    def test_trigger_accepts_payload_and_lazy_enables_before_queueing(self):
        script = SCRIPT.read_text(encoding="utf-8")
        body = script.split("function queueAction", 1)[1].split(
            "function status", 1
        )[0]

        self.assertIn("actionOrPayload", body)
        self.assertIn("actionOrPayload.action", body)
        self.assertIn("enableFeature()", body)
        self.assertLess(body.index("enableFeature()"), body.index("Runtime.pendingAction = action"))

    def test_cleanup_accepts_integrated_runtime_payload(self):
        script = SCRIPT.read_text(encoding="utf-8")

        self.assertIn("function cleanupFeature(_payload)", script)

    def test_manifest_declares_inline_one_shot_actions(self):
        self.assertTrue(MANIFEST.is_file(), "manifest.json must be created")
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

        self.assertEqual("role_transform", manifest["feature_id"])
        self.assertEqual("nano4t_tab", manifest["tab"])
        self.assertEqual("多人生化", manifest["tab_title"])
        self.assertEqual("special_inline_card", manifest["ui"]["mode"])
        self.assertFalse(manifest["lifecycle"]["restore"])
        self.assertFalse(manifest["state"]["sync_enabled_from_config"])
        buttons = [item for item in manifest["controls"] if item.get("type") == "button"]
        self.assertEqual(
            EXPECTED_ACTIONS,
            {item["payload"]["action"] for item in buttons},
        )
        self.assertEqual({"trigger"}, {item["action"] for item in buttons})
        switches = [item for item in manifest["controls"] if item.get("type") == "switch"]
        self.assertEqual(1, len(switches))
        self.assertEqual("enable", switches[0]["action"])
        self.assertEqual("role_transform_switch", manifest["ui_handles"]["switch"])
        self.assertTrue(manifest["actions"]["trigger"]["requires_connection"])
        self.assertEqual(
            "05-正式功能/34-角色变身/AAAAA-role_transform_min.js",
            manifest["source"]["single_feature_js"],
        )
        self.assertEqual(
            "05-正式功能/34-角色变身/AAAAA-role_transform_ui.py",
            manifest["source"].get("single_feature_py"),
        )

    def test_panel_routes_manifest_payloads_through_generic_action_callback(self):
        self.assertTrue(PANEL.is_file(), "panel.py must be created")
        panel = PANEL.read_text(encoding="utf-8")

        self.assertIn('callbacks["action"](feature_id, action, payload)', panel)
        self.assertIn('control.get("payload")', panel)
        self.assertNotIn("FridaManager", panel)
        self.assertNotIn("app._", panel)

    def test_script_keeps_verified_main_thread_transform_routes(self):
        script = SCRIPT.read_text(encoding="utf-8")

        for token in (
            "ModeBase_Update: 0x00AF6A00",
            "NanoRoleSelect_OpenMasterRole: 0x00B4ED30",
            "Mode_Nano4_Terminator_BecomeRandomMasterHero: 0x00B42E90",
            "Mode_Nano4_Terminator_TryBecomeRandomMasterTerminator: 0x00B45B90",
            "function consumePendingAction",
            "Native.openMasterRole(selector, isHero ? 1 : 0, ptr(0))",
            "Native.becomeRandomMasterHero(mode, player, 0, ptr(0))",
            "Native.tryBecomeRandomMasterTerminator(mode, player, ptr(0))",
        ):
            self.assertIn(token, script)

    def test_panel_places_itself_after_existing_inline_cards(self):
        panel = load_panel_module()

        self.assertTrue(
            hasattr(panel, "_next_available_row"),
            "panel must avoid overlapping the existing skill cooldown card",
        )

        class ExistingCard:
            @staticmethod
            def grid_info():
                return {"row": 0, "rowspan": 2}

        class InlineHost:
            @staticmethod
            def grid_slaves():
                return [ExistingCard()]

        self.assertEqual(2, panel._next_available_row(InlineHost(), requested_row=0))

    def test_manifest_loader_discovers_role_transform_plugin(self):
        manifests = ManifestLoader(ROOT.parent, logger=lambda _message: None).load()
        role_transform = next(
            item for item in manifests if item.get("feature_id") == "role_transform"
        )

        self.assertEqual(ROOT, Path(role_transform["_plugin_dir"]).resolve())

    def test_runtime_script_is_source_script_plus_minimal_integration_patch(self):
        source = SOURCE_SCRIPT.read_text(encoding="utf-8")
        expected = source.replace(
            "function cleanupFeature() {",
            "function cleanupFeature(_payload) {",
        )
        expected = expected.replace(
            """function queueAction(action) {
        if (!VALID_ACTIONS[action]) {""",
            """function queueAction(actionOrPayload) {
        var action = typeof actionOrPayload === 'string'
            ? actionOrPayload
            : actionOrPayload && actionOrPayload.action;
        if (!VALID_ACTIONS[action]) {""",
        )
        expected = expected.replace(
            """if (!Runtime.enabled || !Runtime.initialized) {
            reject('feature is disabled');
            return status();
        }
        if (Runtime.pendingAction) {""",
            """if (!Runtime.enabled || !Runtime.initialized) {
            enableFeature();
        }
        if (!Runtime.enabled || !Runtime.initialized) {
            reject('feature initialization failed');
            return status();
        }
        if (Runtime.pendingAction) {""",
        )

        self.assertEqual(expected, SCRIPT.read_text(encoding="utf-8"))

    def test_persistence_record_marks_actions_as_non_restoring(self):
        record = PERSISTENCE_RECORD.read_text(encoding="utf-8")

        self.assertIn(
            "| 34-角色变身 | 四个变身按钮 | 不记录动作或参数 | 不恢复 |",
            record,
        )

    def test_action_router_forwards_button_payload_to_trigger_rpc(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        control = next(
            item
            for item in manifest["controls"]
            if (item.get("payload") or {}).get("action") == "local_hero"
        )
        calls = []

        class Feature:
            def __init__(self):
                self.manifest = manifest

        class Registry:
            @staticmethod
            def get(feature_id):
                return Feature() if feature_id == "role_transform" else None

        class Service:
            @staticmethod
            def call_action(feature_id, action, payload):
                calls.append((feature_id, action, payload))
                return {"ok": True}

        router = ActionRouter(
            registry=Registry(),
            feature_service=Service(),
            config_manager=None,
            state={},
            is_connected=lambda: True,
            logger=lambda _message: None,
            update_switch=lambda _feature_id: None,
            sync_config=lambda *_args: None,
            schedule_save=lambda: None,
        )

        result = router.action(
            "role_transform",
            control["action"],
            dict(control["payload"]),
        )

        self.assertEqual({"ok": True}, result)
        self.assertEqual(
            [("role_transform", "trigger", {"action": "local_hero"})],
            calls,
        )


if __name__ == "__main__":
    unittest.main()
