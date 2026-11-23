# -*- coding: utf-8 -*-
import sys, struct, json, collections
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
SRC = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
env = UnityPy.load(SRC + "globalgamemanagers.assets")
ms = {}
for o in env.objects:
    if o.type.name != "MonoScript": continue
    try:
        d = o.read()
        ms[o.path_id] = getattr(d,"m_ClassName",None) or "?"
    except Exception:
        ms[o.path_id] = "<ERR>"
print("MonoScript:", len(ms))

allc = collections.Counter()
per = {}
for i in range(0, 12):
    lv = "level" + str(i)
    env = UnityPy.load(SRC + lv)
    gos = {}
    for o in env.objects:
        if o.type.name == "GameObject":
            d = o.read(); gos[o.path_id] = d.m_Name
    c = collections.Counter()
    rows = {}
    for o in env.objects:
        if o.type.name != "MonoBehaviour": continue
        raw = o.get_raw_data()
        if len(raw) < 28: continue
        go_fid, go_pid = struct.unpack_from("<iq", raw, 0)
        sc_fid, sc_pid = struct.unpack_from("<iq", raw, 16)
        cls = ms.get(sc_pid, "?"+str(sc_pid))
        c[cls] += 1
        allc[cls] += 1
        rows.setdefault(gos.get(go_pid, "?"), []).append(cls)
    per[lv] = {k: v for k, v in c.items()}
    print(f"{lv}: MB={sum(c.values())} classes={len(c)}")
print("\n=== 全局脚本类（按出现次数） ===")
for k, v in allc.most_common(60):
    print(f"  {k:34s} {v}")
json.dump(per, open(r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\_points\\scripts_per_level.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
