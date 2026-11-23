#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AssetRipper 导出的 Unity 工程 -> geo/web/<level>.bin（UCFG v2）

数据来源（全部是 AssetRipper 的持久化导出，不靠猜）：
  * 场景：<project>/Assets/Scenes/<scene>.unity
      - MeshRenderer.m_StaticBatchInfo.firstSubMesh/subMeshCount
      - MeshRenderer.m_Materials -> 材质资产
      - GameObject.m_Name
  * 合并网格：<project>/Assets/Mesh/Combined Mesh (root_ scene) 2.asset
      - m_VertexData._typelessdata：位置（float32x3，stride 32，offset 0）
      - UV0（float16x2，offset 28）
      - m_IndexBuffer（uint16）+ m_SubMeshes（firstByte/indexCount/baseVertex）
      - 顶点已经是世界坐标（TransportShip 的 180° Y 旋转已烘进去）
  * 材质：<project>/Assets/Material/*.mat
      - _MainTex / _BaseMap 的贴图 GUID、_Color/_BaseColor
  * 贴图：<project>/Assets/**/*.png + .meta 里的 GUID

产出：
  geo/web/<level>.bin       UCFG v2（位置/法线/UV/索引 + 每块贴图号）
  geo/tex/<level>/*.png     本图用到的贴图（从导出工程复制）

用法：
  python 06-测试/ucf_mod/docs/guide/地图3D资源导出/代码/scene_export2web.py --scene level1 --level level1
  python 06-测试/ucf_mod/docs/guide/地图3D资源导出/代码/scene_export2web.py --scene level2 --level level2 --project <导出工程目录>
"""
import argparse
import glob
import hashlib
import json
import os
import re
import shutil
import struct
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def _find_ucf(start):
    """从脚本位置向上找 ucf_mod 根目录（同时有 geo/ 和 tools/）。"""
    cur = start
    for _ in range(10):
        if os.path.isdir(os.path.join(cur, "geo")) and os.path.isdir(os.path.join(cur, "tools")):
            return cur
        nxt = os.path.dirname(cur)
        if nxt == cur:
            break
        cur = nxt
    return os.path.abspath(os.path.join(start, "..", "..", ".."))


UCF = _find_ucf(HERE)
REPO = os.path.dirname(os.path.dirname(UCF))          # d:\trae_project\ucf1.7-modifier
GEO = os.path.join(UCF, "geo")
OUT = os.path.join(GEO, "web")
TEXROOT = os.path.join(GEO, "tex")
DEFAULT_PROJECT = os.path.join(REPO, "00-游戏逆向分析-相关信息", "地图3D资源导出",
                               "AssetRipper工程", "ExportedProject")
MAGIC = b"UCFG"
VERSION = 2


def _read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _guid_map(project):
    """扫 Assets 下所有 .meta，建 guid -> 资产路径。缓存放临时目录，不落资源库。"""
    cache = os.path.join(tempfile.gettempdir(), "ucf_scene_export_guid_map.json")
    if os.path.isfile(cache):
        try:
            j = json.load(open(cache, "r", encoding="utf-8"))
            if j.get("project") == project and j.get("map"):
                return j["map"]
        except Exception:
            pass
    out = {}
    for meta in glob.glob(os.path.join(project, "Assets", "**", "*.meta"), recursive=True):
        try:
            head = open(meta, "r", encoding="utf-8", errors="replace").read(400)
            m = re.search(r"guid: ([0-9a-f]+)", head)
            if m:
                out[m.group(1)] = meta[:-5]
        except Exception:
            continue
    try:
        json.dump({"project": project, "map": out}, open(cache, "w", encoding="utf-8"),
                  ensure_ascii=False)
    except Exception:
        pass
    return out


def _scene_objects(scene_text):
    """把 Unity YAML 拆成 {fileID: (classID, body)}。"""
    blocks = re.split(r"\n--- !u!(\d+) &(\d+)\n", scene_text)
    objs = {}
    for i in range(1, len(blocks), 3):
        objs[int(blocks[i + 1])] = (int(blocks[i]), blocks[i + 2])
    return objs


def _material_info(mat_path, guid2path):
    text = _read(mat_path)
    name = ""
    m = re.search(r"\n  m_Name: (.*)", text)
    if m:
        name = m.group(1).strip().strip("'")
    shader = ""
    m = re.search(r"m_Shader: \{fileID: \d+, guid: ([0-9a-f]+)", text)
    if m:
        shader = os.path.basename(guid2path.get(m.group(1), ""))
    tex = ""
    for key in ("_MainTex", "_BaseMap"):
        m = re.search(key + r":\s*\n\s*m_Texture: \{fileID: \d+, guid: ([0-9a-f]+)", text)
        if m and m.group(1) in guid2path and guid2path[m.group(1)].lower().endswith((".png", ".jpg", ".jpeg", ".tga")):
            tex = guid2path[m.group(1)]
            break
    color = (1.0, 1.0, 1.0, 1.0)
    mc = re.search(r"m_Colors:\s*\n((?:\s+\w+: \{r: [^}]+\}\s*\n?)+)", text)
    if mc:
        props = {}
        for nm, r, g, b, a in re.findall(
                r"(\w+): \{r: ([-\d.eE+]+), g: ([-\d.eE+]+), b: ([-\d.eE+]+), a: ([-\d.eE+]+)\}",
                mc.group(1)):
            props[nm] = (r, g, b, a)
        key = "_BaseColor" if "_BaseColor" in props else ("_Color" if "_Color" in props else None)
        if key:
            try:
                color = tuple(float(x) for x in props[key])
            except Exception:
                pass
    transparent = False
    m = re.search(r"_AlphaClip: (\d+)", text)
    if m and m.group(1) == "1":
        transparent = True
    m = re.search(r"_Mode: (\d+)", text)
    if m and m.group(1) not in ("0",):
        transparent = True
    return {"name": name, "shader": shader, "tex": tex, "color": color, "transparent": transparent}


def _decode_mesh(mesh_path):
    """解析 AssetRipper 导出的网格（合并网格 / 单体网格通用）。返回 pos/uv/indices/submeshes。"""
    text = _read(mesh_path)
    m_vc = re.search(r"m_VertexCount: (\d+)", text)
    m_ds = re.search(r"m_DataSize: (\d+)", text)
    if not m_vc or not m_ds:
        raise RuntimeError("缺少 m_VertexCount/m_DataSize")
    vc = int(m_vc.group(1))
    ds = int(m_ds.group(1))
    if vc <= 0 or ds <= 0 or ds % vc:
        raise RuntimeError("顶点数据不完整（vc=%d ds=%d）" % (vc, ds))
    stride = ds // vc
    if stride < 12 or stride % 4:
        raise RuntimeError("顶点 stride 异常：%d" % stride)
    m_hex = re.search(r"_typelessdata: ([0-9a-fA-F]+)", text)
    if not m_hex:
        raise RuntimeError("没有 _typelessdata")
    raw = bytes.fromhex(m_hex.group(1))
    if len(raw) < ds:
        raw = raw + b"\x00" * (ds - len(raw))
    raw = raw[:ds]
    pos = np.frombuffer(raw, dtype="<f4").reshape(-1, stride // 4)[:, :3].astype(np.float32)
    if len(pos) != vc:
        raise RuntimeError("顶点数不符：%d != %d" % (len(pos), vc))
    # UV0：在 m_Channels 里找 dimension=2 的通道；format 0=Float32，1=Float16
    uv = np.zeros((len(pos), 2), dtype=np.float32)
    uv_off = None
    uv_fmt = None
    chans = re.findall(r"- stream: \d+\s*\n\s*offset: (\d+)\s*\n\s*format: (\d+)\s*\n\s*dimension: (\d+)", text)
    for off, fmt, dim in chans:
        if int(dim) == 2 and int(off) >= 12:
            uv_off = int(off)
            uv_fmt = int(fmt)
            break
    if uv_off is not None:
        try:
            if uv_fmt == 0 and uv_off + 8 <= stride:
                arr = np.frombuffer(raw, dtype="<f4").reshape(-1, stride // 4)
                uv = arr[:len(pos), uv_off // 4:uv_off // 4 + 2].astype(np.float32)
            elif uv_fmt == 1 and uv_off + 4 <= stride:
                arr = np.frombuffer(raw, dtype="<f2").reshape(-1, stride // 2)
                uv = arr[:len(pos), uv_off // 2:uv_off // 2 + 2].astype(np.float32)
            if not np.isfinite(uv).all():
                uv = np.nan_to_num(uv, nan=0.0, posinf=0.0, neginf=0.0)
        except Exception:
            uv = np.zeros((len(pos), 2), dtype=np.float32)
    # 个别网格的 UV 是未初始化垃圾值（例如 level2 的 tanklorry/bl_a）；用 XZ 平面投影兜底
    if len(pos) and (not np.isfinite(uv).all() or float(np.abs(uv).max()) > 1000.0):
        mn = pos.min(0)
        ext = np.maximum(pos.max(0) - mn, 1e-6)
        uv = np.zeros((len(pos), 2), dtype=np.float32)
        uv[:, 0] = (pos[:, 0] - mn[0]) / ext[0]
        uv[:, 1] = (pos[:, 2] - mn[2]) / ext[2]
    # 索引：m_IndexFormat 0 = uint16，1 = uint32
    idx_fmt = int(re.search(r"m_IndexFormat: (\d+)", text).group(1)) if "m_IndexFormat:" in text else 0
    m_idx = re.search(r"m_IndexBuffer: ([0-9a-fA-F ]+)", text)
    if m_idx and m_idx.group(1).strip():
        idx = np.frombuffer(bytes.fromhex(m_idx.group(1).replace(" ", "")),
                            dtype="<u2" if idx_fmt == 0 else "<u4")
    else:
        idx = np.zeros(0, dtype=np.uint16 if idx_fmt == 0 else np.uint32)
    subs = []
    for m in re.finditer(r"firstByte: (\d+)\s*\n\s*indexCount: (\d+)\s*\n\s*topology: 0\s*\n\s*baseVertex: (\d+)", text):
        subs.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    return pos, uv, idx, subs


def _qmat(q):
    x, y, z, w = q
    return np.array([
        [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
        [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
        [2 * (x * z - y * w), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]], dtype=np.float64)


def _local_matrix(body):
    def vec(key):
        m = re.search(key + r": \{x: ([-\d.eE+]+), y: ([-\d.eE+]+), z: ([-\d.eE+]+)(?:, w: ([-\d.eE+]+))?\}", body)
        return [float(v) for v in m.groups() if v is not None] if m else None
    p = vec("m_LocalPosition") or [0, 0, 0]
    q = vec("m_LocalRotation") or [0, 0, 0, 1]
    s = vec("m_LocalScale") or [1, 1, 1]
    M = np.eye(4)
    M[:3, :3] = _qmat(q) * np.array(s)[None, :]
    M[:3, 3] = p
    return M


def _triangles(idx, first_byte, index_count, base_vertex):
    start = first_byte // idx.itemsize
    tri = idx[start:start + index_count].astype(np.int64)
    if len(tri) % 3:
        tri = tri[:len(tri) // 3 * 3]
    tri = tri + base_vertex
    return tri.reshape(-1, 3)


def _vertex_normals(pos, tris):
    vn = np.zeros((len(pos), 3), dtype=np.float64)
    a = pos[tris[:, 0]].astype(np.float64)
    b = pos[tris[:, 1]].astype(np.float64)
    c = pos[tris[:, 2]].astype(np.float64)
    fn = np.cross(b - a, c - a)
    ln = np.linalg.norm(fn, axis=1)
    ln[ln == 0] = 1.0
    fn /= ln[:, None]
    for k in range(3):
        np.add.at(vn, tris[:, k], fn)
    ln = np.linalg.norm(vn, axis=1)
    ln[ln == 0] = 1.0
    return (vn / ln[:, None]).astype(np.float32)


def convert(project, scene, level, keep_shadow=False):
    guid2path = _guid_map(project)
    scene_path = os.path.join(project, "Assets", "Scenes", scene + ".unity")
    if not os.path.isfile(scene_path):
        raise SystemExit("找不到场景：" + scene_path)
    objs = _scene_objects(_read(scene_path))

    go_name = {}
    for oid, (cls, body) in objs.items():
        if cls == 1:
            m = re.search(r"\n  m_Name: (.*)", body)
            if m:
                go_name[oid] = m.group(1).strip().strip("'")

    # ---- 变换层级（单体网格要用） ----
    tr_body, tr_go, tr_father = {}, {}, {}
    for oid, (cls, body) in objs.items():
        if cls != 4:
            continue
        tr_body[oid] = body
        g = re.search(r"m_GameObject: \{fileID: (\d+)\}", body)
        if g:
            tr_go[int(g.group(1))] = oid
        f = re.search(r"m_Father: \{fileID: (\d+)\}", body)
        tr_father[oid] = int(f.group(1)) if f else 0
    wcache = {}

    def world_tid(tid, dep=0):
        if tid in wcache:
            return wcache[tid]
        M = _local_matrix(tr_body[tid])
        f = tr_father.get(tid, 0)
        if f and f in tr_body and dep < 64:
            M = world_tid(f, dep + 1) @ M
        wcache[tid] = M
        return M

    def world_of_go(gid):
        tid = tr_go.get(gid)
        return world_tid(tid) if tid in tr_body else np.eye(4)

    mf_by_go = {}
    for oid, (cls, body) in objs.items():
        if cls != 33:
            continue
        g = re.search(r"m_GameObject: \{fileID: (\d+)\}", body)
        if not g:
            continue
        mm = re.search(r"m_Mesh: \{fileID: \d+, guid: ([0-9a-f]+)", body)
        mf_by_go[int(g.group(1))] = guid2path.get(mm.group(1)) if mm else None

    renderers = []
    mesh_path = None
    for oid, (cls, body) in objs.items():
        if cls != 23:
            continue
        g = re.search(r"m_GameObject: \{fileID: (\d+)\}", body)
        if not g:
            continue
        gid = int(g.group(1))
        en = re.search(r"m_Enabled: (\d+)", body)
        if en and en.group(1) != "1":
            continue
        sbi = re.search(r"m_StaticBatchInfo:\s*\n\s*firstSubMesh: (\d+)\s*\n\s*subMeshCount: (\d+)", body)
        first, count = (int(sbi.group(1)), int(sbi.group(2))) if sbi else (0, 0)
        mm = re.search(r"m_Materials:\s*\n((?:\s*- \{fileID: \d+, guid: [0-9a-f]+, type: \d+\}\s*\n?)+)", body)
        guids = re.findall(r"guid: ([0-9a-f]+)", mm.group(1)) if mm else []
        mats = []
        for gu in guids:
            mp = guid2path.get(gu)
            if mp and mp.lower().endswith(".mat"):
                mats.append(_material_info(mp, guid2path))
            else:
                mats.append({"name": "", "shader": "", "tex": "", "color": (1, 1, 1, 1), "transparent": False})
        mf = mf_by_go.get(gid)
        if mf and "Combined Mesh" in mf:
            mesh_path = mf
        renderers.append({
            "gid": gid, "name": go_name.get(gid, "?"), "first": first, "count": count,
            "mats": mats, "mesh": mf,
        })

    if mesh_path is None:
        # 其他地图通常是单体网格（没有静态合批），不需要合并网格
        pos = np.zeros((0, 3), dtype=np.float32)
        uv = np.zeros((0, 2), dtype=np.float32)
        idx = np.zeros(0, dtype=np.int64)
        subs = []
        print("没有静态合批网格，按单体网格导出")
    else:
        pos, uv, idx, subs = _decode_mesh(mesh_path)
        print("网格：%s" % os.path.basename(mesh_path))
        print("顶点 %d  索引 %d  子网格 %d" % (len(pos), len(idx), len(subs)))

    # 输出贴图目录
    texdir = os.path.join(TEXROOT, level)
    os.makedirs(texdir, exist_ok=True)
    tex_files = []
    tex_index = {}
    tex_source = {}
    chunks = []

    pool_pos = []
    pool_uv = []
    pool_nrm = []
    pool_tri = []
    cursor = 0
    skipped = []

    def tex_of(mat):
        tfile = mat.get("tex") or ""
        if not tfile or not os.path.isfile(tfile):
            return -1
        fname = os.path.basename(tfile)
        if fname in tex_index and tex_source.get(fname) != tfile:
            stem, ext = os.path.splitext(fname)
            fname = "%s_%s%s" % (stem, hashlib.md5(tfile.encode("utf-8")).hexdigest()[:6], ext)
        if fname not in tex_index:
            dst = os.path.join(texdir, fname)
            shutil.copyfile(tfile, dst)
            from PIL import Image
            im = Image.open(dst)
            tex_index[fname] = len(tex_files)
            tex_source[fname] = tfile
            tex_files.append({"file": fname, "w": im.width, "h": im.height})
        return tex_index[fname]

    def append_chunk(name, mat, pos, uv, tris):
        nonlocal cursor
        if len(tris) == 0:
            return
        a = pos[tris[:, 0]]
        b = pos[tris[:, 1]]
        c = pos[tris[:, 2]]
        area = np.linalg.norm(np.cross(b - a, c - a), axis=1)
        tris = tris[area > 1e-9]
        if len(tris) == 0:
            return
        used = np.unique(tris.ravel())
        remap = np.full(len(pos), -1, dtype=np.int64)
        remap[used] = np.arange(len(used))
        vpos = pos[used].astype(np.float32)
        vuv = uv[used].astype(np.float32)
        local_tris = remap[tris]
        vn = _vertex_normals(vpos, local_tris)
        base = cursor
        pool_pos.append(vpos)
        pool_uv.append(vuv)
        pool_nrm.append(vn)
        pool_tri.append(local_tris + base)
        cursor += len(vpos)
        col = mat.get("color") or (1, 1, 1, 1)
        chunks.append({
            "name": name[:80],
            "start": 0,   # 后面统一重算
            "count": int(len(local_tris)),
            "color": [round(float(max(0.0, min(1.0, col[0]))), 3),
                      round(float(max(0.0, min(1.0, col[1]))), 3),
                      round(float(max(0.0, min(1.0, col[2]))), 3)],
            "tex": tex_of(mat),
            "alpha": 1 if mat.get("transparent") else 0,
        })

    # 1) 合批可见物体：直接取合并网格的 world-space 子网格
    for r in renderers:
        if r["count"] <= 0 or not subs:
            continue
        for k in range(r["count"]):
            si = r["first"] + k
            if si >= len(subs):
                skipped.append((r["name"], si, "submesh out of range"))
                continue
            mat = r["mats"][k] if k < len(r["mats"]) else (r["mats"][0] if r["mats"] else None)
            if not mat:
                skipped.append((r["name"], si, "no material"))
                continue
            if "shadow" in (mat.get("name") or "").lower() or "shadow" in (mat.get("shader") or "").lower():
                skipped.append((r["name"], si, "shadow material"))
                continue
            fb, ic, bv = subs[si]
            append_chunk(r["name"], mat, pos, uv, _triangles(idx, fb, ic, bv))

    # 2) 非合批可见物体（卡板/围栏/水等）：单体网格 × 世界变换
    for r in renderers:
        if r["count"] > 0:
            continue
        mat = r["mats"][0] if r["mats"] else None
        if not mat:
            continue
        mn = (mat.get("name") or "").lower()
        if "shadow" in mn or mn.startswith("alpha") or mn == "" or "water" in mn:
            skipped.append((r["name"], 0, "non-visible material: " + (mat.get("name") or "")))
            continue
        mp = r["mesh"]
        if not mp or not os.path.isfile(mp):
            # Unity 内置 Quad：材质有贴图时补一个 1x1 面片；Lit 灯片/Shadow 跳过
            if r["name"].lower().startswith("quad") and mat.get("tex"):
                mpos = np.array([[-0.5, -0.5, 0], [0.5, -0.5, 0],
                                 [0.5, 0.5, 0], [-0.5, 0.5, 0]], dtype=np.float32)
                muv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32)
                midx = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint16)
                msubs = [(0, 6, 0)]
            else:
                skipped.append((r["name"], 0, "mesh missing"))
                continue
        else:
            try:
                mpos, muv, midx, msubs = _decode_mesh(mp)
            except Exception as exc:
                skipped.append((r["name"], 0, "mesh decode: %s" % exc))
                continue
        M = world_of_go(r["gid"])
        wpos = (np.hstack([mpos, np.ones((len(mpos), 1))]) @ M.T)[:, :3]
        for si, (fb, ic, bv) in enumerate(msubs):
            m2 = r["mats"][si] if si < len(r["mats"]) else mat
            append_chunk(r["name"], m2, wpos, muv, _triangles(midx, fb, ic, bv))

    if not chunks:
        raise SystemExit("没有可导出的分块")

    # 重新计算 chunk start（按池内三角形累计）
    tri_start = 0
    for ch in chunks:
        ch["start"] = tri_start
        tri_start += ch["count"]

    pos_all = np.vstack(pool_pos)
    uv_all = np.vstack(pool_uv)
    nrm_all = np.vstack(pool_nrm)
    tri_all = np.vstack(pool_tri)

    lo = pos_all.min(0).astype(float).tolist()
    hi = pos_all.max(0).astype(float).tolist()
    header = {
        "level": level,
        "ver": VERSION,
        "nverts": int(len(pos_all)),
        "ntris": int(len(tri_all)),
        "bbox": [[round(v, 3) for v in lo], [round(v, 3) for v in hi]],
        "ambient": [0.66, 0.68, 0.70],
        "tex": tex_files,
        "chunks": chunks,
    }
    js = json.dumps(header, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    nrm_i8 = np.clip(np.round(nrm_all * 127.0), -127, 127).astype(np.int8)

    dst = os.path.join(OUT, level + ".bin")
    os.makedirs(OUT, exist_ok=True)
    tmp = dst + ".tmp"
    pos_bytes = np.ascontiguousarray(pos_all, dtype="<f4").tobytes()
    nrm_bytes = np.ascontiguousarray(nrm_i8, dtype=np.int8).tobytes()
    uv_bytes = np.ascontiguousarray(uv_all, dtype="<f4").tobytes()
    idx_bytes = np.ascontiguousarray(tri_all, dtype="<u4").tobytes()
    pad_json = (4 - ((12 + len(js)) % 4)) % 4
    head_len = 12 + len(js) + pad_json + len(pos_bytes) + len(nrm_bytes)
    pad_n = (4 - (head_len % 4)) % 4
    head2 = head_len + pad_n + len(uv_bytes)
    pad = (4 - (head2 % 4)) % 4
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

    print("输出：%s" % dst)
    print("  顶点 %d  三角 %d  分块 %d  贴图 %d  %.2f MB" % (
        len(pos_all), len(tri_all), len(chunks), len(tex_files), os.path.getsize(dst) / 1048576.0))
    if skipped:
        print("  跳过 %d 块：" % len(skipped))
        for s in skipped[:8]:
            print("    %-30s sub%-3d %s" % (s[0][:30], s[1], s[2]))
    return dst


def main():
    ap = argparse.ArgumentParser(description="AssetRipper 导出工程 -> 工作台 UCFG bin")
    ap.add_argument("--project", default=DEFAULT_PROJECT, help="AssetRipper 导出的 Unity 工程目录")
    ap.add_argument("--scene", default="level1", help="场景名（默认 level1）")
    ap.add_argument("--level", default="level1_export", help="输出 level 名（默认 level1_export）")
    args = ap.parse_args()
    convert(args.project, args.scene, args.level)


if __name__ == "__main__":
    main()
