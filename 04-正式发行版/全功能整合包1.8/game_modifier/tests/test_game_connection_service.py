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


class FakeSessionManager:
    def __init__(self):
        self.calls = []

    def reconnect(self):
        self.calls.append(("reconnect", ()))

    def disconnect(self):
        self.calls.append(("disconnect", ()))


class GameConnectionServiceTests(unittest.TestCase):
    def test_connection_service_requests_session_lifecycle(self):
        frida = FakeFrida()
        session = FakeSessionManager()
        service = GameConnectionService(frida, session)

        self.assertFalse(service.is_connected)
        self.assertEqual(service.find_pid(), 42)
        self.assertEqual(service.connect(42), (True, "requested"))

        service.disconnect()

        self.assertFalse(service.is_connected)
        self.assertIsNone(service.pid)
        self.assertEqual(frida.calls, [("find_pid", ())])
        self.assertEqual(session.calls, [("reconnect", ()), ("disconnect", ())])


if __name__ == "__main__":
    unittest.main()
