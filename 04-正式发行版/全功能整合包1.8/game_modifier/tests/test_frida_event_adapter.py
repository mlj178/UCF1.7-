import unittest

from core.adapters.frida_event_adapter import FridaEventAdapter


class FakeEventBus:
    def __init__(self):
        self.subscribed = []
        self.unsubscribed = []

    def subscribe(self, event_type, callback):
        self.subscribed.append((event_type, callback))

    def unsubscribe(self, event_type, callback):
        self.unsubscribed.append((event_type, callback))


class FakeCallbacks:
    def __init__(self):
        self.calls = []

    def handle_log_message(self, **kwargs):
        self.calls.append(("log", kwargs))

    def handle_connection_status(self, **kwargs):
        self.calls.append(("connection", kwargs))

    def handle_feature_status(self, **kwargs):
        self.calls.append(("feature", kwargs))

    def handle_gather_result(self, **kwargs):
        self.calls.append(("gather", kwargs))

    def handle_round_skipped(self, **kwargs):
        self.calls.append(("round", kwargs))

    def handle_nano4t_event(self, **kwargs):
        self.calls.append(("nano4t", kwargs))

    def handle_battle_round_event(self, **kwargs):
        self.calls.append(("battle", kwargs))

    def handle_isbot_event(self, **kwargs):
        self.calls.append(("isbot", kwargs))


class FridaEventAdapterTests(unittest.TestCase):
    def test_adapter_subscribes_all_expected_events(self):
        bus = FakeEventBus()
        callbacks = FakeCallbacks()

        adapter = FridaEventAdapter(bus, callbacks)
        adapter.subscribe()
        adapter.unsubscribe()

        self.assertEqual(len(bus.subscribed), 8)
        self.assertEqual(len(bus.unsubscribed), 8)
        self.assertEqual(
            [event for event, _ in bus.subscribed],
            [
                "log_message",
                "connection_status",
                "feature_status_changed",
                "gather_result",
                "round_skipped",
                "nano4t_event",
                "battle_round_event",
                "isbot_event",
            ],
        )

    def test_adapter_normalizes_payloads_for_callbacks(self):
        bus = FakeEventBus()
        callbacks = FakeCallbacks()
        adapter = FridaEventAdapter(bus, callbacks)

        adapter._on_log_message(level="success", module="system", message="ok", audience="dev", dev_detail="detail")
        adapter._on_connection_status(status="connected", pid=123)
        adapter._on_feature_status(feature="knife", enabled=True)
        adapter._on_gather_result(data={"ok": True})
        adapter._on_round_skipped(count=3)
        adapter._on_nano4t_event(msg_type="nano4t_ready", payload={"ids": [1, 2]})
        adapter._on_battle_round_event(msg_type="battle_round_round", payload={"enabled": True})
        adapter._on_isbot_event(state="active", payload={"state": "active"})

        self.assertEqual(
            callbacks.calls,
            [
                ("log", {"level": "success", "module": "system", "message": "ok", "audience": "dev", "dev_detail": "detail"}),
                ("connection", {"status": "connected", "pid": 123}),
                ("feature", {"feature_id": "knife", "enabled": True}),
                ("gather", {"data": {"ok": True}}),
                ("round", {"count": 3}),
                ("nano4t", {"event_type": "nano4t_ready", "payload": {"ids": [1, 2]}}),
                ("battle", {"event_type": "battle_round_round", "payload": {"enabled": True}}),
                ("isbot", {"state": "active", "payload": {"state": "active"}}),
            ],
        )


if __name__ == "__main__":
    unittest.main()
