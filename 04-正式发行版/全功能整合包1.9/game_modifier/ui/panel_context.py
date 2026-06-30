from ui.views.common import bind_view_handles


class PanelContext:
    """Small capability object passed to plugin panels and event handlers."""

    def __init__(self, app):
        self._app = app
        self.event_bus = app._event_bus
        self.feature_service = app._feature_service
        self.config_manager = app._config_manager
        self.callbacks = {
            "toggle": app._feature_controller.toggle_feature,
            "set_config": app._feature_controller.set_feature_config,
            "action": app._feature_controller.trigger_feature_action,
        }

    def log(self, message):
        self._app._log(message)

    def after(self, delay_ms, callback):
        return self._app.after(delay_ms, callback)

    def bind_handles(self, handles):
        bind_view_handles(self._app, handles)

    def get_state(self, key, default=None):
        return getattr(self._app, f"_{key}", default)

    def set_state(self, key, value):
        setattr(self._app, f"_{key}", value)

    def get_handle(self, name, default=None):
        return getattr(self._app, name, default)

    def set_handle(self, name, value):
        setattr(self._app, name, value)

    def controller(self, name):
        return getattr(self._app, f"_{name}_controller")

    def service(self, name):
        return getattr(self._app, f"_{name}_service")

    def is_connected(self):
        return bool(self._app._ready)

    def is_enabled(self, feature_id):
        return bool(self._app._features.get(feature_id, False))

    @property
    def weapon_top_frames(self):
        return self._app._weapon_top_frames

    @property
    def weapon_hotkey_badges(self):
        return self._app._weapon_hotkey_badges

    @property
    def weapon_controller(self):
        return self._app._weapon_controller
