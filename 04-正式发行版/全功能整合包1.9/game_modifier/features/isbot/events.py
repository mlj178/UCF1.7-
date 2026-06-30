import features.isbot.state as isbot_state


def _apply_state(context, state):
    isbot_state.state = state
    from features.isbot.panel import get_status_label

    label = get_status_label()
    if label is None:
        return
    if state == "awaiting_room":
        label.configure(text="状态: 已预约，等待进房", text_color="#f39c12")
    elif state == "awaiting_reenter":
        label.configure(text="状态: 已预约，等待重进房间生效", text_color="#f39c12")
    elif state == "active":
        label.configure(text="状态: 已生效", text_color="#2ecc71")
    else:
        label.configure(text="状态: 已关闭", text_color="#888888")


def handle_event(context, event, payload):
    if event == "state":
        context.after(0, lambda: _apply_state(context, payload.get("state", "off")))
