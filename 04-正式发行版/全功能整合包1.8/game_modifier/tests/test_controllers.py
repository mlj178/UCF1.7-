import tempfile
import unittest
from pathlib import Path

from core.config import NANO4T_ATTRS
from core.services.feature_command_service import FeatureCommandService
from core.repositories.nano4t_config_repository import Nano4tConfigRepository
from ui.controllers.app_event_controller import AppEventController
from ui.controllers.feature_action_controller import FeatureActionController
from ui.controllers.nano4t_runtime_controller import Nano4tRuntimeController
from ui.controllers.nano4t_selection_controller import Nano4tSelectionController
from ui.controllers.weapon_interaction_controller import WeaponInteractionController


class FakeBus:
    def __init__(self):
        self.subscriptions = []

    def subscribe(self, event_name, callback):
        self.subscriptions.append((event_name, callback.__name__))


class FakeApp:
    def __init__(self):
        self._ui_ready = True
        self._early_log_messages = []
        self._stop = False
        self._features = {"isbot": True}
        self.isbot_states = []
        self.updated_switches = []
        self.logs = []

    def after(self, _delay, callback):
        callback()

    def _log(self, message):
        self.logs.append(message)

    def _set_isbot_state(self, state):
        self.isbot_states.append(state)

    def _update_switch(self, feature_id):
        self.updated_switches.append(feature_id)


class FakeFrida:
    def __init__(self):
        self.sent = []

    def send_toggle(self, feature_id, enabled, extra_params=None):
        self.sent.append((feature_id, enabled, extra_params))


class FakeSound:
    def __init__(self):
        self.toggle_count = 0

    def play_toggle_sound(self):
        self.toggle_count += 1


class FakeFeatureApp:
    def __init__(self):
        self._ready = True
        self._features = {"knife": False, "gravity": False}
        self._knife_speed = 5.0
        self._movespeed = 3.0
        self._range_mult = 50.0
        self._gravity = 1.0
        self._jump = 1.0
        self._gravity_mode = "player_only"
        self._timescale = 1.0
        self._frida = FakeFrida()
        self._feature_service = FeatureCommandService(self._frida)
        self._sound = FakeSound()
        self.updated_switches = []
        self.saved = False
        self.logs = []

    def _log(self, message):
        self.logs.append(message)

    def _update_switch(self, feature_id):
        self.updated_switches.append(feature_id)

    def _schedule_save_state(self):
        self.saved = True

    def after(self, _delay, callback):
        callback()
        return "timer"

    def after_cancel(self, _timer):
        pass


class FakeLabel:
    def __init__(self):
        self.configures = []

    def configure(self, **kwargs):
        self.configures.append(kwargs)


class FakeRoundSkipMonitor:
    def __init__(self):
        self.start_count = 0
        self.stop_count = 0

    def start(self):
        self.start_count += 1

    def stop(self):
        self.stop_count += 1


class FakeConnectionFeatureController:
    def __init__(self):
        self.restore_count = 0

    def restore_features(self):
        self.restore_count += 1


class FakeConnectionWeaponController:
    def __init__(self):
        self.init_count = 0
        self.pause_count = 0

    def init_hotkey_manager(self):
        self.init_count += 1

    def pause_hotkeys(self):
        self.pause_count += 1


class FakeBattleRoundController:
    def __init__(self):
        self.sync_count = 0
        self.disconnect_count = 0

    def sync_to_game_on_connect(self):
        self.sync_count += 1

    def on_disconnected(self):
        self.disconnect_count += 1


class FakeNano4tRuntimeController:
    def __init__(self):
        self.auto_init_count = 0

    def auto_init_async(self):
        self.auto_init_count += 1


class FakeConnectionFrida:
    def __init__(self):
        self.sent = []

    def send_toggle(self, feature_id, enabled, extra_params=None):
        self.sent.append((feature_id, enabled, extra_params))


class FakeConnectionApp:
    def __init__(self):
        self._ui_ready = True
        self._early_log_messages = []
        self._features = {"isbot": False}
        self._battle_round_enabled = False
        self._battle_round_active = False
        self._battle_mode_active = False
        self._ready = False
        self._pid = None
        self.pid_label = FakeLabel()
        self.status_updates = []
        self.isbot_states = []
        self.battle_button_updates = 0
        self._frida = FakeConnectionFrida()
        self._feature_controller = FakeConnectionFeatureController()
        self._weapon_controller = FakeConnectionWeaponController()
        self._roundskip_monitor = FakeRoundSkipMonitor()
        self._battle_round_controller = FakeBattleRoundController()
        self._nano4t_runtime_controller = FakeNano4tRuntimeController()

    def after(self, _delay, callback):
        callback()

    def _set_status(self, color, text):
        self.status_updates.append((color, text))

    def _set_isbot_state(self, state):
        self.isbot_states.append(state)

class ControllerTests(unittest.TestCase):
    def test_event_controller_registers_expected_events(self):
        bus = FakeBus()
        controller = AppEventController(FakeApp())

        controller.register(bus)

        event_names = [event_name for event_name, _ in bus.subscriptions]
        self.assertIn("connection_status", event_names)
        self.assertIn("nano4t_event", event_names)
        self.assertIn("battle_round_event", event_names)

    def test_event_controller_updates_feature_status(self):
        app = FakeApp()
        controller = AppEventController(app)

        controller.on_feature_status(feature="isbot", enabled=False)

        self.assertFalse(app._features["isbot"])
        self.assertEqual(app.isbot_states, ["off"])
        self.assertEqual(app.updated_switches, ["isbot"])

    def test_event_controller_ignores_feature_status_while_app_is_stopping(self):
        app = FakeApp()
        app._stop = True
        controller = AppEventController(app)

        controller.on_feature_status(feature="isbot", enabled=False)

        self.assertTrue(app._features["isbot"])
        self.assertEqual(app.isbot_states, [])
        self.assertEqual(app.updated_switches, [])

    def test_event_controller_hides_dev_log_from_ui(self):
        app = FakeApp()
        controller = AppEventController(app, log_writer=lambda *_args: None)

        controller.on_log_message(
            level="info",
            module="回合跳过",
            message="新回合 #1",
            audience="dev",
            dev_detail="RoundSkip captured ModeBase instance",
        )

        self.assertEqual(app.logs, [])

    def test_event_controller_shows_user_log_in_ui(self):
        app = FakeApp()
        controller = AppEventController(app, log_writer=lambda *_args: None)

        controller.on_log_message(
            level="warn",
            module="回合跳过",
            message="回合暂未就绪，请稍后重试",
            audience="user",
        )

        self.assertEqual(app.logs, ["⚠️ [回合跳过] 回合暂未就绪，请稍后重试"])

    def test_event_controller_starts_roundskip_monitor_when_connected(self):
        app = FakeConnectionApp()
        controller = AppEventController(app)

        controller.on_connection_status(status="connected", pid=1234)

        self.assertEqual(app._roundskip_monitor.start_count, 1)
        self.assertTrue(app._ready)

    def test_event_controller_stops_roundskip_monitor_when_disconnected(self):
        app = FakeConnectionApp()
        app._ready = True
        controller = AppEventController(app)

        controller.on_connection_status(status="disconnected")

        self.assertEqual(app._roundskip_monitor.stop_count, 1)
        self.assertFalse(app._ready)

    def test_feature_action_controller_toggles_knife_with_speed_config(self):
        app = FakeFeatureApp()
        controller = FeatureActionController(app)

        controller.toggle_feature("knife")

        self.assertTrue(app._features["knife"])
        self.assertEqual(app._frida.sent, [("knife", True, None), ("knife_speed", 5.0, None)])
        self.assertEqual(app.updated_switches, ["knife"])
        self.assertTrue(app.saved)

    def test_nano4t_selection_controller_validates_and_persists_choices(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Nano4tConfigRepository(Path(tmp_dir) / "Nano-4T-selector.json")
            controller = Nano4tSelectionController(repo, NANO4T_ATTRS)

            ghost_result = controller.select_ghost("5: 钢铁利爪")
            human_result = controller.select_human("14: 无限弹药")

            self.assertTrue(ghost_result.ok)
            self.assertTrue(human_result.ok)
            self.assertEqual(repo.load(), {"ghost": 5, "human": 14})
            self.assertEqual(ghost_result.description, f"效果: {NANO4T_ATTRS[5][1]}")

    def test_nano4t_selection_controller_rejects_wrong_side_ids(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Nano4tConfigRepository(Path(tmp_dir) / "Nano-4T-selector.json")
            controller = Nano4tSelectionController(repo, NANO4T_ATTRS)

            result = controller.select_ghost("14: 无限弹药")

            self.assertFalse(result.ok)
            self.assertIn("幽灵方", result.error)

    def test_nano4t_runtime_status_dot_uses_visible_text_color(self):
        app = type("FakeNano4tApp", (), {})()
        app.nano4t_status_dot = FakeLabel()
        app.nano4t_status_label = FakeLabel()

        controller = Nano4tRuntimeController(app)
        controller.set_status("green", "已就绪")

        self.assertEqual(app.nano4t_status_dot.configures[-1]["text"], "●")
        self.assertEqual(app.nano4t_status_dot.configures[-1]["text_color"], "#2ecc71")
        self.assertEqual(app.nano4t_status_label.configures[-1]["text"], "已就绪")

    def test_weapon_interaction_controller_uses_catalog_fallback_copy(self):
        controller = WeaponInteractionController(app=None)

        self.assertEqual(controller.get_weapon_name_by_id("120"), "NANOKNIFE")
        self.assertEqual(controller.get_weapon_name_by_id("999999"), "武器999999")


if __name__ == "__main__":
    unittest.main()
