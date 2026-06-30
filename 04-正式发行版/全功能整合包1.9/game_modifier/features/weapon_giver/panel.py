from features.weapon_giver.controller import WeaponInteractionController
from features.weapon_giver.state import load_from_config, state
from ui.views import WeaponGiverView


def build_panel(context, parent):
    load_from_config(context.get_config())
    controller = WeaponInteractionController(context, parent.winfo_toplevel())
    view = WeaponGiverView(
        respawn_enabled=state.respawn_enabled,
        on_respawn_toggle=controller.on_respawn_weapon_toggle,
        on_give_weapon=controller.give_weapon_by_id,
        on_bind_hotkey=controller.bind_weapon_hotkey_dialog,
        create_hotkey_badge=controller.create_hotkey_badge,
        weapon_top_frames=state.weapon_top_frames,
        weapon_hotkey_badges=state.weapon_hotkey_badges,
    )
    handles = view.build(parent)
    state.respawn_weapon_var = handles.respawn_weapon_var
    state.respawn_weapon_check = handles.respawn_weapon_check
    state.current_weapon_label = handles.current_weapon_label
    state.controller = controller
    return handles
