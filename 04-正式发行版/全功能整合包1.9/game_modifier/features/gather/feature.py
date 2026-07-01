from core.plugin.plugin_base import PluginFeatureBase


class GatherFeature(PluginFeatureBase):
    feature_id = 'gather'
    js_filename = '08-gather_enemies.js'
    name = '聚怪'
    icon = '👾'
    category = 'other'
    desc = '将所有人机聚集。一般用于多人生化模式'

    def __init__(self):
        super().__init__()
