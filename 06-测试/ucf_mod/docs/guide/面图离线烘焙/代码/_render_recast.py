
import struct, glob
import numpy as np
from PIL import Image, ImageDraw
p = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/10_*Storm*/navmesh_auto.bin")[0]
b=open(p,"rb").read(); ver,jl,nv,nt=struct.unpack_from("<IIII",b,4)
V=np.frombuffer(b,dtype="<f4",count=nv*3,offset=20+jl).reshape(nv,3)
T=np.frombuffer(b,dtype="<u4",count=nt*3,offset=20+jl+nv*12).reshape(nt,3)
tri=V[T]
n=np.cross(tri[:,1]-tri[:,0], tri[:,2]-tri[:,0])
area=np.linalg.norm(n,axis=1)/2
print("navmesh: verts %d tris %d area %.0f m2" % (nv,nt,area.sum()))
print("bbox x %.1f..%.1f  z %.1f..%.1f  y %.1f..%.1f" % (V[:,0].min(),V[:,0].max(),V[:,2].min(),V[:,2].max(),V[:,1].min(),V[:,1].max()))
# 高度分布
ym = tri[:,:,1].mean(1)
for lo,hi in ((-5,3),(3,8),(8,15),(15,60)):
    m=(ym>=lo)&(ym<hi)
    print("  y %2d..%2d: %6d tris  %7.0f m2" % (lo,hi,int(m.sum()),area[m].sum()))
# 渲染俯视图
W,H=900,900
img=Image.new("RGB",(W,H),(0,0,0)); dr=ImageDraw.Draw(img,"RGBA")
x0,x1=V[:,0].min(),V[:,0].max(); z0,z1=V[:,2].min(),V[:,2].max()
sx=(W-20)/(x1-x0+1e-6); sz=(H-20)/(z1-z0+1e-6); s=min(sx,sz)
def P(x,z): return (10+(x-x0)*s, 10+(z-z0)*s)
for t in tri:
    pts=[P(t[0,0],t[0,2]),P(t[1,0],t[1,2]),P(t[2,0],t[2,2])]
    dr.polygon(pts, fill=(90,180,90,110), outline=(40,120,40,180))
img.save(r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/面图离线烘焙/out/recast_top.png")
print("saved recast_top.png")
