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

    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))

    ctk.CTkLabel(
        top,
        text=f"{manifest.get('icon', '')} {manifest.get('display_name', '')}",
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
        text_color="#cbd5e1",
        font=("Microsoft YaHei", 12),
        wraplength=560,
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=12, pady=(4, 4))

    button_row = ctk.CTkFrame(frame, fg_color="transparent")
    button_row.pack(fill="x", padx=12, pady=(2, 4))
    button_row.grid_columnconfigure((0, 1), weight=1, uniform="fixed_point_teleport_actions")

    save_button = _button(
        button_row,
        controls.get("savepoint", {}).get("label", "保存当前位置"),
        lambda: callbacks["action"](feature_id, "savepoint"),
        "#2563eb",
    )
    save_button.grid(row=0, column=0, sticky="ew", padx=(0, 4))

    teleport_button = _button(
        button_row,
        controls.get("teleporttopoint", {}).get("label", "瞬移到保存点"),
        lambda: callbacks["action"](feature_id, "teleporttopoint"),
        "#16a34a",
    )
    teleport_button.grid(row=0, column=1, sticky="ew", padx=4)

    shortcut_label = ctk.CTkLabel(
        frame,
        text="快捷键：Alt+1 保存当前位置，Alt+2 瞬移到保存点",
        text_color="#9aa3b2",
        font=("Microsoft YaHei", 11),
        anchor="w",
    )
    shortcut_label.pack(fill="x", padx=12, pady=(0, 4))

    return {
        handles.get("switch", "fixed_point_teleport_switch"): switch,
        handles.get("save_button", "fixed_point_teleport_save_btn"): save_button,
        handles.get("teleport_button", "fixed_point_teleport_teleport_btn"): teleport_button,
    }
