#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「00 练习场」：一块 40x40 的空地 + 几个箱子 + 一组台阶 + 一根柱子。

这是什么：
  * geo/web/practice.bin  —— 3D 视图里的灰模（UCFG 格式，和 geo2web.py 输出的完全一样）
  * maps/00_练习场.json   —— 一张 0 个点、0 条边的空白路点图（练习用，随便画）

练习场的指纹固定是 n0-0000000000000000，意思是「这张图本来一个路点都没有」。
它只在练习场 / 空图里生效，不会碰到任何真地图。

用法：
    python make_practice.py            # 生成（已存在也覆盖）
    python make_practice.py --check    # 只检查现有文件对不对
"""
import argparse
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
for _p in (os.path.join(UCF_ROOT, "core"), HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from ucf_paths import GEO, DEV  # noqa: E402

GEOWEB = os.path.join(GEO, "web")
LEVEL = "practice"
PRACTICE_FP = "n0-0000000000000000"

pos = []
nrm = []
idx = []
chunks = []


def add_tri(p0, p1, p2, n):
    base = len(pos)
    for p in (p0, p1, p2):
        pos.append((float(p[0]), float(p[1]), float(p[2])))
        nrm.append((float(n[0]), float(n[1]), float(n[2])))
    idx.extend((base, base + 1, base + 2))


def add_quad(a, b, c, d, n):
    add_tri(a, b, c, n)
    add_tri(a, c, d, n)


def begin(name, color):
    chunks.append({"name": name, "start": len(idx) // 3, "count": 0, "color": color})
    return chunks[-1]


def end(ch):
    ch["count"] = len(idx) // 3 - ch["start"]


def box(cx, cy, cz, sx, sy, sz):
    """轴对齐方盒：cy 是底面高度。"""
    x0, x1 = cx - sx / 2.0, cx + sx / 2.0
    y0, y1 = cy, cy + sy
    z0, z1 = cz - sz / 2.0, cz + sz / 2.0
    add_quad((x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1), (0, 1, 0))   # 顶
    add_quad((x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1), (0, 0, 1))   # +z
    add_quad((x1, y0, z0), (x0, y0, z0), (x0, y1, z0), (x1, y1, z0), (0, 0, -1))  # -z
    add_quad((x1, y0, z1), (x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (1, 0, 0))   # +x
    add_quad((x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0), (-1, 0, 0))  # -x


def floor(y=0.0, half=20.0):
    add_quad((-half, y, -half), (-half, y, half), (half, y, half), (half, y, -half), (0, 1, 0))


def grid(y=0.012, half=20.0, step=5.0, w=0.05):
    """每 5 米一条细线，纯粹为了让人看得出方向。"""
    x = -half
    while x <= half + 0.001:
        add_quad((x - w, y, -half), (x + w, y, -half), (x + w, y, half), (x - w, y, half), (0, 1, 0))
        add_quad((-half, y, x - w), (half, y, x - w), (half, y, x + w), (-half, y, x + w), (0, 1, 0))
        x += step


def build():
    ch = begin("floor", [0.42, 0.46, 0.52])
    floor()
    end(ch)

    ch = begin("grid", [0.30, 0.33, 0.39])
    grid()
    end(ch)

    ch = begin("box", [0.58, 0.46, 0.34])
    box(-8.0, 0.0, -6.0, 4.0, 1.5, 4.0)      # 矮箱子，能跳上去
    box(7.0, 0.0, 5.0, 3.0, 1.2, 3.0)        # 另一个箱子
    box(0.0, 0.0, 12.0, 6.0, 1.0, 2.0)       # 一道矮墙
    end(ch)

    ch = begin("stairs", [0.50, 0.52, 0.55])
    for i in range(5):                        # 5 级台阶，每级 0.25 m
        box(10.0 + i * 0.6, 0.0, 0.0, 0.6, 0.25 * (i + 1), 3.0)
    box(13.6, 0.0, 0.0, 3.0, 1.25, 3.0)       # 台阶顶上的平台
    end(ch)

    ch = begin("pillar", [0.48, 0.48, 0.50])
    box(0.0, 0.0, -12.0, 2.0, 3.0, 2.0)
    end(ch)


def write_bin(path):
    lo = [min(p[i] for p in pos) for i in range(3)]
    hi = [max(p[i] for p in pos) for i in range(3)]
    hdr = {
        "level": LEVEL,
        "nverts": len(pos),
        "ntris": len(idx) // 3,
        "bbox": [lo, hi],
        "ambient": [0.55, 0.58, 0.62],
        "chunks": chunks,
    }
    js = json.dumps(hdr, separators=(",", ":")).encode("utf-8")
    pad = (-len(js)) % 4
    out = bytearray()
    out += b"UCFG" + struct.pack("<II", 1, len(js)) + js + b"\x00" * pad
    for p in pos:
        out += struct.pack("<3f", p[0], p[1], p[2])
    for n in nrm:
        out += struct.pack("<3b", int(n[0] * 127), int(n[1] * 127), int(n[2] * 127))
    out += b"\x00" * ((-len(out)) % 4)
    for i in idx:
        out += struct.pack("<I", i)
    with open(path, "wb") as f:
        f.write(out)
    return hdr, len(out)


def practice_doc(bbox):
    return {
        "format": "ucf-navgraph",
        "version": 1,
        "generated": "2026-11-16 14:00:00",
        "plugin": "ucf_mod practice",
        "map": {
            "name": "00_练习场",
            "label": "练习场（空白）",
            "level": LEVEL,
            "scene": "Practice",
            "fingerprint": PRACTICE_FP,
            "source": "practice",
            "node_count": 0,
            "edge_count": 0,
            "bbox": bbox,
            "support": 1.0,
        },
        "counts": {"nodes": 0, "edges": 0, "features": 0},
        "nodes": [],
        "edges": [],
        "features": [],
        "lines": {
            "nano_area": [], "nano_pos": [], "crouch": [], "guard_area": [],
            "guard": [], "jump": [], "tag_region": [],
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    binp = os.path.join(GEOWEB, LEVEL + ".bin")
    # 练习场是自造的沙盒，不属于任何一张正式图；放 ② 00_公共，别塞进图文件夹
    jsonp = os.path.join(DEV, "00_公共", "00_练习场.json")
    if a.check:
        print("bin  :", binp, os.path.getsize(binp) if os.path.exists(binp) else "缺失")
        print("json :", jsonp, os.path.getsize(jsonp) if os.path.exists(jsonp) else "缺失")
        if os.path.exists(jsonp):
            with open(jsonp, "r", encoding="utf-8") as f:
                d = json.load(f)
            print("指纹 :", d["map"]["fingerprint"], "节点", d["counts"]["nodes"])
        return
    os.makedirs(GEOWEB, exist_ok=True)
    os.makedirs(os.path.dirname(jsonp), exist_ok=True)
    build()
    hdr, nbytes = write_bin(binp)
    with open(jsonp, "w", encoding="utf-8") as f:
        json.dump(practice_doc(hdr["bbox"]), f, ensure_ascii=False, indent=1)
    print("写出 %s（%d 顶点 / %d 三角 / %d 字节）" % (binp, hdr["nverts"], hdr["ntris"], nbytes))
    print("写出 %s（0 点 0 边，指纹 %s）" % (jsonp, PRACTICE_FP))


if __name__ == "__main__":
    main()
