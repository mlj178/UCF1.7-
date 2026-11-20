
import sys
sys.path.insert(0, r'D:/trae_project/ucf1.7-modifier/.dsh-tmp-dis')
import tool as T
code = T.read_rva(0xB31E90, 0x3C0)
insns = list(T.md.disasm(code, 0x10B31E90))
out = []
for i in insns:
    s, op = i.mnemonic, i.op_str
    tgt = ''
    if s.startswith('call') and op.startswith('0x'):
        try: tgt = T.owner(int(op, 16)) or ''
        except Exception: pass
    out.append((i.address, s, op, tgt))
print('n=', len(out))
for a, s, op, tgt in out:
    if ('0xb8' in op and ('[e' in op)) or s.startswith('call') or '0xc0' in op and '[' in op:
        print('%08x  %-20s %-26s %s' % (a, s, op, tgt))
