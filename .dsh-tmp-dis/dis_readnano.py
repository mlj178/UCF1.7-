import pefile, capstone
p=r'D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod\ucf_mod.dll'
pe=pefile.PE(p, fast_load=True)
def rva2off(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData):
            return s.PointerToRawData+(rva-s.VirtualAddress)
data=open(p,'rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
rva=0x93e0; off=rva2off(rva); code=data[off:off+0x320]
for ins in md.disasm(code, 0x10000000+rva):
    print('%08x  %-18s %s %s' % (ins.address, ins.bytes.hex(), ins.mnemonic, ins.op_str))