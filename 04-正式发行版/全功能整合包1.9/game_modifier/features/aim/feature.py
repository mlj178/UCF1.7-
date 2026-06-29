from core.plugin.plugin_base import PluginFeatureBase


class AimFeature(PluginFeatureBase):
    feature_id = 'aim'
    js_filename = '11-auto_aim.js'
    name = '自瞄'
    icon = '🎯'
    category = 'weapon'
    desc = '自动瞄准最近敌人'
