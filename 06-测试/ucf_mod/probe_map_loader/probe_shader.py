# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
U = "D:/BaiduNetdiskDownload/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
P = U + "resources.assets"
env = UnityPy.load(P); sf = list(env.files.values())[0]
buf = open(P, "rb").read()
print("=== resources.assets 里的 Shader ===")
for pid, oi in sf.objects.items():
    if getattr(oi.type, "name", "") != "Shader": continue
    raw = buf[oi.byte_start:oi.byte_start+min(oi.byte_size, 400)]
    strs = [m.group().decode("latin1") for m in re.finditer(rb"[ -~]{4,}", raw)]
    print(f"  pid={pid} size={oi.byte_size} {strs[:4]}")
print("\n=== sharedassets1 里的 Shader ===")
env2 = UnityPy.load(U+"sharedassets1.assets"); sf2 = list(env2.files.values())[0]
buf2 = open(U+"sharedassets1.assets","rb").read()
for pid, oi in sf2.objects.items():
    if getattr(oi.type, "name", "") != "Shader": continue
    raw = buf2[oi.byte_start:oi.byte_start+min(oi.byte_size, 400)]
    strs = [m.group().decode("latin1") for m in re.finditer(rb"[ -~]{4,}", raw)]
    print(f"  pid={pid} size={oi.byte_size} {strs[:4]}")
