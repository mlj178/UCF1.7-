from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DUMP = ROOT / "01-游戏逆向分析-相关信息" / "Il2CppDumper" / "dump.cs"
OUT = ROOT / "04-正式发行版" / "全功能整合包1.8" / "类关系分析" / "字段关系图"
DOC_OUT = OUT / "文档汇总"
HTML_OUT = DOC_OUT / "HTML"

TARGETS = [
    "GameManager",
    "Player",
    "ClientData",
    "Bot",
    "PlayerWeapons",
    "ModeBase",
    "Entity",
    "CameraManager",
    "CharacterModel",
    "MapManager",
]

HIGH_PRIORITY_TARGETS = [
    "Bot_GuardPos",
    "Bot_JumpLink.Link",
    "BotAbility",
    "BotActionBase",
    "BotEnemyInfo",
    "DamageEventData",
    "DeathEventData",
    "GameMode",
    "HealthData",
    "HUD_NanoRoleSign",
    "HUD_PlayerRect",
    "MapGun",
    "MapTrigger",
    "ModeBase_Nano",
    "Nano4T_Data",
    "NanoGuard",
    "NanoRoleSelect",
    "Player.RespawnType",
    "PlayerCameraManager",
    "PlayerData",
    "PlayerInput",
    "PlayerMdlInfo",
    "PlayerSkills",
    "PlayerVelocity",
    "SpawnPoint",
    "SpawnPointDictionary",
    "TabScoreBoard_PlayerData",
    "Team",
    "Weapon",
    "WeaponAsset",
    "WeaponBag",
    "WeaponData",
    "WeaponLimited",
    "WPN_GhostBlade",
    "WPN_Gun.AmmoData",
    "WPN_Missile",
]

ALL_TARGETS = TARGETS + HIGH_PRIORITY_TARGETS


def collect_render_targets(all_fields: dict[str, list[dict[str, str]]]) -> list[str]:
    targets = list(ALL_TARGETS)
    seen = set(targets)
    for target in ALL_TARGETS:
        own, external = field_relation_summary(target, all_fields)
        for name in sorted(set(own) | set(external), key=str.lower):
            if name not in seen:
                targets.append(name)
                seen.add(name)
    return targets

CLASS_ANALYSIS = {
    "GameManager": [
        "功能翻译：一局战斗的总管理器",
        "Unity：场景单例，统一持有预制体、资源和运行时列表",
        "CF：创建/记录玩家和 Bot，区分 BL / GR 阵营",
        "管理存活 Player / Entity，用于胜负、复活和回合判断",
        "管理 GameMode、WeaponLimited、武器数据、角色资源和对象池",
    ],
    "Player": [
        "功能：玩家战斗对象",
        "Unity：实体组件，继承 Entity",
        "CF：承载生命、阵营、武器、角色模型、HUD 相关状态",
    ],
    "ClientData": [
        "功能：进场前数据容器",
        "Unity：偏数据类，不是场景对象",
        "CF：保存房间玩家、阵营、背包等开局资料",
    ],
    "Bot": [
        "功能：AI 玩家控制组件",
        "Unity：MonoBehaviour 行为脚本",
        "CF：控制 Bot 寻路、目标、武器和战斗行为",
    ],
    "PlayerWeapons": [
        "功能：玩家武器管理组件",
        "Unity：挂在玩家对象上的武器子系统",
        "CF：处理背包、当前武器、换枪和发枪结果",
    ],
    "ModeBase": [
        "功能：玩法规则基类",
        "Unity：模式单例/规则控制器",
        "CF：承接胜负、计分、复活、回合流程的公共规则",
    ],
    "Entity": [
        "功能：战斗实体基类",
        "Unity：MonoBehaviour 实体组件",
        "CF：玩家/Bot 等可受击对象的生命、阵营、受伤基础",
    ],
    "CameraManager": [
        "功能：摄像机管理器",
        "Unity：相机单例管理器",
        "CF：控制第一人称/观战/死亡等视角切换",
    ],
    "CharacterModel": [
        "功能：角色模型表现",
        "Unity：模型组件",
        "CF：管理角色身体、动画、材质和武器挂点表现",
    ],
    "MapManager": [
        "功能：地图点位管理器",
        "Unity：地图单例管理器",
        "CF：管理出生点、补给点、地图枪和小地图参数",
    ],
}

TYPE_ANALYSIS = {
    "AlternativePath": "AI 备用路径：Bot 主路径不可用时的替代移动路线",
    "Animation": "Unity 动画组件：控制角色/物体动画播放",
    "Animator": "Unity 动画状态机：控制角色动作切换",
    "AudioClip": "Unity 音频资源：角色语音、脚步或武器音效素材",
    "AudioSource": "Unity 音源组件：播放武器、角色或场景声音",
    "Bot": "AI 玩家对象：自动寻路、索敌、开火的电脑角色",
    "Bot_GuardPos": "Bot 防守点逻辑：让 AI 占位、巡逻或守点",
    "Bot_JumpLink.Link": "Bot 跳跃连接点：AI 寻路中跨越/跳跃路径段",
    "BotTarget": "Bot 路径/目标点数据：辅助 AI 移动和战术路线",
    "BotAbility": "Bot 能力配置：控制 AI 战斗、移动或模式能力",
    "BotActionBase": "Bot 行为基类：AI 动作/决策节点的公共父类",
    "BotEnemyInfo": "Bot 敌人记忆：记录 AI 发现或正在攻击的目标信息",
    "Buff": "状态增益/减益：影响生命、速度、控制或战斗属性",
    "Camera": "Unity 摄像机：负责画面视角输出",
    "CameraManager": "摄像机管理器：切换第一人称、观战、死亡等视角",
    "CharacterController": "Unity 角色控制器：处理碰撞、移动和胶囊体控制",
    "CharacterEffect": "角色特效组件：控制角色身上的光效、受击或技能表现",
    "CharacterAsset": "角色资源配置表：管理可用角色/模型资源",
    "CharacterModel": "角色模型表现：身体、动画、材质和挂点",
    "CharacterModel.MoveDirection": "角色移动方向枚举：给走、跑、死亡倒地方向选择对应动画",
    "CharacterModel.Sex": "角色性别枚举：区分男/女角色，用于语音、模型和受击/恢复特效表现",
    "CharacterVoice": "角色语音配置：管理角色语音、呼喊或受击声音",
    "CharWpnAnimData": "角色持枪动画数据：不同武器对应的动作配置",
    "CinemachineBrain": "Cinemachine 相机大脑：混合和驱动虚拟相机输出",
    "CinemachineFreeLook": "Cinemachine 自由视角相机：第三人称/观察视角控制",
    "ClientData": "房间/开局数据：玩家、阵营、背包等进场资料",
    "ClientData.ClipBuffInfo": "备弹/弹夹加成信息：记录进入对局时各类子弹补给或弹夹 Buff 拥有状态",
    "Coroutine": "Unity 协程句柄：保存延时、复活、动画等待等异步流程",
    "CrabStep": "Bot 横移步法：AI 躲避或交火时的左右移动行为",
    "DamageEventData": "伤害事件数据：记录攻击者、受害者、伤害类型和命中信息",
    "DeathEventData": "死亡事件数据：记录击杀者、死亡者、爆头和特殊击杀信息",
    "EffectObj": "特效对象：命中、爆炸、枪口火光等视觉效果实例",
    "Entity": "战斗实体基类：玩家/Bot 等可受击对象",
    "ForwardRendererData": "URP 渲染器配置：控制后处理、渲染特性和画面管线",
    "GameMode": "玩法模式配置：决定当前对局类型",
    "GameManager": "对局总管理器：统一协调玩家、实体、模式、武器和回合",
    "GameObject": "Unity 场景对象/预制体：用于生成或引用场景对象",
    "GhostBladeOneShine": "幽灵刀光特效：近战武器或技能的一次性视觉表现",
    "GraphNode": "寻路图节点：AI 路径搜索中的地图节点",
    "HealthData": "生命数据：保存血量、护甲或受伤相关状态",
    "Helmet": "头盔/头部装备表现：角色头部模型或防具组件",
    "HUD_Crosshair": "准星 HUD：根据玩家武器和状态显示准星",
    "HUD_HeartBeatRadar": "心跳雷达 HUD：显示被侦测敌人或特殊模式提示",
    "HUD_KillMark.EventData": "击杀标记数据：HUD 显示连杀、爆头等击杀反馈",
    "HUD_NanoRoleSign": "纳米模式角色标识 HUD：显示纳米/终结者身份提示",
    "HUD_PlayerRect": "玩家矩形 UI：记分板或模式界面中的玩家条目",
    "HUD_RadarIcon_Alive": "雷达存活图标：小地图上显示活着的玩家/实体",
    "HUD_RadarIcon_Entity": "雷达实体图标：小地图上显示普通实体位置",
    "HUD_RadarIcon_HearBeat": "心跳雷达图标：显示被心跳雷达探测到的目标",
    "HUD_RoleAsset": "角色 HUD 资源：角色头像、身份标识或界面素材",
    "Image": "Unity UI 图片：显示图标、准星、血条等界面元素",
    "KeyInputState": "按键输入状态：保存某个动作键的按下/松开状态",
    "MapManager": "地图点位管理器：出生点、补给点、地图枪等",
    "MapGun": "地图枪对象：地图上可拾取或使用的武器点",
    "MapTrigger": "地图交互触发器：开关、占点、拾取或场景互动区域",
    "Material": "Unity 材质：控制模型表面颜色、贴图和渲染效果",
    "Model": "模型基类：角色或物体表现层的父级结构",
    "ModeBase": "玩法规则基类：胜负、计分、复活、回合流程",
    "ModeBase_Nano": "纳米模式规则：终结者/幽灵相关玩法、吸收和胜负逻辑",
    "NameKeyPool": "按名称索引的对象池：复用角色/武器对象",
    "Nano4T_Data": "纳米 4T 模式数据：终结者模式角色/属性配置",
    "NanoGuard": "纳米守卫 AI/角色逻辑：纳米模式中的守卫单位行为",
    "NanoRoleSelect": "纳米角色选择数据：纳米模式角色选择或身份配置",
    "ObscuredBool": "加密布尔值：防作弊保护的 true/false 状态",
    "ObscuredInt": "加密整数：防作弊保护的数值字段",
    "ParticleSystem": "Unity 粒子系统：烟雾、火花、爆炸等特效",
    "Path": "AI 寻路路径：Bot 从当前位置到目标点的路径结果",
    "PathInterpolator": "路径插值器：让 Bot 沿寻路结果平滑移动",
    "Player": "玩家对象：本机/敌我玩家的战斗状态主体",
    "PlayerCameraManager": "玩家相机控制：玩家视角、后坐力和观察点管理",
    "PlayerController": "玩家控制器：输入、移动、视角控制入口",
    "PlayerData": "玩家资料数据：保存玩家身份、队伍或对局基础资料",
    "PlayerInput": "玩家输入封装：移动、开火、交互等输入状态",
    "PlayerMdlInfo": "玩家模型信息：角色模型、皮肤或显示状态资料",
    "PlayerSkills": "玩家技能集合：角色技能、被动或模式能力",
    "PlayerVelocity": "玩家速度数据：移动速度、跳跃或物理速度状态",
    "PlayerWeapons": "玩家武器管理：背包、当前武器、切枪和发枪",
    "Player.RespawnType": "玩家复活方式枚举：决定按队伍点、原地或敌方区域等规则复活",
    "PropertyModifier": "属性修改器：临时改变速度、弹药、控制等属性",
    "QVModel": "第一人称手臂/武器模型：玩家自己视角的模型表现",
    "RawImage": "Unity UI 原始图片：显示贴图类界面内容",
    "Recoil": "后坐力数据：控制开火时视角/枪口上跳",
    "Ref2Float": "两个浮点引用值：用于共享或实时修改成对数值",
    "RefBool": "布尔引用值：用于共享开关、禁用状态或 Buff 状态",
    "RefInt": "整数引用值：用于 AI/玩法共享计数或状态值",
    "RefPosition": "位置引用值：Bot 寻路、目标点或守点位置",
    "RecyclableObject": "可回收场景物：掉落物或临时对象清理",
    "Renderer": "Unity 渲染器：控制模型材质和可见性",
    "Rigidbody": "Unity 物理刚体：提供碰撞、速度、受力",
    "Saunter": "Bot 慢走/游走行为：AI 非战斗移动状态",
    "ScriptableRendererFeature": "URP 渲染特性：热成像、描边或屏幕效果开关",
    "Seeker": "A* 寻路请求器：给 Bot 计算路径",
    "SimpleObjectPool": "简单对象池：复用 UI、特效或临时对象",
    "SpawnPoint": "出生/补给点位：决定玩家或物品生成位置",
    "SpawnPointArray": "出生点数组：按阵营/用途组织点位",
    "SpawnPointDictionary": "出生点字典：用名称索引地图点位集合",
    "TabScoreBoard_PlayerData": "TAB 记分板玩家数据：显示分数、击杀、死亡等",
    "Team": "队伍/阵营枚举：区分 BL、GR、观战或中立阵营",
    "TerminatorMoveSnd": "终结者移动声音：纳米模式重型角色脚步/移动音效",
    "Text": "Unity UI 文本：显示名字、分数、提示等",
    "Texture": "Unity 贴图基类：UI、材质或屏幕效果用图像资源",
    "Texture2D": "Unity 贴图资源：小地图、材质或 UI 图片数据",
    "ThermalVision": "热成像效果：特殊视野/技能下的屏幕或目标显示",
    "TombStone": "墓碑/死亡标记：玩家死亡后场景中的标记对象",
    "Transform": "Unity 变换组件：位置、旋转、层级挂点",
    "UI_GameRoom": "游戏房间 UI：准备、队伍、背包和开局配置界面",
    "VolumeProfile": "URP 后处理配置：色调、模糊、热成像等画面效果",
    "Vector2": "二维向量：UI、坐标或平面数值",
    "Vector2Int": "二维整数向量：格点、弹药数量或尺寸",
    "Vector3": "三维向量：世界坐标、方向、命中位置",
    "Weapon": "武器实例：实际可装备、发射、掉落的武器对象",
    "WeaponAsset": "武器资源配置表：提供可加载/可发放武器资源",
    "WeaponBag": "武器背包配置：玩家进场携带的主武器、副武器和道具",
    "WeaponData": "武器数值配置：伤害、弹药、图标等资料",
    "WeaponLimited": "武器限制规则：限制刀、手枪、狙击等可用武器",
    "WPN_GhostBlade": "幽灵之刃武器：近战/特殊技能武器逻辑",
    "WPN_Gun.AmmoData": "枪械弹药数据：当前弹匣、备弹和弹药显示",
    "WPN_Missile": "导弹类武器：爆炸、飞行和范围伤害对象",
}

TYPE_ANALYSIS.update(
    {
        "AnimationHud": "动画 HUD 控件：显示模式倒计时、提示动画或状态切换反馈",
        "BotEnemyInfo.DistanceControl": "Bot 距离控制枚举/配置：决定 AI 与目标保持、接近或拉开的距离策略",
        "Bot_JumpLink": "Bot 跳跃连接配置：定义 AI 可跨越或跳跃通过的寻路连接",
        "Bot_NanoGuardArea": "纳米守卫区域：限制或指引纳米守卫 AI 活动范围",
        "Bot_NanoGuardPos": "纳米守卫点位：纳米模式中守卫 AI 的站位、巡逻或防守点",
        "BoxCollider": "Unity 盒形碰撞体：地图枪、触发器或拾取区域的碰撞检测",
        "CinemachineVirtualCamera": "Cinemachine 虚拟相机：玩家视角、观战或特殊镜头的相机配置",
        "Color": "Unity 颜色值：控制 UI、模型或特效颜色表现",
        "CommonHud_1": "通用对局 HUD：承载模式提示、计分、倒计时等基础界面元素",
        "CommonKillMark": "通用击杀提示：显示击杀、连杀、爆头等战斗反馈",
        "DamageTag": "伤害标签枚举：标记普通伤害、爆炸、近战、技能等伤害来源特征",
        "DamageType": "伤害类型枚举：区分身体命中、爆头、环境或特殊规则伤害",
        "HeadShotType": "爆头类型枚举：区分是否爆头以及爆头反馈规则",
        "MapAsset.Map": "地图枚举/标识：表示当前选择或加载的对局地图",
        "Model.Type": "模型类型枚举：区分角色、武器、第一人称或其他表现模型类型",
        "MultiKillTimer": "连杀计时器：记录短时间连续击杀窗口，用于连杀提示和计分反馈",
        "PlayerCameraManager.FovZoomInfo": "视野缩放信息：保存开镜、技能或观察状态下的 FOV 变化参数",
        "PlayerMdlInfo.FxType": "玩家模型特效类型：控制角色模型附加光效、阵营色或状态表现",
        "PlayerVelocity.VelLockType": "速度锁定类型：决定玩家移动速度是否被技能、状态或规则锁定",
        "RankField": "段位/排名字段：记分板里显示军衔、等级或排名信息的 UI 项",
        "RaycastHit": "Unity 射线命中信息：记录开火、瞄准或检测命中的物体和位置",
        "RectTransform": "Unity UI 矩形变换：控制 HUD/UI 元素位置、尺寸和锚点",
        "SerializableDictionaryBase": "可序列化字典基类：让 Unity Inspector 保存键值映射配置",
        "Skill": "技能对象：玩家、武器或模式触发的主动/被动能力逻辑",
        "Skill_ModeChange": "模式切换技能：用于幽灵之刃等武器触发形态或攻击模式变化",
        "SpecialKillType": "特殊击杀类型枚举：标记首杀、终结、连杀等特殊击杀规则",
        "Sprite": "Unity 精灵图片资源：UI 图标、武器图标、地图标识或提示图",
        "SubscribeableProperty": "可订阅属性：数值变化时通知 UI、玩法或表现系统刷新",
        "Test": "测试/调试数据类型：多用于开发期验证字段或临时配置，实际功能价值需结合字段来源确认",
        "TrailRenderer": "Unity 拖尾渲染器：导弹、刀光或高速运动物体的尾迹效果",
        "Vector3Int": "三维整数向量：格子坐标、方向索引或离散移动方向",
        "Weapon.SlotType": "武器槽位枚举：区分主武器、副武器、近战、投掷物等背包位置",
        "WeaponClass": "武器类别枚举：区分步枪、狙击、机枪、手枪、近战等规则分类",
        "WpnComponent": "武器组件基类：武器上的功能模块，如开火、瞄准、特效或命中处理",
        "WD_GhostBlade": "幽灵之刃武器数据：保存该特殊武器的伤害、技能或表现参数",
    }
)

MODIFIERS = {
    "public",
    "private",
    "protected",
    "internal",
    "static",
    "readonly",
    "volatile",
    "const",
    "new",
    "unsafe",
}

WRAPPERS = {
    "List",
    "Dictionary",
    "Action",
    "Func",
    "Predicate",
    "IEnumerable",
    "IEnumerator",
    "Nullable",
}

BASIC_TYPES = {
    "bool",
    "byte",
    "sbyte",
    "short",
    "ushort",
    "int",
    "uint",
    "long",
    "ulong",
    "float",
    "double",
    "decimal",
    "char",
    "string",
    "object",
    "void",
    "IntPtr",
}

FRAMEWORK_TYPES = {
    "AsyncCallback",
    "IAsyncResult",
    "IEnumerator",
    "IDisposable",
    "MulticastDelegate",
}

DELEGATE_TYPES: set[str] = set()


def discover_delegate_types(text: str) -> set[str]:
    return set(
        re.findall(
            r"\b(?:class|struct)\s+([A-Za-z_][\w.<>]*)[^\n]*:\s*MulticastDelegate\b",
            text,
        )
    )


def is_delegate_field(type_text: str) -> bool:
    compact = type_text.replace(" ", "")
    if compact in {"Action", "Func", "Predicate"}:
        return True
    return compact.startswith(("Action<", "Func<", "Predicate<"))


def is_generated_name(name: str) -> bool:
    return (
        "<" in name
        or ">" in name
        or "DisplayClass" in name
        or "CS$" in name
        or "__" in name
    )


def class_blocks(text: str) -> dict[str, str]:
    pattern = re.compile(
        r"(?ms)^.*?\b(?:class|struct)\s+(?P<name>[A-Za-z_][\w.<>]*)[^\n]*\n\{(?P<body>.*?)(?=^// Namespace:|\Z)"
    )
    return {m.group("name"): m.group("body") for m in pattern.finditer(text)}


def fields_from_body(body: str) -> list[dict[str, str]]:
    if "// Fields" not in body:
        return []
    section = body.split("// Fields", 1)[1]
    for marker in ("// Properties", "// Methods"):
        if marker in section:
            section = section.split(marker, 1)[0]
    fields: list[dict[str, str]] = []
    for raw in section.splitlines():
        line = raw.strip()
        if not line or ";" not in line or line.startswith("[") or "//" not in line:
            continue
        left = line.split(";", 1)[0].strip()
        if "=" in left:
            left = left.split("=", 1)[0].strip()
        parts = left.split()
        if len(parts) < 2:
            continue
        name = parts[-1]
        type_text = " ".join(parts[:-1])
        while True:
            changed = False
            for mod in sorted(MODIFIERS, key=len, reverse=True):
                if type_text == mod:
                    type_text = ""
                    changed = True
                elif type_text.startswith(mod + " "):
                    type_text = type_text[len(mod) + 1 :]
                    changed = True
            if not changed:
                break
        if not type_text or "const " in raw:
            continue
        fields.append({"name": name, "type": type_text})
    return fields


def type_tokens(type_text: str, current: str | None = None) -> list[str]:
    found = re.findall(r"[A-Za-z_][\w]*(?:\.[A-Za-z_][\w]*)?", type_text)
    out: list[str] = []
    for token in found:
        leaf = token.split(".")[-1]
        if token in WRAPPERS or leaf in WRAPPERS:
            continue
        if token in BASIC_TYPES or leaf in BASIC_TYPES:
            continue
        if token in FRAMEWORK_TYPES or leaf in FRAMEWORK_TYPES:
            continue
        if token in DELEGATE_TYPES or leaf in DELEGATE_TYPES:
            continue
        if is_generated_name(token):
            continue
        if token not in out:
            out.append(token)
    return out


def short_desc(type_name: str, fields: list[dict[str, str]]) -> str:
    names = [f["name"] for f in fields[:4]]
    more = "" if len(fields) <= 4 else f" 等 {len(fields)} 个字段"
    return " / ".join(names) + more


def analysis_for_type(type_name: str) -> str:
    if type_name in TYPE_ANALYSIS:
        return TYPE_ANALYSIS[type_name]
    if type_name.startswith("WD_"):
        return "武器数据配置：保存某个具体武器的伤害、弹药、技能或表现参数"
    if type_name.startswith("SO_"):
        return "ScriptableObject 配置资源：用资源文件保存声音、道具、武器或界面配置"
    if type_name.startswith("HUD_"):
        return "HUD 界面组件：显示玩家状态、提示、图标或模式信息"
    if type_name.startswith("UI_"):
        return "UI 界面类：负责菜单、房间、背包或游戏内交互显示"
    if type_name.startswith("WPN_"):
        return "武器逻辑类：处理特定武器的攻击、表现或特殊效果"
    if type_name.startswith("CF"):
        return "项目封装类型：穿越火线项目对 Unity 或 gameplay 逻辑的二次封装"
    if type_name.startswith("Mode_"):
        return "具体玩法模式类：实现某种模式的规则和流程"
    if type_name.startswith("Nano"):
        return "纳米模式相关类型：处理终结者/幽灵玩法数据或行为"
    if type_name.startswith("Ref"):
        return "共享引用值：让多个系统读写同一个运行时状态"
    if "Cinemachine" in type_name or "Camera" in type_name or "Lens" in type_name:
        return "相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态"
    if "VFX" in type_name or "Effect" in type_name or "FX" in type_name:
        return "视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈"
    if "Astar" in type_name or "Navmesh" in type_name or "Graph" in type_name or "Path" in type_name or "RVO" in type_name:
        return "寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点"
    if "Bot" in type_name or type_name.startswith("AI") or "Agent" in type_name:
        return "AI 行为类型：用于电脑角色、代理移动、决策或目标选择"
    if "Weapon" in type_name or "WPN" in type_name or "Ammo" in type_name or "Gun" in type_name or "Missile" in type_name or "Grenade" in type_name or "RPG" in type_name:
        return "武器相关类型：用于武器数据、发射逻辑、弹药、投掷物或特殊武器表现"
    if "Damage" in type_name or "Hit" in type_name or "Kill" in type_name or "HeadShot" in type_name:
        return "战斗结算类型：用于伤害、命中、击杀、爆头或战斗反馈"
    if "Input" in type_name or "Touch" in type_name or "Mouse" in type_name or "Key" in type_name:
        return "输入交互类型：用于鼠标、触摸、按键或输入模块状态"
    if "Button" in type_name or "Slider" in type_name or "Scroll" in type_name or "Layout" in type_name or "Graphic" in type_name or "Canvas" in type_name or "Text" in type_name:
        return "UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件"
    if "Light" in type_name or "Render" in type_name or "Renderer" in type_name or "Shader" in type_name or "Volume" in type_name:
        return "渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果"
    if "Collider" in type_name or "Collision" in type_name or "Raycast" in type_name or "Physics" in type_name:
        return "物理检测类型：用于碰撞、射线检测、触发器或命中查询"
    if "Animation" in type_name or "Animator" in type_name or "IK" in type_name or "Ragdoll" in type_name or "Mecanim" in type_name:
        return "动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接"
    if "Audio" in type_name or "Sound" in type_name or "Snd" in type_name:
        return "声音类型：用于音效资源、触发播放、脚步声、武器声或环境声"
    if "Skill" in type_name:
        return "技能相关类型：用于角色、武器或模式技能的触发、状态和表现"
    if "Pool" in type_name or "Cache" in type_name:
        return "缓存/对象池类型：用于复用对象、缓存计算结果或降低运行时分配"
    if "Settings" in type_name or "Data" in type_name or "Config" in type_name or "Profile" in type_name or "Desc" in type_name:
        return "配置/数据类型：保存运行参数、资源引用、显示数据或系统配置"
    if "Event" in type_name:
        return "事件数据类型：用于在系统之间传递状态变化、动画回调或玩法通知"
    if "Color" in type_name:
        return "颜色配置类型：用于 UI、特效、渲染或阵营表现的颜色数据"
    if "Vector" in type_name or "Position" in type_name or "Rotation" in type_name:
        return "空间数据类型：保存位置、方向、旋转、速度或坐标信息"
    if "Asset" in type_name:
        return "资源索引类型：保存可加载资源、图标、预制体或表现素材引用"
    if type_name.endswith("Manager"):
        return "管理器类：集中维护对应系统的运行时对象和流程"
    if type_name.endswith("Asset"):
        return "资源配置类：保存可加载、可显示或可生成的资源资料"
    if type_name.endswith("Data"):
        return "数据配置类：保存该系统运行或显示所需的数值资料"
    if type_name.endswith("Model"):
        return "模型表现类：负责角色、武器或物体的可视表现"
    return "项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类"


def field_relation_summary(target: str, all_fields: dict[str, list[dict[str, str]]]):
    own_map: dict[str, list[dict[str, str]]] = {}
    for field in all_fields.get(target, []):
        if is_delegate_field(field["type"]):
            continue
        for token in type_tokens(field["type"], target):
            own_map.setdefault(token, []).append(field)

    external: dict[str, list[dict[str, str]]] = {}
    for owner, fields in all_fields.items():
        if is_generated_name(owner):
            continue
        hits = []
        for field in fields:
            if is_delegate_field(field["type"]):
                continue
            tokens = type_tokens(field["type"], owner)
            if target in tokens:
                hits.append(field)
        if hits:
            external[owner] = hits
    return own_map, external


def svg_node(x: int, y: int, w: int, h: int, title: str, desc: str, cls: str = "box", analysis: str | None = None) -> str:
    analysis_line = analysis or analysis_for_type(title)
    return f"""
  <g transform="translate({x} {y})">
    <rect class="{cls}" width="{w}" height="{h}"/>
    <text x="18" y="27" class="name">{html.escape(title)}</text>
    <text x="18" y="49" class="desc">{html.escape(analysis_line)}</text>
    <text x="18" y="69" class="desc">字段依据：{html.escape(desc)}</text>
  </g>"""


def render(target: str, own_map: dict[str, list[dict[str, str]]], external: dict[str, list[dict[str, str]]]) -> str:
    rows = max(4, len(own_map), len(external) if external else 1)
    spacing = 98
    node_h = 78
    height = 260 + rows * spacing + 140
    left_nodes = []
    if external:
        for i, (owner, fields) in enumerate(sorted(external.items())):
            left_nodes.append(svg_node(70, 235 + i * spacing, 330, node_h, owner, short_desc(owner, fields), "source"))
    else:
        left_nodes.append(svg_node(70, 235, 330, node_h, "没有发现", f"0 个类的字段保存 {target}", "empty", f"没有其他类字段直接保存 {target}"))

    right_nodes = []
    for i, (typ, fields) in enumerate(sorted(own_map.items())):
        right_nodes.append(svg_node(1020, 235 + i * spacing, 360, node_h, typ, short_desc(typ, fields), "target"))

    left_edges = []
    if external:
        for i in range(len(external)):
            y = 274 + i * spacing
            left_edges.append(f'<path class="edge source-edge" marker-end="url(#arrowSource)" d="M400 {y} H575 V430 H660"/>')

    right_edges = []
    for i in range(len(own_map)):
        y = 274 + i * spacing
        right_edges.append(f'<path class="edge target-edge" marker-end="url(#arrowTarget)" d="M840 430 H940 V{y} H1020"/>')

    analysis = CLASS_ANALYSIS.get(
        target,
        [
            f"功能翻译：{analysis_for_type(target)}",
            "关系依据：只看 dump.cs 字段声明",
            "用途判断：看左侧谁保存它、右侧它保存哪些类型",
        ],
    )
    analysis_lines = "\n".join(
        f'  <text x="750" y="{454 + i * 23}" text-anchor="middle" class="desc">{html.escape(line)}</text>'
        for i, line in enumerate(analysis)
    )
    external_analysis = (
        f"分析：没有其他类字段直接保存 {target}"
        if not external
        else f"分析：有 {len(external)} 个类字段保存 {target}"
    )
    own_analysis = (
        f"分析：{target} 字段直接保存 {len(own_map)} 种非基础类型"
        if own_map
        else f"分析：{target} 没有字段直接保存其他非基础类型"
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(target)} 字段关系图</title>
  <style>
    :root{{--bg:#f3f5f8;--ink:#1f2633;--muted:#5f6878;--line:#cfd7e4;--core:#1f5fbf;--source:#315f9f;--target:#24724c}}
    *{{box-sizing:border-box}}html,body{{margin:0;background:var(--bg);font-family:"Microsoft YaHei","Segoe UI",Arial,sans-serif;color:var(--ink)}}
    .canvas{{width:100%;min-height:100vh;padding:12px}}svg{{display:block;width:100%;min-width:1180px;height:auto;background:#fff;border:1px solid var(--line);border-radius:8px}}
    .title{{font-size:25px;font-weight:700;fill:var(--ink)}}.note{{font-size:13px;fill:var(--muted)}}.lane{{fill:#f8fafc;stroke:#e2e8f0;stroke-width:1;rx:12}}
    .core{{fill:#eef5ff;stroke:var(--core);stroke-width:3;rx:12}}.box,.source,.target,.empty{{fill:#fff;stroke:#cbd5e1;stroke-width:1.5;rx:10}}.source{{fill:#f2f7ff}}.target{{fill:#f1fbf5}}.empty{{fill:#f8fafc}}
    .name{{font-size:15px;font-weight:700;fill:#1f2633}}.desc{{font-size:12px;fill:var(--muted)}}.count{{font-size:14px;font-weight:700;fill:#1f7a4d}}.lane-title{{font-size:17px;font-weight:700;fill:#2d3748}}
    .edge{{fill:none;stroke-width:2.7}}.source-edge{{stroke:var(--source)}}.target-edge{{stroke:var(--target)}}.label{{font-size:12px;fill:#344054}}.label-bg{{fill:#fff;stroke:#edf0f5;rx:5}}
  </style>
</head>
<body>
<div class="canvas">
<svg viewBox="0 0 1450 {height}" role="img" aria-label="{html.escape(target)} field relationship graph">
  <defs>
    <marker id="arrowSource" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L9,3 L0,6 Z" fill="#315f9f"/></marker>
    <marker id="arrowTarget" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L9,3 L0,6 Z" fill="#24724c"/></marker>
  </defs>
  <text x="36" y="44" class="title">{html.escape(target)} 字段关系图</text>
  <text x="36" y="70" class="note">只统计 dump.cs 字段声明：左边是谁的字段保存了 {html.escape(target)}；右边是 {html.escape(target)} 自己字段保存的类型。委托事件字段和基础值不画。</text>

  <rect class="lane" x="40" y="110" width="390" height="{height - 160}"/>
  <rect class="lane" x="530" y="110" width="370" height="{height - 160}"/>
  <rect class="lane" x="980" y="110" width="420" height="{height - 160}"/>
  <text x="70" y="148" class="lane-title">谁保存了这个类</text>
  <text x="70" y="172" class="note">通俗说：其他类字段里有没有它</text>
  <text x="70" y="196" class="count">统计：{len(external)} / {len(external)} 已画出</text>
  <text x="70" y="220" class="note">{html.escape(external_analysis)}</text>
  <text x="560" y="148" class="lane-title">当前类</text>
  <text x="560" y="172" class="note">分析直接写在类名下面</text>
  <text x="1010" y="148" class="lane-title">它保存了哪些类型</text>
  <text x="1010" y="172" class="note">通俗说：这个类字段里有哪些对象</text>
  <text x="1010" y="196" class="count">统计：{len(own_map)} / {len(own_map)} 已画出</text>
  <text x="1010" y="220" class="note">{html.escape(own_analysis)}</text>

  <rect class="core" x="610" y="340" width="280" height="170"/>
  <text x="750" y="382" text-anchor="middle" style="font-size:24px;font-weight:700;fill:#1f5fbf">{html.escape(target)}</text>
  <text x="750" y="414" text-anchor="middle" class="desc">字段关系中心</text>
{analysis_lines}
{''.join(left_nodes)}
{''.join(right_nodes)}
{''.join(left_edges)}
{''.join(right_edges)}
</svg>
</div>
</body>
</html>
"""


def main() -> None:
    global DELEGATE_TYPES
    text = DUMP.read_text(encoding="utf-8", errors="ignore")
    DELEGATE_TYPES = discover_delegate_types(text)
    blocks = class_blocks(text)
    all_fields = {name: fields_from_body(body) for name, body in blocks.items()}
    DOC_OUT.mkdir(parents=True, exist_ok=True)
    HTML_OUT.mkdir(parents=True, exist_ok=True)
    index_lines = ["# 字段关系图\n"]
    for target in collect_render_targets(all_fields):
        own, external = field_relation_summary(target, all_fields)
        out_file = HTML_OUT / f"{target}字段关系图.html"
        out_file.write_text(render(target, own, external), encoding="utf-8")
        index_lines.append(f"- {target}: 外部保存 {len(external)}，自身保存类型 {len(own)} -> HTML/{out_file.name}\n")
    (DOC_OUT / "README.md").write_text("".join(index_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
