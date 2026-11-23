# -*- coding: utf-8 -*-
import sys, json, os, math
sys.stdout.reconfigure(encoding="utf-8")
import UnityPy

SRC = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
OUT = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\_points"
os.makedirs(OUT, exist_ok=True)

def extract(level):
    path = SRC + level
    env = UnityPy.load(path)
    objs = list(env.objects)
    by_id = {}
    gos = {}
    trs = {}
    comp_class = {}
    colliders = {}
    for o in objs:
        tn = o.type.name
        pid = o.path_id
        comp_class[pid] = tn
        if tn == "GameObject":
            d = o.read()
            gos[pid] = {"name": d.m_Name, "comps": [c.component.path_id for c in d.m_Component]}
        elif tn == "Transform":
            d = o.read()
            p = d.m_LocalPosition
            trs[pid] = {"go": d.m_GameObject.path_id,
                        "pos": [round(p.x,4), round(p.y,4), round(p.z,4)],
                        "father": d.m_Father.path_id if d.m_Father else 0,
                        "children": [c.path_id for c in d.m_Children]}
        elif tn in ("BoxCollider","SphereCollider","CapsuleCollider","MeshCollider"):
            try:
                d = o.read()
                info = {"type": tn, "go": d.m_GameObject.path_id}
                if tn == "BoxCollider":
                    info["center"] = [round(d.m_Center.x,4), round(d.m_Center.y,4), round(d.m_Center.z,4)]
                    info["size"]   = [round(d.m_Size.x,4), round(d.m_Size.y,4), round(d.m_Size.z,4)]
                elif tn == "SphereCollider":
                    info["center"] = [round(d.m_Center.x,4), round(d.m_Center.y,4), round(d.m_Center.z,4)]
                    info["radius"] = round(d.m_Radius,4)
                elif tn == "CapsuleCollider":
                    info["center"] = [round(d.m_Center.x,4), round(d.m_Center.y,4), round(d.m_Center.z,4)]
                    info["radius"] = round(d.m_Radius,4)
                    info["height"] = round(d.m_Height,4)
                colliders[pid] = info
            except Exception:
                colliders[pid] = {"type": tn, "err": True}
    # 世界坐标
    def world(tid, depth=0):
        t = trs.get(tid)
        if not t or depth > 64: return (0.0,0.0,0.0)
        p = t["pos"]; f = t["father"]
        if f and f in trs:
            w = world(f, depth+1)
            return (round(p[0]+w[0],4), round(p[1]+w[1],4), round(p[2]+w[2],4))
        return (p[0], p[1], p[2])
    tr_of_go = {}
    for tid, t in trs.items():
        tr_of_go[t["go"]] = tid
    out = []
    for gid, g in gos.items():
        tid = tr_of_go.get(gid)
        t = trs.get(tid) if tid else None
        w = world(tid) if tid else (0.0,0.0,0.0)
        # 父级 GameObject 名
        pname = None
        pgid = None
        if t and t["father"] and t["father"] in trs:
            pgid = trs[t["father"]]["go"]
            pname = gos.get(pgid, {}).get("name")
        comps = [comp_class.get(c, "?") for c in g["comps"]]
        out.append({
            "go": gid, "tr": tid, "name": g["name"],
            "local": t["pos"] if t else None,
            "world": list(w),
            "parent": pname, "parent_go": pgid,
            "comps": comps,
        })
    return out

for lv in ["level1"]:
    rows = extract(lv)
    fn = os.path.join(OUT, lv + ".json")
    json.dump(rows, open(fn,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print(lv, "objects dumped:", len(rows), "->", fn)
    # 分类概览
    import re
    KW = re.compile(r"point|link|area|pos|guard|npc|spawn|born|supply|jump|stair|crouch|fall|air|wall|setpos|waypoints|respawn", re.I)
    hit = [r for r in rows if KW.search(r["name"] or "")]
    print("  命中点位关键词:", len(hit))
    for r in hit[:40]:
        print(f'    {r["name"]:24s} world={r["world"]} parent={r["parent"]} comps={r["comps"]}')
