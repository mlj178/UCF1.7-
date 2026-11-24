#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""数据统计：导出收件箱、可走面、目录哈希与差异（「数据」「导出」页用）。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


import hashlib
import os

from ui.env import P
from ui.packs import _is_pack_dir
from ui.util import _listdir


def latest_export(root):
    r"""最新一份导出 JSON：<图>\导出\ 与收件箱 vis\（认不出关卡的会留在收件箱）。
    返回 (文件名, 完整路径, 修改时间戳)；没有则 None。"""
    best = None
    scan = [os.path.join(root, "vis")]
    for _rel, path in P.map_files(root):
        scan.append(os.path.join(os.path.dirname(path), "导出"))
    for d in scan:
        if not os.path.isdir(d):
            continue
        for base, dirs, files in os.walk(d):
            dirs[:] = [x for x in dirs if x not in ("navmesh", "_state", "_noise")]
            for fn in files:
                if fn.startswith("_seen_") or not fn.endswith(".json"):
                    continue
                p = os.path.join(base, fn)
                try:
                    st = os.stat(p)
                except OSError:
                    continue
                if not os.path.isfile(p):
                    continue
                if best is None or st.st_mtime > best[2]:
                    best = (fn, p, st.st_mtime)
    return best


def vis_raw_dir(root):
    r"""新结构优先打开 vis\raw（按地图分好）；旧结构回退 vis 根。"""
    raw = os.path.join(root, "vis", "raw")
    return raw if os.path.isdir(raw) else os.path.join(root, "vis")


def data_counts(root):
    r"""(图数, 路线文件数, 路线条数, 可走面数) —— 只看每张图文件夹里的数据。"""
    maps = len(P.map_files(root))
    routes = P.route_files(root)
    lines = 0
    for _fp, path in routes:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                lines += len([ln for ln in f if ln.strip() and not ln.lstrip().startswith("#")])
        except OSError:
            pass
    return maps, len(routes), lines, len(P.navmesh_files(root))


def test_stats(root):
    r"""② 开发版收件箱：(导出 JSON 数, 可走面数, 测试包数, 字节数, 最新写入时间)。"""
    vis = os.path.join(root, "vis")
    n_json = n_bin = total = 0
    latest = 0.0
    for base_dir, dirs, files in os.walk(vis):
        dirs[:] = [x for x in dirs if x not in ("_state", "_noise")]
        for fn in files:
            p = os.path.join(base_dir, fn)
            try:
                st = os.stat(p)
            except OSError:
                continue
            if not os.path.isfile(p):
                continue
            total += st.st_size
            latest = max(latest, st.st_mtime)
            if fn.startswith("navmesh_") and fn.endswith(".bin"):
                n_bin += 1
            elif fn.endswith(".json"):
                n_json += 1
    packs = 0
    pk_dir = os.path.join(root, "packs")
    try:
        for entry in os.listdir(pk_dir):
            d = os.path.join(pk_dir, entry)
            if not os.path.isdir(d):
                continue
            if _is_pack_dir(d):
                packs += 1
                continue
            for sub in _listdir(d):
                if os.path.isdir(os.path.join(d, sub)) and _is_pack_dir(os.path.join(d, sub)):
                    packs += 1
    except OSError:
        pass
    return n_json, n_bin, packs, total, latest


def export_filed(root):
    r"""已经归位到各图文件夹的导出份数：<图>\导出\*.json。"""
    n = 0
    for _rel, path in P.map_files(root):
        d = os.path.join(os.path.dirname(path), "导出")
        if os.path.isdir(d):
            n += len([f for f in os.listdir(d) if f.endswith(".json")])
    return n


def tree_hashes(root):
    r"""每张图的 map.json + 路线 txt 的 sha1：判断两版是不是同一份数据。
    名字注册表 names.json 与自动生成的索引不算（格式差异不影响游戏）。"""
    out = {}
    for rel, path in P.map_files(root):
        try:
            with open(path, "rb") as f:
                out[rel] = hashlib.sha1(f.read()).hexdigest()
        except OSError:
            pass
    for fp, path in P.route_files(root):
        try:
            with open(path, "rb") as f:
                out[fp + ".txt"] = hashlib.sha1(f.read()).hexdigest()
        except OSError:
            pass
    return out


def diff_count(a, b):
    keys = set(a) | set(b)
    return sum(1 for k in keys if a.get(k) != b.get(k))
