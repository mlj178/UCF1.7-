from core.plugin.plugin_base import PluginFeatureBase


class TimeFreezeFeature(PluginFeatureBase):
    feature_id = 'time'
    js_filename = '03-unlimited_time.js'
    name = '无限时间'
    category = 'player'
    desc = '设定时间为99:59'
