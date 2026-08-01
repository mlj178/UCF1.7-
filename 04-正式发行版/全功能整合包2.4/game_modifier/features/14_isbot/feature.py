from core.plugin.plugin_base import PluginFeatureBase


class IsBotFeature(PluginFeatureBase):
    feature_id = 'isbot'
    js_filename = '14-become_bot.js'
    name = '天机傀儡'
    category = 'player'
    desc = '伪装为Bot，可触发特殊效果'
