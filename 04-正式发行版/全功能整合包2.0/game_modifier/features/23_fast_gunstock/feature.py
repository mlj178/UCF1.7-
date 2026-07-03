from core.plugin.plugin_base import PluginFeatureBase


class FastGunstockFeature(PluginFeatureBase):
    feature_id = "fast_gunstock"
    js_filename = "script.js"
    name = "极速枪托"
    icon = "⚡"
    category = "weapon"
    desc = "枪托右键重击攻击速度更快"
