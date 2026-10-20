
import struct, sys, os
path=sys.argv[1]
data=open(path,'rb').read()
sig,ver,nstreams,dir_rva,checksum,tds,flags=struct.unpack_from('<IIIIIIQ',data,0)
streams={}
for i in range(nstreams):
    st,size,rva=struct.unpack_from('<III',data,dir_rva+i*12); streams.setdefault(st,[]).append((size,rva))
mods=[]
size,rva=streams[4][0]; n=struct.unpack_from('<I',data,rva)[0]; off=rva+4
for i in range(n):
    base,imgsize,cksum,ts,namerva=struct.unpack_from('<QIIII',data,off)
    nameoff=struct.unpack_from('<I',data,namerva)[0]
    name=data[namerva+4:namerva+4+nameoff].decode('utf-16-le','replace')
    mods.append((base,imgsize,name)); off+=108
def modof(a):
    for b,s,nm in mods:
        if b<=a<b+s: return os.path.basename(nm),a-b
    return None,None
# exception
size,rva=streams[6][0]
tid=struct.unpack_from('<I',data,rva)[0]
code,eflags,erec,eaddr,nparams,unused=struct.unpack_from('<IIQQII',data,rva+8)
params=struct.unpack_from('<15Q',data,rva+8+32)
print('EXC tid=%d code=%08x addr=%08x nparams=%d params=%s' % (tid,code,eaddr,nparams,[hex(p) for p in params[:nparams]]))
# threads
size,rva=streams[3][0]; cnt=struct.unpack_from('<I',data,rva)[0]; off=rva+4
T=None
for i in range(cnt):
    thid,susp,pclass,prio=struct.unpack_from('<IIII',data,off)
    teb=struct.unpack_from('<Q',data,off+16)[0]
    st_start,st_size,st_rva=struct.unpack_from('<QII',data,off+24)
    cs,cr=struct.unpack_from('<II',data,off+40)
    if thid==tid: T=(st_start,st_size,st_rva,cs,cr,teb)
    off+=48
st_start,st_size,st_rva,cs,cr,teb=T
stack=data[st_rva:st_rva+st_size]
def rd(a):
    if not (st_start<=a<=st_start+st_size-4): return None
    return struct.unpack_from('<I',stack,a-st_start)[0]
# find x86 CONTEXT with matching EIP
found=None
for i in range(0,len(stack)-0xcc,4):
    if struct.unpack_from('<I',stack,i)[0]==0x0001007f:
        eip=struct.unpack_from('<I',stack,i+0xb8)[0]
        if eip==eaddr or True:
            found=(st_start+i,eip); break
print('thread stack=%x..%x teb=%x ctxsize=%x' % (st_start,st_start+st_size,teb,cs))
if found:
    B,eip=found
    edi,esi,ebx,edx,ecx,eax=struct.unpack_from('<6I',stack,B-st_start+156)
    ebp,eip2,segcs,efl,esp,segss=struct.unpack_from('<6I',stack,B-st_start+180)
    print('CONTEXT@%08x EIP=%08x ESP=%08x EBP=%08x EAX=%08x EBX=%08x ECX=%08x EDX=%08x ESI=%08x EDI=%08x' % (B,eip2,esp,ebp,eax,ebx,ecx,edx,esi,edi))
    print('stack from ESP:')
    for k in range(0,40,4):
        a=esp+k; v=rd(a); nm,o=modof(v) if v else (None,None)
        print('  %08x: %08x %s' % (a,v,('%s+0x%x'%(nm,o)) if nm else ''))
    print('EBP chain from fault EBP:')
    cur=ebp
    for k in range(30):
        prev=rd(cur); ret=rd(cur+4)
        if prev is None or ret is None: break
        nm,o=modof(ret)
        print('  EBP %08x prev %08x ret %08x %s' % (cur,prev,ret,('%s+0x%x'%(nm,o)) if nm else ''))
        if prev<=cur or prev==0: break
        cur=prev
# fault memory
size,rva=streams[5][0]; nr=struct.unpack_from('<I',data,rva)[0]; ranges=[]; off=rva+4
for i in range(nr):
    s,ds,r=struct.unpack_from('<QII',data,off); ranges.append((s,ds,r)); off+=16
ranges.sort()
def readmem(a,n):
    for s,ds,r in ranges:
        if s<=a<s+ds:
            av=min(n,s+ds-a); return data[r+(a-s):r+(a-s)+av]
    return None
m=readmem(eaddr-0x40,0x100)
print('fault memory:', 'yes' if m else 'no')
if m:
    base=eaddr-0x40
    for i in range(0,len(m),16):
        chunk=m[i:i+16]
        print('  %08x: %s | %s' % (base+i,chunk.hex(' '),''.join(chr(c) if 32<=c<127 else '.' for c in chunk)))
