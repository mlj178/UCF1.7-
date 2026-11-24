#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：① 备份 / ② 开发 是不是「一张图一个文件夹」（2026-11-21 的布局）。

跑法：python tests/test_mapfolders.py

查 7 件事：
  1) 两个数据根都是新布局，10 个图文件夹都在（对照表 11 张里，有数据的 9 张 + 只有可走面的 2 张）
  2) 每张图的 map.json 在自己文件夹里；可走面叫 navmesh.bin，也在同一个文件夹
  3) 公共文件只在 00_公共\；旧的 maps\ nav\ vis\ 不再存数据
  4) 收件箱 vis\ 只留认不出关卡的导出（不删）
  5) ucf_paths / 控制台 / 网页编辑器 / navdata 四个读法算出来的数一致：9 图 / 8 面
  6) 迁移日志还在（--undo 能退回去）
  7) packs\ final\ archive\ 没被碰过
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
for _p in (os.path.join(UCF_ROOT, "core"), os.path.join(UCF_ROOT, "console"), HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import ucf_paths as P                    # noqa: E402
import map_table                          # noqa: E402

FAIL = []


def check(cond, msg):
    if cond:
        print("  OK   " + msg)
    else:
        print("  !!   " + msg)
        FAIL.append(msg)


def main():
    print("== 1) 两个数据根都是新布局")
    for name, root in (("① 备份", P.NATIVE), ("② 开发", P.DEV)):
        check(os.path.isdir(os.path.join(root, P.COMMON)), "%s 有 00_公共\\" % name)
        check(P.is_folders(root), "%s 认得出「一张图一个文件夹」" % name)

    print("== 2) 图文件夹 / map.json / navmesh.bin")
    for name, root in (("① 备份", P.NATIVE), ("② 开发", P.DEV)):
        docs = P.map_docs(root)
        check(len(docs) == 9, "%s 有 9 张图的 map.json（实际 %d）" % (name, len(docs)))
        for level, _cn, path in docs:
            folder = os.path.dirname(path)
            want = P.map_dir(root, level)
            check(os.path.normcase(os.path.abspath(folder)) == os.path.normcase(os.path.abspath(want)),
                  "%s %s -> %s" % (name, level, os.path.basename(folder)))
        check(len(P.navmesh_files(root)) == 8, "%s 有 8 个 navmesh.bin（实际 %d）"
              % (name, len(P.navmesh_files(root))))
        for rel, path in P.navmesh_files(root):
            check(os.path.basename(path) == P.NAVMESH, "%s %s 叫 navmesh.bin" % (name, rel))

    print("== 3) 旧目录不再存数据")
    for name, root in (("① 备份", P.NATIVE), ("② 开发", P.DEV)):
        for legacy, tip in ((os.path.join(root, "maps"), "maps"), (os.path.join(root, "nav"), "nav")):
            left = os.listdir(legacy) if os.path.isdir(legacy) else []
            check(not left, "%s 的 %s\\ 里没有数据了（%s）" % (name, tip, "、".join(left) or "空"))
        check(os.path.isfile(P.names_path(root)), "%s names.json 在 00_公共\\" % name)
    check(os.path.isfile(P.index_path(P.DEV)), "② _index.json 在 00_公共\\")
    check(os.path.isfile(os.path.join(P.common_dir(P.DEV), "INDEX.md")), "② INDEX.md 在 00_公共\\")

    print("== 4) 收件箱只剩认不出的导出")
    idx = {}
    try:
        with open(P.index_path(P.DEV), encoding="utf-8") as f:
            for row in (json.load(f).get("maps") or []):
                fp = (row.get("fingerprint") or "").strip()
                if fp:
                    idx[fp] = row.get("level")
    except (OSError, ValueError):
        pass
    inbox = []
    raw = os.path.join(P.VIS, "raw")
    for base, _dirs, files in os.walk(raw):
        for fn in files:
            if not fn.endswith(".json"):
                continue
            try:
                with open(os.path.join(base, fn), encoding="utf-8") as f:
                    fp = ((json.load(f).get("map") or {}).get("fingerprint") or "").strip()
            except (OSError, ValueError):
                continue
            if fp in idx:
                inbox.append(os.path.join(base, fn))
    check(not inbox, "收件箱里没有「认得出却没归位」的导出（%d 个）" % len(inbox))

    print("== 5) 四个读法数字一致")
    n_maps = len(P.map_files(P.DEV))
    n_bins = len(P.navmesh_files(P.DEV))

    spec = importlib.util.spec_from_file_location("ucf_console_test", os.path.join(P.PROJ, "console", "控制台.pyw"))
    con = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(con)
    con_counts = con.data_counts(con.DEV)
    check(con_counts[0] == n_maps and con_counts[3] == n_bins,
          "控制台 data_counts=(%d 图, %d 面)" % (con_counts[0], con_counts[3]))
    check(len(con.load_maps()) == 9, "控制台 load_maps 9 张能测的图")

    import navserver as S
    rows = S.collect_maps()
    check(len(rows) == 11, "网页编辑器 11 行（对照表补全 04/07）")
    check(len([r for r in rows if r.get("file")]) == 9, "网页编辑器 9 行有文件")
    dev_ver = S._dir_version(S.DEV)
    check(dev_ver["maps"] == n_maps and dev_ver["navmesh"] == n_bins,
          "网页编辑器版本统计 (%d 图, %d 面)" % (dev_ver["maps"], dev_ver["navmesh"]))

    import navdata as N
    s = N.summary(P.DEV)
    check(s["sub"].get("图") == n_maps and s["sub"].get("可走面") == n_bins,
          "navdata.py summary (%s)" % s["sub"])

    print("== 6) 迁移日志在")
    logs = [f for f in os.listdir(os.path.join(P.DATA_ROOT, "navdata"))
            if f.startswith("_migrate_mapfolders_") and f.endswith(".json")]
    check(bool(logs), "有迁移日志 %d 个（可 --undo）" % len(logs))

    print("== 7) packs / final / archive 没被碰过")
    check(os.path.isdir(P.PACKS_DIR), "packs\\ 还在")
    # 迁移时 packs 里是 3 个包；2026-11-21 起还会边玩边建新包（TransportShip_20261121_140112），
    # 所以这里只要求「迁移没把包删掉」，不再钉死 3。
    check(len(N.pack_ids()) >= 3, "packs 里至少有迁移时的 3 个包（实际 %d）" % len(N.pack_ids()))
    check(os.path.isdir(os.path.join(P.DEV, "final")), "final\\ 还在")
    check(os.path.isdir(os.path.join(P.DEV, "archive")), "archive\\ 还在")

    print("")
    if FAIL:
        print("!! %d 项没过" % len(FAIL))
        return 1
    print("OK: 布局自检通过（9 图 / 8 面 / 00_公共 / 收件箱干净）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
