
import struct, binascii
p = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod\\vis\\navmesh_nm944-a99b40ea454de4a0.bin"
d = open(p,'rb').read()
print(len(d), binascii.hexlify(d[:64]).decode())
print("ascii", "".join(chr(c) if 32<=c<127 else "." for c in d[:64]))
