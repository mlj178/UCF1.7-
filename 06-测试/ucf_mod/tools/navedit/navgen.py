"""离线路点重建：用提取出来的地图网格，模拟游戏里的路点扫描。

这不是"导出的游戏数据"，而是按同样参数（4 m 网格、向下射线、4.6 m 连接）
在地图上重算一遍得到的**草稿**，文件名带 _sim 后缀，导出字段 source=offline-sim。
真数据只能在游戏里由 navfix 生成后按 Ctrl+E 导出。
"""
import numpy as np

WALK_NY = 0.55        # 法线 y 分量大于它才算可站立的"地面"
LAYER_GAP = 0.55      # 同一点位两层之间至少差这么多
MAX_LAYERS = 4        # 每个网格点最多保留几层（游戏是 5 层射线）
WALL_NY = 0.55        # 法线 y 分量小于它算"墙"


def _pai_2d(px, pz, ax, az, bx, bz, cx, cz):
    d = (bz - cz) * (ax - cx) + (cx - bx) * (az - cz)
    if abs(d) < 1e-12:
        return None
    a = ((bz - cz) * (px - cx) + (cx - bx) * (pz - cz)) / d
    b = ((cz - az) * (px - cx) + (ax - cx) * (pz - cz)) / d
    return a, b, 1.0 - a - b


def generate(geo, cell=4.0, connect=4.6, max_dy=1.6, los=True, progress=None):
    pos = geo.positions
    tri = geo.indices.reshape(-1, 3)
    n = len(tri)
    if n == 0:
        return np.zeros((0, 3)), np.zeros((0, 2), dtype=np.int64), {}

    a = pos[tri[:, 0]]
    b = pos[tri[:, 1]]
    c = pos[tri[:, 2]]
    fn = np.cross(b - a, c - a)
    ln = np.linalg.norm(fn, axis=1)
    ln[ln < 1e-9] = 1e-9
    ny = np.abs(fn[:, 1] / ln)

    walkable = ny >= WALK_NY
    walls = ~walkable
    if progress:
        progress("分类三角面 %d（可站立 %d）" % (n, int(walkable.sum())))

    # ---- 1) 每个网格中心向下打"射线"，收集所有命中高度 ----
    cells = {}
    idxs = np.nonzero(walkable)[0]
    for k in idxs:
        i0, i1, i2 = tri[k]
        p0, p1, p2 = pos[i0], pos[i1], pos[i2]
        x0 = min(p0[0], p1[0], p2[0]); x3 = max(p0[0], p1[0], p2[0])
        z0 = min(p0[2], p1[2], p2[2]); z3 = max(p0[2], p1[2], p2[2])
        cx0 = int(np.floor(x0 / cell)); cx1 = int(np.floor(x3 / cell))
        cz0 = int(np.floor(z0 / cell)); cz1 = int(np.floor(z3 / cell))
        if (cx1 - cx0) > 60 or (cz1 - cz0) > 60:
            continue
        for cx in range(cx0, cx1 + 1):
            for cz in range(cz0, cz1 + 1):
                px = (cx + 0.5) * cell
                pz = (cz + 0.5) * cell
                r = _pai_2d(px, pz, p0[0], p0[2], p1[0], p1[2], p2[0], p2[2])
                if r is None:
                    continue
                u, v, w = r
                if u < -0.001 or v < -0.001 or w < -0.001:
                    continue
                y = u * p0[1] + v * p1[1] + w * p2[1]
                cells.setdefault((cx, cz), []).append(float(y))

    points = []
    for key, ys in cells.items():
        ys.sort(reverse=True)
        kept = []
        for y in ys:
            if all(abs(y - o) > LAYER_GAP for o in kept):
                kept.append(y)
            if len(kept) >= MAX_LAYERS:
                break
        for y in kept:
            points.append((key[0] * cell + cell * 0.5, y + 0.06, key[1] * cell + cell * 0.5))
    points = np.array(points, dtype=np.float64).reshape(-1, 3)
    if progress:
        progress("生成候选路点 %d" % len(points))

    # ---- 2) 连边：4.6 m 内、高度差小、视线不穿墙 ----
    wall_cells = {}
    widx = np.nonzero(walls)[0]
    for k in widx:
        i0, i1, i2 = tri[k]
        p0, p1, p2 = pos[i0], pos[i1], pos[i2]
        x0 = min(p0[0], p1[0], p2[0]); x3 = max(p0[0], p1[0], p2[0])
        z0 = min(p0[2], p1[2], p2[2]); z3 = max(p0[2], p1[2], p2[2])
        cx0 = int(np.floor(x0 / cell)); cx1 = int(np.floor(x3 / cell))
        cz0 = int(np.floor(z0 / cell)); cz1 = int(np.floor(z3 / cell))
        if (cx1 - cx0) > 12 or (cz1 - cz0) > 12:
            continue
        ylo = float(min(p0[1], p1[1], p2[1])); yhi = float(max(p0[1], p1[1], p2[1]))
        for cx in range(cx0, cx1 + 1):
            for cz in range(cz0, cz1 + 1):
                wall_cells.setdefault((cx, cz), []).append((ylo, yhi))

    def blocked(p, q):
        if not los:
            return False
        for t in (0.25, 0.5, 0.75):
            x = p[0] + (q[0] - p[0]) * t
            y = p[1] + (q[1] - p[1]) * t
            z = p[2] + (q[2] - p[2]) * t
            key = (int(np.floor(x / cell)), int(np.floor(z / cell)))
            for (ylo, yhi) in wall_cells.get(key, ()):
                if ylo - 0.35 <= y <= yhi + 0.35:
                    return True
        return False

    by_cell = {}
    for i, p in enumerate(points):
        by_cell.setdefault((int(np.floor(p[0] / cell)), int(np.floor(p[2] / cell))), []).append(i)

    edges = []
    r2 = connect * connect
    reach = int(np.ceil(connect / cell)) + 1
    for (cx, cz), ids in by_cell.items():
        cand = []
        for dx in range(-reach, reach + 1):
            for dz in range(-reach, reach + 1):
                cand.extend(by_cell.get((cx + dx, cz + dz), ()))
        for i in ids:
            pi = points[i]
            for j in cand:
                if j <= i:
                    continue
                pj = points[j]
                dx = pj[0] - pi[0]; dy = pj[1] - pi[1]; dz = pj[2] - pi[2]
                if dx * dx + dz * dz > r2:
                    continue
                if abs(dy) > max_dy:
                    continue
                if blocked(pi, pj):
                    continue
                edges.append((i, j))
    if progress:
        progress("连边 %d" % len(edges))
    return points, np.array(edges, dtype=np.int64).reshape(-1, 2), {
        "candidates": len(points), "walkable_tris": int(walkable.sum()), "tris": int(n)}


def stats(nodes, edges):
    deg = np.zeros(len(nodes), dtype=np.int32)
    if len(edges):
        np.add.at(deg, edges[:, 0], 1)
        np.add.at(deg, edges[:, 1], 1)
    iso = int((deg == 0).sum())
    # 连通分量
    parent = list(range(len(nodes)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(int(a)), find(int(b))
        if ra != rb:
            parent[ra] = rb
    comps = len(set(find(i) for i in range(len(nodes))))
    from collections import Counter
    sizes = Counter(find(i) for i in range(len(nodes)))
    return {"nodes": len(nodes), "edges": len(edges), "isolated": iso,
            "components": comps, "largest": max(sizes.values()) if sizes else 0}
