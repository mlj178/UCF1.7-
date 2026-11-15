
import struct, sys, os

path = sys.argv[1]
data = open(path,'rb').read()
sig, ver, nstreams, dirrva, csum, tds, flags = struct.unpack_from('<IIIIIII', data, 0)
assert sig == 0x504d444d, hex(sig)
streams = {}
for i in range(nstreams):
    st, dsize, rva = struct.unpack_from('<III', data, dirrva + i*12)
    streams[st] = (dsize, rva)
print('streams:', sorted(streams.keys()))

def read_utf16(rva):
    n = struct.unpack_from('<I', data, rva)[0]
    return data[rva+4:rva+4+n].decode('utf-16-le', 'replace')

# system info
if 7 in streams:
    _, rva = streams[7]
    arch, level, rev, ncpu, prodtype, major, minor, build, plat = struct.unpack_from('<HHHBBIIII', data, rva)
    print('arch', arch, 'build', build, 'plat', plat)

# modules
mods = []
if 4 in streams:
    _, rva = streams[4]
    n = struct.unpack_from('<I', data, rva)[0]
    for i in range(n):
        off = rva + 4 + i*108
        base, size = struct.unpack_from('<QI', data, off)
        name_rva = struct.unpack_from('<I', data, off+20)[0]
        name = read_utf16(name_rva)
        mods.append((base, size, name))
mods.sort()
print('modules:', len(mods))
for b,s,n in mods:
    if any(k in n.lower() for k in ['unitycrossfire','gameassembly','ucf_mod','frida','unityplayer','winhttp','kernelbase','ntdll']):
        print('  %08x %08x %s' % (b,s,n))

def modof(addr):
    for b,s,n in mods:
        if b <= addr < b+s:
            return (b,s,n)
    return None

# exception
if 6 in streams:
    _, rva = streams[6]
    tid, align = struct.unpack_from('<II', data, rva)
    code, eflags, rec, eaddr, nparams, _ = struct.unpack_from('<IIQQII', data, rva+8)
    params = [struct.unpack_from('<Q', data, rva+8+32+i*8)[0] for i in range(min(nparams,15))]
    ctx_size, ctx_rva = struct.unpack_from('<II', data, rva+8+32+15*8)
    print('exception tid=%d code=%08x addr=%08x nparams=%d params=%s ctxsize=%d' % (tid, code, eaddr, nparams, [hex(p) for p in params], ctx_size))
    regs = {}
    if ctx_size >= 0xcc:
        eax,ebx,ecx,edx,esi,edi,ebp,eip,esp = struct.unpack_from('<IIIIIIIII', data, ctx_rva+0xa4)
        regs = dict(eax=eax,ebx=ebx,ecx=ecx,edx=edx,esi=esi,edi=edi,ebp=ebp,eip=eip,esp=esp)
        print('regs:', {k:hex(v) for k,v in regs.items()})
    m = modof(eaddr)
    if m: print('fault module:', m[2], 'offset=%x' % (eaddr-m[0]))

# memory ranges
ranges = []
for st in (5,):
    if st in streams:
        _, rva = streams[st]
        n = struct.unpack_from('<I', data, rva)[0]
        for i in range(n):
            off = rva+4+i*16
            start, msize, mrva = struct.unpack_from('<QII', data, off)
            ranges.append((start,msize,mrva))
if 9 in streams:
    _, rva = streams[9]
    n, base_rva = struct.unpack_from('<QI', data, rva)
    off = rva+12
    cur = base_rva
    for i in range(n):
        start, msize = struct.unpack_from('<QQ', data, off+i*16)
        ranges.append((start,msize,cur))
        cur += msize
ranges.sort()
print('ranges:', len(ranges))

def readmem(addr, size):
    for start,msize,mrva in ranges:
        if start <= addr and addr+size <= start+msize:
            o = mrva + (addr-start)
            return data[o:o+size]
    return None

# stack scan
if regs:
    esp = regs['esp']
    stack = readmem(esp, 0x4000) or b''
    print('stack bytes', len(stack))
    seen = set()
    out = []
    for i in range(0, len(stack)-4, 4):
        v = struct.unpack_from('<I', stack, i)[0]
        m = modof(v)
        if m:
            key=(v,)
            if key in seen: continue
            seen.add(key)
            out.append((esp+i, v, m[2], v-m[0]))
    for a,v,n,o in out[:120]:
        print('stack %08x -> %08x %s+%x' % (a,v,os.path.basename(n),o))
