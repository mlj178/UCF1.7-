import customtkinter as ctk


class _SyncedSliderVar:
    def __init__(self, var, value_label, sync_guard):
        self._var = var
        self._value_label = value_label
        self._sync_guard = sync_guard

    def get(self):
        return self._var.get()

    def set(self, value):
        self._sync_guard["value"] = True
        try:
            numeric = float(value)
            self._var.set(numeric)
            self._value_label.configure(text=f"{numeric:.1f}")
        finally:
            self._sync_guard["value"] = False


def _control(manifest, key):
    for item in manifest.get("controls", []):
        if item.get("key") == key:
            return item
    return {}


def _steps(control):
    minimum = float(control.get("min", 0.0))
    maximum = float(control.get("max", 1.0))
    step = float(control.get("step", 1.0))
    return int(round((maximum - minimum) / step)) if step > 0 else 100


def _speed_slider(parent, feature_id, control, callbacks):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", padx=8, pady=(4, 8))
    frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        frame,
        text=control.get("label", "移动速度"),
        font=("Microsoft YaHei", 12),
        text_color="#e0e0e0",
        anchor="w",
    ).grid(row=0, column=0, sticky="w", padx=4)

    value_label = ctk.CTkLabel(
        frame,
        text=f"{float(control.get('default', 10.0)):.1f}",
        font=("Microsoft YaHei", 11),
        text_color="#e0e0e0",
        width=28,
    )
    value_label.grid(row=0, column=1, sticky="e", padx=4)

    var = ctk.DoubleVar(value=float(control.get("default", 10.0)))
    sync_guard = {"value": False}

    def on_change(value):
        if sync_guard["value"]:
            value_label.configure(text=f"{float(value):.1f}")
            return
        numeric = round(float(value), 1)
        value_label.configure(text=f"{numeric:.1f}")
        callbacks["set_config"](feature_id, "moveSpeed", numeric)

    slider = ctk.CTkSlider(
        frame,
        from_=float(control.get("min", 1.0)),
        to=float(control.get("max", 80.0)),
        number_of_steps=_steps(control),
        variable=var,
        command=on_change,
    )
    slider.grid(row=1, column=0, columnspan=2, sticky="ew", padx=4, pady=(2, 4))
    return _SyncedSliderVar(var, value_label, sync_guard), slider, value_label


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})
    lines = manifest.get("ui_text", {}).get("lines", [manifest.get("desc", "")])
    switch_control = next((item for item in manifest.get("controls", []) if item.get("type") == "switch"), {})
    speed_control = _control(manifest, "moveSpeed")

    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="transparent", border_width=1, border_color="#4b5563")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))

    title_name_label = ctk.CTkLabel(
        top,
        text=manifest["display_name"],
        font=("Microsoft YaHei", 15, "bold"),
        text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0"),
    )
    title_name_label.pack(side="left", padx=(4, 4))

    switch = ctk.CTkSwitch(
        top,
        text=switch_control.get("label", ""),
        font=("Microsoft YaHei", 12),
        width=50,
        command=lambda: callbacks["toggle"](feature_id),
    )
    switch.pack(side="right", padx=6)

    ctk.CTkLabel(
        frame,
        text="\n".join(lines),
        text_color="#a0a0a0",
        font=("Microsoft YaHei", 12),
        wraplength=280 * colspan,
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(4, 8))

    speed_var, speed_slider, speed_label = _speed_slider(frame, feature_id, speed_control, callbacks)

    return {
        handles.get("switch", "free_camera_switch"): switch,
        handles.get("moveSpeed_var", "free_camera_move_speed_var"): speed_var,
        handles.get("moveSpeed_slider", "free_camera_move_speed_slider"): speed_slider,
        handles.get("moveSpeed_label", "free_camera_move_speed_label"): speed_label,
    }
