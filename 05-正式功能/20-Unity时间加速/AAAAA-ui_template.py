# ============================================================
# Unity时间加速 - CustomTkinter UI
#
# 功能：滑块控制时间倍速 + 锁定开关 + 预设按钮
# ============================================================

import customtkinter as ctk
import frida
import psutil
import threading
import time
import os
import sys
from datetime import datetime

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "AAAAA-game_template.js")

COLOR_GREEN = "#2ecc71"
COLOR_RED = "#e74c3c"
COLOR_ORANGE = "#f39c12"
COLOR_BLUE = "#3498db"
COLOR_DARK = "#1a1a2e"
COLOR_DARKER = "#16213e"

GAME_PROCESS_NAME = "UnityCrossFire.exe"


class GameFeatureUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Unity时间加速")
        self.geometry("700x500")
        self.minsize(600, 420)
        self.resizable(True, True)

        self.session = None
        self.script = None
        self.device = None
        self.is_connected = False
        self._cleanup_done = False
        self._connecting = False

        self._gs_lock = threading.Lock()
        self._locked = False

        self.setup_ui()
        self.after(800, self._auto_connect_thread)

    # ==================== UI ====================

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 标题
        ctk.CTkLabel(
            self, text="Unity 时间加速",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, pady=(15, 5), padx=20, sticky="w")

        # 状态栏
        status_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_DARK)
        status_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)

        self.status_dot = ctk.CTkLabel(status_frame, text="⚫", font=ctk.CTkFont(size=18))
        self.status_dot.grid(row=0, column=0, padx=(12, 4), pady=8)

        self.status_label = ctk.CTkLabel(status_frame, text="等待游戏启动...", font=ctk.CTkFont(size=13))
        self.status_label.grid(row=0, column=1, padx=4, pady=8, sticky="w")

        self.pid_label = ctk.CTkLabel(status_frame, text="", font=ctk.CTkFont(size=11), text_color="#888")
        self.pid_label.grid(row=0, column=2, padx=12, pady=8, sticky="e")

        self.connect_btn = ctk.CTkButton(
            status_frame, text="连接", width=80,
            command=self.toggle_connect
        )
        self.connect_btn.grid(row=0, column=3, padx=10, pady=8)

        # 日志区
        log_frame = ctk.CTkFrame(self, corner_radius=8)
        log_frame.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)

        log_header = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_header.grid(row=0, column=0, padx=8, pady=(6, 2), sticky="ew")

        ctk.CTkLabel(log_header, text="日志", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left")

        ctk.CTkButton(
            log_header, text="清空", width=50, height=22,
            font=ctk.CTkFont(size=10), fg_color="#444", hover_color="#555",
            command=self.clear_log
        ).pack(side="right")

        self.log_text = ctk.CTkTextbox(
            log_frame, font=ctk.CTkFont(size=11, family="Consolas"),
            fg_color="#0a0a0a", text_color="#e0e0e0", corner_radius=6
        )
        self.log_text.grid(row=1, column=0, padx=8, pady=(0, 8), sticky="nsew")
        self._log_counter = 0

        # 控制区
        ctrl_frame = ctk.CTkFrame(self, fg_color="transparent")
        ctrl_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        ctrl_frame.grid_columnconfigure(1, weight=1)

        # 锁定开关
        self.lock_btn = ctk.CTkButton(
            ctrl_frame, text="锁定", width=80, height=35,
            fg_color="#444", hover_color="#555",
            command=self.toggle_lock
        )
        self.lock_btn.grid(row=0, column=0, padx=(0, 10))

        # 滑块
        self.scale_label = ctk.CTkLabel(
            ctrl_frame, text="1.0x", font=ctk.CTkFont(size=16, weight="bold"),
            width=60
        )
        self.scale_label.grid(row=0, column=2, padx=(10, 5))

        self.time_slider = ctk.CTkSlider(
            ctrl_frame, from_=0.1, to=10.0, number_of_steps=99,
            command=self.on_slider_change
        )
        self.time_slider.grid(row=0, column=1, sticky="ew", padx=5)
        self.time_slider.set(1.0)

        # 预设按钮
        preset_frame = ctk.CTkFrame(ctrl_frame, fg_color="transparent")
        preset_frame.grid(row=1, column=0, columnspan=3, pady=(8, 0), sticky="ew")

        for label, val in [("1x", 1.0), ("2x", 2.0), ("3x", 3.0), ("5x", 5.0), ("10x", 10.0)]:
            ctk.CTkButton(
                preset_frame, text=label, width=55, height=28,
                font=ctk.CTkFont(size=11),
                fg_color="#333", hover_color="#555",
                command=lambda v=val: self.apply_preset(v)
            ).pack(side="left", padx=3)

        # 当前倍速显示
        self.current_scale_label = ctk.CTkLabel(
            preset_frame, text="当前: --", font=ctk.CTkFont(size=11), text_color="#888"
        )
        self.current_scale_label.pack(side="right", padx=5)

    # ==================== 滑块/预设回调 ====================

    def on_slider_change(self, value):
        scale = round(value, 1)
        self.scale_label.configure(text=str(scale) + "x")
        if self._locked and self.is_connected and self.script:
            threading.Thread(target=self._do_lock, args=(scale,), daemon=True).start()
        elif self.is_connected and self.script:
            threading.Thread(target=self._do_set, args=(scale,), daemon=True).start()

    def apply_preset(self, value):
        self.time_slider.set(value)
        self.scale_label.configure(text=str(value) + "x")
        if self._locked and self.is_connected and self.script:
            threading.Thread(target=self._do_lock, args=(value,), daemon=True).start()
        elif self.is_connected and self.script:
            threading.Thread(target=self._do_set, args=(value,), daemon=True).start()

    def toggle_lock(self):
        if not self.is_connected or not self.script:
            self._safe_log("未连接到游戏")
            return
        self._locked = not self._locked
        if self._locked:
            scale = round(self.time_slider.get(), 1)
            self.lock_btn.configure(text="解锁", fg_color=COLOR_ORANGE, hover_color="#d68910")
            threading.Thread(target=self._do_lock, args=(scale,), daemon=True).start()
        else:
            self.lock_btn.configure(text="锁定", fg_color="#444", hover_color="#555")
            threading.Thread(target=self._do_unlock, daemon=True).start()

    # ==================== Frida调用 ====================

    def _do_set(self, scale):
        try:
            ok = self.script.exports.set_time_scale(scale)
            if ok:
                self._safe_log("倍速设为 " + str(scale) + "x")
        except frida.InvalidOperationError:
            self._safe_log("脚本已失效")
            self._do_disconnect()
        except Exception as e:
            self._safe_log("设置失败: " + str(e))

    def _do_lock(self, scale):
        try:
            self.script.exports.lock_time_scale(scale)
            self._safe_log("锁定倍速: " + str(scale) + "x")
        except frida.InvalidOperationError:
            self._safe_log("脚本已失效")
            self._do_disconnect()
        except Exception as e:
            self._safe_log("锁定失败: " + str(e))

    def _do_unlock(self):
        try:
            self.script.exports.unlock_time_scale()
            self._safe_log("已恢复正常速度")
        except frida.InvalidOperationError:
            self._safe_log("脚本已失效")
            self._do_disconnect()
        except Exception as e:
            self._safe_log("解锁失败: " + str(e))

    # ==================== 自动连接 ====================

    def _auto_connect_thread(self):
        threading.Thread(target=self._auto_connect_loop, daemon=True).start()

    def _auto_connect_loop(self):
        while not self._cleanup_done:
            if self.is_connected:
                time.sleep(5)
                continue
            if self._connecting:
                time.sleep(2)
                continue
            pid = self._find_pid()
            if pid:
                self._do_connect(pid)
            time.sleep(3)

    def _find_pid(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == GAME_PROCESS_NAME.lower():
                    return proc.info['pid']
            except:
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

            self._safe_config(self.status_dot, text="🟢", text_color=COLOR_GREEN)
            self._safe_config(self.status_label, text="已连接 - " + GAME_PROCESS_NAME)
            self._safe_config(self.pid_label, text="PID: " + str(pid))
            self._safe_config(self.connect_btn, text="断开")
            self._safe_log("Frida 脚本已加载，已就绪！")

            # 读取当前倍速
            self._refresh_current_scale()

        except frida.ProcessNotFoundError:
            self._safe_log("游戏进程已退出")
            self._connecting = False
        except frida.ServerNotStartedError:
            self._safe_log("Frida Server 未运行，请启动 frida-server")
            self._connecting = False
        except Exception as e:
            self._safe_log("连接异常: " + str(e))
            self._connecting = False

    def _refresh_current_scale(self):
        if not self.is_connected or not self.script:
            return
        try:
            scale = self.script.exports.get_time_scale()
            if scale is not None:
                self._safe_config(self.current_scale_label, text="当前: " + str(round(scale, 2)) + "x")
        except:
            pass

    def toggle_connect(self):
        if self.is_connected:
            threading.Thread(target=self._do_disconnect, daemon=True).start()
        else:
            pid = self._find_pid()
            if pid:
                threading.Thread(target=self._do_connect, args=(pid,), daemon=True).start()
            else:
                self._safe_log("未找到游戏进程: " + GAME_PROCESS_NAME)

    def _do_disconnect(self):
        # 断开前恢复速度
        if self.script and self._locked:
            try:
                self.script.exports.unlock_time_scale()
            except:
                pass
            self._locked = False
            self._safe_config(self.lock_btn, text="锁定", fg_color="#444", hover_color="#555")

        if self.script:
            try:
                self.script.unload()
            except:
                pass
            self.script = None
        if self.session:
            try:
                self.session.detach()
            except:
                pass
            self.session = None
        self.is_connected = False
        self._safe_config(self.status_dot, text="⚫", text_color="#888")
        self._safe_config(self.status_label, text="已断开")
        self._safe_config(self.pid_label, text="")
        self._safe_config(self.connect_btn, text="连接")
        self._safe_config(self.current_scale_label, text="当前: --")
        self._safe_log("已断开连接")

    # ==================== JS消息处理 ====================

    def on_message(self, message, data):
        if message["type"] == "send":
            payload = message["payload"]
            if isinstance(payload, dict):
                ptype = payload.get("type", "")
                plevel = payload.get("level", "info")
                pmodule = payload.get("module", "")
                pmsg = payload.get("message", str(payload))

                if ptype == "log":
                    prefix = ""
                    if plevel == "success":
                        prefix = "[OK]"
                    elif plevel == "error":
                        prefix = "[错误]"
                    elif plevel == "warn":
                        prefix = "[警告]"
                    else:
                        prefix = "[" + pmodule + "]"
                    self._safe_log(prefix + " " + pmsg)
                else:
                    self._safe_log("[JS] " + str(payload))
            else:
                self._safe_log("[JS] " + str(payload))
        elif message["type"] == "error":
            self._safe_log("[JS错误] " + message.get("description", ""))

    # ==================== 线程安全UI更新 ====================

    def _safe_log(self, msg):
        self.after(0, self._do_log, msg)

    def _do_log(self, msg):
        self._log_counter += 1
        t = datetime.now().strftime("%H:%M:%S")
        entry = "[" + t + "] " + msg + "\n"
        self.log_text.configure(state="normal")
        self.log_text.insert("end", entry)
        self.log_text.see("end")
        if self._log_counter > 500:
            self.log_text.delete("1.0", "2.0")
        self.log_text.configure(state="disabled")

    def _safe_config(self, widget, **kw):
        self.after(0, lambda: widget.configure(**kw))

    def clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        self._log_counter = 0

    # ==================== 清理 ====================

    def on_closing(self):
        if self._cleanup_done:
            return
        self._cleanup_done = True
        # 恢复正常速度
        if self.script and self._locked:
            try:
                self.script.exports.unlock_time_scale()
            except:
                pass
        if self.script:
            try:
                self.script.unload()
            except:
                pass
            self.script = None
        if self.session:
            try:
                self.session.detach()
            except:
                pass
            self.session = None
        self.is_connected = False
        self.destroy()


if __name__ == "__main__":
    app = GameFeatureUI()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
