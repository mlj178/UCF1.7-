# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
P = r"D:\ucf_test_level12\game\UnityCrossFire_Data\sharedassets0.assets"
env = UnityPy.load(P)
sf = list(env.files.values())[0]
print("data_offset", sf.header.data_offset)
entries = sorted(sf.objects.items(), key=lambda kv: kv[1].byte_start)
print("=== objects in 0x42cae00..0x42cb800 ===")
for pid, oi in entries:
    s = oi.byte_start; e = s + oi.byte_size
    if e < 0x42cae00 or s > 0x42cb800: continue
    tn = getattr(oi.type, "name", str(oi.type))
    print(f"  pid={pid:<7d} start=0x{s:08x} size={oi.byte_size:<5d} {tn}")
# 找包含 TeamDeath 的对象
print("=== objects containing 'TeamDeath' ===")
for pid, oi in entries:
    raw = sf.reader.read(oi.byte_start, oi.byte_size)
    if b"TeamDeath" in raw:
        tn = getattr(oi.type, "name", str(oi.type))
        print(f"  pid={pid} size={oi.byte_size} {tn}")
        for i in range(0, len(raw), 16):
            c = raw[i:i+16]
            print(f'    {i:04x}  ' + ' '.join(f'{b:02x}' for b in c) + '  ' + ''.join(chr(b) if 32<=b<127 else '.' for b in c))
