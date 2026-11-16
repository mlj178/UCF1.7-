
import UnityPy, collections, os
base = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data"
for lvl in ["level1","level2","level3","level4","level5","level6","level7","level8","level9","level10","level11"]:
    env = UnityPy.load(os.path.join(base,lvl))
    sf = list(env.files.values())[0]
    c = collections.Counter()
    for pid_, o in sf.objects.items():
        if o.type.name != "GameObject": continue
        try:
            go = o.read(); c[go.m_Tag] += 1
        except Exception: pass
    print(lvl, "GO tags:", c.most_common(6))
