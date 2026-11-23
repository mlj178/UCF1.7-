# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
P = r"D:\ucf_test_level12\game\UnityCrossFire_Data\sharedassets0.assets"
buf = open(P, "rb").read()
env = UnityPy.load(P)
sf = list(env.files.values())[0]
def dump(pid):
    oi = sf.objects[pid]
    raw = buf[oi.byte_start:oi.byte_start+oi.byte_size]
    print(f"=== pid {pid}  start 0x{oi.byte_start:x}  size {oi.byte_size}")
    for i in range(0, len(raw), 16):
        c = raw[i:i+16]
        print(f'  {i:04x}  ' + ' '.join(f'{b:02x}' for b in c) + '  ' + ''.join(chr(b) if 32<=b<127 else '.' for b in c))
for pid in (22385, 22386, 22387, 22388):
    dump(pid)
