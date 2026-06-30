from core.config_runtime.config_manager import ConfigManager


class FeatureCommandService:
    def __init__(self, frida_manager, config_manager=None):
        self._frida = frida_manager
        self._config = config_manager or ConfigManager()

    def enable(self, feature_id):
        config = self._config.set(feature_id, {"enabled": True})
        return self._frida.plugin_call(feature_id, "enable", config)

    def disable(self, feature_id):
        self._config.set(feature_id, {"enabled": False})
        return self._frida.plugin_call(feature_id, "disable")

    def set_config(self, feature_id, config):
        current = self._config.set(feature_id, config)
        if current.get("enabled"):
            return self._frida.plugin_call(feature_id, "setConfig", current)
        return current

    def status(self, feature_id):
        return self._frida.plugin_call(feature_id, "status")

    def call_action(self, feature_id, action, payload=None):
        return self._frida.plugin_call(feature_id, action, payload or {})

    def cleanup(self, feature_id):
        return self._frida.plugin_call(feature_id, "cleanup", {"reason": "feature_cleanup"})

    def cleanup_all(self, reason="feature_cleanup_all"):
        return self._frida.plugin_cleanup_all(reason)

    def toggle_feature(self, feature_id, enabled, **_ignored):
        return self.enable(feature_id) if enabled else self.disable(feature_id)

    def restore_feature(self, feature_id, **_ignored):
        return self.enable(feature_id)
