from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class AimFeature(FeatureBase):
    feature_id = 'aim'
    js_filename = '11-auto_aim.js'
    name = '自瞄'
    icon = '🎯'
    category = 'weapon'
    desc = '自动瞄准最近敌人'
