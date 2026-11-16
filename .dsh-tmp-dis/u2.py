
import UnityPy
from UnityPy.classes import MonoBehaviour
p = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data\\level1"
env = UnityPy.load(p)
for o in env.objects:
    if o.type.name != "MonoBehaviour": continue
    try:
        d = o.read()
        s = d.m_Script
        sc = s.read()
        name = getattr(sc, "m_ClassName", None)
        ns = getattr(sc, "m_Namespace", "")
        asm = getattr(sc, "m_AssemblyName", "")
        print(o.path_id, "|", asm, "|", ns, "|", name, "| name=", getattr(d,"m_Name",""))
    except Exception as e:
        print(o.path_id, "ERR", type(e).__name__, str(e)[:120])
