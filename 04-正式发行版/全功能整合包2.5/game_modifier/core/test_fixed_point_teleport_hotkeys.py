import ast
import json
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
CONFIG_FILE = PROJECT_DIR / "core" / "config.py"
APP_FILE = PROJECT_DIR / "ui" / "app.py"
FEATURE_DIR = PROJECT_DIR / "features" / "31_fixed_point_teleport"


def assigned_literal(source: str, name: str):
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise AssertionError(f"Missing assignment: {name}")


class FixedPointTeleportHotkeyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_text = CONFIG_FILE.read_text(encoding="utf-8")
        cls.positions = assigned_literal(cls.config_text, "HOTKEY_POSITIONS")
        cls.display_names = assigned_literal(cls.config_text, "HOTKEY_DISPLAY_NAMES")
        cls.dedicated = assigned_literal(cls.config_text, "DEDICATED_HOTKEY_ACTIONS")

    def test_point_two_uses_f1_and_f2_as_dedicated_hotkeys(self):
        self.assertEqual(
            self.dedicated["f1"],
            {
                "feature_id": "fixed_point_teleport",
                "action": "savepoint2",
                "label": "定点瞬移：保存点位2",
            },
        )
        self.assertEqual(
            self.dedicated["f2"],
            {
                "feature_id": "fixed_point_teleport",
                "action": "teleporttopoint2",
                "label": "定点瞬移：瞬移到点位2",
            },
        )

    def test_removed_hotkeys_are_absent_from_core_configuration(self):
        for hotkey in ("f3", "alt+3", "alt+4"):
            self.assertNotIn(hotkey, self.positions)
            self.assertNotIn(hotkey, self.display_names)
            self.assertNotIn(hotkey, self.dedicated)

        saved_hotkeys = json.loads((PROJECT_DIR / "data" / "hotkeys.json").read_text(encoding="utf-8"))
        self.assertIsNone(saved_hotkeys["f1"])
        self.assertIsNone(saved_hotkeys["f2"])
        for hotkey in ("f3", "alt+3", "alt+4"):
            self.assertNotIn(hotkey, saved_hotkeys)

    def test_tk_listener_leaves_f1_f2_to_native_global_hotkeys(self):
        app_text = APP_FILE.read_text(encoding="utf-8")
        method_text = app_text.split("    def _setup_tk_hotkeys(self):", 1)[1].split(
            "    def _on_tk_hotkey", 1
        )[0]
        for token in ("'<Alt-Key-1>': 'alt+1'", "'<Alt-Key-2>': 'alt+2'"):
            self.assertIn(token, method_text)
        for token in ("<F1>", "<F2>", "<F3>", "<Alt-Key-3>", "<Alt-Key-4>"):
            self.assertNotIn(token, method_text)

    def test_feature_copy_describes_f1_f2_without_removed_alt_hotkeys(self):
        manifest = json.loads((FEATURE_DIR / "manifest.json").read_text(encoding="utf-8"))
        labels = {control.get("action"): control.get("label") for control in manifest["controls"]}
        self.assertEqual(labels["savepoint2"], "保存点位2  F1")
        self.assertEqual(labels["teleporttopoint2"], "瞬移到点位2  F2")

        panel_text = (FEATURE_DIR / "panel.py").read_text(encoding="utf-8")
        doc_text = (FEATURE_DIR / "定点瞬移-简要说明.md").read_text(encoding="utf-8")
        for text in (panel_text, doc_text):
            self.assertIn("F1", text)
            self.assertIn("F2", text)
            self.assertNotIn("Alt+3", text)
            self.assertNotIn("Alt+4", text)


if __name__ == "__main__":
    unittest.main()
