#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""静态自检：工作台数据档（① 备份版 / ② 成品 / ② 编辑中）三处必须一致。

2026-11-23：工作台顶栏从旧的「①备份 / ②开发 / ③部署」改成
「①备份 / ②成品 / ②编辑中」。③ 部署版只当游戏运行目录，不再作为数据档。
另外成品/编辑中的清单里可能有 grow（原生点全禁 + AddNode 新建）和 jump add，
工作台 2D 与 navview 3D 都要按同一套规则渲染，否则数字会和游戏对不上。

只读源码，不需要游戏、网络或窗口。
跑法：python tests/test_workbench_views.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
PROJ = UCF_ROOT


def read(rel):
    with open(os.path.join(PROJ, rel), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def main():
    html = read(os.path.join("console", "web", "nav-studio.html"))
    js = read(os.path.join("console", "web", "nav-studio-app.js"))
    server = read(os.path.join("console", "navserver.py"))
    navview = read(os.path.join("console", "web", "navview.html"))

    # 顶栏：三档 + 包选择器；旧的 profSel / data-vprof 不能再回来
    for key in ('id="viewSel"', 'id="packSel"', 'id="finalChip"'):
        assert key in html, "nav-studio.html 丢了 " + key
    assert "profSel" not in html and "profSel" not in js, "工作台还在用旧 profSel"
    assert "data-vprof" not in js, "工作台还在用旧 data-vprof"
    assert "③ 部署版" not in html, "nav-studio.html 还显示 ③ 部署版"

    # 前端三档与旧参数兼容
    assert "VIEW_ORDER = ['native', 'final', 'pack']" in js, "工作台三档顺序不对"
    assert "'② 成品'" in js and "'② 编辑中'" in js, "工作台缺少成品/编辑中标签"
    assert "ST.packByFolder" in js and "STORAGE_PACKS" in js, "工作台没有记住每个图的包"
    assert "syncURL" in js and "u.searchParams.set('view'" in js, "工作台 URL 没有同步数据档"
    assert "data-pack-view" in js, "地图数据页没有按包查看的入口"

    # 渲染语义：grow 必须当成空白底图；jump add 要追加到跳链
    assert "s === 'grow'" in js, "工作台 applyTxt 没有识别 grow"
    assert "t[0] === 'jump'" in js, "工作台没有解析清单里的 jump add"
    assert "fromTxt" in js, "工作台跳链没有标出来源"

    # 服务端三档 + 旧别名
    assert 'PROFILE_ORDER = ("native", "final", "pack")' in server, "navserver 三档不对"
    for alias in ('"dev": "final"', '"deploy": "final"', '"test": "pack"'):
        assert alias in server, "navserver 丢了旧别名 " + alias
    assert "VIEW_NOTE" in server, "navserver 没有给旧链接提示"
    assert '"grow": bool(manifest.get("grow"))' in server, "navserver 没把 grow 带给前端"
    assert '"full": str(pk.get("name")' in server, "navserver 没给 per-map 包的全名"

    # navview：同一套 grow / jump / 单向边
    assert "t === \"blank\" || t === \"grow\"" in navview, "navview 没把 grow 当空白底图"
    assert "function parseJumpAdds" in navview, "navview 没解析 jump add"
    assert "addout" in navview and "delout" in navview, "navview 没识别单向边"
    assert '"② 成品"' in navview and '"② 编辑中"' in navview, "navview 下拉还是旧标签"

    print("OK: 工作台三档（① 备份 / ② 成品 / ② 编辑中）+ grow/jump/单向边一致")


if __name__ == "__main__":
    main()
