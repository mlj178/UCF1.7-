import pefile, capstone, glob, os
paths=glob.glob(r'D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod\ucf_mod.dll*')
for p in sorted(paths, key=os.path.getmtime):
    try:
        pe=pefile.PE(p, fast_load=True)
        print('%-70s %8d szimg=%x base=%x' % (os.path.basename(p), os.path.getsize(p), pe.OPTIONAL_HEADER.SizeOfImage, pe.OPTIONAL_HEADER.ImageBase))
    except Exception as e:
        print(p, e)