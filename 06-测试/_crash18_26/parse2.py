
import struct, bisect

path = r"C:\Users\17242\AppData\Local\CrashDumps\UnityCrossFire.exe.15552.dmp"
data = open(path,'rb').read()
sig,ver,nstreams,dirrva,chk,tds,flags = struct.unpack_from('<IIIIIIQ', data, 0)
streams={}
for i in range(nstreams):
    st,dsize,rva = struct.unpack_from('<III', data, dirrva+12*i); streams[st]=(dsize,rva)
def rstr(rva):
    ln=struct.unpack_from('<I',data,rva)[0]; return data[rva+4:rva+4+ln].decode('utf-16-le','replace')
mods=[]; d,r=streams[4]; n=struct.unpack_from('<I',data,r)[0]; off=r+4
for i in range(n):
    base,size,csum,tds2,namerva=struct.unpack_from('<QIIII',data,off); mods.append((base&0xffffffff,size,rstr(namerva))); off+=108
mods.sort(); bases=[m[0] for m in mods]
def modname(a):
    a&=0xffffffff; i=bisect.bisect_right(bases,a)-1
    if i>=0:
        b,s,nm=mods[i]
        if a<b+s: return "%s+0x%x"%(nm.split('\\')[-1],a-b)
    return None
d5,r5=streams[5]; nmr=struct.unpack_from('<I',data,r5)[0]; ranges=[];o=r5+4
for i in range(nmr):
    st,sz,rv=struct.unpack_from('<QII',data,o); ranges.append((st&0xffffffff,sz,rv)); o+=16
ranges.sort(); rstarts=[x[0] for x in ranges]
def read_mem(addr,length):
    a=addr&0xffffffff; i=bisect.bisect_right(rstarts,a)-1
    if i>=0:
        s,sz,rv=ranges[i]
        if a>=s and a+length<=s+sz: return data[rv+(a-s):rv+(a-s)+length]
    return None
def dword(a):
    b=read_mem(a,4); return struct.unpack('<I',b)[0] if b else None

exc = 0x42096b30
print("memory ranges containing 0x%08x:"%exc, [hex(s) for (s,sz,rv) in ranges if s<=exc<s+sz])
b=read_mem(exc,0x20)
print("bytes @exc:", b.hex() if b else None)
klass = dword(exc)
print("klass =", hex(klass) if klass else klass)
if klass:
    print("range contains klass:", [hex(s) for (s,sz,rv) in ranges if s<=klass<s+sz])
    kb = read_mem(klass,0x40)
    print("klass bytes:", kb.hex() if kb else None)
    if kb:
        nameptr = struct.unpack_from('<I',kb,0x08)[0]
        nsp = struct.unpack_from('<I',kb,0x0C)[0]
        print("name ptr = 0x%08x  namespace ptr = 0x%08x"%(nameptr,nsp))
        for p,label in ((nameptr,'name'),(nsp,'namespace')):
            raw=read_mem(p,64)
            if raw:
                z=raw.split(b'\x00')[0]
                print(" %s = %r"%(label,z.decode('utf-8','replace')))
            else:
                print(" %s unreadable"%label)
# also try to interpret exc+0x0C etc as strings
print("\nscan 0x%08x for ascii strings:"%exc)
raw=read_mem(exc,0x80)
if raw:
    import re
    for m in re.finditer(rb'[ -~]{5,}', raw):
        print("  +0x%x %r"%(m.start(), m.group().decode()))
else:
    print("  unreadable")
# list captured ranges
print("\ncaptured ranges (%d):"%len(ranges))
for s,sz,rv in ranges[:40]:
    print("  %08x-%08x size=%x"%(s,s+sz,sz))
