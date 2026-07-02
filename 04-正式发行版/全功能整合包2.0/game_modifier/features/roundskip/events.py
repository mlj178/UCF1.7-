from features.roundskip.monitor import RoundSkipMonitor


_monitor = None


def _get_monitor(context):
    global _monitor
    if _monitor is None:
        _monitor = RoundSkipMonitor(context)
    return _monitor


def handle_event(context, event, payload):
    if event == "skipped":
        context.log("⏭️ 回合已跳过!")
    elif event == "skip_failed":
        context.log(f"❌ 跳过失败: {payload.get('reason', 'unknown')}")


def handle_lifecycle(context, event, payload):
    monitor = _get_monitor(context)
    if event == "game_connected":
        monitor.start()
    elif event in {"game_disconnected", "app_closing"}:
        monitor.stop()
