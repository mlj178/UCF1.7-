
import struct, sys
p=r'D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\GameAssembly.dll'
data=open(p,'rb').read()
for va in [0x1012AF7F,0x103D18E2,0x1072BE79,0x109DA472,0x10154FBA,0x102BF6F8,0x105C0E4B,0x10B30F3C,0x10B67F07]:
    pat=struct.pack('<I',va)
    offs=[]
    start=0
    while True:
        i=data.find(pat,start)
        if i<0: break
        offs.append(i)
        start=i+1
        if len(offs)>10: break
    print(hex(va), 'data refs(file offsets):', [hex(x) for x in offs[:10]])
