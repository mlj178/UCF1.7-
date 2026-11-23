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
gos, trs, mb = {}, {}, []
for o in env.objects:
    tn = o.type.name
    if tn == "GameObject":
        d = o.read(); gos[o.path_id] = {"name": d.m_Name, "comps":[c.component.path_id for c in d.m_Component]}
    elif tn == "Transform":
        d = o.read(); p = d.m_LocalPosition
        trs[o.path_id] = {"go": d.m_GameObject.path_id, "pos":[p.x,p.y,p.z], "father": d.m_Father.path_id if d.m_Father else 0}
tr_of_go = {t["go"]: tid for tid, t in trs.items()}
def world(tid, d=0):
    t = trs.get(tid)
    if not t or d>64: return (0,0,0)
    p, f = t["pos"], t["father"]
    if f and f in trs:
        w = world(f, d+1); return (p[0]+w[0], p[1]+w[1], p[2]+w[2])
    return tuple(p)
def name_of_transform(tid):
    t = trs.get(tid)
    if not t: return "?"
    return gos.get(t["go"],{}).get("name","?")
rows = []
for o in env.objects:
    if o.type.name != "MonoBehaviour": continue
    raw = o.get_raw_data()
    sc = ms.get(struct.unpack_from("<q", raw, 20)[0], "?")
    if sc not in ("NodeLink","NodeLink2","Bot_JumpLink"): continue
    go_pid = struct.unpack_from("<q", raw, 4)[0]
    tid = tr_of_go.get(go_pid)
    w = world(tid) if tid else (0,0,0)
    off = 44 if sc == "NodeLink" else (48 if sc == "Bot_JumpLink" else None)
    tgt = None
    if off:
        fid, pid = struct.unpack_from("<iq", raw, off)
        if fid == 0 and pid in trs: tgt = (name_of_transform(pid), world(pid))
    rows.append((sc, gos.get(go_pid,{}).get("name","?"), [round(x,2) for x in w], tgt and tgt[0], tgt and [round(x,2) for x in tgt[1]]))
print("total links:", len(rows), " resolved:", sum(1 for r in rows if r[3]))
c = collections.Counter(r[0] for r in rows)
print("by class:", dict(c))
for r in rows[:25]:
    print(f"  {r[0]:14s} {r[1][:18]:20s} {str(r[2]):26s} -> {str(r[3])[:20]:22s} {r[4]}")
