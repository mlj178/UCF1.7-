
import struct
p=r'D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\GameAssembly.dll'
data=open(p,'rb').read()
targets={0x12AF7F:'12AF7F',0x3D18E2:'3D18E2',0x72BE79:'72BE79',0x9DA472:'9DA472'}
# sections: (file_start, file_end, rva_delta)
secs=[(0x400,0x196000,0xC00),(0x196000,0xB7FC00,0x1000)]
found={v:[] for v in targets}
for fs,fe,delta in secs:
    buf=data[fs:fe]
    for i in range(len(buf)-5):
        op=buf[i]
        if op not in (0xE8,0xE9): continue
        rel=struct.unpack_from('<i',buf,i+1)[0]
        rva=(fs+i)+delta
        tgt=(rva+5+rel) & 0xFFFFFFFF
        if tgt in targets:
            found[targets[tgt]].append((rva, 'call' if op==0xE8 else 'jmp'))
for k,v in found.items():
    print(k, len(v), [ (hex(a),t) for a,t in v[:20] ])
