# -*- coding: utf-8 -*-
import sys, json, struct, collections
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
U = "D:/BaiduNetdiskDownload/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
LEVELS = [f"level{i}" for i in range(12)]

allmap = {}
for name in LEVELS:
    buf = open(U + name, "rb").read()
    env = UnityPy.load(U + name)
    sf = list(env.files.values())[0]
    scripts = collections.Counter()
    for pid, oi in sf.objects.items():
        if getattr(oi.type, "name", "") != "MonoBehaviour": continue
        s = oi.byte_start
        if s + 28 > len(buf): continue
        file_id = struct.unpack_from("<i", buf, s + 16)[0]
        path_id = struct.unpack_from("<q", buf, s + 20)[0]
        scripts[(file_id, path_id)] += 1
    allmap[name] = dict((f"{k[0]}:{k[1]}", v) for k, v in scripts.items())
    print(f"{name:9s} MonoBehaviour={sum(scripts.values()):4d}  不同脚本={len(scripts):3d}")

# 每张图都出现、且每张只出现一次的脚本 = 固定管理对象
common = None
for name, d in allmap.items():
    once = set(k for k, v in d.items() if v == 1)
    common = once if common is None else (common & once)
print("\n12 张图都恰好出现 1 次的脚本数:", len(common or []))
print(sorted(common or []))
json.dump(allmap, open(r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/probe_map_loader/ucf_scripts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved")
