
import glob, json, math
import numpy as np
p = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/geo/level9.npz")[0]
z = np.load(p, allow_pickle=True)
meta = z["meta"]
d = meta.item() if hasattr(meta, "item") else meta
if isinstance(d, str): d = json.loads(d)
V = z["p"].astype(np.float64); I = z["i"].astype(np.int64)
tri = V[I]
n = np.cross(tri[:,1]-tri[:,0], tri[:,2]-tri[:,0])
area = np.linalg.norm(n, axis=1)/2
un = n/np.maximum(np.linalg.norm(n,axis=1),1e-9)[:,None]
flat = (np.abs(un[:,1]) > 0.7) & (area > 0.02)
ym = tri[:,:,1].mean(1)
agg = {}
for c in d["chunks"]:
    s, cnt = int(c["start"]), int(c["count"])
    if cnt <= 0: continue
    sl = slice(s, s+cnt)
    low = area[sl][flat[sl] & (ym[sl] > -1) & (ym[sl] < 3)].sum()
    key = ("water" if c.get("water") else "") + ("card" if c.get("card") else "") + \
          ("blocker" if c.get("blocker") else "") + ("shadow" if c.get("shadow") else "")
    key = key or "normal"
    a = agg.setdefault(key, {"tris": 0, "low": 0.0, "names": []})
    a["tris"] += cnt; a["low"] += low
    if low > 50: a["names"].append((c["name"], round(float(low))))
for k, v in sorted(agg.items(), key=lambda kv: -kv[1]["low"]):
    print("%-14s tris %6d  ground(-1..3) %8.0f m2  %s" % (k, v["tris"], v["low"], str(v["names"][:4])))
