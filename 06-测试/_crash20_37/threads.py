
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
        if a<b+s: return nm.split('\\')[-1]
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
d,r=streams[3]; nt=struct.unpack_from('<I',data,r)[0]; threads=[];off=r+4
def x86ctx(rva):
    edi,esi,ebx,edx,ecx,eax=struct.unpack_from('<6I',data,rva+0x9C)
    ebp,eip,cs,efl,esp,ss=struct.unpack_from('<6I',data,rva+0xB4)
    return dict(edi=edi,esi=esi,ebx=ebx,edx=edx,ecx=ecx,eax=eax,ebp=ebp,eip=eip,esp=esp)
for i in range(nt):
    tid2,sc,pc,pri,teb=struct.unpack_from('<IIIIQ',data,off)
    sstart,ssize,srva=struct.unpack_from('<QII',data,off+24)
    csize,crva=struct.unpack_from('<II',data,off+40)
    threads.append((tid2, sstart&0xffffffff, ssize, crva)); off+=48
interesting=('Universal','frida','UnityPlayer')
for tid,sstart,ssize,crva in threads:
    if crva==0: continue
    c=x86ctx(crva)
    # collect module hits by walking ebp chain + scanning stack
    hits={}
    ebp=c['ebp']
    for k in range(80):
        b=read_mem(ebp,8)
        if not b: break
        sav,nxt=struct.unpack('<II',b)
        nm=modname(nxt)
        if nm and any(x in nm for x in interesting): hits.setdefault(nm,[]).append("ret:0x%08x"%nxt)
        if sav<=ebp: break
        ebp=sav
    esp=c['esp']
    raw=read_mem(esp,0x800)
    if raw:
        cur=None
        for i in range(0,len(raw),4):
            v=struct.unpack_from('<I',raw,i)[0]
            nm=modname(v)
            if nm and any(x in nm for x in interesting):
                hits.setdefault(nm,[]).append("stk+0x%x:0x%08x"%(i,v))
    if hits:
        print("tid=%d eip=0x%08x %s" % (tid,c['eip'],modname(c['eip'])))
        for nm,vs in hits.items():
            print("   %s x%d : %s" % (nm, len(vs), ' '.join(vs[:6])))
