# -*- coding: utf-8 -*-
import glob, math, collections
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
horiz = np.abs(un[:,1]) >= cos_s          # 上下都算水平面
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

# vs 墙：竖直面仍然用带法线的
vert = tri[~horiz]
hs_all = raster(tri[horiz])
wa = raster(vert)
lo={}; hi={}
for k,hs in wa.items(): lo[k]=min(hs); hi[k]=max(hs)
print("horizontal cells", len(hs_all))

for head in (1.5, 1.8):
    walk=0; heights=[]; wallrej=0
    for k, hs in hs_all.items():
        hs=sorted(hs); m=[]
        for h in hs:
            if m and abs(h-m[-1])<=0.3: m[-1]=(m[-1]+h)/2
            else: m.append(h)
        for i,h in enumerate(m):
            nxt = m[i+1] if i+1<len(m) else None
            if nxt is not None and nxt-h < head: continue
            if k in lo and hi[k] > h+0.1 and lo[k] < h+head: wallrej+=1; continue
            walk+=1; heights.append(round(h,0)); break
    print("head %.1f -> walkable cells %d | by height %s" % (head, walk, dict(sorted(collections.Counter(heights).items())[:0]) or ""))
    c=collections.Counter(heights)
    print("   low(<=2m): %d  mid(3-9): %d  high(>=10): %d" % (
        sum(v for k,v in c.items() if k<=2), sum(v for k,v in c.items() if 3<=k<=9), sum(v for k,v in c.items() if k>=10)))
