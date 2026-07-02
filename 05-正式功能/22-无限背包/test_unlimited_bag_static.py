import re
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "AAAAA-unlimited_bag_min.js"
UI_FILE = BASE_DIR / "AAAAA-unlimited_bag_ui.py"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class UnlimitedBagStaticTests(unittest.TestCase):

    def test_js_contains_verified_rvas_and_offsets(self):
        text = read_text(JS_FILE)

        required_tokens = [
            "SelectWeaponBag: 0xB52830",
            "HudBagUpdate: 0xB00360",
            "ObscuredBoolEncrypt: 0x7F93D0",
            "Player_weaponBag: 0xA4",
            "WeaponBag_disabled: 0x8",
            "WeaponBag_tooFarFromSpawnPos: 0x14",
            "HudBag_bag: 0x2C",
        ]

        for token in required_tokens:
            self.assertIn(token, text)

    def test_js_uses_attach_hooks_and_keeps_original_game_flow(self):
        text = read_text(JS_FILE)

        self.assertIn("Interceptor.attach", text)
        self.assertNotIn("Interceptor.replace", text)
        self.assertRegex(text, r"SelectWeaponBag\s*:")
        self.assertIn("clearWeaponBagLimits", text)
        self.assertIn("writeObscuredBoolFalse", text)

    def test_js_exports_minimum_rpc_controls(self):
        text = read_text(JS_FILE)

        self.assertIn("rpc.exports", text)
        for export_name in ["enable", "disable", "status", "cleanup"]:
            self.assertRegex(text, rf"\b{export_name}\s*:")

    def test_customtkinter_ui_loads_minimum_script_and_rpc(self):
        text = read_text(UI_FILE)

        self.assertIn("import customtkinter as ctk", text)
        self.assertIn("import frida", text)
        self.assertIn("import psutil", text)
        self.assertIn('JS_FILE = os.path.join(BASE_DIR, "AAAAA-unlimited_bag_min.js")', text)
        self.assertIn('GAME_PROCESS_NAME = "UnityCrossFire.exe"', text)
        self.assertIn("ctk.CTkSwitch", text)
        self.assertIn("ctk.CTkTextbox", text)
        self.assertIn("self.script.exports_sync.enable()", text)
        self.assertIn("self.script.exports_sync.disable()", text)
        self.assertIn("self.script.exports_sync.status()", text)
        self.assertIn("self.script.exports_sync.cleanup()", text)

    def test_ui_does_not_shadow_tk_state_method(self):
        text = read_text(UI_FILE)

        self.assertNotIn("self.state =", text)
        self.assertNotIn("self.state.update", text)
        self.assertIn("self.game_state =", text)
        self.assertIn("self.game_state.update", text)


if __name__ == "__main__":
    unittest.main()
