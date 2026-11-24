
import UnityPy, os, hashlib

OUT = "D:/ucf_unity/out_final"
env = UnityPy.load(OUT + "/level12")
for name, sf in env.files.items():
    if not hasattr(sf, "objects"):
        continue
    print("level12 unity_version", sf.unity_version, "objects", len(sf.objects))
    for k, e in enumerate(sf.externals):
        print("  ext", k, "path=", e.path, "| name=", e.name, "| type=", e.type)
    break

env2 = UnityPy.load(OUT + "/sharedassets12.assets")
for name, sf in env2.files.items():
    if hasattr(sf, "objects"):
        print("shared12 objects", len(sf.objects), "externals", [e.path for e in sf.externals])
        break

def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()

gd = "D:/ucf_test_level12/game/UnityCrossFire_Data"
print("--- game data dir ---")
for f in ["level11", "level12", "sharedassets11.assets", "sharedassets12.assets", "sharedassets12.assets.resS", "unity default resources", "globalgamemanagers"]:
    p = gd + "/" + f
    print(f, os.path.exists(p), os.path.getsize(p) if os.path.exists(p) else "-", md5(p) if os.path.exists(p) else "")
