
import struct, sys, os
path=sys.argv[1]
data=open(path,'rb').read()
sig,ver,nstreams,dir_rva,checksum,tds,flags=struct.unpack_from('<IIIIIIQ',data,0)
streams={}
for i in range(nstreams):
    st,size,rva=struct.unpack_from('<III',data,dir_rva+i*12); streams.setdefault(st,[]).append((size,rva))
size,rva=streams[15][0]
hdr_size,hdr_entry,count=struct.unpack_from('<IIQ',data,rva)
print('meminfo',hdr_size,hdr_entry,count)
entries=[]
off=rva+hdr_size
for i in range(count):
    base,alloc,ap,al1,rsize,state,prot,typ,al2=struct.unpack_from('<QQIIQIIII',data,off); off+=hdr_entry
    entries.append((base,alloc,ap,rsize,state,prot,typ))
entries.sort()
def find(a):
    for e in entries:
        if e[0] <= a < e[0]+e[3]: return e
    return None
for a in [0x10E35B80,0x233e7e00,0x5e8e0000,0x5f718B80,0x10000000,0x9b0000,0x3497a2e0]:
    e=find(a)
    if e:
        print(hex(a),'base',hex(e[0]),'size',hex(e[3]),'allocprot',hex(e[2]),'state',hex(e[4]),'prot',hex(e[5]),'type',hex(e[6]))
    else:
        print(hex(a),'NOT MAPPED')
