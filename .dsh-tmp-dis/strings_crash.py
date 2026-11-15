import pefile
p=r'D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod\ucf_mod.dll.bak_20261115_185346'
pe=pefile.PE(p, fast_load=True)
def rva2off(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData):
            return s.PointerToRawData+(rva-s.VirtualAddress)
data=open(p,'rb').read()
for rva in (0x2ac48,0x2ac58,0x2ac78,0x2ac88,0x2ad14,0x2a418,0x2a428):
    off=rva2off(rva)
    b=data[off:off+64]
    print(hex(rva), b.split(b'\x00')[0])