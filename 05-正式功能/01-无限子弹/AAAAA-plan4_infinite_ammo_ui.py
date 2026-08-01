# AAAAA-plan4_infinite_ammo_ui.py - 无限子弹 UI
# 原理：Interceptor.replace ConsumeAmmo → 仅本地玩家返回 true
# 零性能开销、无状态、无需缓存指针、不怕切房间
# 注意：换弹动画不会触发（弹药永远不变空）

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
JS_FILE = os.path.join(BASE_DIR, "AAAAA_plan4_replace_consume.js")

COLOR_GREEN = "#2ecc71"
COLOR_RED = "#e74c3c"
COLOR_ORANGE = "#f39c12"
COLOR_BLUE = "#3498db"
COLOR_DARK = "#1a1a2e"
COLOR_DARKER = "#16213e"


class InfiniteAmmoApp(ctk.CTk):
    """无限子弹 - Python CustomTkinter 可视化界面"""

    def __init__(self):
        super().__init__()

        self.title("无限子弹 v1.0 (Interceptor.replace)")
        self.geometry("500x620")
        self.minsize(460, 540)
        self.resizable(True, True)

        # Frida 连接相关
        self.session = None
        self.script = None
        self.device = None
        self.is_connected = False
        self._cleanup_done = False
        self._connecting = False

        # 功能开关状态
        self._ammo_enabled = False

        self.setup_ui()
        self.after(800, self._auto_connect_thread)

    # ==================== UI 构建 ====================

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # ---- 标题 ----
        ctk.CTkLabel(
            self, text="\U0001f52b 无限子弹",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, pady=(16, 2), padx=20, sticky="ew")

        ctk.CTkLabel(
            self, text="Interceptor.replace ConsumeAmmo | 仅本地玩家 | RPG/AT4 全覆盖",
            font=ctk.CTkFont(size=12), text_color="#888"
        ).grid(row=1, column=0, pady=(0, 8), padx=20, sticky="ew")

        # ---- 状态栏 ----
        status_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_DARK)
        status_frame.grid(row=2, column=0, padx=16, pady=4, sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)

        self.status_dot = ctk.CTkLabel(status_frame, text="\u26ab", font=ctk.CTkFont(size=18))
        self.status_dot.grid(row=0, column=0, padx=(12, 4), pady=8)

        self.status_label = ctk.CTkLabel(status_frame, text="等待游戏启动...", font=ctk.CTkFont(size=14))
        self.status_label.grid(row=0, column=1, padx=4, pady=8, sticky="w")

        self.pid_label = ctk.CTkLabel(status_frame, text="", font=ctk.CTkFont(size=11), text_color="#888")
        self.pid_label.grid(row=0, column=2, padx=12, pady=8, sticky="e")

        # ---- 控制面板 ----
        ctrl_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_DARKER)
        ctrl_frame.grid(row=3, column=0, padx=16, pady=4, sticky="ew")
        ctrl_frame.grid_columnconfigure(1, weight=1)

        # 无限子弹开关
        ctk.CTkLabel(ctrl_frame, text="无限子弹开关",
                      font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, padx=(12, 4), pady=(12, 4), sticky="w")

        self.ammo_toggle = ctk.CTkSwitch(
            ctrl_frame, text="关闭", font=ctk.CTkFont(size=13),
            command=self.on_toggle_ammo, progress_color=COLOR_GREEN,
            switch_width=50, switch_height=24
        )
        self.ammo_toggle.grid(row=0, column=1, padx=4, pady=(12, 4), sticky="w")
        self.ammo_toggle.configure(state="disabled")

        # 提示文字
        ctk.CTkLabel(ctrl_frame, text="注意：开启后换弹动画不会触发（弹药永远不变空）",
                      font=ctk.CTkFont(size=11), text_color="#666").grid(
            row=1, column=0, columnspan=2, padx=12, pady=(0, 12), sticky="w")

        # ---- 信息面板 ----
        info_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_DARK)
        info_frame.grid(row=4, column=0, padx=16, pady=4, sticky="ew")
        info_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(info_frame, text="功能状态", font=ctk.CTkFont(size=10), text_color="#888").grid(
            row=0, column=0, padx=6, pady=(6, 0))
        self.state_label = ctk.CTkLabel(info_frame, text="\u274c 关闭",
                                         font=ctk.CTkFont(size=14, weight="bold"))
        self.state_label.grid(row=1, column=0, padx=6, pady=(0, 4))

        ctk.CTkLabel(info_frame, text="Gun Hook", font=ctk.CTkFont(size=10), text_color="#888").grid(
            row=0, column=1, padx=6, pady=(6, 0))
        self.gun_hook_label = ctk.CTkLabel(info_frame, text="\u26ab 未安装",
                                            font=ctk.CTkFont(size=14, weight="bold"))
        self.gun_hook_label.grid(row=1, column=1, padx=6, pady=(0, 4))

        ctk.CTkLabel(info_frame, text="RPG Hook", font=ctk.CTkFont(size=10), text_color="#888").grid(
            row=0, column=2, padx=6, pady=(6, 0))
        self.rpg_hook_label = ctk.CTkLabel(info_frame, text="\u26ab 未安装",
                                            font=ctk.CTkFont(size=14, weight="bold"))
        self.rpg_hook_label.grid(row=1, column=2, padx=6, pady=(0, 4))

        ctk.CTkLabel(info_frame, text="方案说明",
                      font=ctk.CTkFont(size=10), text_color="#888").grid(
            row=2, column=0, columnspan=3, padx=6, pady=(6, 0))
        self.desc_label = ctk.CTkLabel(
            info_frame,
            text="Plan4: Interceptor.replace | 零性能开销 | 不怕切房间",
            font=ctk.CTkFont(size=11))
        self.desc_label.grid(row=3, column=0, columnspan=3, padx=6, pady=(0, 4))

        # ---- 日志 ----
        log_frame = ctk.CTkFrame(self, corner_radius=8)
        log_frame.grid(row=5, column=0, padx=16, pady=(8, 12), sticky="nsew")
        log_frame.grid_rowconfigure(1, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        log_header = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_header.grid(row=0, column=0, padx=8, pady=(6, 2), sticky="ew")

        ctk.CTkLabel(log_header, text="\U0001f4dd 运行日志",
                      font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")

        self.clear_log_btn = ctk.CTkButton(
            log_header, text="清空", width=50, height=22,
            font=ctk.CTkFont(size=10), fg_color="#444", hover_color="#555",
            command=self.on_clear_log
        )
        self.clear_log_btn.pack(side="right")

        self.log_text = ctk.CTkTextbox(
            log_frame, font=ctk.CTkFont(size=11, family="Consolas"),
            fg_color="#0a0a0a", text_color="#e0e0e0", corner_radius=6
        )
        self.log_text.grid(row=1, column=0, padx=8, pady=(0, 8), sticky="nsew")
        self._log_counter = 0

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
                if proc.info['name'] and 'unitycrossfire' in proc.info['name'].lower():
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

            self._safe_config(self.status_dot, text="\U0001f7e2", text_color=COLOR_GREEN)
            self._safe_config(self.status_label, text="已连接 - UnityCrossFire.exe")
            self._safe_config(self.pid_label, text="PID: " + str(pid))
            self._safe_log("Frida 脚本已加载，无限子弹模块待命！")
            self.after(0, self._enable_controls)

        except frida.ProcessNotFoundError:
            self._safe_log("游戏进程已退出")
            self._connecting = False
        except frida.ServerNotStartedError:
            self._safe_log("Frida Server 未运行，请启动 frida-server")
            self._connecting = False
        except Exception as e:
            self._safe_log("连接异常: " + str(e))
            self._connecting = False

    def disconnect_from_game(self):
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
        self._ammo_enabled = False
        self._safe_config(self.status_dot, text="\u26ab", text_color="#888")
        self._safe_config(self.status_label, text="已断开")
        self._safe_config(self.pid_label, text="")
        self.after(0, self._disable_controls)
        self._safe_log("已断开连接")

    # ==================== 控件状态 ====================

    def _enable_controls(self):
        self.ammo_toggle.configure(state="normal")

    def _disable_controls(self):
        self.ammo_toggle.configure(state="disabled")
        self.ammo_toggle.deselect()
        self.ammo_toggle.configure(text="关闭")
        self.state_label.configure(text="\u274c 关闭", text_color=COLOR_RED)
        self.gun_hook_label.configure(text="\u26ab 未安装", text_color="#888")
        self.rpg_hook_label.configure(text="\u26ab 未安装", text_color="#888")

    # ==================== 操作回调 ====================

    def on_toggle_ammo(self):
        if not self.is_connected or not self.script:
            self.ammo_toggle.deselect()
            return
        state = self.ammo_toggle.get()
        if state:
            self.ammo_toggle.configure(text="开启")
            self._ammo_enabled = True
            self.state_label.configure(text="\u2705 开启", text_color=COLOR_GREEN)
            self._safe_log("无限子弹已开启 (Interceptor.replace 已生效)")
        else:
            self.ammo_toggle.configure(text="关闭")
            self._ammo_enabled = False
            self.state_label.configure(text="\u274c 关闭", text_color=COLOR_RED)
            self._safe_log("无限子弹已关闭")

    def on_clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        self._log_counter = 0

    # ==================== JS 消息 ====================

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

                elif ptype == "status":
                    feat = payload.get("feature", "")
                    en = payload.get("enabled", False)
                    self._safe_log("[状态] " + feat + " -> " + ("开" if en else "关"))
                else:
                    self._safe_log("[JS] " + str(payload))
            else:
                self._safe_log("[JS] " + str(payload))
        elif message["type"] == "error":
            self._safe_log("[JS错误] " + message.get("description", ""))

    # ==================== 线程安全工具 ====================

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

    # ==================== 清理 ====================

    def on_closing(self):
        if self._cleanup_done:
            return
        self._cleanup_done = True

        self._safe_log("正在清理资源...")

        if self.script:
            try:
                self.script.unload()
                self._safe_log("JS 脚本已卸载")
            except:
                pass
            self.script = None

        if self.session:
            try:
                self.session.detach()
                self._safe_log("Frida 已断开")
            except:
                pass
            self.session = None

        self.is_connected = False
        self.destroy()


if __name__ == "__main__":
    app = InfiniteAmmoApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
