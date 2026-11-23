# -*- coding: utf-8 -*-
import sys, json, os, re
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
SRC = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
OUT = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\_points"
os.makedirs(OUT, exist_ok=True)

def extract(level):
    env = UnityPy.load(SRC + level)
    gos, trs, cc = {}, {}, {}
    for o in env.objects:
        tn = o.type.name; pid = o.path_id
        cc[pid] = tn
        if tn == "GameObject":
            d = o.read(); gos[pid] = {"name": d.m_Name, "comps": [c.component.path_id for c in d.m_Component]}
        elif tn == "Transform":
            d = o.read(); p = d.m_LocalPosition
            trs[pid] = {"go": d.m_GameObject.path_id, "pos": [p.x,p.y,p.z],
                        "father": d.m_Father.path_id if d.m_Father else 0}
    tr_of_go = {t["go"]: tid for tid, t in trs.items()}
    def world(tid, depth=0):
        t = trs.get(tid)
        if not t or depth > 64: return (0.0,0.0,0.0)
        p = t["pos"]; f = t["father"]
        if f and f in trs:
            w = world(f, depth+1); return (p[0]+w[0], p[1]+w[1], p[2]+w[2])
        return (p[0], p[1], p[2])
    rows = []
    for gid, g in gos.items():
        tid = tr_of_go.get(gid); t = trs.get(tid) if tid else None
        w = world(tid) if tid else (0.0,0.0,0.0)
        pname, pgid = None, None
        if t and t["father"] and t["father"] in trs:
            pgid = trs[t["father"]]["go"]; pname = gos.get(pgid,{}).get("name")
        rows.append({"go": gid, "name": g["name"],
                     "local": [round(x,4) for x in (t["pos"] if t else [0,0,0])],
                     "world": [round(x,4) for x in w],
                     "parent": pname, "comps": [cc.get(c,"?") for c in g["comps"]]})
    return rows

KW = re.compile(r"point|link|area|pos|guard|npc|spawn|born|supply|jump|stair|crouch|fall|air|wall|setpos|waypoints|respawn|redpoint|effect", re.I)
summary = {}
for i in range(0, 12):
    lv = "level" + str(i)
    try:
        rows = extract(lv)
    except Exception as e:
        print(lv, "ERR", str(e)[:100]); continue
    json.dump(rows, open(os.path.join(OUT, lv + ".json"), "w", encoding="utf-8"), ensure_ascii=False)
    hits = [r for r in rows if KW.search(r["name"] or "")]
    summary[lv] = len(hits)
    kinds = {}
    for r in hits:
        for c in r["comps"]:
            kinds[c] = kinds.get(c, 0) + 1
    print(f"{lv:8s} objs={len(rows):5d} 命中={len(hits):4d} 组件={kinds}")
print("\nsummary:", summary)
