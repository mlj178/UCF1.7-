import customtkinter as ctk


def _control(manifest, control_type, key=None):
    for item in manifest.get("controls", []):
        if item.get("type") != control_type:
            continue
        if key is None or item.get("key") == key:
            return item
    return {}


def _steps(control):
    step = float(control.get("step", 0.1))
    if step <= 0:
        return 1
    return int(round((float(control["max"]) - float(control["min"])) / step))


def _display_values(control):
    mapping = control.get("display_values", {})
    values = control.get("values", [])
    return [mapping.get(value, value) for value in values]


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})
    gravity_control = _control(manifest, "slider", "gravity")
    jump_control = _control(manifest, "slider", "jump")
    mode_control = _control(manifest, "combo", "mode")
    mode_labels = _display_values(mode_control)
    mode_by_label = {
        label: value
        for value, label in zip(mode_control.get("values", []), mode_labels)
    }

    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(
        top,
        text=f"{manifest['icon']} {manifest['display_name']}",
        font=("Microsoft YaHei", 15, "bold"),
        text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0"),
    ).pack(side="left", padx=4)
    switch = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: callbacks["toggle"](feature_id))
    switch.pack(side="right", padx=12)

    slider_frame = ctk.CTkFrame(frame, fg_color="transparent")
    slider_frame.pack(fill="x", padx=8, pady=(4, 0))
    ctk.CTkLabel(slider_frame, text=gravity_control.get("label", "\u91cd\u529b:"), font=("Microsoft YaHei", 11), text_color="#e0e0e0").pack(side="left", padx=(4, 2))
    gravity_var = ctk.DoubleVar(value=float(gravity_control.get("default", 1.0)))
    gravity_label = ctk.CTkLabel(slider_frame, text="1.0", font=("Microsoft YaHei", 11), text_color="#e0e0e0", width=28)

    def on_gravity(value):
        numeric = round(float(value), 1)
        gravity_label.configure(text=f"{numeric:.1f}")
        callbacks["set_config"](feature_id, gravity_control.get("key", "gravity"), numeric)

    gravity_slider = ctk.CTkSlider(
        slider_frame,
        from_=float(gravity_control.get("min", 0.0)),
        to=float(gravity_control.get("max", 1.0)),
        variable=gravity_var,
        number_of_steps=_steps(gravity_control),
        command=on_gravity,
        width=100,
    )
    gravity_slider.pack(side="left", padx=2)
    gravity_label.pack(side="left", padx=(2, 6))

    ctk.CTkLabel(slider_frame, text=jump_control.get("label", "\u8df3\u8dc3:"), font=("Microsoft YaHei", 11), text_color="#e0e0e0").pack(side="left", padx=(4, 2))
    jump_var = ctk.DoubleVar(value=float(jump_control.get("default", 1.0)))
    jump_label = ctk.CTkLabel(slider_frame, text="1.0", font=("Microsoft YaHei", 11), text_color="#e0e0e0", width=28)

    def on_jump(value):
        numeric = round(float(value), 1)
        jump_label.configure(text=f"{numeric:.1f}")
        callbacks["set_config"](feature_id, jump_control.get("key", "jump"), numeric)

    jump_slider = ctk.CTkSlider(
        slider_frame,
        from_=float(jump_control.get("min", 1.0)),
        to=float(jump_control.get("max", 5.0)),
        variable=jump_var,
        number_of_steps=_steps(jump_control),
        command=on_jump,
        width=100,
    )
    jump_slider.pack(side="left", padx=2)
    jump_label.pack(side="left", padx=2)

    mode_frame = ctk.CTkFrame(frame, fg_color="transparent")
    mode_frame.pack(fill="x", padx=8, pady=(2, 2))
    ctk.CTkLabel(mode_frame, text=mode_control.get("label", "\u751f\u6548\u8303\u56f4:"), font=("Microsoft YaHei", 11), text_color="#e0e0e0").pack(side="left", padx=(4, 4))
    mode_var = ctk.StringVar(value=mode_labels[0] if mode_labels else "")
    mode_combo = ctk.CTkComboBox(
        mode_frame,
        values=mode_labels,
        variable=mode_var,
        font=("Microsoft YaHei", 12),
        height=30,
        width=120,
        state="readonly",
        command=lambda value: callbacks["set_config"](
            feature_id,
            mode_control.get("key", "mode"),
            mode_by_label.get(value, value),
        ),
    )
    mode_combo.pack(side="left", padx=4)
    ctk.CTkLabel(frame, font=("Microsoft YaHei", 15), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=5, pady=5)
    return {
        handles.get("switch", "gravity_switch"): switch,
        handles.get("gravity_var", "gravity_var"): gravity_var,
        handles.get("gravity_slider", "gravity_slider"): gravity_slider,
        handles.get("gravity_label", "gravity_label"): gravity_label,
        handles.get("jump_var", "jump_var"): jump_var,
        handles.get("jump_slider", "jump_slider"): jump_slider,
        handles.get("jump_label", "jump_label"): jump_label,
        handles.get("mode_var", "gravity_mode_var"): mode_var,
        handles.get("mode_combo", "gravity_mode_combo"): mode_combo,
    }
