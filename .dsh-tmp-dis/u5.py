
import os, re, base64, io, zipfile, json
base = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data"
files = [f for f in os.listdir(base) if os.path.isfile(os.path.join(base,f))]
files.sort()
pat = re.compile(rb"[A-Za-z0-9+/]{200,}={0,2}")
for f in files:
    p = os.path.join(base,f)
    sz = os.path.getsize(p)
    if sz <= 1_000_000 and not f.startswith("level"): continue
    data = open(p,"rb").read()
    for m in re.finditer(rb"UEsDBBQ", data):
        start = m.start()
        e = start
        while e < len(data) and (data[e:e+1].isalnum() or data[e:e+1] in b"+/="):
            e += 1
        b64 = data[start:e]
        try:
            raw = base64.b64decode(b64 + b"="*((4-len(b64)%4)%4))
            z = zipfile.ZipFile(io.BytesIO(raw))
            names = z.namelist()
            info = [(n, z.getinfo(n).file_size) for n in names]
            print(f"{f} @{start} b64={len(b64)} zip={len(raw)} entries={info}")
        except Exception as ex:
            print(f"{f} @{start} b64={len(b64)} FAIL {type(ex).__name__} {str(ex)[:80]}")
