"""Standalone CustomTkinter UI for 33-生化幽灵专区."""

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
JS_FILE = os.path.join(BASE_DIR, "AAAAA-bio_ghost_boost_min.js")
GAME_PROCESS_NAME = "UnityCrossFire.exe"

GREEN = "#2ecc71"
ORANGE = "#f39c12"
RED = "#e74c3c"
PANEL = "#1d2430"
PANEL_DARK = "#161c26"


SLIDER_DEFS = (
    ("承伤倍率", "damage_taken_multiplier", 0.1, 3.0, 0.5, "本地幽灵受到伤害倍率"),
    ("攻击倍率", "attack_damage_multiplier", 0.1, 10.0, 1.5, "本地幽灵造成伤害倍率"),
    ("移动倍率", "move_speed_multiplier", 0.5, 4.0, 1.4, "本地幽灵移动速度倍率"),
    ("刀速倍率", "knife_speed_multiplier", 0.5, 6.0, 1.5, "本地幽灵近战速度倍率"),
    ("刀距倍率", "knife_range_multiplier", 0.5, 5.0, 1.4, "本地幽灵近战范围倍率"),
    ("击退倍率", "knockback_multiplier", 0.0, 3.0, 0.5, "实验项：受击速度反馈倍率"),
)


class BioGhostBoostApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("33-生化幽灵专区")
        self.geometry("720x720")
        self.minsize(660, 620)

        self.session = None
        self.script = None
        self.connected = False
        self.connecting = False
        self.closing = False
        self.rpc_busy = False
        self.status_busy = False
        self.shutdown_done = False
        self.desired_enabled = False

        self.values = {key: default for _, key, _, _, default, _ in SLIDER_DEFS}
        self.skill_no_cooldown = True
        self.diagnostic_log = True

        self.rpc_lock = threading.Lock()
        self.ui_queue = queue.Queue()
        self.slider_labels = {}
        self.slider_widgets = {}

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._drain_ui_queue)
        self.after(600, self._schedule_connect)

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)

        ctk.CTkLabel(
            self,
            text="33-生化幽灵专区",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=18, pady=(18, 4), sticky="ew")

        ctk.CTkLabel(
            self,
            text="本地玩家成为生化幽灵时，统一调节伤害、速度、近战、技能冷却与击退反馈。",
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

        sliders = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        sliders.grid(row=4, column=0, padx=18, pady=5, sticky="ew")
        sliders.grid_columnconfigure(1, weight=1)

        for row, (title, key, min_value, max_value, default, desc) in enumerate(SLIDER_DEFS):
            ctk.CTkLabel(
                sliders,
                text=title,
                font=ctk.CTkFont(size=13, weight="bold"),
                width=76,
                anchor="w",
            ).grid(row=row, column=0, padx=(12, 4), pady=7, sticky="w")

            slider = ctk.CTkSlider(
                sliders,
                from_=min_value,
                to=max_value,
                number_of_steps=int((max_value - min_value) * 10),
                command=lambda value, cfg_key=key: self._on_slider_changed(cfg_key, value),
            )
            slider.set(default)
            slider.grid(row=row, column=1, padx=8, pady=7, sticky="ew")
            self.slider_widgets[key] = slider

            label = ctk.CTkLabel(
                sliders,
                text=f"{default:.1f}x",
                width=52,
                font=ctk.CTkFont(size=13, weight="bold"),
            )
            label.grid(row=row, column=2, padx=(4, 12), pady=7, sticky="e")
            self.slider_labels[key] = label

            ctk.CTkLabel(
                sliders,
                text=desc,
                text_color="#8f98a8",
                font=ctk.CTkFont(size=11),
                anchor="w",
            ).grid(row=row, column=3, padx=(0, 12), pady=7, sticky="w")

        extra = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL_DARK)
        extra.grid(row=5, column=0, padx=18, pady=5, sticky="ew")
        extra.grid_columnconfigure((0, 1), weight=1)

        self.skill_switch = ctk.CTkSwitch(
            extra,
            text="技能无冷却",
            command=self._on_config_changed,
            progress_color=GREEN,
            switch_width=50,
            switch_height=24,
        )
        self.skill_switch.select()
        self.skill_switch.grid(row=0, column=0, padx=12, pady=12, sticky="w")

        self.log_switch = ctk.CTkSwitch(
            extra,
            text="诊断日志",
            command=self._on_config_changed,
            progress_color=GREEN,
            switch_width=50,
            switch_height=24,
        )
        self.log_switch.select()
        self.log_switch.grid(row=0, column=1, padx=12, pady=12, sticky="w")

        metrics = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        metrics.grid(row=6, column=0, padx=18, pady=5, sticky="ew")
        metrics.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.enabled_label = self._add_metric(metrics, 0, "功能状态", "关闭")
        self.damage_label = self._add_metric(metrics, 1, "伤害修改", "0")
        self.move_label = self._add_metric(metrics, 2, "移速命中", "0")
        self.knife_label = self._add_metric(metrics, 3, "近战命中", "0/0")
        self.knockback_label = self._add_metric(metrics, 4, "击退命中", "0")

        self.detail_label = ctk.CTkLabel(
            self,
            text="等待连接游戏",
            text_color="#9aa3b2",
            font=ctk.CTkFont(size=12),
        )
        self.detail_label.grid(row=7, column=0, padx=18, pady=(6, 4), sticky="ew")

        self.log_box = ctk.CTkTextbox(self, height=170, font=ctk.CTkFont(size=11))
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
        self.skill_switch.configure(state=state)
        self.log_switch.configure(state=state)
        for slider in self.slider_widgets.values():
            slider.configure(state=state)

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

            if not os.path.exists(JS_FILE):
                raise FileNotFoundError(JS_FILE)

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
        self._log("生化幽灵专区脚本已加载")
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
                    result = self.script.exports_sync.enable(self._current_config())
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
        self._rpc_call("enable" if enabled else "disable")

    def _on_slider_changed(self, key, value):
        rounded = round(float(value), 1)
        self.values[key] = rounded
        self.slider_labels[key].configure(text=f"{rounded:.1f}x")
        self.after(180, self._send_config)

    def _on_config_changed(self):
        self.skill_no_cooldown = self.skill_switch.get() == 1
        self.diagnostic_log = self.log_switch.get() == 1
        self._send_config()

    def _send_config(self):
        if not self.script or self.rpc_busy:
            return
        self._rpc_call("setconfig", self._current_config())

    def _current_config(self):
        config = dict(self.values)
        config.update(
            {
                "skill_no_cooldown": self.skill_no_cooldown,
                "include_infect_damage": False,
                "use_no_hit_feedback_when_zero_knockback": True,
                "diagnostic_log": self.diagnostic_log,
            }
        )
        return config

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

        self.damage_label.configure(text=str(status.get("damage_changed", 0)))
        self.move_label.configure(text=str(status.get("move_changed", 0)))
        self.knife_label.configure(
            text=f"{status.get('knife_speed_changed', 0)}/{status.get('knife_range_changed', 0)}"
        )
        self.knockback_label.configure(text=str(status.get("knockback_changed", 0)))

        config = status.get("config") or {}
        for key, value in config.items():
            if key in self.values:
                value = round(float(value), 1)
                if abs(self.values[key] - value) > 0.05:
                    self.values[key] = value
                    self.slider_widgets[key].set(value)
                    self.slider_labels[key].configure(text=f"{value:.1f}x")

        errors = int(status.get("errors", 0) or 0)
        last_error = status.get("last_error") or ""
        last_decision = status.get("last_decision") or "-"
        detail = (
            f"初始化={status.get('initialized', False)} | "
            f"模块={status.get('module_found', False)} | "
            f"本地玩家={status.get('local_player_seen', 0)} | "
            f"幽灵命中={status.get('local_ghost_seen', 0)} | "
            f"幽灵标记={status.get('last_is_ghost_value', False)} | "
            f"本地幽灵受击={status.get('local_ghost_hits', 0)} | "
            f"技能刷新={status.get('skill_cold_ended', 0)} | "
            f"最近={last_decision}"
        )
        if last_error:
            detail += " | " + last_error
        self.detail_label.configure(text=detail, text_color=RED if errors else "#9aa3b2")

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
    BioGhostBoostApp().mainloop()
