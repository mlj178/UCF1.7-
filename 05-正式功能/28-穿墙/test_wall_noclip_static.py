import re
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "AAAAA-wall_noclip_min.js"
UI_FILE = BASE_DIR / "AAAAA-wall_noclip_ui.py"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class WallNoclipStaticTests(unittest.TestCase):

    def test_js_contains_verified_rvas_offsets_and_feature_id(self):
        text = read_text(JS_FILE)

        required_tokens = [
            'feature_id: "wall_noclip"',
            "Player_get_isMyPlayer: 0x00B55FD0",
            "Player_MoveByLocalDirection: 0x00B50A00",
            "CharacterController_Move: 0x00AB8210",
            "Component_get_transform: 0x0032CF40",
            "Transform_get_position_Injected: 0x003F4280",
            "Transform_set_position_Injected: 0x003F4810",
            "Player_characterController: 0x2C",
        ]

        for token in required_tokens:
            self.assertIn(token, text)

    def test_js_uses_attach_not_replace_and_preserves_vertical_move(self):
        text = read_text(JS_FILE)

        self.assertIn("Interceptor.attach", text)
        self.assertNotIn("Interceptor.replace", text)
        self.assertIn("applyHorizontalNoclip", text)
        self.assertIn("beforePosition", text)
        self.assertNotIn("args[1] = floatToStackArg(0.0)", text)
        self.assertNotIn("args[3] = floatToStackArg(0.0)", text)
        self.assertNotIn("args[2] = floatToStackArg(0.0)", text)

    def test_js_applies_horizontal_offset_after_original_move(self):
        text = read_text(JS_FILE)

        move_hook = text.split("attachHook('UnityEngine.CharacterController.Move'", 1)[1]
        self.assertIn("onLeave:", move_hook)
        on_enter = move_hook.split("onLeave:", 1)[0]
        on_leave = move_hook.split("onLeave:", 1)[1].split("});", 1)[0]

        self.assertIn("this.motionX", on_enter)
        self.assertIn("this.motionZ", on_enter)
        self.assertIn("this.beforePosition", on_enter)
        self.assertNotIn("applyHorizontalNoclip", on_enter)
        self.assertIn(
            "applyHorizontalNoclip(this.controller, this.beforePosition, this.motionX, this.motionZ)",
            on_leave,
        )

    def test_js_requires_alt_key_before_horizontal_noclip(self):
        text = read_text(JS_FILE)

        self.assertIn("VK_MENU: 0x12", text)
        self.assertIn("requireAltKey: true", text)
        self.assertIn("GetAsyncKeyState", text)
        self.assertIn("'stdcall'", text)
        self.assertIn("function isAltNoclipKeyDown()", text)
        self.assertIn("if (Runtime.config.requireAltKey && !isAltNoclipKeyDown()) {", text)
        self.assertIn("Runtime.stats.altGateSkipped += 1;", text)
        self.assertIn("alt_key_required: Runtime.config.requireAltKey", text)
        self.assertIn("alt_key_down: isAltNoclipKeyDown()", text)

    def test_js_exports_standard_rpc_and_lifecycle_helpers(self):
        text = read_text(JS_FILE)

        self.assertIn("rpc.exports", text)
        for export_name in ["enable", "disable", "status", "cleanup", "setconfig"]:
            self.assertRegex(text, rf"\b{export_name}\s*:")

        for helper in ["resetRuntime", "cleanupHooks", "enableFeature", "disableFeature"]:
            self.assertIn(helper, text)

    def test_ui_loads_script_and_uses_standard_rpc(self):
        text = read_text(UI_FILE)

        self.assertIn("import customtkinter as ctk", text)
        self.assertIn("import frida", text)
        self.assertIn("import psutil", text)
        self.assertIn('JS_FILE = os.path.join(BASE_DIR, "AAAAA-wall_noclip_min.js")', text)
        self.assertIn('GAME_PROCESS_NAME = "UnityCrossFire.exe"', text)
        self.assertIn("ctk.CTkSwitch", text)
        self.assertIn("ctk.CTkTextbox", text)
        self.assertIn("self.script.exports_sync.enable()", text)
        self.assertIn("self.script.exports_sync.disable()", text)
        self.assertIn("self.script.exports_sync.status()", text)
        self.assertIn("self.script.exports_sync.cleanup()", text)

    def test_no_accidental_flight_ui_controls(self):
        text = read_text(UI_FILE) + "\n" + read_text(JS_FILE)

        self.assertNotRegex(text, re.compile(r"fly|free[_ -]?camera|vertical[_ -]?speed", re.I))
        self.assertNotIn("VK_SPACE", text)


if __name__ == "__main__":
    unittest.main()
