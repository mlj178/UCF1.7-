"""开火直伤 —— 05 本地调试 UI（整合包不接入本文件）。"""

import hashlib
import json
import os
import queue
import tempfile
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

# 目标选择模式：与 script.js 的 config.target_mode 保持一致
TARGET_MODES = {
    "准星方向 + 距离最近": "angle_then_distance",
    "角度/距离加权": "weighted",
    "仅取最近(调试)": "nearest",
}

# 伤害注入入口：与 script.js 的 config.damage_entry 保持一致
#   hurt 排第一是因为它是唯一被验证过的入口：
#     IDA 反汇编确认 Entity.OnEntityHurt 内部就是
#       HealthData.Hurt(this.healthData, (int)eventData.damage)
#     且整合包 2.7 的"增加伤害倍率"功能就挂在这两个入口上工作。
DAMAGE_ENTRIES = {
    "实体受伤入口(推荐)": "hurt",
    "统一伤害入口": "gamemanager",
    "仅扣血(兜底)": "health",
    "空跑不伤害(调试)": "dry_run",
}

# 逆向分析所用的 GameAssembly.dll，用于比对当前游戏版本
EXPECTED_MODULE_MD5 = "fab04426db6a014c0129ef2001530908"


class DirectDamageApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("开火直伤 - 独立测试")
        self.geometry("760x900")
        self.minsize(700, 720)

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
        self.script_log_path = self._new_script_log_path()
        self.module_info = ""
        self._write_log_file("session_start feature=direct_damage")
        self._write_log_file("script_log=" + (self.script_log_path or "(空：由 script.js 兜底到游戏目录)"))
        self._write_log_file("expected_module_md5=" + EXPECTED_MODULE_MD5)
        self._suspend_config_sync = True

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._drain_ui_queue)
        self.after(600, self._schedule_connect)
        self._suspend_config_sync = False

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(9, weight=1)

        ctk.CTkLabel(
            self, text="开火直伤", font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=18, pady=(18, 4), sticky="ew")

        ctk.CTkLabel(
            self,
            text="开火不走子弹射线，直接把伤害结算到准星方向距离最近的敌人",
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
        controls.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(controls, text="功能总开关", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, padx=12, pady=12, sticky="w")
        self.enable_switch = ctk.CTkSwitch(
            controls, text="关闭", command=self._on_enable_changed,
            progress_color=GREEN, switch_width=50, switch_height=24,
        )
        self.enable_switch.grid(row=0, column=1, padx=12, pady=12, sticky="e")

        # 三个独立开关
        self.guns_switch = self._add_config_switch(controls, 1, "常规枪械直伤", "enable_guns", True)
        self.explosives_switch = self._add_config_switch(
            controls, 2, "榴弹/手雷/RPG 直伤", "enable_explosives", True)
        self.skills_switch = self._add_config_switch(
            controls, 3, "特殊技能弹直伤", "enable_skill_projectiles", True)

        ctk.CTkLabel(controls, text="伤害入口", text_color="#8f98a8").grid(
            row=4, column=0, padx=12, pady=(8, 4), sticky="w")
        self.entry_menu = ctk.CTkOptionMenu(
            controls, values=list(DAMAGE_ENTRIES.keys()), command=self._on_entry_changed,
            fg_color="#1f2937", button_color="#374151", width=220,
        )
        self.entry_menu.grid(row=4, column=1, padx=12, pady=(8, 4), sticky="e")

        ctk.CTkLabel(controls, text="打谁策略", text_color="#8f98a8").grid(
            row=5, column=0, padx=12, pady=(4, 12), sticky="w")
        self.mode_menu = ctk.CTkOptionMenu(
            controls, values=list(TARGET_MODES.keys()), command=self._on_mode_changed,
            fg_color="#1f2937", button_color="#374151", width=220,
        )
        self.mode_menu.grid(row=5, column=1, padx=12, pady=(4, 4), sticky="e")

        # 探针模式：只选目标 + 记日志，绝不注入任何伤害，原版弹道照常走。
        # 用来安全地回答"钩子有没有命中 / 能不能选到敌人"这两个问题。
        ctk.CTkLabel(controls, text="探针模式（不改玩法，只记录）", text_color="#c8d0dc").grid(
            row=6, column=0, padx=12, pady=(0, 12), sticky="w")
        self.probe_only_switch = ctk.CTkSwitch(
            controls, text="", progress_color="#f0a020", switch_width=50, switch_height=24,
        )
        self.probe_only_switch.grid(row=6, column=1, padx=12, pady=(0, 12), sticky="e")
        self.probe_only_switch.configure(command=self._on_probe_only_changed)

        # 参数滑块
        params = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        params.grid(row=4, column=0, padx=18, pady=5, sticky="ew")
        params.grid_columnconfigure(1, weight=1)

        self.angle_slider, self.angle_label = self._add_slider(
            params, 0, "准星锥角度(度)", "max_angle_deg", 5, 120, 1, 30)
        self.distance_slider, self.distance_label = self._add_slider(
            params, 1, "最大距离(米, 0=不限)", "max_distance", 0, 200, 5, 80)
        self.multiplier_slider, self.multiplier_label = self._add_slider(
            params, 2, "直伤倍率", "damage_multiplier", 1, 20, 1, 1)

        # 统计
        metrics = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        metrics.grid(row=5, column=0, padx=18, pady=5, sticky="ew")
        metrics.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        self.enabled_label = self._add_metric(metrics, 0, "功能状态", "关闭")
        self.selected_label = self._add_metric(metrics, 1, "选中目标", "0")
        self.damage_label = self._add_metric(metrics, 2, "造成伤害", "0")
        self.notarget_label = self._add_metric(metrics, 3, "无目标", "0")
        self.angle_stat_label = self._add_metric(metrics, 4, "最近夹角", "-")
        self.error_label = self._add_metric(metrics, 5, "错误", "0")
        # 探针指标：这两个是"功能到底成不成"的直接证据
        self.hook_label = self._add_metric(metrics, 6, "钩子命中", "0")
        self.hp_label = self._add_metric(metrics, 7, "HP对照(降)", "-")

        # ---- 诊断探针面板 ----
        probe = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        probe.grid(row=6, column=0, padx=18, pady=5, sticky="ew")
        probe.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(probe, text="诊断探针", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, padx=12, pady=(10, 2), sticky="w")

        self.probe_label = ctk.CTkLabel(
            probe, text="待开启", text_color="#8f98a8",
            font=ctk.CTkFont(size=11), anchor="w", justify="left",
            wraplength=700,
        )
        self.probe_label.grid(row=1, column=0, padx=12, pady=(0, 6), sticky="ew")

        self.log_file_label = ctk.CTkLabel(
            probe, text="脚本日志: -", text_color="#6b7280",
            font=ctk.CTkFont(size=10), anchor="w", justify="left", wraplength=700,
        )
        self.log_file_label.grid(row=2, column=0, padx=12, pady=(0, 8), sticky="ew")

        buttons = ctk.CTkFrame(probe, fg_color="transparent")
        buttons.grid(row=3, column=0, padx=12, pady=(0, 12), sticky="w")
        ctk.CTkButton(buttons, text="拉取脚本日志", command=self._pull_script_logs, width=120).pack(
            side="left", padx=(0, 8))
        ctk.CTkButton(
            buttons, text="清空脚本日志", command=self._clear_script_logs, width=120,
            fg_color="#374151", hover_color="#4b5563").pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            buttons, text="打世界快照", command=self._snapshot, width=110,
            fg_color="#374151", hover_color="#4b5563").pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            buttons, text="打开日志目录", command=self._open_log_dir, width=110,
            fg_color="#374151", hover_color="#4b5563").pack(side="left")

        self.result_label = ctk.CTkLabel(
            self, text="就绪", text_color="#9aa3b2", font=ctk.CTkFont(size=12),
        )
        self.result_label.grid(row=7, column=0, padx=18, pady=(6, 4), sticky="ew")

        self.hint_label = ctk.CTkLabel(
            self,
            text=("排查顺序：① 开「探针模式」开枪 —— 看「钩子命中」是否 >0；"
                  "② 再看「HP对照(降)」是否 >0；③ 都不动就点「拉取脚本日志」把日志发我。"),
            text_color="#f0a020", font=ctk.CTkFont(size=11), wraplength=700,
            justify="left", anchor="w",
        )
        self.hint_label.grid(row=8, column=0, padx=18, pady=(0, 4), sticky="ew")

        self.log_box = ctk.CTkTextbox(self, height=220, font=ctk.CTkFont(size=11))
        self.log_box.grid(row=9, column=0, padx=18, pady=(4, 16), sticky="nsew")
        self.log_box.configure(state="disabled")

        self._set_controls_enabled(False)

    def _add_config_switch(self, parent, row, label, config_key, default):
        ctk.CTkLabel(parent, text=label, text_color="#c8d0dc").grid(
            row=row, column=0, padx=12, pady=4, sticky="w")
        switch = ctk.CTkSwitch(
            parent, text="", progress_color=GREEN, switch_width=50, switch_height=24,
        )
        switch.grid(row=row, column=1, padx=12, pady=4, sticky="e")
        if default:
            switch.select()
        switch.configure(
            command=lambda key=config_key, widget=switch: self._on_config_changed(key, bool(widget.get()))
        )
        return switch

    def _add_slider(self, parent, row, title, config_key, minimum, maximum, step, default):
        ctk.CTkLabel(parent, text=title, text_color="#c8d0dc").grid(
            row=row, column=0, padx=12, pady=(10, 2), sticky="w")
        label = ctk.CTkLabel(parent, text=str(default), text_color=GREEN)
        label.grid(row=row, column=2, padx=12, pady=(10, 2), sticky="e")
        slider = ctk.CTkSlider(
            parent, from_=minimum, to=maximum,
            number_of_steps=max(1, int(round((maximum - minimum) / step))),
            progress_color=GREEN,
        )
        slider.set(default)
        slider.grid(row=row, column=1, padx=12, pady=(10, 2), sticky="ew")
        slider.configure(command=lambda value, key=config_key, lbl=label: self._on_slider_changed(
            key, value, lbl))
        return slider, label

    def _on_slider_changed(self, key, value, label):
        label.configure(text=f"{float(value):.0f}")
        self._on_config_changed(key, float(value))

    def _add_metric(self, parent, column, title, value):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=column, padx=4, pady=10, sticky="ew")
        ctk.CTkLabel(frame, text=title, text_color="#8f98a8", font=ctk.CTkFont(size=10)).pack()
        label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(pady=(2, 0))
        return label

    # ------------------------------------------------------------------
    # 事件泵
    # ------------------------------------------------------------------
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
        elif event == "rpc_logs":
            self.rpc_busy = False
            lines = [str(x) for x in (args[0] if args else [])]
            # 全部写进磁盘日志，界面里只显示尾部，避免卡 UI
            self._write_log_file(f"==== 脚本端日志导出（共 {len(lines)} 行） ====")
            for line in lines:
                self._write_log_file(line)
            for line in lines[-300:]:
                self._log_display_only(line)
            self._log(f"已从脚本端导出 {len(lines)} 行到 {os.path.basename(self.log_path)}")
            self._set_controls_enabled(self.connected)
        elif event == "destroy":
            self.destroy()

    # ------------------------------------------------------------------
    # 日志
    # ------------------------------------------------------------------
    @staticmethod
    def _open_log_file():
        os.makedirs(LOG_DIR, exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(LOG_DIR, f"direct_damage_ui_{stamp}.log")
        open(path, "a", encoding="utf-8").close()
        return path

    @staticmethod
    def _new_script_log_path():
        """脚本端（Frida）持久化日志的落盘路径，由 script.js 自己写文件。

        注意：Frida 的 File API **打不开含中文的路径**（会报 'Illegal byte sequence'），
        而本功能目录是「05-正式功能/40-开火直伤」——路径里必然有中文，
        所以这里改放到系统临时目录（纯 ASCII）。script.js 内部还有一层兜底：
        路径打不开就写到 GameAssembly.dll 同目录的 direct_damage_script.log。
        UI 自己那份日志（logs/direct_damage_ui_*.log）不受影响，且包含脚本端全部输出。
        """
        stamp = time.strftime("%Y%m%d_%H%M%S")
        candidate = os.path.join(tempfile.gettempdir(), f"ucf_direct_damage_script_{stamp}.log")
        try:
            candidate.encode("ascii")
        except UnicodeEncodeError:
            return ""
        return candidate

    @staticmethod
    def _module_identity():
        """比对游戏目录里的 GameAssembly.dll 与逆向分析版本。

        如果 md5 不一致，说明 script.js 里的所有 RVA 都可能失效，
        这时候任何"没效果"都只需要重新做静态分析，不用再折腾逻辑。
        """
        try:
            pid = DirectDamageApp._find_game_pid()
            if not pid:
                return "游戏未运行，跳过模块校验"
            exe = psutil.Process(pid).exe()
            dll = os.path.join(os.path.dirname(exe), "GameAssembly.dll")
            if not os.path.isfile(dll):
                return f"未找到 {dll}"
            digest = hashlib.md5()
            with open(dll, "rb") as fp:
                for chunk in iter(lambda: fp.read(1024 * 1024), b""):
                    digest.update(chunk)
            value = digest.hexdigest()
            verdict = ("与逆向分析版本一致" if value == EXPECTED_MODULE_MD5
                       else "*** 与逆向分析版本不一致，RVA 可能全部失效 ***")
            return f"{dll} | md5={value} | {verdict}"
        except Exception as exc:  # noqa: BLE001 - 诊断代码，任何异常都只记录
            return "模块校验失败: " + str(exc)

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

    def _log_display_only(self, text):
        """只往界面日志框里塞，不再重复写磁盘（用于批量导出脚本端日志）。"""
        stamp = time.strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{stamp}] {text}\n")
        self.log_box.configure(state="disabled")

    def _set_connection(self, connected, text, pid_text=""):
        self.status_dot.configure(text_color=GREEN if connected else "#777")
        self.connection_label.configure(text=text)
        self.pid_label.configure(text=pid_text)

    def _set_controls_enabled(self, enabled):
        state = "normal" if enabled and not self.rpc_busy else "disabled"
        self.enable_switch.configure(state=state)

    # ------------------------------------------------------------------
    # 连接
    # ------------------------------------------------------------------
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
            # 版本校验：md5 不一致的话，所有 RVA 都可能失效（在后台线程里算，避免卡 UI）
            self._post("log", "游戏模块: " + self._module_identity())
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
        self._push_config()
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

    # ------------------------------------------------------------------
    # RPC
    # ------------------------------------------------------------------
    def _current_config(self):
        probe_only = bool(self.probe_only_switch.get())
        return {
            "enable_guns": bool(self.guns_switch.get()),
            "enable_explosives": bool(self.explosives_switch.get()),
            "enable_skill_projectiles": bool(self.skills_switch.get()),
            "target_mode": TARGET_MODES.get(self.mode_menu.get(), "angle_then_distance"),
            "max_angle_deg": float(self.angle_slider.get()),
            "max_distance": float(self.distance_slider.get()),
            "damage_multiplier": float(self.multiplier_slider.get()),
            # 探针模式 = 空跑 + 原版弹道照常走，保证"只观察、不改玩法"
            "damage_entry": "dry_run" if probe_only
            else DAMAGE_ENTRIES.get(self.entry_menu.get(), "hurt"),
            "fallback_to_original": probe_only,
            # 持久化日志与探针（默认开）
            "verbose_probe": True,
            "diagnostic_log": True,
            "log_to_file": True,
            "log_file": self.script_log_path,
        }

    def _push_config(self):
        if not self.script:
            return
        config = self._current_config()
        self._log("下发配置: " + json.dumps(config, ensure_ascii=False))

        def worker():
            with self.rpc_lock:
                try:
                    self.script.exports_sync.setconfig(config)
                except Exception as exc:
                    self._post("log", "配置同步失败：" + str(exc))

        threading.Thread(target=worker, daemon=True).start()

    def _on_config_changed(self, key, value):
        if self._suspend_config_sync or not self.script:
            return
        self._log(f"配置 {key} = {value}")

        def worker():
            with self.rpc_lock:
                try:
                    self.script.exports_sync.setconfig({key: value})
                except Exception as exc:
                    self._post("log", "配置同步失败：" + str(exc))

        threading.Thread(target=worker, daemon=True).start()

    def _on_entry_changed(self, _value):
        self._on_config_changed("damage_entry", DAMAGE_ENTRIES.get(self.entry_menu.get()))

    def _on_mode_changed(self, _value):
        self._on_config_changed("target_mode", TARGET_MODES.get(self.mode_menu.get()))

    def _on_probe_only_changed(self):
        enabled = bool(self.probe_only_switch.get())
        self._log(f"探针模式 = {enabled}"
                  + ("（只记录日志，不改玩法，原版弹道照常生效）" if enabled else ""))
        self._push_config()

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
                elif method == "logs":
                    # 一次性把脚本端内存日志全部拉回来（界面显示尾部，磁盘存全量）
                    self._post("rpc_logs", self.script.exports_sync.logs(0))
                    return
                elif method == "clear_logs":
                    result = self.script.exports_sync.clearLogs()
                elif method == "snapshot":
                    result = self.script.exports_sync.snapshot("ui")
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

    # ------------------------------------------------------------------
    # 交互
    # ------------------------------------------------------------------
    def _on_enable_changed(self):
        enabled = self.enable_switch.get() == 1
        self.enable_switch.configure(text="开启" if enabled else "关闭")
        if enabled:
            self._rpc_call("enable")
        else:
            self._rpc_call("disable")

    def _pull_script_logs(self):
        self._rpc_call("logs")

    def _clear_script_logs(self):
        self._rpc_call("clear_logs")

    def _snapshot(self):
        self._rpc_call("snapshot")

    def _open_log_dir(self):
        try:
            os.startfile(LOG_DIR)  # noqa: S606 - Windows 专用打开目录
        except Exception as exc:  # noqa: BLE001
            self._log("打开日志目录失败: " + str(exc))

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

        self.selected_label.configure(text=str(status.get("targets_selected", 0)))
        self.damage_label.configure(text=str(status.get("damage_applied", 0)))
        self.notarget_label.configure(text=str(status.get("no_target", 0)))
        angle = status.get("last_target_angle", -1)
        self.angle_stat_label.configure(
            text="-" if not isinstance(angle, (int, float)) or angle < 0 else f"{angle:.0f}°")

        errors = status.get("error_count", 0)
        self.error_label.configure(text=str(errors), text_color=RED if errors else "#ddd")

        # 探针指标：这两个是"功能到底成不成"的直接证据
        gun_calls = status.get("gun_damage_calls", 0)
        self.hook_label.configure(
            text=str(gun_calls), text_color=GREEN if gun_calls else "#f0a020")
        checks = status.get("hp_checks", 0)
        dropped = status.get("hp_dropped", 0)
        self.hp_label.configure(
            text=f"{dropped}/{checks}",
            text_color=GREEN if dropped else ("#f0a020" if checks else "#ddd"))

        entry = (status.get("config") or {}).get("damage_entry", "-")
        self.probe_label.configure(text=(
            f"入口={entry}  本地玩家来源={status.get('own_player_source') or '-'}  "
            f"接管开火={status.get('local_gun_fires', 0)}  "
            f"管线 开火{status.get('pipeline_gun_shoot', 0)}"
            f"/统一{status.get('pipeline_take_damage', 0)}"
            f"/实体{status.get('pipeline_entity_hurt', 0)}"
            f"/玩家{status.get('pipeline_player_hurt', 0)}"
            f"/扣血{status.get('pipeline_health_hurt', 0)}  "
            f"HP {status.get('last_hp_before', -1)}→{status.get('last_hp_after', -1)}  "
            f"内存日志={status.get('log_lines', 0)}行"
        ))
        log_file = status.get("log_file") or "(未下发)"
        failed = status.get("log_file_failed") or ""
        self.log_file_label.configure(
            text="脚本日志: " + log_file + (("   写文件失败: " + failed) if failed else ""),
            text_color=RED if failed else "#6b7280")

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
    app = DirectDamageApp()
    app.mainloop()
