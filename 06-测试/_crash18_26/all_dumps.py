
import struct, bisect, os, glob

def analyze(path):
    out=[]
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
    if 6 not in streams: return "no exception stream"
    d,r=streams[6]
    tid,align=struct.unpack_from('<II',data,r)
    ec,ef,erec,eaddr,npar,unalign=struct.unpack_from('<IIQQII',data,r+8)
    params=struct.unpack_from('<15Q',data,r+40)
    ctxsize,ctxrva=struct.unpack_from('<II',data,r+160)
    edi,esi,ebx,edx,ecx,eax=struct.unpack_from('<6I',data,ctxrva+0x9C)
    ebp,eip,cs,efl,esp,ss=struct.unpack_from('<6I',data,ctxrva+0xB4)
    out.append("  file=%s size=%d"%(os.path.basename(path),len(data)))
    out.append("  code=0x%08x addr=0x%08x (%s) npar=%d params=%s"%(ec,eaddr,modname(eaddr),npar,[hex(x) for x in params[:npar]]))
    out.append("  eip=0x%08x (%s) esp=0x%08x ebp=0x%08x esi=0x%08x edi=0x%08x"%(eip,modname(eip),esp,ebp,esi,edi))
    eb=ebp; chain=[]
    for k in range(12):
        b=read_mem(eb,8)
        if not b: break
        sav,nxt=struct.unpack('<II',b)
        chain.append("%s"%modname(nxt))
        if sav<=eb: break
        eb=sav
    out.append("  ebp-chain: "+ " <- ".join(x or "?" for x in chain))
    return "\n".join(out)

base=r"C:\Users\17242\AppData\Local\CrashDumps"
for f in sorted(glob.glob(base+r"\UnityCrossFire.exe.*.dmp"), key=os.path.getmtime):
    print(f)
    print(analyze(f))
    print()
