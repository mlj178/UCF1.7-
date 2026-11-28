
import glob, re, math
import numpy as np
# route
rp = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/10_*/*.bak-route196")[0]
pts = []
for line in open(rp, encoding="utf-8", errors="replace"):
    m = re.match(r"node add ([-\d.]+) ([-\d.]+) ([-\d.]+)", line.strip())
    if m: pts.append([float(x) for x in m.groups()])
P = np.array(pts)
# navmesh (current, but we want raw surfaces) -> read original bake? use the .navmesh vertices
nv = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/docs/guide/*/out/nano30_storm/nano30_storm.navmesh")[0]
import struct
b = open(nv, "rb").read()
ver, jl, cnt_v, cnt_t = struct.unpack_from("<IIII", b, 4)
V = np.frombuffer(b, dtype="<f4", count=cnt_v*3, offset=20+jl).reshape(cnt_v,3)
from collections import Counter
# 最近顶点高度差
d = []
for p in P:
    idx = np.argmin((V[:,0]-p[0])**2 + (V[:,2]-p[2])**2)
    if math.hypot(V[idx,0]-p[0], V[idx,2]-p[2]) < 1.5:
        d.append(p[1]-V[idx,1])
d = np.array(d)
print("matched", len(d), "median dy", round(float(np.median(d)),2), "p10/p90", np.percentile(d,[10,90]).round(2))
h = Counter(int(round(x)) for x in d)
print(dict(sorted(h.items())))
