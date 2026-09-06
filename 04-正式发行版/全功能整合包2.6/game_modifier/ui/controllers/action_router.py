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
        run_in_background=None,
        schedule_ui=None,
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
        # 后台执行 RPC，避免阻塞 UI 线程；schedule_ui 把回调 post 回 UI 线程
        self._run_in_background = run_in_background or (lambda fn: fn())
        self._schedule_ui = schedule_ui or (lambda delay_ms, fn: fn())

    def toggle(self, feature_id):
        enabled = not bool(self._state.get(feature_id, False))
        action = "enable" if enabled else "disable"

        # 连接检查仍在 UI 线程，给即时反馈
        manifest = self._manifest(feature_id)
        action_meta = self._action_meta(manifest, action)
        if self._requires_connection(action_meta) and not self._is_connected():
            self._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return False

        # 乐观更新：UI 立即响应，不等待 RPC
        self._state[feature_id] = enabled
        self._update_switch(feature_id)
        self._schedule_save()
        self._play_toggle_sound()

        # 后台执行 RPC。这些功能采用「延迟 apply」设计（规范 §9.3）：
        # enable 只置 state.enabled=true，实际写入靠 room-ready Hook；
        # RPC 抛异常或返回 False 并不代表功能未生效，故不回滚 UI 状态。
        def background():
            try:
                self._execute_toggle_rpc(feature_id, action, manifest, action_meta)
            except Exception as exc:
                self._log(f"⚠ 开关操作异常（功能可能延迟生效）: {feature_id}: {exc}")

        self._run_in_background(background)
        return None

    def _execute_toggle_rpc(self, feature_id, action, manifest, action_meta):
        """执行 enable/disable 的实际 RPC，在后台线程调用，不碰 UI。"""
        route_type = action_meta.get("type")
        if route_type == "plugin_feature":
            return self._call_plugin_feature(feature_id, action, None)
        if action == "enable":
            return self._feature_service.enable(feature_id)
        if action == "disable":
            return self._feature_service.disable(feature_id)
        return None

    def set_config(self, feature_id, key, value):
        normalized = self._normalize_config_value(value)
        # UI 配置立即落盘与同步，不等待 RPC
        self._config.set(feature_id, {key: normalized})
        self._sync_config(feature_id, key, normalized)
        self._schedule_save()

        if self._is_connected() and (
            self._state.get(feature_id, False) or feature_id == "esp_box"
        ):
            def background():
                try:
                    self._feature_service.set_config(feature_id, {key: normalized})
                except Exception as exc:
                    self._log(f"⚠ 配置同步失败: {feature_id}.{key}: {exc}")
            self._run_in_background(background)
        return None

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
            result = self._call_plugin_feature(feature_id, action, payload)
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

    def _call_plugin_feature(self, feature_id, action, payload=None):
        feature = self._registry.get(feature_id)
        if not feature:
            return False
        method = getattr(feature, action, None)
        if not callable(method):
            self._log(f"⚠ 插件未提供动作: {feature_id}.{action}")
            return False
        try:
            return method(payload or {})
        except TypeError as exc:
            # Preserve compatibility with existing zero-argument plugin actions.
            try:
                return method()
            except TypeError:
                self._log(f"⚠ 插件动作参数错误: {feature_id}.{action}: {exc}")
                return False

    @staticmethod
    def _normalize_config_value(value):
        if isinstance(value, (int, float)):
            return round(float(value), 1)
        try:
            return round(float(value), 1)
        except (TypeError, ValueError):
            return value
