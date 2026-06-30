from ui.views import WeaponGiverView


def build_panel(context, parent):
    view = WeaponGiverView(
        respawn_enabled=context.get_state("weapon_giver_respawn_enabled", False),
        on_respawn_toggle=context.weapon_controller.on_respawn_weapon_toggle,
        on_give_weapon=context.weapon_controller.give_weapon_by_id,
        on_bind_hotkey=context.weapon_controller.bind_weapon_hotkey_dialog,
        create_hotkey_badge=context.weapon_controller.create_hotkey_badge,
        weapon_top_frames=context.weapon_top_frames,
        weapon_hotkey_badges=context.weapon_hotkey_badges,
    )
    handles = view.build(parent)
    context.set_handle("respawn_weapon_var", handles.respawn_weapon_var)
    context.set_handle("respawn_weapon_check", handles.respawn_weapon_check)
    context.set_handle("current_weapon_label", handles.current_weapon_label)
    return handles
