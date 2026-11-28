# -*- coding: utf-8 -*-
import struct, os
src = r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/data/maps/10_Nano30_Storm飓风危城/navmesh_auto.bin"
b = open(src, "rb").read()
ver, jl, nv, nt = struct.unpack_from("<IIII", b, 4)
V = struct.unpack_from("<%df" % (nv*3), b, 20+jl)
T = struct.unpack_from("<%dI" % (nt*3), b, 20+jl+nv*12)
out = r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/面图离线烘焙/out/Nano30_Storm_NavMesh.obj"
with open(out, "w", encoding="utf-8") as f:
    f.write("# UCF baked navmesh for Nano30_Storm\n")
    f.write("# verts %d tris %d\n" % (nv, nt))
    for i in range(nv):
        # Unity(左手) -> OBJ(右手)：Z 取反，Unity 导入时再翻回来
        f.write("v %.4f %.4f %.4f\n" % (V[i*3], V[i*3+1], -V[i*3+2]))
    for i in range(nt):
        f.write("f %d %d %d\n" % (T[i*3]+1, T[i*3+2]+1, T[i*3+1]+1))
print("wrote", out, "verts", nv, "tris", nt)
