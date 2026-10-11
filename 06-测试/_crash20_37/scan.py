
import struct
path = r"C:\Users\17242\AppData\Local\CrashDumps\UnityCrossFire.exe.8596.dmp"
data=open(path,'rb').read()
def find(val):
    pat = struct.pack('<I', val)
    out=[]; i=0
    while True:
        i = data.find(pat, i)
        if i<0: break
        out.append(i); i+=1
        if len(out)>200: break
    return out
for val,name in [(0x6c0c5170,'GC fn 0x6c0c5170'),(0x48a7df00,'object 0x48a7df00'),(0x11370ea0,'class 0x11370ea0')]:
    locs = find(val)
    print("%s: %d occurrences in dump file bytes" % (name, len(locs)))
    print("   first offsets:", [hex(x) for x in locs[:20]])
