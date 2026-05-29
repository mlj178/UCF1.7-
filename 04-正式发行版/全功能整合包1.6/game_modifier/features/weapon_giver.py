from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class WeaponGiverFeature(FeatureBase):
    feature_id = 'weapon_giver'
    js_filename = 'weapon_giver.js'
    name = '赋予武器'
    icon = '🔫'
    category = 'weapon'
    desc = '赋予武器、复活自动装备武器'

    def __init__(self):
        super().__init__()
        self._respawn_weapon_id = None
        self._respawn_weapon_name = None

    def enable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle('weapon_giver', True)

    def disable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle('weapon_giver', False)

    def get_custom_ui(self, parent):
        return 'weapon_giver'
