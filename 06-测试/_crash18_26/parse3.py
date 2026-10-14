
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
def cstr(a,maxlen=120):
    b=read_mem(a,maxlen)
    if not b: return None
    return b.split(b'\x00')[0].decode('utf-8','replace')

mi = 0x11245c3c
print("MethodInfo candidate 0x%08x"%mi)
print("captured ranges containing it:", [ "%08x(+%x)"%(s,mi-s) for (s,sz,rv) in ranges if s<=mi<s+sz ])
b=read_mem(mi,0x30)
print("bytes:", b.hex() if b else None)
if b:
    methodPointer, invoker = struct.unpack_from('<II',b,0)
    nameptr, klass, rettype, params = struct.unpack_from('<IIII',b,8)
    flags = struct.unpack_from('<H',b,0x24)[0]
    print(" methodPointer=0x%08x (%s)"%(methodPointer, modname(methodPointer)))
    print(" invoker      =0x%08x (%s)"%(invoker, modname(invoker)))
    print(" name ptr     =0x%08x -> %r"%(nameptr, cstr(nameptr)))
    print(" klass        =0x%08x"%(klass))
    kb=read_mem(klass,0x10)
    if kb:
        kname, kns = struct.unpack_from('<II',kb,8)
        print(" klass name   =%r ns=%r"%(cstr(kname), cstr(kns)))
    print(" flags=0x%04x"%(flags))
print()
# also check the klass of 0x11245c3c region generally: dump nearby words
for off in range(0,0x40,4):
    w=struct.unpack_from('<I',b,off)[0] if b and off+4<=len(b) else None
    print("  +0x%02x = 0x%08x %s"%(off,w if w is not None else 0, (modname(w) if w else '') or ''))
