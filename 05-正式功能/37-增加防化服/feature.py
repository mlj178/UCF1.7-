from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "nano_cloth"
    js_filename = "script.js"
    name = "增加防化服"
    category = "special"
    desc = "将本地玩家防化服数量直接设为指定值（多人生化模式）。"