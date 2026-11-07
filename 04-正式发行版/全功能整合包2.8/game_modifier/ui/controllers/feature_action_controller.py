from ui.controllers.action_router import ActionRouter


class FeatureActionController:
    def __init__(self, app):
        self._app = app
        self._router = None

    def _get_router(self):
        if self._router is None:
            app = self._app
            self._router = ActionRouter(
                registry=app._plugin_registry,
                feature_service=app._feature_service,
                config_manager=app._config_manager,
                state=app._features,
                is_connected=lambda: app._ready,
                logger=app._log,
                update_switch=app._update_switch,
                sync_config=app._on_plugin_config_changed,
                schedule_save=app._schedule_save_state,
                play_toggle_sound=app._sound.play_toggle_sound,
                run_in_background=app._run_in_background,
                schedule_ui=app._safe_after,
            )
        return self._router

    def toggle_feature(self, feature_id):
        return self._get_router().toggle(feature_id)

    def set_feature_config(self, feature_id, key, value):
        return self._get_router().set_config(feature_id, key, value)

    def trigger_feature_action(self, feature_id, action, payload=None):
        return self._get_router().action(feature_id, action, payload)

    def restore_features(self):
        return self._get_router().restore_enabled()
