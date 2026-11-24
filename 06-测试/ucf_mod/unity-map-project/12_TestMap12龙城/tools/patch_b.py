
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
        print("WARN no material for", key); continue
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

go_name = {}
for pid, o in objs.items():
    if o.type.name == "GameObject":
        go_name[pid] = o.read_typetree().get("m_Name", "")

go_tree = {}
for pid, o in objs.items():
    if o.type.name == "GameObject":
        go_tree[pid] = [c["component"]["m_PathID"] for c in o.read_typetree().get("m_Component", [])
                        if c["component"]["m_FileID"] == 0]

info = []
for pid, o in objs.items():
    if o.type.name != "MeshRenderer":
        continue
    t = o.read_typetree()
    gopid = t["m_GameObject"]["m_PathID"]
    cs = go_tree.get(gopid, [])
    info.append({
        "mr": pid, "go": gopid,
        "tr": next((c for c in cs if type_of.get(c) == "Transform"), None),
        "mf": next((c for c in cs if type_of.get(c) == "MeshFilter"), None),
        "mc": next((c for c in cs if type_of.get(c) == "MeshCollider"), None),
    })
info.sort(key=lambda r: (0 if r["mc"] else 1, r["go"]))
print("renderers", len(info), "with collider", sum(1 for r in info if r["mc"]))

# ---------- null any PPtr into external slot 3 (fileID 3) ----------
nulled = [0]
def walk(node):
    if isinstance(node, dict):
        if "m_FileID" in node and "m_PathID" in node:
            if node["m_FileID"] == 3:
                node["m_FileID"] = 0; node["m_PathID"] = 0
                nulled[0] += 1
            return
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)

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

# ---------- apply ----------
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
print("used", len(used), "hidden", len(unused))

for fpid, cpid in father_fix:
    o = objs.get(fpid)
    if o is None:
        continue
    t = o.read_typetree()
    ch = [c for c in t.get("m_Children", []) if c.get("m_PathID") != cpid]
    t["m_Children"] = ch
    o.save_typetree(t)

# keep BoxColliders enabled (they carry DeathRing's floor)
print("boxcolliders left untouched")

# ---- move spawn markers above our ground slab ----
spawn_moved = 0
for pid, o in objs.items():
    if o.type.name == "Transform":
        t = o.read_typetree()
        gopid = t["m_GameObject"]["m_PathID"]
        nm = go_name.get(gopid, "")
        if nm in ("SpawnVel_BL", "SpawnVel_GR"):
            t["m_LocalPosition"] = {"x": 0.0, "y": 40.0, "z": -40.0 if "BL" in nm else 40.0}
            o.save_typetree(t)
            spawn_moved += 1
print("spawn markers moved:", spawn_moved)

# ---- repurpose one BoxCollider as a giant invisible floor ----
box_used = 0
for pid, o in objs.items():
    if o.type.name != "BoxCollider":
        continue
    t = o.read_typetree()
    gopid = t["m_GameObject"]["m_PathID"]
    cs = go_tree.get(gopid, [])
    trp = next((c for c in cs if type_of.get(c) == "Transform"), None)
    if box_used == 0:
        t["m_Center"] = {"x": 0.0, "y": -1.0, "z": 0.0}
        t["m_Size"] = {"x": 2000.0, "y": 2.0, "z": 2000.0}
        t["m_IsTrigger"] = False
        if "m_Enabled" in t:
            t["m_Enabled"] = True
        o.save_typetree(t)
        if trp:
            tt = objs[trp].read_typetree()
            if tt["m_Father"]["m_PathID"] != 0:
                father_fix.append((tt["m_Father"]["m_PathID"], trp))
            tt["m_LocalRotation"] = {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
            tt["m_LocalPosition"] = {"x": 0.0, "y": 0.0, "z": 0.0}
            tt["m_LocalScale"] = {"x": 1.0, "y": 1.0, "z": 1.0}
            tt["m_Father"] = {"m_FileID": 0, "m_PathID": 0}
            objs[trp].save_typetree(tt)
        box_used += 1
    else:
        if "m_Enabled" in t:
            t["m_Enabled"] = False
            o.save_typetree(t)
print("box floor installed:", box_used)

out = sf.save()
print("saved", len(out))
i = out.find(b"sharedassets11.assets")
if i != -1:
    out = out[:i] + b"sharedassets12.assets" + out[i+21:]
    print("renamed external at", i)
open(OUT + "/level12", "wb").write(out)

# verify
env2 = UnityPy.load(out)
for k, f in env2.files.items():
    if hasattr(f, "objects"):
        print("reload ok objects", len(f.objects))
        for kk, e in enumerate(f.externals):
            print("  ext", kk, e.path)
        break

for fn in ["level12", "sharedassets12.assets", "sharedassets12.assets.resS"]:
    shutil.copyfile(OUT + "/" + fn, GAME + "/" + fn)
    print("deployed", fn, os.path.getsize(GAME + "/" + fn))
