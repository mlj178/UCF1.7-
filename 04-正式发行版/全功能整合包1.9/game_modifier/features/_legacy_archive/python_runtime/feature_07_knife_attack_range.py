from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class KnifeRangeFeature(FeatureBase):
    feature_id = 'range'
    js_filename = '07-knife_attack_range.js'
    name = '剑气化丝'
    icon = '⚔️'
    category = 'weapon'
    has_slider = True
    slider_range = (1.0, 50.0, 1.0)
    slider_value = 50.0
    desc = '扩大近战攻击距离（人类+生化幽灵通用）'

    def __init__(self):
        super().__init__()
        self._range_mult = 50.0

    def enable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle('range', True)
            fm.send_toggle('range_config', self._range_mult)

    def disable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle('range', False)

    def on_slider_change(self, value):
        self._range_mult = round(float(value), 0)
        self.slider_value = self._range_mult
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected and self._enabled:
            fm.send_toggle('range_config', self._range_mult)
