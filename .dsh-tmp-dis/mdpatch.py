
import struct, sys
path = sys.argv[1]
data=open(path,'rb').read()
sig,ver,nstreams,dir_rva,checksum,tds,flags=struct.unpack_from('<IIIIIIQ',data,0)
streams={}
for i in range(nstreams):
    st,size,rva=struct.unpack_from('<III',data,dir_rva+i*12); streams.setdefault(st,[]).append((size,rva))
size,rva=streams[5][0]; nr=struct.unpack_from('<I',data,rva)[0]; ranges=[]; off=rva+4
for i in range(nr):
    s,ds,r=struct.unpack_from('<QII',data,off); ranges.append((s,ds,r)); off+=16
ranges.sort()
def readmem(a,n):
    for s,ds,r in ranges:
        if s<=a<s+ds:
            av=min(n,s+ds-a); return data[r+(a-s):r+(a-s)+av]
    return None
base=0x5e8e0000
checks={
 'bot_cave_B30F3C':(0xB30F3C,32),
 'nano_tail_AF04FB':(0xAF04FB,16),
 'nano_idx_AF04EA':(0xAF04EA,8),
 'supply_B44895':(0xB44895,8),
 'cap_AF9C69':(0xAF9C69,2),
 'conv_B25C68':(0xB25C68,4),
 'name_B67F07':(0xB67F07,8),
 'cave_154FBA':(0x154FBA,24),
 'cave_2BF6F8':(0x2BF6F8,24),
}
for k,(rva,n) in checks.items():
    m=readmem(base+rva,n)
    print(k, hex(base+rva), m.hex(' ') if m else 'NOT IN DUMP')
