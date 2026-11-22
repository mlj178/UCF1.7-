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
for lv in ("level2","level3"):
    env = UnityPy.load(SRC + lv)
    tr = set(); gos = {}
    for o in env.objects:
        if o.type.name == "Transform": tr.add(o.path_id)
        elif o.type.name == "GameObject": gos[o.path_id] = o.read().m_Name
    print("====", lv, "transforms:", len(tr))
    for o in env.objects:
        if o.type.name != "MonoBehaviour": continue
        raw = o.get_raw_data()
        cls = ms.get(struct.unpack_from("<q", raw, 20)[0], "?")
        if cls not in ("NodeLink","NodeLink2","Bot_JumpLink"): continue
        go = struct.unpack_from("<q", raw, 4)[0]
        vals = []
        for off in range(28, min(len(raw)-12, 76), 4):
            fid, pid = struct.unpack_from("<iq", raw, off)
            vals.append(f"{off}:f{fid}p{pid}{'*' if (fid==0 and pid in tr) else ''}")
        print(f"  {cls} name={gos.get(go,'?')} len={len(raw)}")
        print("     ", " ".join(vals))
