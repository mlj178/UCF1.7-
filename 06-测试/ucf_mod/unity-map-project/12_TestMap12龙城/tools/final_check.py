
import UnityPy, os, json, collections

D = "D:/ucf_test_level12/game/UnityCrossFire_Data"
env = UnityPy.load(D + "/level12")
sf = None
for name, f in env.files.items():
    if hasattr(f, "objects"):
        sf = f
        break
print("deployed level12 objects:", len(sf.objects))
for k, e in enumerate(sf.externals):
    try:
        print("  ext", k, repr(e.path), "type", e.type)
    except Exception as ex:
        print("  ext", k, "err", ex)

ext_ids = collections.Counter()
sample = []
for pid, obj in sf.objects.items():
    if obj.type.name == "MeshFilter":
        try:
            tree = obj.read()
            m = tree.m_Mesh
            ext_ids[str(m.m_FileID)] += 1
            if len(sample) < 3:
                sample.append({"path_id": m.m_PathID, "file_id": m.m_FileID})
        except Exception as ex:
            ext_ids["err"] += 1
print("MeshFilter m_Mesh fileIDs:", dict(ext_ids))
print("sample:", sample)

# check globalgamemanagers scene count
import struct
ggm = open(D + "/globalgamemanagers", "rb").read()
print("globalgamemanagers size", len(ggm))
i = ggm.find(b"Assets/Scenes/")
names = []
while i != -1:
    j = ggm.find(b"\x00", i)
    names.append(ggm[i:j].decode("utf-8", "replace"))
    i = ggm.find(b"Assets/Scenes/", j)
print("scenes found:", names)
