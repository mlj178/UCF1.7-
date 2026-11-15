import pefile, capstone
p=r'D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod\ucf_mod.dll.bak_20261115_185346'
pe=pefile.PE(p, fast_load=True)
def rva2off(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData):
            return s.PointerToRawData+(rva-s.VirtualAddress)
data=open(p,'rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
ib=pe.OPTIONAL_HEADER.ImageBase
for label,rva,n in [('R7bf5',0x7b80,0x120),('R7bf5b',0x7900,0x300),('Rb0a9',0xafc0,0x180),('Rb0a9b',0xae00,0x300)]:
    print('====',label,hex(rva))
    off=rva2off(rva); code=data[off:off+n]
    for ins in md.disasm(code, ib+rva):
        print('%08x  %-20s %s %s' % (ins.address, ins.bytes.hex(), ins.mnemonic, ins.op_str))