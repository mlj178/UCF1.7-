import os
import sys

if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
    RESOURCE_DIR = os.path.join(sys._MEIPASS, "资源")
else:
    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RESOURCE_DIR = os.path.join(os.path.dirname(APP_DIR), "资源")

DATA_DIR = os.path.join(APP_DIR, "data")
SCRIPTS_DIR = os.path.join(APP_DIR, "scripts")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

HOTKEYS_FILE = os.path.join(DATA_DIR, "hotkeys.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
NANO4T_FILE = os.path.join(DATA_DIR, "Nano-4T-selector.json")

HOTKEY_POSITIONS = ['ctrl+1', 'ctrl+2', 'ctrl+3', 'ctrl+4', 'ctrl+5', 'f1', 'f2', 'f3', 'alt+1', 'alt+2', 'alt+3']

HOTKEY_DISPLAY_NAMES = {
    'ctrl+1': 'Ctrl+1', 'ctrl+2': 'Ctrl+2', 'ctrl+3': 'Ctrl+3',
    'ctrl+4': 'Ctrl+4', 'ctrl+5': 'Ctrl+5',
    'f1': 'F1', 'f2': 'F2', 'f3': 'F3',
    'alt+1': 'Alt+1', 'alt+2': 'Alt+2', 'alt+3': 'Alt+3',
}

HOTKEY_EXCLUDED = {'nano4t'}

FEATURES_INFO = {
    'knife': {'name': '快刀', 'icon': '🔪', 'category': 'weapon'},
    'time': {'name': '无限时间', 'icon': '⏰', 'category': 'player'},
    'recoil': {'name': '无后座力', 'icon': '🎯', 'category': 'weapon'},
    'ammo': {'name': '无限子弹', 'icon': '🔫', 'category': 'weapon'},
    'movespeed': {'name': '滑板鞋', 'icon': '👟', 'category': 'player'},
    'ammoplus': {'name': '快速换弹', 'icon': '⚡', 'category': 'weapon'},
    'range': {'name': '剑气化丝', 'icon': '⚔️', 'category': 'weapon'},
    'gather': {'name': '聚怪', 'icon': '👾', 'category': 'other'},
    'gravity': {'name': '轻重力', 'icon': '🌌', 'category': 'player'},
    'aim': {'name': '自瞄', 'icon': '🎯', 'category': 'weapon'},
    'godmode': {'name': '金刚不坏', 'icon': '🛡️', 'category': 'player'},
    'speedgun': {'name': '射速变快', 'icon': '⚡', 'category': 'weapon'},
    'isbot': {'name': '天机傀儡', 'icon': '🧠', 'category': 'other'},
    'skillcd': {'name': '技能无冷却', 'icon': '✨', 'category': 'player'},
    'roundskip': {'name': '回合跳过', 'icon': '⏭️', 'category': 'other'},
    'nano4t': {'name': '多人生化特性', 'icon': '🧬', 'category': 'other'},
}

GRAVITY_PRESETS = {
    '月球': {'gravity': 0.2, 'jump': 2.0},
    '火星': {'gravity': 0.4, 'jump': 1.5},
    '轻': {'gravity': 0.6, 'jump': 1.3},
    '自定义': {'gravity': 1.0, 'jump': 1.0},
}

NANO4T_ATTRS = {
    0: ("基因变异", "缩短技能冷却时间", "ghost"),
    1: ("末日降临", "首波生化全部作为终结者登场", "ghost"),
    2: ("过度增长", "进化时获得额外HP", "ghost"),
    3: ("硬化", "减少受到的所有伤害", "ghost"),
    4: ("补给防御", "获取补给箱时增加防御力", "ghost"),
    5: ("钢铁利爪", "生化幽灵的攻击力与攻击范围增加", "ghost"),
    6: ("感染经验值", "成功感染后自身攻击力与HP都会增加", "ghost"),
    7: ("沸血", "获取补给箱时获得移速和攻速加成", "ghost"),
    8: ("终结者出现", "额外提供红色补给箱", "ghost"),
    9: ("不死契约", "死亡时出现墓碑，一段时间后复活", "ghost"),
    10: ("救世主", "回合开始时救世主英雄登场", "human"),
    11: ("致命一击", "击杀生化幽灵后攻击力增加", "human"),
    12: ("连发手雷", "提高手雷携带数量和攻击力", "human"),
    13: ("强力补给", "获取补给箱时增加攻击力（可叠加）", "human"),
    14: ("无限弹药", "无限弹药", "human"),
    15: ("快速装弹", "加快佣兵装弹速度", "human"),
    16: ("绝命生还", "所有佣兵均可使用特殊技能", "human"),
    17: ("特工", "所有佣兵均可使用特殊技能", "human"),
    18: ("英雄出现", "额外提供蓝色补给箱", "human"),
    19: ("致命攻击", "适用暴击伤害", "human"),
}


def get_feature_info(feature_id):
    return FEATURES_INFO.get(feature_id, {})
