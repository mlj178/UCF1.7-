# -*- coding: utf-8 -*-
"""dump_stack.py —— 读 Unity crash.dmp，把崩溃线程栈上的 ucf_mod 帧还原成函数名。

用法：python dump_stack.py <crash.dmp> [--dll <ucf_mod.dll>]
（只依赖标准库 + mingw 的 nm.exe；没有 nm 就只给模块+偏移）
"""
import os, struct, subprocess, sys

NM = r"D:/Program Files/mingw32/bin/nm.exe"
DEFAULT_DLL = r"D:/BaiduNetdiskDownload/UnityCrossFire1.7.1/UnityCrossFire1.7.1/ucf_mod/ucf_mod.dll"

def parse(path):
    d = open(path, "rb").read()
    sig, ver, ns, rva = struct.unpack_from("<IIII", d, 0)
    st = {}
    for i in range(ns):
        k, size, r = struct.unpack_from("<III", d, rva + i * 12)
        st[k] = (size, r)
    mods = []
    size, r = st[4]
    n = struct.unpack_from("<I", d, r)[0]
    for i in range(n):
        off = r + 4 + i * 108
        base, nbytes, chk, ts, namerva = struct.unpack_from("<QIIII", d, off)
        mlen = struct.unpack_from("<I", d, namerva)[0]
        name = d[namerva + 4: namerva + 4 + mlen].decode("utf-16-le", "replace")
        mods.append((name, base, nbytes))
    tid, code_, addr = 0, 0, 0
    if 6 in st:
        size, r = st[6]
        tid = struct.unpack_from("<I", d, r)[0]
        code_ = struct.unpack_from("<I", d, r + 8)[0]
        addr = struct.unpack_from("<Q", d, r + 24)[0]
    threads = []
    size, r = st[3]
    nt = struct.unpack_from("<I", d, r)[0]
    for i in range(nt):
        off = r + 4 + i * 48
        t_i = struct.unpack_from("<I", d, off)[0]
        s_start, s_size, s_rva = struct.unpack_from("<QII", d, off + 24)
        c_size, c_rva = struct.unpack_from("<II", d, off + 40)
        threads.append((t_i, s_start, s_size, s_rva, c_size, c_rva))
    return d, mods, (tid, code_, addr), threads

def main():
    dmp = sys.argv[1]
    dll = DEFAULT_DLL
    if "--dll" in sys.argv:
        dll = sys.argv[sys.argv.index("--dll") + 1]
    d, mods, (tid, code_, addr), threads = parse(dmp)

    def where(a):
        for nm, b, sz in mods:
            if b <= a < b + sz:
                return nm.split("\\")[-1], a - b
        return None, 0

    fn, off = where(addr)
    print("dump     : %s" % os.path.basename(os.path.dirname(dmp)))
    print("faulting : %s+0x%x   code=0x%08x   tid=%d" % (fn, off, code_, tid))
    ucf = [m for m in mods if "ucf" in m[0].lower()]
    if not ucf:
        print("!! 模块表里没有 ucf_mod")
        return
    base, size = ucf[0][1], ucf[0][2]
    t = [x for x in threads if x[0] == tid]
    if not t:
        print("!! 找不到崩溃线程")
        return
    _, s_start, s_size, s_rva, c_size, c_rva = t[0]
    stack = d[s_rva: s_rva + s_size]
    seen = []
    for o in range(0, len(stack) - 4, 4):
        a = struct.unpack_from("<I", stack, o)[0]
        if base <= a < base + size and (a - base) not in [x[1] for x in seen]:
            seen.append((o, a - base))

    syms = []
    ib = None
    try:
        out = subprocess.run([DLL_OD, "-p", dll], capture_output=True, text=True, errors="replace").stdout
        for line in out.splitlines():
            if "ImageBase" in line:
                ib = int(line.split()[-1], 16)
                break
    except Exception:
        pass
    if ib is not None:
        nm = subprocess.run([NM, "-n", "-S", "--defined-only", dll],
                            capture_output=True, text=True, errors="replace").stdout
        for line in nm.splitlines():
            p = line.split()
            if len(p) == 4 and p[2] in ("T", "t", "W", "w"):
                try:
                    syms.append((int(p[0], 16) - ib, int(p[1], 16), p[3]))
                except ValueError:
                    pass
            elif len(p) == 3 and p[1] in ("T", "t", "W", "w"):
                try:
                    syms.append((int(p[0], 16) - ib, 0, p[2]))
                except ValueError:
                    pass
        syms.sort()

    def sym(rva):
        best = None
        for a, sz, nm in syms:
            if a <= rva < a + max(sz, 1):
                return nm, rva - a
            if a <= rva:
                best = (nm, rva - a)
        return best or ("?", rva)

    print("ucf_mod 栈帧（按栈位置，越靠前越接近崩溃点）：")
    for o, r in seen[:26]:
        nmn, delta = sym(r)
        print("  +0x%04x  %-34s +0x%x" % (o, nmn, delta))

DLL_OD = r"D:/Program Files/mingw32/bin/objdump.exe"
if __name__ == "__main__":
    main()
