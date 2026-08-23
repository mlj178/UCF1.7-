from __future__ import annotations

import json
import pathlib
import queue
import threading
import time
import tkinter.filedialog as filedialog

import customtkinter as ctk
import frida
import psutil


GAME_PROCESS_NAME = "UnityCrossFire.exe"
BASE_DIR = pathlib.Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "AAAAA-healthbar_prefab_probe_min.js"

BG = "#111318"
PANEL = "#1a1e26"
PANEL_DARK = "#151820"
GREEN = "#39c47a"
ORANGE = "#f0a33a"
RED = "#e65757"


class HealthBarPrefabProbeApp(ctk.CTk):
    def __init__(self) -> None:
        ctk.set_appearance_mode("dark")
        super().__init__()
        self.title("HUD HealthBar Prefab 探针")
        self.geometry("940x780")
        self.minsize(820, 620)
        self.configure(fg_color=BG)

        self.ui_queue: queue.Queue[tuple[str, tuple]] = queue.Queue()
        self.rpc_lock = threading.Lock()
        self.session = None
        self.script = None
        self.connected = False
        self.connecting = False
        self.rpc_busy = False
        self.status_busy = False
        self.closing = False
        self.shutdown_done = False
        self.log_lines: list[str] = []

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._drain_ui_queue)
        self.after(250, self._schedule_connect)

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        title = ctk.CTkLabel(
            self,
            text="HUD HealthBar Prefab 探针",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title.grid(row=0, column=0, padx=20, pady=(18, 4), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="默认只读；可显式排队一次原生 GetSign → Bind → Active 血条验证",
            text_color="#98a2b3",
            font=ctk.CTkFont(size=12),
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")

        connection = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=9)
        connection.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        connection.grid_columnconfigure(1, weight=1)
        self.status_dot = ctk.CTkLabel(connection, text="●", text_color="#666", width=24)
        self.status_dot.grid(row=0, column=0, padx=(12, 4), pady=10)
        self.connection_label = ctk.CTkLabel(connection, text="等待游戏启动...")
        self.connection_label.grid(row=0, column=1, padx=4, pady=10, sticky="w")
        self.pid_label = ctk.CTkLabel(connection, text="", text_color="#8d96a7")
        self.pid_label.grid(row=0, column=2, padx=12, pady=10)

        controls = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=9)
        controls.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        controls.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.enable_switch = ctk.CTkSwitch(
            controls,
            text="启用只读采样",
            command=self._toggle_probe,
            progress_color=GREEN,
        )
        self.enable_switch.grid(row=0, column=0, padx=12, pady=12, sticky="w")
        self.enable_switch.select()

        self.interval_menu = ctk.CTkOptionMenu(
            controls,
            values=["1000", "2000", "5000"],
            command=self._on_interval_changed,
            width=105,
        )
        self.interval_menu.set("2000")
        self.interval_menu.grid(row=0, column=1, padx=8, pady=12)

        self.snapshot_button = ctk.CTkButton(
            controls,
            text="请求主线程快照",
            command=lambda: self._call_rpc("debugdump"),
            fg_color=GREEN,
        )
        self.snapshot_button.grid(row=0, column=2, padx=8, pady=12, sticky="ew")

        self.reset_button = ctk.CTkButton(
            controls,
            text="重置 generation",
            command=lambda: self._call_rpc("reset", "manual_ui"),
            fg_color=ORANGE,
        )
        self.reset_button.grid(row=0, column=3, padx=8, pady=12, sticky="ew")

        self.save_button = ctk.CTkButton(
            controls,
            text="保存日志",
            command=self._save_log,
            fg_color="#44506a",
        )
        self.save_button.grid(row=0, column=4, padx=(8, 12), pady=12, sticky="ew")

        self.create_test_button = ctk.CTkButton(
            controls,
            text="主动生成测试血条",
            command=lambda: self._call_rpc("createtestbar"),
            fg_color="#2f6fbd",
        )
        self.create_test_button.grid(row=1, column=0, columnspan=3, padx=(12, 8), pady=(0, 12), sticky="ew")

        self.recycle_test_button = ctk.CTkButton(
            controls,
            text="回收测试血条",
            command=lambda: self._call_rpc("recycletestbar"),
            fg_color=RED,
        )
        self.recycle_test_button.grid(row=1, column=3, columnspan=2, padx=(8, 12), pady=(0, 12), sticky="ew")

        metrics = ctk.CTkFrame(self, fg_color=PANEL_DARK, corner_radius=9)
        metrics.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        metrics.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.hud_metric = self._metric(metrics, 0, "HUD_Tombstone", "等待")
        self.prefab_metric = self._metric(metrics, 1, "Prefab", "等待")
        self.component_metric = self._metric(metrics, 2, "HealthBar", "等待")
        self.image_metric = self._metric(metrics, 3, "Image", "等待")
        self.sprite_metric = self._metric(metrics, 4, "Sprite", "等待")

        log_frame = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=9)
        log_frame.grid(row=5, column=0, padx=20, pady=(5, 18), sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)
        self.detail_label = ctk.CTkLabel(
            log_frame,
            text="请从一局全新的、尚未出现墓碑的对局开始记录。",
            text_color="#a7b0c0",
            anchor="w",
        )
        self.detail_label.grid(row=0, column=0, padx=12, pady=(10, 4), sticky="ew")
        self.log_box = ctk.CTkTextbox(log_frame, font=ctk.CTkFont(family="Consolas", size=11))
        self.log_box.grid(row=1, column=0, padx=12, pady=(4, 12), sticky="nsew")
        self.log_box.configure(state="disabled")

        self._set_controls_enabled(False)

    def _metric(self, parent, column: int, title: str, value: str):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=column, padx=6, pady=10, sticky="ew")
        ctk.CTkLabel(frame, text=title, text_color="#8993a5", font=ctk.CTkFont(size=11)).pack()
        label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=15, weight="bold"))
        label.pack(pady=(2, 0))
        return label

    def _post(self, event: str, *args) -> None:
        if not self.closing:
            self.ui_queue.put((event, args))

    def _post_allow_closing(self, event: str, *args) -> None:
        self.ui_queue.put((event, args))

    def _drain_ui_queue(self) -> None:
        try:
            while True:
                event, args = self.ui_queue.get_nowait()
                self._handle_event(event, *args)
        except queue.Empty:
            pass
        if not self.closing:
            self.after(100, self._drain_ui_queue)

    def _handle_event(self, event: str, *args) -> None:
        if event == "log":
            self._append_log(str(args[0]))
        elif event == "waiting":
            self._set_connection(False, str(args[0]), str(args[1]) if len(args) > 1 else "")
        elif event == "connected":
            self._on_connected(int(args[0]))
        elif event == "detached":
            self._on_detached(str(args[0]))
        elif event == "retry_connect":
            self.after(800, self._schedule_connect)
        elif event == "rpc_done":
            self.rpc_busy = False
            if isinstance(args[0], dict):
                self._render_status(args[0])
            self._set_controls_enabled(self.connected)
        elif event == "rpc_error":
            self.rpc_busy = False
            self._append_log("RPC 失败：" + str(args[0]))
            self._set_controls_enabled(self.connected)
        elif event == "status":
            self._render_status(args[0])
        elif event == "destroy":
            self.destroy()

    def _append_log(self, text: str) -> None:
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{stamp}] {text}"
        self.log_lines.append(line)
        self.log_box.configure(state="normal")
        self.log_box.insert("end", line + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _set_connection(self, connected: bool, text: str, pid_text: str = "") -> None:
        self.status_dot.configure(text_color=GREEN if connected else "#666")
        self.connection_label.configure(text=text)
        self.pid_label.configure(text=pid_text)

    def _set_controls_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled and not self.rpc_busy else "disabled"
        for widget in (
            self.enable_switch,
            self.interval_menu,
            self.snapshot_button,
            self.reset_button,
            self.create_test_button,
            self.recycle_test_button,
        ):
            widget.configure(state=state)
        self.save_button.configure(state="normal")

    @staticmethod
    def _find_game_pid() -> int | None:
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info["name"] == GAME_PROCESS_NAME:
                    return int(proc.info["pid"])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    def _schedule_connect(self) -> None:
        if self.closing or self.connected or self.connecting:
            return
        threading.Thread(target=self._connect_worker, daemon=True).start()

    def _connect_worker(self) -> None:
        self.connecting = True
        session = None
        script = None
        try:
            pid = self._find_game_pid()
            if pid is None:
                self._post("waiting", "等待 UnityCrossFire.exe 启动...", "")
                self._post("retry_connect")
                return
            self._post("waiting", "正在连接游戏...", f"PID {pid}")
            session = frida.attach(pid)
            source = JS_FILE.read_text(encoding="utf-8")
            script = session.create_script(source)
            script.on("message", self._on_message)
            script.load()
            with self.rpc_lock:
                script.exports_sync.setconfig(self._current_config())
                enabled = script.exports_sync.enable()
                if enabled is not True:
                    status = script.exports_sync.status()
                    last_error = (status.get("stats") or {}).get("lastError", "未知错误")
                    raise RuntimeError("探针初始化失败：" + str(last_error))
            session.on("detached", self._on_detached_frida)
            self.session = session
            self.script = script
            self.connected = True
            self._post("connected", pid)
        except Exception as exc:
            self.connected = False
            if script is not None:
                try:
                    script.unload()
                except Exception:
                    pass
            if session is not None:
                try:
                    session.detach()
                except Exception:
                    pass
            self.script = None
            self.session = None
            self._post("log", "连接失败：" + str(exc))
            self._post("waiting", "连接失败，稍后重试...", "")
            self._post("retry_connect")
        finally:
            self.connecting = False

    def _on_connected(self, pid: int) -> None:
        self._set_connection(True, "已连接，等待主线程采样", f"PID {pid}")
        self._set_controls_enabled(True)
        self._append_log("脚本已加载并启用；请保留从无墓碑阶段开始的完整日志")
        self.after(700, self._poll_status)

    def _on_detached_frida(self, reason, crash=None) -> None:
        detail = str(reason)
        if crash:
            detail += " " + str(crash)
        self._post("detached", detail)

    def _on_detached(self, detail: str) -> None:
        self.connected = False
        self.script = None
        self.session = None
        self._set_connection(False, "游戏已断开", "")
        self._set_controls_enabled(False)
        self._append_log("已断开：" + detail)
        if not self.closing:
            self.after(1000, self._schedule_connect)

    def _on_message(self, message, data) -> None:
        if message.get("type") == "send":
            payload = message.get("payload", {})
            if isinstance(payload, dict) and payload.get("type") == "log":
                category = payload.get("category", "LOG")
                level = payload.get("level", "info")
                text = payload.get("message", "")
                self._post("log", f"[{level}][{category}] {text}")
            else:
                self._post("log", json.dumps(payload, ensure_ascii=False, default=str))
        elif message.get("type") == "error":
            self._post("log", message.get("stack", message.get("description", "Frida error")))
        else:
            self._post("log", str(message))

    def _current_config(self) -> dict:
        return {
            "sample_interval_ms": int(self.interval_menu.get()),
            "log_unchanged_every_ms": 15000,
        }

    def _toggle_probe(self) -> None:
        self._call_rpc("enable" if self.enable_switch.get() else "disable")

    def _on_interval_changed(self, _value: str) -> None:
        if self.connected:
            self._call_rpc("setconfig", self._current_config())

    def _call_rpc(self, action: str, *args) -> None:
        if not self.script or self.rpc_busy:
            return
        self.rpc_busy = True
        self._set_controls_enabled(False)
        threading.Thread(target=self._rpc_worker, args=(action, args), daemon=True).start()

    def _rpc_worker(self, action: str, args: tuple) -> None:
        try:
            with self.rpc_lock:
                result = getattr(self.script.exports_sync, action)(*args)
            self._post("rpc_done", result)
        except Exception as exc:
            self._post("rpc_error", exc)

    def _poll_status(self) -> None:
        if self.closing:
            return
        if self.connected and not self.status_busy and not self.rpc_busy:
            threading.Thread(target=self._status_worker, daemon=True).start()
        self.after(1000, self._poll_status)

    def _status_worker(self) -> None:
        self.status_busy = True
        try:
            with self.rpc_lock:
                result = self.script.exports_sync.status()
            self._post("status", result)
        except Exception as exc:
            if self.connected:
                self._post("detached", "状态读取失败：" + str(exc))
        finally:
            self.status_busy = False

    @staticmethod
    def _set_metric(label, ready, waiting_text="未就绪") -> None:
        if ready is True:
            label.configure(text="有效", text_color=GREEN)
        elif ready is False:
            label.configure(text=waiting_text, text_color=ORANGE)
        else:
            label.configure(text="等待", text_color="#ddd")

    def _render_status(self, status) -> None:
        snapshot = (status or {}).get("snapshot") or {}
        conclusion = snapshot.get("conclusion") or {}
        hud = snapshot.get("hudTombstone") or {}
        self._set_metric(self.hud_metric, hud.get("readable"))
        self._set_metric(self.prefab_metric, conclusion.get("prefabReady"))
        self._set_metric(self.component_metric, conclusion.get("componentReady"))
        self._set_metric(self.image_metric, conclusion.get("imageReady"))
        self._set_metric(self.sprite_metric, conclusion.get("spriteReady"), "无贴图")

        stats = (status or {}).get("stats") or {}
        generation = (status or {}).get("generation", 0)
        self.detail_label.configure(
            text=(
                f"generation={generation} | Update命中={stats.get('updateHits', 0)} | "
                f"采样={stats.get('samples', 0)} | 时间线事件={stats.get('timelineEvents', 0)} | "
                f"主动创建={stats.get('activeTestCreated', 0)} | "
                f"主动回收={stats.get('activeTestRecycled', 0)} | 错误={stats.get('errorCount', 0)}"
            )
        )

    def _save_log(self) -> None:
        default_name = time.strftime("healthbar-prefab-probe-%Y%m%d-%H%M%S.log")
        path = filedialog.asksaveasfilename(
            title="保存探针日志",
            defaultextension=".log",
            initialfile=default_name,
            filetypes=[("Log 文件", "*.log"), ("文本文件", "*.txt"), ("所有文件", "*.*")],
        )
        if not path:
            return
        pathlib.Path(path).write_text("\n".join(self.log_lines) + "\n", encoding="utf-8")
        self._append_log("日志已保存：" + path)

    def _on_close(self) -> None:
        if self.shutdown_done:
            return
        self.shutdown_done = True
        self.closing = True
        self._set_controls_enabled(False)
        threading.Thread(target=self._shutdown_worker, daemon=True).start()

    def _shutdown_worker(self) -> None:
        try:
            if self.script:
                try:
                    with self.rpc_lock:
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
            try:
                self.after(0, self._drain_ui_queue)
            except Exception:
                pass


if __name__ == "__main__":
    app = HealthBarPrefabProbeApp()
    app.mainloop()
