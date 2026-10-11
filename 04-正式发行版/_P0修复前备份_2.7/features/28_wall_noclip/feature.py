from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "28_wall_noclip"
    js_filename = "script.js"
    name = "人体穿墙"
    category = "player"
    desc = "按住Alt，让玩家穿过墙体等障碍物。"
