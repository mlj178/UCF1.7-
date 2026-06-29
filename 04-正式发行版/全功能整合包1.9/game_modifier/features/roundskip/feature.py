from core.plugin.plugin_base import PluginFeatureBase


class RoundSkipFeature(PluginFeatureBase):
    feature_id = 'roundskip'
    js_filename = '10-skip_round.js'
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
