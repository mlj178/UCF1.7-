import threading

import customtkinter as ctk

from . import status_monitor


class _CountLabel(ctk.CTkLabel):
    def configure(self, require_redraw=False, **kwargs):
        # 中心 UI 恢复配置时按 .1f 格式化滑块文本；此处统一为整数 + 件。
        if "text" in kwargs:
            try:
                value = float(str(kwargs["text"]).removesuffix("件").removesuffix("x").strip())
                kwargs["text"] = f"{int(round(value))}件"
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

    switch_control = _control(manifest, "switch")
    slider_control = _control(manifest, "slider", "cloth_count")
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
        text_color=manifest.get("layout", {}).get("title_color", "#4ECDC4"),
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
        text=manifest.get("desc", ""),
        text_color="#a0a0a0",
        font=("Microsoft YaHei", 12),
        wraplength=280 * colspan,
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=10, pady=(4, 8))

    # 防化服数量滑块（1-10 整数）
    slider_row = ctk.CTkFrame(frame, fg_color="transparent")
    slider_row.pack(fill="x", padx=12, pady=(2, 6))
    slider_row.grid_columnconfigure(1, weight=1)

    minimum = int(slider_control.get("min", 1))
    maximum = int(slider_control.get("max", 10))
    default_value = int(slider_control.get("default", 10))

    ctk.CTkLabel(
        slider_row,
        text=slider_control.get("label", "每次增加量"),
        font=("Microsoft YaHei", 12),
        text_color="#e0e0e0",
    ).grid(row=0, column=0, sticky="w", padx=(0, 8))

    value_label = _CountLabel(
        slider_row,
        text=f"{default_value}件",
        font=("Microsoft YaHei", 11),
        text_color="#e0e0e0",
        width=40,
    )
    value_label.grid(row=0, column=2, sticky="e", padx=(8, 0))

    var = ctk.IntVar(value=default_value)

    def on_change(value):
        numeric = int(round(float(value)))
        var.set(numeric)
        value_label.configure(text=f"{numeric}件")
        callbacks["set_config"](feature_id, "cloth_count", numeric)

    slider = ctk.CTkSlider(
        slider_row,
        from_=minimum,
        to=maximum,
        number_of_steps=maximum - minimum,
        variable=var,
        command=on_change,
    )
    slider.grid(row=0, column=1, sticky="ew", padx=4)

    # 当前防化服数量（绿色）：status_monitor 连接游戏后每秒刷新
    current_label = ctk.CTkLabel(
        frame,
        text="当前防化服：--",
        font=("Microsoft YaHei", 12, "bold"),
        text_color="#9aa3b2",
        anchor="w",
    )
    current_label.pack(fill="x", padx=12, pady=(2, 6))

    def render_status(result):
        if not isinstance(result, dict):
            current_label.configure(text="当前防化服：--", text_color="#9aa3b2")
            return
        current = result.get("current_cloth_count")
        if current is not None:
            current_label.configure(text=f"当前防化服：{current} 件", text_color="#4ade80")
            return
        # 玩家已捕获但字段未初始化（还没获得过防化服）
        if result.get("player_cached"):
            current_label.configure(text="当前防化服：--（尚未获得）", text_color="#9aa3b2")
            return
        # 缓存最后一次读到的数量（切回合/退房后 localPlayer 暂空）
        last = result.get("last_known_cloth_count")
        if last is not None:
            current_label.configure(text=f"当前防化服：--（上次 {last} 件）", text_color="#9aa3b2")
            return
        current_label.configure(text="当前防化服：--（等待进房）", text_color="#9aa3b2")

    status_monitor.set_renderer(render_status)

    # 应用按钮：后台线程调 RPC，避免阻塞 UI 线程
    def run_apply():
        log = callbacks["log"]
        if not callbacks["is_connected"]():
            log("⚠ 尚未连接到游戏，请先连接游戏")
            return
        if not callbacks["is_enabled"](feature_id):
            log("⚠ 请先打开「增加防化服」开关再应用")
            return

        button.configure(state="disabled", text="应用中...")

        def worker():
            try:
                result = callbacks["action"](feature_id, button_control.get("action", "apply"))
                if isinstance(result, dict) and result.get("pending_apply") is False and \
                        result.get("last_apply_result", "").startswith("added"):
                    detail = result.get("last_apply_result", "")
                    change_text = f"（{detail.split('（', 1)[1]}" if "（" in detail else ""
                    log(f"✅ 防化服已增加 {int(var.get())} 件 {change_text}".rstrip())
                else:
                    log("🛡 已触发防化服增加，等待生效")
            except Exception as exc:
                log(f"❌ 增加防化服异常: {exc}")
            finally:
                button.after(0, lambda: button.configure(state="normal", text=button_control.get("label", "应用防化服")))

        threading.Thread(target=worker, daemon=True).start()

    button = ctk.CTkButton(
        frame,
        text=button_control.get("label", "应用防化服"),
        font=("Microsoft YaHei", 14, "bold"),
        height=40,
        command=run_apply,
        fg_color="#0e7490",
        hover_color="#155e75",
    )
    button.pack(fill="x", padx=12, pady=(0, 10))

    return {
        handles.get("switch", "nano_cloth_switch"): switch,
        handles.get("cloth_count_var", "nano_cloth_cloth_count_var"): var,
        handles.get("cloth_count_slider", "nano_cloth_cloth_count_slider"): slider,
        handles.get("cloth_count_label", "nano_cloth_cloth_count_label"): value_label,
        handles.get("current_label", "nano_cloth_current_label"): current_label,
        handles.get("button", "nano_cloth_apply_btn"): button,
    }