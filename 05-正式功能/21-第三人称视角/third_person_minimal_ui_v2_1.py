# -*- coding: utf-8 -*-
"""
第三人称最小化 Demo v2.1 UI

配套脚本:
    third_person_minimal_demo_v2.js

依赖:
    pip install customtkinter frida-tools psutil

特点:
    - 自动检测 UnityCrossFire.exe
    - 自动附加 Frida 并加载 JS
    - 开启/关闭最小第三人称
    - 配置肩位、距离、稳定枢轴高度、FOV、纵向速度
    - UI 与文件双重日志
    - 不包含诊断工具，不修改移动和射击
"""

from __future__ import annotations

import ctypes
import json
import logging
import os
import queue
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional


def show_error(message: str) -> None:
    try:
        if os.name == "nt":
            ctypes.windll.user32.MessageBoxW(
                0,
                message,
                "第三人称最小 Demo",
                0x10,
            )
        else:
            print(message, file=sys.stderr)
    except Exception:
        print(message, file=sys.stderr)


try:
    import customtkinter as ctk
except ImportError:
    show_error(
        "缺少 customtkinter。\n\n"
        "请执行：\n"
        "pip install customtkinter frida-tools psutil"
    )
    raise SystemExit(1)

try:
    import frida
except ImportError:
    show_error(
        "缺少 frida。\n\n"
        "请执行：\n"
        "pip install frida-tools"
    )
    raise SystemExit(1)

try:
    import psutil
except ImportError:
    show_error(
        "缺少 psutil。\n\n"
        "请执行：\n"
        "pip install psutil"
    )
    raise SystemExit(1)


APP_VERSION = "2.1"
PROCESS_NAMES = ("unitycrossfire.exe", "unitycrossfire")
SCRIPT_NAME = "third_person_minimal_demo_v2_1.js"

BASE_DIR = Path(__file__).resolve().parent
SCRIPT_PATH = BASE_DIR / SCRIPT_NAME
CONFIG_PATH = BASE_DIR / "third_person_minimal_config.json"
LOG_DIR = BASE_DIR / "logs"

DEFAULT_CONFIG = {
    "shoulder": "right",
    "distance": 3.0,
    "pivotHeight": 1.40,
    "screenY": 0.52,
    "fieldOfView": 70.0,
    "pitchScale": 1.0,
    "invertY": False,
}

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class DemoLogger:
    def __init__(self) -> None:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.path = LOG_DIR / f"third_person_minimal_{stamp}.txt"

        self.logger = logging.getLogger(f"tp_minimal_{id(self)}")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        handler = logging.FileHandler(self.path, encoding="utf-8")
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        self.logger.addHandler(handler)

    def write(self, level: str, message: str) -> None:
        if level == "error":
            self.logger.error(message)
        elif level in ("warning", "warn"):
            self.logger.warning(message)
        elif level == "debug":
            self.logger.debug(message)
        else:
            self.logger.info(message)


FILE_LOG = DemoLogger()


class MinimalThirdPersonUI(ctk.CTk):
    GREEN = "#2E9E5B"
    GREEN_HOVER = "#267F4B"
    RED = "#C44747"
    RED_HOVER = "#A83C3C"
    ORANGE = "#C88732"
    MUTED = "#8A8A8A"

    def __init__(self) -> None:
        super().__init__()

        self.title(f"第三人称最小化 Demo v{APP_VERSION}")
        self.geometry("820x760+160+70")
        self.minsize(780, 700)

        self.session: Optional[Any] = None
        self.script: Optional[Any] = None
        self.pid: Optional[int] = None

        self.connected = False
        self.enabled = False
        self.closing = False

        self.rpc_lock = threading.RLock()
        self.state_lock = threading.RLock()
        self.stop_event = threading.Event()
        self.connect_event = threading.Event()

        self.log_queue: queue.Queue[tuple[str, str]] = queue.Queue()
        self.status_busy = False
        self.apply_after: Optional[str] = None
        self.syncing_controls = False

        self.config_data = self.load_config()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.build_ui()
        self.apply_config_to_controls()
        self.set_connected_controls(False)

        self.after(100, self.drain_logs)
        self.after(1500, self.status_tick)

        threading.Thread(
            target=self.connection_loop,
            name="TP-Minimal-Connection",
            daemon=True,
        ).start()

        self.emit_log("UI 已启动。v2.1 会每秒把 PitchTelemetry 写入 TXT 日志。")

    # ------------------------------------------------------------
    # UI
    # ------------------------------------------------------------
    def build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(self, corner_radius=12)
        header.grid(
            row=0,
            column=0,
            padx=14,
            pady=(14, 8),
            sticky="ew",
        )
        header.grid_columnconfigure(0, weight=1)

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.grid(row=0, column=0, padx=16, pady=12, sticky="w")

        ctk.CTkLabel(
            title_box,
            text="第三人称最小化 Demo",
            font=ctk.CTkFont(size=23, weight="bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="原生 FreeLook + 玩家原生俯仰角；不修改 WASD、人物 Yaw 和射击",
            font=ctk.CTkFont(size=11),
            text_color=self.MUTED,
        ).pack(anchor="w", pady=(2, 0))

        status_box = ctk.CTkFrame(header, fg_color="transparent")
        status_box.grid(row=0, column=1, padx=12, pady=10, sticky="e")

        self.connection_label = ctk.CTkLabel(
            status_box,
            text="● 等待游戏",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.ORANGE,
        )
        self.connection_label.grid(row=0, column=0, padx=8)

        self.pid_label = ctk.CTkLabel(
            status_box,
            text="PID: -",
            font=ctk.CTkFont(size=11),
            text_color=self.MUTED,
        )
        self.pid_label.grid(row=1, column=0, padx=8)

        self.reconnect_button = ctk.CTkButton(
            status_box,
            text="重新连接",
            width=92,
            command=self.request_reconnect,
        )
        self.reconnect_button.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=(8, 0),
        )

        control_card = ctk.CTkFrame(self, corner_radius=12)
        control_card.grid(
            row=1,
            column=0,
            padx=14,
            pady=8,
            sticky="ew",
        )
        control_card.grid_columnconfigure(0, weight=1)

        self.toggle_button = ctk.CTkButton(
            control_card,
            text="开启最小第三人称",
            height=48,
            font=ctk.CTkFont(size=17, weight="bold"),
            fg_color=self.GREEN,
            hover_color=self.GREEN_HOVER,
            command=self.toggle_demo,
        )
        self.toggle_button.grid(
            row=0,
            column=0,
            padx=14,
            pady=(14, 6),
            sticky="ew",
        )

        self.mode_label = ctk.CTkLabel(
            control_card,
            text="当前：未连接",
            font=ctk.CTkFont(size=12),
        )
        self.mode_label.grid(row=1, column=0, pady=(0, 12))

        self.tabview = ctk.CTkTabview(self, corner_radius=12)
        self.tabview.grid(
            row=2,
            column=0,
            padx=14,
            pady=(0, 8),
            sticky="nsew",
        )

        camera_tab = self.tabview.add("相机")
        status_tab = self.tabview.add("状态")
        log_tab = self.tabview.add("日志")

        self.build_camera_tab(camera_tab)
        self.build_status_tab(status_tab)
        self.build_log_tab(log_tab)

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(
            row=3,
            column=0,
            padx=16,
            pady=(0, 10),
            sticky="ew",
        )
        footer.grid_columnconfigure(0, weight=1)

        self.footer_label = ctk.CTkLabel(
            footer,
            text=f"日志：{FILE_LOG.path}",
            font=ctk.CTkFont(size=10),
            text_color=self.MUTED,
        )
        self.footer_label.grid(row=0, column=0, sticky="w")

    def build_camera_tab(self, tab: Any) -> None:
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(tab, corner_radius=12)
        top.grid(
            row=0,
            column=0,
            padx=12,
            pady=(12, 8),
            sticky="ew",
        )
        top.grid_columnconfigure((0, 1), weight=1)

        shoulder_frame = ctk.CTkFrame(top, fg_color="transparent")
        shoulder_frame.grid(
            row=0,
            column=0,
            padx=12,
            pady=12,
            sticky="ew",
        )

        ctk.CTkLabel(
            shoulder_frame,
            text="肩位构图",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(anchor="w")

        self.shoulder_control = ctk.CTkSegmentedButton(
            shoulder_frame,
            values=["左肩", "居中", "右肩"],
            command=self.on_shoulder_changed,
        )
        self.shoulder_control.pack(fill="x", pady=(7, 0))

        option_frame = ctk.CTkFrame(top, fg_color="transparent")
        option_frame.grid(
            row=0,
            column=1,
            padx=12,
            pady=12,
            sticky="ew",
        )

        self.invert_switch = ctk.CTkSwitch(
            option_frame,
            text="反转鼠标上下",
            command=self.on_invert_changed,
        )
        self.invert_switch.pack(anchor="w", pady=(24, 0))

        controls = ctk.CTkScrollableFrame(tab, corner_radius=12)
        controls.grid(
            row=1,
            column=0,
            padx=12,
            pady=(8, 12),
            sticky="nsew",
        )
        controls.grid_columnconfigure(0, weight=1)

        self.distance_slider, self.distance_value = self.make_slider(
            controls,
            0,
            "相机距离",
            1.5,
            6.0,
            45,
            " m",
            self.on_distance_changed,
        )

        self.height_slider, self.height_value = self.make_slider(
            controls,
            1,
            "稳定枢轴高度",
            0.8,
            2.2,
            56,
            " m",
            self.on_height_changed,
        )

        self.screen_y_slider, self.screen_y_value = self.make_slider(
            controls,
            2,
            "画面垂直构图",
            0.40,
            0.65,
            50,
            "",
            self.on_screen_y_changed,
        )

        self.fov_slider, self.fov_value = self.make_slider(
            controls,
            3,
            "FOV",
            50.0,
            100.0,
            50,
            "°",
            self.on_fov_changed,
        )

        self.pitch_slider, self.pitch_value = self.make_slider(
            controls,
            4,
            "纵向俯仰倍率",
            0.5,
            2.0,
            30,
            "",
            self.on_pitch_changed,
        )

        button_row = ctk.CTkFrame(controls, fg_color="transparent")
        button_row.grid(
            row=5,
            column=0,
            padx=10,
            pady=(12, 6),
            sticky="ew",
        )
        button_row.grid_columnconfigure((0, 1), weight=1)

        self.apply_button = ctk.CTkButton(
            button_row,
            text="立即应用",
            command=self.apply_config_requested,
        )
        self.apply_button.grid(
            row=0,
            column=0,
            padx=(0, 5),
            sticky="ew",
        )

        self.reset_button = ctk.CTkButton(
            button_row,
            text="恢复默认",
            fg_color="#555555",
            hover_color="#444444",
            command=self.reset_config,
        )
        self.reset_button.grid(
            row=0,
            column=1,
            padx=(5, 0),
            sticky="ew",
        )

        ctk.CTkLabel(
            controls,
            text=(
                "Demo 不修改人物水平朝向、移动输入和射击 Ray。"
                "准星策略保持游戏原生/屏幕中心。"
            ),
            wraplength=700,
            justify="left",
            font=ctk.CTkFont(size=11),
            text_color=self.MUTED,
        ).grid(
            row=6,
            column=0,
            padx=12,
            pady=(8, 14),
            sticky="w",
        )

    def make_slider(
        self,
        parent: Any,
        row: int,
        title: str,
        minimum: float,
        maximum: float,
        steps: int,
        suffix: str,
        command: Callable[[float], None],
    ) -> tuple[Any, Any]:
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(
            row=row,
            column=0,
            padx=10,
            pady=7,
            sticky="ew",
        )
        frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        value_label = ctk.CTkLabel(
            header,
            text="-",
            width=80,
            anchor="e",
        )
        value_label.grid(row=0, column=1, sticky="e")

        slider = ctk.CTkSlider(
            frame,
            from_=minimum,
            to=maximum,
            number_of_steps=steps,
            command=command,
        )
        slider.grid(row=1, column=0, pady=(5, 0), sticky="ew")

        return slider, value_label

    def build_status_tab(self, tab: Any) -> None:
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        summary = ctk.CTkFrame(tab, corner_radius=12)
        summary.grid(
            row=0,
            column=0,
            padx=12,
            pady=(12, 8),
            sticky="ew",
        )
        summary.grid_columnconfigure((0, 1, 2), weight=1)

        self.status_labels: dict[str, Any] = {}

        fields = [
            ("脚本状态", "state"),
            ("纵向写入", "pitchWrites"),
            ("写入失败", "pitchWriteFailures"),
            ("玩家俯仰角", "lastPlayerPitch"),
            ("写入后 Y", "lastYAxisWritten"),
            ("真实相机俯仰", "lastCameraPitch"),
        ]

        for index, (title, key) in enumerate(fields):
            box = ctk.CTkFrame(summary)
            box.grid(
                row=index // 3,
                column=index % 3,
                padx=6,
                pady=6,
                sticky="nsew",
            )

            ctk.CTkLabel(
                box,
                text=title,
                font=ctk.CTkFont(size=10),
                text_color=self.MUTED,
            ).pack(pady=(9, 2))

            label = ctk.CTkLabel(
                box,
                text="-",
                font=ctk.CTkFont(size=16, weight="bold"),
            )
            label.pack(pady=(0, 9))
            self.status_labels[key] = label

        self.status_text = ctk.CTkTextbox(
            tab,
            font=("Consolas", 11),
        )
        self.status_text.grid(
            row=1,
            column=0,
            padx=12,
            pady=(8, 12),
            sticky="nsew",
        )
        self.status_text.insert("end", "尚未取得状态。\n")

    def build_log_tab(self, tab: Any) -> None:
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        toolbar = ctk.CTkFrame(tab, corner_radius=12)
        toolbar.grid(
            row=0,
            column=0,
            padx=12,
            pady=(12, 8),
            sticky="ew",
        )
        toolbar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            toolbar,
            text="运行日志",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).grid(row=0, column=0, padx=12, pady=10, sticky="w")

        ctk.CTkButton(
            toolbar,
            text="打开日志目录",
            width=110,
            command=self.open_log_dir,
        ).grid(row=0, column=1, padx=5, pady=10)

        ctk.CTkButton(
            toolbar,
            text="清空界面",
            width=90,
            fg_color="#555555",
            hover_color="#444444",
            command=lambda: self.log_text.delete("1.0", "end"),
        ).grid(row=0, column=2, padx=(5, 12), pady=10)

        self.log_text = ctk.CTkTextbox(
            tab,
            font=("Consolas", 11),
        )
        self.log_text.grid(
            row=1,
            column=0,
            padx=12,
            pady=(0, 12),
            sticky="nsew",
        )

    # ------------------------------------------------------------
    # 配置
    # ------------------------------------------------------------
    def load_config(self) -> dict[str, Any]:
        config = dict(DEFAULT_CONFIG)

        try:
            if CONFIG_PATH.exists():
                loaded = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    config.update(loaded)
        except Exception as exc:
            FILE_LOG.write("warning", f"读取配置失败: {exc}")

        shoulder = str(config.get("shoulder", "right")).lower()
        if shoulder not in ("left", "center", "right"):
            shoulder = "right"
        config["shoulder"] = shoulder

        config["distance"] = self.clamp(
            config.get("distance"),
            1.5,
            6.0,
            3.0,
        )
        config["pivotHeight"] = self.clamp(
            config.get("pivotHeight"),
            0.8,
            2.2,
            1.40,
        )
        config["screenY"] = self.clamp(
            config.get("screenY"),
            0.40,
            0.65,
            0.52,
        )
        config["fieldOfView"] = self.clamp(
            config.get("fieldOfView"),
            50.0,
            100.0,
            70.0,
        )
        config["pitchScale"] = self.clamp(
            config.get("pitchScale"),
            0.5,
            2.0,
            1.0,
        )
        config["invertY"] = bool(config.get("invertY", True))

        return config

    @staticmethod
    def clamp(
        value: Any,
        minimum: float,
        maximum: float,
        fallback: float,
    ) -> float:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return fallback

        if number < minimum or number > maximum:
            return fallback
        return number

    def save_config(self) -> None:
        try:
            CONFIG_PATH.write_text(
                json.dumps(
                    self.config_data,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
        except Exception as exc:
            self.emit_log(f"保存配置失败: {exc}", "warning")

    def apply_config_to_controls(self) -> None:
        self.syncing_controls = True
        try:
            shoulder_map = {
                "left": "左肩",
                "center": "居中",
                "right": "右肩",
            }
            self.shoulder_control.set(
                shoulder_map[self.config_data["shoulder"]]
            )

            self.distance_slider.set(self.config_data["distance"])
            self.height_slider.set(self.config_data["pivotHeight"])
            self.screen_y_slider.set(self.config_data["screenY"])
            self.fov_slider.set(self.config_data["fieldOfView"])
            self.pitch_slider.set(self.config_data["pitchScale"])

            if self.config_data["invertY"]:
                self.invert_switch.select()
            else:
                self.invert_switch.deselect()

            self.refresh_value_labels()
        finally:
            self.syncing_controls = False

    def refresh_value_labels(self) -> None:
        self.distance_value.configure(
            text=f"{self.config_data['distance']:.1f} m"
        )
        self.height_value.configure(
            text=f"{self.config_data['pivotHeight']:.2f} m"
        )
        self.screen_y_value.configure(
            text=f"{self.config_data['screenY']:.2f}"
        )
        self.fov_value.configure(
            text=f"{self.config_data['fieldOfView']:.0f}°"
        )
        self.pitch_value.configure(
            text=f"{self.config_data['pitchScale']:.2f}x"
        )

    def config_changed(self) -> None:
        self.save_config()

        if self.apply_after is not None:
            try:
                self.after_cancel(self.apply_after)
            except Exception:
                pass

        self.apply_after = self.after(
            350,
            self.apply_config_debounced,
        )

    def on_shoulder_changed(self, value: str) -> None:
        if self.syncing_controls:
            return

        reverse_map = {
            "左肩": "left",
            "居中": "center",
            "右肩": "right",
        }
        self.config_data["shoulder"] = reverse_map[value]
        self.config_changed()

    def on_invert_changed(self) -> None:
        if self.syncing_controls:
            return

        self.config_data["invertY"] = bool(
            self.invert_switch.get()
        )
        self.config_changed()

    def on_distance_changed(self, value: float) -> None:
        if self.syncing_controls:
            return
        self.config_data["distance"] = round(float(value), 2)
        self.refresh_value_labels()
        self.config_changed()

    def on_height_changed(self, value: float) -> None:
        if self.syncing_controls:
            return
        self.config_data["pivotHeight"] = round(float(value), 2)
        self.refresh_value_labels()
        self.config_changed()

    def on_screen_y_changed(self, value: float) -> None:
        if self.syncing_controls:
            return
        self.config_data["screenY"] = round(float(value), 3)
        self.refresh_value_labels()
        self.config_changed()

    def on_fov_changed(self, value: float) -> None:
        if self.syncing_controls:
            return
        self.config_data["fieldOfView"] = round(float(value), 1)
        self.refresh_value_labels()
        self.config_changed()

    def on_pitch_changed(self, value: float) -> None:
        if self.syncing_controls:
            return
        self.config_data["pitchScale"] = round(float(value), 2)
        self.refresh_value_labels()
        self.config_changed()

    def reset_config(self) -> None:
        self.config_data = dict(DEFAULT_CONFIG)
        self.apply_config_to_controls()
        self.save_config()
        self.apply_config_requested()

    def apply_config_debounced(self) -> None:
        self.apply_after = None
        if self.connected:
            self.apply_config_requested(silent=True)

    def apply_config_requested(self, silent: bool = False) -> None:
        if not self.connected:
            if not silent:
                self.emit_log(
                    "当前未连接，参数已保存，连接后自动应用。",
                    "warning",
                )
            return

        payload = dict(self.config_data)

        def success(result: Any) -> None:
            if not silent:
                self.emit_log(f"参数已应用: {result}")

        self.run_rpc_async(
            "setconfig",
            payload,
            on_success=success,
            description="应用参数",
        )

    # ------------------------------------------------------------
    # 日志
    # ------------------------------------------------------------
    def emit_log(
        self,
        message: str,
        level: str = "info",
    ) -> None:
        FILE_LOG.write(level, message)
        self.log_queue.put((level, message))

    def drain_logs(self) -> None:
        if self.closing:
            return

        processed = 0
        while processed < 80:
            try:
                level, message = self.log_queue.get_nowait()
            except queue.Empty:
                break

            timestamp = datetime.now().strftime("%H:%M:%S")
            label = {
                "error": "错误",
                "warning": "警告",
                "warn": "警告",
                "debug": "调试",
            }.get(level, "信息")

            self.log_text.insert(
                "end",
                f"[{timestamp}] [{label}] {message}\n",
            )
            processed += 1

        if processed:
            self.log_text.see("end")

            try:
                line_count = int(
                    self.log_text.index("end-1c").split(".")[0]
                )
                if line_count > 2500:
                    self.log_text.delete(
                        "1.0",
                        f"{line_count - 2500}.0",
                    )
            except Exception:
                pass

        self.after(
            20 if not self.log_queue.empty() else 100,
            self.drain_logs,
        )

    def open_log_dir(self) -> None:
        try:
            LOG_DIR.mkdir(parents=True, exist_ok=True)

            if os.name == "nt":
                os.startfile(LOG_DIR)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                os.system(f'open "{LOG_DIR}"')
            else:
                os.system(
                    f'xdg-open "{LOG_DIR}" >/dev/null 2>&1 &'
                )
        except Exception as exc:
            self.emit_log(
                f"打开日志目录失败: {exc}",
                "error",
            )

    # ------------------------------------------------------------
    # Frida
    # ------------------------------------------------------------
    @staticmethod
    def find_game_pid() -> Optional[int]:
        for process in psutil.process_iter(["pid", "name"]):
            try:
                name = (process.info.get("name") or "").lower()

                if name in PROCESS_NAMES or "unitycrossfire" in name:
                    return int(process.info["pid"])
            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                TypeError,
                ValueError,
            ):
                continue

        return None

    def connection_loop(self) -> None:
        while not self.stop_event.is_set():
            if self.connected:
                if self.pid is None or not psutil.pid_exists(self.pid):
                    self.handle_disconnect("游戏进程已结束")

                self.connect_event.wait(timeout=1.5)
                self.connect_event.clear()
                continue

            pid = self.find_game_pid()

            if pid is None:
                self.set_connection_ui("waiting", None)
                self.connect_event.wait(timeout=2.0)
                self.connect_event.clear()
                continue

            self.set_connection_ui("connecting", pid)

            try:
                self.connect_once(pid)
            except frida.PermissionDeniedError:
                self.emit_log(
                    "Frida 权限不足，请以管理员身份运行 UI。",
                    "error",
                )
                self.set_connection_ui("error", pid)
                self.connect_event.wait(timeout=5.0)
                self.connect_event.clear()
            except Exception as exc:
                self.emit_log(f"连接失败: {exc}", "error")
                self.disconnect_resources(call_cleanup=False)
                self.set_connection_ui("error", pid)
                self.connect_event.wait(timeout=3.0)
                self.connect_event.clear()

    def connect_once(self, pid: int) -> None:
        if not SCRIPT_PATH.exists():
            raise FileNotFoundError(
                f"未找到 {SCRIPT_NAME}，请把 UI 和 JS 放在同一目录。"
            )

        source = SCRIPT_PATH.read_text(encoding="utf-8")

        if len(source) < 1000:
            raise RuntimeError("JS 文件内容异常。")

        session = frida.attach(pid)
        session.on("detached", self.on_session_detached)

        script = session.create_script(source)
        script.on("message", self.on_script_message)
        script.load()

        with self.state_lock:
            self.session = session
            self.script = script
            self.pid = pid

        install_result = self.call_rpc("installhooks")

        if not isinstance(install_result, dict) or not install_result.get("ok"):
            raise RuntimeError(f"installhooks 失败: {install_result}")

        with self.state_lock:
            self.connected = True

        self.set_connection_ui("connected", pid)
        self.emit_log(
            f"已连接游戏 PID={pid}，最小化 Hook 已安装。"
        )

        self.call_rpc("setconfig", dict(self.config_data))
        status = self.call_rpc("getstatus")
        self.schedule_ui(lambda: self.apply_status(status))

    def call_rpc(self, name: str, *args: Any) -> Any:
        with self.state_lock:
            script = self.script

        if script is None:
            raise RuntimeError("Frida 脚本未连接")

        try:
            with self.rpc_lock:
                method = getattr(script.exports_sync, name)
                return method(*args)
        except (
            frida.InvalidOperationError,
            frida.TransportError,
        ) as exc:
            self.handle_disconnect(str(exc))
            raise

    def run_rpc_async(
        self,
        name: str,
        *args: Any,
        on_success: Optional[Callable[[Any], None]] = None,
        description: str = "",
    ) -> None:
        def worker() -> None:
            try:
                result = self.call_rpc(name, *args)

                if on_success is not None:
                    self.schedule_ui(
                        lambda: on_success(result)
                    )
            except Exception as exc:
                label = description or name
                self.emit_log(
                    f"{label}失败: {exc}",
                    "error",
                )

        threading.Thread(
            target=worker,
            name=f"RPC-{name}",
            daemon=True,
        ).start()

    def on_script_message(
        self,
        message: dict[str, Any],
        data: Any,
    ) -> None:
        message_type = message.get("type")

        if message_type == "send":
            payload = message.get("payload")

            if isinstance(payload, dict) and payload.get("type") == "log":
                level = str(payload.get("level", "info"))
                module = str(payload.get("module", ""))
                text = str(payload.get("message", ""))
                extra = payload.get("extra")

                full = f"[{module}] {text}" if module else text

                if extra is not None:
                    try:
                        full += " | " + json.dumps(
                            extra,
                            ensure_ascii=False,
                            default=str,
                        )
                    except Exception:
                        full += f" | {extra}"

                self.emit_log(full, level)
            else:
                self.emit_log(f"[JS] {payload}")
            return

        if message_type == "error":
            description = message.get(
                "description",
                "未知脚本错误",
            )
            stack = message.get("stack", "")
            self.emit_log(
                f"Frida 脚本错误: {description}\n{stack}",
                "error",
            )

    def request_reconnect(self) -> None:
        self.emit_log("用户请求重新连接。")

        threading.Thread(
            target=self.reconnect_worker,
            name="TP-Minimal-Reconnect",
            daemon=True,
        ).start()

    def reconnect_worker(self) -> None:
        self.disconnect_resources(call_cleanup=True)
        self.connect_event.set()

    def on_session_detached(self, *args: Any) -> None:
        reason = str(args[0]) if args else "未知原因"
        self.handle_disconnect(reason)

    def handle_disconnect(self, reason: str) -> None:
        if not self.connected and self.script is None:
            return

        self.emit_log(
            f"连接已断开: {reason}",
            "warning",
        )
        self.disconnect_resources(call_cleanup=False)
        self.set_connection_ui("waiting", None)
        self.connect_event.set()

    def disconnect_resources(self, call_cleanup: bool) -> None:
        with self.state_lock:
            script = self.script
            session = self.session

        if call_cleanup and script is not None:
            try:
                with self.rpc_lock:
                    script.exports_sync.cleanup()
            except Exception as exc:
                FILE_LOG.write(
                    "warning",
                    f"cleanup 调用失败: {exc}",
                )

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

        with self.state_lock:
            self.script = None
            self.session = None
            self.pid = None
            self.connected = False
            self.enabled = False

        self.schedule_ui(self.show_disabled_ui)

    # ------------------------------------------------------------
    # 状态与开关
    # ------------------------------------------------------------
    def toggle_demo(self) -> None:
        if not self.connected:
            self.emit_log(
                "尚未连接游戏。",
                "warning",
            )
            return

        self.toggle_button.configure(state="disabled")

        threading.Thread(
            target=self.toggle_worker,
            name="TP-Minimal-Toggle",
            daemon=True,
        ).start()

    def toggle_worker(self) -> None:
        try:
            if self.enabled:
                result = self.call_rpc("disable")

                if isinstance(result, dict) and result.get("ok"):
                    self.schedule_ui(
                        lambda: self.set_enabled_ui(False)
                    )
                    self.emit_log("最小第三人称已关闭。")
                else:
                    self.emit_log(
                        f"关闭失败: {result}",
                        "error",
                    )
            else:
                self.call_rpc(
                    "setconfig",
                    dict(self.config_data),
                )
                result = self.call_rpc("enable")

                if isinstance(result, dict) and result.get("ok"):
                    self.schedule_ui(
                        lambda: self.set_enabled_ui(True)
                    )
                    self.emit_log("最小第三人称已开启。")
                else:
                    self.emit_log(
                        f"开启失败: {result}",
                        "warning",
                    )
        except Exception as exc:
            self.emit_log(
                f"切换失败: {exc}",
                "error",
            )
        finally:
            self.schedule_ui(
                lambda: self.toggle_button.configure(
                    state=(
                        "normal"
                        if self.connected
                        else "disabled"
                    )
                )
            )

    def status_tick(self) -> None:
        if self.closing:
            return

        if self.connected and not self.status_busy:
            self.status_busy = True

            threading.Thread(
                target=self.status_worker,
                name="TP-Minimal-Status",
                daemon=True,
            ).start()

        self.after(2000, self.status_tick)

    def status_worker(self) -> None:
        try:
            status = self.call_rpc("getstatus")
            self.schedule_ui(
                lambda: self.apply_status(status)
            )
        except Exception:
            pass
        finally:
            self.status_busy = False

    def apply_status(self, status: Any) -> None:
        if not isinstance(status, dict):
            return

        self.set_enabled_ui(bool(status.get("enabled")))

        stats = status.get("stats") or {}

        values = {
            "state": status.get("state", "-"),
            "pitchWrites": stats.get("pitchWrites", 0),
            "pitchWriteFailures": stats.get(
                "pitchWriteFailures",
                0,
            ),
            "lastPlayerPitch": (
                f"{float(stats.get('lastPlayerPitch', 0.0)):.2f}°"
            ),
            "lastYAxisWritten": (
                f"{float(stats.get('lastYAxisWritten', 0.5)):.3f}"
            ),
            "lastCameraPitch": (
                f"{float(stats.get('lastCameraPitch', 0.0)):.2f}°"
            ),
        }

        for key, value in values.items():
            label = self.status_labels.get(key)
            if label is not None:
                label.configure(text=str(value))

        self.status_text.delete("1.0", "end")
        self.status_text.insert(
            "end",
            json.dumps(
                status,
                ensure_ascii=False,
                indent=2,
                default=str,
            ),
        )

    def set_enabled_ui(self, enabled: bool) -> None:
        self.enabled = bool(enabled)

        if enabled:
            self.toggle_button.configure(
                text="关闭最小第三人称",
                fg_color=self.RED,
                hover_color=self.RED_HOVER,
            )
            self.mode_label.configure(
                text="当前：最小第三人称已开启"
            )
        else:
            self.toggle_button.configure(
                text="开启最小第三人称",
                fg_color=self.GREEN,
                hover_color=self.GREEN_HOVER,
            )
            self.mode_label.configure(
                text=(
                    "当前：已连接"
                    if self.connected
                    else "当前：未连接"
                )
            )

    def show_disabled_ui(self) -> None:
        self.set_enabled_ui(False)

    def set_connection_ui(
        self,
        mode: str,
        pid: Optional[int],
    ) -> None:
        def update() -> None:
            states = {
                "waiting": (
                    "● 等待游戏",
                    self.ORANGE,
                ),
                "connecting": (
                    "● 正在连接",
                    "#2D72B8",
                ),
                "connected": (
                    "● 已连接",
                    self.GREEN,
                ),
                "error": (
                    "● 连接失败",
                    self.RED,
                ),
            }

            text, color = states.get(
                mode,
                ("● 未连接", self.MUTED),
            )

            self.connection_label.configure(
                text=text,
                text_color=color,
            )
            self.pid_label.configure(
                text=f"PID: {pid}" if pid else "PID: -"
            )

            connected = mode == "connected"
            self.set_connected_controls(connected)

        self.schedule_ui(update)

    def set_connected_controls(self, connected: bool) -> None:
        state = "normal" if connected else "disabled"

        for widget in (
            self.toggle_button,
            self.apply_button,
        ):
            widget.configure(state=state)

    # ------------------------------------------------------------
    # 退出
    # ------------------------------------------------------------
    def schedule_ui(
        self,
        callback: Callable[[], None],
    ) -> None:
        if self.closing:
            return

        try:
            self.after(0, callback)
        except Exception:
            pass

    def on_close(self) -> None:
        if self.closing:
            return

        self.closing = True
        self.stop_event.set()
        self.connect_event.set()

        FILE_LOG.write(
            "info",
            "用户关闭 UI，开始清理。",
        )

        try:
            if self.apply_after is not None:
                self.after_cancel(self.apply_after)
        except Exception:
            pass

        self.disconnect_resources(call_cleanup=True)

        try:
            self.destroy()
        except Exception:
            pass


def main() -> None:
    app = MinimalThirdPersonUI()
    app.mainloop()


if __name__ == "__main__":
    main()
