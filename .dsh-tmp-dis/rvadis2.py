
# -*- coding: utf-8 -*-
import re, struct
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

SYM={}
cur='?'
pending=None
cls_hdr = re.compile(r'class\s+([A-Za-z0-9_.<>@]+)')
rva_re = re.compile(r'// RVA: 0x([0-9A-Fa-f]+) Offset')
meth_re = re.compile(r'^\t[^/].*?\b([A-Za-z0-9_<>.]+)\((.*)\)\s*\{\s*\}\s*$')
for line in open(DUMP,'r',encoding='utf-8',errors='ignore'):
    if 'TypeDefIndex' in line:
        m = cls_hdr.search(line)
        if m: cur = m.group(1)
    m = rva_re.search(line)
    if m:
        pending = int(m.group(1),16); SYM.setdefault(pending, cur)
        continue
    if pending is not None:
        m = meth_re.match(line)
        if m:
            SYM[pending] = cur+'::'+m.group(1)
        pending=None

md = Cs(CS_ARCH_X86, CS_MODE_64)
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
        print('%08X  %-30s%s' % (ins.address, ins.mnemonic+' '+ins.op_str, ann))
        if n>=maxins: break
        if ins.mnemonic=='ret':
            nb = read_rva(ins.address+ins.size, 4)
            if nb[:1] in (b'\xcc', b'\x90', b'', None) or nb[:1]==b'\xc3': break

import sys
which = sys.argv[1] if len(sys.argv)>1 else 'awake'
if which=='awake': dis(0x445BE0, 0x600, 300, 'AstarPath.Awake')
elif which=='initpp': dis(0x4477A0, 0x500, 260, 'AstarPath.InitializePathProcessor')
elif which=='ph': dis(0x5E6990, 0x200, 90, 'PathHandler..ctor')
elif which=='pp': dis(0x5E99E0, 0x400, 200, 'PathProcessor..ctor')
elif which=='scan': dis(0x448B90, 0x300, 160, 'AstarPath.Scan(NavGraph[])')
elif which=='scan1': dis(0x448DF0, 0x180, 90, 'AstarPath.Scan(NavGraph)')
elif which=='pginit': dis(0x5F0440, 0x120, 60, 'PointGraph.ScanInternal')
elif which=='addkids': dis(0x5EE510, 0x340, 160, 'PointGraph.AddChildren')
elif which=='countkids': dis(0x5EE9E0, 0x140, 70, 'PointGraph.CountChildren')
elif which=='conn': dis(0x5EE8E0, 0x200, 100, 'PointGraph.ConnectNodes')
