from core.log_router import build_log_route
from core.log_manager import log_to_file


class AppEventController:
    def __init__(self, app, log_writer=log_to_file):
        self._app = app
        self._log_writer = log_writer

    def register(self, event_bus):
        event_bus.subscribe("log_message", self.on_log_message)
        event_bus.subscribe("connection_status", self.on_connection_status)
        event_bus.subscribe("feature_status_changed", self.on_feature_status)
        event_bus.subscribe("gather_result", self.on_gather_result)
        event_bus.subscribe("round_skipped", self.on_round_skipped)
        event_bus.subscribe("nano4t_event", self.on_nano4t_event)
        event_bus.subscribe("battle_round_event", self.on_battle_round_event)
        event_bus.subscribe("isbot_event", self.on_isbot_event)

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
                if app._features.get("isbot"):
                    app._set_isbot_state("awaiting_room")
                else:
                    app._set_isbot_state("off")
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
                if app._features.get("isbot"):
                    app._set_isbot_state("awaiting_room")
                else:
                    app._set_isbot_state("off")
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
        if feature_id == "isbot" and not enabled:
            app._set_isbot_state("off")
        app.after(0, lambda: app._update_switch(feature_id))

    def on_isbot_event(self, **kwargs):
        self._app.after(0, lambda: self._app._set_isbot_state(kwargs.get("state", "off")))

    def on_gather_result(self, **kwargs):
        app = self._app
        data = kwargs.get("data", {})
        ok = data.get("ok", False)
        if ok:
            bots = data.get("bots", 0)
            fail = data.get("fail", 0)
            app._log(f"✅ 聚怪结果: 传送成功{bots} 失败{fail}")
        else:
            app._log(f"❌ 聚怪失败: {data.get('msg', '未知')}")

    def on_round_skipped(self, **kwargs):
        app = self._app
        app._log("⏭️ 回合已跳过!")

    def on_nano4t_event(self, **kwargs):
        app = self._app
        event_type = kwargs.get("msg_type", "")
        payload = kwargs.get("payload", {})

        if event_type == "nano4t_ready":
            ids = payload.get("ids", [])
            app.after(0, lambda: app._nano4t_runtime_controller.on_ready(len(ids)))
            app.after(0, app._battle_round_controller.update_button_state)
        elif event_type == "nano4t_destroyed":
            app._nano4t_runtime_controller.on_destroyed_event()
        elif event_type == "nano4t_error":
            app._nano4t_runtime_controller.on_error(payload)
        elif event_type == "nano4t_set":
            g = int(payload.get("g", 0))
            h = int(payload.get("h", 0))
            app._nano4t_runtime_controller.on_set(g, h)
        elif event_type == "nano4t_current":
            g = int(payload.get("g", -1))
            h = int(payload.get("h", -1))
            app.after(0, lambda gg=g, hh=h: app._nano4t_runtime_controller.update_round_label(gg, hh))
        elif event_type == "nano4t_dead":
            app._nano4t_runtime_controller.on_dead()
        elif event_type == "nano4t_alive":
            app._nano4t_runtime_controller.on_alive()

    def on_battle_round_event(self, **kwargs):
        app = self._app
        event_type = kwargs.get("msg_type", "")
        payload = kwargs.get("payload", {})

        def update():
            if event_type == "battle_round_mode_enter":
                app._battle_round_controller.on_mode_enter()
            elif event_type == "battle_round_mode_exit":
                app._battle_round_controller.on_mode_exit()
            elif event_type == "battle_round_round":
                app._battle_round_controller.on_round(payload)

        app.after(0, update)
