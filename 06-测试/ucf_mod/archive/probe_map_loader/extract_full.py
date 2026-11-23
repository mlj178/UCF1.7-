# -*- coding: utf-8 -*-
import sys, struct, json, os, collections, re
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
SRC = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
OUT = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\_points"

env0 = UnityPy.load(SRC + "globalgamemanagers.assets")
ms = {}
for o in env0.objects:
    if o.type.name == "MonoScript":
        try: ms[o.path_id] = o.read().m_ClassName
        except Exception: ms[o.path_id] = "?"

LINK_OFF = {"NodeLink":44, "NodeLink2":44, "Bot_JumpLink":48}
LINK_CLS = set(LINK_OFF)

def extract(lv):
    env = UnityPy.load(SRC + lv)
    gos, trs, mb, cols = {}, {}, [], {}
    for o in env.objects:
        tn = o.type.name
        if tn == "GameObject":
            d = o.read(); gos[o.path_id] = {"name": d.m_Name, "tag": int(d.m_Tag), "active": bool(d.m_IsActive), "comps":[c.component.path_id for c in d.m_Component]}
        elif tn == "Transform":
            d = o.read(); p = d.m_LocalPosition
            trs[o.path_id] = {"go": d.m_GameObject.path_id, "pos":[p.x,p.y,p.z], "father": d.m_Father.path_id if d.m_Father else 0}
        elif tn == "BoxCollider":
            try:
                d = o.read()
                cols[o.path_id] = {"go": d.m_GameObject.path_id,
                    "center":[round(d.m_Center.x,3),round(d.m_Center.y,3),round(d.m_Center.z,3)],
                    "size":[round(d.m_Size.x,3),round(d.m_Size.y,3),round(d.m_Size.z,3)],
                    "trigger": bool(getattr(d,"m_IsTrigger",False))}
            except Exception: pass
        elif tn == "MonoBehaviour":
            mb.append(o)
    cls_of = {}
    for o in mb:
        raw = o.get_raw_data()
        if len(raw) < 28: continue
        go_pid = struct.unpack_from("<q", raw, 4)[0]
        sc = ms.get(struct.unpack_from("<q", raw, 20)[0], "?")
        cls_of.setdefault(go_pid, []).append((sc, o.path_id, raw))
    tr_of_go = {t["go"]: tid for tid, t in trs.items()}
    def world(tid, d=0):
        t = trs.get(tid)
        if not t or d>64: return (0.0,0.0,0.0)
        p, f = t["pos"], t["father"]
        if f and f in trs:
            w = world(f,d+1); return (p[0]+w[0], p[1]+w[1], p[2]+w[2])
        return tuple(p)
    col_of_go = {c["go"]: c for c in cols.values()}
    rows = []
    for gid, g in gos.items():
        tid = tr_of_go.get(gid); w = world(tid) if tid else (0.0,0.0,0.0)
        pname = None
        if tid and trs[tid]["father"] and trs[tid]["father"] in trs:
            pg = trs[trs[tid]["father"]]["go"]; pname = gos.get(pg,{}).get("name")
        scripts = [s[0] for s in cls_of.get(gid, [])]
        link_to = None
        for sc, mbp, raw in cls_of.get(gid, []):
            off = LINK_OFF.get(sc)
            if off and len(raw) >= off+12:
                fid, pid = struct.unpack_from("<iq", raw, off)
                if fid == 0 and pid in trs:
                    link_to = {"go": trs[pid]["go"], "name": gos.get(trs[pid]["go"],{}).get("name","?"),
                               "world":[round(x,3) for x in world(pid)]}
                break
        rows.append({"go": gid, "name": g["name"], "tag": g.get("tag"), "active": g.get("active"), "world":[round(x,3) for x in w],
                     "parent": pname, "scripts": scripts, "link_to": link_to,
                     "box": col_of_go.get(gid)})
    return rows

os.makedirs(OUT, exist_ok=True)
allrows = {}
for i in range(0, 12):
    lv = "level" + str(i)
    rows = extract(lv)
    allrows[lv] = rows
    json.dump(rows, open(os.path.join(OUT, "full_" + lv + ".json"), "w", encoding="utf-8"), ensure_ascii=False)
    links = [r for r in rows if r["link_to"]]
    pts = [r for r in rows if any(s in ("Bot_CrouchPos","Bot_GuardPos","Bot_NanoGuardPos","Bot_GuardArea","Bot_NanoGuardArea","LockVelocityArea") for s in r["scripts"])]
    print(f"{lv:8s} objs={len(rows):5d} links={len(links):4d} botpts={len(pts):3d} withbox={sum(1 for r in rows if r['box']):3d}")
