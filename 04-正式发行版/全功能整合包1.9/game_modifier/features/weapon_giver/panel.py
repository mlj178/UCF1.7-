from ui.views import WeaponGiverView


def build_panel(context, parent):
    legacy = context.legacy
    view = WeaponGiverView(
        respawn_enabled=legacy.get_state("weapon_giver_respawn_enabled", False),
        on_respawn_toggle=legacy.weapon_controller.on_respawn_weapon_toggle,
        on_give_weapon=legacy.weapon_controller.give_weapon_by_id,
        on_bind_hotkey=legacy.weapon_controller.bind_weapon_hotkey_dialog,
        create_hotkey_badge=legacy.weapon_controller.create_hotkey_badge,
        weapon_top_frames=legacy.weapon_top_frames,
        weapon_hotkey_badges=legacy.weapon_hotkey_badges,
    )
    handles = view.build(parent)
    legacy.set_handle("respawn_weapon_var", handles.respawn_weapon_var)
    legacy.set_handle("respawn_weapon_check", handles.respawn_weapon_check)
    legacy.set_handle("current_weapon_label", handles.current_weapon_label)
    return handles
