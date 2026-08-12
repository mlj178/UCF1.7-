from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "damage_multiplier"
    js_filename = "script.js"
    name = "调整伤害倍率"
    category = "weapon"
    desc = "放大玩家造成的输出伤害。"
