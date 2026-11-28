
import re
p = r"D:/trae_project/ucf1.7-modifier/00-游戏逆向分析-相关信息/Il2CppDumper/dump.cs"
lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
for i, l in enumerate(lines):
    s = l.strip()
    if ("get_vertexCount" in s or "get_triangles" in s or "get_subMeshCount" in s) and "{" in s:
        rva = lines[i-1].strip()
        if "RVA" in rva:
            print("%-50s %s" % (s[:50], rva[:70]))
