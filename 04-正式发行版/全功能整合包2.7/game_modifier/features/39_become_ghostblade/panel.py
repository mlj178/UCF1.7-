import tkinter as tk

import customtkinter as ctk

from ui.theme import (
    ACCENT,
    BG_CARD,
    BG_HOVER,
    BG_INNER,
    BG_WINDOW,
    FONT_BODY_BOLD,
    FONT_CAPTION,
    FONT_TITLE,
    FG_BODY,
    FG_MUTED,
    HEIGHT_BADGE,
    HEIGHT_BUTTON_ACTION,
    HEIGHT_SWITCH,
    LINE,
    LINE_STRONG,
    PAD_MD,
    PAD_SM,
    PAD_XS,
    RADIUS_CARD,
    RADIUS_CONTROL,
    RADIUS_PILL,
    WIDTH_BADGE,
    WIDTH_SWITCH,
)

# 卡片强调色沿用 manifest 的 title_color，此处只补悬停色
ACCENT_HOVER = "#06b6d4"
STATE_POLL_MS = 700


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})
    accent = manifest.get("layout", {}).get("title_color", ACCENT)
    switch_label = next(
        (
            item.get("label", "")
            for item in manifest.get("controls", [])
            if item.get("action") == "enable"
        ),
        "",
    )

    frame = ctk.CTkFrame(
        parent,
        corner_radius=RADIUS_CARD,
        fg_color=BG_CARD,
        border_width=1,
        border_color=LINE,
    )
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=PAD_XS, pady=PAD_XS)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=PAD_MD, pady=(PAD_MD, 0))

    ctk.CTkLabel(
        top,
        text=manifest.get("display_name", "直接变身剑客"),
        font=FONT_TITLE,
        text_color=accent,
    ).pack(side="left", padx=(0, PAD_SM))

    badge = ctk.CTkLabel(
        top,
        text="未启用",
        font=FONT_CAPTION,
        text_color=FG_MUTED,
        fg_color=BG_INNER,
        corner_radius=RADIUS_PILL,
        width=WIDTH_BADGE,
        height=HEIGHT_BADGE,
    )
    badge.pack(side="left")

    switch = ctk.CTkSwitch(
        top,
        text=switch_label,
        font=FONT_CAPTION,
        width=WIDTH_SWITCH,
        switch_width=WIDTH_SWITCH,
        switch_height=HEIGHT_SWITCH,
        progress_color=accent,
        fg_color=BG_HOVER,
        command=lambda: callbacks["toggle"](feature_id),
    )
    switch.pack(side="right", padx=(PAD_SM, 0))

    ctk.CTkFrame(frame, height=1, fg_color=LINE).pack(fill="x", padx=PAD_MD, pady=(PAD_MD, 0))

    ctk.CTkLabel(
        frame,
        text=manifest.get("desc", ""),
        text_color=FG_MUTED,
        font=FONT_CAPTION,
        wraplength=280 * colspan,
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=PAD_MD, pady=(PAD_SM, 0))

    button_controls = {
        (control.get("payload") or {}).get("action"): control
        for control in manifest.get("controls", [])
        if control.get("type") == "button"
    }

    def run_action(payload_action, button, busy_text):
        if not callbacks["is_connected"]():
            callbacks["log"]("尚未连接到游戏")
            return
        if not callbacks["is_enabled"](feature_id):
            callbacks["log"]("请先打开「直接变身剑客」开关")
            return
        original = button.cget("text")
        button.configure(state="disabled", text=busy_text)
        try:
            callbacks["action"](feature_id, "trigger", {"action": payload_action})
        except Exception as exc:
            callbacks["log"](f"变身异常: {exc}")
        finally:
            button.after(400, lambda: button.configure(state="normal", text=original))

    local_button = ctk.CTkButton(
        frame,
        text=button_controls.get("local_ghostblade", {}).get("label", "本地变身剑客"),
        height=HEIGHT_BUTTON_ACTION,
        font=FONT_BODY_BOLD,
        fg_color=accent,
        hover_color=ACCENT_HOVER,
        text_color=BG_WINDOW,
        corner_radius=RADIUS_CONTROL,
        command=lambda: run_action("local_ghostblade", local_button, "变身中..."),
    )
    local_button.pack(fill="x", padx=PAD_MD, pady=(PAD_MD, PAD_SM))

    bot_button = ctk.CTkButton(
        frame,
        text=button_controls.get("bot_ghostblade", {}).get("label", "所有 Bot 变剑客"),
        height=HEIGHT_BUTTON_ACTION,
        font=FONT_BODY_BOLD,
        fg_color=BG_INNER,
        hover_color=BG_HOVER,
        text_color=FG_BODY,
        border_width=1,
        border_color=LINE_STRONG,
        corner_radius=RADIUS_CONTROL,
        command=lambda: run_action("bot_ghostblade", bot_button, "变身中..."),
    )
    bot_button.pack(fill="x", padx=PAD_MD, pady=(0, PAD_MD))

    # 开关状态可能由快捷键或启动恢复流程改写，这里轮询同步徽标与描边色。
    state = {"enabled": None}

    def sync_state():
        try:
            alive = bool(frame.winfo_exists())
        except tk.TclError:
            alive = False
        if not alive:
            return
        enabled = bool(switch.get())
        if enabled != state["enabled"]:
            state["enabled"] = enabled
            badge.configure(
                text="已启用" if enabled else "未启用",
                text_color=accent if enabled else FG_MUTED,
            )
            frame.configure(border_color=accent if enabled else LINE)
        frame.after(STATE_POLL_MS, sync_state)

    frame.after(0, sync_state)

    return {
        handles.get("switch", "become_ghostblade_switch"): switch,
        handles.get("local_button", "become_ghostblade_local_btn"): local_button,
        handles.get("bot_button", "become_ghostblade_bot_btn"): bot_button,
    }