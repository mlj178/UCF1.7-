
import re
p = r"D:/trae_project/ucf1.7-modifier/00-游戏逆向分析-相关信息/Il2CppDumper/dump.cs"
txt = open(p, encoding="utf-8", errors="replace").read()
m = re.search(r"\n(?:public )*sealed class Mesh\b.*?\n\{(.*?)\n\}", txt, re.S)
b = m.group(1) if m else ""
for line in b.splitlines():
    s = line.strip()
    if re.search(r"vertices|triangles|SetVertices|SetTriangles|vertexCount|subMeshCount", s, re.I):
        print("  ", s[:160])
print("---- List<T> Add? ----")
print("has set_vertices:", "set_vertices" in txt)
