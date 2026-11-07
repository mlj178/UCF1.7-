import customtkinter as ctk


def _next_available_row(parent, requested_row):
    next_row = int(requested_row)
    for child in parent.grid_slaves():
        info = child.grid_info()
        try:
            child_end = int(info.get("row", 0)) + int(info.get("rowspan", 1))
        except (TypeError, ValueError):
            continue
        next_row = max(next_row, child_end)
    return next_row


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    row = _next_available_row(parent, row)
    frame = ctk.CTkFrame(
        parent,
        corner_radius=6,
        fg_color="transparent",
        border_width=1,
        border_color="#4b5563",
    )
    frame.grid(
        row=row,
        column=col,
        columnspan=colspan,
        sticky="ew",
        padx=3,
        pady=3,
    )

    ui_handles = manifest.get("ui_handles", {})

    handles = {}
    action_buttons = []

    def feature_enabled():
        return bool(callbacks["is_enabled"](feature_id))

    def sync_action_buttons():
        state = "normal" if feature_enabled() else "disabled"
        for button in action_buttons:
            button.configure(state=state)

    def on_switch_toggle():
        callbacks["toggle"](feature_id)
        sync_action_buttons()

    title_frame = ctk.CTkFrame(frame, fg_color="transparent")
    title_frame.pack(fill="x", padx=12, pady=(8, 2))

    ctk.CTkLabel(
        title_frame,
        text=manifest.get("display_name", "角色变身"),
        font=("Microsoft YaHei", 15, "bold"),
        text_color=manifest.get("layout", {}).get("title_color", "#A855F7"),
    ).pack(side="left", anchor="w")

    switch = ctk.CTkSwitch(
        title_frame,
        text="",
        font=("Microsoft YaHei", 12),
        command=on_switch_toggle,
    )
    switch.pack(side="right", padx=6)

    ctk.CTkLabel(
        frame,
        text=manifest.get("desc", ""),
        text_color="#a0a0a0",
        font=("Microsoft YaHei", 12),
        anchor="w",
        justify="left",
        wraplength=560,
    ).pack(fill="x", padx=12, pady=(0, 6))

    button_frame = ctk.CTkFrame(frame, fg_color="transparent")
    button_frame.pack(fill="x", padx=8, pady=(0, 8))
    button_frame.grid_columnconfigure((0, 1), weight=1, uniform="role_actions")

    def run_action(control):
        action = control.get("action", "trigger")
        payload = dict(control.get("payload") or {})
        if not feature_enabled():
            log = callbacks.get("log")
            if callable(log):
                log("⚠ 请先打开「角色变身」开关，变身按钮才会生效")
            return False
        return callbacks["action"](feature_id, action, payload)

    button_controls = [
        control
        for control in manifest.get("controls", [])
        if control.get("type") == "button"
    ]

    for index, control in enumerate(button_controls):
        payload_action = (control.get("payload") or {}).get("action", str(index))
        button = ctk.CTkButton(
            button_frame,
            text=control.get("label", payload_action),
            command=lambda selected=control: run_action(selected),
            height=36,
            fg_color="#7e22ce",
            hover_color="#6b21a8",
        )
        button.grid(
            row=index // 2,
            column=index % 2,
            sticky="ew",
            padx=4,
            pady=4,
        )
        action_buttons.append(button)
        handle_name = manifest.get("ui_handles", {}).get(
            payload_action,
            f"role_transform_{payload_action}_button",
        )
        handles[handle_name] = button

    sync_action_buttons()
    handles[ui_handles.get("switch", f"{feature_id}_switch")] = switch
    handles[f"{feature_id}_frame"] = frame
    return handles
