from features.nano4t.runtime import Nano4tRuntime
from features.nano4t.selection import Nano4tSelectionController
from features.nano4t.state import save_selection, state
from core.config import NANO4T_ATTRS


def _runtime(context):
    selector = Nano4tSelectionController(NANO4T_ATTRS, state, on_save=lambda: save_selection(context))
    return Nano4tRuntime(context, selector)


def handle_event(context, event, payload):
    runtime = _runtime(context)

    if event == "nano4t_ready":
        ids = payload.get("ids", [])
        context.after(0, lambda: runtime.on_ready(len(ids)))
    elif event == "nano4t_destroyed":
        runtime.on_destroyed_event()
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
    elif event == "nano4t_dead":
        runtime.on_dead()
    elif event == "nano4t_alive":
        runtime.on_alive()
    elif event == "mode_detected":
        runtime.auto_init_if_needed_async()
    elif event == "get_current":
        runtime.get_current_async()


def handle_lifecycle(context, event, payload):
    runtime = _runtime(context)
    if event == "game_connected":
        runtime.auto_init_async()
    elif event == "game_disconnected":
        runtime.handle_mode_exit()
