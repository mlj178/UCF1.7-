
import os, shutil, struct

SRC = "D:/ucf_unity/build/UcfTest_Data"
OUT = "D:/ucf_unity/out_final"
GAME = "D:/ucf_test_level12/game/UnityCrossFire_Data"
TEST = "D:/ucf_test_level12/_test/glb"
os.makedirs(OUT, exist_ok=True); os.makedirs(TEST, exist_ok=True)

# ---- level ----
data = bytearray(open(SRC + "/level0", "rb").read())
old = b"sharedassets0.assets"
new = b"sharedassets12.assets"
i = data.find(old)
assert i != -1 and data.find(old, i + 1) == -1
assert data[i+20:i+22] == b"\x00\x00"
data[i:i+22] = new + b"\x00"
print("level external patched at", i)

# ---- shared assets: fix m_StreamData.path ----
sa = bytearray(open(SRC + "/sharedassets0.assets", "rb").read())
oldp = b"sharedassets0.assets.resS"      # 25 chars
newp = b"sharedassets12.assets.resS"     # 26 chars
cnt = 0
i = sa.find(oldp)
while i != -1:
    pre = struct.unpack("<i", sa[i-4:i])[0]
    assert pre == 25, ("unexpected prefix", pre, i)
    block = struct.pack("<i", 26) + newp + b"\x00\x00"
    assert len(block) == 32, len(block)
    sa[i-4:i-4+32] = block
    cnt += 1
    i = sa.find(oldp, i + 25)
print("resS paths patched:", cnt)
assert sa.find(oldp) == -1

open(OUT + "/level12", "wb").write(bytes(data))
open(OUT + "/sharedassets12.assets", "wb").write(bytes(sa))
src_res = SRC + "/sharedassets0.assets.resS"
dst_res = OUT + "/sharedassets12.assets.resS"
if os.path.exists(src_res):
    shutil.copyfile(src_res, dst_res)

# verify new name present
print("new path count in file:", bytes(sa).count(newp))

for f in ["level12", "sharedassets12.assets", "sharedassets12.assets.resS"]:
    shutil.copyfile(OUT + "/" + f, GAME + "/" + f)
    print("deployed", f, os.path.getsize(GAME + "/" + f))
for f in ["level12", "sharedassets12.assets"]:
    shutil.copyfile(OUT + "/" + f, TEST + "/" + f)
print("done")
