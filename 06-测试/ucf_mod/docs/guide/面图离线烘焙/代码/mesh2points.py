#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""mesh2points.py - 把烘焙好的面（<map>.navmesh）铺成 grow 点图

为什么要 grow：插件注释写死了——运行期「借槽位」加点不能超过进图时的节点数，
超过会让 A* 的 PathHandler 越界、寻路线程永久停摆（人机全部不动）。
真·新增节点必须走 grow 包（在 PathProcessor.Lock 窗口里建点）。

输入  <map>.navmesh（UCFN v2）
输出  <out>/<map>_grow.txt   # ucf-navedit v1，grow，node add / edge add
"""
import argparse, json, math, os, struct, sys
import numpy as np


def read_navmesh(path):
    b = open(path, "rb").read()
    if b[:4] != b"UCFN":
        raise SystemExit("not UCFN: %s" % path)
    ver, jl, nv, nt = struct.unpack_from("<IIII", b, 4)
    if ver != 2:
        raise SystemExit("need UCFN v2")
    verts = np.frombuffer(b, dtype="<f4", count=nv * 3, offset=20 + jl).reshape(nv, 3).astype(np.float64)
    tris = np.frombuffer(b, dtype="<u4", count=nt * 3, offset=20 + jl + nv * 12).reshape(nt, 3)
    return verts, tris


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--navmesh", required=True)
    ap.add_argument("--user", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--gap", type=float, default=3.0)
    ap.add_argument("--dist", type=float, default=2.2)
    # 桥接（手摆点 <-> 面图点）：2026-11-28 实测 2.2/0.9 太紧，548 个新点只连出 11 条桥。
    # 手摆点间距 ~5 m，且比地面高 1.4~1.5 m（录制时就那样），所以高度差必须放宽。
    ap.add_argument("--bridge", type=float, default=3.0, help="水平距离上限")
    ap.add_argument("--bridge-dy", type=float, default=1.8, help="高度差上限")
    ap.add_argument("--fp", default="")
    args = ap.parse_args()

    V, T = read_navmesh(args.navmesh)
    xmin, zmin = V[:, 0].min(), V[:, 2].min()
    xmax, zmax = V[:, 0].max(), V[:, 2].max()
    cs = 1.0
    W = int(math.ceil((xmax - xmin) / cs)) + 1
    H = int(math.ceil((zmax - zmin) / cs)) + 1
    # 三角形 -> 格子 索引
    cell = {}
    for ti, t in enumerate(T):
        p = V[t]
        i0 = max(0, int((p[:, 0].min() - xmin) / cs)); i1 = min(W - 1, int((p[:, 0].max() - xmin) / cs))
        j0 = max(0, int((p[:, 2].min() - zmin) / cs)); j1 = min(H - 1, int((p[:, 2].max() - zmin) / cs))
        for j in range(j0, j1 + 1):
            for i in range(i0, i1 + 1):
                cell.setdefault((j, i), []).append(ti)

    def height_at(x, z):
        i = int((x - xmin) / cs); j = int((z - zmin) / cs)
        for ti in cell.get((j, i), ()):
            p = V[T[ti]]
            x1, z1 = p[0, 0], p[0, 2]; x2, z2 = p[1, 0], p[1, 2]; x3, z3 = p[2, 0], p[2, 2]
            d = (z2 - z3) * (x1 - x3) + (x3 - x2) * (z1 - z3)
            if abs(d) < 1e-9:
                continue
            a = ((z2 - z3) * (x - x3) + (x3 - x2) * (z - z3)) / d
            b = ((z3 - z1) * (x - x3) + (x1 - x3) * (z - z3)) / d
            c = 1 - a - b
            if a >= -1e-6 and b >= -1e-6 and c >= -1e-6:
                return a * p[0, 1] + b * p[1, 1] + c * p[2, 1]
        return None

    # 采样
    pts = []
    g = args.gap
    y = xmin + g * 0.5
    while y < xmax:
        z = zmin + g * 0.5
        while z < zmax:
            h = height_at(y, z)
            if h is not None:
                pts.append((y, h, z))
            z += g
        y += g
    print("mesh points", len(pts))

    # 你的点
    unodes, uedges, ujumps = [], [], []
    if args.user and os.path.isfile(args.user):
        import re
        for line in open(args.user, encoding="utf-8", errors="replace"):
            s = line.strip()
            m = re.match(r"node add ([-\d.]+) ([-\d.]+) ([-\d.]+)", s)
            if m:
                unodes.append(tuple(float(x) for x in m.groups())); continue
            m = re.match(r"edge add ([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)", s)
            if m:
                v = [float(x) for x in m.groups()]
                uedges.append(((v[0], v[1], v[2]), (v[3], v[4], v[5]))); continue
            m = re.match(r"jump add ([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)", s)
            if m:
                v = [float(x) for x in m.groups()]
                ujumps.append(s)
    print("user nodes", len(unodes), "edges", len(uedges), "jumps", len(ujumps))

    # 跳跃起终点：这附近不铺点，否则 A* 直接绕路走，永远用不上跳
    jump_pts = []
    for j in ujumps:
        import re as _re
        m = _re.match(r"jump add ([-d.]+) ([-d.]+) ([-d.]+) ([-d.]+) ([-d.]+) ([-d.]+)", j)
        if m:
            v = [float(x) for x in m.groups()]
            jump_pts.append((v[0], v[1], v[2]))
            jump_pts.append((v[3], v[4], v[5]))

    # 避让你的点 + 跳跃端点
    keep = []
    for p in pts:
        # 2026-11-28：避让改成 3D 判定。手摆点普遍比地面高 1.4~1.5 m（录制时就那样），
        # 原来只按水平距离避让，会在每个手摆点底下挖一个半径 1.2 m 的洞 —— 桥接只能跨 3 m 以上，
        # 196 个手摆点只连上 45 个。高度差 ≥1 m 的不算重复，面图点该留就留。
        if any(math.hypot(p[0] - q[0], p[2] - q[2]) < 1.2 and abs(p[1] - q[1]) < 1.0 for q in unodes):
            continue
        if any(math.hypot(p[0] - q[0], p[2] - q[2]) < 2.5 and abs(p[1] - q[1]) < 2.0 for q in jump_pts):
            continue
        keep.append(p)
    print("mesh points after avoid", len(keep))

    # 连边：3D 距离 + 沿线贴面
    buckets = {}
    for k, p in enumerate(keep):
        buckets.setdefault((int(p[0] // args.dist), int(p[2] // args.dist)), []).append(k)
    edges = set()

    def ok(a, b):
        L = math.hypot(b[0] - a[0], b[2] - a[2])
        n = max(2, int(L / 0.5))
        for t in range(1, n):
            f = t / n
            x = a[0] + (b[0] - a[0]) * f
            z = a[2] + (b[2] - a[2]) * f
            h = height_at(x, z)
            if h is None or abs(h - (a[1] + (b[1] - a[1]) * f)) > 0.5:
                return False
        return True

    for k, p in enumerate(keep):
        bx, bz = int(p[0] // args.dist), int(p[2] // args.dist)
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for m in buckets.get((bx + dx, bz + dz), ()):
                    if m <= k:
                        continue
                    q = keep[m]
                    if math.hypot(q[0] - p[0], q[2] - p[2]) > args.dist:
                        continue
                    if abs(q[1] - p[1]) > 0.6:
                        continue
                    if ok(p, q):
                        edges.add((k, m))
    print("edges", len(edges))

    fp = args.fp or "auto"
    out = args.out or os.path.join(os.path.dirname(args.navmesh), "grow.txt")
    lines = ["# ucf-navedit v1 fp=%s" % fp,
             "# grow: 面图铺点 %d + 手摆 %d" % (len(keep), len(unodes)),
             "grow"]
    # 顺序很重要：插件最多吃 4096 条编辑，超了尾部会被截掉。
    # 所以你的点/边/跳必须放最前面，面图铺点在后面。
    for p in unodes:
        lines.append("node add %.3f %.3f %.3f" % p)
    for a, b in uedges:
        lines.append("edge add %.3f %.3f %.3f %.3f %.3f %.3f" % (a + b))
    for j in ujumps:
        lines.append(j)
    for p in keep:
        lines.append("node add %.3f %.3f %.3f" % p)
    # 桥边：把两张网连起来。
    # 2026-11-28 实测改了方向：原来是从面图点往手摆点找（水平 ≤2.2 且 |dy| ≤0.9），
    # 手摆点间距 ~5 m，绝大多数面图点 2.2 m 内根本没有手摆点 —— 548 个新点只连出 11 条桥，
    # 新网等于孤岛，人机不会走。现在反过来：**每个手摆点**就近连到一个面图点，
    # 保证手摆点一定接进新网；高差大的（屋顶 / 上层）故意不连，别把街面连到屋顶上。
    bridges = []
    used = set()
    for q in unodes:
        best = None
        for p_ in keep:
            d = math.hypot(p_[0] - q[0], p_[2] - q[2])
            if d <= args.bridge and abs(p_[1] - q[1]) <= args.bridge_dy and (best is None or d < best[0]):
                best = (d, p_)
        if best is None:
            continue
        key = (round(best[1][0], 2), round(best[1][2], 2), round(best[1][1], 1))
        if key in used:
            continue
        used.add(key)
        bridges.append((q, best[1]))
    # 双向：插件里 edge add 只建一条有向边，单向会让一半方向走不通
    for k, m in sorted(edges):
        p, q = keep[k], keep[m]
        lines.append("edge add %.3f %.3f %.3f %.3f %.3f %.3f" % (p + q))
        lines.append("edge add %.3f %.3f %.3f %.3f %.3f %.3f" % (q + p))
    for a, b in bridges:
        lines.append("edge add %.3f %.3f %.3f %.3f %.3f %.3f" % (a + b))
        lines.append("edge add %.3f %.3f %.3f %.3f %.3f %.3f" % (b + a))
    print("bridges", len(bridges))
    print("total edits", len(lines) - 3, "(cap 4096)")
    open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("wrote", out, "lines", len(lines), "KB", round(os.path.getsize(out) / 1024.0, 1))


if __name__ == "__main__":
    main()
