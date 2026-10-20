
import struct, sys, os
path = sys.argv[1]
data = open(path,'rb').read()
sig, ver, nstreams, dir_rva, checksum, tds, flags = struct.unpack_from('<IIIIIIQ', data, 0)
streams = {}
for i in range(nstreams):
    st, size, rva = struct.unpack_from('<III', data, dir_rva + i*12)
    streams.setdefault(st, []).append((size, rva))
mods=[]
size, rva = streams[4][0]; n=struct.unpack_from('<I',data,rva)[0]; off=rva+4
for i in range(n):
    base, imgsize, cksum, ts, namerva = struct.unpack_from('<QIIII', data, off)
    nameoff = struct.unpack_from('<I', data, namerva)[0]
    name = data[namerva+4:namerva+4+nameoff].decode('utf-16-le','replace')
    mods.append((base, imgsize, name)); off+=108
def modof(a):
    for b,s,nm in mods:
        if b <= a < b+s: return os.path.basename(nm), a-b
    return None, None
size, rva = streams[6][0]
tid = struct.unpack_from('<I', data, rva)[0]
code, eflags, erec, eaddr, nparams, unused = struct.unpack_from('<IIQQII', data, rva+8)
size, rva = streams[3][0]; cnt=struct.unpack_from('<I',data,rva)[0]; off=rva+4
T=None
for i in range(cnt):
    thid, susp, pclass, prio = struct.unpack_from('<IIII', data, off)
    teb = struct.unpack_from('<Q', data, off+16)[0]
    st_start, st_size, st_rva = struct.unpack_from('<QII', data, off+24)
    cs, cr = struct.unpack_from('<II', data, off+40)
    if thid==tid: T=(st_start,st_size,st_rva,cs,cr)
    off+=48
st_start,st_size,st_rva,cs,cr=T
ctx=data[cr:cr+cs]
edi, esi, ebx, edx, ecx, eax = struct.unpack_from('<6I', ctx, 156)
ebp, eip, segcs, efl, esp, segss = struct.unpack_from('<6I', ctx, 180)
stack=data[st_rva:st_rva+st_size]
print('ESP=%08x EBP=%08x EIP=%08x' % (esp,ebp,eip))
print('--- stack from ESP ---')
for i in range(0, 220, 4):
    a=esp+i
    v=struct.unpack_from('<I', stack, a-st_start)[0]
    nm,o=modof(v)
    extra = ('%s+0x%x' % (nm,o)) if nm else ''
    print('%08x: %08x %s' % (a,v,extra))
print('--- EBP chain ---')
cur=ebp
for k in range(60):
    if not (st_start <= cur < st_start+st_size-8): print('ebp out',hex(cur)); break
    prev=struct.unpack_from('<I',stack,cur-st_start)[0]
    ret=struct.unpack_from('<I',stack,cur+4-st_start)[0]
    nm,o=modof(ret)
    print('EBP %08x -> prev %08x ret %08x %s' % (cur,prev,ret, ('%s+0x%x'%(nm,o)) if nm else ''))
    if prev<=cur: break
    cur=prev
