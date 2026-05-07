# AAA-skip_round_ui.py - 回合跳过器 UI
# 原理：将 ModeBase.restGameTime 设为 0:00，所有模式时间耗尽触发原生结束流程
# 适用：全模式通用（生化 / 团队 / 个人 / 特殊战）

import customtkinter as ctk
import frida
import json
import threading
import time
import os
import sys
from datetime import datetime

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

JS_FILE = os.path.join(os.path.dirname(__file__), "skip_round.js")

COLOR_GREEN = "#2ecc71"
COLOR_RED = "#e74c3c"
COLOR_ORANGE = "#f39c12"
COLOR_BLUE = "#3498db"
COLOR_DARK = "#1a1a2e"
COLOR_DARKER = "#16213e"


class SkipRoundApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("回合跳过器 v1.0")
        self.geometry("550x650")
        self.minsize(500, 550)
        self.resizable(True, True)

        self.session = None
        self.script = None
        self.device = None
        self.is_connected = False
        self._cleanup_done = False

        self._gs_lock = threading.Lock()
        self.game_state = {
            "skip_count": 0,
            "current_round": 0,
            "round_active": False,
            "rest_game_time": "--:--",
            "rpc_ready": False
        }

        self.setup_ui()
        self.after(800, self._auto_connect_thread)

    # ==================== UI ====================

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(
            self, text="\u23f0 回合跳过器",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, pady=(16, 2), padx=20, sticky="ew")

        ctk.CTkLabel(
            self, text="全模式通用 | 生化 / 团队 / 个人 / 特殊战",
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

        # ---- 信息面板 ----
        info_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_DARKER)
        info_frame.grid(row=3, column=0, padx=16, pady=4, sticky="ew")
        info_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(info_frame, text="当前回合", font=ctk.CTkFont(size=10), text_color="#888").grid(
            row=0, column=0, padx=6, pady=(6, 0))
        self.round_label = ctk.CTkLabel(info_frame, text="--", font=ctk.CTkFont(size=13, weight="bold"))
        self.round_label.grid(row=1, column=0, padx=6, pady=(0, 4))

        ctk.CTkLabel(info_frame, text="剩余时间", font=ctk.CTkFont(size=10), text_color="#888").grid(
            row=0, column=1, padx=6, pady=(6, 0))
        self.time_label = ctk.CTkLabel(info_frame, text="--:--", font=ctk.CTkFont(size=13, weight="bold"))
        self.time_label.grid(row=1, column=1, padx=6, pady=(0, 4))

        ctk.CTkLabel(info_frame, text="已跳过", font=ctk.CTkFont(size=10), text_color="#888").grid(
            row=0, column=2, padx=6, pady=(6, 0))
        self.skip_count_label = ctk.CTkLabel(info_frame, text="0", font=ctk.CTkFont(size=13, weight="bold"))
        self.skip_count_label.grid(row=1, column=2, padx=6, pady=(0, 4))

        # ---- 按钮 ----
        btn_frame = ctk.CTkFrame(self, corner_radius=8, fg_color="transparent")
        btn_frame.grid(row=4, column=0, padx=16, pady=(8, 2), sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        self.skip_btn = ctk.CTkButton(
            btn_frame, text="\u25b6 跳过当前回合",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=COLOR_GREEN, hover_color="#27ae60",
            height=52, corner_radius=10,
            command=self.on_skip_round,
            state="disabled"
        )
        self.skip_btn.grid(row=0, column=0, columnspan=2, padx=4, pady=4, sticky="ew")

        # ---- 日志 ----
        log_frame = ctk.CTkFrame(self, corner_radius=8)
        log_frame.grid(row=6, column=0, padx=16, pady=(4, 12), sticky="nsew")
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

    # ==================== 连接 ====================

    def _auto_connect_thread(self):
        threading.Thread(target=self.connect_to_game, daemon=True).start()

    def connect_to_game(self):
        if self.is_connected:
            return
        try:
            self._safe_log("正在扫描游戏进程...")
            self.device = frida.get_local_device()
            target_process = None
            for proc in self.device.enumerate_processes():
                pname = proc.name.lower()
                if "unity" in pname or "crossfire" in pname or "cross fire" in pname.lower():
                    target_process = proc
                    break
            if not target_process:
                self._safe_log("未找到游戏进程 (Unity/CrossFire)")
                return
            self._safe_log("进程: " + target_process.name + " (PID: " + str(target_process.pid) + ")")
            self.session = self.device.attach(target_process.pid)
            self._safe_log("Frida 已附加")
            if not os.path.exists(JS_FILE):
                self._safe_log("JS 文件不存在: " + JS_FILE)
                return
            with open(JS_FILE, "r", encoding="utf-8") as f:
                js_code = f.read()
            self.script = self.session.create_script(js_code)
            self.script.on("message", self.on_message)
            self.script.load()
            self.is_connected = True
            self._safe_config(self.status_dot, text="\U0001f7e2", text_color=COLOR_GREEN)
            self._safe_config(self.status_label, text="已连接 - " + target_process.name)
            self._safe_config(self.pid_label, text="PID: " + str(target_process.pid))
            self._safe_log("Frida 脚本已加载，正在安装 Hook...")
            result = self.script.exports_sync.install()
            self._safe_log("install() 返回: " + json.dumps(result))
            if result.get("ok"):
                self._safe_config(self.skip_btn, state="normal")
                self._safe_log("所有 Hook 已安装，就绪！")
                self._start_status_polling()
            else:
                self._safe_log("Hook 安装失败: " + result.get("error", "未知错误"))
        except frida.ProcessNotFoundError:
            self._safe_log("游戏进程未运行")
        except frida.ServerNotStartedError:
            self._safe_log("Frida Server 未运行")
        except Exception as e:
            self._safe_log("连接异常: " + str(e))

    def disconnect_from_game(self):
        self._stop_status_polling()
        if self.script:
            try: self.script.unload()
            except: pass
            self.script = None
        if self.session:
            try: self.session.detach()
            except: pass
            self.session = None
        self.is_connected = False
        self._safe_config(self.status_dot, text="\u26ab", text_color="#888")
        self._safe_config(self.status_label, text="已断开")
        self._safe_config(self.pid_label, text="")
        self._safe_config(self.skip_btn, state="disabled")
        self._safe_log("已断开连接")

    # ==================== 轮询 ====================

    def _polling_active(self):
        return hasattr(self, "_polling") and self._polling

    def _start_status_polling(self):
        self._polling = True
        threading.Thread(target=self._poll_loop, daemon=True).start()

    def _stop_status_polling(self):
        self._polling = False

    def _poll_loop(self):
        while self._polling_active() and self.is_connected and self.script:
            try:
                status = self.script.exports_sync.getstatus()
                if status.get("ok"):
                    with self._gs_lock:
                        self.game_state["skip_count"] = status.get("skipCount", 0)
                        self.game_state["current_round"] = status.get("currentRound", 0)
                        self.game_state["round_active"] = status.get("roundActive", False)
                        self.game_state["rest_game_time"] = status.get("restGameTime", "--:--")
                        self.game_state["rpc_ready"] = status.get("rpcReady", False)
                    self._update_info_display()
            except Exception as e:
                pass
            time.sleep(0.5)

    def _update_info_display(self):
        self.after(0, self._do_update_info)

    def _do_update_info(self):
        with self._gs_lock:
            rnd = self.game_state["current_round"]
            cnt = self.game_state["skip_count"]
            ttxt = self.game_state["rest_game_time"] or "--:--"
            active = self.game_state["round_active"]
        self.round_label.configure(text=str(rnd))
        self.skip_count_label.configure(text=str(cnt))
        self.time_label.configure(text=ttxt)
        if active:
            self.skip_btn.configure(fg_color=COLOR_GREEN, hover_color="#27ae60", state="normal")
        else:
            self.skip_btn.configure(fg_color="#555", hover_color="#666", state="disabled")

    # ==================== 操作 ====================

    def on_skip_round(self):
        if not self.is_connected or not self.script:
            self._safe_log("未连接游戏")
            return
        self.skip_btn.configure(text="\u23f3 跳转中...", state="disabled")
        self._safe_log("正在跳过当前回合...")
        threading.Thread(target=self._do_skip_round, daemon=True).start()

    def _do_skip_round(self):
        try:
            result = self.script.exports_sync.skipround()
            ok = result.get("ok", False)
            reason = result.get("reason", "")
            self.after(0, self._on_skip_result, ok, reason)
        except Exception as e:
            self.after(0, self._on_skip_result, False, str(e))

    def _on_skip_result(self, ok, reason):
        if ok:
            self._safe_log("跳过成功！回合将立即结束")
        else:
            msg_map = {
                "guard_active": "上一跳进行中，请稍后",
                "already_zero": "回合已结束",
                "no_instance": "未检测到游戏实例",
                "read_failed": "读取状态失败",
                "write_failed": "写入失败"
            }
            self._safe_log(msg_map.get(reason, reason or "未知"))
        self.skip_btn.configure(text="\u25b6 跳过当前回合", state="normal")

    def on_clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        self._log_counter = 0

    # ==================== 消息 ====================

    def on_message(self, message, data):
        if message["type"] == "send":
            payload = message["payload"]
            if isinstance(payload, dict):
                msg_type = payload.get("type", "")
                msg_text = payload.get("message", str(payload))
                if msg_type == "round_skipped":
                    from_val = payload.get("from", "?")
                    count = payload.get("count", 0)
                    self._safe_log("[跳过] " + str(from_val) + " -> 0:00 (总计:" + str(count) + ")")
                    with self._gs_lock:
                        self.game_state["skip_count"] = count
                elif msg_type == "round_end":
                    self._safe_log("[回合] 回合结束")
                elif msg_type == "timeout":
                    self._safe_log("[时间] 计时器归零")
                elif msg_type == "error":
                    self._safe_log("[错误] " + msg_text)
                elif msg_type == "warn":
                    self._safe_log("[警告] " + msg_text)
                elif msg_type == "status":
                    self._safe_log("[状态] " + msg_text)
                else:
                    self._safe_log("[JS] " + str(payload))
            else:
                self._safe_log("[JS] " + str(payload))
        elif message["type"] == "error":
            self._safe_log("[JS错误] " + message.get("description", ""))

    # ==================== 工具 ====================

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

    def on_closing(self):
        if self._cleanup_done:
            return
        self._cleanup_done = True
        self._stop_status_polling()
        if self.script:
            try: self.script.unload()
            except: pass
        if self.session:
            try: self.session.detach()
            except: pass
        self.destroy()


if __name__ == "__main__":
    app = SkipRoundApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
