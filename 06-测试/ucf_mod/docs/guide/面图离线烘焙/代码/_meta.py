
import glob, json
import numpy as np
p = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/geo/level9.npz")[0]
z = np.load(p, allow_pickle=True)
m = z["meta"]
try:
    s = m.item() if hasattr(m, "item") else m
    d = json.loads(s) if isinstance(s, str) else dict(s)
    for k in ("scenes", "stats", "skipped_shells", "batched", "blocks", "chunks"):
        if k in d: print(k, str(d[k])[:600])
    print("meta keys", list(d.keys())[:20])
except Exception as e:
    print("meta raw", str(m)[:800])
