# AAAAA-bot_pause_ui.py - Bot pause CustomTkinter UI
#
# Connects to UnityCrossFire.exe, loads AAAAA-bot_pause_min.js,
# and toggles Bot.stopAllBot through enable/disable/status/cleanup.

import customtkinter as ctk
import frida
import psutil
import threading
import time
import os
from datetime import datetime


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "AAAAA-bot_pause_min.js")
GAME_PROCESS_NAME = "UnityCrossFire.exe"

COLOR_GREEN = "#2ecc71"
COLOR_RED = "#e74c3c"
COLOR_ORANGE = "#f39c12"
COLOR_DARK = "#1a1a2e"
COLOR_DARKER = "#16213e"


class BotPauseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("人机暂停")
        self.geometry("560x560")
        self.minsize(500, 480)

        self.session = None
        self.script = None
        self.is_connected = False
        self._connecting = False
        self._cleanup_done = False
        self._polling = False
        self.game_state = {
            "enabled": False,
            "paused": False,
            "currentValue": -1,
            "writeCount": 0,
            "lastError": None,
        }
        self._state_lock = threading.Lock()

        self.setup_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(800, self._auto_connect_thread)

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(
            self,
            text="人机暂停",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=18, pady=(16, 2), sticky="ew")

        ctk.CTkLabel(
            self,
            text="写入 Bot.stopAllBot 静态字段，暂停或恢复所有人机",
            font=ctk.CTkFont(size=12),
            text_color="#888",
        ).grid(row=1, column=0, padx=18, pady=(0, 8), sticky="ew")

        status_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_DARK)
        status_frame.grid(row=2, column=0, padx=16, pady=4, sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)

        self.status_dot = ctk.CTkLabel(status_frame, text="●", font=ctk.CTkFont(size=18), text_color="#888")
        self.status_dot.grid(row=0, column=0, padx=(12, 4), pady=8)

        self.status_label = ctk.CTkLabel(status_frame, text="等待游戏启动...", font=ctk.CTkFont(size=14))
        self.status_label.grid(row=0, column=1, padx=4, pady=8, sticky="w")

        self.pid_label = ctk.CTkLabel(status_frame, text="", font=ctk.CTkFont(size=11), text_color="#888")
        self.pid_label.grid(row=0, column=2, padx=12, pady=8, sticky="e")

        ctrl_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_DARKER)
        ctrl_frame.grid(row=3, column=0, padx=16, pady=4, sticky="ew")
        ctrl_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(ctrl_frame, text="功能开关", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, padx=(12, 6), pady=12, sticky="w"
        )

        self.feature_switch = ctk.CTkSwitch(
            ctrl_frame,
            text="恢复",
            font=ctk.CTkFont(size=13),
            command=self.on_toggle_feature,
            progress_color=COLOR_GREEN,
            switch_width=50,
            switch_height=24,
        )
        self.feature_switch.grid(row=0, column=1, padx=4, pady=12, sticky="w")
        self.feature_switch.configure(state="disabled")

        info_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_DARK)
        info_frame.grid(row=4, column=0, padx=16, pady=4, sticky="ew")
        info_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.enabled_label = self._add_info_cell(info_frame, 0, "功能状态", "关闭")
        self.paused_label = self._add_info_cell(info_frame, 1, "人机状态", "未知")
        self.write_label = self._add_info_cell(info_frame, 2, "写入次数", "0")

        log_frame = ctk.CTkFrame(self, corner_radius=8)
        log_frame.grid(row=5, column=0, padx=16, pady=(8, 12), sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)

        log_header = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_header.grid(row=0, column=0, padx=8, pady=(6, 2), sticky="ew")

        ctk.CTkLabel(log_header, text="运行日志", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
        ctk.CTkButton(
            log_header,
            text="清空",
            width=50,
            height=22,
            font=ctk.CTkFont(size=10),
            fg_color="#444",
            hover_color="#555",
            command=self.clear_log,
        ).pack(side="right")

        self.log_text = ctk.CTkTextbox(log_frame, font=ctk.CTkFont(size=11))
        self.log_text.grid(row=1, column=0, padx=8, pady=(2, 8), sticky="nsew")
        self.log_text.configure(state="disabled")

    def _add_info_cell(self, parent, column, title, value):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=column, padx=8, pady=8, sticky="ew")
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=11), text_color="#888").pack()
        label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=15, weight="bold"))
        label.pack(pady=(2, 0))
        return label

    def log(self, message):
        now = datetime.now().strftime("%H:%M:%S")
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{now}] {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def find_game_pid(self):
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info["name"] == GAME_PROCESS_NAME:
                    return proc.info["pid"]
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return None

    def _auto_connect_thread(self):
        if self._connecting or self.is_connected or self._cleanup_done:
            return
        self._connecting = True
        threading.Thread(target=self._connect_worker, daemon=True).start()

    def _connect_worker(self):
        try:
            while not self._cleanup_done and not self.is_connected:
                pid = self.find_game_pid()
                if pid is None:
                    self.after(0, lambda: self._set_connection_status(False, "等待游戏启动...", ""))
                    time.sleep(1.5)
                    continue

                self.after(0, lambda pid=pid: self._set_connection_status(False, "正在连接游戏...", f"PID {pid}"))
                self.session = frida.attach(pid)

                with open(JS_FILE, "r", encoding="utf-8") as f:
                    js_code = f.read()

                self.script = self.session.create_script(js_code)
                self.script.on("message", self.on_frida_message)
                self.script.load()
                self.is_connected = True
                self.after(0, lambda pid=pid: self._on_connected(pid))
                return
        except Exception as exc:
            self.after(0, lambda exc=exc: self.log(f"连接失败：{exc}"))
            self.after(2000, self._auto_connect_thread)
        finally:
            self._connecting = False

    def _set_connection_status(self, connected, text, pid_text):
        self.status_dot.configure(text_color=COLOR_GREEN if connected else "#888")
        self.status_label.configure(text=text)
        self.pid_label.configure(text=pid_text)

    def _on_connected(self, pid):
        self._set_connection_status(True, "已连接游戏", f"PID {pid}")
        self.feature_switch.configure(state="normal")
        self.log("脚本已加载")
        self._start_polling()

    def on_frida_message(self, message, data):
        if message.get("type") == "send":
            payload = message.get("payload", {})
            if payload.get("type") == "log":
                self.after(0, lambda: self.log(payload.get("message", "")))
        elif message.get("type") == "error":
            self.after(0, lambda: self.log(str(message)))

    def on_toggle_feature(self):
        if not self.script:
            return
        try:
            if self.feature_switch.get() == 1:
                result = self.script.exports_sync.enable()
                self.feature_switch.configure(text="暂停")
            else:
                result = self.script.exports_sync.disable()
                self.feature_switch.configure(text="恢复")
            self.log(result.get("msg", str(result)))
            self.refresh_status()
        except Exception as exc:
            self.log(f"切换失败：{exc}")

    def _start_polling(self):
        if self._polling:
            return
        self._polling = True
        self.after(500, self._poll_status)

    def _poll_status(self):
        if self._cleanup_done:
            return
        self.refresh_status()
        self.after(1000, self._poll_status)

    def refresh_status(self):
        if not self.script:
            return
        try:
            status = self.script.exports_sync.status()
            with self._state_lock:
                self.game_state.update(status)
            self._render_state()
        except Exception as exc:
            self.log(f"状态读取失败：{exc}")

    def _render_state(self):
        paused = bool(self.game_state.get("paused"))
        enabled = bool(self.game_state.get("enabled"))
        write_count = self.game_state.get("writeCount", 0)

        self.enabled_label.configure(text="开启" if enabled else "关闭", text_color=COLOR_GREEN if enabled else "#ccc")
        self.paused_label.configure(text="暂停" if paused else "恢复", text_color=COLOR_ORANGE if paused else COLOR_GREEN)
        self.write_label.configure(text=str(write_count))

    def on_close(self):
        if self._cleanup_done:
            self.destroy()
            return
        self._cleanup_done = True
        try:
            if self.script:
                self.script.exports_sync.cleanup()
        except Exception:
            pass
        try:
            if self.session:
                self.session.detach()
        except Exception:
            pass
        self.destroy()


if __name__ == "__main__":
    app = BotPauseApp()
    app.mainloop()
