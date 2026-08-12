from importlib import import_module

from core.config import NANO4T_ATTRS
from ui.views import Nano4tView

from .runtime import Nano4tRuntime
from .selection import Nano4tSelectionController
from .state import load_from_config, save_selection, state

BattleRoundController = import_module("features.19_battle_round.controller").BattleRoundController
battle_state_module = import_module("features.19_battle_round.state")
load_battle_config = battle_state_module.load_from_config
battle_state = battle_state_module.state


def build_panel(context, parent):
    load_from_config(context.get_config())
    load_battle_config(context.config_manager.get("battle_round"))
    selector = Nano4tSelectionController(
        NANO4T_ATTRS,
        state,
        on_save=lambda: save_selection(context),
    )
    runtime = Nano4tRuntime(context, selector)
    battle_controller = BattleRoundController(context)
    view = Nano4tView(
        attrs=NANO4T_ATTRS,
        temp_ghost=state.temp_ghost,
        temp_human=state.temp_human,
        on_ghost_select=runtime.on_ghost_select,
        on_human_select=runtime.on_human_select,
        on_apply=runtime.apply,
        on_toggle_battle_round=battle_controller.toggle,
    )
    handles = view.build(parent)
    state.handles = handles
    battle_state.handles = handles
    battle_controller.update_button_state()
    return handles
