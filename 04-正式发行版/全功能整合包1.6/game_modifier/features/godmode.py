from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class GodModeFeature(FeatureBase):
    feature_id = 'godmode'
    name = '金刚不坏'
    icon = '🛡️'
    category = 'player'
    desc = '免疫所有伤害'
