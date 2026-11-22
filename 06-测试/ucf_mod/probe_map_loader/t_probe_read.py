# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy, traceback
P = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/level1"
env = UnityPy.load(P)
sf = list(env.files.values())[0]
print("objects", len(sf.objects), "data_offset", sf.header.data_offset, "ver", sf.header.version)
from collections import Counter
c = Counter()
for pid, oi in sf.objects.items():
    c[getattr(oi.type, "name", str(oi.type))] += 1
print("class counts:", dict(c))
# 试读一个 GameObject
for pid, oi in sf.objects.items():
    if getattr(oi.type, "name", "") == "GameObject":
        try:
            o = env.objects[pid] if pid in getattr(env,'objects',{}) else UnityPy.files.ObjectReader(oi, sf)
        except Exception:
            o = None
        break
try:
    from UnityPy.files.ObjectReader import ObjectReader
    pid0 = next(p for p,oi in sf.objects.items() if getattr(oi.type,"name","")=="GameObject")
    r = ObjectReader(sf.objects[pid0], sf)
    d = r.read()
    print("read ok:", type(d), getattr(d, "m_Name", None))
except Exception:
    traceback.print_exc()
try:
    pid0 = next(p for p,oi in sf.objects.items() if getattr(oi.type,"name","")=="GameObject")
    r = ObjectReader(sf.objects[pid0], sf)
    tt = r.read_typetree()
    print("typetree ok:", str(tt)[:300])
except Exception:
    traceback.print_exc()
