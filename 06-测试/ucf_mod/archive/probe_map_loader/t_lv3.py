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
for lv in ("level8","level11"):
    env = UnityPy.load(SRC + lv)
    print("==== " + lv)
    for o in env.objects:
        if o.type.name != "MonoBehaviour": continue
        raw = o.get_raw_data()
        if ms.get(struct.unpack_from("<q", raw, 20)[0]) != "LockVelocityArea": continue
        v = struct.unpack_from("<ffff", raw, 28)
        b36 = raw[36]; b37 = raw[37]
        print("  raw28-43: %s  f=[%g %g %g %g]  byte36=%d byte37=%d" % (raw[28:44].hex(), v[0], v[1], v[2], v[3], b36, b37))
