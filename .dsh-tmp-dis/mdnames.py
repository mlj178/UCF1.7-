
import struct, sys
path=sys.argv[1]
data=open(path,'rb').read()
sig,ver,nstreams,dir_rva,checksum,tds,flags=struct.unpack_from('<IIIIIIQ',data,0)
streams={}
for i in range(nstreams):
    st,size,rva=struct.unpack_from('<III',data,dir_rva+i*12); streams.setdefault(st,[]).append((size,rva))
size,rva=streams[24][0]
n=struct.unpack_from('<I',data,rva)[0]
print('thread names',n)
names={}
for i in range(n):
    tid,nrva=struct.unpack_from('<II',data,rva+4+i*8)
    ln=struct.unpack_from('<I',data,nrva)[0]
    s=data[nrva+4:nrva+4+ln].decode('utf-16-le','replace')
    names[tid]=s
for tid,s in names.items(): print(tid,s)
