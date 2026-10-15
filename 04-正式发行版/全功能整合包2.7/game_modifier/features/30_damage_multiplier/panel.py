"""调整伤害倍率 · 方案 A 面板。

单张卡片里放三行：敌人 / 自己 / 队友，每行都有
「滑块 + 0.1x 数值 + ± 步进 + 独立开关」，底部一行实时汇总当前设置。

本文件只负责搭 UI 和把用户操作转成 callbacks，不直接碰 Frida。
"""

import customtkinter as ctk

# (config 前缀, 显示名, 主题色)
CATEGORIES = (
    ("enemy", "敌人", "#f87171"),
    ("self", "自己", "#4c8dff"),
    ("mate", "队友", "#34d399"),
)

NUDGE_STEP = 0.1
DISABLED_COLOR = "#5a626e"


def _find_control(manifest, control_type=None, key=None):
    for item in manifest.get("controls", []):
        if control_type and item.get("type") != control_type:
            continue
        if key is not None and item.get("key") != key:
            continue
        return item
    return {}


def _master_control(manifest):
    for item in manifest.get("controls", []):
        if item.get("type") == "switch" and not item.get("key"):
            return item
    return {}


def _slider_steps(control):
    minimum = float(control.get("min", 0.1))
    maximum = float(control.get("max", 10.0))
    step = float(control.get("step", 0.1))
    if step <= 0:
        return 199
    return int(round((maximum - minimum) / step))


def _value_color(value):
    if value < 1.0:
        return "#6cc7ff"  # 削弱
    if value > 1.0:
        return "#ff9a6b"  # 增强
    return "#e0e0e0"  # 原版


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})
    config = dict(manifest.get("config") or {})
    master = _master_control(manifest)

    frame = ctk.CTkFrame(
        parent,
        corner_radius=6,
        fg_color="transparent",
        border_width=1,
        border_color="#4b5563",
    )
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))

    ctk.CTkLabel(
        top,
        text=manifest.get("display_name", ""),
        font=("Microsoft YaHei", 15, "bold"),
        text_color=manifest.get("layout", {}).get("title_color", "#f97316"),
    ).pack(side="left", padx=4)

    switch = ctk.CTkSwitch(
        top,
        text=master.get("label", ""),
        font=("Microsoft YaHei", 12),
        width=50,
        command=lambda: callbacks["toggle"](feature_id),
    )
    switch.pack(side="right", padx=6)

    ctk.CTkLabel(
        frame,
        text=manifest.get("desc", ""),
        text_color="#a0a0a0",
        font=("Microsoft YaHei", 12),
        wraplength=520 * max(1, colspan // 2),
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(4, 6))

    state = {
        "vars": {},
        "labels": {},
        "sliders": {},
        "enabled_vars": {},
        "enabled_switches": {},
    }

    # 底部：实时汇总 + 一键复位。先建好、最后再 pack，保证显示在三个阵营行下面。
    foot = ctk.CTkFrame(frame, fg_color="transparent")
    summary = ctk.CTkLabel(
        foot,
        text="",
        font=("Microsoft YaHei", 11),
        text_color="#a0a0a0",
        anchor="w",
        justify="left",
    )

    def refresh_summary():
        parts = []
        for key, name, _color in CATEGORIES:
            value_var = state["vars"].get(key)
            enabled_var = state["enabled_vars"].get(key)
            if value_var is None or enabled_var is None:
                continue
            if bool(enabled_var.get()):
                parts.append(f"{name} {float(value_var.get()):.1f}x")
            else:
                parts.append(f"{name} 关")
        summary.configure(text="当前 · " + " ｜ ".join(parts) if parts else "当前 · --")

    def reset_all():
        for key, _name, _color in CATEGORIES:
            slider = state["sliders"].get(key)
            if slider is None:
                continue
            slider.set(1.0)
            callbacks["set_config"](feature_id, key + "_multiplier", 1.0)

    reset_btn = ctk.CTkButton(
        foot,
        text="全部 1.0x",
        width=78,
        height=24,
        font=("Microsoft YaHei", 11),
        fg_color="#2f3540",
        hover_color="#3a424e",
        command=reset_all,
    )
    reset_btn.pack(side="right")
    summary.pack(side="left")

    for key, name, color in CATEGORIES:
        slider_control = _find_control(manifest, "slider", key + "_multiplier")
        enabled_control = _find_control(manifest, "switch", key + "_enabled")

        minimum = float(slider_control.get("min", 0.1))
        maximum = float(slider_control.get("max", 10.0))
        default_value = float(config.get(key + "_multiplier", slider_control.get("default", 1.0)))
        default_value = min(maximum, max(minimum, default_value))
        default_enabled = bool(config.get(key + "_enabled", enabled_control.get("default", True)))

        row_frame = ctk.CTkFrame(frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=10, pady=1)
        row_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            row_frame,
            text=name,
            font=("Microsoft YaHei", 12, "bold"),
            text_color=color,
            width=42,
            anchor="w",
        ).grid(row=0, column=0, padx=(0, 8), sticky="w")

        value_var = ctk.DoubleVar(value=default_value)
        enabled_var = ctk.BooleanVar(value=default_enabled)

        value_label = ctk.CTkLabel(
            row_frame,
            text=f"{default_value:.1f}x",
            font=("Microsoft YaHei", 11),
            text_color=_value_color(default_value),
            width=44,
            anchor="e",
        )

        def on_slider_change(value, fid=feature_id, cfg_key=key + "_multiplier"):
            callbacks["set_config"](fid, cfg_key, round(float(value), 1))

        slider = ctk.CTkSlider(
            row_frame,
            from_=minimum,
            to=maximum,
            number_of_steps=_slider_steps(slider_control),
            variable=value_var,
            command=on_slider_change,
        )
        slider.grid(row=0, column=1, padx=(0, 8), sticky="ew")

        def nudge(
            delta,
            slider=slider,
            var=value_var,
            lo=minimum,
            hi=maximum,
            fid=feature_id,
            cfg_key=key + "_multiplier",
        ):
            numeric = round(min(hi, max(lo, float(var.get()) + delta)), 1)
            # slider.set 会同步变量并重绘，但不会触发 command，所以这里显式下发配置。
            slider.set(numeric)
            callbacks["set_config"](fid, cfg_key, numeric)

        minus_btn = ctk.CTkButton(
            row_frame,
            text="−",
            width=24,
            height=24,
            font=("Microsoft YaHei", 12),
            fg_color="#2f3540",
            hover_color="#3a424e",
            command=lambda n=nudge: n(-NUDGE_STEP),
        )
        minus_btn.grid(row=0, column=2, padx=1)
        plus_btn = ctk.CTkButton(
            row_frame,
            text="＋",
            width=24,
            height=24,
            font=("Microsoft YaHei", 12),
            fg_color="#2f3540",
            hover_color="#3a424e",
            command=lambda n=nudge: n(NUDGE_STEP),
        )
        plus_btn.grid(row=0, column=3, padx=1)
        value_label.grid(row=0, column=4, padx=(8, 8))

        def on_enabled_toggle(fid=feature_id, cfg_key=key + "_enabled", var=enabled_var):
            callbacks["set_config"](fid, cfg_key, 1.0 if var.get() else 0.0)

        enabled_switch = ctk.CTkSwitch(
            row_frame,
            text="",
            width=40,
            variable=enabled_var,
            command=on_enabled_toggle,
        )
        enabled_switch.grid(row=0, column=5, padx=(0, 2))

        state["vars"][key] = value_var
        state["labels"][key] = value_label
        state["sliders"][key] = slider
        state["enabled_vars"][key] = enabled_var
        state["enabled_switches"][key] = enabled_switch

        def refresh_row(
            *_args,
            var=value_var,
            label=value_label,
            enabled_var=enabled_var,
            slider=slider,
            minus=minus_btn,
            plus=plus_btn,
        ):
            numeric = float(var.get())
            enabled = bool(enabled_var.get())
            label.configure(
                text=f"{numeric:.1f}x",
                text_color=_value_color(numeric) if enabled else DISABLED_COLOR,
            )
            control_state = "normal" if enabled else "disabled"
            slider.configure(state=control_state)
            minus.configure(state=control_state)
            plus.configure(state=control_state)
            refresh_summary()

        # 变量 trace 同时覆盖「用户拖滑块」和「程序按配置回填」两种情况。
        value_var.trace_add("write", refresh_row)
        enabled_var.trace_add("write", refresh_row)
        refresh_row()

    foot.pack(fill="x", padx=10, pady=(4, 8))

    result = {
        handles.get("switch", "damage_multiplier_switch"): switch,
        handles.get("summary", "damage_multiplier_summary"): summary,
        handles.get("reset_button", "damage_multiplier_reset_btn"): reset_btn,
    }
    for key, _name, _color in CATEGORIES:
        result[handles.get(key + "_multiplier_var", f"damage_multiplier_{key}_var")] = state["vars"][key]
        result[handles.get(key + "_multiplier_slider", f"damage_multiplier_{key}_slider")] = state["sliders"][key]
        result[handles.get(key + "_multiplier_label", f"damage_multiplier_{key}_label")] = state["labels"][key]
        result[handles.get(key + "_enabled_var", f"damage_multiplier_{key}_enabled_var")] = state["enabled_vars"][key]
        result[handles.get(key + "_enabled_switch", f"damage_multiplier_{key}_enabled_switch")] = state["enabled_switches"][key]
    return result
