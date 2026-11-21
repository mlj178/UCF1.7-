# -*- coding: utf-8 -*-
import struct
from capstone import *

DLL = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityPlayer.dll"
IMAGE_BASE = 0x10000000
TARGETS = {
    0x121474: "level%d",
    0x12b83e8: "sharedassets%d.assets",
    0x121f570: "err:by-name",
    0x12b81b8: "err:by-index",
    0x12c26d8: "err:invalid-index",
}

data = open(DLL, "rb").read()
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
nsec = struct.unpack_from("<H", data, e_lfanew + 6)[0]
opt_size = struct.unpack_from("<H", data, e_lfanew + 20)[0]
sec_off = e_lfanew + 24 + opt_size
secs = []
for i in range(nsec):
    o = sec_off + i * 40
    name = data[o:o+8].rstrip(b"\x00").decode("latin1")
    vsize, va, rawsize, rawptr = struct.unpack_from("<IIII", data, o + 8)
    secs.append((name, va, vsize, rawptr, rawsize))
    print(f"sec {name:8s} va=0x{va:08x} vsize=0x{vsize:x} raw=0x{rawptr:x}")

def rva_from_va(va): return va - IMAGE_BASE

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = False
hits = []
for (name, va, vsize, rawptr, rawsize) in secs:
    if not (name == ".text"): continue
    code = data[rawptr:rawptr+vsize]
    start = IMAGE_BASE + va
    for insn in md.disasm(code, start):
        op = insn.op_str
        if "rip" in op and insn.mnemonic in ("lea", "mov"):
            try:
                disp = int(op.split("+")[-1].split("]")[0].strip(), 0)
            except Exception:
                continue
            tgt = insn.address + insn.size + disp - IMAGE_BASE
            if tgt in TARGETS:
                hits.append((insn.address, TARGETS[tgt]))
for a, t in sorted(hits):
    print(f"XREF 0x{a:x} -> {t}")
print("total hits", len(hits))
