from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "nano_cloth"
    js_filename = "script.js"
    name = "增加防化服"
    category = "player"
    desc = "每触发一次将本地玩家防化服设为滑块值。"