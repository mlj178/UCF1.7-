import threading

import customtkinter as ctk


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    controls = manifest.get("controls", [])
    switch_control = next((item for item in controls if item.get("type") == "switch"), {})
    button_control = next((item for item in controls if item.get("type") == "button"), {})
    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0")).pack(side="left", padx=4)
    switch = ctk.CTkSwitch(top, text=switch_control.get("label", "\u542f\u7528\u8ffd\u8e2a"), font=("Microsoft YaHei", 12), width=50, command=lambda: callbacks["toggle"](feature_id))
    switch.pack(side="right", padx=12)
    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(fill="x", padx=8, pady=(2, 2))
    def run_gather():
        log = callbacks["log"]
        if not callbacks["is_connected"]():
            log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return
        if not callbacks["is_enabled"](feature_id):
            log("⚠ 聚怪功能未启用，请先打开「启用追踪」开关")
            return

        log("📍 正在聚怪（传送所有 Bot 到佣兵出生点）...")
        button.configure(state="disabled", text="⏳ 聚怪中...")

        def worker():
            try:
                result = callbacks["action"](feature_id, button_control.get("action", "gather"))
                if result:
                    if result.get("ok", False):
                        log(f"✅ 聚怪完成! 成功{result.get('bots', 0)} 失败{result.get('fail', 0)}")
                    else:
                        log(f"❌ 聚怪失败: {result.get('msg', '未知错误')}")
            except Exception as exc:
                log(f"❌ 聚怪异常: {exc}")
            finally:
                button.after(0, lambda: button.configure(state="normal", text=button_control.get("label", "📍 一键聚怪")))

        threading.Thread(target=worker, daemon=True).start()

    button = ctk.CTkButton(
        btn_frame,
        text=button_control.get("label", "\U0001f4cd \u4e00\u952e\u805a\u602a"),
        font=("Microsoft YaHei", 14, "bold"),
        height=45,
        command=run_gather,
        fg_color="#b45309",
        hover_color="#92400e",
    )
    button.pack(fill="x", padx=4, pady=4)
    ctk.CTkLabel(frame, font=("Microsoft YaHei", 15), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(2, 6))
    handles = manifest.get("ui_handles", {})
    return {handles.get("switch", "gather_switch"): switch, handles.get("button", "gather_btn"): button}
