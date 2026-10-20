
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
# memory list
size, rva = streams[5][0]
nr = struct.unpack_from('<I', data, rva)[0]
ranges=[]
off=rva+4
for i in range(nr):
    start, dsize, drva = struct.unpack_from('<QII', data, off)
    ranges.append((start, dsize, drva)); off+=16
ranges.sort()
print('ranges', len(ranges))
def readmem(addr, n):
    for s,ds,r in ranges:
        if s <= addr < s+ds:
            avail = min(n, s+ds-addr)
            return data[r+(addr-s):r+(addr-s)+avail]
    return None
bad = 0x233e7e00
m = readmem(bad-0x80, 0x200)
print('memory at fault:', 'yes' if m else 'no')
if m:
    base = bad-0x80
    for i in range(0, len(m), 16):
        chunk = m[i:i+16]
        print('%08x: %s  | %s' % (base+i, chunk.hex(' '), ''.join(chr(c) if 32<=c<127 else '.' for c in chunk)))
# stack window
size, rva = streams[6][0]; tid=struct.unpack_from('<I',data,rva)[0]
size, rva = streams[3][0]; cnt=struct.unpack_from('<I',data,rva)[0]; off=rva+4
for i in range(cnt):
    thid, susp, pclass, prio = struct.unpack_from('<IIII', data, off)
    teb = struct.unpack_from('<Q', data, off+16)[0]
    st_start, st_size, st_rva = struct.unpack_from('<QII', data, off+24)
    cs, cr = struct.unpack_from('<II', data, off+40)
    if thid==tid: T=(st_start,st_size,st_rva,cs,cr)
    off+=48
st_start,st_size,st_rva,cs,cr=T
stack=data[st_rva:st_rva+st_size]
print('--- stack 6ee600-6eeb40 ---')
for a in range(0x6ee600,0x6eeb40,4):
    v=struct.unpack_from('<I', stack, a-st_start)[0]
    nm,o=modof(v)
    print('%08x: %08x %s' % (a,v,('%s+0x%x'%(nm,o)) if nm else ''))
