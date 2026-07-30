from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "fixed_point_teleport"
    js_filename = "script.js"
    name = "定点瞬移"
    icon = "📍"
    category = "other"
    desc = "保存点位1或点位2后，将本地玩家瞬移回对应点位。"
