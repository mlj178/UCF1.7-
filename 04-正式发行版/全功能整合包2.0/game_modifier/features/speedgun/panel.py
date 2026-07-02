import customtkinter as ctk


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    lines = manifest.get("ui_text", {}).get(
        "lines",
        [
            "\u2022 \u5c04\u901f 10 \u500d\u52a0\u901f",
            "\u2022 \u8fde\u72d9\uff1a\u534a\u81ea\u52a8 \u2192 \u5168\u81ea\u52a8\uff0c\u72d9\u51fb\u955c\u5e38\u5f00",
            "\u2022 \u540e\u5750\u529b\u6e05\u96f6 + \u6269\u6563\u5f52\u96f6",
        ],
    )
    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="#3a3a1a", border_width=1, border_color="#555555")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0")).pack(side="left", padx=4)
    switch = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: callbacks["toggle"](feature_id))
    switch.pack(side="right", padx=12)
    ctk.CTkLabel(
        frame,
        font=("Microsoft YaHei", 12),
        text="\n".join(lines),
        text_color="#a0a0a0",
        wraplength=280,
        justify="left",
        anchor="w",
    ).pack(fill="x", expand=False, padx=8, pady=(2, 6))
    return {manifest.get("ui_handles", {}).get("switch", "speedgun_switch"): switch}
