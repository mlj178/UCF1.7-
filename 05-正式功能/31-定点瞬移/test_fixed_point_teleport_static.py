import re
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "AAAAA-fixed_point_teleport_min.js"
UI_FILE = BASE_DIR / "AAAAA-fixed_point_teleport_ui.py"
DOC_FILE = BASE_DIR / "定点瞬移-简要说明.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class FixedPointTeleportStaticTests(unittest.TestCase):

    def test_js_contains_feature_id_rvas_and_offsets(self):
        text = read_text(JS_FILE)

        required_tokens = [
            'feature_id: "fixed_point_teleport"',
            "Player_Update: 0x00B551D0",
            "Player_get_isMyPlayer: 0x00B55FD0",
            "Player_SetPos: 0x00B534C0",
            "Component_get_transform: 0x0032CF40",
            "Transform_get_position_Injected: 0x003F4280",
            "Player_characterController: 0x2C",
        ]

        for token in required_tokens:
            self.assertIn(token, text)

    def test_js_uses_player_setpos_for_teleport_and_does_not_replace(self):
        text = read_text(JS_FILE)

        self.assertIn("Interceptor.attach", text)
        self.assertNotIn("Interceptor.replace", text)
        self.assertIn("native.playerSetPos", text)
        self.assertIn("function teleportToSavedPoint()", text)
        self.assertIn("native.playerSetPos(player, point.x, point.y, point.z, ptr(0))", text)
        self.assertNotIn("Transform_set_position_Injected", text)

    def test_js_saves_position_from_local_player_only(self):
        text = read_text(JS_FILE)

        self.assertIn("function captureLocalPlayer", text)
        self.assertIn("native.isMyPlayer(player, ptr(0))", text)
        self.assertIn("function saveCurrentPoint()", text)
        self.assertIn("Runtime.savedPoint", text)
        self.assertIn("saved_point", text)

    def test_js_exports_standard_rpc_and_point_commands(self):
        text = read_text(JS_FILE)

        self.assertIn("rpc.exports", text)
        for export_name in [
            "enable",
            "disable",
            "status",
            "cleanup",
            "setconfig",
            "savepoint",
            "teleporttopoint",
            "clearpoint",
        ]:
            self.assertRegex(text, rf"\b{export_name}\s*:")

        for status_key in [
            "has_saved_point",
            "saved_point",
            "last_teleport_result",
            "save_count",
            "teleport_count",
        ]:
            self.assertIn(status_key, text)

    def test_ui_loads_script_and_uses_standard_rpc(self):
        text = read_text(UI_FILE)

        self.assertIn("import customtkinter as ctk", text)
        self.assertIn("import frida", text)
        self.assertIn("import psutil", text)
        self.assertIn('JS_FILE = os.path.join(BASE_DIR, "AAAAA-fixed_point_teleport_min.js")', text)
        self.assertIn('GAME_PROCESS_NAME = "UnityCrossFire.exe"', text)
        self.assertIn("ctk.CTkSwitch", text)
        self.assertIn("ctk.CTkButton", text)
        self.assertIn("ctk.CTkTextbox", text)
        self.assertIn("self.script.exports_sync.enable()", text)
        self.assertIn("self.script.exports_sync.disable()", text)
        self.assertIn("self.script.exports_sync.status()", text)
        self.assertIn("self.script.exports_sync.cleanup()", text)
        self.assertIn("self.script.exports_sync.setconfig", text)
        self.assertIn("self.script.exports_sync.savepoint()", text)
        self.assertIn("self.script.exports_sync.teleporttopoint()", text)
        self.assertIn("self.script.exports_sync.clearpoint()", text)

    def test_ui_stays_single_point_without_hotkeys_or_multislot(self):
        text = read_text(UI_FILE)

        self.assertNotRegex(text, re.compile(r"hotkey|keyboard|RegisterHotKey|VK_", re.I))
        self.assertNotRegex(text, re.compile(r"slot|multi|槽位|多点", re.I))
        self.assertIn("保存当前位置", text)
        self.assertIn("瞬移到保存点", text)

    def test_doc_records_sources_and_minimal_scope(self):
        text = read_text(DOC_FILE)

        for token in [
            "feature_id: fixed_point_teleport",
            "Player.SetPos",
            "RVA 0xB534C0",
            "Player.Update",
            "RVA 0xB551D0",
            "Player.get_isMyPlayer",
            "RVA 0xB55FD0",
            "第一版只做单保存点",
        ]:
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
