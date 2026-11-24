
import os, shutil

SRC = "D:/ucf_unity/build/UcfTest_Data"
OUT = "D:/ucf_unity/out_final"
os.makedirs(OUT, exist_ok=True)

data = bytearray(open(SRC + "/level0", "rb").read())
print("hex 70330..70500:")
print(data[70330:70500].hex())

needle = b"sharedassets0.assets"
i = data.find(needle)
assert i == 70345, i
new = b"sharedassets12.assets\x00"
assert len(new) == 22, len(new)
assert data[i:i+22][20:22] == b"\x00\x00"
data[i:i+22] = new
print("patched at", i, "->", bytes(data[i-4:i+30]))

open(OUT + "/level12", "wb").write(bytes(data))

shutil.copyfile(SRC + "/sharedassets0.assets", OUT + "/sharedassets12.assets")
shutil.copyfile(SRC + "/sharedassets0.assets.resS", OUT + "/sharedassets12.assets.resS")

for f in ["level12", "sharedassets12.assets", "sharedassets12.assets.resS"]:
    print(f, os.path.getsize(OUT + "/" + f))
