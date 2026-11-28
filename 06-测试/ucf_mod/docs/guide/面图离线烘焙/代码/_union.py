
import struct
import numpy as np
def read(p):
    b=open(p,"rb").read(); ver,jl,nv,nt=struct.unpack_from("<IIII",b,4)
    V=np.frombuffer(b,dtype="<f4",count=nv*3,offset=20+jl).reshape(nv,3)
    T=np.frombuffer(b,dtype="<u4",count=nt*3,offset=20+jl+nv*12).reshape(nt,3)
    return V,T
scan = r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/面图离线烘焙/out/nano30_storm/sweep.navmesh"
recast = r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/unity-navmesh/recast.navmesh"
Vs=[]; Ts=[]; off=0
for p in (scan, recast):
    V,T=read(p); Vs.append(V); Ts.append(T+off); off+=len(V)
V=np.concatenate(Vs); T=np.concatenate(Ts)
out=r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/面图离线烘焙/out/union.navmesh"
head=b'{"map":"nano30_storm","union":"scan+recast"}'
open(out,"wb").write(b"UCFN"+struct.pack("<IIII",2,len(head),len(V),len(T))+head+V.astype("<f4").tobytes()+T.astype("<u4").tobytes())
print("union verts",len(V),"tris",len(T),"size",len(open(out,'rb').read()))
