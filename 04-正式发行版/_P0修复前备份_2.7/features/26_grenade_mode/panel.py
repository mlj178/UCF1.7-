import json
from pathlib import Path

import customtkinter as ctk


CARD_GROUPS = ("手雷模式", "无限手雷", "手雷强化")
ENHANCEMENT_GROUPS = (
    ("enable_damage", "damage_value", "damage_apply_scope"),
    ("enable_range", "range_value", "range_apply_scope"),
    ("enable_shoot_speed", "shoot_speed_value", "shoot_speed_apply_scope"),
)
DEPENDENT_KEYS = ("bot_grenade_mode_enabled",)
SESSION_ONLY_KEYS = ("bot_grenade_mode_enabled",)
USER_SWITCH_KEYS = (
    "lock999_enabled",
    "enable_damage",
    "enable_range",
    "enable_shoot_speed",
    "bot_grenade_mode_enabled",
)


def feature_should_run(config):
    """判断是否有任意独立手雷功能需要共享运行时。"""
    independent_keys = ("lock999_enabled", "enable_damage", "enable_range", "enable_shoot_speed")
    if any(bool(config.get(key, False)) for key in independent_keys):
        return True
    return bool(config.get("lock999_enabled", False) and any(config.get(key, False) for key in DEPENDENT_KEYS))


def requires_infinite_grenade(key):
    return key in DEPENDENT_KEYS


def should_persist_config(key):
    return key not in SESSION_ONLY_KEYS


def apply_session_defaults(config):
    for key in SESSION_ONLY_KEYS:
        config[key] = False


def should_auto_start(config, is_enabled):
    """页面打开时，已有功能配置开启且后端未运行则自动启动。"""
    return not is_enabled and feature_should_run(config)


def should_start_runtime(config, is_connected, is_enabled):
    """只有连接已就绪时才真正启动，避免按钮先开但脚本未加载。"""
    return bool(is_connected and should_auto_start(config, is_enabled))


def _load_manifest():
    with (Path(__file__).with_name("manifest.json")).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _control_map(manifest):
    return {item["key"]: item for item in manifest.get("controls", []) if item.get("key")}


def _merged_config(context, manifest):
    config = dict(manifest.get("config") or {})
    config.update(context.get_config() or {})
    apply_session_defaults(config)
    return config


def _display_value(control, value):
    scale = float(control.get("scale", 1.0) or 1.0)
    try:
        return float(value) / scale
    except (TypeError, ValueError):
        return float(control.get("default", 0.0))


def _format_number(value, suffix=""):
    numeric = float(value)
    if numeric.is_integer():
        text = str(int(numeric))
    else:
        text = f"{numeric:.1f}"
    return f"{text}{suffix}"


def _set_config(context, key, value):
    feature_id = context.feature_id
    if should_persist_config(key):
        context.config_manager.set(feature_id, {key: value})
    if context.is_connected() and context.is_enabled():
        if should_persist_config(key):
            context.feature_service.set_config(feature_id, {key: value})
        else:
            context.feature_service.set_config_runtime(feature_id, {key: value})
    config = dict(context.get_config() or {})
    config[key] = value
    # 联动说明：每张卡片都可独立使用；只要有一个子功能打开，就自动启动共享手雷后端。
    if feature_should_run(config) and not context.is_enabled():
        context.callbacks["toggle"](feature_id)


def _parameter_group(parent, title):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", padx=8, pady=(8, 2))
    if title:
        ctk.CTkLabel(
            frame,
            text=title,
            font=("Microsoft YaHei", 15, "bold"),
            text_color="#f3f4f6",
            anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))
    return frame


def _switch(parent, context, control, config, handles, on_change=None):
    key = control["key"]
    var = ctk.BooleanVar(value=bool(config.get(key, control.get("default", False))))
    def handle_change():
        value = bool(var.get())
        _set_config(context, key, value)
        if on_change:
            on_change(key, value, var, switch)

    switch = ctk.CTkSwitch(
        parent,
        text=control.get("label", key),
        variable=var,
        font=("Microsoft YaHei", 12),
        command=handle_change,
    )
    switch.pack(anchor="w", padx=12, pady=3)
    handles[f"{key}_switch"] = switch
    return switch


def _select(parent, context, control, config, handles):
    key = control["key"]
    display_values = control.get("display_values", {})
    value_by_label = {display_values.get(value, value): value for value in control.get("values", [])}
    label_by_value = {value: label for label, value in value_by_label.items()}
    current_value = config.get(key, control.get("default"))
    current_label = label_by_value.get(current_value, next(iter(value_by_label), ""))
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", padx=12, pady=3)
    ctk.CTkLabel(
        row,
        text=control.get("label", key),
        width=150,
        font=("Microsoft YaHei", 12),
        text_color="#d1d5db",
        anchor="w",
    ).pack(side="left", padx=(0, 8))
    var = ctk.StringVar(value=current_label)

    def on_select(label):
        _set_config(context, key, value_by_label.get(label, current_value))

    combo = ctk.CTkComboBox(
        row,
        values=list(value_by_label.keys()),
        variable=var,
        command=on_select,
        width=180,
        state="readonly",
    )
    combo.pack(side="left")
    handles[f"{key}_select"] = combo
    return combo


def _slider(parent, context, control, config, handles):
    key = control["key"]
    suffix = control.get("suffix", "")
    initial = _display_value(control, config.get(key, control.get("default", 0.0)))
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", padx=12, pady=4)
    row.grid_columnconfigure(1, weight=1)
    ctk.CTkLabel(
        row,
        text=control.get("label", key),
        width=150,
        font=("Microsoft YaHei", 12),
        text_color="#e0e0e0",
        anchor="w",
    ).grid(row=0, column=0, sticky="w", padx=(0, 8))
    value_label = ctk.CTkLabel(
        row,
        text=_format_number(initial, suffix),
        width=28,
        font=("Microsoft YaHei", 11),
        text_color="#e0e0e0",
    )
    value_label.grid(row=0, column=2, sticky="e", padx=(8, 0))
    var = ctk.DoubleVar(value=initial)
    minimum = float(control.get("min", 0.0))
    maximum = float(control.get("max", 1.0))
    step = float(control.get("step", 0.1))
    scale = float(control.get("scale", 1.0) or 1.0)

    def on_change(raw):
        numeric = round(float(raw), 1)
        value_label.configure(text=_format_number(numeric, suffix))
        outgoing = numeric * scale
        if step >= 1 and scale == 1.0:
            outgoing = int(round(outgoing))
        else:
            outgoing = round(outgoing, 4)
        _set_config(context, key, outgoing)

    slider = ctk.CTkSlider(
        row,
        from_=minimum,
        to=maximum,
        number_of_steps=int(round((maximum - minimum) / step)) if step > 0 else 100,
        variable=var,
        command=on_change,
    )
    slider.grid(row=0, column=1, sticky="ew")
    handles[f"{key}_var"] = var
    handles[f"{key}_slider"] = slider
    handles[f"{key}_label"] = value_label
    return slider


def _add_switch_grid(parent, context, controls, config, handles, keys, on_change=None):
    grid = ctk.CTkFrame(parent, fg_color="transparent")
    grid.pack(fill="x", padx=4, pady=(0, 6))
    grid.grid_columnconfigure(0, weight=1)
    grid.grid_columnconfigure(1, weight=1)
    for index, key in enumerate(keys):
        cell = ctk.CTkFrame(grid, fg_color="transparent")
        cell.grid(row=index // 2, column=index % 2, sticky="ew", padx=4, pady=1)
        _switch(cell, context, controls[key], config, handles, on_change=on_change)


def _add_slider_rows(parent, context, controls, config, handles, keys):
    for key in keys:
        _slider(parent, context, controls[key], config, handles)


def _add_select_rows(parent, context, controls, config, handles, keys):
    for key in keys:
        _select(parent, context, controls[key], config, handles)


def _inline_enhancement_row(parent, context, controls, config, handles, keys, on_change):
    switch_key, slider_key, scope_key = keys
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", padx=12, pady=4)
    row.grid_columnconfigure(1, weight=1)

    switch_control = controls[switch_key]
    switch_var = ctk.BooleanVar(value=bool(config.get(switch_key, switch_control.get("default", False))))

    def handle_switch():
        value = bool(switch_var.get())
        _set_config(context, switch_key, value)
        on_change(switch_key, value, switch_var, switch)

    switch = ctk.CTkSwitch(
        row,
        text=switch_control.get("label", switch_key),
        variable=switch_var,
        font=("Microsoft YaHei", 12),
        command=handle_switch,
        width=150,
    )
    switch.grid(row=0, column=0, sticky="w", padx=(0, 8))
    handles[f"{switch_key}_switch"] = switch

    slider_control = controls[slider_key]
    initial = _display_value(slider_control, config.get(slider_key, slider_control.get("default", 0.0)))
    value_label = ctk.CTkLabel(
        row,
        text=_format_number(initial, slider_control.get("suffix", "")),
        width=28,
        font=("Microsoft YaHei", 11),
        text_color="#e0e0e0",
    )
    value_label.grid(row=0, column=2, sticky="e", padx=(8, 8))
    minimum = float(slider_control.get("min", 0.0))
    maximum = float(slider_control.get("max", 1.0))
    step = float(slider_control.get("step", 0.1))
    scale = float(slider_control.get("scale", 1.0) or 1.0)

    def handle_slider(raw):
        numeric = round(float(raw), 1)
        value_label.configure(text=_format_number(numeric, slider_control.get("suffix", "")))
        outgoing = numeric * scale
        if step >= 1 and scale == 1.0:
            outgoing = int(round(outgoing))
        else:
            outgoing = round(outgoing, 4)
        _set_config(context, slider_key, outgoing)

    slider = ctk.CTkSlider(
        row,
        from_=minimum,
        to=maximum,
        number_of_steps=int(round((maximum - minimum) / step)) if step > 0 else 100,
        variable=ctk.DoubleVar(value=initial),
        command=handle_slider,
    )
    slider.grid(row=0, column=1, sticky="ew")
    handles[f"{slider_key}_slider"] = slider
    handles[f"{slider_key}_label"] = value_label

    scope_control = controls[scope_key]
    display_values = scope_control.get("display_values", {})
    value_by_label = {display_values.get(value, value): value for value in scope_control.get("values", [])}
    label_by_value = {value: label for label, value in value_by_label.items()}
    current_value = config.get(scope_key, scope_control.get("default"))
    scope_var = ctk.StringVar(value=label_by_value.get(current_value, next(iter(value_by_label), "")))

    def handle_scope(label):
        _set_config(context, scope_key, value_by_label.get(label, current_value))

    scope = ctk.CTkComboBox(row, values=list(value_by_label.keys()), variable=scope_var, command=handle_scope, width=145, state="readonly")
    scope.grid(row=0, column=3, sticky="e")
    handles[f"{scope_key}_select"] = scope


def _add_enhancement_rows(parent, context, controls, config, handles, on_change):
    for keys in ENHANCEMENT_GROUPS:
        _inline_enhancement_row(parent, context, controls, config, handles, keys, on_change)


def _card(parent, title):
    card = ctk.CTkFrame(parent, corner_radius=6, fg_color="transparent", border_width=1, border_color="#4b5563")
    card.pack(fill="x", padx=8, pady=5)
    ctk.CTkLabel(
        card,
        text=title,
        font=("Microsoft YaHei", 16, "bold"),
        text_color="#f3f4f6",
        anchor="w",
    ).pack(fill="x", padx=12, pady=(10, 5))
    return card


def _sync_engine(context, config, handles):
    # 联动说明：所有卡片共用一个脚本，因此只在“至少一个功能启用”时运行，全部关闭后停止。
    if feature_should_run(config) and not context.is_enabled():
        context.callbacks["toggle"](context.feature_id)
    elif not feature_should_run(config) and context.is_enabled():
        context.callbacks["toggle"](context.feature_id)


def _on_user_switch(context, config, handles, key, value, var, switch):
    config[key] = value
    # 联动说明：手雷模式依赖无限手雷，开启时自动打开无限手雷。
    if requires_infinite_grenade(key) and value and not config.get("lock999_enabled", False):
        config["lock999_enabled"] = True
        _set_config(context, "lock999_enabled", True)
        infinite_switch = handles.get("lock999_enabled_switch")
        if infinite_switch:
            infinite_switch.select()
    # 联动说明：如果依赖功能仍开启，用户关闭无限手雷时会被自动恢复，避免留下无效状态。
    elif key == "lock999_enabled" and not value and any(config.get(dependent_key, False) for dependent_key in DEPENDENT_KEYS):
        config["lock999_enabled"] = True
        _set_config(context, "lock999_enabled", True)
        switch.select()
    _sync_engine(context, config, handles)
    if not should_persist_config(key) and context.is_connected() and context.is_enabled():
        context.feature_service.set_config_runtime(context.feature_id, {key: value})


def build_panel(context, parent):
    manifest = _load_manifest()
    controls = _control_map(manifest)
    config = _merged_config(context, manifest)
    handles = {}

    # 联动说明：手雷模式仅本次运行有效，启动时关闭并清除旧版本可能留下的记忆。
    for key in SESSION_ONLY_KEYS:
        context.config_manager.remove_user_key(context.feature_id, key)

    def sync_runtime():
        current_config = _merged_config(context, manifest)
        if should_start_runtime(current_config, context.is_connected(), context.is_enabled()):
            context.callbacks["toggle"](context.feature_id)

    # 联动说明：页面未连接时只显示已保存状态，不尝试启动脚本；连接成功后再同步一次，避免“开关已开但功能未运行”。
    context.event_bus.subscribe("game_connected", lambda **_: context.after(0, sync_runtime))
    if should_start_runtime(config, context.is_connected(), context.is_enabled()):
        context.callbacks["toggle"](context.feature_id)

    root = ctk.CTkFrame(parent, fg_color="transparent")
    root.pack(fill="both", expand=True, padx=4, pady=4)

    title_row = ctk.CTkFrame(root, fg_color="transparent")
    title_row.pack(fill="x", padx=10, pady=(8, 2))
    ctk.CTkLabel(
        title_row,
        text=manifest.get("display_name", "手雷模式"),
        font=("Microsoft YaHei", 18, "bold"),
        text_color="#f8fafc",
    ).pack(side="left")
    ctk.CTkLabel(
        root,
        text="三个卡片可单独使用；手雷模式依赖无限手雷。",
        font=("Microsoft YaHei", 12),
        text_color="#a0a0a0",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(0, 5))

    def on_switch(key, value, var, switch):
        _on_user_switch(context, config, handles, key, value, var, switch)

    bot_card = _card(root, CARD_GROUPS[0])
    ctk.CTkLabel(
        bot_card,
        text="人机禁枪改投雷，全员进入手雷战。",
        font=("Microsoft YaHei", 12),
        text_color="#a0a0a0",
        anchor="w",
    ).pack(fill="x", padx=12, pady=(0, 4))
    _switch(bot_card, context, controls["bot_grenade_mode_enabled"], config, handles, on_change=on_switch)
    _add_slider_rows(bot_card, context, controls, config, handles, ("bot_throw_drive_cooldown_ms",))

    infinite_card = _card(root, CARD_GROUPS[1])
    _switch(infinite_card, context, controls["lock999_enabled"], config, handles, on_change=on_switch)
    _add_select_rows(infinite_card, context, controls, config, handles, ("infinite_grenade_scope",))

    enhancement_card = _card(root, CARD_GROUPS[2])
    _add_enhancement_rows(enhancement_card, context, controls, config, handles, on_switch)

    context.bind_handles(handles)
    return handles
