
import UnityPy, collections, sys
p = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data\\level1"
env = UnityPy.load(p)
print("objects:", len(env.objects), "files:", list(env.files.keys())[:5])
cnt = collections.Counter()
mb = []
ta = []
for o in env.objects:
    t = o.type.name
    cnt[t] += 1
    if t == "MonoBehaviour":
        mb.append(o)
    elif t == "TextAsset":
        ta.append(o)
print("types:", cnt.most_common(20))
print("MonoBehaviour:", len(mb), "TextAsset:", len(ta))
for o in ta:
    d = o.read()
    print("TA:", getattr(d, "m_Name", "?"), len(getattr(d, "m_Script", b"") or b""))
