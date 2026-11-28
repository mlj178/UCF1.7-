
import re
p = r"D:/trae_project/ucf1.7-modifier/00-游戏逆向分析-相关信息/Il2CppDumper/dump.cs"
lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
cur = None
for i, l in enumerate(lines):
    m = re.match(r"\s*(?:public |internal |private |protected )*(?:sealed |abstract )?class (\w+)", l)
    if m: cur = m.group(1)
    if "ReplaceTile" in l and "{" in l:
        print("%-16s %s" % (cur, l.strip()[:120]))
print("--- NavmeshTile fields ---")
cur = None
for i, l in enumerate(lines):
    m = re.match(r"\s*(?:public |internal |private |protected )*(?:sealed |abstract )?class (\w+)", l)
    if m: cur = m.group(1)
    if cur == "NavmeshTile" and "// 0x" in l:
        print("   ", l.strip()[:100])
