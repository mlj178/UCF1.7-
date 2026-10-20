import sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

hexstr = sys.argv[1]
base = int(sys.argv[2], 16)
raw = bytes(int(x, 16) for x in hexstr.replace("0x", "").split())
md = Cs(CS_ARCH_X86, CS_MODE_32)
for ins in md.disasm(raw, base):
    print("0x%08x  %-24s %s %s" % (ins.address, ins.bytes.hex(), ins.mnemonic, ins.op_str))
