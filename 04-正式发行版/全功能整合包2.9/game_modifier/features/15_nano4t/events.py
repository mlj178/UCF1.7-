from core.config import NANO4T_ATTRS

from .runtime import Nano4tRuntime
from .selection import Nano4tSelectionController
from .state import save_selection, state


def _runtime(context):
    selector = Nano4tSelectionController(NANO4T_ATTRS, state, on_save=lambda: save_selection(context))
    return Nano4tRuntime(context, selector)


def handle_event(context, event, payload):
    runtime = _runtime(context)

    if event == "nano4t_ready":
        ids = payload.get("ids", [])
        context.after(0, lambda: runtime.on_ready(len(ids)))
    elif event == "nano4t_mode_enter":
        context.after(0, runtime.on_mode_detected)
    elif event == "nano4t_mode_exit":
        runtime.handle_mode_exit()
    elif event == "nano4t_error":
        runtime.on_error(payload)
    elif event == "nano4t_set":
        g = int(payload.get("g", 0))
        h = int(payload.get("h", 0))
        runtime.on_set(g, h)
    elif event == "nano4t_current":
        g = int(payload.get("g", -1))
        h = int(payload.get("h", -1))
        context.after(0, lambda gg=g, hh=h: runtime.update_round_label(gg, hh))
    elif event == "get_current":
        runtime.get_current_async()


def handle_lifecycle(context, event, payload):
    runtime = _runtime(context)
    if event == "game_connected":
        runtime.auto_init_async()
    elif event == "game_disconnected":
        runtime.handle_mode_exit()
