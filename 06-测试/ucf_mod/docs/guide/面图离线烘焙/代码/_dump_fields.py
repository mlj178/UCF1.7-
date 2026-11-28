
import re
p = r"D:/trae_project/ucf1.7-modifier/00-游戏逆向分析-相关信息/Il2CppDumper/dump.cs"
txt = open(p, encoding="utf-8", errors="replace").read()

def block(name):
    m = re.search(r"\n(?:public |internal |sealed |abstract )*class %s\b.*?\n\{(.*?)\n\}" % re.escape(name), txt, re.S)
    return m.group(1) if m else ""

for cls in ("NavmeshBase", "NavMeshGraph"):
    b = block(cls)
    print("=====", cls, "len", len(b))
    # fields with offsets
    for line in b.splitlines():
        if "// 0x" in line:
            print("  ", line.strip()[:140])

b = block("Mesh")
print("===== Mesh methods (Set*/Recalculate) =====")
for line in b.splitlines():
    if re.search(r"SetVertices|SetTriangles|SetIndices|RecalculateBounds|RecalculateNormals|Clear\(|MarkDynamic", line):
        print("  ", line.strip()[:140])
