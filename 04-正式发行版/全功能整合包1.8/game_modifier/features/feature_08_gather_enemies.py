from features.base import FeatureBase
from core.feature_registry import register_feature
from core.event_bus import EventBus


@register_feature
class GatherFeature(FeatureBase):
    feature_id = 'gather'
    js_filename = '08-gather_enemies.js'
    name = '聚怪'
    icon = '👾'
    category = 'other'
    desc = '将所有人机聚集。一般用于多人生化模式'

    def __init__(self):
        super().__init__()

    def do_gather(self):
        from core.frida_manager import FridaManager
        fm = FridaManager.get_instance()
        if not fm.is_connected:
            return {'ok': False, 'msg': '未连接游戏'}
        if not self._enabled:
            return {'ok': False, 'msg': '聚怪功能未启用'}
        result = fm.call_export('gather')
        return result or {'ok': False, 'msg': '调用失败'}
