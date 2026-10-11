from core.plugin.plugin_base import PluginFeatureBase


class KnifeFeature(PluginFeatureBase):
    feature_id = 'knife'
    js_filename = '04-fast_knife.js'
    name = '快刀'
    category = 'weapon'
    has_slider = True
    slider_range = (1.0, 10.0, 0.1)
    slider_value = 5.0
    desc = '提升挥刀速度（人类+幽灵通用）'

    # enable / disable / setConfig 一律走基类的插件 RPC（ActionRouter -> FeatureCommandService
    # -> plugin_call -> script.js 的 rpc.exports）。这里不要再用 FridaManager.send_toggle：
    # 该方法在 2.7 已不存在，覆写后开关会抛 AttributeError，导致 UI 状态与游戏实际不一致。
