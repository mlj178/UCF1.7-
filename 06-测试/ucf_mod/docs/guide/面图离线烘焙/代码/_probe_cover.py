
import json, struct, math, os, re, glob
import numpy as np
ROOT = r"D:/trae_project/ucf1.7-modifier"
GEO = glob.glob(os.path.join(ROOT, "06-*", "ucf_mod", "data", "geo", "web", "nano30_storm.bin"))[0]
USER = glob.glob(os.path.join(ROOT, "06-*", "ucf_mod", "data", "maps", "10_*", "n0-*.txt"))[0]

b = open(GEO, "rb").read()
ver, jl = struct.unpack_from("<II", b, 4)
js = json.loads(b[12:12+jl].decode("utf-8"))
off = (12 + jl + 3) & ~3
n, t = js["nverts"], js["ntris"]
pos = np.frombuffer(b, dtype="<f4", count=n*3, offset=off).reshape(n,3).astype(np.float64); off += n*12
off += n*3
if ver >= 2: off += n*8
off = (off + 3) & ~3
idx = np.frombuffer(b, dtype="<u4", count=t*3, offset=off).reshape(t,3)
tri = pos[idx]
nrm = np.cross(tri[:,1]-tri[:,0], tri[:,2]-tri[:,0])
ln = np.linalg.norm(nrm, axis=1); ln[ln==0]=1
up = nrm[:,1]/ln
area = ln/2
flat = (np.abs(up) >= math.cos(math.radians(45))) & (area > 0.02)
cs = 0.5
xmin, zmin = pos[:,0].min(), pos[:,2].min()
W = int(math.ceil((pos[:,0].max()-xmin)/cs))+1
H = int(math.ceil((pos[:,2].max()-zmin)/cs))+1
layers = {}
for t3, u in zip(tri[flat], up[flat]):
    xs, ys, zs = t3[:,0], t3[:,1], t3[:,2]
    i0 = max(0,int((xs.min()-xmin)/cs)); i1 = min(W-1,int((xs.max()-xmin)/cs))
    j0 = max(0,int((zs.min()-zmin)/cs)); j1 = min(H-1,int((zs.max()-zmin)/cs))
    if i1<i0 or j1<j0: continue
    cx = xmin + (np.arange(i0,i1+1)+0.5)*cs; cz = zmin + (np.arange(j0,j1+1)+0.5)*cs
    X, Z = np.meshgrid(cx, cz)
    d = (t3[1,2]-t3[2,2])*(t3[0,0]-t3[2,0]) + (t3[2,0]-t3[1,0])*(t3[0,2]-t3[2,2])
    if abs(d) < 1e-9: continue
    w0 = ((t3[1,2]-t3[2,2])*(X-t3[2,0]) + (t3[2,0]-t3[1,0])*(Z-t3[2,2]))/d
    w1 = ((t3[2,2]-t3[0,2])*(X-t3[2,0]) + (t3[0,0]-t3[2,0])*(Z-t3[2,2]))/d
    w2 = 1-w0-w1
    ins = (w0>=-1e-6)&(w1>=-1e-6)&(w2>=-1e-6)
    if not ins.any(): continue
    hy = w0*ys[0] + w1*ys[1] + w2*ys[2]
    jj, ii = np.nonzero(ins)
    for k in range(len(jj)):
        layers.setdefault((j0+int(jj[k]), i0+int(ii[k])), []).append((float(hy[jj[k],ii[k]]), bool(u > 0)))

pts = []
for line in open(USER, encoding="utf-8", errors="replace"):
    m = re.match(r"node add ([-\d.]+) ([-\d.]+) ([-\d.]+)", line.strip())
    if m: pts.append([float(x) for x in m.groups()])
pts = np.array(pts)
covered = 0; dists = []
for p in pts:
    j0 = int((p[2]-zmin)/cs); i0 = int((p[0]-xmin)/cs)
    best = None
    for dj in range(-3,4):
        for di in range(-3,4):
            hs = layers.get((j0+dj, i0+di))
            if not hs: continue
            for h, isf in hs:
                if not isf: continue
                d = math.hypot(di*cs, dj*cs) + abs(h-p[1])*0.5
                if best is None or d < best: best = d
    if best is None: dists.append(99); continue
    dists.append(best)
    if best <= 1.2: covered += 1
dists = np.array(dists)
print("cells with surfaces", len(layers))
print("user points", len(pts), "covered(<=1.2 cost)", covered, "(%.0f%%)" % (100*covered/len(pts)))
print("cost percentiles 50/75/90:", np.percentile(dists,[50,75,90]).round(2))
