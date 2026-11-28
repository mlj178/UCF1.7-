
import UnityPy, collections, os
base = "D:/BaiduNetdiskDownload/ucf_test_level12/game/UnityCrossFire_Data"
files = [base + "/" + f for f in ("level9", "sharedassets9.assets", "sharedassets9.assets.resS")]
files = [f for f in files if os.path.isfile(f)]
print("files", len(files))
env = UnityPy.load(*files)
c = collections.Counter(); tris = 0; verts = 0
for o in env.objects:
    t = o.type.name
    c[t] += 1
    if t == "Mesh":
        try:
            m = o.read()
            ib = getattr(m, "m_IndexBuffer", None)
            if ib: tris += len(ib) // 2
            verts += int(getattr(m, "m_VertexCount", 0) or 0)
        except Exception:
            pass
print(dict(c.most_common(12)))
print("mesh objects", c["Mesh"], "approx verts", verts, "approx index16", tris)
