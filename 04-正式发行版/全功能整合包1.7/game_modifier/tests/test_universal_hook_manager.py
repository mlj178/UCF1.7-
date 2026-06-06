import os
import sys
import unittest
from unittest.mock import patch


GAME_MODIFIER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if GAME_MODIFIER_DIR not in sys.path:
    sys.path.insert(0, GAME_MODIFIER_DIR)

from core.universal_hook_manager import UniversalHookManager


class UniversalHookManagerTests(unittest.TestCase):
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
