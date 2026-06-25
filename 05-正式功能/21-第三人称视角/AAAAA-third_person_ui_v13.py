# -*- coding: utf-8 -*-
"""
UCF1.7 第三人称视角修改器 v11 配套 UI

配套脚本:
    AAAAA-third_person_v11_camera_finalstage.js

依赖:
    pip install customtkinter frida-tools psutil

功能:
    - 自动检测并附加 UnityCrossFire.exe
    - 自动加载 JS、安装 Hook、断线重连
    - 第三人称启停
    - 左右肩、距离、水平偏移、高度、FOV 调节
    - 状态与 Hook 统计显示
    - 模型诊断、瞄准诊断、快照
    - 参数本地保存
    - 关闭时调用 cleanup()，尽量恢复游戏原始状态
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


def _show_dependency_error(message: str) -> None:
    """在缺少依赖时尽量给出可见提示。"""
    try:
        if os.name == "nt":
            ctypes.windll.user32.MessageBoxW(0, message, "第三人称 UI 启动失败", 0x10)
        else:
            print(message, file=sys.stderr)
    except Exception:
        print(message, file=sys.stderr)


try:
    import customtkinter as ctk
except ImportError:
    _show_dependency_error(
        "缺少 customtkinter。\n\n"
        "请在命令提示符执行：\n"
        "pip install customtkinter frida-tools psutil"
    )
    raise SystemExit(1)

try:
    import frida
except ImportError:
    _show_dependency_error(
        "缺少 frida。\n\n"
        "请在命令提示符执行：\n"
        "pip install frida-tools"
    )
    raise SystemExit(1)

try:
    import psutil
except ImportError:
    _show_dependency_error(
        "缺少 psutil。\n\n"
        "请在命令提示符执行：\n"
        "pip install psutil"
    )
    raise SystemExit(1)


APP_VERSION = "13.0"
PROCESS_NAMES = ("unitycrossfire.exe", "unitycrossfire")
SCRIPT_FILENAME = "AAAAA-third_person_v11_camera_finalstage.js"

BASE_DIR = Path(__file__).resolve().parent
SCRIPT_PATH = BASE_DIR / SCRIPT_FILENAME
SCRIPT_TXT_FALLBACK = BASE_DIR / "AAAAA-third_person_v11_camera_finalstage.txt"
CONFIG_PATH = BASE_DIR / "third_person_ui_config.json"
LOG_DIR = BASE_DIR / "logs"

DEFAULT_CONFIG = {
    "shoulderSide": "right",
    "distance": 3.0,
    "horizontalOffset": 0.55,
    "heightOffset": 0.15,
    "fieldOfView": 70.0,
    "sensitivity": 1.0,
    "aimDiagnosticSeconds": 20,
    "syncCharacterYaw": True,
    "verticalInputEnabled": True,
}

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class FileLogger:
    def __init__(self, log_dir: Path) -> None:
        log_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = log_dir / f"third_person_ui_{stamp}.txt"

        self.logger = logging.getLogger(f"third_person_ui_{id(self)}")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        handler = logging.FileHandler(self.log_path, encoding="utf-8")
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        self.logger.addHandler(handler)

        self.info("=" * 72)
        self.info(f"第三人称视角修改器 UI v{APP_VERSION}")
        self.info(f"工作目录: {BASE_DIR}")
        self.info(f"目标脚本: {SCRIPT_PATH}")
        self.info("=" * 72)

    def write(self, level: str, message: str) -> None:
        level = level.lower()
        if level == "error":
            self.logger.error(message)
        elif level in ("warn", "warning"):
            self.logger.warning(message)
        elif level == "debug":
            self.logger.debug(message)
        else:
            self.logger.info(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warn(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)


file_log = FileLogger(LOG_DIR)


class ThirdPersonApp(ctk.CTk):
    COLOR_GREEN = "#2E9E5B"
    COLOR_GREEN_HOVER = "#267F4B"
    COLOR_RED = "#C44747"
    COLOR_RED_HOVER = "#A83C3C"
    COLOR_ORANGE = "#C88732"
    COLOR_BLUE = "#2D72B8"
    COLOR_MUTED = "#8A8A8A"

    def __init__(self) -> None:
        super().__init__()

        self.title(f"第三人称视角修改器 v{APP_VERSION}")
        self.geometry("860x790+160+70")
        self.minsize(820, 720)

        self.session: Optional[Any] = None
        self.script: Optional[Any] = None
        self.current_pid: Optional[int] = None

        self.is_connected = False
        self.is_enabled = False
        self._closing = False
        self._status_poll_busy = False
        self._config_apply_after: Optional[str] = None
        self._ui_syncing = False

        self._state_lock = threading.RLock()
        self._rpc_lock = threading.RLock()
        self._stop_event = threading.Event()
        self._connect_wakeup = threading.Event()
        self._log_queue: queue.Queue[tuple[str, str]] = queue.Queue()
        self._aim_diag_lines: list[str] = []
        self._aim_diag_session_id: str = ''
        self._aim_diag_ui_pending = False
        self._aim_diag_dropped = 0
        self._max_ui_log_lines = 2500

        self.config_data = self._load_config()

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._build_ui()
        self._apply_config_to_controls()
        self._set_controls_connected(False)
        self._drain_log_queue()

        threading.Thread(
            target=self._connection_loop,
            name="ThirdPersonConnection",
            daemon=True,
        ).start()

        self.after(1200, self._status_poll_tick)
        self._emit_log("UI 已启动，正在等待游戏进程。")

    # ============================================================
    # UI 构建
    # ============================================================
    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, corner_radius=12)
        header.grid(row=0, column=0, padx=14, pady=(14, 8), sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.grid(row=0, column=0, padx=16, pady=12, sticky="w")

        ctk.CTkLabel(
            title_box,
            text="第三人称视角修改器",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text=f"配套脚本：{SCRIPT_FILENAME}",
            font=ctk.CTkFont(size=11),
            text_color=self.COLOR_MUTED,
        ).pack(anchor="w", pady=(2, 0))

        status_box = ctk.CTkFrame(header, fg_color="transparent")
        status_box.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.connection_status = ctk.CTkLabel(
            status_box,
            text="● 等待游戏",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.COLOR_ORANGE,
        )
        self.connection_status.grid(row=0, column=0, padx=8, sticky="e")

        self.pid_label = ctk.CTkLabel(
            status_box,
            text="PID: -",
            font=ctk.CTkFont(size=11),
            text_color=self.COLOR_MUTED,
        )
        self.pid_label.grid(row=1, column=0, padx=8, sticky="e")

        self.reconnect_button = ctk.CTkButton(
            status_box,
            text="重新连接",
            width=92,
            command=self._request_reconnect,
        )
        self.reconnect_button.grid(row=0, column=1, rowspan=2, padx=(8, 0))

        self.tabview = ctk.CTkTabview(self, corner_radius=12)
        self.tabview.grid(row=1, column=0, padx=14, pady=(0, 8), sticky="nsew")

        self.tab_camera = self.tabview.add("相机控制")
        self.tab_status = self.tabview.add("运行状态")
        self.tab_diag = self.tabview.add("诊断工具")
        self.tab_log = self.tabview.add("日志")

        self._build_camera_tab()
        self._build_status_tab()
        self._build_diag_tab()
        self._build_log_tab()

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, padx=16, pady=(0, 10), sticky="ew")
        footer.grid_columnconfigure(0, weight=1)

        self.footer_label = ctk.CTkLabel(
            footer,
            text=f"日志：{file_log.log_path}",
            font=ctk.CTkFont(size=10),
            text_color=self.COLOR_MUTED,
        )
        self.footer_label.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            footer,
            text="关闭 UI 时会调用 cleanup() 并卸载脚本",
            font=ctk.CTkFont(size=10),
            text_color=self.COLOR_MUTED,
        ).grid(row=0, column=1, sticky="e")

    def _build_camera_tab(self) -> None:
        tab = self.tab_camera
        tab.grid_columnconfigure((0, 1), weight=1)
        tab.grid_rowconfigure(2, weight=1)

        toggle_card = ctk.CTkFrame(tab, corner_radius=12)
        toggle_card.grid(
            row=0, column=0, columnspan=2,
            padx=12, pady=(12, 8), sticky="ew"
        )
        toggle_card.grid_columnconfigure(0, weight=1)

        self.toggle_button = ctk.CTkButton(
            toggle_card,
            text="开启第三人称",
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=self.COLOR_GREEN,
            hover_color=self.COLOR_GREEN_HOVER,
            command=self._toggle_requested,
        )
        self.toggle_button.grid(row=0, column=0, padx=14, pady=(14, 6), sticky="ew")

        self.mode_label = ctk.CTkLabel(
            toggle_card,
            text="当前模式：第一人称",
            font=ctk.CTkFont(size=13),
        )
        self.mode_label.grid(row=1, column=0, padx=14, pady=(0, 12))

        shoulder_card = ctk.CTkFrame(tab, corner_radius=12)
        shoulder_card.grid(row=1, column=0, padx=(12, 6), pady=8, sticky="nsew")
        shoulder_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            shoulder_card,
            text="肩位",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).grid(row=0, column=0, padx=12, pady=(12, 6))

        self.shoulder_control = ctk.CTkSegmentedButton(
            shoulder_card,
            values=["左肩", "右肩"],
            command=self._on_shoulder_changed,
        )
        self.shoulder_control.grid(row=1, column=0, padx=14, pady=(4, 8), sticky="ew")

        self.vertical_input_switch = ctk.CTkSwitch(
            shoulder_card,
            text="鼠标上下控制镜头",
            command=self._on_camera_switch_changed,
        )
        self.vertical_input_switch.grid(row=2, column=0, padx=14, pady=(4, 5), sticky="w")

        self.yaw_sync_switch = ctk.CTkSwitch(
            shoulder_card,
            text="人物与枪械水平跟随镜头",
            command=self._on_camera_switch_changed,
        )
        self.yaw_sync_switch.grid(row=3, column=0, padx=14, pady=(4, 14), sticky="w")

        preset_card = ctk.CTkFrame(tab, corner_radius=12)
        preset_card.grid(row=1, column=1, padx=(6, 12), pady=8, sticky="nsew")
        preset_card.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            preset_card,
            text="操作",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).grid(row=0, column=0, columnspan=2, padx=12, pady=(12, 6))

        self.apply_button = ctk.CTkButton(
            preset_card,
            text="立即应用",
            command=self._apply_config_requested,
        )
        self.apply_button.grid(row=1, column=0, padx=(12, 5), pady=(4, 14), sticky="ew")

        self.reset_button = ctk.CTkButton(
            preset_card,
            text="恢复默认",
            fg_color="#555555",
            hover_color="#444444",
            command=self._reset_requested,
        )
        self.reset_button.grid(row=1, column=1, padx=(5, 12), pady=(4, 14), sticky="ew")

        controls = ctk.CTkScrollableFrame(tab, corner_radius=12)
        controls.grid(
            row=2, column=0, columnspan=2,
            padx=12, pady=(8, 12), sticky="nsew"
        )
        controls.grid_columnconfigure(0, weight=1)

        self.distance_slider, self.distance_value = self._make_slider(
            controls, 0, "相机距离", 1.0, 8.0, 70, " m",
            self._on_distance_changed,
        )
        self.horizontal_slider, self.horizontal_value = self._make_slider(
            controls, 1, "水平肩位偏移", 0.0, 1.5, 60, " m",
            self._on_horizontal_changed,
        )
        self.height_slider, self.height_value = self._make_slider(
            controls, 2, "相机高度偏移", -1.0, 1.5, 50, " m",
            self._on_height_changed,
        )
        self.fov_slider, self.fov_value = self._make_slider(
            controls, 3, "视野 FOV", 40.0, 110.0, 70, "°",
            self._on_fov_changed,
        )
        self.sensitivity_slider, self.sensitivity_value = self._make_slider(
            controls, 4, "鼠标灵敏度（脚本暂未实际应用）",
            0.2, 3.0, 56, "x",
            self._on_sensitivity_changed,
        )

        ctk.CTkLabel(
            controls,
            text=(
                "参数会自动保存。拖动滑块后约 350ms 合并发送一次，"
                "避免高频 RPC 调用导致界面或游戏卡顿。"
            ),
            wraplength=700,
            justify="left",
            font=ctk.CTkFont(size=11),
            text_color=self.COLOR_MUTED,
        ).grid(row=5, column=0, padx=14, pady=(8, 14), sticky="w")

    def _make_slider(
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
        frame.grid(row=row, column=0, padx=10, pady=7, sticky="ew")
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
            text=f"0{suffix}",
            width=72,
            anchor="e",
            font=ctk.CTkFont(size=12),
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

    def _build_status_tab(self) -> None:
        tab = self.tab_status
        tab.grid_columnconfigure((0, 1), weight=1)
        tab.grid_rowconfigure(2, weight=1)

        connection = ctk.CTkFrame(tab, corner_radius=12)
        connection.grid(
            row=0, column=0, columnspan=2,
            padx=12, pady=(12, 8), sticky="ew"
        )
        connection.grid_columnconfigure((1, 3), weight=1)

        self._status_field(connection, 0, 0, "FSM 状态", "state")
        self._status_field(connection, 0, 2, "第三人称", "enabled")
        self._status_field(connection, 1, 0, "GameManager", "haveGM")
        self._status_field(connection, 1, 2, "CameraManager", "haveCameraManager")

        stats_frame = ctk.CTkFrame(tab, corner_radius=12)
        stats_frame.grid(
            row=1, column=0, columnspan=2,
            padx=12, pady=8, sticky="ew"
        )
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        stats = [
            ("最终相机写入", "finalCameraWrites"),
            ("Collider 回调", "colliderCallbacks"),
            ("Hook 调用", "hookCalls"),
            ("状态变化", "stateChanges"),
            ("对象重取", "objectRegets"),
            ("错误数", "errors"),
        ]
        self.stat_value_labels: dict[str, Any] = {}
        for idx, (label, key) in enumerate(stats):
            box = ctk.CTkFrame(stats_frame)
            box.grid(
                row=idx // 3,
                column=idx % 3,
                padx=7, pady=7, sticky="nsew"
            )
            ctk.CTkLabel(
                box,
                text=label,
                font=ctk.CTkFont(size=11),
                text_color=self.COLOR_MUTED,
            ).pack(pady=(10, 2))
            value = ctk.CTkLabel(
                box,
                text="0",
                font=ctk.CTkFont(size=20, weight="bold"),
            )
            value.pack(pady=(0, 10))
            self.stat_value_labels[key] = value

        status_box = ctk.CTkFrame(tab, corner_radius=12)
        status_box.grid(
            row=2, column=0, columnspan=2,
            padx=12, pady=(8, 12), sticky="nsew"
        )
        status_box.grid_columnconfigure(0, weight=1)
        status_box.grid_rowconfigure(1, weight=1)

        toolbar = ctk.CTkFrame(status_box, fg_color="transparent")
        toolbar.grid(row=0, column=0, padx=10, pady=(8, 4), sticky="ew")
        toolbar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            toolbar,
            text="完整状态",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        self.refresh_status_button = ctk.CTkButton(
            toolbar,
            text="刷新",
            width=80,
            command=lambda: self._refresh_status_requested(sync_controls=True),
        )
        self.refresh_status_button.grid(row=0, column=1, sticky="e")

        self.status_text = ctk.CTkTextbox(status_box, font=("Consolas", 11))
        self.status_text.grid(row=1, column=0, padx=10, pady=(4, 10), sticky="nsew")
        self.status_text.insert("end", "尚未取得状态。\n")

    def _status_field(
        self, parent: Any, row: int, column: int, title: str, key: str
    ) -> None:
        ctk.CTkLabel(
            parent,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color=self.COLOR_MUTED,
        ).grid(row=row, column=column, padx=(12, 6), pady=10, sticky="w")

        label = ctk.CTkLabel(
            parent,
            text="-",
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        label.grid(row=row, column=column + 1, padx=(0, 12), pady=10, sticky="w")

        if not hasattr(self, "status_value_labels"):
            self.status_value_labels: dict[str, Any] = {}
        self.status_value_labels[key] = label

    def _build_diag_tab(self) -> None:
        tab = self.tab_diag
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)

        tools = ctk.CTkFrame(tab, corner_radius=12)
        tools.grid(row=0, column=0, padx=12, pady=(12, 8), sticky="ew")
        tools.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.debug_model_button = ctk.CTkButton(
            tools,
            text="模型/武器诊断",
            command=self._debug_model_requested,
        )
        self.debug_model_button.grid(row=0, column=0, padx=6, pady=10, sticky="ew")

        self.snapshot_button = ctk.CTkButton(
            tools,
            text="捕获瞄准快照",
            command=self._capture_snapshot_requested,
        )
        self.snapshot_button.grid(row=0, column=1, padx=6, pady=10, sticky="ew")

        self.stop_diag_button = ctk.CTkButton(
            tools,
            text="停止瞄准诊断",
            fg_color="#555555",
            hover_color="#444444",
            command=self._stop_aim_diag_requested,
        )
        self.stop_diag_button.grid(row=0, column=2, padx=6, pady=10, sticky="ew")

        self.diag_status_button = ctk.CTkButton(
            tools,
            text="诊断状态",
            command=self._aim_diag_status_requested,
        )
        self.diag_status_button.grid(row=0, column=3, padx=6, pady=10, sticky="ew")

        aim = ctk.CTkFrame(tab, corner_radius=12)
        aim.grid(row=1, column=0, padx=12, pady=8, sticky="ew")
        aim.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            aim,
            text="瞄准诊断时长",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, padx=12, pady=12, sticky="w")

        self.diag_duration_slider = ctk.CTkSlider(
            aim,
            from_=5,
            to=60,
            number_of_steps=55,
            command=self._on_diag_duration_changed,
        )
        self.diag_duration_slider.grid(row=0, column=1, padx=10, pady=12, sticky="ew")

        self.diag_duration_label = ctk.CTkLabel(aim, text="20 秒", width=65)
        self.diag_duration_label.grid(row=0, column=2, padx=(0, 8), pady=12)

        self.start_diag_button = ctk.CTkButton(
            aim,
            text="开始诊断",
            width=100,
            fg_color=self.COLOR_ORANGE,
            hover_color="#AA722B",
            command=self._start_aim_diag_requested,
        )
        self.start_diag_button.grid(row=0, column=3, padx=(4, 12), pady=12)

        output = ctk.CTkFrame(tab, corner_radius=12)
        output.grid(row=2, column=0, padx=12, pady=(8, 12), sticky="nsew")
        output.grid_columnconfigure(0, weight=1)
        output.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            output,
            text="诊断返回结果",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, padx=10, pady=(8, 4), sticky="w")

        self.diag_text = ctk.CTkTextbox(output, font=("Consolas", 11))
        self.diag_text.grid(row=1, column=0, padx=10, pady=(4, 10), sticky="nsew")
        self.diag_text.insert(
            "end",
            "进入对局后可执行模型诊断。\n"
            "瞄准诊断建议依次测试：腰射、ADS、切枪、近距离遮挡。\n",
        )

    def _build_log_tab(self) -> None:
        tab = self.tab_log
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        toolbar = ctk.CTkFrame(tab, corner_radius=12)
        toolbar.grid(row=0, column=0, padx=12, pady=(12, 8), sticky="ew")
        toolbar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            toolbar,
            text="运行日志",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).grid(row=0, column=0, padx=12, pady=10, sticky="w")

        ctk.CTkButton(
            toolbar,
            text="打开日志目录",
            width=112,
            command=self._open_log_dir,
        ).grid(row=0, column=1, padx=5, pady=10)

        ctk.CTkButton(
            toolbar,
            text="清空界面日志",
            width=112,
            fg_color="#555555",
            hover_color="#444444",
            command=self._clear_ui_log,
        ).grid(row=0, column=2, padx=(5, 12), pady=10)

        self.log_text = ctk.CTkTextbox(tab, font=("Consolas", 11))
        self.log_text.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="nsew")

    # ============================================================
    # 配置持久化
    # ============================================================
    def _load_config(self) -> dict[str, Any]:
        config = dict(DEFAULT_CONFIG)
        try:
            if CONFIG_PATH.exists():
                loaded = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    config.update(loaded)
        except Exception as exc:
            file_log.warn(f"读取配置失败，将使用默认值: {exc}")

        config["shoulderSide"] = (
            "left" if str(config.get("shoulderSide")).lower() == "left" else "right"
        )
        config["distance"] = self._clamp_float(config.get("distance"), 1.0, 8.0, 3.0)
        config["horizontalOffset"] = self._clamp_float(
            config.get("horizontalOffset"), 0.0, 1.5, 0.55
        )
        config["heightOffset"] = self._clamp_float(
            config.get("heightOffset"), -1.0, 1.5, 0.15
        )
        config["fieldOfView"] = self._clamp_float(
            config.get("fieldOfView"), 40.0, 110.0, 70.0
        )
        config["sensitivity"] = self._clamp_float(
            config.get("sensitivity"), 0.2, 3.0, 1.0
        )
        config["aimDiagnosticSeconds"] = int(
            self._clamp_float(config.get("aimDiagnosticSeconds"), 5, 60, 20)
        )
        config["syncCharacterYaw"] = bool(config.get("syncCharacterYaw", True))
        config["verticalInputEnabled"] = bool(config.get("verticalInputEnabled", True))
        return config

    @staticmethod
    def _clamp_float(value: Any, minimum: float, maximum: float, fallback: float) -> float:
        try:
            result = float(value)
            if not (minimum <= result <= maximum):
                return fallback
            return result
        except (TypeError, ValueError):
            return fallback

    def _save_config(self) -> None:
        try:
            CONFIG_PATH.write_text(
                json.dumps(self.config_data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as exc:
            self._emit_log(f"保存配置失败: {exc}", "warning")

    def _apply_config_to_controls(self) -> None:
        self._ui_syncing = True
        try:
            self.shoulder_control.set(
                "左肩" if self.config_data["shoulderSide"] == "left" else "右肩"
            )
            self.distance_slider.set(self.config_data["distance"])
            self.horizontal_slider.set(self.config_data["horizontalOffset"])
            self.height_slider.set(self.config_data["heightOffset"])
            self.fov_slider.set(self.config_data["fieldOfView"])
            self.sensitivity_slider.set(self.config_data["sensitivity"])
            self.diag_duration_slider.set(self.config_data["aimDiagnosticSeconds"])
            if self.config_data.get("verticalInputEnabled", True):
                self.vertical_input_switch.select()
            else:
                self.vertical_input_switch.deselect()
            if self.config_data.get("syncCharacterYaw", True):
                self.yaw_sync_switch.select()
            else:
                self.yaw_sync_switch.deselect()
            self._refresh_value_labels()
        finally:
            self._ui_syncing = False

    def _refresh_value_labels(self) -> None:
        self.distance_value.configure(text=f"{self.config_data['distance']:.1f} m")
        self.horizontal_value.configure(
            text=f"{self.config_data['horizontalOffset']:.2f} m"
        )
        self.height_value.configure(text=f"{self.config_data['heightOffset']:.2f} m")
        self.fov_value.configure(text=f"{self.config_data['fieldOfView']:.0f}°")
        self.sensitivity_value.configure(
            text=f"{self.config_data['sensitivity']:.1f}x"
        )
        self.diag_duration_label.configure(
            text=f"{self.config_data['aimDiagnosticSeconds']} 秒"
        )

    # ============================================================
    # 日志
    # ============================================================
    def _emit_log(self, message: str, level: str = "info") -> None:
        file_log.write(level, message)
        self._log_queue.put((level, message))

    def _drain_log_queue(self) -> None:
        if self._closing:
            return

        processed = 0
        while processed < 80:
            try:
                level, message = self._log_queue.get_nowait()
            except queue.Empty:
                break

            timestamp = datetime.now().strftime("%H:%M:%S")
            prefix = {
                "error": "错误",
                "warning": "警告",
                "warn": "警告",
                "debug": "调试",
            }.get(level.lower(), "信息")
            self.log_text.insert(
                "end",
                f"[{timestamp}] [{prefix}] {message}\n",
            )
            processed += 1

        if processed:
            try:
                line_count = int(self.log_text.index("end-1c").split(".")[0])
                if line_count > self._max_ui_log_lines:
                    self.log_text.delete(
                        "1.0",
                        f"{line_count - self._max_ui_log_lines}.0",
                    )
            except Exception:
                pass
            self.log_text.see("end")

        # 队列仍很大时更快继续，但每次绝不无限清空，避免阻塞 Tk 主线程。
        delay = 20 if not self._log_queue.empty() else 100
        self.after(delay, self._drain_log_queue)

    def _clear_ui_log(self) -> None:
        self.log_text.delete("1.0", "end")

    def _open_log_dir(self) -> None:
        try:
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            if os.name == "nt":
                os.startfile(LOG_DIR)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                os.system(f'open "{LOG_DIR}"')
            else:
                os.system(f'xdg-open "{LOG_DIR}" >/dev/null 2>&1 &')
        except Exception as exc:
            self._emit_log(f"打开日志目录失败: {exc}", "error")

    # ============================================================
    # 进程与连接
    # ============================================================
    @staticmethod
    def _find_game_pid() -> Optional[int]:
        for process in psutil.process_iter(["pid", "name"]):
            try:
                name = (process.info.get("name") or "").lower()
                if name in PROCESS_NAMES or "unitycrossfire" in name:
                    return int(process.info["pid"])
            except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError, TypeError):
                continue
        return None

    @staticmethod
    def _resolve_script_path() -> Optional[Path]:
        if SCRIPT_PATH.is_file():
            return SCRIPT_PATH
        if SCRIPT_TXT_FALLBACK.is_file():
            return SCRIPT_TXT_FALLBACK
        return None

    def _connection_loop(self) -> None:
        while not self._stop_event.is_set():
            if self.is_connected:
                pid = self.current_pid
                if pid is None or not psutil.pid_exists(pid):
                    self._handle_connection_lost("游戏进程已结束")
                self._connect_wakeup.wait(timeout=1.5)
                self._connect_wakeup.clear()
                continue

            pid = self._find_game_pid()
            if pid is None:
                self._set_connection_ui("waiting", None)
                self._connect_wakeup.wait(timeout=2.0)
                self._connect_wakeup.clear()
                continue

            self._set_connection_ui("connecting", pid)
            self._emit_log(f"检测到游戏进程 PID={pid}，开始附加。")

            try:
                self._connect_once(pid)
            except frida.ProcessNotFoundError:
                self._emit_log(f"进程 PID={pid} 已退出。", "warning")
                self._set_connection_ui("waiting", None)
            except frida.PermissionDeniedError:
                self._emit_log("Frida 权限不足，请以管理员身份运行 UI。", "error")
                self._set_connection_ui("permission", pid)
                self._connect_wakeup.wait(timeout=5.0)
                self._connect_wakeup.clear()
            except Exception as exc:
                self._emit_log(f"连接失败: {exc}", "error")
                self._disconnect_resources(call_cleanup=False)
                self._set_connection_ui("error", pid)
                self._connect_wakeup.wait(timeout=3.0)
                self._connect_wakeup.clear()

    def _connect_once(self, pid: int) -> None:
        script_path = self._resolve_script_path()
        if script_path is None:
            raise FileNotFoundError(
                f"未找到 {SCRIPT_FILENAME}，请把 UI 和 JS 放在同一目录。"
            )

        js_code = script_path.read_text(encoding="utf-8")
        if len(js_code) < 1000:
            raise RuntimeError(f"JS 文件内容异常，大小只有 {len(js_code)} 字节。")

        session = frida.attach(pid)
        session.on("detached", self._on_session_detached)

        script = session.create_script(js_code)
        script.on("message", self._on_script_message)
        try:
            script.on("destroyed", self._on_script_destroyed)
        except Exception:
            pass
        script.load()

        with self._state_lock:
            self.session = session
            self.script = script
            self.current_pid = pid

        install_result = self._call_rpc("installhook")
        if not isinstance(install_result, dict) or not install_result.get("ok"):
            raise RuntimeError(f"installhook 失败: {install_result}")

        with self._state_lock:
            self.is_connected = True

        self._set_connection_ui("connected", pid)
        self._emit_log(
            f"连接成功，已加载 {script_path.name}，Hook 安装完成。"
        )

        # 连接后先把 UI 保存的配置同步到 JS，再读取状态。
        self._apply_config_to_script(silent=True)
        status = self._call_rpc("getstatus")
        self._schedule_ui(lambda: self._apply_status(status, sync_controls=True))

    def _request_reconnect(self) -> None:
        if self._closing:
            return
        self._emit_log("用户请求重新连接。")
        self._set_connection_ui("connecting", self.current_pid)
        threading.Thread(
            target=self._reconnect_worker,
            name="ThirdPersonReconnect",
            daemon=True,
        ).start()

    def _reconnect_worker(self) -> None:
        self._disconnect_resources(call_cleanup=True)
        self._connect_wakeup.set()

    def _disconnect_resources(self, call_cleanup: bool) -> None:
        with self._state_lock:
            script = self.script
            session = self.session

        if call_cleanup and script is not None:
            try:
                with self._rpc_lock:
                    script.exports_sync.cleanup()
            except Exception as exc:
                file_log.warn(f"cleanup 调用失败: {exc}")

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

        with self._state_lock:
            self.script = None
            self.session = None
            self.current_pid = None
            self.is_connected = False
            self.is_enabled = False

        self._schedule_ui(self._show_disconnected_mode)

    def _handle_connection_lost(self, reason: str) -> None:
        if not self.is_connected and self.script is None:
            return
        self._emit_log(f"连接已断开: {reason}", "warning")
        self._disconnect_resources(call_cleanup=False)
        self._set_connection_ui("waiting", None)
        self._connect_wakeup.set()

    def _on_session_detached(self, *args: Any) -> None:
        reason = str(args[0]) if args else "未知原因"
        self._handle_connection_lost(reason)

    def _on_script_destroyed(self, *args: Any) -> None:
        if not self._closing:
            self._handle_connection_lost("Frida 脚本已销毁")

    def _set_connection_ui(self, state: str, pid: Optional[int]) -> None:
        def update() -> None:
            if self._closing:
                return

            states = {
                "waiting": ("● 等待游戏", self.COLOR_ORANGE, "等待游戏启动..."),
                "connecting": ("● 正在连接", self.COLOR_BLUE, "正在附加游戏进程..."),
                "connected": ("● 已连接", self.COLOR_GREEN, "Frida 与脚本工作正常"),
                "permission": ("● 权限不足", self.COLOR_RED, "请以管理员身份运行"),
                "error": ("● 连接失败", self.COLOR_RED, "稍后自动重试"),
            }
            title, color, tooltip = states.get(
                state, ("● 未连接", self.COLOR_MUTED, "")
            )
            self.connection_status.configure(text=title, text_color=color)
            self.pid_label.configure(
                text=f"PID: {pid}" if pid is not None else "PID: -"
            )
            self.footer_label.configure(
                text=f"{tooltip}　|　日志：{file_log.log_path}"
            )
            self._set_controls_connected(state == "connected")

        self._schedule_ui(update)

    def _show_disconnected_mode(self) -> None:
        self.is_enabled = False
        self.toggle_button.configure(
            text="开启第三人称",
            fg_color=self.COLOR_GREEN,
            hover_color=self.COLOR_GREEN_HOVER,
        )
        self.mode_label.configure(text="当前模式：第一人称 / 未连接")

    def _set_controls_connected(self, connected: bool) -> None:
        state = "normal" if connected else "disabled"
        for widget in (
            self.toggle_button,
            self.apply_button,
            self.refresh_status_button,
            self.debug_model_button,
            self.snapshot_button,
            self.stop_diag_button,
            self.diag_status_button,
            self.start_diag_button,
        ):
            widget.configure(state=state)

    # ============================================================
    # Frida RPC
    # ============================================================
    def _call_rpc(self, name: str, *args: Any) -> Any:
        with self._state_lock:
            script = self.script
        if script is None:
            raise RuntimeError("Frida 脚本未连接")

        try:
            with self._rpc_lock:
                method = getattr(script.exports_sync, name)
                return method(*args)
        except (frida.InvalidOperationError, frida.TransportError) as exc:
            self._handle_connection_lost(str(exc))
            raise

    def _run_rpc_async(
        self,
        name: str,
        *args: Any,
        on_success: Optional[Callable[[Any], None]] = None,
        description: Optional[str] = None,
    ) -> None:
        def worker() -> None:
            try:
                result = self._call_rpc(name, *args)
                if on_success is not None:
                    self._schedule_ui(lambda: on_success(result))
            except Exception as exc:
                label = description or name
                self._emit_log(f"{label}失败: {exc}", "error")

        threading.Thread(
            target=worker,
            name=f"RPC-{name}",
            daemon=True,
        ).start()

    def _on_script_message(self, message: dict[str, Any], data: Any) -> None:
        message_type = message.get("type")

        if message_type == "send":
            payload = message.get("payload")

            # 诊断流不能逐行送入主日志文本框，否则数千条消息会卡住 Tk。
            if isinstance(payload, dict) and payload.get("type") == "aim_diag":
                line = str(payload.get("line", ""))
                if len(self._aim_diag_lines) < 4000:
                    self._aim_diag_lines.append(line)
                else:
                    self._aim_diag_dropped += 1
                self._schedule_aim_diag_preview()
                return

            if isinstance(payload, dict) and payload.get("type") == "aim_diag_complete":
                self._handle_aim_diag_complete(payload)
                return

            if isinstance(payload, dict) and payload.get("type") == "log":
                level = str(payload.get("level", "info"))
                module = str(payload.get("module", "")).strip()
                text = str(payload.get("message", ""))
                extra = payload.get("extra")

                full = f"[{module}] {text}" if module else text
                if extra is not None:
                    try:
                        full += " | " + json.dumps(
                            extra, ensure_ascii=False, default=str
                        )
                    except Exception:
                        full += f" | {extra}"
                self._emit_log(full, level)
            else:
                self._emit_log(f"[JS] {payload}")
            return

        if message_type == "error":
            description = message.get("description", "未知 Frida 错误")
            stack = message.get("stack", "")
            self._emit_log(
                f"Frida 脚本错误: {description}\n{stack}",
                "error",
            )

    def _schedule_aim_diag_preview(self) -> None:
        if self._aim_diag_ui_pending or self._closing:
            return
        self._aim_diag_ui_pending = True
        self.after(350, self._refresh_aim_diag_preview)

    def _refresh_aim_diag_preview(self) -> None:
        self._aim_diag_ui_pending = False
        if self._closing:
            return

        recent = self._aim_diag_lines[-120:]
        header = (
            f"诊断实时预览：已接收 {len(self._aim_diag_lines)} 行"
            f"，丢弃 {self._aim_diag_dropped} 行\n"
            + "=" * 64
            + "\n"
        )
        self.diag_text.delete("1.0", "end")
        self.diag_text.insert("end", header + "\n".join(recent))
        self.diag_text.see("end")

    def _handle_aim_diag_complete(self, payload: dict[str, Any]) -> None:
        session_id = str(payload.get("sessionId", "unknown"))
        lines = payload.get("lines")
        if isinstance(lines, list):
            complete_lines = [str(item) for item in lines]
        else:
            complete_lines = list(self._aim_diag_lines)

        diag_dir = LOG_DIR / "aim_diagnostics"
        diag_dir.mkdir(parents=True, exist_ok=True)
        output_path = diag_dir / f"{session_id}.txt"

        try:
            output_path.write_text(
                "\n".join(complete_lines),
                encoding="utf-8",
            )
            self._emit_log(
                f"瞄准诊断完成：{len(complete_lines)} 行，已保存到 {output_path}"
            )
        except Exception as exc:
            self._emit_log(f"保存诊断文件失败: {exc}", "error")

        self._aim_diag_lines = complete_lines[-4000:]
        self._schedule_aim_diag_preview()

    # ============================================================
    # 配置控件
    # ============================================================
    def _on_shoulder_changed(self, value: str) -> None:
        if self._ui_syncing:
            return
        self.config_data["shoulderSide"] = "left" if value == "左肩" else "right"
        self._configuration_changed()

    def _on_camera_switch_changed(self) -> None:
        if self._ui_syncing:
            return
        self.config_data["verticalInputEnabled"] = bool(
            self.vertical_input_switch.get()
        )
        self.config_data["syncCharacterYaw"] = bool(
            self.yaw_sync_switch.get()
        )
        self._configuration_changed()

    def _on_distance_changed(self, value: float) -> None:
        if self._ui_syncing:
            return
        self.config_data["distance"] = round(float(value), 1)
        self.distance_value.configure(text=f"{self.config_data['distance']:.1f} m")
        self._configuration_changed()

    def _on_horizontal_changed(self, value: float) -> None:
        if self._ui_syncing:
            return
        self.config_data["horizontalOffset"] = round(float(value), 2)
        self.horizontal_value.configure(
            text=f"{self.config_data['horizontalOffset']:.2f} m"
        )
        self._configuration_changed()

    def _on_height_changed(self, value: float) -> None:
        if self._ui_syncing:
            return
        self.config_data["heightOffset"] = round(float(value), 2)
        self.height_value.configure(
            text=f"{self.config_data['heightOffset']:.2f} m"
        )
        self._configuration_changed()

    def _on_fov_changed(self, value: float) -> None:
        if self._ui_syncing:
            return
        self.config_data["fieldOfView"] = round(float(value))
        self.fov_value.configure(text=f"{self.config_data['fieldOfView']:.0f}°")
        self._configuration_changed()

    def _on_sensitivity_changed(self, value: float) -> None:
        if self._ui_syncing:
            return
        self.config_data["sensitivity"] = round(float(value), 1)
        self.sensitivity_value.configure(
            text=f"{self.config_data['sensitivity']:.1f}x"
        )
        self._configuration_changed()

    def _on_diag_duration_changed(self, value: float) -> None:
        if self._ui_syncing:
            return
        self.config_data["aimDiagnosticSeconds"] = int(round(float(value)))
        self.diag_duration_label.configure(
            text=f"{self.config_data['aimDiagnosticSeconds']} 秒"
        )
        self._save_config()

    def _configuration_changed(self) -> None:
        self._save_config()
        if self._config_apply_after is not None:
            try:
                self.after_cancel(self._config_apply_after)
            except Exception:
                pass
        self._config_apply_after = self.after(350, self._apply_config_debounced)

    def _apply_config_debounced(self) -> None:
        self._config_apply_after = None
        if self.is_connected:
            self._apply_config_requested(silent=True)

    def _camera_payload(self) -> dict[str, Any]:
        return {
            "shoulderSide": self.config_data["shoulderSide"],
            "distance": float(self.config_data["distance"]),
            "horizontalOffset": float(self.config_data["horizontalOffset"]),
            "heightOffset": float(self.config_data["heightOffset"]),
            "fieldOfView": float(self.config_data["fieldOfView"]),
            "verticalInputEnabled": bool(self.config_data.get("verticalInputEnabled", True)),
            "syncCharacterYaw": bool(self.config_data.get("syncCharacterYaw", True)),
        }

    def _apply_config_to_script(self, silent: bool) -> bool:
        camera_result = self._call_rpc("setcamera", self._camera_payload())
        sensitivity_result = self._call_rpc(
            "setsensitivity", float(self.config_data["sensitivity"])
        )

        ok = (
            isinstance(camera_result, dict)
            and camera_result.get("ok")
            and isinstance(sensitivity_result, dict)
            and sensitivity_result.get("ok")
        )
        if not silent:
            if ok:
                self._emit_log(
                    "相机参数已应用："
                    f"{self.config_data['shoulderSide']} shoulder, "
                    f"distance={self.config_data['distance']}, "
                    f"horizontal={self.config_data['horizontalOffset']}, "
                    f"height={self.config_data['heightOffset']}, "
                    f"FOV={self.config_data['fieldOfView']}"
                )
            else:
                self._emit_log(
                    f"参数应用返回异常: camera={camera_result}, "
                    f"sensitivity={sensitivity_result}",
                    "warning",
                )
        return bool(ok)

    def _apply_config_requested(self, silent: bool = False) -> None:
        if not self.is_connected:
            if not silent:
                self._emit_log("当前未连接，参数已保存，将在连接后自动应用。", "warning")
            return

        def worker() -> None:
            try:
                self._apply_config_to_script(silent=silent)
            except Exception as exc:
                if not silent:
                    self._emit_log(f"应用参数失败: {exc}", "error")

        threading.Thread(
            target=worker,
            name="ApplyCameraConfig",
            daemon=True,
        ).start()

    def _reset_requested(self) -> None:
        self.config_data = dict(DEFAULT_CONFIG)
        self._apply_config_to_controls()
        self._save_config()

        if not self.is_connected:
            self._emit_log("界面参数已恢复默认；连接后自动应用。")
            return

        def completed(result: Any) -> None:
            self._set_enabled_ui(False)
            self._emit_log(f"脚本与界面参数已恢复默认: {result}")

        self._run_rpc_async(
            "resetall",
            on_success=completed,
            description="恢复默认",
        )

    # ============================================================
    # 第三人称开关
    # ============================================================
    def _toggle_requested(self) -> None:
        if not self.is_connected:
            self._emit_log("尚未连接游戏。", "warning")
            return

        self.toggle_button.configure(state="disabled")
        threading.Thread(
            target=self._toggle_worker,
            name="ThirdPersonToggle",
            daemon=True,
        ).start()

    def _toggle_worker(self) -> None:
        try:
            if self.is_enabled:
                result = self._call_rpc("disable")
                ok = isinstance(result, dict) and result.get("ok")
                if ok:
                    self._schedule_ui(lambda: self._set_enabled_ui(False))
                    self._emit_log("第三人称已关闭，正在使用第一人称。")
                else:
                    self._emit_log(f"关闭第三人称失败: {result}", "error")
            else:
                # 启用前先同步参数，确保第一次进入就是 UI 当前配置。
                self._apply_config_to_script(silent=True)
                result = self._call_rpc("enable")
                ok = isinstance(result, dict) and result.get("ok")
                if ok:
                    self._schedule_ui(lambda: self._set_enabled_ui(True))
                    self._emit_log("第三人称已开启。")
                else:
                    error = (
                        result.get("error", "未知错误")
                        if isinstance(result, dict)
                        else str(result)
                    )
                    self._emit_log(
                        f"开启失败: {error}。请确认已经进入对局。",
                        "warning",
                    )
        except Exception as exc:
            self._emit_log(f"切换第三人称失败: {exc}", "error")
        finally:
            self._schedule_ui(
                lambda: self.toggle_button.configure(
                    state="normal" if self.is_connected else "disabled"
                )
            )

    def _set_enabled_ui(self, enabled: bool) -> None:
        self.is_enabled = bool(enabled)
        if enabled:
            self.toggle_button.configure(
                text="关闭第三人称",
                fg_color=self.COLOR_RED,
                hover_color=self.COLOR_RED_HOVER,
            )
            self.mode_label.configure(text="当前模式：第三人称")
        else:
            self.toggle_button.configure(
                text="开启第三人称",
                fg_color=self.COLOR_GREEN,
                hover_color=self.COLOR_GREEN_HOVER,
            )
            self.mode_label.configure(text="当前模式：第一人称")

    # ============================================================
    # 状态轮询
    # ============================================================
    def _status_poll_tick(self) -> None:
        if self._closing:
            return
        if self.is_connected and not self._status_poll_busy:
            self._status_poll_busy = True
            threading.Thread(
                target=self._status_poll_worker,
                name="ThirdPersonStatusPoll",
                daemon=True,
            ).start()
        self.after(2000, self._status_poll_tick)

    def _status_poll_worker(self) -> None:
        try:
            status = self._call_rpc("getstatus")
            self._schedule_ui(lambda: self._apply_status(status, sync_controls=False))
        except Exception:
            pass
        finally:
            self._status_poll_busy = False

    def _refresh_status_requested(self, sync_controls: bool) -> None:
        if not self.is_connected:
            self._emit_log("尚未连接，无法读取状态。", "warning")
            return

        def worker() -> None:
            try:
                status = self._call_rpc("getstatus")
                self._schedule_ui(
                    lambda: self._apply_status(status, sync_controls=sync_controls)
                )
                self._emit_log("状态已刷新。")
            except Exception as exc:
                self._emit_log(f"刷新状态失败: {exc}", "error")

        threading.Thread(
            target=worker,
            name="ManualStatusRefresh",
            daemon=True,
        ).start()

    def _apply_status(self, status: Any, sync_controls: bool) -> None:
        if not isinstance(status, dict):
            return

        self._set_enabled_ui(bool(status.get("enabled")))

        values = {
            "state": status.get("state", "-"),
            "enabled": "已开启" if status.get("enabled") else "已关闭",
            "haveGM": "已获取" if status.get("haveGM") else "未获取",
            "haveCameraManager": (
                "已获取" if status.get("haveCameraManager") else "未获取"
            ),
        }
        for key, value in values.items():
            label = self.status_value_labels.get(key)
            if label is not None:
                label.configure(text=str(value))

        stats = status.get("stats") or {}
        for key, label in self.stat_value_labels.items():
            label.configure(text=str(stats.get(key, 0)))

        self.status_text.delete("1.0", "end")
        self.status_text.insert(
            "end",
            json.dumps(status, ensure_ascii=False, indent=2, default=str),
        )

        if sync_controls:
            self._ui_syncing = True
            try:
                shoulder = int(status.get("shoulderSide", 1))
                self.config_data["shoulderSide"] = "left" if shoulder < 0 else "right"
                self.config_data["distance"] = self._clamp_float(
                    status.get("distance"), 1.0, 8.0, self.config_data["distance"]
                )
                self.config_data["horizontalOffset"] = self._clamp_float(
                    status.get("horizontalOffset"),
                    0.0, 1.5,
                    self.config_data["horizontalOffset"],
                )
                self.config_data["heightOffset"] = self._clamp_float(
                    status.get("heightOffset"),
                    -1.0, 1.5,
                    self.config_data["heightOffset"],
                )
                self.config_data["fieldOfView"] = self._clamp_float(
                    status.get("fieldOfView"),
                    40.0, 110.0,
                    self.config_data["fieldOfView"],
                )
                self.config_data["sensitivity"] = self._clamp_float(
                    status.get("sensitivity"),
                    0.2, 3.0,
                    self.config_data["sensitivity"],
                )
                self.config_data["verticalInputEnabled"] = bool(
                    status.get("verticalInputEnabled", self.config_data.get("verticalInputEnabled", True))
                )
                self.config_data["syncCharacterYaw"] = bool(
                    status.get("syncCharacterYaw", self.config_data.get("syncCharacterYaw", True))
                )
                self._apply_config_to_controls()
                self._save_config()
            finally:
                self._ui_syncing = False

    # ============================================================
    # 诊断工具
    # ============================================================
    def _show_diag_result(self, title: str, result: Any) -> None:
        display_result = result
        if isinstance(result, dict):
            display_result = dict(result)
            lines = display_result.get("lines")
            if isinstance(lines, list) and len(lines) > 120:
                display_result["lines"] = lines[-120:]
                display_result["linesTruncatedForUI"] = len(lines) - 120

        self.diag_text.delete("1.0", "end")
        self.diag_text.insert(
            "end",
            f"{title}\n{'=' * 64}\n"
            + json.dumps(display_result, ensure_ascii=False, indent=2, default=str),
        )
        self.tabview.set("诊断工具")

    def _debug_model_requested(self) -> None:
        self._run_rpc_async(
            "debugmodel",
            on_success=lambda result: self._show_diag_result("模型/武器诊断", result),
            description="模型诊断",
        )

    def _start_aim_diag_requested(self) -> None:
        seconds = int(self.config_data["aimDiagnosticSeconds"])
        self._aim_diag_lines = []
        self._aim_diag_dropped = 0
        self.start_diag_button.configure(state="disabled")

        def completed(result: Any) -> None:
            self.start_diag_button.configure(
                state="normal" if self.is_connected else "disabled"
            )
            self._show_diag_result("开始瞄准诊断", result)
            if isinstance(result, dict) and result.get("ok"):
                self._emit_log(f"瞄准诊断已启动，时长 {seconds} 秒。")
            else:
                self._emit_log(f"瞄准诊断未启动: {result}", "warning")

        self._run_rpc_async(
            "startaimdiagnostic",
            seconds,
            on_success=completed,
            description="启动瞄准诊断",
        )

    def _stop_aim_diag_requested(self) -> None:
        self._run_rpc_async(
            "stopaimdiagnostic",
            on_success=lambda result: self._show_diag_result("停止瞄准诊断", result),
            description="停止瞄准诊断",
        )

    def _capture_snapshot_requested(self) -> None:
        tag = datetime.now().strftime("ui_%H%M%S")
        self._run_rpc_async(
            "captureaimsnapshot",
            tag,
            on_success=lambda result: self._show_diag_result(
                f"瞄准快照 {tag}", result
            ),
            description="捕获瞄准快照",
        )

    def _aim_diag_status_requested(self) -> None:
        self._run_rpc_async(
            "getaimdiagstatus",
            on_success=lambda result: self._show_diag_result("瞄准诊断状态", result),
            description="读取瞄准诊断状态",
        )

    # ============================================================
    # 通用 UI 调度与关闭
    # ============================================================
    def _schedule_ui(self, callback: Callable[[], None]) -> None:
        if self._closing:
            return
        try:
            self.after(0, callback)
        except Exception:
            pass

    def _on_close(self) -> None:
        if self._closing:
            return

        self._closing = True
        self._stop_event.set()
        self._connect_wakeup.set()
        file_log.info("用户关闭 UI，开始清理。")

        try:
            if self._config_apply_after is not None:
                self.after_cancel(self._config_apply_after)
        except Exception:
            pass

        # cleanup 会禁用第三人称、恢复相机并 detach Hook。
        self._disconnect_resources(call_cleanup=True)

        try:
            self.destroy()
        except Exception:
            pass


def main() -> None:
    app = ThirdPersonApp()
    app.mainloop()


if __name__ == "__main__":
    main()
