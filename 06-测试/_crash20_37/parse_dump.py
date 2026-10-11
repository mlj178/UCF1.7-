
import struct, sys, os

path = r"C:\Users\17242\AppData\Local\CrashDumps\UnityCrossFire.exe.8596.dmp"
data = open(path,'rb').read()
print("size", len(data))
assert data[:4]==b'MDMP', data[:4]
sig, ver, nstreams, dirrva, chk, tds, flags = struct.unpack_from('<IIIIIIQ', data, 0)
print("version %x streams %d dirrva %x flags %x" % (ver, nstreams, dirrva, flags))

streams={}
for i in range(nstreams):
    st, dsize, rva = struct.unpack_from('<III', data, dirrva+12*i)
    streams[st]=(dsize,rva)
    print("stream type %d size %d rva %x" % (st, dsize, rva))

def rstr(rva):
    ln = struct.unpack_from('<I', data, rva)[0]
    return data[rva+4:rva+4+ln].decode('utf-16-le', 'replace')

# System info
if 7 in streams:
    d,r = streams[7]
    arch, lvl, rev, ncpu, ptype, major, minor, build, platid = struct.unpack_from('<HHHBBIIII', data, r)
    print("SystemInfo arch=%d (0=x86,9=x64,5=arm) cpus=%d platid=%d" % (arch, ncpu, platid))

# Modules
mods=[]
if 4 in streams:
    d,r = streams[4]
    n = struct.unpack_from('<I', data, r)[0]
    off = r+4
    for i in range(n):
        base, size, csum, tds2, namerva = struct.unpack_from('<QIIII', data, off)
        mods.append((base & 0xffffffff, size, rstr(namerva)))
        off += 108  # 8+4+4+4+4 + 10*4 version + 8 cv + 8 misc + 8 + 8 = 108
    print("modules", n)
    for b,s,nm in mods:
        if any(k in nm.lower() for k in ['gameassembly','frida','universal','unityplayer','kernelbase','ntdll','win32u','d3d11','igd']):
            print("  %08x-%08x %s" % (b, b+s, nm))
