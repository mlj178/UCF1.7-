from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "hp_boost"
    js_filename = "script.js"
    name = "增加血量"
    category = "player"
    desc = "开启后，每触发一次快捷键或「加血一次」按钮，为本地玩家加一次血（上限同步提升）。"