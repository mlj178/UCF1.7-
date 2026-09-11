import customtkinter as ctk


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    handles = manifest.get("ui_handles", {})
    controls = {item.get("action"): item for item in manifest.get("controls", []) if item.get("action")}

    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="transparent", border_width=1, border_color="#4b5563")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))

    ctk.CTkLabel(
        top,
        text=manifest.get("display_name", "直接变身剑客"),
        font=("Microsoft YaHei", 15, "bold"),
        text_color=manifest.get("layout", {}).get("title_color", "#22d3ee"),
    ).pack(side="left", padx=4)

    switch = ctk.CTkSwitch(
        top,
        text=controls.get("enable", {}).get("label", ""),
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

    button_controls = {
        (control.get("payload") or {}).get("action"): control
        for control in manifest.get("controls", [])
        if control.get("type") == "button"
    }

    def run_action(payload_action, button, busy_text):
        if not callbacks["is_connected"]():
            callbacks["log"]("尚未连接到游戏")
            return
        if not callbacks["is_enabled"](feature_id):
            callbacks["log"]("请先打开「直接变身剑客」开关")
            return
        original = button.cget("text")
        button.configure(state="disabled", text=busy_text)
        try:
            callbacks["action"](feature_id, "trigger", {"action": payload_action})
        except Exception as exc:
            callbacks["log"](f"变身异常: {exc}")
        finally:
            button.after(400, lambda: button.configure(state="normal", text=original))

    local_button = ctk.CTkButton(
        frame,
        text=button_controls.get("local_ghostblade", {}).get("label", "本地变身剑客"),
        height=36,
        font=("Microsoft YaHei", 12, "bold"),
        fg_color="#0e7490",
        hover_color="#155e75",
        command=lambda: run_action("local_ghostblade", local_button, "变身中..."),
    )
    local_button.pack(fill="x", padx=12, pady=(2, 4))

    bot_button = ctk.CTkButton(
        frame,
        text=button_controls.get("bot_ghostblade", {}).get("label", "所有 Bot 变剑客"),
        height=36,
        font=("Microsoft YaHei", 12, "bold"),
        fg_color="#1e40af",
        hover_color="#1e3a8a",
        command=lambda: run_action("bot_ghostblade", bot_button, "变身中..."),
    )
    bot_button.pack(fill="x", padx=12, pady=(0, 10))

    return {
        handles.get("switch", "become_ghostblade_switch"): switch,
        handles.get("local_button", "become_ghostblade_local_btn"): local_button,
        handles.get("bot_button", "become_ghostblade_bot_btn"): bot_button,
    }
