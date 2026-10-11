
import struct, bisect
path = r"C:\Users\17242\AppData\Local\CrashDumps\UnityCrossFire.exe.8596.dmp"
data=open(path,'rb').read()
sig,ver,nstreams,dirrva,chk,tds,flags=struct.unpack_from('<IIIIIIQ',data,0)
streams={}
for i in range(nstreams):
    st,dsize,rva=struct.unpack_from('<III',data,dirrva+12*i); streams[st]=(dsize,rva)
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
def show(addr,n,label):
    b=read_mem(addr,n)
    if not b: print("%s @0x%08x: NOT CAPTURED"%(label,addr)); return None
    print("%s @0x%08x: %s"%(label,addr,b.hex(' ')))
    return b
print("--- suspected class 0x11370ea0 (Mode_Nano4_Terminator TypeInfo) ---")
b=show(0x11370ea0,0x30,"klass head")
if b:
    print("   [0]=klass? 0x%08x  [0x10]=0x%08x [0x2C]=0x%08x" % (struct.unpack_from('<I',b,0)[0],struct.unpack_from('<I',b,0x10)[0],struct.unpack_from('<I',b,0x2c)[0]))
v=show(0x11370ea0+0x240,0x18,"klass+0x240")
if v:
    for off in range(0,0x18,4):
        print("   klass+0x%x = 0x%08x" % (0x240+off, struct.unpack_from('<I',v,off)[0]))
print()
print("--- instance 0x48a7df00 ---")
show(0x48a7df00,0x80,"instance")
print()
print("--- check candidate class ptrs in module data 0x6cdffab0 region ---")
show(0x6cdffab0-0x20,0x60,"ModuleData-0x20")
print()
print("--- range containing 0x11370ea0 ---")
st,sz,rv=[x for x in ranges if x[0]<=0x11370ea0<x[0]+x[1]][:1][0]
print("  mem range 0x%08x size 0x%x rva 0x%x" % (st,sz,rv))
print("--- range containing 0x48a7df00 ---")
cand=[x for x in ranges if x[0]<=0x48a7df00<x[0]+x[1]][:1]
print("  ", ["0x%08x size 0x%x rva 0x%x"%c for c in cand])
