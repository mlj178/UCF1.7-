from __future__ import annotations

import html
import math
import re
from pathlib import Path


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
    / "GameManager字段关系图.html"
)


FIELD_INFO: dict[str, dict[str, str]] = {
    "playerPrefab": {
        "category": "预制体/场景生成",
        "meaning": "玩家对象预制体，GameManager 创建或初始化玩家实体时会依赖它。Unity 角度看，这是场景里生成 Player 的模板。",
        "advice": "可改，但风险高；替换预制体会影响玩家身上的控制、碰撞、模型和武器挂点。",
    },
    "botPrefab": {
        "category": "预制体/场景生成",
        "meaning": "Bot 对象预制体，用于生成电脑玩家。它通常带有 Bot AI、寻路、武器和实体组件。",
        "advice": "可改，用于替换 Bot 形态或测试 AI；要确认 Bot 脚本依赖组件齐全。",
    },
    "myPlayer": {
        "category": "玩家与阵营列表",
        "meaning": "本机玩家的全局引用。很多输入、相机、HUD、伤害反馈都会通过它找到当前操控的 Player。",
        "advice": "不建议直接改引用；功能开发更适合读取它，再改 Player 子系统。",
    },
    "gameMode": {
        "category": "玩法规则",
        "meaning": "当前对局玩法模式对象，决定爆破、团队、纳米等模式规则入口。",
        "advice": "可用于定位模式逻辑；直接替换实例风险较高，容易破坏回合和计分流程。",
    },
    "weaponLimited": {
        "category": "玩法规则",
        "meaning": "当前模式的武器限制规则，例如是否禁用某些枪、投掷物或特殊武器。",
        "advice": "适合做武器限制、解锁、禁用规则分析；修改前要确认 GameMode 是否也二次校验。",
    },
    "revengeEnable": {
        "category": "玩法规则",
        "meaning": "复仇相关开关，可能控制击杀后复仇提示、复仇判定或特殊得分。",
        "advice": "基础布尔值，可忽略于类关系图；若做击杀奖励功能，可追踪它的读写点。",
    },
    "gameModePrefab": {
        "category": "预制体/场景生成",
        "meaning": "玩法模式预制体，用于实例化当前规则控制器或模式相关对象。",
        "advice": "可用于查找模式入口；替换预制体会影响整局规则，不建议盲改。",
    },
    "entityBL_Alive": {
        "category": "玩家与阵营列表",
        "meaning": "BL 阵营当前存活实体列表。Entity 是 Player/Bot 等可受击对象的基础层。",
        "advice": "适合做存活统计、雷达、胜负判断分析；不要手动插入错误对象。",
    },
    "entityGR_Alive": {
        "category": "玩家与阵营列表",
        "meaning": "GR 阵营当前存活实体列表，用于和 BL 存活列表一起支撑回合胜负判断。",
        "advice": "可读用于统计；修改会直接影响胜负和 HUD 显示。",
    },
    "allPlayers": {
        "category": "玩家与阵营列表",
        "meaning": "对局内全部玩家数组，通常包括本机、其他玩家和 Bot 映射后的 Player 对象。",
        "advice": "适合枚举玩家；不要改变数组结构，容易造成 HUD/计分板不同步。",
    },
    "playersBL": {
        "category": "玩家与阵营列表",
        "meaning": "BL 阵营所有玩家列表，不只包含存活玩家。",
        "advice": "适合阵营人数统计、计分板分类；修改需同步存活列表。",
    },
    "playersBL_Alive": {
        "category": "玩家与阵营列表",
        "meaning": "BL 阵营存活玩家列表，粒度比 Entity 列表更偏 Player 层。",
        "advice": "适合判断玩家存活人数；不要和 entityBL_Alive 改出不一致。",
    },
    "playersGR": {
        "category": "玩家与阵营列表",
        "meaning": "GR 阵营所有玩家列表，支撑阵营队伍、计分板和回合初始化。",
        "advice": "可读为主；修改会影响队伍组织。",
    },
    "playersGR_Alive": {
        "category": "玩家与阵营列表",
        "meaning": "GR 阵营存活玩家列表，用于胜负、复活和 HUD 存活人数显示。",
        "advice": "可用于功能判断；直接改列表要同步死亡/复活流程。",
    },
    "<ace>k__BackingField": {
        "category": "可忽略字段",
        "meaning": "ace 属性的编译器生成后备字段，记录本局 ACE 或关键玩家引用。",
        "advice": "关系分析可忽略，因为应通过 ace 属性和相关方法看逻辑；统计中保留。",
    },
    "weaponAsset": {
        "category": "资源与对象池",
        "meaning": "武器资源配置入口，保存武器模型、图标、音效或数据索引。",
        "advice": "适合查武器资源加载；改资源引用前要确认 WeaponData 和实际 Weapon 一致。",
    },
    "characterAsset": {
        "category": "资源与对象池",
        "meaning": "角色资源配置入口，管理角色模型、皮肤、头像或角色表现资源。",
        "advice": "适合查角色替换、模型资源和角色外观；直接替换需保证动画骨骼匹配。",
    },
    "characterPool": {
        "category": "资源与对象池",
        "meaning": "角色对象池，按名称或 Key 复用角色相关对象，减少频繁实例化。",
        "advice": "适合查角色生成/回收；修改池逻辑会影响性能和对象生命周期。",
    },
    "weaponPool": {
        "category": "资源与对象池",
        "meaning": "武器对象池，复用枪械、投掷物或掉落武器对象。",
        "advice": "适合查武器生成、切枪和回收；池内对象状态必须清理干净。",
    },
    "WpnDictionary": {
        "category": "武器数据",
        "meaning": "武器实例字典，按 int ID 快速找到 Weapon 对象。",
        "advice": "适合做武器枚举、武器替换入口；不要破坏 ID 到实例的一致性。",
    },
    "WpnDataDictionary": {
        "category": "武器数据",
        "meaning": "武器配置数据字典，按 int ID 找 WeaponData，如伤害、弹药、类型等。",
        "advice": "适合做伤害、弹夹、射速等数据分析；修改要注意客户端/规则校验。",
    },
    "<gameRoundOver>k__BackingField": {
        "category": "可忽略字段",
        "meaning": "gameRoundOver 属性的编译器生成后备字段，表示当前回合是否结束。",
        "advice": "字段关系可忽略；开发时应优先查 gameRoundOver 属性和回合结束方法。",
    },
    "DamageEvent_InvalidCheck_Observers": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "伤害无效检查事件订阅链，通常在正式计算伤害前过滤无效命中。",
        "advice": "委托字段，关系图可忽略；做无敌、免伤、命中规则时值得追踪调用点。",
    },
    "DamageEvent_PreCal_Observers": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "伤害预计算事件订阅链，在伤害进入正式计算前调整数据。",
        "advice": "适合查伤害倍率、Buff、护甲前置处理；委托本身不作为类关系节点。",
    },
    "DamageEvent_PostCal_Observers": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "伤害计算后事件订阅链，用于根据最终伤害触发反馈或二次处理。",
        "advice": "适合查伤害结算后逻辑；不要把它当普通对象引用统计。",
    },
    "DamageEvent_Post_Observers": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "伤害事件最终通知链，可能负责 HUD 提示、音效、命中特效或统计。",
        "advice": "做伤害反馈功能时查它；委托字段不建议直接修改。",
    },
    "DeathEvent_Observers": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "通用死亡事件通知链，死亡后通知计分、HUD、特殊击杀等系统。",
        "advice": "适合查击杀提示、死亡流程；不要随意清空订阅。",
    },
    "DeathEvent_ForGameRule": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "给玩法规则使用的死亡事件链，通常由 GameMode 或 ModeBase 处理胜负和计分。",
        "advice": "查胜负判定、回合结束优先看它的订阅者。",
    },
    "firstAndLastKillChecker": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "首杀/终结击杀检查委托，用于特殊击杀称号或额外奖励判断。",
        "advice": "做击杀奖励、播报时有价值；关系统计中按委托忽略。",
    },
    "NewPlayerJoinEvent_Observers": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "新玩家加入对局事件，通知 HUD、队伍列表、初始化装备等系统。",
        "advice": "委托字段；查加入流程时追踪 add/remove 和触发点。",
    },
    "PlayerSpawnEvent_Observers": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "玩家出生事件，出生后通知相机、HUD、保护期、武器初始化等系统。",
        "advice": "适合查复活、出生保护和初始化；不要直接覆盖订阅链。",
    },
    "MyPlayerJoinEvent_Observers": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "本机玩家加入事件，只关注当前操控玩家进入对局后的初始化。",
        "advice": "查本机 HUD、输入、相机绑定时有价值；关系图按委托忽略。",
    },
    "MyPlayerSpawnEvent_Observers": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "本机玩家出生事件，触发第一人称视角、准星、武器界面等本地表现。",
        "advice": "适合开发本机复活/出生相关功能。",
    },
    "MyPlayerCasueDamageEvent_Observers": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "本机玩家造成伤害事件，可能用于命中反馈、伤害数字、任务统计。",
        "advice": "字段名疑似 Cause 拼写误差；查本机打中敌人的反馈时重点看它。",
    },
    "MyPlayerGetDamageEvent_Observers": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "本机玩家受到伤害事件，用于红屏、受击方向、音效或震动反馈。",
        "advice": "适合做受击提示分析；委托字段本身不作为对象关系。",
    },
    "MyPlayerKillEvent_Observers": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "本机玩家击杀事件，通知击杀标记、连杀、得分和任务系统。",
        "advice": "查击杀提示、连杀播报、奖励逻辑时优先看。",
    },
    "MyPlayerDeathEvent_Observers": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "本机玩家死亡事件，通知死亡镜头、复活倒计时、HUD 状态切换。",
        "advice": "适合查死亡后视角和复活流程。",
    },
    "NewGameRoundStart_Observer": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "新回合开始事件，通知各系统重置分数、状态、武器和 UI。",
        "advice": "做回合初始化功能时很关键；委托字段关系统计可忽略。",
    },
    "GetGrenadeFromBag_Observer": {
        "category": "伤害/死亡/玩家事件",
        "meaning": "从背包取得手雷事件，可能用于投掷物 HUD、弹药变化或模式限制检查。",
        "advice": "查投掷物背包和补给逻辑时有价值；委托字段可忽略于类关系。",
    },
    "recyclableObjects": {
        "category": "回合与回收/镜头控制",
        "meaning": "可回收对象列表，管理掉落武器、临时特效、地图物件等需要延迟清理的对象。",
        "advice": "适合查对象生命周期和性能；不要只删除列表项而不处理场景对象。",
    },
    "dropWpnRecycleTime": {
        "category": "回合与回收/镜头控制",
        "meaning": "掉落武器回收时间，控制地图上掉枪多久后被清理。",
        "advice": "基础 float，可忽略于类关系；可作为掉落武器保留时间的修改点。",
    },
    "playerCameraChanger": {
        "category": "回合与回收/镜头控制",
        "meaning": "玩家相机切换索引或计数，可能用于死亡观战时切换观察目标。",
        "advice": "基础 int，可忽略于类关系；查观战/死亡镜头切人时追踪它。",
    },
}

CATEGORY_ORDER = [
    "预制体/场景生成",
    "玩家与阵营列表",
    "玩法规则",
    "资源与对象池",
    "武器数据",
    "伤害/死亡/玩家事件",
    "回合与回收/镜头控制",
    "可忽略字段",
]

IGNORE_REASONS = {
    "<ace>k__BackingField": "编译器生成的属性后备字段，逻辑入口应看 ace 属性。",
    "<gameRoundOver>k__BackingField": "编译器生成的属性后备字段，逻辑入口应看 gameRoundOver 属性。",
    "revengeEnable": "基础 bool，不能形成类关系；只在复仇规则分析时追踪读写点。",
    "dropWpnRecycleTime": "基础 float，不能形成类关系；只在掉落武器回收时间分析时使用。",
    "playerCameraChanger": "基础 int，不能形成类关系；只在相机切换流程中追踪。",
}


def parse_game_manager_fields() -> list[dict[str, str]]:
    text = DUMP.read_text(encoding="utf-8", errors="ignore")
    match = re.search(
        r"public class GameManager : Singleton<GameManager>.*?\{\n\t// Fields\n(?P<fields>.*?)\n\n\t// Properties",
        text,
        re.S,
    )
    if not match:
        raise RuntimeError("GameManager fields block not found")

    fields: list[dict[str, str]] = []
    attrs: list[str] = []
    for line in match.group("fields").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("["):
            attrs.append(stripped)
            continue
        field_match = re.match(
            r"(?P<access>public|private|protected|internal)\s+"
            r"(?P<static>static\s+)?"
            r"(?P<type>.+?)\s+"
            r"(?P<name>[^\s;]+);"
            r"\s*//\s*(?P<offset>0x[0-9A-Fa-f]+)",
            stripped,
        )
        if not field_match:
            attrs = []
            continue
        name = field_match.group("name")
        info = FIELD_INFO.get(name)
        if not info:
            raise RuntimeError(f"Missing field analysis for {name}")
        fields.append(
            {
                "access": field_match.group("access"),
                "static": "static" if field_match.group("static") else "instance",
                "type": field_match.group("type"),
                "name": name,
                "offset": field_match.group("offset"),
                "compiler": "是" if attrs else "否",
                "category": info["category"],
                "meaning": info["meaning"],
                "advice": info["advice"],
                "ignored": "是" if name in IGNORE_REASONS or "Event" in field_match.group("type") or field_match.group("type").startswith("Action") else "否",
                "ignore_reason": IGNORE_REASONS.get(
                    name,
                    "委托/事件订阅链，不作为普通对象字段关系统计；但对调用链分析有价值。"
                    if ("Event" in field_match.group("type") or field_match.group("type").startswith("Action"))
                    else "",
                ),
            }
        )
        attrs = []
    return fields


def category_stats(fields: list[dict[str, str]]) -> dict[str, int]:
    return {cat: sum(1 for field in fields if field["category"] == cat) for cat in CATEGORY_ORDER}


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


def render_category_cards(fields: list[dict[str, str]]) -> str:
    stats = category_stats(fields)
    notes = {
        "预制体/场景生成": "负责把玩法、玩家、Bot 的 Unity 模板接入对局。",
        "玩家与阵营列表": "负责记录谁在场、属于哪边、是否存活，是胜负和 HUD 的基础。",
        "玩法规则": "负责当前模式、武器限制和特殊规则开关。",
        "资源与对象池": "负责角色/武器资源索引和对象复用。",
        "武器数据": "负责武器实例和配置表的全局查找。",
        "伤害/死亡/玩家事件": "负责把伤害、死亡、出生、加入、回合开始等流程广播给其他系统。",
        "回合与回收/镜头控制": "负责临时对象清理、掉落武器回收和观战镜头切换线索。",
        "可忽略字段": "不进入类关系图的字段，但仍保留统计，防止漏项。",
    }
    return "\n".join(
        f"""
        <article class="stat-card">
          <strong>{html.escape(cat)}</strong>
          <span>{stats[cat]} 个字段</span>
          <p>{html.escape(notes[cat])}</p>
        </article>
        """
        for cat in CATEGORY_ORDER
    )


TYPE_SUMMARY = {
    "Player": "玩家战斗主体。保存生命、阵营、武器、输入、模型和 HUD 相关状态，是本机玩家、队友、敌人和 Bot 映射到战斗层后的核心对象。",
    "Entity": "可受击实体基础层。GameManager 用它统一统计 BL/GR 双方存活目标，便于胜负、伤害、雷达和回合流程不只依赖 Player。",
    "GameMode": "玩法模式入口。决定当前对局采用哪套规则，例如回合流程、胜负条件、复活方式、计分规则和特殊模式逻辑。",
    "WeaponLimited": "武器限制规则。用于判断当前模式或房间是否允许某类武器、手雷、特殊装备进入战斗。",
    "WeaponAsset": "武器资源配置表。更偏 Unity 资源侧，负责把武器 ID/名称映射到模型、图标、音效或可生成对象。",
    "CharacterAsset": "角色资源配置表。负责角色模型、皮肤、头像、表现资源等，常用于角色生成和外观替换。",
    "NameKeyPool": "按名称或 Key 管理的对象池。GameManager 用它复用角色和武器对象，减少频繁 Instantiate/Destroy。",
    "Weapon": "战斗中的武器实例。代表已经生成出来、可以开火/换弹/掉落/回收的具体武器对象。",
    "WeaponData": "武器配置数据。通常保存伤害、弹药、射速、类型、限制等数值，是改武器参数时最值得查的对象。",
    "RecyclableObject": "可回收临时对象。用于掉落武器、临时特效或需要延迟清理的场景对象生命周期管理。",
    "GameObject": "Unity 场景对象或预制体。这里主要是玩家、Bot、模式控制器的 prefab 引用，用于运行时生成对象。",
}


def find_external_game_manager_holders() -> list[tuple[str, list[str]]]:
    text = DUMP.read_text(encoding="utf-8", errors="ignore")
    holders: list[tuple[str, list[str]]] = []
    for match in re.finditer(r"(?m)^public (?:class|struct) (?P<name>[^\s:]+).*?\{\n(?P<body>.*?)(?=^// Namespace:|\Z)", text, re.S):
        class_name = match.group("name")
        if class_name == "GameManager" or class_name.startswith("GameManager."):
            continue
        fields_block = re.search(r"\t// Fields\n(?P<fields>.*?)(?:\n\n\t// Properties|\n\n\t// Methods|\n\})", match.group("body"), re.S)
        if not fields_block:
            continue
        field_names = []
        for line in fields_block.group("fields").splitlines():
            stripped = line.strip()
            field_match = re.match(
                r"(?:public|private|protected|internal)\s+(?:static\s+)?(?P<type>.+?)\s+(?P<name>[^\s;]+);",
                stripped,
            )
            if field_match and field_match.group("type") == "GameManager":
                field_names.append(field_match.group("name"))
        if field_names:
            holders.append((class_name, field_names))
    return holders


def render_external_holders() -> str:
    holders = find_external_game_manager_holders()
    if not holders:
        return ""
    nodes = "\n".join(
        f'<div class="node"><b>{html.escape(owner)}</b><span>字段依据：{html.escape(" / ".join(names))}</span><p>{html.escape(TYPE_SUMMARY.get(owner, "该类字段直接保存 GameManager，可作为反向调用入口继续追踪。"))}</p></div>'
        for owner, names in holders
    )
    return f"""
    <section class="panel section-panel">
      <h2 style="margin-top:0">谁保存了这个类</h2>
      <p class="section-note">只统计 dump.cs 里字段类型直接声明为 GameManager 的类。没有直接保存者时，本区域自动隐藏。</p>
      <div class="nodes">{nodes}</div>
    </section>
    """


def render(fields: list[dict[str, str]]) -> str:
    total = len(fields)
    ignored = sum(1 for field in fields if field["ignored"] == "是")
    focused = total - ignored
    pages = math.ceil(total / 15)
    relation_types = [
        ("Player", "myPlayer / allPlayers / playersBL / playersBL_Alive / playersGR / playersGR_Alive / ace"),
        ("Entity", "entityBL_Alive / entityGR_Alive"),
        ("GameMode", "gameMode"),
        ("WeaponLimited", "weaponLimited"),
        ("WeaponAsset", "weaponAsset"),
        ("CharacterAsset", "characterAsset"),
        ("NameKeyPool", "characterPool / weaponPool"),
        ("Weapon", "WpnDictionary"),
        ("WeaponData", "WpnDataDictionary"),
        ("RecyclableObject", "recyclableObjects"),
        ("GameObject", "playerPrefab / botPrefab / gameModePrefab"),
    ]
    relation_nodes = "\n".join(
        f"""
        <div class="node">
          <b>{html.escape(name)}</b>
          <span>字段依据：{html.escape(reason)}</span>
          <p>{html.escape(TYPE_SUMMARY[name])}</p>
        </div>
        """
        for name, reason in relation_types
    )
    category_options = "\n".join(
        f'<option value="{html.escape(category)}">{html.escape(category)}（{sum(1 for field in fields if field["category"] == category)}）</option>'
        for category in CATEGORY_ORDER
    )
    external_holders = render_external_holders()
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GameManager 字段关系图与字段说明</title>
  <style>
    :root {{
      --bg:#f4f6f8; --panel:#ffffff; --ink:#1f2937; --muted:#667085; --line:#d9e1ec;
      --blue:#2457a6; --green:#207450; --amber:#9a5b13; --red:#a33a3a;
    }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--ink); font-family:"Microsoft YaHei","Segoe UI",Arial,sans-serif; }}
    .page {{ max-width:1360px; margin:0 auto; padding:18px; }}
    header {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:18px 20px; }}
    h1 {{ margin:0 0 8px; font-size:26px; letter-spacing:0; }}
    h2 {{ margin:26px 0 12px; font-size:20px; }}
    p {{ margin:0; line-height:1.65; }}
    .summary {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin-top:16px; }}
    .metric {{ border:1px solid var(--line); border-radius:8px; padding:12px; background:#fafcff; }}
    .metric strong {{ display:block; font-size:24px; color:var(--blue); }}
    .metric span {{ color:var(--muted); font-size:13px; }}
    .graph {{ display:grid; grid-template-columns:1fr 1.1fr; gap:14px; margin-top:16px; }}
    .panel {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:16px; }}
    .core {{ border:2px solid var(--blue); background:#eef5ff; border-radius:8px; padding:16px; }}
    .core strong {{ display:block; font-size:24px; color:var(--blue); margin-bottom:8px; }}
    .nodes {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; margin-top:12px; }}
    .section-panel {{ margin-top:14px; }}
    .section-note {{ color:var(--muted); font-size:13px; margin-bottom:12px; }}
    .node {{ border:1px solid #cbd8e8; background:#fbfdff; border-radius:8px; padding:10px; min-height:112px; }}
    .node b {{ display:block; color:var(--green); margin-bottom:4px; }}
    .node span {{ color:var(--muted); font-size:13px; line-height:1.45; }}
    .node p {{ color:#344054; font-size:13px; line-height:1.55; margin-top:8px; }}
    .stats {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; }}
    .stat-card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:12px; min-height:116px; }}
    .stat-card strong {{ display:block; font-size:16px; margin-bottom:6px; }}
    .stat-card span {{ display:inline-block; color:#fff; background:var(--blue); border-radius:999px; padding:3px 9px; font-size:12px; margin-bottom:8px; }}
    .stat-card p {{ color:var(--muted); font-size:13px; }}
    .toolbar {{ display:flex; align-items:center; justify-content:space-between; gap:12px; margin:16px 0 8px; flex-wrap:wrap; }}
    .filters {{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; }}
    .pager {{ display:flex; gap:8px; flex-wrap:wrap; }}
    button,select {{ border:1px solid var(--line); background:#fff; color:var(--ink); border-radius:6px; padding:8px 12px; cursor:pointer; font:inherit; }}
    button.active {{ background:var(--blue); color:#fff; border-color:var(--blue); }}
    .hint {{ color:var(--muted); font-size:13px; }}
    table {{ width:100%; border-collapse:separate; border-spacing:0; background:var(--panel); border:1px solid var(--line); border-radius:8px; overflow:hidden; }}
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
    .footnote {{ margin-top:14px; color:var(--muted); font-size:13px; }}
    @media (max-width: 900px) {{
      .summary,.graph,.stats,.nodes {{ grid-template-columns:1fr; }}
      table {{ font-size:13px; }}
      code {{ white-space:normal; }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <header>
      <h1>GameManager 字段关系图与字段说明</h1>
      <p>依据 dump.cs 的 GameManager 字段声明生成。这个类可以理解为一局对战的总控：它保存玩家、阵营、模式、武器数据、角色/武器资源池，并通过事件把伤害、死亡、出生、回合开始等流程通知给其他系统。</p>
      <div class="summary">
        <div class="metric"><strong>{total}</strong><span>dump.cs 中字段总数</span></div>
        <div class="metric"><strong>{focused}</strong><span>建议重点分析字段</span></div>
        <div class="metric"><strong>{ignored}</strong><span>可忽略但已统计字段</span></div>
        <div class="metric"><strong>{pages}</strong><span>字段表分页，每页 15 行</span></div>
      </div>
    </header>

    <section class="graph">
      <div class="panel">
        <div class="core">
          <strong>GameManager</strong>
          <p>核心职责：组织对局运行时状态。Unity 角度，它像一个场景级单例控制器；穿越火线角度，它把玩家/Bot、BL/GR 阵营、玩法模式、武器规则、资源对象池、伤害死亡事件串在一起。</p>
        </div>
      </div>
      <div class="panel">
        <h2 style="margin-top:0">它直接保存的主要类型</h2>
        <div class="nodes">{relation_nodes}</div>
      </div>
    </section>
    {external_holders}

    <h2>字段系统分类统计</h2>
    <section class="stats">
      {render_category_cards(fields)}
    </section>

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
      <tbody>
        {render_rows(fields)}
      </tbody>
    </table>
    <p class="footnote">忽略规则：基础值字段、编译器生成后备字段、Action/事件委托字段不作为“类保存类”的关系图节点；但本页仍逐项解释并计入总数。</p>
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
      const category = filter.value;
      return rows.filter(row => category === '全部' || row.dataset.category === category);
    }}
    function renderPager(totalPages) {{
      pager.innerHTML = '';
      for (let page = 1; page <= totalPages; page++) {{
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = '第 ' + page + ' 页';
        button.className = page === currentPage ? 'active' : '';
        button.addEventListener('click', () => {{
          currentPage = page;
          updateTable();
        }});
        pager.appendChild(button);
      }}
    }}
    function updateTable() {{
      const matched = matchingRows();
      const totalPages = Math.max(1, Math.ceil(matched.length / pageSize));
      if (currentPage > totalPages) currentPage = totalPages;
      const start = (currentPage - 1) * pageSize;
      const end = start + pageSize;
      const visibleSet = new Set(matched.slice(start, end));
      rows.forEach(row => row.style.display = visibleSet.has(row) ? '' : 'none');
      visibleCount.textContent = matched.length;
      label.textContent = '第 ' + currentPage + ' 页';
      renderPager(totalPages);
    }}
    filter.addEventListener('change', () => {{
      currentPage = 1;
      updateTable();
    }});
    updateTable();
  </script>
</body>
</html>
"""


def main() -> None:
    fields = parse_game_manager_fields()
    if len(fields) != 42:
        raise RuntimeError(f"Expected 42 GameManager fields, got {len(fields)}")
    missing_categories = set(field["category"] for field in fields) - set(CATEGORY_ORDER)
    if missing_categories:
        raise RuntimeError(f"Unknown categories: {sorted(missing_categories)}")
    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(render(fields), encoding="utf-8")
    print(f"Wrote {HTML_OUT}")
    print(f"fields={len(fields)} focused={sum(1 for f in fields if f['ignored'] == '否')} ignored={sum(1 for f in fields if f['ignored'] == '是')}")
    for category in CATEGORY_ORDER:
        print(f"{category}: {sum(1 for f in fields if f['category'] == category)}")


if __name__ == "__main__":
    main()
