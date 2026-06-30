from core.config import NANO4T_ATTRS
from ui.views import Nano4tView
from ui.views.common import bind_view_handles


def build_panel(app, parent):
    view = Nano4tView(
        attrs=NANO4T_ATTRS,
        temp_ghost=app._nano4t_temp_ghost,
        temp_human=app._nano4t_temp_human,
        on_ghost_select=app._nano4t_runtime_controller.on_ghost_select,
        on_human_select=app._nano4t_runtime_controller.on_human_select,
        on_apply=app._nano4t_runtime_controller.apply,
        on_toggle_battle_round=app._battle_round_controller.toggle,
    )
    handles = view.build(parent)
    bind_view_handles(app, handles)
    return handles
