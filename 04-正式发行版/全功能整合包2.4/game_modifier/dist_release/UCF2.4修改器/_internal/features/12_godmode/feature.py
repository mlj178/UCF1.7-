from core.plugin.plugin_base import PluginFeatureBase


class GodModeFeature(PluginFeatureBase):
    feature_id = 'godmode'
    js_filename = '12-invincibility.js'
    name = '金刚不坏'
    category = 'player'
    desc = '免疫所有伤害'
