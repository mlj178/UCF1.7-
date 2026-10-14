
import struct, bisect, sys, os, re

path = r"C:\Users\17242\AppData\Local\CrashDumps\UnityCrossFire.exe.15552.dmp"
data = open(path,'rb').read()
print("dump size", len(data), data[:4])
sig,ver,nstreams,dirrva,chk,tds,flags = struct.unpack_from('<IIIIIIQ', data, 0)
streams={}
for i in range(nstreams):
    st,dsize,rva = struct.unpack_from('<III', data, dirrva+12*i); streams[st]=(dsize,rva)
print("streams:", {k:(v[0],hex(v[1])) for k,v in sorted(streams.items())})

def rstr(rva):
    ln=struct.unpack_from('<I',data,rva)[0]; return data[rva+4:rva+4+ln].decode('utf-16-le','replace')

mods=[]
d,r=streams[4]; n=struct.unpack_from('<I',data,r)[0]; off=r+4
for i in range(n):
    base,size,csum,tds2,namerva=struct.unpack_from('<QIIII',data,off); mods.append((base&0xffffffff,size,rstr(namerva))); off+=108
mods.sort(); bases=[m[0] for m in mods]
def modname(a, full=False):
    a&=0xffffffff; i=bisect.bisect_right(bases,a)-1
    if i>=0:
        b,s,nm=mods[i]
        if a<b+s: return ("%s+0x%x"%(nm if full else nm.split('\\')[-1],a-b), b)
    return (None,None)

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

def x86ctx(rva):
    edi,esi,ebx,edx,ecx,eax=struct.unpack_from('<6I',data,rva+0x9C)
    ebp,eip,cs,efl,esp,ss=struct.unpack_from('<6I',data,rva+0xB4)
    return dict(edi=edi,esi=esi,ebx=ebx,edx=edx,ecx=ecx,eax=eax,ebp=ebp,eip=eip,esp=esp)

d,r=streams[6]
tid,align=struct.unpack_from('<II',data,r)
ec,ef,erec,eaddr,npar,unalign=struct.unpack_from('<IIQQII',data,r+8)
params=struct.unpack_from('<15Q',data,r+40)
ctxsize,ctxrva=struct.unpack_from('<II',data,r+160)
print("\n=== EXCEPTION STREAM ===")
print("thread=%d code=0x%08x flags=0x%x address=0x%08x npar=%d" % (tid,ec,ef,eaddr,npar))
print("params:", [hex(x) for x in params[:npar]])
mn,mb=modname(eaddr)
print("address module:", mn, "rva=0x%x"%(eaddr-mb) if mb else "")
c=x86ctx(ctxrva)
print("ctx eip=0x%08x (%s) esp=0x%08x ebp=0x%08x eax=%08x ebx=%08x ecx=%08x edx=%08x esi=%08x edi=%08x" % (
    c['eip'],modname(c['eip'])[0],c['esp'],c['ebp'],c['eax'],c['ebx'],c['ecx'],c['edx'],c['esi'],c['edi']))

print("\n=== EBP CHAIN (thread %d) ===" % tid)
ebp=c['ebp']
for k in range(80):
    b=read_mem(ebp,8)
    if not b: print("  [%02d] ebp=0x%08x unreadable"%(k,ebp)); break
    sav,nxt=struct.unpack('<II',b)
    print("  [%02d] ebp=0x%08x ret=0x%08x %s"%(k,ebp,nxt,modname(nxt)[0] or '?'))
    if sav<=ebp: print("  chain end"); break
    ebp=sav

print("\n=== STACK WORDS around esp ===")
raw=read_mem(c['esp']-0x40,0x300)
if raw:
    for i in range(0,len(raw),4):
        v=struct.unpack_from('<I',raw,i)[0]; nm=modname(v)[0]
        print("  esp%+5d 0x%08x %s"%(i-0x40,v,nm or ''))
print("\n=== C++ exception records (0xE06D7363) in memory ===")
pat=struct.pack('<I',0xE06D7363)
hits=0
for s,sz,rv in ranges:
    blob=data[rv:rv+sz]
    start=0
    while True:
        j=blob.find(pat,start)
        if j<0: break
        start=j+1
        rec=blob[j:j+0x100]
        if len(rec)>=0x50:
            code,efl2,erec2,eaddr2,npar2=struct.unpack_from('<IIQII',rec,0)
            if npar2==3:
                p0,p1,p2=struct.unpack_from('<III',rec,20)
                if p0==0x19930520:
                    hits+=1
                    print("record @0x%08x addr=%s params=[0x%08x,0x%08x,0x%08x]"%(s+j,modname(eaddr2)[0],p0,p1,p2))
                    if hits>20: break
        if hits>20: break
    if hits>20: break
print("records found:",hits)
