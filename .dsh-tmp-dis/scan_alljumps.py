
import struct
p=r'D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\GameAssembly.dll'
data=open(p,'rb').read()
targets={0x12AF7F,0x3D18E2,0x72BE79,0x9DA472,0x5C0E4B,0x154FBA,0x2BF6F8}
secs=[(0x400,0x196000,0xC00),(0x196000,0xB7FC00,0x1000)]
found=[]
for fs,fe,delta in secs:
    buf=data[fs:fe]
    n=len(buf)
    for i in range(n-6):
        rva=fs+i+delta
        op=buf[i]
        tgt=None; kind=None
        if op in (0xE8,0xE9):
            rel=struct.unpack_from('<i',buf,i+1)[0]; tgt=(rva+5+rel)&0xFFFFFFFF; kind='call' if op==0xE8 else 'jmp'
        elif op==0xEB or 0x70<=op<=0x7F:
            rel=struct.unpack_from('<b',buf,i+1)[0]; tgt=(rva+2+rel)&0xFFFFFFFF; kind='jcc8'
        elif op==0x0F and 0x80<=buf[i+1]<=0x8F:
            rel=struct.unpack_from('<i',buf,i+2)[0]; tgt=(rva+6+rel)&0xFFFFFFFF; kind='jcc32'
        if tgt in targets:
            found.append((rva,kind,hex(tgt)))
for f in found[:50]: print(f)
print('total',len(found))
