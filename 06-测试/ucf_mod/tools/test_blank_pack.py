#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""静态自检：测试包两条建法（空白地图 grow / 原版基础 + 新增 keep）有没有被改断。

空白地图 grow = 插件先把该图所有原生点禁用，再把包里的 node add / edge add 按
PointGraph.AddNode 真·新建（不借槽位、点数不限）。
原版基础 + 新增 keep = 原生点一个都不动，只把新点加到原图上。
blank / seed 两种旧建法 2026-11-20 已删：旧文件里的 blank 行按 grow 读，老包照常能用。

链路跨 5 个文件：src/editor.c / tools/navdata.py / tools/navserver.py /
tools/navview.html / tools/控制台.pyw。本测试只读源码，不需要游戏、网络或窗口。

跑法：python tools/test_blank_pack.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)


def read(rel):
    with open(os.path.join(PROJ, rel), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def main():
    editor = read(os.path.join("src", "editor.c"))
    # 空白地图（grow）：原生点点全禁 + AddNode 新建
    assert "g_nedBlank" in editor, "editor.c 丢了 g_nedBlank"
    assert "g_nedGrow" in editor, "editor.c 丢了 g_nedGrow"
    assert "nav_apply_grow" in editor, "editor.c 丢了 grow 新建节点路径"
    assert 'nav_tok(line, "grow")' in editor, "editor.c 不再解析 grow 行"
    assert 'nav_tok(line, "blank")' in editor, "editor.c 不再兼容旧文件里的 blank 行"
    assert "nav_drop_add" in editor, "editor.c 丢了「删自己加的点」修正"
    assert "naved: blank base: disabled" not in editor, \
        "editor.c 又出现了借槽位的 blank 应用路径（2026-11-20 已删）"
    assert "R_PP_LOCK" in editor and "0x5E9660" in editor, \
        "editor.c 丢了 PathProcessor.Lock（建点必须在阻塞窗口里）"
    # keep：原版基础 + 新增，原生点一个都不动
    assert "g_nedKeep" in editor, "editor.c 丢了 g_nedKeep"
    assert 'nav_tok(line, "keep")' in editor, "editor.c 不再解析 keep 行"
    assert "if (!keep) {" in editor, "editor.c keep 模式又去禁用原生点了"
    assert "nav_add_live" in editor, "editor.c 丢了运行中加点（grow/keep 必须真·新建）"
    assert "nav_diag" in editor, "editor.c 丢了寻路诊断日志（nav_diag）"
    assert "pathID(ushort) +0x8" in editor or "pathID" in editor, \
        "editor.c 诊断不再读 PathHandler.pathID"
    assert "UCF_NAV_DIR" in editor, "editor.c 丢了 UCF_NAV_DIR（正式版 nav 可放游戏外）"
    assert "ucf_navcmd.txt" in editor and "nav_cmd_tick" in editor, \
        "editor.c 丢了控制台运行中命令（ucf_navcmd.txt / nav_cmd_tick）"

    navdata = read(os.path.join("tools", "navdata.py"))
    assert '"--grow"' in navdata, "navdata.py pack new 丢了 --grow"
    assert '"--keep"' in navdata, "navdata.py pack new 丢了 --keep"
    assert '"--blank"' not in navdata, "navdata.py 又加回了 --blank（已并入 --grow）"
    assert "is_grow" in navdata, "navdata.py promote 不再拦 grow 包"
    assert "is_keep" in navdata, "navdata.py promote 不再拦 keep 包"
    assert "def cmd_pack_seed" not in navdata, "navdata.py 又加回了 pack seed（已删）"
    assert "def seed_pack_lines" not in navdata, "navdata.py 又加回了 seed_pack_lines（已删）"

    server = read(os.path.join("tools", "navserver.py"))
    assert "/api/pack-txt" in server, "navserver.py 丢了 /api/pack-txt（只读看包）"
    assert "只读服务，不提供写入接口" in server, "navserver.py 不再拒绝网页写入"

    view = read(os.path.join("tools", "navview.html"))
    assert "function hasBlank" in view, "navview.html 丢了 hasBlank"
    assert "async function loadPack" in view, "navview.html 丢了 loadPack"
    assert '"blank"' in view and "blankBase" in view, \
        "navview.html 不再兼容旧包里的 blank 行"

    console = read(os.path.join("tools", "控制台.pyw"))
    assert "def create_pack" in console, "控制台丢了「新建测试包」"
    assert "空白地图（新建节点）" in console, "控制台新建弹窗丢了「空白地图（新建节点）」"
    assert "原版基础 + 新增" in console, "控制台新建弹窗丢了「原版基础 + 新增」"
    assert "真·新建节点（grow）" not in console, "控制台又出现了四个选项里的 grow 老标签"
    assert "复制原版路点（seed）" not in console, "控制台又加回了 seed 选项（已删）"
    assert "def seed_lines" not in console, "控制台又加回了 seed_lines（已删）"
    assert 'out["keep"]' in console and 'summ["keep"]' in console, \
        "控制台不再解析/传递 keep"
    assert "keep_native" in console, "控制台「清空当前图」不再保留 keep 模式"
    assert 'if s in ("grow", "blank")' in console, "控制台不再兼容旧包里的 blank 行"
    assert "nogen.txt" in console, "控制台不再写 nogen.txt（关自动铺点）"
    assert 'out["blank"]' not in console and 'summ["blank"]' not in console, \
        "控制台又按 blank 单独分支（已并入 grow）"
    assert "def send_pack_cmd" in console and "ucf_navcmd" in console, \
        "控制台丢了「载入到游戏 / 重新应用 / 保存路线」命令入口"

    # 测试包文件夹带序号（2026-11-20）：packs\01_TransportShip运输船\<包名>\
    assert "from map_table import folder_name as map_folder_name" in console, \
        "控制台不再用 map_table 取序号"
    assert "def folder_alias" in console, "控制台丢了「旧文件夹改名合并」（folder_alias）"
    assert "map_table.folder_name" in navdata, "navdata.py 建包不再用 map_table 的序号"
    sys.path.insert(0, HERE)
    import map_table
    got = [map_table.folder_name(lv) for _no, lv, _cn, _sc in map_table.rows()]
    want = ["01_TransportShip运输船", "02_Factory小型工厂", "03_Cebu_City椰岛之巅",
            "04_NY_TM胜利广场", "05_Arena竞技场", "06_GrimReaperKM刀锋寨",
            "07_DeathRing死亡擂台", "08_DesertFort沙漠要塞", "09_NanoResort生化酒店",
            "10_Nano30_Storm飓风危城", "11_Nano_DawnVillage新寂静村"]
    assert got == want, got
    for name in want:
        assert re.match(r"^[^\\/:*?\"<>|]{1,30}$", name), name   # 控制台的包 id 规则

    print("OK: grow/keep pack chain present in editor.c / navdata.py / navserver.py / "
          "navview.html / 控制台.pyw（blank / seed 已删）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
