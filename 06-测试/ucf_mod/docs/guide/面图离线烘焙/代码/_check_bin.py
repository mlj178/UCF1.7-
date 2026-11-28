
import struct
p = r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/data/maps/10_Nano30_Storm飓风危城/navmesh_auto.bin"
b = open(p, "rb").read()
magic = b[:4]
ver, jl, nv, nt = struct.unpack_from("<IIII", b, 4)
print("magic", magic, "ver", ver, "jsonLen", jl, "nv", nv, "nt", nt, "size", len(b))
need = 20 + jl + nv*12 + nt*12
print("expected size", need, "match", need == len(b))
print("json", b[20:20+jl][:160])
