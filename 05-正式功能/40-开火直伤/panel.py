"""开火直伤 —— 整合包卡片 UI。

只使用通用 callbacks：
- callbacks["toggle"](feature_id)
- callbacks["set_config"](feature_id, key, value)
- callbacks["get_config"](feature_id)
"""

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
ACCENT_HOVER = "#db2777"
STATE_POLL_MS = 700

# 子开关：manifest.config key -> 显示名
SUB_SWITCHES = (
    ("enable_guns", "常规枪械直伤"),
    ("enable_explosives", "榴弹/手雷/RPG 直伤"),
    ("enable_skill_projectiles", "特殊技能弹直伤"),
)


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

    try:
        current_config = dict(callbacks["get_config"](feature_id) or {})
    except Exception:
        current_config = {}
    defaults = {}
    for item in manifest.get("controls", []):
        if item.get("type") == "slider":
            defaults[item.get("key")] = item.get("default")
    defaults.update(manifest.get("config", {}))
    defaults.update(current_config)

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
        text=manifest.get("display_name", "开火直伤"),
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

    # ---------------- 三个独立开关 ----------------
    sub_frame = ctk.CTkFrame(frame, fg_color="transparent")
    sub_frame.pack(fill="x", padx=PAD_MD, pady=(PAD_SM, 0))

    sub_handles = {}
    for key, label in SUB_SWITCHES:
        line = ctk.CTkFrame(sub_frame, fg_color="transparent")
        line.pack(fill="x", pady=2)
        ctk.CTkLabel(line, text=label, font=FONT_CAPTION, text_color=FG_BODY).pack(side="left")
        sub_switch = ctk.CTkSwitch(
            line,
            text="",
            width=WIDTH_SWITCH,
            switch_width=WIDTH_SWITCH,
            switch_height=HEIGHT_SWITCH,
            progress_color=accent,
            fg_color=BG_HOVER,
        )
        sub_switch.pack(side="right")
        if defaults.get(key, True):
            sub_switch.select()
        else:
            sub_switch.deselect()
        sub_switch.configure(
            command=lambda fid=feature_id, config_key=key, widget=sub_switch: callbacks[
                "set_config"
            ](fid, config_key, bool(widget.get()))
        )
        sub_handles[key] = sub_switch

    # ---------------- 参数滑块 ----------------
    def make_slider(title, key, minimum, maximum, step):
        line = ctk.CTkFrame(frame, fg_color="transparent")
        line.pack(fill="x", padx=PAD_MD, pady=(PAD_SM, 0))
        header = ctk.CTkFrame(line, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(header, text=title, font=FONT_CAPTION, text_color=FG_BODY).pack(side="left")
        value = float(defaults.get(key, minimum) or minimum)
        value_label = ctk.CTkLabel(
            header, text=f"{value:.0f}", font=FONT_CAPTION, text_color=accent
        )
        value_label.pack(side="right")

        slider = ctk.CTkSlider(
            line,
            from_=float(minimum),
            to=float(maximum),
            number_of_steps=max(1, int(round((float(maximum) - float(minimum)) / float(step)))),
            progress_color=accent,
            button_color=accent,
            button_hover_color=ACCENT_HOVER,
            command=lambda v, fid=feature_id, cfg_key=key, lbl=value_label: (
                lbl.configure(text=f"{float(v):.0f}"),
                callbacks["set_config"](fid, cfg_key, float(v)),
            ),
        )
        slider.set(value)
        slider.pack(fill="x", pady=(2, 0))
        return slider, value_label

    angle_slider, angle_label = make_slider("准星锥角度(度)", "max_angle_deg", 5, 120, 1)
    distance_slider, distance_label = make_slider("最大距离(米, 0=不限)", "max_distance", 0, 200, 5)

    ctk.CTkFrame(frame, height=1, fg_color=LINE).pack(fill="x", padx=PAD_MD, pady=(PAD_MD, 0))

    ctk.CTkLabel(
        frame,
        text="开火即命中：不再走子弹射线，也不修改镜头。",
        text_color=FG_MUTED,
        font=FONT_CAPTION,
        wraplength=280 * colspan,
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=PAD_MD, pady=(PAD_SM, PAD_MD))

    # ---------------- 状态轮询 ----------------
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

    result = {
        handles.get("switch", "direct_damage_switch"): switch,
        handles.get("angle_slider", "direct_damage_angle_slider"): angle_slider,
        handles.get("angle_label", "direct_damage_angle_label"): angle_label,
        handles.get("distance_slider", "direct_damage_distance_slider"): distance_slider,
        handles.get("distance_label", "direct_damage_distance_label"): distance_label,
    }
    for key, _label in SUB_SWITCHES:
        result[handles.get(key + "_switch", "direct_damage_" + key + "_switch")] = sub_handles[key]
    return result
