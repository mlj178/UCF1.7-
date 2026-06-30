def handle_event(context, event, payload):
    battle_round = context.controller("battle_round")
    nano4t_runtime = context.controller("nano4t_runtime")

    def update():
        if event == "battle_round_mode_enter":
            battle_round.on_mode_enter()
        elif event == "battle_round_mode_exit":
            battle_round.on_mode_exit()
        elif event == "battle_round_round":
            battle_round.on_round(payload)
            nano4t_runtime.get_current_async()

    context.after(0, update)
