from core.config_runtime.config_manager import ConfigManager


class FeatureCommandService:
    def __init__(self, frida_manager, config_manager=None):
        self._frida = frida_manager
        self._config = config_manager or ConfigManager()

    def enable(self, feature_id):
        config = self._config.remove_user_key(feature_id, "enabled")
        return self._frida.plugin_call(feature_id, "enable", config)

    def disable(self, feature_id):
        self._config.remove_user_key(feature_id, "enabled")
        return self._frida.plugin_call(feature_id, "disable")

    def set_config(self, feature_id, config):
        current = self._config.set(feature_id, config)
        if feature_id == "esp_box":
            # 方框透视的所有选项都要实时下发到已注入的 DLL：
            # esp_target_scope（显示对象）、esp_health_mode（百分比/剩余数值）、
            # esp_health_display（仅血条/仅数值/两者）、esp_box_outline（方框轮廓开关）。
            if "esp_target_scope" in current:
                from core.game_session_manager import GameSessionManager
                GameSessionManager.get_instance().set_esp_target_scope(current["esp_target_scope"])
            if "esp_health_mode" in current or "esp_health_display" in current:
                from core.game_session_manager import GameSessionManager
                GameSessionManager.get_instance().set_esp_health_options(
                    current.get("esp_health_mode"),
                    current.get("esp_health_display"),
                )
            if "esp_box_outline" in current:
                from core.game_session_manager import GameSessionManager
                GameSessionManager.get_instance().set_esp_box_outline(
                    current["esp_box_outline"]
                )
        return self._frida.plugin_call(feature_id, "setConfig", current)

    def set_config_runtime(self, feature_id, config):
        current = self._config.get(feature_id)
        current.update(config or {})
        return self._frida.plugin_call(feature_id, "setConfig", current)

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
