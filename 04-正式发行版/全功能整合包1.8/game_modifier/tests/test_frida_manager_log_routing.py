import unittest

from core.frida_manager import FridaManager


class FakeEventBus:
    def __init__(self):
        self.events = []

    def emit(self, event_name, **kwargs):
        self.events.append((event_name, kwargs))


class FridaManagerLogRoutingTests(unittest.TestCase):
    def test_js_log_without_audience_defaults_to_dev(self):
        manager = FridaManager()
        manager._event_bus = FakeEventBus()

        manager._on_message({
            "type": "send",
            "payload": {
                "type": "log",
                "level": "info",
                "module": "回合跳过",
                "message": "新回合 #1",
            },
        }, None)

        self.assertEqual(manager._event_bus.events, [(
            "log_message",
            {
                "level": "info",
                "module": "回合跳过",
                "message": "新回合 #1",
                "audience": "dev",
                "dev_detail": "",
            },
        )])

    def test_js_user_log_keeps_user_audience(self):
        manager = FridaManager()
        manager._event_bus = FakeEventBus()

        manager._on_message({
            "type": "send",
            "payload": {
                "type": "log",
                "level": "warn",
                "module": "回合跳过",
                "message": "回合暂未就绪，请稍后重试",
                "audience": "user",
            },
        }, None)

        self.assertEqual(manager._event_bus.events[0][1]["audience"], "user")


if __name__ == "__main__":
    unittest.main()
