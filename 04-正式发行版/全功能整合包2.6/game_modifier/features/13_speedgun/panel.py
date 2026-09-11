import customtkinter as ctk


def _control(manifest, control_type=None, key=None):
    for item in manifest.get("controls", []):
        if control_type and item.get("type") != control_type:
            continue
        if key and item.get("key") != key:
            continue
        return item
    return {}


def _steps(control):
    minimum = float(control.get("min", 1.0))
    maximum = float(control.get("max", 10.0))
    step = float(control.get("step", 0.1))
    return int(round((maximum - minimum) / step)) if step > 0 else 100


def build_card(scroll, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})
    slider_control = _control(manifest, "slider", "fire_rate")
    lines = manifest.get("ui_text", {}).get("lines", [manifest.get("desc", "")])

    frame = ctk.CTkFrame(
        scroll,
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
        text=manifest["display_name"],
        font=("Microsoft YaHei", 15, "bold"),
        text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0"),
    ).pack(side="left", padx=4)
    switch = ctk.CTkSwitch(
        top,
        text="",
        font=("Microsoft YaHei", 12),
        width=50,
        command=lambda: callbacks["toggle"](feature_id),
    )
    switch.pack(side="right", padx=6)

    ctk.CTkLabel(
        frame,
        text="\n".join(lines),
        text_color="#a0a0a0",
        font=("Microsoft YaHei", 12),
        wraplength=280 * colspan,
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(4, 8))

    slider_row = ctk.CTkFrame(frame, fg_color="transparent")
    slider_row.pack(fill="x", padx=12, pady=(2, 8))
    slider_row.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(
        slider_row,
        text=slider_control.get("label", "射速倍率"),
        font=("Microsoft YaHei", 12),
        text_color="#e0e0e0",
    ).grid(row=0, column=0, sticky="w", padx=(0, 8))

    value_label = ctk.CTkLabel(
        slider_row,
        text=f"{float(slider_control.get('default', 10.0)):.1f}x",
        font=("Microsoft YaHei", 11),
        text_color="#e0e0e0",
        width=28,
    )
    value_label.grid(row=0, column=2, sticky="e", padx=(8, 0))

    var = ctk.DoubleVar(value=float(slider_control.get("default", 10.0)))

    def on_change(value):
        numeric = round(float(value), 1)
        value_label.configure(text=f"{numeric:.1f}x")
        callbacks["set_config"](feature_id, "fire_rate", numeric)

    slider = ctk.CTkSlider(
        slider_row,
        from_=float(slider_control.get("min", 1.0)),
        to=float(slider_control.get("max", 10.0)),
        number_of_steps=_steps(slider_control),
        variable=var,
        command=on_change,
    )
    slider.grid(row=0, column=1, sticky="ew", padx=4)

    return {
        handles.get("switch", "speedgun_switch"): switch,
        handles.get("slider_var", "speedgun_rate_var"): var,
        handles.get("slider_slider", "speedgun_rate_slider"): slider,
        handles.get("slider_label", "speedgun_rate_label"): value_label,
    }