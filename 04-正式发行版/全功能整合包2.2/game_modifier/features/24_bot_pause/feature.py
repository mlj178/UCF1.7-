from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "bot_pause"
    js_filename = "script.js"
    name = "人机暂停"
    icon = "⏸️"
    category = "other"
    desc = "所有人机停止行动。"
