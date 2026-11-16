
import UnityPy
p = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data\\level1"
env = UnityPy.load(p)
sf = list(env.files.values())[0]
for pid_, o in sf.objects.items():
    if o.type.name != "GameObject": continue
    go = o.read()
    print("obj", pid_, type(go))
    print("  keys:", list(go.__dict__.keys())[:20] if hasattr(go,'__dict__') else 'n/a')
    for k in ("m_Name","m_Tag","m_TagString","m_IsActive","m_Layer"):
        print("  ", k, "=", repr(getattr(go,k,"<missing>")))
    raw = o.get_raw_data()
    print("  rawlen", len(raw))
    break
