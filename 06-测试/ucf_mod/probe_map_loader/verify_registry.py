# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
P = r"D:\\ucf_test_level12\\game\\UnityCrossFire_Data\sharedassets0.assets"
env = UnityPy.load(P)
sf = list(env.files.values())[0]
print("objects", len(sf.objects), "data_offset", sf.header.data_offset)
buf = open(P, "rb").read()
oi = sf.objects[22391]
raw = buf[oi.byte_start:oi.byte_start+oi.byte_size]
print("pid 22391 size", oi.byte_size)
import re
for m in re.finditer(rb'[\x20-\x7e]{4,}', raw):
    print("   ", m.group().decode())
for m in re.finditer(rb'(?:[\xe4-\xe9][\x80-\xbf]{2}){2,}', raw):
    print("   CN:", m.group().decode('utf8'))
