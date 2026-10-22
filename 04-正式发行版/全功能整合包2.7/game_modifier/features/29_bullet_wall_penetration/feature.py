from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "29_bullet_wall_penetration"
    js_filename = "script.js"
    name = "子弹穿墙/弹体穿墙"
    category = "weapon"
    desc = "子弹和弹体（火箭弹/榴弹/手雷/技能弹）能直接穿墙，隔墙也能打到人。只对自己生效。"
