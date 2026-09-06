from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "29_bullet_wall_penetration"
    js_filename = "script.js"
    name = "子弹穿墙"
    category = "weapon"
    desc = "玩家开火允许子弹穿墙。"
