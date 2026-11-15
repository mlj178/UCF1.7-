"""路点体检（waypoint_probe）独立启动界面。

不依赖修改器：自己 attach 游戏进程，加载同目录下的 script.js（与修改器功能同源），
通过 Frida RPC 控制 停战 / 跟随 / 人机采样 / 物理探针。
"""

import os
import queue
import sys
import threading
import time
import traceback
import tkinter.filedialog as filedialog

import customtkinter as ctk
import frida
import psutil


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_CANDIDATES = ("script.js", "AAAAA-waypoint_probe_min.js")
LOG_DIR = os.path.join(BASE_DIR, "logs")
GAME_PROCESS_NAME = "UnityCrossFire.exe"

GREEN = "#2ecc71"
ORANGE = "#f39c12"
RED = "#e74c3c"
CYAN = "#22d3ee"
PANEL = "#1d2430"
PANEL_DARK = "#151b24"
DIM = "#8f98a8"

DEFAULT_CONFIG = {
    "pacify": False,
    "freeze": False,
    "follow": False,
    "walk": False,
    "sample_ms": 200,
}

ENABLE_CANDIDATES = ("enable",)
DISABLE_CANDIDATES = ("disable", "cleanup")
SETCONFIG_CANDIDATES = ("setConfig", "setconfig", "set_config")
RUNPROBE_CANDIDATES = ("runProbe", "runprobe", "run_probe")
STATUS_CANDIDATES = ("status",)
SELFTEST_CANDIDATES = ("selfTest", "selftest", "self_test")
CLEANUP_CANDIDATES = ("cleanup", "disable")


def find_js_file():
    for name in JS_CANDIDATES:
        path = os.path.join(BASE_DIR, name)
        if os.path.isfile(path):
            return path
    raise FileNotFoundError("找不到脚本：" + " / ".join(JS_CANDIDATES))


class WaypointProbeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("路点体检 · waypoint_probe")
        self.geometry("760x880")
        self.minsize(700, 780)

        self.session = None
        self.script = None
        self.connected = False
        self.connecting = False
        self.closing = False
        self.rpc_busy = False
        self.status_busy = False
        self.polling = False
        self.shutdown_done = False
        self.enabled = False

        self.ui_queue = queue.Queue()
        self.rpc_lock = threading.Lock()
        self.all_logs = []          # 完整日志（含 EDGES 明细），保存时写这个
        self._edges_hint_shown = False
        self.log_handle = None
        self.log_file_path = ""
        self.verbose_state = False

        self._open_log_file()          # 自动落盘：logs/waypoint-probe-ui-*.log
        self._install_exception_hooks()
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._drain_ui_queue)
        self.after(400, self._schedule_connect)

    # ---------------- UI ----------------
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)

        ctk.CTkLabel(
            self, text="路点体检", font=ctk.CTkFont(family="Microsoft YaHei", size=22, weight="bold")
        ).grid(row=0, column=0, padx=18, pady=(16, 2), sticky="ew")
        ctk.CTkLabel(
            self,
            text="物理探针判定每条路点边的可通行性；停战让 bot 不再打架；跟随让每个阵营派 1 个人机走到你身边",
            font=ctk.CTkFont(family="Microsoft YaHei", size=12),
            text_color=DIM,
            wraplength=700,
            justify="left",
        ).grid(row=1, column=0, padx=18, pady=(0, 8), sticky="ew")

        status = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        status.grid(row=2, column=0, padx=18, pady=4, sticky="ew")
        status.grid_columnconfigure(1, weight=1)
        self.status_dot = ctk.CTkLabel(status, text="●", text_color="#777")
        self.status_dot.grid(row=0, column=0, padx=(12, 5), pady=8)
        self.connection_label = ctk.CTkLabel(
            status, text="等待游戏启动...", font=ctk.CTkFont(family="Microsoft YaHei", size=13)
        )
        self.connection_label.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        self.pid_label = ctk.CTkLabel(status, text="", text_color=DIM)
        self.pid_label.grid(row=0, column=2, padx=12, pady=8)

        metrics = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL_DARK)
        metrics.grid(row=3, column=0, padx=18, pady=4, sticky="ew")
        metrics.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.node_label = self._add_metric(metrics, 0, "路点边", "-")
        self.bot_label = self._add_metric(metrics, 1, "人机", "-")
        self.follow_label = self._add_metric(metrics, 2, "跟随中", "-")
        self.sample_label = self._add_metric(metrics, 3, "采样/过边", "-")

        controls = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        controls.grid(row=4, column=0, padx=18, pady=4, sticky="ew")
        controls.grid_columnconfigure(1, weight=1)

        self.master_switch = ctk.CTkSwitch(
            controls,
            text="总开关（关掉会把改过的队伍/无敌还原）",
            font=ctk.CTkFont(family="Microsoft YaHei", size=14, weight="bold"),
            progress_color=GREEN,
            command=self._on_master_toggle,
        )
        self.master_switch.grid(row=0, column=0, columnspan=2, padx=14, pady=(12, 8), sticky="w")

        self.pacify_var = ctk.BooleanVar(value=DEFAULT_CONFIG["pacify"])
        self.pacify_switch = self._add_switch(controls, 1, "停战（人机不开火 + 全员不掉血）", self.pacify_var)
        self.freeze_var = ctk.BooleanVar(value=DEFAULT_CONFIG["freeze"])
        self.freeze_switch = self._add_switch(controls, 2, "冻结人机行为（不寻敌/不巡逻/不行动）", self.freeze_var)
        self.follow_var = ctk.BooleanVar(value=DEFAULT_CONFIG["follow"])
        self.follow_switch = self._add_switch(controls, 3, "跟随我（所有人机都朝我走）", self.follow_var)
        self.walk_var = ctk.BooleanVar(value=DEFAULT_CONFIG["walk"])
        self.walk_switch = self._add_switch(controls, 4, "人机采样（记录 bot 走过哪些边）", self.walk_var)

        ctk.CTkLabel(
            controls, text="采样间隔 (ms)", font=ctk.CTkFont(family="Microsoft YaHei", size=13)
        ).grid(row=5, column=0, padx=14, pady=(8, 2), sticky="w")
        self.sample_value_label = ctk.CTkLabel(controls, text=str(DEFAULT_CONFIG["sample_ms"]))
        self.sample_value_label.grid(row=5, column=1, padx=14, pady=(8, 2), sticky="e")
        self.sample_slider = ctk.CTkSlider(
            controls, from_=50, to=1000, number_of_steps=19, command=self._on_sample_changed
        )
        self.sample_slider.grid(row=6, column=0, columnspan=2, padx=14, pady=(0, 12), sticky="ew")
        self.sample_slider.set(DEFAULT_CONFIG["sample_ms"])

        actions = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL_DARK)
        actions.grid(row=5, column=0, padx=18, pady=4, sticky="ew")
        actions.grid_columnconfigure((0, 1, 2), weight=1)
        self.probe_button = ctk.CTkButton(
            actions, text="跑一次物理探针", height=34, fg_color="#0e7490", hover_color="#155e75",
            font=ctk.CTkFont(family="Microsoft YaHei", size=14, weight="bold"), command=self._run_probe,
        )
        self.probe_button.grid(row=0, column=0, padx=8, pady=(12, 4), sticky="ew")
        self.selftest_button = ctk.CTkButton(
            actions, text="自检（不打架也能量）", height=34, fg_color="#7c3aed", hover_color="#6d28d9",
            font=ctk.CTkFont(family="Microsoft YaHei", size=13), command=self._run_selftest,
        )
        self.selftest_button.grid(row=0, column=1, padx=8, pady=(12, 4), sticky="ew")
        self.restore_button = ctk.CTkButton(
            actions, text="停止并还原", height=34, fg_color=ORANGE, hover_color="#b9770e",
            font=ctk.CTkFont(family="Microsoft YaHei", size=13), command=self._stop_and_restore,
        )
        self.restore_button.grid(row=0, column=2, padx=8, pady=(12, 4), sticky="ew")
        self.save_button = ctk.CTkButton(
            actions, text="另存日志", height=30, fg_color="#374151", hover_color="#4b5563",
            font=ctk.CTkFont(family="Microsoft YaHei", size=13), command=self._save_log,
        )
        self.save_button.grid(row=1, column=0, padx=8, pady=(0, 10), sticky="ew")
        self.openlog_button = ctk.CTkButton(
            actions, text="打开日志目录", height=30, fg_color="#374151", hover_color="#4b5563",
            font=ctk.CTkFont(family="Microsoft YaHei", size=13), command=self._open_log_dir,
        )
        self.openlog_button.grid(row=1, column=1, columnspan=2, padx=8, pady=(0, 10), sticky="ew")

        result = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        result.grid(row=6, column=0, padx=18, pady=4, sticky="ew")
        result.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.pass_label = self._add_metric(result, 0, "通行 PASS", "-")
        self.block_label = self._add_metric(result, 1, "阻断 BLOCK", "-")
        self.gap_label = self._add_metric(result, 2, "断空 GAP", "-")
        self.step_label = self._add_metric(result, 3, "台阶 STEP", "-")
        self.steep_label = self._add_metric(result, 4, "陡坡 STEEP", "-")
        self.total_label = self._add_metric(result, 5, "合计", "-")

        head = ctk.CTkFrame(self, fg_color="transparent")
        head.grid(row=7, column=0, padx=18, pady=(8, 0), sticky="ew")
        head.grid_columnconfigure(0, weight=1)
        self.detail_label = ctk.CTkLabel(
            head, text="未连接。", text_color=DIM, font=ctk.CTkFont(family="Microsoft YaHei", size=12),
            anchor="w", justify="left", wraplength=560,
        )
        self.detail_label.grid(row=0, column=0, sticky="w")
        self.verbose_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            head, text="显示 EDGES 明细", variable=self.verbose_var,
            font=ctk.CTkFont(family="Microsoft YaHei", size=12), command=self._on_verbose_changed,
        ).grid(row=0, column=1, padx=6, sticky="e")
        self.logpath_label = ctk.CTkLabel(
            head, text="日志：" + self.log_file_path, text_color="#6b7280",
            font=ctk.CTkFont(family="Microsoft YaHei", size=11), anchor="w", justify="left",
        )
        self.logpath_label.grid(row=1, column=0, columnspan=2, pady=(2, 0), sticky="w")

        self.log_box = ctk.CTkTextbox(self, height=260, font=ctk.CTkFont(family="Consolas", size=11))
        self.log_box.grid(row=8, column=0, padx=18, pady=(4, 16), sticky="nsew")
        self.log_box.configure(state="disabled")

        self._set_controls_enabled(False)

    def _add_metric(self, parent, column, title, value):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=column, padx=6, pady=8, sticky="ew")
        ctk.CTkLabel(frame, text=title, text_color=DIM, font=ctk.CTkFont(family="Microsoft YaHei", size=11)).pack()
        label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(family="Microsoft YaHei", size=15, weight="bold"))
        label.pack(pady=(2, 0))
        return label

    def _add_switch(self, parent, row, text, var):
        switch = ctk.CTkSwitch(
            parent, text=text, variable=var, font=ctk.CTkFont(family="Microsoft YaHei", size=13),
            command=self._push_config,
        )
        switch.grid(row=row, column=0, columnspan=2, padx=14, pady=3, sticky="w")
        return switch

    def _set_controls_enabled(self, enabled):
        state = "normal" if enabled and not self.rpc_busy else "disabled"
        for widget in (
            self.master_switch, self.pacify_switch, self.freeze_switch, self.follow_switch, self.walk_switch,
            self.sample_slider, self.probe_button, self.restore_button,
        ):
            widget.configure(state=state)

    # ---------------- queue ----------------
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
            self.after(900, self._schedule_connect)
        elif event == "rpc_done":
            self.rpc_busy = False
            self._set_controls_enabled(self.connected)
            if args and isinstance(args[0], dict) and args[0].get("ok") is False:
                self._log("操作未生效：" + str(args[0].get("reason", "unknown")))
            if args and len(args) > 1 and args[1]:
                self._render_status(args[1])
        elif event == "rpc_error":
            self.rpc_busy = False
            self._log("操作失败：" + str(args[0]))
            self._set_controls_enabled(self.connected)
        elif event == "status":
            self._render_status(args[0])
        elif event == "destroy":
            self.destroy()

    # ---------------- log ----------------
    def _log(self, text):
        text = str(text)
        line = f"[{time.strftime('%H:%M:%S')}] {text}"
        self.all_logs.append(line)          # 完整日志始终保留
        self._write_file(text)              # 同时自动写盘
        if "PROBE|EDGES|" in text and not self.verbose_state:
            if not self._edges_hint_shown:
                self._edges_hint_shown = True
                self._display("… EDGES 明细已隐藏（点右侧勾选框显示；保存日志时仍完整写入）")
            return
        self._display(text)

    def _append_log(self, text):
        """直接写一行到日志（同时进完整日志）。"""
        self.all_logs.append(f"[{time.strftime('%H:%M:%S')}] {text}")
        self._write_file(text)
        self._display(text)

    def _display(self, text):
        stamp = time.strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{stamp}] {text}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _save_log(self):
        os.makedirs(LOG_DIR, exist_ok=True)
        default = os.path.join(LOG_DIR, "waypoint-probe-" + time.strftime("%Y%m%d-%H%M%S") + ".log")
        path = filedialog.asksaveasfilename(
            title="保存路点体检日志", initialdir=LOG_DIR, initialfile=os.path.basename(default),
            defaultextension=".log", filetypes=[("日志", "*.log"), ("全部", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("\n".join(self.all_logs))
            self._append_log("日志已保存：" + path)
        except OSError as exc:
            self._append_log("保存失败：" + str(exc))

    # ---------------- 自动落盘与异常捕获 ----------------
    def _open_log_file(self):
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
            self.log_file_path = os.path.join(
                LOG_DIR, "waypoint-probe-ui-" + time.strftime("%Y%m%d-%H%M%S") + ".log"
            )
            self.log_handle = open(self.log_file_path, "a", encoding="utf-8", buffering=1)
            self._write_file("=== 路点体检 UI 启动 " + time.strftime("%Y-%m-%d %H:%M:%S") + " ===")
        except OSError as exc:
            self.log_handle = None
            self.log_file_path = "(写盘失败: " + str(exc) + ")"

    def _write_file(self, text):
        if not self.log_handle:
            return
        try:
            self.log_handle.write("[" + time.strftime("%H:%M:%S") + "] " + str(text) + "\n")
            self.log_handle.flush()
        except Exception:
            pass

    def _close_log_file(self):
        if not self.log_handle:
            return
        try:
            self.log_handle.write("[" + time.strftime("%H:%M:%S") + "] === 退出 ===\n")
            self.log_handle.flush()
            self.log_handle.close()
        except Exception:
            pass
        self.log_handle = None

    def _install_exception_hooks(self):
        sys.excepthook = self._on_uncaught
        self.report_callback_exception = self._on_tk_error

    def _on_uncaught(self, exc_type, exc_value, exc_tb):
        detail = "".join(traceback.format_exception(exc_type, exc_value, exc_tb)).strip()
        try:
            self._post("log", "[Python 异常] " + detail)
        except Exception:
            print(detail)

    def _on_tk_error(self, exc_type, exc_value, exc_tb):
        detail = "".join(traceback.format_exception(exc_type, exc_value, exc_tb)).strip()
        self._post("log", "[界面异常] " + detail)

    def _on_verbose_changed(self):
        self.verbose_state = bool(self.verbose_var.get())

    def _open_log_dir(self):
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
            os.startfile(LOG_DIR)
        except Exception as exc:
            self._log("打开日志目录失败：" + str(exc))

    # ---------------- connection ----------------
    def _set_connection(self, connected, text, pid_text=""):
        self.status_dot.configure(text_color=GREEN if connected else "#777")
        self.connection_label.configure(text=text)
        self.pid_label.configure(text=pid_text)

    def _find_game_pid(self):
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info["name"] == GAME_PROCESS_NAME:
                    return proc.info["pid"]
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    def _schedule_connect(self):
        if self.closing or self.connected or self.connecting:
            return
        threading.Thread(target=self._connect_worker, daemon=True).start()

    def _connect_worker(self):
        self.connecting = True
        try:
            pid = self._find_game_pid()
            if not pid:
                self._post("waiting", "等待游戏启动...", "")
                self._post("retry_connect")
                return

            self._post("waiting", "正在连接游戏...", f"PID {pid}")
            js_file = find_js_file()
            self.session = frida.attach(pid)
            with open(js_file, "r", encoding="utf-8") as handle:
                source = handle.read()
            self.script = self.session.create_script(source)
            self.script.on("message", self._on_message)
            self.session.on("detached", self._on_detached_frida)
            self.script.load()
            self.connected = True
            self._post("connected", pid)
            self._post("log", "已加载 " + os.path.basename(js_file))
        except Exception as exc:
            self._post("log", "连接失败：" + str(exc))
            self._post("waiting", "连接失败，稍后重试...", "")
            self._post("retry_connect")
        finally:
            self.connecting = False

    def _on_connected(self, pid):
        self._set_connection(True, "已连接游戏", f"PID {pid}")
        self._set_controls_enabled(True)
        self.detail_label.configure(text="已就绪：打开总开关生效。", text_color=DIM)
        if not self.polling:
            self.polling = True
            self.after(1000, self._poll_status)

    def _on_detached_frida(self, reason, crash=None):
        detail = str(reason)
        if crash:
            detail += " " + str(crash)
        self._post("detached", detail)

    def _on_detached(self, detail):
        self.connected = False
        self.enabled = False
        self.script = None
        self.session = None
        self.master_switch.deselect()
        self._set_connection(False, "游戏已断开", "")
        self._set_controls_enabled(False)
        self._log("已断开：" + str(detail))
        if not self.closing:
            self.after(1200, self._schedule_connect)

    def _on_message(self, message, data):
        kind = message.get("type")
        if kind == "send":
            payload = message.get("payload", {})
            if isinstance(payload, dict) and payload.get("type") == "log":
                level = payload.get("level", "info")
                text = str(payload.get("message", ""))
                if level == "error":
                    text = "[错误] " + text
                elif level == "warn":
                    text = "[提示] " + text
                self._post("log", text)
            else:
                self._post("log", "[脚本] " + str(payload))
        elif kind == "error":
            self._post("log", "[脚本错误] " + str(message.get("stack") or message.get("description") or "Frida error"))
        elif kind == "log":
            # JS 里 console.log 的镜像（log() 已经 send 过一份），默认不重复显示
            if self.verbose_state:
                self._post("log", "[console] " + str(message.get("payload", "")))
        else:
            self._post("log", str(message))

    # ---------------- rpc ----------------
    def _rpc_worker(self, names, args, render):
        try:
            with self.rpc_lock:
                result = self._invoke(names, *args)
            status = None
            if render:
                try:
                    status = self._invoke(STATUS_CANDIDATES)
                except Exception:
                    status = None
            self._post("rpc_done", result, status)
        except Exception as exc:
            self._post("rpc_error", exc)

    def _invoke(self, names, *args):
        if not self.script:
            raise RuntimeError("脚本未加载")
        exports = self.script.exports_sync
        last = None
        for name in names:
            try:
                return getattr(exports, name)(*args)
            except Exception as exc:  # 方法不存在时 Frida 报 "unable to find method"
                last = exc
                if "unable to find method" not in str(exc).lower():
                    raise
        raise RuntimeError(last if last else ("missing rpc " + "/".join(names)))

    def _call_sequence(self, steps, render=True):
        """按顺序一次性执行多个 RPC（例如先 setConfig 再 enable）。"""
        if not self.script or self.rpc_busy:
            return
        self.rpc_busy = True
        self._set_controls_enabled(False)
        threading.Thread(target=self._sequence_worker, args=(tuple(steps), render), daemon=True).start()

    def _sequence_worker(self, steps, render):
        try:
            result = None
            with self.rpc_lock:
                for step in steps:
                    result = self._invoke(step[0], *step[1:])
            status = None
            if render:
                try:
                    status = self._invoke(STATUS_CANDIDATES)
                except Exception:
                    status = None
            self._post("rpc_done", result, status)
        except Exception as exc:
            self._post("rpc_error", exc)

    def _call(self, names, *args, render=True):
        if not self.script or self.rpc_busy:
            return
        self.rpc_busy = True
        self._set_controls_enabled(False)
        threading.Thread(target=self._rpc_worker, args=(tuple(names), args, render), daemon=True).start()

    # ---------------- actions ----------------
    def _current_config(self):
        return {
            "pacify": bool(self.pacify_var.get()),
            "freeze": bool(self.freeze_var.get()),
            "follow": bool(self.follow_var.get()),
            "walk": bool(self.walk_var.get()),
            "sample_ms": int(self.sample_slider.get()),
        }

    def _on_sample_changed(self, value):
        self.sample_value_label.configure(text=str(int(value)))
        self._push_config()

    def _push_config(self):
        if self.connected and not self.rpc_busy and not self.closing:
            self._call(SETCONFIG_CANDIDATES, self._current_config())

    def _on_master_toggle(self):
        if not self.connected:
            self.master_switch.deselect()
            return
        if self.master_switch.get():
            self.enabled = True
            self._call_sequence(((SETCONFIG_CANDIDATES, self._current_config()), (ENABLE_CANDIDATES,)))
            self._log("已开启")
        else:
            self._call(DISABLE_CANDIDATES)
            self.enabled = False
            self._log("已关闭，队伍/无敌已还原")

    def _stop_and_restore(self):
        self.master_switch.deselect()
        self.enabled = False
        self._call(DISABLE_CANDIDATES)

    def _run_selftest(self):
        if not self.connected:
            return
        self._log("开始自检 ...")
        self._call(SELFTEST_CANDIDATES)

    def _run_probe(self):
        if not self.connected:
            return
        if not self.enabled or not self.master_switch.get():
            self._log("请先打开总开关")
            return
        self._log("开始物理探针（边多时会有几秒卡顿）...")
        self._call(RUNPROBE_CANDIDATES)

    # ---------------- status ----------------
    def _poll_status(self):
        if self.closing or not self.connected:
            self.polling = False
            return
        if not self.rpc_busy and not self.status_busy:
            threading.Thread(target=self._status_worker, daemon=True).start()
        self.after(1500, self._poll_status)

    def _status_worker(self):
        self.status_busy = True
        try:
            result = self._invoke(STATUS_CANDIDATES)
            if isinstance(result, dict) and result.get("ok"):
                self._post("status", result)
        except Exception as exc:
            self._post("log", "状态读取失败：" + str(exc))
            if self.connected:
                self._post("detached", "RPC 状态读取失败，可能游戏已退出")
        finally:
            self.status_busy = False

    def _render_status(self, status):
        if not isinstance(status, dict):
            return
        summary = status.get("probe") or {}
        total = summary.get("total")
        if isinstance(total, int) and total > 0:
            self.total_label.configure(text=str(total))
            self.pass_label.configure(text=str(summary.get("pass", 0)), text_color=GREEN)
            self.block_label.configure(text=str(summary.get("block", 0)), text_color=RED)
            self.gap_label.configure(text=str(summary.get("gap", 0)), text_color=ORANGE)
            self.step_label.configure(text=str(summary.get("step", 0)))
            self.steep_label.configure(text=str(summary.get("steep", 0)))
            self.node_label.configure(text=str(total))
        bots = status.get("bots")
        if isinstance(bots, int):
            self.bot_label.configure(text=str(bots))
        followers = status.get("followers")
        if isinstance(followers, int):
            self.follow_label.configure(text=str(followers))
        stats = status.get("stats") or {}
        self.sample_label.configure(text=f"{stats.get('samples', 0)}/{stats.get('traversals', 0)}")

        config = status.get("config") or {}
        if config:
            self.pacify_var.set(bool(config.get("pacify")))
            self.follow_var.set(bool(config.get("follow")))
            self.walk_var.set(bool(config.get("walk")))

        last_error = status.get("lastError") or ""
        detail = "运行中" if status.get("enabled") else "总开关关闭"
        if last_error:
            detail += " | 最近错误：" + str(last_error)
        self.detail_label.configure(text=detail, text_color=RED if last_error else DIM)

    # ---------------- shutdown ----------------
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
                try:
                    self._invoke(CLEANUP_CANDIDATES)
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
            self._close_log_file()
            self._post_allow_closing("destroy")


if __name__ == "__main__":
    app = WaypointProbeApp()
    app.mainloop()
