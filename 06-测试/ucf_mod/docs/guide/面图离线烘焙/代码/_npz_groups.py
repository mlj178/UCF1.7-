
import glob, numpy as np, collections
p = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/geo/nano30_storm.npz")[0]
z = np.load(p, allow_pickle=True)
V, F, G = z["v"], z["f"], z["g"]
print("verts", len(V), "tris", len(F), "groups", len(set(G.tolist())))
tri = V[F]
n = np.cross(tri[:,1]-tri[:,0], tri[:,2]-tri[:,0])
area = np.linalg.norm(n, axis=1) / 2
up = n[:,1] / np.maximum(np.linalg.norm(n,axis=1),1e-9)
flat = np.abs(up) > 0.7
print("total area %.0f m2 | flat %.0f m2" % (area.sum(), area[flat].sum()))
# per group
G = G.astype(int)
for g in sorted(set(G.tolist())):
    m = G == g
    a = area[m].sum(); fa = area[m & flat].sum()
    ys = tri[m][:, :, 1]
    print("  group %3d: tris %6d area %8.0f flat %8.0f y[%.1f..%.1f]" % (
        g, int(m.sum()), a, fa, float(ys.min()), float(ys.max())))
print("--- area by height (flat tris) ---")
h = tri[flat][:, :, 1].mean(axis=1)
bins = np.arange(-10, 30, 2)
hist, edges = np.histogram(h, bins=bins, weights=area[flat])
for i in range(len(hist)):
    if hist[i] > 50:
        print("  y %4.0f..%4.0f : %6.0f m2" % (edges[i], edges[i+1], hist[i]))
