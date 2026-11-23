# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
P = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/level1"
env = UnityPy.load(P)
go = [o for o in env.objects if o.type.name == "GameObject"][0]
d = go.read()
c = d.m_Component[0]
print("type:", type(c).__name__)
print("attrs:", [a for a in dir(c) if not a.startswith('_')])
for a in [a for a in dir(c) if not a.startswith('_')]:
    try: print("  ", a, "=", getattr(c, a))
    except Exception as e: print("  ", a, "ERR", e)
