from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class SpeedGunFeature(FeatureBase):
    feature_id = 'speedgun'
    js_filename = 'speed_gun.js'
    name = '射速变快'
    icon = '💨'
    category = 'weapon'
    desc = '大幅提升射击速度'
