from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "27_game_mode_override"
    js_filename = "script.js"
    name = "游戏模式切换"
    category = "other"
    desc = "切换游戏模式，请在游戏房间创建前应用。"
