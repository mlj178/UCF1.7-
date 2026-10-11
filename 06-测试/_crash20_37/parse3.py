
import struct, bisect

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
    mods.append((base&0xffffffff, size, rstr(namerva))); off+=108
mods.sort(); bases=[m[0] for m in mods]
def modname(a):
    a&=0xffffffff
    i=bisect.bisect_right(bases,a)-1
    if i>=0:
        b,s,nm=mods[i]
        if a<b+s: return "%s+0x%x" % (nm.split('\\')[-1], a-b)
    return None

d5,r5 = streams[5]
nmr = struct.unpack_from('<I', data, r5)[0]
ranges=[]
o=r5+4
for i in range(nmr):
    st,sz,rv = struct.unpack_from('<QII', data, o)
    ranges.append((st&0xffffffff, sz, rv)); o+=16
ranges.sort(); rstarts=[x[0] for x in ranges]
print("mem ranges:", nmr)
def read_mem(addr,length):
    a=addr&0xffffffff
    i=bisect.bisect_right(rstarts,a)-1
    if i>=0:
        s,sz,rv=ranges[i]
        if a>=s and a+length<=s+sz: return data[rv+(a-s):rv+(a-s)+length]
    return None

d,r = streams[6]
tid, align = struct.unpack_from('<II', data, r)
ec, ef, erec, eaddr, npar, unused = struct.unpack_from('<IIQQII', data, r+8)
print("exc code=0x%08x addr=0x%08x npar=%d" % (ec,eaddr,npar))
raw_params = struct.unpack_from('<15Q', data, r+32)
print("  params:", [hex(x) for x in raw_params[:npar]])
# raw hex of exception stream to verify layout
print("  exc stream hex:", data[r:r+168].hex())

d,r = streams[3]
nt=struct.unpack_from('<I',data,r)[0]
threads=[];off=r+4
for i in range(nt):
    tid2,sc,pc,pri,teb=struct.unpack_from('<IIIIQ',data,off)
    sstart,ssize,srva=struct.unpack_from('<QII',data,off+24)
    csize,crva=struct.unpack_from('<II',data,off+40)
    threads.append(dict(tid=tid2,stack=(sstart&0xffffffff,ssize,srva),ctx=(csize,crva)));off+=48
fault=[t for t in threads if t['tid']==tid][0]
print("fault thread stack: start=0x%08x size=0x%x rva=0x%x captured=%s" % (fault['stack'][0],fault['stack'][1],fault['stack'][2], read_mem(fault['stack'][0],16) is not None))

def x86ctx(rva):
    edi,esi,ebx,edx,ecx,eax=struct.unpack_from('<6I',data,rva+0x9C)
    ebp,eip,cs,efl,esp,ss=struct.unpack_from('<6I',data,rva+0xB4)
    return dict(edi=edi,esi=esi,ebx=ebx,edx=edx,ecx=ecx,eax=eax,ebp=ebp,eip=eip,esp=esp)
c=x86ctx(fault['ctx'][1])
print("FAULT ctx eip=0x%08x esp=0x%08x ebp=0x%08x edx=0x%08x eax=0x%08x  eip=%s" % (c['eip'],c['esp'],c['ebp'],c['edx'],c['eax'],modname(c['eip'])))

print("\n=== EBP chain ===")
ebp=c['ebp']
for k in range(50):
    b=read_mem(ebp,8)
    if not b: print("  [%02d] ebp=0x%08x unreadable" % (k,ebp)); break
    sav,nxt=struct.unpack('<II',b)
    print("  [%02d] ebp=0x%08x ret=0x%08x %s" % (k,ebp,nxt,modname(nxt) or '(none)'))
    if sav<=ebp and k>0: 
        print("   (chain not increasing, stop)"); break
    ebp=sav

print("\n=== stack dump around esp ===")
raw=read_mem(c['esp'],0x300)
if raw:
    for i in range(0,0x300,4):
        v=struct.unpack_from('<I',raw,i)[0]
        cl=modname(v)
        mark='*' if cl else ' '
        print("  %s esp+0x%03x 0x%08x %s" % (mark,i,v,cl or ''))
else:
    print("  esp region not captured")
