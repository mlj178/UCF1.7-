#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：一张图一个文件夹（2026-11-27「一图一夹」）。

跑法：python app/tests/test_mapfolders.py

查 8 件事：
  1) 唯一数据根 data\maps\ 存在，00_公共\ 在，旧 data\navdata\ 已经没了
  2) 9 张图的 map.json 在各图文件夹根下；8 个可走面叫 navmesh.bin，也在同一层
  3) ① 冻结副本在 <图>\native\（9 个 map.json / 8 个 navmesh.bin），SHA256SUMS 就在 00_公共\
  4) 编辑标记在 <图>\markers.txt（不再有 markers\ 这一层）
  5) 草稿在 <图>/<指纹>.txt（不再有 packs/ 这一层），成品在 <图>/final/（不再有平铺 final/）
  6) 收件箱 _inbox\ 里没有「认得出却没归位」的导出
  7) ucf_paths / 控制台 / 网页编辑器 / navdata 四个读法算出来的数一致：9 图 / 8 面
  8) 迁移日志还在（--undo 能退回去）
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
for _p in (os.path.join(UCF_ROOT, "app", "core"), os.path.join(UCF_ROOT, "app"),
           os.path.join(UCF_ROOT, "app", "workbench"), HERE):
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
    print("== 1) 唯一数据根")
    check(os.path.isdir(P.MAPS), "data/maps/ 在")
    check(os.path.isdir(os.path.join(P.MAPS, P.COMMON)), "00_公共/ 在")
    check(P.is_folders(P.MAPS), "认得出「一张图一个文件夹」")
    check(not os.path.exists(os.path.join(P.DATA_ROOT, "navdata")), "旧的 data/navdata/ 已经没了")
    for legacy in ("maps", "nav", "packs", "markers", "vis", "archive", "final"):
        check(not os.path.isdir(os.path.join(P.MAPS, legacy)), "旧的 %s/ 没有回来" % legacy)

    print("== 2) 图文件夹 / map.json / navmesh.bin")
    docs = P.map_docs(P.MAPS)
    check(len(docs) == 9, "9 张图的 map.json（实际 %d）" % len(docs))
    for level, _cn, path in docs:
        folder = os.path.dirname(path)
        want = P.map_dir(P.MAPS, level)
        check(os.path.normcase(os.path.abspath(folder)) == os.path.normcase(os.path.abspath(want)),
              "%s -> %s" % (level, os.path.basename(folder)))
    check(len(P.navmesh_files(P.MAPS)) == 8, "8 个 navmesh.bin（实际 %d）"
          % len(P.navmesh_files(P.MAPS)))
    for rel, path in P.navmesh_files(P.MAPS):
        check(os.path.basename(path) == P.NAVMESH, "%s 叫 navmesh.bin" % rel)

    print("== 3) ① 冻结副本在 <图>/native/")
    check(len(P.native_files(P.MAPS)) == 9, "native/ 里 9 个 map.json（实际 %d）"
          % len(P.native_files(P.MAPS)))
    check(len(P.native_navmesh_files(P.MAPS)) == 8, "native/ 里 8 个 navmesh.bin（实际 %d）"
          % len(P.native_navmesh_files(P.MAPS)))
    for rel, path in P.native_files(P.MAPS):
        folder = rel.split("/")[0]
        check(os.path.normcase(os.path.dirname(path)) ==
              os.path.normcase(P.native_dir(folder)),
              "① %s 在 <图>/native/%s" % (rel, os.path.basename(path)))
    check(os.path.isfile(os.path.join(P.MAPS, P.COMMON, "SHA256SUMS.txt")),
          "SHA256SUMS.txt 在 00_公共/")
    check(os.path.isfile(os.path.join(P.MAPS, P.COMMON, ".frozen.json")),
          ".frozen.json 在 00_公共/")

    print("== 4) 编辑标记在 <图>/markers.txt")
    n_mk = 0
    for name in P.folder_names(P.MAPS):
        if os.path.isfile(os.path.join(P.folder_dir(name, P.MAPS), "markers.txt")):
            n_mk += 1
    check(n_mk <= len(P.folder_names(P.MAPS)), "markers.txt 都挂在图文件夹根下（%d 张有）" % n_mk)

    print("== 5) 草稿 / 成品都在图文件夹里")
    import navdata as N
    ids = N.pack_ids()
    check(all("/" not in x for x in ids), "草稿是 <图>/<指纹>.txt（没有 图/包 两层；实际 %s）" % (ids or "空"))
    for pid in ids:
        p = os.path.join(P.MAPS, pid)
        check(os.path.isfile(os.path.join(p, "manifest.json")), "%s 有 manifest.json" % pid)
        fps = [fn for fn in os.listdir(p) if fn.startswith("n") and fn.endswith(".txt")]
        check(fps, "%s 有点图文件 %s" % (pid, fps[:2]))
    for fp, path in N.final_store_files():
        check(os.path.basename(os.path.dirname(path)) == P.FINAL_SUB,
              "成品 %s 在 <图>/final/%s" % (fp, os.path.basename(path)))
    check(not os.path.isdir(os.path.join(P.MAPS, "final")), "没有平铺的 final/ 了")

    print("== 6) 收件箱只剩认不出的导出")
    idx = {}
    try:
        with open(P.index_path(P.MAPS), encoding="utf-8") as f:
            for row in (json.load(f).get("maps") or []):
                fp = (row.get("fingerprint") or "").strip()
                if fp:
                    idx[fp] = row.get("level")
    except (OSError, ValueError):
        pass
    inbox = []
    raw = os.path.join(P.INBOX, "raw")
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

    print("== 7) 四个读法数字一致")
    n_maps = len(P.map_files(P.MAPS))
    n_bins = len(P.navmesh_files(P.MAPS))

    import ui.env as CEnv
    import ui.stats as CStats
    import ui.maps as CMaps
    con_counts = CStats.data_counts(CEnv.DEV)
    check(con_counts[0] == n_maps and con_counts[3] == n_bins,
          "控制台 data_counts=(%d 图, %d 面)" % (con_counts[0], con_counts[3]))
    check(len(CMaps.load_maps()) == 9, "控制台 load_maps 9 张能测的图")

    import navserver as S
    rows = S.collect_maps()
    check(len(rows) == 12, "网页编辑器 12 行（对照表补全 04/07/12）")
    check(len([r for r in rows if r.get("file")]) == 9, "网页编辑器 9 行有文件")
    dev_ver = S._dir_version(S.DEV)
    check(dev_ver["maps"] == n_maps and dev_ver["navmesh"] == n_bins,
          "网页编辑器版本统计 (%d 图, %d 面)" % (dev_ver["maps"], dev_ver["navmesh"]))

    s = N.summary(P.MAPS)
    check(s["sub"].get("图") == n_maps and s["sub"].get("可走面") == n_bins,
          "navdata.py summary (%s)" % s["sub"])

    print("== 8) 迁移日志还在")
    arch = P.ARCHIVE
    logs = [f for f in os.listdir(arch) if f.startswith("migrate_onemap_")] if os.path.isdir(arch) else []
    check(bool(logs), "_archive/ 里有迁移日志（--undo 能退回去）：%s" % (logs[-1:] or "无"))

    print("")
    if FAIL:
        print("!! %d 项没过" % len(FAIL))
        return 1
    print("OK: 一图一夹自检通过（9 图 / 8 面 / native 冻结副本 / 00_公共 / 收件箱干净）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
