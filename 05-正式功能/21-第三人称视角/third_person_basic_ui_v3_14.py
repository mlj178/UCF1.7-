# -*- coding: utf-8 -*-
"""
最小可用第三人称射击版 v3.4 UI

配套脚本：
    third_person_basic_v3_3.js

依赖：
    pip install customtkinter frida-tools psutil

功能：
    - 自动检测并附加 UnityCrossFire.exe
    - 开启/关闭最小第三人称射击补丁
    - 只配置 7 个基础参数
    - 显示相机、WASD、射击和生命周期状态
    - 记录结构化 TXT 日志
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


APP_VERSION = "3.14"
PROCESS_NAMES = ("unitycrossfire.exe", "unitycrossfire")
SCRIPT_NAME = "third_person_basic_v3_14_stable_yaw.js"

def _get_app_dir() -> Path:
    """EXE 旁边（配置/日志写入位置）"""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def _get_internal_dir() -> Path:
    """打包内部资源位置（JS 脚本等只读资源）"""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


APP_DIR = _get_app_dir()
INTERNAL_DIR = _get_internal_dir()

SCRIPT_PATH = INTERNAL_DIR / SCRIPT_NAME
CONFIG_PATH = APP_DIR / "third_person_basic_v3_14_config.json"
LOG_DIR = APP_DIR / "logs"

DEFAULT_CONFIG: dict[str, Any] = {
    "shoulder": "center",
    "distance": 3.0,
    "pivotHeight": 1.35,
    "invertY": False,
}


def show_error(message: str) -> None:
    try:
        if os.name == "nt":
            ctypes.windll.user32.MessageBoxW(
                0,
                message,
                "第三人称基础版",
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


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class FileLogger:
    def __init__(self) -> None:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.path = LOG_DIR / f"third_person_mv_tps_{stamp}.txt"

        self.logger = logging.getLogger(f"mv_tps_{id(self)}")
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
        normalized = level.lower()
        if normalized == "error":
            self.logger.error(message)
        elif normalized in ("warning", "warn"):
            self.logger.warning(message)
        elif normalized == "debug":
            self.logger.debug(message)
        else:
            self.logger.info(message)


FILE_LOG = FileLogger()


class MinimalTPSUI(ctk.CTk):
    GREEN = "#2E9E5B"
    GREEN_HOVER = "#267F4B"
    RED = "#C44747"
    RED_HOVER = "#A83C3C"
    ORANGE = "#C88732"
    MUTED = "#909090"

    def __init__(self) -> None:
        super().__init__()

        self.title(f"最小可用第三人称射击版 v{APP_VERSION}")
        self.geometry("860x760+160+60")
        self.minsize(800, 680)

        self.session: Optional[Any] = None
        self.script: Optional[Any] = None
        self.pid: Optional[int] = None

        self.connected = False
        self.enabled = False
        self.waiting_enable = False
        self.closing = False
        self.status_busy = False
        self.syncing_controls = False

        self.rpc_lock = threading.RLock()
        self.state_lock = threading.RLock()
        self.stop_event = threading.Event()

        self.log_queue: queue.Queue[tuple[str, str]] = queue.Queue(
            maxsize=1000
        )
        self.dropped_ui_logs = 0
        self.apply_after: Optional[str] = None

        self.config_data = self.load_config()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.build_ui()
        self.apply_config_to_controls()
        self.set_connected_ui(False)

        self.after(100, self.drain_logs)
        self.after(8000, self.status_tick)

        threading.Thread(
            target=self.connection_loop,
            name="MV-TPS-Connection",
            daemon=True,
        ).start()

        self.emit_log(
            f"UI 已启动。日志文件：{FILE_LOG.path}",
            "info",
        )

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
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            header,
            text="最小可用第三人称射击版",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).grid(
            row=0,
            column=0,
            padx=16,
            pady=(14, 2),
            sticky="w",
        )

        self.connection_label = ctk.CTkLabel(
            header,
            text="等待游戏进程",
            text_color=self.ORANGE,
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        self.connection_label.grid(
            row=0,
            column=1,
            padx=16,
            pady=(14, 2),
            sticky="e",
        )

        ctk.CTkLabel(
            header,
            text=(
                "只保留：背后相机、人物模型、相机相对 WASD、"
                "枪口到准星射线。"
            ),
            text_color=self.MUTED,
            font=ctk.CTkFont(size=12),
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            padx=16,
            pady=(2, 14),
            sticky="w",
        )

        action = ctk.CTkFrame(self, corner_radius=12)
        action.grid(
            row=1,
            column=0,
            padx=14,
            pady=8,
            sticky="ew",
        )
        action.grid_columnconfigure((0, 1, 2), weight=1)

        self.toggle_button = ctk.CTkButton(
            action,
            text="开启第三人称",
            command=self.toggle_feature,
            fg_color=self.GREEN,
            hover_color=self.GREEN_HOVER,
            height=40,
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.toggle_button.grid(
            row=0,
            column=0,
            padx=(12, 6),
            pady=12,
            sticky="ew",
        )

        self.apply_button = ctk.CTkButton(
            action,
            text="应用参数",
            command=self.apply_config_requested,
            height=40,
        )
        self.apply_button.grid(
            row=0,
            column=1,
            padx=6,
            pady=12,
            sticky="ew",
        )

        self.reset_button = ctk.CTkButton(
            action,
            text="恢复默认参数",
            command=self.reset_config,
            height=40,
        )
        self.reset_button.grid(
            row=0,
            column=2,
            padx=(6, 12),
            pady=12,
            sticky="ew",
        )

        self.tabview = ctk.CTkTabview(self, corner_radius=12)
        self.tabview.grid(
            row=2,
            column=0,
            padx=14,
            pady=(8, 14),
            sticky="nsew",
        )

        camera_tab = self.tabview.add("基础参数")
        status_tab = self.tabview.add("运行状态")
        log_tab = self.tabview.add("日志")

        self.build_camera_tab(camera_tab)
        self.build_status_tab(status_tab)
        self.build_log_tab(log_tab)

    def build_camera_tab(self, tab: Any) -> None:
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkScrollableFrame(tab, corner_radius=10)
        frame.grid(
            row=0,
            column=0,
            padx=12,
            pady=12,
            sticky="nsew",
        )
        frame.grid_columnconfigure(0, weight=1)

        fixed = ctk.CTkFrame(frame, corner_radius=10)
        fixed.grid(
            row=0,
            column=0,
            padx=8,
            pady=(8, 12),
            sticky="ew",
        )
        fixed.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            fixed,
            text="肩位",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, padx=12, pady=12, sticky="w")

        ctk.CTkLabel(
            fixed,
            text="居中（固定）",
            text_color=self.MUTED,
        ).grid(row=0, column=1, padx=12, pady=12, sticky="e")

        self.distance_slider, self.distance_value = self.make_slider(
            frame,
            1,
            "镜头距离",
            1.5,
            8.0,
            65,
            " m",
            self.on_distance_changed,
        )

        self.pivot_slider, self.pivot_value = self.make_slider(
            frame,
            2,
            "上背部枢轴高度",
            0.5,
            2.5,
            40,
            " m",
            self.on_pivot_changed,
        )

        switch_frame = ctk.CTkFrame(frame, corner_radius=10)
        switch_frame.grid(
            row=3,
            column=0,
            padx=8,
            pady=10,
            sticky="ew",
        )

        self.invert_switch = ctk.CTkSwitch(
            switch_frame,
            text="反转鼠标上下方向",
            command=self.on_invert_changed,
        )
        self.invert_switch.pack(
            side="left",
            padx=14,
            pady=14,
        )

        ctk.CTkLabel(
            frame,
            text=(
                "WASD：相对于相机水平朝向移动；人物身体平滑跟随相机。\n"
                "射击：屏幕中心目标点 → 枪口位置 → GetShootRay。"
            ),
            justify="left",
            wraplength=720,
            text_color=self.MUTED,
            font=ctk.CTkFont(size=12),
        ).grid(
            row=4,
            column=0,
            padx=12,
            pady=(10, 16),
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
        frame = ctk.CTkFrame(parent, corner_radius=10)
        frame.grid(
            row=row,
            column=0,
            padx=8,
            pady=6,
            sticky="ew",
        )
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(
            row=0,
            column=0,
            padx=12,
            pady=(10, 2),
            sticky="w",
        )

        value_label = ctk.CTkLabel(
            frame,
            text=f"-{suffix}",
            text_color=self.MUTED,
        )
        value_label.grid(
            row=0,
            column=1,
            padx=12,
            pady=(10, 2),
            sticky="e",
        )

        slider = ctk.CTkSlider(
            frame,
            from_=minimum,
            to=maximum,
            number_of_steps=steps,
            command=command,
        )
        slider.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=12,
            pady=(4, 12),
            sticky="ew",
        )

        return slider, value_label

    def build_status_tab(self, tab: Any) -> None:
        tab.grid_columnconfigure((0, 1), weight=1)
        tab.grid_rowconfigure(4, weight=1)

        fields = [
            ("脚本状态", "state"),
            ("本地玩家", "haveLocalPlayer"),
            ("相机更新帧", "cameraFrames"),
            ("水平角模式", "yawSource"),
            ("移动向量修正", "movementVectorsModified"),
            ("射击 Ray 修正", "shootRayModified"),
            ("单帧目标计算", "aimFramesComputed"),
            ("同帧目标复用", "sameFrameAimReuses"),
            ("生命周期合并", "lifecycleEventsMerged"),
            ("脚本错误", "errors"),
        ]

        self.status_cards: dict[str, Any] = {}

        for index, (title, key) in enumerate(fields):
            card = ctk.CTkFrame(tab, corner_radius=10)
            card.grid(
                row=index // 2,
                column=index % 2,
                padx=8,
                pady=8,
                sticky="ew",
            )

            ctk.CTkLabel(
                card,
                text=title,
                text_color=self.MUTED,
                font=ctk.CTkFont(size=11),
            ).pack(anchor="w", padx=12, pady=(9, 1))

            value = ctk.CTkLabel(
                card,
                text="-",
                font=ctk.CTkFont(size=17, weight="bold"),
            )
            value.pack(anchor="w", padx=12, pady=(1, 10))
            self.status_cards[key] = value

        self.status_text = ctk.CTkTextbox(
            tab,
            wrap="word",
            font=("Consolas", 11),
        )
        self.status_text.grid(
            row=4,
            column=0,
            columnspan=2,
            padx=8,
            pady=(10, 8),
            sticky="nsew",
        )

    def build_log_tab(self, tab: Any) -> None:
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        self.log_text = ctk.CTkTextbox(
            tab,
            wrap="word",
            font=("Consolas", 11),
        )
        self.log_text.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew",
        )

        ctk.CTkButton(
            tab,
            text="清空界面日志",
            width=140,
            command=lambda: self.log_text.delete("1.0", "end"),
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=(0, 10),
            sticky="e",
        )

    # ------------------------------------------------------------
    # Config
    # ------------------------------------------------------------
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
        return max(minimum, min(maximum, number))

    def load_config(self) -> dict[str, Any]:
        config = dict(DEFAULT_CONFIG)

        try:
            if CONFIG_PATH.exists():
                loaded = json.loads(
                    CONFIG_PATH.read_text(encoding="utf-8")
                )
                if isinstance(loaded, dict):
                    for key in DEFAULT_CONFIG:
                        if key in loaded:
                            config[key] = loaded[key]
        except Exception as exc:
            FILE_LOG.write(
                "warning",
                f"读取配置失败，使用默认值：{exc}",
            )

        config["shoulder"] = "center"
        config["distance"] = self.clamp(
            config.get("distance"),
            1.5,
            8.0,
            3.0,
        )
        config["pivotHeight"] = self.clamp(
            config.get("pivotHeight"),
            0.5,
            2.5,
            1.35,
        )
        config["invertY"] = bool(config.get("invertY", False))
        return config

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
            self.emit_log(f"保存配置失败：{exc}", "warning")

    def apply_config_to_controls(self) -> None:
        self.syncing_controls = True
        try:
            self.distance_slider.set(self.config_data["distance"])
            self.pivot_slider.set(self.config_data["pivotHeight"])

            if self.config_data["invertY"]:
                self.invert_switch.select()
            else:
                self.invert_switch.deselect()

            self.refresh_value_labels()
        finally:
            self.syncing_controls = False

    def refresh_value_labels(self) -> None:
        self.distance_value.configure(
            text=f"{self.config_data['distance']:.2f} m"
        )
        self.pivot_value.configure(
            text=f"{self.config_data['pivotHeight']:.2f} m"
        )

    def config_changed(self) -> None:
        if self.syncing_controls:
            return

        self.config_data["shoulder"] = "center"
        self.save_config()

        if self.apply_after is not None:
            try:
                self.after_cancel(self.apply_after)
            except Exception:
                pass

        self.apply_after = self.after(
            300,
            self.apply_config_requested,
        )

    def on_distance_changed(self, value: float) -> None:
        if self.syncing_controls:
            return
        self.config_data["distance"] = round(float(value), 2)
        self.refresh_value_labels()
        self.config_changed()

    def on_pivot_changed(self, value: float) -> None:
        if self.syncing_controls:
            return
        self.config_data["pivotHeight"] = round(float(value), 2)
        self.refresh_value_labels()
        self.config_changed()

    def on_invert_changed(self) -> None:
        if self.syncing_controls:
            return
        self.config_data["invertY"] = bool(self.invert_switch.get())
        self.config_changed()

    def reset_config(self) -> None:
        self.config_data = dict(DEFAULT_CONFIG)
        self.apply_config_to_controls()
        self.save_config()
        self.apply_config_requested()
        self.emit_log("已恢复默认参数。")

    # ------------------------------------------------------------
    # Process / Frida
    # ------------------------------------------------------------
    @staticmethod
    def find_game_pid() -> Optional[int]:
        for process in psutil.process_iter(["pid", "name"]):
            try:
                name = str(process.info.get("name") or "").lower()
                if name in PROCESS_NAMES:
                    return int(process.info["pid"])
            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                ValueError,
                TypeError,
            ):
                continue
        return None

    def connection_loop(self) -> None:
        while not self.stop_event.is_set():
            pid = self.find_game_pid()

            with self.state_lock:
                connected = self.connected
                current_pid = self.pid

            if pid is None:
                if connected:
                    self.disconnect(
                        call_cleanup=False,
                        reason="游戏进程已退出",
                    )
                self.stop_event.wait(1.0)
                continue

            if not connected:
                self.connect(pid)
            elif current_pid != pid:
                self.disconnect(
                    call_cleanup=False,
                    reason="检测到游戏进程已更换",
                )
                self.connect(pid)

            self.stop_event.wait(1.0)

    def connect(self, pid: int) -> None:
        if not SCRIPT_PATH.exists():
            self.emit_log(
                f"缺少 JS 文件：{SCRIPT_PATH}",
                "error",
            )
            return

        session = None
        script = None

        try:
            source = SCRIPT_PATH.read_text(encoding="utf-8")
            device = frida.get_local_device()
            session = device.attach(pid)
            script = session.create_script(source)
            script.on("message", self.on_script_message)
            script.load()

            with self.state_lock:
                self.session = session
                self.script = script
                self.pid = pid
                self.connected = True
                self.enabled = False
                self.waiting_enable = False

            self.schedule_ui(lambda: self.set_connected_ui(True))
            self.emit_log(f"已连接游戏进程 PID={pid}")

            self.apply_config_sync(silent=True)
        except Exception as exc:
            self.emit_log(f"连接游戏失败：{exc}", "error")

            try:
                if script is not None:
                    script.unload()
            except Exception:
                pass

            try:
                if session is not None:
                    session.detach()
            except Exception:
                pass

    def disconnect(
        self,
        call_cleanup: bool,
        reason: str,
    ) -> None:
        with self.state_lock:
            session = self.session
            script = self.script

            self.session = None
            self.script = None
            self.pid = None
            self.connected = False
            self.enabled = False
            self.waiting_enable = False

        if call_cleanup and script is not None:
            try:
                with self.rpc_lock:
                    status = script.exports_sync.getstatus()

                    if (
                        isinstance(status, dict)
                        and status.get("enabled")
                        and status.get("haveCameraManager")
                        and not status.get("sessionDestroyed")
                    ):
                        script.exports_sync.disable()

                deadline = time.monotonic() + 1.5
                while time.monotonic() < deadline:
                    time.sleep(0.05)
                    try:
                        with self.rpc_lock:
                            status = script.exports_sync.getstatus()
                        if (
                            isinstance(status, dict)
                            and not status.get("enabled")
                            and not status.get("pendingDisable")
                        ):
                            break
                    except Exception:
                        break

                with self.rpc_lock:
                    script.exports_sync.cleanup()
            except Exception as exc:
                FILE_LOG.write(
                    "warning",
                    f"cleanup 调用失败：{exc}",
                )

        try:
            if script is not None:
                script.unload()
        except Exception:
            pass

        try:
            if session is not None:
                session.detach()
        except Exception:
            pass

        self.schedule_ui(lambda: self.set_connected_ui(False))
        self.emit_log(reason, "warning")

    # ------------------------------------------------------------
    # RPC actions
    # ------------------------------------------------------------
    def apply_config_sync(self, silent: bool = False) -> bool:
        with self.state_lock:
            script = self.script
            connected = self.connected

        if not connected or script is None:
            if not silent:
                self.emit_log("尚未连接游戏，参数已保存在本地。", "warning")
            return False

        try:
            payload = dict(self.config_data)
            payload["shoulder"] = "center"

            with self.rpc_lock:
                result = script.exports_sync.setconfig(payload)

            if not isinstance(result, dict) or not result.get("ok"):
                if not silent:
                    self.emit_log(f"应用参数失败：{result}", "error")
                return False

            returned = result.get("config")
            if isinstance(returned, dict):
                for key in DEFAULT_CONFIG:
                    if key in returned:
                        self.config_data[key] = returned[key]
                self.config_data["shoulder"] = "center"
                self.save_config()
                self.schedule_ui(self.apply_config_to_controls)

            if not silent:
                self.emit_log(result.get("message", "参数已应用。"))
            return True
        except Exception as exc:
            if not silent:
                self.emit_log(f"应用参数异常：{exc}", "error")
            return False

    def apply_config_requested(self) -> None:
        self.apply_after = None
        threading.Thread(
            target=self.apply_config_sync,
            name="MV-TPS-Apply",
            daemon=True,
        ).start()

    def toggle_feature(self) -> None:
        if not self.connected:
            self.emit_log("请先启动游戏并等待连接。", "warning")
            return

        self.toggle_button.configure(state="disabled")

        threading.Thread(
            target=self.toggle_worker,
            name="MV-TPS-Toggle",
            daemon=True,
        ).start()

    def toggle_worker(self) -> None:
        with self.state_lock:
            script = self.script
            should_disable = self.enabled or self.waiting_enable

        if script is None:
            self.schedule_ui(
                lambda: self.toggle_button.configure(state="normal")
            )
            return

        try:
            if should_disable:
                with self.rpc_lock:
                    result = script.exports_sync.disable()

                self.emit_log(
                    result.get("message", "关闭命令已排队。")
                    if isinstance(result, dict)
                    else f"关闭结果：{result}"
                )
            else:
                self.apply_config_sync(silent=True)

                with self.rpc_lock:
                    result = script.exports_sync.enable()

                if isinstance(result, dict) and result.get("ok"):
                    if result.get("enabled"):
                        self.schedule_ui(
                            lambda: self.set_enabled_ui(True)
                        )
                    else:
                        with self.state_lock:
                            self.waiting_enable = True
                        self.schedule_ui(self.refresh_toggle_button)
                        self.emit_log(
                            result.get(
                                "message",
                                "开启命令已排队。",
                            )
                        )
                else:
                    self.emit_log(f"开启失败：{result}", "error")
        except Exception as exc:
            self.emit_log(f"切换功能异常：{exc}", "error")
        finally:
            self.schedule_ui(
                lambda: self.toggle_button.configure(state="normal")
            )

    # ------------------------------------------------------------
    # Script messages / status
    # ------------------------------------------------------------
    def on_script_message(
        self,
        message: dict[str, Any],
        data: Any,
    ) -> None:
        message_type = message.get("type")

        if message_type == "error":
            details = message.get("stack") or message.get("description")
            self.emit_log(f"Frida 脚本错误：{details}", "error")
            return

        if message_type != "send":
            self.emit_log(f"Frida 消息：{message}", "debug")
            return

        payload = message.get("payload")

        if not isinstance(payload, dict):
            self.emit_log(str(payload))
            return

        payload_type = payload.get("type")

        if payload_type == "log":
            level = str(payload.get("level", "info"))
            text = str(payload.get("message", ""))
            extra = payload.get("extra")
            if extra is not None:
                text += " | " + json.dumps(
                    extra,
                    ensure_ascii=False,
                    default=str,
                )
            self.emit_log(text, level)
            return

        if payload_type == "auto_enabled":
            self.schedule_ui(lambda: self.set_enabled_ui(True))
            self.emit_log("游戏主线程已完成第三人称开启。")
            return

        if payload_type == "auto_disabled":
            self.schedule_ui(lambda: self.set_enabled_ui(False))
            self.emit_log("游戏主线程已完成第三人称关闭。")
            return

        if payload_type == "session_destroyed":
            self.schedule_ui(lambda: self.set_enabled_ui(False))
            self.emit_log(
                f"游戏场景已销毁：{payload.get('reason', '-')}",
                "warning",
            )
            return

        if payload_type == "state_changed":
            self.emit_log(
                f"脚本状态：{payload.get('oldState')} -> "
                f"{payload.get('newState')}"
            )
            return

        self.emit_log(
            "脚本消息：" +
            json.dumps(payload, ensure_ascii=False, default=str),
            "debug",
        )

    def status_tick(self) -> None:
        if not self.closing and self.connected and not self.status_busy:
            self.status_busy = True
            threading.Thread(
                target=self.status_worker,
                name="MV-TPS-Status",
                daemon=True,
            ).start()

        if not self.closing:
            self.after(8000, self.status_tick)

    def status_worker(self) -> None:
        try:
            with self.state_lock:
                script = self.script

            if script is None:
                return

            with self.rpc_lock:
                status = script.exports_sync.getstatus()

            if isinstance(status, dict):
                self.schedule_ui(
                    lambda value=status: self.apply_status(value)
                )
        except Exception as exc:
            FILE_LOG.write("warning", f"读取状态失败：{exc}")
        finally:
            self.status_busy = False

    def apply_status(self, status: dict[str, Any]) -> None:
        enabled = bool(status.get("enabled"))
        pending = bool(status.get("pendingEnable"))

        with self.state_lock:
            self.enabled = enabled
            self.waiting_enable = pending and not enabled

        self.refresh_toggle_button()

        stats = status.get("stats")
        if not isinstance(stats, dict):
            stats = {}

        values = {
            "state": status.get("state", "-"),
            "haveLocalPlayer": (
                "已捕获" if status.get("haveLocalPlayer") else "未捕获"
            ),
            "cameraFrames": stats.get(
                "cameraFrames",
                0,
            ),
            "movementVectorsModified": stats.get(
                "movementVectorsModified",
                0,
            ),
            "shootRayModified": stats.get("shootRayModified", 0),
            "yawSource": "稳定最终相机方向",
            "aimFramesComputed": stats.get(
                "aimFramesComputed",
                0,
            ),
            "sameFrameAimReuses": stats.get(
                "sameFrameAimReuses",
                0,
            ),
            "lifecycleEventsMerged": stats.get(
                "lifecycleEventsMerged",
                0,
            ),
            "errors": stats.get("errors", 0),
        }

        for key, value in values.items():
            label = self.status_cards.get(key)
            if label is not None:
                label.configure(text=str(value))

        runtime = status.get("runtime")
        summary = {
            "enabled": status.get("enabled"),
            "pendingEnable": status.get("pendingEnable"),
            "pendingDisable": status.get("pendingDisable"),
            "haveCameraManager": status.get("haveCameraManager"),
            "haveLocalPlayer": status.get("haveLocalPlayer"),
            "config": status.get("config"),
            "runtime": runtime,
            "stats": {
                "cameraFrames": stats.get("cameraFrames"),
                "cameraFailures": stats.get("cameraFailures"),
                "movementVectorsModified": stats.get(
                    "movementVectorsModified"
                ),
                "physicsRaycastCalls": stats.get("physicsRaycastCalls"),
                "shootRayCalls": stats.get("shootRayCalls"),
                "shootRayModified": stats.get("shootRayModified"),
                "shootRayFailures": stats.get("shootRayFailures"),
                                "errors": stats.get("errors"),
            },
        }

        self.status_text.delete("1.0", "end")
        self.status_text.insert(
            "end",
            json.dumps(
                summary,
                ensure_ascii=False,
                indent=2,
                default=str,
            ),
        )

    # ------------------------------------------------------------
    # UI state / logs / close
    # ------------------------------------------------------------
    def set_connected_ui(self, connected: bool) -> None:
        self.connected = connected

        if connected:
            self.connection_label.configure(
                text=f"已连接 PID {self.pid}",
                text_color=self.GREEN,
            )
        else:
            self.connection_label.configure(
                text="等待游戏进程",
                text_color=self.ORANGE,
            )
            self.set_enabled_ui(False)

        state = "normal" if connected else "disabled"
        self.toggle_button.configure(state=state)
        self.apply_button.configure(state=state)

    def set_enabled_ui(self, enabled: bool) -> None:
        with self.state_lock:
            self.enabled = enabled
            self.waiting_enable = False
        self.refresh_toggle_button()

    def refresh_toggle_button(self) -> None:
        if self.enabled:
            self.toggle_button.configure(
                text="关闭第三人称",
                fg_color=self.RED,
                hover_color=self.RED_HOVER,
            )
        elif self.waiting_enable:
            self.toggle_button.configure(
                text="取消等待开启",
                fg_color=self.ORANGE,
                hover_color="#A56E28",
            )
        else:
            self.toggle_button.configure(
                text="开启第三人称",
                fg_color=self.GREEN,
                hover_color=self.GREEN_HOVER,
            )

    def schedule_ui(self, callback: Callable[[], None]) -> None:
        if self.closing:
            return
        try:
            self.after(0, callback)
        except Exception:
            pass

    def emit_log(
        self,
        message: str,
        level: str = "info",
    ) -> None:
        FILE_LOG.write(level, message)

        try:
            self.log_queue.put_nowait((level, message))
        except queue.Full:
            self.dropped_ui_logs += 1
            try:
                self.log_queue.get_nowait()
            except queue.Empty:
                pass
            try:
                self.log_queue.put_nowait((level, message))
            except queue.Full:
                pass

    def drain_logs(self) -> None:
        processed = 0

        while processed < 80:
            try:
                level, message = self.log_queue.get_nowait()
            except queue.Empty:
                break

            stamp = datetime.now().strftime("%H:%M:%S")
            self.log_text.insert(
                "end",
                f"[{stamp}] [{level.upper()}] {message}\n",
            )
            processed += 1

        if processed:
            if self.dropped_ui_logs:
                self.log_text.insert(
                    "end",
                    f"[性能] 已丢弃 {self.dropped_ui_logs} 条旧 UI 日志；"
                    "TXT 日志不受影响。\n",
                )
                self.dropped_ui_logs = 0
            self.log_text.see("end")

        if not self.closing:
            delay = 50 if not self.log_queue.empty() else 150
            self.after(delay, self.drain_logs)

    def on_close(self) -> None:
        if self.closing:
            return

        self.closing = True
        self.stop_event.set()

        self.toggle_button.configure(state="disabled")
        self.apply_button.configure(state="disabled")
        self.reset_button.configure(state="disabled")
        self.connection_label.configure(
            text="正在安全退出…",
            text_color=self.ORANGE,
        )

        threading.Thread(
            target=self.close_worker,
            name="MV-TPS-Close",
            daemon=True,
        ).start()

    def close_worker(self) -> None:
        self.disconnect(
            call_cleanup=True,
            reason="UI 已关闭",
        )
        try:
            self.after(0, self.destroy)
        except Exception:
            pass


def main() -> None:
    if not SCRIPT_PATH.exists():
        show_error(
            "缺少配套脚本：\n"
            f"{SCRIPT_PATH}\n\n"
            "请将 JS 和 Python UI 放在同一目录。"
        )
        raise SystemExit(1)

    app = MinimalTPSUI()
    app.mainloop()


if __name__ == "__main__":
    main()
