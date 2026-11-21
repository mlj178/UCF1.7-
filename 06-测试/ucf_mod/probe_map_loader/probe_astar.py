# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import UnityPy
D = "D:/ucf_test_level12/game/UnityCrossFire_Data/"
for f in ["level3","level4","level11"]:
    p = D + f
    buf = open(p,"rb").read()
    env = UnityPy.load(p)
    sf = list(env.files.values())[0]
    print(f"===== {f}  objects {len(sf.objects)}  filesize {len(buf)}")
    big = []
    for pid, oi in sf.objects.items():
        tn = getattr(oi.type, "name", str(oi.type))
        if tn == "MonoBehaviour" and oi.byte_size >= 1200:
            big.append((oi.byte_size, pid, oi.byte_start))
    big.sort(reverse=True)
    for size, pid, start in big[:5]:
        blob = buf[start:start+size]
        print(f"  pid={pid} size={size} head={blob[:32].hex()}")
        for name, pat in [("i32 4,2,17", bytes([4,0,0,0,2,0,0,0,17,0,0,0])),
                          ("i32 4,2,2",  bytes([4,0,0,0,2,0,0,0,2,0,0,0])),
                          ("b 4,2,17",   bytes([4,2,17])),
                          ("b 4,2,2",    bytes([4,2,2]))]:
            i = blob.find(pat)
            if i >= 0: print(f"      {name} @ 0x{i:x}")
