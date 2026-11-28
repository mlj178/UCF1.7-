
import re, glob, struct
import numpy as np
from PIL import Image, ImageDraw

def parse_native(p):
    t = open(p, encoding="utf-8", errors="replace").read()
    vc = int(re.search(r"m_VertexCount:\s*(\d+)", t).group(1))
    raw = bytes.fromhex(re.search(r"_typelessdata:\s*([0-9a-fA-F]+)", t).group(1))
    stride = len(raw) // vc
    V = np.zeros((vc,3), dtype=np.float32)
    for i in range(vc):
        V[i] = struct.unpack_from("<3f", raw, i*stride)
    ib = bytes.fromhex(re.search(r"m_IndexBuffer:\s*([0-9a-fA-F]+)", t).group(1))
    idx = np.frombuffer(ib, dtype="<u2").reshape(-1,3)
    return V, idx

p = glob.glob("D:/trae_project/ucf1.7-modifier/00-*/地图3D资源导出/AssetRipper工程/ExportedProject/Assets/Resources/DesertFort_Navmesh.asset")[0]
V, T = parse_native(p)
tri = V[T]
n = np.cross(tri[:,1]-tri[:,0], tri[:,2]-tri[:,0]); area = np.linalg.norm(n,axis=1)/2
print("native DesertFort: verts %d tris %d area %.0f m2  mean tri %.2f m2  bbox %.0f..%.0f x %.0f..%.0f" % (
    len(V), len(T), area.sum(), area.mean(), V[:,0].min(), V[:,0].max(), V[:,2].min(), V[:,2].max()))

# 我们当前的
q = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/10_*Storm*/navmesh_auto.bin")[0]
b = open(q,"rb").read(); ver,jl,nv,nt = struct.unpack_from("<IIII", b, 4)
MV = np.frombuffer(b,dtype="<f4",count=nv*3,offset=20+jl).reshape(nv,3)
MT = np.frombuffer(b,dtype="<u4",count=nt*3,offset=20+jl+nv*12).reshape(nt,3)
mt = MV[MT]
mn = np.cross(mt[:,1]-mt[:,0], mt[:,2]-mt[:,0]); ma = np.linalg.norm(mn,axis=1)/2
print("ours:              verts %d tris %d area %.0f m2  mean tri %.2f m2" % (nv, nt, ma.sum(), ma.mean()))

def draw(V, T, path, col):
    W=H=700; img=Image.new("RGB",(W,H),(0,0,0)); dr=ImageDraw.Draw(img,"RGBA")
    x0,x1=V[:,0].min(),V[:,0].max(); z0,z1=V[:,2].min(),V[:,2].max()
    s=min((W-20)/(x1-x0+1e-6),(H-20)/(z1-z0+1e-6))
    for t in V[T]:
        pts=[(10+(t[0,0]-x0)*s,10+(t[0,2]-z0)*s),(10+(t[1,0]-x0)*s,10+(t[1,2]-z0)*s),(10+(t[2,0]-x0)*s,10+(t[2,2]-z0)*s)]
        dr.polygon(pts, fill=col+(90,), outline=col+(200,))
    img.save(path)
draw(V, T, r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/面图离线烘焙/out/cmp_native.png", (90,180,90))
draw(MV, MT, r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/面图离线烘焙/out/cmp_ours.png", (200,120,60))
print("saved comparison images")
