from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "lifesteal"
    js_filename = "script.js"
    name = "伤害吸血"
    category = "player"
    desc = "对敌人造成伤害时，按实际扣血 × 吸血比例回复自身血量。"
