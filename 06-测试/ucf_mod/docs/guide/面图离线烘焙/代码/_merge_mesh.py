
import struct
import numpy as np
def read(p):
    b=open(p,"rb").read(); ver,jl,nv,nt=struct.unpack_from("<IIII",b,4)
    V=np.frombuffer(b,dtype="<f4",count=nv*3,offset=20+jl).reshape(nv,3)
    T=np.frombuffer(b,dtype="<u4",count=nt*3,offset=20+jl+nv*12).reshape(nt,3)
    return V,T
files=[r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/面图离线烘焙/out/fine/nano30_storm.navmesh",
       r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/面图离线烘焙/out/upper/sweep_upper.navmesh"]
Vs=[];Ts=[];off=0
for f in files:
    V,T=read(f); Vs.append(V); Ts.append(T+off); off+=len(V)
V=np.concatenate(Vs); T=np.concatenate(Ts)
head=b'{"map":"nano30_storm","merged":2}'
out=r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/面图离线烘焙/out/merged.navmesh"
open(out,"wb").write(b"UCFN"+struct.pack("<IIII",2,len(head),len(V),len(T))+head+V.astype("<f4").tobytes()+T.astype("<u4").tobytes())
print("merged verts",len(V),"tris",len(T))
