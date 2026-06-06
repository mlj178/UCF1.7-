import os
import re
import sys
import unittest
from unittest.mock import patch


GAME_MODIFIER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if GAME_MODIFIER_DIR not in sys.path:
    sys.path.insert(0, GAME_MODIFIER_DIR)

from core.universal_hook_manager import UniversalHookManager


class UniversalHookManagerTests(unittest.TestCase):
    def test_dll_module_lookups_do_not_increment_self_reference(self):
        project_dir = os.path.abspath(os.path.join(
            GAME_MODIFIER_DIR,
            "..",
            "..",
            "..",
            "05-正式功能",
            "17-Universal-ESP盒子",
            "Universal-Dear-ImGui-Hook",
        ))
        offenders = []

        for name in ("stdafx.h", "dllmain.cpp"):
            path = os.path.join(project_dir, name)
            with open(path, "r", encoding="utf-8", errors="ignore") as source:
                text = source.read()
            for call in re.findall(
                r"GetModuleHandleExW\s*\((.*?)\);",
                text,
                flags=re.DOTALL,
            ):
                if "GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT" not in call:
                    offenders.append(name)

        self.assertEqual(offenders, [])

    def test_pending_dll_update_replaces_release_dll(self):
        manager = UniversalHookManager()

        with patch(
            "core.universal_hook_manager.os.path.exists",
            return_value=True,
        ), patch(
            "core.universal_hook_manager.os.replace",
        ) as replace:
            result = manager._apply_pending_update()

        self.assertTrue(result)
        replace.assert_called_once_with(
            manager._pending_dll_path,
            manager._dll_path,
        )

    def test_loaded_dll_connection_failure_is_not_an_injection_attempt(self):
        manager = UniversalHookManager()

        with patch.object(
            manager,
            "_is_dll_loaded",
            return_value=True,
        ), patch.object(
            manager,
            "try_connect_existing",
            return_value=False,
        ):
            result = manager.inject_and_connect(456)

        self.assertFalse(result)
        self.assertFalse(manager.last_injection_attempted)

    def test_unload_sends_command_and_clears_connection(self):
        manager = UniversalHookManager()
        manager._pipe = 123
        manager._pid = 456

        with patch.object(
            manager,
            "_send",
            return_value={"ok": True},
        ) as send, patch.object(manager, "_close_pipe") as close_pipe:
            result = manager.unload()

        self.assertTrue(result)
        send.assert_called_once_with({"cmd": "unload"})
        close_pipe.assert_called_once_with()
        self.assertIsNone(manager._pid)
        self.assertEqual(manager._revision, 0)


if __name__ == "__main__":
    unittest.main()
