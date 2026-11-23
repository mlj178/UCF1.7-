# -*- coding: utf-8 -*-
import struct
from capstone import *

DLL = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityPlayer.dll"
BASE = 0x10000000
data = open(DLL, "rb").read()
e = struct.unpack_from("<I", data, 0x3C)[0]
nsec = struct.unpack_from("<H", data, e+6)[0]
opt = struct.unpack_from("<H", data, e+20)[0]
so = e + 24 + opt
secs = []
for i in range(nsec):
    o = so + i*40
    nm = data[o:o+8].rstrip(b"\x00").decode("latin1")
    vs, va, rs, rp = struct.unpack_from("<IIII", data, o+8)
    secs.append((nm, va, vs, rp, rs))
def va2off(va):
    rva = va - BASE
    for nm, sva, svs, rp, rs in secs:
        if sva <= rva < sva + max(svs, rs):
            return rp + (rva - sva)
    return None
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = False

def dump(va, label, maxn=70):
    # find int3 padding before va -> function start
    off = va2off(va)
    start_off = off
    back = 0
    while back < 0x400:
        if data[start_off-1] == 0xCC and data[start_off-2] == 0xCC:
            break
        start_off -= 1; back += 1
    start_va = va - back
    code = data[start_off:start_off + 0x600]
    print(f"\n===== {label}  func_start=0x{start_va:08x} =====")
    n = 0
    for insn in md.disasm(code, start_va):
        mark = "  <<<" if insn.address <= va < insn.address + insn.size else ""
        print(f"0x{insn.address:08x}  {insn.mnemonic:8s} {insn.op_str}{mark}")
        n += 1
        if n >= maxn: break

dump(0x1024f74a, "by-name error")
dump(0x1061d951, "by-index error + sharedassets", 80)
dump(0x10c07427, "level%d builder", 80)
