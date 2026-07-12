"""Minimal CustomTkinter UI for game mode override."""

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
JS_FILE = os.path.join(BASE_DIR, "AAAAA-game_mode_override_min.js")
GAME_PROCESS_NAME = "UnityCrossFire.exe"

MODE_OPTIONS = {
    "团队竞技": "team_death",
    "特殊战": "special",
    "个人竞技": "death_match",
    "生化3": "nano3",
    "多人生化（生化4）": "nano4",
    "生化6": "nano6",
    "生化4终结者": "nano4_terminator",
    "狙击战": "sniper",
    "手枪战": "handgun",
}

GREEN = "#2ecc71"
ORANGE = "#f39c12"
RED = "#e74c3c"
PANEL = "#1d2430"


class GameModeOverrideApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("游戏模式切换")
        self.geometry("560x430")
        self.minsize(500, 390)

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

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._drain_ui_queue)
        self.after(500, self._schedule_connect)

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(
            self,
            text="游戏模式切换",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=18, pady=(18, 8), sticky="ew")

        status = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        status.grid(row=1, column=0, padx=18, pady=5, sticky="ew")
        status.grid_columnconfigure(1, weight=1)
        self.status_dot = ctk.CTkLabel(status, text="●", text_color="#777")
        self.status_dot.grid(row=0, column=0, padx=(12, 5), pady=10)
        self.connection_label = ctk.CTkLabel(status, text="等待游戏启动...")
        self.connection_label.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        self.pid_label = ctk.CTkLabel(status, text="", text_color="#999")
        self.pid_label.grid(row=0, column=2, padx=12, pady=10)

        controls = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        controls.grid(row=2, column=0, padx=18, pady=5, sticky="ew")
        controls.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(controls, text="模式替换").grid(
            row=0, column=0, padx=12, pady=12, sticky="w"
        )
        self.enable_switch = ctk.CTkSwitch(
            controls,
            text="关闭",
            command=self._on_enable_changed,
            progress_color=GREEN,
        )
        self.enable_switch.grid(row=0, column=1, padx=12, pady=12, sticky="w")

        ctk.CTkLabel(controls, text="目标模式").grid(
            row=1, column=0, padx=12, pady=(4, 14), sticky="w"
        )
        self.mode_menu = ctk.CTkOptionMenu(
            controls,
            values=list(MODE_OPTIONS.keys()),
            command=self._on_mode_changed,
            width=240,
        )
        self.mode_menu.set("团队竞技")
        self.mode_menu.grid(row=1, column=1, padx=12, pady=(4, 14), sticky="w")

        self.apply_label = ctk.CTkLabel(
            self,
            text="关闭状态：游戏使用原始模式",
            text_color="#aaa",
            font=ctk.CTkFont(size=13),
        )
        self.apply_label.grid(row=3, column=0, padx=18, pady=(8, 4), sticky="ew")

        ctk.CTkLabel(
            self,
            text="选择会在下一次点击游戏“开始游戏”时生效",
            text_color="#888",
            font=ctk.CTkFont(size=11),
        ).grid(row=4, column=0, padx=18, pady=(0, 5), sticky="ew")

        self.log_box = ctk.CTkTextbox(self, height=110, font=ctk.CTkFont(size=11))
        self.log_box.grid(row=5, column=0, padx=18, pady=(5, 16), sticky="nsew")
        self.log_box.configure(state="disabled")

        self._set_controls_enabled(False)

    def _post(self, event, *args):
        if not self.closing:
            self.ui_queue.put((event, args))

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
            self.after(500, self._schedule_connect)
        elif event == "rpc_result":
            self.rpc_busy = False
            self._render_status(args[0])
            self._set_controls_enabled(self.connected)
        elif event == "rpc_error":
            self.rpc_busy = False
            self._log("设置失败：" + str(args[0]))
            self._set_controls_enabled(self.connected)
        elif event == "status":
            self._render_status(args[0])

    def _log(self, text):
        stamp = time.strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{stamp}] {text}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _set_connection(self, connected, text, pid_text=""):
        self.status_dot.configure(text_color=GREEN if connected else "#777")
        self.connection_label.configure(text=text)
        self.pid_label.configure(text=pid_text)

    def _set_controls_enabled(self, enabled):
        state = "normal" if enabled and not self.rpc_busy else "disabled"
        self.enable_switch.configure(state=state)
        self.mode_menu.configure(state=state)

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
            while not self.closing and not self.connected:
                pid = self._find_game_pid()
                if pid is None:
                    self._post("waiting", "等待游戏启动...", "")
                    time.sleep(1.5)
                    continue

                self._post("waiting", "正在连接游戏...", f"PID {pid}")
                session = frida.attach(pid)
                session.on("detached", self._frida_detached)
                with open(JS_FILE, "r", encoding="utf-8") as handle:
                    script = session.create_script(handle.read())
                script.on("message", self._frida_message)
                script.load()

                if self.closing:
                    script.unload()
                    session.detach()
                    return

                self.session = session
                self.script = script
                self.connected = True
                self._post("connected", pid)
                return
        except Exception as exc:
            self._post("log", "连接失败：" + str(exc))
            self._post("waiting", "连接失败，稍后重试...", "")
            time.sleep(1.5)
        finally:
            self.connecting = False
            if not self.closing and not self.connected:
                self._post("retry_connect")

    def _on_connected(self, pid):
        self._set_connection(True, "已连接游戏", f"PID {pid}")
        self._set_controls_enabled(True)
        self._log("脚本已加载")
        self._push_config()
        self.after(600, self._poll_status)

    def _frida_message(self, message, data):
        if message.get("type") == "send":
            payload = message.get("payload") or {}
            if payload.get("type") == "log":
                self._post("log", payload.get("message", ""))
        elif message.get("type") == "error":
            self._post("log", str(message))

    def _frida_detached(self, reason, crash=None):
        detail = str(reason)
        if crash:
            detail += " / " + str(crash)
        self._post("detached", detail)

    def _on_detached(self, reason):
        self.connected = False
        self.script = None
        self.session = None
        self.rpc_busy = False
        self.status_busy = False
        self._set_controls_enabled(False)
        self._set_connection(False, "游戏连接已断开", "")
        self._log("连接断开：" + reason)
        if not self.closing:
            self.after(1200, self._schedule_connect)

    def _selected_config(self):
        label = self.mode_menu.get()
        return {
            "enabled": self.enable_switch.get() == 1,
            "mode_key": MODE_OPTIONS[label],
        }

    def _on_enable_changed(self):
        self.enable_switch.configure(text="开启" if self.enable_switch.get() else "关闭")
        self._push_config()

    def _on_mode_changed(self, _choice):
        self._push_config()

    def _push_config(self):
        if not self.connected or not self.script or self.rpc_busy:
            return
        config = self._selected_config()
        self.rpc_busy = True
        self._set_controls_enabled(False)
        threading.Thread(target=self._config_worker, args=(config,), daemon=True).start()

    def _config_worker(self, config):
        try:
            with self.rpc_lock:
                result = self.script.exports_sync.setconfig(config)
            self._post("rpc_result", result)
        except Exception as exc:
            self._post("rpc_error", exc)

    def _poll_status(self):
        if self.closing or not self.connected:
            return
        if not self.status_busy and self.script:
            self.status_busy = True
            threading.Thread(target=self._status_worker, daemon=True).start()
        self.after(1000, self._poll_status)

    def _status_worker(self):
        try:
            with self.rpc_lock:
                result = self.script.exports_sync.status()
            self._post("status", result)
        except Exception as exc:
            self._post("detached", "状态读取失败：" + str(exc))
        finally:
            self.status_busy = False

    def _render_status(self, status):
        if not isinstance(status, dict):
            return
        enabled = bool(status.get("enabled"))
        mode_label = status.get("modeLabel", self.mode_menu.get())
        applied = status.get("lastApplied") or {}
        error = status.get("lastError")

        if error:
            self.apply_label.configure(text="等待失败：" + str(error), text_color=RED)
        elif applied:
            self.apply_label.configure(
                text=f"已应用：{applied.get('label', mode_label)}（第 {applied.get('count', 0)} 次）",
                text_color=GREEN,
            )
        elif enabled:
            self.apply_label.configure(text="等待开始游戏：" + mode_label, text_color=ORANGE)
        else:
            self.apply_label.configure(text="关闭状态：游戏使用原始模式", text_color="#aaa")

    def _on_close(self):
        if self.closing:
            return
        self.closing = True
        self._set_controls_enabled(False)
        threading.Thread(target=self._shutdown_worker, daemon=True).start()
        self.after(50, self._wait_for_shutdown)

    def _wait_for_shutdown(self):
        if self.shutdown_done:
            self.destroy()
            return
        self.after(50, self._wait_for_shutdown)

    def _shutdown_worker(self):
        try:
            with self.rpc_lock:
                if self.script:
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
            self.shutdown_done = True


if __name__ == "__main__":
    GameModeOverrideApp().mainloop()
