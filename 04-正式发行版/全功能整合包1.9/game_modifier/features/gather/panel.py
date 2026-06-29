import customtkinter as ctk


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0")).pack(side="left", padx=4)
    switch = ctk.CTkSwitch(top, text="\u542f\u7528\u8ffd\u8e2a", font=("Microsoft YaHei", 12), width=50, command=lambda: callbacks["toggle"](feature_id))
    switch.pack(side="right", padx=12)
    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(fill="x", padx=8, pady=(2, 2))
    button = ctk.CTkButton(
        btn_frame,
        text="\U0001f4cd \u4e00\u952e\u805a\u602a",
        font=("Microsoft YaHei", 14, "bold"),
        height=45,
        command=lambda: callbacks["action"](feature_id, "gather"),
        fg_color="#b45309",
        hover_color="#92400e",
    )
    button.pack(fill="x", padx=4, pady=4)
    ctk.CTkLabel(frame, font=("Microsoft YaHei", 15), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(2, 6))
    handles = manifest.get("ui_handles", {})
    return {handles.get("switch", "gather_switch"): switch, handles.get("button", "gather_btn"): button}
