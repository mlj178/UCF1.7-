from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "damage_multiplier"
    js_filename = "script.js"
    name = "调整伤害倍率"
    category = "weapon"
    desc = "分开调整敌人 / 自己 / 队友造成的伤害，可调高也可调低。"
