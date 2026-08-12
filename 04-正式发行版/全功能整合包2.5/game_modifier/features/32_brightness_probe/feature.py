from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "brightness_probe"
    js_filename = "script.js"
    name = "亮度调节"
    category = "other"
    desc = "验证并调节游戏 URP 后处理参数。"
