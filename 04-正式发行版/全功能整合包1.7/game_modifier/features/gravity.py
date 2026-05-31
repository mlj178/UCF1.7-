from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class GravityFeature(FeatureBase):
    feature_id = 'gravity'
    name = '轻重力'
    icon = '🌌'
    category = 'player'
    has_slider = False
    desc = '调整重力与跳跃倍率'

    def __init__(self):
        super().__init__()
        self._gravity = 1.0
        self._jump = 1.0
        self._gravity_mode = 'player_only'

    def enable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle('gravity', True)
            self._send_gravity_config(fm)

    def disable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle('gravity', False)

    def _send_gravity_config(self, fm=None):
        if fm is None:
            from core.frida_manager import FridaManager
            fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle('gravity_config', {'g': self._gravity, 'j': self._jump, 'm': self._gravity_mode})

    def set_gravity(self, value):
        self._gravity = round(float(value), 1)
        self._send_gravity_config()

    def set_jump(self, value):
        self._jump = round(float(value), 1)
        self._send_gravity_config()

    def set_mode(self, mode):
        self._gravity_mode = mode
        self._send_gravity_config()

    def get_custom_ui(self, parent):
        return 'gravity'
