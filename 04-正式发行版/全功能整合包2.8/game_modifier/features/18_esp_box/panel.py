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

    defaults = manifest.get("config", {}) or {}
    config = callbacks.get("get_config", lambda _feature_id: {})(feature_id) or {}

    body = ctk.CTkFrame(frame, fg_color="transparent")
    body.pack(fill="x", padx=10, pady=(0, 8))
    body.grid_columnconfigure(1, weight=1)

    # --- 显示对象（原功能） ---
    scope_values = ["仅显示敌人", "敌人和队友"]
    scope_to_value = {
        "仅显示敌人": "enemy_only",
        "敌人和队友": "all_players",
    }
    current_scope = config.get("esp_target_scope", defaults.get("esp_target_scope", "enemy_only"))
    selected_scope = next(
        (label for label, value in scope_to_value.items() if value == current_scope),
        scope_values[0],
    )

    # --- 血量显示格式：百分比 / 剩余数值（只显示当前血量） ---
    mode_values = ["百分比", "剩余数值"]
    mode_to_value = {
        "百分比": "percent",
        "剩余数值": "value",
    }
    current_mode = config.get("esp_health_mode", defaults.get("esp_health_mode", "percent"))
    selected_mode = next(
        (label for label, value in mode_to_value.items() if value == current_mode),
        mode_values[0],
    )

    # --- 显示内容：仅血条 / 仅数值 / 血条和数值 ---
    display_values = ["仅血条", "仅数值", "血条和数值"]
    display_to_value = {
        "仅血条": "bar",
        "仅数值": "text",
        "血条和数值": "both",
    }
    current_display = config.get(
        "esp_health_display", defaults.get("esp_health_display", "both")
    )
    selected_display = next(
        (label for label, value in display_to_value.items() if value == current_display),
        display_values[2],
    )

    # --- 方框轮廓开关：关闭后只看血条/数值，不画方框 ---
    current_outline = config.get("esp_box_outline", defaults.get("esp_box_outline", True))
    if isinstance(current_outline, str):
        current_outline = current_outline.strip().lower() not in ("false", "0", "no", "off")

    def add_row(row_index, label_text, values, selected_label, on_change):
        ctk.CTkLabel(
            body,
            text=label_text,
            font=("Microsoft YaHei", 13),
            text_color="#c0c0c0",
            width=72,
            anchor="w",
        ).grid(row=row_index, column=0, padx=(0, 8), pady=3, sticky="w")
        combo = ctk.CTkComboBox(
            body,
            values=values,
            command=on_change,
            font=("Microsoft YaHei", 13),
            dropdown_font=("Microsoft YaHei", 13),
            width=180,
            state="readonly",
        )
        combo.set(selected_label)
        combo.grid(row=row_index, column=1, padx=(0, 8), pady=3, sticky="w")
        return combo

    def on_scope_changed(label):
        callbacks["set_config"](feature_id, "esp_target_scope", scope_to_value[label])
        schedule_sync()

    def on_mode_changed(label):
        callbacks["set_config"](feature_id, "esp_health_mode", mode_to_value[label])
        schedule_sync()

    def on_display_changed(label):
        callbacks["set_config"](feature_id, "esp_health_display", display_to_value[label])
        schedule_sync()

    def on_outline_toggled():
        callbacks["set_config"](feature_id, "esp_box_outline", bool(outline_switch.get()))
        schedule_sync()

    scope_menu = add_row(0, "显示对象", scope_values, selected_scope, on_scope_changed)
    mode_menu = add_row(1, "血量显示", mode_values, selected_mode, on_mode_changed)
    display_menu = add_row(2, "显示内容", display_values, selected_display, on_display_changed)

    # 方框轮廓：独立开关，可与「显示内容」组合成只留血条/数值
    ctk.CTkLabel(
        body,
        text="方框轮廓",
        font=("Microsoft YaHei", 13),
        text_color="#c0c0c0",
        width=72,
        anchor="w",
    ).grid(row=3, column=0, padx=(0, 8), pady=3, sticky="w")
    outline_switch = ctk.CTkSwitch(
        body,
        text="",
        font=("Microsoft YaHei", 13),
        command=on_outline_toggled,
        onvalue=1,
        offvalue=0,
    )
    if current_outline:
        outline_switch.select()
    else:
        outline_switch.deselect()
    outline_switch.grid(row=3, column=1, padx=(0, 8), pady=3, sticky="w")

    # --- 所选即所得 ---------------------------------------------------------
    # 配置是唯一权威来源：改动失败时后端会把配置回退成 DLL 当前生效值，
    # 这里负责把控件重新对齐到配置，避免"界面选 A、游戏里是 B"。
    def sync_from_config():
        try:
            latest = callbacks.get("get_config", lambda _feature_id: {})(feature_id) or {}
        except Exception:
            return

        scope_now = latest.get("esp_target_scope", defaults.get("esp_target_scope", "enemy_only"))
        label = next(
            (item for item, value in scope_to_value.items() if value == scope_now), scope_values[0]
        )
        if scope_menu.get() != label:
            scope_menu.set(label)

        mode_now = latest.get("esp_health_mode", defaults.get("esp_health_mode", "percent"))
        label = next(
            (item for item, value in mode_to_value.items() if value == mode_now), mode_values[0]
        )
        if mode_menu.get() != label:
            mode_menu.set(label)

        display_now = latest.get(
            "esp_health_display", defaults.get("esp_health_display", "both")
        )
        label = next(
            (item for item, value in display_to_value.items() if value == display_now),
            display_values[2],
        )
        if display_menu.get() != label:
            display_menu.set(label)

        outline_now = latest.get("esp_box_outline", defaults.get("esp_box_outline", True))
        if isinstance(outline_now, str):
            outline_now = outline_now.strip().lower() not in ("false", "0", "no", "off")
        if bool(outline_now) != bool(outline_switch.get()):
            outline_switch.select() if outline_now else outline_switch.deselect()

    def schedule_sync():
        # 下发在后台线程，失败回退可能晚一点到；多补几次确保界面最终对齐。
        for delay in (800, 2000, 4000):
            try:
                outline_switch.after(delay, sync_from_config)
            except Exception:
                pass

    return {
        manifest.get("ui_handles", {}).get("switch", "esp_box_switch"): switch,
        "esp_target_scope_menu": scope_menu,
        "esp_health_mode_menu": mode_menu,
        "esp_health_display_menu": display_menu,
        "esp_box_outline_switch": outline_switch,
    }
