# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy, os, hashlib
GAME = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire_Data\globalgamemanagers"
PAT  = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\work\globalgamemanagers.patched"
for tag, p in [("orig", GAME), ("patched", PAT)]:
    env = UnityPy.load(p); sf = list(env.files.values())[0]
    print(f"--- {tag}  size={os.path.getsize(p)}")
    for k in ("header",):
        h = getattr(sf, k, None)
        if h is not None:
            print("  header:", {kk: getattr(h, kk) for kk in dir(h) if kk.startswith("m_")})
    objs = sorted(env.objects, key=lambda x: x.path_id)
    print("  objects:", len(objs))
    for o in objs:
        d = o.get_raw_data()
        print(f"    {o.type.name:28s} id={o.path_id:<4d} off=0x{o.byte_offset:06x} size={len(d):7d} md5={hashlib.md5(d).hexdigest()[:10]}")
