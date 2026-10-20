
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
base=0x233e7e00
m=readmem(base,0x100)
print('obj len', len(m) if m else None)
if m:
    for o in range(0,0x100,0x10):
        chunk=m[o:o+0x10]
        vals=struct.unpack_from('<4I',chunk,0)
        print('+%03x: %s | %s' % (o, chunk.hex(' '), ' '.join('%08x'%v for v in vals)))
