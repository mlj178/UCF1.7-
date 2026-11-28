
import re
p = r"D:/trae_project/ucf1.7-modifier/00-游戏逆向分析-相关信息/Il2CppDumper/dump.cs"
lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
for i, l in enumerate(lines):
    if re.search(r"\bNavmeshBase\(\)|\bNavMeshGraph\(\)|\bNavGraph\(\)|NavmeshUpdateSettings", l):
        print(i+1, l.strip()[:130])
