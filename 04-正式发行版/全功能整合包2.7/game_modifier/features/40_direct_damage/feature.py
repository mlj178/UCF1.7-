from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    feature_id = "direct_damage"
    js_filename = "script.js"
    name = "开火直伤/弹体追踪"
    category = "weapon"
    desc = (
        "普通枪械：开启「普通枪械自动跟枪」后，开火时子弹方向会自动修正到当前选中的敌人；"
        "命中判定和伤害仍由游戏原版结算，不额外改伤。关闭后普通枪械完全按准星方向射击。"
        "榴弹/手雷/RPG/榴弹枪与特殊技能弹（奥术手榴弹、地狱终结者火球）改为弹体拐弯追踪。"
        "「突破复活无敌」只复位目标的复活保护（完全免疫）：枪械=选中目标，爆炸=半径内敌人，让复活无敌期间也能打掉血/炸死。"
        "本版本不注入伤害、不处理死亡与复活。"
    )