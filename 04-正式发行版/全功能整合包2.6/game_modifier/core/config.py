import os
import sys
import json
from pathlib import Path

if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
    BASE_DIR = sys._MEIPASS  # PyInstaller 解压目录
    RESOURCE_DIR = os.path.join(BASE_DIR, "资源")
    PLUGINS_DIR = os.path.join(BASE_DIR, "game_modifier", "plugins")
    FEATURES_DIR = os.path.join(BASE_DIR, "features")  # features 在打包目录内
    # 用户可写数据重定向到 %LOCALAPPDATA%，避免写 Program Files（安装器打包规范 §7.1 方案A）
    _local_app_data = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~\\AppData\\Local")
    DATA_DIR = os.path.join(_local_app_data, "UCFModifier", "2.5", "data")
else:
    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BASE_DIR = APP_DIR
    RESOURCE_DIR = os.path.join(os.path.dirname(APP_DIR), "资源")
    PLUGINS_DIR = os.path.join(APP_DIR, "plugins")
    FEATURES_DIR = os.path.join(APP_DIR, "features")
    DATA_DIR = os.path.join(APP_DIR, "data")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

HOTKEYS_FILE = os.path.join(DATA_DIR, "hotkeys.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
NANO4T_FILE = os.path.join(DATA_DIR, "Nano-4T-selector.json")

HOTKEY_POSITIONS = ['ctrl+1', 'ctrl+2', 'ctrl+3', 'ctrl+4', 'ctrl+5', 'f1', 'f2', 'alt+1', 'alt+2']

HOTKEY_DISPLAY_NAMES = {
    'ctrl+1': 'Ctrl+1', 'ctrl+2': 'Ctrl+2', 'ctrl+3': 'Ctrl+3',
    'ctrl+4': 'Ctrl+4', 'ctrl+5': 'Ctrl+5',
    'f1': 'F1', 'f2': 'F2',
    'alt+1': 'Alt+1', 'alt+2': 'Alt+2',
}

DEDICATED_HOTKEY_ACTIONS = {
    'alt+1': {
        'feature_id': 'fixed_point_teleport',
        'action': 'savepoint',
        'label': '定点瞬移：保存点位1',
    },
    'alt+2': {
        'feature_id': 'fixed_point_teleport',
        'action': 'teleporttopoint',
        'label': '定点瞬移：瞬移到点位1',
    },
    'f1': {
        'feature_id': 'fixed_point_teleport',
        'action': 'savepoint2',
        'label': '定点瞬移：保存点位2',
    },
    'f2': {
        'feature_id': 'fixed_point_teleport',
        'action': 'teleporttopoint2',
        'label': '定点瞬移：瞬移到点位2',
    },
}

ROLE_TRANSFORM_HOTKEY_ACTIONS = {
    'alt+q': {
        "label": "本地玩家：选择英雄",
        "feature_id": "role_transform",
        "action": "trigger",
        "payload": {"action": "local_hero"},
    },
    'alt+w': {
        "label": "本地玩家：选择超级终结者",
        "feature_id": "role_transform",
        "action": "trigger",
        "payload": {"action": "local_terminator"},
    },
    'alt+e': {
        "label": "所有 Bot：随机英雄",
        "feature_id": "role_transform",
        "action": "trigger",
        "payload": {"action": "bot_hero"},
    },
    'alt+r': {
        "label": "所有 Bot：随机超级终结者",
        "feature_id": "role_transform",
        "action": "trigger",
        "payload": {"action": "bot_terminator"},
    },
}

ROLE_TRANSFORM_HOTKEY_DISPLAY_NAMES = {
    'alt+q': 'Alt+Q',
    'alt+w': 'Alt+W',
    'alt+e': 'Alt+E',
    'alt+r': 'Alt+R',
}

def _load_feature_manifests():
    features_dir = Path(FEATURES_DIR)
    manifests = {}
    if not features_dir.exists():
        return manifests
    for manifest_path in sorted(features_dir.glob("*/manifest.json")):
        if manifest_path.parent.name.startswith("_"):
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        feature_id = manifest.get("feature_id")
        if feature_id:
            manifests[feature_id] = manifest
    return manifests


def _build_features_info(manifests):
    return {
        feature_id: {
            "name": manifest.get("display_name", feature_id),
            "category": manifest.get("category", "other"),
        }
        for feature_id, manifest in manifests.items()
    }


def _build_hotkey_excluded(manifests):
    excluded = set()
    for feature_id, manifest in manifests.items():
        hotkey = manifest.get("hotkey", {})
        has_trigger = any(control.get("type") in {"switch", "button"} for control in manifest.get("controls", []))
        if hotkey.get("enabled") is not True or not has_trigger:
            excluded.add(feature_id)
    return excluded


_FEATURE_MANIFESTS = _load_feature_manifests()
FEATURES_INFO = _build_features_info(_FEATURE_MANIFESTS)
HOTKEY_EXCLUDED = _build_hotkey_excluded(_FEATURE_MANIFESTS)

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

# 武器快捷键配置
WEAPON_HOTKEYS_FILE = os.path.join(DATA_DIR, "weapon_hotkeys.json")

WEAPON_HOTKEY_POSITIONS = ['ctrl+z', 'ctrl+x', 'ctrl+c']

WEAPON_HOTKEY_DISPLAY_NAMES = {
    'ctrl+z': 'Ctrl+Z',
    'ctrl+x': 'Ctrl+X',
    'ctrl+c': 'Ctrl+C',
}
