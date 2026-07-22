from core.plugin.plugin_base import PluginFeatureBase


class UnlimitedBagFeature(PluginFeatureBase):
    feature_id = "unlimited_bag"
    js_filename = "script.js"
    name = "无限背包"
    icon = "🎒"
    category = "other"
    desc = "在远离出生点时也能切换背包武器"
