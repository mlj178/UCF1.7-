
import struct, sys
sys.argv=['x']
src = open(r'D:/trae_project/ucf1.7-modifier/.dsh-tmp-dis/rd2.py',encoding='utf-8').read()
base = src.split("k = sys.argv[1]")[0]
exec(base)
targets=[0x5E67F0,0x4477A0]
hits={t:0 for t in targets}
for name,vaddr,vsize,rawptr,rawsize in SECS:
    if name != '.text': continue
    buf = DATA[rawptr:rawptr+rawsize]
    for i in range(len(buf)-5):
        if buf[i] != 0xE8: continue
        tgt = vaddr + i + 5 + struct.unpack_from('<i', buf, i+1)[0]
        if tgt in hits: hits[tgt]+=1
print('section name test:', repr(name), 'hits:', hits)
print('tail of rd2.py:')
print('\n'.join(src.splitlines()[-12:]))
