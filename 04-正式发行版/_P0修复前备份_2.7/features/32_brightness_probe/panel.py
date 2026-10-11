import customtkinter as ctk


def _control(manifest, key):
    return next((item for item in manifest.get("controls", []) if item.get("key") == key), {})


class _SyncedVar:
    def __init__(self, variable, label, formatter):
        self.variable = variable
        self.label = label
        self.formatter = formatter
        self.syncing = False

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.syncing = True
        try:
            numeric = float(value)
            self.variable.set(numeric)
            self.label.configure(text=self.formatter(numeric))
        finally:
            self.syncing = False


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})
    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="transparent", border_width=1, border_color="#4b5563")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
    frame.grid_columnconfigure(1, weight=1)

    title = ctk.CTkFrame(frame, fg_color="transparent")
    title.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(title, text=manifest.get("display_name", ""), font=("Microsoft YaHei", 15, "bold"), text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0")).pack(side="left", padx=4)
    variables = {}
    for index, key in enumerate(("exposure", "contrast", "saturation", "gamma", "gain")):
        control = _control(manifest, key)
        row_frame = ctk.CTkFrame(frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=12, pady=2)
        row_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(row_frame, text=control.get("label", key), width=110, anchor="w", font=("Microsoft YaHei", 12), text_color="#e0e0e0").grid(row=0, column=0, sticky="w")
        value_label = ctk.CTkLabel(row_frame, text="", width=28, anchor="e", font=("Microsoft YaHei", 11), text_color="#e0e0e0")
        value_label.grid(row=0, column=2, padx=(8, 0))
        formatter = (lambda value: f"{value:.0f}") if control.get("format") == "{:.0f}" else (lambda value: f"{value:.2f}")
        variable = ctk.DoubleVar(value=float(control.get("default", 0.0)))
        synced = _SyncedVar(variable, value_label, formatter)
        synced.set(variable.get())

        def on_change(value, key=key, control=control, synced=synced, value_label=value_label, formatter=formatter):
            numeric = round(float(value), 2 if float(control.get("step", 0.1)) < 0.1 else 1)
            value_label.configure(text=formatter(numeric))
            if not synced.syncing:
                callbacks["action"](feature_id, "setconfig", {key: numeric})

        slider = ctk.CTkSlider(row_frame, from_=float(control["min"]), to=float(control["max"]), number_of_steps=int(round((float(control["max"]) - float(control["min"])) / float(control["step"]))), variable=variable, command=on_change)
        slider.grid(row=0, column=1, sticky="ew", padx=4)
        variables[key] = (synced, slider)

    actions = ctk.CTkFrame(frame, fg_color="transparent")
    actions.pack(fill="x", padx=12, pady=(2, 8))
    actions.grid_columnconfigure((0, 1), weight=1, uniform="brightness_actions")

    def apply():
        callbacks["action"](feature_id, "enable")
        callbacks["action"](feature_id, "setconfig", {key: float(item[0].get()) for key, item in variables.items()})
        callbacks["action"](feature_id, "applybrightness", float(variables["exposure"][0].get()))

    def reset():
        callbacks["action"](feature_id, "resetbrightness")

    ctk.CTkButton(actions, text="应用参数", command=apply, fg_color="#16a34a", hover_color="#15803d").grid(row=0, column=0, sticky="ew", padx=(0, 4))
    ctk.CTkButton(actions, text="恢复游戏初始值", command=reset, fg_color="#b45309", hover_color="#92400e").grid(row=0, column=1, sticky="ew", padx=(4, 0))
    return {
        handles.get("exposure_var", "brightness_probe_exposure_var"): variables["exposure"][0],
        handles.get("contrast_var", "brightness_probe_contrast_var"): variables["contrast"][0],
        handles.get("saturation_var", "brightness_probe_saturation_var"): variables["saturation"][0],
        handles.get("gamma_var", "brightness_probe_gamma_var"): variables["gamma"][0],
        handles.get("gain_var", "brightness_probe_gain_var"): variables["gain"][0],
    }
