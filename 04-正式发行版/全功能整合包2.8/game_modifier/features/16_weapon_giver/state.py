from dataclasses import dataclass, field


@dataclass
class WeaponGiverState:
    respawn_enabled: bool = False
    current_weapon_label: object | None = None
    respawn_weapon_var: object | None = None
    respawn_weapon_check: object | None = None
    controller: object | None = None
    weapon_hotkey_badges: dict = field(default_factory=dict)
    weapon_top_frames: dict = field(default_factory=dict)


state = WeaponGiverState()


def load_from_config(config):
    state.respawn_enabled = bool(config.get("respawn_weapon", False))
    return state
