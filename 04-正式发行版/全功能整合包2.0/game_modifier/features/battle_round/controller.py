from features.battle_round.state import state


class BattleRoundController:
    def __init__(self, context):
        self._context = context

    @property
    def handles(self):
        return state.handles

    def sync_to_game_on_connect(self):
        self._context.feature_service.call_action("battle_round", "battleRoundGetStatus", {})
        if state.enabled:
            self._context.feature_service.enable("battle_round")
        self.update_button_state()

    def on_disconnected(self):
        state.active = False
        state.mode_active = False
        self.update_button_state()

    def toggle(self):
        current = self.handles.battle_round_switch.get()
        state.enabled = bool(current)
        state.active = bool(current and state.mode_active)
        self._context.config_manager.set("battle_round", {"enabled": state.enabled})

        if self._context.is_connected():
            if current:
                self._context.feature_service.enable("battle_round")
            else:
                self._context.feature_service.disable("battle_round")

        if current:
            if not self._context.is_connected():
                self._context.log("✅ 强制决战回合已预约，等待连接游戏")
            elif not state.mode_active:
                self._context.log("✅ 强制决战回合已预约，等待进入多人生化")
            else:
                self._context.log("✅ 强制决战回合已启用，将在下一回合生效")
        else:
            self._context.log("强制决战回合已关闭，后续回合不再写入")

        self.update_button_state()

    def update_button_state(self):
        if not self.handles:
            return
        self.handles.battle_round_switch.configure(state="normal")
        if not state.enabled:
            self.handles.battle_round_switch.deselect()
            self.handles.battle_round_status_label.configure(text="状态: 已关闭", text_color="#888888")
        elif not self._context.is_connected():
            self.handles.battle_round_switch.select()
            self.handles.battle_round_status_label.configure(text="状态: 已预约，等待连接游戏", text_color="#f39c12")
        elif not state.mode_active:
            self.handles.battle_round_switch.select()
            self.handles.battle_round_status_label.configure(text="状态: 已预约，等待多人生化", text_color="#f39c12")
        else:
            self.handles.battle_round_switch.select()
            self.handles.battle_round_status_label.configure(text="状态: 已启用，下回合生效", text_color="#2ecc71")

    def apply_status(self, flag):
        if not self.handles:
            return
        try:
            if flag == 1:
                self.handles.battle_round_status_label.configure(text="状态: ⚔️ 决战回合", text_color="#2ecc71")
            elif flag == 0:
                self.handles.battle_round_status_label.configure(text="状态: 🔄 普通回合", text_color="#f39c12")
            else:
                self.handles.battle_round_status_label.configure(text="状态: 读取中...", text_color="#888888")
        except Exception:
            pass

    def on_mode_enter(self):
        state.mode_active = True
        state.active = state.enabled
        self.update_button_state()

    def on_mode_exit(self):
        state.mode_active = False
        state.active = False
        self.update_button_state()

    def on_round(self, payload):
        state.active = bool(payload.get("enabled", False))
        if payload.get("applied", False):
            self.apply_status(payload.get("currentIsBattleRound", 1))
        else:
            self.update_button_state()
