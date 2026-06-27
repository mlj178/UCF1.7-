import threading
import time

from core.config import NANO4T_ATTRS
from ui.views.shell_view import apply_status_dot_style


class Nano4tRuntimeController:
    def __init__(self, app):
        self._app = app

    def on_ghost_select(self, value):
        app = self._app
        try:
            result = app._nano4t_selector.select_ghost(value)
            if not result.ok:
                app._log(f"⚠ [多人生化] {result.error}")
                return
            app._nano4t_temp_ghost = result.feature_id
            app.nano4t_ghost_desc.configure(text=result.description)
            if app._nano4t_ready:
                app.nano4t_next_label.configure(text="💡 请点击「应用」按钮生效")
        except Exception as e:
            app._log(f"❌ [多人生化] 幽灵方选择错误: {e}")

    def on_human_select(self, value):
        app = self._app
        try:
            result = app._nano4t_selector.select_human(value)
            if not result.ok:
                app._log(f"⚠ [多人生化] {result.error}")
                return
            app._nano4t_temp_human = result.feature_id
            app.nano4t_human_desc.configure(text=result.description)
            if app._nano4t_ready:
                app.nano4t_next_label.configure(text="💡 请点击「应用」按钮生效")
        except Exception as e:
            app._log(f"❌ [多人生化] 人类方选择错误: {e}")

    def refresh_next_label(self):
        app = self._app
        if app._nano4t_ready and app._nano4t_activated:
            g = app._nano4t_wanted_ghost
            h = app._nano4t_wanted_human
            if g >= 0 and h >= 0:
                app.nano4t_next_label.configure(
                    text=f"下一回合已锁定: 👻 {NANO4T_ATTRS[g][0]}  |  🛡️ {NANO4T_ATTRS[h][0]}"
                )
            else:
                app.nano4t_next_label.configure(text="请选择特性并点击「应用」")
        elif app._nano4t_ready:
            app.nano4t_next_label.configure(text="请选择特性并点击「应用」")
        else:
            app.nano4t_next_label.configure(text="")

    def set_status(self, color, text):
        app = self._app
        apply_status_dot_style(app.nano4t_status_dot, color)
        app.nano4t_status_label.configure(text=text)

    def on_ready(self, count):
        app = self._app
        app._nano4t_ready = True
        app._battle_mode_active = True
        self.set_status("green", "已就绪")
        app.nano4t_apply_btn.configure(state="normal", fg_color="#2563eb")
        app._log(f"✅ [多人生化] 已就绪！共 {count} 种特性")
        app._log("[多人生化] 当前未激活，游戏将正常运行。选择特性后点击应用 → 下一回合生效")
        app.nano4t_next_label.configure(text="💡 请选择特性后点击「应用」按钮")
        self.get_current_async()

    def on_destroyed_event(self):
        app = self._app
        if app._nano4t_ready:
            app._log("⚠ 检测到退出多人生化房间，特性系统已销毁")
        self.handle_mode_exit()

    def on_dead(self):
        app = self._app
        if app._nano4t_ready:
            app._log("⚠ [多人生化] 模式实例已失效")
        self.handle_mode_exit()

    def on_alive(self):
        app = self._app
        if not app._nano4t_ready and app._ready:
            app._log("ℹ️ [多人生化] 检测到已进入多人生化模式，正在初始化...")
            self.auto_init_if_needed_async()

    def handle_mode_exit(self):
        app = self._app
        app._nano4t_ready = False
        app._nano4t_activated = False
        app._nano4t_current_ghost = -1
        app._nano4t_current_human = -1
        app._battle_mode_active = False
        app._battle_round_active = False
        app.after(0, self.on_destroyed)

    def on_destroyed(self):
        app = self._app
        app.nano4t_apply_btn.configure(state="disabled", fg_color="#333333")
        self.set_status("yellow", "已退出房间")
        app.nano4t_next_label.configure(text="")
        app.nano4t_round_label.configure(text="当前回合: 等待进入多人生化模式...")
        app.nano4t_ghost_status_label.configure(text="[未激活]", text_color="#888888")
        app.nano4t_human_status_label.configure(text="[未激活]", text_color="#888888")
        app.battle_round_switch.configure(state="normal")
        app._battle_round_controller.update_button_state()

    def on_error(self, payload):
        app = self._app
        app._nano4t_ready = False
        if app._nano4t_log_errors:
            app._nano4t_log_errors = False
            message = payload.get("msg", "")
            if "未检测到游戏" in message:
                app._log("⚠ [多人生化] 未检测到游戏进程")
            elif "未进入多人生化模式" in message:
                app._log("⚠ [多人生化] 检测到游戏，但尚未进入「多人生化模式」")
                app._log("  请选择多人生化模式并进入房间")
            elif "房间" in message:
                app._log("⚠ [多人生化] 已在多人生化模式菜单，但尚未进入房间")
            else:
                app._log(f"❌ [多人生化] {message}")
        app.after(0, lambda: self.set_status("yellow", "未就绪"))
        app.after(0, app._battle_round_controller.update_button_state)

    def on_set(self, ghost_id, human_id):
        app = self._app
        app._nano4t_wanted_ghost = ghost_id
        app._nano4t_wanted_human = human_id
        app._nano4t_activated = True
        app._log(
            f"✅ [多人生化] 已锁定: {NANO4T_ATTRS[ghost_id][0]} + "
            f"{NANO4T_ATTRS[human_id][0]}，下一回合生效"
        )
        app.after(0, self.refresh_next_label)
        app.after(0, lambda: app.nano4t_ghost_status_label.configure(text="[已激活]", text_color="#88ff88"))
        app.after(0, lambda: app.nano4t_human_status_label.configure(text="[已激活]", text_color="#88ff88"))

    def update_round_label(self, ghost_id, human_id):
        app = self._app
        app._nano4t_current_ghost = ghost_id
        app._nano4t_current_human = human_id
        if ghost_id >= 0 and human_id >= 0:
            text = f"当前回合: 👻 {NANO4T_ATTRS[ghost_id][0]}  |  🛡️ {NANO4T_ATTRS[human_id][0]}"
        elif app._nano4t_ready:
            text = "当前回合: 等待回合开始..."
        else:
            text = "当前回合: 等待进入游戏..."
        app.nano4t_round_label.configure(text=text)

    def apply(self):
        app = self._app
        if not app._nano4t_ready:
            app._log("⚠ [多人生化] 尚未就绪，请先进入「多人生化模式」房间")
            return

        current_time = time.time()
        if current_time - app._nano4t_apply_cooldown < 0.5:
            app._log("⚠ [多人生化] 请勿频繁点击")
            return
        app._nano4t_apply_cooldown = current_time

        ghost_id = app._nano4t_temp_ghost
        human_id = app._nano4t_temp_human
        if ghost_id < 0 or ghost_id >= 10:
            app._log(f"❌ [多人生化] 幽灵方特性ID无效: {ghost_id}（有效范围: 0-9）")
            return
        if human_id < 10 or human_id >= 20:
            app._log(f"❌ [多人生化] 人类方特性ID无效: {human_id}（有效范围: 10-19）")
            return

        threading.Thread(target=lambda: self.apply_bg(ghost_id, human_id), daemon=True).start()

    def apply_bg(self, ghost_id, human_id):
        app = self._app
        try:
            app._game_action_service.nano4t_set(ghost_id, human_id)
            app._nano4t_wanted_ghost = ghost_id
            app._nano4t_wanted_human = human_id
        except Exception as e:
            app._log(f"❌ [多人生化] 应用失败: {e}")
            app._nano4t_ready = False
            app.after(0, lambda: (
                app.nano4t_apply_btn.configure(state="disabled", fg_color="#333333"),
                self.set_status("yellow", "已断开"),
                app.nano4t_ghost_status_label.configure(text="[未激活]", text_color="#888888"),
                app.nano4t_human_status_label.configure(text="[未激活]", text_color="#888888"),
            ))

    def auto_init_async(self):
        threading.Thread(target=self.auto_init_bg, daemon=True).start()

    def auto_init_bg(self):
        app = self._app
        try:
            app._game_action_service.nano4t_init_if_connected(app._nano4t_ready)
        except Exception:
            pass

    def get_current_async(self):
        threading.Thread(target=self.get_current_bg, daemon=True).start()

    def get_current_bg(self):
        app = self._app
        try:
            app._game_action_service.nano4t_get_current_if_ready(app._nano4t_ready)
        except Exception:
            pass

    def auto_init_if_needed_async(self):
        threading.Thread(target=self.auto_init_if_needed, daemon=True).start()

    def auto_init_if_needed(self):
        app = self._app
        try:
            app._game_action_service.nano4t_init_if_connected(app._nano4t_ready)
        except Exception:
            pass
