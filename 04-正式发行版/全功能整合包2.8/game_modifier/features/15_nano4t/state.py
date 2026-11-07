from dataclasses import dataclass


@dataclass
class Nano4tState:
    ready: bool = False
    temp_ghost: int = 0
    temp_human: int = 10
    wanted_ghost: int = -1
    wanted_human: int = -1
    activated: bool = False
    current_ghost: int = -1
    current_human: int = -1
    log_errors: bool = False
    apply_cooldown: float = 0.0
    handles: object | None = None


state = Nano4tState()


def load_from_config(config):
    ghost = _clamp_ghost(config.get("ghost", 0))
    human = _clamp_human(config.get("human", 10))
    state.temp_ghost = ghost
    state.temp_human = human
    return state


def save_selection(context):
    context.config_manager.set(
        "nano4t",
        {
            "ghost": state.temp_ghost,
            "human": state.temp_human,
        },
    )


def _clamp_ghost(value):
    try:
        feature_id = int(value)
    except Exception:
        return 0
    return feature_id if 0 <= feature_id < 10 else 0


def _clamp_human(value):
    try:
        feature_id = int(value)
    except Exception:
        return 10
    return feature_id if 10 <= feature_id < 20 else 10
