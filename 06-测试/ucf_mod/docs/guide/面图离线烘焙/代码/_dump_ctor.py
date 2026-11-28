
import re
p = r"D:/trae_project/ucf1.7-modifier/00-游戏逆向分析-相关信息/Il2CppDumper/dump.cs"
txt = open(p, encoding="utf-8", errors="replace").read()
for pat in ("NavmeshBase..ctor", "NavMeshGraph..ctor", "NavGraph..ctor", "NavmeshUpdateSettings..ctor"):
    hits = [l.strip() for l in txt.splitlines() if pat in l]
    print(pat, "->", hits[:4])
