from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "hp_boost"
    js_filename = "script.js"
    name = "增加血量"
    category = "player"
    desc = "开启后，按一次 F3（或点“加血一次”）为本地玩家加一次血。"