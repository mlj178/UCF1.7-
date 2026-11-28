#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""sweep2navmesh.py - 用游戏里量出来的地面高度表，直接烘一张面（UCFN v2）

输入  log/ground_samples_<图>.txt   插件「跟随式采样」量出来的地面
                                  （每行 格x 格z 地面y，玩家脚下的真实碰撞面）
输出  <out>/<map>.navmesh        UCFN v2；每格自己出面，不再要求四邻都在

2026-11-28：格子边长从数据自己推（--cell > 文件头 cell= > 从数据推）。
以前写死 1.5，把 1 m 的跟随采样数据按 1.5 m 取整，土丘整片叠在一起。
"""
import argparse, math, os, struct, json, sys
import numpy as np

CELL = 1.5


def read_header_cell(path):
    r"""文件头里写了 cell= 就用它（跟随采样的第一行就写着）。"""
    try:
        for line in open(path, encoding="utf-8", errors="replace"):
            if not line.startswith("#"):
                break
            if "cell=" in line:
                try:
                    return float(line.split("cell=", 1)[1].split()[0])
                except (IndexError, ValueError):
                    return 0.0
    except OSError:
        pass
    return 0.0


def guess_cell(path):
    r"""从数据里推格子边长：取所有点里最小的正间距（1 m 数据 -> 1.0）。"""
    xs, zs = [], []
    for line in open(path, encoding="utf-8", errors="replace"):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        a = s.split()
        if len(a) < 3:
            continue
        xs.append(float(a[0])); zs.append(float(a[1]))
        if len(xs) > 4000:
            break
    best = 0.0
    for arr in (sorted(set(round(v, 3) for v in xs)), sorted(set(round(v, 3) for v in zs))):
        for p, q in zip(arr, arr[1:]):
            d = q - p
            if 0.05 < d < 5.0 and (best == 0.0 or d < best):
                best = d
    return best or 1.5


def load_sweep(path, ymin=-1e9, ymax=1e9):
    cells = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        a = s.split()
        if len(a) < 3:
            continue
        x, z, y = float(a[0]), float(a[1]), float(a[2])
        if y < ymin or y > ymax:
            continue
        i = int(round((x - X0) / CELL))
        j = int(round((z - Z0) / CELL))
        cells[(j, i)] = y
    return cells


def main():
    global X0, Z0
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", required=True)
    ap.add_argument("--out", default="")
    ap.add_argument("--map", default="nano30_storm")
    # 0 = 自动（1.2 × 格子边长 ≈ 50°）。老默认 0.9 是按 1.5 m 手调的，
    # 会把 31° 以上的斜坡整片丢掉 —— 用户要"可走斜坡"，所以改成跟格子走。
    ap.add_argument("--max-rise", type=float, default=0.0)
    ap.add_argument("--cell", type=float, default=0.0, help="格子边长；不给就读文件头、再不给就从数据推")
    ap.add_argument("--ymin", type=float, default=-1e9)
    ap.add_argument("--ymax", type=float, default=1e9)
    args = ap.parse_args()

    global CELL
    CELL = args.cell or read_header_cell(args.sweep) or guess_cell(args.sweep)
    if args.max_rise <= 0:
        args.max_rise = round(1.2 * CELL, 3)
    print("cell", CELL, "max_rise", args.max_rise)

    # 原点取数据自己的最小格中心：老扫描是固定 -220/-280，跟随采样是任意位置，
    # 用"最小坐标"当原点两边都不用改数据。
    X0 = Z0 = 0.0
    first = None
    for line in open(args.sweep, encoding="utf-8", errors="replace"):
        s = line.strip()
        if s and not s.startswith("#"):
            a = s.split()
            if len(a) >= 3:
                first = (float(a[0]), float(a[1]))
                break
    if first is None:
        raise SystemExit("empty sweep")
    X0, Z0 = first[0], first[1]
    cells = load_sweep(args.sweep, args.ymin, args.ymax)
    if not cells:
        raise SystemExit("no cells")
    js = [k[0] for k in cells]; ii = [k[1] for k in cells]
    j0, j1 = min(js), max(js); i0, i1 = min(ii), max(ii)
    print("cells", len(cells), "grid", (i1 - i0 + 1), "x", (j1 - j0 + 1))

    # 顶点高度：四邻命中格的中位数；缺就用最近的那个
    vh = {}
    for (j, i) in cells:
        for dj in (0, 1):
            for di in (0, 1):
                vh.setdefault((j + dj, i + di), []).append(cells[(j, i)])
    for k, v in vh.items():
        v.sort(); vh[k] = v[len(v) // 2]

    verts = {}
    tris = []
    def vid(k):
        if k not in verts:
            verts[k] = len(verts)
        return verts[k]

    kept = 0
    for (j, i), y in cells.items():
        hs = [vh.get((j, i), y), vh.get((j, i + 1), y), vh.get((j + 1, i + 1), y), vh.get((j + 1, i), y)]
        if max(hs) - min(hs) > args.max_rise:
            continue
        a = vid((j, i)); b = vid((j, i + 1)); c = vid((j + 1, i + 1)); d = vid((j + 1, i))
        tris.append((a, c, b)); tris.append((a, d, c))
        kept += 1
    print("cells kept", kept, "verts", len(verts), "tris", len(tris))

    V = np.zeros((len(verts), 3), dtype=np.float32)
    for (j, i), k in verts.items():
        V[k] = (X0 + i * CELL, vh.get((j, i), 0.0), Z0 + j * CELL)
    T = np.array(tris, dtype=np.int64)

    # 按面积留岛
    parent = list(range(len(V)))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for a, b, c in T:
        for p, q in ((a, b), (b, c)):
            ra, rb = find(p), find(q)
            if ra != rb: parent[ra] = rb
    comp = np.array([find(x) for x in range(len(V))])
    tc = comp[T[:, 0]]
    ids, cnt = np.unique(tc, return_counts=True)
    keep = set(ids[cnt >= 8])
    m = np.isin(tc, list(keep))
    T = T[m]
    used = np.unique(T); remap = -np.ones(len(V), dtype=np.int64); remap[used] = np.arange(len(used))
    T = remap[T]; V = V[used]
    print("islands", len(ids), "->", len(keep), "| final verts", len(V), "tris", len(T))

    out = args.out or os.path.join(os.path.dirname(args.sweep), args.map + "_sweep.navmesh")
    head = json.dumps({"map": args.map, "cell": CELL, "verts": int(len(V)), "tris": int(len(T)),
                       "bbox": [[float(V[:,0].min()), float(V[:,2].min())],
                                [float(V[:,0].max()), float(V[:,2].max())]]},
                      separators=(",", ":")).encode("utf-8")
    with open(out, "wb") as f:
        f.write(b"UCFN"); f.write(struct.pack("<IIII", 2, len(head), len(V), len(T)))
        f.write(head); f.write(V.astype("<f4").tobytes()); f.write(T.astype("<u4").tobytes())
    print("wrote", out, round(os.path.getsize(out)/1024.0,1), "KB")


if __name__ == "__main__":
    main()
