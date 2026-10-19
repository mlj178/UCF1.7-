from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "direct_damage"
    js_filename = "script.js"
    name = "开火直伤/弹体追踪"
    category = "weapon"
    desc = (
        "常规枪械：把这一发的射线方向掰到准星优先的目标身上（射线接管），"
        "命中判定 / 伤害 / 死亡广播 / 复活调度全部由游戏原版完成；"
        "榴弹/手雷/RPG/榴弹枪与特殊技能弹（奥术手榴弹、地狱终结者火球）改为弹体拐弯追踪。"
        "本版本不注入伤害、不处理死亡与复活。"
    )