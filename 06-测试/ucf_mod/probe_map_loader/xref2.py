# -*- coding: utf-8 -*-
import struct
from capstone import *
from capstone.x86 import *

DLL = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityPlayer.dll"
IMAGE_BASE = 0x10000000
TARGETS = {
    0x11341474: "level%d",
    0x112b83e8: "sharedassets%d.assets",
    0x1121f570: "err:by-name",
    0x112b81b8: "err:by-index",
    0x112c26d8: "err:invalid-index",
}
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

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
md.skipdata = True
hits = []
for nm, va, vs, rp, rs in secs:
    if nm != ".text": continue
    code = data[rp:rp+vs]
    start = IMAGE_BASE + va
    n = 0
    for insn in md.disasm(code, start):
        n += 1
        if insn.mnemonic not in ("lea", "mov"): continue
        if len(insn.operands) < 2: continue
        m = insn.operands[1]
        if m.type != X86_OP_MEM or m.mem.base != X86_REG_RIP: continue
        t = insn.address + insn.size + m.mem.disp
        if t in TARGETS:
            hits.append((insn.address, TARGETS[t]))
    print("decoded insns in", nm, n)
for a, t in sorted(hits):
    print(f"XREF 0x{a:x} -> {t}")
print("total", len(hits))
