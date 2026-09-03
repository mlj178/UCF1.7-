"""Integer-only room size control; other features keep their original sliders."""
import math
import tkinter as tk

import customtkinter as ctk


def _count(value):
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        numeric = 50
    if not math.isfinite(numeric):
        numeric = 50
    # Match script.js Math.round, including old fractional saved settings.
    return max(2, min(100, math.floor(numeric + 0.5)))


class _CountVar(ctk.IntVar):
    def set(self, value):
        super().set(_count(value))


class _CountLabel(ctk.CTkLabel):
    def configure(self, require_redraw=False, **kwargs):
        # The trainer's config refresh unconditionally formats sliders as .1f.
        # Normalize that refresh too, without changing the shared UI code.
        if "text" in kwargs:
            value = str(kwargs["text"]).removesuffix("人").removesuffix("x")
            kwargs["text"] = f"{_count(value)}人"
        return super().configure(require_redraw=require_redraw, **kwargs)


class _RoomCountController:
    """Keep room-size writes behind the feature's explicit lifecycle switch."""

    def __init__(self, host, variable, value_label, feedback, callbacks, feature_id, key):
        self.host = host
        self.variable = variable
        self.value_label = value_label
        self.feedback = feedback
        self.callbacks = callbacks
        self.feature_id = feature_id
        self.key = key
        self.requested = None
        self.closed = False

    def connected(self):
        return bool(self.callbacks["is_connected"]())

    def show(self, message, color="#a0a0a0"):
        self.feedback.configure(text=message, text_color=color)

    def log(self, message):
        self.callbacks.get("log", lambda *_: None)("[房间人数] " + message)

    def enabled(self):
        return bool(self.callbacks["is_enabled"](self.feature_id))

    def toggle(self):
        self.callbacks["toggle"](self.feature_id)
        if self.enabled():
            self.show("已开启：请点击应用人数", "#fbbf24")
            self.log("功能已开启，等待手动应用人数。")
        else:
            self.show("已关闭：正在恢复原始人数逻辑", "#fbbf24")
            self.log("功能已关闭，正在恢复原始人数逻辑。")

    def change(self, value):
        self.requested = _count(value)
        self.variable.set(self.requested)
        self.value_label.configure(text=f"{self.requested}人")
        self.show("待应用：点击应用人数后生效")

    def apply(self):
        if self.closed:
            return
        self.requested = _count(self.variable.get())
        if not self.callbacks["is_enabled"](self.feature_id):
            self.show("请先开启功能，再点击应用人数", "#fbbf24")
            self.log("功能未开启，未应用人数。")
            return
        if not self.connected():
            # Persist the selection, but never arrange an automatic write on reconnect.
            self.callbacks["set_config"](self.feature_id, self.key, self.requested)
            self.show("未连接：人数已保存；连接后请手动点击应用人数", "#fbbf24")
            self.log("尚未连接游戏；人数已保存，连接后请手动点击应用人数。")
            return
        self.show("正在应用人数…", "#fbbf24")
        try:
            result = self.callbacks["action"](
                self.feature_id, "apply_count",
                {self.key: self.requested},
            )
        except Exception as error:
            self.show("应用失败：请查看日志并重试", "#f87171")
            self.log(f"应用失败：{error}")
            return
        if not isinstance(result, dict) or result.get("ok") is not True:
            reason = (result.get("message") or result.get("reason", "未收到成功确认")) if isinstance(result, dict) else "未收到成功确认"
            self.show("应用失败：请查看日志并重试", "#f87171")
            self.log(f"应用失败：{reason}；当前游戏不在已验证的原始30人版/100人v3版范围内。")
            return
        self.show(f"已应用 {self.requested}人（机器人{self.requested - 1}），下局生效", "#4ade80")
        self.log(f"已应用总人数 {self.requested}（机器人 {self.requested - 1}），请开始新对局。")

    def close(self, event):
        if event.widget is self.host and not self.closed:
            self.closed = True


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    control = next(c for c in manifest["controls"] if c["type"] == "slider")
    initial = _count(control.get("default", 50))
    rowspan = int(manifest.get("layout", {}).get("rowspan", 1))
    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="transparent",
                         border_width=1, border_color="#4b5563")
    frame.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan,
               sticky="nsew", padx=3, pady=3)
    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=10, pady=(6, 0))
    top.grid_columnconfigure(0, weight=1)
    ctk.CTkLabel(top, text=manifest["display_name"],
                 font=("Microsoft YaHei", 15, "bold"),
                 text_color=manifest.get("layout", {}).get("title_color", "#fbbf24")
                 ).grid(row=0, column=0, sticky="w", padx=(0, 8))
    variable = _CountVar(master=top, value=initial)
    slider_row = ctk.CTkFrame(frame, fg_color="transparent")
    slider_row.pack(fill="x", padx=10, pady=(2, 4))
    slider_row.grid_columnconfigure(0, weight=1)
    slider = ctk.CTkSlider(slider_row, from_=2, to=100, number_of_steps=98,
                           variable=variable)
    slider.grid(row=0, column=0, sticky="ew")
    label = _CountLabel(slider_row, text=f"{initial}人", width=44,
                        font=("Microsoft YaHei", 11), text_color="#e0e0e0")
    label.grid(row=0, column=1, sticky="e", padx=(8, 0))
    help_text = manifest.get(
        "desc",
        "开启后，设置人数并点击“应用人数”。下一局生效；关闭后恢复默认人数。",
    )
    ctk.CTkLabel(frame, text=help_text, font=("Microsoft YaHei", 12),
                 text_color="#a0a0a0", wraplength=250, justify="left", anchor="w"
                 ).pack(fill="x", padx=10, pady=(2, 8))
    apply_row = ctk.CTkFrame(frame, fg_color="transparent")
    apply_row.pack(fill="x", padx=10, pady=(0, 8))
    feedback = ctk.CTkLabel(apply_row, text="请拖动滑条或点击应用人数", anchor="w",
                           font=("Microsoft YaHei", 11), text_color="#a0a0a0",
                           wraplength=190, justify="left")
    feedback.pack(side="left", fill="x", expand=True)
    controller = _RoomCountController(frame, variable, label, feedback, callbacks,
                                      feature_id, control["key"])
    switch = ctk.CTkSwitch(top, text="", width=42, command=controller.toggle)
    switch.grid(row=0, column=1, sticky="e", padx=(8, 0))
    slider.configure(command=controller.change)
    apply_button = ctk.CTkButton(apply_row, text="应用人数", width=86, height=28,
                                 font=("Microsoft YaHei", 12), command=controller.apply)
    apply_button.pack(side="right", padx=(6, 0))
    # CTkFrame.bind targets its internal canvas; bind the actual frame lifetime.
    tk.Misc.bind(frame, "<Destroy>", controller.close, add="+")
    handles = manifest.get("ui_handles", {})
    return {
        handles.get("switch", "room_player_count_switch"): switch,
        handles.get("slider_var", "room_player_count_var"): variable,
        handles.get("slider", "room_player_count_slider"): slider,
        handles.get("slider_label", "room_player_count_label"): label,
        "room_player_count_apply_button": apply_button,
        "room_player_count_feedback": feedback,
        "room_player_count_controller": controller,
    }
