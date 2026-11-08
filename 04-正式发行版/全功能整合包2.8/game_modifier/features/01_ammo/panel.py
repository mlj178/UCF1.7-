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


def _scope_maps(control):
    values = control.get("values", [])
    labels = _display_values(control)
    value_by_label = {label: value for value, label in zip(values, labels)}
    label_by_value = {value: label for label, value in value_by_label.items()}
    return value_by_label, label_by_value


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    ui_handles = manifest.get("ui_handles", {})
    config = dict(manifest.get("config") or {})

    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="transparent", border_width=1, border_color="#4b5563")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(
        top,
        text=manifest["display_name"],
        font=("Microsoft YaHei", 15, "bold"),
        text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0"),
    ).pack(side="left", padx=4)
    master = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=lambda: callbacks["toggle"](feature_id))
    master.pack(side="right", padx=6)
    ctk.CTkLabel(top, text="总开关", font=("Microsoft YaHei", 11), text_color="#a0a0a0").pack(side="right", padx=(0, 2))

    ctk.CTkLabel(
        frame,
        font=("Microsoft YaHei", 12),
        text=manifest["desc"],
        text_color="#a0a0a0",
        wraplength=300 * colspan,
        justify="left",
        anchor="w",
    ).pack(fill="x", expand=False, padx=10, pady=(4, 4))

    state = {}
    for prefix, title, color in (
        ("infinite_bullet", "无限子弹", "#E5B73B"),
        ("infinite_ammo", "无限弹药", "#4ECDC4"),
    ):
        enabled_key = prefix + "_enabled"
        scope_key = prefix + "_scope"
        enabled_control = _control(manifest, "switch", enabled_key)
        scope_control = _control(manifest, "combo", scope_key)
        scope_labels = _display_values(scope_control)
        value_by_label, label_by_value = _scope_maps(scope_control)
        default_enabled = bool(config.get(enabled_key, enabled_control.get("default", False)))
        default_scope = config.get(scope_key, scope_control.get("default"))
        default_label = label_by_value.get(default_scope, scope_labels[0] if scope_labels else "")

        row_frame = ctk.CTkFrame(frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=10, pady=(6, 0))

        ctk.CTkLabel(
            row_frame,
            text=title,
            font=("Microsoft YaHei", 12, "bold"),
            text_color=color,
            width=64,
            anchor="w",
        ).pack(side="left")

        enabled_var = ctk.BooleanVar(value=default_enabled)
        switch = ctk.CTkSwitch(
            row_frame,
            text="",
            width=40,
            variable=enabled_var,
            command=lambda fid=feature_id, key=enabled_key, var=enabled_var: callbacks["set_config"](
                fid, key, bool(var.get())
            ),
        )
        switch.pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            row_frame,
            text="范围",
            font=("Microsoft YaHei", 11),
            text_color="#a0a0a0",
        ).pack(side="left", padx=(0, 4))

        scope_var = ctk.StringVar(value=default_label)
        combo = ctk.CTkComboBox(
            row_frame,
            values=scope_labels,
            variable=scope_var,
            font=("Microsoft YaHei", 11),
            dropdown_font=("Microsoft YaHei", 11),
            height=26,
            width=132,
            state="readonly",
            command=lambda label, fid=feature_id, key=scope_key, mapping=value_by_label: callbacks["set_config"](
                fid, key, mapping.get(label, label)
            ),
        )
        combo.pack(side="left")

        state[prefix] = {
            "enabled_var": enabled_var,
            "switch": switch,
            "scope_var": scope_var,
            "combo": combo,
        }

    ctk.CTkLabel(
        frame,
        text="无限弹药覆盖普通枪械与 RPG/AT4（刀/手雷除外）；两种模式可同时开启，同时开启时以无限子弹为准。",
        font=("Microsoft YaHei", 10),
        text_color="#7d8590",
        wraplength=300 * colspan,
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(6, 8))

    result = {
        ui_handles.get("switch", "ammo_switch"): master,
        "ammo_scope_var": state["infinite_bullet"]["scope_var"],
        "ammo_scope_combo": state["infinite_bullet"]["combo"],
    }
    for prefix in ("infinite_bullet", "infinite_ammo"):
        result[f"{prefix}_enabled_var"] = state[prefix]["enabled_var"]
        result[f"{prefix}_enabled_switch"] = state[prefix]["switch"]
        result[f"{prefix}_scope_var"] = state[prefix]["scope_var"]
        result[f"{prefix}_scope_combo"] = state[prefix]["combo"]
    return result