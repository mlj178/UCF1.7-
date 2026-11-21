# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy, struct
P = r"D:\\ucf_test_level12\\game\\UnityCrossFire_Data\globalgamemanagers"
env = UnityPy.load(P)
o = [x for x in env.objects if x.type.name == "BuildSettings"][0]
raw = o.get_raw_data()
cnt = struct.unpack_from("<i", raw, 0)[0]
pos = 4
print("count", cnt, "size", len(raw))
for i in range(cnt):
    l = struct.unpack_from("<i", raw, pos)[0]
    s = raw[pos+4:pos+4+l].decode("latin1")
    print(f"  [{i}] {s}")
    pos += 4 + ((l + 3) // 4) * 4
print("tail at", hex(pos), "tail len", len(raw)-pos)
