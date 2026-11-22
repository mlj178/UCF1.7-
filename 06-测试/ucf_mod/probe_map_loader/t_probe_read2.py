# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy, traceback
P = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/level1"
env = UnityPy.load(P)
objs = list(env.objects)
print("readers:", len(objs))
go = [o for o in objs if o.type.name == "GameObject"][0]
try:
    d = go.read()
    print("read() ->", type(d).__name__, "m_Name=", repr(getattr(d, "m_Name", None)))
except Exception:
    traceback.print_exc()
tr = [o for o in objs if o.type.name == "Transform"][0]
try:
    d = tr.read()
    print("transform ->", type(d).__name__, "pos=", getattr(d, "m_LocalPosition", None))
except Exception:
    traceback.print_exc()
mb = [o for o in objs if o.type.name == "MonoBehaviour"]
print("monobehaviours:", len(mb))
for o in mb[:5]:
    try:
        d = o.read()
        print("  MB:", type(d).__name__, getattr(d, "m_Script", None))
    except Exception as e:
        print("  MB err:", str(e)[:80])
