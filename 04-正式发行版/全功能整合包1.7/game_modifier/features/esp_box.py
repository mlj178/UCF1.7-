from features.base import FeatureBase
from core.feature_registry import register_feature
from core.universal_hook_manager import UniversalHookManager


@register_feature
class ESPBoxFeature(FeatureBase):
    feature_id = 'esp_box'
    name = '方框透视'
    icon = '📦'
    category = 'other'
    desc = '通过 Universal DLL 显示方框透视'

    def __init__(self):
        super().__init__()
        self._manager = UniversalHookManager()

    def enable(self):
        if self._manager.set_esp_box(True):
            self._enabled = True
            return True
        self._enabled = False
        return False

    def disable(self):
        ok = self._manager.set_esp_box(False)
        self._enabled = False
        return ok

    def cleanup(self):
        self._manager.shutdown()
