from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "become_ghostblade"
    js_filename = "script.js"
    name = "直接变身剑客"
    category = "special"
    desc = "生化6（剑客模式）：本地玩家或佣兵 Bot 直接变成剑客。"
