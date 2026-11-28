# -*- coding: utf-8 -*-
import glob, math, json
import numpy as np

npz = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/geo/nano30_storm.npz")[0]
z = np.load(npz, allow_pickle=True)
V, F = z["v"].astype(np.float64), z["f"].astype(np.int64)
tri = V[F]
n = np.cross(tri[:,1]-tri[:,0], tri[:,2]-tri[:,0])
ln = np.linalg.norm(n, axis=1); ln[ln==0]=1
un = n/ln[:,None]; area = ln/2
ok = (area > 0.02) & (np.abs(un[:,1]) > 0.02)
tri, un, area = tri[ok], un[ok], area[ok]
cs = 1.0
cos_s = math.cos(math.radians(45))
flat = np.abs(un[:,1]) >= cos_s
floor_t, ceil_t, wall_t = tri[flat & (un[:,1] > 0)], tri[flat & (un[:,1] < 0)], tri[~flat]
xmin, zmin = float(V[:,0].min()), float(V[:,2].min())
W = int(math.ceil((V[:,0].max()-xmin)/cs))+1
H = int(math.ceil((V[:,2].max()-zmin)/cs))+1

def raster(ts):
    out = {}
    for t in ts:
        xs, ys, zs = t[:,0], t[:,1], t[:,2]
        i0 = max(0,int((xs.min()-xmin)/cs)); i1 = min(W-1,int((xs.max()-xmin)/cs))
        j0 = max(0,int((zs.min()-zmin)/cs)); j1 = min(H-1,int((zs.max()-zmin)/cs))
        if i1<i0 or j1<j0: continue
        cx = xmin+(np.arange(i0,i1+1)+0.5)*cs; cz = zmin+(np.arange(j0,j1+1)+0.5)*cs
        X,Z = np.meshgrid(cx,cz)
        d = (t[1,2]-t[2,2])*(t[0,0]-t[2,0]) + (t[2,0]-t[1,0])*(t[0,2]-t[2,2])
        if abs(d)<1e-9: continue
        w0 = ((t[1,2]-t[2,2])*(X-t[2,0]) + (t[2,0]-t[1,0])*(Z-t[2,2]))/d
        w1 = ((t[2,2]-t[0,2])*(X-t[2,0]) + (t[0,0]-t[2,0])*(Z-t[2,2]))/d
        w2 = 1-w0-w1
        ins = (w0>=-1e-6)&(w1>=-1e-6)&(w2>=-1e-6)
        if not ins.any(): continue
        hy = w0*ys[0]+w1*ys[1]+w2*ys[2]
        jj, ii = np.nonzero(ins)
        for k in range(len(jj)):
            out.setdefault((j0+int(jj[k]), i0+int(ii[k])), []).append(float(hy[jj[k],ii[k]]))
    return out

fl = raster(floor_t); ce = raster(ceil_t); wa = raster(wall_t)
print("floor cells", len(fl), "ceil cells", len(ce), "wall cells", len(wa))
lo = {}; hi = {}
for k, hs in wa.items():
    lo[k] = min(hs); hi[k] = max(hs)
lowceil = wall = none = 0
walkable = 0
heights = []
for k, hs in fl.items():
    hs = sorted(hs)
    merged = []
    for h in hs:
        if merged and abs(h-merged[-1]) <= 0.3: merged[-1] = (merged[-1]+h)/2
        else: merged.append(h)
    got = False
    for i, h in enumerate(merged):
        nxt = merged[i+1] if i+1 < len(merged) else None
        if nxt is not None and nxt-h < 1.8:
            lowceil += 1; continue
        if k in lo and hi[k] > h+0.1 and lo[k] < h+1.8:
            wall += 1; continue
        walkable += 1; got = True; heights.append(round(h,0)); break
    if not got: none += 1
print("floor cells", len(fl), "| walkable", walkable, "| rejected lowceil", lowceil, "wall", wall, "| none", none)
import collections
print("walkable by height:", dict(sorted(collections.Counter(heights).items())))
