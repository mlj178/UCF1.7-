"""直接变身剑客独立测试 UI。"""

import json
import os
import queue
import threading
import time

import customtkinter as ctk
import frida
import psutil


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "script.js")
LOG_DIR = os.path.join(BASE_DIR, "logs")
GAME_PROCESS_NAME = "UnityCrossFire.exe"

GREEN = "#2ecc71"
RED = "#e74c3c"
PANEL = "#1d2430"
PANEL_DARK = "#161c26"


class BecomeGhostbladeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("直接变身剑客 - 独立测试")
        self.geometry("600x560")
        self.minsize(520, 480)

        self.session = None
        self.script = None
        self.connected = False
        self.connecting = False
        self.closing = False
        self.rpc_busy = False
        self.status_busy = False
        self.shutdown_done = False

        self.rpc_lock = threading.Lock()
        self.ui_queue = queue.Queue()
        self.log_path = self._open_log_file()
        self._write_log_file(f"session_start feature=become_ghostblade pid_file={self.log_path}")

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._drain_ui_queue)
        self.after(600, self._schedule_connect)

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(
            self, text="直接变身剑客", font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=18, pady=(18, 4), sticky="ew")

        ctk.CTkLabel(
            self,
            text="生化6（剑客模式）下让本地/存活 Bot 变成剑客（需当前为佣兵）",
            text_color="#8f98a8", font=ctk.CTkFont(size=12),
        ).grid(row=1, column=0, padx=18, pady=(0, 8), sticky="ew")

        status = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        status.grid(row=2, column=0, padx=18, pady=5, sticky="ew")
        status.grid_columnconfigure(1, weight=1)

        self.status_dot = ctk.CTkLabel(status, text="●", text_color="#777")
        self.status_dot.grid(row=0, column=0, padx=(12, 5), pady=10)
        self.connection_label = ctk.CTkLabel(status, text="等待游戏启动...")
        self.connection_label.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        self.pid_label = ctk.CTkLabel(status, text="", text_color="#999")
        self.pid_label.grid(row=0, column=2, padx=12, pady=10)

        controls = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL_DARK)
        controls.grid(row=3, column=0, padx=18, pady=5, sticky="ew")

        ctk.CTkLabel(controls, text="功能开关", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, padx=12, pady=12, sticky="w")
        self.enable_switch = ctk.CTkSwitch(
            controls, text="关闭", command=self._on_enable_changed,
            progress_color=GREEN, switch_width=50, switch_height=24,
        )
        self.enable_switch.grid(row=0, column=1, padx=12, pady=12, sticky="e")

        self.local_button = ctk.CTkButton(
            controls, text="本地变身剑客", height=36,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#0e7490", hover_color="#155e75",
            command=lambda: self._on_trigger("local_ghostblade"),
        )
        self.local_button.grid(row=1, column=0, columnspan=2, padx=12, pady=(4, 6), sticky="ew")

        self.bot_button = ctk.CTkButton(
            controls, text="所有 Bot 变剑客", height=36,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1e40af", hover_color="#1e3a8a",
            command=lambda: self._on_trigger("bot_ghostblade"),
        )
        self.bot_button.grid(row=2, column=0, columnspan=2, padx=12, pady=(0, 12), sticky="ew")

        metrics = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        metrics.grid(row=4, column=0, padx=18, pady=5, sticky="ew")
        metrics.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.enabled_label = self._add_metric(metrics, 0, "功能状态", "关闭")
        self.local_label = self._add_metric(metrics, 1, "本地变身", "0")
        self.bot_label = self._add_metric(metrics, 2, "Bot变身", "0")
        self.error_label = self._add_metric(metrics, 3, "错误", "0")

        self.result_label = ctk.CTkLabel(
            self, text="就绪", text_color="#9aa3b2", font=ctk.CTkFont(size=12),
        )
        self.result_label.grid(row=5, column=0, padx=18, pady=(6, 4), sticky="ew")

        self.log_box = ctk.CTkTextbox(self, height=160, font=ctk.CTkFont(size=11))
        self.log_box.grid(row=6, column=0, padx=18, pady=(4, 16), sticky="nsew")
        self.log_box.configure(state="disabled")

        self._set_controls_enabled(False)

    def _add_metric(self, parent, column, title, value):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=column, padx=8, pady=10, sticky="ew")
        ctk.CTkLabel(frame, text=title, text_color="#8f98a8", font=ctk.CTkFont(size=11)).pack()
        label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=15, weight="bold"))
        label.pack(pady=(2, 0))
        return label

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
            self._log("RPC_STATUS " + json.dumps(args[0], ensure_ascii=False, default=str))
            self._render_status(args[0])
            self._set_controls_enabled(self.connected)
        elif event == "rpc_error":
            self.rpc_busy = False
            self._log("RPC_ERROR " + str(args[0]))
            self._set_controls_enabled(self.connected)
        elif event == "status":
            self._render_status(args[0])
        elif event == "destroy":
            self.destroy()

    @staticmethod
    def _open_log_file():
        os.makedirs(LOG_DIR, exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(LOG_DIR, f"become_ghostblade_ui_{stamp}.log")
        open(path, "a", encoding="utf-8").close()
        return path

    def _write_log_file(self, text):
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.log_path, "a", encoding="utf-8") as fp:
                fp.write(f"[{stamp}] {text}\n")
        except OSError:
            pass

    def _log(self, text):
        stamp = time.strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{stamp}] {text}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        self._write_log_file(str(text))

    def _set_connection(self, connected, text, pid_text=""):
        self.status_dot.configure(text_color=GREEN if connected else "#777")
        self.connection_label.configure(text=text)
        self.pid_label.configure(text=pid_text)

    def _set_controls_enabled(self, enabled):
        state = "normal" if enabled and not self.rpc_busy else "disabled"
        self.enable_switch.configure(state=state)
        self.local_button.configure(state=state)
        self.bot_button.configure(state=state)

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

            self._post("waiting", "正在注入脚本...", f"PID {pid}")
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
        self._log("脚本已加载")
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
        if message.get("type") == "send":
            payload = message.get("payload", {})
            if isinstance(payload, dict) and payload.get("type") == "log":
                self._post("log", payload.get("message", ""))
            elif isinstance(payload, dict) and payload.get("type") == "status":
                self._post("log", "FRIDA_STATUS " + json.dumps(payload, ensure_ascii=False))
            return
        if message.get("type") == "error":
            self._post("log", message.get("stack", message.get("description", "Frida error")))

    def _rpc_call(self, method, *args):
        if not self.script or self.rpc_busy:
            return
        self.rpc_busy = True
        self._set_controls_enabled(False)
        threading.Thread(target=self._rpc_worker, args=(method, args), daemon=True).start()

    def _rpc_worker(self, method, args):
        with self.rpc_lock:
            try:
                if method == "enable":
                    result = self.script.exports_sync.enable()
                elif method == "disable":
                    result = self.script.exports_sync.disable()
                elif method == "status":
                    result = self.script.exports_sync.status()
                elif method == "trigger":
                    result = self.script.exports_sync.trigger(*args)
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
            except Exception as exc:
                self._post("log", "状态读取失败：" + str(exc))
            finally:
                self.status_busy = False

    def _schedule_status_poll(self):
        if self.closing:
            return
        if self.connected and not self.rpc_busy:
            self._refresh_status()
        if self.connected:
            self.after(1000, self._schedule_status_poll)

    def _on_enable_changed(self):
        enabled = self.enable_switch.get() == 1
        self.enable_switch.configure(text="开启" if enabled else "关闭")
        if enabled:
            self._rpc_call("enable")
        else:
            self._rpc_call("disable")

    def _on_trigger(self, action):
        if not self.script:
            return
        self._log(f"已发送动作: {action}")
        self._rpc_call("trigger", action)

    def _render_status(self, status):
        if not isinstance(status, dict):
            return

        enabled = bool(status.get("enabled"))
        self.enabled_label.configure(
            text="开启" if enabled else "关闭",
            text_color=GREEN if enabled else "#ddd",
        )
        self.enable_switch.configure(text="开启" if enabled else "关闭")
        if enabled and self.enable_switch.get() == 0:
            self.enable_switch.select()
        if not enabled and self.enable_switch.get() == 1:
            self.enable_switch.deselect()

        self.local_label.configure(text=str(status.get("local_ghostblade_applied", 0)))
        self.bot_label.configure(text=str(status.get("bot_ghostblade_applied", 0)))
        errors = status.get("error_count", 0)
        self.error_label.configure(text=str(errors), text_color=RED if errors else "#ddd")

        last_result = status.get("last_result") or ""
        last_error = status.get("last_error") or ""
        parts = [f"最近结果: {last_result}" if last_result else "最近结果: -"]
        if last_error:
            parts.append(f"错误: {last_error}")
        self.result_label.configure(text=" | ".join(parts))

    def _on_close(self):
        if self.shutdown_done:
            return
        self.shutdown_done = True
        self.closing = True
        self._set_controls_enabled(False)
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
            self._post_allow_closing("destroy")


if __name__ == "__main__":
    app = BecomeGhostbladeApp()
    app.mainloop()
