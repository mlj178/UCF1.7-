# -*- coding: utf-8 -*-
import struct
from capstone import *
from capstone.x86 import *

DLL = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityPlayer.dll"
BASE = 0x10000000
data = open(DLL, "rb").read()
e = struct.unpack_from("<I", data, 0x3C)[0]
machine = struct.unpack_from("<H", data, e+4)[0]
print("PE machine:", hex(machine), "(0x14c=i386, 0x8664=x64)")
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
md.detail = True

def show(va, before=0x60, n=28, label=""):
    print("\n###", label, hex(va))
    base_va = va - before
    off = va2off(base_va)
    code = data[off:off + before + 0x80]
    best = None
    for shift in range(0, 16):
        insns = list(md.disasm(code[shift:], base_va + shift))
        if not insns: continue
        addrs = {i.address for i in insns}
        if va in addrs:
            best = insns
            break
    if not best:
        print("  <no aligned disasm>")
        return
    idx = [i.address for i in best].index(va)
    for i in best[max(0, idx-n): idx+6]:
        print(f"  0x{i.address:08x}  {i.mnemonic:8s} {i.op_str}")

show(0x1024f74a, 0x70, 24, "by-name error site")
show(0x1061d4f8, 0x70, 20, "sharedassets%d site")
show(0x10c07427, 0x70, 24, "level%d site")
show(0x112b81b8 - 0x10000000 + BASE - 0x12b81b8 + 0x1061d951, 0x70, 12, "by-index error site")
