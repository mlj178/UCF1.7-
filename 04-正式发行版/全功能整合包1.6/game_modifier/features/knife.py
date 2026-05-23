from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class KnifeFeature(FeatureBase):
    feature_id = 'knife'
    name = '快刀'
    icon = '🔪'
    category = 'weapon'
    has_slider = True
    slider_range = (1.0, 10.0, 0.1)
    slider_value = 5.0
    desc = '提升挥刀速度（人类+生化幽灵通用）'

    def __init__(self):
        super().__init__()
        self._current_speed = 5.0

    def enable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle('knife', True)
            fm.send_toggle('knife_speed', self._current_speed)

    def disable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle('knife', False)

    def on_slider_change(self, value):
        self._current_speed = round(float(value), 1)
        self.slider_value = self._current_speed
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected and self._enabled:
            fm.send_toggle('knife_speed', self._current_speed)
