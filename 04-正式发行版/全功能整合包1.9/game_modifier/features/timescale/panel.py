import customtkinter as ctk


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(4, 0))
    ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0")).pack(side="left", padx=4)
    switch = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: callbacks["toggle"](feature_id))
    switch.pack(side="right", padx=6)
    slider_frame = ctk.CTkFrame(frame, fg_color="transparent")
    slider_frame.pack(fill="x", padx=8, pady=(4, 0))
    var = ctk.DoubleVar(value=1.0)
    slider = ctk.CTkSlider(slider_frame, from_=0.1, to=10.0, variable=var, number_of_steps=99, command=callbacks["slider"][feature_id], width=150)
    slider.pack(side="left", padx=4)
    label = ctk.CTkLabel(slider_frame, text="1.0x", font=("Microsoft YaHei", 12), text_color="#e0e0e0", width=50)
    label.pack(side="left")
    ctk.CTkLabel(frame, font=("Microsoft YaHei", 15), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(2, 6))
    handles = manifest.get("ui_handles", {})
    return {
        handles.get("switch", "timescale_switch"): switch,
        handles.get("slider_var", "timescale_var"): var,
        handles.get("slider", "timescale_slider"): slider,
        handles.get("slider_label", "timescale_label"): label,
    }
