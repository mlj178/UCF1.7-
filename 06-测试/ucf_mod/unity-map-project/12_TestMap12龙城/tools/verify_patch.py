
import UnityPy

GAME = "D:/ucf_test_level12/game/UnityCrossFire_Data"

envL = UnityPy.load(GAME + "/level12")
sl = None
for k, f in envL.files.items():
    if hasattr(f, "objects"):
        sl = f; break
print("level12 objects", len(sl.objects))

cnt = 0
for pid, o in sl.objects.items():
    if o.type.name == "MeshFilter":
        t = o.read_typetree()
        if t["m_Mesh"]["m_FileID"] == 3:
            print("MF", pid, "-> mesh", t["m_Mesh"]["m_PathID"])
            cnt += 1
            if cnt >= 5:
                break
print("MF pointing at ext3:", cnt)

# check a transform
n = 0
for pid, o in sl.objects.items():
    if o.type.name == "Transform":
        t = o.read_typetree()
        if t["m_Father"]["m_PathID"] == 0 and t["m_LocalScale"]["x"] == 1.0:
            print("Transform", pid, "pos", t["m_LocalPosition"], "scale", t["m_LocalScale"])
            n += 1
            if n >= 3: break

envS = UnityPy.load(GAME + "/sharedassets12.assets")
ss = None
for k, f in envS.files.items():
    if hasattr(f, "objects"):
        ss = f; break
print("shared12 objects", len(ss.objects))
names = {}
for pid, o in ss.objects.items():
    if o.type.name == "Mesh":
        names[pid] = o.read_typetree().get("m_Name","")
print("mesh path_ids sample:", list(names.items())[:5])

# does the path id referenced by MeshFilter exist?
for pid, o in sl.objects.items():
    if o.type.name == "MeshFilter":
        t = o.read_typetree()
        if t["m_Mesh"]["m_FileID"] == 3:
            tid = t["m_Mesh"]["m_PathID"]
            print("checking pathid", tid, "exists:", tid in ss.objects, ss.objects[tid].type.name if tid in ss.objects else "-")
            break
