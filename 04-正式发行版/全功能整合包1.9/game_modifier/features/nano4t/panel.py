from core.config import NANO4T_ATTRS
from ui.views import Nano4tView


def build_panel(context, parent):
    view = Nano4tView(
        attrs=NANO4T_ATTRS,
        temp_ghost=context.get_state("nano4t_temp_ghost", 0),
        temp_human=context.get_state("nano4t_temp_human", 10),
        on_ghost_select=context.controller("nano4t_runtime").on_ghost_select,
        on_human_select=context.controller("nano4t_runtime").on_human_select,
        on_apply=context.controller("nano4t_runtime").apply,
        on_toggle_battle_round=context.controller("battle_round").toggle,
    )
    handles = view.build(parent)
    context.bind_handles(handles)
    return handles
