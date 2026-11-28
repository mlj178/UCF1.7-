
import re, glob, struct
import numpy as np
from PIL import Image, ImageDraw
p = glob.glob("D:/trae_project/ucf1.7-modifier/00-*/地图3D资源导出/AssetRipper工程/ExportedProject/Assets/Resources/DesertFort_Navmesh.asset")[0]
t = open(p, encoding="utf-8", errors="replace").read()
# 顶点数据
m = re.search(r"m_VertexData:\s*\n(.*?)m_IndexBuffer:", t, re.S)
blk = m.group(1)
vc = int(re.search(r"m_VertexCount:\s*(\d+)", blk).group(1))
data = re.search(r"_typelessdata:\s*([0-9a-fA-F]+)", blk)
raw = bytes.fromhex(data.group(1))
chans = re.findall(r"- stream:\s*\d+\s*\n\s*offset:\s*(\d+)\s*\n\s*format:\s*(\d+)\s*\n\s*dimension:\s*(\d+)", blk)
print("verts", vc, "channels", len(chans), "data bytes", len(raw))
off0 = int(chans[0][0]); dim0 = int(chans[0][2])
stride = int(re.search(r"stride:\s*(\d+)", blk).group(1)) if re.search(r"stride:\s*(\d+)", blk) else 0
print("stride", stride, "off0", off0, "dim0", dim0)
V = np.zeros((vc,3), dtype=np.float32)
for i in range(vc):
    o = i*stride + off0
    V[i] = struct.unpack_from("<3f", raw, o)
ib = re.search(r"m_IndexBuffer:\s*([0-9a-fA-F]+)", t).group(1)
idx = np.frombuffer(bytes.fromhex(ib), dtype="<u2").reshape(-1,3)
print("tris", len(idx))
tri = V[idx]
n = np.cross(tri[:,1]-tri[:,0], tri[:,2]-tri[:,0])
area = np.linalg.norm(n, axis=1)/2
print("area %.0f m2  bbox x %.0f..%.0f z %.0f..%.0f y %.1f..%.1f" % (
    area.sum(), V[:,0].min(), V[:,0].max(), V[:,2].min(), V[:,2].max(), V[:,1].min(), V[:,1].max()))
print("avg tri %.2f m2" % (area.sum()/len(idx)))
