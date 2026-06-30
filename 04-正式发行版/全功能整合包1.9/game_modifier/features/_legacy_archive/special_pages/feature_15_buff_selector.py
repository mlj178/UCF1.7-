from features.base import FeatureBase
from core.feature_registry import register_feature
from core.config import NANO4T_ATTRS


@register_feature
class Nano4tFeature(FeatureBase):
    feature_id = 'nano4t'
    js_filename = '15-buff_selector.js'
    name = '多人生化特性'
    icon = '🧬'
    category = 'other'
    has_combo = True
    combo_options = NANO4T_ATTRS
    desc = '多人生化模式特性选择'

    def __init__(self):
        super().__init__()
        self._ghost_attr = -1
        self._human_attr = -1

    def enable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.call_export('nano4tinit')

    def disable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.call_export('nano4tinit')

    def set_attrs(self, ghost, human):
        self._ghost_attr = ghost
        self._human_attr = human
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.call_export('nano4tset', ghost, human)

    def on_combo_change(self, selected):
        if isinstance(selected, dict):
            ghost = selected.get('ghost', -1)
            human = selected.get('human', -1)
            self.set_attrs(ghost, human)

    def get_custom_ui(self, parent):
        return 'nano4t'
