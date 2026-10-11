
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
GA=0x6bf70000
print("=== call site bytes (GameAssembly+0xb2188d) ===")
b=read_mem(GA+0xb2188d, 0x20)
print(b.hex(' ') if b else "not captured")
print("=== ModeBase_Nano_TypeInfo? 0x6cdffab0 ===")
b2=read_mem(0x6cdffab0, 0x40)
print(b2.hex(' ') if b2 else "not captured")
print("=== 0x6cdffab0 + 0x244 ===")
b3=read_mem(0x6cdffab0+0x244, 16)
print(b3.hex(' ') if b3 else "not captured")
if b3:
    print("  value at +0x244 = 0x%08x   at +0x248 = 0x%08x" % (struct.unpack_from('<I',b3,0)[0], struct.unpack_from('<I',b3,4)[0]))
print("=== heap obj 0x48a7df00 ===")
b4=read_mem(0x48a7df00, 64)
print(b4.hex(' ') if b4 else "not captured")
print("=== heap obj 0x4939b240 (arg) ===")
b5=read_mem(0x4939b240, 0x40)
print(b5.hex(' ') if b5 else "not captured")
# also check what other candidate: instance returned by get_instance2 static
print("=== ModeBase_Nano static il2cpp? xref: read data at several ===")
for a in [0x6cddb8e0, 0x6caf0980, 0x6c0c54ef, 0x6c0c546e]:
    bb=read_mem(a,16)
    print(" 0x%08x: %s" % (a, bb.hex(' ') if bb else 'not captured'))
