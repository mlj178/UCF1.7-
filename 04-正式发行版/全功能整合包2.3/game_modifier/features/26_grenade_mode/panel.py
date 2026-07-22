import json
from pathlib import Path

import customtkinter as ctk


def _load_manifest():
    with (Path(__file__).with_name("manifest.json")).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _control_map(manifest):
    return {item["key"]: item for item in manifest.get("controls", []) if item.get("key")}


def _merged_config(context, manifest):
    config = dict(manifest.get("config") or {})
    config.update(context.get_config() or {})
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
    context.config_manager.set(feature_id, {key: value})
    if context.is_connected() and context.is_enabled():
        context.feature_service.set_config(feature_id, {key: value})


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


def _switch(parent, context, control, config, handles):
    key = control["key"]
    var = ctk.BooleanVar(value=bool(config.get(key, control.get("default", False))))
    switch = ctk.CTkSwitch(
        parent,
        text=control.get("label", key),
        variable=var,
        font=("Microsoft YaHei", 12),
        command=lambda: _set_config(context, key, bool(var.get())),
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

    combo = ctk.CTkOptionMenu(
        row,
        values=list(value_by_label.keys()),
        variable=var,
        command=on_select,
        width=180,
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
        text_color="#d1d5db",
        anchor="w",
    ).grid(row=0, column=0, sticky="w", padx=(0, 8))
    value_label = ctk.CTkLabel(
        row,
        text=_format_number(initial, suffix),
        width=70,
        font=("Microsoft YaHei", 12),
        text_color="#e5e7eb",
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


def _add_switch_grid(parent, context, controls, config, handles, keys):
    grid = ctk.CTkFrame(parent, fg_color="transparent")
    grid.pack(fill="x", padx=4, pady=(0, 6))
    grid.grid_columnconfigure(0, weight=1)
    grid.grid_columnconfigure(1, weight=1)
    for index, key in enumerate(keys):
        cell = ctk.CTkFrame(grid, fg_color="transparent")
        cell.grid(row=index // 2, column=index % 2, sticky="ew", padx=4, pady=1)
        _switch(cell, context, controls[key], config, handles)


def _add_slider_rows(parent, context, controls, config, handles, keys):
    for key in keys:
        _slider(parent, context, controls[key], config, handles)


def _add_select_rows(parent, context, controls, config, handles, keys):
    for key in keys:
        _select(parent, context, controls[key], config, handles)


def build_panel(context, parent):
    manifest = _load_manifest()
    controls = _control_map(manifest)
    config = _merged_config(context, manifest)
    callbacks = context.callbacks
    feature_id = context.feature_id
    handles = {}

    root = ctk.CTkFrame(parent, fg_color="transparent")
    root.pack(fill="both", expand=True, padx=4, pady=4)

    content_box = ctk.CTkFrame(root, corner_radius=6, fg_color="#262626", border_width=1, border_color="#525252")
    content_box.pack(fill="x", padx=8, pady=(8, 6))
    title_row = ctk.CTkFrame(content_box, fg_color="transparent")
    title_row.pack(fill="x", padx=10, pady=(8, 2))
    ctk.CTkLabel(
        title_row,
        text=f"{manifest.get('icon', '')} {manifest.get('display_name', '手雷模式')}",
        font=("Microsoft YaHei", 18, "bold"),
        text_color="#f8fafc",
    ).pack(side="left")
    main_switch = ctk.CTkSwitch(
        title_row,
        text="开启",
        font=("Microsoft YaHei", 12),
        command=lambda: callbacks["toggle"](feature_id),
    )
    main_switch.pack(side="right", padx=8)
    if context.is_enabled():
        main_switch.select()
    else:
        main_switch.deselect()
    handles[manifest.get("ui_handles", {}).get("switch", "grenade_mode_switch")] = main_switch
    ctk.CTkLabel(
        content_box,
        text="手雷数量：999",
        font=("Microsoft YaHei", 12),
        text_color="#cbd5e1",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(0, 8))

    basic = _parameter_group(content_box, "")
    _add_select_rows(basic, context, controls, config, handles, ("infinite_grenade_scope",))

    bot = _parameter_group(content_box, "")
    _add_slider_rows(bot, context, controls, config, handles, ("bot_throw_drive_cooldown_ms",))

    runtime = _parameter_group(content_box, "手雷强化参数")
    _add_switch_grid(runtime, context, controls, config, handles, ("enable_damage", "enable_range", "enable_shoot_speed"))
    _add_slider_rows(runtime, context, controls, config, handles, ("damage_value", "range_value", "shoot_speed_value"))
    _add_select_rows(runtime, context, controls, config, handles, ("damage_apply_scope", "range_apply_scope", "shoot_speed_apply_scope"))

    careful = _parameter_group(content_box, "")
    _add_switch_grid(
        careful,
        context,
        controls,
        config,
        handles,
        ("force_throw_ready_enabled",),
    )
    _add_select_rows(careful, context, controls, config, handles, ("force_throw_ready_scope",))

    context.bind_handles(handles)
    return handles
