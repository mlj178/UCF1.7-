# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
P = "D:/BaiduNetdiskDownload/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/globalgamemanagers.assets"
env = UnityPy.load(P)
sf = list(env.files.values())[0]
buf = open(P, "rb").read()
targets = [952,705,1343,308,420,1065,680,1210,85,972,1034,307,937,1329,852,182,1276,682]
for t in targets:
    oi = sf.objects.get(t)
    if oi is None:
        print(f"{t}: 不存在"); continue
    raw = buf[oi.byte_start:oi.byte_start+oi.byte_size]
    strs = [m.group().decode("latin1") for m in re.finditer(rb"[ -~]{3,}", raw)]
    tn = getattr(oi.type, "name", "?")
    print(f"{t:5d} {tn:14s} size={oi.byte_size:4d} strings={strs[:8]}")
