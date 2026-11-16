
import json, struct
d = open(r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod\\geo\\web\\practice.bin","rb").read()
ver, jl = struct.unpack_from("<II", d, 4)
hdr = json.loads(d[12:12+jl].decode("utf-8"))
off = 12 + jl; off += (4 - off % 4) % 4
n, t = hdr["nverts"], hdr["ntris"]
ys = struct.unpack_from("<%df" % (n*3), d, off)
ys = [ys[i*3+1] for i in range(n)]
def survive(lo, hi):
    c = 0
    for k in range(t):
        base = k*3
        if all(lo <= ys[base+i] <= hi for i in range(3)): c += 1
    return c
print("triangles:", t, "y range:", min(ys), max(ys))
print("旧 band (1e9, -1e9) 存活:", survive(1e9-2, -1e9+2))
print("新 band (-2, 5)     存活:", survive(-2, 5))
