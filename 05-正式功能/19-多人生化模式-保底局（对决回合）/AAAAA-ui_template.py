# ============================================================
# AAAAA-ui_template.py - CustomTkinter UI模板
#
# 功能：Frida注入 + 日志显示 + 功能控制
# 特点：
#   - CustomTkinter现代化UI
#   - 后台线程自动连接游戏进程（不阻塞UI）
#   - 所有Frida操作在后台线程执行
#   - 所有UI更新通过self.after()调度到主线程
#   - 日志显示系统（线程安全）
#   - 完善的清理机制
#
# 使用方法：
#   1. 修改游戏进程名称（默认：UnityCrossFire.exe）
#   2. 修改JS脚本路径
#   3. 添加自定义UI控件
#   4. 添加功能调用方法
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

        self.title("游戏功能修改器 - 模板")
        self.geometry("700x550")
        self.minsize(600, 450)
        self.resizable(True, True)

        self.session = None
        self.script = None
        self.device = None
        self.is_connected = False
        self._cleanup_done = False
        self._connecting = False

        self._gs_lock = threading.Lock()

        self.setup_ui()
        self.after(800, self._auto_connect_thread)

    # ==================== UI ====================

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self, text="🎮 游戏功能修改器",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, pady=(15, 5), padx=20, sticky="w")

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

        log_frame = ctk.CTkFrame(self, corner_radius=8)
        log_frame.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)

        log_header = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_header.grid(row=0, column=0, padx=8, pady=(6, 2), sticky="ew")

        ctk.CTkLabel(log_header, text="📋 日志", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left")

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

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.nickname_btn = ctk.CTkButton(
            btn_frame, text="📝 获取昵称",
            command=self.get_nickname, width=120, height=35
        )
        self.nickname_btn.pack(side="left", padx=5)

        self.instance_btn = ctk.CTkButton(
            btn_frame, text="🔍 获取实例",
            command=self.get_instances, width=120, height=35
        )
        self.instance_btn.pack(side="left", padx=5)

    # ==================== 自动连接（后台线程） ====================

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
            self._safe_log("✅ Frida 脚本已加载，已就绪！")

        except frida.ProcessNotFoundError:
            self._safe_log("游戏进程已退出")
            self._connecting = False
        except frida.ServerNotStartedError:
            self._safe_log("Frida Server 未运行，请启动 frida-server")
            self._connecting = False
        except Exception as e:
            self._safe_log("连接异常: " + str(e))
            self._connecting = False

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
        self._safe_log("已断开连接")

    # ==================== 功能调用（后台线程） ====================

    def get_nickname(self):
        if not self.is_connected or not self.script:
            self._safe_log("未连接到游戏")
            return
        self._safe_log("正在获取玩家昵称...")
        threading.Thread(target=self._do_get_nickname, daemon=True).start()

    def _do_get_nickname(self):
        try:
            nickname = self.script.exports.get_nickname()
            if nickname:
                self._safe_log("✅ 玩家昵称: " + nickname)
            else:
                self._safe_log("获取昵称失败（可能未进入游戏）")
        except frida.InvalidOperationError:
            self._safe_log("脚本已失效，请重新连接")
            self._do_disconnect()
        except Exception as e:
            self._safe_log("获取昵称失败: " + str(e))

    def get_instances(self):
        if not self.is_connected or not self.script:
            self._safe_log("未连接到游戏")
            return
        self._safe_log("正在获取实例地址...")
        threading.Thread(target=self._do_get_instances, daemon=True).start()

    def _do_get_instances(self):
        try:
            instances = self.script.exports.get_player_instances()
            if instances:
                self._safe_log("✅ myPlayer: " + str(instances.get("myPlayer", "null")))
                self._safe_log("✅ clientData: " + str(instances.get("clientData", "null")))
            else:
                self._safe_log("获取实例地址失败")
        except frida.InvalidOperationError:
            self._safe_log("脚本已失效，请重新连接")
            self._do_disconnect()
        except Exception as e:
            self._safe_log("获取实例地址失败: " + str(e))

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
        self._safe_log("正在清理资源...")
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
