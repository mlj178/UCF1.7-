import customtkinter as ctk


SLIDERS = (
    ("承伤倍率", "damage_taken_multiplier", "damage_taken_var", 0.1, 3.0, 0.1),
    ("攻击倍率", "attack_damage_multiplier", "attack_damage_var", 0.1, 10.0, 0.1),
    ("移动倍率", "move_speed_multiplier", "move_speed_var", 0.5, 4.0, 0.1),
    ("刀速倍率", "knife_speed_multiplier", "knife_speed_var", 0.5, 6.0, 0.1),
    ("刀距倍率", "knife_range_multiplier", "knife_range_var", 0.5, 5.0, 0.1),
    ("击退倍率", "knockback_multiplier", "knockback_var", 0.0, 3.0, 0.1),
)


def build_card(scroll, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    config = manifest.get("config", {})
    handles = {}

    frame = ctk.CTkFrame(
        scroll,
        corner_radius=6,
        fg_color="#26312b",
        border_width=1,
        border_color="#3f5f49",
    )
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(3, weight=1)

    header = ctk.CTkFrame(frame, fg_color="transparent")
    header.grid(row=0, column=0, columnspan=4, sticky="ew", padx=10, pady=(8, 4))
    header.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(
        header,
        text=f"{manifest.get('icon', '')} {manifest.get('display_name', '')}",
        font=("Microsoft YaHei", 16, "bold"),
        text_color=manifest.get("layout", {}).get("title_color", "#22c55e"),
    ).grid(row=0, column=0, sticky="w")

    switch = ctk.CTkSwitch(
        header,
        text="",
        width=50,
        command=lambda: callbacks["toggle"](feature_id),
    )
    switch.grid(row=0, column=2, sticky="e")
    handles[manifest.get("ui_handles", {}).get("switch", f"{feature_id}_switch")] = switch

    desc = ctk.CTkLabel(
        frame,
        text=manifest.get("desc", ""),
        font=("Microsoft YaHei", 13),
        text_color="#b7c4bc",
        wraplength=650,
        justify="left",
        anchor="w",
    )
    desc.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=(0, 6))

    for index, item in enumerate(SLIDERS):
        label, key, handle_key, min_value, max_value, step = item
        slider_row = 2 + index // 2
        label_col = 0 if index % 2 == 0 else 2
        slider_col = 1 if index % 2 == 0 else 3

        value_var = ctk.DoubleVar(value=float(config.get(key, 1.0)))
        value_label = ctk.CTkLabel(
            frame,
            text=f"{value_var.get():.1f}x",
            font=("Microsoft YaHei", 12),
            text_color="#dbe7df",
            width=42,
        )

        ctk.CTkLabel(
            frame,
            text=label,
            font=("Microsoft YaHei", 13),
            text_color="#dbe7df",
            width=68,
            anchor="w",
        ).grid(row=slider_row, column=label_col, sticky="w", padx=(10, 4), pady=4)

        slider_frame = ctk.CTkFrame(frame, fg_color="transparent")
        slider_frame.grid(row=slider_row, column=slider_col, sticky="ew", padx=(0, 10), pady=4)
        slider_frame.grid_columnconfigure(0, weight=1)

        slider = ctk.CTkSlider(
            slider_frame,
            from_=min_value,
            to=max_value,
            number_of_steps=int((max_value - min_value) / step),
            variable=value_var,
            command=lambda value, cfg_key=key: callbacks["set_config"](feature_id, cfg_key, value),
        )
        slider.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        value_label.grid(row=0, column=1, sticky="e")
        value_var.trace_add("write", lambda *args, var=value_var, label_ref=value_label: label_ref.configure(text=f"{var.get():.1f}x"))

        handles[manifest.get("ui_handles", {}).get(handle_key, f"{feature_id}_{key}_var")] = value_var

    footer = ctk.CTkFrame(frame, fg_color="transparent")
    footer.grid(row=5, column=0, columnspan=4, sticky="ew", padx=10, pady=(4, 10))
    footer.grid_columnconfigure(1, weight=1)

    skill_var = ctk.BooleanVar(value=bool(config.get("skill_no_cooldown", True)))
    skill_switch = ctk.CTkSwitch(
        footer,
        text="技能无冷却",
        variable=skill_var,
        font=("Microsoft YaHei", 13),
        command=lambda: callbacks["set_config"](feature_id, "skill_no_cooldown", bool(skill_var.get())),
    )
    skill_switch.grid(row=0, column=0, sticky="w")
    handles[manifest.get("ui_handles", {}).get("skill_cd_switch", f"{feature_id}_skill_cd_switch")] = skill_switch

    status_button = ctk.CTkButton(
        footer,
        text="状态",
        width=72,
        height=30,
        command=lambda: callbacks["action"](feature_id, "status"),
        fg_color="#166534",
        hover_color="#14532d",
    )
    status_button.grid(row=0, column=2, sticky="e")
    handles[manifest.get("ui_handles", {}).get("status_button", f"{feature_id}_status_button")] = status_button

    return handles
