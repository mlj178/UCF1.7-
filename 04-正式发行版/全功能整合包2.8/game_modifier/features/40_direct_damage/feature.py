from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "direct_damage"
    js_filename = "script.js"
    name = "开火直伤/弹体追踪"
    category = "weapon"
    desc = (
        "准星附近有敌人时，开枪子弹会自动追踪目标（搭配子弹穿墙，可追踪墙后的敌人）；"
        "手雷、榴弹、火箭弹、技能弹会拐弯追人；"
        "刚复活的敌人也能打掉血（无视复活无敌）。"
    )