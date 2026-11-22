# -*- coding: utf-8 -*-
import sys, struct, re
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
SRC = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
env = UnityPy.load(SRC + "globalgamemanagers")
o = [x for x in env.objects if x.type.name == "TagManager"][0]
raw = o.get_raw_data()
print("len", len(raw))
print(raw[:400].hex())
strs = [m.group().decode("latin1") for m in re.finditer(rb"[ -~]{2,}", raw)]
print("strings:", strs[:80])
