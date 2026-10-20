
import struct, sys, os
path = sys.argv[1]
data = open(path,'rb').read()
sig, ver, nstreams, dir_rva, checksum, tds, flags = struct.unpack_from('<IIIIIIQ', data, 0)
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
size,rva=streams[6][0]; tid=struct.unpack_from('<I',data,rva)[0]
size,rva=streams[3][0]; cnt=struct.unpack_from('<I',data,rva)[0]; off=rva+4
for i in range(cnt):
    thid,susp,pclass,prio=struct.unpack_from('<IIII',data,off)
    teb=struct.unpack_from('<Q',data,off+16)[0]
    st_start,st_size,st_rva=struct.unpack_from('<QII',data,off+24)
    cs,cr=struct.unpack_from('<II',data,off+40)
    if thid==tid: T=(st_start,st_size,st_rva,cs,cr)
    off+=48
st_start,st_size,st_rva,cs,cr=T
stack=data[st_rva:st_rva+st_size]
def rd(a): return struct.unpack_from('<I',stack,a-st_start)[0]
print('fault ctx: EIP=%08x ESP=%08x EBP=%08x EAX=%08x EDX=%08x EDI=%08x' % (rd(0x6ee8b0),rd(0x6eec60),rd(0x6eeca8),rd(0x6ee8a8),rd(0x6ee8a0),rd(0x6ee894)))
print('--- stack 6eec00-6eed40 ---')
for a in range(0x6eec00,0x6eed40,4):
    v=rd(a); nm,o=modof(v)
    print('%08x: %08x %s' % (a,v,('%s+0x%x'%(nm,o)) if nm else ''))
print('--- EBP chain from fault EBP ---')
cur=0x6eeca8
for k in range(30):
    prev=rd(cur); ret=rd(cur+4); nm,o=modof(ret)
    print('EBP %08x prev %08x ret %08x %s' % (cur,prev,ret,('%s+0x%x'%(nm,o)) if nm else ''))
    if prev<=cur or prev==0: break
    cur=prev
