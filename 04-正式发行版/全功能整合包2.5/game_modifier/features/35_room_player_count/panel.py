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
    """Use an explicit action, not the disabled-feature-gated slider route."""

    def __init__(self, host, variable, value_label, feedback, callbacks, feature_id, key):
        self.host = host
        self.variable = variable
        self.value_label = value_label
        self.feedback = feedback
        self.callbacks = callbacks
        self.feature_id = feature_id
        self.key = key
        self.requested = None
        self.pending = None
        self.closed = False
        self.was_connected = self.connected()
        self.poll = host.after(500, self.check_connection)

    def connected(self):
        return bool(self.callbacks["is_connected"]())

    def show(self, message, color="#a0a0a0"):
        self.feedback.configure(text=message, text_color=color)

    def log(self, message):
        self.callbacks.get("log", lambda *_: None)("[房间人数] " + message)

    def cancel_pending(self):
        if self.pending is not None:
            self.host.after_cancel(self.pending)
            self.pending = None

    def change(self, value):
        self.requested = _count(value)
        self.variable.set(self.requested)
        self.value_label.configure(text=f"{self.requested}人")
        self.cancel_pending()
        self.show("待应用：松开滑条后自动生效")
        # Coalesce rapid pointer events so an older request cannot arrive last.
        self.pending = self.host.after(180, self.apply)

    def apply(self):
        if self.closed:
            return
        self.cancel_pending()
        self.requested = _count(self.variable.get())
        if not self.connected():
            # This route is safe while disconnected: it saves only local config.
            self.callbacks["set_config"](self.feature_id, self.key, self.requested)
            self.show("未连接：已保存，连接后自动应用", "#fbbf24")
            self.log("尚未连接游戏；人数已保存，连接后自动应用。")
            return
        self.show("正在应用人数…", "#fbbf24")
        try:
            # Manifest's set_config action persists config and calls the runtime
            # directly, even when ActionRouter._state[feature_id] is initially False.
            # script.js setConfig enables the patch idempotently on the first call.
            result = self.callbacks["action"](
                self.feature_id, "apply_count",
                {self.key: self.requested, "enabled": True},
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

    def check_connection(self):
        if self.closed:
            return
        connected = self.connected()
        if not connected and self.was_connected:
            self.show("连接已断开：重新连接后自动应用", "#fbbf24")
        if connected and not self.was_connected and self.requested is not None:
            self.apply()
        self.was_connected = connected
        self.poll = self.host.after(500, self.check_connection)

    def close(self, event):
        if event.widget is self.host and not self.closed:
            self.closed = True
            self.cancel_pending()
            self.host.after_cancel(self.poll)


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    control = next(c for c in manifest["controls"] if c["type"] == "slider")
    initial = _count(control.get("default", 50))
    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="transparent",
                         border_width=1, border_color="#4b5563")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=10, pady=(6, 0))
    top.grid_columnconfigure(1, weight=1)
    ctk.CTkLabel(top, text=manifest["display_name"],
                 font=("Microsoft YaHei", 15, "bold"),
                 text_color=manifest.get("layout", {}).get("title_color", "#fbbf24")
                 ).grid(row=0, column=0, sticky="w", padx=(0, 8))
    variable = _CountVar(master=top, value=initial)
    label = _CountLabel(top, text=f"{initial}人", width=44,
                        font=("Microsoft YaHei", 11), text_color="#e0e0e0")
    label.grid(row=0, column=2, sticky="e", padx=(6, 0))

    slider = ctk.CTkSlider(top, from_=2, to=100, number_of_steps=98,
                          width=110, variable=variable)
    slider.grid(row=0, column=1, sticky="ew")
    ctk.CTkLabel(frame, text=manifest["desc"], font=("Microsoft YaHei", 12),
                 text_color="#a0a0a0", wraplength=280, justify="left", anchor="w"
                 ).pack(fill="x", padx=10, pady=(4, 8))
    apply_row = ctk.CTkFrame(frame, fg_color="transparent")
    apply_row.pack(fill="x", padx=10, pady=(0, 8))
    feedback = ctk.CTkLabel(apply_row, text="请拖动滑条或点击应用人数", anchor="w",
                           font=("Microsoft YaHei", 11), text_color="#a0a0a0",
                           wraplength=190, justify="left")
    feedback.pack(side="left", fill="x", expand=True)
    controller = _RoomCountController(frame, variable, label, feedback, callbacks,
                                      feature_id, control["key"])
    slider.configure(command=controller.change)
    slider.bind("<ButtonRelease-1>", lambda event: controller.apply(), add=True)
    apply_button = ctk.CTkButton(apply_row, text="应用人数", width=86, height=28,
                                 font=("Microsoft YaHei", 12), command=controller.apply)
    apply_button.pack(side="right", padx=(6, 0))
    # CTkFrame.bind targets its internal canvas; bind the actual frame lifetime.
    tk.Misc.bind(frame, "<Destroy>", controller.close, add="+")
    handles = manifest.get("ui_handles", {})
    return {
        handles.get("switch", "room_player_count_switch"): None,
        handles.get("slider_var", "room_player_count_var"): variable,
        handles.get("slider", "room_player_count_slider"): slider,
        handles.get("slider_label", "room_player_count_label"): label,
        "room_player_count_apply_button": apply_button,
        "room_player_count_feedback": feedback,
        "room_player_count_controller": controller,
    }
