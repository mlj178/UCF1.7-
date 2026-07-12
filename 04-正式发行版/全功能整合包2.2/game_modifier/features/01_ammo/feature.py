from core.plugin.plugin_base import PluginFeatureBase


class AmmoFeature(PluginFeatureBase):
    feature_id = 'ammo'
    js_filename = '01-unlimited_ammo.js'
    name = '无限子弹'
    icon = '🔫'
    category = 'weapon'
    desc = '子弹永不消耗'
