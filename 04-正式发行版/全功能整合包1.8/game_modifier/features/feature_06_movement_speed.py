from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class MoveSpeedFeature(FeatureBase):
    feature_id = 'movespeed'
    js_filename = '06-movement_speed.js'
    name = '滑板鞋'
    icon = '👟'
    category = 'player'
    has_slider = True
    slider_range = (1.0, 6.0, 0.1)
    slider_value = 3.0
    desc = '提升移动速度'

    def __init__(self):
        super().__init__()
        self._current_speed = 3.0

    def enable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle('movespeed', True)
            fm.send_toggle('movespeed_speed', self._current_speed)

    def disable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle('movespeed', False)

    def on_slider_change(self, value):
        self._current_speed = round(float(value), 1)
        self.slider_value = self._current_speed
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected and self._enabled:
            fm.send_toggle('movespeed_speed', self._current_speed)
