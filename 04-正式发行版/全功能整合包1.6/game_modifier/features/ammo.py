from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class AmmoFeature(FeatureBase):
    feature_id = 'ammo'
    name = '无限子弹'
    icon = '🔫'
    category = 'weapon'
    desc = '子弹永不消耗'
