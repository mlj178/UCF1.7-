#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""静态自检：src/cfg.c 的开关表 vs tools/控制台.pyw 的面板分组

为什么要有它：C 侧多一个开关、面板里少一行，功能就永远关不掉，而且不报错。
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


def console_groups():
    """控制台.pyw 里的 GROUPS = [(组名, 说明, [(key, 标题, 说明, 默认), ...]), ...]"""
    tree = ast.parse(read(CONSOLE))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "GROUPS" for t in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError("控制台.pyw 里找不到 GROUPS")


def main():
    defs = cfg_defs()
    groups = console_groups()

    seen = {}
    for title, _hint, items in groups:
        for key, label, _desc, _default in items:
            assert key not in seen, "开关重复：%s（%s / %s）" % (key, seen[key], label)
            seen[key] = title

    expected = set(defs) - {"enabled"}          # enabled 是窗口顶部的总开关
    missing = expected - set(seen)
    extra = set(seen) - expected
    assert not missing, "cfg.c 有、控制台没有：" + ", ".join(sorted(missing))
    assert not extra, "控制台有、cfg.c 没有：" + ", ".join(sorted(extra))

    for key, (default, _doc) in defs.items():
        if key == "enabled":
            continue
        got = [d for _t, _h, items in groups for k, _l, _desc, d in items if k == key]
        assert got and got[0] == bool(default), \
            "默认值不一致：%s cfg=%d console=%s" % (key, default, got)

    build_group = seen.get("auto_waypoints")
    assert seen.get("hidden_map") != build_group, \
        "hidden_map（加载暴风地图）必须与建图三项分开分组"

    print("OK: %d feature switches in %d groups; hidden_map separate" % (
        len(seen), len(groups)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
