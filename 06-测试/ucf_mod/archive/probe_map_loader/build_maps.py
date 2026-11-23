# -*- coding: utf-8 -*-
import sys, json, os, re
sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/docs/guide/原始地图标准数据"
PTS  = "D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/probe_map_loader/_points"
META = [(0,"GameStart","大厅","TeamDeath 团队模式","大厅"),(1,"TransportShip","运输船","TeamDeath 团队模式","团队模式（TeamDeath）"),(2,"Factory","小型工厂","TeamDeath 团队模式","团队模式（TeamDeath）"),(3,"Cebu_City","椰岛之巅","TeamDeath 团队模式","团队模式（TeamDeath）"),(4,"NY_TM","胜利广场","DeathMatch 个人竞技","个人竞技（DeathMatch）"),(5,"Arena","竞技场","Special 特殊战","特殊战（Special）"),(6,"GrimReaperKM","刀锋寨","Special 特殊战","特殊战（Special）"),(7,"DesertFort","沙漠要塞","Nano4 终结者模式 / Nano6 生化剑客模式","终结者 / 生化剑客"),(8,"NanoResort","生化酒店","Nano4 终结者模式 / Nano6 生化剑客模式","终结者 / 生化剑客"),(9,"Nano30_Storm","飓风危城","Nano4_Terminator 多人终结者模式（隐藏图）","多人终结者（隐藏图）"),(10,"Nano_DawnVillage","新寂静村","Nano4_Terminator 多人终结者模式","多人终结者"),(11,"DeathRing","死亡擂台","Special 特殊战","特殊战（Special）")]
MD5 = ["3597612b9a732b7f1a7f4277ca80cbfe","88a70fb22af57ddce6293f89aa692832","fba06f8bb8e39244dd45d73033441444","7546065d5f8daf143ca72ffc16b9af02","e94602dd66d0672fc82475864b15075f","7148afffde84d8325ca9daa03c875ffc","b764d94d64e848d87e3f5a1ba34c3b55","f4dba2dc8e16245deeab9c5b56f2b483","82471539c82ac7fd85ab610c0d16cdef","89c56148f205eb630730dcf58ba4fa20","d555d653e5536998cb7e10c093af52a9","b7f8c56b28ac80b3e5b8ee5cbfa855e5"]
SIZE = [209276,354420,76876,60500,63532,47772,50364,82068,741516,192140,197932,61980]
SCENE = ["Assets/Scenes/GameStart.unity","Assets/Scenes/TeamDeath/TransportShip.unity","Assets/Scenes/TeamDeath/Factory.unity","Assets/Scenes/TeamDeath/Cebu_City.unity","Assets/Scenes/BlastingMode/NY_TM.unity","Assets/Scenes/Special/Arena.unity","Assets/Scenes/Special/GrimReaperKM.unity","Assets/Scenes/Nano/DesertFort.unity","Assets/Scenes/Nano/NanoResort.unity","Assets/Scenes/Nano30/Nano30_Storm.unity","Assets/Scenes/Nano30/Nano_DawnVillage.unity","Assets/Scenes/Special/DeathRing.unity"]
FACTION = set(["BL_Area","GR_Area","Neutral_Area","BL_SpawnArea","GR_SpawnArea"])
def f3(v): return "%.3f" % v
def pkind(r):
    n = r.get("name") or ""; s = r.get("scripts") or []
    if "Bot_CrouchPos" in s or re.match(r"^CrouchPos", n): return "crouch_pos"
    if "Bot_GuardPos" in s or "Bot_NanoGuardPos" in s or re.match(r"^GuardPos", n): return "guard_pos"
    if "Bot_GuardArea" in s or "Bot_NanoGuardArea" in s or re.match(r"^GuardArea", n): return "guard_area"
    if "LockVelocityArea" in s: return "area_lock"
    if n in FACTION: return "area_faction"
    if re.match(r"^GR_Fall|^Fall", n): return "fall_point"
    if re.match(r"^AirPoint", n): return "air_point"
    return None
def has_link(r):
    return any(s in ("NodeLink","NodeLink2","Bot_JumpLink") for s in (r.get("scripts") or []))

A_HDR = "| # | 名称 | 类型 | 中心X | 中心Y | 中心Z | 尺寸X | 尺寸Y | 尺寸Z | 形状 | 父级 | 备注 |"
A_SEP = "|---|---|---|---|---|---|---|---|---|---|---|---|"
P_HDR = "| # | 名称 | 类型 | X | Y | Z | 父级 | 脚本 | 备注 |"
P_SEP = "|---|---|---|---|---|---|---|---|---|"
L_HDR = "| # | 名称 | 类型 | 起点X | 起点Y | 起点Z | 终点对象 | 终点X | 终点Y | 终点Z | 父级 | 备注 |"
L_SEP = "|---|---|---|---|---|---|---|---|---|---|---|---|"

for n, en, cn, mode, grp in META:
    rows = json.load(open(os.path.join(PTS, "full_level%d.json" % n), encoding="utf-8"))
    wp = [r for r in rows if r.get("tag") == 20022]
    links = [r for r in rows if has_link(r) and r.get("link_to")]
    node_ids = set()
    for r in links:
        node_ids.add(r["go"]); node_ids.add(r["link_to"]["go"])
    area_list = []; point_list = []
    for r in rows:
        k = pkind(r)
        is_area = (k in ("area_faction","area_lock","guard_area")) or (("Area" in (r.get("name") or "")) and r["go"] not in node_ids)
        if (not is_area) and r.get("box") and (k is None) and (r["go"] not in node_ids):
            if (r.get("parent") == "Water") or (r.get("name") == "Collider"): continue
            is_area = True
        if is_area: area_list.append(r)
        elif k: point_list.append(r)
    cnt = {}
    for r in point_list:
        k = pkind(r) or "node"; cnt[k] = cnt.get(k,0)+1
    a_rows = []
    for i, r in enumerate(area_list):
        k = pkind(r) or ("area_box" if r.get("box") else "area_generic")
        b = r.get("box")
        sx = f3(b["size"][0]) if b else "-"; sy = f3(b["size"][1]) if b else "-"; sz = f3(b["size"][2]) if b else "-"
        a_rows.append("| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (i+1, r["name"], k, f3(r["world"][0]), f3(r["world"][1]), f3(r["world"][2]), sx, sy, sz, "盒体" if b else "标记点", r.get("parent") or "-", "Trigger" if (b and b.get("trigger")) else "-"))
    p_rows = []
    for i, r in enumerate(point_list):
        k = pkind(r) or "node"
        sc = "/".join(r.get("scripts") or []) or "-"
        p_rows.append("| %d | %s | %s | %s | %s | %s | %s | %s | - |" % (i+1, r["name"], k, f3(r["world"][0]), f3(r["world"][1]), f3(r["world"][2]), r.get("parent") or "-", sc))
    l_rows = []
    for i, r in enumerate(links):
        t2 = r["link_to"]; sc = "/".join(r.get("scripts") or [])
        l_rows.append("| %d | %s | link | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (i+1, r["name"], f3(r["world"][0]), f3(r["world"][1]), f3(r["world"][2]), t2["name"], f3(t2["world"][0]), f3(t2["world"][1]), f3(t2["world"][2]), r.get("parent") or "-", sc))
    g = {}
    for r in area_list + point_list:
        k = r.get("parent") or "(根)"; g[k] = g.get(k,0)+1
    tree = "\n".join("%s  (%d 个)" % (k, v) for k, v in sorted(g.items(), key=lambda x: -x[1])[:12]) or "(无)"
    out = []
    out.append("# level%d · %s · %s" % (n, en, cn))
    out.append("")
    out.append("> 所属模式：%s　｜　上级索引：[点位与区域标准.md](../../点位与区域标准.md)" % mode)
    out.append("")
    out.append("## 0. 来源文件")
    out.append("")
    out.append("```")
    out.append("文件：UnityCrossFire_Data\\level%d" % n)
    out.append("大小：%s 字节" % format(SIZE[n], ","))
    out.append("MD5 ：%s" % MD5[n])
    out.append("场景：%s" % SCENE[n])
    out.append("提取：SerializedFile v22 对象表遍历，%d 个 GameObject 全量分类" % len(rows))
    out.append("```")
    out.append("")
    out.append("## 1. 摘要")
    out.append("")
    out.append("| 项目 | 数量 |")
    out.append("|---|---|")
    out.append("| GameObject 总数 | %d |" % len(rows))
    out.append("| 路点（tag 20022） | %s |" % format(len(wp), ","))
    out.append("| 区域对象 | %d |" % len(area_list))
    out.append("| 标记点对象 | %d |" % len(point_list))
    out.append("| 连线 | %d |" % len(links))
    for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
        out.append("| └ %s | %d |" % (k, v))
    out.append("")
    out.append("## 2. 区域表（%d 条）" % len(area_list))
    out.append("")
    out.append(A_HDR); out.append(A_SEP)
    out.extend(a_rows if a_rows else ["（本图无区域对象）"])
    out.append("")
    out.append("## 3. 标记点表（%d 条）" % len(point_list))
    out.append("")
    out.append(P_HDR); out.append(P_SEP)
    out.extend(p_rows if p_rows else ["（本图无标记点对象）"])
    out.append("")
    out.append("## 4. 线表（%d 条）" % len(links))
    out.append("")
    out.append(L_HDR); out.append(L_SEP)
    out.extend(l_rows if l_rows else ["（本图无连线）"])
    out.append("")
    out.append("## 5. 分组结构")
    out.append("")
    out.append("```")
    out.append(tree)
    out.append("```")
    out.append("")
    out.append("## 6. 路点全量坐标（%s 个）" % format(len(wp), ","))
    out.append("")
    out.append("路点 = 场景里 tag 等于 20022（WayPoint）的 GameObject。格式：X Y Z 名称。")
    out.append("")
    out.append("```")
    for r in wp:
        out.append("%.3f %.3f %.3f %s" % (r["world"][0], r["world"][1], r["world"][2], r["name"]))
    out.append("```")
    folder = os.path.join(BASE, "maps", "level%d-%s-%s" % (n, en, cn))
    os.makedirs(folder, exist_ok=True)
    fn = os.path.join(folder, "level%d-%s-%s.md" % (n, en, cn))
    open(fn, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("OK", fn, os.path.getsize(fn))