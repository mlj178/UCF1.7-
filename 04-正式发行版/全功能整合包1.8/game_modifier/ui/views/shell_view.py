from dataclasses import dataclass

import customtkinter as ctk


@dataclass(frozen=True)
class StatusHint:
    fg_color: str
    text_color: str
    text: str


@dataclass
class StatusBarHandles:
    frame: ctk.CTkFrame
    status_dot: ctk.CTkLabel
    status_label: ctk.CTkLabel
    settings_btn: ctk.CTkButton
    collapse_btn: ctk.CTkButton
    pid_label: ctk.CTkLabel


@dataclass
class HintBarHandles:
    frame: ctk.CTkFrame
    label: ctk.CTkLabel


def resolve_status_hint(color):
    if color == "green":
        return StatusHint("#1a3a1a", "#88ff88", "已连接，点击功能开关启用修改")
    if color == "red":
        return StatusHint("#3a1a1a", "#ff8888", "连接断开，正在重连...")
    return StatusHint("#2a2a00", "#ffcc00", "1. 启动游戏  2. 进入任意模式  3. 打开本工具  4. 开启功能")


class AppShellView:
    def __init__(self, parent, *, on_settings, on_toggle_collapse, on_connect):
        self._parent = parent
        self._on_settings = on_settings
        self._on_toggle_collapse = on_toggle_collapse
        self._on_connect = on_connect

    def build_status_bar(self):
        frame = ctk.CTkFrame(self._parent, corner_radius=8, fg_color="#2b2b2b")
        frame.pack(fill="x", padx=12, pady=(12, 6))

        status_dot = ctk.CTkLabel(frame, text="●", font=("Arial", 18))
        status_dot.pack(side="left", padx=(12, 4))
        status_label = ctk.CTkLabel(frame, text="等待游戏启动...", font=("Microsoft YaHei", 14))
        status_label.pack(side="left", padx=4)

        settings_btn = ctk.CTkButton(
            frame,
            text="设置",
            width=70,
            height=28,
            font=("Microsoft YaHei", 11),
            command=self._on_settings,
            fg_color="#3a3a3a",
            hover_color="#555555",
        )
        settings_btn.pack(side="right", padx=(4, 8))

        collapse_btn = ctk.CTkButton(
            frame,
            text="折叠界面",
            width=100,
            height=28,
            font=("Microsoft YaHei", 12),
            command=self._on_toggle_collapse,
            fg_color="#3a3a3a",
            hover_color="#555555",
        )
        collapse_btn.pack(side="right", padx=(4, 8))

        pid_label = ctk.CTkLabel(frame, text="", font=("Microsoft YaHei", 11), text_color="#888")
        pid_label.pack(side="right", padx=12)

        return StatusBarHandles(frame, status_dot, status_label, settings_btn, collapse_btn, pid_label)

    def build_hint_bar(self):
        hint = resolve_status_hint("yellow")
        frame = ctk.CTkFrame(self._parent, corner_radius=6, fg_color=hint.fg_color)
        frame.pack(fill="x", padx=12, pady=(2, 8))
        label = ctk.CTkLabel(
            frame,
            text=hint.text,
            font=("Microsoft YaHei", 11),
            text_color=hint.text_color,
            wraplength=760,
        )
        label.pack(padx=8, pady=4)
        return HintBarHandles(frame, label)

    def build_connect_button(self):
        frame = ctk.CTkFrame(self._parent, corner_radius=8)
        frame.pack(fill="x", padx=12, pady=(2, 6))
        button = ctk.CTkButton(
            frame,
            text="连接游戏",
            font=("Microsoft YaHei", 13),
            height=40,
            command=self._on_connect,
            fg_color="#2a6e2a",
        )
        button.pack(fill="x", padx=12, pady=10)
        return frame, button

    def build_log_panel(self):
        log_box = ctk.CTkTextbox(self._parent, font=("Consolas", 11), wrap="word", height=80, state="disabled")
        log_box.pack(fill="x", padx=12, pady=(2, 12))
        return log_box

    def apply_status(self, *, status_dot, status_label, hint_frame, hint_label, color, text):
        dot_map = {"green": "●", "yellow": "●", "red": "●", "gray": "●"}
        status_dot.configure(text=dot_map.get(color, "●"))
        status_label.configure(text=text)

        hint = resolve_status_hint(color)
        hint_frame.configure(fg_color=hint.fg_color)
        hint_label.configure(text_color=hint.text_color)
        hint_label.configure(text=hint.text)
