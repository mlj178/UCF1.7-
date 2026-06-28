# AAAAA-fast_gunstock_ui.py - 极速枪托 CustomTkinter UI
#
# 作用：自动连接 UnityCrossFire.exe，加载 AAAAA-fast_gunstock_min.js，
#      用开关和倍率滑块调用 JS 的 enable/disable/setmultiplier/status/cleanup。

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
JS_FILE = os.path.join(BASE_DIR, "AAAAA-fast_gunstock_min.js")
GAME_PROCESS_NAME = "UnityCrossFire.exe"

COLOR_GREEN = "#2ecc71"
COLOR_RED = "#e74c3c"
COLOR_ORANGE = "#f39c12"
COLOR_DARK = "#1a1a2e"
COLOR_DARKER = "#16213e"


class FastGunstockApp(ctk.CTk):
    """极速枪托单功能 UI。"""

    def __init__(self):
        super().__init__()

        self.title("极速枪托")
        self.geometry("580x660")
        self.minsize(520, 560)
        self.resizable(True, True)

        self.session = None
        self.script = None
        self.is_connected = False
        self._connecting = False
        self._cleanup_done = False
        self._polling = False
        self._log_counter = 0

        self.game_state = {
            "enabled": False,
            "initialized": False,
            "hooksInstalled": False,
            "multiplier": 4.0,
            "specialHits": 0,
            "attackDataHits": 0,
            "damageEventHits": 0,
            "knifeExitHits": 0,
            "speedSetCount": 0,
            "skippedNoGunstock": 0,
            "skippedLocked": 0,
            "lastError": None,
        }
        self._state_lock = threading.Lock()

        self.setup_ui()
        self.after(800, self._auto_connect_thread)

    # ==================== UI ====================

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(
            self,
            text="极速枪托",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=18, pady=(16, 2), sticky="ew")

        ctk.CTkLabel(
            self,
            text="加快 WPN_Gun 右键枪托/刺刀近战动作，不改普通射击",
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

        ctk.CTkLabel(
            ctrl_frame,
            text="功能开关",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, padx=(12, 6), pady=(12, 6), sticky="w")

        self.feature_switch = ctk.CTkSwitch(
            ctrl_frame,
            text="关闭",
            font=ctk.CTkFont(size=13),
            command=self.on_toggle_feature,
            progress_color=COLOR_GREEN,
            switch_width=50,
            switch_height=24,
        )
        self.feature_switch.grid(row=0, column=1, padx=4, pady=(12, 6), sticky="w")
        self.feature_switch.configure(state="disabled")

        ctk.CTkLabel(ctrl_frame, text="动作倍率", font=ctk.CTkFont(size=13)).grid(
            row=1, column=0, padx=(12, 6), pady=(6, 12), sticky="w"
        )

        self.multiplier_slider = ctk.CTkSlider(
            ctrl_frame,
            from_=1.0,
            to=30.0,
            number_of_steps=29,
            command=self.on_multiplier_change,
        )
        self.multiplier_slider.set(4.0)
        self.multiplier_slider.grid(row=1, column=1, padx=4, pady=(6, 12), sticky="ew")
        self.multiplier_slider.configure(state="disabled")

        self.multiplier_label = ctk.CTkLabel(
            ctrl_frame,
            text="4x",
            width=44,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#aaa",
        )
        self.multiplier_label.grid(row=1, column=2, padx=(6, 12), pady=(6, 12))

        info_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_DARK)
        info_frame.grid(row=4, column=0, padx=16, pady=4, sticky="ew")
        info_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.enabled_label = self._add_info_cell(info_frame, 0, "功能状态", "关闭")
        self.hook_label = self._add_info_cell(info_frame, 1, "Hook 状态", "未安装")
        self.multiplier_info_label = self._add_info_cell(info_frame, 2, "当前倍率", "4x")

        self.count_label = ctk.CTkLabel(
            info_frame,
            text="右键: 0 / 伤害: 0 / 退出: 0 / 解锁: 0 / 锁中跳过: 0",
            font=ctk.CTkFont(size=11),
            text_color="#aaa",
        )
        self.count_label.grid(row=2, column=0, columnspan=3, padx=8, pady=(4, 8), sticky="ew")

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

        self.log_text = ctk.CTkTextbox(
            log_frame,
            font=ctk.CTkFont(size=11, family="Consolas"),
            fg_color="#0a0a0a",
            text_color="#e0e0e0",
            corner_radius=6,
        )
        self.log_text.grid(row=1, column=0, padx=8, pady=(0, 8), sticky="nsew")

    def _add_info_cell(self, parent, column, title, value):
        ctk.CTkLabel(parent, text=title, font=ctk.CTkFont(size=10), text_color="#888").grid(
            row=0, column=column, padx=6, pady=(8, 0)
        )
        label = ctk.CTkLabel(parent, text=value, font=ctk.CTkFont(size=13, weight="bold"))
        label.grid(row=1, column=column, padx=6, pady=(0, 4))
        return label

    # ==================== 自动连接 ====================

    def _auto_connect_thread(self):
        threading.Thread(target=self._auto_connect_loop, daemon=True).start()

    def _auto_connect_loop(self):
        while not self._cleanup_done:
            if self.is_connected or self._connecting:
                time.sleep(2)
                continue

            pid = self._find_pid()
            if pid:
                self._do_connect(pid)
            time.sleep(3)

    def _find_pid(self):
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                name = proc.info.get("name") or ""
                if name.lower() == GAME_PROCESS_NAME.lower():
                    return proc.info["pid"]
            except Exception:
                pass
        return None

    def _do_connect(self, pid):
        if self._connecting:
            return
        self._connecting = True
        self._safe_log("检测到游戏 PID: " + str(pid) + "，正在连接...")

        try:
            self.session = frida.attach(pid)
            self._safe_log("Frida 已附加，正在加载脚本...")

            if not os.path.exists(JS_FILE):
                self._safe_log("JS 文件不存在: " + JS_FILE)
                self._connecting = False
                return

            with open(JS_FILE, "r", encoding="utf-8") as f:
                js_code = f.read()

            self.script = self.session.create_script(js_code)
            self.script.on("message", self.on_message)
            self.script.load()

            self.is_connected = True
            self._connecting = False
            self._safe_config(self.status_dot, text_color=COLOR_GREEN)
            self._safe_config(self.status_label, text="已连接 - " + GAME_PROCESS_NAME)
            self._safe_config(self.pid_label, text="PID: " + str(pid))
            self.after(0, self._enable_controls)
            self._safe_log("脚本已加载，打开开关即可启用极速枪托")
            self._apply_multiplier_async()
            self._start_status_polling()

        except frida.ProcessNotFoundError:
            self._safe_log("游戏进程已退出")
            self._connecting = False
        except frida.ServerNotStartedError:
            self._safe_log("Frida Server 未运行，请启动 frida-server")
            self._connecting = False
        except Exception as exc:
            self._safe_log("连接异常: " + str(exc))
            self._connecting = False

    # ==================== 控件回调 ====================

    def _enable_controls(self):
        self.feature_switch.configure(state="normal")
        self.multiplier_slider.configure(state="normal")

    def _disable_controls(self):
        self.feature_switch.configure(state="disabled")
        self.feature_switch.deselect()
        self.feature_switch.configure(text="关闭")
        self.multiplier_slider.configure(state="disabled")

    def on_toggle_feature(self):
        if not self.is_connected or not self.script:
            self.feature_switch.deselect()
            return

        if self.feature_switch.get():
            self.feature_switch.configure(text="开启")
            threading.Thread(target=self._do_enable, daemon=True).start()
        else:
            self.feature_switch.configure(text="关闭")
            threading.Thread(target=self._do_disable, daemon=True).start()

    def on_multiplier_change(self, value):
        multiplier = int(round(float(value)))
        self.multiplier_label.configure(text=str(multiplier) + "x")
        self.multiplier_info_label.configure(text=str(multiplier) + "x")
        if self.is_connected and self.script:
            self._apply_multiplier_async()

    def _apply_multiplier_async(self):
        threading.Thread(target=self._do_set_multiplier, daemon=True).start()

    def _do_set_multiplier(self):
        try:
            multiplier = int(round(float(self.multiplier_slider.get())))
            ok = self.script.exports_sync.setmultiplier(multiplier)
            if ok:
                self._safe_log("倍率已设置为 " + str(multiplier) + "x")
        except Exception as exc:
            self._safe_log("设置倍率失败: " + str(exc))

    def _do_enable(self):
        try:
            self.script.exports_sync.setmultiplier(int(round(float(self.multiplier_slider.get()))))
            ok = self.script.exports_sync.enable()
            self._safe_log("enable() 返回: " + str(ok))
        except Exception as exc:
            self._safe_log("开启失败: " + str(exc))
            self.after(0, self.feature_switch.deselect)

    def _do_disable(self):
        try:
            ok = self.script.exports_sync.disable()
            self._safe_log("disable() 返回: " + str(ok))
        except Exception as exc:
            self._safe_log("关闭失败: " + str(exc))

    # ==================== 状态轮询 ====================

    def _start_status_polling(self):
        self._polling = True
        threading.Thread(target=self._poll_loop, daemon=True).start()

    def _stop_status_polling(self):
        self._polling = False

    def _poll_loop(self):
        while self._polling and self.is_connected and self.script:
            try:
                status = self.script.exports_sync.status()
                if isinstance(status, dict):
                    with self._state_lock:
                        self.game_state.update(status)
                    self.after(0, self._update_info_display)
            except frida.InvalidOperationError:
                self._safe_log("脚本已失效")
                self._do_disconnect()
                return
            except Exception:
                pass
            time.sleep(0.5)

    def _update_info_display(self):
        with self._state_lock:
            enabled = self.game_state.get("enabled", False)
            hooks = self.game_state.get("hooksInstalled", False)
            multiplier = self.game_state.get("multiplier", 8.0)
            special_hits = self.game_state.get("specialHits", 0)
            damage_hits = self.game_state.get("damageEventHits", 0)
            exit_hits = self.game_state.get("knifeExitHits", 0)
            skipped_locked = self.game_state.get("skippedLocked", 0)

        if enabled:
            self.enabled_label.configure(text="开启", text_color=COLOR_GREEN)
        else:
            self.enabled_label.configure(text="关闭", text_color=COLOR_RED)

        if hooks:
            self.hook_label.configure(text="已安装", text_color=COLOR_GREEN)
        else:
            self.hook_label.configure(text="未安装", text_color=COLOR_ORANGE)

        self.multiplier_info_label.configure(text=str(round(float(multiplier), 1)) + "x")
        self.count_label.configure(
            text=(
                "右键: " + str(special_hits)
                + " / 伤害: " + str(damage_hits)
                + " / 退出: " + str(exit_hits)
                + " / 锁中跳过: " + str(skipped_locked)
            )
        )

    # ==================== 断开与清理 ====================

    def _do_disconnect(self):
        self._stop_status_polling()
        if self.script:
            try:
                self.script.exports_sync.cleanup()
            except Exception:
                pass
            try:
                self.script.unload()
            except Exception:
                pass
            self.script = None

        if self.session:
            try:
                self.session.detach()
            except Exception:
                pass
            self.session = None

        self.is_connected = False
        self._safe_config(self.status_dot, text_color="#888")
        self._safe_config(self.status_label, text="已断开")
        self._safe_config(self.pid_label, text="")
        self.after(0, self._disable_controls)
        self._safe_log("已断开连接")

    def on_closing(self):
        if self._cleanup_done:
            return
        self._cleanup_done = True
        self._do_disconnect()
        self.destroy()

    # ==================== JS 消息与日志 ====================

    def on_message(self, message, data):
        if message.get("type") == "send":
            payload = message.get("payload")
            if isinstance(payload, dict) and payload.get("type") == "log":
                level = payload.get("level", "info")
                module = payload.get("module", "")
                msg = payload.get("message", "")
                self._safe_log("[" + level + "][" + module + "] " + msg)
            else:
                self._safe_log("[JS] " + str(payload))
        elif message.get("type") == "error":
            self._safe_log("[JS错误] " + message.get("description", str(message)))

    def clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        self._log_counter = 0

    def _safe_log(self, msg):
        self.after(0, self._do_log, msg)

    def _do_log(self, msg):
        self._log_counter += 1
        entry = "[" + datetime.now().strftime("%H:%M:%S") + "] " + msg + "\n"
        self.log_text.configure(state="normal")
        self.log_text.insert("end", entry)
        self.log_text.see("end")
        if self._log_counter > 500:
            self.log_text.delete("1.0", "2.0")
        self.log_text.configure(state="disabled")

    def _safe_config(self, widget, **kwargs):
        self.after(0, lambda: widget.configure(**kwargs))


if __name__ == "__main__":
    app = FastGunstockApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
