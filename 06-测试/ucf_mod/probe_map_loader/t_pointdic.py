# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding="utf-8")
SRC = "D:/BaiduNetdiskDownload/原始/UnityCrossFire1.7.1/UnityCrossFire1.7.1/UnityCrossFire_Data/"
KEYS = ["BL","GR","Neutral","SupplyBox","RedBox","BlueBox","Netural"]
def pat(s):
    b = s.encode()
    pad = b"\x00" * ((4 - ((len(b)+1) % 4)) % 4 + 1)
    return struct.pack("<i", len(b)) + b + pad
print("level | " + " | ".join(KEYS))
for i in range(12):
    data = open(SRC + "level%d" % i, "rb").read()
    row = []
    for k in KEYS:
        row.append("Y" if data.find(pat(k)) >= 0 else "-")
    print("%d | %s" % (i, " | ".join(row)))
