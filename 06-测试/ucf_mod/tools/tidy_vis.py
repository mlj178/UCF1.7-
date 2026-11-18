#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""整理 ④ 测试版 vis/：raw/<级别_中文名>/ + navmesh/ + _state/

用途：插件 Ctrl+E 把文件平铺写在导出根（④ 测试版 vis\，或旧的 ③ 部署版 vis\）；
跑一次本脚本就归位。2026-11-18 起默认目标是 navdata\test\vis。
可反复跑（已归位的文件不会再动）。--dry 只看会做什么。

映射依据：navdata\dev\maps\_index.json 的 指纹 -> level/中文名。
游戏里读到的地图名（h_ / x_ / dS_）不可靠，这里不用它当目录名。
"""
import argparse
import hashlib
import json
import os
import time

from ucf_paths import EXPORT as VIS, DEV

RAW = os.path.join(VIS, "raw")
NAVBIN = os.path.join(VIS, "navmesh")
STATE = os.path.join(VIS, "_state")
INDEX = os.path.join(DEV, "maps", "_index.json")
SKIP_DIRS = {"navmesh", "_state", "_noise", "backup"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_index():
    out = {}
    if os.path.isfile(INDEX):
        with open(INDEX, encoding="utf-8") as f:
            for m in (json.load(f).get("maps") or []):
                fp = (m.get("fingerprint") or "").strip()
                if fp:
                    out[fp] = (m.get("level") or "", m.get("name") or "")
    return out


def classify(doc, idx):
    """返回 (相对目录, 后缀说明)。"""
    mp = doc.get("map") or {}
    fp = (mp.get("fingerprint") or "").strip()
    src = (mp.get("source") or "").strip()
    if fp in idx:
        return "%s_%s" % idx[fp], ""
    if src == "ours":
        return "_非原生_插件铺点", "__插件铺点"
    if fp.lower().startswith("n786-c652"):
        return "_未识别_n786_疑似运输船", "__可疑0边"
    return "_未识别_%s" % (fp or "无指纹"), ""


def unique(path):
    base, ext = os.path.splitext(path)
    n = 1
    dst = path
    while os.path.exists(dst):
        dst = "%s_%d%s" % (base, n, ext)
        n += 1
    return dst


def main():
    ap = argparse.ArgumentParser(description="整理 vis 目录结构")
    ap.add_argument("--dry", action="store_true", help="只打印，不动文件")
    args = ap.parse_args()
    idx = load_index()
    if not args.dry:
        for d in (RAW, NAVBIN, STATE):
            os.makedirs(d, exist_ok=True)

    # 现有可走面（用于判断伴随副本是不是重复）
    bins = {}
    for base, dirs, files in os.walk(VIS):
        dirs[:] = [d for d in dirs if d not in ("_state", "_noise")]
        for fn in files:
            if fn.startswith("navmesh_") and fn.endswith(".bin"):
                p = os.path.join(base, fn)
                try:
                    bins.setdefault(sha(p), p)
                except OSError:
                    pass

    moved = 0
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
            nodes = mp.get("node_count", 0)
            src = (mp.get("source") or "").strip()
            gen = doc.get("generated") or ""
            try:
                ts = time.strftime("%Y%m%d-%H%M%S", time.strptime(gen, "%Y-%m-%d %H:%M:%S"))
            except ValueError:
                ts = time.strftime("%Y%m%d-%H%M%S", time.localtime(os.path.getmtime(p)))
            folder, suffix = classify(doc, idx)
            want_dir = os.path.join(RAW, folder)
            want = "%s_%s%s.json" % (ts, fp or "nofp", suffix)
            dst = os.path.join(want_dir, want)
            if os.path.abspath(p) == os.path.abspath(dst):
                continue
            if os.path.exists(dst) and os.path.abspath(p) != os.path.abspath(dst):
                dst = unique(dst)
            print("%-52s -> %s" % (os.path.relpath(p, VIS), os.path.relpath(dst, VIS)))
            if args.dry:
                continue
            os.makedirs(want_dir, exist_ok=True)
            os.replace(p, dst)
            moved += 1
            # 同名伴随可走面
            comp = os.path.splitext(p)[0] + ".navmesh.bin"
            if os.path.isfile(comp):
                h = sha(comp)
                if h in bins and os.path.abspath(bins[h]) != os.path.abspath(comp):
                    os.remove(comp)
                    print("    删重复可走面副本（= %s）" % os.path.basename(bins[h]))
                else:
                    os.replace(comp, os.path.splitext(dst)[0] + ".navmesh.bin")
                    bins[h] = os.path.splitext(dst)[0] + ".navmesh.bin"
                    print("    可走面副本随文件移动")

    # 根目录/旧位置的 navmesh_*.bin -> navmesh/
    if not args.dry:
        for base, dirs, files in os.walk(VIS):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS or d == "navmesh"]
            if os.path.abspath(base) == os.path.abspath(NAVBIN):
                continue
            for fn in files:
                if fn.startswith("navmesh_") and fn.endswith(".bin"):
                    src = os.path.join(base, fn)
                    dst = os.path.join(NAVBIN, fn)
                    if os.path.exists(dst):
                        if sha(src) == sha(dst):
                            os.remove(src)
                            continue
                        dst = unique(dst)
                    os.replace(src, dst)
                    print("%-52s -> %s" % (os.path.relpath(src, VIS), os.path.relpath(dst, VIS)))

    # _seen_* -> _state/
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

    # README 重新生成（只列 raw 下的 JSON）
    rows = []
    for base, dirs, files in os.walk(RAW):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.endswith(".json"):
                continue
            p = os.path.join(base, fn)
            try:
                with open(p, encoding="utf-8") as f:
                    d = json.load(f)
                mp = d.get("map") or {}
                rows.append((os.path.basename(base), fn, mp.get("fingerprint", ""),
                             mp.get("node_count", 0), mp.get("source", "")))
            except (OSError, ValueError):
                pass
    rows.sort()
    lines = [
        "④ 测试版 vis/ —— 游戏内 Ctrl+E 的导出（按性质分类）",
        "",
        "raw/      每次导出的原始扫描，按地图分文件夹：<级别>_<中文名>/<时间>_<指纹>.json",
        "          _非原生_插件铺点/ = 插件自己铺的点，不是游戏原生（不要当原始数据用）",
        "          _未识别_*/        = 指纹不在 navdata/dev/maps/_index.json 里",
        "navmesh/  去重后的 A* 可走面 navmesh_nm<顶点数>-<指纹>.bin",
        "_state/   插件内部去重标记 _seen_*（不用看）",
        "",
        "新导出仍会先落在 vis/ 根目录；跑一次 tools/tidy_vis.py 就归位。",
        "这个目录是 ④ 测试版，整理好之后用控制台「导入到开发版 ④→②」进 ②。",
        "",
        "当前收录：",
    ]
    for folder, fn, fp, nodes, src in rows:
        lines.append("  %-30s %-50s %-24s %4s 点  %s" % (folder, fn, fp, nodes, src or "-"))
    if not args.dry:
        with open(os.path.join(VIS, "README.txt"), "w", encoding="utf-8", newline="\r\n") as f:
            f.write("\n".join(lines) + "\n")
    print("完成：移动 %d 个 JSON；raw 共 %d 份" % (moved, len(rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
