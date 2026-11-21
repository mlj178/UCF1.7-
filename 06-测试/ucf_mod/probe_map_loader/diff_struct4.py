# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy, os, hashlib
GAME = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire_Data\globalgamemanagers"
PAT  = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\work\globalgamemanagers.patched"
for tag, p in [("orig", GAME), ("patched", PAT)]:
    env = UnityPy.load(p); sf = list(env.files.values())[0]
    h = sf.header
    print(f"--- {tag} size={os.path.getsize(p)} data_offset={h.data_offset} metadata_size={h.metadata_size} endian={h.endian} ver={h.version}")
    for pid, oi in sorted(sf.objects.items()):
        name = oi.type.name if hasattr(oi.type, "name") else str(oi.type)
        print(f"    id={pid:<4d} start=0x{oi.byte_start:06x} size={oi.byte_size:7d} {name}")
