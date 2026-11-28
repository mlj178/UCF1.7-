# -*- coding: utf-8 -*-
# 把 storm 的地图几何（UCFG/npz）导成 OBJ，给 Unity 的 Recast 烘焙用
import glob, struct
src = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/geo/nano30_storm.npz")[0]
import numpy as np
z = np.load(src, allow_pickle=True)
V, F = z["v"].astype("float64"), z["f"].astype("int64")
out = "D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/unity-navmesh/Assets/map_geometry.obj"
with open(out, "w", encoding="utf-8") as f:
    f.write("# Nano30_Storm map geometry (%d tris)\n" % len(F))
    for i in range(len(V)):
        f.write("v %.4f %.4f %.4f\n" % (V[i,0], V[i,1], V[i,2]))
    for i in range(len(F)):
        f.write("f %d %d %d\n" % (F[i,0]+1, F[i,1]+1, F[i,2]+1))
print("wrote", out, "verts", len(V), "tris", len(F))
