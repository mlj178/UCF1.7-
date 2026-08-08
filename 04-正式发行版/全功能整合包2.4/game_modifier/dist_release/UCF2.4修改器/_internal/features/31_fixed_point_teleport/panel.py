import customtkinter as ctk


def _controls_by_action(manifest):
    return {
        item.get("action"): item
        for item in manifest.get("controls", [])
        if item.get("action")
    }


def _button(parent, text, command, color):
    hover = {
        "#2563eb": "#1d4ed8",
        "#16a34a": "#15803d",
        "#6b7280": "#4b5563",
    }.get(color, "#1f2937")
    return ctk.CTkButton(
        parent,
        text=text,
        height=36,
        font=("Microsoft YaHei", 12, "bold"),
        command=command,
        fg_color=color,
        hover_color=hover,
    )


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})
    controls = _controls_by_action(manifest)

    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="transparent", border_width=1, border_color="#4b5563")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))

    ctk.CTkLabel(
        top,
        text=manifest.get("display_name", ""),
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

    ctk.CTkLabel(
        frame,
        text=manifest.get("desc", ""),
        text_color="#a0a0a0",
        font=("Microsoft YaHei", 12),
        wraplength=280 * colspan,
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(4, 8))

    button_row = ctk.CTkFrame(frame, fg_color="transparent")
    button_row.pack(fill="x", padx=12, pady=(2, 4))
    button_row.grid_columnconfigure(0, weight=0)
    button_row.grid_columnconfigure((1, 2), weight=1, uniform="fixed_point_teleport_actions")

    def add_slot(row_index, slot_label, save_action, teleport_action, default_save, default_teleport):
        ctk.CTkLabel(
            button_row,
            text=slot_label,
            text_color="#e5e7eb",
            font=("Microsoft YaHei", 12, "bold"),
            width=58,
            anchor="w",
        ).grid(row=row_index, column=0, sticky="w", padx=(0, 6), pady=2)

        save = _button(
            button_row,
            controls.get(save_action, {}).get("label", default_save),
            lambda action=save_action: callbacks["action"](feature_id, action),
            "#2563eb",
        )
        save.grid(row=row_index, column=1, sticky="ew", padx=4, pady=2)

        teleport = _button(
            button_row,
            controls.get(teleport_action, {}).get("label", default_teleport),
            lambda action=teleport_action: callbacks["action"](feature_id, action),
            "#16a34a",
        )
        teleport.grid(row=row_index, column=2, sticky="ew", padx=(4, 0), pady=2)
        return save, teleport

    save_button, teleport_button = add_slot(
        0,
        "点位1",
        "savepoint",
        "teleporttopoint",
        "保存点位1  Alt+1",
        "瞬移到点位1  Alt+2",
    )
    save_button2, teleport_button2 = add_slot(
        1,
        "点位2",
        "savepoint2",
        "teleporttopoint2",
        "保存点位2  Alt+3",
        "瞬移到点位2  Alt+4",
    )

    shortcut_label = ctk.CTkLabel(
        frame,
        text="快捷键：Alt+1 保存点位1，Alt+2 瞬移到点位1；Alt+3 保存点位2，Alt+4 瞬移到点位2",
        text_color="#9aa3b2",
        font=("Microsoft YaHei", 11),
        anchor="w",
    )
    shortcut_label.pack(fill="x", padx=12, pady=(0, 4))

    return {
        handles.get("switch", "fixed_point_teleport_switch"): switch,
        handles.get("save_button", "fixed_point_teleport_save_btn"): save_button,
        handles.get("teleport_button", "fixed_point_teleport_teleport_btn"): teleport_button,
        handles.get("save_button2", "fixed_point_teleport_save2_btn"): save_button2,
        handles.get("teleport_button2", "fixed_point_teleport_teleport2_btn"): teleport_button2,
    }
