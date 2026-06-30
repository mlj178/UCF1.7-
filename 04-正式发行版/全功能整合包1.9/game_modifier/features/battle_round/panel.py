def build_panel(context, parent):
    # The battle round controls are embedded in the nano4t special page to keep
    # the existing layout and interaction unchanged.
    legacy = context.legacy
    return {
        'battle_round_switch': legacy.get_handle('battle_round_switch'),
        'battle_round_status_label': legacy.get_handle('battle_round_status_label'),
    }
