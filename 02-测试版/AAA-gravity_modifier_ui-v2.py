import customtkinter as ctk
import frida
import json
import threading
import time
from datetime import datetime
import os
import sys

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class GravityModifierApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("重力修改器")
        self.geometry("650+100+100")
        self.resizable(False, False)

        self.session = None
        self.script = None
        self.device = None
        self.is_connected = False
        self.is_monitoring = False

        self.current_gravity = -20.0
        self.original_gravity = -9.81
        self.gravity_mode = "player_only"

        self.setup_ui()
        self.after(500, self._auto_connect_thread)

    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="重力修改器",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=10)

        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.pack(pady=5, padx=20, fill="x")

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="状态: 未连接",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(side="left", padx=10, pady=5)

        self.address_label = ctk.CTkLabel(
            self.status_frame,
            text="地址: 未获取",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.address_label.pack(side="right", padx=10, pady=5)

        self.gravity_display_frame = ctk.CTkFrame(self.main_frame)
        self.gravity_display_frame.pack(pady=10, padx=20, fill="x")

        self.gravity_label = ctk.CTkLabel(
            self.gravity_display_frame,
            text="当前重力值: -20.0",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.gravity_label.pack(pady=10)

        self.original_label = ctk.CTkLabel(
            self.gravity_display_frame,
            text="原始重力值: -9.81",
            font=ctk.CTkFont(size=14)
        )
        self.original_label.pack(pady=5)

        self.mode_label = ctk.CTkLabel(
            self.gravity_display_frame,
            text="作用范围: 仅玩家",
            font=ctk.CTkFont(size=14)
        )
        self.mode_label.pack(pady=5)

        self.slider_frame = ctk.CTkFrame(self.main_frame)
        self.slider_frame.pack(pady=10, padx=20, fill="x")

        self.slider_label = ctk.CTkLabel(
            self.slider_frame,
            text="重力值调节 (-30 ~ 0)",
            font=ctk.CTkFont(size=14)
        )
        self.slider_label.pack(pady=5)

        self.gravity_slider = ctk.CTkSlider(
            self.slider_frame,
            from_=-30, to=0, number_of_steps=60,
            command=self.on_slider_change
        )
        self.gravity_slider.set(-20.0)
        self.gravity_slider.pack(pady=10, padx=20, fill="x")

        self.slider_value_label = ctk.CTkLabel(
            self.slider_frame,
            text="-20.0",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.slider_value_label.pack(pady=5)

        self.mode_frame = ctk.CTkFrame(self.main_frame)
        self.mode_frame.pack(pady=10, padx=20, fill="x")

        self.mode_label_title = ctk.CTkLabel(
            self.mode_frame,
            text="作用范围:",
            font=ctk.CTkFont(size=14)
        )
        self.mode_label_title.pack(side="left", padx=10, pady=5)

        self.mode_var = ctk.StringVar(value="player_only")

        self.player_only_radio = ctk.CTkRadioButton(
            self.mode_frame,
            text="仅玩家", variable=self.mode_var,
            value="player_only", command=self.on_mode_change
        )
        self.player_only_radio.pack(side="left", padx=10, pady=5)

        self.all_radio = ctk.CTkRadioButton(
            self.mode_frame,
            text="玩家 + BOT", variable=self.mode_var,
            value="all", command=self.on_mode_change
        )
        self.all_radio.pack(side="left", padx=10, pady=5)

        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.pack(pady=10, padx=20, fill="x")

        self.apply_btn = ctk.CTkButton(
            self.control_frame,
            text="应用重力", command=self.apply_gravity,
            fg_color="green", hover_color="darkgreen", width=120
        )
        self.apply_btn.pack(side="left", padx=10, pady=10)

        self.reset_btn = ctk.CTkButton(
            self.control_frame,
            text="重置重力", command=self.reset_gravity,
            fg_color="orange", hover_color="darkorange", width=120
        )
        self.reset_btn.pack(side="left", padx=10, pady=10)

        self.monitor_btn = ctk.CTkButton(
            self.control_frame,
            text="开始监控", command=self.toggle_monitor,
            fg_color="blue", hover_color="darkblue", width=120
        )
        self.monitor_btn.pack(side="left", padx=10, pady=10)

        self.log_frame = ctk.CTkFrame(self.main_frame)
        self.log_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.log_label = ctk.CTkLabel(
            self.log_frame,
            text="日志输出:",
            font=ctk.CTkFont(size=14)
        )
        self.log_label.pack(anchor="w", padx=10, pady=5)

        self.log_text = ctk.CTkTextbox(
            self.log_frame,
            height=250,
            font=ctk.CTkFont(size=12, family="Consolas")
        )
        self.log_text.pack(padx=10, pady=5, fill="both", expand=True)

        self.preset_frame = ctk.CTkFrame(self.main_frame)
        self.preset_frame.pack(pady=5, padx=20, fill="x")

        self.preset_label = ctk.CTkLabel(
            self.preset_frame, text="预设值:", font=ctk.CTkFont(size=12)
        )
        self.preset_label.pack(side="left", padx=5, pady=5)

        presets = [
            ("正常重力 (-20)", -20.0),
            ("低重力 (-10)", -10.0),
            ("月球重力 (-3)", -3.0),
            ("无重力 (0)", 0.0)
        ]
        for text, value in presets:
            btn = ctk.CTkButton(
                self.preset_frame, text=text,
                command=lambda v=value: self.set_preset(v),
                width=100, height=30
            )
            btn.pack(side="left", padx=5, pady=5)

    def _auto_connect_thread(self):
        threading.Thread(target=self.connect_to_game, daemon=True).start()

    def _safe_log(self, message, level="info"):
        self.after(0, lambda: self.log(message, level))

    def _safe_configure(self, widget, **kwargs):
        self.after(0, lambda: widget.configure(**kwargs))

    def connect_to_game(self):
        try:
            self._safe_log("正在连接游戏...")

            self.device = frida.get_local_device()
            self._safe_log(f"[调试] 本地设备: {self.device}")

            processes = self.device.enumerate_processes()
            self._safe_log(f"[调试] 进程数: {len(processes)}")

            game_process = None
            for proc in processes:
                if "Unity" in proc.name or "GameAssembly" in proc.name:
                    game_process = proc
                    break

            if not game_process:
                self._safe_log("错误: 未找到游戏进程", "error")
                return

            self._safe_log(f"找到游戏进程: {game_process.name} (PID: {game_process.pid})")

            self.session = self.device.attach(game_process.pid)
            self._safe_log(f"[调试] session 已创建")

            js_path = os.path.join(os.path.dirname(__file__), "AAA-gravity_modifier-v8.js")
            if not os.path.exists(js_path):
                self._safe_log(f"错误: 找不到JS脚本 {js_path}", "error")
                self._safe_log(f"[调试] 当前目录: {os.path.dirname(__file__)}")
                return

            with open(js_path, 'r', encoding='utf-8') as f:
                js_code = f.read()

            self._safe_log(f"[调试] JS脚本长度: {len(js_code)} 字节")

            self.script = self.session.create_script(js_code)
            self.script.on('message', self.on_message)
            self.script.load()

            self.is_connected = True
            self._safe_configure(self.status_label, text="状态: 已连接")
            self._safe_log("✓ 成功连接到游戏")
            self._safe_log("✓ 重力修改器已加载")

        except Exception as e:
            self._safe_log(f"连接失败: {str(e)}", "error")
            self._safe_log(f"[调试] 异常类型: {type(e).__name__}")

    def on_message(self, message, data):
        if message['type'] == 'send':
            payload = message['payload']
            if isinstance(payload, dict):
                self._safe_log(f"[JS] {payload.get('text', str(payload))}")
            else:
                self._safe_log(f"[JS] {payload}")

        elif message['type'] == 'error':
            desc = message.get('description', '')
            self._safe_log(f"[JS错误] {desc}", "error")

    def on_slider_change(self, value):
        value = round(value, 1)
        self.slider_value_label.configure(text=str(value))
        self.current_gravity = value

    def on_mode_change(self):
        self.gravity_mode = self.mode_var.get()
        if self.gravity_mode == "player_only":
            self.mode_label.configure(text="作用范围: 仅玩家")
        else:
            self.mode_label.configure(text="作用范围: 玩家 + BOT")

    def apply_gravity(self):
        if not self.is_connected:
            self.log("错误: 请先连接游戏", "error")
            return

        try:
            value = self.current_gravity
            mode = self.gravity_mode
            self.log(f"安装 Hook + 设置重力: {value} (模式: {mode})")

            hook_result = self.script.exports_sync.installhook()
            if not hook_result.get('ok'):
                self.log(f"✗ 初始化失败", "error")
                return

            self.log("✓ 重力修改已启动")

            result = self.script.exports_sync.setgravity(value, mode)

            if result.get('ok'):
                scale = result.get('scale', 1.0)
                self.log(f"✓ 已应用 (缩放比: {scale:.2f})")
            else:
                self.log(f"✗ 失败", "error")

        except Exception as e:
            self.log(f"异常: {str(e)}", "error")

    def reset_gravity(self):
        if not self.is_connected:
            self.log("错误: 请先连接游戏", "error")
            return

        try:
            self.log("正在重置重力...")
            self.script.exports_sync.resetgravity()
            self.gravity_slider.set(-20.0)
            self.slider_value_label.configure(text="-20.0")
            self.current_gravity = -20.0
            self.log(f"✓ 重力已重置为默认值")
        except Exception as e:
            self.log(f"重置重力失败: {str(e)}", "error")

    def toggle_monitor(self):
        if not self.is_connected:
            self.log("错误: 请先连接游戏", "error")
            return

        try:
            if self.is_monitoring:
                self.script.exports_sync.stopmonitor()
                self.is_monitoring = False
                self.monitor_btn.configure(text="开始监控")
                self.log("停止监控")
            else:
                self.script.exports_sync.startmonitor()
                self.is_monitoring = True
                self.monitor_btn.configure(text="停止监控")
                self.log("开始监控重力值")
        except Exception as e:
            self.log(f"切换监控失败: {str(e)}", "error")

    def get_current_gravity(self):
        if not self.is_connected:
            return
        try:
            result = self.script.exports_sync.getgravity()
            self.current_gravity = result.get('current', -20.0)
            self.original_gravity = result.get('original', -9.81)
            self.gravity_mode = result.get('mode', 'player_only')
            self.update_display()
            self.log(f"当前重力: {self.current_gravity}, 原始重力: {self.original_gravity}")
        except Exception as e:
            self.log(f"获取重力值失败: {str(e)}", "error")

    def set_preset(self, value):
        self.gravity_slider.set(value)
        self.slider_value_label.configure(text=str(value))
        self.current_gravity = value
        self.log(f"选择预设值: {value}")

    def update_display(self):
        self.gravity_label.configure(text=f"当前重力值: {self.current_gravity}")
        self.original_label.configure(text=f"原始重力值: {self.original_gravity}")
        self.gravity_slider.set(self.current_gravity)
        self.slider_value_label.configure(text=str(self.current_gravity))

    def log(self, message, level="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.configure(state="normal")
        self.log_text.insert("end", log_entry)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def on_closing(self):
        if self.script:
            try:
                self.script.unload()
            except:
                pass
        if self.session:
            try:
                self.session.detach()
            except:
                pass
        self.destroy()


if __name__ == "__main__":
    app = GravityModifierApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
