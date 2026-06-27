import unittest

from core.frida_manager import FridaManager
from core.game_session_manager import GameSessionManager


class FakeCleanupExports:
    def __init__(self, calls):
        self._calls = calls

    def cleanup(self, reason):
        self._calls.append(("cleanup", reason))
        return '{"ok":true}'


class FakeScript:
    def __init__(self, calls):
        self.exports_sync = FakeCleanupExports(calls)
        self._calls = calls

    def unload(self):
        self._calls.append(("unload", None))


class FakeSession:
    def __init__(self, calls):
        self._calls = calls

    def detach(self):
        self._calls.append(("detach", None))


class FailingUniversalManager:
    def unload(self):
        raise RuntimeError("dll unload failed")


class FakeFridaDisconnect:
    def __init__(self):
        self.disconnected = False

    def disconnect(self):
        self.disconnected = True


class FridaCleanupTests(unittest.TestCase):
    def test_disconnect_calls_js_cleanup_before_unload_and_detach(self):
        calls = []
        manager = FridaManager()
        manager._script = FakeScript(calls)
        manager._session = FakeSession(calls)
        manager._ready = True
        manager._pid = 1234

        manager.disconnect()

        self.assertEqual(calls, [
            ("cleanup", "python_disconnect"),
            ("unload", None),
            ("detach", None),
        ])
        self.assertFalse(manager._ready)
        self.assertIsNone(manager._pid)
        self.assertIsNone(manager._script)
        self.assertIsNone(manager._session)

    def test_built_js_exposes_cleanup_helpers_and_rpc_cleanup(self):
        manager = FridaManager()

        js_code = manager._build_js_code()

        self.assertIn("function registerCleanup", js_code)
        self.assertIn("function cleanupAll", js_code)
        self.assertIn("cleanup: function(reason)", js_code)

    def test_session_stop_still_disconnects_frida_when_universal_unload_fails(self):
        manager = GameSessionManager()
        frida = FakeFridaDisconnect()
        manager._universal_manager = FailingUniversalManager()
        manager._frida_manager = frida

        manager.stop()

        self.assertTrue(frida.disconnected)
        self.assertIsNone(manager._universal_manager)
        self.assertIsNone(manager._frida_manager)


if __name__ == "__main__":
    unittest.main()
