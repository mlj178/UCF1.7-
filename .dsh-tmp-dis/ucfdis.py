
import sys, struct
from capstone import *

DLL = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\GameAssembly.dll"
BASE = 0x10000000
data = open(DLL, "rb").read()
pe = struct.unpack_from("<I", data, 0x3C)[0]
nsec = struct.unpack_from("<H", data, pe + 6)[0]
optsz = struct.unpack_from("<H", data, pe + 20)[0]
opt = pe + 24
secs = []
off = opt + optsz
for i in range(nsec):
    s = off + i * 40
    vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", data, s + 8)
    secs.append((vaddr, vsize, rawsize, rawptr))

def rva2off(rva):
    for va, vsz, rsz, rp in secs:
        if va <= rva < va + max(vsz, rsz):
            return rp + (rva - va)
    return None

def read(rva, size):
    o = rva2off(rva)
    return data[o:o+size] if o is not None else b""

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
REGS = {1:"ecx",2:"edx",3:"ebx",4:"esp",5:"ebp",6:"esi",7:"edi",8:"eax"}

out = []
def emit(s=""):
    out.append(s)

def dis(rva, size, label=""):
    code = read(rva, size)
    emit("=== %s  rva=0x%X size=0x%X ===" % (label, rva, size))
    for ins in md.disasm(code, BASE + rva):
        tgt = ""
        if ins.mnemonic.startswith("j") or ins.mnemonic == "call":
            if ins.operands and ins.operands[0].type == CS_OP_IMM:
                tgt = "  -> rva 0x%X" % (ins.operands[0].imm - BASE)
        mem = ""
        for op in ins.operands:
            if op.type == CS_OP_MEM and op.mem.disp:
                mem += "    ; [%s+0x%X]" % (REGS.get(op.mem.base, "?"), op.mem.disp & 0xFFFFFFFF)
        emit("  0x%08X  %-20s %s %s%s%s" % (ins.address, ins.bytes.hex(), ins.mnemonic, ins.op_str, tgt, mem))
    emit()

what = sys.argv[1]
if what == "move": dis(0x0B2FBE0, 0x4C0, "Bot.Move")
elif what == "ps": dis(0x0B31E90, 0x3B0, "Bot.PathSetting")
elif what == "update": dis(0x0B33370, 0x1C0, "Bot.Update")
elif what == "act": dis(0x0B33070, 0x100, "Bot.UpdateAction")
elif what == "goto": dis(int(sys.argv[2],16), int(sys.argv[3],16), sys.argv[4] if len(sys.argv)>4 else "")

open(r"D:\trae_project\ucf1.7-modifier\.dsh-tmp-dis\out.txt", "w", encoding="utf-8").write("\n".join(out))

