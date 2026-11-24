#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""整理 ② 开发版的导出收件箱 vis/：认得出的图，直接归进 <图>\导出\ 和 <图>\navmesh.bin

用途：插件 Ctrl+E 把文件平铺写在导出根（② 开发版 vis\，或旧的 ③ 部署版 vis\）；
跑一次本脚本就归位。认不出关卡的（指纹不在台账里）留在 vis\raw\ 不动，没删。
可反复跑（已归位的文件不会再动）。--dry 只看会做什么。

映射依据：② 00_公共\_index.json 的 指纹 -> level/中文名（老布局 maps\_index.json 也认）。
游戏里读到的地图名（h_ / x_ / dS_）不可靠，这里不用它当目录名。
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
for _p in (os.path.join(UCF_ROOT, "app", "core"), HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import ucf_paths as P
from ucf_paths import DATA, EXPORT as VIS

STATE = os.path.join(VIS, "_state")          # 插件「同一指纹只导一次」的标记
RAW = os.path.join(VIS, "raw")               # 认不出关卡的导出留在这
SKIP_DIRS = {"navmesh", "_state", "_noise", "backup"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_index():
    r"""指纹 -> (level, 中文名)：读 00_公共\_index.json（老布局 maps\_index.json）。"""
    out = {}
    path = P.index_path(DATA)
    if os.path.isfile(path):
        try:
            with open(path, encoding="utf-8") as f:
                for m in (json.load(f).get("maps") or []):
                    fp = (m.get("fingerprint") or "").strip()
                    if fp:
                        out[fp] = (m.get("level") or "", m.get("name") or "")
        except (OSError, ValueError):
            pass
    return out


def bin_level(fn):
    r"""navmesh_nm840-xxxx.bin -> level2（按原生 A* 顶点数对号，见《地图对照表》）。"""
    m = re.search(r"nm(\d+)-", fn)
    if not m:
        return ""
    verts = {v: k for k, v in P.NATIVE_VERTS.items()}
    return verts.get(int(m.group(1)), "")


def unique(path):
    base, ext = os.path.splitext(path)
    n = 1
    dst = path
    while os.path.exists(dst):
        dst = "%s_%d%s" % (base, n, ext)
        n += 1
    return dst


def main():
    ap = argparse.ArgumentParser(description="整理 vis 收件箱：认得出的图归进自己的文件夹")
    ap.add_argument("--dry", action="store_true", help="只打印，不动文件")
    args = ap.parse_args()
    idx = load_index()
    if not args.dry:
        os.makedirs(STATE, exist_ok=True)
        os.makedirs(RAW, exist_ok=True)

    moved_json = moved_bin = dropped = 0
    left = []

    # 1) 导出 JSON：指纹在台账里 -> <图>\导出\<时间>_<指纹>.json
    for base, dirs, files in os.walk(VIS):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in sorted(files):
            if not fn.lower().endswith(".json") or fn in ("names.json", "_index.json"):
                continue
            p = os.path.join(base, fn)
            try:
                with open(p, encoding="utf-8") as f:
                    doc = json.load(f)
            except (OSError, ValueError) as exc:
                print("跳过（读不了）", os.path.relpath(p, VIS), exc)
                continue
            mp = doc.get("map") or {}
            fp = (mp.get("fingerprint") or "").strip()
            gen = doc.get("generated") or ""
            try:
                ts = time.strftime("%Y%m%d-%H%M%S", time.strptime(gen, "%Y-%m-%d %H:%M:%S"))
            except ValueError:
                ts = time.strftime("%Y%m%d-%H%M%S", time.localtime(os.path.getmtime(p)))
            hit = idx.get(fp)
            if not hit:
                left.append((os.path.relpath(p, VIS), fp or "无指纹"))
                continue
            level, _cn = hit
            want_dir = os.path.join(P.map_dir(DATA, level), "导出")
            dst = os.path.join(want_dir, "%s_%s.json" % (ts, fp))
            if os.path.abspath(p) == os.path.abspath(dst):
                continue
            if os.path.exists(dst):
                dst = unique(dst)
            print("%-52s -> %s" % (os.path.relpath(p, VIS), os.path.relpath(dst, DATA)))
            if args.dry:
                continue
            os.makedirs(want_dir, exist_ok=True)
            os.replace(p, dst)
            moved_json += 1
            # 同名伴随可走面一起走
            comp = os.path.splitext(p)[0] + ".navmesh.bin"
            if os.path.isfile(comp):
                os.replace(comp, os.path.splitext(dst)[0] + ".navmesh.bin")
                print("    可走面副本随文件移动")

    # 2) navmesh_<顶点数>-<指纹>.bin -> <图>\navmesh.bin（已有一份就只留一份）
    roots = [VIS, os.path.join(VIS, "navmesh")]
    for root in roots:
        if not os.path.isdir(root):
            continue
        for fn in sorted(os.listdir(root)):
            if not (fn.startswith("navmesh_") and fn.lower().endswith(".bin")):
                continue
            src = os.path.join(root, fn)
            if not os.path.isfile(src):
                continue
            level = bin_level(fn)
            if not level:
                print("跳过（认不出是哪张图）%s" % os.path.relpath(src, VIS))
                continue
            want_dir = P.map_dir(DATA, level)
            dst = os.path.join(want_dir, P.NAVMESH)
            if os.path.abspath(src) == os.path.abspath(dst):
                continue
            if os.path.exists(dst):
                if sha(src) == sha(dst):
                    print("%-52s 与 %s 相同，删掉重复" % (os.path.relpath(src, VIS), os.path.relpath(dst, DATA)))
                    if not args.dry:
                        os.remove(src)
                        dropped += 1
                    continue
                dst = unique(dst)          # 内容不同：留成 navmesh_<指纹>.bin，不覆盖
            print("%-52s -> %s" % (os.path.relpath(src, VIS), os.path.relpath(dst, DATA)))
            if args.dry:
                continue
            os.makedirs(want_dir, exist_ok=True)
            os.replace(src, dst)
            moved_bin += 1

    # 3) _seen_* -> _state/（插件内部标记，不用看）
    if not args.dry:
        for base, dirs, files in os.walk(VIS):
            dirs[:] = [d for d in dirs if d not in ("_state", "_noise")]
            for fn in files:
                if fn.startswith("_seen_"):
                    src = os.path.join(base, fn)
                    dst = os.path.join(STATE, fn)
                    if os.path.exists(dst):
                        os.remove(src)
                        continue
                    os.replace(src, dst)
                    print("%-52s -> _state/" % os.path.relpath(src, VIS))

    # 3.5) 清掉搬空的 raw\/<地图>/ 目录（只删空目录，认不出的照旧留着）
    if not args.dry and os.path.isdir(RAW):
        for base, dirs, files in os.walk(RAW, topdown=False):
            if os.path.abspath(base) == os.path.abspath(RAW):
                continue
            if not os.listdir(base):
                try:
                    os.rmdir(base)
                except OSError:
                    pass

    # 4) README 重新生成（列每张图收了几份导出）
    rows = []
    for lv in sorted(P.NATIVE_VERTS) + ["level1", "level8", "level9"]:
        exp = os.path.join(P.map_dir(DATA, lv), "导出")
        if not os.path.isdir(exp):
            continue
        fns = [x for x in os.listdir(exp) if x.endswith(".json")]
        if fns:
            rows.append((P.map_folder(lv), len(fns), max(fns)))
    lines = [
        "② 开发版 vis/ —— 插件的导出收件箱（临时的，整理后就空）",
        "",
        "游戏里按 Ctrl+E 导出、进图自动落可走面，都会先写在这里（平铺）。",
        "跑一次 tools/data/tidy_vis.py 就归位：",
        "    认得出的图 -> ②\\<图>\\导出\\<时间>_<指纹>.json",
        "                   ②\\<图>\\navmesh.bin（可走面，同一张图只留一份）",
        "    认不出的   -> 留在 vis\\raw\\，不删、等你确认",
        "_state/   插件内部去重标记 _seen_*（不用看）",
        "",
        "认图的依据是 ②\\00_公共\\_index.json 里的指纹 -> 关卡对照。",
        "",
        "当前每张图收了几份导出：",
    ]
    for folder, n, latest in rows:
        lines.append("  %-30s %d 份    最近 %s" % (folder, n, latest))
    if not rows:
        lines.append("  （还没有）")
    if not args.dry:
        with open(os.path.join(VIS, "README.txt"), "w", encoding="utf-8", newline="\r\n") as f:
            f.write("\n".join(lines) + "\n")
    for rel, fp in left[:10]:
        print("留在收件箱（认不出关卡）：%s  fp=%s" % (rel, fp))
    print("完成：导出归位 %d 个，可走面归位 %d 个，删重复 %d 个" % (moved_json, moved_bin, dropped))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
