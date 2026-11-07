import queue
import threading
import unittest
from unittest import mock


try:
    from core.native_hotkey_listener import (
        MOD_NOREPEAT,
        VK_BY_POSITION,
        WM_HOTKEY,
        NativeHotkeyListener,
    )
except ImportError:
    MOD_NOREPEAT = None
    VK_BY_POSITION = None
    WM_HOTKEY = None
    NativeHotkeyListener = None


class FakeWin32Api:
    def __init__(self, failures=()):
        self.failures = set(failures)
        self.messages = queue.Queue()
        self.register_calls = []
        self.unregister_calls = []
        self.post_quit_calls = []
        self.queue_ready = False

    def current_thread_id(self):
        return threading.get_ident()

    def ensure_message_queue(self):
        self.queue_ready = True

    def register_hotkey(self, hotkey_id, modifiers, virtual_key):
        self.register_calls.append((hotkey_id, modifiers, virtual_key))
        return hotkey_id not in self.failures

    def unregister_hotkey(self, hotkey_id):
        self.unregister_calls.append(hotkey_id)
        return True

    def next_message(self):
        return self.messages.get(timeout=1)

    def post_quit(self, thread_id):
        self.post_quit_calls.append(thread_id)
        self.messages.put(None)
        return True

    def last_error(self):
        return 1409


class FakeNativeListener:
    def __init__(self):
        self.errors = {"f2": 1409}
        self.callback = None
        self.stop_count = 0

    def start(self, positions, callback):
        self.callback = callback
        self.positions = tuple(positions)
        return {"f1": True, "f2": False}

    def stop(self):
        self.stop_count += 1


class ImmediateApp:
    @staticmethod
    def after(_delay, callback):
        callback()


class NativeHotkeyListenerTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(NativeHotkeyListener, "NativeHotkeyListener has not been implemented")

    def test_registers_f1_f2_with_no_repeat_and_dispatches_messages(self):
        api = FakeWin32Api()
        received = []
        listener = NativeHotkeyListener(api=api)

        result = listener.start(("f1", "f2"), received.append)
        self.assertEqual(result, {"f1": True, "f2": True})
        self.assertTrue(api.queue_ready)
        self.assertEqual(
            api.register_calls,
            [
                (1, MOD_NOREPEAT, VK_BY_POSITION["f1"]),
                (2, MOD_NOREPEAT, VK_BY_POSITION["f2"]),
            ],
        )

        api.messages.put((WM_HOTKEY, 1))
        api.messages.put((WM_HOTKEY, 2))
        for _ in range(50):
            if received == ["f1", "f2"]:
                break
            threading.Event().wait(0.01)
        self.assertEqual(received, ["f1", "f2"])

        listener.stop()
        self.assertEqual(api.unregister_calls, [1, 2])
        self.assertEqual(len(api.post_quit_calls), 1)

    def test_reports_partial_registration_failure_for_fallback(self):
        api = FakeWin32Api(failures={2})
        listener = NativeHotkeyListener(api=api)

        result = listener.start(("f1", "f2"), lambda position: None)

        self.assertEqual(result, {"f1": True, "f2": False})
        self.assertEqual(listener.errors, {"f2": 1409})
        listener.stop()
        self.assertEqual(api.unregister_calls, [1])


class HotkeyManagerNativeIntegrationTests(unittest.TestCase):
    def test_native_success_skips_keyboard_and_failure_falls_back(self):
        from core.hotkey_manager import HotkeyManager

        native = FakeNativeListener()
        received = []
        with mock.patch("core.hotkey_manager.keyboard.add_hotkey", return_value=mock.Mock()) as add_hotkey:
            manager = HotkeyManager()
            manager._native_hotkey_listener = native
            manager.set_app(ImmediateApp())
            manager.setup_hotkeys(received.append, silent=True)

        registered_with_keyboard = [call.args[0] for call in add_hotkey.call_args_list]
        self.assertIsNotNone(native.callback, "HotkeyManager did not start the native listener")
        self.assertEqual(native.positions, ("f1", "f2"))
        self.assertNotIn("f1", registered_with_keyboard)
        self.assertIn("f2", registered_with_keyboard)

        native.callback("f1")
        self.assertEqual(received[-1]["action"], "savepoint2")
        manager.cleanup()
        self.assertGreaterEqual(native.stop_count, 2)


if __name__ == "__main__":
    unittest.main()
