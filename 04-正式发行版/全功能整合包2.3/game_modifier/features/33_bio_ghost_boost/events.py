def handle_event(context, event, payload):
    if event == "status":
        context.log(f"生化幽灵专区状态: {payload}")
