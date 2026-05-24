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

GRAVITY_OPTIONS = [
    ("正常 (1.0)", 1.0),
    ("低重力 (0.5)", 0.5),
]


class GravityModifierApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("重力 & 跳跃修改器")
        self.geometry("500+200+100")
        self.resizable(False, False)

        self.session = None
        self.script = None
        self.device = None
        self.is_connected = False

        self.gravity_scale = 1.0
        self.jump_scale = 1.0
        self.gravity_mode = "player_only"

        self.setup_ui()
        self.after(500, self._auto_connect_thread)

    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(
            self.main_frame, text="重力 & 跳跃修改器",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(pady=8)

        self.status_label = ctk.CTkLabel(
            self.main_frame, text="状态: 未连接",
            font=ctk.CTkFont(size=13)
        )
        self.status_label.pack(pady=2)

        # === 重力 ===
        self.gravity_frame = ctk.CTkFrame(self.main_frame)
        self.gravity_frame.pack(pady=8, padx=15, fill="x")

        ctk.CTkLabel(self.gravity_frame, text="▼ 重力（下落速度）",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=4)

        self.gravity_var = ctk.StringVar(value="1.0")
        for text, val in GRAVITY_OPTIONS:
            row = ctk.CTkFrame(self.gravity_frame, fg_color="transparent")
            row.pack(pady=2, fill="x")
            ctk.CTkRadioButton(row, text=text, variable=self.gravity_var,
                               value=str(val), command=self.on_gravity_change).pack(side="left", padx=15)

        # === 跳跃 ===
        self.jump_frame = ctk.CTkFrame(self.main_frame)
        self.jump_frame.pack(pady=8, padx=15, fill="x")

        ctk.CTkLabel(self.jump_frame, text="▲ 跳跃高度",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=4)

        self.jump_slider = ctk.CTkSlider(self.jump_frame, from_=1.0, to=2.0,
                                          number_of_steps=100, command=self.on_jump_slider_change)
        self.jump_slider.set(1.0)
        self.jump_slider.pack(pady=5, fill="x", padx=15)

        self.jump_value_label = ctk.CTkLabel(self.jump_frame, text="当前: 1.00x",
                                              font=ctk.CTkFont(size=12))
        self.jump_value_label.pack(pady=2)

        # === 作用范围 ===
        self.mode_frame = ctk.CTkFrame(self.main_frame)
        self.mode_frame.pack(pady=8, padx=15, fill="x")

        self.mode_var = ctk.StringVar(value="player_only")
        ctk.CTkLabel(self.mode_frame, text="作用范围:",
                     font=ctk.CTkFont(size=13)).pack(side="left", padx=10)
        ctk.CTkRadioButton(self.mode_frame, text="仅玩家", variable=self.mode_var,
                           value="player_only").pack(side="left", padx=8)
        ctk.CTkRadioButton(self.mode_frame, text="玩家+BOT", variable=self.mode_var,
                           value="all").pack(side="left", padx=8)

        # === 空中控制 ===
        self.air_frame = ctk.CTkFrame(self.main_frame)
        self.air_frame.pack(pady=8, padx=15, fill="x")

        ctk.CTkLabel(self.air_frame, text="✈ 空中控制",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=4)

        self.air_jump_var = ctk.IntVar(value=0)
        self.air_move_var = ctk.IntVar(value=0)

        air_row = ctk.CTkFrame(self.air_frame, fg_color="transparent")
        air_row.pack(pady=2, fill="x")
        ctk.CTkCheckBox(air_row, text="空中跳跃 (空中可连续跳)",
                        variable=self.air_jump_var).pack(side="left", padx=15)
        ctk.CTkCheckBox(air_row, text="空中移动 (空中可WASD)",
                        variable=self.air_move_var).pack(side="left", padx=15)

        # === 按钮 ===
        self.btn_frame = ctk.CTkFrame(self.main_frame)
        self.btn_frame.pack(pady=12, padx=15, fill="x")

        self.apply_btn = ctk.CTkButton(self.btn_frame, text="应用修改",
                                       command=self.apply_all,
                                       fg_color="green", hover_color="darkgreen", height=35)
        self.apply_btn.pack(side="left", padx=10, expand=True, fill="x")

        self.reset_btn = ctk.CTkButton(self.btn_frame, text="重置",
                                       command=self.reset_all,
                                       fg_color="orange", hover_color="darkorange", height=35)
        self.reset_btn.pack(side="right", padx=10, expand=True, fill="x")

        # === 日志 ===
        self.log_label = ctk.CTkLabel(self.main_frame, text="日志:",
                                      font=ctk.CTkFont(size=12))
        self.log_label.pack(anchor="w", padx=15)

        self.log_text = ctk.CTkTextbox(self.main_frame, height=160,
                                       font=ctk.CTkFont(size=11, family="Consolas"))
        self.log_text.pack(padx=15, pady=5, fill="both", expand=True)

    def _auto_connect_thread(self):
        threading.Thread(target=self.connect_to_game, daemon=True).start()

    def _safe_log(self, msg):
        self.after(0, lambda: self.log(msg))

    def _safe_config(self, widget, **kw):
        self.after(0, lambda: widget.configure(**kw))

    def on_gravity_change(self):
        self.gravity_scale = float(self.gravity_var.get())

    def on_jump_slider_change(self, value):
        self.jump_scale = round(value, 2)
        self.jump_value_label.configure(text="当前: " + f"{self.jump_scale:.2f}x")

    def connect_to_game(self):
        try:
            self._safe_log("连接游戏...")
            self.device = frida.get_local_device()
            for proc in self.device.enumerate_processes():
                if "Unity" in proc.name or "GameAssembly" in proc.name:
                    game_process = proc
                    break
            else:
                self._safe_log("未找到游戏进程")
                return

            self._safe_log("进程: " + game_process.name)
            self.session = self.device.attach(game_process.pid)

            js_path = os.path.join(os.path.dirname(__file__), "AAAAA-gravity_modifier-v8.js")
            with open(js_path, 'r', encoding='utf-8') as f:
                js_code = f.read()

            self.script = self.session.create_script(js_code)
            self.script.on('message', self.on_message)
            self.script.load()

            self.is_connected = True
            self._safe_config(self.status_label, text="状态: 已连接")
            self._safe_log("✓ 已连接")

        except Exception as e:
            self._safe_log("连接失败: " + str(e))

    def on_message(self, message, data):
        if message['type'] == 'send':
            p = message['payload']
            if isinstance(p, dict):
                self._safe_log("[JS] " + p.get('text', str(p)))
            else:
                self._safe_log("[JS] " + str(p))
        elif message['type'] == 'error':
            self._safe_log("[JS错误] " + message.get('description', ''))

    def apply_all(self):
        if not self.is_connected:
            self.log("未连接")
            return
        try:
            mode = self.mode_var.get()
            gs = self.gravity_scale
            js = self.jump_scale
            aj = bool(self.air_jump_var.get())
            am = bool(self.air_move_var.get())
            self.log("应用: 重力=" + str(gs) + " 跳跃=" + str(js) + "x 模式=" + mode + " 空中跳=" + str(aj) + " 空中移动=" + str(am))

            r = self.script.exports_sync.installhook()
            if not r.get('ok'):
                self.log("初始化失败")
                return

            r = self.script.exports_sync.setconfig(gs, js, mode, aj, am)
            if r.get('ok'):
                self.log("✓ 已生效 (退出房间重新进入无需重启)")
            else:
                self.log("应用失败")
        except Exception as e:
            self.log("异常: " + str(e))

    def reset_all(self):
        if not self.is_connected:
            self.log("未连接")
            return
        try:
            self.script.exports_sync.resetall()
            self.gravity_var.set("1.0")
            self.jump_slider.set(1.0)
            self.jump_value_label.configure(text="当前: 1.00x")
            self.gravity_scale = 1.0
            self.jump_scale = 1.0
            self.air_jump_var.set(0)
            self.air_move_var.set(0)
            self.log("✓ 已重置")
        except Exception as e:
            self.log("重置失败: " + str(e))

    def log(self, msg, level="info"):
        t = datetime.now().strftime("%H:%M:%S")
        entry = "[" + t + "] " + msg + "\n"
        self.log_text.configure(state="normal")
        self.log_text.insert("end", entry)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def on_closing(self):
        if self.script:
            try: self.script.unload()
            except: pass
        if self.session:
            try: self.session.detach()
            except: pass
        self.destroy()


if __name__ == "__main__":
    app = GravityModifierApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
