#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""静态自检：src/cfg.c 的开关表 vs tools/控制台.pyw 的页签分组

为什么要有它：C 侧多一个开关、面板里少一行，功能就永远关不掉，而且不报错。
例外是「建图」页：2026-11-17 控制台删掉了这一页的三个开关，C 侧键留给旧配置
与回滚用（默认仍为开），所以它们在 RETIRED 里显式豁免，不允许再冒回面板。

另外核对「状态面板」页的快捷键文案：那一页照抄 src/editor.c 的 hud_refresh()，
两边只改一边就会在游戏里显示过期的键位，所以逐行做子串比对。

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
# C 侧键保留默认开，旧 ucf_mod.json 与回滚仍然有效；面板里不许再出现。
RETIRED = {"auto_waypoints", "auto_crouch", "ghost_areas"}
TABS = ["地图", "查看", "状态面板", "手动"]   # 「测试数据」「数据」不是开关页，不在此列
# 三态开关（0 关 / 1 近距 / 2 全部）：控件不是 switch，但必须在「状态面板」页有入口
CUSTOM = {"vis_labels": "状态面板"}


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
    assert console_const("LABEL_DEFAULT") == defs["vis_labels"][0], \
        "vis_labels 默认值不一致：cfg=%d console=%s" % (
            defs["vis_labels"][0], console_const("LABEL_DEFAULT"))

    titles = [title for title, _hint, _items in groups]
    assert titles == TABS, "控制台页签应为 %s，实际 %s" % (TABS, titles)
    assert seen.get("hidden_map") == "地图", \
        "hidden_map（加载暴风地图）必须留在「地图」页"
    assert seen.get("hud") == "状态面板", \
        "hud（进图显示状态面板）必须单独在「状态面板」页，不许混在「查看」"
    for key in console_const("LAYER_KEYS"):
        assert seen.get(key) == "状态面板", \
            "可视化开关 %s 必须在「状态面板」页" % key
    assert seen.get("vis_labels") == "状态面板", \
        "文字标签（vis_labels）必须在「状态面板」页"

    editor_c = read(os.path.join(PROJ, "src", "editor.c"))
    keys = console_const("HUD_KEYS").splitlines()
    for line in keys:
        assert line in editor_c, \
            "「状态面板」页的快捷键与 src/editor.c 不一致（改一边忘一边）：" + line

    # cfg.c 里加了键、editor.c 忘了读 -> 开关永远不生效，也不会报错
    for key in console_const("LAYER_KEYS"):
        assert ('cfg_bool("%s"' % key) in editor_c, \
            "cfg.c 有 %s，但 editor.c 没有 cfg_bool 读取" % key
    for key in ("hud_states", "hud_keys", "hud_log"):
        assert ('cfg_bool("%s"' % key) in editor_c, \
            "cfg.c 有 %s，但 editor.c 没有 cfg_bool 读取" % key
    assert 'cfg_int("vis_labels"' in editor_c, \
        "cfg.c 有 vis_labels，但 editor.c 没有 cfg_int 读取"

    # 测试数据面板必须是页签（2026-11-17 21:10 用户要求：不再压在上面常驻）
    src = read(CONSOLE)
    assert 'self.tabview.add("测试数据")' in src, "测试数据必须是页签"
    assert "build_pack_panel" not in src, "build_pack_panel 旧入口应已删除"
    assert src.index('add("测试数据")') < src.index('add("数据")'), \
        "「测试数据」页应在「数据」页之前"
    assert 'text="打开文件夹"' in src and "def open_folder" in src, \
        "数据页的「打开文件夹」按钮 / open_folder 不见了"

    print("OK: %d feature switches in %d tabs (%s); %d build-map switches retired; "
          "HUD keys %d/%d match editor.c" % (
              len(seen), len(groups), "/".join(titles), len(RETIRED),
              len(keys), len(keys)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
