from core.plugin.plugin_base import PluginFeatureBase


class SpeedGunFeature(PluginFeatureBase):
    feature_id = 'speedgun'
    js_filename = '13-fire_rate_auto_sniper.js'
    name = '射速变快+连狙'
    category = 'weapon'
    desc = '射速10倍 | 半自动→全自动 | 狙击镜常开 | 后坐力清零'
