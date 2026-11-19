
# -*- coding: utf-8 -*-
import re, struct, sys
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

md = Cs(CS_ARCH_X86, CS_MODE_32)
def nm(t): return SYM.get(t,'')

def dis(rva, maxbytes=0x600, maxins=400, title=''):
    print('\n===== %s  RVA 0x%X =====' % (title, rva))
    buf = read_rva(rva, maxbytes); n=0
    for ins in md.disasm(buf, rva):
        n+=1; ann=''
        if ins.mnemonic in ('call','jmp') and ins.op_str.startswith('0x'):
            try:
                t=int(ins.op_str,16); s=nm(t)
                if s: ann='   ; '+s
            except Exception: pass
        print('%08X  %-32s%s' % (ins.address, ins.mnemonic+' '+ins.op_str, ann))
        if n>=maxins: break
        if ins.mnemonic=='ret':
            nb = read_rva(ins.address+ins.size, 2)
            if nb[:1] in (b'\xcc', b'\x90', b'\xc3', b''): break

W={'awake':(0x445BE0,0x500,300,'AstarPath.Awake'),
 'initpp':(0x4477A0,0x400,200,'AstarPath.InitializePathProcessor'),
 'ph':(0x5E6990,0x120,60,'PathHandler..ctor'),
 'pp':(0x5E99E0,0x300,160,'PathProcessor..ctor'),
 'scanarr':(0x448B90,0x260,130,'AstarPath.Scan(NavGraph[])'),
 'scan1':(0x448DF0,0x140,70,'AstarPath.Scan(NavGraph)'),
 'pgscan':(0x5F0440,0x100,50,'PointGraph.ScanInternal'),
 'count':(0x5EE9E0,0x120,60,'PointGraph.CountChildren'),
 'addkids':(0x5EE510,0x340,150,'PointGraph.AddChildren'),
 'addnode':(0x5EE7D0,0x140,70,'PointGraph.AddNode'),
 'ctor_pn':(0x0,0,0,''),
}
k = sys.argv[1]
a = W[k]
dis(a[0], a[1], a[2], a[3])

    # ---- xref scan ----
    if k == 'xref':
        targets = [int(x,0) for x in sys.argv[2:]]
        tset = {t: nm(t) for t in targets}
        hits = {t: [] for t in targets}
        # .text section
        for name,vaddr,vsize,rawptr,rawsize in SECS:
            if name != '.text': continue
            buf = DATA[rawptr: rawptr+rawsize]
            for i in range(len(buf)-5):
                if buf[i] != 0xE8: continue
                rel = struct.unpack_from('<i', buf, i+1)[0]
                tgt = vaddr + i + 5 + rel
                if tgt in hits:
                    hits[tgt].append(vaddr + i)
        # map addr -> enclosing symbol
        syms = sorted(SYM.items())
        import bisect
        keys = [s[0] for s in syms]
        def owner(a):
            p = bisect.bisect_right(keys, a) - 1
            if p < 0: return '?'
            k2 = keys[p]
            # allow up to 0x4000 bytes to count as inside
            if a - k2 < 0x4000: return SYM[k2]
            return '?@0x%X' % k2
        for t in targets:
            print('\n### xrefs to 0x%X (%s): %d' % (t, tset[t], len(hits[t])))
            seen = {}
            for a in hits[t]:
                o = owner(a)
                seen[o] = seen.get(o,0)+1
            for o,c in sorted(seen.items(), key=lambda x:-x[1])[:40]:
                print('   %-60s x%d' % (o, c))
        sys.exit(0)
