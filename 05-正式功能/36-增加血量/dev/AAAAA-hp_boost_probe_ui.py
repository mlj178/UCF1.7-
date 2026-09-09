"""增加血量 探测 UI（临时调试用，位于 dev/）

- 自动连接 UnityCrossFire.exe，加载同目录 AAAAA-hp_boost_probe.js
- 三种探测：只读快照 / Heal 探测 / AddHealthMax 探测
- 所有日志持久化到 dev/logs/hp_boost_probe_YYYYMMDD_HHMMSS.log，方便发给别人分析
"""

import os
import queue
import threading
import time
from datetime import datetime

import customtkinter as ctk
import frida
import psutil


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "AAAAA-hp_boost_probe.js")
LOG_DIR = os.path.join(BASE_DIR, "logs")
GAME_PROCESS_NAME = "UnityCrossFire.exe"

GREEN = "#2ecc71"
ORANGE = "#f39c12"
RED = "#e74c3c"
PANEL = "#1d2430"
PANEL_DARK = "#161c26"


class HpBoostProbeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("增加血量 - 探测工具")
        self.geometry("680x640")
        self.minsize(560, 560)

        self.session = None
        self.script = None
        self.connected = False
        self.connecting = False
        self.closing = False
        self.rpc_busy = False
        self.status_busy = False
        self.shutdown_done = False

        self.amount = 10

        self.rpc_lock = threading.Lock()
        self.ui_queue = queue.Queue()

        # 日志文件（启动即创建）
        os.makedirs(LOG_DIR, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(LOG_DIR, f"hp_boost_probe_{stamp}.log")
        self._log_file = open(self.log_path, "a", encoding="utf-8")
        self._file_lock = threading.Lock()

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._drain_ui_queue)
        self.after(600, self._schedule_connect)

        self._log(f"日志文件: {self.log_path}")
        self._log(f"探测脚本: {JS_FILE}")

    # ==================== 持久化日志 ====================

    def _log(self, text, write_file=True):
        """写入 UI 日志框 + 持久化文件。必须在 UI 线程调用。"""
        stamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        line = f"[{stamp}] {text}"
        try:
            self.log_box.configure(state="normal")
            self.log_box.insert("end", line + "\n")
            self.log_box.see("end")
            if float(self.log_box.index("end-1c").split(".")[0]) > 800:
                self.log_box.delete("1.0", "200.0")
            self.log_box.configure(state="disabled")
        except Exception:
            pass
        if write_file:
            try:
                with self._file_lock:
                    self._log_file.write(line + "\n")
                    self._log_file.flush()
            except Exception:
                pass

    # ==================== UI 构建 ====================

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(self, text="增加血量 探测工具", font=ctk.CTkFont(size=22, weight="bold")).grid(
            row=0, column=0, padx=18, pady=(16, 2), sticky="ew")
        ctk.CTkLabel(
            self, text="验证 Heal 封顶问题 / AddHealthMax 是否生效 | 日志已持久化",
            text_color="#8f98a8", font=ctk.CTkFont(size=12),
        ).grid(row=1, column=0, padx=18, pady=(0, 6), sticky="ew")

        # 连接状态
        status = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        status.grid(row=2, column=0, padx=18, pady=5, sticky="ew")
        status.grid_columnconfigure(1, weight=1)

        self.status_dot = ctk.CTkLabel(status, text="●", text_color="#777")
        self.status_dot.grid(row=0, column=0, padx=(12, 5), pady=8)
        self.connection_label = ctk.CTkLabel(status, text="等待游戏启动...")
        self.connection_label.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        self.pid_label = ctk.CTkLabel(status, text="", text_color="#999")
        self.pid_label.grid(row=0, column=2, padx=12, pady=8)

        # 控制面板
        controls = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL_DARK)
        controls.grid(row=3, column=0, padx=18, pady=5, sticky="ew")
        controls.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            controls, text="探测数值(+N)", font=ctk.CTkFont(size=12, weight="bold"),
        ).grid(row=0, column=0, columnspan=3, padx=12, pady=(8, 0), sticky="w")

        slider_row = ctk.CTkFrame(controls, fg_color="transparent")
        slider_row.grid(row=1, column=0, columnspan=3, padx=12, pady=(2, 4), sticky="ew")
        slider_row.grid_columnconfigure(0, weight=1)

        self.amount_slider = ctk.CTkSlider(
            slider_row, from_=1, to=100, number_of_steps=99, command=self._on_slider_change)
        self.amount_slider.set(self.amount)
        self.amount_slider.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.amount_label = ctk.CTkLabel(
            slider_row, text=str(self.amount), width=44,
            font=ctk.CTkFont(size=14, weight="bold"))
        self.amount_label.grid(row=0, column=1, sticky="e")

        self.btn_readonly = ctk.CTkButton(
            controls, text="① 只读快照\n(不写入)", height=48,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#4b5563", hover_color="#374151",
            command=lambda: self._run_probe("readonly"))
        self.btn_readonly.grid(row=2, column=0, padx=6, pady=6, sticky="ew")

        self.btn_heal = ctk.CTkButton(
            controls, text="② Heal 探测\n(测试封顶)", height=48,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#2563eb", hover_color="#1d4ed8",
            command=lambda: self._run_probe("heal"))
        self.btn_heal.grid(row=2, column=1, padx=6, pady=6, sticky="ew")

        self.btn_addmax = ctk.CTkButton(
            controls, text="③ AddHealthMax 探测\n(测试加上限)", height=48,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#16a34a", hover_color="#15803d",
            command=lambda: self._run_probe("addmax"))
        self.btn_addmax.grid(row=2, column=2, padx=6, pady=6, sticky="ew")

        # 状态指标
        metrics = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        metrics.grid(row=4, column=0, padx=18, pady=5, sticky="ew")
        metrics.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.phase_label = self._add_metric(metrics, 0, "探测阶段", "idle")
        self.rate_label = self._add_metric(metrics, 1, "血量比例 rate", "-")
        self.maxhp_label = self._add_metric(metrics, 2, "isMaxHP", "-")
        self.error_label = self._add_metric(metrics, 3, "错误", "0")

        # 日志
        log_header = ctk.CTkFrame(self, fg_color="transparent")
        log_header.grid(row=5, column=0, padx=18, pady=(6, 0), sticky="ew")
        ctk.CTkLabel(log_header, text="探测日志（已写入文件）", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        ctk.CTkLabel(
            log_header, text=os.path.basename(self.log_path),
            text_color="#6b7280", font=ctk.CTkFont(size=11)).pack(side="right")

        self.log_box = ctk.CTkTextbox(self, font=ctk.CTkFont(size=11, family="Consolas"))
        self.log_box.grid(row=6, column=0, padx=18, pady=(2, 14), sticky="nsew")
        self.log_box.configure(state="disabled")
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(5, weight=0)

        self._set_controls_enabled(False)

    def _add_metric(self, parent, column, title, value):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=column, padx=8, pady=8, sticky="ew")
        ctk.CTkLabel(frame, text=title, text_color="#8f98a8", font=ctk.CTkFont(size=11)).pack()
        label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(pady=(2, 0))
        return label

    # ==================== UI 事件队列 ====================

    def _post(self, event, *args):
        if not self.closing:
            self.ui_queue.put((event, args))

    def _post_allow_closing(self, event, *args):
        self.ui_queue.put((event, args))
        try:
            self.after(0, self._drain_ui_queue)
        except Exception:
            pass

    def _drain_ui_queue(self):
        try:
            while True:
                event, args = self.ui_queue.get_nowait()
                self._handle_event(event, *args)
        except queue.Empty:
            pass
        if not self.closing:
            self.after(100, self._drain_ui_queue)

    def _handle_event(self, event, *args):
        if event == "log":
            self._log(args[0])
        elif event == "waiting":
            self._set_connection(False, args[0], args[1] if len(args) > 1 else "")
        elif event == "connected":
            self._on_connected(args[0])
        elif event == "detached":
            self._on_detached(args[0])
        elif event == "retry_connect":
            self.after(800, self._schedule_connect)
        elif event == "rpc_done":
            self.rpc_busy = False
            self._render_status(args[0])
            self._set_controls_enabled(self.connected)
        elif event == "rpc_error":
            self.rpc_busy = False
            self._log("操作失败：" + str(args[0]))
            self._set_controls_enabled(self.connected)
        elif event == "status":
            self._render_status(args[0])
        elif event == "destroy":
            self.destroy()

    def _set_connection(self, connected, text, pid_text=""):
        self.status_dot.configure(text_color=GREEN if connected else "#777")
        self.connection_label.configure(text=text)
        self.pid_label.configure(text=pid_text)

    def _set_controls_enabled(self, enabled):
        state = "normal" if enabled and not self.rpc_busy else "disabled"
        self.btn_readonly.configure(state=state)
        self.btn_heal.configure(state=state)
        self.btn_addmax.configure(state=state)
        self.amount_slider.configure(state=state)

    # ==================== 连接 ====================

    @staticmethod
    def _find_game_pid():
        target = GAME_PROCESS_NAME.lower()
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if (proc.info.get("name") or "").lower() == target:
                    return proc.info["pid"]
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    def _schedule_connect(self):
        if self.closing or self.connected or self.connecting:
            return
        self.connecting = True
        threading.Thread(target=self._connect_worker, daemon=True).start()

    def _connect_worker(self):
        try:
            pid = self._find_game_pid()
            if not pid:
                self.connecting = False
                self._post("waiting", "等待 UnityCrossFire.exe", "")
                self._post("retry_connect")
                return

            self._post("waiting", "正在注入探测脚本...", f"PID {pid}")
            session = frida.attach(pid)
            with open(JS_FILE, "r", encoding="utf-8") as fp:
                source = fp.read()
            script = session.create_script(source)
            script.on("message", self._on_frida_message)
            session.on("detached", self._on_session_detached)
            script.load()

            self.session = session
            self.script = script
            self.connected = True
            self.connecting = False
            self._post("connected", pid)
        except Exception as exc:
            self.connecting = False
            self.connected = False
            self._post("waiting", "连接失败，等待重试", "")
            self._post("log", "连接异常：" + str(exc))
            self._post("retry_connect")

    def _on_connected(self, pid):
        self._set_connection(True, "已连接游戏", f"PID {pid}")
        self._set_controls_enabled(True)
        self._log("探测脚本已加载，自动开启探测模式...")
        # 自动 enable（探测工具默认开启）
        self._rpc_call("enable", {"amount": self.amount})
        self._schedule_status_poll()

    def _on_session_detached(self, reason):
        self._post("detached", reason)

    def _on_detached(self, reason):
        self.connected = False
        self.script = None
        self.session = None
        self._set_connection(False, f"连接断开：{reason}", "")
        self._set_controls_enabled(False)
        if not self.closing:
            self._post("retry_connect")

    def _on_frida_message(self, message, data):
        # JS 的 send() 日志
        if message.get("type") == "send":
            payload = message.get("payload", {})
            if isinstance(payload, dict) and payload.get("type") == "log":
                level = payload.get("level", "info")
                text = payload.get("message", "")
                prefix = {"error": "[JS错误]", "warn": "[JS警告]"}.get(level, "[JS]")
                self._post("log", f"{prefix} {text}")
            elif isinstance(payload, dict):
                self._post("log", "[JS] " + str(payload))
            else:
                self._post("log", "[JS] " + str(payload))
            return
        # console.log 输出
        if message.get("type") == "log":
            self._post("log", "[JS日志] " + str(message.get("payload", "")))
            return
        if message.get("type") == "error":
            self._post("log", "[JS异常] " + message.get("stack", message.get("description", "")))

    # ==================== RPC ====================

    def _rpc_call(self, method, *args):
        if not self.script or self.rpc_busy:
            return
        self.rpc_busy = True
        self._set_controls_enabled(False)
        threading.Thread(target=self._rpc_worker, args=(method, args), daemon=True).start()

    def _rpc_worker(self, method, args):
        with self.rpc_lock:
            try:
                ex = self.script.exports_sync
                if method == "enable":
                    result = ex.enable(*args)
                elif method == "setconfig":
                    result = ex.setconfig(*args)
                elif method == "probe":
                    result = ex.probe(*args)
                elif method == "status":
                    result = ex.status()
                elif method == "cleanup":
                    result = ex.cleanup()
                else:
                    raise ValueError("unknown rpc method: " + method)
                self._post("rpc_done", result)
            except Exception as exc:
                self._post("rpc_error", exc)

    def _refresh_status(self):
        if not self.script or self.status_busy:
            return
        self.status_busy = True
        threading.Thread(target=self._status_worker, daemon=True).start()

    def _status_worker(self):
        with self.rpc_lock:
            try:
                result = self.script.exports_sync.status()
                self._post("status", result)
            except Exception:
                pass
            finally:
                self.status_busy = False

    def _schedule_status_poll(self):
        if self.closing:
            return
        if self.connected:
            self._refresh_status()
            self.after(1000, self._schedule_status_poll)

    # ==================== 控件回调 ====================

    def _on_slider_change(self, value):
        self.amount = int(round(float(value)))
        self.amount_label.configure(text=str(self.amount))
        if self.script and not self.rpc_busy:
            self._rpc_call("setconfig", {"amount": self.amount})

    def _run_probe(self, action):
        if not self.script:
            return
        names = {"readonly": "只读快照", "heal": "Heal 探测", "addmax": "AddHealthMax 探测"}
        self._log(f">>> 点击 {names.get(action, action)} (amount=+{self.amount})")
        self._rpc_call("probe", action)

    # ==================== 状态渲染 ====================

    def _render_status(self, status):
        if not isinstance(status, dict):
            return

        phase = str(status.get("probe_phase", "idle"))
        self.phase_label.configure(
            text=phase, text_color=ORANGE if phase != "idle" else "#ddd")

        rate = status.get("last_rate")
        if isinstance(rate, (int, float)):
            self.rate_label.configure(text=f"{rate:.4f}")
        else:
            self.rate_label.configure(text="-")

        is_max = status.get("last_isMaxHP")
        if is_max is None:
            self.maxhp_label.configure(text="-")
        else:
            self.maxhp_label.configure(
                text="满血" if is_max else "未满",
                text_color=RED if is_max else GREEN)

        stats = status.get("stats", {}) or {}
        errors = stats.get("errorCount", 0)
        self.error_label.configure(text=str(errors), text_color=RED if errors else "#ddd")

    # ==================== 关闭 ====================

    def _on_close(self):
        if self.shutdown_done:
            return
        self.shutdown_done = True
        self.closing = True
        self._set_controls_enabled(False)
        self._log("正在清理并关闭...")
        threading.Thread(target=self._shutdown_worker, daemon=True).start()

    def _shutdown_worker(self):
        try:
            if self.script:
                with self.rpc_lock:
                    try:
                        self.script.exports_sync.cleanup()
                    except Exception:
                        pass
                    try:
                        self.script.unload()
                    except Exception:
                        pass
            if self.session:
                try:
                    self.session.detach()
                except Exception:
                    pass
        finally:
            try:
                with self._file_lock:
                    self._log_file.close()
            except Exception:
                pass
            self._post_allow_closing("destroy")


if __name__ == "__main__":
    app = HpBoostProbeApp()
    app.mainloop()