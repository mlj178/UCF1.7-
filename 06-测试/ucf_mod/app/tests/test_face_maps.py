#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：纯面图（胜利广场 / 死亡擂台）画点的整条链路（2026-11-27）。

用户问「胜利广场这张图我也选择不了」，选了「插件运行时补一张 PointGraph」+「grow 时关掉可走面」。

事实（app/tools/data/scan_native_nav.py 实读游戏场景）：
    level4  胜利广场  NavMeshGraph · NY_TM_NavMesh     716 顶点 / 976 三角，**没有 PointGraph**
    level11 死亡擂台  NavMeshGraph · DeathRing_NavMesh  60 顶点 /  94 三角，**没有 PointGraph**
（对比 level9 飓风危城：有 PointGraph，只是 0 个点 —— 所以它能直接画。）

链路：
    1) ui/maps.py        load_maps 收纯面图，指纹空串；face_maps() 说清证据
    2) ui/packs.py       runtime_fp() 给运行期指纹 n0-…；纯面图可以建草稿，不能发布
    3) tabs/waypoint.py  地图下拉带「· 纯面图」后缀；开始编辑照常可用
    4) src/editor.c      nav_edit_tick：没有 PointGraph 且有测试包 → navfix_add_point_graph()
    5) src/navfix.c      手工挂 PointGraph 到 AstarData.graphs + Scan；grow 时 navfix_drop_navmesh()
    6) 车测实测（2026-11-27 15:39）：level4 日志 pointgraph: created -> 1 -> 2 / navmesh: 已摘掉 /
       grow 0 -> 1 节点 / RESULT PASS

跑法：python app/tests/test_face_maps.py
"""
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.isfile(os.path.join(ROOT, ".ucfroot")) and os.path.dirname(ROOT) != ROOT:
    ROOT = os.path.dirname(ROOT)


def read(*parts):
    with open(os.path.join(ROOT, *parts), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def data_layer():
    app = os.path.join(ROOT, "app")
    for p in (os.path.join(app, "ui"), os.path.join(app, "core"), app,
              os.path.join(app, "tabs"), os.path.join(app, "tabs", "deploy"),
              os.path.join(app, "tabs", "record"), os.path.join(app, "tabs", "dev")):
        if p not in sys.path:
            sys.path.insert(0, p)

    from ui.maps import load_maps, face_maps, maps_not_listed, map_folder
    from ui.packs import runtime_fp

    ms = load_maps()
    by_lv = {lv: (lab, fp) for lv, lab, fp in ms}
    assert by_lv.get("level4") == ("胜利广场", ""), "胜利广场 没进 load_maps（或指纹不是空串）"
    assert by_lv.get("level11") == ("死亡擂台", ""), "死亡擂台 没进 load_maps"
    assert by_lv.get("level1", ("", ""))[1], "运输船 的指纹没了"
    assert {lv for lv, _l, _n in face_maps()} == {"level4", "level11"}, "face_maps 只该有 04/07"
    miss = [m[1] for m in maps_not_listed([m[0] for m in ms])]
    assert "level4" not in miss and "level11" not in miss, "纯面图还在「下拉里没有」的名单里"
    assert map_folder("level4", "") == "04_NY_TM胜利广场", "纯面图文件夹名算不对（fp 空串）"
    # 运行期指纹：这两张补完点图就是 0 点图
    assert runtime_fp("level4", "") == "n0-0000000000000000", "纯面图运行期指纹不对"
    assert runtime_fp("level1", "n786-57a46e3465c847cb") == "n786-57a46e3465c847cb", "点图指纹被改了"
    assert runtime_fp("", "") == "", "空关卡不该有指纹"


def ui_layer():
    from tabs.waypoint import WaypointTab
    from ui.packs import runtime_fp

    assert WaypointTab.map_label("level4", "胜利广场", "") == "胜利广场（level4 · 纯面图）"
    assert WaypointTab.map_label("level1", "运输船", "n786-57a46e3465c847cb") == "运输船（level1）"
    d = types.SimpleNamespace(opt_map=object(), current_map=lambda: ("level4", "胜利广场", ""))
    assert WaypointTab.is_face_map(d) is True, "is_face_map 认不出纯面图"
    d.current_map = lambda: ("level1", "运输船", "n786-57a46e3465c847cb")
    assert WaypointTab.is_face_map(d) is False, "is_face_map 把点图当成纯面图"

    class W(object):
        def __init__(self):
            self.kw = {}

        def configure(self, **kw):
            self.kw.update(kw)

        def winfo_manager(self):
            return "pack"

        def pack_forget(self):
            self.kw["packed"] = False

    class FakeTab(WaypointTab):
        pass

    o = FakeTab()
    o.opt_map = object()
    o.current_map = lambda: ("level4", "胜利广场", "")
    o.lbl_draft, o.lbl_markers, o.lbl_publish, o.lbl_mode, o.wp_meta = W(), W(), W(), W(), W()
    o.btn_start_draft, o.btn_open_draft, o.btn_reset_draft = W(), W(), W()
    o.btn_delete_draft, o.btn_clear_markers, o.btn_promote = W(), W(), W()
    o.open_workbench = lambda: None
    o.start_or_open_draft = lambda: None
    o.draft_exists = lambda: False

    WaypointTab.refresh_draft_panel(o)
    assert o.btn_start_draft.kw.get("text") == "开始编辑这张图", "纯面图没给「开始编辑这张图」"
    assert o.btn_start_draft.kw.get("command") is o.start_or_open_draft, "主按钮没接建草稿"
    assert o.btn_promote.kw.get("state") == "disabled", "纯面图「发布」没灰（成品会撞指纹）"
    assert "纯面图" in o.lbl_publish.kw.get("text", ""), "发布卡没解释为什么不能发"

    WaypointTab.update_mode_hint(o)
    txt = o.lbl_mode.kw.get("text", "")
    assert "纯面图" in txt and ("补一张" in txt or "0 点" in txt), "顶部没解释「插件会现场补点图」"
    WaypointTab.refresh_wp_status(o)
    assert "纯面图" in o.wp_meta.kw.get("text", ""), "指纹那行没写「纯面图」"


def source_layer():
    way = read("app", "tabs", "waypoint.py")
    packs = read("app", "ui", "packs.py")
    maps = read("app", "ui", "maps.py")
    con = read("app", "控制台.pyw")
    editor = read("src", "editor.c")
    navfix = read("src", "navfix.c")

    # 数据层
    assert "def face_maps" in maps and 'out.append((lv, cn, ""))' in maps, "ui/maps.py 没把纯面图收进 load_maps"
    assert "n0-0000000000000000" in packs and "def runtime_fp" in packs, "packs.py 缺运行期指纹"
    # 界面
    assert "def is_face_map" in way and "纯面图" in way, "waypoint.py 缺纯面图分支"
    assert "现场补" in (way + packs + con), "界面没说「插件进图会现场补点图」"
    assert "只能停在「编辑中」" in way, "发布卡没写清纯面图只能编辑中"
    # 控制台启动
    assert 'pk.get("face")' in con, "控制台启动没认纯面图的标记"
    # 插件
    assert "navfix_add_point_graph" in editor and "navfix_drop_navmesh" in editor, \
        "editor.c 没把「补点图 / 摘可走面」接进 tick / grow"
    assert "navfix_add_point_graph" in navfix and "PointGraph" in navfix, \
        "navfix.c 里没看到补 PointGraph 的实现"
    assert "i_class_get_method_from_name(cls, \"RemoveGraph\", 1)" in navfix, \
        "navfix.c 没走 AstarData.RemoveGraph 摘可走面"
    assert "pointgraph: created" in navfix, "navfix.c 缺创建日志（车测靠它确认）"


def main():
    data_layer()
    ui_layer()
    source_layer()
    print("OK: 纯面图链路（可选 + 建草稿 + 插件现场补 PointGraph + grow 摘可走面 + 不能发布）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
