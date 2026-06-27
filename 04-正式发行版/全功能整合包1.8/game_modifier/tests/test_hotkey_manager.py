import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import core.hotkey_manager as hotkey_manager_module
from core.hotkey_manager import HotkeyManager


class HotkeyManagerTests(unittest.TestCase):
    def test_set_hotkey_is_memory_only_until_save_and_apply(self):
        with TemporaryDirectory() as tmp_dir:
            hotkeys_file = Path(tmp_dir) / "hotkeys.json"
            old_file = hotkey_manager_module.HOTKEYS_FILE
            hotkey_manager_module.HOTKEYS_FILE = str(hotkeys_file)
            try:
                manager = HotkeyManager()
                manager.set_hotkey("ctrl+1", "knife")

                self.assertFalse(hotkeys_file.exists())

                setup_calls = []
                manager.setup_hotkeys = lambda callback, silent=False: setup_calls.append((callback, silent))
                callback = lambda feature_id: feature_id
                manager.save_and_apply(callback, silent=True)

                self.assertEqual(json.loads(hotkeys_file.read_text(encoding="utf-8"))["ctrl+1"], "knife")
                self.assertEqual(setup_calls, [(callback, True)])
            finally:
                hotkey_manager_module.HOTKEYS_FILE = old_file


if __name__ == "__main__":
    unittest.main()
