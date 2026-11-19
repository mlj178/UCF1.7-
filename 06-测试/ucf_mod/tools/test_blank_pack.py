#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""静态自检：测试包「空白底图」（blank）链路有没有被改断。

空白底图 = 插件先把该图所有原生点禁用，再套包里的 node add / edge add。
链路跨 5 个文件：src/editor.c / tools/navdata.py / tools/navserver.py /
tools/navview.html / tools/控制台.pyw。本测试只读源码，不需要游戏、网络或窗口。

2026-11-18 起网页端只读：测试包只由控制台 / navdata.py 创建，网页端只读查看包。

跑法：python tools/test_blank_pack.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)


def read(rel):
    with open(os.path.join(PROJ, rel), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def main():
    editor = read(os.path.join("src", "editor.c"))
    assert "g_nedBlank" in editor, "editor.c 丢了 g_nedBlank"
    assert 'strncmp(line, "blank"' in editor, "editor.c 不再解析 blank 行"
    assert "blank base" in editor, "editor.c 不再记录/应用空白底图"
    assert "nav_drop_add" in editor, "editor.c 丢了「删自己加的点」修正"
    # grow（2026-11-19）：真·新建节点 + 正式版 nav 目录可外置
    assert "g_nedGrow" in editor, "editor.c 丢了 g_nedGrow"
    assert 'strncmp(line, "grow"' in editor, "editor.c 不再解析 grow 行"
    assert "nav_apply_grow" in editor, "editor.c 丢了 grow 新建节点路径"
    assert "R_PP_LOCK" in editor and "0x5E9660" in editor, \
        "editor.c 丢了 PathProcessor.Lock（建点必须在阻塞窗口里）"
    assert "UCF_NAV_DIR" in editor, "editor.c 丢了 UCF_NAV_DIR（正式版 nav 可放游戏外）"
    assert "ucf_navcmd.txt" in editor and "nav_cmd_tick" in editor, \
        "editor.c 丢了控制台运行中命令（ucf_navcmd.txt / nav_cmd_tick）"

    navdata = read(os.path.join("tools", "navdata.py"))
    assert '"--blank"' in navdata, "navdata.py pack new 丢了 --blank"
    assert '"--grow"' in navdata, "navdata.py pack new 丢了 --grow"
    assert "is_blank" in navdata, "navdata.py promote 不再拦空白包"
    assert "is_grow" in navdata, "navdata.py promote 不再拦 grow 包"
    assert "def cmd_pack_seed" in navdata and "def seed_pack_lines" in navdata, \
        "navdata.py 丢了 pack seed（从原版点图播种）"

    server = read(os.path.join("tools", "navserver.py"))
    assert "/api/pack-txt" in server, "navserver.py 丢了 /api/pack-txt（只读看包）"
    assert "只读服务，不提供写入接口" in server, "navserver.py 不再拒绝网页写入"

    view = read(os.path.join("tools", "navview.html"))
    assert "function hasBlank" in view, "navview.html 丢了 hasBlank"
    assert "async function loadPack" in view, "navview.html 丢了 loadPack"
    assert '"blank"' in view and "blankBase" in view, "navview.html 不再写 blank"

    console = read(os.path.join("tools", "控制台.pyw"))
    assert "def create_blank_pack" in console, "控制台丢了「新建测试包」"
    assert "真·新建节点（grow）" in console, "控制台新建弹窗丢了 grow 选项"
    assert "keep_grow" in console, "控制台「清空当前图」不再保留 grow 模式"
    assert "def seed_lines" in console, "控制台丢了「复制原版路点（seed）」"
    assert "复制原版路点（seed）" in console, "控制台新建弹窗丢了 seed 选项"
    assert "blank" in console and "nogen.txt" in console, "控制台不再写 blank / nogen"
    assert "def send_pack_cmd" in console and "ucf_navcmd" in console, \
        "控制台丢了「载入到游戏 / 重新应用 / 保存路线」命令入口"

    print("OK: blank pack chain present in editor.c / navdata.py / navserver.py / "
          "navview.html / 控制台.pyw（含 ucf_navcmd 运行中命令）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
