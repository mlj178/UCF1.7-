from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "free_camera"
    js_filename = "script.js"
    name = "自由视角"
    category = "other"
    desc = "脱离玩家跟随，可无限制拖动镜头查看全地图战局。"
