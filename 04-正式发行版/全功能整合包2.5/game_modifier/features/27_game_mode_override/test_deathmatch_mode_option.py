import importlib.util
import json
import re
import sys
import types
import unittest
from pathlib import Path


FEATURE_DIR = Path(__file__).parent
PANEL_PATH = FEATURE_DIR / "panel.py"
MANIFEST_PATH = FEATURE_DIR / "manifest.json"
SCRIPT_PATH = FEATURE_DIR / "script.js"


def load_panel_module():
    sys.modules.setdefault("customtkinter", types.SimpleNamespace())
    spec = importlib.util.spec_from_file_location(
        "game_mode_override_panel_under_test",
        PANEL_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DeathmatchModeOptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel = load_panel_module()
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.script = SCRIPT_PATH.read_text(encoding="utf-8")
        cls.mode_control = next(
            control
            for control in cls.manifest["controls"]
            if control.get("key") == "mode_key"
        )

    def test_panel_exposes_personal_competition(self):
        self.assertEqual(self.panel.MODE_OPTIONS["个人竞技"], "death_match")

    def test_manifest_declares_death_match(self):
        self.assertIn("death_match", self.mode_control["values"])
        self.assertEqual(
            self.mode_control["display_values"]["death_match"],
            "个人竞技",
        )

    def test_script_maps_death_match_to_native_mode(self):
        pattern = re.compile(
            r"death_match\s*:\s*\{\s*label\s*:\s*'个人竞技'\s*,\s*"
            r"gameMode\s*:\s*1\s*,\s*weaponLimited\s*:\s*0\s*\}",
            re.MULTILINE,
        )
        self.assertRegex(self.script, pattern)

    def test_panel_and_manifest_mode_keys_stay_in_sync(self):
        self.assertEqual(
            set(self.panel.MODE_OPTIONS.values()),
            set(self.mode_control["values"]),
        )


if __name__ == "__main__":
    unittest.main()
