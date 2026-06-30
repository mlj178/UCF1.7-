def build_panel(app, parent):
    # The battle round controls are embedded in the nano4t special page to keep
    # the existing layout and interaction unchanged.
    return {
        'battle_round_switch': getattr(app, 'battle_round_switch', None),
        'battle_round_status_label': getattr(app, 'battle_round_status_label', None),
    }
