import customtkinter as ctk


class _SyncedSliderVar:
    def __init__(self, var, value_label, sync_guard):
        self._var = var
        self._value_label = value_label
        self._sync_guard = sync_guard
        self._syncing = False

    def get(self):
        return self._var.get()

    def set(self, value):
        self._syncing = True
        self._sync_guard["value"] = True
        try:
            numeric = float(value)
            self._var.set(numeric)
            self._value_label.configure(text=f"{numeric:.2f}")
        finally:
            self._sync_guard["value"] = False
            self._syncing = False


def _control(manifest, key):
    for item in manifest.get("controls", []):
        if item.get("key") == key:
            return item
    return {}


def _steps(control):
    minimum = float(control.get("min", 0.0))
    maximum = float(control.get("max", 1.0))
    step = float(control.get("step", 0.1))
    return int(round((maximum - minimum) / step)) if step > 0 else 100


def _slider(parent, feature_id, control, callbacks):
    key = control["key"]
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", padx=8, pady=(4, 8))
    frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        frame,
        text=control.get("label", key),
        font=("Microsoft YaHei", 12),
        text_color="#e0e0e0",
        anchor="w",
    ).grid(row=0, column=0, sticky="w", padx=4)

    value_label = ctk.CTkLabel(
        frame,
        text=f"{float(control.get('default', 0.0)):.2f}",
        font=("Microsoft YaHei", 11),
        text_color="#e0e0e0",
        width=28,
    )
    value_label.grid(row=0, column=1, sticky="e", padx=4)

    var = ctk.DoubleVar(value=float(control.get("default", 0.0)))
    sync_guard = {"value": False}

    def on_change(value):
        if sync_guard["value"]:
            value_label.configure(text=f"{float(value):.2f}")
            return
        numeric = round(float(value), 2)
        value_label.configure(text=f"{numeric:.2f}")
        callbacks["set_config"](feature_id, key, numeric)

    slider = ctk.CTkSlider(
        frame,
        from_=float(control.get("min", 0.0)),
        to=float(control.get("max", 1.0)),
        number_of_steps=_steps(control),
        variable=var,
        command=on_change,
    )
    slider.grid(row=1, column=0, columnspan=2, sticky="ew", padx=4, pady=(2, 4))
    return _SyncedSliderVar(var, value_label, sync_guard), slider, value_label


def build_card(scroll, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})
    switch_control = next(
        (item for item in manifest.get("controls", []) if item.get("type") == "switch"),
        {},
    )
    distance_control = _control(manifest, "distance")
    pivot_control = _control(manifest, "pivotHeight")
    rowspan = int(manifest.get("layout", {}).get("rowspan", 1))

    frame = ctk.CTkFrame(
        scroll,
        corner_radius=6,
        fg_color="transparent",
        border_width=1,
        border_color="#4b5563",
    )
    sticky = "nsew" if rowspan > 1 else "ew"
    frame.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan, sticky=sticky, padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))

    ctk.CTkLabel(
        top,
        text=manifest["display_name"],
        font=("Microsoft YaHei", 15, "bold"),
        text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0"),
    ).pack(side="left", padx=4)

    switch = ctk.CTkSwitch(
        top,
        text=switch_control.get("label", "开启 / 关闭第三人称"),
        font=("Microsoft YaHei", 12),
        width=50,
        command=lambda: callbacks["toggle"](feature_id),
    )
    switch.pack(side="right", padx=6)

    ctk.CTkLabel(
        frame,
        text=manifest.get("desc", ""),
        text_color="#a0a0a0",
        font=("Microsoft YaHei", 12),
        wraplength=280,
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(4, 8))

    distance_var, distance_slider, distance_label = _slider(
        frame,
        feature_id,
        distance_control,
        callbacks,
    )
    pivot_var, pivot_slider, pivot_label = _slider(
        frame,
        feature_id,
        pivot_control,
        callbacks,
    )

    return {
        handles.get("switch", "third_person_camera_switch"): switch,
        handles.get("distance_var", "third_person_camera_distance_var"): distance_var,
        handles.get("distance_slider", "third_person_camera_distance_slider"): distance_slider,
        handles.get("distance_label", "third_person_camera_distance_label"): distance_label,
        handles.get("pivotHeight_var", "third_person_camera_pivot_height_var"): pivot_var,
        handles.get("pivotHeight_slider", "third_person_camera_pivot_height_slider"): pivot_slider,
        handles.get("pivotHeight_label", "third_person_camera_pivot_height_label"): pivot_label,
    }
