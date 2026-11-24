#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""静态自检：src/cfg.c 的开关表 vs console/控制台.pyw 的页签分组

为什么要有它：C 侧多一个开关、面板里少一行，功能就永远关不掉，而且不报错。
例外是「建图」页：2026-11-17 控制台删掉了这一页的三个开关，C 侧键留给旧配置
与回滚用（默认仍为开），所以它们在 RETIRED 里显式豁免，不允许再冒回面板。

另外核对页面归属：可视化、导出两页的开关必须留在对应页。

本测试只读两份源码，不需要游戏、部署端、网络或窗口。

跑法：python tests/test_console_switches.py
"""
import ast
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
PROJ = UCF_ROOT
CFG_C = os.path.join(PROJ, "src", "cfg.c")
CONSOLE = os.path.join(PROJ, "app", "控制台.pyw")
# 2026-11-24 目录重构：页签常量在 app/ui/consts.py，页签装配在 app/控制台.pyw
CONSTS = os.path.join(PROJ, "app", "ui", "consts.py")
DEV_TAB = os.path.join(PROJ, "app", "tabs", "dev", "tab.py")
REC_TAB = os.path.join(PROJ, "app", "tabs", "record", "tab.py")
VIS_TAB = os.path.join(PROJ, "app", "tabs", "vis.py")
DATA_TAB = os.path.join(PROJ, "app", "tabs", "data.py")
AUTOTEST_TAB = os.path.join(PROJ, "app", "tabs", "autotest.py")
OVERVIEW_TAB = os.path.join(PROJ, "app", "tabs", "overview.py")
KIT = os.path.join(PROJ, "app", "ui", "kit.py")

# 2026-11-17：控制台删掉「建图」页（自动铺路点 / 自动补蹲守点 / 幽灵守卫区）。
# 2026-11-18：用户要求自动铺设回控制台，落在「手动」页（不再是 RETIRED）。
# 2026-11-19：用户要求删除「手动」页的自动铺设整块，回到 RETIRED（C 侧键保留，默认仍为开）。
# 2026-11-19：用户要求删除 editor（允许游戏内编辑）；C 侧仍按默认 1 运行。
# 2026-11-19：用户要求整个「手动」页删除，collect_only 入口一并下线（collect.flag 仍可用）。
RETIRED = {"auto_waypoints", "auto_crouch", "ghost_areas", "editor", "collect_only"}
TABS = ["地图", "可视化", "导出", "快捷键"]   # 「测试数据」「数据」「车测」不是开关页，不在此列
# 非 bool 开关（画笔字符串等）：控件不是 switch，但必须在对应页有入口
CUSTOM = {"wp_menu": "人机路点", "wp_autoground": "人机路点"}
# 2026-11-19：可视化改成逐类开关（读+画同一颗），全部落在「可视化」页
# 2026-11-20：加 vis_compass（方向罗盘，东南西北）——它不读游戏数据，但同样是
#              「画不画」，所以和可走面一样归在「可视化」页并在 editor.c 里读。
# 2026-11-21：玩家坐标记录搬出「可视化」，和原始轨迹采集一起进新页「开发者选项」；
#              该页的开关不在 GROUPS 里，单独定义在控制台的 DEV_ITEMS。
VIS_DATA = ("vis_nodes", "vis_crouch", "vis_guard", "vis_nano", "vis_born",
            "vis_supply", "vis_jump", "vis_tag", "navmesh_show", "vis_compass")
DEV_PAGE = "开发者选项"


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def cfg_defs():
    """cfg.c 里 g_defs[] 的 { key, 默认值, 说明 }。"""
    src = read(CFG_C)
    body = src[src.index("g_defs[]"):src.index("const CFG_DEF* cfg_table")]
    defs = {}
    for key, default, doc in re.findall(
            r'\{\s*"([^"]+)"\s*,\s*([01])\s*,\s*"([^"]*)"\s*\}', body):
        defs[key] = (int(default), doc)
    return defs


def console_const(name):
    """控制台.pyw 里的模块级字符串常量（GROUPS / HUD_KEYS …）。"""
    tree = ast.parse(read(CONSTS))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError("控制台.pyw 里找不到 " + name)


def console_groups():
    """控制台.pyw 里的 GROUPS = [(组名, 说明, [(key, 标题, 说明, 默认), ...]), ...]"""
    return console_const("GROUPS")


def console_dev_items():
    """控制台.pyw 里的 DEV_ITEMS：单开的「开发者选项」页的开关，格式同 GROUPS 的 items。"""
    return console_const("DEV_ITEMS")


def main():
    defs = cfg_defs()
    groups = console_groups()
    dev_items = console_dev_items()

    seen = {}
    for title, _hint, items in groups:
        for key, label, _desc, _default in items:
            assert key not in seen, "开关重复：%s（%s / %s）" % (key, seen[key], label)
            seen[key] = title
    # 2026-11-21：开发者选项单独成页（页签排在最后），开关同样要「cfg.c 有 -> 面板能关」
    for key, label, _desc, _default in dev_items:
        assert key not in seen, "开关重复：%s（%s / %s）" % (key, seen[key], label)
        seen[key] = DEV_PAGE
    for key, title in CUSTOM.items():
        assert key not in seen, "开关重复：%s（%s / %s）" % (key, seen[key], title)
        seen[key] = title

    for key in RETIRED:
        assert key not in seen, "自动铺设开关 %s 已从控制台删除，不能再出现在「%s」页" % (
            key, seen[key])

    # enabled 是窗口顶部总开关：2026-11-24 起只在开发者身份显示（用户身份不建这个控件）
    expected = set(defs) - {"enabled"} - RETIRED
    missing = expected - set(seen)
    extra = set(seen) - expected
    assert not missing, "cfg.c 有、控制台没有：" + ", ".join(sorted(missing))
    assert not extra, "控制台有、cfg.c 没有：" + ", ".join(sorted(extra))

    for key, (default, _doc) in defs.items():
        if key == "enabled" or key in RETIRED or key in CUSTOM:
            continue
        got = [d for _t, _h, items in groups for k, _l, _desc, d in items if k == key]
        got += [d for k, _l, _desc, d in dev_items if k == key]
        assert got and got[0] == bool(default), \
            "默认值不一致：%s cfg=%d console=%s" % (key, default, got)

    titles = [title for title, _hint, _items in groups]
    assert titles == TABS, "控制台页签应为 %s，实际 %s" % (TABS, titles)
    assert seen.get("hidden_map") == "地图", \
        "hidden_map（加载暴风地图）必须留在「地图」页"
    assert seen.get("visualizer") == "可视化", \
        "可视化总开关（visualizer）必须留在「可视化」页顶部（2026-11-19 用户要求）"
    for key in VIS_DATA:
        assert seen.get(key) == "可视化", \
            "可视化开关 %s 必须在「可视化」页（2026-11-19 用户要求）" % key
    # 2026-11-21 用户要求：玩家坐标记录 + 原始轨迹采集搬到「开发者选项」，不再在可视化 / 录制页
    assert seen.get("vis_player_marks") == DEV_PAGE, \
        "玩家坐标记录开关必须搬到「%s」页（2026-11-21 用户要求）" % DEV_PAGE
    assert seen.get("vis_player_marks") != "可视化", "玩家坐标记录不能再留在「可视化」页"

    editor_c = read(os.path.join(PROJ, "src", "editor.c"))
    assert "editor_freecam_tick" in editor_c and "CinemachineBrain" in editor_c, \
        "车测自由视角（freecam）实现缺失：editor_freecam_tick / CinemachineBrain"

    # 2026-11-21 用户要求：玩家坐标记录只在本次（当前场景）画金色方块，不连折线，
    # 历史坐标只当日志 —— 旧代码会把文件里所有历史点和顺序折线一起画进场景。
    assert "g_pmSesP[PM_MAX]" in editor_c and "g_pmSesN" in editor_c, \
        "玩家坐标记录必须只画本次会话的点（g_pmSesP / g_pmSesN）"
    assert "vis_pmark_line" not in editor_c, "玩家坐标记录不再连折线（vis_pmark_line 已删）"
    assert "g_pmSesN = 0;" in editor_c, "换图时必须清空本次的玩家坐标记录"
    assert "bs_solid(g_pmP[i]" not in editor_c, "vis_draw 不能再画 player_marks.txt 里的历史记录"

    # cfg.c 里加了键、editor.c 忘了读 -> 开关永远不生效，也不会报错
    for key in ("visualizer",) + VIS_DATA:
        assert ('cfg_bool("%s"' % key) in editor_c, \
            "cfg.c 有 %s，但 editor.c 没有 cfg_bool 读取" % key

    # 2026-11-19 用户要求：「测试数据」页删除，选图/选包并入「人机路点」①；
    # 人机路点必须在数据页之前（数据页读它建的 opt_pack / opt_map）。
    src = read(CONSOLE)
    assert 'add("测试数据")' not in src, "「测试数据」页已删除，不能再出现"
    assert "build_pack_panel" not in src, "build_pack_panel 旧入口应已删除"

    # 2026-11-24 用户要求：页签按功能分 4 组（插件开关 / 路点数据 / 部署与测试 / 开发调试）。
    # 分组表是唯一来源，和 控制台.pyw 的 build_page() 分派对应。
    nav = console_const("TAB_GROUPS")
    group_names = [g[0] for g in nav]
    pages_of = {g[0]: list(g[1]) for g in nav}
    assert group_names == ["插件开关", "路点数据", "部署与测试", "开发调试"], \
        "控制台分组应为 插件开关/路点数据/部署与测试/开发调试，实际 %s" % group_names
    flat_pages = [p for pages in pages_of.values() for p in pages]
    assert len(flat_pages) == len(set(flat_pages)) == 11, \
        "11 个页签必须一组一个、不重不漏，实际 %s" % flat_pages
    assert pages_of["插件开关"] == ["地图", "可视化", "导出", "快捷键"], \
        "「插件开关」组应为 地图/可视化/导出/快捷键"
    assert pages_of["路点数据"][0] == "地图总览", \
        "「地图总览」应排在「路点数据」第一位"
    assert pages_of["路点数据"].index("人机路点") < pages_of["路点数据"].index("数据"), \
        "「人机路点」页应在「数据」页之前（数据页读它建的 opt_pack / opt_map）"
    assert "def build_overview_tab" in read(OVERVIEW_TAB) and "def refresh_overview" in read(OVERVIEW_TAB), \
        "「地图总览」页缺少 build_overview_tab / refresh_overview"
    assert "build_overview_tab(frame)" in src and "refresh_overview()" in src, \
        "控制台没有接入地图总览页"
    assert 'text="打开文件夹"' in read(DATA_TAB) and "def open_folder" in read(KIT), \
        "数据页的「打开文件夹」按钮 / open_folder 不见了"

    # 2026-11-21 用户要求：新开一页「开发者选项」（页签排在最后），
    # 玩家坐标记录从「可视化」、原始轨迹采集从「录制」搬进去。
    assert "开发者选项" in pages_of["开发调试"], \
        "「开发者选项」必须是独立一页（收在「开发调试」组）"
    assert group_names.index("部署与测试") < group_names.index("开发调试"), \
        "「开发调试」组应排在最后"
    dev_src = read(DEV_TAB)
    dev_body = dev_src[dev_src.index("def build_dev_tab("):dev_src.index("def build_pmark_card(")]
    assert "self.build_pmark_card(body)" in dev_body, \
        "「开发者选项」页少了玩家坐标记录卡片"
    assert "self.build_trace_card(body)" in dev_body, \
        "「开发者选项」页少了原始轨迹采集卡片"
    rec_src = read(REC_TAB)
    rec_body = rec_src[rec_src.index("def build_record_tab("):rec_src.index("def build_rec_ready(")]
    assert "build_trace_card" not in rec_body, \
        "「录制」页不该再放原始轨迹采集（2026-11-21 已搬到开发者选项）"
    vis_src = read(VIS_TAB)
    vis_body = vis_src[vis_src.index("def build_vis_tab("):]
    assert "build_pmark_card" not in vis_body, \
        "「可视化」页不该再放玩家坐标记录卡片（2026-11-21 已搬到开发者选项）"

    # 车测页（2026-11-18 用户要求：启动器里能直接跑车测，不用命令行 autotest.ps1）
    assert "车测" in pages_of["部署与测试"], "车测必须是页签（收在「部署与测试」组）"
    assert group_names.index("路点数据") < group_names.index("部署与测试"), \
        "「数据」应在「车测」之前（分组顺序：路点数据 → 部署与测试）"
    at_src = read(AUTOTEST_TAB)
    assert "UCF_AUTOTEST" in at_src and "def run_autotest" in at_src, \
        "车测页缺少 UCF_AUTOTEST / run_autotest"
    assert "UCF_FREECAM" in at_src and 'text="自由视角' in at_src, \
        "车测页缺少「自由视角」（UCF_FREECAM）"
    assert 'os.remove(find_log("autotest.txt"))' in at_src, \
        "车测开跑前必须删旧 autotest.txt，否则上一次的 PASS 会被当成这次的结果"
    can = console_const("AT_CAN")
    cannot = console_const("AT_CANNOT")
    assert len(can) == 7 and len(cannot) == 4, \
        "车测说明应为「7 项能做 + 4 项不能做」，实际 %d / %d" % (len(can), len(cannot))
    joined = " ".join(name + desc for name, desc in can) + " ".join(cannot)
    for key in ("!!! crash", "buildIndex", "pack: skip", "PointGraph", "大厅"):
        assert key in joined, "车测说明缺少 %s" % key
    assert "假通过" in console_const("AT_NOTE"), "车测说明缺少「假通过」提醒"

    print("OK: %d feature switches in %d tabs (%s); %d build-map switches retired" % (
        len(seen), len(groups), "/".join(titles), len(RETIRED)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
