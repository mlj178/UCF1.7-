# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
SRC = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
env0 = UnityPy.load(SRC + "globalgamemanagers.assets")
ms = {}
for o in env0.objects:
    if o.type.name == "MonoScript":
        try: ms[o.path_id] = o.read().m_ClassName
        except Exception: ms[o.path_id] = "?"
env = UnityPy.load(SRC + "level8")
n = 0
for o in env.objects:
    if o.type.name != "MonoBehaviour": continue
    raw = o.get_raw_data()
    if ms.get(struct.unpack_from("<q", raw, 20)[0]) != "LockVelocityArea": continue
    print("len", len(raw), "hex", raw.hex())
    for off in range(24, len(raw)-3, 4):
        f = struct.unpack_from("<f", raw, off)[0]
        i = struct.unpack_from("<i", raw, off)[0]
        print("  off=%2d  float=%-12.4f int=%d" % (off, f, i))
    n += 1
    if n >= 1: break
