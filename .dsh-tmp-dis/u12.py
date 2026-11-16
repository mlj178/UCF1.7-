
import base64, io, zipfile, os, re
base = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data"
data = open(os.path.join(base,"level1"),"rb").read()
idxs = [m.start() for m in re.finditer(rb"UEsDBBQ", data)]
print("occurrences:", idxs)
i = idxs[0]
e = i
while e < len(data) and (data[e:e+1].isalnum() or data[e:e+1] in b"+/="): e += 1
b64 = data[i:e]
print("len b64", len(b64), "pad", (4-len(b64)%4)%4)
raw = base64.b64decode(b64 + b"="*((4-len(b64)%4)%4))
z = zipfile.ZipFile(io.BytesIO(raw))
m = z.read("meta.json")
print(repr(m))
