def handle_event(context, event, payload):
    """本功能插件事件处理，保持功能局部化。"""
    if event == "enabled":
        context.log("伤害吸血已启用")
    elif event == "disabled":
        context.log("伤害吸血已关闭")
    return None


def handle_lifecycle(context, event, payload):
    return None
