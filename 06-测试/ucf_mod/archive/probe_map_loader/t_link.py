# -*- coding: utf-8 -*-
import sys, struct, collections
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
SRC = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
env0 = UnityPy.load(SRC + "globalgamemanagers.assets")
ms = {}
for o in env0.objects:
    if o.type.name == "MonoScript":
        try: ms[o.path_id] = o.read().m_ClassName
        except Exception: ms[o.path_id] = "?"
env = UnityPy.load(SRC + "level10")
tr = set()
gos = {}
for o in env.objects:
    if o.type.name == "Transform": tr.add(o.path_id)
    elif o.type.name == "GameObject":
        gos[o.path_id] = o.read().m_Name
print("level10 transforms:", len(tr))
cands = collections.Counter(); samples = {}
for o in env.objects:
    if o.type.name != "MonoBehaviour": continue
    raw = o.get_raw_data()
    sc_pid = struct.unpack_from("<q", raw, 20)[0]
    cls = ms.get(sc_pid, "?")
    if cls not in ("NodeLink","NodeLink2","Bot_JumpLink"): continue
    for off in range(28, 80, 4):
        if off + 12 > len(raw): break
        fid, pid = struct.unpack_from("<iq", raw, off)
        if fid == 0 and pid in tr and pid != 0:
            key = (cls, off)
            cands[key] += 1
            samples.setdefault(key, []).append((o.path_id, pid))
print("\n候选 (class, offset) -> 命中数")
for k, v in cands.most_common(20):
    print("  ", k, v, "示例:", samples[k][:3])
