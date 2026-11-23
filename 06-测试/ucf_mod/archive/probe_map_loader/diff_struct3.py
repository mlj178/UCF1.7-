# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy, os, hashlib
GAME = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire_Data\globalgamemanagers"
PAT  = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\work\globalgamemanagers.patched"
info = {}
def hd(h):
    out = {}
    for k in dir(h):
        if k.startswith("__"): continue
        try:
            v = getattr(h, k)
            if not callable(v): out[k] = v
        except Exception: pass
    return out
for tag, p in [("orig", GAME), ("patched", PAT)]:
    env = UnityPy.load(p); sf = list(env.files.values())[0]
    print(f"--- {tag} size={os.path.getsize(p)}")
    print("   header:", hd(sf.header))
    rows = {}
    for o in sorted(env.objects, key=lambda x: x.path_id):
        d = o.get_raw_data()
        rows[o.path_id] = (o.type.name, len(d), hashlib.md5(d).hexdigest()[:8], o.reader.byte_start)
    info[tag] = rows
print("\n=== per-object ===")
for pid in sorted(info["orig"]):
    a = info["orig"][pid]; b = info["patched"].get(pid)
    flag = "  " if b and (a[1]==b[1] and a[2]==b[2]) else "**"
    print(f"{flag} id={pid:<4d} {a[0]:28s} off 0x{(a[3] or 0):06x} -> 0x{(b[3] if b else 0) or 0:06x}  size {a[1]:7d} -> {(b[1] if b else -1):7d}")
