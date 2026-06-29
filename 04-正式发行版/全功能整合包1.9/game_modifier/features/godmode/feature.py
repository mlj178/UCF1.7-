from core.plugin.plugin_base import PluginFeatureBase
from core.feature_registry import register_feature


@register_feature
class GodModeFeature(PluginFeatureBase):
    feature_id = 'godmode'
    js_filename = '12-invincibility.js'
    name = '金刚不坏'
    icon = '🛡️'
    category = 'player'
    desc = '免疫所有伤害'
