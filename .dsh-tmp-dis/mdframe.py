
import struct, sys
path=sys.argv[1]
data=open(path,'rb').read()
sig,ver,nstreams,dir_rva,checksum,tds,flags=struct.unpack_from('<IIIIIIQ',data,0)
streams={}
for i in range(nstreams):
    st,size,rva=struct.unpack_from('<III',data,dir_rva+i*12); streams.setdefault(st,[]).append((size,rva))
size,rva=streams[3][0]; cnt=struct.unpack_from('<I',data,rva)[0]; off=rva+4
T=None
for i in range(cnt):
    thid,susp,pclass,prio=struct.unpack_from('<IIII',data,off)
    st_start,st_size,st_rva=struct.unpack_from('<QII',data,off+24)
    if thid==7744: T=(st_start,st_size,st_rva)
    off+=48
st_start,st_size,st_rva=T
stack=data[st_rva:st_rva+st_size]
def rd(a): return struct.unpack_from('<I',stack,a-st_start)[0]
ebp=0x12eee68
print('frame:')
for k,label in [(4,'ret'),(8,'this'),(0xc,'player'),(0x10,'boxType'),(0x14,'method')]:
    print('  [ebp+0x%x] %s = %08x' % (k,label,rd(ebp+k)))
this=rd(ebp+8)
# dump object fields from stack only if object on stack? read memory list
size,rva=streams[5][0]; nr=struct.unpack_from('<I',data,rva)[0]; ranges=[]; off=rva+4
for i in range(nr):
    s,ds,r=struct.unpack_from('<QII',data,off); ranges.append((s,ds,r)); off+=16
ranges.sort()
def readmem(a,n):
    for s,ds,r in ranges:
        if s<=a<s+ds:
            av=min(n,s+ds-a); return data[r+(a-s):r+(a-s)+av]
    return None
for a,n,label in [(this,0xC0,'this obj'),(rd(ebp+0xc),0x40,'player obj')]:
    m=readmem(a,n)
    print(label,hex(a), 'len', len(m) if m else None)
    if m:
        for o in range(0,len(m),0x10):
            vals=struct.unpack_from('<4I',m,o)
            print('  +%03x: %s' % (o,' '.join('%08x'%v for v in vals)))
