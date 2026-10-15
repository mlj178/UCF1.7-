
import struct, bisect, sys
path = sys.argv[1]
data = open(path,'rb').read()
sig,ver,nstreams,dirrva,chk,tds,flags = struct.unpack_from('<IIIIIIQ', data, 0)
streams={}
for i in range(nstreams):
    st,dsize,rva = struct.unpack_from('<III', data, dirrva+12*i); streams[st]=(dsize,rva)
def rstr(rva):
    ln=struct.unpack_from('<I',data,rva)[0]; return data[rva+4:rva+4+ln].decode('utf-16-le','replace')
mods=[]
d,r=streams[4]; n=struct.unpack_from('<I',data,r)[0]; off=r+4
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
blob = data[streams[6][1]:streams[6][1]+streams[6][0]]
tid = struct.unpack_from('<I', blob, 0)[0]
code = struct.unpack_from('<I', blob, 8)[0]
eaddr = struct.unpack_from('<Q', blob, 0x18)[0] & 0xffffffff
nparams = struct.unpack_from('<Q', blob, 0x20)[0]
p = [struct.unpack_from('<Q', blob, 0x28+8*i)[0] & 0xffffffff for i in range(min(3, nparams))]
ctxsize, ctxrva = struct.unpack_from('<II', blob, 0xA0)
print("== %s"%path.split('\\')[-1])
print("  tid=%d code=0x%08x addr=0x%08x (%s) params=%s"%(tid, code, eaddr, modname(eaddr), [hex(x) for x in p]))
ebp,eip,cs,efl,esp,ss=struct.unpack_from('<6I',data,ctxrva+0xB4)
print("  eip=0x%08x esp=0x%08x ebp=0x%08x"%(eip,esp,ebp))
st = read_mem(esp, 0x300)
if st:
    out=[]
    for i in range(0,len(st),4):
        v=struct.unpack_from('<I',st,i)[0]
        nm=modname(v)
        if nm and ('GameAssembly' in nm or 'UnityPlayer' in nm or 'ImGui' in nm):
            out.append(nm)
    print("  chain:", " <- ".join(out[:18]))
# also search all threads' contexts for the eip pattern? just report first 3 distinct
print()
