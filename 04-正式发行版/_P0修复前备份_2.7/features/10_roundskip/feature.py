from core.plugin.plugin_base import PluginFeatureBase


class RoundSkipFeature(PluginFeatureBase):
    feature_id = 'roundskip'
    js_filename = '10-skip_round.js'
    name = '回合跳过'
    category = 'other'
    desc = '结束当前回合（需要等待几秒）'

    def __init__(self):
        super().__init__()
        self._skip_count = 0

    def get_custom_ui(self, parent):
        return 'round_skip'
