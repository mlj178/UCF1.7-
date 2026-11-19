
# -*- coding: utf-8 -*-
"""Minimal RVA disassembler / xref tool for GameAssembly.dll (x86 32-bit)."""
import re, struct, sys, bisect
from capstone import *

GAME = r'D:/BaiduNetdiskDownload/UnityCrossFire1.7.1/UnityCrossFire1.7.1'
DLL = GAME + '/GameAssembly.dll'
DUMP = r'D:/trae_project/ucf1.7-modifier/00-游戏逆向分析-相关信息/Il2CppDumper/dump.cs'

def sections(path):
    data = open(path,'rb').read()
    pe = struct.unpack_from('<I', data, 0x3C)[0]
    nsec = struct.unpack_from('<H', data, pe+6)[0]
    optsz = struct.unpack_from('<H', data, pe+20)[0]
    sec0 = pe+24+optsz
    out=[]
    for i in range(nsec):
        off = sec0+i*40
        name = data[off:off+8].rstrip(b'\x00').decode('latin-1')
        vsize,vaddr,rawsize,rawptr = struct.unpack_from('<IIII', data, off+8)
        out.append((name,vaddr,vsize,rawptr,rawsize))
    return data,out

DATA, SECS = sections(DLL)

def read_rva(rva, n):
    for name,vaddr,vsize,rawptr,rawsize in SECS:
        if vaddr <= rva < vaddr+max(vsize,rawsize):
            d = rva-vaddr
            if d >= rawsize: return b''
            return DATA[rawptr+d: rawptr+d+n]
    return b''

SYM={}; cur='?'; pending=None
cls_hdr = re.compile(r'class\s+([A-Za-z0-9_.<>@]+)')
rva_re = re.compile(r'// RVA: 0x([0-9A-Fa-f]+) Offset')
meth_re = re.compile(r'^\t[^/].*?\b([A-Za-z0-9_<>.]+)\((.*)\)\s*\{\s*\}\s*$')
for line in open(DUMP,'r',encoding='utf-8',errors='ignore'):
    if 'TypeDefIndex' in line:
        m = cls_hdr.search(line)
        if m: cur = m.group(1)
    m = rva_re.search(line)
    if m:
        pending = int(m.group(1),16); SYM.setdefault(pending, cur); continue
    if pending is not None:
        m = meth_re.match(line)
        if m: SYM[pending] = cur+'::'+m.group(1)
        pending=None

KEYS = sorted(SYM)
def nm(t): return SYM.get(t,'')
def owner(a):
    p = bisect.bisect_right(KEYS, a)-1
    if p < 0: return '?'
    k = KEYS[p]
    return SYM[k] if a-k < 0x5000 else '?@0x%X' % k

md = Cs(CS_ARCH_X86, CS_MODE_32)

def dis(rva, maxbytes=0x600, maxins=400, title=''):
    print('\n===== %s  RVA 0x%X =====' % (title or nm(rva), rva))
    buf = read_rva(rva, maxbytes); n=0
    for ins in md.disasm(buf, rva):
        n+=1; ann=''
        if ins.mnemonic in ('call','jmp') and ins.op_str.startswith('0x'):
            try:
                s = nm(int(ins.op_str,16))
                if s: ann='   ; '+s
            except Exception: pass
        print('%08X  %-32s%s' % (ins.address, ins.mnemonic+' '+ins.op_str, ann))
        if n>=maxins: break
        if ins.mnemonic=='ret':
            nb = read_rva(ins.address+ins.size, 2)
            if nb[:1] in (b'\xcc', b'\x90', b'\xc3', b''): break

def xref(*targets, maxshow=40):
    hits = {t: [] for t in targets}
    for name,vaddr,vsize,rawptr,rawsize in SECS:
        buf = DATA[rawptr:rawptr+rawsize]
        for i in range(len(buf)-5):
            if buf[i] != 0xE8: continue
            tgt = vaddr + i + 5 + struct.unpack_from('<i', buf, i+1)[0]
            if tgt in hits: hits[tgt].append(vaddr+i)
    for t in targets:
        seen={}
        for a in hits[t]: seen[owner(a)] = seen.get(owner(a),0)+1
        print('\n### xrefs -> 0x%X (%s): %d' % (t, nm(t), len(hits[t])))
        for o,c in sorted(seen.items(), key=lambda x:-x[1])[:maxshow]:
            print('   %-62s x%d' % (o,c))

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'd':
        for a in sys.argv[2:]:
            dis(int(a,0))
    elif cmd == 'x':
        xref(*[int(a,0) for a in sys.argv[2:]])
