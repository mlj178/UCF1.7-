
import UnityPy, os, collections
base = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data"
files = ["sharedassets0.assets","sharedassets1.assets"] + [f"sharedassets{i}.assets" for i in range(2,12)] + ["resources.assets","globalgamemanagers.assets"]
for f in files:
    p = os.path.join(base,f)
    if not os.path.exists(p): continue
    try:
        env = UnityPy.load(p)
    except Exception as e:
        print(f, "LOAD FAIL", type(e).__name__); continue
    tot = collections.Counter(); n22 = 0
    for sf in env.files.values():
        try:
            objs = sf.objects
        except Exception: continue
        for pid_, o in objs.items():
            if o.type.name != "GameObject": continue
            try:
                go = o.read(); tot[go.m_Tag] += 1
                if go.m_Tag == 20022: n22 += 1
            except Exception: pass
    print(f, "GO total", sum(tot.values()), "tag20022", n22, "top", tot.most_common(4))
