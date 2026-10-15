from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "29_bullet_wall_penetration"
    js_filename = "script.js"
    name = "子弹穿墙/弹体穿墙"
    category = "weapon"
    desc = "玩家开火允许子弹穿墙；本地玩家的投射物（火箭筒 / 榴弹 / 手雷 / 技能弹）撞墙也不被挡住。"
