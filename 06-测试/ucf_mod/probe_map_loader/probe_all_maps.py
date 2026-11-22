# -*- coding: utf-8 -*-
import sys, json, collections
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy

U = "D:/BaiduNetdiskDownload/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
LEVELS = [f"level{i}" for i in range(12)]
SHARED = [f"sharedassets{i}.assets" for i in range(12)]

report = {"levels": {}, "shared": {}, "resources": {}}

def hist(path):
    env = UnityPy.load(path)
    sf = list(env.files.values())[0]
    c = collections.Counter()
    for pid, oi in sf.objects.items():
        c[getattr(oi.type, "name", str(oi.type))] += 1
    return len(sf.objects), dict(c)

for name in LEVELS:
    try:
        n, c = hist(U + name)
        report["levels"][name] = {"objects": n, "types": c}
        print(f"{name:10s} objects={n}")
    except Exception as e:
        report["levels"][name] = {"error": str(e)}
        print(f"{name:10s} ERR {type(e).__name__}")

for name in SHARED:
    try:
        n, c = hist(U + name)
        report["shared"][name] = {"objects": n, "types": c}
        print(f"{name:24s} objects={n} mesh={c.get('Mesh',0)} tex={c.get('Texture2D',0)} mat={c.get('Material',0)}")
    except Exception as e:
        report["shared"][name] = {"error": str(e)}
        print(f"{name:24s} ERR {type(e).__name__}")

try:
    n, c = hist(U + "resources.assets")
    report["resources"] = {"objects": n, "types": c}
    print("resources.assets objects=", n)
except Exception as e:
    print("resources ERR", e)

out = r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/probe_map_loader/ucf_all_maps.json"
json.dump(report, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved", out)
