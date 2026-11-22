# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
SRC = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
env0 = UnityPy.load(SRC + "globalgamemanagers.assets")
ms = {}
for o in env0.objects:
    if o.type.name == "MonoScript":
        try: ms[o.path_id] = o.read().m_ClassName
        except Exception: ms[o.path_id] = "?"
for lv in ("level8","level11"):
    env = UnityPy.load(SRC + lv)
    gos = {}
    for o in env.objects:
        if o.type.name == "GameObject": gos[o.path_id] = o.read().m_Name
    print("====", lv)
    n = 0
    for o in env.objects:
        if o.type.name != "MonoBehaviour": continue
        raw = o.get_raw_data()
        sc = ms.get(struct.unpack_from("<q", raw, 20)[0], "?")
        if sc != "LockVelocityArea": continue
        go = struct.unpack_from("<q", raw, 4)[0]
        fl = struct.unpack_from("<ff", raw, 28)
        b = raw[36] if len(raw) > 36 else None
        print("  %-8s speed=%.3f lockTime=%.3f saveVelY=%s len=%d" % (gos.get(go,"?"), fl[0], fl[1], b, len(raw)))
        n += 1
        if n >= 6: break
