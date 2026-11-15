
import struct, sys, os
path=sys.argv[1]
data=open(path,'rb').read()
sig,ver,nstreams,dirrva=struct.unpack_from('<IIII',data,0)
streams={}
for i in range(nstreams):
    st,ds,rva=struct.unpack_from('<III',data,dirrva+i*12); streams[st]=(ds,rva)
def utf16(rva):
    n=struct.unpack_from('<I',data,rva)[0]; return data[rva+4:rva+4+n].decode('utf-16-le','replace')
mods=[]
_,rva=streams[4]; n=struct.unpack_from('<I',data,rva)[0]
for i in range(n):
    off=rva+4+i*108; base,size=struct.unpack_from('<QI',data,off); nr=struct.unpack_from('<I',data,off+20)[0]
    mods.append((base,size,utf16(nr)))
mods.sort()
def modof(a):
    for b,s,nm in mods:
        if b<=a<b+s: return (b,s,nm)
_,rva=streams[6]
tid,align=struct.unpack_from('<II',data,rva)
code,eflags,rec,eaddr,nparams,_=struct.unpack_from('<IIQQII',data,rva+8)
params=[struct.unpack_from('<Q',data,rva+8+32+i*8)[0] for i in range(min(nparams,15))]
ctx_size,ctx_rva=struct.unpack_from('<II',data,rva+8+32+15*8)
print('file',os.path.basename(path),'tid',tid,'code=%08x eaddr=%08x params=%s'%(code,eaddr,[hex(x) for x in params]))
if code==0xe06d7363:
    print('  exception object ptr:',hex(params[1]) if len(params)>1 else '?', 'type_info:',hex(params[2]) if len(params)>2 else '?', 'throwinfo:',hex(params[3]) if len(params)>3 else '?')
edi,esi,ebx,edx,ecx,eax=struct.unpack_from('<IIIIII',data,ctx_rva+0x9c)
ebp,eip,cs,eflags2,esp,ss=struct.unpack_from('<IIIIII',data,ctx_rva+0xb4)
print('eax=%08x ebx=%08x ecx=%08x edx=%08x esi=%08x edi=%08x ebp=%08x eip=%08x esp=%08x'%(eax,ebx,ecx,edx,esi,edi,ebp,eip,esp))
m=modof(eaddr); print('fault', m[2] if m else '?', hex(eaddr-m[0]) if m else '')
ranges=[]
_,rva=streams[5]; n=struct.unpack_from('<I',data,rva)[0]
for i in range(n):
    st,ms,mr=struct.unpack_from('<QII',data,rva+4+i*16); ranges.append((st,ms,mr))
if 9 in streams:
    _,rva=streams[9]; n,base=struct.unpack_from('<QI',data,rva); cur=base
    for i in range(n):
        st,ms=struct.unpack_from('<QQ',data,rva+12+i*16); ranges.append((st,ms,cur)); cur+=ms
ranges.sort()
def readmem(addr,size):
    for st,ms,mr in ranges:
        if st<=addr and addr+size<=st+ms: return data[mr+(addr-st):mr+(addr-st)+size]
    return None
print('--- ebp chain ---')
p=ebp
for k in range(30):
    b=readmem(p,8)
    if not b: break
    nex,ret=struct.unpack('<II',b)
    m=modof(ret)
    print('frm%02d ebp=%08x ret=%08x %s'%(k,p,ret, (os.path.basename(m[2])+'+%x'%(ret-m[0])) if m else '?'))
    if nex<=p or nex-p>0x10000: break
    p=nex
print('--- stack module ptrs ---')
st=readmem(esp,0x8000) or b''
seen=set()
for i in range(0,len(st)-4,4):
    v=struct.unpack_from('<I',st,i)[0]; m=modof(v)
    if m and v not in seen:
        seen.add(v); print('%08x -> %08x %s+%x'%(esp+i,v,os.path.basename(m[2]),v-m[0]))
