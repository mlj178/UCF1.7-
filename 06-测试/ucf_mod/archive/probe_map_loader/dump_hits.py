# -*- coding: utf-8 -*-
import sys, json, re, os
sys.stdout.reconfigure(encoding="utf-8")
OUT = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\_points"
KW = re.compile(r"point|link|area|pos|guard|npc|spawn|born|supply|jump|stair|crouch|fall|air|wall|setpos|waypoints|respawn|redpoint|effect", re.I)
for i in range(0, 12):
    lv = "level" + str(i)
    rows = json.load(open(os.path.join(OUT, lv + ".json"), encoding="utf-8"))
    hits = [r for r in rows if KW.search(r["name"] or "")]
    print(f"===== {lv}  {len(hits)}")
    for r in hits:
        c = ",".join(r["comps"])
        print(f'  {r["name"][:30]:32s} {str(r["world"]):30s} p={str(r["parent"])[:22]:24s} {c}')
