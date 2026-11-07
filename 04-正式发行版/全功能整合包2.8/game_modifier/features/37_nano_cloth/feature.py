from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "nano_cloth"
    js_filename = "script.js"
    name = "增加防化服"
    category = "player"
    desc = "点一次给防化服加 N 件，可反复叠加，回合结束自动清回原样。"