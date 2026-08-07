import customtkinter as ctk


MODE_OPTIONS = {
    "团队竞技": "team_death",
    "刀战": "special",
    "生化4（普通生化）": "nano4",
    "生化6（剑客模式）": "nano6",
    "生化4终结者（多人生化）": "nano4_terminator",
    "狙击战": "sniper",
    "手枪战": "handgun",
}


def _current_config(manifest):
    return dict(manifest.get("config") or {})


def build_card(scroll, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    config = _current_config(manifest)
    handles = {}

    frame, switch, _label = card_builder.make_feature_card(
        scroll,
        row,
        col,
        colspan,
        manifest,
    )
    switch.configure(command=lambda: callbacks["toggle"](feature_id))
    handles[manifest.get("ui_handles", {}).get("switch", f"{feature_id}_switch")] = switch

    body = ctk.CTkFrame(frame, fg_color="transparent")
    body.pack(fill="x", padx=10, pady=(0, 8))
    body.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(
        body,
        text="目标模式",
        font=("Microsoft YaHei", 12),
        text_color="#d1d5db",
        width=72,
        anchor="w",
    ).grid(row=0, column=0, padx=(0, 8), pady=3, sticky="w")

    value_by_label = MODE_OPTIONS
    label_by_value = {value: label for label, value in value_by_label.items()}
    initial_value = config.get("mode_key", "team_death")
    mode_var = ctk.StringVar(value=label_by_value.get(initial_value, "团队竞技"))

    def on_mode_changed(label):
        callbacks["set_config"](feature_id, "mode_key", value_by_label.get(label, "team_death"))

    mode_menu = ctk.CTkComboBox(
        body,
        values=list(value_by_label.keys()),
        variable=mode_var,
        command=on_mode_changed,
        width=220,
        state="readonly",
    )
    mode_menu.grid(row=0, column=1, padx=(0, 8), pady=3, sticky="w")
    handles[manifest.get("ui_handles", {}).get("mode_key_select", f"{feature_id}_mode_key_select")] = mode_menu

    return handles
