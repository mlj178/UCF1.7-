from __future__ import annotations

import html
import importlib.util
import math
import re
from pathlib import Path

import generate_field_relation_graphs as graphs


ROOT = Path(__file__).resolve().parents[1]
DUMP = next(ROOT.rglob("dump.cs"))
HTML_OUT = (
    ROOT
    / "04-正式发行版"
    / "全功能整合包1.8"
    / "类关系分析"
    / "字段关系图"
    / "文档汇总"
    / "HTML"
)

MATCH_RULE_TARGETS = [
    "GameManager",
    "GameMode",
    "ModeBase",
    "ModeBase_Nano",
    "Player.RespawnType",
    "Team",
    "WeaponLimited",
]

BASIC_TYPES = {
    "bool",
    "byte",
    "char",
    "double",
    "float",
    "int",
    "long",
    "object",
    "sbyte",
    "short",
    "string",
    "uint",
    "ulong",
    "ushort",
}

UNITY_BASIC = {
    "GameObject",
    "Material",
    "RawImage",
    "Text",
    "Texture",
    "Vector2Int",
}

CLASS_SUMMARY = {
    "GameManager": "一局对战的全局总控。它保存玩家、阵营、模式、武器数据、角色/武器资源池，并通过事件把伤害、死亡、出生、回合开始等流程通知给其他系统。",
    "GameMode": "玩法模式枚举。它不是运行时对象，而是对局类型编号，用来决定当前局是团队竞技、个人竞技、特殊模式还是纳米/终结者模式。",
    "ModeBase": "玩法规则基类。它集中维护比分、回合、时间、复活、双方人数和计分板 UI，是具体模式规则的共同底座。",
    "ModeBase_Nano": "纳米模式规则扩展。它继承玩法规则基类，并额外保存纳米模式里死亡后转化或吸收相关的角色状态。",
    "Player.RespawnType": "玩家复活方式枚举。用于说明玩家死亡后按队伍出生点、原地或敌方区域等规则复活。",
    "Team": "阵营枚举。用于区分 BlackList、GlobalRisk 和中立对象，是玩家分队、胜负判断、HUD 阵营显示的基础值。",
    "WeaponLimited": "武器限制枚举。用于描述当前玩法或房间限制的武器类型，例如刀战、手枪战、狙击战。",
}

TYPE_SUMMARY = {
    "GameManager": CLASS_SUMMARY["GameManager"],
    "GameMode": CLASS_SUMMARY["GameMode"],
    "ModeBase": CLASS_SUMMARY["ModeBase"],
    "ModeBase_Nano": CLASS_SUMMARY["ModeBase_Nano"],
    "Player.RespawnType": CLASS_SUMMARY["Player.RespawnType"],
    "Team": CLASS_SUMMARY["Team"],
    "WeaponLimited": CLASS_SUMMARY["WeaponLimited"],
    "Player": "玩家战斗主体。保存生命、阵营、武器、输入、模型和 HUD 状态，是本机玩家、队友、敌人和 Bot 在战斗层的核心对象。",
    "NanoRole": "纳米模式角色身份。用于表示终结者、幽灵或人类等特殊模式身份，影响死亡转化和技能规则。",
    "HUD_PlayerRect": "计分板玩家条目 UI。用于显示玩家名称、阵营、存活、击杀死亡等对局状态。",
    "SimpleObjectPool": "简单对象池。用于复用计分板条目、临时 UI 或场景对象，减少频繁创建销毁。",
    "GameObject": "Unity 场景对象或预制体。这里多用于 UI 容器、玩家条目模板或模式对象生成。",
    "RawImage": "Unity UI 原始图片组件。用于显示计分板背景或模式相关图片。",
    "Texture": "Unity 贴图资源。用于计分板、模式提示或 UI 皮肤切换。",
    "Text": "Unity UI 文本组件。用于显示比分、回合、倒计时、模式提示等。",
    "Material": "Unity 材质资源。这里常用于倒计时闪烁、警告色或 UI 特效表现。",
    "Vector2Int": "二维整数值。用于比分、时间、回合等两个数字组合，例如 BL/GR 分数或分钟/秒。",
}

ENUM_VALUE_SUMMARY = {
    "GameMode": {
        "TeamDeath": "团队竞技。双方阵营按击杀数或目标分数决胜。",
        "DeathMatch": "个人竞技。更偏自由混战或个人击杀排名。",
        "Special": "特殊玩法入口。通常承载刀战、手枪战、狙击战等限制玩法。",
        "Nano3": "纳米模式变体之一。用于终结者/幽灵类感染玩法。",
        "Nano4": "纳米模式变体之一。用于不同人数或规则的纳米对局。",
        "Nano6": "纳米模式变体之一。代表另一套纳米规则配置。",
        "Nano4_Terminator": "终结者纳米模式。通常对应终结者身份、最终战或特殊胜负规则。",
    },
    "WeaponLimited": {
        "None": "不限制武器。玩家可按背包或模式默认规则使用武器。",
        "Knife": "刀战限制。主要允许近战武器。",
        "HandGun": "手枪战限制。主要允许副武器/手枪。",
        "Sniper": "狙击战限制。主要允许狙击枪。",
    },
    "Team": {
        "BlackList": "潜伏者/BL 阵营。GameManager 用 BL 列表维护该阵营玩家和存活对象。",
        "GlobalRisk": "保卫者/GR 阵营。GameManager 用 GR 列表维护该阵营玩家和存活对象。",
        "Neutral": "中立阵营。用于地图物件、无阵营实体或暂未分队状态。",
    },
    "Player.RespawnType": {
        "Team": "按己方队伍出生规则复活，常见于团队模式。",
        "Stay": "原地或当前位置附近复活，适合特殊复活规则。",
        "EnemyTeam": "按敌方阵营区域或反向出生规则复活，用于特殊玩法。",
    },
}


def load_game_manager_info():
    path = ROOT / "tools" / "generate_gamemanager_field_sample.py"
    spec = importlib.util.spec_from_file_location("gm_sample", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.FIELD_INFO, module.IGNORE_REASONS


GM_FIELD_INFO, GM_IGNORE_REASONS = load_game_manager_info()

FIELD_OVERRIDES = {
    "ModeBase": {
        "score": ("玩法规则/比分回合", "当前比分，通常两个整数分别代表 BL/GR 或左右两侧队伍分数。", "可读用于计分板和胜负分析；直接改会影响胜负判断。"),
        "currentRound": ("玩法规则/比分回合", "当前回合编号，用于回合制模式的流程推进和显示。", "适合查回合切换；修改要同步回合开始/结束流程。"),
        "targetRound": ("玩法规则/比分回合", "目标回合数，到达后可能触发整局结束。", "可作为修改局数上限的入口。"),
        "targetScore": ("玩法规则/比分回合", "目标分数，团队竞技或个人竞技中常用作胜利条件。", "可作为修改胜利分数的入口。"),
        "gameTime": ("玩法规则/时间复活", "整局时间配置，通常表示分钟/秒或时间上限。", "适合查限时对局；注意倒计时 UI 也会引用。"),
        "respawnTime": ("玩法规则/时间复活", "复活等待时间，控制玩家死亡后多久重新出生。", "可作为复活时间修改点。"),
        "BLOnLeft": ("玩法规则/阵营显示", "BL 阵营是否显示在左侧，用于左右比分和计分板阵营布局。", "基础 bool，关系图可忽略；UI 阵营错位时可查。"),
        "scoreBoardImage": ("HUD/UI/计分板", "计分板背景图片组件。", "改 UI 皮肤时可查；不影响核心规则。"),
        "scoreBoardTex": ("HUD/UI/计分板", "计分板背景贴图数组，用于不同模式或阵营布局切换。", "适合查模式 UI 资源。"),
        "scoreText_L": ("HUD/UI/计分板", "左侧比分文本。", "只影响显示；实际分数看 score。"),
        "scoreText_R": ("HUD/UI/计分板", "右侧比分文本。", "只影响显示；实际分数看 score。"),
        "roundText_T": ("HUD/UI/计分板", "回合标题或总回合文本。", "用于 UI 显示，不是规则源头。"),
        "roundText_C": ("HUD/UI/计分板", "当前回合文本。", "用于显示 currentRound。"),
        "restGameTime": ("玩法规则/时间复活", "剩余对局时间，通常为分钟/秒组合。", "可读用于倒计时；直接改要同步 UI 和结束判断。"),
        "timeText_M": ("HUD/UI/计分板", "倒计时分钟文本。", "显示层字段。"),
        "timeText_S": ("HUD/UI/计分板", "倒计时秒文本。", "显示层字段。"),
        "timeFlashMat": ("HUD/UI/计分板", "时间警告闪烁材质，用于临近结束时的 UI 强提醒。", "只影响表现。"),
        "playerCountBL": ("玩家与阵营统计", "BL 阵营玩家总数缓存。", "用于 HUD/胜负统计；要和 GameManager 阵营列表一致。"),
        "playerCountGR": ("玩家与阵营统计", "GR 阵营玩家总数缓存。", "用于 HUD/胜负统计；要和 GameManager 阵营列表一致。"),
        "aliveCountBL": ("玩家与阵营统计", "BL 阵营存活人数缓存。", "胜负判断和计分板都可能依赖。"),
        "aliveCountGR": ("玩家与阵营统计", "GR 阵营存活人数缓存。", "胜负判断和计分板都可能依赖。"),
        "rectContainer": ("HUD/UI/计分板", "计分板玩家条目的父容器。", "改 UI 布局时可查。"),
        "playerRectPrefab": ("HUD/UI/计分板", "计分板玩家条目预制体。", "可替换显示样式，但要保留 HUD_PlayerRect 组件。"),
        "playerRectPool": ("资源与对象池", "计分板条目对象池，用于复用玩家 UI 行。", "修改池逻辑要注意刷新和回收状态。"),
        "playerRect_BL": ("HUD/UI/计分板", "BL 阵营计分板玩家条目列表。", "用于刷新 BL 玩家 UI。"),
        "playerRect_GR": ("HUD/UI/计分板", "GR 阵营计分板玩家条目列表。", "用于刷新 GR 玩家 UI。"),
        "myPlayer": ("玩家与阵营统计", "本机玩家引用，模式规则可据此判断本机阵营、复活和 HUD 显示。", "读为主，不建议在模式里直接替换。"),
        "modeTip": ("HUD/UI/计分板", "模式提示文本数组，用于显示玩法说明或回合提示。", "适合改提示文案。"),
    },
    "ModeBase_Nano": {
        "asset": ("纳米/特殊规则", "纳米模式资源配置入口，保存终结者/幽灵/人类等模式资源和规则素材。", "查纳米模式角色资源、技能资源时优先看。"),
        "basicAsset": ("纳米/特殊规则", "纳米模式基础配置资源，通常保存通用数值、提示、基础表现资源。", "适合查纳米模式基础参数。"),
        "nanoTimerTip": ("HUD/UI/计分板", "纳米模式倒计时提示 HUD，用于显示感染、最终战或阶段计时。", "只影响显示；实际计时逻辑要看方法读写。"),
        "finalBattle": ("HUD/UI/计分板", "最终战 HUD 控件，用于纳米模式末期阶段提示和表现。", "查最终战 UI 或触发提示时重点看。"),
        "hpRecoverIcon": ("HUD/UI/计分板", "回血提示图标，纳米/终结者角色恢复生命时用于 UI 表现。", "改表现可查；规则数值不在这里。"),
        "gKeyTip": ("HUD/UI/计分板", "G 键技能或交互提示，提示玩家使用纳米模式特殊能力。", "查技能按键提示时有价值。"),
        "mark": ("HUD/UI/计分板", "击杀标记 HUD，用于纳米模式击杀、人类感染或连杀提示。", "查击杀反馈表现时重点看。"),
        "nanoClothIcon": ("HUD/UI/计分板", "纳米布料/身份图标对象，用于显示纳米相关状态或外观提示。", "Unity 对象引用，主要影响 UI/表现。"),
        "supplyBoxTip": ("HUD/UI/计分板", "补给箱提示 HUD，用于纳米模式补给箱刷新或拾取提示。", "查补给箱流程时有价值。"),
        "meleeKillNanoTip": ("HUD/UI/计分板", "近战击杀纳米提示，用于特殊击杀或转化反馈。", "查刀杀纳米奖励或提示时看它。"),
        "nanoKillMark": ("HUD/UI/计分板", "纳米击杀动画标记，用于单次击杀表现。", "只影响击杀表现。"),
        "nanoKillMark_MultiKill": ("HUD/UI/计分板", "纳米连杀动画标记，用于多杀反馈。", "查纳米连杀提示时看它。"),
        "thisRoundPlayer": ("玩家与阵营统计", "本回合参与玩家数量缓存，影响纳米身份分配、感染比例或胜负统计。", "基础 int，关系图可忽略；规则分析时要查读写点。"),
        "soldierAttackPower": ("纳米/特殊规则", "士兵/人类攻击力配置，可能影响人类对纳米角色的伤害倍率。", "适合查纳米模式伤害强化。"),
        "ignoreSoldierPowerWpnList": ("武器数据", "不受士兵攻击力加成影响的武器 ID 列表。", "查纳米模式武器伤害例外规则时重点看。"),
        "respawningPlayer": ("玩家与阵营统计", "正在复活倒计时的玩家列表。", "查纳米模式复活流程和倒计时 UI 时重点看。"),
        "<nanoRespawn_Melee>k__BackingField": ("纳米/特殊规则", "nanoRespawn_Melee 属性后备字段，表示近战击杀是否允许纳米复活或特殊复活规则。", "编译器字段，逻辑入口看属性和复活方法。"),
        "<nanoRespawn_Headshot>k__BackingField": ("纳米/特殊规则", "nanoRespawn_Headshot 属性后备字段，表示爆头击杀是否触发纳米复活限制或特殊规则。", "编译器字段，逻辑入口看属性和复活方法。"),
        "supplyBoxPool": ("资源与对象池", "补给箱对象池，用于纳米模式补给箱生成和回收。", "查补给箱刷新、回收和性能时重点看。"),
        "randomPlayerList": ("玩家与阵营统计", "随机玩家列表，用于抽取纳米角色、终结者或特殊身份。", "查身份随机分配时重点看。"),
        "nanoLevelUpNeedExp": ("纳米/特殊规则", "纳米升级所需经验数组，控制不同等级升级门槛。", "可作为等级成长参数入口。"),
        "BornNanoGhostHP": ("纳米/特殊规则", "出生时纳米幽灵生命值。", "可作为纳米角色初始血量修改点。"),
        "AbsorbNeedTime": ("纳米/特殊规则", "吸收所需时间，控制纳米模式吸收/感染动作持续时长。", "查吸收机制和交互耗时。"),
        "AbsorbCheckCount": ("纳米/特殊规则", "吸收检查次数，可能用于持续判定吸收是否完成或中断。", "查吸收判定稳定性和频率。"),
        "Text_GetSkill": ("HUD/UI/计分板", "获得技能提示文本。", "适合改纳米模式提示文案。"),
        "Tip_Infect": ("HUD/UI/计分板", "感染提示文本数组，用于不同感染场景的 HUD 提示。", "适合改感染提示文案。"),
    },
}

CATEGORY_ORDER = [
    "预制体/场景生成",
    "玩家与阵营列表",
    "玩法规则",
    "资源与对象池",
    "武器数据",
    "武器与伤害结算",
    "伤害/死亡/玩家事件",
    "Bot/AI/寻路",
    "地图与出生点",
    "纳米/特殊规则",
    "HUD/UI/计分板",
    "角色模型与表现资源",
    "相机/视角/渲染",
    "数据结构/工具/对象池",
    "Unity基础组件/外部类型",
    "回合与回收/镜头控制",
    "玩法规则/比分回合",
    "玩法规则/时间复活",
    "玩法规则/阵营显示",
    "玩家与阵营统计",
    "可忽略字段",
]


def class_blocks(text: str) -> dict[str, str]:
    return graphs.class_blocks(text)


def extract_type_body(type_name: str, text: str, kind: str = "class") -> str:
    if kind == "enum":
        pattern = (
            r"(?m)^(?:public|private|protected|internal)?\s*enum\s+"
            + re.escape(type_name)
            + r"(?=\s|:|//|\n)[^\n]*"
        )
    else:
        pattern = (
            r"(?m)^(?:public|private|protected|internal)?\s*(?:static\s+)?(?:class|struct)\s+"
            + re.escape(type_name)
            + r"(?=\s|:|//|\n)[^\n]*"
        )
    match = re.search(pattern, text)
    if not match:
        return ""
    brace_start = text.find("{", match.end())
    if brace_start < 0:
        return ""
    depth = 0
    for index in range(brace_start, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[brace_start + 1 : index]
    return ""


def parse_fields(type_name: str, text: str) -> list[dict[str, str]]:
    body = extract_type_body(type_name, text)
    if not body:
        return []
    fields_block = re.search(
        r"\t// Fields\n(?P<fields>.*?)(?:\n\n\t// Properties|\n\n\t// Methods|\n\})",
        body,
        re.S,
    )
    if not fields_block:
        return []
    fields = []
    attrs: list[str] = []
    for line in fields_block.group("fields").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("["):
            attrs.append(stripped)
            continue
        match = re.match(
            r"(?P<access>public|private|protected|internal)\s+"
            r"(?P<static>static\s+)?"
            r"(?P<type>.+?)\s+"
            r"(?P<name>[^\s;]+);"
            r"\s*//\s*(?P<offset>0x[0-9A-Fa-f]+)",
            stripped,
        )
        if not match:
            attrs = []
            continue
        name = match.group("name")
        category, meaning, advice = explain_field(type_name, name, match.group("type"))
        ignored, reason = ignore_info(type_name, name, match.group("type"), bool(attrs))
        fields.append(
            {
                "access": match.group("access"),
                "static": "static" if match.group("static") else "instance",
                "type": match.group("type"),
                "name": name,
                "offset": match.group("offset"),
                "compiler": "是" if attrs else "否",
                "category": category,
                "meaning": meaning,
                "advice": advice,
                "ignored": "是" if ignored else "否",
                "ignore_reason": reason,
            }
        )
        attrs = []
    return fields


def parse_enum_values(type_name: str, text: str) -> list[dict[str, str]]:
    body = extract_type_body(type_name, text, kind="enum")
    if not body:
        return []
    values = []
    for line in body.splitlines():
        stripped = line.strip().rstrip(",")
        const_match = re.match(r"public const .+? (?P<name>[A-Za-z_]\w*) = (?P<value>-?\d+);", stripped)
        if not const_match:
            continue
        name = const_match.group("name")
        values.append(
            {
                "name": name,
                "value": const_match.group("value"),
                "meaning": ENUM_VALUE_SUMMARY.get(type_name, {}).get(name, "枚举值，用于玩法规则中的状态判断。"),
            }
        )
    return values


def explain_field(owner: str, name: str, typ: str) -> tuple[str, str, str]:
    if owner == "GameManager" and name in GM_FIELD_INFO:
        info = GM_FIELD_INFO[name]
        return info["category"], info["meaning"], info["advice"]
    if owner in FIELD_OVERRIDES and name in FIELD_OVERRIDES[owner]:
        return FIELD_OVERRIDES[owner][name]

    lowered = f"{name} {typ}".lower()
    if "prefab" in lowered or typ == "GameObject":
        return "预制体/场景生成", f"{name} 保存 Unity 场景对象或预制体引用，用于运行时生成、挂载或组织对局对象。", "修改前确认组件完整。"
    if any(key in lowered for key in ("weapon", "wpn", "ammo", "gun", "knife", "grenade", "missile", "damage", "death", "hit", "recoil")):
        return "武器与伤害结算", f"{name} 与武器、弹药、命中、伤害或死亡结算有关，是战斗数值和反馈链路的一部分。", "适合查武器参数、伤害结算或击杀反馈；修改时注意玩法规则是否二次限制。"
    if any(key in lowered for key in ("bot", "ai", "path", "guard", "enemy", "target", "seeker", "node", "jump", "saunter")):
        return "Bot/AI/寻路", f"{name} 与 Bot 行为、目标选择、寻路或 AI 状态有关，用于控制电脑玩家移动和战斗决策。", "适合查 AI 行为；修改前确认寻路状态和目标缓存同步。"
    if any(key in lowered for key in ("map", "spawn", "trigger", "supply", "point", "area")):
        return "地图与出生点", f"{name} 与地图点位、出生点、触发区域或补给点有关，用于组织场景玩法空间。", "适合查出生、补给、地图互动；改点位要注意阵营和模式限制。"
    if any(key in lowered for key in ("nano", "terminator", "ghost", "absorb", "infect", "finalbattle")):
        return "纳米/特殊规则", f"{name} 与纳米、终结者、感染、吸收或特殊模式阶段有关。", "适合查特殊模式规则和表现；修改时注意身份转换和胜负条件。"
    if any(key in lowered for key in ("camera", "fov", "view", "render", "thermal", "cinemachine", "volume", "material", "renderer")):
        return "相机/视角/渲染", f"{name} 与相机视角、FOV、观战、渲染材质或后处理表现有关。", "多为表现层字段；改动前确认是否影响第一人称/观战视角。"
    if any(key in lowered for key in ("character", "model", "mdl", "anim", "voice", "effect", "fx", "helmet", "skin", "cloth")):
        return "角色模型与表现资源", f"{name} 与角色模型、动画、语音、特效、材质或外观资源有关。", "适合查角色外观和表现；替换资源时要确认骨骼、挂点和动画匹配。"
    if "player" in lowered or "team" in lowered or "alive" in lowered:
        return "玩家与阵营统计", f"{name} 与玩家、阵营或存活统计相关，用于对局胜负、复活和 HUD 显示。", "读为主；修改时要同步 GameManager 和 UI。"
    if "score" in lowered or "round" in lowered or "mode" in lowered:
        return "玩法规则/比分回合", f"{name} 属于比分、回合或模式规则字段。", "适合查规则入口；直接改会影响胜负流程。"
    if "time" in lowered or "respawn" in lowered:
        return "玩法规则/时间复活", f"{name} 与对局时间、倒计时或复活等待有关。", "适合查限时或复活功能。"
    if typ in ("Text", "RawImage", "Texture", "Material") or "hud" in lowered or "rect" in lowered or "tip" in lowered:
        return "HUD/UI/计分板", f"{name} 是 UI 或计分板表现字段。", "只改显示通常风险较低，但不要当规则源头。"
    if any(key in lowered for key in ("pool", "dict", "dictionary", "data", "list", "array", "cache", "config", "asset")):
        return "数据结构/工具/对象池", f"{name} 保存数据表、列表、缓存、资源配置或对象池，是其他系统读取运行数据的支撑字段。", "适合查数据来源和对象生命周期；修改时注意引用一致性。"
    if typ in UNITY_BASIC or typ.startswith("Vector") or typ in ("Transform", "Sprite", "Image", "Animation", "Animator", "AudioClip", "AudioSource", "ParticleSystem"):
        return "Unity基础组件/外部类型", f"{name} 保存 Unity 基础组件或资源引用，用于连接脚本逻辑和场景/表现对象。", "多为表现或挂载引用；修改前确认场景对象存在。"
    return "数据结构/工具/对象池", f"{name} 保存 {typ} 类型的运行时引用或配置值，用于支撑 {owner} 的当前系统职责。", "先按字段所属系统读取；需要修改时优先追踪该字段的读写方法。"


def ignore_info(owner: str, name: str, typ: str, compiler_generated: bool) -> tuple[bool, str]:
    if owner == "GameManager" and name in GM_IGNORE_REASONS:
        return True, GM_IGNORE_REASONS[name]
    normalized = normalize_type(typ)
    if compiler_generated:
        return True, "编译器生成的属性后备字段，逻辑入口应优先看属性或方法。"
    if normalized in BASIC_TYPES:
        return True, f"基础值类型 {normalized}，不作为类关系节点；但字段仍计入总数。"
    if "Event" in typ or typ.startswith("Action") or "Delegate" in typ:
        return True, "委托/事件订阅链，不作为普通对象字段关系统计；但对调用链分析有价值。"
    return False, ""


def normalize_type(typ: str) -> str:
    typ = typ.strip()
    if typ.endswith("[]"):
        typ = typ[:-2]
    list_match = re.match(r"(?:List|IList|IEnumerable)<(.+)>", typ)
    if list_match:
        return normalize_type(list_match.group(1))
    dict_match = re.match(r"Dictionary<[^,]+,\s*(.+)>", typ)
    if dict_match:
        return normalize_type(dict_match.group(1).rstrip(">"))
    return typ


def relation_types(owner: str, fields: list[dict[str, str]]) -> list[tuple[str, str, str]]:
    found: dict[str, list[str]] = {}
    for field in fields:
        typ = normalize_type(field["type"])
        if typ in BASIC_TYPES:
            continue
        if typ.startswith("Action") or "Event" in typ or "Delegate" in typ:
            continue
        if typ.startswith(owner + "."):
            continue
        found.setdefault(typ, []).append(field["name"])
    rows = []
    for typ, names in sorted(found.items(), key=lambda item: item[0].lower()):
        desc = TYPE_SUMMARY.get(typ) or graphs.analysis_for_type(typ)
        rows.append((typ, " / ".join(names), desc))
    return rows


def fields_from_body(owner: str, body: str) -> list[dict[str, str]]:
    fields_block = re.search(
        r"\t// Fields\n(?P<fields>.*?)(?:\n\n\t// Properties|\n\n\t// Methods|\n\})",
        body,
        re.S,
    )
    if not fields_block:
        return []
    fields = []
    attrs: list[str] = []
    for line in fields_block.group("fields").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("["):
            attrs.append(stripped)
            continue
        match = re.match(
            r"(?P<access>public|private|protected|internal)\s+"
            r"(?P<static>static\s+)?"
            r"(?P<type>.+?)\s+"
            r"(?P<name>[^\s;]+);"
            r"\s*//\s*(?P<offset>0x[0-9A-Fa-f]+)",
            stripped,
        )
        if not match:
            attrs = []
            continue
        category, meaning, advice = explain_field(owner, match.group("name"), match.group("type"))
        ignored, reason = ignore_info(owner, match.group("name"), match.group("type"), bool(attrs))
        fields.append(
            {
                "access": match.group("access"),
                "static": "static" if match.group("static") else "instance",
                "type": match.group("type"),
                "name": match.group("name"),
                "offset": match.group("offset"),
                "compiler": "是" if attrs else "否",
                "category": category,
                "meaning": meaning,
                "advice": advice,
                "ignored": "是" if ignored else "否",
                "ignore_reason": reason,
            }
        )
        attrs = []
    return fields


def all_direct_field_relations(text: str) -> dict[str, list[tuple[str, str]]]:
    blocks = class_blocks(text)
    relations: dict[str, list[tuple[str, str]]] = {}
    for owner, body in blocks.items():
        fields = fields_from_body(owner, body)
        for field in fields:
            typ = normalize_type(field["type"])
            if typ in BASIC_TYPES or typ.startswith("Action") or "Event" in field["type"]:
                continue
            relations.setdefault(typ, []).append((owner, field["name"]))
    return relations


def render_rows(fields: list[dict[str, str]]) -> str:
    rows = []
    for idx, field in enumerate(fields, start=1):
        rows.append(
            f"""
            <tr data-page="{math.ceil(idx / 15)}" data-category="{html.escape(field['category'])}">
              <td class="num">{idx}</td>
              <td><strong>{html.escape(field['name'])}</strong><span>{html.escape(field['access'])} / {field['static']} / offset {field['offset']}</span></td>
              <td><code>{html.escape(field['type'])}</code></td>
              <td><b>{html.escape(field['category'])}</b><p>{html.escape(field['meaning'])}</p></td>
              <td><p>{html.escape(field['advice'])}</p>{ignore_badge(field)}</td>
            </tr>
            """
        )
    return "\n".join(rows)


def ignore_badge(field: dict[str, str]) -> str:
    if field["ignored"] != "是":
        return '<span class="badge keep">纳入重点分析</span>'
    return f'<span class="badge ignore">可忽略</span><small>{html.escape(field["ignore_reason"])}</small>'


def render_enum_rows(values: list[dict[str, str]]) -> str:
    return "\n".join(
        f"""
        <tr>
          <td class="num">{idx}</td>
          <td><strong>{html.escape(value['name'])}</strong></td>
          <td><code>{html.escape(value['value'])}</code></td>
          <td colspan="2"><p>{html.escape(value['meaning'])}</p></td>
        </tr>
        """
        for idx, value in enumerate(values, start=1)
    )


def render_category_cards(fields: list[dict[str, str]]) -> str:
    used = [category for category in CATEGORY_ORDER if any(field["category"] == category for field in fields)]
    return "\n".join(
        f"""
        <article class="stat-card">
          <strong>{html.escape(category)}</strong>
          <span>{sum(1 for field in fields if field['category'] == category)} 个字段</span>
          <p>{html.escape(category_note(category))}</p>
        </article>
        """
        for category in used
    )


def category_note(category: str) -> str:
    notes = {
        "预制体/场景生成": "负责 Unity 对象生成、容器挂载或预制体引用。",
        "玩家与阵营列表": "负责记录玩家、阵营、存活状态和队伍列表。",
        "玩法规则": "负责模式、限制、胜负或特殊规则开关。",
        "资源与对象池": "负责资源索引和对象复用。",
        "武器数据": "负责武器实例和配置表查找。",
        "伤害/死亡/玩家事件": "负责伤害、死亡、出生、加入、回合开始等通知链。",
        "回合与回收/镜头控制": "负责回合清理、掉落回收或镜头切换线索。",
        "玩法规则/比分回合": "负责比分、目标分数、目标回合和回合推进。",
        "玩法规则/时间复活": "负责对局倒计时、剩余时间和复活等待。",
        "玩法规则/阵营显示": "负责 BL/GR 在 UI 或规则中的方向和位置。",
        "玩家与阵营统计": "负责双方人数、存活人数和本机玩家引用。",
        "HUD/UI/计分板": "负责比分、时间、玩家条目和模式提示显示。",
        "角色模型与表现资源": "负责角色模型、动画、声音、特效、材质和外观资源。",
        "纳米/特殊规则": "负责纳米模式身份、死亡转化或特殊规则。",
        "武器与伤害结算": "负责武器、弹药、命中、伤害、死亡和击杀反馈。",
        "Bot/AI/寻路": "负责电脑玩家目标、路径、动作和决策状态。",
        "地图与出生点": "负责地图点位、出生点、触发区域和补给空间。",
        "相机/视角/渲染": "负责玩家视角、观战、FOV、材质和渲染表现。",
        "数据结构/工具/对象池": "负责列表、字典、缓存、配置和对象复用。",
        "Unity基础组件/外部类型": "负责 Unity 组件、资源和外部类型引用。",
        "可忽略字段": "不进入类关系图的字段，但仍保留统计。",
    }
    return notes.get(category, "该分类用于聚合同类字段，方便快速筛选。")


def render_relation_nodes(rows: list[tuple[str, str, str]]) -> str:
    if not rows:
        return '<p class="section-note">没有字段直接保存其他主要类型。</p>'
    return "\n".join(
        f"""
        <div class="node">
          <b>{html.escape(typ)}</b>
          <span>字段依据：{html.escape(fields)}</span>
          <p>{html.escape(desc)}</p>
        </div>
        """
        for typ, fields, desc in rows
    )


def render_external_holders(type_name: str, relations: dict[str, list[tuple[str, str]]]) -> str:
    holders = [
        (owner, field)
        for owner, field in relations.get(type_name, [])
        if owner != type_name and "<" not in owner and ">" not in owner and not owner.startswith(type_name + ".")
    ]
    if not holders:
        return ""
    grouped: dict[str, list[str]] = {}
    for owner, field in holders:
        grouped.setdefault(owner, []).append(field)
    nodes = "\n".join(
        f'<div class="node"><b>{html.escape(owner)}</b><span>字段依据：{html.escape(" / ".join(names))}</span><p>{html.escape(TYPE_SUMMARY.get(owner) or graphs.analysis_for_type(owner))}</p></div>'
        for owner, names in sorted(grouped.items())
    )
    return f"""
    <section class="panel section-panel">
      <h2 style="margin-top:0">谁保存了这个类</h2>
      <p class="section-note">只统计 dump.cs 里字段类型直接使用 {html.escape(type_name)} 的类。</p>
      <div class="nodes">{nodes}</div>
    </section>
    """


def render_page(type_name: str, text: str, relations: dict[str, list[tuple[str, str]]]) -> str:
    fields = parse_fields(type_name, text)
    enum_values = parse_enum_values(type_name, text)
    is_enum = bool(enum_values)
    total = len(fields)
    ignored = sum(1 for field in fields if field["ignored"] == "是")
    focused = total - ignored
    pages = max(1, math.ceil(total / 15))
    relation_nodes = render_relation_nodes(relation_types(type_name, fields))
    category_options = "\n".join(
        f'<option value="{html.escape(category)}">{html.escape(category)}（{sum(1 for field in fields if field["category"] == category)}）</option>'
        for category in CATEGORY_ORDER
        if any(field["category"] == category for field in fields)
    )
    external_holders = render_external_holders(type_name, relations)
    category_stats = render_category_cards(fields)
    if fields:
        detail_table = render_field_table(type_name, fields, category_options, total)
    elif is_enum:
        detail_table = render_enum_table(type_name, enum_values)
    else:
        detail_table = render_empty_detail(type_name)
    if fields:
        stats_cards = category_stats
    elif enum_values:
        stats_cards = f'<article class="stat-card"><strong>枚举值</strong><span>{len(enum_values)} 个值</span><p>该类型是枚举，没有普通字段；页面展示枚举值和反向保存者。</p></article>'
    else:
        stats_cards = '<article class="stat-card"><strong>无字段</strong><span>0 个字段</span><p>dump.cs 中没有该类型的字段声明，通常是 Unity 基础类型、外部类型、空壳类型或只通过方法使用的类型。</p></article>'
    return PAGE_TEMPLATE.format(
        title=html.escape(type_name),
        summary=html.escape(CLASS_SUMMARY.get(type_name, graphs.analysis_for_type(type_name))),
        total=total,
        focused=focused,
        ignored=ignored,
        pages=pages,
        relation_nodes=relation_nodes,
        external_holders=external_holders,
        stats_cards=stats_cards,
        detail_table=detail_table,
        enum_count=len(enum_values),
    )


def render_field_table(type_name: str, fields: list[dict[str, str]], category_options: str, total: int) -> str:
    return f"""
    <h2>字段完整说明</h2>
    <div class="toolbar">
      <div class="filters">
        <label for="categoryFilter">字段系统分类</label>
        <select id="categoryFilter">
          <option value="全部">全部字段（{total}）</option>
          {category_options}
        </select>
      </div>
      <div class="pager" id="pager"></div>
      <div class="hint">当前显示 <span id="pageLabel">第 1 页</span>，筛选后 <span id="visibleCount">{total}</span> 个字段；可忽略字段不会遗漏，只是不进入主要类关系判断。</div>
    </div>
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>字段</th>
          <th>类型</th>
          <th>功能分类与解释</th>
          <th>修改/忽略建议</th>
        </tr>
      </thead>
      <tbody>{render_rows(fields)}</tbody>
    </table>
    <p class="footnote">忽略规则：基础值字段、编译器生成后备字段、Action/事件委托字段不作为“类保存类”的关系图节点；但本页仍逐项解释并计入总数。</p>
    """


def render_enum_table(type_name: str, values: list[dict[str, str]]) -> str:
    return f"""
    <h2>枚举值说明</h2>
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>枚举值</th>
          <th>数值</th>
          <th colspan="2">功能说明</th>
        </tr>
      </thead>
      <tbody>{render_enum_rows(values)}</tbody>
    </table>
    <p class="footnote">{html.escape(type_name)} 是枚举类型，没有普通字段；它的价值主要体现在被哪些类字段保存、以及各枚举值在玩法规则里的含义。</p>
    """


def render_empty_detail(type_name: str) -> str:
    return f"""
    <h2>字段说明</h2>
    <section class="panel section-panel">
      <p>{html.escape(type_name)} 在 dump.cs 中没有普通字段或枚举值。它通常属于 Unity 基础组件、外部库类型、空壳类型，或者只通过方法和继承关系参与逻辑。本页重点看“谁保存了这个类”，用反向字段关系判断它在哪些系统里被使用。</p>
    </section>
    """


PAGE_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} 字段关系图与字段说明</title>
  <style>
    :root {{ --bg:#f4f6f8; --panel:#ffffff; --ink:#1f2937; --muted:#667085; --line:#d9e1ec; --blue:#2457a6; --green:#207450; --amber:#9a5b13; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--ink); font-family:"Microsoft YaHei","Segoe UI",Arial,sans-serif; }}
    .page {{ max-width:1360px; margin:0 auto; padding:18px; }}
    header,.panel,table {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; }}
    header {{ padding:18px 20px; }}
    h1 {{ margin:0 0 8px; font-size:26px; letter-spacing:0; }}
    h2 {{ margin:26px 0 12px; font-size:20px; }}
    p {{ margin:0; line-height:1.65; }}
    .summary {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin-top:16px; }}
    .metric {{ border:1px solid var(--line); border-radius:8px; padding:12px; background:#fafcff; }}
    .metric strong {{ display:block; font-size:24px; color:var(--blue); }}
    .metric span {{ color:var(--muted); font-size:13px; }}
    .graph {{ display:grid; grid-template-columns:1fr 1.1fr; gap:14px; margin-top:16px; }}
    .panel {{ padding:16px; }}
    .core {{ border:2px solid var(--blue); background:#eef5ff; border-radius:8px; padding:16px; }}
    .core strong {{ display:block; font-size:24px; color:var(--blue); margin-bottom:8px; }}
    .section-panel {{ margin-top:14px; }}
    .section-note {{ color:var(--muted); font-size:13px; margin-bottom:12px; }}
    .nodes {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; margin-top:12px; }}
    .node {{ border:1px solid #cbd8e8; background:#fbfdff; border-radius:8px; padding:10px; min-height:112px; }}
    .node b {{ display:block; color:var(--green); margin-bottom:4px; }}
    .node span {{ display:block; color:var(--muted); font-size:13px; line-height:1.45; }}
    .node p {{ color:#344054; font-size:13px; line-height:1.55; margin-top:8px; }}
    .stats {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; }}
    .stat-card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:12px; min-height:116px; }}
    .stat-card strong {{ display:block; font-size:16px; margin-bottom:6px; }}
    .stat-card span {{ display:inline-block; color:#fff; background:var(--blue); border-radius:999px; padding:3px 9px; font-size:12px; margin-bottom:8px; }}
    .stat-card p {{ color:var(--muted); font-size:13px; }}
    .toolbar {{ display:flex; align-items:center; justify-content:space-between; gap:12px; margin:16px 0 8px; flex-wrap:wrap; }}
    .filters,.pager {{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; }}
    button,select {{ border:1px solid var(--line); background:#fff; color:var(--ink); border-radius:6px; padding:8px 12px; cursor:pointer; font:inherit; }}
    button.active {{ background:var(--blue); color:#fff; border-color:var(--blue); }}
    .hint,.footnote {{ color:var(--muted); font-size:13px; }}
    table {{ width:100%; border-collapse:separate; border-spacing:0; overflow:hidden; }}
    th,td {{ padding:11px 12px; border-bottom:1px solid #edf1f6; vertical-align:top; text-align:left; }}
    th {{ background:#f8fafc; font-size:13px; color:#344054; }}
    tr:last-child td {{ border-bottom:0; }}
    td.num {{ width:44px; color:var(--muted); }}
    td strong {{ display:block; margin-bottom:4px; }}
    td span, small {{ display:block; color:var(--muted); font-size:12px; line-height:1.45; }}
    code {{ white-space:nowrap; color:#344054; background:#f3f6fa; border:1px solid #e0e7ef; border-radius:5px; padding:2px 5px; }}
    .badge {{ display:inline-block; border-radius:999px; padding:3px 8px; font-size:12px; margin-top:8px; }}
    .badge.keep {{ background:#eaf7ef; color:var(--green); }}
    .badge.ignore {{ background:#fff4e5; color:var(--amber); }}
    .footnote {{ margin-top:14px; }}
    @media (max-width: 900px) {{ .summary,.graph,.stats,.nodes {{ grid-template-columns:1fr; }} table {{ font-size:13px; }} code {{ white-space:normal; }} }}
  </style>
</head>
<body>
  <main class="page">
    <header>
      <h1>{title} 字段关系图与字段说明</h1>
      <p>{summary}</p>
      <div class="summary">
        <div class="metric"><strong>{total}</strong><span>dump.cs 中字段总数</span></div>
        <div class="metric"><strong>{focused}</strong><span>建议重点分析字段</span></div>
        <div class="metric"><strong>{ignored}</strong><span>可忽略但已统计字段</span></div>
        <div class="metric"><strong>{pages}</strong><span>字段表分页，每页 15 行</span></div>
      </div>
    </header>
    <section class="graph">
      <div class="panel"><div class="core"><strong>{title}</strong><p>{summary}</p></div></div>
      <div class="panel"><h2 style="margin-top:0">它直接保存的主要类型</h2><div class="nodes">{relation_nodes}</div></div>
    </section>
    {external_holders}
    <h2>字段系统分类统计</h2>
    <section class="stats">{stats_cards}</section>
    {detail_table}
  </main>
  <script>
    const rows = Array.from(document.querySelectorAll('tbody tr[data-page]'));
    const filter = document.getElementById('categoryFilter');
    const pager = document.getElementById('pager');
    const label = document.getElementById('pageLabel');
    const visibleCount = document.getElementById('visibleCount');
    const pageSize = 15;
    let currentPage = 1;
    function matchingRows() {{
      if (!filter) return rows;
      const category = filter.value;
      return rows.filter(row => category === '全部' || row.dataset.category === category);
    }}
    function renderPager(totalPages) {{
      if (!pager) return;
      pager.innerHTML = '';
      for (let page = 1; page <= totalPages; page++) {{
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = '第 ' + page + ' 页';
        button.className = page === currentPage ? 'active' : '';
        button.addEventListener('click', () => {{ currentPage = page; updateTable(); }});
        pager.appendChild(button);
      }}
    }}
    function updateTable() {{
      const matched = matchingRows();
      const totalPages = Math.max(1, Math.ceil(matched.length / pageSize));
      if (currentPage > totalPages) currentPage = totalPages;
      const start = (currentPage - 1) * pageSize;
      const visibleSet = new Set(matched.slice(start, start + pageSize));
      rows.forEach(row => row.style.display = visibleSet.has(row) ? '' : 'none');
      if (visibleCount) visibleCount.textContent = matched.length;
      if (label) label.textContent = '第 ' + currentPage + ' 页';
      renderPager(totalPages);
    }}
    if (filter) filter.addEventListener('change', () => {{ currentPage = 1; updateTable(); }});
    updateTable();
  </script>
</body>
</html>
"""


def main() -> None:
    text = DUMP.read_text(encoding="utf-8", errors="ignore")
    relations = all_direct_field_relations(text)
    HTML_OUT.mkdir(parents=True, exist_ok=True)
    targets = sorted(
        path.name[: -len("字段关系图.html")]
        for path in HTML_OUT.glob("*字段关系图.html")
    )
    for type_name in targets:
        page = render_page(type_name, text, relations)
        out = HTML_OUT / f"{type_name}字段关系图.html"
        out.write_text(page, encoding="utf-8")
        fields = parse_fields(type_name, text)
        enums = parse_enum_values(type_name, text)
        print(f"{type_name}: fields={len(fields)} enum_values={len(enums)} -> {out}")


if __name__ == "__main__":
    main()
