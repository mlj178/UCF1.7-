from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "35_room_player_count"
    js_filename = "script.js"
    name = "全模式房间人数"
    category = "other"
    desc = "开局前设置总人数；机器人数量自动为总人数减一。"
