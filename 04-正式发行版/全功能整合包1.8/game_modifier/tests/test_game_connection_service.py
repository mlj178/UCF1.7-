import unittest

from core.services.game_connection_service import GameConnectionService


class FakeFrida:
    def __init__(self):
        self.is_connected = False
        self.pid = None
        self.calls = []

    def find_pid(self):
        self.calls.append(("find_pid", ()))
        return 42

    def connect(self, pid):
        self.calls.append(("connect", (pid,)))
        self.is_connected = True
        self.pid = pid
        return True, "success"

    def disconnect(self):
        self.calls.append(("disconnect", ()))
        self.is_connected = False
        self.pid = None


class GameConnectionServiceTests(unittest.TestCase):
    def test_connection_service_wraps_frida_connection_lifecycle(self):
        frida = FakeFrida()
        service = GameConnectionService(frida)

        self.assertFalse(service.is_connected)
        self.assertEqual(service.find_pid(), 42)
        self.assertEqual(service.connect(42), (True, "success"))
        self.assertTrue(service.is_connected)
        self.assertEqual(service.pid, 42)

        service.disconnect()

        self.assertFalse(service.is_connected)
        self.assertIsNone(service.pid)
        self.assertEqual(
            frida.calls,
            [
                ("find_pid", ()),
                ("connect", (42,)),
                ("disconnect", ()),
            ],
        )


if __name__ == "__main__":
    unittest.main()
