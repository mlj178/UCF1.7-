#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""静态自检：src/cfg.c 的开关表 vs tools/控制台.pyw 的页签分组

为什么要有它：C 侧多一个开关、面板里少一行，功能就永远关不掉，而且不报错。
例外是「建图」页：2026-11-17 控制台删掉了这一页的三个开关，C 侧键留给旧配置
与回滚用（默认仍为开），所以它们在 RETIRED 里显式豁免，不允许再冒回面板。

另外核对页面归属：可视化、导出、手动各页的开关必须留在对应页。

本测试只读两份源码，不需要游戏、部署端、网络或窗口。

跑法：python tools/test_console_switches.py
"""
import ast
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
CFG_C = os.path.join(PROJ, "src", "cfg.c")
CONSOLE = os.path.join(HERE, "控制台.pyw")

# 2026-11-17：控制台删掉「建图」页（自动铺路点 / 自动补蹲守点 / 幽灵守卫区）。
# 2026-11-18：用户要求自动铺设回控制台，落在「手动」页（不再是 RETIRED）。
RETIRED = set()
TABS = ["地图", "可视化", "导出", "快捷键", "手动"]   # 「测试数据」「数据」「车测」不是开关页，不在此列
# 非 bool 开关（画笔字符串等）：控件不是 switch，但必须在对应页有入口
CUSTOM = {"wp_menu": "人机路点", "wp_autoground": "人机路点"}
# 2026-11-19：可视化改成逐类开关（读+画同一颗），全部落在「可视化」页
VIS_DATA = ("vis_nodes", "vis_crouch", "vis_guard", "vis_nano", "vis_born",
            "vis_supply", "vis_jump", "vis_tag", "navmesh_show")


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
    tree = ast.parse(read(CONSOLE))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError("控制台.pyw 里找不到 " + name)


def console_groups():
    """控制台.pyw 里的 GROUPS = [(组名, 说明, [(key, 标题, 说明, 默认), ...]), ...]"""
    return console_const("GROUPS")


def main():
    defs = cfg_defs()
    groups = console_groups()

    seen = {}
    for title, _hint, items in groups:
        for key, label, _desc, _default in items:
            assert key not in seen, "开关重复：%s（%s / %s）" % (key, seen[key], label)
            seen[key] = title
    for key, title in CUSTOM.items():
        assert key not in seen, "开关重复：%s（%s / %s）" % (key, seen[key], title)
        seen[key] = title

    for key in RETIRED:
        assert key not in seen, "「建图」开关 %s 已从控制台删除，不能再出现在「%s」页" % (
            key, seen[key])

    expected = set(defs) - {"enabled"} - RETIRED   # enabled 是窗口顶部的总开关
    missing = expected - set(seen)
    extra = set(seen) - expected
    assert not missing, "cfg.c 有、控制台没有：" + ", ".join(sorted(missing))
    assert not extra, "控制台有、cfg.c 没有：" + ", ".join(sorted(extra))

    for key, (default, _doc) in defs.items():
        if key == "enabled" or key in RETIRED or key in CUSTOM:
            continue
        got = [d for _t, _h, items in groups for k, _l, _desc, d in items if k == key]
        assert got and got[0] == bool(default), \
            "默认值不一致：%s cfg=%d console=%s" % (key, default, got)

    titles = [title for title, _hint, _items in groups]
    assert titles == TABS, "控制台页签应为 %s，实际 %s" % (TABS, titles)
    assert seen.get("hidden_map") == "地图", \
        "hidden_map（加载暴风地图）必须留在「地图」页"
    for key in ("auto_waypoints", "auto_crouch", "ghost_areas"):
        assert seen.get(key) == "手动", \
            "自动铺设开关 %s 必须在「手动」页（2026-11-18 用户要求）" % key
    assert seen.get("visualizer") == "可视化", \
        "可视化总开关（visualizer）必须留在「可视化」页顶部（2026-11-19 用户要求）"
    for key in VIS_DATA:
        assert seen.get(key) == "可视化", \
            "可视化开关 %s 必须在「可视化」页（2026-11-19 用户要求）" % key

    editor_c = read(os.path.join(PROJ, "src", "editor.c"))
    assert "editor_freecam_tick" in editor_c and "CinemachineBrain" in editor_c, \
        "车测自由视角（freecam）实现缺失：editor_freecam_tick / CinemachineBrain"

    # cfg.c 里加了键、editor.c 忘了读 -> 开关永远不生效，也不会报错
    for key in ("visualizer",) + VIS_DATA:
        assert ('cfg_bool("%s"' % key) in editor_c, \
            "cfg.c 有 %s，但 editor.c 没有 cfg_bool 读取" % key

    # 测试数据面板必须是页签（2026-11-17 21:10 用户要求：不再压在上面常驻）
    src = read(CONSOLE)
    assert 'self.tabview.add("测试数据")' in src, "测试数据必须是页签"
    assert "build_pack_panel" not in src, "build_pack_panel 旧入口应已删除"
    assert src.index('add("测试数据")') < src.index('add("数据")'), \
        "「测试数据」页应在「数据」页之前"
    assert 'text="打开文件夹"' in src and "def open_folder" in src, \
        "数据页的「打开文件夹」按钮 / open_folder 不见了"

    # 车测页（2026-11-18 用户要求：启动器里能直接跑车测，不用命令行 autotest.ps1）
    assert 'self.tabview.add("车测")' in src, "车测必须是页签"
    assert src.index('add("数据")') < src.index('add("车测")'), \
        "「车测」页应在「数据」页之后"
    assert "UCF_AUTOTEST" in src and "def run_autotest" in src, \
        "车测页缺少 UCF_AUTOTEST / run_autotest"
    assert "UCF_FREECAM" in src and 'text="自由视角' in src, \
        "车测页缺少「自由视角」（UCF_FREECAM）"
    assert "os.remove(AUTOTEST_TXT)" in src, \
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
