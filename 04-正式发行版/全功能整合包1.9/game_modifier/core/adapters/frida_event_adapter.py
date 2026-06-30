"""DEPRECATED / LEGACY ONLY.

New plugin messages must use FridaManager -> plugin_event -> PluginEventRouter.
Do not add feature branches or new runtime wiring here.
"""


class FridaEventAdapter:
    def __init__(self, event_bus, callbacks):
        self._event_bus = event_bus
        self._callbacks = callbacks
        self._subscriptions = (
            ("log_message", self._on_log_message),
            ("connection_status", self._on_connection_status),
            ("feature_status_changed", self._on_feature_status),
            ("gather_result", self._on_gather_result),
            ("round_skipped", self._on_round_skipped),
            ("nano4t_event", self._on_nano4t_event),
            ("battle_round_event", self._on_battle_round_event),
            ("isbot_event", self._on_isbot_event),
        )

    def subscribe(self):
        for event_type, handler in self._subscriptions:
            self._event_bus.subscribe(event_type, handler)

    def unsubscribe(self):
        for event_type, handler in self._subscriptions:
            self._event_bus.unsubscribe(event_type, handler)

    def _on_log_message(self, **kwargs):
        self._callbacks.handle_log_message(
            level=kwargs.get("level", "info"),
            module=kwargs.get("module", ""),
            message=kwargs.get("message", ""),
            audience=kwargs.get("audience", "user"),
            dev_detail=kwargs.get("dev_detail", ""),
        )

    def _on_connection_status(self, **kwargs):
        self._callbacks.handle_connection_status(
            status=kwargs.get("status", "disconnected"),
            pid=kwargs.get("pid"),
        )

    def _on_feature_status(self, **kwargs):
        self._callbacks.handle_feature_status(
            feature_id=kwargs.get("feature", ""),
            enabled=kwargs.get("enabled", False),
        )

    def _on_gather_result(self, **kwargs):
        self._callbacks.handle_gather_result(data=kwargs.get("data", {}))

    def _on_round_skipped(self, **kwargs):
        self._callbacks.handle_round_skipped(count=kwargs.get("count", 0))

    def _on_nano4t_event(self, **kwargs):
        self._callbacks.handle_nano4t_event(
            event_type=kwargs.get("msg_type", ""),
            payload=kwargs.get("payload", {}),
        )

    def _on_battle_round_event(self, **kwargs):
        self._callbacks.handle_battle_round_event(
            event_type=kwargs.get("msg_type", ""),
            payload=kwargs.get("payload", {}),
        )

    def _on_isbot_event(self, **kwargs):
        self._callbacks.handle_isbot_event(
            state=kwargs.get("state", "off"),
            payload=kwargs.get("payload", {}),
        )
