
import struct, hashlib, glob, os
def info(p):
    b = open(p,"rb").read()
    ver, jl, nv, nt = struct.unpack_from("<IIII", b, 4)
    js = b[20:20+jl].decode("utf-8","replace")
    return dict(path=os.path.basename(p), size=len(b), ver=ver, nv=nv, nt=nt,
                json=js[:90], md5=hashlib.md5(b).hexdigest()[:12])
a = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/unity-navmesh/recast.navmesh")[0]
b = glob.glob("D:/trae_project/ucf1.7-modifier/06-*/ucf_mod/data/maps/10_*Storm*/navmesh_auto.bin")[0]
for p in (a, b):
    d = info(p)
    print("%-18s size %7d  ver %d  verts %6d  tris %5d  md5 %s" % (d["path"], d["size"], d["ver"], d["nv"], d["nt"], d["md5"]))
    print("    json:", d["json"])
