def handle_event(context, event, payload):
    """本功能插件事件处理，保持功能局部化。"""
    if event == "enabled":
        context.log("增加血量已启用")
    elif event == "disabled":
        context.log("增加血量已关闭")