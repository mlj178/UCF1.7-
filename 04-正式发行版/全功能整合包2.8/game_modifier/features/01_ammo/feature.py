from core.plugin.plugin_base import PluginFeatureBase


class AmmoFeature(PluginFeatureBase):
    feature_id = 'ammo'
    js_filename = 'script.js'
    name = '无限子弹'
    category = 'weapon'
    desc = '无限子弹（开火不扣弹）与无限弹药（备弹无限，覆盖普通枪械与 RPG/AT4）可分别开关并设置应用范围。'