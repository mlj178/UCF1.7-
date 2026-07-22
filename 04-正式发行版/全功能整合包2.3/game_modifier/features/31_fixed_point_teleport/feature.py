from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "fixed_point_teleport"
    js_filename = "script.js"
    name = "定点瞬移"
    icon = "📍"
    category = "other"
    desc = "保存当前位置后，将本地玩家瞬移回保存点。"
