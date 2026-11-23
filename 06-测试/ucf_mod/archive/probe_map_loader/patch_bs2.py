# -*- coding: utf-8 -*-
import sys, inspect
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy, struct, os, shutil, traceback
GAME = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire_Data\globalgamemanagers"
WORK = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\work"
os.makedirs(WORK, exist_ok=True)
dst = os.path.join(WORK, "globalgamemanagers.work")
shutil.copy2(GAME, dst)

env = UnityPy.load(dst)
sf = list(env.files.values())[0]
obj = [x for x in env.objects if x.type.name == "BuildSettings"][0]
print("env.save sig:", inspect.signature(env.save))
print("sf.save  sig:", inspect.signature(sf.save))

raw = obj.get_raw_data()
cnt = struct.unpack_from("<i", raw, 0)[0]
def parse(raw):
    cnt = struct.unpack_from("<i", raw, 0)[0]
    pos = 4; out = []
    for i in range(cnt):
        l = struct.unpack_from("<i", raw, pos)[0]
        s = raw[pos+4:pos+4+l].decode("latin1")
        out.append((l, s))
        pos += 4 + ((l + 3) // 4) * 4
    return cnt, out, pos

cnt, items, rest_pos = parse(raw)
print("count", cnt, "tail at", hex(rest_pos), "tail len", len(raw)-rest_pos)
for i,(l,s) in enumerate(items):
    print(f"  [{i:2d}] len={l:3d} {s}")
print("tail hex:", raw[rest_pos:rest_pos+24].hex())

NEW = b"Assets/Scenes/Test/Map12.unity"
pad = ((len(NEW) + 3) // 4) * 4 - len(NEW)
entry = struct.pack("<i", len(NEW)) + NEW + b"\x00" * pad
new_raw = struct.pack("<i", cnt + 1) + raw[4:rest_pos] + entry + raw[rest_pos:]
print("new size", len(new_raw), "delta", len(new_raw) - len(raw))
obj.set_raw_data(new_raw)

out = os.path.join(WORK, "globalgamemanagers.patched")
for name, fn in [("env.save(out)", lambda: env.save(out)), ("env.save()", lambda: env.save())]:
    try:
        r = fn()
        print(name, "->", type(r), (len(r) if isinstance(r,(bytes,bytearray)) else r))
        if isinstance(r, (bytes, bytearray)):
            open(out, "wb").write(r)
        break
    except Exception:
        traceback.print_exc()
print("exists?", os.path.exists(out), os.path.getsize(out) if os.path.exists(out) else 0)
