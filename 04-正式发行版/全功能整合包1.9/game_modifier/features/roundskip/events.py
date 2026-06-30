def handle_event(context, event, payload):
    if event == "skipped":
        context.log("⏭️ 回合已跳过!")
