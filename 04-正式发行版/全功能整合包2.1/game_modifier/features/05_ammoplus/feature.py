from core.plugin.plugin_base import PluginFeatureBase


class ReloadSpeedFeature(PluginFeatureBase):
    feature_id = 'ammoplus'
    js_filename = '05-fast_reload_buff.js'
    name = '快速换弹'
    icon = '⚡'
    category = 'weapon'
    desc = '换弹速度加快'
