import customtkinter as ctk


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    lines = manifest.get("ui_text", {}).get("lines", [manifest.get("desc", "")])

    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="transparent", border_width=1, border_color="#4b5563")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))

    ctk.CTkLabel(
        top,
        text=f"{manifest['icon']} {manifest['display_name']}",
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
    switch.pack(side="right", padx=12)

    ctk.CTkLabel(
        frame,
        font=("Microsoft YaHei", 12),
        text="\n".join(lines),
        text_color="#cbd5e1",
        wraplength=280,
        justify="left",
        anchor="w",
    ).pack(fill="x", expand=False, padx=10, pady=(4, 8))

    handles = manifest.get("ui_handles", {})
    return {handles.get("switch", "bot_pause_switch"): switch}
