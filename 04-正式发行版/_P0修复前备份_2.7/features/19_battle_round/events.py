from .controller import BattleRoundController


def _notify_nano4t_mode_detected(context):
    context.feature_event("mode_detected", {}, feature_id="nano4t")


def handle_event(context, event, payload):
    battle_round = BattleRoundController(context)

    def update():
        if event in {"battle_round_mode_enter", "mode_enter"}:
            battle_round.on_mode_enter()
            _notify_nano4t_mode_detected(context)
        elif event in {"battle_round_mode_exit", "mode_exit"}:
            battle_round.on_mode_exit()
        elif event == "battle_round_round":
            battle_round.on_round(payload)
            _notify_nano4t_mode_detected(context)
            context.feature_event("get_current", {}, feature_id="nano4t")

    context.after(0, update)


def handle_lifecycle(context, event, payload):
    battle_round = BattleRoundController(context)
    if event == "game_connected":
        context.after(0, battle_round.sync_to_game_on_connect)
    elif event == "game_disconnected":
        context.after(0, battle_round.on_disconnected)
