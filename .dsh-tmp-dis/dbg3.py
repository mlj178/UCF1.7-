
import struct, sys
sys.argv=['x']
src = open(r'D:/trae_project/ucf1.7-modifier/.dsh-tmp-dis/rd2.py',encoding='utf-8').read()
exec(src.split("k = sys.argv[1]")[0])
txt = DATA[0x400:0x400+0x195C00]
i = 0x444DC2
print('byte:', hex(txt[i]), 'next4:', txt[i+1:i+5].hex())
rel = struct.unpack_from('<i', txt, i+1)[0]
print('tgt', hex(0x1000+i+5+rel))
# count E8 at even positions? 
print('total e8:', txt.count(b'\xe8'))
n=0
for i in range(len(txt)-5):
    if txt[i]==0xE8:
        t = 0x1000+i+5+struct.unpack_from('<i',txt,i+1)[0]
        if t in (0x4477A0,0x5E67F0): n+=1
print('found', n)
