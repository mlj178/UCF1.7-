from core.plugin.plugin_base import PluginFeatureBase


class TimeScaleFeature(PluginFeatureBase):
    feature_id = 'timescale'
    js_filename = '20-unity_time_acceleration.js'
    name = '时间加速'
    category = 'other'
    has_slider = True
    slider_range = (0.1, 10.0, 0.1)
    slider_value = 1.0
    desc = '调整Unity游戏时间倍速'

    # enable / disable / setConfig 走基类的插件 RPC（与 04_knife 同）。不要覆写成
    # FridaManager.send_toggle：2.7 已无该方法，覆写会让开关静默失效。
    # 速度经 ActionRouter.set_config -> setConfig({speed}) 下发，无需额外通道。
