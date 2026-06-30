def build_panel(context, parent):
    # The battle round controls are embedded in the nano4t special page to keep
    # the existing layout and interaction unchanged.
    from features.battle_round.state import state

    if not state.handles:
        return {}
    return {
        "battle_round_switch": state.handles.battle_round_switch,
        "battle_round_status_label": state.handles.battle_round_status_label,
    }
