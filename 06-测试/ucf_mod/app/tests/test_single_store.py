#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""静态自检：单草稿 / 单成品（2026-11-24）。

一条图一条线：packs\<地图文件夹>\ 一个草稿，final\<指纹>.txt 一份成品；
控制台不再有“测试包 / 成品版本”两个下拉；启动成品用 UCF_PACK_DIR=dev + UCF_PACK=final。
只读源码和数据目录名，不需要游戏/窗口。

跑法：python app/tests/test_single_store.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
ROOT = APP
while not os.path.isfile(os.path.join(ROOT, ".ucfroot")) and os.path.dirname(ROOT) != ROOT:
    ROOT = os.path.dirname(ROOT)


def read(*parts):
    with open(os.path.join(ROOT, *parts), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def main():
    nav = read("app", "core", "navdata.py")
    packs = read("app", "ui", "packs.py")
    way = read("app", "tabs", "waypoint.py")
    console = read("app", "控制台.pyw")

    assert "def final_store_publish" in nav, "navdata.py 缺 final_store_publish"
    assert "FINAL_PREV" in nav and "final_prev" in nav, "navdata.py 缺发布前快照"
    assert "final_new_version(base=cur" not in nav, "navdata.py 还在建多版本"
    assert "def final_store_files" in nav and "ucf-final-single" in nav, "navdata.py 缺单份成品台账"
    assert "def cmd_pack_new" in nav and "packs_root(), folder" in nav, "pack new 不再是一图一草稿"
    assert "def prepare_final_root" in packs, "packs.py 缺 prepare_final_root"
    assert "opt_pack" not in way and "opt_final" not in way, "waypoint.py 还有包/版本下拉"
    assert "一张图一个" in way or "一张图只有一个" in way, "waypoint.py 没写单草稿"
    assert 'env["UCF_PACK"] = "final"' in console, "成品启动没改成 UCF_PACK=final"
    assert 'env["UCF_PACK_DIR"] = DEV' in console, "成品启动没改成 UCF_PACK_DIR=dev"
    assert "prepare_final_root()" in console, "控制台还在用 prepare_final_dir(版本)"

    dev = os.path.join(ROOT, "data", "navdata", "dev")
    pack_root = os.path.join(dev, "packs")
    if os.path.isdir(pack_root):
        for name in os.listdir(pack_root):
            d = os.path.join(pack_root, name)
            if not os.path.isdir(d) or name.startswith("_"):
                continue
            subs = [x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))]
            assert not subs, "packs\\%s 里还有第二层包目录：%s" % (name, subs)
    final = os.path.join(dev, "final")
    if os.path.isdir(final):
        for name in os.listdir(final):
            assert not os.path.isdir(os.path.join(final, name)),                 "final\\ 里还有版本目录：%s" % name
        assert not os.path.isfile(os.path.join(final, "_current.txt")),             "final\\ 里还有 _current.txt"

    print("OK: 单草稿 / 单成品（packs\\<图> / final\\<指纹>.txt，无版本下拉）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
