# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy, os, hashlib
GAME = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire_Data\globalgamemanagers"
PAT  = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\work\globalgamemanagers.patched"
info = {}
for tag, p in [("orig", GAME), ("patched", PAT)]:
    env = UnityPy.load(p); sf = list(env.files.values())[0]
    h = sf.header
    print(f"--- {tag} size={os.path.getsize(p)} header={h.__dict__}")
    objs = sorted(env.objects, key=lambda x: x.path_id)
    rows = {}
    for o in objs:
        d = o.get_raw_data()
        rows[o.path_id] = (o.type.name, len(d), hashlib.md5(d).hexdigest()[:8], o.reader.byte_start)
    info[tag] = rows
    for pid, (tn, sz, md5, off) in rows.items():
        print(f"    {tn:28s} id={pid:<4d} off=0x{(off or 0):06x} size={sz:7d} {md5}")
print("\n=== diff ===")
for pid in sorted(info["orig"]):
    a = info["orig"][pid]; b = info["patched"].get(pid)
    if not b: print("missing", pid); continue
    if a[2] != b[2] or a[1] != b[1]:
        print(f"  CHANGED {a[0]} id={pid} size {a[1]}->{b[1]} off 0x{a[3]:x}->0x{b[3]:x}")
