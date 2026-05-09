# AAA-aim_assist_ui.py - 自瞄辅助器 UI（v1.1 距离最近方案）
# 原理：直接读内存选距离最近敌人 → 计算角度 → 写入 cameraRotation
# 触发：鼠标左键按下 (Input.GetMouseButton)
# 适用：全模式通用（团队 / 个人 / 生化 / 特殊战）

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

# 固定路径：脚本和 UI 在同一目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "aimbot_v1_dll_approach.js")

COLOR_GREEN = "#2ecc71"
COLOR_RED = "#e74c3c"
COLOR_ORANGE = "#f39c12"
COLOR_BLUE = "#3498db"
COLOR_DARK = "#1a1a2e"
COLOR_DARKER = "#16213e"


class AimAssistApp(ctk.CTk):
    """自瞄辅助器 - Python CustomTkinter 可视化界面"""

    def __init__(self):
        super().__init__()

        self.title("自瞄辅助器 v1.1 (DLL方案)")
        self.geometry("580x720")
        self.minsize(520, 620)
        self.resizable(True, True)

        # Frida 连接相关
        self.session = None
        self.script = None
        self.device = None
        self.is_connected = False
        self._cleanup_done = False
        self._connecting = False

        # 状态数据（线程安全）
        self._gs_lock = threading.Lock()
        self.game_state = {
            "enabled": False,
            "target_info": "无",
            "smoothness": 0.3,
            "aim_bone": "chest",
        }

        # 构建 UI
        self.setup_ui()

        # 延迟启动自动连接
        self.after(800, self._auto_connect_thread)

    # ==================== UI 构建 ====================

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        # ---- 标题 ----
        ctk.CTkLabel(
            self, text="\U0001f3af 自瞄辅助器",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, pady=(16, 2), padx=20, sticky="ew")

        ctk.CTkLabel(
            self, text="角度方案 | AddCameraRotation | DLL逆向还原 v1",
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

        # 自瞄开关
        ctk.CTkLabel(ctrl_frame, text="自瞄开关",
                      font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, padx=(12, 4), pady=(12, 4), sticky="w")

        self.aim_toggle = ctk.CTkSwitch(
            ctrl_frame, text="关闭", font=ctk.CTkFont(size=13),
            command=self.on_toggle_aim, progress_color=COLOR_GREEN,
            switch_width=50, switch_height=24
        )
        self.aim_toggle.grid(row=0, column=1, padx=4, pady=(12, 4), sticky="w")
        self.aim_toggle.configure(state="disabled")

        # 平滑度
        ctk.CTkLabel(ctrl_frame, text="平滑度",
                      font=ctk.CTkFont(size=13)).grid(
            row=1, column=0, padx=(12, 4), pady=4, sticky="w")

        self.smoothness_slider = ctk.CTkSlider(
            ctrl_frame, from_=0.05, to=1.0, number_of_steps=95,
            command=self.on_smoothness_change
        )
        self.smoothness_slider.set(0.3)
        self.smoothness_slider.grid(row=1, column=1, padx=4, pady=4, sticky="ew")
        self.smoothness_slider.configure(state="disabled")

        self.smoothness_label = ctk.CTkLabel(ctrl_frame, text="0.30",
                                              font=ctk.CTkFont(size=12), text_color="#aaa")
        self.smoothness_label.grid(row=1, column=2, padx=(4, 12), pady=4)

        # 瞄准部位
        ctk.CTkLabel(ctrl_frame, text="瞄准部位",
                      font=ctk.CTkFont(size=13)).grid(
            row=2, column=0, padx=(12, 4), pady=(4, 12), sticky="w")

        self.bone_var = ctk.StringVar(value="chest")
        self.bone_menu = ctk.CTkOptionMenu(
            ctrl_frame, values=["chest", "head"],
            command=self.on_bone_change, font=ctk.CTkFont(size=12)
        )
        self.bone_menu.grid(row=2, column=1, padx=4, pady=(4, 12), sticky="w")
        self.bone_menu.configure(state="disabled")

        # ---- 信息面板 ----
        info_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_DARK)
        info_frame.grid(row=4, column=0, padx=16, pady=4, sticky="ew")
        info_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(info_frame, text="自瞄状态", font=ctk.CTkFont(size=10), text_color="#888").grid(
            row=0, column=0, padx=6, pady=(6, 0))
        self.state_label = ctk.CTkLabel(info_frame, text="\u274c 关闭",
                                         font=ctk.CTkFont(size=13, weight="bold"))
        self.state_label.grid(row=1, column=0, padx=6, pady=(0, 4))

        ctk.CTkLabel(info_frame, text="当前目标", font=ctk.CTkFont(size=10), text_color="#888").grid(
            row=0, column=1, padx=6, pady=(6, 0))
        self.target_label = ctk.CTkLabel(info_frame, text="无",
                                         font=ctk.CTkFont(size=13, weight="bold"))
        self.target_label.grid(row=1, column=1, padx=6, pady=(0, 4))

        # ---- 日志 ----
        log_frame = ctk.CTkFrame(self, corner_radius=8)
        log_frame.grid(row=6, column=0, padx=16, pady=(8, 12), sticky="nsew")
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

    # ==================== 自动连接机制 ====================

    def _auto_connect_thread(self):
        """后台线程：自动检测游戏进程并连接"""
        threading.Thread(target=self._auto_connect_loop, daemon=True).start()

    def _auto_connect_loop(self):
        """持续检测 UnityCrossFire.exe 进程，发现后自动连接"""
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
        """通过 psutil 查找 UnityCrossFire.exe 进程 PID"""
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and 'unitycrossfire' in proc.info['name'].lower():
                    return proc.info['pid']
            except:
                pass
        return None

    def _do_connect(self, pid):
        """连接到指定 PID 的游戏进程"""
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

            # 更新 UI
            self._safe_config(self.status_dot, text="\U0001f7e2", text_color=COLOR_GREEN)
            self._safe_config(self.status_label, text="已连接 - UnityCrossFire.exe")
            self._safe_config(self.pid_label, text="PID: " + str(pid))
            self._safe_log("Frida 脚本已加载，已就绪！")
            self.after(0, self._enable_controls)
            self._safe_log("自瞄模块待命，开启开关即可使用")

            # 启动状态轮询
            self._start_status_polling()

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
        """主动断开连接"""
        self._stop_status_polling()
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
        self._safe_config(self.status_dot, text="\u26ab", text_color="#888")
        self._safe_config(self.status_label, text="已断开")
        self._safe_config(self.pid_label, text="")
        self.after(0, self._disable_controls)
        self._safe_log("已断开连接")

    # ==================== 控件状态切换 ====================

    def _enable_controls(self):
        self.aim_toggle.configure(state="normal")
        self.smoothness_slider.configure(state="normal")
        self.bone_menu.configure(state="normal")

    def _disable_controls(self):
        self.aim_toggle.configure(state="disabled")
        self.aim_toggle.deselect()
        self.aim_toggle.configure(text="关闭")
        self.smoothness_slider.configure(state="disabled")
        self.bone_menu.configure(state="disabled")

    # ==================== 操作回调 ====================

    def on_toggle_aim(self):
        if not self.is_connected or not self.script:
            self.aim_toggle.deselect()
            return
        state = self.aim_toggle.get()
        if state:
            self.aim_toggle.configure(text="开启")
            threading.Thread(target=self._do_enable, daemon=True).start()
        else:
            self.aim_toggle.configure(text="关闭")
            threading.Thread(target=self._do_disable, daemon=True).start()

    def on_smoothness_change(self, value):
        val = round(value, 2)
        self.smoothness_label.configure(text="{:.2f}".format(val))
        if self.is_connected and self.script:
            threading.Thread(target=self._do_update_config, daemon=True).start()

    def on_bone_change(self, choice):
        if self.is_connected and self.script:
            threading.Thread(target=self._do_update_config, daemon=True).start()

    def on_clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        self._log_counter = 0

    # ==================== Frida 操作（后台线程） ====================

    def _do_enable(self):
        try:
            self.script.exports.aim_enable()
            self._safe_log("自瞄已开启")
        except Exception as e:
            self._safe_log("开启失败: " + str(e))
            self.after(0, lambda: self.aim_toggle.deselect())

    def _do_disable(self):
        try:
            self.script.exports.aim_disable()
            self._safe_log("自瞄已关闭")
        except Exception as e:
            self._safe_log("关闭失败: " + str(e))

    def _do_update_config(self):
        try:
            smooth = round(self.smoothness_slider.get(), 2)
            bone_name = self.bone_var.get()
            bone_index = 7 if bone_name == "chest" else 0
            cfg = json.dumps({"smoothness": smooth, "aimBone": bone_index})
            self.script.exports.aim_set_config(cfg)
        except Exception as e:
            pass

    # ==================== 状态轮询机制 ====================

    def _polling_active(self):
        return hasattr(self, "_polling") and self._polling

    def _start_status_polling(self):
        self._polling = True
        threading.Thread(target=self._poll_loop, daemon=True).start()

    def _stop_status_polling(self):
        self._polling = False

    def _poll_loop(self):
        """后台轮询：每 0.5 秒调用 JS 的 aimGetStatus() 获取最新状态"""
        while self._polling_active() and self.is_connected and self.script:
            try:
                raw = self.script.exports.aim_get_status()
                status = json.loads(raw)
                with self._gs_lock:
                    self.game_state["enabled"] = status.get("enabled", False)
                    t = status.get("targetEnemy", None)
                    self.game_state["target_info"] = t if t else "无"
                    self.game_state["smoothness"] = status.get("smoothness", 0.3)
                    bone_idx = status.get("aimBone", 7)
                    self.game_state["aim_bone"] = "chest" if bone_idx == 7 else "head"
                self._update_info_display()
            except Exception:
                pass
            time.sleep(0.5)

    def _update_info_display(self):
        self.after(0, self._do_update_info)

    def _do_update_info(self):
        with self._gs_lock:
            en = self.game_state["enabled"]
            target = self.game_state["target_info"]

        if en:
            self.state_label.configure(text="\u2705 开启", text_color=COLOR_GREEN)
        else:
            self.state_label.configure(text="\u274c 关闭", text_color=COLOR_RED)

        if target and target != "无":
            self.target_label.configure(text=target[-12:] if len(target) > 12 else target)
        else:
            self.target_label.configure(text="无")

    # ==================== JS 消息接收 ====================

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

    # ==================== 线程安全 UI 更新工具 ====================

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

    # ==================== 清理机制 ====================

    def on_closing(self):
        """窗口关闭时的清理：停止轮询 → 卸载脚本 → 断开连接 → 销毁窗口"""
        if self._cleanup_done:
            return
        self._cleanup_done = True

        self._safe_log("正在清理资源...")
        self._stop_status_polling()

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
    app = AimAssistApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
