from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class TimeScaleFeature(FeatureBase):
    feature_id = 'timescale'
    js_filename = 'time_scale.js'
    name = '时间加速'
    icon = '⏩'
    category = 'other'
    has_slider = True
    slider_range = (0.1, 10.0, 0.1)
    slider_value = 1.0
    desc = '调整Unity游戏时间倍速'

    def __init__(self):
        super().__init__()
        self._current_speed = 1.0

    def enable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            # 合并两条消息，避免竞态：通过 extra_params 传递 speed
            fm.send_toggle('timescale', True, extra_params={'speed': self._current_speed})

    def disable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle('timescale', False)

    def on_slider_change(self, value):
        self._current_speed = round(float(value), 1)
        self.slider_value = self._current_speed
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected and self._enabled:
            fm.send_toggle('timescale_speed', self._current_speed)
