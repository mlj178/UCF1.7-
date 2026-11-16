
import UnityPy, json, math, os, numpy as np
BASE = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data"
MOD  = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod"
def qcm(v): return int(math.floor(float(f"{v:.2f}")*100.0 + 0.5))
def fnv_u32(h, v):
    for i in range(4):
        h ^= (v >> (i*8)) & 0xFF
        h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h
def pt_hash(p, seed=0):
    h = 14695981039346656037
    h = fnv_u32(h, seed & 0xFFFFFFFF)
    for v in p: h = fnv_u32(h, qcm(v) & 0xFFFFFFFF)
    return h
def M(pos, q, scl):
    x,y,z,w = q; n = x*x+y*y+z*z+w*w; s = 2.0/n if n>1e-12 else 0.0
    R = np.array([[1-s*(y*y+z*z), s*(x*y-z*w),   s*(x*z+y*w)],
                  [s*(x*y+z*w),   1-s*(x*x+z*z), s*(y*z-x*w)],
                  [s*(x*z-y*w),   s*(y*z+x*w),   1-s*(x*x+y*y)]])
    M4 = np.eye(4); M4[:3,:3] = R * np.array(scl)[None,:]; M4[:3,3] = pos; return M4

def scene_waypoints(lvl):
    env = UnityPy.load(os.path.join(BASE,lvl))
    sf = list(env.files.values())[0]; objs = sf.objects
    tr_go, tr_data, goes = {}, {}, {}
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
            tr_data[pid_] = (np.array([tr.m_LocalPosition.x,tr.m_LocalPosition.y,tr.m_LocalPosition.z]),
                             (tr.m_LocalRotation.x,tr.m_LocalRotation.y,tr.m_LocalRotation.z,tr.m_LocalRotation.w),
                             (tr.m_LocalScale.x,tr.m_LocalScale.y,tr.m_LocalScale.z), tr.m_Father.path_id)
    cache = {}
    def world(tid, d=0):
        if tid in cache: return cache[tid]
        if tid not in tr_data or d > 64: return np.eye(4)
        pos, rot, scl, fa = tr_data[tid]
        F = world(fa, d+1) if fa and fa in tr_data else np.eye(4)
        W = F @ M(pos, rot, scl); cache[tid] = W; return W
    act, ina = [], []
    for gid,(tag,on) in goes.items():
        if tag != 20022: continue
        tid = tr_go.get(gid)
        if tid is None: continue
        W = world(tid); p = (float(W[0,3]),float(W[1,3]),float(W[2,3]))
        (act if on else ina).append(p)
    return act, ina

for lvl in [f"level{i}" for i in range(1,12)]:
    a, i_ = scene_waypoints(lvl)
    xr = 0
    for p in a: xr ^= pt_hash(p)
    print(f"{lvl}: active={len(a)} inactive={len(i_)} fp=n{len(a)}-{xr:016x}", flush=True)
