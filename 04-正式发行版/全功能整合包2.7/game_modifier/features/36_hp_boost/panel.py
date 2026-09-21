import threading

import customtkinter as ctk


class _HpAmountLabel(ctk.CTkLabel):
    def configure(self, require_redraw=False, **kwargs):
        # 中心 UI 恢复配置时按 .1f 格式化滑块文本；此处统一为整数。
        if "text" in kwargs:
            try:
                value = float(str(kwargs["text"]).removesuffix("").removesuffix("x").strip())
                kwargs["text"] = f"{int(round(value))}"
            except (TypeError, ValueError):
                pass
        return super().configure(require_redraw=require_redraw, **kwargs)


def _control(manifest, control_type=None, key=None):
    for item in manifest.get("controls", []):
        if control_type and item.get("type") != control_type:
            continue
        if key and item.get("key") != key:
            continue
        return item
    return {}


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})
    lines = manifest.get("ui_text", {}).get("lines", [manifest.get("desc", "")])

    switch_control = _control(manifest, "switch")
    slider_control = _control(manifest, "slider", "add_amount")
    button_control = _control(manifest, "button")

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
        text=manifest.get("display_name", ""),
        font=("Microsoft YaHei", 15, "bold"),
        text_color=manifest.get("layout", {}).get("title_color", "#4ade80"),
    ).pack(side="left", padx=4)

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

    # 单次加血量滑块（1-100 整数）
    slider_row = ctk.CTkFrame(frame, fg_color="transparent")
    slider_row.pack(fill="x", padx=12, pady=(2, 6))
    slider_row.grid_columnconfigure(1, weight=1)

    minimum = int(slider_control.get("min", 1))
    maximum = int(slider_control.get("max", 100))
    default_value = int(slider_control.get("default", 10))

    ctk.CTkLabel(
        slider_row,
        text=slider_control.get("label", "单次加血量"),
        font=("Microsoft YaHei", 12),
        text_color="#e0e0e0",
    ).grid(row=0, column=0, sticky="w", padx=(0, 8))

    value_label = _HpAmountLabel(
        slider_row,
        text=f"{default_value}",
        font=("Microsoft YaHei", 11),
        text_color="#e0e0e0",
        width=40,
    )
    value_label.grid(row=0, column=2, sticky="e", padx=(8, 0))

    var = ctk.IntVar(value=default_value)

    def on_change(value):
        numeric = int(round(float(value)))
        var.set(numeric)
        value_label.configure(text=f"{numeric}")
        callbacks["set_config"](feature_id, "add_amount", numeric)

    slider = ctk.CTkSlider(
        slider_row,
        from_=minimum,
        to=maximum,
        number_of_steps=maximum - minimum,
        variable=var,
        command=on_change,
    )
    slider.grid(row=0, column=1, sticky="ew", padx=4)

    # 加血按钮：后台线程调 RPC，避免阻塞 UI 线程
    def run_add_hp():
        log = callbacks["log"]
        if not callbacks["is_connected"]():
            log("⚠ 尚未连接到游戏，请先连接游戏")
            return
        if not callbacks["is_enabled"](feature_id):
            log("⚠ 请先打开「增加血量」开关再加血")
            return

        button.configure(state="disabled", text="加血中...")

        def worker():
            try:
                result = callbacks["action"](feature_id, button_control.get("action", "addhp"))
                if isinstance(result, dict):
                    last_result = result.get("last_result", "")
                    heal_count = result.get("heal_count", 0)
                    if last_result == "pending":
                        log("❤ 已触发加血，等待生效")
                    elif heal_count:
                        log(f"❤ 已加血，累计 {heal_count} 次")
                    else:
                        log(f"❤ 加血结果: {last_result or '已触发'}")
                else:
                    log("❤ 已触发加血")
            except Exception as exc:
                log(f"❌ 加血异常: {exc}")
            finally:
                button.after(0, lambda: button.configure(state="normal", text=button_control.get("label", "加血一次")))

        threading.Thread(target=worker, daemon=True).start()

    button = ctk.CTkButton(
        frame,
        text=button_control.get("label", "加血一次"),
        font=("Microsoft YaHei", 14, "bold"),
        height=40,
        command=run_add_hp,
        fg_color="#16a34a",
        hover_color="#15803d",
    )
    button.pack(fill="x", padx=12, pady=(0, 10))

    return {
        handles.get("switch", "hp_boost_switch"): switch,
        handles.get("add_amount_var", "hp_boost_add_amount_var"): var,
        handles.get("add_amount_label", "hp_boost_add_amount_label"): value_label,
        handles.get("button", "hp_boost_add_btn"): button,
    }