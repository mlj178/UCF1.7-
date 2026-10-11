
import struct, bisect
path = r"C:\Users\17242\AppData\Local\CrashDumps\UnityCrossFire.exe.8596.dmp"
data=open(path,'rb').read()
sig,ver,nstreams,dirrva,chk,tds,flags=struct.unpack_from('<IIIIIIQ',data,0)
streams={}
for i in range(nstreams):
    st,dsize,rva=struct.unpack_from('<III',data,dirrva+12*i); streams[st]=(dsize,rva)
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
d,r=streams[6]
tid,align=struct.unpack_from('<II',data,r)
ec,ef,erec,eaddr,npar,unalign=struct.unpack_from('<IIQQII',data,r+8)
params=struct.unpack_from('<15Q',data,r+40)
ctxsize,ctxrva=struct.unpack_from('<II',data,r+160)
print("tid=%d code=0x%08x addr=0x%08x npar=%d params=%s ctxsize=%d ctxrva=0x%x"%(tid,ec,eaddr,npar,[hex(x) for x in params[:npar]],ctxsize,ctxrva))
def x86ctx(rva):
    edi,esi,ebx,edx,ecx,eax=struct.unpack_from('<6I',data,rva+0x9C)
    ebp,eip,cs,efl,esp,ss=struct.unpack_from('<6I',data,rva+0xB4)
    return dict(edi=edi,esi=esi,ebx=ebx,edx=edx,ecx=ecx,eax=eax,ebp=ebp,eip=eip,esp=esp)
c=x86ctx(ctxrva)
print("EXC ctx eip=0x%08x (%s) esp=0x%08x ebp=0x%08x eax=0x%08x ebx=0x%08x ecx=0x%08x edx=0x%08x esi=0x%08x edi=0x%08x"%(c['eip'],modname(c['eip']),c['esp'],c['ebp'],c['eax'],c['ebx'],c['ecx'],c['edx'],c['esi'],c['edi']))
print("\n=== EBP chain at exception ===")
ebp=c['ebp']
for k in range(60):
    b=read_mem(ebp,8)
    if not b: print("  [%02d] ebp=0x%08x unreadable"% (k,ebp)); break
    sav,nxt=struct.unpack('<II',b)
    print("  [%02d] ebp=0x%08x ret=0x%08x %s"%(k,ebp,nxt,modname(nxt) or '(none)'))
    if sav<=ebp: print("   chain not increasing; stop"); break
    ebp=sav
print("\n=== stack words around esp ===")
raw=read_mem(c['esp']-0x20,0x200)
if raw:
    for i in range(0,0x200,4):
        v=struct.unpack_from('<I',raw,i)[0]; cl=modname(v)
        print("  %s esp%+d 0x%08x %s"%('*' if cl else ' ',i-0x20,v,cl or ''))
else: print("  not captured")
