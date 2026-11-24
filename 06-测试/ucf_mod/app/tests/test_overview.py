#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：地图总览页 / 三视图 / 数据口径。

跑法：python app/tests/test_overview.py

只读，不开窗口。查：
  1) 「地图总览」在「路点数据」第一位，TAB_OLD_MAP 能迁移
  2) 三视图、刷新、详情入口都在
  3) 数据层能把 grow / keep 的点边算对（grow 以 0 为底，keep 以原生为底）
  4) 状态判定：已同步 / 待发布 / 只有成品 / 未开始 / 无点图
  5) 总览只读：数据层不写盘，界面不删除文件
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)
APP = os.path.join(UCF_ROOT, "app")
for _p in (os.path.join(APP, "core"), APP):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from ui.consts import TAB_GROUPS, TAB_OLD_MAP  # noqa: E402
from ui.overview import parse_nav, status_for  # noqa: E402

FAIL = []


def check(cond, what):
    if cond:
        print("  OK   " + what)
    else:
        print("  !!   " + what)
        FAIL.append(what)


def read(rel):
    with open(os.path.join(UCF_ROOT, rel), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def main():
    print("== 1) 页签位置")
    pages = dict(TAB_GROUPS)
    check(pages.get("路点数据", ())[:1] == ("地图总览",), "地图总览是「路点数据」第一页")
    check("地图总览" in TAB_OLD_MAP, "TAB_OLD_MAP 覆盖地图总览（旧配置能迁移）")

    print("== 2) 三视图")
    src = read(os.path.join("app", "tabs", "overview.py"))
    for token in ("_ov_build_matrix", "_ov_build_cards", "_ov_build_board",
                  "def refresh_overview", "def ov_on_view", "def ov_toggle_row"):
        check(token in src, "overview.py 有 %s" % token)
    for name in ("矩阵", "卡片", "看板"):
        check('"%s"' % name in src, "视图名 %s 在" % name)
    check("collect_overview" in read(os.path.join("app", "ui", "overview.py")),
          "ui/overview.py 有 collect_overview()")

    print("== 3) grow / keep 点边")
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "grow.txt")
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write("blank\ngrow\nnode add 1 2 3\nnode add 4 5 6\n"
                    "edge add 1 2\nedge out 2 3\n")
        g = parse_nav(p, base_nodes=786, base_edges=1391)
        check(g and g["nodes"] == 2, "grow 点数 = 新增 2（不被原生 786 撑大）")
        check(g and g["edges"] == 2, "grow 边数 = 新增 2")

        p2 = os.path.join(td, "keep.txt")
        with open(p2, "w", encoding="utf-8", newline="\n") as f:
            f.write("keep\nnode add 1 2 3\nnode del 9\nedge add 1 2\nedge del 3 4\n")
        k = parse_nav(p2, base_nodes=10, base_edges=20)
        check(k and k["nodes"] == 10 and k["edges"] == 20,
              "keep 点数 = 原生 10 + 1 - 1；边数 = 20 + 1 - 1")
        check(k and k["mode"] == "keep", "keep 模式识别")

    print("== 4) 状态判定")
    a = {"sha256": "A", "changes": 3}
    b = {"sha256": "B", "changes": 1}
    check(status_for(False, None, None) == "nograph", "无 map.json -> 无点图")
    check(status_for(True, None, None) == "idle", "无草稿无成品 -> 未开始")
    check(status_for(True, None, a) == "finalonly", "只有成品 -> finalonly")
    check(status_for(True, a, None) == "publish", "有改动、没成品 -> 待发布")
    check(status_for(True, {"sha256": "A", "changes": 0}, None) == "drafting",
          "刚建、0 点改动、没成品 -> 编辑中")
    check(status_for(True, a, a) == "sync", "草稿=成品（sha 相同）-> 已同步")
    check(status_for(True, a, b) == "publish", "草稿和成品不同 -> 待发布")

    print("== 5) 只读")
    data_src = read(os.path.join("app", "ui", "overview.py"))
    check("os.makedirs" not in data_src and "os.remove" not in data_src,
          "数据层不建目录 / 不删文件")
    check("shutil" not in data_src, "数据层不复制 / 移动文件")
    check("open(" in data_src and 'open(path, "r"' in data_src,
          "数据层只读打开文件")

    if FAIL:
        print("\n!! %d 项没过" % len(FAIL))
        return 1
    print("\nOK: 地图总览 / 三视图 / 点边口径 / 状态 / 只读 都对得上")
    return 0


if __name__ == "__main__":
    sys.exit(main())
