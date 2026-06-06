import os
import sys
import unittest
from unittest.mock import patch


GAME_MODIFIER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if GAME_MODIFIER_DIR not in sys.path:
    sys.path.insert(0, GAME_MODIFIER_DIR)

from core.game_session_manager import GameSessionManager, SessionState


class FakeEventBus:
    def __init__(self):
        self.events = []

    def emit(self, event_type, **kwargs):
        self.events.append((event_type, kwargs))


class FakeFridaManager:
    def __init__(self, result=(True, "success")):
        self.result = result
        self.pid = None

    def connect(self, pid):
        self.pid = pid
        return self.result

    def is_ready(self):
        return self.result[0]

    def disconnect(self):
        self.pid = None


class FakeUniversalManager:
    def __init__(self, connect_result=False, inject_result=False):
        self.connect_result = connect_result
        self.inject_result = inject_result
        self.set_calls = []
        self.disconnected = False
        self.unloaded = False
        self.inject_calls = []

    def try_connect_existing(self, pid):
        return self.connect_result

    def inject_and_connect(self, pid):
        self.inject_calls.append(pid)
        return self.inject_result

    def set_esp_box(self, enabled):
        self.set_calls.append(enabled)
        return True

    def disconnect(self):
        self.disconnected = True

    def unload(self):
        self.unloaded = True
        return True


class GameSessionManagerTests(unittest.TestCase):
    def setUp(self):
        self.manager = GameSessionManager()
        self.manager._bus = FakeEventBus()
        self.manager._save_desired_states = lambda: None
        self.manager._pid = 1234
        self.manager._pid_create_time = 10.0

    def test_frida_success_emits_connected_status_for_ui(self):
        fake_frida = FakeFridaManager()

        with patch(
            "core.frida_manager.FridaManager.get_instance",
            return_value=fake_frida,
        ):
            self.manager._step_connecting_frida()

        self.assertEqual(
            self.manager.get_state(),
            SessionState.READY,
        )
        self.assertIn(
            ("connection_status", {"status": "connected", "pid": 1234}),
            self.manager._bus.events,
        )

    def test_stable_game_connects_universal_before_frida(self):
        self.manager._state = SessionState.WAITING_GAME_READY
        self.manager._stability_wait = 0

        with patch.object(
            self.manager,
            "_find_game_process",
            return_value=(1234, 10.0),
        ), patch.object(
            self.manager,
            "_is_process_stable",
            return_value=True,
        ):
            self.manager._step_waiting_game_ready()

        self.assertEqual(
            self.manager.get_state(),
            SessionState.CONNECTING_EXISTING_DLL,
        )

    def test_universal_failure_continues_to_frida_connection(self):
        self.manager._state = SessionState.INJECTING_DLL
        fake_universal = FakeUniversalManager(inject_result=False)

        with patch(
            "core.universal_hook_manager.UniversalHookManager.get_instance",
            return_value=fake_universal,
        ):
            self.manager._step_injecting_dll()

        self.assertEqual(self.manager.get_state(), SessionState.CONNECTING_FRIDA)
        self.assertIn(
            ("universal_status", {"status": "unavailable", "pid": 1234}),
            self.manager._bus.events,
        )

    def test_same_game_process_is_only_injected_once(self):
        self.manager._state = SessionState.INJECTING_DLL
        fake_universal = FakeUniversalManager(inject_result=False)

        with patch(
            "core.universal_hook_manager.UniversalHookManager.get_instance",
            return_value=fake_universal,
        ):
            self.manager._step_injecting_dll()
            self.manager._state = SessionState.INJECTING_DLL
            self.manager._step_injecting_dll()

        self.assertEqual(fake_universal.inject_calls, [1234])

    def test_esp_toggle_applies_immediately_without_injection(self):
        fake_universal = FakeUniversalManager()
        self.manager._universal_manager = fake_universal

        self.manager.set_desired_state("esp_box", True)
        self.manager.set_desired_state("esp_box", False)

        self.assertEqual(fake_universal.set_calls, [True, False])
        self.assertEqual(self.manager.get_applied_state("esp_box"), False)

    def test_stop_unloads_dll(self):
        fake_universal = FakeUniversalManager()
        self.manager._universal_manager = fake_universal

        self.manager.stop()

        self.assertTrue(fake_universal.unloaded)
        self.assertFalse(fake_universal.disconnected)


if __name__ == "__main__":
    unittest.main()
