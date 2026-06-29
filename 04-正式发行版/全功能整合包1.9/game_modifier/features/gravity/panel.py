import customtkinter as ctk

GRAVITY_MODE_VALUES = ("\u4ec5\u81ea\u5df1", "\u5168\u90e8\u73a9\u5bb6")
GRAVITY_MODE_CONFIG = {
    GRAVITY_MODE_VALUES[0]: "player_only",
    GRAVITY_MODE_VALUES[1]: "all",
}


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
    frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0")).pack(side="left", padx=4)
    switch = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: callbacks["toggle"](feature_id))
    switch.pack(side="right", padx=12)

    slider_frame = ctk.CTkFrame(frame, fg_color="transparent")
    slider_frame.pack(fill="x", padx=8, pady=(4, 0))
    ctk.CTkLabel(slider_frame, text="\u91cd\u529b:", font=("Microsoft YaHei", 11), text_color="#e0e0e0").pack(side="left", padx=(4, 2))
    gravity_var = ctk.DoubleVar(value=1.0)
    def on_gravity(value):
        numeric = round(float(value), 1)
        gravity_label.configure(text=f"{numeric:.1f}")
        callbacks["set_config"](feature_id, "gravity", numeric)

    gravity_slider = ctk.CTkSlider(slider_frame, from_=0.0, to=1.0, variable=gravity_var, number_of_steps=10, command=on_gravity, width=100)
    gravity_slider.pack(side="left", padx=2)
    gravity_label = ctk.CTkLabel(slider_frame, text="1.0", font=("Microsoft YaHei", 11), text_color="#e0e0e0", width=28)
    gravity_label.pack(side="left", padx=(2, 6))
    ctk.CTkLabel(slider_frame, text="\u8df3\u8dc3:", font=("Microsoft YaHei", 11), text_color="#e0e0e0").pack(side="left", padx=(4, 2))
    jump_var = ctk.DoubleVar(value=1.0)
    def on_jump(value):
        numeric = round(float(value), 1)
        jump_label.configure(text=f"{numeric:.1f}")
        callbacks["set_config"](feature_id, "jump", numeric)

    jump_slider = ctk.CTkSlider(slider_frame, from_=1.0, to=5.0, variable=jump_var, number_of_steps=8, command=on_jump, width=100)
    jump_slider.pack(side="left", padx=2)
    jump_label = ctk.CTkLabel(slider_frame, text="1.0", font=("Microsoft YaHei", 11), text_color="#e0e0e0", width=28)
    jump_label.pack(side="left", padx=2)

    mode_frame = ctk.CTkFrame(frame, fg_color="transparent")
    mode_frame.pack(fill="x", padx=8, pady=(2, 2))
    ctk.CTkLabel(mode_frame, text="\u751f\u6548\u8303\u56f4:", font=("Microsoft YaHei", 11), text_color="#e0e0e0").pack(side="left", padx=(4, 4))
    mode_var = ctk.StringVar(value=GRAVITY_MODE_VALUES[0])
    mode_combo = ctk.CTkComboBox(
        mode_frame,
        values=list(GRAVITY_MODE_VALUES),
        variable=mode_var,
        font=("Microsoft YaHei", 12),
        height=30,
        width=120,
        state="readonly",
        command=lambda value: callbacks["set_config"](
            feature_id,
            "mode",
            GRAVITY_MODE_CONFIG.get(value, "all"),
        ),
    )
    mode_combo.pack(side="left", padx=4)
    ctk.CTkLabel(frame, font=("Microsoft YaHei", 15), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=5, pady=5)
    return {
        "gravity_switch": switch,
        "gravity_var": gravity_var,
        "gravity_slider": gravity_slider,
        "gravity_label": gravity_label,
        "jump_var": jump_var,
        "jump_slider": jump_slider,
        "jump_label": jump_label,
        "gravity_mode_var": mode_var,
        "gravity_mode_combo": mode_combo,
    }
