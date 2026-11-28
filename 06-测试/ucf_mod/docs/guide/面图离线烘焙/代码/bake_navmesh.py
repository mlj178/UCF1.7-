#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""bake_navmesh.py - 从地图三角网烘焙「可走面」（NavMeshGraph 用的三角网）

输入  data/geo/web/<map>.bin          UCFG v1/v2 世界坐标三角网
输出  <out>/<map>.navmesh             UCFN v1（顶点 f32x3 + 三角形 u32x3）
      <out>/<map>_preview.png         俯视预览（可走面 + 你的路点）
      <out>/<map>_report.txt          数字与人话结论

做法（高度场式，稳、可复现）
  1) 三角面分类：地面 / 天花板 / 墙
  2) 栅格 1 m：每格取最低的、头顶够高的地面层；墙挡住的格不算
  3) 顶点高度取四邻可走格的平均（共享顶点 -> A* 能连边）
  4) 四个角都合法的格出两个三角形
"""
import argparse, glob, json, math, os, struct
import numpy as np

MAGIC = b"UCFN"
VERSION = 2   # v2: 头里带 nv/nt，插件直接读，不用解 json


def read_ucfg(path):
    b = open(path, "rb").read()
    if b[:4] != b"UCFG":
        raise SystemExit("not UCFG: %s" % path)
    ver, jl = struct.unpack_from("<II", b, 4)
    js = json.loads(b[12:12 + jl].decode("utf-8"))
    off = (12 + jl + 3) & ~3
    n, t = js["nverts"], js["ntris"]
    pos = np.frombuffer(b, dtype="<f4", count=n * 3, offset=off).reshape(n, 3); off += n * 12
    off += n * 3
    if ver >= 2:
        off += n * 8
    off = (off + 3) & ~3
    idx = np.frombuffer(b, dtype="<u4", count=t * 3, offset=off).reshape(t, 3)
    return js, pos.astype(np.float64), idx


def raster(tris, xmin, zmin, W, H, cs, is_floor):
    cells = {}
    for t in tris:
        xs, ys, zs = t[:, 0], t[:, 1], t[:, 2]
        i0 = max(0, int((xs.min() - xmin) / cs) - 1); i1 = min(W - 1, int((xs.max() - xmin) / cs) + 1)
        j0 = max(0, int((zs.min() - zmin) / cs) - 1); j1 = min(H - 1, int((zs.max() - zmin) / cs) + 1)
        if i1 < i0 or j1 < j0:
            continue
        cx = xmin + (np.arange(i0, i1 + 1) + 0.5) * cs
        cz = zmin + (np.arange(j0, j1 + 1) + 0.5) * cs
        X, Z = np.meshgrid(cx, cz)
        d = (t[1, 2] - t[2, 2]) * (t[0, 0] - t[2, 0]) + (t[2, 0] - t[1, 0]) * (t[0, 2] - t[2, 2])
        if abs(d) < 1e-9:
            continue
        w0 = ((t[1, 2] - t[2, 2]) * (X - t[2, 0]) + (t[2, 0] - t[1, 0]) * (Z - t[2, 2])) / d
        w1 = ((t[2, 2] - t[0, 2]) * (X - t[2, 0]) + (t[0, 0] - t[2, 0]) * (Z - t[2, 2])) / d
        w2 = 1.0 - w0 - w1
        inside = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
        if not inside.any():
            continue
        hy = w0 * ys[0] + w1 * ys[1] + w2 * ys[2]
        jj, ii = np.nonzero(inside)
        for k in range(len(jj)):
            cells.setdefault((j0 + int(jj[k]), i0 + int(ii[k])), []).append(
                (float(hy[jj[k], ii[k]]), is_floor))
    return cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", default="nano30_storm")
    ap.add_argument("--geo", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--cell", type=float, default=1.0)
    ap.add_argument("--step", type=float, default=0.45)
    ap.add_argument("--head", type=float, default=1.8)
    ap.add_argument("--slope", type=float, default=45.0)
    ap.add_argument("--min-tri", type=int, default=12, help="小于这个三角形数的岛丢掉")
    ap.add_argument("--merge", type=int, default=0, help="1=把可走格合并成大矩形（像原厂面图那样大三角）")
    ap.add_argument("--merge-max", type=int, default=8, help="合并时单块最大格数（8=8 米见方）")
    ap.add_argument("--merge-tol", type=float, default=0.35, help="合并允许的高差")
    ap.add_argument("--ground-only", type=int, default=1, help="1=只留地面那一层（默认）")
    ap.add_argument("--ground-tol", type=float, default=3.0, help="离地面高度 ±多少米内算地面")
    ap.add_argument("--ground-h", type=float, default=None, help="手动指定这一层的高度（不指定就用面积最大的高度）")
    ap.add_argument("--max-rise", type=float, default=0.9, help="一个格子里 4 个角高差超过它就不出（防小山包）")
    ap.add_argument("--user", default="", help="你的路点文件，只用来算覆盖率")
    args = ap.parse_args()

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    geo = args.geo or os.path.join(root, "data", "geo", "web", args.map + ".bin")
    out = args.out or os.path.join(os.path.dirname(__file__), "..", "out", args.map)
    os.makedirs(out, exist_ok=True)

    if geo.lower().endswith(".npz"):
        z = np.load(geo, allow_pickle=True)
        V, F = z["v"].astype(np.float64), z["f"].astype(np.int64)
        pos = V
        idx = F
        js = {"nverts": len(V), "ntris": len(F)}
    else:
        js, pos, idx = read_ucfg(geo)
    tri = pos[idx]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ln = np.linalg.norm(n, axis=1); ln[ln == 0] = 1
    un = n / ln[:, None]
    area = ln / 2
    ok = (area > 0.02) & (np.abs(un[:, 1]) > 0.02)
    tri, un, area = tri[ok], un[ok], area[ok]
    cs = args.cell
    cos_s = math.cos(math.radians(args.slope))
    flat = np.abs(un[:, 1]) >= cos_s
    floor_t, ceil_t, wall_t = tri[flat & (un[:, 1] > 0)], tri[flat & (un[:, 1] < 0)], tri[~flat]

    xmin, zmin = float(pos[:, 0].min()), float(pos[:, 2].min())
    xmax, zmax = float(pos[:, 0].max()), float(pos[:, 2].max())
    W = int(math.ceil((xmax - xmin) / cs)) + 1
    H = int(math.ceil((zmax - zmin) / cs)) + 1

    surf = raster(floor_t, xmin, zmin, W, H, cs, True)
    if len(ceil_t):
        for k, v in raster(ceil_t, xmin, zmin, W, H, cs, False).items():
            surf.setdefault(k, []).extend(v)
    walls = raster(wall_t, xmin, zmin, W, H, cs, False)

    wh = np.full((H, W), np.nan, dtype=np.float32)
    wall_lo = np.full((H, W), np.inf, dtype=np.float32)
    wall_hi = np.full((H, W), -np.inf, dtype=np.float32)
    for (j, i), hs in walls.items():
        wall_lo[j, i] = min(h for h, _ in hs); wall_hi[j, i] = max(h for h, _ in hs)
    CNT = {"lowceil": 0, "wall": 0}
    for (j, i), hs in surf.items():
        merged = []
        for h, isf in sorted(hs, key=lambda x: x[0]):
            if merged and abs(h - merged[-1][0]) <= 0.3:
                merged[-1] = (merged[-1][0], merged[-1][1] or isf)
            else:
                merged.append((h, isf))
        for k, (h, isf) in enumerate(merged):
            if not isf:
                continue
            nxt = merged[k + 1][0] if k + 1 < len(merged) else None
            if nxt is not None and (nxt - h) < args.head:
                CNT['lowceil'] += 1
                continue
            if wall_hi[j, i] > h + 0.1 and wall_lo[j, i] < h + args.head:
                CNT['wall'] += 1
                continue
            wh[j, i] = h
            break

    walk = ~np.isnan(wh)

    # 只留地面那一层：先找"面积最大的那个高度"当地面，再把高出/低出 tol 的面全砍掉
    if args.ground_only and walk.any():
        # 地面 = 面积最大的那个高度（整张图的街面/主层）；只留它 ±tol 内的格。
        # 楼层/屋顶比它高，会被砍掉；低洼/台阶在带内，保留。
        hv = wh[walk]
        step = 0.25
        bins = np.arange(float(hv.min()), float(hv.max()) + step, step)
        hist, edges = np.histogram(hv, bins=bins)
        ground = float(args.ground_h) if args.ground_h is not None else float(edges[int(hist.argmax())] + step * 0.5)
        band = np.abs(wh - ground) <= args.ground_tol
        print("ground %.2f m (mode) tol %.1f | keep %d/%d cells (%.0f m2)" % (
            ground, args.ground_tol, int((walk & band).sum()), int(walk.sum()),
            (walk & band).sum() * cs * cs))
        walk = walk & band
    print("grid %dx%d cell %.2f | walkable %.0f m2" % (W, H, cs, walk.sum() * cs * cs))

    # 顶点高度：四邻可走格平均
    vh = np.full((H + 1, W + 1), np.nan, dtype=np.float32)
    for j in range(H + 1):
        for i in range(W + 1):
            vals = []
            for dj in (-1, 0):
                for di in (-1, 0):
                    jj, ii = j + dj, i + di
                    if 0 <= jj < H and 0 <= ii < W and walk[jj, ii]:
                        vals.append(float(wh[jj, ii]))
            if vals:
                vals.sort()
                vh[j, i] = vals[len(vals) // 2]      # 取中位：边角不会因为一个高格起包

    # 出三角形：四个角都有高度、四格都可走
    verts = {}
    tris = []
    def vid(j, i):
        k = (j, i)
        if k not in verts:
            verts[k] = len(verts)
        return verts[k]

    if args.merge:
        used = np.zeros((H, W), dtype=bool)
        mmax = max(1, int(args.merge_max))
        for j in range(H):
            for i in range(W):
                if not walk[j, i] or used[j, i]:
                    continue
                h0 = float(wh[j, i])
                w = 1
                while i + w < W and w < mmax and walk[j, i + w] and not used[j, i + w] and abs(wh[j, i + w] - h0) <= args.merge_tol:
                    w += 1
                hh = 1
                while j + hh < H and hh < mmax:
                    ok = True
                    for k in range(w):
                        if not walk[j + hh, i + k] or used[j + hh, i + k] or abs(wh[j + hh, i + k] - h0) > args.merge_tol:
                            ok = False
                            break
                    if not ok:
                        break
                    hh += 1
                used[j:j + hh, i:i + w] = True
                a = vid(j, i); b = vid(j, i + w); c = vid(j + hh, i + w); d = vid(j + hh, i)
                vh[j, i] = h0; vh[j, i + w] = h0; vh[j + hh, i + w] = h0; vh[j + hh, i] = h0
                tris.append((a, c, b)); tris.append((a, d, c))
    for j in range(H):
        for i in range(W):
            if args.merge:
                break
            if not walk[j, i]:
                continue
            # 只要本格能站就出面（不再要求四邻都能站）：否则一个坏格会把周围 4 平米全挖掉
            hs4 = (vh[j, i], vh[j, i + 1], vh[j + 1, i + 1], vh[j + 1, i])
            if any(math.isnan(float(x)) for x in hs4):
                continue
            if max(hs4) - min(hs4) > args.max_rise:
                continue                            # 高差太大：不是平地，别出成小山包
            a, b = vid(j, i), vid(j, i + 1)
            c, d = vid(j + 1, i + 1), vid(j + 1, i)
            tris.append((a, c, b))      # 逆时针，法线朝上
            tris.append((a, d, c))

    if not tris:
        raise SystemExit("no triangles")

    V = np.zeros((len(verts), 3), dtype=np.float32)
    for (j, i), k in verts.items():
        V[k] = (xmin + i * cs, vh[j, i], zmin + j * cs)
    T = np.array(tris, dtype=np.int64)

    # 岛过滤：按共享顶点做连通
    parent = list(range(len(V)))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    def uni(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    for a, b, c in T:
        uni(a, b); uni(b, c)
    comp = np.array([find(i) for i in range(len(V))])
    tri_comp = comp[T[:, 0]]
    ids, cnt = np.unique(tri_comp, return_counts=True)
    keep = set(ids[cnt >= args.min_tri])
    mask = np.isin(tri_comp, list(keep))
    T = T[mask]
    used = np.unique(T)
    remap = -np.ones(len(V), dtype=np.int64)
    remap[used] = np.arange(len(used))
    T = remap[T]; V = V[used]
    print("islands %d -> keep %d | verts %d tris %d" % (len(ids), len(keep), len(V), len(T)))

    # 写 navmesh
    head = json.dumps({"map": args.map, "cell": cs, "verts": int(len(V)), "tris": int(len(T)),
                       "bbox": [[float(xmin), float(zmin)], [float(xmax), float(zmax)]],
                       "step": args.step, "head": args.head, "slope": args.slope},
                      separators=(",", ":")).encode("utf-8")
    nm = os.path.join(out, args.map + ".navmesh")
    with open(nm, "wb") as f:
        f.write(MAGIC); f.write(struct.pack("<IIII", VERSION, len(head), len(V), len(T))); f.write(head)
        f.write(V.astype("<f4").tobytes()); f.write(T.astype("<u4").tobytes())

    # 预览
    from PIL import Image, ImageDraw
    jj, ii = np.nonzero(walk)
    j0, j1 = max(0, jj.min() - 4), min(H, jj.max() + 4)
    i0, i1 = max(0, ii.min() - 4), min(W, ii.max() + 4)
    img = np.zeros((j1 - j0, i1 - i0, 3), dtype=np.uint8)
    sub = walk[j0:j1, i0:i1]
    h2 = wh[j0:j1, i0:i1]
    ylo, yhi = float(np.nanmin(h2)), float(np.nanmax(h2))
    t = (np.nan_to_num(h2, nan=0.0) - ylo) / max(yhi - ylo, 1e-6)
    img[..., 0] = np.where(sub, 90 + t * 120, 0).astype(np.uint8)
    img[..., 1] = np.where(sub, 110 + t * 100, 0).astype(np.uint8)
    img[..., 2] = np.where(sub, 90 + t * 60, 0).astype(np.uint8)
    im = Image.fromarray(np.flipud(img)).resize(((i1 - i0) * 2, (j1 - j0) * 2), Image.NEAREST)
    dr = ImageDraw.Draw(im)
    cover, total = 0, 0
    if args.user and os.path.isfile(args.user):
        import re
        for line in open(args.user, encoding="utf-8", errors="replace"):
            m = re.match(r"node add ([-\d.]+) ([-\d.]+) ([-\d.]+)", line.strip())
            if not m:
                continue
            x, y, z = (float(v) for v in m.groups())
            total += 1
            jf, iF = int((z - zmin) / cs), int((x - xmin) / cs)
            if 0 <= jf < H and 0 <= iF < W and walk[jf, iF] and abs(wh[jf, iF] - y) <= 1.0:
                cover += 1
            pi = int((x - xmin) / cs) - i0; pj = int((z - zmin) / cs) - j0
            if 0 <= pi < (i1 - i0) and 0 <= pj < (j1 - j0):
                dr.ellipse([pi * 2 - 3, ((j1 - j0) - pj) * 2 - 3, pi * 2 + 3, ((j1 - j0) - pj) * 2 + 3],
                           fill=(60, 120, 255))
    im.save(os.path.join(out, args.map + "_preview.png"))

    rep = ["map %s cell %.2f" % (args.map, cs),
           "walkable %.0f m2 | verts %d tris %d | islands kept %d/%d" % (
               walk.sum() * cs * cs, len(V), len(T), len(keep), len(ids))]
    if total:
        rep.append("user route nodes %d | inside mesh (+-1m) %d (%.0f%%)" % (total, cover, 100.0 * cover / total))
    open(os.path.join(out, args.map + "_report.txt"), "w", encoding="utf-8-sig").write("\n".join(rep) + "\n")
    print("\n".join(rep))
    print("wrote", nm, round(os.path.getsize(nm) / 1024.0, 1), "KB")


if __name__ == "__main__":
    main()
