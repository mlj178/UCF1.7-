
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
def off2addr(off):
    for st,sz,rv in ranges:
        if rv <= off < rv+sz:
            return st + (off-rv), (st,sz,rv)
    return None, None
for off in [0x680806,0x848677]:
    a,rng = off2addr(off)
    print("file off 0x%x -> addr %s range %s" % (off, hex(a) if a else None, ["0x%08x/0x%x/0x%x"%rng] if rng else None))
    if a:
        print("   context:", data[off-16:off+16].hex(' '))
        ga = a - 0x6bf70000
        print("   GameAssembly RVA: 0x%x" % ga)
