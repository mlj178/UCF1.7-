
import struct

path = r"C:\Users\17242\AppData\Local\CrashDumps\UnityCrossFire.exe.8596.dmp"
data = open(path,'rb').read()
sig, ver, nstreams, dirrva, chk, tds, flags = struct.unpack_from('<IIIIIIQ', data, 0)
streams={}
for i in range(nstreams):
    st, dsize, rva = struct.unpack_from('<III', data, dirrva+12*i)
    streams[st]=(dsize,rva)
def rstr(rva):
    ln = struct.unpack_from('<I', data, rva)[0]
    return data[rva+4:rva+4+ln].decode('utf-16-le','replace')
mods=[]
d,r = streams[4]
n = struct.unpack_from('<I', data, r)[0]
off=r+4
for i in range(n):
    base,size,csum,tds2,namerva = struct.unpack_from('<QIIII', data, off)
    mods.append((base&0xffffffff, size, rstr(namerva)))
    off+=108
mods.sort()
import bisect
bases=[m[0] for m in mods]
def classify(a):
    a &= 0xffffffff
    i = bisect.bisect_right(bases, a)-1
    if i>=0:
        b,s,nm = mods[i]
        if a < b+s:
            return "%s+0x%x" % (nm.split('\\')[-1], a-b)
    return None
def modname(a):
    c=classify(a)
    return c

# exception
d,r = streams[6]
tid, align = struct.unpack_from('<II', data, r)
ec, ef, erec, eaddr, npar, unused = struct.unpack_from('<IIQQII', data, r+8)
params = struct.unpack_from('<15Q', data, r+32)
ctxsize, ctxrva = struct.unpack_from('<II', data, r+152)
print("ExceptionStream: tid=%d code=0x%08x flags=0x%x addr=0x%08x nparams=%d params=%s" % (tid, ec, ef, eaddr, npar, [hex(x) for x in params[:npar]]))
print("  ctx size=%d rva=%x" % (ctxsize, ctxrva))

def x86ctx(rva):
    f = struct.unpack_from('<I', data, rva)[0]
    edi,esi,ebx,edx,ecx,eax = struct.unpack_from('<6I', data, rva+0x9C)
    ebp,eip,cs,efl,esp,ss = struct.unpack_from('<6I', data, rva+0xB4)
    return dict(flags=f, edi=edi,esi=esi,ebx=ebx,edx=edx,ecx=ecx,eax=eax,ebp=ebp,eip=eip,esp=esp)

# threads
d,r = streams[3]
nt = struct.unpack_from('<I', data, r)[0]
threads=[]
off=r+4
for i in range(nt):
    tid2, sc, pc, pri, teb = struct.unpack_from('<IIIIQ', data, off)
    sstart, ssize, srva = struct.unpack_from('<QII', data, off+24)
    csize, crva = struct.unpack_from('<II', data, off+40)
    threads.append(dict(tid=tid2, stack=(sstart&0xffffffff, ssize, srva), ctx=(csize,crva)))
    off+=48
print("threads=%d" % nt)
fault=[t for t in threads if t['tid']==tid][0]
c=x86ctx(fault['ctx'][1])
print("FAULT thread %d  eip=0x%08x esp=0x%08x ebp=0x%08x eax=0x%08x ebx=0x%08x ecx=0x%08x edx=0x%08x esi=0x%08x edi=0x%08x" % (tid,c['eip'],c['esp'],c['ebp'],c['eax'],c['ebx'],c['ecx'],c['edx'],c['esi'],c['edi']))
print("  eip classified:", modname(c['eip']), " addr in event 0x48a7df00 classified:", modname(0x48a7df00))

memrange_streams = {}
d5,r5 = streams[5]
nmr = struct.unpack_from('<I', data, r5)[0]
memranges=[]
o=r5+4
for i in range(nmr):
    st,sz,rv = struct.unpack_from('<QII', data, o)
    memranges.append((st&0xffffffff, sz, rv))
    o+=16
def read_mem(addr, length):
    a=addr&0xffffffff
    i=bisect.bisect_right([m[0] for m in memranges], a)-1
    if i>=0:
        s,sz,rv = memranges[i]
        if a>=s and a+length<=s+sz:
            return data[rv+(a-s):rv+(a-s)+length]
    return None

# walk ebp chain
print("\n=== EBP chain (fault thread) ===")
ebp=c['ebp']
for k in range(40):
    b=read_mem(ebp,8)
    if not b: 
        print("  [%02d] ebp=0x%08x unreadable" % (k,ebp)); break
    sav,nxt = struct.unpack('<II', b)
    cl = modname(nxt)
    print("  [%02d] ebp=0x%08x -> ret=0x%08x %s" % (k, ebp, nxt, cl or "(no module)"))
    if nxt==0 and sav==0: break
    ebp=sav

print("\n=== stack scan around esp (fault thread) ===")
esp=c['esp']
base=esp-0x40
raw=read_mem(base, 0x400)
if raw:
    for i in range(0, 0x400, 4):
        v=struct.unpack_from('<I', raw, i)[0]
        cl=modname(v)
        if cl:
            print("  [esp%+d] 0x%08x %s" % (i-0x40, v, cl))
