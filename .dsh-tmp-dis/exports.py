
import pefile
p=r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\GameAssembly.dll"
pe=pefile.PE(p, fast_load=True)
ib=pe.OPTIONAL_HEADER.ImageBase
exp=[]
if hasattr(pe,'DIRECTORY_ENTRY_EXPORT'):
    for e in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if e.address: exp.append((e.address, e.name.decode(errors='replace') if e.name else ''))
exp.sort()
print('exports', len(exp))
for a,n in exp:
    if 0x120000 <= a <= 0x14a000:
        print('%08x %s' % (ib+a,n))
