from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class RecoilFeature(FeatureBase):
    feature_id = 'recoil'
    js_filename = '02-no_recoil.js'
    name = '无后座力'
    icon = '🎯'
    category = 'weapon'
    desc = '消除所有枪械后座力'
