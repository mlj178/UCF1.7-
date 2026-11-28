
r"""_cover.py - 烘出来的面到底盖住了多少"玩家真实走过的地面"

真值 = log/ground_samples_<图>.txt（跟随采样，玩家脚下的碰撞面）。
判据 = 面在这个 (x,z) 上的高度和真值差 < 0.8 m（双层建筑会互相挡住，属于已知误判）。
用法：python _cover.py            # 自动找最新的 ground_samples_*.txt 和 storm 的面
"""
import glob, os, struct
import numpy as np
# 真值：跟随采样优先；没有才退回旧的整图扫描
p = sorted(glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/log/ground_samples_*.txt"),
           key=os.path.getmtime, reverse=True)
if p:
    p = p[0]
else:
    p = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/10_*Storm*/ground_low.txt")[0]
pts=[]
for line in open(p,encoding="utf-8",errors="replace"):
    s=line.strip()
    if not s or s.startswith("#"): continue
    a=s.split()
    pts.append((float(a[0]),float(a[1]),float(a[2])))
pts=np.array(pts)
# recast 面
b=open(glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/10_*Storm*/navmesh_auto.bin")[0],"rb").read()
ver,jl,nv,nt=struct.unpack_from("<IIII",b,4)
V=np.frombuffer(b,dtype="<f4",count=nv*3,offset=20+jl).reshape(nv,3).astype(np.float64)
T=np.frombuffer(b,dtype="<u4",count=nt*3,offset=20+jl+nv*12).reshape(nt,3)
# 粗网格索引
cs=2.0
x0,z0=V[:,0].min(),V[:,2].min()
cell={}
for ti,t in enumerate(T):
    tri=V[t]
    i0=int((tri[:,0].min()-x0)/cs); i1=int((tri[:,0].max()-x0)/cs)
    j0=int((tri[:,2].min()-z0)/cs); j1=int((tri[:,2].max()-z0)/cs)
    for j in range(j0,j1+1):
        for i in range(i0,i1+1):
            cell.setdefault((j,i),[]).append(ti)
def height_at(x,z):
    i=int((x-x0)/cs); j=int((z-z0)/cs)
    for ti in cell.get((j,i),()):
        t=V[T[ti]]
        d=(t[1,2]-t[2,2])*(t[0,0]-t[2,0])+(t[2,0]-t[1,0])*(t[0,2]-t[2,2])
        if abs(d)<1e-9: continue
        a=((t[1,2]-t[2,2])*(x-t[2,0])+(t[2,0]-t[1,0])*(z-t[2,2]))/d
        bb=((t[2,2]-t[0,2])*(x-t[2,0])+(t[0,0]-t[2,0])*(z-t[2,2]))/d
        c=1-a-bb
        if a>=-1e-6 and bb>=-1e-6 and c>=-1e-6: return a*t[0,1]+bb*t[1,1]+c*t[2,1]
    return None
hit=0
for x,z,y in pts:
    h=height_at(x,z)
    if h is not None and abs(h-y)<0.8: hit+=1
print("真值 %s" % os.path.basename(p))
print("真值点 %d 个 | 面覆盖 %d 个（%.0f%%）" % (len(pts), hit, 100*hit/len(pts)))
