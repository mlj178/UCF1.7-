
import os, shutil, struct
import UnityPy

GAME = "D:/ucf_test_level12/game/UnityCrossFire_Data"
OUT = "D:/ucf_unity/out_final"

# ---------- pairs ----------
envO = UnityPy.load(OUT + "/sharedassets12.assets")
sfo = None
for k, f in envO.files.items():
    if hasattr(f, "objects"):
        sfo = f; break
meshes, mats = {}, {}
for pid, o in sfo.objects.items():
    if o.type.name == "Mesh":
        meshes[o.read_typetree().get("m_Name","")] = pid
    elif o.type.name == "Material":
        mats[o.read_typetree().get("m_Name","")] = pid
pairs = []
for nm, mpid in meshes.items():
    if not nm.startswith("GRP_"):
        continue
    key = nm[4:]
    matid = mats.get("M_GRP_" + key)
    if matid is None:
        continue
    pairs.append((key, mpid, matid))
pairs.sort(key=lambda x: (0 if x[0] == "zzground" else 1, x[0]))
print("pairs", len(pairs))

# ---------- load level11 ----------
env = UnityPy.load(GAME + "/level11")
sf = None
for k, f in env.files.items():
    if hasattr(f, "objects"):
        sf = f; break
objs = sf.objects
type_of = {pid: o.type.name for pid, o in objs.items()}
go_name, go_tree = {}, {}
for pid, o in objs.items():
    if o.type.name == "GameObject":
        t = o.read_typetree()
        go_name[pid] = t.get("m_Name", "")
        go_tree[pid] = [c["component"]["m_PathID"] for c in t.get("m_Component", []) if c["component"]["m_FileID"] == 0]

# ---------- renderer / component map ----------
info = []
for pid, o in objs.items():
    if o.type.name != "MeshRenderer":
        continue
    t = o.read_typetree()
    gopid = t["m_GameObject"]["m_PathID"]
    cs = go_tree.get(gopid, [])
    info.append({"mr": pid, "go": gopid,
                 "tr": next((c for c in cs if type_of.get(c) == "Transform"), None),
                 "mf": next((c for c in cs if type_of.get(c) == "MeshFilter"), None),
                 "mc": next((c for c in cs if type_of.get(c) == "MeshCollider"), None)})
info.sort(key=lambda r: (0 if r["mc"] else 1, r["go"]))

# ---------- null any PPtr into external slot 3 ----------
nulled = [0]
def walk(node):
    if isinstance(node, dict):
        if "m_FileID" in node and "m_PathID" in node:
            if node["m_FileID"] == 3:
                node["m_FileID"] = 0; node["m_PathID"] = 0; nulled[0] += 1
            return
        for v in node.values(): walk(v)
    elif isinstance(node, list):
        for v in node: walk(v)

for pid, o in objs.items():
    try:
        t = o.read_typetree()
    except Exception:
        continue
    before = nulled[0]
    walk(t)
    if nulled[0] != before:
        o.save_typetree(t)
print("nulled external-3 PPtrs:", nulled[0])

# ---------- FIX SPAWN HEIGHT INSIDE MapManager ----------
SPAWN_Y = 3.0
mm_pid = None
for pid, o in objs.items():
    if o.type.name == "MonoBehaviour":
        raw0 = o.get_raw_data()
        if len(raw0) < 12:
            continue
        fid, gopid = struct.unpack("<iq", raw0[:12])
        if fid == 0 and go_name.get(gopid) == "MapManager":
            mm_pid = pid
            break
print("MapManager pid", mm_pid)
fixed = 0
if mm_pid is not None:
    o = objs[mm_pid]
    raw = bytearray(o.get_raw_data())
    for off in range(0, len(raw) - 12, 4):
        x, y, z = struct.unpack("<fff", raw[off:off+12])
        if abs(y + 1.85) < 0.02 and -200 < x < 200 and -200 < z < 200:
            struct.pack_into("<f", raw, off + 4, SPAWN_Y)
            fixed += 1
    if fixed:
        o.set_raw_data(bytes(raw))
print("spawn points raised:", fixed)

# ---------- repoint renderers ----------
used = info[:len(pairs)]
unused = info[len(pairs):]
father_fix = []
for r, (key, mpid, matid) in zip(used, pairs):
    t = objs[r["mf"]].read_typetree()
    t["m_Mesh"] = {"m_FileID": 3, "m_PathID": mpid}
    objs[r["mf"]].save_typetree(t)

    t = objs[r["mr"]].read_typetree()
    t["m_Materials"] = [{"m_FileID": 3, "m_PathID": matid}]
    t["m_Enabled"] = True
    objs[r["mr"]].save_typetree(t)

    if r["mc"]:
        t = objs[r["mc"]].read_typetree()
        t["m_Mesh"] = {"m_FileID": 3, "m_PathID": mpid}
        objs[r["mc"]].save_typetree(t)

    t = objs[r["tr"]].read_typetree()
    if t["m_Father"]["m_PathID"] != 0:
        father_fix.append((t["m_Father"]["m_PathID"], r["tr"]))
    t["m_LocalRotation"] = {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
    t["m_LocalPosition"] = {"x": 0.0, "y": 0.0, "z": 0.0}
    t["m_LocalScale"] = {"x": 1.0, "y": 1.0, "z": 1.0}
    t["m_Father"] = {"m_FileID": 0, "m_PathID": 0}
    objs[r["tr"]].save_typetree(t)

for r in unused:
    if r["mf"]:
        t = objs[r["mf"]].read_typetree(); t["m_Mesh"] = {"m_FileID": 0, "m_PathID": 0}; objs[r["mf"]].save_typetree(t)
    if r["mc"]:
        t = objs[r["mc"]].read_typetree(); t["m_Mesh"] = {"m_FileID": 0, "m_PathID": 0}; objs[r["mc"]].save_typetree(t)
    if r["tr"]:
        t = objs[r["tr"]].read_typetree(); t["m_LocalScale"] = {"x": 0.0, "y": 0.0, "z": 0.0}; objs[r["tr"]].save_typetree(t)

for fpid, cpid in father_fix:
    o = objs.get(fpid)
    if o is None: continue
    t = o.read_typetree()
    t["m_Children"] = [c for c in t.get("m_Children", []) if c.get("m_PathID") != cpid]
    o.save_typetree(t)

print("used", len(used), "hidden", len(unused))

out = sf.save()
i = out.find(b"sharedassets11.assets")
if i != -1:
    out = out[:i] + b"sharedassets12.assets" + out[i+21:]
    print("renamed external")
open(OUT + "/level12", "wb").write(out)

for fn in ["level12", "sharedassets12.assets", "sharedassets12.assets.resS"]:
    shutil.copyfile(OUT + "/" + fn, GAME + "/" + fn)
    print("deployed", fn, os.path.getsize(GAME + "/" + fn))
