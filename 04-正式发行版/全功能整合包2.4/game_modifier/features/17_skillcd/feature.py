from core.plugin.plugin_base import PluginFeatureBase


class SkillCdFeature(PluginFeatureBase):
    feature_id = 'skillcd'
    js_filename = '17-skill_no_cooldown.js'
    name = '技能无冷却'
    icon = '🔄'
    category = 'player'
    desc = '所有技能无冷却时间'
