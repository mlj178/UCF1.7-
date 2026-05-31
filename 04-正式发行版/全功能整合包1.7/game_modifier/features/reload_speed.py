from features.base import FeatureBase
from core.feature_registry import register_feature


@register_feature
class ReloadSpeedFeature(FeatureBase):
    feature_id = 'ammoplus'
    js_filename = 'reload_speed.js'
    name = '快速换弹'
    icon = '⚡'
    category = 'weapon'
    desc = '换弹速度加快'
