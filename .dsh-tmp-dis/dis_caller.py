
import pefile, capstone
p=r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\GameAssembly.dll"
pe=pefile.PE(p, fast_load=True)
ib=pe.OPTIONAL_HEADER.ImageBase
def rva2off(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData):
            return s.PointerToRawData+(rva-s.VirtualAddress)
data=open(p,'rb').read()
start=0x10144000; end=0x10144700
off=rva2off(start-ib); code=data[off:off+(end-start)]
md=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
for ins in md.disasm(code, start):
    print('%08x  %-20s %s %s' % (ins.address, ins.bytes.hex(), ins.mnemonic, ins.op_str))
