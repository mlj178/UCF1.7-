
import glob, struct
import numpy as np
from PIL import Image, ImageDraw
p = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/10_*Storm*/navmesh_auto.bin")[0]
b=open(p,"rb").read(); ver,jl,nv,nt=struct.unpack_from("<IIII",b,4)
V=np.frombuffer(b,dtype="<f4",count=nv*3,offset=20+jl).reshape(nv,3).astype(np.float64)
T=np.frombuffer(b,dtype="<u4",count=nt*3,offset=20+jl+nv*12).reshape(nt,3)
tri=V[T]
n=np.cross(tri[:,1]-tri[:,0], tri[:,2]-tri[:,0]); area=np.linalg.norm(n,axis=1)/2
print("union: verts %d tris %d area %.0f m2" % (nv,nt,area.sum()))
W=H=700; img=Image.new("RGB",(W,H),(0,0,0)); dr=ImageDraw.Draw(img,"RGBA")
x0,x1=V[:,0].min(),V[:,0].max(); z0,z1=V[:,2].min(),V[:,2].max()
s=min((W-20)/(x1-x0+1e-6),(H-20)/(z1-z0+1e-6))
for t in tri:
    pts=[(10+(t[0,0]-x0)*s,10+(t[0,2]-z0)*s),(10+(t[1,0]-x0)*s,10+(t[1,2]-z0)*s),(10+(t[2,0]-x0)*s,10+(t[2,2]-z0)*s)]
    dr.polygon(pts, fill=(90,180,90,80), outline=(60,140,60,160))
img.save(r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/面图离线烘焙/out/union_top.png")
print("saved union_top.png")
