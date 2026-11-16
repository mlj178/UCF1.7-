
import UnityPy, json, math, os, numpy as np
BASE = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data"

def qcm(v):
    return int(math.floor(float(f"{v:.2f}")*100.0 + 0.5))

def fnv_u32(h, v):
    for i in range(4):
        h ^= (v >> (i*8)) & 0xFF
        h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h

def pt_hash(x,y,z,seed=0):
    h = 14695981039346656037
    h = fnv_u32(h, seed & 0xFFFFFFFF)
    for v in (qcm(x), qcm(y), qcm(z)):
        h = fnv_u32(h, v & 0xFFFFFFFF)
    return h

def quat_mat(q):
    x,y,z,w = q
    n = x*x+y*y+z*z+w*w
    if n < 1e-12: return np.eye(3)
    s = 2.0/n
    M = np.array([
      [1-s*(y*y+z*z), s*(x*y-z*w),   s*(x*z+y*w)],
      [s*(x*y+z*w),   1-s*(x*x+z*z), s*(y*z-x*w)],
      [s*(x*z-y*w),   s*(y*z+x*w),   1-s*(x*x+y*y)]])
    return M

env = UnityPy.load(os.path.join(BASE,"level1"))
sf = list(env.files.values())[0]
objs = sf.objects
gpos = {}
tr_of_go = {}
for pid_, o in objs.items():
    if o.type.name != "GameObject": continue
    go = o.read()
    gpos[pid_] = go
    comp = go.m_Component
    for c in comp:
        ptr = c.component if hasattr(c,"component") else c
        tp = ptr.path_id
        if tp in objs and objs[tp].type.name in ("Transform","RectTransform"):
            tr_of_go[pid_] = tp
            break
print("GAMEOBJECTS", len(gpos), "with transform", len(tr_of_go))
print("sample transform:", objs[list(tr_of_go.values())[0]].read().__dict__.keys())
