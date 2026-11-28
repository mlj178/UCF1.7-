
import re
p = r"D:/trae_project/ucf1.7-modifier/00-游戏逆向分析-相关信息/Il2CppDumper/dump.cs"
lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
targets = {"NavmeshBase": ["..ctor", "Scan"], "NavMeshGraph": ["..ctor", "Scan", "ScanInternal"], "NavGraph": ["Scan"]}
cur = None
for i, l in enumerate(lines):
    m = re.match(r"\s*(?:public |internal |private |protected )*(?:sealed |abstract )*class (\w+)", l)
    if m:
        cur = m.group(1)
    if cur in targets:
        s = l.strip()
        for t in targets[cur]:
            if t in s and ("{" in s):
                rva = lines[i-1].strip() if i > 0 else ""
                if "RVA" in rva:
                    print("%-14s %-46s %s" % (cur, s[:46], rva[:80]))
