import customtkinter as ctk


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    status_control = next(
        (item for item in manifest.get("controls", []) if item.get("type") == "status"),
        {},
    )
    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0")).pack(side="left", padx=4)
    switch = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: callbacks["toggle"](feature_id))
    switch.pack(side="right", padx=6)
    status = ctk.CTkLabel(frame, text=status_control.get("label", "\u72b6\u6001: \u5df2\u5173\u95ed"), font=("Microsoft YaHei", 11), text_color="#888888", anchor="w")
    status.pack(fill="x", padx=12, pady=(2, 0))
    placeholder = ctk.CTkFrame(frame, fg_color="transparent", height=1)
    placeholder.pack(fill="x", padx=8, pady=(0, 0))
    placeholder.pack_propagate(False)
    ctk.CTkLabel(frame, font=("Microsoft YaHei", 15), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(0, 4))
    handles = manifest.get("ui_handles", {})
    return {handles.get("switch", "isbot_switch"): switch, handles.get("status_label", "isbot_status_label"): status}
