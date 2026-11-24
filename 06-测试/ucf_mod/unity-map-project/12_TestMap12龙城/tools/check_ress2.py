
import os, collections

GAME = "D:/ucf_test_level12/game/UnityCrossFire_Data"
print("=== data dir resS files ===")
for f in sorted(os.listdir(GAME)):
    if f.lower().endswith(".ress"):
        print("  ", f, os.path.getsize(os.path.join(GAME, f)))

target = GAME + "/sharedassets0.assets"
d = open(target, "rb").read()
print("\nsharedassets0.assets size", len(d))
occ = []
i = d.find(b".resS")
while i != -1:
    occ.append(i)
    i = d.find(b".resS", i + 1)
print("occurrences of .resS:", len(occ))
for i in occ[:8]:
    # walk back to start of printable run
    s = i
    while s > 0 and 32 <= d[s-1] < 127:
        s -= 1
    name = d[s:i+5]
    print("  at", i, "str=", name, "len=", len(name), "pre8=", d[s-8:s].hex(), "post=", d[i+5:i+9].hex())
