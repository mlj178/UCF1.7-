"""UCF 资源读取层：索引地图、提取几何（位置/法线/UV）、材质与贴图。

只用只读方式访问游戏目录，任何提取结果都缓存到 cache_dir，不碰游戏文件。

缓存结构（每张场景一份）：
    <cache>/<scene>.npz          几何 + 分块表 + 材质表（JSON 字符串）
    <cache>/tex/<scene>/*.png    解码后的贴图
"""
import json
import os
import time

import numpy as np

try:
    import UnityPy
except Exception as exc:
    UnityPy = None
    _UNITYPY_ERR = repr(exc)
else:
    _UNITYPY_ERR = ""

try:
    import texture2ddecoder
except Exception:
    texture2ddecoder = None

try:
    from PIL import Image
except Exception:
    Image = None

CACHE_VERSION = 7

# Unity TextureFormat 枚举里我们会自己解码的几种
FMT_RGB24 = 3
FMT_RGBA32 = 4
FMT_ALPHA8 = 1
FMT_DXT1 = 10
FMT_DXT5 = 12

FMT_NAMES = {
    1: "Alpha8", 3: "RGB24", 4: "RGBA32", 5: "ARGB32", 7: "RGB565",
    10: "DXT1", 12: "DXT5", 13: "RGBA4444", 47: "BC7", 50: "BC5",
}


def unitypy_ready():
    return UnityPy is not None


def unitypy_error():
    return _UNITYPY_ERR


def find_data_dir(start=None):
    """在常见位置找 UnityCrossFire_Data 目录。"""
    cands = []
    if start:
        cands.append(start)
    env = os.environ.get("UCF_GAME_DIR")
    if env:
        cands.append(os.path.join(env, "UnityCrossFire_Data"))
    here = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        here = os.path.dirname(here)
        cands.append(os.path.join(here, "UnityCrossFire_Data"))
    for c in cands:
        if c and os.path.isdir(c) and os.path.isfile(os.path.join(c, "resources.assets")):
            return c
    return ""


def default_cache_dir(data_dir):
    root = os.path.dirname(os.path.abspath(data_dir))
    cache = os.path.join(root, "ucf_mod", "geo")
    try:
        os.makedirs(cache, exist_ok=True)
        return cache
    except Exception:
        fallback = os.path.join(os.environ.get("TEMP", "."), "ucf_navedit_cache")
        os.makedirs(fallback, exist_ok=True)
        return fallback


def _qmat(q):
    x, y, z, w = q.x, q.y, q.z, q.w
    return np.array([
        [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
        [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
        [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def _local(t):
    m = np.eye(4)
    s = np.array([t.m_LocalScale.x, t.m_LocalScale.y, t.m_LocalScale.z], dtype=np.float64)
    m[:3, :3] = _qmat(t.m_LocalRotation) * s[None, :]
    p = t.m_LocalPosition
    m[:3, 3] = [p.x, p.y, p.z]
    return m


def _parse_obj(text):
    """解析 OBJ，返回 (顶点, UV, 三角形顶点下标, 三角形UV下标)。

    Unity 导出的 OBJ 顶点与 UV 通常一一对应；对不上时交给 _align_uv 去重映射。
    """
    vs, vts, fs, fts = [], [], [], []
    for line in text.split("\n"):
        if line.startswith("v "):
            p = line.split()
            vs.append((float(p[1]), float(p[2]), float(p[3])))
        elif line.startswith("vt "):
            p = line.split()
            vts.append((float(p[1]), float(p[2])))
        elif line.startswith("f "):
            vi, ti = [], []
            for tok in line.split()[1:]:
                bits = tok.split("/")
                vi.append(int(bits[0]) - 1)
                ti.append(int(bits[1]) - 1 if len(bits) > 1 and bits[1] else int(bits[0]) - 1)
            for k in range(1, len(vi) - 1):
                fs.append((vi[0], vi[k], vi[k + 1]))
                fts.append((ti[0], ti[k], ti[k + 1]))
    if not vs:
        return (np.zeros((0, 3)), np.zeros((0, 2)),
                np.zeros((0, 3), dtype=np.int64), np.zeros((0, 3), dtype=np.int64))
    return (np.array(vs, dtype=np.float64), np.array(vts, dtype=np.float64) if vts else np.zeros((0, 2)),
            np.array(fs, dtype=np.int64), np.array(fts, dtype=np.int64) if fts else np.zeros((0, 3), dtype=np.int64))


def _align_uv(pos, uv, fv, ft):
    """把顶点和 UV 对齐。多数网格是一一对应的，对不上时按 (顶点, UV) 组合拆分。"""
    if len(uv) == 0 or len(uv) != len(pos):
        if len(uv) == 0:
            return pos, np.zeros((len(pos), 2), dtype=np.float32), fv
        n = min(len(pos), len(uv))
        return pos[:n], uv[:n].astype(np.float32), np.clip(fv, 0, n - 1)
    if np.array_equal(fv, ft):
        return pos, uv.astype(np.float32), fv
    nv = len(pos)
    code = fv.astype(np.int64).ravel() * (len(uv) + 1) + ft.astype(np.int64).ravel()
    uniq, inv = np.unique(code, return_inverse=True)
    vi = uniq // (len(uv) + 1)
    ti = uniq % (len(uv) + 1)
    new_pos = pos[vi]
    new_uv = uv[ti].astype(np.float32)
    new_f = inv.reshape(-1, 3).astype(np.int64)
    return new_pos, new_uv, new_f


class MatInfo(object):
    """一个材质的渲染所需信息。"""

    __slots__ = ("name", "shader", "color", "tex", "tex_w", "tex_h",
                 "tex_fmt", "transparent", "cutoff", "queue")

    def __init__(self, name="", shader="", color=(1.0, 1.0, 1.0, 1.0), tex="",
                 tex_w=0, tex_h=0, tex_fmt="", transparent=False, cutoff=0.5, queue=-1):
        self.name = name
        self.shader = shader
        self.color = color
        self.tex = tex
        self.tex_w = tex_w
        self.tex_h = tex_h
        self.tex_fmt = tex_fmt
        self.transparent = transparent
        self.cutoff = cutoff
        self.queue = queue

    def to_dict(self):
        return {
            "name": self.name, "shader": self.shader,
            "color": list(self.color), "tex": self.tex,
            "tex_w": self.tex_w, "tex_h": self.tex_h, "tex_fmt": self.tex_fmt,
            "transparent": bool(self.transparent), "cutoff": self.cutoff,
            "queue": self.queue,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d.get("name", ""), d.get("shader", ""), tuple(d.get("color") or (1, 1, 1, 1)),
                   d.get("tex", ""), d.get("tex_w", 0), d.get("tex_h", 0), d.get("tex_fmt", ""),
                   d.get("transparent", False), d.get("cutoff", 0.5), d.get("queue", -1))


class Geo(object):
    """一块可供 GPU 直接吃的几何，按网格分块。"""

    def __init__(self, positions, normals, uvs, colors, indices, groups, bbox,
                 chunks=None, mats=None, tex_dir="", env=None):
        self.positions = positions
        self.normals = normals
        self.uvs = uvs
        self.colors = colors
        self.indices = indices
        self.groups = groups
        self.bbox = bbox
        self.chunks = chunks or []
        self.mats = mats or []
        self.tex_dir = tex_dir
        self.env = env or {}

    @property
    def vertex_count(self):
        return int(len(self.positions))

    @property
    def triangle_count(self):
        return int(len(self.groups))

    @property
    def textured_count(self):
        return sum(1 for c in self.chunks if c.get("tex"))

    def tex_path(self, chunk):
        tex = chunk.get("tex") or ""
        if not tex:
            return ""
        return os.path.join(self.tex_dir, tex)


def _normals(positions, tris):
    n = np.zeros(len(positions), dtype=np.float64)
    if len(tris) == 0:
        return np.zeros((len(positions), 3), dtype=np.float32)
    a = positions[tris[:, 0]]
    b = positions[tris[:, 1]]
    c = positions[tris[:, 2]]
    fn = np.cross(b - a, c - a)
    ln = np.linalg.norm(fn, axis=1)
    ln[ln == 0] = 1.0
    fn = fn / ln[:, None]
    out = np.zeros((len(positions), 3), dtype=np.float64)
    for k in range(3):
        np.add.at(out, tris[:, k], fn)
    ln2 = np.linalg.norm(out, axis=1)
    ln2[ln2 == 0] = 1.0
    out = out / ln2[:, None]
    return out.astype(np.float32)


def _lenient_dict(reader):
    """读 typetree。这个 Unity 构建的 Texture2D 结构比 UnityPy 自带的少 24 字节，
    正常读取会抛 Expected to read N bytes，容错模式能拿到全部需要的字段。"""
    return reader.read_typetree(check_read=False)


def _tex_raw(d, data_dir):
    """取出贴图原始像素字节。返回 (w, h, raw, mode)。"""
    w = int(d.get("m_Width") or 0)
    h = int(d.get("m_Height") or 0)
    fmt = int(d.get("m_TextureFormat") or 0)
    if w <= 0 or h <= 0:
        return 0, 0, b"", ""
    sd = d.get("m_StreamData") or {}
    raw = b""
    if isinstance(sd, dict) and sd.get("size"):
        path = sd.get("path") or ""
        full = os.path.join(data_dir, str(path))
        if os.path.isfile(full):
            with open(full, "rb") as f:
                f.seek(int(sd.get("offset") or 0))
                raw = f.read(int(sd.get("size")))
    if not raw:
        raw = d.get("image data") or b""
    if not raw:
        return 0, 0, b"", ""
    if fmt == FMT_DXT1 and texture2ddecoder is not None:
        return w, h, texture2ddecoder.decode_bc1(raw, w, h), "RGBA"
    if fmt == FMT_DXT5 and texture2ddecoder is not None:
        return w, h, texture2ddecoder.decode_bc3(raw, w, h), "RGBA"
    if fmt == FMT_RGB24:
        return w, h, raw[:w * h * 3], "RGB"
    if fmt == FMT_RGBA32:
        return w, h, raw[:w * h * 4], "RGBA"
    if fmt == FMT_ALPHA8:
        return w, h, raw[:w * h], "L"
    return 0, 0, b"", ""


class AssetDB(object):
    def __init__(self, data_dir, cache_dir=None):
        self.data_dir = data_dir
        self.cache_dir = cache_dir or default_cache_dir(data_dir)
        self.env = None
        self.files = []
        self.maps = []
        self.skipped_shells = 0
        self.batched_renderers = 0
        self.card_triangles = 0
        self.last_extract_seconds = 0.0

    # ---- 索引 -------------------------------------------------------
    def open(self):
        if UnityPy is None:
            raise RuntimeError("缺少 UnityPy：" + _UNITYPY_ERR)
        t0 = time.time()
        self.env = UnityPy.load(self.data_dir)
        self.files = sorted(os.path.basename(str(k)) for k in self.env.files)
        self.maps = self._scan_maps()
        self.load_seconds = time.time() - t0
        return self

    def _scan_maps(self):
        out = []
        for name in self.files:
            low = name.lower()
            if low.startswith("level") and "." not in low:
                path = os.path.join(self.data_dir, name)
                out.append({
                    "scene": name,
                    "size": os.path.getsize(path) if os.path.isfile(path) else 0,
                    "title": name,
                    "pieces": 0,
                })
        out.sort(key=lambda m: (len(m["scene"]), m["scene"]))
        return out

    def scene_object(self, scene):
        for key, val in self.env.files.items():
            if os.path.basename(str(key)).lower() == scene.lower():
                return val
        return None

    # ---- 缓存 -------------------------------------------------------
    def cache_path(self, scene):
        return os.path.join(self.cache_dir, "%s.npz" % scene)

    def tex_dir(self, scene):
        d = os.path.join(self.cache_dir, "tex", scene)
        os.makedirs(d, exist_ok=True)
        return d

    def cache_valid(self, scene):
        p = self.cache_path(scene)
        if not os.path.isfile(p):
            return False
        src = os.path.join(self.data_dir, scene)
        if not os.path.isfile(src):
            return False
        if os.path.getmtime(p) < os.path.getmtime(src):
            return False
        try:
            z = np.load(p, allow_pickle=True)
            if "meta" not in z.files or "uv" not in z.files:
                return False
            meta = json.loads(str(z["meta"][0]))
            return int(meta.get("v", 0)) == CACHE_VERSION
        except Exception:
            return False

    # ---- 材质 / 贴图 -------------------------------------------------
    def _shader_name(self, mat):
        try:
            sh = mat.m_Shader.read()
        except Exception:
            return ""
        pf = getattr(sh, "m_ParsedForm", None)
        if pf is not None:
            return str(getattr(pf, "m_Name", "") or "")
        return str(getattr(sh, "m_Name", "") or "")

    def _material(self, mat_obj, scene, tex_seen, progress=None):
        name = str(getattr(mat_obj, "m_Name", "") or "")
        shader = self._shader_name(mat_obj)
        sp = getattr(mat_obj, "m_SavedProperties", None)
        colors, floats, teximg = {}, {}, None
        for kv in (getattr(sp, "m_Colors", None) or []):
            try:
                nm, c = kv
                colors[str(nm)] = (float(c.r), float(c.g), float(c.b), float(c.a))
            except Exception:
                pass
        for kv in (getattr(sp, "m_Floats", None) or []):
            try:
                nm, v = kv
                floats[str(nm)] = float(v)
            except Exception:
                pass
        for kv in (getattr(sp, "m_TexEnvs", None) or []):
            try:
                nm, e = kv
            except Exception:
                continue
            if str(nm).lower() in ("_maintex", "_basemap"):
                teximg = getattr(e, "m_Texture", None)
                if teximg is not None and int(getattr(teximg, "m_PathID", 0) or 0):
                    break
                teximg = None
        color = colors.get("_BaseColor") or colors.get("_Color") or (1.0, 1.0, 1.0, 1.0)
        cutoff = floats.get("_Cutoff", 0.5)
        queue = int(getattr(mat_obj, "m_CustomRenderQueue", -1) or -1)
        surf = floats.get("_Surface", 0.0)
        transparent = queue >= 3000 or surf >= 1.0 or "Water" in shader
        info = MatInfo(name=name, shader=shader, color=color, cutoff=cutoff,
                       transparent=transparent, queue=queue)
        if teximg is None:
            return info
        af = getattr(teximg, "assetsfile", None)
        tkey = (str(getattr(af, "name", "") or ""), int(teximg.m_PathID))
        cached = tex_seen.get(tkey)
        if cached is None:
            cached = self._texture(teximg, scene)
            tex_seen[tkey] = cached
        if cached:
            info.tex = cached.get("file", "")
            info.tex_w = cached.get("w", 0)
            info.tex_h = cached.get("h", 0)
            info.tex_fmt = cached.get("fmt", "")
        return info

    def _texture(self, tex_pptr, scene):
        try:
            rd = tex_pptr.deref()
            d = _lenient_dict(rd)
        except Exception:
            return None
        tname = str(d.get("m_Name", "") or "")
        fmt = FMT_NAMES.get(int(d.get("m_TextureFormat") or 0), str(d.get("m_TextureFormat")))
        w, h, raw, mode = _tex_raw(d, self.data_dir)
        if not raw or Image is None:
            return {"file": "", "w": int(d.get("m_Width") or 0),
                    "h": int(d.get("m_Height") or 0), "fmt": fmt, "name": tname}
        try:
            safe = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in tname)[:48]
            fname = "%s_%d.png" % (safe or "tex", int(d.get("m_TextureFormat") or 0))
            out = os.path.join(self.tex_dir(scene), fname)
            if not os.path.isfile(out):
                img = Image.frombytes(mode, (w, h), raw)
                img.save(out)
            return {"file": fname, "w": w, "h": h, "fmt": fmt, "name": tname}
        except Exception:
            return None

    # ---- 提取 -------------------------------------------------------
    def extract(self, scene, progress=None, use_cache=True):
        if use_cache and self.cache_valid(scene):
            return self.load_cache(scene)
        if self.env is None:
            self.open()
        t0 = time.time()
        sf = self.scene_object(scene)
        if sf is None:
            raise RuntimeError("找不到场景文件：" + scene)
        objs = list(sf.objects.values())
        if progress:
            progress("解析 %s（%d 个对象）" % (scene, len(objs)))

        trs, tr_of_go, go_names, mfs, rends = {}, {}, {}, [], {}
        keep_types = ("Transform", "MeshFilter", "MeshRenderer", "SkinnedMeshRenderer", "GameObject")
        for o in objs:
            kind = str(o.type.name)
            if kind not in keep_types:
                continue
            try:
                d = o.read()
            except Exception:
                continue
            if kind == "Transform":
                trs[o.path_id] = d
                try:
                    tr_of_go[int(d.m_GameObject.path_id)] = o.path_id
                except Exception:
                    pass
            elif kind == "GameObject":
                try:
                    go_names[int(o.path_id)] = str(d.m_Name)
                except Exception:
                    pass
            elif kind == "MeshFilter":
                mfs.append((o.path_id, d))
            else:
                try:
                    rends[int(d.m_GameObject.path_id)] = d
                except Exception:
                    pass

        father = {}
        for pid, t in trs.items():
            try:
                f = int(t.m_Father.path_id)
                father[pid] = f if f else None
            except Exception:
                father[pid] = None

        wcache = {}

        def world(pid, depth=0):
            if pid in wcache:
                return wcache[pid]
            l = _local(trs[pid])
            f = father.get(pid)
            if f in trs and depth < 64:
                w = world(f, depth + 1) @ l
            else:
                w = l
            wcache[pid] = w
            return w

        mesh_cache = {}
        mat_cache = {}
        tex_seen = {}
        shared_verts = {}
        pool_pos, pool_uv = [], []
        nv_total = 0
        raws = []
        total = len(mfs)
        batch_count = 0
        for i, (pid, d) in enumerate(mfs):
            if progress and (i % 25 == 0):
                progress("提取网格 %d/%d" % (i, total))
            try:
                mp = d.m_Mesh
                if mp.m_PathID == 0:
                    continue
                af = getattr(mp, "assets_file", None)
                key = (str(af.name) if af else "?", int(mp.m_PathID))
                if key not in mesh_cache:
                    mh = mp.read()
                    parsed = _parse_obj(mh.export("obj"))
                    mesh_cache[key] = (parsed, str(mh.m_Name), _submesh_ranges(mh, len(parsed[2])))
                (vs, vts, fv, ft), mname, ranges = mesh_cache[key]
                if len(fv) == 0:
                    continue
                vs, vts, fv = _align_uv(vs, vts, fv, ft)
                if len(vts) and not np.isfinite(vts).all():
                    vts = np.nan_to_num(vts, nan=0.0, posinf=0.0, neginf=0.0)

                gid = int(d.m_GameObject.path_id)
                rend = rends.get(gid)
                mlist = []
                if rend is not None:
                    try:
                        mlist = list(getattr(rend, "m_Materials", None) or [])
                    except Exception:
                        mlist = []
                sbi = getattr(rend, "m_StaticBatchInfo", None) if rend is not None else None
                first = int(getattr(sbi, "firstSubMesh", getattr(sbi, "m_FirstSubMesh", 0)) or 0) if sbi is not None else 0
                cnt = int(getattr(sbi, "subMeshCount", getattr(sbi, "m_SubMeshCount", 0)) or 0) if sbi is not None else 0
                batched = bool(sbi is not None and cnt >= 1 and len(ranges) > 1
                               and first + cnt <= len(ranges))

                if batched:
                    if key not in shared_verts:
                        shared_verts[key] = nv_total
                        pool_pos.append(vs)
                        pool_uv.append(vts)
                        nv_total += len(vs)
                    vbase = shared_verts[key]
                    vcount = len(vs)
                    sel = ranges[first:first + cnt]
                    batch_count += 1
                else:
                    tr = tr_of_go.get(gid)
                    w = world(tr) if tr in trs else np.eye(4)
                    v4 = np.hstack([vs, np.ones((len(vs), 1))]) @ w.T
                    vbase = nv_total
                    vcount = len(vs)
                    pool_pos.append(v4[:, :3])
                    pool_uv.append(vts)
                    nv_total += len(vs)
                    sel = ranges

                for si, (s, n) in enumerate(sel):
                    if n <= 0:
                        continue
                    tri = fv[s:s + n]
                    if len(tri) == 0:
                        continue
                    if batched:
                        mp2 = mlist[0] if mlist else None
                    elif si < len(mlist):
                        mp2 = mlist[si]
                    else:
                        mp2 = mlist[0] if mlist else None
                    mat = None
                    if mp2 is not None:
                        try:
                            mkey = (str(mp2.assetsfile.name), int(mp2.m_PathID))
                            if mkey not in mat_cache:
                                mat_cache[mkey] = self._material(mp2.read(), scene, tex_seen)
                            mat = mat_cache[mkey]
                        except Exception:
                            mat = None
                    raws.append({
                        "tris": tri + vbase,
                        "vbase": vbase, "vcount": vcount,
                        "name": go_names.get(gid, mname),
                        "mesh": mname,
                        "mat": mat or MatInfo(),
                    })
            except Exception:
                continue

        if not raws:
            raise RuntimeError("这个场景里没有可提取的网格：" + scene)

        pos_all = np.vstack(pool_pos)
        uv_all = np.vstack(pool_uv)
        glo = pos_all.min(0)
        ghi = pos_all.max(0)
        gdiag = float(np.linalg.norm(ghi - glo))
        tot_tris = sum(len(r["tris"]) for r in raws)
        keep = []
        for i, r in enumerate(raws):
            p = pos_all[r["tris"]].reshape(-1, 3)
            diag = float(np.linalg.norm(p.max(0) - p.min(0)))
            if gdiag > 0 and diag > 0.85 * gdiag and len(r["tris"]) <= 0.04 * max(1, tot_tris):
                continue
            keep.append(i)
        if not keep:
            keep = list(range(len(raws)))
        self.skipped_shells = len(raws) - len(keep)
        self.batched_renderers = batch_count

        parts = [raws[i] for i in keep]

        # 装饰板/特效片的识别：单个三角形大到不可能是正常结构件，
        # 又几乎没有碰撞体意义（灯塔光锥、玻璃、烟雾片、海面卡片之类）。
        # 它们在游戏里多半是半透明或看不见的，硬画出来就是一片片糊住视线的板子。
        alltri = np.vstack([r["tris"] for r in parts])
        pa = pos_all[alltri[:, 0]].astype(np.float64)
        pb = pos_all[alltri[:, 1]].astype(np.float64)
        pc = pos_all[alltri[:, 2]].astype(np.float64)
        e1 = pb - pa
        e2 = pc - pa
        maxedge = np.maximum(np.maximum(np.linalg.norm(e1, axis=1), np.linalg.norm(e2, axis=1)),
                             np.linalg.norm(pc - pb, axis=1))
        area = 0.5 * np.linalg.norm(np.cross(e1, e2), axis=1)
        is_card = (maxedge > 25.0) | (area > 150.0)
        self.card_triangles = int(is_card.sum())

        cursor = 0
        tri_all = alltri
        tri_group = np.zeros(len(tri_all), dtype=np.int32)
        chunks = []
        mats = []
        mat_index = {}
        nt = 0
        for r in parts:
            m = r["mat"]
            mk = (m.name, m.tex)
            if mk not in mat_index:
                mat_index[mk] = len(mats)
                mats.append(m)
            mi = mat_index[mk]
            is_shadow = m.shader.endswith("Shadow")
            is_water = "Water" in m.shader
            low = str(r["name"]).lower()
            is_blocker = any(k in low for k in ("blocker", "collision", "invisible", "invis_"))
            alpha_test = 0.35 if str(m.tex_fmt).upper() in ("DXT5", "BC3", "RGBA32", "BC7") else 0.0
            alpha = 0.55 if is_water else max(0.0, min(1.0, float(m.color[3])))
            # 该块的三角形切一段出来，再按"装饰板"拆成两块
            n = len(r["tris"])
            for card in (False, True):
                sel = is_card[cursor:cursor + n] == card
                if not sel.any():
                    continue
                idx = r["tris"][sel]
                chunks.append({
                    "name": r["name"], "mesh": r["mesh"],
                    "mat": mi, "start": nt, "count": int(len(idx)),
                    "vstart": int(r["vbase"]), "vcount": int(r["vcount"]),
                    "tex": m.tex, "color": list(m.color),
                    "alpha": alpha,
                    "alpha_test": alpha_test,
                    "shadow": bool(is_shadow),
                    "water": bool(is_water),
                    "blocker": bool(is_blocker),
                    "card": bool(card),
                    "transparent": bool(m.transparent or is_water or alpha < 0.99),
                })
                tri_group[nt:nt + len(idx)] = len(chunks) - 1
                nt += len(idx)
            cursor += n

        env = _read_env(sf, trs, tr_of_go)
        nrm = _normals(pos_all, tri_all)
        rng = np.random.default_rng(11)
        tint = 0.82 + 0.18 * rng.random((max(1, len(chunks)), 3))
        col = tint[tri_group][:, :]
        vcol = np.zeros((len(pos_all), 3), dtype=np.float32)
        vcol[tri_all[:, 0]] = col
        vcol[tri_all[:, 1]] = col
        vcol[tri_all[:, 2]] = col
        bbox = np.array([pos_all.min(0), pos_all.max(0)])
        geo = Geo(pos_all.astype(np.float32), nrm, uv_all.astype(np.float32), vcol,
                  tri_all.astype(np.int32), tri_group.astype(np.int32), bbox.astype(np.float32),
                  chunks=chunks, mats=mats, tex_dir=self.tex_dir(scene), env=env)
        self.save_cache(scene, geo)
        self.last_extract_seconds = time.time() - t0
        return geo

    def save_cache(self, scene, geo):
        meta = {
            "v": CACHE_VERSION,
            "scene": scene,
            "chunks": geo.chunks,
            "mats": [m.to_dict() for m in geo.mats],
            "skipped_shells": self.skipped_shells,
            "batched": getattr(self, "batched_renderers", 0),
            "env": geo.env,
        }
        try:
            np.savez_compressed(
                self.cache_path(scene),
                p=geo.positions, n=geo.normals, uv=geo.uvs, c=geo.colors,
                i=geo.indices, g=geo.groups, b=geo.bbox,
                meta=np.array([json.dumps(meta)]))
        except Exception:
            pass

    def load_cache(self, scene):
        t0 = time.time()
        z = np.load(self.cache_path(scene), allow_pickle=True)
        meta = {}
        if "meta" in z.files:
            try:
                meta = json.loads(str(z["meta"][0]))
            except Exception:
                meta = {}
        mats = [MatInfo.from_dict(d) for d in meta.get("mats", [])]
        geo = Geo(z["p"], z["n"], z["uv"] if "uv" in z.files else np.zeros((len(z["p"]), 2), "f4"),
                  z["c"], z["i"], z["g"], z["b"],
                  chunks=meta.get("chunks", []), mats=mats,
                  tex_dir=self.tex_dir(scene), env=meta.get("env") or {})
        self.skipped_shells = int(meta.get("skipped_shells", 0))
        self.batched_renderers = int(meta.get("batched", 0))
        self.last_extract_seconds = time.time() - t0
        return geo


LIGHT_DIRECTIONAL = 1
LIGHT_POINT = 2


def _read_env(sf, trs, tr_of_go):
    """读场景的真实光照参数：RenderSettings 的三色环境光 + 各盏灯。

    Unity 的 AmbientMode=3 是 Trilight（天空/赤道/地面三段插值），
    方向光取它 Transform 的 +Z 方向，点光带范围和强度。
    这些就是游戏里实际用的光，照搬过来比我自己瞎猜的"太阳+环境光"像得多。
    """
    env = {
        "ambient": {"sky": (0.5, 0.5, 0.5), "equator": (0.3, 0.3, 0.3), "ground": (0.15, 0.15, 0.15)},
        "fog": {"on": False, "color": (0.5, 0.5, 0.5), "start": 0.0, "end": 300.0, "density": 0.01, "mode": 3},
        "sun": {"dir": (0.3, -0.9, 0.2), "color": (1.0, 1.0, 1.0)},
        "points": [],
    }
    rs = None
    for o in sf.objects.values():
        if str(o.type.name) == "RenderSettings":
            try:
                rs = o.read()
            except Exception:
                rs = None
            break
    if rs is not None:
        try:
            a = env["ambient"]
            for key, attr in (("sky", "m_AmbientSkyColor"), ("equator", "m_AmbientEquatorColor"),
                              ("ground", "m_AmbientGroundColor")):
                c = getattr(rs, attr, None)
                if c is not None:
                    a[key] = (float(c.r), float(c.g), float(c.b))
            f = env["fog"]
            f["on"] = bool(getattr(rs, "m_Fog", False))
            c = getattr(rs, "m_FogColor", None)
            if c is not None:
                f["color"] = (float(c.r), float(c.g), float(c.b))
            f["start"] = float(getattr(rs, "m_LinearFogStart", 0.0) or 0.0)
            f["end"] = float(getattr(rs, "m_LinearFogEnd", 300.0) or 300.0)
            f["density"] = float(getattr(rs, "m_FogDensity", 0.01) or 0.01)
            f["mode"] = int(getattr(rs, "m_FogMode", 3) or 3)
        except Exception:
            pass

    def light_dir(gid):
        pid = tr_of_go.get(gid)
        if pid not in trs:
            return None
        m = np.eye(4)
        depth = 0
        cur = pid
        while cur in trs and depth < 64:
            m = _local(trs[cur]) @ m
            try:
                f = int(trs[cur].m_Father.path_id)
            except Exception:
                f = 0
            if not f:
                break
            cur = f
            depth += 1
        d = m[:3, 2]
        n = float(np.linalg.norm(d))
        return tuple((d / n).tolist()) if n > 1e-9 else None

    def light_pos(gid):
        pid = tr_of_go.get(gid)
        if pid not in trs:
            return None
        m = np.eye(4)
        depth = 0
        cur = pid
        while cur in trs and depth < 64:
            m = _local(trs[cur]) @ m
            try:
                f = int(trs[cur].m_Father.path_id)
            except Exception:
                f = 0
            if not f:
                break
            cur = f
            depth += 1
        return tuple(float(x) for x in m[:3, 3])

    pts = []
    for o in sf.objects.values():
        if str(o.type.name) != "Light":
            continue
        try:
            d = o.read()
        except Exception:
            continue
        try:
            gid = int(d.m_GameObject.path_id)
        except Exception:
            continue
        lt = int(getattr(d, "m_Type", -1))
        col = getattr(d, "m_Color", None)
        rgb = (float(col.r), float(col.g), float(col.b)) if col is not None else (1.0, 1.0, 1.0)
        inten = float(getattr(d, "m_Intensity", 1.0) or 1.0)
        enabled = bool(getattr(d, "m_Enabled", True))
        if not enabled:
            continue
        if lt == LIGHT_DIRECTIONAL:
            d3 = light_dir(gid)
            if d3:
                env["sun"] = {"dir": d3, "color": tuple(c * inten for c in rgb)}
        elif lt == LIGHT_POINT:
            p3 = light_pos(gid)
            rng = float(getattr(d, "m_Range", 10.0) or 10.0)
            if p3 and rng > 0:
                pts.append({"pos": p3, "range": rng, "color": tuple(c * inten for c in rgb)})
    env["points"] = pts[:8]
    return env


def _submesh_ranges(mesh, ntri):
    """网格每个子网格的三角形区间（按 indexCount 累加，OBJ 面顺序与子网格顺序一致）。"""
    subs = getattr(mesh, "m_SubMeshes", None) or []
    out = []
    acc = 0
    for sm in subs:
        n = int(getattr(sm, "indexCount", 0) or 0) // 3
        out.append((acc, n))
        acc += n
    if not out or acc != ntri:
        return [(0, ntri)]
    return out


def support_ratio(geo, pts, cell=2.0, tol=2.5, max_tris=400000):
    """判断一组点是不是属于这张图的几何：每个点所在的 2 m 格子里必须有几何。

    返回 (命中比例, 未命中的点数, 参与统计的点数)。用来挡掉"别的地图的路点"。
    """
    if geo is None or len(pts) == 0 or len(geo.indices) == 0:
        return 1.0, 0, 0
    tri = geo.indices
    if len(tri) > max_tris:
        step = max(1, len(tri) // max_tris)
        tri = tri[::step]
    c = geo.positions[tri].mean(axis=1).astype(np.float64)
    key = (np.floor(c[:, 0] / cell).astype(np.int64) * 1000003
           + np.floor(c[:, 2] / cell).astype(np.int64))
    ymin = np.full(len(c), 1e9)
    ymax = np.full(len(c), -1e9)
    uniq, inv = np.unique(key, return_inverse=True)
    np.minimum.at(ymin, inv, c[:, 1])
    np.maximum.at(ymax, inv, c[:, 1])

    p = np.asarray(pts, dtype=np.float64)
    pk = (np.floor(p[:, 0] / cell).astype(np.int64) * 1000003
          + np.floor(p[:, 2] / cell).astype(np.int64))
    pos = np.searchsorted(uniq, pk)
    hit = 0
    for i in range(len(p)):
        j = int(pos[i])
        if j < len(uniq) and uniq[j] == pk[i]:
            if ymin[j] - tol <= p[i, 1] <= ymax[j] + tol:
                hit += 1
    return hit / float(len(p)), len(p) - hit, len(p)


def guess_map_title(names):
    """从网格名猜地图名，例如 nano30_quake_004 -> nano30。"""
    if not names:
        return "?"
    counts = {}
    for n in names:
        stem = str(n).split("_")[0]
        counts[stem] = counts.get(stem, 0) + 1
    return sorted(counts.items(), key=lambda kv: -kv[1])[0][0]
