from ui.views.common import bind_view_handles


class PanelContext:
    """Safe capability object passed to plugin panels and event handlers."""

    def __init__(self, app):
        self.event_bus = app._event_bus
        self.feature_service = app._feature_service
        self.config_manager = app._config_manager
        self.callbacks = {
            "toggle": app._feature_controller.toggle_feature,
            "set_config": app._feature_controller.set_feature_config,
            "action": app._feature_controller.trigger_feature_action,
        }
        self._log = app._log
        self._after = getattr(app, "_safe_after", app.after)
        self._bind_target = app
        self._is_connected = lambda: bool(app._ready)
        self._is_enabled = lambda feature_id: bool(app._features.get(feature_id, False))

    def for_feature(self, feature_id):
        return FeaturePanelContext(self, feature_id)

    def log(self, message):
        self._log(message)

    def after(self, delay_ms, callback):
        return self._after(delay_ms, callback)

    def bind_handles(self, handles):
        bind_view_handles(self._bind_target, handles)

    def get_config(self, feature_id):
        return self.config_manager.get(feature_id)

    def set_config(self, feature_id, config):
        return self.config_manager.set(feature_id, config)

    def is_connected(self):
        return self._is_connected()

    def is_enabled(self, feature_id):
        return self._is_enabled(feature_id)

    def emit(self, event_name, **payload):
        self.event_bus.emit(event_name, **payload)

    def feature_event(self, feature_id, event_name, payload=None):
        self.emit(
            "plugin_event",
            feature=feature_id,
            event=event_name,
            payload=payload or {},
        )


class FeaturePanelContext:
    """Feature-scoped safe context passed to a plugin panel or event handler."""

    def __init__(self, safe_context, feature_id):
        self._safe_context = safe_context
        self.feature_id = feature_id
        self.event_bus = safe_context.event_bus
        self.feature_service = safe_context.feature_service
        self.config_manager = safe_context.config_manager
        self.callbacks = safe_context.callbacks

    def log(self, message):
        return self._safe_context.log(message)

    def after(self, delay_ms, callback):
        return self._safe_context.after(delay_ms, callback)

    def bind_handles(self, handles):
        return self._safe_context.bind_handles(handles)

    def get_config(self, feature_id=None):
        return self._safe_context.get_config(feature_id or self.feature_id)

    def set_config(self, config, feature_id=None):
        return self._safe_context.set_config(feature_id or self.feature_id, config)

    def is_connected(self):
        return self._safe_context.is_connected()

    def is_enabled(self, feature_id=None):
        return self._safe_context.is_enabled(feature_id or self.feature_id)

    def after(self, delay_ms, callback):
        return self._safe_context.after(delay_ms, callback)

    def emit(self, event_name, **payload):
        return self._safe_context.emit(event_name, **payload)

    def feature_event(self, event_name, payload=None, feature_id=None):
        return self._safe_context.feature_event(
            feature_id or self.feature_id,
            event_name,
            payload or {},
        )
