
import re, bisect, sys
p = r"00-游戏逆向分析-相关信息\Il2CppDumper\dump.cs"
rv = []
pat = re.compile(r'// RVA: 0x([0-9A-Fa-f]+) Offset:')
lines = open(p, encoding='utf-8', errors='replace').read().splitlines()
for i, line in enumerate(lines):
    m = pat.search(line)
    if m:
        rva = int(m.group(1), 16)
        # signature is next line
        sig = lines[i+1].strip() if i+1 < len(lines) else ''
        rv.append((rva, i+1, sig[:150]))
rv.sort()
addrs = [0x1290A0,0x1290B1,0x12D0F0,0x1441F8,0x14458A,0x144217]
for a in addrs:
    idx = bisect.bisect_right(rv, (a, 10**9, '')) - 1
    print('=== target %x ===' % a)
    for j in range(max(0, idx-2), min(len(rv), idx+4)):
        print('  rva=%x line=%d %s' % (rv[j][0], rv[j][1], rv[j][2]))
