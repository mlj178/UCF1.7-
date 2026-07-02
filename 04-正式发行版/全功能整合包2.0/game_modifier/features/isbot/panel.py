import customtkinter as ctk

import features.isbot.state as isbot_state


_status_label = None


def get_status_label():
    return isbot_state.status_label or _status_label


def _status_props(state):
    if state == "awaiting_room":
        return "状态: 已预约，等待进房", "#f39c12"
    if state == "awaiting_reenter":
        return "状态: 已预约，等待重进房间生效", "#f39c12"
    if state == "active":
        return "状态: 已生效", "#2ecc71"
    return "状态: 已关闭", "#888888"


def apply_status_label(label, state):
    text, color = _status_props(state)
    label.configure(text=text, text_color=color)


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    global _status_label
    feature_id = manifest["feature_id"]
    status_control = next(
        (item for item in manifest.get("controls", []) if item.get("type") == "status"),
        {},
    )
    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
    top = ctk.CTkFrame(frame, fg_color="transparent")
    top.pack(fill="x", padx=8, pady=(6, 0))
    ctk.CTkLabel(top, text=f"{manifest['icon']} {manifest['display_name']}", font=("Microsoft YaHei", 15, "bold"), text_color=manifest.get("layout", {}).get("title_color", "#e0e0e0")).pack(side="left", padx=4)

    def toggle_isbot():
        result = callbacks["toggle"](feature_id)
        if result is False:
            apply_status_label(status, isbot_state.state)
            return
        isbot_state.state = "awaiting_room" if switch.get() else "off"
        apply_status_label(status, isbot_state.state)

    switch = ctk.CTkSwitch(top, text="", font=("Microsoft YaHei", 12), width=50, command=toggle_isbot)
    switch.pack(side="right", padx=6)
    initial_text, initial_color = _status_props(isbot_state.state)
    status = ctk.CTkLabel(
        frame,
        text=initial_text or status_control.get("label", "\u72b6\u6001: \u5df2\u5173\u95ed"),
        font=("Microsoft YaHei", 11),
        text_color=initial_color,
        anchor="w",
    )
    _status_label = status
    isbot_state.status_label = status
    apply_status_label(status, isbot_state.state)
    status.pack(fill="x", padx=12, pady=(2, 0))
    placeholder = ctk.CTkFrame(frame, fg_color="transparent", height=1)
    placeholder.pack(fill="x", padx=8, pady=(0, 0))
    placeholder.pack_propagate(False)
    ctk.CTkLabel(frame, font=("Microsoft YaHei", 15), text=manifest["desc"], text_color="#a0a0a0", wraplength=280, justify="left", anchor="w").pack(fill="x", expand=False, padx=8, pady=(0, 4))
    handles = manifest.get("ui_handles", {})
    return {handles.get("switch", "isbot_switch"): switch, handles.get("status_label", "isbot_status_label"): status}
