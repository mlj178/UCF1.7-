import threading

import customtkinter as ctk


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    button_control = next(
        (item for item in manifest.get("controls", []) if item.get("type") == "button"),
        {},
    )
    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0")).pack(side="left", padx=4)
    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(fill="x", padx=8, pady=(2, 2))
    def run_skip_round():
        log = callbacks["log"]
        if not callbacks["is_connected"]():
            log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return

        log("⏭️ 正在跳过当前回合...")
        button.configure(state="disabled", text="⏳ 跳转中...")

        def worker():
            try:
                result = callbacks["action"](feature_id, button_control.get("action", "skip_round"))
                if result:
                    if result.get("ok", False):
                        log("✅ 回合跳过成功！")
                    else:
                        reason = result.get("reason", "未知错误")
                        if reason == "no_instance":
                            log("⚠ 未能获取到游戏回合实例，请确保已进入游戏模式")
                        elif reason == "already_zero":
                            log("⚠ 回合时间已为 0:00，无需跳过")
                        else:
                            log(f"❌ 跳过失败: {reason}")
            except Exception as exc:
                log(f"❌ 跳过异常: {exc}")
            finally:
                button.after(0, lambda: button.configure(state="normal", text="▶ 跳过当前回合"))

        threading.Thread(target=worker, daemon=True).start()

    button = ctk.CTkButton(
        btn_frame,
        text=button_control.get("label", "\u25b6 \u7b2c\u4e00\u6b21\u8df3\u8fc7\u9700\u8981\u70b9\u51fb\u4e24\u6b21"),
        font=("Microsoft YaHei", 14, "bold"),
        height=45,
        command=run_skip_round,
        fg_color="#b45309",
        hover_color="#92400e",
    )
    button.pack(fill="x", padx=4, pady=4)
    ctk.CTkLabel(frame, font=("Microsoft YaHei", 15), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(2, 6))
    return {manifest.get("ui_handles", {}).get("button", "skip_round_btn"): button}
