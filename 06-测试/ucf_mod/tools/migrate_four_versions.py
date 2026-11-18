#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""一次性迁移：把 ③ 部署版里的"实验数据"搬进 ④ 测试版（2026-11-18）。

四版分开之后，③ 部署版只留游戏要读的东西（ucf_mod.dll / ucf_mod.json /
nav\<指纹>.txt / markers / packs 由 ④ 提供）；导出、测试包、错放的文件都归 ④。

搬什么（都从 ③ 游戏目录 -> 工程端 navdata\test）：
    vis\raw\  vis\navmesh\  vis\_state\  vis\*.navmesh.bin  vis\_seen_*  -> ④\vis\
    packs\<包名>\                                                        -> ④\packs\
    ② nav\map_*.json（放错目录的导出快照，游戏不读）                       -> ④\vis\raw\_待整理\
    ② nav\*.txt 里只有表头、0 条改动的                                   -> ④\archive\empty_edits\

不搬：
    ③\vis\README.txt        保留，说明这里已经不用
    ③\backup\               回滚区（DLL 备份 + 历史导出），工具只读兼容
    ③\maps\  ③\nav\          部署数据，只由「部署到游戏」从 ② 推

搬之前先把 ③\vis 整份复制到 ④\archive\pre_migrate_<时间>\（约 1 MB，能回退）。

用法（在 tools\ 下）：
    python migrate_four_versions.py --dry     # 只看会搬什么
    python migrate_four_versions.py           # 真搬
"""
import argparse
import io
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import ucf_paths as P  # noqa: E402

SKIP_VIS = {"README.txt"}


def log(*a):
    print(*a)
    sys.stdout.flush()


def unique(path):
    base, ext = os.path.splitext(path)
    n = 1
    dst = path
    while os.path.exists(dst):
        dst = "%s_%d%s" % (base, n, ext)
        n += 1
    return dst


def merge_move(src, dst, dry=False):
    """把 src 文件/目录搬到 dst；目录按相对路径合并，重名改成 xxx_1。"""
    if not os.path.exists(src):
        return 0
    moved = 0
    if os.path.isdir(src):
        for item in sorted(os.listdir(src)):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                moved += merge_move(s, d, dry)
                continue
            if os.path.exists(d):
                d = unique(d)
            log("    %s -> %s" % (os.path.relpath(s, P.PROJ), os.path.relpath(d, P.PROJ)))
            if not dry:
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.move(s, d)
            moved += 1
        if not dry:
            try:
                os.rmdir(src)
            except OSError:
                pass
        return moved
    if os.path.exists(dst):
        dst = unique(dst)
    log("    %s -> %s" % (os.path.relpath(src, P.PROJ), os.path.relpath(dst, P.PROJ)))
    if not dry:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
    return 1


def edit_count(path):
    """非注释、非空行 = 实际改动条数。"""
    n = 0
    try:
        with io.open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                s = line.strip()
                if s and not s.startswith("#"):
                    n += 1
    except OSError:
        return 0
    return n


def main():
    ap = argparse.ArgumentParser(description="③ 部署版里的实验数据搬到 ④ 测试版")
    ap.add_argument("--dry", action="store_true", help="只打印，不动文件")
    args = ap.parse_args()
    dry = args.dry
    stamp = time.strftime("%Y%m%d_%H%M%S")
    total = 0

    log("=" * 78)
    log("迁移：%s" % ("只预览" if dry else "真搬"))
    log("  ③ 部署版：%s" % P.DEPLOY)
    log("  ④ 测试版：%s" % P.TEST)
    log("=" * 78)

    # 0) 先留一份 ③\vis 快照，出问题能整份放回去
    src_vis = P.GAME_VIS
    if os.path.isdir(src_vis) and not dry:
        bak = os.path.join(P.ARCHIVE, "pre_migrate_" + stamp)
        shutil.copytree(src_vis, bak)
        log("回退快照：%s" % bak)

    # 1) ③\vis -> ④\vis
    log("")
    log("[1] ③\\vis -> ④\\vis")
    if os.path.isdir(src_vis):
        for item in sorted(os.listdir(src_vis)):
            p = os.path.join(src_vis, item)
            if item in SKIP_VIS:
                continue
            total += merge_move(p, os.path.join(P.VIS, item), dry)
    else:
        log("    （没有 %s）" % src_vis)

    # 2) ③\packs -> ④\packs
    log("")
    log("[2] ③\\packs -> ④\\packs")
    deploy_packs = os.path.join(P.DEPLOY, "packs")
    if os.path.isdir(deploy_packs):
        for item in sorted(os.listdir(deploy_packs)):
            total += merge_move(os.path.join(deploy_packs, item),
                                os.path.join(P.PACKS_DIR, item), dry)
    else:
        log("    （没有 %s）" % deploy_packs)

    # 3) ②\nav 里放错的导出快照（游戏不读，nav\ 只该有 <指纹>.txt 和 names.json）
    log("")
    log("[3] ②\\nav 里放错的导出快照 -> ④\\vis\\raw\\_待整理")
    devnav = os.path.join(P.DEV, "nav")
    if os.path.isdir(devnav):
        for fn in sorted(os.listdir(devnav)):
            if not (fn.startswith("map_") and fn.endswith(".json")):
                continue
            total += merge_move(os.path.join(devnav, fn),
                                os.path.join(P.VIS, "raw", "_待整理", fn), dry)

    # 4) ②\nav 里 0 条改动的空清单（只有表头）
    log("")
    log("[4] ②\\nav 里 0 条改动的空清单 -> ④\\archive\\empty_edits")
    if os.path.isdir(devnav):
        for fn in sorted(os.listdir(devnav)):
            if not fn.endswith(".txt"):
                continue
            p = os.path.join(devnav, fn)
            if not os.path.isfile(p):
                continue
            if edit_count(p) == 0:
                total += merge_move(p, os.path.join(P.ARCHIVE, "empty_edits", fn), dry)

    # 5) ③\vis 留个说明，别让人以为导出没了
    readme = os.path.join(src_vis, "README.txt")
    if not dry:
        os.makedirs(src_vis, exist_ok=True)
        with io.open(readme, "w", encoding="utf-8", newline="\r\n") as f:
            f.write("③ 部署版 vis\\ 已经不再使用（2026-11-18 四版分离）。\r\n\r\n")
            f.write("插件 Ctrl+E 导出 / navmesh / _seen_ 现在写 ④ 测试版：\r\n")
            f.write("    " + P.VIS + "\r\n\r\n")
            f.write("整理：python tools\\tidy_vis.py\r\n")
            f.write("导入开发版：控制台「数据」页 →「导入到开发版 ④→②」\r\n")
    log("")
    log("=" * 78)
    log("完成：%s %d 个文件" % ("会搬" if dry else "搬了", total))
    if not dry:
        log("下一步：")
        log("  1) python tools\\tidy_vis.py        （把 ④ 里的 JSON 按地图归类）")
        log("  2) 控制台「数据」页确认 ④ 的数字，需要时点「导入到开发版 ④→②」")
        log("  3) ②/③ 不一致时，手动点「部署到游戏 ②→③」")
    return 0


if __name__ == "__main__":
    sys.exit(main())
