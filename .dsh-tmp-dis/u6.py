
import base64, io, zipfile
p = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data\\level1"
data = open(p,"rb").read()
i = data.find(b"UEsDBBQ")
e = i
while e < len(data) and (data[e:e+1].isalnum() or data[e:e+1] in b"+/="): e += 1
b64 = data[i:e]
raw = base64.b64decode(b64 + b"="*((4-len(b64)%4)%4))
z = zipfile.ZipFile(io.BytesIO(raw))
for n in z.namelist():
    print("=====", n)
    print(z.read(n).decode("utf-8", "replace"))
