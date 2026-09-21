from . import status_monitor


def handle_event(context, event, payload):
    return None


def handle_lifecycle(context, event, payload):
    monitor = status_monitor.get_monitor(context)
    if event == "game_connected":
        monitor.start()
    elif event in {"game_disconnected", "game_not_found", "app_closing"}:
        monitor.stop()