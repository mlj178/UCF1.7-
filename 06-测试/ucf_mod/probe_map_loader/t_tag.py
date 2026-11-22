# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
SRC = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
env = UnityPy.load(SRC + "level1")
go = [o for o in env.objects if o.type.name == "GameObject"][0]
d = go.read()
print("attrs:", [a for a in dir(d) if not a.startswith("_")])
for a in ["m_Name","m_Tag","m_Layer","m_IsActive","m_TagString"]:
    try: print(" ", a, "=", getattr(d, a))
    except Exception as e: print(" ", a, "ERR", e)
