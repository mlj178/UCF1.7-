"""独立测试 UI —— 伤害吸血 (lifesteal)。

脱离整合包单独测试用：自动连接 UnityCrossFire.exe，加载同目录的 script.js，
提供总开关 / 吸血比例滑条 / 伤害来源开关 / 状态 / 日志。

正式版入口见 manifest.json 与 panel.py；本文件不接入整合包。
"""

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
GAME_PROCESS_NAME = "UnityCrossFire.exe"

GREEN = "#2ecc71"
ORANGE = "#f39c12"
RED = "#e74c3c"
PANEL = "#1d2430"
PANEL_DARK = "#161c26"

CATEGORY_LABELS = {
    "gun_primary": "主武器",
    "gun_secondary": "副武器",
    "gun_stock": "枪托重击",
    "knife": "近战武器",
    "grenade": "投掷/爆炸",
    "special": "特殊/技能",
    "infect": "感染",
}

SOURCES = (
    ("gun_primary", "主武器", "步枪/狙击/机枪/冲锋枪/霰弹枪", "#f87171"),
    ("gun_secondary", "副武器", "手枪", "#fb923c"),
    ("gun_stock", "枪托重击", "枪械近战", "#fbbf24"),
    ("knife", "近战武器", "刀 / 英雄近战", "#a78bfa"),
    ("grenade", "投掷/爆炸", "手雷 / RPG / 榴弹", "#60a5fa"),
    ("special", "特殊/技能", "其它伤害类型", "#34d399"),
    ("infect", "感染", "生化感染（默认关）", "#94a3b8"),
)

DEFAULT_CONFIG = {
    "lifesteal_percent": 10,
    "src_gun_primary_enabled": True,
    "src_gun_secondary_enabled": True,
    "src_gun_stock_enabled": True,
    "src_knife_enabled": True,
    "src_grenade_enabled": True,
    "src_special_enabled": True,
    "src_infect_enabled": False,
    "only_enemy_victim": True,
    "diagnostic_log": True,
    "max_pending_heal": 5000,
}


class LifestealApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("伤害吸血 - 独立测试")
        self.geometry("820x860")
        self.minsize(720, 760)

        self.session = None
        self.script = None
        self.connected = False
        self.connecting = False
        self.closing = False
        self.rpc_busy = False
        self.status_busy = False
        self.shutdown_done = False
        self.desired_enabled = False
        self.config_job = None
        self.status_job = None

        self.config = dict(DEFAULT_CONFIG)

        self.rpc_lock = threading.Lock()
        self.ui_queue = queue.Queue()

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._drain_ui_queue)
        self.after(600, self._schedule_connect)

    # ==================== UI 构建 ====================

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)

        ctk.CTkLabel(
            self, text="伤害吸血", font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=18, pady=(16, 2), sticky="ew")

        ctk.CTkLabel(
            self,
            text="按「实际扣掉的血量 × 吸血比例」回复自身血量；来源可分别开关。",
            text_color="#8f98a8", font=ctk.CTkFont(size=12),
        ).grid(row=1, column=0, padx=18, pady=(0, 6), sticky="ew")

        # 连接状态栏
        status = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        status.grid(row=2, column=0, padx=18, pady=4, sticky="ew")
        status.grid_columnconfigure(1, weight=1)

        self.status_dot = ctk.CTkLabel(status, text="●", text_color="#777")
        self.status_dot.grid(row=0, column=0, padx=(12, 5), pady=8)
        self.connection_label = ctk.CTkLabel(status, text="等待游戏启动...")
        self.connection_label.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        self.pid_label = ctk.CTkLabel(status, text="", text_color="#999")
        self.pid_label.grid(row=0, column=2, padx=12, pady=8)

        # 控制面板
        controls = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL_DARK)
        controls.grid(row=3, column=0, padx=18, pady=4, sticky="ew")
        controls.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(controls, text="功能开关", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, padx=12, pady=10, sticky="w")
        self.enable_switch = ctk.CTkSwitch(
            controls, text="关闭", command=self._on_enable_changed,
            progress_color=GREEN, switch_width=50, switch_height=24,
        )
        self.enable_switch.grid(row=0, column=1, padx=12, pady=10, sticky="w")

        ctk.CTkLabel(controls, text="吸血比例", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=1, column=0, padx=12, pady=(2, 10), sticky="w")

        slider_row = ctk.CTkFrame(controls, fg_color="transparent")
        slider_row.grid(row=1, column=1, padx=12, pady=(2, 10), sticky="ew")
        slider_row.grid_columnconfigure(0, weight=1)

        self.percent_slider = ctk.CTkSlider(
            slider_row, from_=0, to=100, number_of_steps=100, command=self._on_percent_change,
        )
        self.percent_slider.set(self.config["lifesteal_percent"])
        self.percent_slider.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.percent_label = ctk.CTkLabel(
            slider_row, text=f"{self.config['lifesteal_percent']}%", width=58,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.percent_label.grid(row=0, column=1, sticky="e")

        # 伤害来源
        sources = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        sources.grid(row=4, column=0, padx=18, pady=4, sticky="ew")
        sources.grid_columnconfigure(0, weight=1)
        sources.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            sources, text="伤害来源", font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, columnspan=2, padx=12, pady=(8, 2), sticky="w")

        self.source_vars = {}
        self.source_switches = {}
        for index, (key, name, hint, color) in enumerate(SOURCES):
            cell = ctk.CTkFrame(sources, fg_color="transparent")
            cell.grid(row=1 + index // 2, column=index % 2, padx=10, pady=3, sticky="ew")
            cell.grid_columnconfigure(0, weight=1)

            var = ctk.BooleanVar(value=bool(self.config.get(f"src_{key}_enabled")))
            self.source_vars[key] = var

            label = ctk.CTkLabel(
                cell, text=name, font=ctk.CTkFont(size=12, weight="bold"),
                text_color=color, anchor="w",
            )
            label.grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(
                cell, text=hint, font=ctk.CTkFont(size=10), text_color="#7c8595", anchor="w",
            ).grid(row=1, column=0, sticky="w")

            switch = ctk.CTkSwitch(
                cell, text="", width=40, variable=var,
                command=lambda k=key: self._on_source_changed(k),
            )
            switch.grid(row=0, column=1, rowspan=2, padx=(6, 0), sticky="e")
            self.source_switches[key] = switch

        enemy_row = ctk.CTkFrame(sources, fg_color="transparent")
        enemy_row.grid(row=5, column=0, columnspan=2, padx=10, pady=(6, 10), sticky="ew")
        enemy_row.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            enemy_row, text="只吸敌人（打队友 / 自己不掉血也不吸血）",
            font=ctk.CTkFont(size=12), text_color="#a0a0a0", anchor="w",
        ).grid(row=0, column=0, sticky="w")
        self.enemy_var = ctk.BooleanVar(value=bool(self.config.get("only_enemy_victim", True)))
        self.enemy_switch = ctk.CTkSwitch(
            enemy_row, text="", width=40, variable=self.enemy_var,
            command=self._on_enemy_victim_changed,
        )
        self.enemy_switch.grid(row=0, column=1, sticky="e")

        # 指标
        metrics = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        metrics.grid(row=5, column=0, padx=18, pady=4, sticky="ew")
        metrics.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.enabled_label = self._add_metric(metrics, 0, "功能状态", "关闭")
        self.events_label = self._add_metric(metrics, 1, "伤害事件", "0")
        self.heal_count_label = self._add_metric(metrics, 2, "吸血次数", "0")
        self.healed_total_label = self._add_metric(metrics, 3, "累计回血", "0")
        self.hp_label = self._add_metric(metrics, 4, "自身血量", "-")
        self.error_label = self._add_metric(metrics, 5, "错误", "0")

        self.result_label = ctk.CTkLabel(
            self, text="就绪", text_color="#9aa3b2", font=ctk.CTkFont(size=12),
            anchor="w", justify="left",
        )
        self.result_label.grid(row=6, column=0, padx=18, pady=(6, 2), sticky="ew")

        self.source_stats_label = ctk.CTkLabel(
            self, text="", text_color="#7c8595", font=ctk.CTkFont(size=11),
            anchor="w", justify="left",
        )
        self.source_stats_label.grid(row=7, column=0, padx=18, pady=(0, 4), sticky="ew")

        # 日志
        self.log_box = ctk.CTkTextbox(self, height=180, font=ctk.CTkFont(size=11))
        self.log_box.grid(row=8, column=0, padx=18, pady=(2, 14), sticky="nsew")
        self.log_box.configure(state="disabled")

        self._set_controls_enabled(False)

    def _add_metric(self, parent, column, title, value):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=column, padx=6, pady=8, sticky="ew")
        ctk.CTkLabel(frame, text=title, text_color="#8f98a8", font=ctk.CTkFont(size=11)).pack()
        label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=15, weight="bold"))
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
        self.percent_slider.configure(state=state)
        self.enemy_switch.configure(state=state)
        for switch in self.source_switches.values():
            switch.configure(state=state)

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
        if self.status_job is not None:
            try:
                self.after_cancel(self.status_job)
            except Exception:
                pass
        self._push_config_now()
        if self.desired_enabled:
            self._rpc_call("enable")
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
            return
        if message.get("type") == "error":
            self._post("log", message.get("stack", message.get("description", "Frida error")))

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
                if method == "enable":
                    self.script.exports_sync.setconfig(self._current_config())
                    result = self.script.exports_sync.enable()
                elif method == "disable":
                    result = self.script.exports_sync.disable()
                elif method == "status":
                    result = self.script.exports_sync.status()
                elif method == "setconfig":
                    result = self.script.exports_sync.setconfig(self._current_config())
                elif method == "cleanup":
                    result = self.script.exports_sync.cleanup()
                elif method == "reset":
                    result = self.script.exports_sync.reset("ui_reset")
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
            self.status_job = self.after(1000, self._schedule_status_poll)

    # ==================== 控件回调 ====================

    def _on_enable_changed(self):
        enabled = self.enable_switch.get() == 1
        self.desired_enabled = enabled
        self.enable_switch.configure(text="开启" if enabled else "关闭")
        if enabled:
            self._rpc_call("enable")
        else:
            self._rpc_call("disable")

    def _on_percent_change(self, value):
        numeric = int(round(float(value)))
        self.config["lifesteal_percent"] = numeric
        self.percent_label.configure(text=f"{numeric}%")
        self._schedule_config_push()

    def _on_source_changed(self, key):
        self.config[f"src_{key}_enabled"] = bool(self.source_vars[key].get())
        self._schedule_config_push()

    def _on_enemy_victim_changed(self):
        self.config["only_enemy_victim"] = bool(self.enemy_var.get())
        self._schedule_config_push()

    def _schedule_config_push(self):
        if self.config_job is not None:
            try:
                self.after_cancel(self.config_job)
            except Exception:
                pass
        self.config_job = self.after(150, self._push_config_now)

    def _push_config_now(self):
        self.config_job = None
        if not self.script:
            return
        config = self._current_config()
        threading.Thread(target=self._config_worker, args=(config,), daemon=True).start()

    def _config_worker(self, config):
        with self.rpc_lock:
            try:
                self.script.exports_sync.setconfig(config)
            except Exception as exc:
                self._post("log", "配置下发失败：" + str(exc))

    def _current_config(self):
        return dict(self.config)

    # ==================== 状态渲染 ====================

    def _render_status(self, status):
        if not isinstance(status, dict):
            return

        enabled = bool(status.get("enabled"))
        initialized = bool(status.get("initialized"))
        self.enabled_label.configure(
            text="开启" if enabled else "关闭",
            text_color=GREEN if enabled and initialized else ("#f39c12" if enabled else "#ddd"),
        )
        self.enable_switch.configure(text="开启" if enabled else "关闭")
        if enabled and self.enable_switch.get() == 0:
            self.enable_switch.select()
        if not enabled and self.enable_switch.get() == 1:
            self.enable_switch.deselect()

        self.events_label.configure(text=str(status.get("local_damage_events", 0)))
        self.heal_count_label.configure(text=str(status.get("heal_calls", 0)))
        self.healed_total_label.configure(text=str(status.get("healed_total", 0)))

        hp = status.get("local_hp", -1)
        max_hp = status.get("local_max_hp", -1)
        if isinstance(hp, int) and hp >= 0:
            self.hp_label.configure(text=f"{hp}/{max_hp}" if max_hp >= 0 else str(hp))
        else:
            self.hp_label.configure(text="-")

        errors = status.get("error_count", 0)
        self.error_label.configure(text=str(errors), text_color=RED if errors else "#ddd")

        percent = int(round(float(status.get("lifesteal_percent", self.config["lifesteal_percent"]))))
        if percent != self.config["lifesteal_percent"]:
            self.config["lifesteal_percent"] = percent
            self.percent_slider.set(percent)
            self.percent_label.configure(text=f"{percent}%")

        category_key = status.get("last_category") or ""
        category = CATEGORY_LABELS.get(category_key, category_key) or "-"
        wpn_name = status.get("last_wpn_name") or ""
        decision = status.get("last_decision") or "-"
        parts = [
            f"最近: {category}",
            f"武器 {wpn_name or status.get('last_wpn_index', -1)}",
            f"伤害 {status.get('last_damage', 0)}",
            f"回血 +{status.get('last_heal', 0)}",
            f"HP {status.get('local_hp', -1)}/{status.get('local_max_hp', -1)}",
            f"判定 {decision}",
        ]
        if status.get("last_error"):
            parts.append("错误 " + str(status.get("last_error")))
        self.result_label.configure(text=" ｜ ".join(parts))

        stats_parts = []
        for key, name, _hint, _color in SOURCES:
            healed = status.get(f"healed_{key}", 0)
            if healed:
                stats_parts.append(f"{name} +{healed}")
        pending = status.get("pending_heal", 0)
        self.source_stats_label.configure(
            text=("分类累计回血: " + ("、".join(stats_parts) if stats_parts else "暂无")) +
            f" ｜ 待结算 {float(pending):.2f}"
        )

    # ==================== 关闭 ====================

    def _on_close(self):
        if self.shutdown_done:
            return
        self.shutdown_done = True
        self.closing = True
        self._set_controls_enabled(False)
        for job in (self.config_job, self.status_job):
            if job is not None:
                try:
                    self.after_cancel(job)
                except Exception:
                    pass
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
    app = LifestealApp()
    app.mainloop()
