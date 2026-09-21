import customtkinter as ctk


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})

    frame = ctk.CTkFrame(
        parent,
        corner_radius=6,
        fg_color="transparent",
        border_width=1,
        border_color="#4b5563",
    )
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(
        top,
        text=manifest["display_name"],
        font=("Microsoft YaHei", 15, "bold"),
        text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0"),
    ).pack(side="left", padx=4)
    switch = ctk.CTkSwitch(
        top,
        text="",
        font=("Microsoft YaHei", 12),
        width=50,
        command=lambda: callbacks["toggle"](feature_id),
    )
    switch.pack(side="right", padx=6)

    # 与左侧无限子弹卡片对齐：预留同高占位行
    spacer = ctk.CTkFrame(frame, fg_color="transparent", height=28)
    spacer.pack(fill="x", padx=10, pady=(2, 0))
    spacer.pack_propagate(False)

    ctk.CTkLabel(
        frame,
        font=("Microsoft YaHei", 12),
        text=manifest["desc"],
        text_color="#a0a0a0",
        wraplength=280 * colspan,
        justify="left",
        anchor="w",
    ).pack(fill="x", expand=False, padx=10, pady=(4, 8))

    return {
        handles.get("switch", "ammoplus_switch"): switch,
    }
