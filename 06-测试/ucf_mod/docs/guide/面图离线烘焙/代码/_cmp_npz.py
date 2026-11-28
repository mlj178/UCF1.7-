
import glob, math, collections
import numpy as np

def stats(path):
    z = np.load(path, allow_pickle=True)
    V, F = z["v"].astype(np.float64), z["f"].astype(np.int64)
    tri = V[F]
    n = np.cross(tri[:,1]-tri[:,0], tri[:,2]-tri[:,0])
    ln = np.linalg.norm(n, axis=1); ln[ln==0]=1
    un = n/ln[:,None]; area = ln/2
    ok = (area > 0.02) & (np.abs(un[:,1]) > 0.02)
    tri, un, area = tri[ok], un[ok], area[ok]
    flat = np.abs(un[:,1]) > math.cos(math.radians(45))
    # 低处水平面上的点数按面积算
    h = tri[flat][:,:,1].mean(1)
    low = flat & (tri[:,:,1].mean(1) < 3.0)
    hi = flat & (tri[:,:,1].mean(1) > 7.0)
    print("%-22s tris %6d  area %8.0f  flat %8.0f  low(<3m) %7.0f m2  high(>7m) %7.0f m2" % (
        path.split("/")[-1], len(tri), area.sum(), area[flat].sum(),
        area[low].sum(), area[hi].sum()))

for p in ("level9.npz", "nano30_storm.npz"):
    f = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/geo/" + p)
    if f: stats(f[0])
    else: print(p, "missing")
