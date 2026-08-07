import customtkinter as ctk


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="transparent", border_width=1, border_color="#4b5563")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)
    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(top, text=manifest["display_name"], font=("Microsoft YaHei", 15, "bold"), text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0")).pack(side="left", padx=4)
    switch = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: callbacks["toggle"](feature_id))
    switch.pack(side="right", padx=6)
    ctk.CTkLabel(frame, font=("Microsoft YaHei", 12), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=10, pady=(4, 8))
    scope_values = ["仅显示敌人", "敌人和队友"]
    scope_to_value = {
        "仅显示敌人": "enemy_only",
        "敌人和队友": "all_players",
    }
    config = callbacks.get("get_config", lambda _feature_id: {})(feature_id) or {}
    current_scope = config.get("esp_target_scope", manifest.get("config", {}).get("esp_target_scope", "enemy_only"))
    selected_label = next(
        (label for label, value in scope_to_value.items() if value == current_scope),
        scope_values[0],
    )

    body = ctk.CTkFrame(frame, fg_color="transparent")
    body.pack(fill="x", padx=10, pady=(0, 8))
    body.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(
        body,
        text="显示对象",
        font=("Microsoft YaHei", 13),
        text_color="#c0c0c0",
        width=72,
        anchor="w",
    ).grid(row=0, column=0, padx=(0, 8), pady=3, sticky="w")

    def on_scope_changed(label):
        callbacks["set_config"](feature_id, "esp_target_scope", scope_to_value[label])

    scope_menu = ctk.CTkComboBox(
        body,
        values=scope_values,
        command=on_scope_changed,
        font=("Microsoft YaHei", 13),
        dropdown_font=("Microsoft YaHei", 13),
        width=180,
        state="readonly",
    )
    scope_menu.set(selected_label)
    scope_menu.grid(row=0, column=1, padx=(0, 8), pady=3, sticky="w")

    return {
        manifest.get("ui_handles", {}).get("switch", "esp_box_switch"): switch,
        "esp_target_scope_menu": scope_menu,
    }
