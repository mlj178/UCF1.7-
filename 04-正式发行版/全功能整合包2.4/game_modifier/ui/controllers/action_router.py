class ActionRouter:
    """Route feature UI actions from manifest metadata."""

    STANDARD_ACTIONS = {"enable", "disable", "cleanup"}

    def __init__(
        self,
        *,
        registry,
        feature_service,
        config_manager,
        state,
        is_connected,
        logger,
        update_switch,
        sync_config,
        schedule_save,
        play_toggle_sound=None,
    ):
        self._registry = registry
        self._feature_service = feature_service
        self._config = config_manager
        self._state = state
        self._is_connected = is_connected
        self._log = logger
        self._update_switch = update_switch
        self._sync_config = sync_config
        self._schedule_save = schedule_save
        self._play_toggle_sound = play_toggle_sound or (lambda: None)

    def toggle(self, feature_id):
        enabled = not bool(self._state.get(feature_id, False))
        action = "enable" if enabled else "disable"
        result = self.action(feature_id, action)
        if result is False:
            return result
        self._state[feature_id] = enabled
        self._update_switch(feature_id)
        self._schedule_save()
        self._play_toggle_sound()
        return result

    def set_config(self, feature_id, key, value):
        normalized = self._normalize_config_value(value)
        self._config.set(feature_id, {key: normalized})
        self._sync_config(feature_id, key, normalized)
        self._schedule_save()
        result = None
        if self._state.get(feature_id, False) and self._is_connected():
            result = self._feature_service.set_config(feature_id, {key: normalized})
        return result

    def action(self, feature_id, action, payload=None):
        manifest = self._manifest(feature_id)
        action_meta = self._action_meta(manifest, action)
        if self._requires_connection(action_meta) and not self._is_connected():
            self._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return False

        route_type = action_meta.get("type")
        if route_type == "set_config":
            config_payload = dict(action_meta.get("payload") or {})
            config_payload.update(payload or {})
            result = self._feature_service.set_config(feature_id, config_payload)
        elif route_type == "plugin_feature":
            result = self._call_plugin_feature(feature_id, action)
        elif action == "enable":
            result = self._feature_service.enable(feature_id)
            self._state[feature_id] = True
        elif action == "disable":
            result = self._feature_service.disable(feature_id)
            self._state[feature_id] = False
        elif action == "cleanup":
            result = self._feature_service.cleanup(feature_id)
        elif action in set(manifest.get("rpc") or ()):
            result = self._feature_service.call_action(feature_id, action, payload or action_meta.get("payload") or {})
        else:
            self._log(f"⚠ 功能动作未在 manifest.rpc 或 manifest.actions 声明: {feature_id}.{action}")
            return False

        self._update_switch(feature_id)
        self._schedule_save()
        return result

    def restore_enabled(self):
        for feature_id, enabled in list(self._state.items()):
            if not enabled:
                continue
            manifest = self._manifest(feature_id)
            if manifest.get("lifecycle", {}).get("restore", True) is False:
                continue
            self.action(feature_id, "enable")
        for feature_id in self._state:
            self._update_switch(feature_id)

    def _manifest(self, feature_id):
        feature = self._registry.get(feature_id)
        return feature.manifest if feature else {"feature_id": feature_id}

    @staticmethod
    def _action_meta(manifest, action):
        actions = manifest.get("actions") or {}
        if action in actions:
            return dict(actions[action] or {})
        for control in manifest.get("controls", []):
            if control.get("action") == action:
                return dict(control)
        return {}

    @staticmethod
    def _requires_connection(action_meta):
        return bool(action_meta.get("requires_connection", True))

    def _call_plugin_feature(self, feature_id, action):
        feature = self._registry.get(feature_id)
        if not feature:
            return False
        method = getattr(feature, action, None)
        if not callable(method):
            self._log(f"⚠ 插件未提供动作: {feature_id}.{action}")
            return False
        return method()

    @staticmethod
    def _normalize_config_value(value):
        if isinstance(value, (int, float)):
            return round(float(value), 1)
        try:
            return round(float(value), 1)
        except (TypeError, ValueError):
            return value
