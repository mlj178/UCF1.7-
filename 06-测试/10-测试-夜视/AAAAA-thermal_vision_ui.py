# AAAAA-thermal_vision_ui.py - 热成像透视功能 UI
# 功能: 所有模式下，所有角色都可以使用热成像透视
# 按键: T键 | 持续: 3秒 | 显示: 仅敌人

import customtkinter as ctk
import frida
import psutil
import json
import threading
import time
import os
import sys
from datetime import datetime

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "AAAAA-thermal_vision_v2.js")  # 使用方案5的JS脚本

COLOR_GREEN = "#2ecc71"
COLOR_RED = "#e74c3c"
COLOR_ORANGE = "#f39c12"
COLOR_BLUE = "#3498db"
COLOR_DARK = "#1a1a2e"
COLOR_DARKER = "#16213e"


class ThermalVisionApp(ctk.CTk):
    """热成像透视功能 - Python CustomTkinter 可视化界面"""

    def __init__(self):
        super().__init__()

        self.title("热成像透视 v2.0 (方案5: 直接修改组件)")
        self.geometry("500x650")
        self.minsize(460, 580)
        self.resizable(True, True)

        # Frida 连接相关
        self.session = None
        self.script = None
        self.device = None
        self.is_connected = False
        self._cleanup_done = False
        self._connecting = False

        # 状态数据
        self._gs_lock = threading.Lock()
        self.game_state = {
            "enabled": False,
            "duration": 3.0,
            "showHuman": False,
            "cooldownRemaining": 0.0,
            "canTrigger": True,
        }

        self.setup_ui()

        # 自动连接
        self.after(800, self._auto_connect_thread)

    # ==================== UI 构建 ====================

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        # ---- 标题 ----
        ctk.CTkLabel(
            self, text="🔥 热成像透视",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, pady=(16, 2), padx=20, sticky="ew")

        ctk.CTkLabel(
            self, text="T键触发 | 持续3秒 | 仅显示敌人 | 全模式通用",
            font=ctk.CTkFont(size=12), text_color="#888"
        ).grid(row=1, column=0, pady=(0, 8), padx=20, sticky="ew")

        # ---- 状态栏 ----
        status_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_DARK)
        status_frame.grid(row=2, column=0, padx=16, pady=4, sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)

        self.status_dot = ctk.CTkLabel(status_frame, text="⚫", font=ctk.CTkFont(size=18))
        self.status_dot.grid(row=0, column=0, padx=(12, 4), pady=8)

        self.status_label = ctk.CTkLabel(status_frame, text="等待游戏启动...", font=ctk.CTkFont(size=14))
        self.status_label.grid(row=0, column=1, padx=4, pady=8, sticky="w")

        self.pid_label = ctk.CTkLabel(status_frame, text="", font=ctk.CTkFont(size=11), text_color="#888")
        self.pid_label.grid(row=0, column=2, padx=12, pady=8, sticky="e")

        # ---- 控制面板 ----
        ctrl_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_DARKER)
        ctrl_frame.grid(row=3, column=0, padx=16, pady=4, sticky="ew")
        ctrl_frame.grid_columnconfigure(1, weight=1)

        # 热成像开关
        ctk.CTkLabel(ctrl_frame, text="功能开关",
                      font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, padx=(12, 4), pady=(12, 4), sticky="w")

        self.thermal_toggle = ctk.CTkSwitch(
            ctrl_frame, text="关闭", font=ctk.CTkFont(size=13),
            command=self.on_toggle_thermal, progress_color=COLOR_GREEN,
            switch_width=50, switch_height=24
        )
        self.thermal_toggle.grid(row=0, column=1, padx=4, pady=(12, 4), sticky="w")
        self.thermal_toggle.configure(state="disabled")

        # 持续时间设置
        ctk.CTkLabel(ctrl_frame, text="持续时间",
                      font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=1, column=0, padx=(12, 4), pady=(8, 4), sticky="w")

        self.duration_slider = ctk.CTkSlider(
            ctrl_frame, from_=1.0, to=10.0, number_of_steps=18,
            command=self.on_duration_change
        )
        self.duration_slider.set(3.0)
        self.duration_slider.grid(row=1, column=1, padx=4, pady=(8, 4), sticky="w")

        self.duration_label = ctk.CTkLabel(
            ctrl_frame, text="3.0 秒", font=ctk.CTkFont(size=12)
        )
        self.duration_label.grid(row=1, column=2, padx=(4, 12), pady=(8, 4), sticky="w")

        # 显示范围
        ctk.CTkLabel(ctrl_frame, text="显示范围",
                      font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=2, column=0, padx=(12, 4), pady=(8, 12), sticky="w")

        self.show_range_var = ctk.StringVar(value="仅敌人")
        self.show_range_menu = ctk.CTkOptionMenu(
            ctrl_frame, values=["仅敌人", "所有玩家"],
            variable=self.show_range_var,
            command=self.on_show_range_change,
            width=120
        )
        self.show_range_menu.grid(row=2, column=1, padx=4, pady=(8, 12), sticky="w")

        # ---- 信息面板 ----
        info_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_DARK)
        info_frame.grid(row=4, column=0, padx=16, pady=4, sticky="ew")
        info_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(info_frame, text="功能状态", font=ctk.CTkFont(size=10), text_color="#888").grid(
            row=0, column=0, padx=6, pady=(6, 0))
        self.state_label = ctk.CTkLabel(info_frame, text="❌ 关闭",
                                         font=ctk.CTkFont(size=14, weight="bold"))
        self.state_label.grid(row=1, column=0, padx=6, pady=(0, 4))

        ctk.CTkLabel(info_frame, text="冷却时间", font=ctk.CTkFont(size=10), text_color="#888").grid(
            row=0, column=1, padx=6, pady=(6, 0))
        self.cooldown_label = ctk.CTkLabel(info_frame, text="就绪",
                                            font=ctk.CTkFont(size=14, weight="bold"))
        self.cooldown_label.grid(row=1, column=1, padx=6, pady=(0, 4))

        ctk.CTkLabel(info_frame, text="按键提示", font=ctk.CTkFont(size=10), text_color="#888").grid(
            row=2, column=0, columnspan=2, padx=6, pady=(6, 0))
        self.key_label = ctk.CTkLabel(info_frame, text="按 T 键启用热成像",
                                        font=ctk.CTkFont(size=12))
        self.key_label.grid(row=3, column=0, columnspan=2, padx=6, pady=(0, 4))

        # ---- 使用说明 ----
        help_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_DARKER)
        help_frame.grid(row=5, column=0, padx=16, pady=4, sticky="ew")

        help_text = """使用说明:
• 按住 T 键启用热成像透视
• 松开 T 键自动关闭
• 仅显示敌人位置
• 可在移动中使用
• 适用于所有游戏模式"""

        ctk.CTkLabel(
            help_frame, text=help_text,
            font=ctk.CTkFont(size=11), text_color="#aaa",
            justify="left"
        ).grid(row=0, column=0, padx=12, pady=8, sticky="w")

        # ---- 日志 ----
        log_frame = ctk.CTkFrame(self, corner_radius=8)
        log_frame.grid(row=6, column=0, padx=16, pady=(8, 12), sticky="nsew")
        log_frame.grid_rowconfigure(1, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        log_header = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_header.grid(row=0, column=0, padx=8, pady=(6, 2), sticky="ew")

        ctk.CTkLabel(log_header, text="📝 运行日志",
                      font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")

        self.clear_log_btn = ctk.CTkButton(
            log_header, text="清空", width=50, height=22,
            font=ctk.CTkFont(size=11),
            command=self.clear_log
        )
        self.clear_log_btn.pack(side="right", padx=(0, 4))

        self.log_text = ctk.CTkTextbox(
            log_frame, font=ctk.CTkFont(size=11),
            text_color="#ddd", wrap="word"
        )
        self.log_text.grid(row=1, column=0, padx=8, pady=(2, 8), sticky="nsew")

    # ==================== Frida 连接 ====================

    def _auto_connect_thread(self):
        if self._connecting:
            return
        self._connecting = True
        threading.Thread(target=self._try_auto_connect, daemon=True).start()

    def _try_auto_connect(self):
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and 'crossfire' in proc.info['name'].lower():
                    pid = proc.info['pid']
                    self.after(0, lambda p=pid: self._connect_to_game(p))
                    return
        except Exception:
            pass
        finally:
            self._connecting = False

    def _connect_to_game(self, pid):
        try:
            self._update_status("正在连接...", COLOR_ORANGE, f"PID: {pid}")

            device = frida.get_local_device()
            session = device.attach(pid)

            with open(JS_FILE, 'r', encoding='utf-8') as f:
                js_code = f.read()

            script = session.create_script(js_code)
            script.on('message', self._on_message)
            script.load()

            self.session = session
            self.script = script
            self.device = device
            self.is_connected = True

            self._update_status("已连接", COLOR_GREEN, f"PID: {pid}")
            self.thermal_toggle.configure(state="normal")

            self._safe_log("✅ 已连接到游戏进程")

            # 启动状态轮询
            self._start_status_polling()

        except frida.ProcessNotFoundError:
            self._update_status("游戏进程未找到", COLOR_RED, "")
            self._safe_log("❌ 游戏进程未找到")
        except frida.ServerNotStartedError:
            self._update_status("Frida Server 未运行", COLOR_RED, "")
            self._safe_log("❌ Frida Server 未运行，请启动 frida-server")
        except Exception as e:
            self._update_status("连接失败", COLOR_RED, "")
            self._safe_log(f"❌ 连接异常: {e}")

    def _update_status(self, text, color, pid_text):
        self.status_label.configure(text=text, text_color=color)
        self.status_dot.configure(text="🟢" if color == COLOR_GREEN else "🔴" if color == COLOR_RED else "🟡")
        self.pid_label.configure(text=pid_text)

    # ==================== 消息处理 ====================

    def _on_message(self, message, data):
        try:
            if message['type'] == 'log':
                level = message.get('level', 'info')
                module = message.get('module', '未知')
                msg = message.get('message', '')
                timestamp = datetime.now().strftime('%H:%M:%S')
                log_line = f"[{timestamp}][{module}] {msg}"
                self.after(0, lambda: self._safe_log(log_line))

            elif message['type'] == 'status':
                feature = message.get('feature', '')
                enabled = message.get('enabled', False)

                if feature == 'thermal_vision_enabled':
                    with self._gs_lock:
                        self.game_state['enabled'] = enabled
                    self.after(0, lambda: self._update_ui_state())

        except Exception as e:
            self._safe_log(f"消息处理错误: {e}")

    def _safe_log(self, text):
        try:
            self.log_text.configure(state="normal")
            self.log_text.insert("end", text + "\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
        except Exception:
            pass

    # ==================== 状态轮询 ====================

    def _start_status_polling(self):
        self._polling = True
        self._polling_thread()

    def _polling_thread(self):
        if not self._polling or not self.script:
            return

        try:
            status = self.script.exports_sync.getstatus()
            with self._gs_lock:
                self.game_state.update(status)
            self.after(0, self._update_ui_state)
        except Exception:
            pass

        self.after(200, self._polling_thread)

    def _update_ui_state(self):
        with self._gs_lock:
            enabled = self.game_state.get('enabled', False)
            cooldown_remaining = self.game_state.get('cooldownRemaining', 0.0)
            can_trigger = self.game_state.get('canTrigger', True)

        # 更新开关状态
        if self.thermal_toggle.get() != enabled:
            if enabled:
                self.thermal_toggle.select()
            else:
                self.thermal_toggle.deselect()
            self.thermal_toggle.configure(text="开启" if enabled else "关闭")

        # 更新状态标签
        self.state_label.configure(
            text="✅ 开启" if enabled else "❌ 关闭",
            text_color=COLOR_GREEN if enabled else COLOR_RED
        )

        # 更新冷却时间
        if can_trigger:
            self.cooldown_label.configure(text="就绪", text_color=COLOR_GREEN)
        else:
            self.cooldown_label.configure(
                text=f"{cooldown_remaining:.1f}秒",
                text_color=COLOR_ORANGE
            )

    # ==================== 控制回调 ====================

    def on_toggle_thermal(self):
        if not self.script:
            return

        enabled = self.thermal_toggle.get()
        self.thermal_toggle.configure(text="开启" if enabled else "关闭")

        try:
            if enabled:
                self.script.exports_sync.enable()
                self._safe_log("✅ 热成像功能已启用")
            else:
                self.script.exports_sync.disable()
                self._safe_log("❌ 热成像功能已禁用")
        except Exception as e:
            self._safe_log(f"操作失败: {e}")

    def on_duration_change(self, value):
        duration = float(value)
        self.duration_label.configure(text=f"{duration:.1f} 秒")

        if self.script:
            try:
                show_human = self.show_range_var.get() == "所有玩家"
                self.script.exports_sync.setconfig(duration, show_human)
                self._safe_log(f"配置已更新: 持续 {duration:.1f} 秒")
            except Exception as e:
                self._safe_log(f"配置更新失败: {e}")

    def on_show_range_change(self, value):
        if self.script:
            try:
                show_human = value == "所有玩家"
                duration = self.duration_slider.get()
                self.script.exports_sync.setconfig(duration, show_human)
                self._safe_log(f"配置已更新: 显示 {value}")
            except Exception as e:
                self._safe_log(f"配置更新失败: {e}")

    def clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    # ==================== 清理 ====================

    def on_closing(self):
        self._polling = False
        if self.script:
            try:
                self.script.exports_sync.disable()
            except Exception:
                pass
        if self.session:
            try:
                self.session.detach()
            except Exception:
                pass
        self.destroy()


if __name__ == "__main__":
    app = ThermalVisionApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
