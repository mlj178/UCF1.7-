import threading
import time

from core.config import NANO4T_ATTRS
from ui.views.shell_view import apply_status_dot_style

from .state import state


class Nano4tRuntime:
    def __init__(self, context, selector):
        self._context = context
        self._selector = selector

    @property
    def handles(self):
        return state.handles

    def on_ghost_select(self, value):
        try:
            result = self._selector.select_ghost(value)
            if not result.ok:
                self._context.log(f"⚠ [多人生化] {result.error}")
                return
            self.handles.nano4t_ghost_desc.configure(text=result.description)
            if state.ready:
                self.handles.nano4t_next_label.configure(text="💡 请点击「应用」按钮生效")
        except Exception as e:
            self._context.log(f"❌ [多人生化] 幽灵方选择错误: {e}")

    def on_human_select(self, value):
        try:
            result = self._selector.select_human(value)
            if not result.ok:
                self._context.log(f"⚠ [多人生化] {result.error}")
                return
            self.handles.nano4t_human_desc.configure(text=result.description)
            if state.ready:
                self.handles.nano4t_next_label.configure(text="💡 请点击「应用」按钮生效")
        except Exception as e:
            self._context.log(f"❌ [多人生化] 人类方选择错误: {e}")

    def refresh_next_label(self):
        if state.ready and state.activated:
            g = state.wanted_ghost
            h = state.wanted_human
            if g >= 0 and h >= 0:
                self.handles.nano4t_next_label.configure(
                    text=f"下一回合已锁定: 👻 {NANO4T_ATTRS[g][0]}  |  🛡️ {NANO4T_ATTRS[h][0]}"
                )
            else:
                self.handles.nano4t_next_label.configure(text="请选择特性并点击「应用」")
        elif state.ready:
            self.handles.nano4t_next_label.configure(text="请选择特性并点击「应用」")
        else:
            self.handles.nano4t_next_label.configure(text="")

    def set_status(self, color, text):
        apply_status_dot_style(self.handles.nano4t_status_dot, color)
        self.handles.nano4t_status_label.configure(text=text)

    def on_ready(self, count):
        state.ready = True
        self._context.feature_event("mode_enter", {}, feature_id="battle_round")
        self.set_status("green", "已就绪")
        self.handles.nano4t_apply_btn.configure(state="normal", fg_color="#2563eb")
        self._context.log(f"✅ [多人生化] 已就绪！共 {count} 种特性")
        self._context.log("[多人生化] 当前未激活，游戏将正常运行。选择特性后点击应用 → 下一回合生效")
        self.handles.nano4t_next_label.configure(text="💡 请选择特性后点击「应用」按钮")
        self.get_current_async()

    def on_destroyed_event(self):
        if state.ready:
            self._context.log("⚠ 检测到退出多人生化房间，特性系统已销毁")
        self.handle_mode_exit()

    def on_dead(self):
        if state.ready:
            self._context.log("⚠ [多人生化] 模式实例已失效")
        self.handle_mode_exit()

    def on_alive(self):
        if not state.ready and self._context.is_connected():
            self._context.log("ℹ️ [多人生化] 检测到已进入多人生化模式，正在初始化...")
            self.auto_init_if_needed_async()

    def handle_mode_exit(self):
        state.ready = False
        state.activated = False
        state.current_ghost = -1
        state.current_human = -1
        self._context.feature_event("mode_exit", {}, feature_id="battle_round")
        self._context.after(0, self.on_destroyed)

    def on_destroyed(self):
        self.handles.nano4t_apply_btn.configure(state="disabled", fg_color="#333333")
        self.set_status("yellow", "已退出房间")
        self.handles.nano4t_next_label.configure(text="")
        self.handles.nano4t_round_label.configure(text="当前回合: 等待进入多人生化模式...")
        self.handles.nano4t_ghost_status_label.configure(text="[未激活]", text_color="#888888")
        self.handles.nano4t_human_status_label.configure(text="[未激活]", text_color="#888888")

    def on_error(self, payload):
        state.ready = False
        if state.log_errors:
            state.log_errors = False
            message = payload.get("msg", "")
            if "未检测到游戏" in message:
                self._context.log("⚠ [多人生化] 未检测到游戏进程")
            elif "未进入多人生化模式" in message:
                self._context.log("⚠ [多人生化] 检测到游戏，但尚未进入「多人生化模式」")
                self._context.log("  请选择多人生化模式并进入房间")
            elif "房间" in message:
                self._context.log("⚠ [多人生化] 已在多人生化模式菜单，但尚未进入房间")
            else:
                self._context.log(f"❌ [多人生化] {message}")
        self._context.after(0, lambda: self.set_status("yellow", "未就绪"))
        self._context.feature_event("mode_exit", {}, feature_id="battle_round")

    def on_set(self, ghost_id, human_id):
        state.wanted_ghost = ghost_id
        state.wanted_human = human_id
        state.activated = True
        self._context.log(
            f"✅ [多人生化] 已锁定: {NANO4T_ATTRS[ghost_id][0]} + "
            f"{NANO4T_ATTRS[human_id][0]}，下一回合生效"
        )
        self._context.after(0, self.refresh_next_label)
        self._context.after(0, lambda: self.handles.nano4t_ghost_status_label.configure(text="[已激活]", text_color="#88ff88"))
        self._context.after(0, lambda: self.handles.nano4t_human_status_label.configure(text="[已激活]", text_color="#88ff88"))

    def update_round_label(self, ghost_id, human_id):
        state.current_ghost = ghost_id
        state.current_human = human_id
        if ghost_id >= 0 and human_id >= 0:
            text = f"当前回合: 👻 {NANO4T_ATTRS[ghost_id][0]}  |  🛡️ {NANO4T_ATTRS[human_id][0]}"
        elif state.ready:
            text = "当前回合: 等待回合开始..."
        else:
            text = "当前回合: 等待进入游戏..."
        self.handles.nano4t_round_label.configure(text=text)

    def apply(self):
        if not state.ready:
            self._context.log("⚠ [多人生化] 尚未就绪，请先进入「多人生化模式」房间")
            return

        current_time = time.time()
        if current_time - state.apply_cooldown < 0.5:
            self._context.log("⚠ [多人生化] 请勿频繁点击")
            return
        state.apply_cooldown = current_time

        ghost_id = state.temp_ghost
        human_id = state.temp_human
        if ghost_id < 0 or ghost_id >= 10:
            self._context.log(f"❌ [多人生化] 幽灵方特性ID无效: {ghost_id}（有效范围: 0-9）")
            return
        if human_id < 10 or human_id >= 20:
            self._context.log(f"❌ [多人生化] 人类方特性ID无效: {human_id}（有效范围: 10-19）")
            return

        threading.Thread(target=lambda: self.apply_bg(ghost_id, human_id), daemon=True).start()

    def apply_bg(self, ghost_id, human_id):
        try:
            self._context.feature_service.call_action("nano4t", "nano4tSet", {"g": ghost_id, "h": human_id})
            state.wanted_ghost = ghost_id
            state.wanted_human = human_id
        except Exception as e:
            self._context.log(f"❌ [多人生化] 应用失败: {e}")
            state.ready = False
            self._context.after(0, lambda: (
                self.handles.nano4t_apply_btn.configure(state="disabled", fg_color="#333333"),
                self.set_status("yellow", "已断开"),
                self.handles.nano4t_ghost_status_label.configure(text="[未激活]", text_color="#888888"),
                self.handles.nano4t_human_status_label.configure(text="[未激活]", text_color="#888888"),
            ))

    def auto_init_async(self):
        threading.Thread(target=self.auto_init_bg, daemon=True).start()

    def auto_init_bg(self):
        try:
            if self._context.is_connected() and not state.ready:
                self._context.feature_service.call_action("nano4t", "nano4tInit", {})
        except Exception:
            pass

    def get_current_async(self):
        threading.Thread(target=self.get_current_bg, daemon=True).start()

    def get_current_bg(self):
        try:
            if self._context.is_connected() and state.ready:
                self._context.feature_service.call_action("nano4t", "nano4tGetCurrent", {})
        except Exception:
            pass

    def auto_init_if_needed_async(self):
        threading.Thread(target=self.auto_init_bg, daemon=True).start()
