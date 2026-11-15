import pefile, capstone
p=r'D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod\ucf_mod.dll'
pe=pefile.PE(p, fast_load=True)
print('imagebase',hex(pe.OPTIONAL_HEADER.ImageBase),'sizeofimage',hex(pe.OPTIONAL_HEADER.SizeOfImage))
def rva2off(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData):
            return s.PointerToRawData+(rva-s.VirtualAddress)
data=open(p,'rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
for label,rva,n in [('CALLER1',0x7b00,0x200),('CALLER2',0xaf80,0x200)]:
    print('====',label,hex(rva))
    off=rva2off(rva); code=data[off:off+n]
    for ins in md.disasm(code, pe.OPTIONAL_HEADER.ImageBase+rva):
        print('%08x  %-20s %s %s' % (ins.address, ins.bytes.hex(), ins.mnemonic, ins.op_str))