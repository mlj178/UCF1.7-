# AAAAA-bot_pause_ui.py - Bot pause CustomTkinter UI
# v1.2-no-il2cpp-api
#
# Notes:
#   - JS side does not call runtime metadata / reflection API.
#   - ZIP package contains only runnable source files.
#
# Fixes:
#   1. No Frida RPC calls on Tk main thread.
#   2. No Tk widget updates from worker/Frida callback threads.
#   3. Session detached handling and reconnect loop.
#   4. Polling overlap prevention.
#   5. Safer shutdown: cleanup + detach in a worker thread.
#   6. Runtime TXT log is generated under logs/ for later analysis, but no TXT file is shipped in ZIP.

import customtkinter as ctk
import frida
import psutil
import threading
import time
import os
import queue
from datetime import datetime


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "AAAAA-bot_pause_min.js")
GAME_PROCESS_NAME = "UnityCrossFire.exe"

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"bot_pause_ui_{datetime.now().strftime('%Y%m%d')}.txt")

COLOR_GREEN = "#2ecc71"
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
        self._closing = False
        self._polling = False
        self._status_inflight = False
        self._rpc_inflight = False
        self._suppress_switch_event = False

        self._connection_lock = threading.Lock()
        self._rpc_lock = threading.Lock()
        self._ui_queue = queue.Queue()

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

        self.after(100, self._drain_ui_queue)
        self.after(800, self._start_connect_thread)

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(self, text="人机暂停", font=ctk.CTkFont(size=24, weight="bold")).grid(
            row=0, column=0, padx=18, pady=(16, 2), sticky="ew"
        )
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

    def _write_log_file(self, message):
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception:
            pass

    def log(self, message):
        now = datetime.now().strftime("%H:%M:%S")
        line = f"[{now}] {message}"
        self._write_log_file(line)
        try:
            self.log_text.configure(state="normal")
            self.log_text.insert("end", line + "\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
        except Exception:
            pass

    def clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def _post_ui(self, event, *args):
        if not self._closing:
            self._ui_queue.put((event, args))

    def _post_ui_allow_closing(self, event, *args):
        self._ui_queue.put((event, args))
        try:
            self.after(0, self._drain_ui_queue)
        except Exception:
            pass

    def _drain_ui_queue(self):
        try:
            while True:
                event, args = self._ui_queue.get_nowait()
                self._handle_ui_event(event, *args)
        except queue.Empty:
            pass
        if not self._closing:
            self.after(100, self._drain_ui_queue)

    def _handle_ui_event(self, event, *args):
        if event == "log":
            self.log(args[0])
        elif event == "status_text":
            connected, text, pid_text = args
            self._set_connection_status(connected, text, pid_text)
        elif event == "connected":
            self._on_connected(args[0])
        elif event == "detached":
            reason = args[0] if args else "unknown"
            self._set_disconnected(f"游戏连接已断开：{reason}")
        elif event == "rpc_done":
            self._on_rpc_done(args[0], args[1])
        elif event == "rpc_error":
            self._on_rpc_error(args[0], args[1])
        elif event == "status_result":
            self._on_status_result(args[0])
        elif event == "destroy":
            self.destroy()

    def find_game_pid(self):
        target = GAME_PROCESS_NAME.lower()
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                name = proc.info.get("name") or ""
                if name.lower() == target:
                    return proc.info["pid"]
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    def _start_connect_thread(self):
        if self._closing:
            return
        with self._connection_lock:
            if self._connecting or self.is_connected:
                return
            self._connecting = True
        threading.Thread(target=self._connect_worker, name="bot-pause-connect", daemon=True).start()

    def _connect_worker(self):
        try:
            if not os.path.exists(JS_FILE):
                self._post_ui("log", f"JS 文件不存在：{JS_FILE}")
                return
            while not self._closing and not self.is_connected:
                pid = self.find_game_pid()
                if pid is None:
                    self._post_ui("status_text", False, "等待游戏启动...", "")
                    time.sleep(1.5)
                    continue
                self._post_ui("status_text", False, "正在连接游戏...", f"PID {pid}")
                session = frida.attach(pid)
                session.on("detached", self._on_frida_detached)
                with open(JS_FILE, "r", encoding="utf-8") as f:
                    js_code = f.read()
                script = session.create_script(js_code)
                script.on("message", self.on_frida_message)
                script.load()
                with self._connection_lock:
                    if self._closing:
                        self._safe_unload_detach(script, session)
                        return
                    self.session = session
                    self.script = script
                    self.is_connected = True
                self._post_ui("connected", pid)
                return
        except Exception as exc:
            self._post_ui("log", f"连接失败：{exc}")
            if not self._closing:
                time.sleep(1.5)
                self._post_ui("status_text", False, "连接失败，稍后重试...", "")
                self.after_safe(1500, self._start_connect_thread)
        finally:
            with self._connection_lock:
                self._connecting = False

    def after_safe(self, delay_ms, callback):
        if self._closing:
            return
        try:
            self.after(delay_ms, callback)
        except Exception:
            pass

    def _set_connection_status(self, connected, text, pid_text):
        self.status_dot.configure(text_color=COLOR_GREEN if connected else "#888")
        self.status_label.configure(text=text)
        self.pid_label.configure(text=pid_text)

    def _on_connected(self, pid):
        self._set_connection_status(True, "已连接游戏", f"PID {pid}")
        self.feature_switch.configure(state="normal")
        self.log("脚本已加载")
        self._start_polling()

    def _safe_unload_detach(self, script=None, session=None):
        try:
            if script:
                script.unload()
        except Exception:
            pass
        try:
            if session:
                session.detach()
        except Exception:
            pass

    def _set_disconnected(self, reason):
        with self._connection_lock:
            old_script = self.script
            old_session = self.session
            self.is_connected = False
            self.script = None
            self.session = None
            self._polling = False
            self._status_inflight = False
            self._rpc_inflight = False
        self.feature_switch.configure(state="disabled")
        self._set_connection_status(False, "未连接", "")
        self.log(reason)
        self._safe_unload_detach(old_script, old_session)
        if not self._closing:
            self.after_safe(2000, self._start_connect_thread)

    def _on_frida_detached(self, reason, crash=None):
        detail = str(reason)
        if crash:
            detail += f" / {crash}"
        self._post_ui("detached", detail)

    def on_frida_message(self, message, data):
        msg_type = message.get("type")
        if msg_type == "send":
            payload = message.get("payload", {})
            if payload.get("type") == "log":
                self._post_ui("log", payload.get("message", ""))
        elif msg_type == "error":
            self._post_ui("log", str(message))

    def on_toggle_feature(self):
        if self._suppress_switch_event:
            return
        if not self.script or not self.is_connected:
            return
        if self._rpc_inflight:
            self.log("上一次操作尚未完成，请稍后")
            self._sync_switch_from_state()
            return
        action = "enable" if self.feature_switch.get() == 1 else "disable"
        self.feature_switch.configure(state="disabled")
        self._rpc_inflight = True
        threading.Thread(target=self._rpc_worker, args=(action,), name=f"bot-pause-rpc-{action}", daemon=True).start()

    def _rpc_worker(self, action):
        try:
            with self._rpc_lock:
                script = self.script
                if not script:
                    raise RuntimeError("Frida script is not loaded")
                result = getattr(script.exports_sync, action)()
            self._post_ui("rpc_done", action, result)
        except Exception as exc:
            self._post_ui("rpc_error", action, exc)

    def _on_rpc_done(self, action, result):
        self._rpc_inflight = False
        if isinstance(result, dict):
            with self._state_lock:
                self.game_state.update(result)
            self.log(result.get("msg", str(result)))
            if result.get("warning"):
                self.log(f"警告：{result.get('warning')}")
            for warning in result.get("warnings", []) or []:
                self.log(f"警告：{warning}")
        else:
            self.log(str(result))
        self._render_state()
        if self.is_connected and not self._closing:
            self.feature_switch.configure(state="normal")
        self.refresh_status_async()

    def _on_rpc_error(self, action, exc):
        self._rpc_inflight = False
        self.log(f"{action} 失败：{exc}")
        self._sync_switch_from_state()
        if self.is_connected and not self._closing:
            self.feature_switch.configure(state="normal")

    def _start_polling(self):
        if self._polling:
            return
        self._polling = True
        self.after_safe(500, self._poll_status)

    def _poll_status(self):
        if self._closing or not self.is_connected:
            self._polling = False
            return
        self.refresh_status_async()
        self.after_safe(1000, self._poll_status)

    def refresh_status_async(self):
        if not self.script or not self.is_connected or self._status_inflight:
            return
        self._status_inflight = True
        threading.Thread(target=self._status_worker, name="bot-pause-status", daemon=True).start()

    def _status_worker(self):
        detached = False
        try:
            with self._rpc_lock:
                script = self.script
                if not script:
                    raise RuntimeError("Frida script is not loaded")
                result = script.exports_sync.status()
            self._post_ui("status_result", result)
        except Exception as exc:
            self._post_ui("log", f"状态读取失败：{exc}")
            detached = True
        finally:
            self._status_inflight = False
            if detached:
                self._post_ui("detached", "Frida RPC 状态读取失败，可能游戏已退出")

    def _on_status_result(self, status):
        if isinstance(status, dict):
            with self._state_lock:
                self.game_state.update(status)
            self._render_state()
            if not status.get("ok", True):
                msg = status.get("msg") or status.get("lastError")
                if msg:
                    self.log(f"状态警告：{msg}")
            if status.get("warning"):
                self.log(f"警告：{status.get('warning')}")
            for warning in status.get("warnings", []) or []:
                self.log(f"警告：{warning}")

    def _sync_switch_from_state(self):
        paused = bool(self.game_state.get("paused"))
        self._suppress_switch_event = True
        try:
            if paused:
                self.feature_switch.select()
                self.feature_switch.configure(text="暂停")
            else:
                self.feature_switch.deselect()
                self.feature_switch.configure(text="恢复")
        finally:
            self._suppress_switch_event = False

    def _render_state(self):
        with self._state_lock:
            paused = bool(self.game_state.get("paused"))
            enabled = bool(self.game_state.get("enabled", paused))
            write_count = self.game_state.get("writeCount", 0)
        self.enabled_label.configure(text="开启" if enabled else "关闭", text_color=COLOR_GREEN if enabled else "#ccc")
        self.paused_label.configure(text="暂停" if paused else "恢复", text_color=COLOR_ORANGE if paused else COLOR_GREEN)
        self.write_label.configure(text=str(write_count))
        self._sync_switch_from_state()

    def on_close(self):
        if self._closing:
            return
        self._closing = True
        self.feature_switch.configure(state="disabled")
        self.log("正在清理并退出...")
        threading.Thread(target=self._shutdown_worker, name="bot-pause-shutdown", daemon=True).start()

    def _shutdown_worker(self):
        try:
            with self._rpc_lock:
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
            self._post_ui_allow_closing("destroy")


if __name__ == "__main__":
    app = BotPauseApp()
    app.mainloop()
