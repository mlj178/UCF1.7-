#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""开关表与界面常量：GROUPS / DEV_ITEMS / 颜色 / 热键速查 / 车测文案。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


# 版本对比的状态色（人机路点最下面那块面板用；唯一判据 = sha256 相同）
CMP_COLOR = {"same": "#2f9e44", "diff": "#f59f00", "only_pack": "#4c6ef5",
             "only_final": "#868e96", "fp_bad": "#e03131"}


CMP_TEXT = {"same": "✔ 一致", "diff": "⚠ 不一致", "only_pack": "○ 只在编辑中",
            "only_final": "◇ 只在成品", "fp_bad": "✖ 指纹不匹配"}


CMP_SHORT = {"same": "✔ 一致", "diff": "⚠ 不一致", "only_pack": "○ 待发布",
             "only_final": "◇ 只在成品", "fp_bad": "✖ 指纹失效"}


CREATE_NO_WINDOW = 0x08000000


FONT = ("Microsoft YaHei UI", 13)


FONT_S = ("Microsoft YaHei UI", 12)


FONT_B = ("Microsoft YaHei UI", 15, "bold")


# ---- 开关定义：(key, 标题, 说明, 默认值) --------------------------------
GROUPS = [
    ("地图", "房间选图列表里要不要多一张「暴风」；关掉后就是原版列表", [
        ("hidden_map", "加载暴风地图", "把隐藏图 Nano30_Storm 插进房间下拉框；关掉后选不到暴风", True),
    ]),
    # 2026-11-19 用户要求：可视化按数据类别拆成勾选框，一颗开关同时管「读不读」和「画不画」；
    # 总开关（visualizer）排在本页顶部。「导出」页那 6 个 export_* 是另一套，互不影响。
    ("可视化", "进图时读什么、画什么都在这一页；关掉哪类就不读也不画（不影响 Ctrl+E 导出）。"
                "给开发用的玩家坐标记录 / 原始轨迹采集在最后一页「开发者选项」", [
        ("visualizer", "可视化总开关（Visualizer）", "整套彩色点线的总开关；关掉后进图不画（可走面独立，不受影响）；Ctrl+V 随时开关", False),
        ("vis_nodes", "路点 / 连线（PointNode / Connection）", "浅蓝点 = 普通路点，橙点 = 带标签，红点 = 禁走点；蓝线 = 连线", True),
        ("vis_crouch", "蹲守点（Bot_CrouchPos）", "红色实心小方块（两阵营同色）", True),
        ("vis_guard", "守卫区 / 守卫点（Bot_GuardArea / Bot_GuardPos）", "紫色线框区 + 橙色实心点", True),
        ("vis_nano", "幽灵守区 / 幽灵守点（Bot_NanoGuardArea / Bot_NanoGuardPos）", "绿色线框区 + 青色实心点", True),
        ("vis_born", "出生点（SpawnPoint）", "潜伏者(蓝)/保卫者(红)/中立点(灰)；个人竞技用中立点、全员敌对；生化/剑客与补给箱混布，叠色偏粉紫", True),
        ("vis_supply", "补给箱（SupplyBox / RedBox / BlueBox）", "金/粉/青实心高柱 = 补给/红/蓝", True),
        ("vis_jump", "跳点（Bot_JumpLink）", "黄色连线（没有点标记）", True),
        ("vis_tag", "标签区（PointNodeTagModifier）", "橙色线框小方块", True),
        ("navmesh_show", "可走面（NavMeshGraph）", "绿色三角网线框（人机真正在上面跑的面）；Ctrl+Shift+6 随时开关；与可视化总开关无关", True),
        # 2026-11-20 用户要求：工作台 / 3D 查看器 / 游戏里都要有「东南西北」，方向约定三处统一。
        ("vis_compass", "方向罗盘（东南西北）", "汉字罗盘：北 = 世界 -Z（和工作台平面图一致）、东 = +X、南 = +Z、西 = -X；圈心金字 = 你正对着哪；Ctrl+Shift+7 开关；与可视化总开关无关", True),
    ]),
    # 2026-11-18：导出单独成页 —— 一个总开关 + 六项内容，默认全勾
    ("导出", "Ctrl+E 导出的总开关与内容（与可视化开关互相独立）", [
        ("export_enabled", "启用导出", "总开关；关掉后下面勾选全部不生效，Ctrl+E 不读也不写", True),
        ("export_nodes", "路点 / 连线", "JSON 主体；关掉后只导特征点（文件名 f<特征数>，不写 _seen 去重）", True),
        ("export_crouch", "人类蹲守点", "读人类蹲守点；关掉后 JSON 里 crouch=0", True),
        ("export_area", "幽灵守区 / 守点", "读幽灵守区与幽灵守点；关掉后 nano_area/nano_pos=0", True),
        ("export_guard", "守卫区 / 守卫点", "读守卫区与守卫点；关掉后 guard=0", True),
        ("export_spawn", "出生点 / 补给箱", "读出生点与补给箱；关掉后 spawn=0", True),
        ("export_tags", "跳点 / 标签区", "读跳点与标签区；关掉后 jump/tag=0", True),
    ]),
    # 2026-11-19：文字标签控件已删除；这一页保留游戏内热键速查。
    ("快捷键", "游戏内热键速查（屏幕不再显示数据面板和文字标签）", []),
    # 2026-11-19 用户要求：删除「自动铺设」整块（auto_waypoints / auto_crouch / ghost_areas）。
    # 2026-11-19 用户要求：删除「允许游戏内编辑」（editor），C 侧键保留（默认开）。
    # 2026-11-19 用户要求：整个「手动」页删除（collect_only 入口随之去掉，功能仍可用
    # collect.flag / Ctrl+Shift+X）。
]


# 2026-11-21 用户要求：给开发 / 离线分析用的入口单独成页「开发者选项」（页签排最后），
# 从「可视化」「录制」里搬出来 —— 正常玩图那几页不再掺这些。
# 这里的开关和 GROUPS 走同一套自检（cfg.c 里有 -> 面板里必须能关、默认值一致）。
DEV_ITEMS = [
    ("vis_player_marks", "玩家坐标记录", "金色方块 = 本次（这张图这一局）记下的玩家脚下位置；换图 / 重开游戏就不画了，也不连折线；坐标只留在 player_marks.txt 当日志，记录 / 删除在下面「玩家坐标记录」卡片里", True),
]


# ---- 控制台页签分组（2026-11-24 用户要求：按功能分组）------------------------
# (组名, (组内页签, ...)) —— 顺序就是界面顺序；组内页在 2 页以上才显示第二行按钮。
# 页签名必须和 `build_page()` 里的分派一致；改这里要同步 控制台.pyw 和自检。
TAB_GROUPS = (
    ("插件开关", ("地图", "可视化", "导出", "快捷键")),
    ("路点数据", ("人机路点", "录制", "数据")),
    ("部署与测试", ("部署", "车测")),
    ("开发调试", ("开发者选项",)),
)
# 旧配置（ui.tab 里存的是平铺页签名）→ 新分组：升级后落到原来那一页，不跳回第一页。
TAB_OLD_MAP = {
    "地图": "插件开关", "可视化": "插件开关", "导出": "插件开关", "快捷键": "插件开关",
    "人机路点": "路点数据", "录制": "路点数据", "数据": "路点数据",
    "部署": "部署与测试", "车测": "部署与测试",
    "开发者选项": "开发调试",
}

# 用户身份只建这两页（2026-11-24 用户要求：别人拿到自己选当用户还是开发）。
# 开发者身份把上面 TAB_GROUPS 里的 10 页全建出来，两页也包含在内。
USER_PAGES = ("地图", "部署")

# 「可视化」页各类数据的图例色块：游戏里画成什么颜色（照抄 src/editor.c 的 COL_* 与 vis_draw）。
# 顺序与 GROUPS 里各项的说明文字一一对应；C 侧改颜色这里要一起改。
VIS_COLORS = {
    "vis_nodes": ("#CCE0FF", "#FF8C0D", "#FF261F", "#4073F2"),
    "vis_crouch": ("#FF261F",),
    "vis_guard": ("#BF59FF", "#FF8C0D"),
    "vis_nano": ("#1AFF40", "#1AF2F2"),
    "vis_born": ("#2666FF", "#FF261F", "#B3B3B3"),
    "vis_supply": ("#FFD933", "#FF59B3", "#1AF2F2"),
    "vis_jump": ("#FFE00D",),
    "vis_tag": ("#FF8C0D",),
    "vis_player_marks": ("#FFD933",),
    "navmesh_show": ("#26FF8C",),
    "vis_compass": ("#F2CC47", "#A3BDE0"),
}


# 游戏内热键速查（控制台专用文档；游戏里不再显示这块）。按功能分组，组间空一行。
HUD_KEYS = (
    "【可视化】\n"
    "Ctrl+V 可视化总开关   Ctrl+Shift+6 可走面   Ctrl+Shift+7 方向罗盘\n"
    "\n"
    "【导出与采集】\n"
    "Ctrl+E 手动导出   Ctrl+Shift+X 只读采集（不创建对象）\n"
    "\n"
    "【标记】\n"
    "Delete 删除准星最近标记   Ctrl+0 显示/隐藏已放标记\n"
    "\n"
    "【编辑模式】\n"
    "Ctrl+1 编辑模式   Ctrl+2 放蹲守点   Ctrl+4 建守卫区\n"
    "Ctrl+5 撤销   Ctrl+6 保存   Ctrl+7 重载   Ctrl+8 阵营   Ctrl+9 状态写日志\n"
    "\n"
    "【路点编辑（Ctrl+Shift+字母）】\n"
    "Ctrl+Shift+A 选A点   Ctrl+Shift+N 加点   Ctrl+Shift+J A↔点 连/断\n"
    "Ctrl+Shift+D 禁用点   Ctrl+Shift+Z 撤销   Ctrl+Shift+S 手动保存   Ctrl+Shift+R 重套用\n"
    "\n"
    "【F2 路点菜单】\n"
    "F2 开关 / 长按 E 备用\n"
    "1-9 直选   小键盘 8/2 上下   5 确认   Esc/0 返回   左键确认 / 右键返回\n"
    "连续编辑：选好类型后停在类型页，5 可以一直放，1-6 随时换类型；Esc 只退一级，不会关菜单"
)


HUD_NOTES = (
    "· 游戏内数据面板和文字标签已删除；节点/守区等计数看 log\\ucf_mod.log 里的 [vis] 行，"
    "或控制台「上次运行」日志框。"
)


# 车测页底部的「车测是干什么的」：用户不熟车测，按「能 / 不能 / 注意」逐条列清楚
AT_CAN = [
    ("1. 崩溃回归（主用途）", "改完 DLL 跑一遍，没有 !!! crash = 没破坏加载链路；崩了日志里有崩溃栈"),
    ("2. 采数据", "进图时自动落 vis/navmesh_*.bin（可走面）；路线 JSON 要在地图里按 Ctrl+E 手动导"),
    ("3. 验数据链路", "日志 naved: grow / keep / pack: skip / pack: nav 证明编辑中、空白地图、成品切换真的生效"),
    ("4. 核对图号映射", "scene[0..15] + LOAD levelN + OK (map='沙漠要塞') 确认 buildIndex 对应哪张图"),
    ("5. 看导航数据", "[nav] diag: graphs=1 / waiting for PointGraph 看出这张图有没有 PointGraph / NavMeshGraph"),
    ("6. 版本对比", "同一组参数跑旧版和新版，日志逐行对照，哪张图开始不一样一目了然"),
    ("7. 批量扫图", "一次勾 11 张，不用手动进 11 次图、不用点大厅"),
]


AT_CANNOT = [
    "人机行为、路线对不对（车测没人机）",
    "正常开局路径（大厅 → 房间 → 开始比赛）",
    "画面 / UI / 帧率 / 手感",
    "玩法逻辑（击杀、胜负、经济）",
]


AT_NOTE = ("PASS 也可能是假通过：settle 太小（20 tick = 5 秒），问题还没触发就判过了；"
           "勾的图太少，也可能刚好全避开。")


AT_SUMMARY = ("车测 = 自动进图跑一圈的快速回归 + 数据采集；核心产出「哪张图会崩」，"
              "次要产出「数据用没用上、图号对不对」。")


AT_QUICK = "日志速记：看开头 armed、数中间 OK、看结尾 RESULT。"
