
import UnityPy, json, math, os, numpy as np
BASE = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data"
MOD  = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod"

def qcm(v): return int(math.floor(float(f"{v:.2f}")*100.0 + 0.5))
def fnv_u32(h, v):
    for i in range(4):
        h ^= (v >> (i*8)) & 0xFF
        h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h
def pt_hash(x,y,z,seed=0):
    h = 14695981039346656037
    h = fnv_u32(h, seed & 0xFFFFFFFF)
    for v in (qcm(x), qcm(y), qcm(z)): h = fnv_u32(h, v & 0xFFFFFFFF)
    return h
def M(pos, q, scl):
    x,y,z,w = q; n = x*x+y*y+z*z+w*w
    s = 2.0/n if n>1e-12 else 0.0
    R = np.array([[1-s*(y*y+z*z), s*(x*y-z*w),   s*(x*z+y*w)],
                  [s*(x*y+z*w),   1-s*(x*x+z*z), s*(y*z-x*w)],
                  [s*(x*z-y*w),   s*(y*z+x*w),   1-s*(x*x+y*y)]])
    M4 = np.eye(4)
    M4[:3,:3] = R * np.array(scl)[None,:]
    M4[:3,3] = pos
    return M4

env = UnityPy.load(os.path.join(BASE,"level1"))
sf = list(env.files.values())[0]; objs = sf.objects
go_tag, go_active, tr_go = {}, {}, {}
tr_data = {}
for pid_, o in objs.items():
    t = o.type.name
    if t == "GameObject":
        go = o.read(); go_tag[pid_] = go.m_Tag; go_active[pid_] = go.m_IsActive
        for c in go.m_Component:
            p = c.component
            if p.path_id in objs and objs[p.path_id].type.name in ("Transform","RectTransform"):
                tr_go[pid_] = p.path_id; break
    elif t in ("Transform","RectTransform"):
        tr = o.read()
        tr_data[pid_] = (np.array([tr.m_LocalPosition.x,tr.m_LocalPosition.y,tr.m_LocalPosition.z]),
                         (tr.m_LocalRotation.x,tr.m_LocalRotation.y,tr.m_LocalRotation.z,tr.m_LocalRotation.w),
                         (tr.m_LocalScale.x,tr.m_LocalScale.y,tr.m_LocalScale.z),
                         tr.m_Father.path_id)
print("transforms", len(tr_data))
cache = {}
def world(tid, depth=0):
    if tid in cache: return cache[tid]
    if tid not in tr_data or depth > 64: return np.eye(4)
    pos, rot, scl, father = tr_data[tid]
    F = world(father, depth+1) if father and father in tr_data else np.eye(4)
    W = F @ M(pos, rot, scl)
    cache[tid] = W; return W

wps = []
for gid, tag in go_tag.items():
    if tag != 20022: continue
    tid = tr_go.get(gid)
    if tid is None: continue
    W = world(tid)
    if not go_active.get(gid, True): continue
    wps.append((float(W[0,3]), float(W[1,3]), float(W[2,3])))
print("waypoints(active)", len(wps))
xr = 0
for x,y,z in wps: xr ^= pt_hash(x,y,z)
print("fingerprint: n%d-%016x" % (len(wps), xr))
print("expected   : n786-57a46e3465c847cb")

j = json.load(open(os.path.join(MOD,"maps","01_运输船.json"),encoding="utf-8"))
nds = j.get("nodes") or j.get("map",{}).get("nodes") or []
print("json keys", list(j.keys())[:12], "nodes", len(nds))
if nds: print("node0", nds[0])
print("bbox scene", min(w[1] for w in wps), max(w[1] for w in wps))
