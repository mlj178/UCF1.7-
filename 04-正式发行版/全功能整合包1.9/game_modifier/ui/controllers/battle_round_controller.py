class BattleRoundController:
    def __init__(self, app):
        self._app = app

    def sync_to_game_on_connect(self):
        app = self._app
        app._game_action_service.battle_round_get_status()
        if app._battle_round_enabled:
            app._game_action_service.set_battle_round_enabled(True)
        self.update_button_state()

    def on_disconnected(self):
        app = self._app
        app._battle_round_active = False
        app._battle_mode_active = False
        self.update_button_state()

    def toggle(self):
        app = self._app
        current = app.battle_round_switch.get()
        app._battle_round_enabled = bool(current)
        app._battle_round_active = bool(current and app._battle_mode_active)

        if app._ready:
            app._game_action_service.set_battle_round_enabled(bool(current))

        if current:
            if not app._ready:
                app._log("✅ 强制决战回合已预约，等待连接游戏")
            elif not app._battle_mode_active:
                app._log("✅ 强制决战回合已预约，等待进入多人生化")
            else:
                app._log("✅ 强制决战回合已启用，将在下一回合生效")
        else:
            app._log("强制决战回合已关闭，后续回合不再写入")

        self.update_button_state()
        app._schedule_save_state()

    def update_button_state(self):
        app = self._app
        app.battle_round_switch.configure(state="normal")
        if not app._battle_round_enabled:
            app.battle_round_switch.deselect()
            app.battle_round_status_label.configure(text="状态: 已关闭", text_color="#888888")
        elif not app._ready:
            app.battle_round_switch.select()
            app.battle_round_status_label.configure(text="状态: 已预约，等待连接游戏", text_color="#f39c12")
        elif not app._battle_mode_active:
            app.battle_round_switch.select()
            app.battle_round_status_label.configure(text="状态: 已预约，等待多人生化", text_color="#f39c12")
        else:
            app.battle_round_switch.select()
            app.battle_round_status_label.configure(text="状态: 已启用，下回合生效", text_color="#2ecc71")

    def apply_status(self, flag):
        app = self._app
        try:
            if flag == 1:
                app.battle_round_status_label.configure(text="状态: ⚔️ 决战回合", text_color="#2ecc71")
            elif flag == 0:
                app.battle_round_status_label.configure(text="状态: 🔄 普通回合", text_color="#f39c12")
            else:
                app.battle_round_status_label.configure(text="状态: 读取中...", text_color="#888888")
        except Exception:
            pass

    def on_mode_enter(self):
        app = self._app
        app._battle_mode_active = True
        app._battle_round_active = app._battle_round_enabled
        self.update_button_state()

    def on_mode_exit(self):
        app = self._app
        app._battle_mode_active = False
        app._battle_round_active = False
        self.update_button_state()

    def on_round(self, payload):
        app = self._app
        app._battle_round_active = bool(payload.get("enabled", False))
        if payload.get("applied", False):
            self.apply_status(payload.get("currentIsBattleRound", 1))
        else:
            self.update_button_state()
