
import binascii, struct
p = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod\\backup\\vis_history_20261116_122127\\navmesh_nm944-a99b40ea454de4a0.bin"
d = open(p,'rb').read()
print(len(d))
print(binascii.hexlify(d[:80]).decode())
print("ascii:", "".join(chr(c) if 32<=c<127 else "." for c in d[:80]))
for i in range(0, 40, 4):
    print(i, struct.unpack_from("<I", d, i)[0], struct.unpack_from("<f", d, i)[0])
