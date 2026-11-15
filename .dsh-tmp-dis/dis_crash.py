
import struct, pefile, capstone
p = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\GameAssembly.dll"
pe = pefile.PE(p, fast_load=True)
ib = pe.OPTIONAL_HEADER.ImageBase
def rva2off(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            return s.PointerToRawData + (rva - s.VirtualAddress)
    return None
data = open(p,'rb').read()
base_rva = 0x1290a0
off = rva2off(base_rva)
code = data[off:off+256]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = False
for ins in md.disasm(code, ib + base_rva):
    marker = ' <== CRASH' if ins.address == ib + 0x1290b1 else ''
    print('%08x  %-24s %s %s%s' % (ins.address, ins.bytes.hex(), ins.mnemonic, ins.op_str, marker))
