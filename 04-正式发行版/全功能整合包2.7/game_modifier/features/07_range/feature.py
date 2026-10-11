from core.plugin.plugin_base import PluginFeatureBase


class KnifeRangeFeature(PluginFeatureBase):
    feature_id = 'range'
    js_filename = '07-knife_attack_range.js'
    name = '剑气化丝'
    category = 'weapon'
    has_slider = True
    slider_range = (1.0, 50.0, 1.0)
    slider_value = 50.0
    desc = '扩大近战攻击距离（人类+幽灵通用）'

    # enable / disable / setConfig 走基类的插件 RPC（与 04_knife 同）。不要覆写成
    # FridaManager.send_toggle：2.7 已无该方法，覆写会让开关静默失效。
