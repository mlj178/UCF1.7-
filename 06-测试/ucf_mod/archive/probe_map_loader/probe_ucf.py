# -*- coding: utf-8 -*-
import sys, collections
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
BASE = "D:/BaiduNetdiskDownload/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
def hist(path, label):
    try:
        env = UnityPy.load(path)
        sf = list(env.files.values())[0]
    except Exception as e:
        print(f"  {label}: 失败 {type(e).__name__}"); return
    c = collections.Counter()
    for pid, oi in sf.objects.items():
        c[getattr(oi.type, "name", str(oi.type))] += 1
    print(f"\n--- {label}  objects={len(sf.objects)} ---")
    for k, v in c.most_common(30):
        print(f"   {k:26s} {v}")
for p,l in [(BASE+"level1","UCF level1 运输船"),(BASE+"sharedassets1.assets","UCF sharedassets1"),(BASE+"level2","UCF level2 小型工厂")]:
    hist(p,l)
