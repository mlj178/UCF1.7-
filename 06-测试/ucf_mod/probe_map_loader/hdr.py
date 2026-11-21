# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding="utf-8")
import struct
G = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire_Data\globalgamemanagers"
P = r"D:\\trae_project\\ucf1.7-modifier\\06-测试\\ucf_mod\\probe_map_loader\\work\globalgamemanagers.patched"
for tag,p in [("orig",G),("patched",P)]:
    d = open(p,"rb").read(64)
    print(tag, d[:48].hex())
    print("  u32 @0,4,8,12:", struct.unpack_from("<IIII", d, 0))
    print("  u32 @16,20,24,28:", struct.unpack_from("<IIII", d, 16))
