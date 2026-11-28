
import glob, math, struct
import numpy as np
npz = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/geo/nano30_storm.npz")[0]
z = np.load(npz, allow_pickle=True)
V, F = z["v"].astype(np.float64), z["f"].astype(np.int64)
tri = V[F]
n = np.cross(tri[:,1]-tri[:,0], tri[:,2]-tri[:,0])
ln = np.linalg.norm(n, axis=1); ln[ln==0]=1
un = n/ln[:,None]; area = ln/2
flat = (np.abs(un[:,1]) > math.cos(math.radians(45))) & (area > 0.02)
ym = tri[:,:,1].mean(1)
cx, cz = (V[:,0].min()+V[:,0].max())/2, (V[:,2].min()+V[:,2].max())/2
quad = {}
for name, m in (("NW", (tri[:,:,0].mean(1) < cx) & (tri[:,:,2].mean(1) > cz)),
                ("NE", (tri[:,:,0].mean(1) >= cx) & (tri[:,:,2].mean(1) > cz)),
                ("SW", (tri[:,:,0].mean(1) < cx) & (tri[:,:,2].mean(1) <= cz)),
                ("SE", (tri[:,:,0].mean(1) >= cx) & (tri[:,:,2].mean(1) <= cz))):
    sel = flat & (ym > -1) & (ym < 3) & m
    quad[name] = area[sel].sum()
print("geometry flat area at ground (-1..3m) by quadrant:")
for k, v in quad.items(): print("  %s %8.0f m2" % (k, v))

nv = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/docs/guide/*/out/nano30_storm/nano30_storm.navmesh")[0]
b = open(nv, "rb").read()
ver, jl, nvv, ntt = struct.unpack_from("<IIII", b, 4)
MV = np.frombuffer(b, dtype="<f4", count=nvv*3, offset=20+jl).reshape(nvv,3).astype(np.float64)
MT = np.frombuffer(b, dtype="<u4", count=ntt*3, offset=20+jl+nvv*12).reshape(ntt,3)
mt = MV[MT]
mn = np.cross(mt[:,1]-mt[:,0], mt[:,2]-mt[:,0]) / 2
ma = np.linalg.norm(mn, axis=1)
print("navmesh area by quadrant:")
for name, m in (("NW", (mt[:,:,0].mean(1) < cx) & (mt[:,:,2].mean(1) > cz)),
                ("NE", (mt[:,:,0].mean(1) >= cx) & (mt[:,:,2].mean(1) > cz)),
                ("SW", (mt[:,:,0].mean(1) < cx) & (mt[:,:,2].mean(1) <= cz)),
                ("SE", (mt[:,:,0].mean(1) >= cx) & (mt[:,:,2].mean(1) <= cz))):
    print("  %s %8.0f m2" % (name, ma[m].sum()))
