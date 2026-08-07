import customtkinter as ctk


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    slider_control = next(
        (item for item in manifest.get("controls", []) if item.get("type") == "slider"),
        {},
    )
    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="transparent", border_width=1, border_color="#4b5563")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)
    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(top, text=manifest["display_name"], font=("Microsoft YaHei", 15, "bold"), text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0")).pack(side="left", padx=4)
    switch = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: callbacks["toggle"](feature_id))
    switch.pack(side="right", padx=6)
    ctk.CTkLabel(frame, font=("Microsoft YaHei", 12), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", padx=10, pady=(4, 8))

    slider_frame = ctk.CTkFrame(frame, fg_color="transparent")
    slider_frame.pack(fill="x", padx=8, pady=(4, 8))
    slider_frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        slider_frame,
        text="加速倍率",
        font=("Microsoft YaHei", 12),
        text_color="#e0e0e0",
        anchor="w",
    ).grid(row=0, column=0, sticky="w", padx=4)

    var = ctk.DoubleVar(value=float(slider_control.get("default", 1.0)))
    step = float(slider_control.get("step", 0.1))
    slider_min = float(slider_control.get("min", 0.1))
    slider_max = float(slider_control.get("max", 10.0))

    def on_speed(value):
        numeric = round(float(value), 1)
        value_label.configure(text=f"{numeric:.1f}x")
        callbacks["set_config"](feature_id, slider_control.get("key", "speed"), numeric)

    value_label = ctk.CTkLabel(
        slider_frame,
        text=f"{float(slider_control.get('default', 1.0)):.1f}x",
        font=("Microsoft YaHei", 11),
        text_color="#e0e0e0",
        width=28,
    )
    value_label.grid(row=0, column=1, sticky="e", padx=4)

    slider = ctk.CTkSlider(
        slider_frame,
        from_=slider_min,
        to=slider_max,
        variable=var,
        number_of_steps=int(round((slider_max - slider_min) / step)) if step > 0 else 99,
        command=on_speed,
    )
    slider.grid(row=1, column=0, columnspan=2, sticky="ew", padx=4, pady=(2, 4))

    handles = manifest.get("ui_handles", {})
    return {
        handles.get("switch", "timescale_switch"): switch,
        handles.get("slider_var", "timescale_var"): var,
        handles.get("slider", "timescale_slider"): slider,
        handles.get("slider_label", "timescale_label"): value_label,
    }
