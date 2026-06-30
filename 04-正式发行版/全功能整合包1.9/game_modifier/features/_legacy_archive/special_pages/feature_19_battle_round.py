from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class BattleRoundAlwaysFeature(FeatureBase):
    feature_id = 'battle_round_always'
    js_filename = '19-battle_round.js'
    name = '强制决战回合'
    icon = '⚔️'
    category = 'nano4t'
    desc = '每局强制触发决战回合（保底局）'

    def __init__(self):
        super().__init__()

    def enable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle('battle_round_always', True)

    def disable(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if fm.is_connected:
            fm.send_toggle('battle_round_always', False)
