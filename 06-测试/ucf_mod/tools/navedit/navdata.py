"""路点数据加载：同时支持旧版 graph_*.json 与 v1 契约（navgraph）。"""
import json
import os

import numpy as np

# 与 C 侧 editor.c 的 #define K_* 一一对应（导出时写的是字符串名，v1 JSON 用 kind_name()）
KIND_NAMES = {
    0: "未分类",
    1: "幽灵守区",
    2: "幽灵守点",
    3: "蹲守点",
    4: "守卫点",
    5: "守卫区",
    6: "出生点",
    7: "跳点",
    8: "标签区",
}

# C 侧导出的 kind 字符串 -> 编号（v1 文件里 kind 是字符串，旧版文件里是整数）
KIND_BY_NAME = {
    "nano_area": 1,
    "nano_pos": 2,
    "crouch": 3,
    "guard": 4,
    "guard_area": 5,
    "spawn": 6,
    "jump": 7,
    "tag_region": 8,
    "unknown": 0,
}

KIND_COLORS = {
    1: (0.98, 0.42, 0.16),
    2: (0.99, 0.76, 0.18),
    3: (0.35, 0.72, 0.98),
    4: (0.86, 0.34, 0.74),
    5: (0.95, 0.62, 0.30),
    6: (0.20, 0.92, 0.85),
    7: (0.55, 0.45, 0.95),
    8: (0.70, 0.70, 0.70),
}

SPAWN_NAMES = {0: "保卫者", 1: "潜伏者", 2: "中立", 3: "补给箱", 4: "红箱", 5: "蓝箱"}


class NavData(object):
    def __init__(self):
        self.nodes = np.zeros((0, 3), dtype=np.float32)
        self.node_info = []
        self.edges = np.zeros((0, 2), dtype=np.int32)
        self.features = []
        self.path = ""
        self.generated = ""
        self.source = ""

    @property
    def node_count(self):
        return int(len(self.nodes))

    @property
    def edge_count(self):
        return int(len(self.edges))

    def bbox(self):
        if len(self.nodes) == 0:
            return np.zeros((2, 3), dtype=np.float32)
        return np.array([self.nodes.min(0), self.nodes.max(0)], dtype=np.float32)


def _feature_from_dict(f):
    p = f.get("p") or [0, 0, 0]
    kind = f.get("kind", 0)
    if isinstance(kind, str):
        kind = KIND_BY_NAME.get(kind.strip().lower(), 0)
    kind = int(kind)
    return {
        "kind": kind,
        "name": f.get("name") or KIND_NAMES.get(kind, "?"),
        "aux": int(f.get("aux", 0)),
        "pos": (float(p[0]), float(p[1]), float(p[2])),
    }


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    nav = NavData()
    nav.path = path
    nav.generated = raw.get("generated", "") or raw.get("map", {}).get("name", "")
    nav.source = raw.get("map", {}).get("source", "") if isinstance(raw.get("map"), dict) else ""

    nodes = raw.get("nodes") or []
    arr = []
    for n in nodes:
        if isinstance(n, dict):
            p = n.get("p") or [0, 0, 0]
            arr.append((float(p[0]), float(p[1]), float(p[2])))
            nav.node_info.append({
                "id": n.get("id", ""),
                "tag": int(n.get("tag", 0)),
                "walk": int(n.get("walk", 1)),
                "pen": float(n.get("pen", 0)),
            })
        else:
            arr.append((float(n[0]), float(n[1]), float(n[2])))
            nav.node_info.append({
                "id": "",
                "tag": int(n[3]) if len(n) > 3 else 0,
                "walk": int(n[4]) if len(n) > 4 else 1,
                "pen": float(n[5]) if len(n) > 5 else 0.0,
            })
    if arr:
        nav.nodes = np.array(arr, dtype=np.float32)

    edges = raw.get("edges") or []
    e = []
    index_by_id = {}
    if any(isinstance(n, dict) for n in nodes):
        for i, n in enumerate(nodes):
            if isinstance(n, dict) and n.get("id"):
                index_by_id[n["id"]] = i
    for ed in edges:
        if isinstance(ed, dict):
            a, b = ed.get("a"), ed.get("b")
            if isinstance(a, str):
                a = index_by_id.get(a, -1)
            if isinstance(b, str):
                b = index_by_id.get(b, -1)
            if a is not None and b is not None and a >= 0 and b >= 0:
                e.append((int(a), int(b)))
        elif len(ed) >= 2:
            a, b = ed[0], ed[1]
            if isinstance(a, str):
                a = index_by_id.get(a, -1)
            if isinstance(b, str):
                b = index_by_id.get(b, -1)
            if a >= 0 and b >= 0:
                e.append((int(a), int(b)))
    if e:
        nav.edges = np.array(e, dtype=np.int32)

    for f in raw.get("features") or []:
        if isinstance(f, dict):
            nav.features.append(_feature_from_dict(f))
        elif isinstance(f, list) and len(f) >= 4:
            kind = int(f[0])
            nav.features.append({
                "kind": kind,
                "name": KIND_NAMES.get(kind, "?"),
                "aux": int(f[4]) if len(f) > 4 else 0,
                "pos": (float(f[1]), float(f[2]), float(f[3])),
            })
    return nav
