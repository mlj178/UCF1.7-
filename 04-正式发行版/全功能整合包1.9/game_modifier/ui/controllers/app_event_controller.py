from core.log_router import build_log_route
from core.log_manager import log_to_file
from ui.controllers.plugin_event_router import PluginEventRouter


class AppEventController:
    def __init__(self, app, log_writer=log_to_file):
        self._app = app
        self._log_writer = log_writer
        self._plugin_events = PluginEventRouter(app._plugin_registry, app._panel_context)

    def register(self, event_bus):
        event_bus.subscribe("log_message", self.on_log_message)
        event_bus.subscribe("connection_status", self.on_connection_status)
        event_bus.subscribe("feature_status_changed", self.on_feature_status)
        event_bus.subscribe("plugin_event", self.on_plugin_event)

    def on_log_message(self, **kwargs):
        app = self._app
        route = build_log_route(
            level=kwargs.get("level", "info"),
            module=kwargs.get("module", ""),
            message=kwargs.get("message", ""),
            audience=kwargs.get("audience", "user"),
            dev_detail=kwargs.get("dev_detail", ""),
        )
        if route.write_to_dev_log:
            self._log_writer(route.level, route.module, route.dev_message)
        if not route.show_in_ui:
            return
        icon_map = {"success": "✅", "error": "❌", "info": "ℹ️", "warn": "⚠️"}
        icon = icon_map.get(route.level, "ℹ️")
        ui_message = f"{icon} [{route.module}] {route.user_message}"
        if not app._ui_ready:
            app._early_log_messages.append(ui_message)
            return
        app._log(ui_message)

    def on_connection_status(self, **kwargs):
        app = self._app
        status = kwargs.get("status", "disconnected")
        pid = kwargs.get("pid")

        def update():
            if status == "connected":
                app._set_status("green", "已连接")
                app.pid_label.configure(text=f"PID: {pid}")
                app._ready = True
                app._pid = pid
                app._feature_controller.restore_features()
                app._battle_round_controller.sync_to_game_on_connect()
                app._nano4t_runtime_controller.auto_init_async()
                app._weapon_controller.init_hotkey_manager()
                app._roundskip_monitor.start()
            elif status == "not_found":
                app._set_status("yellow", "未找到游戏")
            else:
                app._set_status("red", "连接断开，正在重连...")
                app._ready = False
                app._battle_round_active = False
                app._battle_mode_active = False
                app._battle_round_controller.on_disconnected()
                app._weapon_controller.pause_hotkeys()
                app._roundskip_monitor.stop()

        app.after(0, update)

    def on_feature_status(self, **kwargs):
        app = self._app
        if getattr(app, "_stop", False):
            return

        feature_id = kwargs.get("feature", "")
        enabled = kwargs.get("enabled", False)
        app._features[feature_id] = enabled
        app.after(0, lambda: app._update_switch(feature_id))

    def on_plugin_event(self, **kwargs):
        self._plugin_events.route(
            kwargs.get("feature", ""),
            kwargs.get("event", ""),
            kwargs.get("payload", {}),
        )
