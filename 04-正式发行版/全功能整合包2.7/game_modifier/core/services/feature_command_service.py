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

    # 方框透视实时下发到 DLL 的四个选项键
    ESP_OPTION_KEYS = (
        "esp_target_scope",
        "esp_health_mode",
        "esp_health_display",
        "esp_box_outline",
    )

    def set_config(self, feature_id, config):
        current = self._config.set(feature_id, config)
        if feature_id == "esp_box":
            current = self._apply_esp_options(current, set(config or {}))
        return self._frida.plugin_call(feature_id, "setConfig", current)

    def _apply_esp_options(self, current, changed_keys):
        """下发方框透视选项到已注入的 DLL，并保证「UI 所选 = 游戏生效」。

        下发路径：显示对象 → 血量显示 → 方框轮廓。每一项都经
        GameSessionManager（它会先按持久化配置校准，再用完整选项下发）。

        若 DLL 明确拒绝了本次改动（只有真正连上 DLL 时才会判定，未连接时只落盘、
        保留用户选择），就把用户刚改的键回退成 DLL 当前生效值：这样界面（读取配置
        渲染）与游戏效果始终一致，而不是界面显示 A、游戏里还是 B。
        """
        from core.game_session_manager import GameSessionManager

        session = GameSessionManager.get_instance()
        if "esp_target_scope" in current:
            session.set_esp_target_scope(current["esp_target_scope"])
        if "esp_health_mode" in current or "esp_health_display" in current:
            session.set_esp_health_options(
                current.get("esp_health_mode"),
                current.get("esp_health_display"),
            )
        if "esp_box_outline" in current:
            session.set_esp_box_outline(current["esp_box_outline"])

        applied = session.get_applied_esp_options()
        if not applied:
            return current

        revert = {
            key: applied[key]
            for key in self.ESP_OPTION_KEYS
            if key in changed_keys and key in applied and current.get(key) != applied[key]
        }
        if not revert:
            return current

        try:
            from core.log_manager import get_logger

            get_logger("ESPConfig").warning(
                "方框透视选项未生效，已回退为游戏当前值: %s", revert
            )
        except Exception:
            pass
        return self._config.set(feature_id="esp_box", config=revert)

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
