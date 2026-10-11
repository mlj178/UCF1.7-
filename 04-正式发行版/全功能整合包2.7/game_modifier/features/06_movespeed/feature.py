from core.plugin.plugin_base import PluginFeatureBase


class MoveSpeedFeature(PluginFeatureBase):
    feature_id = 'movespeed'
    js_filename = '06-movement_speed.js'
    name = '滑板鞋'
    category = 'player'
    has_slider = True
    slider_range = (1.0, 6.0, 0.1)
    slider_value = 3.0
    desc = '提升移动速度'

    # enable / disable / setConfig 走基类的插件 RPC（与 04_knife 同）。不要覆写成
    # FridaManager.send_toggle：2.7 已无该方法，覆写会让开关静默失效。
