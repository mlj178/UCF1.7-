"""Minimal CustomTkinter UI for local-player damage multiplier."""

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
JS_FILE = os.path.join(BASE_DIR, "AAAAA-damage_multiplier_min.js")
GAME_PROCESS_NAME = "UnityCrossFire.exe"

GREEN = "#2ecc71"
ORANGE = "#f39c12"
RED = "#e74c3c"
PANEL = "#1d2430"
PANEL_DARK = "#161c26"


class DamageMultiplierApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("调整伤害倍率")
        self.geometry("660x620")
        self.minsize(600, 540)

        self.session = None
        self.script = None
        self.connected = False
        self.connecting = False
        self.closing = False
        self.rpc_busy = False
        self.status_busy = False
        self.shutdown_done = False
        self.desired_enabled = False

        self.multiplier = 2.0
        self.allow_other_damage_type = True
        self.diagnostic_log = True

        self.rpc_lock = threading.Lock()
        self.ui_queue = queue.Queue()

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._drain_ui_queue)
        self.after(600, self._schedule_connect)

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)

        ctk.CTkLabel(
            self,
            text="调整伤害倍率",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=18, pady=(18, 4), sticky="ew")

        ctk.CTkLabel(
            self,
            text="放大玩家造成的输出伤害",
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

        ctk.CTkLabel(
            controls,
            text="倍率",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=1, column=0, padx=12, pady=(2, 12), sticky="w")

        slider_row = ctk.CTkFrame(controls, fg_color="transparent")
        slider_row.grid(row=1, column=1, padx=12, pady=(2, 12), sticky="ew")
        slider_row.grid_columnconfigure(0, weight=1)

        self.multiplier_slider = ctk.CTkSlider(
            slider_row,
            from_=1.0,
            to=20.0,
            number_of_steps=190,
            command=self._on_multiplier_preview,
        )
        self.multiplier_slider.set(self.multiplier)
        self.multiplier_slider.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.multiplier_label = ctk.CTkLabel(
            slider_row,
            text=self._format_multiplier(self.multiplier),
            width=58,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.multiplier_label.grid(row=0, column=1, sticky="e")

        self.other_switch = ctk.CTkSwitch(
            controls,
            text="覆盖 Other 类型特殊技能伤害",
            command=self._on_config_changed,
            progress_color=GREEN,
            switch_width=50,
            switch_height=24,
        )
        self.other_switch.select()
        self.other_switch.grid(row=2, column=0, columnspan=2, padx=12, pady=(0, 10), sticky="w")

        self.log_switch = ctk.CTkSwitch(
            controls,
            text="诊断日志",
            command=self._on_config_changed,
            progress_color=GREEN,
            switch_width=50,
            switch_height=24,
        )
        self.log_switch.select()
        self.log_switch.grid(row=3, column=0, columnspan=2, padx=12, pady=(0, 12), sticky="w")

        metrics = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        metrics.grid(row=4, column=0, padx=18, pady=5, sticky="ew")
        metrics.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.enabled_label = self._add_metric(metrics, 0, "功能状态", "关闭")
        self.total_label = self._add_metric(metrics, 1, "伤害事件", "0")
        self.multiplied_label = self._add_metric(metrics, 2, "已放大", "0")
        self.owner_label = self._add_metric(metrics, 3, "归属命中", "0/0")

        last_panel = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL_DARK)
        last_panel.grid(row=5, column=0, padx=18, pady=5, sticky="ew")
        last_panel.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.damage_label = self._add_metric(last_panel, 0, "最近伤害", "-")
        self.type_label = self._add_metric(last_panel, 1, "类型", "-")
        self.weapon_label = self._add_metric(last_panel, 2, "武器", "-")
        self.decision_label = self._add_metric(last_panel, 3, "决策", "-")

        skip_panel = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        skip_panel.grid(row=6, column=0, padx=18, pady=5, sticky="ew")
        skip_panel.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.skip_attacker_label = self._add_metric(skip_panel, 0, "非本地", "0")
        self.skip_victim_label = self._add_metric(skip_panel, 1, "本地受击", "0")
        self.skip_infect_label = self._add_metric(skip_panel, 2, "感染跳过", "0")
        self.error_label = self._add_metric(skip_panel, 3, "错误", "0")

        self.detail_label = ctk.CTkLabel(
            self,
            text="等待连接游戏",
            text_color="#9aa3b2",
            font=ctk.CTkFont(size=12),
        )
        self.detail_label.grid(row=7, column=0, padx=18, pady=(6, 4), sticky="ew")

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

    @staticmethod
    def _format_multiplier(value):
        return f"{float(value):.1f}x"

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
        self.multiplier_slider.configure(state=state)
        self.other_switch.configure(state=state)
        self.log_switch.configure(state=state)

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
            self._post("log", str(exc))
            self._post("retry_connect")

    def _on_connected(self, pid):
        self._set_connection(True, "已连接游戏", f"PID {pid}")
        self._set_controls_enabled(True)
        self._log("脚本已加载")
        if self.desired_enabled:
            self._rpc_call("enable")
        else:
            self._send_config()
            self._refresh_status()
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
            if payload.get("type") == "log":
                self._post("log", payload.get("message", ""))
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
                    self.script.exports_sync.setconfig(self._current_config())
                    result = self.script.exports_sync.enable()
                elif method == "disable":
                    result = self.script.exports_sync.disable()
                elif method == "status":
                    result = self.script.exports_sync.status()
                elif method == "cleanup":
                    result = self.script.exports_sync.cleanup()
                elif method == "setconfig":
                    result = self.script.exports_sync.setconfig(*args)
                else:
                    raise ValueError(f"unknown rpc method: {method}")
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
        self.desired_enabled = enabled
        self.enable_switch.configure(text="开启" if enabled else "关闭")
        if enabled:
            self._rpc_call("enable")
        else:
            self._rpc_call("disable")

    def _on_multiplier_preview(self, value):
        self.multiplier = round(float(value), 1)
        self.multiplier_label.configure(text=self._format_multiplier(self.multiplier))
        self.after(180, self._send_config)

    def _on_config_changed(self):
        self.allow_other_damage_type = self.other_switch.get() == 1
        self.diagnostic_log = self.log_switch.get() == 1
        self._send_config()

    def _send_config(self):
        if not self.script or self.rpc_busy:
            return
        self._rpc_call("setconfig", self._current_config())

    def _current_config(self):
        return {
            "multiplier": self.multiplier,
            "allow_other_damage_type": self.allow_other_damage_type,
            "diagnostic_log": self.diagnostic_log,
            "skip_local_victim": True,
            "include_infect": False,
            "enable_owner_mapping": True,
        }

    def _render_status(self, status):
        if not isinstance(status, dict):
            return

        enabled = bool(status.get("enabled"))
        self.enabled_label.configure(text="开启" if enabled else "关闭", text_color=GREEN if enabled else "#ddd")
        self.enable_switch.configure(text="开启" if enabled else "关闭")
        if enabled and self.enable_switch.get() == 0:
            self.enable_switch.select()
        if not enabled and self.enable_switch.get() == 1:
            self.enable_switch.deselect()

        self.total_label.configure(text=str(status.get("total_hurt_events", 0)))
        self.multiplied_label.configure(text=str(status.get("multiplied_events", 0)))
        self.owner_label.configure(
            text=f"{status.get('missile_owner_hits', 0)}/{status.get('sentry_owner_hits', 0)}"
        )
        old_damage = float(status.get("last_original_damage", 0.0) or 0.0)
        new_damage = float(status.get("last_new_damage", 0.0) or 0.0)
        self.damage_label.configure(text=f"{old_damage:.1f}->{new_damage:.1f}" if old_damage else "-")
        self.type_label.configure(text=str(status.get("last_damage_type", "-")))
        self.weapon_label.configure(text=str(status.get("last_wpn_index", "-")))
        self.decision_label.configure(text=str(status.get("last_decision", "-"))[:18])
        self.skip_attacker_label.configure(text=str(status.get("skipped_not_local_attacker", 0)))
        self.skip_victim_label.configure(text=str(status.get("skipped_local_victim", 0)))
        self.skip_infect_label.configure(text=str(status.get("skipped_infect", 0)))
        self.error_label.configure(text=str(status.get("error_count", 0)), text_color=RED if status.get("error_count", 0) else "#ddd")

        multiplier = float(status.get("multiplier", self.multiplier) or self.multiplier)
        if abs(multiplier - self.multiplier) > 0.05:
            self.multiplier = multiplier
            self.multiplier_slider.set(multiplier)
            self.multiplier_label.configure(text=self._format_multiplier(multiplier))

        last_error = status.get("last_error") or ""
        detail = (
            f"倍率 {multiplier:.1f}x | source={status.get('last_source', '-')} "
            f"| tag={status.get('last_damage_tag', 0)} | ignoreDmgRate={status.get('last_ignore_dmg_rate', False)}"
        )
        if last_error:
            detail += " | " + last_error
        self.detail_label.configure(text=detail)

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
    app = DamageMultiplierApp()
    app.mainloop()
