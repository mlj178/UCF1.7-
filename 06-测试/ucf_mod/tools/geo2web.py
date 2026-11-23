#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""geo/<关卡>.npz  ->  geo/web/<关卡>.bin （给 navview.html 的 3D 视图用）

navedit 用的 npz 里带贴图与分块表，但贴图接得很乱；网页版只要「能看懂地形」的
灰模 + 法线 + 分块颜色，所以这里做一次离线瘦身：

  * 只丢 blocker（碰撞壳）—— 它们在游戏里本来就不画。card（巨幅装饰面）默认
    保留：运输船的船体外壳/吊臂/桅杆/围栏都被标成了 card，丢掉后船就剩一块飘着
    的平板（2026-11-23 用户反馈后改）；要老行为用 --drop-cards。
  * 同一件道具在场景里有两个 MeshRenderer：`X (1)`（独立网格 + CrossFire/Shadow
    材质，MeshCollider 用的也是这份网格）和 `X`（合并网格 "Combined Mesh" 的
    子网格，带贴图的普通材质）。合并网格那套在我们这里每个子网格都被平移过、位置
    对不上，所以用这张图的路点当尺子（navdata/dev/<图>/map.json）挑一份：运输船上
    Shadow 那套 0.99、合并网格 0.86，只留 Shadow 那套。
    代价：只在合并网格里出现的十几个小块（玻璃/灯/气罐等，约 3% 三角形）会缺。
  * 顶点颜色（npz 的 c）是 navedit 用的随机染色，噪点很大，不用；
    改用材质色 x 法线光照，所以在 JSON 头里带上每块的颜色；
  * 法线量化成 int8（x127），位置 f32，索引 u32；
  * 贴图（2026-11-23 加）：带 UV + 每块的贴图名。贴图由 tools/fetch_tex.py
    从 AssetRipper 取到 geo/tex/<关卡>/，和这里的文件名一一对应；没取到的
    分块 tex=-1，navview 退回纯色，不会报错。
  * 运输船的 Shadow 那套没有贴图（材质就叫 Shadow），按网格名找哑邻块的
    贴图补上（同一块网格导出了两遍，UV 是同一份）。

二进制布局（小端，version=2）：
    magic   'UCFG'
    u32     version = 2
    u32     jsonLen
    json    utf-8（字段见下，后面补 0 到 4 字节对齐）
    f32[n*3]   positions
    i8 [n*3]   normals (-1..1 乘 127 取整)
    f32[n*2]   uv（version 1 没有这段）
    u32[t*3]   indices（前面补 0 对齐到 4 字节）

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
VERSION = 2                          # v2 = 带 UV + 贴图表（v1 老文件仍能读）
TEXROOT = os.path.join(GEO, "tex")   # tools/fetch_tex.py 落的 PNG：<关卡>/<贴图名>
# 只丢 blocker（碰撞壳，游戏里本来就不画）。card 原来一律丢，但运输船的
# 船体外壳/吊臂/桅杆/围栏都被标成了 card —— 丢完船就剩一块飘着的平板，
# 2026-11-23 改成默认保留；确实想丢掉它们时用 --drop-cards。
SKIP_FLAGS = ("blocker",)


def _bool(x):
    return bool(x)


def load_npz(path):
    """统一成 (pos, tris, groups, normals, meta, uv)。"""
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
    uv = z["uv"] if "uv" in keys else None
    if uv is not None and len(uv) == len(pos):
        uv = np.ascontiguousarray(uv, dtype=np.float32)
    else:
        uv = None
    return pos, tri, grp, nrm, meta, uv


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



NAVDATA = os.path.join(UCF, "navdata", "dev")   # ② 开发版的图文件夹（只读，用来校准分块）


def _level_waypoints(level):
    """这张图的路点（navdata/dev/<图文件夹>/map.json 的 nodes），没有就返回 None。

    只用来判断「同一块网格被导出了两遍时，哪一遍的世界坐标是对的」，不改任何数据。
    路点是游戏运行时 A* 图里的真实坐标（出生点、人机走的路都在上面），
    比任何一次离线抓取都可信。"""
    if not os.path.isdir(NAVDATA):
        return None
    for fn in sorted(os.listdir(NAVDATA)):
        p = os.path.join(NAVDATA, fn, "map.json")
        if not os.path.isfile(p):
            continue
        try:
            with open(p, "r", encoding="utf-8") as f:
                j = json.load(f)
        except Exception:
            continue
        if ((j.get("map") or {}).get("level") or "") != level:
            continue
        pts = []
        for n in (j.get("nodes") or []):
            q = n.get("p")
            if isinstance(q, (list, tuple)) and len(q) == 3:
                try:
                    pts.append([float(q[0]), float(q[1]), float(q[2])])
                except (TypeError, ValueError):
                    pass
        if len(pts) >= 8:
            return np.asarray(pts, dtype=np.float64)
    return None


def _pass_cover(pos, tri, sel, pts, band, res=1.0):
    """这套分块在俯视图上盖住了多少比例的路点（只看高度带里的三角形）。

    只做粗判：1 m 栅格 + 点是否落在三角形投影里。够用来区分「差 15 m」这种情况。"""
    if pts is None or len(pts) == 0 or not sel.any():
        return 0.0
    P = pos[tri[sel]]
    if len(P) == 0:
        return 0.0
    cy = (P[:, 0, 1] + P[:, 1, 1] + P[:, 2, 1]) / 3.0
    P = P[(cy >= band[0]) & (cy <= band[1])]
    if len(P) == 0:
        return 0.0
    lo = pts.min(axis=0) - 25.0
    hi = pts.max(axis=0) + 25.0
    nx = int((hi[0] - lo[0]) / res) + 2
    nz = int((hi[2] - lo[2]) / res) + 2
    mask = np.zeros((nx, nz), dtype=bool)
    for t in range(len(P)):
        ax, az = P[t, 0, 0], P[t, 0, 2]
        bx, bz = P[t, 1, 0], P[t, 1, 2]
        cx, cz = P[t, 2, 0], P[t, 2, 2]
        d = (bz - cz) * (ax - cx) + (cx - bx) * (az - cz)
        if abs(d) < 1e-9:
            continue
        i0 = max(0, int((min(ax, bx, cx) - lo[0]) / res))
        i1 = min(nx - 1, int((max(ax, bx, cx) - lo[0]) / res) + 1)
        j0 = max(0, int((min(az, bz, cz) - lo[2]) / res))
        j1 = min(nz - 1, int((max(az, bz, cz) - lo[2]) / res) + 1)
        if i1 < i0 or j1 < j0:
            continue
        X = lo[0] + np.arange(i0, i1 + 1) * res
        Z = lo[2] + np.arange(j0, j1 + 1) * res
        XX, ZZ = np.meshgrid(X, Z, indexing="ij")
        w1 = ((bz - cz) * (XX - cx) + (cx - bx) * (ZZ - cz)) / d
        w2 = ((cz - az) * (XX - cx) + (ax - cx) * (ZZ - cz)) / d
        w3 = 1.0 - w1 - w2
        mask[i0:i1 + 1, j0:j1 + 1] |= (w1 >= -0.002) & (w2 >= -0.002) & (w3 >= -0.002)
    ii = np.round((pts[:, 0] - lo[0]) / res).astype(int)
    jj = np.round((pts[:, 2] - lo[2]) / res).astype(int)
    ok = (ii >= 0) & (ii < nx) & (jj >= 0) & (jj < nz)
    hit = np.zeros(len(pts), dtype=bool)
    hit[ok] = mask[ii[ok], jj[ok]]
    return float(hit.mean())


def convert(name, force=False, keep_cards=True):
    src = os.path.join(GEO, name + ".npz")
    dst = os.path.join(OUT, name + ".bin")
    if not os.path.isfile(src):
        return None
    if not force and os.path.isfile(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return {"level": name, "cached": True, "bytes": os.path.getsize(dst)}

    pos, tri, grp, nrm, meta, uv = load_npz(src)
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

    # 按分块标记过滤三角形。card（巨幅装饰面）默认保留 —— 见 SKIP_FLAGS 上面的说明；
    # 老行为（丢 card）用 --drop-cards。
    skip_flags = tuple(SKIP_FLAGS) + (() if keep_cards else ("card",))
    drop_group = set()
    for gi, ch in enumerate(chunks):
        if any(_bool(ch.get(k)) for k in skip_flags):
            drop_group.add(gi)

    # 同一块网格常常被导出两遍：一遍普通材质、一遍 Shadow 材质，两份的世界坐标
    # 大多重合，但在个别图（运输船）上差了 ~15 m —— 用这张图的路点当尺子，
    # 哪一套盖住路点就用哪一套；没有路点可对照时，沿用原来的「只留普通材质」。
    shadow_gi = [gi for gi in range(len(chunks))
                 if gi not in drop_group and _bool(chunks[gi].get("shadow"))]
    normal_gi = [gi for gi in range(len(chunks))
                 if gi not in drop_group and not _bool(chunks[gi].get("shadow"))]
    use_shadow = False
    if shadow_gi and normal_gi:
        pts = _level_waypoints(name)
        if pts is not None:
            ymed = float(np.median(pts[:, 1]))
            band = (ymed - 6.0, ymed + 6.0)
            sel_sh = np.isin(grp, shadow_gi)
            sel_ns = np.isin(grp, normal_gi)
            c_sh = _pass_cover(pos, tri, sel_sh, pts, band)
            c_ns = _pass_cover(pos, tri, sel_ns, pts, band)
            n_sh = int(sel_sh.sum())
            n_ns = int(sel_ns.sum())
            if c_sh > c_ns + 0.05 and n_sh >= 0.6 * max(1, n_ns):
                use_shadow = True
            print("  %s: 分块对照 路点覆盖 shadow %.2f (%d 三角) / 普通 %.2f (%d 三角) -> %s" % (
                  name, c_sh, n_sh, c_ns, n_ns,
                  "shadow 那套位置对，只留它" if use_shadow else "两套基本重合，都留"))
    if use_shadow:
        # 只有「普通那套明显错位」时才整批丢掉它；两套重合的图保持原样（都画），
        # 重合的部分由 z-buffer 处理，不会互相遮挡。
        for gi in normal_gi:
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
    uv2 = uv[used] if uv is not None else None
    tri2 = remap[tri2]

    # 重组分块表（按原始顺序，只保留还有三角形的块）
    order = np.argsort(grp2, kind="stable")
    tri2 = tri2[order]
    grp2 = grp2[order]
    counts = {}
    for g in grp2.tolist():
        counts[g] = counts.get(g, 0) + 1
    # 贴图：先看这块自己的材质；运输船的 Shadow 那套材质没有贴图，
    # 就借同名哑邻块（"X (1)" -> "X"）的 —— 同一块网格导出了两遍，UV 是同一份。
    # 最后还要确认 geo/tex/<关卡>/ 里真有这个 png，没有就 tex=-1（退回纯色）。
    by_name = {}
    for ch in chunks:
        nm = str(ch.get("name") or "")
        if nm and nm not in by_name:
            by_name[nm] = ch
    mat_by_tex = {}
    for m in mats:
        fn = str(m.get("tex") or "").strip()
        if fn and fn not in mat_by_tex:
            mat_by_tex[fn] = m

    def tex_of(ch):
        want = str(ch.get("tex") or "").strip()
        if want:
            return want
        nm = str(ch.get("name") or "")
        if nm.endswith(" (1)"):
            sib = by_name.get(nm[:-4])
            if sib:
                return str(sib.get("tex") or "").strip()
        return ""

    tex_files = []
    tex_index = {}
    out_chunks = []
    cursor = 0
    for gi in sorted(counts):
        ch = chunks[gi] if gi < len(chunks) else {}
        want = tex_of(ch)
        ti = -1
        if want and os.path.isfile(os.path.join(TEXROOT, name, want)):
            if want not in tex_index:
                mi = mat_by_tex.get(want) or {}
                tex_index[want] = len(tex_files)
                tex_files.append({
                    "file": want,
                    "w": int(mi.get("tex_w") or 0),
                    "h": int(mi.get("tex_h") or 0),
                })
            ti = tex_index[want]
        out_chunks.append({
            "name": str(ch.get("name") or "")[:80],
            "start": int(cursor),
            "count": int(counts[gi]),
            "color": [round(v, 3) for v in rgb_of(ch)],
            "tex": ti,
            "alpha": 1 if _bool(ch.get("transparent")) else 0,
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
        "ver": VERSION,
        "nverts": int(len(pos2)),
        "ntris": int(len(tri2)),
        "bbox": [[round(v, 3) for v in lo], [round(v, 3) for v in hi]],
        "ambient": ambient,
        "tex": tex_files,
        "chunks": out_chunks,
    }
    js = json.dumps(header, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    nrm_i8 = np.clip(np.round(nrm2 * 127.0), -127, 127).astype(np.int8)

    os.makedirs(OUT, exist_ok=True)
    tmp = dst + ".tmp"
    pos_bytes = np.ascontiguousarray(pos2, dtype="<f4").tobytes()
    nrm_bytes = np.ascontiguousarray(nrm_i8, dtype=np.int8).tobytes()
    if uv2 is None:
        uv2 = np.zeros((len(pos2), 2), dtype=np.float32)
    uv_bytes = np.ascontiguousarray(uv2, dtype="<f4").tobytes()
    idx_bytes = np.ascontiguousarray(tri2, dtype="<u4").tobytes()
    pad_json = (4 - ((12 + len(js)) % 4)) % 4      # JSON 头之后也要对齐（Float32Array 要求）
    head_len = 12 + len(js) + pad_json + len(pos_bytes) + len(nrm_bytes)
    pad_n = (4 - (head_len % 4)) % 4               # UV 是 f32，从 4 字节边界开始
    head2 = head_len + pad_n + len(uv_bytes)
    pad = (4 - (head2 % 4)) % 4                    # 索引是 u32，同样要 4 字节对齐
    with open(tmp, "wb") as f:
        f.write(MAGIC)
        f.write(struct.pack("<II", VERSION, len(js)))
        f.write(js)
        if pad_json:
            f.write(b"\x00" * pad_json)
        f.write(pos_bytes)
        f.write(nrm_bytes)
        if pad_n:
            f.write(b"\x00" * pad_n)
        f.write(uv_bytes)
        if pad:
            f.write(b"\x00" * pad)
        f.write(idx_bytes)
    os.replace(tmp, dst)
    return {
        "level": name,
        "nverts": int(len(pos2)),
        "ntris": int(len(tri2)),
        "chunks": len(out_chunks),
        "tex": len(tex_files),
        "dropped_tris": int(len(tri) - len(tri2)),
        "bytes": os.path.getsize(dst),
    }


def main():
    ap = argparse.ArgumentParser(description="npz 关卡几何 -> 网页可读的 .bin")
    ap.add_argument("levels", nargs="*", help="只转这些关卡名（默认全部）")
    ap.add_argument("--force", action="store_true", help="源文件没变也重转")
    ap.add_argument("--drop-cards", action="store_true",
                    help="丢掉 card（巨幅装饰面）分块。默认保留：运输船的船体外壳/桅杆也被标成 card")
    args = ap.parse_args()

    if not os.path.isdir(GEO):
        sys.exit("找不到 geo 目录: " + GEO)
    names = args.levels or sorted(fn[:-4] for fn in os.listdir(GEO) if fn.lower().endswith(".npz"))
    if not names:
        sys.exit("geo 目录里没有 .npz（先跑 navedit 提取一次几何，或确认路径）")
    total = 0
    for name in names:
        r = convert(name, force=args.force, keep_cards=not args.drop_cards)
        if not r:
            print("跳过 %s（源文件不存在或没有可用三角形）" % name)
            continue
        if r.get("cached"):
            print("%-12s 已是最新  %6.2f MB" % (name, r["bytes"] / 1048576.0))
        else:
            total += r["bytes"]
            print("%-12s 顶点 %7d  三角 %7d  分块 %3d  贴图 %3d  丢弃 %6d   %6.2f MB" % (
                name, r["nverts"], r["ntris"], r["chunks"], r.get("tex", 0),
                r["dropped_tris"], r["bytes"] / 1048576.0))
    print("完成，输出目录 %s" % OUT)


if __name__ == "__main__":
    main()