
import glob, struct, math
import numpy as np
nv = "D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/data/maps/10_Nano30_Storm飓风危城/navmesh_auto.bin"
b=open(nv,"rb").read(); ver,jl,nvv,ntt=struct.unpack_from("<IIII",b,4)
V=np.frombuffer(b,dtype="<f4",count=nvv*3,offset=20+jl).reshape(nvv,3)
T=np.frombuffer(b,dtype="<u4",count=ntt*3,offset=20+jl+nvv*12).reshape(ntt,3)
print("mesh verts",len(V),"tris",len(T))
# 邻接格
cell={}
cs=1.5
xmin,zmin=V[:,0].min(),V[:,2].min()
for ti,t in enumerate(T):
    p=V[t]; i0=int((p[:,0].min()-xmin)/cs); i1=int((p[:,0].max()-xmin)/cs)
    j0=int((p[:,2].min()-zmin)/cs); j1=int((p[:,2].max()-zmin)/cs)
    for j in range(j0,j1+1):
        for i in range(i0,i1+1):
            cell.setdefault((j,i),[]).append(ti)
def under(x,z):
    i=int((x-xmin)/cs); j=int((z-zmin)/cs)
    out=[]
    for ti in cell.get((j,i),()):
        p=V[T[ti]]
        d=(p[1,2]-p[2,2])*(p[0,0]-p[2,0])+(p[2,0]-p[1,0])*(p[0,2]-p[2,2])
        if abs(d)<1e-9: continue
        a=((p[1,2]-p[2,2])*(x-p[2,0])+(p[2,0]-p[1,0])*(z-p[2,2]))/d
        bb=((p[2,2]-p[0,2])*(x-p[2,0])+(p[0,0]-p[2,0])*(z-p[2,2]))/d
        c=1-a-bb
        if a>=-1e-6 and bb>=-1e-6 and c>=-1e-6:
            out.append(a*p[0,1]+bb*p[1,1]+c*p[2,1])
    return out
for name,(x,y,z) in (("stuck1",(6.2,2.56,-23.2)),("stuck2",(-3.0,2.57,-7.5))):
    hs=under(x,z)
    print(name, (x,y,z), "mesh ys:", [round(h,2) for h in hs] or "NONE")
# 最近节点
mp="D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/data/maps/10_Nano30_Storm飓风危城/n0-0000000000000000.txt"
N=[]
for line in open(mp,encoding="utf-8",errors="replace"):
    s=line.strip()
    if s.startswith("node add "):
        v=[float(q) for q in s.split()[2:5]]; N.append(v)
N=np.array(N)
print("nodes",len(N))
for name,(x,y,z) in (("stuck1",(6.2,2.56,-23.2)),("stuck2",(-3.0,2.57,-7.5))):
    P=np.array([x,y,z]); d=np.linalg.norm(N-P,axis=1); dxz=np.linalg.norm(N[:,[0,2]]-P[[0,2]],axis=1)
    print(name,"nearest3d %.2f dxz %.2f dy %.2f"%(d.min(),dxz.min(),abs(N[d.argmin(),1]-y)))
