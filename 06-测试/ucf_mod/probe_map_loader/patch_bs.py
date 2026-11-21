# -*- coding: utf-8 -*-
import UnityPy, struct, os, shutil, traceback
GAME = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire_Data\globalgamemanagers"
WORK = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\work"
os.makedirs(WORK, exist_ok=True)
dst = os.path.join(WORK, "globalgamemanagers.patched")
shutil.copy2(GAME, dst)

env = UnityPy.load(dst)
sf = list(env.files.values())[0]
obj = [x for x in env.objects if x.type.name == "BuildSettings"][0]
print("APIs:", [m for m in dir(obj) if "raw" in m.lower()])
print("save APIs:", [m for m in dir(sf) if "save" in m.lower()])

raw = obj.get_raw_data()
print("orig size", len(raw))
cnt = struct.unpack_from("<i", raw, 0)[0]
print("scene count", cnt)
pos = 4
for i in range(cnt):
    l = struct.unpack_from("<i", raw, pos)[0]
    s = raw[pos+4:pos+4+l].rstrip(b"\x00").decode("utf8", "replace")
    total = 4 + ((l + 1 + 3) // 4) * 4
    print(f"  [{i}] len={l:3d} span={total:3d} {s}")
    pos += total
print("rest starts at", pos, "rest bytes", len(raw) - pos)
rest = raw[pos:]

NEW = b"Assets/Scenes/Test/Map12.unity"
new_entry = struct.pack("<i", len(NEW)) + NEW + b"\x00" * (((len(NEW)+1+3)//4)*4 - len(NEW))
new_raw = struct.pack("<i", cnt + 1) + raw[4:pos] + new_entry + rest
print("new size", len(new_raw), "delta", len(new_raw) - len(raw))

obj.set_raw_data(new_raw)
print("set ok")

out = os.path.join(WORK, "globalgamemanagers.patched2")
try:
    env.save(out)
    print("env.save ok ->", out)
except Exception as e:
    traceback.print_exc()
