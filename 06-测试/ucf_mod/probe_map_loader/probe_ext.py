# -*- coding: utf-8 -*-
import sys, collections
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
U = "D:/BaiduNetdiskDownload/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
D = "C:/Users/17242/Downloads/DC穿越火线挑战版本/DC穿越火线挑战版本/DC穿越火线挑战版本_Data/"

def ext(path, label):
    env = UnityPy.load(path); sf = list(env.files.values())[0]
    print(f"--- {label} externals:")
    for e in getattr(sf, "externals", []):
        print("     ", getattr(e, "path", e))

ext(U+"level1", "UCF level1")
ext(U+"sharedassets1.assets", "UCF sharedassets1")
ext(D+"level2", "DC level2")

def types(path, label, wanted):
    env = UnityPy.load(path); sf = list(env.files.values())[0]
    c = collections.Counter()
    names = collections.defaultdict(list)
    for pid, oi in sf.objects.items():
        tn = getattr(oi.type, "name", str(oi.type))
        c[tn] += 1
    print(f"\n--- {label} objects={len(sf.objects)}")
    for w in wanted:
        print(f"    {w:22s} {c.get(w,0)}")

types(U+"resources.assets", "UCF resources.assets", ["Mesh","Texture2D","Material","Shader","MeshCollider","RenderTexture"])
types(U+"sharedassets1.assets", "UCF sharedassets1", ["Mesh","Texture2D","Material","Shader"])
types(D+"sharedassets2.assets", "DC sharedassets2", ["Mesh","Texture2D","Material","Shader","NavMeshData","AnimationClip"])

# 找 Lightmap 贴图名
import re
for path,label in [(U+"resources.assets","UCF resources"),(D+"sharedassets2.assets","DC sharedassets2")]:
    b = open(path,"rb").read()
    hits = set(m.group().decode("latin1") for m in re.finditer(rb"Lightmap[-A-Za-z0-9_]{0,20}", b))
    print(f"\n{label} 里的 Lightmap 贴图名（前20）:", list(hits)[:20])
