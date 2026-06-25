import unittest

from core.services.game_action_service import GameActionService


class FakeFrida:
    def __init__(self, connected=True):
        self.is_connected = connected
        self.export_calls = []
        self.toggle_calls = []

    def call_export(self, name, *args):
        self.export_calls.append((name, args))
        return {"ok": True}

    def send_toggle(self, feature, enable, extra_params=None):
        self.toggle_calls.append((feature, enable, extra_params))


class GameActionServiceTests(unittest.TestCase):
    def test_exports_common_game_actions(self):
        frida = FakeFrida()
        service = GameActionService(frida)

        service.gather()
        service.skip_round()
        service.nano4t_init()
        service.nano4t_set(1, 12)
        service.nano4t_get_current()

        self.assertEqual(
            frida.export_calls,
            [
                ("gather", ()),
                ("roundskip", ()),
                ("nano4tinit", ()),
                ("nano4tset", (1, 12)),
                ("nano4tgetcurrent", ()),
            ],
        )

    def test_battle_round_and_guarded_nano4t_init_use_frida_state(self):
        frida = FakeFrida(connected=True)
        service = GameActionService(frida)

        service.set_battle_round_enabled(True)
        self.assertTrue(service.nano4t_init_if_connected(ready=False))
        self.assertFalse(service.nano4t_init_if_connected(ready=True))

        self.assertEqual(frida.toggle_calls, [("battle_round_always", True, None)])
        self.assertEqual(frida.export_calls, [("nano4tinit", ())])

    def test_guarded_calls_do_not_export_when_disconnected_or_ready(self):
        frida = FakeFrida(connected=False)
        service = GameActionService(frida)

        self.assertFalse(service.nano4t_init_if_connected(ready=False))
        self.assertFalse(service.nano4t_get_current_if_ready(ready=True))

        self.assertEqual(frida.export_calls, [])


if __name__ == "__main__":
    unittest.main()
