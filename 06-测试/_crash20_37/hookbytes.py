
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
targets={'Bot.Update':0xB33370,'ModeBase.OnStartNewGameRound':0xAF5B30,'ModeBase_Nano.OnStartNewGameRound':0xAF15D0,'GameManager.OnDestroy':0xAFB6F0}
for name,rva in targets.items():
    b=read_mem(GA+rva,16)
    print("%-38s RVA 0x%06x : %s" % (name, rva, b.hex(' ') if b else 'NOT CAPTURED'))
