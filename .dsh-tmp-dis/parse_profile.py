
import re, json, sys
text=open(r'04-正式发行版/全功能整合包2.7/game_modifier/features/35_room_player_count/script.js',encoding='utf-8').read()
m=re.search(r"var BASE_30_TO_V3_PROFILE = \[(.*?)\n  \];", text, re.S)
body=m.group(1)
entries=re.findall(r"\[0x([0-9A-Fa-f]+), '([^']*)', '([^']*)'\]", body)
print('entries',len(entries))
for rva, base, v3 in entries:
    rva=int(rva,16)
    print('==== RVA 0x%X base_len=%d v3_len=%d' % (rva, len(base.split()), len(v3.split())))
    b=bytes(int(x,16) for x in v3.split())
    i=0
    while i < len(b):
        op=b[i]
        if op in (0xE8,0xE9) and i+4 < len(b):
            rel=int.from_bytes(b[i+1:i+5],'little',signed=True)
            print('  0x%X: %s rel=%d -> 0x%X' % (rva+i, 'call' if op==0xE8 else 'jmp', rel, rva+i+5+rel))
            i+=5; continue
        if op in (0x74,0x75,0x7C,0x7D,0xEB) and i+1 < len(b):
            rel=int.from_bytes(b[i+1:i+2],'little',signed=True)
            print('  0x%X: jcc %02X rel=%d -> 0x%X' % (rva+i, op, rel, rva+i+2+rel))
            i+=2; continue
        if op==0x0F and i+1<len(b) and 0x80<=b[i+1]<=0x8F and i+5<len(b):
            rel=int.from_bytes(b[i+2:i+6],'little',signed=True)
            print('  0x%X: jcc0F %02X rel=%d -> 0x%X' % (rva+i, b[i+1], rel, rva+i+6+rel))
            i+=6; continue
        i+=1
