# -*- coding: utf-8 -*-
import UnityPy
GAME = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire_Data\globalgamemanagers"
env = UnityPy.load(GAME)
for o in env.objects:
    if o.type.name != "ResourceManager": continue
    d = o.get_raw_data()
    print("ResourceManager size:", len(d))
    for pat in [b'level0', b'level1', b'level11', b'level12', b'sharedassets', b'resources.assets', b'globalgamemanagers']:
        print(" ", pat, "->", d.count(pat))
    for i in range(0, 160, 16):
        c = d[i:i+16]
        print(f'{i:04x}  ' + ' '.join(f'{b:02x}' for b in c))
