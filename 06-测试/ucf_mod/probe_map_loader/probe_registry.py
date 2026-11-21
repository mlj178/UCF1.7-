# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
P = r"D:\ucf_test_level12\game\UnityCrossFire_Data\sharedassets0.assets"
TARGET = 0x42cb0f0
env = UnityPy.load(P)
sf = list(env.files.values())[0]
print("objects", len(sf.objects), "data_offset", sf.header.data_offset)
for pid, oi in sf.objects.items():
    s = oi.byte_start; e = s + oi.byte_size
    if s <= TARGET < e:
        print("CONTAINED:", pid, oi.byte_size, hex(s), hex(e))
        o = env.objects[pid] if pid in env.objects else None
        print("type:", o.type.name if o else "?")
        raw = o.get_raw_data()
        rel = TARGET - s
        print("target rel:", hex(rel))
        lo = max(0, rel - 0x200)
        hi = min(len(raw), rel + 0x600)
        for i in range(lo, hi, 16):
            c = raw[i:i+16]
            hexs = ' '.join(f'{b:02x}' for b in c)
            asc = ''.join(chr(b) if 32 <= b < 127 else '.' for b in c)
            print(f'{i:04x}  {hexs:<48s}  {asc}')
        break
