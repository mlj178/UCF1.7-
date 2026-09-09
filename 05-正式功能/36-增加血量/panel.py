import customtkinter as ctk


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})
    controls = {item.get("action"): item for item in manifest.get("controls", []) if item.get("action")}
    slider_control = next(
        (item for item in manifest.get("controls", []) if item.get("type") == "slider"),
        {},
    )
    config_key = slider_control.get("key", "add_amount")

    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="transparent", border_width=1, border_color="#4b5563")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)

    # 标题行 + 开关
    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))

    ctk.CTkLabel(
        top,
        text=manifest.get("display_name", "增加血量"),
        font=("Microsoft YaHei", 15, "bold"),
        text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0"),
    ).pack(side="left", padx=4)

    switch = ctk.CTkSwitch(
        top,
        text=controls.get("enable", {}).get("label", ""),
        font=("Microsoft YaHei", 12),
        width=50,
        command=lambda: callbacks["toggle"](feature_id),
    )
    switch.pack(side="right", padx=6)

    # 说明
    ctk.CTkLabel(
        frame,
        text=manifest.get("desc", ""),
        text_color="#a0a0a0",
        font=("Microsoft YaHei", 12),
        wraplength=280 * colspan,
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(4, 6))

    # 单次加血量滑条
    slider_frame = ctk.CTkFrame(frame, fg_color="transparent")
    slider_frame.pack(fill="x", padx=12, pady=(0, 6))

    ctk.CTkLabel(slider_frame, text="单次加血量", font=("Microsoft YaHei", 12)).pack(side="left")

    slider_var = ctk.DoubleVar(value=float(slider_control.get("default", 10)))
    value_label = ctk.CTkLabel(
        slider_frame,
        text=str(int(slider_var.get())),
        font=("Microsoft YaHei", 12, "bold"),
        text_color="#93c5fd",
    )
    value_label.pack(side="right")

    slider = ctk.CTkSlider(
        slider_frame,
        from_=float(slider_control.get("min", 1)),
        to=float(slider_control.get("max", 100)),
        number_of_steps=max(0, int(slider_control.get("max", 100)) - int(slider_control.get("min", 1))),
        variable=slider_var,
        command=lambda value: (
            value_label.configure(text=str(int(value))),
            callbacks["set_config"](feature_id, config_key, int(value)),
        ),
    )
    slider.pack(fill="x", pady=(4, 0))

    # 加血按钮
    add_button = ctk.CTkButton(
        frame,
        text=controls.get("addhp", {}).get("label", "加血一次 · F3"),
        height=36,
        font=("Microsoft YaHei", 12, "bold"),
        fg_color="#16a34a",
        hover_color="#15803d",
        command=lambda: callbacks["action"](feature_id, "addhp"),
    )
    add_button.pack(fill="x", padx=12, pady=(4, 4))

    # 快捷键提示
    ctk.CTkLabel(
        frame,
        text="快捷键：F3 加一次血（正式接入整合包时在 core/config.py 注册 F3）",
        text_color="#9aa3b2",
        font=("Microsoft YaHei", 11),
        anchor="w",
    ).pack(fill="x", padx=12, pady=(0, 8))

    return {
        handles.get("switch", "hp_boost_switch"): switch,
        handles.get("slider_var", "hp_boost_add_amount_var"): slider_var,
        handles.get("slider_label", "hp_boost_add_amount_label"): value_label,
        handles.get("add_button", "hp_boost_add_button"): add_button,
    }