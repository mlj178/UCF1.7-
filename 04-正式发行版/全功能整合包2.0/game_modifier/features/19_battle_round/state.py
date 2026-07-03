from dataclasses import dataclass


@dataclass
class BattleRoundState:
    enabled: bool = False
    active: bool = False
    mode_active: bool = False
    handles: object | None = None


state = BattleRoundState()


def load_from_config(config):
    state.enabled = bool(config.get("enabled", False))
    return state
