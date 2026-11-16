
import UnityPy, math, os, numpy as np
BASE = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data"
F32 = np.float32
def qcm(v): return int(math.floor(float(f"{float(v):.2f}")*100.0 + 0.5))
def qcm_f(v):
    # mimic C: sprintf("%.2f") on float then atof*100+0.5 floor
    return int(math.floor(float(np.format_float_positional(F32(v), precision=2, unique=False, fractional=True, trim='k'))*100 + 0.5))
def fnv_u32(h, v):
    for i in range(4):
        h ^= (v >> (i*8)) & 0xFF
        h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h
def fp_of(pts, qf):
    h = 0
    for p in pts:
        x = 14695981039346656037
        x = fnv_u32(x, 0)
        for v in p: x = fnv_u32(x, qf(v) & 0xFFFFFFFF)
        h ^= x
    return "n%d-%016x" % (len(pts), h)

def load(lvl):
    env = UnityPy.load(os.path.join(BASE,lvl))
    sf = list(env.files.values())[0]; objs = sf.objects
    tr_go, trd, goes = {}, {}, {}
    for pid_, o in objs.items():
        t = o.type.name
        if t == "GameObject":
            go = o.read(); goes[pid_] = (go.m_Tag, go.m_IsActive)
            for c in go.m_Component:
                p = c.component
                if p.path_id in objs and objs[p.path_id].type.name in ("Transform","RectTransform"):
                    tr_go[pid_] = p.path_id; break
        elif t in ("Transform","RectTransform"):
            tr = o.read()
            trd[pid_] = ((tr.m_LocalPosition.x,tr.m_LocalPosition.y,tr.m_LocalPosition.z),
                         (tr.m_LocalRotation.x,tr.m_LocalRotation.y,tr.m_LocalRotation.z,tr.m_LocalRotation.w),
                         (tr.m_LocalScale.x,tr.m_LocalScale.y,tr.m_LocalScale.z), tr.m_Father.path_id)
    return objs, tr_go, trd, goes

def world_pts(lvl, dtype):
    objs, tr_go, trd, goes = load(lvl)
    cache = {}
    def mat(pos,q,s):
        pos = np.array(pos, dtype=dtype); q = np.array(q, dtype=dtype); s = np.array(s, dtype=dtype)
        x,y,z,w = q; n = x*x+y*y+z*z+w*w
        if n < 1e-12: R = np.eye(3, dtype=dtype)
        else:
            s2 = dtype(2.0)/n
            R = np.array([[1-s2*(y*y+z*z), s2*(x*y-z*w),   s2*(x*z+y*w)],
                          [s2*(x*y+z*w),   1-s2*(x*x+z*z), s2*(y*z-x*w)],
                          [s2*(x*z-y*w),   s2*(y*z+x*w),   1-s2*(x*x+y*y)]], dtype=dtype)
        M = np.eye(4, dtype=dtype); M[:3,:3] = R * s[None,:]; M[:3,3] = pos
        return M
    def W(tid, d=0):
        if tid in cache: return cache[tid]
        if tid not in trd or d > 64: return np.eye(4, dtype=dtype)
        pos,q,s,fa = trd[tid]
        F = W(fa, d+1) if fa and fa in trd else np.eye(4, dtype=dtype)
        M = F @ mat(pos,q,s); cache[tid] = M; return M
    pts = []
    for gid,(tag,on) in goes.items():
        if tag != 20022 or not on: continue
        tid = tr_go.get(gid)
        if tid is None: continue
        M = W(tid); pts.append((float(M[0,3]),float(M[1,3]),float(M[2,3])))
    return pts

for lvl, exp in [("level1","n786-57a46e3465c847cb"), ("level8","n3063-b04b59b2593bfae4"), ("level10","n180-03b43b7ee737fcdc")]:
    p64 = world_pts(lvl, np.float64)
    p32 = world_pts(lvl, np.float32)
    print(lvl, "exp", exp)
    print("   f64", fp_of(p64, qcm), " match" if fp_of(p64,qcm)==exp else "")
    print("   f32", fp_of(p32, qcm), " match" if fp_of(p32,qcm)==exp else "")
