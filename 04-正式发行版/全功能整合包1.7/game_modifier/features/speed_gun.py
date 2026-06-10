from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class SpeedGunFeature(FeatureBase):
    feature_id = 'speedgun'
    js_filename = 'speed_gun.js'
    name = '射速变快+连狙'
    icon = '⚡'
    category = 'weapon'
    desc = '射速10倍 | 半自动→全自动 | 狙击镜常开 | 后坐力清零'
