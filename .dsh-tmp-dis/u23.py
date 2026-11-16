
import UnityPy, os
BASE = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data"
for lvl in ["level10","level8","level1"]:
    env = UnityPy.load(os.path.join(BASE,lvl))
    sf = list(env.files.values())[0]
    print(lvl)
    for pid_, o in sf.objects.items():
        if o.type.name != "Mesh": continue
        try:
            m = o.read()
            print("   mesh", pid_, repr(m.m_Name), "verts", m.m_VertexData.m_VertexCount, "submeshes", len(m.m_SubMeshes))
        except Exception as e:
            print("   mesh", pid_, "ERR", type(e).__name__, str(e)[:80])
