from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "direct_damage"
    js_filename = "script.js"
    name = "开火直伤/弹体追踪"
    category = "weapon"
    desc = "常规枪械开火直接结算伤害；榴弹/手雷/RPG/榴弹枪与特殊技能弹（奥术手榴弹、地狱终结者火球）改为弹体拐弯追踪。"