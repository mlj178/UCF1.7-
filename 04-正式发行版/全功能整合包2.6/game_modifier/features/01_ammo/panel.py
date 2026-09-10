import customtkinter as ctk


def _control(manifest, control_type, key=None):
    for item in manifest.get("controls", []):
        if item.get("type") != control_type:
            continue
        if key is None or item.get("key") == key:
            return item
    return {}


def _display_values(control):
    mapping = control.get("display_values", {})
    values = control.get("values", [])
    return [mapping.get(value, value) for value in values]


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})
    scope_control = _control(manifest, "combo", "scope")
    scope_labels = _display_values(scope_control)
    scope_by_label = {
        label: value
        for value, label in zip(scope_control.get("values", []), scope_labels)
    }

    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="transparent", border_width=1, border_color="#4b5563")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(top, text=manifest["display_name"], font=("Microsoft YaHei", 15, "bold"), text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0")).pack(side="left", padx=4)
    switch = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: callbacks["toggle"](feature_id))
    switch.pack(side="right", padx=6)

    scope_frame = ctk.CTkFrame(frame, fg_color="transparent")
    scope_frame.pack(fill="x", padx=10, pady=(2, 0))
    ctk.CTkLabel(scope_frame, text=scope_control.get("label", "应用范围:"), font=("Microsoft YaHei", 12), text_color="#c0c0c0").pack(side="left", padx=(0, 6))
    scope_var = ctk.StringVar(value=scope_labels[0] if scope_labels else "")
    scope_combo = ctk.CTkComboBox(
        scope_frame,
        values=scope_labels,
        variable=scope_var,
        font=("Microsoft YaHei", 12),
        dropdown_font=("Microsoft YaHei", 12),
        height=28,
        width=170,
        state="readonly",
        command=lambda value: callbacks["set_config"](
            feature_id,
            scope_control.get("key", "scope"),
            scope_by_label.get(value, value),
        ),
    )
    scope_combo.pack(side="left", padx=2)

    ctk.CTkLabel(frame, font=("Microsoft YaHei", 12), text=manifest["desc"], text_color="#a0a0a0", wraplength=280 * colspan, justify="left", anchor="w").pack(fill="x", expand=False, padx=10, pady=(4, 8))

    return {
        handles.get("switch", "ammo_switch"): switch,
        handles.get("scope_var", "ammo_scope_var"): scope_var,
        handles.get("scope_combo", "ammo_scope_combo"): scope_combo,
    }
