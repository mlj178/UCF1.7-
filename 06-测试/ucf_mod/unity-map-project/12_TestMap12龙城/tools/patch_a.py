
import os, shutil, struct, collections
import UnityPy

GAME = "D:/ucf_test_level12/game/UnityCrossFire_Data"
SRCB = "D:/ucf_unity/build/UcfTest_Data"
OUT = "D:/ucf_unity/out_final"
os.makedirs(OUT, exist_ok=True)

# ---------- 1. shared assets: rename + fix resS paths ----------
sa = bytearray(open(SRCB + "/sharedassets0.assets", "rb").read())
oldp = b"sharedassets0.assets.resS"
newp = b"sharedassets12.assets.resS"
n = 0
i = sa.find(oldp)
while i != -1:
    assert struct.unpack("<i", sa[i-4:i])[0] == 25
    sa[i-4:i-4+32] = struct.pack("<i", 26) + newp + b"\x00\x00"
    n += 1
    i = sa.find(oldp, i + 25)
print("resS paths patched:", n)
open(OUT + "/sharedassets12.assets", "wb").write(bytes(sa))
res_src = SRCB + "/sharedassets0.assets.resS"
if os.path.exists(res_src):
    shutil.copyfile(res_src, OUT + "/sharedassets12.assets.resS")
    print("resS", os.path.getsize(OUT + "/sharedassets12.assets.resS"))

# ---------- 2. read our meshes / materials ----------
envO = UnityPy.load(OUT + "/sharedassets12.assets")
sfo = None
for k, f in envO.files.items():
    if hasattr(f, "objects"):
        sfo = f; break

meshes = {}
mats = {}
for pid, o in sfo.objects.items():
    if o.type.name == "Mesh":
        nmm = o.read_typetree().get("m_Name", "")
        meshes[nmm] = pid
    elif o.type.name == "Material":
        nmm = o.read_typetree().get("m_Name", "")
        mats[nmm] = pid
print("meshes", len(meshes), "materials", len(mats))

pairs = []
for name, mpid in meshes.items():
    if name.startswith("GRP_"):
        key = name[4:]
        matname = "GRP_" + key
        if matname in mats:
            pairs.append((key, mpid, mats[matname]))
print("pairs", len(pairs))
pairs.sort(key=lambda x: (0 if x[0] == "zzground" else 1, x[0]))

# ---------- 3. build level12 shell ----------
d = open(GAME + "/level11", "rb").read()
open(OUT + "/level12_shell_src.bin", "wb").write(d)
print("shell base", len(d))
