
import UnityPy

OUT = "D:/ucf_unity/out_final"
envO = UnityPy.load(OUT + "/sharedassets12.assets")
sfo = None
for k, f in envO.files.items():
    if hasattr(f, "objects"):
        sfo = f; break
for pid, o in sfo.objects.items():
    if o.type.name in ("Mesh", "Material"):
        t = o.read_typetree()
        print(o.type.name, pid, repr(t.get("m_Name")))
