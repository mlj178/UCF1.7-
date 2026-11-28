
import re
p = r"D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod/src/navfix.c"
lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
start = None
for i, l in enumerate(lines):
    if "int navfix_load_navmesh(const char* path) {" in l:
        start = i
        break
print("start", start+1 if start is not None else None)
if start is not None:
    # find matching closing brace at column 0
    end = None
    for j in range(start, len(lines)):
        if lines[j] == "}":
            end = j
            break
    print("end", end+1 if end is not None else None)
    # also drop the preceding comment block
    s = start
    while s > 0 and lines[s-1].strip().startswith(("*", "/*", "*/")) or (s > 0 and lines[s-1].strip().startswith("/*")):
        s -= 1
        if lines[s].strip().startswith("/*"):
            break
    print("drop lines", s+1, "to", end+1)
    del lines[s:end+1]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("remaining", len(lines))
