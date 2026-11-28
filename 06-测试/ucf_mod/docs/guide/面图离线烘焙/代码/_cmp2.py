
import glob, math
import numpy as np
p = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/geo/level9.npz")[0]
z = np.load(p, allow_pickle=True)
print("keys", {k: getattr(z[k], "shape", None) for k in z.keys() if k != "meta"})
V = z["p"].astype(np.float64); F = z["i"].astype(np.int64)
tri = V[F]
n = np.cross(tri[:,1]-tri[:,0], tri[:,2]-tri[:,0])
ln = np.linalg.norm(n, axis=1); ln[ln==0]=1
un = n/ln[:,None]; area = ln/2
ok = (area > 0.02) & (np.abs(un[:,1]) > 0.02)
tri, un, area = tri[ok], un[ok], area[ok]
flat = np.abs(un[:,1]) > math.cos(math.radians(45))
ym = tri[:,:,1].mean(1)
print("tris", len(tri), "area %.0f flat %.0f" % (area.sum(), area[flat].sum()))
for lo, hi in ((-1,3),(3,7),(7,13),(13,20),(20,60)):
    m = flat & (ym>=lo) & (ym<hi)
    print("  y %2d..%2d : %8.0f m2" % (lo, hi, area[m].sum()))
