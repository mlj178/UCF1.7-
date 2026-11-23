# -*- coding: utf-8 -*-
import sys, json, os, collections
sys.stdout.reconfigure(encoding="utf-8")
OUT = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\_points"
rows = json.load(open(os.path.join(OUT,"full_level1.json"), encoding="utf-8"))
by_name = collections.Counter(r["name"] for r in rows)
print("level1 对象总数:", len(rows))
print("=== 所有带 NodeLink 的对象 ===")
links = [r for r in rows if r["link_to"]]
print("links:", len(links))
for r in links:
    t = r["link_to"]
    print(f'  {r["name"][:22]:24s} {str(r["world"]):28s} -> {t["name"][:22]:24s} {t["world"]}  scripts={r["scripts"]}')
print()
print("=== 点位/区域类对象 ===")
for r in rows:
    if r["scripts"] or r["box"] or any(k in (r["name"] or "") for k in ("Area","WayPoints","Point")):
        if r["name"] in ("Point Light","Point Light (1)"): continue
        print(f'  {r["name"][:26]:28s} {str(r["world"]):28s} p={str(r["parent"])[:18]:20s} s={r["scripts"]} box={r["box"]}')
