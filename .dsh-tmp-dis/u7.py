
import UnityPy, collections
p = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data\\level1"
env = UnityPy.load(p)
sf = list(env.files.values())[0]
tags = collections.Counter()
pos_sample = None
ok = 0
for pid_, o in sf.objects.items():
    if o.type.name != "GameObject": continue
    try:
        go = o.read()
        ok += 1
        tags[go.m_TagString] += 1
    except Exception as e:
        if ok == 0: print("ERR", type(e).__name__, str(e)[:100])
print("gameobjects read:", ok, "tags:", tags.most_common(15))
