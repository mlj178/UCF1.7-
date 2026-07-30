"""Minimal CustomTkinter UI for fixed_point_teleport."""

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
JS_FILE = os.path.join(BASE_DIR, "AAAAA-fixed_point_teleport_min.js")
GAME_PROCESS_NAME = "UnityCrossFire.exe"

GREEN = "#2ecc71"
ORANGE = "#f39c12"
RED = "#e74c3c"
PANEL = "#1d2430"
PANEL_DARK = "#161c26"


class FixedPointTeleportApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("定点瞬移")
        self.geometry("560x560")
        self.minsize(500, 500)

        self.session = None
        self.script = None
        self.connected = False
        self.connecting = False
        self.closing = False
        self.rpc_busy = False
        self.status_busy = False
        self.shutdown_done = False
        self.desired_enabled = False

        self.rpc_lock = threading.Lock()
        self.ui_queue = queue.Queue()

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._drain_ui_queue)
        self.after(600, self._schedule_connect)

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(
            self,
            text="定点瞬移",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=18, pady=(18, 4), sticky="ew")

        ctk.CTkLabel(
            self,
            text="保存点位1或点位2后，可将本地玩家瞬移回对应点位",
            text_color="#8f98a8",
            font=ctk.CTkFont(size=12),
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
        controls.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            controls,
            text="功能开关",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, padx=12, pady=12, sticky="w")

        self.enable_switch = ctk.CTkSwitch(
            controls,
            text="关闭",
            command=self._on_enable_changed,
            progress_color=GREEN,
            switch_width=50,
            switch_height=24,
        )
        self.enable_switch.grid(row=0, column=1, padx=12, pady=12, sticky="w")

        actions = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        actions.grid(row=4, column=0, padx=18, pady=5, sticky="ew")
        actions.grid_columnconfigure(0, weight=0)
        actions.grid_columnconfigure((1, 2), weight=1)

        ctk.CTkLabel(actions, text="点位1", width=52).grid(row=0, column=0, padx=(8, 2), pady=(12, 4), sticky="w")

        self.save_button = ctk.CTkButton(
            actions,
            text="保存点位1",
            command=self._save_point,
            height=34,
            fg_color="#2878c9",
        )
        self.save_button.grid(row=0, column=1, padx=4, pady=(12, 4), sticky="ew")

        self.teleport_button = ctk.CTkButton(
            actions,
            text="瞬移到点位1",
            command=self._teleport_to_point,
            height=34,
            fg_color=GREEN,
        )
        self.teleport_button.grid(row=0, column=2, padx=(4, 8), pady=(12, 4), sticky="ew")

        ctk.CTkLabel(actions, text="点位2", width=52).grid(row=1, column=0, padx=(8, 2), pady=(4, 12), sticky="w")

        self.save_button2 = ctk.CTkButton(
            actions,
            text="保存点位2",
            command=self._save_point2,
            height=34,
            fg_color="#2878c9",
        )
        self.save_button2.grid(row=1, column=1, padx=4, pady=(4, 12), sticky="ew")

        self.teleport_button2 = ctk.CTkButton(
            actions,
            text="瞬移到点位2",
            command=self._teleport_to_point2,
            height=34,
            fg_color=GREEN,
        )
        self.teleport_button2.grid(row=1, column=2, padx=(4, 8), pady=(4, 12), sticky="ew")

        metrics = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL_DARK)
        metrics.grid(row=5, column=0, padx=18, pady=5, sticky="ew")
        metrics.grid_columnconfigure((0, 1, 2), weight=1)

        self.enabled_label = self._add_metric(metrics, 0, "功能状态", "关闭")
        self.player_label = self._add_metric(metrics, 1, "玩家捕获", "等待")
        self.count_label = self._add_metric(metrics, 2, "瞬移次数", "0")

        self.point_label = ctk.CTkLabel(
            self,
            text="保存点：无",
            text_color="#9aa3b2",
            font=ctk.CTkFont(size=12),
        )
        self.point_label.grid(row=6, column=0, padx=18, pady=(6, 4), sticky="ew")

        self.detail_label = ctk.CTkLabel(
            self,
            text="等待连接游戏",
            text_color="#9aa3b2",
            font=ctk.CTkFont(size=12),
        )
        self.detail_label.grid(row=7, column=0, padx=18, pady=(2, 4), sticky="ew")

        self.log_box = ctk.CTkTextbox(self, height=150, font=ctk.CTkFont(size=11))
        self.log_box.grid(row=8, column=0, padx=18, pady=(4, 16), sticky="nsew")
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
        self.save_button.configure(state=state)
        self.teleport_button.configure(state=state)
        self.save_button2.configure(state=state)
        self.teleport_button2.configure(state=state)

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
            if not os.path.exists(JS_FILE):
                self._post("log", f"JS 文件不存在：{JS_FILE}")
                return

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
                    self._safe_unload_detach(script, session)
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
        self._sync_desired_state()
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
        old_script = self.script
        old_session = self.session
        self.connected = False
        self.script = None
        self.session = None
        self.rpc_busy = False
        self.status_busy = False
        self._set_controls_enabled(False)
        self._set_connection(False, "游戏连接已断开", "")
        self._log("连接断开：" + reason)
        self._safe_unload_detach(old_script, old_session)
        if not self.closing:
            self.after(1500, self._schedule_connect)

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

    def _on_enable_changed(self):
        self.desired_enabled = self.enable_switch.get() == 1
        self.enable_switch.configure(text="开启" if self.desired_enabled else "关闭")
        self._sync_desired_state()

    def _sync_desired_state(self):
        if not self.connected or not self.script or self.rpc_busy:
            return
        self.rpc_busy = True
        self._set_controls_enabled(False)
        threading.Thread(target=self._rpc_worker, args=("toggle",), daemon=True).start()

    def _save_point(self):
        self._run_point_rpc("save")

    def _teleport_to_point(self):
        self._run_point_rpc("teleport")

    def _save_point2(self):
        self._run_point_rpc("save2")

    def _teleport_to_point2(self):
        self._run_point_rpc("teleport2")


    def _run_point_rpc(self, action):
        if not self.connected or not self.script or self.rpc_busy:
            return
        self.rpc_busy = True
        self._set_controls_enabled(False)
        threading.Thread(target=self._rpc_worker, args=(action,), daemon=True).start()

    def _rpc_worker(self, action):
        try:
            with self.rpc_lock:
                if action == "toggle":
                    if self.desired_enabled:
                        self.script.exports_sync.setconfig(self._current_config())
                        result = self.script.exports_sync.enable()
                    else:
                        result = self.script.exports_sync.disable()
                elif action == "save":
                    result = self.script.exports_sync.savepoint()
                elif action == "teleport":
                    result = self.script.exports_sync.teleporttopoint()
                elif action == "save2":
                    result = self.script.exports_sync.savepoint2()
                elif action == "teleport2":
                    result = self.script.exports_sync.teleporttopoint2()
                else:
                    result = self.script.exports_sync.status()
            self._post("rpc_done", result)
        except Exception as exc:
            self._post("rpc_error", exc)

    def _current_config(self):
        return {
            "require_enabled_for_actions": True,
            "max_cached_player_age_ms": 3000,
        }

    def _poll_status(self):
        if self.closing or not self.connected:
            return
        if not self.status_busy and self.script:
            self.status_busy = True
            threading.Thread(target=self._status_worker, daemon=True).start()
        self.after(1000, self._poll_status)

    def _status_worker(self):
        detached = False
        try:
            with self.rpc_lock:
                result = self.script.exports_sync.status()
            self._post("status", result)
        except Exception as exc:
            self._post("log", "状态读取失败：" + str(exc))
            detached = True
        finally:
            self.status_busy = False
            if detached:
                self._post("detached", "Frida RPC 状态读取失败，可能游戏已退出")

    @staticmethod
    def _format_point(point):
        if not isinstance(point, dict):
            return "无"
        try:
            return f"({point.get('x', 0):.3f}, {point.get('y', 0):.3f}, {point.get('z', 0):.3f})"
        except Exception:
            return str(point)

    def _render_status(self, status):
        if not isinstance(status, dict):
            return

        enabled = bool(status.get("enabled"))
        applied = bool(status.get("applied"))
        pending = bool(status.get("pendingApply"))
        saved = bool(status.get("has_saved_point"))
        point = status.get("saved_point")
        teleports = status.get("teleport_count", 0)
        last_error = status.get("last_error") or ""
        last_save = status.get("last_save_result") or ""
        last_teleport = status.get("last_teleport_result") or ""

        self.enabled_label.configure(
            text="开启" if enabled else "关闭",
            text_color=GREEN if enabled else "#ccc",
        )

        if applied:
            self.player_label.configure(text="已捕获", text_color=GREEN)
        elif pending:
            self.player_label.configure(text="等待进房", text_color=ORANGE)
        else:
            self.player_label.configure(text="等待", text_color="#ccc")

        self.count_label.configure(text=str(teleports), text_color=GREEN if teleports else "#ccc")
        self.point_label.configure(
            text="保存点：" + self._format_point(point),
            text_color=GREEN if saved else "#9aa3b2",
        )

        if last_error:
            self.detail_label.configure(text="错误：" + last_error, text_color=RED)
        elif last_teleport:
            self.detail_label.configure(text=last_teleport, text_color=GREEN if "teleported" in last_teleport else ORANGE)
        elif last_save:
            self.detail_label.configure(text=last_save, text_color=GREEN if saved else ORANGE)
        elif enabled and applied:
            self.detail_label.configure(text="已开启，可保存点位或瞬移", text_color=GREEN)
        elif enabled:
            self.detail_label.configure(text="已开启，等待本地玩家进入运行状态", text_color=ORANGE)
        else:
            self.detail_label.configure(text="关闭状态：不会保存或瞬移", text_color="#9aa3b2")

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
            self._post_allow_closing("destroy")


if __name__ == "__main__":
    FixedPointTeleportApp().mainloop()
