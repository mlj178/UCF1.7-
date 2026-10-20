
import struct, sys, os, json
path = sys.argv[1]
data = open(path,'rb').read()
sig, ver, nstreams, dir_rva, checksum, tds, flags = struct.unpack_from('<IIIIIIQ', data, 0)
streams = {}
for i in range(nstreams):
    st, size, rva = struct.unpack_from('<III', data, dir_rva + i*12)
    streams.setdefault(st, []).append((size, rva))

mods = []
size, rva = streams[4][0]
n = struct.unpack_from('<I', data, rva)[0]
off = rva+4
for i in range(n):
    base, imgsize, cksum, ts, namerva = struct.unpack_from('<QIIII', data, off)
    nameoff = struct.unpack_from('<I', data, namerva)[0]
    name = data[namerva+4:namerva+4+nameoff].decode('utf-16-le','replace')
    mods.append((base, imgsize, name))
    off += 108

def modof(a):
    for b,s,nm in mods:
        if b <= a < b+s: return nm, a-b
    return None, None

# exception
size, rva = streams[6][0]
tid = struct.unpack_from('<I', data, rva)[0]
code, eflags, erec, eaddr, nparams, unused = struct.unpack_from('<IIQQII', data, rva+8)
params = struct.unpack_from('<15Q', data, rva+8+32)
print('tid',tid,'code',hex(code),'addr',hex(eaddr),'params',[hex(p) for p in params[:nparams]])

threads=[]
size, rva = streams[3][0]
cnt = struct.unpack_from('<I', data, rva)[0]
off = rva+4
for i in range(cnt):
    thid, susp, pclass, prio = struct.unpack_from('<IIII', data, off)
    teb = struct.unpack_from('<Q', data, off+16)[0]
    st_start, st_size, st_rva = struct.unpack_from('<QII', data, off+24)
    cs, cr = struct.unpack_from('<II', data, off+40)
    threads.append((thid, st_start, st_size, st_rva, cs, cr, teb))
    off += 48

th = [t for t in threads if t[0]==tid][0]
thid, st_start, st_size, st_rva, cs, cr, teb = th
print('thread stack %x size %x ctx size %x' % (st_start, st_size, cs))
ctx = data[cr:cr+cs]
print('ctx head:', ctx[:32].hex(' '))
# interpret as x86 context
edi, esi, ebx, edx, ecx, eax = struct.unpack_from('<6I', ctx, 156)
ebp, eip, segcs, efl, esp, segss = struct.unpack_from('<6I', ctx, 180)
print('x86 EIP=%08x ESP=%08x EBP=%08x EAX=%08x EBX=%08x ECX=%08x EDX=%08x ESI=%08x EDI=%08x' % (eip,esp,ebp,eax,ebx,ecx,edx,esi,edi))
# interpret as amd64
if cs >= 0x4d0:
    rip = struct.unpack_from('<Q', ctx, 0xf8)[0]
    rsp = struct.unpack_from('<Q', ctx, 0x98)[0]
    rbp = struct.unpack_from('<Q', ctx, 0xa0)[0]
    print('x64 RIP=%016x RSP=%016x RBP=%016x' % (rip,rsp,rbp))

# stack bytes
stack = data[st_rva:st_rva+st_size]
print('stack bytes', len(stack), 'range %x-%x' % (st_start, st_start+st_size))
# find code pointers
hits=[]
for i in range(0, len(stack)-3, 4):
    v = struct.unpack_from('<I', stack, i)[0]
    nm, offv = modof(v)
    if nm and (nm.lower().endswith('gameassembly.dll') or 'frida-agent' in nm.lower() or nm.lower().endswith('unityplayer.dll')):
        hits.append((st_start+i, v, nm, offv))
print('code pointer hits:', len(hits))
for addr,v,nm,offv in hits[-120:]:
    print('  %08x -> %08x %s+0x%x' % (addr, v, os.path.basename(nm), offv))
json.dump(dict(start=st_start,size=st_size,base=mods), open('.dsh-tmp-dis/stack_meta.json','w'))
open('.dsh-tmp-dis/stack.bin','wb').write(stack)
