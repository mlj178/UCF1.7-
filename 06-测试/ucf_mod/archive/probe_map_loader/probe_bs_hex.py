# -*- coding: utf-8 -*-
import UnityPy
GAME = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire_Data\globalgamemanagers"
env = UnityPy.load(GAME)
sf = list(env.files.values())[0]
print("serialized version:", getattr(sf, "version", None), "big_endian:", getattr(sf, "big_id_enabled", None))
print("unity version:", getattr(sf, "unity_version", None))
print("m_EnableTypeTree:", getattr(sf, "enable_type_tree", None))
for o in env.objects:
    if o.type.name != "BuildSettings": continue
    d = o.get_raw_data()
    print("len:", len(d), "endian:", o.reader.endian)
    for i in range(0, len(d), 16):
        chunk = d[i:i+16]
        hexs = ' '.join(f'{b:02x}' for b in chunk)
        asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print(f'{i:04x}  {hexs:<48s}  {asc}')
