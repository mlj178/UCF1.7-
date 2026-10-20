
import struct, sys
path=sys.argv[1]
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
for a,n,label in [(0x10E35B80,0x40,'pref_base_class'),(0x10E35DC0,0x20,'pref_base_vtable_slot'),(0x233e7e00,0x60,'obj'),(0x9B0000,0x10,'low'),(0x5e8e0000,0x20,'module_base')]:
    m=readmem(a,n)
    print(label, hex(a), m.hex(' ') if m else 'NOT IN DUMP')
# memory info list protections
if 15 in streams:
    size,rva=streams[15][0]
    hdr=struct.unpack_from('<IIQQ',data,rva)
    print('meminfo hdr', [hex(x) for x in hdr])
    count=hdr[1]; entries=[]
    off=rva+16
    for i in range(count):
        base,alloc,align,prot,typ,state=struct.unpack_from('<QQIIII',data,off); off+=32
        if base <= 0x10E35B80 < base+ (1<<32) and abs(base-0x10E35B80)<0x1000000:
            print('prot entry',hex(base),hex(alloc),hex(prot),hex(typ),hex(state))
        if base <= 0x10000000 < base+0x2000000:
            print('range near 0x10000000:',hex(base),hex(alloc),hex(prot),hex(typ),hex(state))
