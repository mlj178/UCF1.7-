from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class RoundSkipFeature(FeatureBase):
    feature_id = 'roundskip'
    js_filename = 'round_skip.js'
    name = '回合跳过'
    icon = '⏭️'
    category = 'other'
    desc = '结束当前回合（需要等待几秒）'

    def __init__(self):
        super().__init__()
        self._skip_count = 0

    def do_skip(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if not fm.is_connected:
            return {'ok': False, 'reason': 'not_connected'}
        result = fm.call_export('roundskip')
        if result and result.get('ok'):
            self._skip_count = result.get('count', self._skip_count + 1)
        return result

    def get_status(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if not fm.is_connected:
            return {'ok': False}
        return fm.call_export('getRoundStatus')

    def get_custom_ui(self, parent):
        return 'round_skip'
