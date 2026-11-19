
import struct, sys
sys.argv=['x']
exec(open(r'D:/trae_project/ucf1.7-modifier/.dsh-tmp-dis/rd2.py',encoding='utf-8').read().split("k = sys.argv[1]")[0])
print('sections:')
for name,vaddr,vsize,rawptr,rawsize in SECS:
    print('  %-10s vaddr=0x%X vsize=0x%X raw=0x%X rawsize=0x%X' % (name,vaddr,vsize,rawptr,rawsize))
b = read_rva(0x445DC2, 8)
print('bytes at 0x445DC2:', ' '.join('%02x'%x for x in b))
rel = struct.unpack_from('<i', b, 1)[0]
print('target = 0x%X' % (0x445DC2+5+rel))
# brute: count E8 in .text
for name,vaddr,vsize,rawptr,rawsize in SECS:
    if name=='.text':
        buf = DATA[rawptr:rawptr+rawsize]
        print('E8 count in .text:', buf.count(b'\xe8'), 'len', len(buf))
