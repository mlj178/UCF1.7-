from core.plugin.plugin_base import PluginFeatureBase
from core.feature_registry import register_feature


@register_feature
class TimeFreezeFeature(PluginFeatureBase):
    feature_id = 'time'
    js_filename = '03-unlimited_time.js'
    name = '无限时间'
    icon = '⏰'
    category = 'player'
    desc = '设定时间为99:59'
