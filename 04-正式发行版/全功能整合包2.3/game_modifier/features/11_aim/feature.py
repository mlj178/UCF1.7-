from core.plugin.plugin_base import PluginFeatureBase


class AimFeature(PluginFeatureBase):
    feature_id = 'aim'
    js_filename = 'script.js'
    name = '自瞄'
    icon = '🎯'
    category = 'weapon'
    desc = '自动瞄准敌方玩家'
