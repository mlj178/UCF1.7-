from ui.views import WeaponGiverView


def build_panel(app, parent):
    view = WeaponGiverView(
        respawn_enabled=app._weapon_giver_respawn_enabled,
        on_respawn_toggle=app._weapon_controller.on_respawn_weapon_toggle,
        on_give_weapon=app._weapon_controller.give_weapon_by_id,
        on_bind_hotkey=app._weapon_controller.bind_weapon_hotkey_dialog,
        create_hotkey_badge=app._weapon_controller.create_hotkey_badge,
        weapon_top_frames=app._weapon_top_frames,
        weapon_hotkey_badges=app._weapon_hotkey_badges,
    )
    handles = view.build(parent)
    app.respawn_weapon_var = handles.respawn_weapon_var
    app.respawn_weapon_check = handles.respawn_weapon_check
    app.current_weapon_label = handles.current_weapon_label
    return handles
