from core.plugin.plugin_base import PluginFeatureBase


class RecoilFeature(PluginFeatureBase):
    feature_id = 'recoil'
    js_filename = '02-no_recoil.js'
    name = '无后座力'
    icon = '🎯'
    category = 'weapon'
    desc = '消除所有枪械后座力'
