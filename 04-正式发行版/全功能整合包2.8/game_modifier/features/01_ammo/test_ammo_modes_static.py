import importlib.util
import json
import sys
import types
import unittest
from pathlib import Path


FEATURE_DIR = Path(__file__).parent


class _FakeWidget:
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self._value = kwargs.get("value")

    def pack(self, *args, **kwargs):
        return None

    def grid(self, *args, **kwargs):
        return None

    def configure(self, *args, **kwargs):
        return None

    def set(self, value):
        self._value = value

    def get(self):
        return self._value


class _FakeVar:
    def __init__(self, value=None, **kwargs):
        self._value = value

    def get(self):
        return self._value

    def set(self, value):
        self._value = value


def _fake_ctk():
    module = types.SimpleNamespace()
    for name in ("CTkFrame", "CTkLabel", "CTkSwitch", "CTkComboBox", "CTkButton"):
        setattr(module, name, _FakeWidget)
    module.BooleanVar = _FakeVar
    module.StringVar = _FakeVar
    module.DoubleVar = _FakeVar
    return module


class AmmoModesStaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.modules["customtkinter"] = _fake_ctk()
        spec = importlib.util.spec_from_file_location("ammo_panel_under_test", FEATURE_DIR / "panel.py")
        cls.panel = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.panel)
        cls.manifest = json.loads((FEATURE_DIR / "manifest.json").read_text(encoding="utf-8"))
        cls.script = (FEATURE_DIR / "script.js").read_text(encoding="utf-8")

    def test_manifest_has_two_switches_and_two_scopes(self):
        controls = {
            item.get("key"): item
            for item in self.manifest["controls"]
            if item.get("key")
        }
        for key in (
            "infinite_bullet_enabled",
            "infinite_bullet_scope",
            "infinite_ammo_enabled",
            "infinite_ammo_scope",
        ):
            self.assertIn(key, controls)
        self.assertTrue(self.manifest["config"]["infinite_bullet_enabled"])
        self.assertFalse(self.manifest["config"]["infinite_ammo_enabled"])
        for key in ("infinite_bullet_scope", "infinite_ammo_scope"):
            self.assertEqual(controls[key]["values"], ["player_only", "all_players"])

    def test_panel_returns_both_switch_and_scope_handles(self):
        calls = []
        callbacks = {
            "toggle": lambda fid: calls.append(("toggle", fid)),
            "set_config": lambda fid, key, value: calls.append((fid, key, value)),
        }
        handles = self.panel.build_card(None, self.manifest, 0, 0, 1, callbacks, None)
        for key in (
            "ammo_switch",
            "infinite_bullet_enabled_var",
            "infinite_bullet_enabled_switch",
            "infinite_bullet_scope_var",
            "infinite_bullet_scope_combo",
            "infinite_ammo_enabled_var",
            "infinite_ammo_enabled_switch",
            "infinite_ammo_scope_var",
            "infinite_ammo_scope_combo",
        ):
            self.assertIn(key, handles)
        self.assertEqual(handles["infinite_bullet_enabled_var"].get(), True)
        self.assertEqual(handles["infinite_ammo_enabled_var"].get(), False)
        self.assertEqual(handles["infinite_bullet_scope_var"].get(), "仅限玩家")
        self.assertEqual(handles["infinite_ammo_scope_var"].get(), "仅限玩家")

    def test_script_reuses_native_buff_flag_and_keeps_bullet_hook(self):
        self.assertIn("0xB547F0", self.script)
        self.assertIn("0x128", self.script)
        self.assertIn("0xB61140", self.script)
        for address in ("0xB66E80", "0xB67AF0", "0xB67C40", "0xB67BC0"):
            self.assertIn(address, self.script)
        self.assertIn("base.add(0xB17120)", self.script)
        self.assertNotIn("0x10B17120", self.script)
        self.assertIn("infinite_ammo_enabled", self.script)
        self.assertIn("infinite_bullet_enabled", self.script)
        self.assertIn("Player.UpdateBuffProperty", self.script)


if __name__ == "__main__":
    unittest.main()