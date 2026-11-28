
import re
p = r"D:/trae_project/ucf1.7-modifier/00-游戏逆向分析-相关信息/Il2CppDumper/dump.cs"
lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
for i, l in enumerate(lines):
    if re.search(r"class (NavGraph|PointGraph|GridGraph)\b", l):
        print("=====", l.strip()[:90])
        for j in range(i+1, min(i+90, len(lines))):
            s = lines[j]
            if s.strip() == "}": break
            if "// 0x" in s:
                print("   ", s.strip()[:120])
