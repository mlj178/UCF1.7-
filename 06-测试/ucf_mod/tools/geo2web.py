#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""geo/<关卡>.npz  ->  geo/web/<关卡>.bin （给 navview.html 的 3D 视图用）

navedit 用的 npz 里带贴图与分块表，但贴图接得很乱；网页版只要「能看懂地形」的
灰模 + 法线 + 分块颜色，所以这里做一次离线瘦身：

  * 丢掉 shadow（阴影体）、blocker（碰撞壳）、card（巨幅装饰面）三类分块，
    它们本来就不该被看见，留在场景里只会挡住视线；
  * 顶点颜色（npz 的 c）是 navedit 用的随机染色，噪点很大，不用；
    改用材质色 x 法线光照，所以在 JSON 头里带上每块的颜色；
  * 法线量化成 int8（x127），位置 f32，索引 u32；
  * UV 不要（不贴图）。

二进制布局（小端）：
    magic   'UCFG'
    u32     version = 1
    u32     jsonLen
    json    utf-8（字段见下，后面补 0 到 4 字节对齐）
    f32[n*3]   positions
    i8 [n*3]   normals (-1..1 乘 127 取整)
    u32[t*3]   indices

json = {"level":..,"nverts":..,"ntris":..,"bbox":[[..],[..]],
        "ambient":[r,g,b],"chunks":[{"name","start","count","color":[r,g,b]}]}
start / count 是三角形区间（不是顶点区间）。

用法：
    python geo2web.py            # 转换 geo/ 下所有 npz
    python geo2web.py level1     # 只转指定关卡
    python geo2web.py --force    # 源文件没变也重转
"""
import argparse
import json
import os
import struct
import sys

import numpy as np

TOOLS = os.path.dirname(os.path.abspath(__file__))
UCF = os.path.dirname(TOOLS)
GEO = os.path.join(UCF, "geo")
OUT = os.path.join(GEO, "web")
MAGIC = b"UCFG"
VERSION = 1
SKIP_FLAGS = ("shadow", "blocker", "card")


def _bool(x):
    return bool(x)


def load_npz(path):
    """统一成 (pos, tris, groups, normals, meta)。"""
    z = np.load(path, allow_pickle=True)
    keys = set(z.files)
    pos = z["p"] if "p" in keys else z["v"]
    tri = z["i"] if "i" in keys else z["f"]
    grp = z["g"] if "g" in keys else np.zeros(len(tri), dtype=np.int32)
    nrm = z["n"] if "n" in keys else None
    meta = {}
    if "meta" in keys:
        try:
            meta = json.loads(str(z["meta"][0]))
        except Exception:
            meta = {}
    pos = np.ascontiguousarray(pos, dtype=np.float32)
    tri = np.ascontiguousarray(tri, dtype=np.int64)
    grp = np.ascontiguousarray(grp, dtype=np.int64)
    if nrm is not None and len(nrm) == len(pos):
        nrm = np.ascontiguousarray(nrm, dtype=np.float32)
    else:
        nrm = None
    return pos, tri, grp, nrm, meta


def face_normals(pos, tri):
    a = pos[tri[:, 0]].astype(np.float64)
    b = pos[tri[:, 1]].astype(np.float64)
    c = pos[tri[:, 2]].astype(np.float64)
    fn = np.cross(b - a, c - a)
    ln = np.linalg.norm(fn, axis=1)
    ln[ln == 0] = 1.0
    return fn / ln[:, None]


def vertex_normals(pos, tri):
    vn = np.zeros((len(pos), 3), dtype=np.float64)
    fn = face_normals(pos, tri)
    for k in range(3):
        np.add.at(vn, tri[:, k], fn)
    ln = np.linalg.norm(vn, axis=1)
    ln[ln == 0] = 1.0
    return (vn / ln[:, None]).astype(np.float32)


def convert(name, force=False):
    src = os.path.join(GEO, name + ".npz")
    dst = os.path.join(OUT, name + ".bin")
    if not os.path.isfile(src):
        return None
    if not force and os.path.isfile(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return {"level": name, "cached": True, "bytes": os.path.getsize(dst)}

    pos, tri, grp, nrm, meta = load_npz(src)
    mats = meta.get("mats") or []
    chunks = meta.get("chunks") or []
    amb = ((meta.get("env") or {}).get("ambient") or {})

    def rgb_of(chunk):
        col = chunk.get("color") or [1, 1, 1, 1]
        try:
            return [max(0.0, min(1.0, float(col[0]))),
                    max(0.0, min(1.0, float(col[1]))),
                    max(0.0, min(1.0, float(col[2])))]
        except Exception:
            return [1.0, 1.0, 1.0]

    if not chunks:
        # 没有分块表：整张图一块
        chunks = [{"name": name, "start": 0, "count": int(len(tri)),
                   "color": [1, 1, 1, 1], "mat": 0}]
        grp = np.zeros(len(tri), dtype=np.int64)

    # 按分块标记过滤三角形
    drop_group = set()
    for gi, ch in enumerate(chunks):
        if any(_bool(ch.get(k)) for k in SKIP_FLAGS):
            drop_group.add(gi)
    keep = np.ones(len(tri), dtype=bool)
    if drop_group:
        for gi in drop_group:
            keep &= (grp != gi)

    # 丢掉退化三角形
    if keep.any():
        a = pos[tri[keep, 0]]
        b = pos[tri[keep, 1]]
        c = pos[tri[keep, 2]]
        cr = np.cross(b - a, c - a)
        area2 = np.linalg.norm(cr, axis=1)
        good = area2 > 1e-7
        idx_keep = np.nonzero(keep)[0]
        keep[idx_keep[~good]] = False

    tri2 = tri[keep]
    grp2 = grp[keep]
    if len(tri2) == 0:
        print("  !! %s 过滤后没有三角形，跳过" % name)
        return None

    used = np.unique(tri2.ravel())
    remap = np.full(len(pos), -1, dtype=np.int64)
    remap[used] = np.arange(len(used))
    pos2 = pos[used]
    nrm2 = nrm[used] if nrm is not None else vertex_normals(pos, tri2)[used]
    tri2 = remap[tri2]

    # 重组分块表（按原始顺序，只保留还有三角形的块）
    order = np.argsort(grp2, kind="stable")
    tri2 = tri2[order]
    grp2 = grp2[order]
    counts = {}
    for g in grp2.tolist():
        counts[g] = counts.get(g, 0) + 1
    out_chunks = []
    cursor = 0
    for gi in sorted(counts):
        ch = chunks[gi] if gi < len(chunks) else {}
        out_chunks.append({
            "name": str(ch.get("name") or "")[:80],
            "start": int(cursor),
            "count": int(counts[gi]),
            "color": [round(v, 3) for v in rgb_of(ch)],
        })
        cursor += counts[gi]

    lo = pos2.min(axis=0).astype(float).tolist()
    hi = pos2.max(axis=0).astype(float).tolist()
    sky = amb.get("sky") or [0.66, 0.68, 0.70]
    try:
        ambient = [round(float(sky[0]), 3), round(float(sky[1]), 3), round(float(sky[2]), 3)]
    except Exception:
        ambient = [0.66, 0.68, 0.70]

    header = {
        "level": name,
        "nverts": int(len(pos2)),
        "ntris": int(len(tri2)),
        "bbox": [[round(v, 3) for v in lo], [round(v, 3) for v in hi]],
        "ambient": ambient,
        "chunks": out_chunks,
    }
    js = json.dumps(header, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    nrm_i8 = np.clip(np.round(nrm2 * 127.0), -127, 127).astype(np.int8)

    os.makedirs(OUT, exist_ok=True)
    tmp = dst + ".tmp"
    pos_bytes = np.ascontiguousarray(pos2, dtype="<f4").tobytes()
    nrm_bytes = np.ascontiguousarray(nrm_i8, dtype=np.int8).tobytes()
    idx_bytes = np.ascontiguousarray(tri2, dtype="<u4").tobytes()
    pad_json = (4 - ((12 + len(js)) % 4)) % 4      # JSON 头之后也要对齐（Float32Array 要求）
    head_len = 12 + len(js) + pad_json + len(pos_bytes) + len(nrm_bytes)
    pad = (4 - (head_len % 4)) % 4                 # 索引是 u32，同样要 4 字节对齐
    with open(tmp, "wb") as f:
        f.write(MAGIC)
        f.write(struct.pack("<II", VERSION, len(js)))
        f.write(js)
        if pad_json:
            f.write(b"\x00" * pad_json)
        f.write(pos_bytes)
        f.write(nrm_bytes)
        if pad:
            f.write(b"\x00" * pad)
        f.write(idx_bytes)
    os.replace(tmp, dst)
    return {
        "level": name,
        "nverts": int(len(pos2)),
        "ntris": int(len(tri2)),
        "chunks": len(out_chunks),
        "dropped_tris": int(len(tri) - len(tri2)),
        "bytes": os.path.getsize(dst),
    }


def main():
    ap = argparse.ArgumentParser(description="npz 关卡几何 -> 网页可读的 .bin")
    ap.add_argument("levels", nargs="*", help="只转这些关卡名（默认全部）")
    ap.add_argument("--force", action="store_true", help="源文件没变也重转")
    args = ap.parse_args()

    if not os.path.isdir(GEO):
        sys.exit("找不到 geo 目录: " + GEO)
    names = args.levels or sorted(fn[:-4] for fn in os.listdir(GEO) if fn.lower().endswith(".npz"))
    if not names:
        sys.exit("geo 目录里没有 .npz（先跑 navedit 提取一次几何，或确认路径）")
    total = 0
    for name in names:
        r = convert(name, force=args.force)
        if not r:
            print("跳过 %s（源文件不存在或没有可用三角形）" % name)
            continue
        if r.get("cached"):
            print("%-12s 已是最新  %6.2f MB" % (name, r["bytes"] / 1048576.0))
        else:
            total += r["bytes"]
            print("%-12s 顶点 %7d  三角 %7d  分块 %3d  丢弃 %6d   %6.2f MB" % (
                name, r["nverts"], r["ntris"], r["chunks"], r["dropped_tris"], r["bytes"] / 1048576.0))
    print("完成，输出目录 %s" % OUT)


if __name__ == "__main__":
    main()