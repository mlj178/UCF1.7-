# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
SRC = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
env = UnityPy.load(SRC + "globalgamemanagers")
o = [x for x in env.objects if x.type.name == "TagManager"][0]
try:
    d = o.read()
    tags = list(d.m_Tags) if hasattr(d, "m_Tags") else []
    print("tags via read():", len(tags))
    for i, t in enumerate(tags):
        print("  %d -> %r" % (i, t))
except Exception as e:
    print("read err:", e)
    raw = o.get_raw_data()
    print("raw len", len(raw), raw[:160].hex())
