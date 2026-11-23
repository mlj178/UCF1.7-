# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy, os, struct, hashlib
DATA = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire_Data"
print("=== data_offset of game files ===")
for f in ["globalgamemanagers","level1","level10","level11","resources.assets","sharedassets1.assets"]:
    p = os.path.join(DATA, f)
    env = UnityPy.load(p); sf = list(env.files.values())[0]; h = sf.header
    print(f"  {f:24s} size={os.path.getsize(p):9d} data_offset={h.data_offset:6d} metadata={h.metadata_size:6d} objs={len(sf.objects)}")

PAT = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\work\globalgamemanagers.patched"
blob = bytearray(open(PAT, "rb").read())
meta_size, file_size, ver, data_off = struct.unpack_from("<IIII", blob, 0)
print("\npatched: meta", meta_size, "size", file_size, "ver", ver, "data_off", data_off)
entry = struct.pack("<qq", 1, 1264)
idx = blob.find(entry, 48, 48 + meta_size)
print("obj table at", idx)
if idx < 0: raise SystemExit("table not found")
n = 18
delta = 4096 - data_off
print("delta", delta)
for i in range(n):
    o = idx + i * 24
    pid, start, size, tid = struct.unpack_from("<qqII", blob, o)
    struct.pack_into("<q", blob, o + 8, start + delta)
blob = blob[:data_off] + b"\x00" * delta + blob[data_off:]
struct.pack_into("<I", blob, 12, 4096)
struct.pack_into("<I", blob, 4, len(blob))
OUT = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\work\globalgamemanagers.patched_aligned"
open(OUT, "wb").write(blob)
print("written", OUT, len(blob))
env = UnityPy.load(OUT); sf = list(env.files.values())[0]; h = sf.header
print("verify header:", h.data_offset, h.metadata_size, os.path.getsize(OUT))
for pid, oi in sorted(sf.objects.items())[:5]:
    print(f"   id={pid} start=0x{oi.byte_start:06x} size={oi.byte_size}")
o = [x for x in env.objects if x.type.name == "BuildSettings"][0]
raw = o.get_raw_data()
cnt = struct.unpack_from("<i", raw, 0)[0]
print("BuildSettings size", len(raw), "count", cnt)
print("last path:", raw[-200:].split(b"\x00")[0][-40:])
