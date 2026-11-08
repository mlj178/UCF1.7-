import customtkinter as ctk


def _slider_control(manifest):
    for control in manifest.get("controls", []):
        if control.get("type") == "slider":
            return control
    return {}


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})

    slider_control = _slider_control(manifest)
    slider_key = slider_control.get("key", "multiplier")
    slider_min = float(slider_control.get("min", 1.0))
    slider_max = float(slider_control.get("max", 5.0))
    slider_step = float(slider_control.get("step", 0.1)) or 0.1
    slider_default = float(slider_control.get("default", 4.0))
    slider_suffix = slider_control.get("suffix", "x")
    slider_steps = max(1, int(round((slider_max - slider_min) / slider_step)))

    frame = ctk.CTkFrame(
        parent,
        corner_radius=6,
        fg_color="transparent",
        border_width=1,
        border_color="#4b5563",
    )
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

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
        text="",
        font=("Microsoft YaHei", 12),
        width=50,
        command=lambda: callbacks["toggle"](feature_id),
    )
    switch.pack(side="right", padx=6)

    # 倍率滑块：拖动即时下发到脚本（set_config -> RPC setConfig），无需重开开关
    slider_row = ctk.CTkFrame(frame, fg_color="transparent")
    slider_row.pack(fill="x", padx=10, pady=(2, 0))

    multiplier_var = ctk.DoubleVar(value=slider_default)
    multiplier_label = ctk.CTkLabel(
        slider_row,
        text=f"{slider_default:.1f}{slider_suffix}",
        font=("Microsoft YaHei", 12, "bold"),
        text_color="#D4AF37",
        width=42,
        anchor="e",
    )

    sent = {"value": round(slider_default, 1)}

    def on_slide(value):
        current = round(float(value), 1)
        if abs(current - sent["value"]) < 0.0001:
            return
        sent["value"] = current
        try:
            callbacks["set_config"](feature_id, slider_key, current)
        except Exception:
            pass

    slider = ctk.CTkSlider(
        slider_row,
        from_=slider_min,
        to=slider_max,
        number_of_steps=slider_steps,
        variable=multiplier_var,
        command=on_slide,
        width=150,
    )
    slider.pack(side="left", padx=(2, 6))
    multiplier_label.pack(side="left")

    def sync_label(*_args):
        try:
            multiplier_label.configure(text=f"{multiplier_var.get():.1f}{slider_suffix}")
        except Exception:
            pass

    # 配置回填（启动/切换页签）时同步刷新数值文字
    multiplier_var.trace_add("write", sync_label)

    # 与左侧无限子弹卡片对齐：预留同高占位行
    spacer = ctk.CTkFrame(frame, fg_color="transparent", height=28)
    spacer.pack(fill="x", padx=10, pady=(2, 0))
    spacer.pack_propagate(False)

    ctk.CTkLabel(
        frame,
        font=("Microsoft YaHei", 12),
        text=manifest["desc"],
        text_color="#a0a0a0",
        wraplength=280 * colspan,
        justify="left",
        anchor="w",
    ).pack(fill="x", expand=False, padx=10, pady=(4, 8))

    return {
        handles.get("switch", "ammoplus_switch"): switch,
        handles.get("slider_var", "ammoplus_multiplier_var"): multiplier_var,
        handles.get("slider_label", "ammoplus_multiplier_label"): multiplier_label,
    }
