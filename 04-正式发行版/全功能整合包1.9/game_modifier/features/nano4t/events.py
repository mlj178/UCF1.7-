def handle_event(context, event, payload):
    runtime = context.controller("nano4t_runtime")
    battle_round = context.controller("battle_round")

    if event == "nano4t_ready":
        ids = payload.get("ids", [])
        context.after(0, lambda: runtime.on_ready(len(ids)))
        context.after(0, battle_round.update_button_state)
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
