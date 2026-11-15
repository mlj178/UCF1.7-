import customtkinter as ctk


def build_card(scroll, manifest, row, col, colspan, callbacks, card_builder):
    """路点体检自定义卡片：总开关 + 三个子开关 + 一个按钮。"""
    feature_id = manifest["feature_id"]
    config = dict(manifest.get("config") or {})
    layout = manifest.get("layout") or {}

    frame = ctk.CTkFrame(
        scroll,
        corner_radius=6,
        fg_color="transparent",
        border_width=1,
        border_color="#4b5563",
    )
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    head = ctk.CTkFrame(frame, fg_color="transparent")
    head.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(
        head,
        text=manifest.get("display_name", "路点体检"),
        font=("Microsoft YaHei", 15, "bold"),
        text_color=layout.get("title_color", "#22d3ee"),
    ).pack(side="left", padx=(4, 4))

    master = ctk.CTkSwitch(
        head,
        text="",
        font=("Microsoft YaHei", 12),
        width=50,
        command=lambda: callbacks["toggle"](feature_id),
    )
    master.pack(side="right", padx=6)

    ctk.CTkLabel(
        frame,
        text=manifest.get("desc", ""),
        font=("Microsoft YaHei", 12),
        text_color="#a0a0a0",
        wraplength=300 * colspan,
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(4, 6))

    handles = {manifest.get("ui_handles", {}).get("switch", f"{feature_id}_switch"): master}

    def _add_switch(key, label, default):
        var = ctk.BooleanVar(value=bool(config.get(key, default)))

        def _on_change():
            callbacks["set_config"](feature_id, key, bool(var.get()))

        switch = ctk.CTkSwitch(
            frame,
            text=label,
            variable=var,
            font=("Microsoft YaHei", 12),
            command=_on_change,
        )
        switch.pack(anchor="w", padx=12, pady=2)
        handles[f"{feature_id}_{key}_switch"] = switch
        handles[f"{feature_id}_{key}_var"] = var
        return switch

    _add_switch("pacify", "停战（人机不再选敌/开火 + 无敌）", False)
    _add_switch("freeze", "冻结人机行为（人机完全不行动）", False)
    _add_switch("follow", "跟随我（所有人机都朝我走）", False)
    _add_switch("walk", "人机采样（记录 bot 走过哪些边）", False)

    button = ctk.CTkButton(
        frame,
        text="跑一次物理探针",
        font=("Microsoft YaHei", 14, "bold"),
        height=34,
        fg_color="#0e7490",
        hover_color="#155e75",
        command=lambda: callbacks["action"](feature_id, "runprobe"),
    )
    button.pack(fill="x", padx=12, pady=(8, 10))
    handles[f"{feature_id}_runprobe"] = button
    return handles
