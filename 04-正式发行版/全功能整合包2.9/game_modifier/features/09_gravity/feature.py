from core.plugin.plugin_base import PluginFeatureBase


class GravityFeature(PluginFeatureBase):
    feature_id = 'gravity'
    js_filename = '09-high_jump_low_gravity.js'
    name = '轻重力'
    category = 'player'
    has_slider = False
    desc = '调整重力与跳跃倍率'

    # enable / disable 走基类的插件 RPC；参数经 setConfig({gravity, jump, mode}) 下发。
    # 不要覆写成 FridaManager.send_toggle：2.7 已无该方法，覆写会让开关静默失效。
    def set_gravity(self, value):
        return self.set_config({'gravity': round(float(value), 1)})

    def set_jump(self, value):
        return self.set_config({'jump': round(float(value), 1)})

    def set_mode(self, mode):
        return self.set_config({'mode': mode})

    def get_custom_ui(self, parent):
        return 'gravity'
