
import os,re,sys
base=r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire_Data"
names=["level1","level2","level3","level4","level5","level6","level7","level8","level9","level10","level11","level0","sharedassets0.assets","sharedassets1.assets","resources.assets"]
pats=[b"PointGraph",b"NavMeshGraph",b"AstarPath",b"AstarData",b"Pathfinding",b"GraphSerialization"]
for n in names:
    p=os.path.join(base,n)
    if not os.path.exists(p): continue
    d=open(p,'rb').read()
    hits={pat.decode():d.count(pat) for pat in pats}
    hits={k:v for k,v in hits.items() if v}
    print(n, len(d), hits)
