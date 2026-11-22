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
TARGET = "PointNodeTagModifier"
for lv in range(12):
    env = UnityPy.load(SRC + "level%d" % lv)
    n = 0
    for o in env.objects:
        if o.type.name != "MonoBehaviour": continue
        raw = o.get_raw_data()
        if len(raw) < 28: continue
        if ms.get(struct.unpack_from("<q", raw, 20)[0]) == TARGET: n += 1
    if n: print("level%d: %d" % (lv, n))
print("done")
