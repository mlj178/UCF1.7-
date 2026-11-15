
import pefile
p=r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\GameAssembly.dll"
pe=pefile.PE(p)
ib=pe.OPTIONAL_HEADER.ImageBase
exp=[]
if hasattr(pe,'DIRECTORY_ENTRY_EXPORT'):
    for e in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if e.address: exp.append((e.address, e.name.decode(errors='replace') if e.name else ''))
exp.sort()
print('exports', len(exp))
for a,n in exp:
    if 0x120000 <= a <= 0x150000:
        print('%08x %s' % (ib+a,n))
print('--- nearest to 0x1290a0 ---')
import bisect
addrs=[a for a,_ in exp]
i=bisect.bisect_left(addrs,0x1290a0)
for j in range(max(0,i-3),min(len(exp),i+3)): print('%08x %s'%(ib+exp[j][0],exp[j][1]))
print('--- nearest to 0x1441f8 ---')
i=bisect.bisect_left(addrs,0x1441f8)
for j in range(max(0,i-3),min(len(exp),i+3)): print('%08x %s'%(ib+exp[j][0],exp[j][1]))
