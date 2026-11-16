
import json, struct, os
p = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod\\geo\\web\\practice.bin"
d = open(p,"rb").read()
assert d[:4] == b"UCFG", "magic"
ver, jl = struct.unpack_from("<II", d, 4)
hdr = json.loads(d[12:12+jl].decode("utf-8"))
off = 12 + jl
off += (4 - off % 4) % 4
n, t = hdr["nverts"], hdr["ntris"]
pos_off = off; off += n*12
nrm_off = off; off += n*3
off += (4 - off % 4) % 4
idx_off = off
print("ver", ver, "n", n, "t", t, "idx_off", idx_off, "need", idx_off + t*12, "have", len(d))
print("bbox", hdr["bbox"], "chunks", [(c["name"], c["start"], c["count"]) for c in hdr["chunks"]])
# 检查索引范围
maxi = 0
for i in range(t*3):
    v = struct.unpack_from("<I", d, idx_off + i*4)[0]
    maxi = max(maxi, v)
print("max_index", maxi, "ok" if maxi < n else "BAD")
