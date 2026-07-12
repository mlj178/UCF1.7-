from . import state as isbot_state


def _status_props(state):
    if state == "awaiting_room":
        return "状态: 已预约，等待进房", "#f39c12"
    if state == "awaiting_reenter":
        return "状态: 已预约，等待重进房间生效", "#f39c12"
    if state == "active":
        return "状态: 已生效", "#2ecc71"
    return "状态: 已关闭", "#888888"


def _desired_state_for_context(context):
    return "awaiting_room" if context.is_enabled() else "off"


def _apply_state(context, state):
    isbot_state.state = state
    label = isbot_state.status_label
    if label is None:
        return
    text, color = _status_props(state)
    label.configure(text=text, text_color=color)


def handle_event(context, event, payload):
    if event == "state":
        context.after(0, lambda: _apply_state(context, payload.get("state", "off")))


def handle_lifecycle(context, event, payload):
    if event in {"game_connected", "game_disconnected"}:
        context.after(0, lambda: _apply_state(context, _desired_state_for_context(context)))
    elif event == "app_closing":
        context.after(0, lambda: _apply_state(context, "off"))
