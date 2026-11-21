# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy, struct, os, shutil, traceback
GAME = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire_Data\globalgamemanagers"
WORK = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\work"
dst = os.path.join(WORK, "globalgamemanagers.work")
shutil.copy2(GAME, dst)
env = UnityPy.load(dst)
sf = list(env.files.values())[0]
obj = [x for x in env.objects if x.type.name == "BuildSettings"][0]
raw = obj.get_raw_data()
def parse(raw):
    cnt = struct.unpack_from("<i", raw, 0)[0]; pos = 4; out = []
    for i in range(cnt):
        l = struct.unpack_from("<i", raw, pos)[0]
        out.append(raw[pos+4:pos+4+l].decode("latin1")); pos += 4 + ((l+3)//4)*4
    return cnt, out, pos
cnt, items, tail = parse(raw)
NEW = b"Assets/Scenes/Test/Map12.unity"
entry = struct.pack("<i", len(NEW)) + NEW + b"\x00"*(((len(NEW)+3)//4)*4-len(NEW))
obj.set_raw_data(struct.pack("<i", cnt+1) + raw[4:tail] + entry + raw[tail:])
blob = sf.save()
out = os.path.join(WORK, "globalgamemanagers.patched")
open(out, "wb").write(blob)
print("written", out, len(blob), "orig", os.path.getsize(GAME))
env2 = UnityPy.load(out)
sf2 = list(env2.files.values())[0]
objs2 = list(env2.objects)
print("objects after:", len(objs2))
obj2 = [x for x in env2.objects if x.type.name == "BuildSettings"][0]
c2, items2, t2 = parse(obj2.get_raw_data())
print("count:", c2, "tail:", hex(t2))
print("last 3:", items2[-3:])
# 完整性：逐对象比大小
bad = []
for a, b in zip(sorted(env.objects, key=lambda x: x.path_id), sorted(objs2, key=lambda x: x.path_id)):
    sa = len(a.get_raw_data()); sb = len(b.get_raw_data())
    if sa != sb: bad.append((a.type.name, a.path_id, sa, sb))
print("size-diff objects:", bad)
